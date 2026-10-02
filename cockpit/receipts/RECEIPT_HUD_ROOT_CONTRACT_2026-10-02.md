# RECEIPT — HUD ROOT-CONTRACT REPAIR (sovereign-ordered)
**Date:** 2026-10-02 08:14 MYT · **Session:** SEAL-e4afa0df3ca94a2c · **Actor:** kimi-code/FI-008

## Change
2 files in /root/AAA/cockpit: generate-hud-state.sh + display-hud.sh.
Backups: *.bak-presovereign2-20261002 (rollback = 2 cp).

## Substance
- ROOT CONTRACT added: BURNING / WAITING / SOURCE≠RUNTIME / FRESHNESS / LAST CONSEQUENCE.
- Truth fixes: brier key .brier→.mean_brier (0.198) · WELL ghost source well.json → /root/WELL/machine_state.json (honest —) · FRAME hardcoded age "7.8" removed, real math on key .ts (7d) · mission staleness gate >90m ⇒ "no active governed mission (exec-path stale Xm)".
- Semantic split per sovereign: canon_integrity ⊓ contradictions_observed — never conflated.
- FRESHNESS per-source (state=render · exec-path=queue age) — render freshness no longer masks source staleness.
- ZERO additions: no organ panels, no tool counts, no session counts, no per-organ verdict labels (arifOS 888 alone owns judge labels). Sensors grow, default HUD shrinks in noise.

## Verified (live render, battery)
?=0 · escape-leaks=0 · unexpanded-vars=0 · stray-zero=0 · contract 5/5 · brier=0.198 · WELL=— · frame age=7d · mission honest-stale · FRESHNESS state=0s/exec-path=108m.
Lines: 17→21 content (+4 canonical pressures, −1 derived duplicate [5b]).

## Race note
display-hud.sh was modified by parallel lane at 08:03 during this mission; edits applied on top of their current state; no conflict observed; WAITING line now surfaces the cockpit concurrent-write protection item itself.

## Prediction delta
Predicted +3–4 lines / all gates pass / no new deps — matched. Delta recorded: honest-fallback for MISSION triggered immediately (queue staler than bound) — gate working as designed.
