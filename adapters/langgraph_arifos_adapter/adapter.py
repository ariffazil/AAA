#!/usr/bin/env python3
"""
LangGraph ↔ arifOS Adapter

Integration for running LangGraph workflows under arifOS constitutional governance.

Pattern:
    arifOS lease → LangGraph run → checkpoint → arifOS 888 → VAULT999 → Reality Ledger

Contract:
    Every LangGraph workflow step sends an adapter request with intent, action_class,
    blast_radius, reversibility. arifOS responds with SEAL/SABAR/HOLD/VOID + lease_id.

Usage:
    adapter = LangGraphAdapter(actor_id="forge-000omega")
    lease = adapter.request_lease(
        intent="Compute basin porosity ensemble",
        action_class="mutate",
        blast_radius="low",
        reversible=True,
        workflow_id="wf-graph-001",
        node_id="node-porosity-ensemble"
    )
    verdict = adapter.checkpoint_verdict(lease["lease_id"])
    seal = adapter.seal_workflow("wf-graph-001", {"status": "completed"})

DITEMPA BUKAN DIBERI — Forged, Not Given.
"""

import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

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

    # Handle JSON-RPC error response
    if "error" in body:
        err = body["error"]
        code = err.get("code", -1)
        msg = err.get("message", "unknown MCP error")
        return {"status": "HOLD", "error": f"MCP error {code}: {msg}"}

    # Unwrap MCP content format (arifOS returns results in content[0].text)
    result = body.get("result", {})
    content = result.get("content")
    if content and isinstance(content, list) and len(content) > 0:
        text = content[0].get("text", "{}")
        try:
            inner = json.loads(text)
            # Merge inner fields into result (inner takes precedence)
            inner.update({k: v for k, v in result.items() if k != "content"})
            return inner
        except (json.JSONDecodeError, TypeError):
            pass

    return result if result else {"status": "UNKNOWN", "error": "No result in MCP response"}


