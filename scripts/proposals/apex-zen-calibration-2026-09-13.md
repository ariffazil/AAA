# APEX-ZEN Calibration Review — 2026-09-13

**Analyst:** 333-AGI · **Trigger:** "12 VIOLATION / 7 DOWNGRADE" preflight histogram
**Evidence base:** 837 telemetry rows · 24 actors · 37 cycles (freshest live run 21:25 MYT)

## 1. Evidence

**Sustained false-flag pattern (formula artifact, not actor conduct):**

| Actor | CD median (37 cyc) | DCR median | Interpretation |
|---|---|---|---|
| `arifFlow:arif` | **1.0 ×37** | **0.0 ×37** | max confusion every cycle — no signal basis |
| `arifFlow:333-AGI/agentic-web` | 1.0 ×37 | 0.0 ×37 | same |
| `arifFlow:333-AGI/dynamic-gate` | 1.0 ×37 | 0.0 ×37 | same |
| `arifFlow:grok-build/FI-007` | 1.0 ×37 | 0.0 ×37 | same |
| `arifFlow:codex` / `codex-startup` | 1.0 ×22 | 0.0 ×22 | same |
| `arifFlow:qwen-code/FI-003` | 1.0 ×37 | 0.889 | CD artifact only |

**Healthy separation exists (metrics discriminate when inputs are present):**
`333-AGI` CD 0.0 / DCR 0.727 · `federation` 0.04 / 0.456 · `a-forge` 0.0 / 0.942 · `grok-build` 0.0 / 0.929 · `hermes-asi` 0.002 / 0.294

**Additional findings:**
- Non-actor `stdin` present in telemetry (16 rows) — must never enter the actor namespace.
- Receipts carry **no `receipt_id`** → ~1,024 receipts/cycle reprocessed from the 1h window (~12× duplication), `receipts.jsonl` growing ~86 MB/day.

## 2. Root cause

CD/DCR default to the worst value (1.0 / 0.0) when the required signal shape is absent, instead of UNKNOWN. The ordering fix (`b20018017`) stopped UNKNOWN from *masking* a measured violation — but "absent basis" is still being *reported* as a measured worst.

## 3. Proposed rules (calibration v1)

- **R1 basis-gate:** CD is computed only with ≥2 distinct signal inputs; otherwise UNKNOWN (never 1.0).
- **R2 namespace:** only registered actors; collector artifacts (`stdin`, file paths) excluded from telemetry verdicts.
- **R3 confidence:** an enforcement-grade verdict requires ≥3 measurable cycles; otherwise `PROVISIONAL`.
- **R4 spike guard:** VIOLATION requires the flag in ≥2 consecutive cycles (or median-based classification); single-cycle spikes downgrade to `WARNING(spike)`.
- **R5 receipts:** `receipt_id = sha256(source|metric|value|timestamp)[:16]`; dedup via index; daily rotation.

Router already emits `per_metric_severity` + `metrics_missing` (INV-5) — R1/R4 need `cd_basis` and `consecutive_flags` added to the record.

## 4. Enforcement ladder (per gate-promotion.md)

```
OBSERVE_ONLY (current — honest, no consumer)
  → ANNOUNCE  (restrictions emitted to receipts/logs; no blocking)
  → GATE      (block MUTATE for VIOLATION actors; UNKNOWN → most-restrictive only for KNOWN actors)
```

- **To ANNOUNCE:** R1–R4 land; false-flag count = 0 across 12 consecutive cycles.
- **To GATE:** ANNOUNCE shows zero false positives over 7 days and ≥1 genuine catch.

## 5. Ownership

- Router + tests: FI-008 wave (active, last edit 21:31).
- Verification + proposal: 333-AGI (this document).
- No edits made to hot files — collision avoidance while FI-008 holds the pen.

## 6. Deliverables

- This proposal: `proposals/apex-zen-calibration-2026-09-13.md`
- Ready-to-apply dedup patch: `proposals/apex-zen-receipts-dedup-2026-09-13.patch` (4 hunks; py_compile OK; `patch -p1 --dry-run` valid). Adds `receipt_id = sha256(source|timestamp|metric|value)[:16]`, index-based dedup, skip-count print.
- Apply when FI-008 hands off: `cd /root/AAA/scripts && patch -p1 -i proposals/apex-zen-receipts-dedup-2026-09-13.patch`

> **UPDATE 22:06** — SUPERSEDED. FI-008 implemented a superior fix at 22:05:55: change-detection watermark (`apex-zen-receipts.state.json`, emit-once-per-signal, `--snapshot` escape), with measured evidence (27,280 rows / 116 distinct signals / 99.6% redundant / ~74MB/day / disk 79%). This patch was never applied; retired to `.SUPERSEDED-by-fi008-watermark`.

> **UPDATE 22:11 — DEDUP VERIFIED LIVE.** The 22:10 cycle emitted **1 receipt** (active signals 123, new 1, suppressed 1409) vs ~1,316/cycle before. Disk bleed (was ~74MB/day at 79% full) collapses to change-only. FI-008 fix confirmed superior; my patch retired.

> **UPDATE 22:16 — SECOND ARTIFACT CLASS (namespace).** Verified the ladder is internally consistent; the remaining flags are real *under the formula*. But the ANNOUNCE set still carries **non-agent labels**: `zen-code`, `zen-doctrine`, `zen-graph`, `zen-skills` (workstream keys), `p0-metabolize`, `reexamine` — 6 of 15. They have no missing metrics (so `severity_reliable` passes) yet are not consequence-bearing agents. **New rule R6:** the actor namespace must be an allow-list of registered agents; workstream/session labels require explicit registration or exclusion (extension of INV-3 beyond collector artifacts). Effective clean announce set = 9 pending R6.
