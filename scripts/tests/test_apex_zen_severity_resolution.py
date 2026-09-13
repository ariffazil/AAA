#!/usr/bin/env python3
"""
Regression tests for APEX-ZEN preflight severity resolution.

Closes the defect found 2026-09-13 (FI-008):
  UNKNOWN was ranked ABOVE VIOLATION in the ordinal ladder used to pick an
  actor's `worst_severity`. Consequence: a metric with no reading (e.g. DD='inf')
  masked a measured VIOLATION on another metric (CD/DCR). 7 of 24 actors were
  affected, including arifFlow:arif.

Invariants asserted here:
  INV-1  A missing metric must never outrank a measured severity.
  INV-2  If no metric has a verdict, severity is UNKNOWN (no invented verdict).
  INV-3  Non-actor sources (collector artifacts) stay out of the namespace.
  INV-4  A compliant actor is unaffected.
  INV-5  per_metric_severity + metrics_missing are emitted, so any consumer can
         see which metric produced the verdict and which were unmeasurable.

Run:  python3 /root/AAA/scripts/tests/test_apex_zen_severity_resolution.py
Exit: 0 = pass, 1 = fail.
"""
import importlib.util
import json
import pathlib
import sys
import tempfile

ROUTER = pathlib.Path('/root/AAA/scripts/apex-zen-consequence-router.py')


def load_router():
    spec = importlib.util.spec_from_file_location('router', ROUTER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def record(source, CD, DD, IAR, DCR, ts='2026-09-13T00:00:00Z'):
    return {'source': source, 'CD': CD, 'DD': DD, 'IAR': IAR, 'DCR': DCR,
            'timestamp': ts}


def main() -> int:
    r = load_router()
    tmp = pathlib.Path(tempfile.mkdtemp()) / 'preflight.json'
    r.PREFLIGHT_OUTPUT = tmp

    r.write_preflight_scores([
        record('arifFlow:mask-test', 0.70, 'inf', 0.95, 0.30),   # CD VIOLATION, DD unmeasurable
        record('arifFlow:all-unknown', None, None, 'N/A', 'inf'),  # genuinely no verdict
        record('stdin', 0.70, 'inf', 0.95, 0.30),                # non-actor
        record('arifFlow:clean', 0.01, 2, 0.99, 0.95),           # compliant
    ])
    out = json.load(tmp.open())

    failures = []

    def check(name, cond, detail=''):
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}{(' — ' + detail) if detail else ''}")
        if not cond:
            failures.append(name)

    print("=== APEX-ZEN severity resolution ===")

    m = out['arifFlow:mask-test']
    check('INV-1 masking: measured VIOLATION survives an unmeasurable sibling metric',
          m['worst_severity'] == 'VIOLATION',
          f"worst_severity={m['worst_severity']}")
    check('INV-5 provenance emitted',
          m['per_metric_severity'].get('CD') == 'VIOLATION'
          and m['metrics_missing'] == ['DD']
          and m['severity_reliable'] is False,
          f"missing={m['metrics_missing']}")

    u = out['arifFlow:all-unknown']
    check('INV-2 no verdict invented when nothing is measurable',
          u['worst_severity'] == 'UNKNOWN' and u['restriction'] == 'no_verdict',
          f"worst_severity={u['worst_severity']}")

    check('INV-3 non-actor source excluded from enforcement namespace',
          'stdin' not in out,
          f"keys={sorted(out)}")

    c = out['arifFlow:clean']
    check('INV-4 compliant actor unaffected',
          c['worst_severity'] == 'COMPLIANT' and c['restriction'] == 'none',
          f"worst_severity={c['worst_severity']}")

    print(f"\n{'ALL PASS' if not failures else 'FAILURES: ' + ', '.join(failures)}")
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
