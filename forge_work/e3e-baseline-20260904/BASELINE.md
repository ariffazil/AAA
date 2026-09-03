# E3E Skill-Mesh Divergence Baseline — 2026-09-04

> Campaign: 5 canonical prompts × 7 CCC harnesses, unattended. Runner: `run_e3e*.sh` · Harness: `AAA/scripts/e3e_skill_mesh.sh`.
> Raw: `results/*.txt` · Tally: `TALLY.txt`. First divergence baseline in federation history (queue item C, SEAL-83defc58).

## Verdict (corrected)

**Cognitive divergence: NONE among answering agents — 4/4 CONVERGENT.**
qwen, kimi, opencode, codex all located both contested skills (`geox-prospect-evaluation`, `wealth-capital-primitives`) via mesh discovery. The skill mesh forged 2026-09-03 works across every harness that could run.

**Substrate divergence: 3/7 harnesses DOWN for unattended campaigns (57% mesh readiness):**

| Harness | State | Failure | Class |
|---|---|---|---|
| qwen | ✅ 7.6KB answer | — | — |
| kimi | ✅ 87KB answer | — | — |
| opencode | ✅ 76KB answer | — | — |
| codex | ✅ 104KB answer (needed `--skip-git-repo-check`) | — | flag-fixable (fixed) |
| gemini | ❌ | **429 prepayment credits depleted** (AI Studio) | BILLING |
| grok | ❌ | **402 usage balance exhausted** (Grok Build) | BILLING |
| claude | ❌ | config model `forge-777` unrecognized by CLI + max-turns | CONFIG DRIFT |

## Interpretation

1. The tally script's raw "DIVERGENT" on both skills is an artifact — error stubs counted as "missing". Corrected: discovery converges wherever cognition happens.
2. The real divergence in the FI mesh is **economic**, not architectural: two harness fronts (Google AI Studio prepay, xAI Grok Build) have depleted balances. Plus one stale model alias (`forge-777`) in claude-code config — cosmetic drift, fixable in minutes.
3. Mesh implication: unattended multi-harness campaigns (E3E quarterly, per ASI proposal Phase 3) currently degrade gracefully to 4 harnesses. Baseline recorded so the next run measures drift *of the drift*.

## Action residue (F13/money class)

- gemini + grok: balance top-up or retire-from-mesh decision (sovereign/money, not agent-fixable).
- claude `forge-777` model alias: replace with a live model in `~/.claude/settings.json` (T1, next session).

## Reproduce

```bash
cd /root/AAA/forge_work/e3e-baseline-20260904
./run_e3e_rest.sh            # or full: run_e3e.sh (with codex/gemini flags fixed)
/root/AAA/scripts/e3e_skill_mesh.sh tally results/
```
