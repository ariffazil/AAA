# APEX-ZEN TOP-20 Highest Leverage Fixes — 2026-09-13

> **Authority:** ARIF (F13 SOVEREIGN)
> **Source audit:** `/root/AAA/reports/APEX-ZEN-ALIGNMENT-AUDIT-2026-09-13.md`
> **Doctrine:** `/root/AAA/governance/APEX-ZEN-EXECUTION-DOCTRINE.md`
> **Ranking:** Impact × (1 / Complexity) × (1 / Risk) × Expected DD reduction

---

## Ranking methodology

- **Impact (I):** How much the fix shifts agent runtime behavior. 1–5.
- **Complexity (C):** Effort to implement. 1–5 (5 = hardest).
- **Risk (R):** Probability of breaking other systems. 1–5 (5 = highest).
- **DD Reduction:** Estimated reduction in Discussion Debt (turns before artifact).
- **Score:** `I × (6 − C) × (6 − R) × DD_Reduction`

---

## TOP 20 Fixes

### Tier 1 — Critical (highest score, do first)

#### #1 — Wire APEX-ZEN telemetry to live session logs

- **What:** Cron job every 5min scans `/root/.kimi-code/sessions/` for new JSONL; runs `apex-zen-telemetry.py`; appends to `/root/VAULT999/apex-zen-telemetry.jsonl`.
- **Impact:** 5 — primary measurement loop unblocked.
- **Complexity:** 2 — small script + cron entry.
- **Risk:** 1 — read-only on sessions.
- **DD Reduction:** 3 turns (per session).
- **Owner:** A-FORGE forge agent.
- **Effort:** ~30 min.

#### #2 — Build APEX-ZEN consequence router

- **What:** `/root/AAA/scripts/apex-zen-consequence-router.py` reads telemetry JSONL, maps values to severity tiers per ladder, emits receipts + applies runtime restrictions.
- **Impact:** 5 — closes the loop (Layer 4 done).
- **Complexity:** 3 — state machine + receipt emission.
- **Risk:** 2 — could emit false-positive restrictions; reversible.
- **DD Reduction:** 2 turns (auto-correction on warning).
- **Owner:** 333-AGI.
- **Effort:** ~2 hours.

#### #3 — Purge 5 active memory files with confirmation anti-patterns

- **What:** Rewrite or delete the 5 files identified in audit Section 2:
  - `/root/AAA/workspace/memory/2026-04-04-sovereign-architect.md` L101
  - `/root/AAA/memory/2026-05-11-1824.md` L109
  - `/root/AAA/memory/2026-05-13-disk-reclaim-safe.md` L39
  - `/root/AAA/memory/2026-06-06-1254.md` L328
  - `/root/AAA/memory/2026-06-06-0248.md` L126
- **Impact:** 4 — removes pattern reinforcement in active code.
- **Complexity:** 1 — file edits.
- **Risk:** 1 — archive before delete.
- **DD Reduction:** 1 turn per affected context.
- **Owner:** A-FORGE.
- **Effort:** ~15 min.

### Tier 2 — High leverage

#### #4 — Add AZ_SCORE pre-check to Hermes response loop

- **What:** Integrate `apex-zen-score.py` as pre-send check in hermes harness. If AZ_SCORE < 0.5, regenerate.
- **Impact:** 4 — runtime enforcement of doctrine.
- **Complexity:** 4 — harness integration.
- **Risk:** 3 — could slow responses; reversible.
- **DD Reduction:** 2 turns.
- **Owner:** Hermes daemon team.
- **Effort:** ~1 day.

#### #5 — Map arifFlow FQ → APEX-ZEN DCR dashboard

- **What:** Grafana panel showing FQ alongside APEX-ZEN metrics. Single pane of glass.
- **Impact:** 3 — visibility.
- **Complexity:** 2 — Grafana config.
- **Risk:** 1 — read-only.
- **DD Reduction:** N/A (observability).
- **Owner:** observability team.
- **Effort:** ~30 min.

#### #6 — Document "Default-ACT reflex" as canonical pattern

- **What:** `/root/AAA/instructions/default-act-reflex.md` — when intent clear, execute highest-confidence safe action. Reference from AAA-ZEN-ALIGNMENT.
- **Impact:** 3 — explicit doctrine artifact.
- **Complexity:** 1 — write doc.
- **Risk:** 1 — additive.
- **DD Reduction:** N/A (training material).
- **Owner:** 333-AGI.
- **Effort:** ~20 min.

#### #7 — Replace confirmation patterns in ARIFOS_FEDERATION_INIT.md

- **What:** Audit `/root/AAA/prompts/ARIFOS_FEDERATION_INIT.md` for "shall i", "would you like", etc. Replace with default-ACT.
- **Impact:** 3 — boot prompt sets initial posture.
- **Complexity:** 1 — text edits.
- **Risk:** 1 — additive.
- **DD Reduction:** 0.5 turn per boot.
- **Owner:** 333-AGI.
- **Effort:** ~10 min.

#### #8 — Add anti-tangguh check to all INIT prompts

- **What:** Edit `/root/AAA/prompts/INIT*.md` to prepend Anti-Tangguh Check as pre-flight.
- **Impact:** 3 — every agent session starts with the check.
- **Complexity:** 1 — additive.
- **Risk:** 1 — additive.
- **DD Reduction:** 1 turn per session.
- **Owner:** 333-AGI.
- **Effort:** ~20 min.

### Tier 3 — Medium leverage

#### #9 — Retire `/root/AAA/skills/hermes-telegram-stack-zen` if redundant

