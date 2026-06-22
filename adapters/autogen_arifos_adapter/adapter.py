#!/usr/bin/env python3
"""
AutoGen ↔ arifOS Adapter (Parliament)

Integration for running AutoGen multi-agent societies under arifOS constitutional governance.

Pattern:
    arifOS constitutional parliament rules → AutoGen agent execution

Each AutoGen agent created under arifOS carries a constitution:
    role, allowed_tools, forbidden_actions, authority_level, lease_scope.

Key rules:
    - arifOS validates agent constitution at creation time.
    - arifOS intercepts all tool calls and cross-agent messages.
    - No agent may self-authorize — only arifOS issues verdicts.

Usage:
    adapter = AutoGenParliamentAdapter(actor_id="forge-000omega")
    agent_config = {
        "role": "analyst",
        "allowed_tools": ["geox_basin_profile", "search_web"],
        "forbidden_actions": ["deploy", "delete_file"],
        "authority_level": "L1",
        "lease_scope": ["earth_data"],
        "may_propose": True,
        "may_authorize": False,
    }
    validation = adapter.constitute_agent(agent_config)
    forbidden = adapter.forbid_action("analyst", "delete_file")
    lease = adapter.lease_agent_tool("analyst", "geox_basin_profile", {"basin_name": "Malay Basin"})

DITEMPA BUKAN DIBERI — Forged, Not Given.
"""

import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

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
MCP_TOOL_OS_ATTEST = "arif_os_attest"
MCP_TOOL_VAULT_SEAL = "arif_vault_seal"

LEGITIMATE_VERDICTS = {"SEAL", "SABAR", "HOLD", "VOID"}
VALID_ROLES = {"analyst", "researcher", "executor", "reviewer"}
VALID_AUTHORITY_LEVELS = {"L1", "L2", "L3"}

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
# Agent constitution schema
# ---------------------------------------------------------------------------
AGENT_CONSTITUTION_SCHEMA = {
    "role": {"type": str, "valid": VALID_ROLES},
    "allowed_tools": {"type": list, "min_items": 0},
    "forbidden_actions": {"type": list, "min_items": 0},
    "authority_level": {"type": str, "valid": VALID_AUTHORITY_LEVELS},
    "lease_scope": {"type": list, "min_items": 0},
    "may_propose": {"type": bool},
    "may_authorize": {"type": bool, "must_be": False},  # No agent may authorize
}


def _validate_agent_constitution(agent_config: Dict[str, Any]) -> List[str]:
    """Validate agent constitution against schema. Returns list of errors (empty = valid)."""
    errors: List[str] = []

    for field, spec in AGENT_CONSTITUTION_SCHEMA.items():
        if field not in agent_config:
            errors.append(f"Missing required field: {field}")
            continue

        value = agent_config[field]
        expected_type = spec.get("type")
        if not isinstance(value, expected_type):
            errors.append(f"Field '{field}' must be {expected_type.__name__}, got {type(value).__name__}")
            continue

        # Valid set membership
        valid_set = spec.get("valid")
        if valid_set and value not in valid_set:
            errors.append(f"Field '{field}' = '{value}' not in valid set: {sorted(valid_set)}")

        # Min items for lists
        min_items = spec.get("min_items")
        if isinstance(value, list) and min_items is not None and len(value) < min_items:
            errors.append(f"Field '{field}' must have at least {min_items} items, got {len(value)}")

        # Must-be constraint
        must_be = spec.get("must_be")
        if must_be is not None and value is not must_be:
            errors.append(f"Field '{field}' must be {must_be}, got {value}")

    return errors


