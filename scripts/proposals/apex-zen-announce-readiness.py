#!/usr/bin/env python3
"""ANNOUNCE-tier readiness validator (read-only).

Checks whether the live preflight meets the ANNOUNCE consumer contract
(see apex-zen-announce-consumer-2026-09-13.md). Exit 0 = READY, 1 = NOT READY.
"""
import json
import pathlib
import sys

PREFLIGHT = pathlib.Path('/root/VAULT999/apex-zen-preflight.json')
ENUM = {'COMPLIANT', 'WATCH', 'WARNING', 'DOWNGRADE', 'VIOLATION', 'UNKNOWN'}
FLAG = {'WARNING', 'DOWNGRADE', 'VIOLATION'}
ARTIFACTS = {'arifFlow:arif', 'arifFlow:333-AGI/agentic-web', 'arifFlow:333-AGI/dynamic-gate',
             'arifFlow:grok-build/FI-007', 'arifFlow:codex', 'arifFlow:codex-startup'}


def main() -> int:
    if not PREFLIGHT.exists():
        print("NOT READY: preflight missing")
        return 1
    d = json.load(PREFLIGHT.open())
    total = len(d)
    missing_sev, bad_enum, no_reliability, announce_set, artifact_hits = [], [], [], [], []
    for actor, rec in d.items():
        if not isinstance(rec, dict):
            missing_sev.append(actor)
            continue
        sev = rec.get('worst_severity')
        rel = rec.get('severity_reliable')
        if sev is None:
            missing_sev.append(actor)
        elif sev not in ENUM:
            bad_enum.append((actor, sev))
        if rel is None:
            no_reliability.append(actor)
        if sev in FLAG and rel is True:
            announce_set.append(actor)
            if actor in ARTIFACTS:
                artifact_hits.append(actor)
    SUSPECT_PREFIX = ('arifFlow:zen-', 'arifFlow:p0-', 'arifFlow:codex-')
    SUSPECT_EXACT = {'arifFlow:reexamine', 'arifFlow:stdin'}
    suspects = [a for a in announce_set if a.startswith(SUSPECT_PREFIX) or a in SUSPECT_EXACT]
    r4 = sum(1 for v in d.values() if isinstance(v, dict) and 'consecutive_flags' in v)
    print(f"actors: {total} | missing verdict: {len(missing_sev)} | bad enum: {len(bad_enum)} | no severity_reliable: {len(no_reliability)}")
    print(f"ANNOUNCE set (flagged AND reliable): {len(announce_set)}")
    print(f"artifact actors inside announce set: {len(artifact_hits)}")
    print(f"GATE-tier field consecutive_flags present: {r4}/{total} (required only for GATE)")
    ready = not missing_sev and not bad_enum and not no_reliability and not artifact_hits
    if suspects:
        print(f"CAUTION namespace suspects in announce set ({len(suspects)}): {suspects}")
        print("  - non-agent labels (workstream keys) pass severity_reliable; extend INV-3 allow-list before GATE.")
    print("READINESS (ANNOUNCE tier):", "READY" if ready else "NOT READY")
    if not ready:
        blockers = []
        if missing_sev: blockers.append(f"{len(missing_sev)} missing verdict")
        if bad_enum: blockers.append(f"{len(bad_enum)} bad enum")
        if no_reliability: blockers.append(f"{len(no_reliability)} missing severity_reliable")
        if artifact_hits: blockers.append(f"{len(artifact_hits)} artifact actors in announce set")
        print("blockers:", "; ".join(blockers))
    return 0 if ready else 1


if __name__ == '__main__':
    sys.exit(main())
