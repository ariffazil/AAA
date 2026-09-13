#!/usr/bin/env python3
"""ANNOUNCE-tier consumer — watermark semantics (log-only, never blocks).

Reads preflight; announces flagged actors whose severity is RELIABLE
(severity_reliable is true). Change-log semantics: a condition is announced
once on appearance and re-announced only if it clears and recurs (state file),
mirroring the receipts watermark (`apex-zen-receipts.state.json`).

Default = preview only. --emit writes to --out (default apex-zen-announce.jsonl)
and maintains <out>.state.json. Never advises action; GATE tier is out of scope.

Contract: proposals/apex-zen-announce-consumer-2026-09-13.md
"""
import argparse
import hashlib
import json
import pathlib
import sys

PREFLIGHT = pathlib.Path('/root/VAULT999/apex-zen-preflight.json')
ANNOUNCE = pathlib.Path('/root/VAULT999/apex-zen-announce.jsonl')
FLAG = {'WARNING', 'DOWNGRADE', 'VIOLATION'}


def condition_key(actor: str, severity: str, restriction: str) -> str:
    return f"{actor}|{severity}|{restriction}"


def announce_id(key: str, cycle_ts: str) -> str:
    return hashlib.sha256(f"{key}|{cycle_ts}".encode()).hexdigest()[:16]


def build(preflight_path: pathlib.Path):
    d = json.load(preflight_path.open())
    current, records = set(), {}
    for actor, rec in d.items():
        if not isinstance(rec, dict):
            continue
        sev = rec.get('worst_severity')
        if sev in FLAG and rec.get('severity_reliable') is True:
            restriction = rec.get('restriction', 'unknown')
            key = condition_key(actor, sev, restriction)
            current.add(key)
            records[key] = {
                'announce_id': announce_id(key, str(rec.get('timestamp', ''))),
                'cycle_ts': rec.get('timestamp'),
                'actor': actor,
                'severity': sev,
                'restriction': restriction,
                'per_metric_severity': rec.get('per_metric_severity'),
                'metrics_missing': rec.get('metrics_missing', []),
                'tier': 'ANNOUNCE',
                'action': 'log_only',
            }
    return current, records


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--preflight', default=str(PREFLIGHT))
    ap.add_argument('--out', default=str(ANNOUNCE))
    ap.add_argument('--emit', action='store_true', help='write to --out (default: preview only)')
    args = ap.parse_args()

    out_path = pathlib.Path(args.out)
    state_path = out_path.with_suffix(out_path.suffix + '.state.json')

    current, records = build(pathlib.Path(args.preflight))
    prev = set(json.load(state_path.open())) if state_path.exists() else set()
    fresh_keys = sorted(current - prev)
    cleared = sorted(prev - current)

    if not args.emit:
        print(f"[preview] active conditions: {len(current)} | new: {len(fresh_keys)} | cleared: {len(cleared)}")
        for k in fresh_keys[:20]:
            r = records.get(k, {})
            print(f"  {r.get('severity', '?'):9s} {r.get('actor', k):34s} {r.get('restriction', '')}")
        return 0

    with out_path.open('a') as f:
        for k in fresh_keys:
            f.write(json.dumps(records[k]) + '\n')
    state_path.write_text(json.dumps(sorted(current)))
    print(f"[emit] wrote {len(fresh_keys)} announcements -> {out_path} (active {len(current)}, cleared {len(cleared)})")
    return 0


if __name__ == '__main__':
    sys.exit(main())
