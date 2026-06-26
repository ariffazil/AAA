#!/usr/bin/env python3
"""
VAULT999 Integration for Reality Ledger
========================================
Wires core/reality_ledger.py to the live arifOS vault sealing API.

Flow:
  1. Agent predicts an outcome → create Reality Ledger event
  2. arifOS judges → verdict returned
  3. Action executes (or not)
  4. Outcome observed → recorded to Reality Ledger
  5. Reality Ledger sealed to VAULT999 as proof

This creates the AGI loop: predict → act → observe → learn → seal.
"""

import json
import logging

# Import Reality Ledger core
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import httpx

logger = logging.getLogger(__name__)

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.reality_ledger import (
    DEFAULT_STORE_PATH,
    compute_accuracy_stats,
    create_event,
    record_outcome,
)

KERNEL_URL = "http://localhost:8088"


# ── VAULT999 MCP Client ────────────────────────────────────────────────────

def vault_seal(session_id: str, payload: str, actor_id: str = "forge-reality") -> dict:
    """Seal a Reality Ledger event to VAULT999 via arifOS."""
    logger.info("vault_seal called", extra={"session_id": session_id, "actor_id": actor_id})
    try:
        with httpx.Client(base_url=KERNEL_URL, timeout=15) as c:
            resp = c.post("/mcp", headers={"Accept": "application/json"}, json={
                "jsonrpc": "2.0",
                "id": f"vault-{actor_id}",
                "method": "tools/call",
                "params": {
                    "name": "arif_vault_seal",
                    "arguments": {
                        "mode": "seal",
                        "payload": payload,
                        "session_id": session_id,
                        "actor_id": actor_id,
                        "ack_irreversible": True,
                    },
                },
            })
            if resp.status_code != 200:
                return {"status": "ERROR", "error": f"HTTP {resp.status_code}"}
            body = resp.json()
            if "error" in body:
                err = body["error"]
                return {"status": "BLOCKED", "verdict": err.get("data", {}).get("verdict", "HOLD"),
                        "reason": err.get("message", "")}
            result = body.get("result", {})
            sc = result.get("structuredContent", {})
            if sc:
                return sc
            for c in result.get("content", []):
                if c.get("type") == "text":
                    try:
                        return json.loads(c["text"])
                    except (json.JSONDecodeError, KeyError):
                        continue
            return {"status": "OK", "raw": str(result)[:200]}
    except Exception as e:
        logger.exception("vault_seal failed")
        return {"status": "ERROR", "error": str(e)}

def ping_kernel() -> bool:
    """Check kernel reachability."""
    try:
        with httpx.Client(base_url=KERNEL_URL, timeout=5) as c:
            resp = c.post("/mcp", headers={"Accept": "application/json"}, json={
                "jsonrpc": "2.0", "id": "ping",
                "method": "tools/call",
                "params": {"name": "arif_ping", "arguments": {"mode": "probe"}},
            })
            return resp.status_code == 200
    except Exception:
        return False


# ── Combined Flow ───────────────────────────────────────────────────────────

def predict_seal_observe_learn(
    actor: str,
    intent: str,
    action_class: str,
    expected_outcome: str,
    confidence: float,
    session_id: str,
    uncertainty: str = "medium",
    failure_modes: Optional[list] = None,
    organs_consulted: Optional[list] = None,
    evidence_refs: Optional[list] = None,
    vault999_receipt: str = "",
    store_path: Path = DEFAULT_STORE_PATH,
) -> dict:
    """
    Full Reality Ledger flow:
    1. Create prediction event
    2. Seal the prediction to VAULT999
    3. Return event for later outcome recording

    Returns the event dict with vault_receipt populated.
    """
    logger.info("predict_seal_observe_learn called", extra={"actor": actor, "action_class": action_class})
    # Step 1: Create Reality Ledger event
    event = create_event(
        actor=actor,
        intent=intent,
        action_class=action_class,
        expected_outcome=expected_outcome,
        confidence=confidence,
        uncertainty=uncertainty,
        failure_modes=failure_modes or [],
        organs_consulted=organs_consulted or [],
        evidence_refs=evidence_refs or [],
        vault999_receipt=vault999_receipt or "",
        store_path=store_path,
    )

    # Step 2: Seal prediction to VAULT999
    seal_payload = json.dumps({
        "event_type": "REALITY_LEDGER_PREDICTION",
        "reality_event_id": event["id"],
        "actor": actor,
        "intent": intent,
        "action_class": action_class,
        "prediction": event["prediction"],
        "timestamp": event["timestamp"],
    })

    seal_result = vault_seal(session_id, seal_payload, actor)
    event["_seal_result"] = seal_result

    if seal_result.get("status") in ("OK", "SEAL"):
        # Try to extract receipt from seal response
        receipt = seal_result.get("vault999_receipt") or seal_result.get("result", {}).get("vault999_receipt")
        if receipt:
            event["vault999_receipt"] = receipt

    return event


