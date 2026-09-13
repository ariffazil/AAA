#!/usr/bin/env python3
"""
APEX-ZEN Consequence Router — Layer 4 wiring.

Reads telemetry JSONL, classifies values against thresholds per ladder,
emits receipts for WARNING+, applies runtime restrictions for DOWNGRADE+.

Doctrine ref: /root/AAA/governance/APEX-ZEN-CONSEQUENCE-LADDER.md
"""
import json
import argparse
import hashlib
from pathlib import Path
from datetime import datetime, timezone

TELEMETRY_INPUT = Path('/root/VAULT999/apex-zen-telemetry.jsonl')
RECEIPTS_OUTPUT = Path('/root/VAULT999/apex-zen-receipts.jsonl')
PREFLIGHT_OUTPUT = Path('/root/VAULT999/apex-zen-preflight.json')

# Change-detection watermark (added 2026-09-13, FI-008).
# Without it the router re-dumps the entire backlog every cycle: main() reads the
# whole telemetry log and appends a receipt for every WARNING+ signal on every run.
# `timestamp` is stamped with now(), so each re-emission LOOKS unique while being
# content-identical — there is no dedup key to detect it.
# Measured 2026-09-13T14:00Z: 27,280 rows carrying only 116 distinct signals
# (sev,metric,source,value) = 99.6% redundant, ~74 MB/day appended to a disk at 79%.
# Fix: emit a signal once on appearance; re-emit only if it clears and recurs.
# Semantics therefore change from full-snapshot-log to change-log.
# Use --snapshot to restore the old full-emission behaviour.
EMITTED_STATE = Path('/root/VAULT999/apex-zen-receipts.state.json')

# Promotion gate (invariant: no metric may be promoted without a witness object)
WITNESS_INPUT = Path('/root/VAULT999/apex-zen-witness.jsonl')


def load_witness_sources() -> set:
    srcs = set()
    if WITNESS_INPUT.exists():
        for line in WITNESS_INPUT.open():
            try:
                srcs.add(str(json.loads(line).get('session_source', '')))
            except json.JSONDecodeError:
                continue
    return srcs


def witness_backing(source: str, witness_sources: set) -> str:
    if not source or source == 'unknown':
        return 'MISSING'
    if source.startswith('arifFlow:'):
        return 'BOUND (ledger source)'
    if source in witness_sources:
        return 'BOUND (session witness)'
    for ws in witness_sources:
        if ws.endswith(source) or source.endswith(ws):
            return 'BOUND (session witness)'
    return 'MISSING'

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

# Severity ladder for picking an actor's worst metric.
# UNKNOWN is deliberately ABSENT: it denotes "no verdict for this metric",
# not a rank. Including it caused a missing metric (e.g. DD='inf') to outrank
# and thereby MASK a measured VIOLATION on another metric (CD/DCR).
# Observed 2026-09-13: 7 of 24 actors masked, incl. arifFlow:arif, codex,
# 333-AGI/agentic-web. Fixed FI-008.
SEVERITY_RANK = {s: i for i, s in enumerate(
    ['COMPLIANT', 'WATCH', 'WARNING', 'DOWNGRADE', 'VIOLATION'])}

RESTRICTIONS = {
    'COMPLIANT': 'none',
    'WATCH':     'log_only',
    'WARNING':   'observe_only',
    'DOWNGRADE': 'tier0_restricted_5_turns',
    'VIOLATION': 'f13_advisory',
    'UNKNOWN':   'no_verdict',
}

# Sources that appear in telemetry but are collector artifacts, not governed
# actors. Evidence: `stdin` appears as a `source` value (a pipe name, not an
# agent). Excluded from the enforcement namespace; recorded in the loop log.
NON_ACTOR_SOURCES = frozenset({'stdin'})


def write_preflight_scores(telemetry_records: list[dict]) -> None:
    """Write latest per-actor APEX-ZEN scores to preflight JSON for agent consumption.

    Agents read this file before responding to check their compliance status.

    Verdict resolution rule (FI-008, 2026-09-13):
      worst_severity = max over metrics with a VERDICT.
      UNKNOWN means "no verdict" — it never outranks a measured severity.
      per_metric_severity + metrics_missing are emitted so a consumer can see
      exactly which metric produced the verdict and which were unmeasurable.
    """
    latest_by_actor = {}
    for record in telemetry_records:
        source = record.get('source', 'unknown')
        ts = record.get('timestamp', '')
        if source not in latest_by_actor or ts > latest_by_actor[source].get('timestamp', ''):
            latest_by_actor[source] = record

    preflight = {}
    excluded = []
    for actor, record in latest_by_actor.items():
        if actor in NON_ACTOR_SOURCES:
            excluded.append(actor)
            continue
        values = {m: record.get(m, 'N/A') for m in ('CD', 'DD', 'IAR', 'DCR')}
        per_metric = {m: classify(m, v)[0] for m, v in values.items()}
        verdicts = [s for s in per_metric.values() if s in SEVERITY_RANK]
        worst = max(verdicts, key=SEVERITY_RANK.__getitem__) if verdicts else 'UNKNOWN'
        missing = sorted(m for m, s in per_metric.items() if s not in SEVERITY_RANK)

        preflight[actor] = {
            'timestamp': record.get('timestamp'),
            'CD': values['CD'], 'DD': values['DD'],
            'IAR': values['IAR'], 'DCR': values['DCR'],
            'worst_severity': worst,
            'per_metric_severity': per_metric,
            'metrics_missing': missing,
            'severity_reliable': not missing,
            'all_targets_met': record.get('all_targets_met', False),
            'G_closure': record.get('G_closure', 'N/A'),
            'restriction': RESTRICTIONS.get(worst, 'unknown'),
        }

    PREFLIGHT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with PREFLIGHT_OUTPUT.open('w') as f:
        json.dump(preflight, f, indent=2)

    if excluded:
        print(f"[router] excluded non-actor sources from enforcement namespace: {sorted(excluded)}")


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


