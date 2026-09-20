---
name: agent-claim-verification
description: "Use when an agent claims X is built. Verify on disk."
tags: [audit, verification, agent-claims]
risk_tier: medium
floor_scope: [F2, F9, F11]
---

# Agent Claim Verification

> Another agent's audit is a claim, not evidence. Reproduce before repeating.

## When to use

Any time an agent says a component is "built", "done", "working", "passes", or "ready". Treat as HEARSAY per claim-receipt-discipline.

## The Three-State Test

Every "X is done" requires checking THREE independent states:

| State | Question | Probe |
|---|---|---|
| **EXISTS** | File/code on disk? | find, ls, read_file |
| **RUNS** | Has it ever executed? | systemctl status, journalctl, ps |
| **WIRED** | Connected to inputs/outputs? | grep callers, check cron, trace data |

If any state is false, the claim is PARTIAL at best.

## Five Failure Shapes

### 1. Gate with 0 callers
Agent claims N/M boundaries pass. Gate has zero scheduled callers.
Probe: grep gate_script across all 4 scheduler surfaces.

### 2. Timer DISABLED
Timer+service exist but is-enabled returns disabled, zero journal entries.
Probe: systemctl is-enabled + journalctl --since today.

### 3. Empty store
Directory exists, 0 files inside.
Probe: ls dir/ | wc -l.

### 4. Phantom artifact
Agent names versioned artifact absent from disk.
Probe: find /root -name artifact.

### 5. Wrong source data
Agent says reading source A, data is actually source B.
Probe: head -1 file, inspect keys.

## Verification Matrix

| Claim | Probe | Pass |
|---|---|---|
| code is built | find + wc -l | exists AND > 0 bytes |
| component wired | grep 4 scheduler surfaces | >= 1 active reference |
| timer fires daily | is-active + journalctl | enabled AND recent entries |
| store has N items | ls | wc -l | count >= claimed |
| prediction live | read + check status | ACTIVE AND verify_at set |
| bridge connects A-B | grep subscription | imported AND called |
| tested N-M pass | check test targets | exercises real code path |

## Partial-Truth Trap

Most dangerous claims are partially true: timer exists but disabled; code exists but untracked; store exists but empty; schema exists but nothing loads it. Report specific state, not general claim.

## Procedure

1. Read the claim. Identify every factual assertion.
2. For each, run the probe from the matrix.
3. Record: EXISTS? RUNS? WIRED?
4. Report specific states, not general verdicts.
5. If PARTIAL, name which states pass and which fail.

## Pitfalls

- "Code exists" is NOT "component works" -- state 1 of 3.
- "Timer exists" is NOT "job runs" -- must be enabled AND have journal entries.
- "Tested 20/20" is NOT "system works" -- tests may exercise private helpers.
- Don't probe from memory -- run grep/find/systemctl NOW.