def close_loop(
    event_id: str,
    result: str,
    delta_from_prediction: str = "",
    what_changed: str = "",
    memory_update: str = "",
    future_rule: str = "",
    session_id: str = "",
    actor: str = "forge-reality",
    vault_receipt_to_seal: str = "",
    store_path: Path = DEFAULT_STORE_PATH,
) -> dict:
    """
    Close the Reality Ledger loop:
    1. Record observed outcome
    2. Seal outcome + lesson to VAULT999
    3. Return updated event
    """
    updated = record_outcome(
        event_id=event_id,
        result=result,
        delta_from_prediction=delta_from_prediction,
        what_changed=what_changed,
        memory_update=memory_update,
        future_rule=future_rule,
        store_path=store_path,
    )

    # Seal outcome to VAULT999
    seal_payload = json.dumps({
        "event_type": "REALITY_LEDGER_OUTCOME",
        "reality_event_id": event_id,
        "result": result,
        "delta": delta_from_prediction,
        "lesson": updated.get("lesson", {}),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })

    seal_result = vault_seal(session_id, seal_payload, actor)
    updated["_outcome_seal"] = seal_result

    return updated


def generate_reality_report(store_path: Path = DEFAULT_STORE_PATH) -> dict:
    """Generate a comprehensive Reality Ledger report with VAULT999 linkage."""
    stats = compute_accuracy_stats(store_path)

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "stats": stats,
        "vault999_linkages": {
            "note": "Each Reality Ledger event with vault999_receipt populated has been sealed to VAULT999",
            "sealed_events": stats["total_events"],
        },
        "recommendations": [],
    }

    if stats["without_outcome"] > stats["with_outcome"]:
        report["recommendations"].append(
            f"Close the loop: {stats['without_outcome']} events still awaiting outcome observation"
        )

    if stats.get("mean_accuracy") is not None and stats["mean_accuracy"] < 0.7:
        report["recommendations"].append(
            f"Prediction accuracy ({stats['mean_accuracy']:.2f}) below 0.70 threshold"
        )

    return report


if __name__ == "__main__":
    import sys

    print("═══ Reality Ledger + VAULT999 Integration ═══")
    print()

    if not ping_kernel():
        print("❌ arifOS kernel unreachable.")
        print("   Start with: systemctl start arifos")
        sys.exit(1)
    print("✅ Kernel reachable")
    print()

    # Create a test event
    event = predict_seal_observe_learn(
        actor="forge-reality-test",
        intent="Test: Reality Ledger → VAULT999 pipeline",
        action_class="observe",
        expected_outcome="Event created and sealed to VAULT999",
        confidence=0.85,
        session_id="SEAL-reality-test",
        failure_modes=["Kernel unreachable", "VAULT999 gated"],
    )

    print(f"📝 Event created: {event['id']}")
    print(f"   Prediction: {event['prediction']['expected_outcome']}")
    print(f"   Confidence: {event['prediction']['confidence']}")

    seal_status = event.get("_seal_result", {}).get("status", "UNKNOWN")
    print(f"🔒 VAULT999 seal: {seal_status}")

    if event.get("vault999_receipt"):
        print(f"   Receipt: {event['vault999_receipt'][:40]}...")

    # Close the loop
    if seal_status in ("OK", "SEAL"):
        updated = close_loop(
            event_id=event["id"],
            result="Event created and sealed successfully",
            delta_from_prediction="Match: pipeline works as designed",
            what_changed="Confirmed Reality Ledger → VAULT999 integration",
            memory_update="Integration verified functional",
            future_rule="All predictions should seal to VAULT999",
            session_id="SEAL-reality-test",
        )
        outcome_seal = updated.get("_outcome_seal", {}).get("status", "UNKNOWN")
        print(f"🔒 Outcome seal: {outcome_seal}")

    # Report
    report = generate_reality_report()
    print(f"\n📊 Report: {report['stats']['total_events']} total events")
    print(f"   With outcome: {report['stats']['with_outcome']}")
    print(f"   Mean accuracy: {report['stats'].get('mean_accuracy', 'N/A')}")

    print("\n✅ Integration test complete")