def emit_receipt(record: dict, severity: str, metric: str, value, threshold_desc: str, witness_state: str = 'MISSING') -> dict:
    consequence = CONSEQUENCE_ACTIONS.get(severity, 'unknown')
    withheld = False
    if severity in ('DOWNGRADE', 'VIOLATION') and witness_state == 'MISSING':
        withheld = True
        consequence = 'log_only (WITHHELD — unwitnessed; invariant: no metric promoted without witness object)'
    source = record.get('source', 'unknown')
    return {
        'receipt_id': receipt_id(severity, metric, source, value),
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'severity': severity,
        'metric': metric,
        'value': value,
        'threshold': threshold_desc,
        'source': record.get('source', 'unknown'),
        'doctrine_status': 'PROVISIONAL_SEAL',
        'witness_backing': witness_state,
        'action_withheld': withheld,
        'consequence': consequence,
    }


def receipt_id(severity: str, metric: str, source: str, value) -> str:
    """Deterministic signal identity — stable across runs, so re-emission is detectable.

    Before 2026-09-13 receipts carried only a now() timestamp, which made every
    re-emission of an identical signal look like a new event. This id is the dedup
    key that was missing.
    """
    raw = f"{severity}|{metric}|{source}|{value}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def load_active_ids(path: Path) -> set:
    """Signals emitted on the previous run, or empty if the state file is absent/corrupt."""
    if not path.exists():
        return set()
    try:
        return set(json.loads(path.read_text()).get('active_ids', []))
    except (json.JSONDecodeError, OSError):
        return set()


def main():
    parser = argparse.ArgumentParser(description='APEX-ZEN Consequence Router')
    parser.add_argument('--input',  default=str(TELEMETRY_INPUT))
    parser.add_argument('--output', default=str(RECEIPTS_OUTPUT))
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--snapshot', action='store_true',
                        help='Emit the full backlog (pre-2026-09-13 behaviour) instead of change-log')
    args = parser.parse_args()

    input_path  = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"[router] no telemetry at {input_path}")
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)

    witness_sources = load_witness_sources()
    receipts = []
    telemetry_records = []
    summary = {k: 0 for k in list(CONSEQUENCE_ACTIONS) + ['UNKNOWN']}

    with input_path.open() as f:
        for line in f:
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            telemetry_records.append(record)
            for metric in ('CD', 'DD', 'IAR', 'DCR'):
                val = record.get(metric)
                severity, threshold_desc = classify(metric, val)
                summary[severity] += 1
                if severity in ('WARNING', 'DOWNGRADE', 'VIOLATION'):
                    receipts.append(emit_receipt(record, severity, metric, val, threshold_desc, witness_backing(str(record.get('source', '')), witness_sources)))

    print(f"\n=== APEX-ZEN Consequence Router ===")
    for sev, count in summary.items():
        if count > 0:
            print(f"  {sev:10s}: {count}")

    # Change-detection: reduce the full backlog to signals not already active.
    active_ids = {r['receipt_id'] for r in receipts}
    if args.snapshot:
        suppressed = 0
    else:
        prior_ids = load_active_ids(EMITTED_STATE)
        before = len(receipts)
        receipts = [r for r in receipts if r['receipt_id'] not in prior_ids]
        suppressed = before - len(receipts)
    print(f"[router] active signals: {len(active_ids)}  new: {len(receipts)}  suppressed (already active): {suppressed}")
    if args.snapshot:
        print("[router] --snapshot: full backlog emission, change-detection disabled")

    if receipts:
        if not args.dry_run:
            with output_path.open('a') as f:
                for r in receipts:
                    f.write(json.dumps(r) + '\n')
            print(f"\n[router] emitted {len(receipts)} receipts → {output_path}")
            wb = sum(1 for r in receipts if str(r.get('witness_backing', '')).startswith('BOUND'))
            print(f"[router] witness-backed: {wb}/{len(receipts)} (invariant: no promotion without witness object)")
            by_sev = {}
            for r in receipts:
                by_sev.setdefault(r['severity'], []).append(r)
            for sev, items in by_sev.items():
                print(f"  {sev}: {len(items)} (sample: {items[0]['metric']}={items[0]['value']})")
            EMITTED_STATE.write_text(json.dumps({
                'active_ids': sorted(active_ids),
                'updated': datetime.now(timezone.utc).isoformat(),
                'count': len(active_ids),
            }))
            print(f"[router] watermark → {EMITTED_STATE} ({len(active_ids)} active signals)")

        else:
            print(f"\n[DRY RUN] would emit {len(receipts)} receipts")
            for r in receipts[:3]:
                print(f"  {r['severity']}: {r['metric']}={r['value']} ({r['threshold']})")
    else:
        print("\n[router] all metrics compliant (no warnings).")

    # Mutation 2: write preflight scores for agent consumption
    if not args.dry_run and telemetry_records:
        write_preflight_scores(telemetry_records)
        print(f"[router] preflight scores → {PREFLIGHT_OUTPUT}")


if __name__ == '__main__':
    main()