# ---------------------------------------------------------------------------
# AutoGenParliamentAdapter
# ---------------------------------------------------------------------------
class AutoGenParliamentAdapter:
    """Constitutional adapter for AutoGen multi-agent societies.

    Validates agent constitutions, checks forbidden actions, and issues
    scoped tool leases through arifOS.
    """

    def __init__(
        self,
        actor_id: str = "autogen-parliament-adapter",
        organ_id: str = "autogen",
        session_id: Optional[str] = None,
    ):
        self.actor_id = actor_id
        self.organ_id = organ_id
        self.session_id = session_id or _new_id()
        self._constitutions: Dict[str, Dict[str, Any]] = {}  # role → config
        self._lease_cache: Dict[str, Dict[str, Any]] = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def constitute_agent(self, agent_config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate an AutoGen agent constitution against the arifOS schema.

        If valid, registers the agent role for future checks.

        Args:
            agent_config: Dict with keys: role, allowed_tools, forbidden_actions,
                         authority_level, lease_scope, may_propose, may_authorize.

        Returns:
            dict with keys: status, verdict, role, errors, warnings, lease_scope.
        """
        errors = _validate_agent_constitution(agent_config)

        if errors:
            return {
                "status": "VOID",
                "verdict": "VOID",
                "role": agent_config.get("role", "unknown"),
                "constituted": False,
                "errors": errors,
                "warnings": [],
                "lease_scope": [],
            }

        role = agent_config["role"]

        # Register the constitution
        self._constitutions[role] = dict(agent_config)

        # Optionally attest through arifOS that this agent is valid
        judge_args = {
            "mode": "judge",
            "candidate": f"autogen-constitute:{role}",
            "session_id": self.session_id,
            "actor_id": self.actor_id,
            "action_class": "propose",
            "evidence_receipt": {
                "constitution": agent_config,
                "schema_valid": True,
            },
        }
        mcp_result = _mcp_tool_call(MCP_TOOL_JUDGE_DELIBERATE, judge_args)
        verdict = _extract_verdict(mcp_result)

        warnings = []
        if not agent_config.get("may_propose", True):
            warnings.append(f"Agent '{role}' cannot propose — will only act when directed.")
        if agent_config.get("lease_scope") and len(agent_config["lease_scope"]) == 0:
            warnings.append(f"Agent '{role}' has no lease scope — cannot call any tool.")

        return {
            "status": "OK" if verdict == "SEAL" else verdict,
            "verdict": verdict,
            "role": role,
            "constituted": True,
            "errors": [],
            "warnings": warnings,
            "lease_scope": agent_config.get("lease_scope", []),
            "allowed_tools": agent_config.get("allowed_tools", []),
            "authority_level": agent_config.get("authority_level", "L1"),
            "vault999_receipt": mcp_result.get("vault999_receipt", ""),
            "timestamp": _now_iso(),
        }

    def forbid_action(self, agent_role: str, action: str) -> Dict[str, Any]:
        """Check if an action is forbidden for a given agent role.

        Args:
            agent_role: The agent's role (e.g. "analyst").
            action:     The action to check (e.g. "delete_file").

        Returns:
            dict with keys: verdict (SEAL = allowed, VOID = forbidden), role,
            action, forbidden_by, reason.
        """
        # Check role exists
        if agent_role not in self._constitutions:
            return {
                "status": "ERROR",
                "verdict": "HOLD",
                "error": f"Agent role '{agent_role}' not constituted. Call constitute_agent() first.",
            }

        config = self._constitutions[agent_role]
        forbidden_actions = config.get("forbidden_actions", [])
        allowed_tools = config.get("allowed_tools", [])

        # Check explicit forbidden list
        if action in forbidden_actions:
            return {
                "status": "VOID",
                "verdict": "VOID",
                "role": agent_role,
                "action": action,
                "forbidden_by": "agent_constitution",
                "reason": f"Action '{action}' is in the forbidden list for role '{agent_role}'.",
                "timestamp": _now_iso(),
            }

        # Check if it's a tool that is not in the allowed list
        if action not in allowed_tools:
            return {
                "status": "HOLD",
                "verdict": "HOLD",
                "role": agent_role,
                "action": action,
                "forbidden_by": "scope_restriction",
                "reason": f"Action '{action}' is not in the allowed_tools for role '{agent_role}'.",
                "timestamp": _now_iso(),
            }

        return {
            "status": "OK",
            "verdict": "SEAL",
            "role": agent_role,
            "action": action,
            "forbidden_by": None,
            "reason": "Action is permitted by agent constitution.",
            "timestamp": _now_iso(),
        }

    def lease_agent_tool(
        self,
        agent_role: str,
        tool: str,
        arguments: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Request a tool lease from arifOS for a specific agent role.

        Combines local constitution check + arifOS lease issuance.

        Args:
            agent_role: The agent's role.
            tool:       The tool name the agent wants to call.
            arguments:  The arguments to the tool.

        Returns:
            dict with keys: status, verdict, lease_id, scope, floors_triggered.
        """
        # 1. Check constitution exists
        if agent_role not in self._constitutions:
            return {
                "status": "ERROR",
                "verdict": "HOLD",
                "error": f"Agent role '{agent_role}' not constituted.",
            }

        # 2. Check forbidden actions
        forbidden_check = self.forbid_action(agent_role, tool)
        if forbidden_check["verdict"] != "SEAL":
            return forbidden_check  # Propagate the BLOCK

        config = self._constitutions[agent_role]

        # 3. Derive action class
        action_class = self._derive_action_class(tool)

        # 4. Build scope from lease_scope + tool heuristics
        scope = list(config.get("lease_scope", []))
        if tool in ("read_file", "search_web", "geox_basin_profile", "geox_evidence_discover"):
            scope.append("read_only")
        else:
            scope.append("operate")

        # 5. Request lease from arifOS
        lease_args = {
            "organ_id": self.organ_id,
            "actor_id": f"{self.actor_id}:{agent_role}",
            "scope": scope,
            "max_action_class": action_class,
            "ttl_seconds": 180,
            "session_id": self.session_id,
        }
        mcp_result = _mcp_tool_call(MCP_TOOL_LEASE_ISSUE, lease_args)
        verdict = _extract_verdict(mcp_result)
        lease_id = mcp_result.get("lease_id", _new_id())

        rv = {
            "status": "OK" if verdict == "SEAL" else verdict,
            "verdict": verdict,
            "lease_id": lease_id,
            "role": agent_role,
            "tool": tool,
            "action_class": action_class,
            "scope": scope,
            "floors_triggered": mcp_result.get("floors_triggered", []),
            "required_human_review": mcp_result.get("required_human_review", False),
            "vault999_receipt": mcp_result.get("vault999_receipt", ""),
            "timestamp": _now_iso(),
        }

        self._lease_cache[lease_id] = rv
        return rv

    # ------------------------------------------------------------------
    # Heuristics
    # ------------------------------------------------------------------

    @staticmethod
    def _derive_action_class(tool_name: str) -> str:
        """Heuristic action class from tool name."""
        lower = tool_name.lower()
        if any(w in lower for w in ("write", "create", "update", "delete", "remove", "drop", "patch", "edit")):
            return "mutate"
        if any(w in lower for w in ("deploy", "restart", "publish", "release")):
            return "deploy"
        if any(w in lower for w in ("send", "email", "message", "notify", "post")):
            return "communicate"
        if any(w in lower for w in ("pay", "spend", "transfer", "allocate")):
            return "allocate"
        return "observe"

    def seal_agent_session(self, session_summary: Dict[str, Any], ack_irreversible: bool = False) -> Dict[str, Any]:
        """Seal an AutoGen agent session to VAULT999.

        Args:
            session_summary: Dict summarizing the session activity.
            ack_irreversible: Must be True for the seal to proceed.

        Returns:
            dict with vault receipt.
        """
        payload = json.dumps({
            "adapter": "autogen",
            "actor_id": self.actor_id,
            "session_summary": session_summary,
            "constitutions": {k: {kk: vv for kk, vv in v.items() if kk != "allowed_tools"}
                              for k, v in self._constitutions.items()},
            "timestamp": _now_iso(),
        }, default=str)

        seal_args = {
            "mode": "seal",
            "payload": payload,
            "session_id": self.session_id,
            "actor_id": self.actor_id,
            "ack_irreversible": ack_irreversible,
            "witness_type": "ai",
        }
        mcp_result = _mcp_tool_call(MCP_TOOL_VAULT_SEAL, seal_args)

        if "error" in mcp_result:
            return {"status": "ERROR", "verdict": "HOLD", "error": mcp_result["error"]}

        return {
            "status": "OK",
            "verdict": "SEAL",
            "vault999_receipt": mcp_result.get("receipt", mcp_result.get("vault999_receipt", "")),
            "timestamp": _now_iso(),
        }


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------
def _self_test() -> None:
    """Run a lightweight self-test against live arifOS."""
    print("=" * 60)
    print("AutoGenParliamentAdapter Self-Test")
    print("=" * 60)

    adapter = AutoGenParliamentAdapter(actor_id="forge-self-test")

    # 1. Attest
    print("\n[1] Attest arifOS kernel...")
    attest = _mcp_tool_call(MCP_TOOL_OS_ATTEST, {
        "actor_id": adapter.actor_id,
        "session_id": adapter.session_id,
    })
    if "error" in attest:
        print("    SKIPPING — arifOS not reachable.")
        return
    print("    OK — arifOS reachable.")

    # 2. Constitute a valid agent
    print("\n[2] Constitute valid analyst agent...")
    valid_config = {
        "role": "analyst",
        "allowed_tools": ["geox_basin_profile", "search_web", "read_file"],
        "forbidden_actions": ["deploy", "delete_file", "send_email"],
        "authority_level": "L1",
        "lease_scope": ["earth_data"],
        "may_propose": True,
        "may_authorize": False,
    }
    c1 = adapter.constitute_agent(valid_config)
    print(f"    verdict: {c1['verdict']}")
    print(f"    constituted: {c1['constituted']}")
    if c1.get("errors"):
        print(f"    ERRORS: {c1['errors']}")

    # 3. Constitute an invalid agent (role wrong, may_authorize=True)
    print("\n[3] Constitute invalid agent (bad role + may_authorize)...")
    bad_config = {
        "role": "king",
        "allowed_tools": ["everything"],
        "forbidden_actions": [],
        "authority_level": "L5",
        "lease_scope": [],
        "may_propose": True,
        "may_authorize": True,
    }
    c2 = adapter.constitute_agent(bad_config)
    print(f"    verdict: {c2['verdict']}")
    print(f"    errors: {c2.get('errors', [])}")

    # 4. Forbid check: allowed action
    print("\n[4] Forbid check: geox_basin_profile (should be SEAL)...")
    f1 = adapter.forbid_action("analyst", "geox_basin_profile")
    print(f"    verdict: {f1['verdict']}")
    assert f1["verdict"] == "SEAL"

    # 5. Forbid check: forbidden action
    print("\n[5] Forbid check: delete_file (should be VOID)...")
    f2 = adapter.forbid_action("analyst", "delete_file")
    print(f"    verdict: {f2['verdict']}")
    assert f2["verdict"] == "VOID"

    # 6. Forbid check: unregistered role
    print("\n[6] Forbid check: unregistered role...")
    f3 = adapter.forbid_action("nonexistent_role", "read_file")
    print(f"    status: {f3['status']}")
    assert "ERROR" in f3["status"] or f3["status"] == "ERROR"

    # 7. Lease tool
    print("\n[7] Lease tool for analyst...")
    l1 = adapter.lease_agent_tool("analyst", "geox_basin_profile", {"basin_name": "Malay Basin"})
    print(f"    verdict: {l1['verdict']}")
    print(f"    lease_id: {l1['lease_id'][:12]}...")

    # 8. Seal session (no ack — should hold)
    print("\n[8] Seal session (no ack)...")
    s1 = adapter.seal_agent_session({"tools_called": 3, "agents_active": 1}, ack_irreversible=False)
    print(f"    status: {s1['status']}")

    print("\n" + "=" * 60)
    print("Self-test complete.")
    print("=" * 60)


if __name__ == "__main__":
    _self_test()
