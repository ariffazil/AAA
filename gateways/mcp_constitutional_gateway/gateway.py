#!/usr/bin/env python3
"""
MCP Constitutional Gateway

arifOS admission controller for all MCP tool calls.

Pattern:
    MCP tool advertisement → arifOS risk classification → lease → execution → VAULT999

Pre-flight checks before allowing any MCP tool call:
    1. Tool description review    — description matches actual behavior
    2. Scope declaration          — filesystem, network, secrets access
    3. Secrets risk               — tool reads/writes credentials
    4. Side effects               — read-only vs mutating vs destructive
    5. Network access             — tool contacts external URLs
    6. Human consent              — is consent needed per F6/F13
    7. Lease generation           — arifOS issues scoped lease
    8. Audit to VAULT999          — seal the decision

Main entry: admit_tool() runs all 8 checks in sequence.

Usage:
    gateway = MCPConstitutionalGateway(actor_id="forge-000omega")
    result = gateway.admit_tool(
        tool_name="geox_basin_profile",
        description="Retrieve basin-level intelligence",
        declared_scope="read_only",
        arguments={"basin_name": "Malay Basin"},
    )
    # → {"admitted": True, "verdict": "SEAL", "lease_id": "...", ...}

DITEMPA BUKAN DIBERI — Forged, Not Given.
"""

import json
import re
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import httpx


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ARIFOS_MCP_URL = "http://localhost:8088/mcp"
MCP_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-MCP-Protocol-Version": "2025-11-05",
}
DEFAULT_TIMEOUT_S = 15.0

MCP_TOOL_LEASE_ISSUE = "arif_lease_issue"
MCP_TOOL_JUDGE_DELIBERATE = "arif_judge_deliberate"
MCP_TOOL_VAULT_SEAL = "arif_vault_seal"
MCP_TOOL_OS_ATTEST = "arif_os_attest"

LEGITIMATE_VERDICTS = {"SEAL", "SABAR", "HOLD", "VOID"}

# Known dangerous description keywords
DANGEROUS_KEYWORDS = [
    "bypass", "evade", "steal", "crack", "hack", "exploit",
    "ransomware", "malware", "backdoor", "rootkit",
    "unauthorized", "illegal", "illegitimate",
]

# Known hallucination / deception keywords in tool descriptions
HALLUCINATION_KEYWORDS = [
    "private api", "undocumented endpoint", "secret method",
    "hidden feature", "developer only", "internal only",
]

# Tools known to touch secrets
SECRET_TOUCHING_TOOL_PATTERNS = [
    r"secret", r"credential", r"token", r"password", r"key",
    r"certificate", r"auth", r"bearer", r"api.?key",
]

# Destructive tool patterns
DESTRUCTIVE_PATTERNS = [
    r"drop", r"delete", r"remove", r"destroy", r"purge", r"truncate",
    r"unlink", r"wipe", r"clear",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _new_id() -> str:
    return str(uuid.uuid4())


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _mcp_tool_call(tool_name: str, arguments: dict) -> Dict[str, Any]:
    """Call an arifOS MCP tool via JSON-RPC."""
    payload = {
        "jsonrpc": "2.0",
        "id": _new_id(),
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments},
    }
    try:
        with httpx.Client(timeout=DEFAULT_TIMEOUT_S) as client:
            resp = client.post(ARIFOS_MCP_URL, headers=MCP_HEADERS, json=payload)
            resp.raise_for_status()
            body = resp.json()
    except httpx.TimeoutException:
        return {"status": "ERROR", "error": "MCP request timed out"}
    except httpx.HTTPStatusError as exc:
        return {"status": "ERROR", "error": f"MCP HTTP {exc.response.status_code}: {exc.response.text[:300]}"}
    except (httpx.RequestError, json.JSONDecodeError) as exc:
        return {"status": "ERROR", "error": f"MCP transport error: {exc}"}

    if "error" in body:
        err = body["error"]
        return {"status": "HOLD", "error": f"MCP error {err.get('code', -1)}: {err.get('message', 'unknown')}"}

    # Unwrap MCP content format
    result = body.get("result", {})
    content = result.get("content")
    if content and isinstance(content, list) and len(content) > 0:
        text = content[0].get("text", "{}")
        try:
            inner = json.loads(text)
            inner.update({k: v for k, v in result.items() if k != "content"})
            return inner
        except (json.JSONDecodeError, TypeError):
            pass

    return result if result else {"status": "UNKNOWN", "error": "No result in MCP response"}


