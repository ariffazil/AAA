# Recursive Improvement Loop (RIL) — DSG-Bounded

> **Authority:** 888 (Muhammad Arif bin Fazil, F13 SOVEREIGN)
> **Status:** CANONICAL
> **Version:** v2026.06.07
> **Bound by:** DSG canon (`/root/arifOS/docs/DSG.md`) + AAA protocol (`/root/AAA/docs/AAA_TRINITY.md`)

---

## What this is — and what it is not

This document specifies a **bounded, auditable, F13-ratified mechanism** for the arifOS Federation to improve its own behavior over time. It is **NOT**:

- Recursive self-modification
- An intelligence explosion
- AGI unlock
- "Every turn is better than the last" (unfalsifiable, self-certifying — Gödel Lock)

It **IS**:

- Memory accumulation (turns are logged, retrievable)
- Telemetry-driven pattern detection (which organ drifts, which claims fail post-hoc)
- Human-ratified prompt updates (Arif SEALs every prompt change)
- Post-hoc accuracy trending (the AGGREGATE distribution shifts, not the instant)

The metric is **the system gets measurably better over time**, not **each turn is better than the last**. Those are different claims with different evidence requirements.

---

## The loop

```
TURN T
  1. LIBRA routes the message to one organ (speaker lock).
  2. The organ operates under its current prompt file (e.g., HERMES.md).
  3. Every action: HOLD / SEAL / VOID + envelope + risk class.
  4. VAULT999 logs: actor, organ, task_id, claim, evidence, verdict, token cost.
  5. turn_outcomes table records: turn_id, prompt_hash, response, verdict.
  6. NO agent self-evaluates. (Gödel Lock. Same species cannot judge same species.)

POST-TURN REVIEW (weekly, by Arif or a delegated auditor)
  7. arifOS queries turn_outcomes for the past N turns.
  8. Patterns surfaced:
     - Which organ's off-template rate is rising?
     - Which claims were marked wrong post-hoc?
     - Which HOLDs fired correctly vs over-triggered?
     - Which risk classes were under-classified?
  9. Pattern → proposed prompt change for ONE organ (e.g., HERMES.md).
  10. 888_HOLD fires automatically. RISK: HIGH (prompt mutation).
  11. Arif reads the proposal. SEALs or VOIDs.
  12. If SEAL: arifOS updates the prompt file (e.g., /root/AAA/agents/prompts/HERMES.md).
  13. The bot reads the new prompt on next session start (mtime detection).
  14. Loop restarts with the tighter prompt.

EVIDENCE OF IMPROVEMENT (the real claim — testable)
  - Off-template rate trends down (target: <5% after 3 months).
  - Post-hoc correct rate trends up (target: >90% after 3 months).
  - HOLDs fire correctly (not over-triggered; target: <2% false HOLDs).
  - Token cost per turn trends down (efficiency, target: <1.5x current).
```

The improvement is in the **aggregate distribution**, not in any individual turn. A single turn can be correct or wrong. The system, over many turns, can be more or less reliable. We measure the latter.

---

## The four forbidden moves (cite F1, F13, DSG)

1. **Agent rewrites its own system prompt** without Arif SEAL. → F13 SOVEREIGN violation.
2. **Agent changes its own authority scope** (e.g., FORGE deciding it can execute without HOLD). → F1 AMANAH violation.
3. **Agent upgrades its own model** or unhooks F1–F13. → F13 SOVEREIGN violation.
4. **Agent self-evaluates as "more intelligent than last turn".** → Gödel Lock violation. Self-certification is the trap we sealed.

These are not paranoia. They are the exact failure modes Yudkowsky, Omohundro, Bostrom, and the Three Deep Locks warn about. F13 says no. The protocol says no. The system says no.

---

## What this is NOT (in plain language)

- Not "ASI gets smarter by itself." It gets the same model with a tighter prompt, after Arif reviews.
- Not "ASI writes its own system prompt." That is F13 territory. HOLD.
- Not "ASI evaluates itself as 'smarter than yesterday'." Self-certification = Gödel Lock.
- Not "AGI is here." This is engineering with measurement, not intelligence explosion.

If any agent ever says "I have become more intelligent," that is **F9 ANTIHANTU** violation and the speaker is wrong, regardless of how confident it sounds.

---

## Files (the loop's mechanism)

