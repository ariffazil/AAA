#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# Hermes — Propose Event to VAULT999 Pending Queue
# Phase 2A: Hermes writes event proposals; OpenClaw witnesses them into VAULT999
# ═══════════════════════════════════════════════════════════════════════════════

import json
import uuid
import datetime
import hmac
import hashlib
import os
import sys

SHARED_SECRET_PATH = "/root/.arifos/shared-secrets/hermes-openclaw-bridge.key"
PENDING_DIR = "/tmp/hermes-pending-events"


def load_secret() -> bytes:
    with open(SHARED_SECRET_PATH, "r") as f:
        return f.read().strip().encode("utf-8")


def sign_event(event: dict, secret: bytes) -> str:
    payload = dict(event)  # copy
    payload.pop("hermes_signature", None)
    payload_bytes = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hmac.new(secret, payload_bytes, hashlib.sha256).hexdigest()


def propose_event(
    description: str,
    event_type: str = "observation",
    evidence: list = None,
    confidence: float = 0.85,
    session_id: str = "unknown",
) -> str:
    """Propose an event to the VAULT999 pending queue.

    Returns the event_id on success.
    """
    if event_type not in ("observation", "preference_update", "project_state_change"):
        raise ValueError(f"Invalid event_type: {event_type}")

    if not (0.0 <= confidence <= 1.0):
        raise ValueError("confidence must be between 0.0 and 1.0")

    event_id = f"hermes_{uuid.uuid4().hex[:12]}"
    event = {
        "event_id": event_id,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "actor": "Hermes ASI",
        "session_id": session_id,
        "type": event_type,
        "payload": {
            "description": description,
            "evidence": evidence or [],
            "confidence": confidence,
        },
    }

    secret = load_secret()
    event["hermes_signature"] = sign_event(event, secret)

    os.makedirs(PENDING_DIR, exist_ok=True)
    pending_path = os.path.join(PENDING_DIR, f"{event_id}.json")
    with open(pending_path, "w") as f:
        json.dump(event, f, indent=2, ensure_ascii=False)

    return event_id


def main():
    if len(sys.argv) < 2:
        print("Usage: propose-vault-event.py <description> [type] [confidence] [session_id]")
        print("  type: observation | preference_update | project_state_change")
        print("  confidence: 0.0-1.0 (default 0.85)")
        sys.exit(1)

    description = sys.argv[1]
    event_type = sys.argv[2] if len(sys.argv) > 2 else "observation"
    confidence = float(sys.argv[3]) if len(sys.argv) > 3 else 0.85
    session_id = sys.argv[4] if len(sys.argv) > 4 else f"cli-{os.getpid()}"

    event_id = propose_event(
        description=description,
        event_type=event_type,
        confidence=confidence,
        session_id=session_id,
    )
    print(f"Event proposed: {event_id}")
    print(f"Pending path: /tmp/hermes-pending-events/{event_id}.json")
    print("OpenClaw will witness within 30 minutes.")


if __name__ == "__main__":
    main()
