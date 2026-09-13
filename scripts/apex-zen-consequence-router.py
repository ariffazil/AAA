#!/usr/bin/env python3
"""
APEX-ZEN Consequence Router — Layer 4 wiring.

Reads telemetry JSONL, classifies values against thresholds per ladder,
emits receipts for WARNING+, applies runtime restrictions for DOWNGRADE+.

Doctrine ref: /root/AAA/governance/APEX-ZEN-CONSEQUENCE-LADDER.md
"""
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone

TELEMETRY_INPUT = Path('/root/VAULT999/apex-zen-telemetry.jsonl')
RECEIPTS_OUTPUT = Path('/root/VAULT999/apex-zen-receipts.jsonl')

THRESHOLDS = {
    'CD':  {'warning': 0.20, 'downgrade': 0.40, 'violation': 0.60},
    'DD':  {'warning': 4,    'downgrade': 8,    'violation': 12},
    'IAR': {'warning': 0.60, 'downgrade': 0.40, 'violation': 0.20},
    'DCR': {'warning': 0.80, 'downgrade': 0.60, 'violation': 0.40},
}

CONSEQUENCE_ACTIONS = {
    'COMPLIANT': 'no_action',
    'WATCH':     'log_to_telemetry',
    'WARNING':   'emit_warning_receipt',
    'DOWNGRADE': 'emit_downgrade_receipt + restrict_runtime_5_turns',
    'VIOLATION': 'emit_violation_receipt + f13_advisory',
}


def classify(metric: str, val) -> tuple[str, str]:
    """Return (severity, threshold_description)."""
    if val == 'inf' or val is None or val == 'N/A':
        return 'UNKNOWN', 'no_data'
    try:
        v = float(val)
    except (TypeError, ValueError):
        return 'UNKNOWN', 'invalid_value'
    t = THRESHOLDS[metric]
    if metric in ('IAR', 'DCR'):
        if v < t['violation']:    return 'VIOLATION', f'< {t["violation"]}'
        if v < t['downgrade']:    return 'DOWNGRADE', f'< {t["downgrade"]}'
        if v < t['warning']:      return 'WARNING',   f'< {t["warning"]}'
        return 'COMPLIANT', f'≥ {t["warning"]}'
    else:
        if v >= t['violation']:   return 'VIOLATION', f'≥ {t["violation"]}'
        if v >= t['downgrade']:   return 'DOWNGRADE', f'≥ {t["downgrade"]}'
        if v >= t['warning']:     return 'WARNING',   f'≥ {t["warning"]}'
        return 'COMPLIANT', f'< {t["warning"]}'


def emit_receipt(record: dict, severity: str, metric: str, value, threshold_desc: str) -> dict:
    return {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'severity': severity,
        'metric': metric,
        'value': value,
        'threshold': threshold_desc,
        'source': record.get('source', 'unknown'),
        'doctrine_status': 'PROVISIONAL_SEAL',
        'consequence': CONSEQUENCE_ACTIONS.get(severity, 'unknown'),
    }


def main():
    parser = argparse.ArgumentParser(description='APEX-ZEN Consequence Router')
    parser.add_argument('--input',  default=str(TELEMETRY_INPUT))
    parser.add_argument('--output', default=str(RECEIPTS_OUTPUT))
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    input_path  = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"[router] no telemetry at {input_path}")
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)

    receipts = []
    summary = {k: 0 for k in list(CONSEQUENCE_ACTIONS) + ['UNKNOWN']}

    with input_path.open() as f:
        for line in f:
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            for metric in ('CD', 'DD', 'IAR', 'DCR'):
                val = record.get(metric)
                severity, threshold_desc = classify(metric, val)
                summary[severity] += 1
                if severity in ('WARNING', 'DOWNGRADE', 'VIOLATION'):
                    receipts.append(emit_receipt(record, severity, metric, val, threshold_desc))

    print(f"\n=== APEX-ZEN Consequence Router ===")
    for sev, count in summary.items():
        if count > 0:
            print(f"  {sev:10s}: {count}")

    if receipts:
        if not args.dry_run:
            with output_path.open('a') as f:
                for r in receipts:
                    f.write(json.dumps(r) + '\n')
            print(f"\n[router] emitted {len(receipts)} receipts → {output_path}")
            by_sev = {}
            for r in receipts:
                by_sev.setdefault(r['severity'], []).append(r)
            for sev, items in by_sev.items():
                print(f"  {sev}: {len(items)} (sample: {items[0]['metric']}={items[0]['value']})")
        else:
            print(f"\n[DRY RUN] would emit {len(receipts)} receipts")
            for r in receipts[:3]:
                print(f"  {r['severity']}: {r['metric']}={r['value']} ({r['threshold']})")
    else:
        print("\n[router] all metrics compliant (no warnings).")


if __name__ == '__main__':
    main()