# ---------------------------------------------------------------------------
# LangGraphAdapter
# ---------------------------------------------------------------------------
class LangGraphAdapter:
    """Constitutional adapter for LangGraph workflows.

    Every workflow step and tool call is gated through arifOS before execution.
    The adapter never performs constitutional judgment — it delegates to the kernel.
    """

    def __init__(
        self,
        actor_id: str = "langgraph-adapter",
        organ_id: str = "langgraph",
        session_id: Optional[str] = None,
    ):
        self.actor_id = actor_id
        self.organ_id = organ_id
        self.session_id = session_id or _new_id()
        self._lease_cache: Dict[str, Dict[str, Any]] = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def request_lease(
        self,
        intent: str,
        action_class: str,
        blast_radius: str = "low",
        reversible: bool = True,
        secret_touching: bool = False,
        workflow_id: Optional[str] = None,
        node_id: Optional[str] = None,
        trace_id: Optional[str] = None,
        **extra: Any,
    ) -> Dict[str, Any]:
        """Request a constitutional lease from arifOS before executing a LangGraph step.

        Args:
            intent:       Free-text description of what the step intends to do.
            action_class: One of observe|propose|mutate|deploy|communicate|allocate.
            blast_radius: low|medium|high.
            reversible:   Whether the action can be rolled back.
            secret_touching: Whether the action touches credentials/secrets.
            workflow_id:  Optional LangGraph workflow identifier.
            node_id:      Optional LangGraph node identifier.
            trace_id:     Optional trace for observability linkage.
            **extra:      Additional context forwarded to arifOS.

        Returns:
            dict with keys: status, verdict, lease_id, scope, floors_triggered,
            vault999_receipt, next_allowed_action.
        """
        trace_id = trace_id or _new_id()

        # Validate action class
        if action_class not in LEGITIMATE_ACTION_CLASSES:
            return {
                "status": "ERROR",
                "verdict": "VOID",
                "error": f"Unknown action_class '{action_class}'. Valid: {sorted(LEGITIMATE_ACTION_CLASSES)}",
            }

        # First: attest organ to ensure kernel is live
        attest = self._call_attest()
        if attest.get("status") != "OK":
            return {
                "status": "ERROR",
                "verdict": "HOLD",
                "error": f"arifOS attestation failed: {attest.get('error', 'unknown')}",
            }

        # Build scope from action metadata
        scope = self._derive_scope(action_class, blast_radius, reversible, secret_touching)

        # Build the lease request
        lease_args = {
            "organ_id": self.organ_id,
            "actor_id": self.actor_id,
            "scope": scope,
            "max_action_class": action_class,
            "ttl_seconds": 300,  # 5 minute lease by default
            "session_id": self.session_id,
        }
        result = _mcp_tool_call(MCP_TOOL_LEASE_ISSUE, lease_args)

        verdict = self._extract_verdict(result)
        lease_id = result.get("lease_id", _new_id())
        rv = {
            "status": "OK" if verdict == "SEAL" else verdict,
            "verdict": verdict,
            "lease_id": lease_id,
            "scope": scope,
            "floors_triggered": result.get("floors_triggered", []),
            "vault999_receipt": result.get("vault999_receipt", ""),
            "next_allowed_action": result.get("next_allowed_action", "none"),
            "trace_id": trace_id,
            "workflow_id": workflow_id,
            "node_id": node_id,
            "intent": intent,
            "action_class": action_class,
            "timestamp": _now_iso(),
        }

        # Cache lease
        self._lease_cache[lease_id] = rv
        return rv

    def checkpoint_verdict(
        self,
        lease_id: str,
        action_class: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Checkpoint: ask arifOS for a verdict on whether this lease's action may proceed.

        Before irreversible transitions, call this to get an 888 verdict.

        Args:
            lease_id: The lease ID returned by request_lease().
            action_class: Override action class (uses cached if None).

        Returns:
            dict with verdict, reason, lease_id.
        """
        cached = self._lease_cache.get(lease_id, {})
        ac = action_class or cached.get("action_class", "observe")

        judge_args = {
            "mode": "judge",
            "candidate": f"langgraph-checkpoint:{lease_id}",
            "session_id": self.session_id,
            "actor_id": self.actor_id,
            "action_class": ac,
        }
        result = _mcp_tool_call(MCP_TOOL_JUDGE_DELIBERATE, judge_args)

        verdict = self._extract_verdict(result)
        return {
            "status": "OK" if verdict == "SEAL" else verdict,
            "verdict": verdict,
            "lease_id": lease_id,
            "reason": result.get("reason", ""),
            "floors_triggered": result.get("floors_triggered", []),
            "required_human_review": result.get("required_human_review", False),
            "next_allowed_action": result.get("next_allowed_action", ""),
            "timestamp": _now_iso(),
        }

    def seal_workflow(
        self,
        workflow_id: str,
        outcome: Dict[str, Any],
        ack_irreversible: bool = False,
    ) -> Dict[str, Any]:
        """Seal a completed LangGraph workflow to VAULT999.

        This is an immutable record. Acknowledge irreversibility to proceed.

        Args:
            workflow_id: LangGraph workflow identifier.
            outcome:     Summary dict of what happened and what was produced.
            ack_irreversible: Must be True for the seal to go through (F1 AMANAH).

        Returns:
            dict with vault receipt and verdict.
        """
        payload = json.dumps({
            "adapter": "langgraph",
            "workflow_id": workflow_id,
            "outcome": outcome,
            "actor_id": self.actor_id,
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
        result = _mcp_tool_call(MCP_TOOL_VAULT_SEAL, seal_args)

        if "error" in result:
            return {
                "status": "ERROR",
                "verdict": "HOLD",
                "error": result["error"],
            }

        return {
            "status": "OK",
            "verdict": "SEAL",
            "workflow_id": workflow_id,
            "vault999_receipt": result.get("receipt", result.get("vault999_receipt", "")),
            "lease_id": result.get("lease_id", ""),
            "timestamp": _now_iso(),
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _call_attest(self) -> Dict[str, Any]:
        """Attest the arifOS kernel is live and constitutional governance is active."""
        result = _mcp_tool_call(MCP_TOOL_OS_ATTEST, {
            "actor_id": self.actor_id,
            "session_id": self.session_id,
        })
        if "error" in result:
            return {"status": "ERROR", "error": result["error"]}
        # arifOS returns verdict=SEAL and result.heartbeat when healthy
        inner = result.get("result", {})
        heartbeat = inner.get("heartbeat", {})
        organ_status = heartbeat.get("status", "")
        if result.get("verdict") == "SEAL" or organ_status == "ALIVE":
            return {"status": "OK", "organ": "arifos"}
        return {"status": "ERROR", "error": result.get("error", "attestation failed")}

    @staticmethod
    def _derive_scope(action_class: str, blast_radius: str, reversible: bool, secret_touching: bool) -> list:
        """Derive an MCP scope list from action metadata."""
        scope = []
        if action_class in ("observe", "propose"):
            scope.append("read_only")
        if action_class in ("mutate", "deploy", "allocate"):
            scope.append("read_write")
            if not reversible:
                scope.append("irreversible")
        if blast_radius == "high":
            scope.append("high_blast")
        if secret_touching:
            scope.append("secrets")
        return scope

    @staticmethod
    def _extract_verdict(result: Dict[str, Any]) -> str:
        """Extract verdict from an MCP result dict."""
        v = result.get("verdict", result.get("status", "HOLD"))
        if v in LEGITIMATE_VERDICTS:
            return v
        if "error" in result:
            return "HOLD"
        return "HOLD"


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------
def _self_test() -> None:
    """Run a lightweight self-test against live arifOS.

    If arifOS is not running, the test will gracefully report failures
    rather than crashing.
    """
    print("=" * 60)
    print("LangGraphAdapter Self-Test")
    print("=" * 60)

    adapter = LangGraphAdapter(actor_id="forge-self-test")

    # 1. Attest
    print("\n[1] Attest arifOS kernel...")
    a = adapter._call_attest()
    print(f"    status: {a['status']}")
    if a["status"] != "OK":
        print("    SKIPPING remaining tests — arifOS not reachable.")
        return

    # 2. Request lease (observe)
    print("\n[2] Request observe lease...")
    lease = adapter.request_lease(
        intent="Self-test: read federation status",
        action_class="observe",
    )
    print(f"    verdict: {lease['verdict']}")
    print(f"    lease_id: {lease['lease_id']}")
    assert lease["verdict"] in ("SEAL", "SABAR", "HOLD"), f"Unexpected verdict: {lease['verdict']}"

    # 3. Checkpoint
    print(f"\n[3] Checkpoint verdict for lease {lease['lease_id'][:12]}...")
    cp = adapter.checkpoint_verdict(lease["lease_id"])
    print(f"    verdict: {cp['verdict']}")
    assert cp["verdict"] in ("SEAL", "SABAR", "HOLD")

    # 4. Seal (dry run — no irreversible ack)
    print("\n[4] Seal workflow (dry, no irreversible ack)...")
    seal = adapter.seal_workflow("self-test-wf", {"test": True}, ack_irreversible=False)
    print(f"    status: {seal['status']}")
    # Without ack_irreversible, this should HOLD

    # 5. Request mutate lease (high blast, irreversible)
    print("\n[5] Request mutate lease (should gate)...")
    bad = adapter.request_lease(
        intent="Self-test: simulated destructive action",
        action_class="mutate",
        blast_radius="high",
        reversible=False,
    )
    print(f"    verdict: {bad['verdict']}")
    print(f"    scope includes irreversible: {'irreversible' in bad.get('scope', [])}")

    print("\n" + "=" * 60)
    print("Self-test complete.")
    print("=" * 60)


if __name__ == "__main__":
    _self_test()
