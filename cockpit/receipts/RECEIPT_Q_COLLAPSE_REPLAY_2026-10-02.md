# RECEIPT — Q_COLLAPSE Executable Contract Replay v0
**Date:** 2026-10-01T22:35:53Z
**Lane:** B (harness + replay, no production wiring)
**Hash:** 329dfa7c7bac7cb1d7ca09cf6152b089361c0a4f405a00fab7b8ede86bf506b9

## 3 Replay Cases (sOVEREIGN spec)
| Case | Input | Required output | Got |
|---|---|---|---|
| T1 deterministic | 1 bug + 1 reversible fix | ONE ACTION | ✓ ACTION / apply_the_verified_reversible_fix / conf=1.0 |
| T2 uncertain+reversible | 2 hypotheses ΔU≈0 | ONE INFORMATION-GAIN PROBE | ✓ PROBE / run_smallest_discriminating_probe / conf=0.7 |
| T3 human sovereignty | genuine value at stake | HOLD + ONE QUESTION | ✓ HOLD / HOLD_pending_sovereign_decision / conf=0.0 |

## 2 Math Corrections Applied (per sovereign 2026-10-02)
1. APEX canonical  (4 dials) — F13-frozen, never modified
2. Decision space  — separate math object, NOT to be confused with APEX G

Q-COLLAPSE consumes APEX gate verdict; never recomputes or replaces it.

## What Did NOT Happen (held sovereign lane)
- No arifOS canonical organ wire
- No production hook
- No cron
- No AGENTS.md mutation
- No /opt touched
- No "sync all agents"
- Stage 1-14 implementation deferred until replay contract validated

## Path Forward (per sovereign)
1. Run 3-case replay to validate contract
2. Shadow-mode deployment: Q-COLLAPSE predicts path silently while existing agents continue
3. CHRON compares collapsed choice vs actual outcomes
4. Only after calibration → live AAA decision membrane

## Reversibility
- Single file: rm /root/AAA/cockpit/q-collapse-harness.py + rm q-collapse-replay.json
- No other side effects