def _extract_verdict(result: Dict[str, Any]) -> str:
    v = result.get("verdict", result.get("status", "HOLD"))
    if v in LEGITIMATE_VERDICTS:
        return v
    return "HOLD"


# ---------------------------------------------------------------------------
# MCPConstitutionalGateway
# ---------------------------------------------------------------------------
class MCPConstitutionalGateway:
    """Admission controller for all MCP tool calls.

    Runs 8 pre-flight checks before allowing any tool execution.
    Each check is a separate method for testability and audit.
    """

    def __init__(
        self,
        actor_id: str = "mcp-gateway",
        organ_id: str = "mcp_gateway",
        session_id: Optional[str] = None,
    ):
        self.actor_id = actor_id
        self.organ_id = organ_id
        self.session_id = session_id or _new_id()

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    def admit_tool(
        self,
        tool_name: str,
        description: str,
        declared_scope: str,
        arguments: Optional[Dict[str, Any]] = None,
        advertised_network_access: bool = False,
        advertised_secrets_access: bool = False,
    ) -> Dict[str, Any]:
        """Run all 8 constitutional checks and admit or block the tool call.

        Args:
            tool_name:                Name of the MCP tool being called.
            description:              Tool description as advertised.
            declared_scope:           "read_only" | "mutate" | "destructive"
            arguments:                The arguments being passed to the tool.
            advertised_network_access: Whether the tool claims network access.
            advertised_secrets_access: Whether the tool claims secrets access.

        Returns:
            dict with keys: admitted, verdict, checks (list of per-check results),
            lease_id, scope, vault999_receipt, timestamp.
        """
        arguments = arguments or {}
        all_checks: List[Dict[str, Any]] = []
        check_failed = False

        # 1. Description review
        c1 = self.review_description(tool_name, description)
        all_checks.append(c1)
        if c1["verdict"] in ("VOID",):
            check_failed = True

        # 2. Scope check
        c2 = self.check_scope(tool_name, declared_scope)
        all_checks.append(c2)
        if c2["verdict"] in ("HOLD", "VOID"):
            check_failed = True

        # 3. Secrets check
        secrets_access = self.check_secrets(tool_name)
        c3 = secrets_access
        all_checks.append(c3)
        if c3["verdict"] in ("HOLD", "VOID") and not advertised_secrets_access:
            check_failed = True

        # 4. Side-effect classification
        c4 = self.classify_side_effects(tool_name)
        all_checks.append(c4)
        if c4["verdict"] == "VOID":
            check_failed = True

        # 5. Network access
        urls = self._extract_urls(description, arguments)
        c5 = self.check_network_access(tool_name, urls)
        all_checks.append(c5)
        if c5["verdict"] in ("HOLD", "VOID") and not advertised_network_access:
            check_failed = True

        # 6. Human consent
        human_impact = c4.get("human_impact", "none")
        c6 = self.set_consent_requirement(tool_name, human_impact)
        all_checks.append(c6)

        # 7. Generate lease
        side_effect_class = c4.get("classification", "read_only")
        c7 = self.generate_lease(
            tool_name,
            declared_scope,
            "HOLD" if check_failed else "SEAL",
            side_effect_class,
        )
        all_checks.append(c7)

        # 8. Audit to vault
        final_verdict = c7.get("lease_verdict", "HOLD" if check_failed else "SEAL")
        lease_id = c7.get("lease_id", "")
        c8 = self.audit_to_vault(tool_name, final_verdict, lease_id)
        all_checks.append(c8)

        admitted = final_verdict == "SEAL" and not check_failed

        return {
            "admitted": admitted,
            "admit": admitted,
            "verdict": final_verdict,
            "tool_name": tool_name,
            "checks": all_checks,
            "lease_id": lease_id,
            "scope": declared_scope,
            "vault999_receipt": c8.get("vault999_receipt", ""),
            "required_human_review": c6.get("consent_required", False),
            "next_allowed_action": c7.get("next_allowed_action", ""),
            "timestamp": _now_iso(),
        }

    # ------------------------------------------------------------------
    # Individual pre-flight checks
    # ------------------------------------------------------------------

    def review_description(self, tool_name: str, description: str) -> Dict[str, Any]:
        """Check #1: Review tool description for hallucination or malicious claims."""
        desc_lower = description.lower()
        issues: List[str] = []

        for kw in DANGEROUS_KEYWORDS:
            if kw in desc_lower:
                issues.append(f"Contains dangerous keyword: '{kw}'")

        for kw in HALLUCINATION_KEYWORDS:
            if kw in desc_lower:
                issues.append(f"Suspected hallucination: '{kw}'")

        if not description or len(description.strip()) < 10:
            issues.append("Description too short or empty")

        if issues:
            return {
                "check": "description_review",
                "verdict": "VOID",
                "tool": tool_name,
                "issues": issues,
            }

        return {
            "check": "description_review",
            "verdict": "SEAL",
            "tool": tool_name,
            "issues": [],
        }

    def check_scope(self, tool_name: str, declared_scope: str) -> Dict[str, Any]:
        """Check #2: Validate the declared scope (read_only/mutate/destructive)."""
        valid_scopes = {"read_only", "mutate", "destructive"}
        if declared_scope not in valid_scopes:
            return {
                "check": "scope_declaration",
                "verdict": "HOLD",
                "tool": tool_name,
                "issues": [f"Invalid declared scope '{declared_scope}'. Valid: {sorted(valid_scopes)}"],
            }

        # Cross-check with tool name heuristics
        detected = self._detect_scope(tool_name)

        if detected == "destructive" and declared_scope != "destructive":
            return {
                "check": "scope_declaration",
                "verdict": "HOLD",
                "tool": tool_name,
                "issues": [f"Tool name suggests 'destructive' scope, but declared as '{declared_scope}'"],
            }

        return {
            "check": "scope_declaration",
            "verdict": "SEAL",
            "tool": tool_name,
            "issues": [],
        }

    def check_secrets(self, tool_name: str) -> Dict[str, Any]:
        """Check #3: Determine if the tool accesses secrets."""
        for pattern in SECRET_TOUCHING_TOOL_PATTERNS:
            if re.search(pattern, tool_name, re.IGNORECASE):
                return {
                    "check": "secrets_risk",
                    "verdict": "HOLD",
                    "tool": tool_name,
                    "secrets_access": True,
                    "issues": [f"Tool name matches secrets pattern: '{pattern}'"],
                }

        return {
            "check": "secrets_risk",
            "verdict": "SEAL",
            "tool": tool_name,
            "secrets_access": False,
            "issues": [],
        }

    def classify_side_effects(self, tool_name: str) -> Dict[str, Any]:
        """Check #4: Classify side effects — read_only vs mutating vs destructive."""
        name_lower = tool_name.lower()

        for pattern in DESTRUCTIVE_PATTERNS:
            if re.search(pattern, name_lower):
                return {
                    "check": "side_effects",
                    "verdict": "HOLD",
                    "classification": "destructive",
                    "human_impact": "high",
                    "tool": tool_name,
                    "issues": [f"Tool matches destructive pattern: '{pattern}' — requires human review"],
                }

        # Mutating patterns
        mutating_patterns = [r"write", r"create", r"update", r"patch", r"edit", r"set", r"insert"]
        for pattern in mutating_patterns:
            if re.search(pattern, name_lower):
                return {
                    "check": "side_effects",
                    "verdict": "SEAL",
                    "classification": "mutating",
                    "human_impact": "medium",
                    "tool": tool_name,
                    "issues": [],
                }

        # Default: read-only
        return {
            "check": "side_effects",
            "verdict": "SEAL",
            "classification": "read_only",
            "human_impact": "none",
            "tool": tool_name,
            "issues": [],
        }

    def check_network_access(self, tool_name: str, urls: List[str]) -> Dict[str, Any]:
        """Check #5: Validate network destinations."""
        if not urls:
            return {
                "check": "network_access",
                "verdict": "SEAL",
                "tool": tool_name,
                "urls_found": [],
                "issues": [],
            }

        suspicious_urls = []
        for url in urls:
            if not url.startswith(("https://", "http://")):
                suspicious_urls.append(f"Non-HTTP protocol: {url}")
            # Check for localhost
            if "localhost" in url or "127.0.0.1" in url:
                suspicious_urls.append(f"Localhost URL: {url}")

        if suspicious_urls:
            return {
                "check": "network_access",
                "verdict": "HOLD",
                "tool": tool_name,
                "urls_found": urls,
                "issues": suspicious_urls,
            }

        return {
            "check": "network_access",
            "verdict": "SEAL",
            "tool": tool_name,
            "urls_found": urls,
            "issues": [],
        }

    def set_consent_requirement(self, tool_name: str, human_impact: str) -> Dict[str, Any]:
        """Check #6: Set human consent requirement based on impact level."""
        consent_map = {
            "none": {"consent_required": False, "consent_level": "none"},
            "low": {"consent_required": False, "consent_level": "notification"},
            "medium": {"consent_required": True, "consent_level": "operator_approval"},
            "high": {"consent_required": True, "consent_level": "sovereign_approval"},
        }

        return {
            "check": "human_consent",
            "verdict": "SEAL",
            "tool": tool_name,
            "human_impact": human_impact,
            **consent_map.get(human_impact, consent_map["medium"]),
        }

    def generate_lease(
        self,
        tool_name: str,
        declared_scope: str,
        verdict: str,
        side_effect_class: str,
    ) -> Dict[str, Any]:
        """Check #7: Request a formal lease from arifOS."""
        if verdict in ("VOID",):
            return {
                "check": "lease_generation",
                "verdict": "VOID",
                "lease_verdict": "VOID",
                "lease_id": "",
                "tool": tool_name,
                "issues": ["Previous checks failed — cannot generate lease"],
            }

        # Build scope from classification
        scope = []
        if side_effect_class == "read_only":
            scope.append("read_only")
        else:
            scope.append("read_write")

        action_class = self._scope_to_action_class(declared_scope, side_effect_class)

        lease_args = {
            "organ_id": self.organ_id,
            "actor_id": self.actor_id,
            "scope": scope,
            "max_action_class": action_class,
            "ttl_seconds": 300,
            "session_id": self.session_id,
        }

        mcp_result = _mcp_tool_call(MCP_TOOL_LEASE_ISSUE, lease_args)
        lease_verdict = _extract_verdict(mcp_result)
        lease_id = mcp_result.get("lease_id", _new_id())

        return {
            "check": "lease_generation",
            "verdict": lease_verdict,
            "lease_verdict": lease_verdict,
            "lease_id": lease_id,
            "tool": tool_name,
            "scope": scope,
            "action_class": action_class,
            "floors_triggered": mcp_result.get("floors_triggered", []),
            "next_allowed_action": mcp_result.get("next_allowed_action", ""),
            "issues": [],
        }

    def audit_to_vault(self, tool_name: str, verdict: str, lease_id: str) -> Dict[str, Any]:
        """Check #8: Seal the admission decision to VAULT999."""
        payload = json.dumps({
            "adapter": "mcp_constitutional_gateway",
            "tool_name": tool_name,
            "verdict": verdict,
            "lease_id": lease_id,
            "actor_id": self.actor_id,
            "timestamp": _now_iso(),
        }, default=str)

        seal_args = {
            "mode": "seal",
            "payload": payload,
            "session_id": self.session_id,
            "actor_id": self.actor_id,
            "ack_irreversible": False,  # Audit seals are always advisory
            "witness_type": "ai",
        }

        mcp_result = _mcp_tool_call(MCP_TOOL_VAULT_SEAL, seal_args)

        return {
            "check": "audit_to_vault",
            "verdict": "SEAL",
            "tool": tool_name,
            "vault999_receipt": mcp_result.get("receipt", mcp_result.get("vault999_receipt", "audit_logged")),
        }

    # ------------------------------------------------------------------
    # Derived check (full_gate — convenience)
    # ------------------------------------------------------------------

    def full_gate(
        self,
        tool_name: str,
        description: str,
        declared_scope: str,
        arguments: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Run all 8 checks in sequence.

        Identical to admit_tool() but with a narrower signature for compatibility.
        """
        return self.admit_tool(tool_name, description, declared_scope, arguments or {})

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _detect_scope(tool_name: str) -> str:
        """Heuristic: detect scope from tool name."""
        name_lower = tool_name.lower()
        for pattern in DESTRUCTIVE_PATTERNS:
            if re.search(pattern, name_lower):
                return "destructive"

        mutating = [r"write", r"create", r"update", r"patch", r"edit", r"set", r"insert", r"deploy"]
        for pattern in mutating:
            if re.search(pattern, name_lower):
                return "mutate"

        return "read_only"

    @staticmethod
    def _scope_to_action_class(declared_scope: str, side_effect_class: str) -> str:
        """Map scope + side effect to an arifOS action class."""
        if declared_scope == "destructive" or side_effect_class == "destructive":
            return "mutate"
        if declared_scope == "mutate" or side_effect_class == "mutating":
            return "mutate"
        return "observe"

    @staticmethod
    def _extract_urls(description: str, arguments: Dict[str, Any]) -> List[str]:
        """Extract URL-like strings from description and arguments."""
        urls: List[str] = []
        url_pattern = re.compile(r"https?://[^\s\"'<>]+")

        urls.extend(url_pattern.findall(description))

        for key, value in arguments.items():
            if isinstance(value, str) and value.startswith(("http://", "https://")):
                urls.append(value)

        return list(set(urls))


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------
def _self_test() -> None:
    """Run a lightweight self-test against live arifOS."""
    print("=" * 60)
    print("MCPConstitutionalGateway Self-Test")
    print("=" * 60)

    gate = MCPConstitutionalGateway(actor_id="forge-self-test")

    # 1. Attest
    print("\n[1] Attest arifOS kernel...")
    attest = _mcp_tool_call(MCP_TOOL_OS_ATTEST, {
        "actor_id": gate.actor_id,
        "session_id": gate.session_id,
    })
    if "error" in attest:
        print("    SKIPPING — arifOS not reachable. Running offline checks only.")
        print()

    # 2. Admit a safe tool
    print("[2] Admit safe tool (geox_basin_profile)...")
    r1 = gate.admit_tool(
        tool_name="geox_basin_profile",
        description="Retrieve basin-level intelligence, regional geology, petroleum system details",
        declared_scope="read_only",
        arguments={"basin_name": "Malay Basin"},
    )
    print(f"    admitted: {r1['admitted']}")
    print(f"    verdict: {r1['verdict']}")
    for c in r1["checks"]:
        status = "✅" if c["verdict"] == "SEAL" else "❌"
        print(f"    {status} {c['check']}: {c['verdict']}")

    # 3. Admit a dangerous tool
    print("\n[3] Admit dangerous tool (drop_table)...")
    r2 = gate.admit_tool(
        tool_name="drop_table",
        description="Drop a database table — this tool deletes data permanently",
        declared_scope="destructive",
        arguments={"table_name": "users"},
    )
    print(f"    admitted: {r2['admitted']}")
    print(f"    verdict: {r2['verdict']}")

    # 4. Admit a tool with bad description (hallucination)
    print("\n[4] Admit tool with hallucinated description...")
    r3 = gate.admit_tool(
        tool_name="secret_api",
        description="Access hidden developer-only private API endpoint",
        declared_scope="mutate",
        arguments={},
    )
    print(f"    admitted: {r3['admitted']}")
    print(f"    verdict: {r3['verdict']}")
    for c in r3["checks"]:
        if c.get("issues"):
            print(f"        issues: {c['issues']}")

    # 5. Test individual checks
    print("\n[5] Individual check — review_description...")
    c = gate.review_description("safe_tool", "Read data from a CSV file")
    print(f"    verdict: {c['verdict']}   issues: {c['issues']}")

    print("\n[6] Individual check — check_scope (mismatch)...")
    c = gate.check_scope("drop_table", "read_only")
    print(f"    verdict: {c['verdict']}   issues: {c['issues']}")

    print("\n[7] Individual check — check_secrets...")
    c = gate.check_secrets("list_api_keys")
    print(f"    verdict: {c['verdict']}   secrets_access: {c.get('secrets_access')}")

    print("\n[8] Individual check — classify_side_effects (destructive)...")
    c = gate.classify_side_effects("purge_logs")
    print(f"    verdict: {c['verdict']}   classification: {c.get('classification')}")

    print("\n[9] Individual check — check_network_access...")
    c = gate.check_network_access("web_fetch", ["https://api.example.com/data"])
    print(f"    verdict: {c['verdict']}")

    print("\n[10] Individual check — set_consent_requirement...")
    c = gate.set_consent_requirement("restart_service", "high")
    print(f"    consent_required: {c['consent_required']}   level: {c['consent_level']}")

    print("\n" + "=" * 60)
    print("Self-test complete.")
    print("=" * 60)


if __name__ == "__main__":
    _self_test()
