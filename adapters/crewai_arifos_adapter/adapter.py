#!/usr/bin/env python3
"""
CrewAI ↔ arifOS Adapter (Flow Gate)

Integration for running CrewAI business workflows under arifOS high-consequence governance.

Pattern:
    arifOS flow step classification → CrewAI execution → VAULT999 seal

Step classification:
    observe     → Auto-allow + log
    draft       → Auto-allow + log
    mutate      → Require lease + rollback
    communicate → Consent check + log
    spend       → WEALTH witness + human gate
    deploy      → 888 SEAL required
    delete      → 888 SEAL required + F13

Key distinction:
    CrewAI runs the workflow. arifOS prevents the workflow from becoming a rogue state.

Usage:
    gate = CrewAIFlowGate(actor_id="forge-000omega")
    cls = gate.classify_step("deploy", "Deploy model to production", {"env": "prod"})
    verdict = gate.gate_step("deploy", "Deploy model to production", cls["lease_id"])
    seal = gate.seal_flow("daily-report-003", {"status": "completed", "outputs": 5})

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

LEGITIMATE_VERDICTS = {"SEAL", "SABAR", "HOLD", "VOID"}
VALID_STEP_TYPES = {"observe", "draft", "mutate", "communicate", "spend", "deploy", "delete"}

# Gate matrix: (step_type) → (gate_level, description, arifOS action_class)
STEP_GATE_MATRIX = {
    "observe":      ("AUTO_ALLOW",  "Read-only observation, auto-allowed",          "observe"),
    "draft":        ("AUTO_ALLOW",  "Draft/proposal, auto-allowed",                 "propose"),
    "mutate":       ("LEASE",       "State mutation, requires lease + rollback",     "mutate"),
    "communicate":  ("CONSENT",     "External communication, requires consent",      "communicate"),
    "spend":        ("WEALTH_GATE", "Capital allocation, WEALTH witness + human",    "allocate"),
    "deploy":       ("888_SEAL",    "Production deployment, requires 888 verdict",   "deploy"),
    "delete":       ("888_SEAL",    "Destructive action, requires 888 + F13 review", "mutate"),
}

# Auto-allowed step types skip arifOS call
AUTO_ALLOW_STEP_TYPES = {"observe", "draft"}


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
# CrewAIFlowGate
# ---------------------------------------------------------------------------
class CrewAIFlowGate:
    """Constitutional flow gate for CrewAI workflows.

    Every CrewAI step is classified before execution. High-consequence
    steps (mutate, communicate, spend, deploy, delete) are gated through
    arifOS for lease, consent, or 888 verdict.
    """

    def __init__(
        self,
        actor_id: str = "crewai-flow-gate",
        organ_id: str = "crewai",
        session_id: Optional[str] = None,
    ):
        self.actor_id = actor_id
        self.organ_id = organ_id
        self.session_id = session_id or _new_id()
        self._lease_cache: Dict[str, Dict[str, Any]] = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def classify_step(
        self,
        step_type: str,
        intent: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Classify a CrewAI step and determine the gate level.

        Args:
            step_type: One of observe|draft|mutate|communicate|spend|deploy|delete.
            intent:    Free-text description of what the step does.
            context:   Optional dict with additional metadata.

        Returns:
            dict with keys: status, step_type, gate_level, description, action_class,
            lease_id (if gated), reversible, blast_radius.
        """
        context = context or {}

        if step_type not in VALID_STEP_TYPES:
            return {
                "status": "VOID",
                "verdict": "VOID",
                "step_type": step_type,
                "error": f"Unknown step type '{step_type}'. Valid: {sorted(VALID_STEP_TYPES)}",
            }

        gate_level, description, action_class = STEP_GATE_MATRIX[step_type]

        # Determine reversibility and blast radius
        reversible = step_type in ("observe", "draft")
        blast_radius = self._derive_blast_radius(step_type, context)

        result = {
            "status": "OK",
            "step_type": step_type,
            "gate_level": gate_level,
            "description": description,
            "action_class": action_class,
            "intent": intent,
            "reversible": reversible,
            "blast_radius": blast_radius,
            "lease_id": "",
            "timestamp": _now_iso(),
        }

        # For auto-allow steps, generate a local lease
        if step_type in AUTO_ALLOW_STEP_TYPES:
            result["lease_id"] = _new_id()
            result["verdict"] = "SEAL"
            return result

        # For gated steps, request a lease from arifOS
        lease_result = self._request_lease(step_type, action_class, intent, reversible, blast_radius, context)
        result["lease_id"] = lease_result.get("lease_id", _new_id())
        result["verdict"] = lease_result.get("verdict", "HOLD")

        # If 888_SEAL level, also get a deliberate verdict
        if gate_level == "888_SEAL":
            judge_result = self._request_judge(step_type, intent, action_class, context)
            result["888_verdict"] = judge_result.get("verdict", "HOLD")
            result["required_human_review"] = judge_result.get("required_human_review", True)
        else:
            result["required_human_review"] = gate_level in ("CONSENT", "WEALTH_GATE")

        result["floors_triggered"] = lease_result.get("floors_triggered", [])
        result["vault999_receipt"] = lease_result.get("vault999_receipt", "")

        self._lease_cache[result["lease_id"]] = result
        return result

    def gate_step(
        self,
        step_type: str,
        intent: str,
        lease_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Gate a classified step — returns the final verdict from arifOS.

        For auto-allow steps, returns SEAL immediately.
        For gated steps, re-verifies with arifOS.

        Args:
            step_type: One of observe|draft|mutate|communicate|spend|deploy|delete.
            intent:    Free-text description.
            lease_id:  Optional lease ID from classify_step().

        Returns:
            dict with verdict and full gate details.
        """
        if step_type not in VALID_STEP_TYPES:
            return {"status": "VOID", "verdict": "VOID", "error": f"Unknown step type '{step_type}'"}

        gate_level, _, action_class = STEP_GATE_MATRIX[step_type]

        # Auto-allow: immediate SEAL
        if step_type in AUTO_ALLOW_STEP_TYPES:
            return {
                "status": "OK",
                "verdict": "SEAL",
                "step_type": step_type,
                "intent": intent,
                "gate_level": gate_level,
                "lease_id": lease_id or _new_id(),
                "required_human_review": False,
                "timestamp": _now_iso(),
            }

        # For gated steps, call arifOS judge
        judge_args = {
            "mode": "judge",
            "candidate": f"crewai-gate:{step_type}:{lease_id or intent[:40]}",
            "session_id": self.session_id,
            "actor_id": self.actor_id,
            "action_class": action_class,
        }
        mcp_result = _mcp_tool_call(MCP_TOOL_JUDGE_DELIBERATE, judge_args)
        verdict = _extract_verdict(mcp_result)

        return {
            "status": "OK" if verdict == "SEAL" else verdict,
            "verdict": verdict,
            "step_type": step_type,
            "intent": intent,
            "gate_level": gate_level,
            "action_class": action_class,
            "lease_id": lease_id or mcp_result.get("lease_id", _new_id()),
            "floors_triggered": mcp_result.get("floors_triggered", []),
            "required_human_review": mcp_result.get("required_human_review", verdict in ("HOLD", "VOID")),
            "vault999_receipt": mcp_result.get("vault999_receipt", ""),
            "next_allowed_action": mcp_result.get("next_allowed_action", ""),
            "timestamp": _now_iso(),
        }

    def seal_flow(
        self,
        flow_id: str,
        outcome: Dict[str, Any],
        ack_irreversible: bool = False,
    ) -> Dict[str, Any]:
        """Seal a completed CrewAI flow to VAULT999.

        Args:
            flow_id:           The CrewAI flow identifier.
            outcome:           Dict summarizing the flow results.
            ack_irreversible:  Must be True for the seal to proceed.

        Returns:
            dict with vault receipt.
        """
        payload = json.dumps({
            "adapter": "crewai",
            "flow_id": flow_id,
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
        mcp_result = _mcp_tool_call(MCP_TOOL_VAULT_SEAL, seal_args)

        if "error" in mcp_result:
            return {"status": "ERROR", "verdict": "HOLD", "error": mcp_result["error"]}

        return {
            "status": "OK",
            "verdict": "SEAL",
            "flow_id": flow_id,
            "vault999_receipt": mcp_result.get("receipt", mcp_result.get("vault999_receipt", "")),
            "timestamp": _now_iso(),
        }

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _request_lease(
        self,
        step_type: str,
        action_class: str,
        intent: str,
        reversible: bool,
        blast_radius: str,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Request an arifOS lease for a gated step."""
        scope = self._derive_scope(step_type, action_class, context)

        lease_args = {
            "organ_id": self.organ_id,
            "actor_id": self.actor_id,
            "scope": scope,
            "max_action_class": action_class,
            "ttl_seconds": 600,  # 10 min for flow steps
            "session_id": self.session_id,
        }
        mcp_result = _mcp_tool_call(MCP_TOOL_LEASE_ISSUE, lease_args)
        verdict = _extract_verdict(mcp_result)

        return {
            "lease_id": mcp_result.get("lease_id", _new_id()),
            "verdict": verdict,
            "scope": scope,
            "floors_triggered": mcp_result.get("floors_triggered", []),
            "vault999_receipt": mcp_result.get("vault999_receipt", ""),
        }

    def _request_judge(
        self,
        step_type: str,
        intent: str,
        action_class: str,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Request an 888 deliberate verdict for high-consequence steps."""
        judge_args = {
            "mode": "judge",
            "candidate": f"crewai-888:{step_type}:{intent[:60]}",
            "session_id": self.session_id,
            "actor_id": self.actor_id,
            "action_class": action_class,
            "evidence_receipt": {
                "step_type": step_type,
                "intent": intent,
                "context": context,
            },
        }
        mcp_result = _mcp_tool_call(MCP_TOOL_JUDGE_DELIBERATE, judge_args)
        verdict = _extract_verdict(mcp_result)

        return {
            "verdict": verdict,
            "required_human_review": mcp_result.get("required_human_review", verdict != "SEAL"),
            "floors_triggered": mcp_result.get("floors_triggered", []),
        }

    # ------------------------------------------------------------------
    # Static Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _derive_blast_radius(step_type: str, context: Dict[str, Any]) -> str:
        """Derive blast radius from step type and context."""
        if step_type in ("delete", "deploy"):
            return "high"
        if step_type == "spend":
            amount = context.get("amount", 0)
            if isinstance(amount, (int, float)) and amount > 10000:
                return "high"
            return "medium"
        if step_type == "communicate":
            audience = context.get("audience", "internal")
            return "medium" if audience == "external" else "low"
        if step_type == "mutate":
            return context.get("blast_radius", "low")
        return "low"

    @staticmethod
    def _derive_scope(step_type: str, action_class: str, context: Dict[str, Any]) -> list:
        """Derive MCP scope from step metadata."""
        scope = []
        if action_class in ("observe", "propose"):
            scope.append("read_only")
        else:
            scope.append("read_write")

        if step_type == "delete":
            scope.append("irreversible")
        if step_type == "deploy":
            scope.append("irreversible")
            scope.append("infrastructure")
        if step_type == "spend":
            scope.append("capital")
        if step_type == "communicate":
            scope.append("network")
        if context.get("secret_touching"):
            scope.append("secrets")

        return scope


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------
def _self_test() -> None:
    """Run a lightweight self-test against live arifOS."""
    print("=" * 60)
    print("CrewAIFlowGate Self-Test")
    print("=" * 60)

    gate = CrewAIFlowGate(actor_id="forge-self-test")

    # 1. Attest
    print("\n[1] Attest arifOS kernel...")
    attest = _mcp_tool_call(MCP_TOOL_OS_ATTEST, {
        "actor_id": gate.actor_id,
        "session_id": gate.session_id,
    })
    if "error" in attest:
        print("    SKIPPING — arifOS not reachable.")
        return
    print("    OK — arifOS reachable.")

    # 2. Classify observe step (auto-allow)
    print("\n[2] Classify 'observe' step...")
    c1 = gate.classify_step("observe", "Read inputs from CSV", {"path": "/tmp/data.csv"})
    print(f"    verdict: {c1.get('verdict', 'N/A')}")
    print(f"    gate_level: {c1.get('gate_level', 'N/A')}")
    assert c1["gate_level"] == "AUTO_ALLOW"

    # 3. Classify draft step (auto-allow)
    print("\n[3] Classify 'draft' step...")
    c2 = gate.classify_step("draft", "Draft summary report", {})
    print(f"    verdict: {c2.get('verdict', 'N/A')}")
    assert c2["gate_level"] == "AUTO_ALLOW"

    # 4. Classify mutate step (requires lease)
    print("\n[4] Classify 'mutate' step...")
    c3 = gate.classify_step("mutate", "Update database record", {"table": "users"})
    print(f"    verdict: {c3.get('verdict')}")
    print(f"    gate_level: {c3.get('gate_level')}")
    print(f"    lease_id: {c3.get('lease_id', 'N/A')[:12]}...")

    # 5. Gate a deploy step
    print("\n[5] Gate 'deploy' step...")
    g1 = gate.gate_step("deploy", "Deploy to production", "test-lease-001")
    print(f"    verdict: {g1['verdict']}")
    print(f"    required_human_review: {g1.get('required_human_review')}")

    # 6. Classify spend step (wealth gate)
    print("\n[6] Classify 'spend' step (large)...")
    c4 = gate.classify_step("spend", "Purchase cloud credits", {"amount": 50000})
    print(f"    verdict: {c4.get('verdict')}")
    print(f"    gate_level: {c4.get('gate_level')}")
    print(f"    blast_radius: {c4.get('blast_radius')}")

    # 7. Gate an auto-allow step (should always SEAL)
    print("\n[7] Gate 'observe' step...")
    g2 = gate.gate_step("observe", "Read logs", None)
    print(f"    verdict: {g2['verdict']}")
    assert g2["verdict"] == "SEAL"

    # 8. Seal flow
    print("\n[8] Seal flow (dry, no ack)...")
    s1 = gate.seal_flow("test-flow-001", {"steps_completed": 5}, ack_irreversible=False)
    print(f"    status: {s1['status']}")

    # 9. Invalid step type
    print("\n[9] Invalid step type...")
    bad = gate.classify_step("fly_to_moon", "Launch", {})
    print(f"    status: {bad['status']}")
    assert bad["status"] == "VOID"

    print("\n" + "=" * 60)
    print("Self-test complete.")
    print("=" * 60)


if __name__ == "__main__":
    _self_test()
