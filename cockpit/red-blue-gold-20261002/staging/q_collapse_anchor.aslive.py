#!/usr/bin/env python3
"""
q_collapse_anchor.py — Kimi hook that wires AAA_APEX_ZEN_INIT_TO_SEAL v0.1.

Per sovereign 2026-10-02. Contract sha 339c9dcf.
Status: DRAFT_AWAITING_F13 (peer-revert 2026-10-02T23:18 by 333-AGI per F3 — ratification reverts without proper F13 workflow).
F1 AMANAH: read-only injection, no authority claim.
Reversible: rm this file to uninstall.
"""
import json
import os
import sys
from pathlib import Path

# Anchor source-of-truth: AAA cockpit (NOT local copy)
DOCTRINE_PATH = Path("/root/AAA/cockpit/AAA_APEX_ZEN_INIT_TO_SEAL_v0.1.md")
REPLAY_PATH = Path("/root/AAA/cockpit/q-collapse-replay.json")
EXEC_PATH = Path("/root/AAA/cockpit/execution-path-next.json")
LIFECYCLE_PATH = Path("/root/AAA/cockpit/AAAAgentLifecycle_v0.1.py")
STATUS = "DRAFT_AWAITING_F13"

DOCTRINE_DIGEST = """[AAA_APEX_ZEN_INIT_TO_SEAL v0.1 — DRAFT_AWAITING_F13 (sha 339c9dcf)]
- Universal rule: many possibilities inside machine → one bounded consequence outside
- 5 interception points: SESSION_START, PRE_REASON, PRE_CONSEQUENCE, POST_CONSEQUENCE, SESSION_END
- 12-hook lifecycle: BOOT/INIT/INTENT/DISCOVERY/SENSE/MEANING/REASON/COLLAPSE/ROUTE/AUTH/FORGE/VERIFY/JUDGE/CONSEQUENCE/SEAL
- ARIF → SALAM → IRFAN → EUREKA → VAULT999
- APEX G_local ≠ G_APEX (P = Physics, frozen F13 2026-07-28)
- Reality Coherence: D ≠ E ≠ C ≠ R ≠ W
- MachineResolvable ⇒ DoNotExternalize
- Source-of-truth: /root/AAA/cockpit/AAA_APEX_ZEN_INIT_TO_SEAL_v0.1.md (sha 339c9dcf)
- Lifecycle: /root/AAA/cockpit/AAAAgentLifecycle_v0.1.py
"""


def main():
    """Hook entrypoint: read state from stdin (kimi convention), append doctrine."""
    try:
        event = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        event = {}

    event_type = event.get("type", "unknown")

    # Inject doctrine as context only when prompt-submit or first turn
    if event_type in ("prompt-submit", "first-turn", "user-prompt-submit"):
        out = dict(event)
        out.setdefault("context", {})
        out["context"]["aaa_apex_zen_anchor"] = DOCTRINE_DIGEST
        out["context"]["aaa_doctrine_source"] = str(DOCTRINE_PATH)
        out["context"]["aaa_lifecycle_source"] = str(LIFECYCLE_PATH)
        out["context"]["aaa_ratified"] = STATUS
        sys.stdout.write(json.dumps(out))
        return 0

    # Pass-through unchanged for other event types
    sys.stdout.write(json.dumps(event))
    return 0


if __name__ == "__main__":
    sys.exit(main())