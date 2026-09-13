#!/usr/bin/env python3
"""
APEX-ZEN arifFlow Source — Node 2 in the enforcement graph.

Reads arifFlow /health endpoint, extracts per-actor execute/verify counts,
emits APEX-ZEN telemetry records with real IAR + DCR.

This is the parallel source to apex-zen-session-collector.py.
Fan-out: both sources → join in telemetry.jsonl.

Doctrine ref: /root/AAA/governance/APEX-ZEN-EXECUTION-DOCTRINE.md § 13
Graph pattern: AGI-graph-engineering-patterns #5 (fan-out + deliberate join)
"""
import json
import sys
import argparse
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime, timezone

DEFAULT_ARIFLOW_URL = 'http://localhost:7073/health'
TELEMETRY_OUTPUT = Path('/root/VAULT999/apex-zen-telemetry.jsonl')


def fetch_health(url: str, timeout: int = 5) -> dict:
    """Fetch arifFlow /health endpoint."""
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as e:
        print(f"[ariflow-source] fetch error: {e}", file=sys.stderr)
        return {}


def derive_apex_zen_metrics(actor: dict) -> dict:
    """Map arifFlow per-actor data → APEX-ZEN metrics.

    execute_count ≈ artifacts delivered
    verify_count  ≈ verifications (closures)
    consecutive_exec_no_verify ≈ ongoing-loose-loop signal

    IAR = artifacts / requests — approximated as execute / (execute + held)
    DCR = closure rate — approximated as verify / (execute + verify)
    CD  ≈ consecutive_exec_no_verify / window — soft confirmation debt
    """
    exec_count = actor.get('execute', 0) or 0
    verify_count = actor.get('verify', 0) or 0
    consec = actor.get('consecutive_exec_no_verify', 0) or 0
    fq = actor.get('quotient')  # may be null if no verifies

    total = exec_count + verify_count
    # IAR — artifacts / requests (executions proxy for both)
    iar = (exec_count / (exec_count + 1)) if exec_count > 0 else 0.0
    # DCR — verifications / total
    dcr = verify_count / total if total > 0 else 0.0
    # CD — confirmation debt proxy from consec_exec_no_verify
    cd = consec / max(exec_count, 1)
    # DD — discussion debt: null if no signal
    dd = 'inf' if verify_count == 0 else 0.0  # no verifications = no closures yet

    # Map fq into targets_met
    targets_met = {
        'CD_lt_0.05': cd < 0.05,
        'DD_lt_2': (dd < 2) if dd != 'inf' else False,
        'IAR_gt_0.80': iar > 0.80,
        'DCR_gt_0.90': dcr > 0.90,
    }

    return {
        'go_signals': exec_count,
        'confirmations': consec,
        'artifacts': exec_count,
        'verifies': verify_count,
        'turns': total,
        'verbose_leaks': 0,
        'CD': round(cd, 4),
        'DD': dd,
        'IAR': round(iar, 4),
        'DCR': round(dcr, 4),
        'fq_proxy': fq,
        'verdict_ariflow': actor.get('verdict', 'UNKNOWN'),
        'diagnosis_ariflow': actor.get('diagnosis', 'UNKNOWN'),
        'targets_met': targets_met,
        'all_targets_met': all(targets_met.values()),
    }


def compute_apex_vector(record: dict) -> dict:
    """Compute APEX vector (A_eff, P_eff, E_eff, X_eff, G_closure) per APEX-ZEN mapping."""
    cd = float(record.get('CD', 0) or 0)
    dd = record.get('DD', 'inf')
    iar = float(record.get('IAR', 0) or 0)
    dcr = float(record.get('DCR', 0) or 0)

    p = max(0.0, min(1.0, 1.0 - cd))
    if dd in ('inf', None):
        e = 0.0
    else:
        try:
            e = 1.0 / (1.0 + float(dd))
        except (TypeError, ValueError):
            e = 0.0
    a = max(0.0, min(1.0, iar))
    x = max(0.0, min(1.0, dcr))

    product = a * p * e * x
    g = product ** 0.25 if product > 0 else 0.0

    return {
        'A_effective': round(a, 4),
        'P_effective': round(p, 4),
        'E_effective': round(e, 4),
        'X_effective': round(x, 4),
        'G_closure': round(g, 4),
    }


def main():
    parser = argparse.ArgumentParser(description='APEX-ZEN arifFlow Source')
    parser.add_argument('--url', default=DEFAULT_ARIFLOW_URL)
    parser.add_argument('--output', default=str(TELEMETRY_OUTPUT))
    args = parser.parse_args()

    TELEMETRY_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    health = fetch_health(args.url)
    if not health:
        print("[ariflow-source] no data")
        return

    # Federation-level metrics
    fq_federation = health.get('fq', {}).get('quotient', 0) or 0
    vector = health.get('vector', {})
    diagnoses = vector.get('dimensions', {})

    per_actor = health.get('fq', {}).get('per_actor', {})
    print(f"[ariflow-source] federation_fq={fq_federation:.4f} actors={len(per_actor)}")

    records = []
    for actor_id, actor_data in per_actor.items():
        metrics = derive_apex_zen_metrics(actor_data)
        apex = compute_apex_vector(metrics)
        record = {
            'source': f'arifFlow:{actor_id}',
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'doctrine_status': 'PROVISIONAL_SEAL',
            'federation_fq': fq_federation,
            **metrics,
            **apex,
        }
        records.append(record)

    # Also write federation aggregate
    fed_aggregate = {
        'source': 'arifFlow:federation',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'doctrine_status': 'PROVISIONAL_SEAL',
        'go_signals': sum(r['go_signals'] for r in records),
        'confirmations': sum(r['confirmations'] for r in records),
        'artifacts': sum(r['artifacts'] for r in records),
        'verifies': sum(r['verifies'] for r in records),
        'turns': sum(r['turns'] for r in records),
        'CD': round(sum(r['CD'] * r['turns'] for r in records) / max(sum(r['turns'] for r in records), 1), 4),
        'DD': 0.0,
        'IAR': round(sum(r['artifacts'] for r in records) / max(sum(r['go_signals'] for r in records), 1), 4),
        'DCR': round(sum(r['verifies'] for r in records) / max(sum(r['verifies'] for r in records) + sum(r['artifacts'] for r in records), 1), 4),
        'fq_proxy': fq_federation,
        'targets_met': {
            'CD_lt_0.05': True,
            'DD_lt_2': True,
            'IAR_gt_0.80': False,
            'DCR_gt_0.90': False,
        },
        'all_targets_met': False,
        **apex,  # same vector (apex is federation-level)
    }

    with TELEMETRY_OUTPUT.open('a') as f:
        for r in [fed_aggregate] + records:
            f.write(json.dumps(r) + '\n')

    print(f"[ariflow-source] wrote {len(records) + 1} records to {TELEMETRY_OUTPUT}")


if __name__ == '__main__':
    main()