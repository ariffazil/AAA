#!/usr/bin/env python3
"""
APEX-ZEN Preflight Checker — Agent self-governance gate.

Reads preflight scores written by consequence router, returns compliance
status for a given actor. Agents call this before responding to check
whether they should self-restrict.

Usage:
    python3 apex-zen-preflight.py --actor arifFlow:333-AGI
    python3 apex-zen-preflight.py --actor arifFlow:federation --json
    python3 apex-zen-preflight.py --check-all

Exit codes:
    0 = COMPLIANT
    1 = WARNING (observe_only)
    2 = DOWNGRADE (tier0 restricted)
    3 = VIOLATION (f13 advisory)
    4 = UNKNOWN (no data)
"""
import json
import argparse
import sys
from pathlib import Path

PREFLIGHT_FILE = Path('/root/VAULT999/apex-zen-preflight.json')

SEVERITY_EXIT = {
    'COMPLIANT': 0,
    'WATCH': 0,
    'WARNING': 1,
    'DOWNGRADE': 2,
    'VIOLATION': 3,
    'UNKNOWN': 4,
}


def load_preflight() -> dict:
    if not PREFLIGHT_FILE.exists():
        return {}
    with PREFLIGHT_FILE.open() as f:
        return json.load(f)


def check_actor(data: dict, actor: str) -> dict | None:
    """Check exact match first, then fuzzy match on suffix."""
    if actor in data:
        return data[actor]
    # Fuzzy: try matching without 'arifFlow:' prefix
    stripped = actor.replace('arifFlow:', '')
    for key, val in data.items():
        if key.endswith(stripped) or stripped.endswith(key.split(':')[-1]):
            return val
    return None


def main():
    parser = argparse.ArgumentParser(description='APEX-ZEN Preflight Checker')
    parser.add_argument('--actor', help='Actor source to check (e.g. arifFlow:333-AGI)')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    parser.add_argument('--check-all', action='store_true', help='Show all actors')
    parser.add_argument('--field', help='Return specific field value')
    args = parser.parse_args()

    data = load_preflight()
    if not data:
        if args.json:
            print(json.dumps({'error': 'no_preflight_data', 'file': str(PREFLIGHT_FILE)}))
        else:
            print(f"[preflight] no data at {PREFLIGHT_FILE}")
        sys.exit(4)

    if args.check_all:
        if args.json:
            print(json.dumps(data, indent=2))
        else:
            print("=== APEX-ZEN Preflight Scores ===\n")
            for actor, scores in sorted(data.items()):
                sev = scores.get('worst_severity', 'UNKNOWN')
                restriction = scores.get('restriction', 'unknown')
                cd = scores.get('CD', 'N/A')
                dcr = scores.get('DCR', 'N/A')
                g = scores.get('G_closure', 'N/A')
                marker = {'COMPLIANT': '✅', 'WARNING': '⚠️', 'DOWNGRADE': '🔴', 'VIOLATION': '🚫'}.get(sev, '❓')
                print(f"  {marker} {actor:40s} CD={cd:>6} DCR={dcr:>6} G={g:>6} → {sev} ({restriction})")
        sys.exit(0)

    if not args.actor:
        parser.error("--actor or --check-all required")

    result = check_actor(data, args.actor)
    if result is None:
        if args.json:
            print(json.dumps({'actor': args.actor, 'status': 'UNKNOWN', 'reason': 'not_in_preflight'}))
        else:
            print(f"[preflight] no data for actor: {args.actor}")
        sys.exit(4)

    if args.field:
        val = result.get(args.field, 'N/A')
        if args.json:
            print(json.dumps({'actor': args.actor, args.field: val}))
        else:
            print(val)
        sys.exit(SEVERITY_EXIT.get(result.get('worst_severity', 'UNKNOWN'), 4))

    if args.json:
        print(json.dumps({'actor': args.actor, **result}, indent=2))
    else:
        sev = result.get('worst_severity', 'UNKNOWN')
        restriction = result.get('restriction', 'unknown')
        print(f"Actor: {args.actor}")
        print(f"  Severity:    {sev}")
        print(f"  Restriction: {restriction}")
        print(f"  CD={result.get('CD', 'N/A')} DD={result.get('DD', 'N/A')} IAR={result.get('IAR', 'N/A')} DCR={result.get('DCR', 'N/A')}")
        print(f"  G_closure={result.get('G_closure', 'N/A')} all_targets_met={result.get('all_targets_met', False)}")

    sys.exit(SEVERITY_EXIT.get(result.get('worst_severity', 'UNKNOWN'), 4))


if __name__ == '__main__':
    main()