- **What:** Check if duplicate of `/root/.kimi-code/skills/hermes/SKILL.md`. Consolidate.
- **Impact:** 2 — reduces skill catalog noise.
- **Complexity:** 2 — audit + retire.
- **Risk:** 2 — could break consumers.
- **DD Reduction:** 0 (clarity).
- **Owner:** skill-mesh.
- **Effort:** ~1 hour.

#### #10 — Build "Tangguh Budget" per-session counter

- **What:** Track confirmations per session; if > 3, emit warning to user.
- **Impact:** 2 — early warning.
- **Complexity:** 2 — small script.
- **Risk:** 1 — additive.
- **DD Reduction:** N/A (metric).
- **Owner:** observability.
- **Effort:** ~30 min.

#### #11 — Replace verbose-default patterns in ARIFOS_FEDERATION_INIT

- **What:** Audit init prompts for "Let me first explain", "Generally speaking", etc. Replace with direct.
- **Impact:** 2 — boot posture.
- **Complexity:** 1 — text edits.
- **Risk:** 1.
- **DD Reduction:** 0.5 turn per boot.
- **Owner:** 333-AGI.
- **Effort:** ~10 min.

#### #12 — Add AZ-5 register rule to AAA-ZEN-ALIGNMENT.md

- **What:** Reference APEX-ZEN register rule from AAA-ZEN-ALIGNMENT (already a 18-rule file).
- **Impact:** 2 — cross-link.
- **Complexity:** 1 — text edit.
- **Risk:** 1.
- **DD Reduction:** N/A.
- **Owner:** 333-AGI.
- **Effort:** ~5 min.

#### #13 — Build session-end AZ_SCORE summary

- **What:** On session close, run scorer on all responses, emit aggregate AZ_SCORE to carry_forward.
- **Impact:** 2 — session-level metric.
- **Complexity:** 2 — hook into close.
- **Risk:** 1 — additive.
- **DD Reduction:** N/A (metric).
- **Owner:** A-FORGE.
- **Effort:** ~1 hour.

#### #14 — Update SPEC files to reference APEX-ZEN

- **What:** Add APEX-ZEN pointer to `/root/AAA/docs/*.md` SPEC files.
- **Impact:** 1 — discoverability.
- **Complexity:** 1 — text edits.
- **Risk:** 1.
- **DD Reduction:** N/A.
- **Owner:** 333-AGI.
- **Effort:** ~15 min.

### Tier 4 — Maintenance

#### #15 — Archive superseded APEX-ZEN v1.0 drafts

- **What:** Move `/root/AAA/governance/APEX-ZEN-INIT-v1.1.md` and `/root/AAA/governance/APEX_ZEN_EXECUTION_DOCTRINE_v1.md` to `.archive/` if superseded.
- **Impact:** 1 — clarity.
- **Complexity:** 1 — file move.
- **Risk:** 1.
- **DD Reduction:** N/A.
- **Owner:** 333-AGI.
- **Effort:** ~5 min.

#### #16 — Add APEX-ZEN to canonical glossary

- **What:** Update `/root/AAA/canon/CANONICAL_GLOSSARY.md` with APEX-ZEN entry.
- **Impact:** 1 — discoverability.
- **Complexity:** 1.
- **Risk:** 1.
- **DD Reduction:** N/A.
- **Owner:** 333-AGI.
- **Effort:** ~5 min.

#### #17 — Build `apex-zen-conformance-test.py`

- **What:** Unit test that verifies APEX-ZEN scripts run correctly on synthetic inputs.
- **Impact:** 1 — regression prevention.
- **Complexity:** 2.
- **Risk:** 1.
- **DD Reduction:** N/A.
- **Owner:** A-FORGE.
- **Effort:** ~1 hour.

#### #18 — Document AZ_SCORE thresholds in skills

- **What:** Update skill descriptions to mention APEX-ZEN scoring.
- **Impact:** 1.
- **Complexity:** 2.
- **Risk:** 1.
- **DD Reduction:** N/A.
- **Owner:** 333-AGI.
- **Effort:** ~30 min.

#### #19 — Add APEX-ZEN to federation-discovery contract

- **What:** `/root/AAA/governance/FEDERATION-DISCOVERY-INSTANTIATION-SPEC-2026-09-12.md` reference APEX-ZEN.
- **Impact:** 1.
- **Complexity:** 1.
- **Risk:** 1.
- **DD Reduction:** N/A.
- **Owner:** 333-AGI.
- **Effort:** ~5 min.

#### #20 — Build APEX-ZEN weekly digest

- **What:** Cron weekly: aggregate telemetry, emit summary to `/root/AAA/reports/apex-zen-weekly-YYYY-MM-DD.md`.
- **Impact:** 1 — visibility.
- **Complexity:** 2.
- **Risk:** 1.
- **DD Reduction:** N/A.
- **Owner:** observability.
- **Effort:** ~1 hour.

---

## Recommended execution order

| Order | Fix | Tier | Effort |
|-------|-----|------|--------|
| 1 | #3 (purge memory) | 1 | 15 min |
| 2 | #1 (wire telemetry) | 1 | 30 min |
| 3 | #6 (default-ACT doc) | 2 | 20 min |
| 4 | #8 (anti-tangguh in INIT) | 2 | 20 min |
| 5 | #7 (replace confirmations in INIT) | 2 | 10 min |
| 6 | #2 (consequence router) | 1 | 2 hours |
| 7 | #4 (AZ_SCORE pre-check) | 2 | 1 day |
| 8 | #5 (FQ→DCR dashboard) | 2 | 30 min |
| 9 | rest | 3–4 | variable |

**Total Tier 1+2 effort:** ~5 hours.
**Expected DD reduction after full implementation:** 60–70%.

---

*Forged 2026-09-13. Source: APEX-ZEN Alignment Audit.*