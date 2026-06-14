#!/usr/bin/env python3
"""
OpenAI Agents SDK ↔ arifOS Adapter

Integration for running OpenAI Agents SDK agent loops under arifOS constitutional governance.

Pattern:
    arifOS guardrail escalation → SDK agent loop → VAULT999 receipt

Mapping:
    - Guardrail failure  → Escalate to arifOS: HOLD or VOID
    - Tool call          → Intercept: request arifOS lease + scope check
    - Agent handoff      → Intercept: request arifOS scope transfer
    - Trace event        → Route to VAULT999 receipt writer

Key distinction:
    OpenAI guardrails validate inputs/outputs at runtime.
    arifOS governs consequences at the constitutional level.

Usage:
    adapter = OpenAISDKAdapter(actor_id="forge-000omega")
    verdict = adapter.check_guardrail("pii_detection", {"sensitive_data": True})
    lease = adapter.lease_tool("read_file", {"path": "/tmp/data.csv"})
    transfer = adapter.scope_transfer("agent-alpha", "agent-beta", "Handoff for summarization")

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
MCP_TOOL_LEASE_INSPECT = "arif_lease_inspect"
MCP_TOOL_JUDGE_DELIBERATE = "arif_judge_deliberate"
MCP_TOOL_OS_ATTEST = "arif_os_attest"

LEGITIMATE_ACTION_CLASSES = {"observe", "propose", "mutate", "deploy", "communicate", "allocate"}
LEGITIMATE_VERDICTS = {"SEAL", "SABAR", "HOLD", "VOID"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _new_id() -> str:
    return str(uuid.uuid4())


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _mcp_tool_call(tool_name: str, arguments: dict) -> Dict[str, Any]:
    """Call an arifOS MCP tool via JSON-RPC over HTTP.

    Returns a flat dict (unwrapped from MCP content/text format) on success,
    or an error-shaped dict on failure.
    Never raises on governance holds — those are valid responses.
    """
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

    # Unwrap MCP content format (arifOS returns results in content[0].text)
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
    """Normalise an MCP result to a verdict string."""
    v = result.get("verdict", result.get("status", "HOLD"))
    if v in LEGITIMATE_VERDICTS:
        return v
    if "error" in result:
        return "HOLD"
    return "HOLD"


# ---------------------------------------------------------------------------
# OpenAISDKAdapter
# ---------------------------------------------------------------------------
class OpenAISDKAdapter:
    """Constitutional adapter for OpenAI Agents SDK.

    Maps SDK guardrails, tool calls, and agent handoffs to arifOS constitutional checks.
    """

    # Mapping of common OpenAI guardrail names to arifOS action classes
    GUARDRAIL_ACTION_MAP: Dict[str, str] = {
        "pii_detection": "observe",
        "moderation": "observe",
        "output_validation": "propose",
        "tool_validation": "propose",
        "input_safety": "observe",
        "jailbreak_detection": "observe",
        "customer_sensitivity": "communicate",
        "compliance_check": "propose",
    }

    def __init__(
        self,
        actor_id: str = "openai-sdk-adapter",
        organ_id: str = "openai_agents_sdk",
        session_id: Optional[str] = None,
    ):
        self.actor_id = actor_id
        self.organ_id = organ_id
        self.session_id = session_id or _new_id()
        self._lease_cache: Dict[str, Dict[str, Any]] = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def check_guardrail(self, guardrail_name: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """Map an OpenAI guardrail failure to an arifOS-compatible verdict.

        Args:
            guardrail_name: Name of the guardrail that fired (e.g. "pii_detection").
            result:         The guardrail result dict from the SDK.

        Returns:
            dict with keys: status, verdict, guardrail, arifos_action, severity,
            required_human_review, lease_id, timestamp.
        """
        action_class = self.GUARDRAIL_ACTION_MAP.get(guardrail_name, "observe")

        # Build an evidence receipt from the guardrail result
        evidence_receipt = {
            "source": "openai_guardrail",
            "guardrail": guardrail_name,
            "result_keys": list(result.keys()),
            "sample": str(result)[:500],
        }

        judge_args = {
            "mode": "judge",
            "candidate": f"guardrail:{guardrail_name}",
            "session_id": self.session_id,
            "actor_id": self.actor_id,
            "action_class": action_class,
            "evidence_receipt": evidence_receipt,
        }

        mcp_result = _mcp_tool_call(MCP_TOOL_JUDGE_DELIBERATE, judge_args)
        verdict = _extract_verdict(mcp_result)
        required_human = mcp_result.get("required_human_review", verdict == "VOID")

        return {
            "status": "OK" if verdict == "SEAL" else verdict,
            "verdict": verdict,
            "guardrail": guardrail_name,
            "arifos_action": action_class,
            "severity": mcp_result.get("severity", "unknown"),
            "required_human_review": required_human,
            "floors_triggered": mcp_result.get("floors_triggered", []),
            "vault999_receipt": mcp_result.get("vault999_receipt", ""),
            "timestamp": _now_iso(),
        }

    def lease_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Request a constitutional tool lease from arifOS.

        Intercepts SDK tool calls before execution.

        Args:
            tool_name:  Name of the tool the agent wants to call.
            arguments:  Arguments the agent wants to pass to the tool.

        Returns:
            dict with keys: status, verdict, lease_id, scope, floors_triggered,
            required_human_review, vault999_receipt, timestamp.
        """
        # Derive action class from tool name heuristics
        action_class = self._classify_tool_action(tool_name)
        scope = self._derive_scope(tool_name, action_class)

        lease_args = {
            "organ_id": self.organ_id,
            "actor_id": self.actor_id,
            "scope": scope,
            "max_action_class": action_class,
            "ttl_seconds": 120,
            "session_id": self.session_id,
            "forbidden": None,
        }

        mcp_result = _mcp_tool_call(MCP_TOOL_LEASE_ISSUE, lease_args)
        verdict = _extract_verdict(mcp_result)
        lease_id = mcp_result.get("lease_id", _new_id())

        rv = {
            "status": "OK" if verdict == "SEAL" else verdict,
            "verdict": verdict,
            "lease_id": lease_id,
            "tool_name": tool_name,
            "action_class": action_class,
            "scope": scope,
            "floors_triggered": mcp_result.get("floors_triggered", []),
            "required_human_review": mcp_result.get("required_human_review", False),
            "vault999_receipt": mcp_result.get("vault999_receipt", ""),
            "next_allowed_action": mcp_result.get("next_allowed_action", ""),
            "timestamp": _now_iso(),
        }

        self._lease_cache[lease_id] = rv
        return rv

    def scope_transfer(
        self,
        source_agent: str,
        target_agent: str,
        intent: str,
    ) -> Dict[str, Any]:
        """Request a scope transfer for agent-to-agent handoff.

        In the OpenAI Agents SDK, an agent can hand off to another agent.
        arifOS must authorize the scope transfer to prevent privilege escalation.

        Args:
            source_agent: Name/ID of the source agent.
            target_agent: Name/ID of the agent receiving handoff.
            intent:       Reason for the handoff/transfer.

        Returns:
            dict with keys: status, verdict, lease_id, source, target,
            scope, floors_triggered, timestamp.
        """
        judge_args = {
            "mode": "judge",
            "candidate": f"scope-transfer:{source_agent}→{target_agent}",
            "session_id": self.session_id,
            "actor_id": self.actor_id,
            "action_class": "communicate",
            "evidence_receipt": {
                "source_agent": source_agent,
                "target_agent": target_agent,
                "intent": intent,
            },
        }

        mcp_result = _mcp_tool_call(MCP_TOOL_JUDGE_DELIBERATE, judge_args)
        verdict = _extract_verdict(mcp_result)
        lease_id = mcp_result.get("lease_id", _new_id())

        return {
            "status": "OK" if verdict == "SEAL" else verdict,
            "verdict": verdict,
            "lease_id": lease_id,
            "source_agent": source_agent,
            "target_agent": target_agent,
            "intent": intent,
            "scope": mcp_result.get("scope", ["limited"]),
            "floors_triggered": mcp_result.get("floors_triggered", []),
            "required_human_review": mcp_result.get("required_human_review", verdict == "HOLD"),
            "vault999_receipt": mcp_result.get("vault999_receipt", ""),
            "timestamp": _now_iso(),
        }

    # ------------------------------------------------------------------
    # Heuristics
    # ------------------------------------------------------------------

    @staticmethod
    def _classify_tool_action(tool_name: str) -> str:
        """Heuristic to classify an SDK tool by name into an arifOS action class."""
        name_lower = tool_name.lower()

        # Write/mutate tools
        if any(token in name_lower for token in (
            "write", "create", "update", "patch", "insert", "upload",
            "edit", "modify", "set", "put", "post",
        )):
            return "mutate"

        # Delete/destructive
        if any(token in name_lower for token in ("delete", "remove", "drop", "destroy", "purge", "clear")):
            return "mutate"  # arifOS will further gate

        # Communication
        if any(token in name_lower for token in ("send", "email", "message", "notify", "post", "tweet", "slack")):
            return "communicate"

        # Deploy
        if any(token in name_lower for token in ("deploy", "publish", "release", "start", "restart")):
            return "deploy"

        # Allocate/spend
        if any(token in name_lower for token in ("pay", "spend", "transfer", "allocate", "buy", "purchase")):
            return "allocate"

        # Default: observe
        return "observe"

    @staticmethod
    def _derive_scope(tool_name: str, action_class: str) -> list:
        """Derive MCP scope from tool name and action class."""
        scope = []
        name_lower = tool_name.lower()

        if "secret" in name_lower or "credential" in name_lower or "token" in name_lower or "password" in name_lower:
            scope.append("secrets")

        if "db" in name_lower or "database" in name_lower or "sql" in name_lower:
            scope.append("database")

        if "fs" in name_lower or "file" in name_lower or "path" in name_lower:
            scope.append("filesystem")

        if "network" in name_lower or "http" in name_lower or "url" in name_lower or "web" in name_lower:
            scope.append("network")

        if action_class in ("mutate", "deploy", "allocate"):
            scope.append("read_write")
        else:
            scope.append("read_only")

        return scope


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------
def _self_test() -> None:
    """Run a lightweight self-test against live arifOS."""
    print("=" * 60)
    print("OpenAISDKAdapter Self-Test")
    print("=" * 60)

    adapter = OpenAISDKAdapter(actor_id="forge-self-test")

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

    # 2. Check guardrail
    print("\n[2] Check guardrail (pii_detection)...")
    gv = adapter.check_guardrail("pii_detection", {"sensitive_data": False, "confidence": 0.1})
    print(f"    verdict: {gv['verdict']}")
    print(f"    required_human_review: {gv['required_human_review']}")

    # 3. Check guardrail (moderation, high severity)
    print("\n[3] Check guardrail (moderation, flagged)...")
    gv2 = adapter.check_guardrail("moderation", {"flagged": True, "categories": ["hate"], "scores": {"hate": 0.95}})
    print(f"    verdict: {gv2['verdict']}")

    # 4. Lease a tool (observe)
    print("\n[4] Lease tool (read_file)...")
    t1 = adapter.lease_tool("read_file", {"path": "/tmp/test.csv"})
    print(f"    verdict: {t1['verdict']}")
    print(f"    scope: {t1['scope']}")

    # 5. Lease a tool (mutate/communicate)
    print("\n[5] Lease tool (send_email)...")
    t2 = adapter.lease_tool("send_email", {"to": "test@example.com", "body": "hello"})
    print(f"    verdict: {t2['verdict']}")
    print(f"    action_class: {t2['action_class']}")

    # 6. Scope transfer
    print("\n[6] Scope transfer (alpha → beta)...")
    tr = adapter.scope_transfer("agent-alpha", "agent-beta", "Summarize research findings")
    print(f"    verdict: {tr['verdict']}")
    print(f"    lease_id: {tr['lease_id'][:12]}...")

    print("\n" + "=" * 60)
    print("Self-test complete.")
    print("=" * 60)


if __name__ == "__main__":
    _self_test()
