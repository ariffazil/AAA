#!/usr/bin/env python3
"""arifflow-hook handler.py — FQ metabolism receipts for Hermes (ASI gateway).

agent:start -> Execute receipt to arifFlow :7073
agent:end   -> Verify + Seal receipts (1:1:1 session ratio, FI pattern)
Canonical: KVM8 /root/HERMES (single pen). Deployed mirror: KVM4 /root/HERMES + ~/.hermes/hooks symlink.
Wired 2026-09-04 by FI-003 under F13 flow-all directive. Fail-soft always.

SCAR NOTE: epistemic_label MUST be from the F2 enum {Observation, Derivation,
Interpretation, Specification, Seal} — arifFlow :7073/ingest rejects anything
else with HTTP 400 ("Verify" is NOT a valid label; step_type Verify uses label
Observation). Silent 400s swallowed by fail-soft were the 2026-09-04 scar.
"""

import json
import os
import time
import urllib.request
import uuid

ARIFLOW_INGEST = os.environ.get("ARIFLOW_INGEST", "http://127.0.0.1:7073/ingest")
ACTOR_ID = "hermes-asi"
TIMEOUT = 3


def _post(step_type: str, label: str, session_id: str, summary: str) -> bool:
    payload = {
        "receipt_id": str(uuid.uuid4()),
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()) + ".000000Z",
        "actor_id": ACTOR_ID,
        "session_id": session_id or "hermes-unbound",
        "step_type": step_type,
        "step_number": 0 if step_type == "Execute" else 1,
        "cost_ns": 0,
        "epistemic_label": label,
        "floor_verdict": "Pass",
        "cooling_decision": "None",
        "summary": summary,
    }
    try:
        req = urllib.request.Request(
            ARIFLOW_INGEST,
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return 200 <= resp.status < 300
    except Exception:
        return False


def handle(event_type=None, context=None, event=None):
    if isinstance(event_type, dict):
        event = event_type
        event_type = event.get("event_type", event.get("type", "unknown"))

    ctx = context if isinstance(context, dict) else (event or {})
    session_id = str(ctx.get("session_id") or ctx.get("session") or "")

    if event_type == "agent:start":
        ok = _post("Execute", "Observation", session_id, "agent:start hermes-asi gateway")
        return {"status": "receipt_posted" if ok else "receipt_failed", "event": event_type}
    if event_type == "agent:end":
        v = _post("Verify", "Observation", session_id, "agent:end verify hermes-asi")
        s = _post("Seal", "Seal", session_id, "agent:end seal hermes-asi")
        return {"status": "receipts_posted" if (v or s) else "receipts_failed",
                "event": event_type, "verify": v, "seal": s}
    return {"status": "ignored", "event": event_type}


if __name__ == "__main__":
    print(json.dumps(handle("agent:start", {"session_id": "wiring-verify"})))
