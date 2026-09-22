---
name: hermes-rca-forge
description: "Metabolize a recurring symptom's root cause, not store it."
version: 1.0.0
tags: [rca, root-cause, metabolization, forge, substrate]
floors: [F1, F2, F4, F7, F13]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Hermes RCA Forge (xyz)

> **Forge a root cause that changes the substrate. Not one that fills the archive.**

## The One Rule

A standard RCA ends with a **postmortem** — a written report of what was learned. This forge ends differently. It ends with **discharge into substrate** — a change to the organism that makes the knowledge impossible to lose by forgetting.

> **If the RCA's output is a document, it is not an RCA. It is chat history.**
> The only valid output is a substrate already rendered different.

## When to Use

- A capability, scar, or doctrine is `improvements_proposed: 0` — knowledge stored, nothing changed.
- A symptom `xyz` recurs despite being "learned" before.
- A ledger is full but the organism is unchanged.
- Someone claims to have learned something, and you can't find what changed in the substrate.
- The RSI ledger shows N entries, all heartbeat, no deltas.

## When NOT to Use

- **Incident response** → `FORGE-incident-triage` (immediate containment + fix, damage in progress).
- **Verification** → `FORGE-verify-runtime` (confirming a completed change is correct).
- **A genuine first-time discovery** → this forge is for *metabolizing* what exists, not for first discovery.

## The Distinction — this forge vs incident-triage

| | FORGE-incident-triage | hermes-rca-forge (this) |
|---|---|---|
| Trigger | Something broke (incident) | Knowledge stored but nothing changed |
| Ends with | Postmortem (report) | **Discharge into substrate** |
| Output | Document + prevention measure | **A substrate rendered different** |
| Failure mode | Report = archive, not change | You write a report and call it learning |
| Question | "How do I fix this?" | "Did I BECOME different from this?" |

## Procedure — 5 Phases

### Phase 0 — CONFIGURE (xyz)
- `xyz` = the symptom being analyzed (a claim, a recurring failure, a leaderboard of noise)
- Record: session_id, actor_id, what symptom
- Declare the assumption of innocence: this may be an unmetabolized capability, not a new bug

### Phase 1 — TRACE: what the ledger says
Was this already handled before?
```python
# Search the ledger / scars / skills for the symptom
# Look for prior "learning" about xyz
# CRITICAL: does a prior record exist? If yes → this is a RE-LEARNING, not a discovery.
```
- If prior records exist → **do not re-learn. Metabolize the existing knowledge.**
- This is the "agent does not know deep thinking was done before" trap. Check FIRST.

### Phase 2 — SEPARATE: chat history vs memory
For the symptom, list what the system has:
| Column | Chat history (L-axis) | Memory (H5, metabolized) |
|---|---|---|
| What it is | What was SAID/done | What it COST / what CHANGED |
| Replayable? | Yes (data) | No (it is substrate) |
| Does it alter the actor? | No | Yes — the actor is different |
| Example | A log line, a postmortem doc | A scar, an obligation |

**The tell:** if the system can reproduce all "learning" about xyz as re-readable text, it has **chat history, not memory.** It has an archive, not a mind.

### Phase 3 — DIAGNOSE: where did metabolization fail?
The root cause is never the symptom. It is one of these:
1. **Unpaid cost** — the experience happened, the lesson was extracted, but no obligation (Q3) was created. The scar is *nostalgia*, not constitutional pressure.
2. **Improvements proposed, not installed** — the RSI/ledger claimed the fix but the substrate did not change (ΔS = 0).
3. **The report replaced the change** — a postmortem/summary was written and treated as the learning. It is a record of the payment, not the unmetabolized cost.
4. **Rehydration substitution** — a re-serialized form of the knowledge was re-fed, but it did not re-live.

### Phase 4 — FORGE: discharge into substrate
This is the only valid output. Choose ONE discharge that changes the organism:
- **Patch a skill** so the same path cannot be re-followed (dedupe a collision, fix a phantom alias)
- **Write a scar with obligation** — event + lesson + responsibility (Q3), sealed
- **Remove a duplicate worker** — the platform of unmetabolized knowledge is running twice
- **Restore a canon to main path** — it was archived out of the substrate and must live again
- **Amend a ledger entry** so `improvements_proposed` is no longer 0 — it reflects a real installed change

**Test of a valid discharge:** *"If the substrate were archived and I had to recover from scratch, would I be different?"* If yes → it is metabolized. If no → it is still chat history.

### Phase 5 — SEAL: prove the change, not the report
- Verify the discharge is on disk / in the ledger / in the live system (not a claim).
- Record: `{who, what: "rca-forge", xyz, root_cause, discharge, verified: true}`
- **If the ONLY artifact you can show is writing, you failed.** Writing is not metabolizing.

## Output Contract

```text
RCA-FORGE: xyz

ROOT CAUSE: <the unmetabolized capability, not the symptom>
SYMPTOM: <what you were asked about>
LEDGER STATE: <prior records found? improvements_proposed before/after>
CHAT-HISTORY-ONLY FIELDS: <what is stored but not alive>
DISCHARGE: <the one change to the substrate>
VERIFIED: <proof it is on disk / live / ledger>
METABOLIZED: <yes/no — is the organism different?>
```

## Pitfalls

- **Writing a postmortem is NOT the completion.** `FORGE-incident-triage` may end there. This forge may not. If your output is a document, go back to Phase 4.
- **"We already know this"** is not metabolization — it is the sign that the knowledge is *stored*. Metabolize it or it will be re-learned next session.
- **Re-learning is the anti-pattern.** If Phase 1 finds prior records, the failure is the failure to metabolize, not to learn. Don't write a "new" lesson over an unmetabolized one.
- **Scar without obligation is nostalgia.** If you forge a scar, include the Q3 responsibility. Without it you have added volume to the archive, not tension to the constitution.
- **ΔS must go negative.** If nothing got simpler, no duplicate removed, no phantom fixed, no canon restored — you have not lowered entropy. You have added noise.

## Alignment with the doctrine (forged 2026-08-31)

> Experience exists. Capability not metabolized.
> Memory ≠ Chat History.
> Knowledge-rich, action-poor.
> The only move that turns action-poor into action-rich is metabolize.

This forge is the instrument of that doctrine. It refuses to mistake the ledger for the learning, and it refuses to end anywhere but in a substrate already changed.

---
*Forged 2026-08-31 under F13 SOVEREIGN directive.*
*DITEMPA BUKAN DIBERI.*
