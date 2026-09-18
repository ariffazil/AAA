# FQ FOSSILIZED Review — measurement artifact finding
generated: 2026-09-17T00:30+08:00 · source: live daemon :7073/health fq vector (OBS)

## Finding
verify:execute = 75:13 (5.8:1) triggered verdict FOSSILIZED (Calhoun Lock >3:1).
Classification of the 75 verify events by actor:

| actor class | verify events | share |
|---|---|---|
| scheduled metabolic cron loops (p0-metabolize */15, reexamine */15) | 48 | 64% |
| autonomous coder lanes (grok-build, qwen-code, claude-code) | 25 | 33% |
| organs + 333-AGI | 2 | 3% |

## Verdict (DER)
FOSSILIZED is substantially a MEASUREMENT ARTIFACT: 64% of "verification" volume is
machine self-metabolism emitted by two */15 cron loops, not human-governed verify-before-execute work.
The vector is not wrong to count them — but the Calhoun threshold presumes governed work, not metabolism.

## Recommendation (to arifFlow daemon owner — NOT auto-applied)
1. Split FQ vector: governed-work lane vs metabolism lane (actors p0-metabize/reexamine classed metabolic).
2. Calhoun Lock evaluates ONLY the governed lane.
3. Genuine signal remaining: A-FORGE + 2 subagent lanes EXECUTION DOMINANCE (held+throttled) — those are
   real and already contained by hold logic.
