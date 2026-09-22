# Portfolio Sweep — Handoff Matrix Template

Drop-in template for Phase 4. Replace placeholders with live repo data; one matrix per repo.

## Pre-handoff checklist

Before presenting to the sovereign:

- [ ] All five Phase 0 checks completed and recorded (protection, settings, inventory, CI, branches).
- [ ] Combined-state validation run; required check passes; regression delta vs main baseline.
- [ ] Each PR's risk class assigned (SAFE / REVIEW / BLOCK) with the reason.
- [ ] Stale branch classification complete (delete / keep / block).
- [ ] One binary per line; no compound questions.

## Template

```
================================================================
<REPO> PORTFOLIO SWEEP — <DATE>
================================================================

SUBSTRATE STATE (Phase 0)
  Branch protection requires: <context list or "(none)">
  allow_auto_merge: <true|false>
  Open PRs: <N>  |  Active branches: <N>
  CI failures on main baseline: <count>  (pre-existing, out of scope)
  Combined-stack regression delta: <count>  (added by PRs vs main)

STOP THE BLEED (Phase 1)
  1.A  Repo setting: <defect name>                  [YES/NO]
  1.B  Missing dep: <package> = <version>            [YES/NO]
  1.C  Pre-existing failure fix: <name>              [YES/NO]

MERGE QUEUE (Phase 3, ordered bijaksana tertib)
  #<N>  <title>  [risk]  <reason>                    [YES/NO/HOLD]
  ...

CLEANUP (Phase 3 final)
  Delete <branch>: <reason>                          [YES/NO]
  Block   <branch>: <reason>                         [YES/NO]

RECEIPT (Phase 5)
  Write ledger + claim_record + TG summary           [YES/NO]

================================================================
ANSWER: write YES/NO/HOLD on each line, send back. I execute in one batch.
================================================================
```

## Worked example (from a real sweep)

```
================================================================
GEOX PORTFOLIO SWEEP — 2026-09-22
================================================================

SUBSTRATE STATE (Phase 0)
  Branch protection requires: uv lock --check && uv sync --frozen (1 check)
  allow_auto_merge: FALSE   ← weekly cadence silently broken
  Open PRs: 7  |  Active branches: 10
  CI failures on main baseline: 6 collection errors (httpx2 undeclared, Aug 3)
  Combined-stack regression delta: 0 (failures identical to baseline)

STOP THE BLEED (Phase 1)
  1.A  Flip allow_auto_merge=true                   [YES]
  1.B  Add httpx2>=2.9.1,<3.0 to pyproject          [YES]

MERGE QUEUE (Phase 3)
  #169  ImgBot optimize (RGBA->RGB, verified lossless)         [YES]
  #170  Dependabot uv/dask 2026.7.1->2026.8.0                  [YES]
  #171  Dependabot uv/numba 0.66.0->0.67.0                      [YES]
  #172  Dependabot uv/holoviews 1.23.1->1.23.2                  [YES]
  #173  Dependabot uv/devito 4.8.22->4.8.23                     [YES]
  #174  Dependabot uv/panel 1.9.3->1.9.4                        [YES]
  #178  Bump actions/checkout v4->v7, setup-python v5->v7       [YES]

CLEANUP
  Delete docs/federation-plane-alignment-2026-09-14 (work landed)   [YES]
  Delete feature/evidence-spine-calibration-20260915 (already in main)[YES]
  Block feat/mcp-dual-era-2026-07-28 (1.5M lines untracked scratch) [YES: keep branch, add protection]

RECEIPT
  Write ledger + claim_record + TG summary                [YES]

================================================================
ANSWER: write YES/NO/HOLD on each line, send back. I execute in one batch.
================================================================
```

## Anti-patterns in the handoff

- **Asking multiple questions on one line.** "Merge 178 and flip auto-merge?" is two
  decisions collapsed; split them.
- **Hiding the baseline number.** If main has 6 pre-existing failures and the sweep adds
  0, say so. Hiding the baseline makes the sweep look like it added regressions.
- **Recommending actions the sovereign already vetoed.** Re-check prior session history
  (carry_forward or session_search) before recommending a delete or a setting flip.
- **Skipping the receipt line.** A sweep without a ledger is hearsay within a session.
