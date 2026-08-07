#!/usr/bin/env python3
"""
Weekly Seal Integrity Sweep — compares active VAULT999 seals against current artifact hashes.
Purpose: detect seal drift (hash/name/count mismatch) before it propagates.
Output: ACTIVE | DRIFT | MISSING | SUPERSEDED per seal.
"""
import hashlib, json, os, sys
from pathlib import Path
from datetime import datetime, timezone

VAULT = Path('/root/arifOS/VAULT999/outcomes.jsonl')
AUDIT_DIR = Path('/root/AAA/reports')

def sha256_of_file(path: str) -> str | None:
    try:
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    except (FileNotFoundError, PermissionError):
        return None

def check_seal(receipt: dict) -> str:
    """Compare seal hashes against current disk state."""
    aid = receipt.get('audit_id', 'UNKNOWN')
    deliverables = receipt.get('deliverables', [])
    if not deliverables:
        return f'NO_DELIVERABLES'

    issues = []
    for d in deliverables:
        fname = d.get('file', '')
        expected_hash = d.get('sha256', '')

        # Resolve path — try common audit directories
        resolved = None
        for base in [AUDIT_DIR]:
            for sub in base.rglob(fname):
                resolved = sub
                break
            if resolved:
                break

        if resolved is None:
            issues.append(f'MISSING:{fname}')
            continue

        actual_hash = sha256_of_file(str(resolved))
        if actual_hash is None:
            issues.append(f'UNREADABLE:{fname}')
        elif actual_hash != expected_hash:
            issues.append(f'DRIFT:{fname}({expected_hash[:8]}→{actual_hash[:8]})')

    if not issues:
        return 'ACTIVE'
    elif any(i.startswith('MISSING') for i in issues):
        return f'PARTIAL_MISSING({"|".join(issues)})'
    else:
        return f'DRIFT({"|".join(issues)})'

def main():
    if not VAULT.exists():
        print('VAULT999 not found')
        sys.exit(1)

    results = {'ACTIVE': [], 'DRIFT': [], 'SUPERSEDED': [], 'UNKNOWN': []}

    with open(VAULT) as f:
        for line in f:
            try:
                raw = line.strip()
                if not raw:
                    continue
                receipt = json.loads(raw)
                # Handle double-encoded entries
                if isinstance(receipt, str):
                    receipt = json.loads(receipt)
                if not isinstance(receipt, dict):
                    continue
            except (json.JSONDecodeError, ValueError):
                continue

            aid = receipt.get('audit_id', receipt.get('record_id', ''))
            verdict = receipt.get('verdict', '')

            # Skip non-audit receipts
            if not any(prefix in str(aid) for prefix in ['MMA-', 'AUDIT-', 'SEAL-']):
                continue

            # Check status
            if 'SUPERSEDED' in str(verdict).upper():
                results['SUPERSEDED'].append(aid)
                continue
            if 'QUARANTINE' in str(verdict).upper():
                results['SUPERSEDED'].append(aid)
                continue

            # Active seal — check artifacts
            if receipt.get('deliverables'):
                status = check_seal(receipt)
                if status == 'ACTIVE':
                    results['ACTIVE'].append(aid)
                else:
                    results['DRIFT'].append((aid, status))
            else:
                results['UNKNOWN'].append(aid)

    # Report
    now = datetime.now(timezone.utc).isoformat()
    print(f'=== SEAL INTEGRITY SWEEP — {now} ===')
    print()
    print(f'ACTIVE: {len(results["ACTIVE"])}')
    for aid in results['ACTIVE']:
        print(f'  ✓ {aid}')

    print(f'DRIFT: {len(results["DRIFT"])}')
    for aid, status in results['DRIFT']:
        print(f'  ✗ {aid}: {status}')

    print(f'SUPERSEDED: {len(results["SUPERSEDED"])}')
    for aid in results['SUPERSEDED']:
        print(f'  – {aid}')

    print(f'UNKNOWN: {len(results["UNKNOWN"])}')
    for aid in results['UNKNOWN']:
        print(f'  ? {aid}')

    print()
    if results['DRIFT']:
        print('ACTION REQUIRED: Seal drift detected. Re-seal affected artifacts.')
    else:
        print('ALL SEALS INTEGRITY VERIFIED.')
    print()

    # JSON output for cron consumption
    summary = {
        'timestamp': now,
        'active': len(results['ACTIVE']),
        'drift': len(results['DRIFT']),
        'superseded': len(results['SUPERSEDED']),
        'unknown': len(results['UNKNOWN']),
        'status': 'DRIFT_DETECTED' if results['DRIFT'] else 'ALL_CLEAR',
        'details': [{'seal': aid, 'status': s} for aid, s in results['DRIFT']] if results['DRIFT'] else [],
    }
    print(json.dumps(summary, indent=2))

if __name__ == '__main__':
    main()
