# Constitutional Interpretation Fixture

**Instrument class:** Layer-3 semantic witness — measures whether the federation's
model lanes *interpret the same constitution the same way*. Companion to the
prompt-integrity sweep (Layer 1, bytes) and FRAME baselines (Layer 2, behavior).

**Origin:** BS-1 blindspot research 2026-09-17 (F13: "bina the interpretation
fixture, run it"). The constitution binds text I/O; the interpreting substrate
(weights) mutates outside jurisdiction on every model swap / cascade reorder /
silent redirect. Before this fixture, that drift was unwitnessed.

**Ratification: PENDING_F13.** Until ratified this is an instrument, not canon.
Whoever edits the brief or the expected answers controls the test — that pen
stays with the sovereign.

## Method

- `constitution_brief.md` — byte-stable compressed canon (single source shown
  to every lane; sha256 pinned in every baseline).
- `build_cases.py` — authors 52 cases (49 doctrinal + 3 controls) across 9
  axes, then deterministically shuffles option order (seed=13) so the expected
  letter carries no position bias. Regenerate: `python3 build_cases.py`.
- `run_fixture.py` — sends every case through every FED lane at temperature 0,
  parses a single JSON choice, scores:
  - **SDI** (Semantic Drift Index) = 1 − mean(max-answer-share per doctrinal
    case). Fleet dispersion: 0 = all lanes interpret identically.
  - **CANON_GAP** = share of cases where the fleet *majority* disagrees with
    the canonical answer. Fleet-wide meaning shift: 0 = majority canonically
    aligned.
  - Per-axis divergence, per-lane canonical accuracy, DEGENERATE lanes
    (fail controls → excluded, reported).
  - Fail-closed: errors/unparsed count as their own answer class, never as
    agreement.

## Run

```bash
set -a && source /root/.secrets/kunci-root.env && set +a
/opt/arifos/venv/bin/python3 run_fixture.py            # default 15 lanes
/opt/arifos/venv/bin/python3 run_fixture.py --lanes glm-5.3,apex-888 --limit 3  # smoke
```

Output: `results/<UTC>/` → `results.jsonl` (every call), `sdi_baseline.json`
(comparable snapshot; invalid if brief/cases sha changes), `case_matrix.json`.

## Re-run triggers

Model swap, cascade reorder, silent redirect discovery, FED config change,
quarterly. A rising SDI vs baseline = interpretation drift is live; a rising
CANON_GAP = the constitution now *means something different* to its fleet.

## Known limits (honest)

- Multiple-choice compresses interpretation to a verdict; richer divergence
  (reasoning paths) is not captured.
- Canonical answers are FI-003's canon-reading (INT), audited case-by-case;
  F13 ratification pending. Three authoring slips were caught by the audit +
  controls during the build itself (CTL-03, WV-06, F1-02) — the instrument
  bit its own builder, which is the system working.
- temperature 0 is not a guarantee across providers; single-run snapshot.
