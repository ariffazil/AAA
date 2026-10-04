# Audit Checklist Template

Copy this checklist for any audit/validation pass. Replace placeholders with concrete values.

## Phase 1 — Artifact validation

```bash
# Audit target
DIR="/path/to/audit/target"

# Verify artifacts exist
ls -la "$DIR"
wc -l "$DIR"/*.md
md5sum "$DIR"/*.md
```

Expected output:
```yaml
artifact_validation:
  pass:
    - directory_exists: <DIR>
    - deliverable_files_present:
        - 01_<name>.md (<bytes>, <lines>, md5=<hash>)
        - ...
  fail:
    - MISSING: <file>
    - DISCREPANCY: <count_drift>
  warnings:
    - WARN-01: <author or framing issue>
```

## Phase 2 — Deliverable quality review

For each deliverable, check:

| Check | Status | Evidence |
|---|---|---|
| Components actually exist | ✅ / ❌ | <probe> |
| Connections are real | ✅ / ❌ | <file:line> |
| No invented systems | ✅ / ❌ | <scan> |
| No duplicate inventory | ✅ / ❌ | <count> |
| Transformations accurate | ✅ / ❌ | <reasoning> |
| Loss analysis reasonable | ✅ / ❌ | <loss_matrix> |
| No unsupported assumptions | ✅ / ❌ | <grep> |
| Every gap supported by evidence | ✅ / ❌ | <gap_table> |
| No hypothetical gap as fact | ✅ / ❌ | <verifiability> |
| Schema compiles (if claimed) | ✅ / ❌ | <jsonschema_run> |
| Types consistent | ✅ / ❌ | <enum_check> |
| Migration syntactically valid | ✅ / ❌ | <migration_test> |
| Backwards compatibility checked | ✅ / ❌ | <old_loader_test> |
| Conflict resolution coherent | ✅ / ❌ | <types_and_rules> |
| Confidence logic internally consistent | ✅ / ❌ | <math_check> |
| No circular scoring | ✅ / ❌ | <dependency_graph> |
| Dependencies correct | ✅ / ❌ | <manifest> |
| Ordering sensible | ✅ / ❌ | <walk> |
| Quick wins realistic | ✅ / ❌ | <cost_check> |
| No hidden prerequisites | ✅ / ❌ | <transitive_check> |

## Phase 3 — Evidence audit (F-claim classification)

For every major finding, log:

```yaml
- id: F1
  finding: <one sentence>
  evidence_location: <file:line or URL>
  confidence: HIGH | MEDIUM | LOW
  status: ✅ verified | ⚠️ drift | ❌ rejected
```

## Phase 4 — Independent re-probe (20% sample)

```yaml
re_probe_sample:
  - finding: F1
    re_probe_result: <live observation>
    match: true | false
  ...
agreement_rate: <X>/<Y> = <Z>%
```

## Phase 5 — Hallucination audit

```yaml
hallucination_risk:
  overall: none | low | medium | high

  paths:
    claimed: N
    missing: 0
    drifted: 0

  services:
    claimed: N
    verified: N
    invented: 0

  counts:
    claimed_X: <value>
    actual: <value>
    drift: <delta>

  warnings:
    - <framing mistakes>
    - <unverified inferences>
```

## Phase 6 — Seal review

Evaluate on five axes:

```yaml
factual_correctness: HIGH | MEDIUM | LOW
evidence_quality: HIGH | MEDIUM | LOW
reproducibility: HIGH | MEDIUM | LOW
operational_usefulness: HIGH | MEDIUM | LOW
migration_safety: HIGH | MEDIUM | LOW
```

Issue ONE verdict:

```yaml
seal_verdict: SEAL | PARTIAL | HOLD | VOID

justification:
  - factual_correctness: <how determined>
  - evidence_quality: <how determined>
  - reproducibility: <how determined>
  - operational_usefulness: <how determined>
  - migration_safety: <how determined>

upgrade_to_seal_conditions:
  - <specific action 1>
  - <specific action 2>
  - sovereign review
```

## Required output artifacts

For every audit pass:
1. `07_validation_report.md` — Phase 1-2 quality review
2. `08_evidence_matrix.md` — Phase 3-5 claim-by-claim matrix
3. `09_seal_review.md` — Phase 6 final verdict

Plus, if missing from the audited deliverable set:
- `SUMMARY.md` — top-level orientation
- Renamed/bannered files where framing was wrong
