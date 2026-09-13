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
ARTIFACTS = {'arifFlow:arif', 'arifFlow:333-AGI/agentic-web', 'arifFlow:333-AGI/dynamic-gate',
             'arifFlow:grok-build/FI-007', 'arifFlow:codex', 'arifFlow:codex-startup'}


def main() -> int:
    if not PREFLIGHT.exists():
        print("NOT READY: preflight missing")
        return 1
    d = json.load(PREFLIGHT.open())
    total = len(d)
    missing_fields, bad_verdict, flagged, artifact_hits = [], [], [], []
    for actor, rec in d.items():
        if not isinstance(rec, dict):
            missing_fields.append(actor)
            continue
        sev = rec.get('worst_severity')
        if sev is None:
            missing_fields.append(actor)
        elif sev not in ENUM:
            bad_verdict.append((actor, sev))
        if sev in ('WARNING', 'DOWNGRADE', 'VIOLATION'):
            flagged.append(actor)
            if actor in ARTIFACTS and not ('consecutive_flags' in rec and 'cd_basis' in rec):
                artifact_hits.append(actor)
    r1r4 = sum(1 for rec in d.values() if isinstance(rec, dict)
               and 'cd_basis' in rec and 'consecutive_flags' in rec)
    print(f"actors: {total} | missing worst_severity: {len(missing_fields)} | bad enum: {len(bad_verdict)}")
    print(f"R1/R4 fields (cd_basis+consecutive_flags) present on: {r1r4}/{total}")
    print(f"flagged actors: {len(flagged)} | artifact false-flag risk: {len(artifact_hits)}")
    if artifact_hits:
        print("artifact-risk actors:", artifact_hits)
    ready = not missing_fields and not bad_verdict and not artifact_hits and r1r4 == total
    print("READINESS:", "READY" if ready else "NOT READY")
    if not ready:
        reasons = []
        if missing_fields:
            reasons.append(f"{len(missing_fields)} actors missing verdict")
        if artifact_hits:
            reasons.append(f"{len(artifact_hits)} artifact false-flag risk (await R1/R4)")
        if r1r4 != total:
            reasons.append(f"R1/R4 fields absent on {total - r1r4} actors")
        print("blockers:", "; ".join(reasons))
    return 0 if ready else 1


if __name__ == '__main__':
    sys.exit(main())
