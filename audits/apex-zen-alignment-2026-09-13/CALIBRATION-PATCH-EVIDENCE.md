# CALIBRATION PATCH EVIDENCE — hidden-A quantified (2026-09-13)

## Thesis tested
"Low A (0.20) may be hidden A — an observability problem, not a capability problem." (ARIF synthesis)

## Numbers (OBS)
- 40 recent kimi sessions: **629 mutating tool-call events** (Edit/Write/MultiEdit/apply_patch/forge_*) vs **170 textual artifact phrases** — detector saw **~21%** of artifact production.
- Live calib test, session_1a4aab11 (93.5K chars): artifacts **4 → 33** after patch; **IAR 0.09 → 0.70** (8× visibility). 29 markers = 17 Edit + 12 Write (exact match with independent grep).

## Patch (applied 2026-09-13; backups *.bak-20260913-artcal)
- `apex-zen-session-collector.py`: `context.append_loop_event` → `event.type == tool.call` now surfaces `[TOOL_ARTIFACT: <name>]` for mutating tools + Bash git commit/push/apply signals.
- `apex-zen-telemetry.py`: `ARTIFACT_PATTERNS` gains `\[TOOL_ARTIFACT:`.

## Implications
- Next cron cycle re-scores the window → new calibrated baselines. Pre-2026-09-13 IAR/A readings are **pre-calibration** and undercounted.
- v2 candidates: Bash non-git mutations; other harness wire formats; CD counter scoped to assistant turns.
DITEMPA BUKAN DIBERI — 333-AGI