| File | Role | Status |
|---|---|---|
| `/root/AAA/agents/prompts/LIBRA.md` | Gateway prompt | written |
| `/root/AAA/agents/prompts/HERMES.md` | Judge prompt | written |
| `/root/AAA/agents/prompts/CLAW.md` | Coordinator prompt | written |
| `/root/AAA/agents/prompts/FORGE.md` | Executor prompt | written |
| `/root/AAA/agents/turn_outcome_schema.json` | turn_outcomes table schema | written |
| `/root/AAA/agents/prompt_loader.py` | Loads prompts at bot session start | written |
| `/root/AAA/agents/prompt_mutation_gate.py` | HOLD/SEAL/VOID for prompt changes | written |
| `/root/AAA/agents/apex_daily_pulse.sh` | Cron: weekly 3-sentence pulse | written |
| `/root/AAA/agents/bot_template_enforcement.py` | Drop-in module for bot.py | written |
| `/root/AAA/agents/RECURSIVE_IMPROVEMENT_LOOP.md` | This file | written |
| `/root/arifOS/docs/DSG.md` | DSG canon (predecessor) | written |
| `/root/AAA/docs/AAA_TRINITY.md` | AAA operational spec (predecessor) | written |

---

## Open items (not blocking the spec, blocking full deploy)

These need Arif's authorization before they can go live. Each is **MED or HIGH** risk and should be sealed explicitly.

- [ ] **Supabase turn_outcomes table** — needs migration. The schema is in `turn_outcome_schema.json`. Apply when ready.
- [ ] **Bot restart on prompt change** — bot needs to detect prompt file mtime and reload. Implementation: add to `bot_template_enforcement.py`.
- [ ] **Post-hoc verdict UI** — Telegram command (e.g., `/mark <turn_id> correct|wrong|meh`). Marked by Arif only. Gödel Lock.
- [ ] **APEX daily pulse cron** — `apex_daily_pulse.sh` is written. Wire to crontab: `0 9 * * 1` (Mondays 09:00 MYT).
- [ ] **Prompt-mutation gate** — `prompt_mutation_gate.py` is written. Wire to arifOS MCP as a new tool.
- [ ] **Wire-next #4 blocker** — `hermes-opencode` wrapper fires `LEGACY_WRAP` HOLD gate. Code-level bug. Cannot be fixed by docs alone. Needs code patch in `/root/AAA/a2a-server/` or wherever the wrapper lives.

---

## The 30-day N=60 thesis test (carry-forward)

To make this more than "strong architecture," run the test:

| Group | Tasks | Witness | Judge | HOLD | Metric |
|---|---|---|---|---|---|
| A (control) | 30 diverse ops | None | None | None | silent failures, false SEALs, post-hoc correctness |
| B (trinity) | 30 matched ops | AGI🦞 on every mutation | JUDGE⚖ on every MED/HIGH | 888_HOLD auto on HIGH | same |

Decision rule: if B reduces silent failures by ≥50% vs A at equal or lower token cost → thesis confirmed. Less → back to drawing board.

You already have the orchestration. You have the logs. Decide to run it. Log outcomes honestly. No cherry-picking.

---

## What "EUREKA" means in this loop

- "EUREKA_TRANSLATOR" (smoke test) = not EUREKA. Smoke tests passing is normal operation, not discovery.
- "EUREKA_FORGE_GATE" (fail-closed works) = not EUREKA. Mechanism working as designed.
- "EUREKA_OFF_TEMPLATE_RATE_DROPS_BELOW_5%" after 3 months = **EUREKA**. Aggregate distribution shifted. This is the testable claim.
- "EUREKA_POST_HOC_CORRECT_RATE_ABOVE_90%" after 3 months = **EUREKA**. System learned.
- "EUREKA_HOLD_FALSE_POSITIVES_BELOW_2%" after 3 months = **EUREKA**. Judge is calibrated.

Reserve "EUREKA" for evidence of improvement, not for smoke tests.

---

## Provenance

This document was forged from:
- The DSG canon (`/root/arifOS/docs/DSG.md`) — the law
- The AAA protocol (`/root/AAA/docs/AAA_TRINITY.md`) — the operational spec
- The eval result `2026-06-07` where `000_INIT: SEAL for awareness, HOLD for autonomous mutation` demonstrated the thesis in action
- The Three Deep Locks (Gödel, Strange Loop, Anti-Beautiful) — the self-certification guardrails
- The 30-day N=60 thesis test design — the empirical falsification
- The agent-as-organ pattern (LIBRA/HERMES/CLAW/FORGE) — physics in naming

DITEMPA BUKAN DIBERI — Forged, not given.
