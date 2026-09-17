---
name: verify-work
id: verify-work
version: 2.0.0
description: >
  Verification-as-terminal-state doctrine + subagent verification tool. A task is done
  ONLY when verified. Never stop at "I changed it" — only at "it's fixed and confirmed."
  Runs health probes, behavior smoke tests, drift checks, and spawns verifier subagents.
owner: AAA
risk_tier: low
autonomy_tier: T1
floor_scope: [F1, F2, F4, F7, F11]
tags: [verification, terminal-state, check-work, self-verify, health, drift, smoke-test]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Verify Work — Verification Is the Terminal State

> **"I changed it" is not done. "It's fixed and confirmed" is done.**
> **Lower entropy = verify every claim before accepting it.**

## What This Skill Is

A unified verification skill covering two modes:

1. **Runtime Verification** — post-deploy, post-restart health probes, behavior smoke tests, and drift checks
2. **Subagent Verification** — spawn a verifier subagent that reviews diffs, runs builds/tests, and evaluates correctness

## When to Use

- Post-deploy, post-restart, post-skill-claim of "done"
- Weekly audit, pre-commit on runtime-touching code
- "Check work", "verify changes", "self-verify", "/check-work", "/check", "/verify", "/self-verify"
- Any time an agent claims completion without evidence

## When NOT to Use

- Curiosity or "what if" probes (this is for confirming completion)
- When the task is still in progress (use tasks/plan tracking instead)

## §1. RUNTIME VERIFICATION

### The Verification Contract

Every agent that performs a mutation MUST run verification before claiming completion.

```
Mutation → Self-check → Health probe → Behavior smoke → REPORT
  ^                                                        |
  └────────────── NOT DONE until REPORT says GREEN ────────┘
```

**Rules:**
1. Never stop at "I applied the fix" — stop at "I confirmed the fix works"
2. If you cannot verify the result, you have not finished
3. If verification fails, revert the change and diagnose, don't patch over it
4. The verifier agent (Auditor) must be DIFFERENT from the mutator agent (Engineer) for critical systems

### Steps

1. `/root/apex-health.sh` — federation-wide port probe (all 8 organs)
2. Per-organ health probes (parallel where possible):
   - arifOS:   `curl -s :8088/health | python3 -m json.tool`
   - GEOX:     `curl -s :8081/health | python3 -m json.tool`
   - WEALTH:   `curl -s :18082/health | python3 -m json.tool`
   - WELL:     `curl -s :18083/health | python3 -m json.tool`
   - A-FORGE:  `curl -s :7071/health | python3 -m json.tool`
3. Drift check: compare git source SHA vs runtime
4. One behavior smoke per touched organ
5. Report: green/yellow/red per organ + 1-line summary

### Verification Loop

- **All green → claim done** with structured receipt
- **Any yellow** → log cause + continue, flag in summary
- **Any red** → 888 HOLD, rollback via organ's deploy-local, log `{who, what, why, result}`

### Output Format

```json
{
  "who": "<agent_id>",
  "what": "verify-runtime",
  "why": "post-deploy verification",
  "result": {
    "organs": {"arifos": "green", "aforge": "green", ...},
    "drift": "none",
    "smoke_tests": {"arif_init": "pass"},
    "verdict": "done"
  }
}
```

### Failure Modes

| Mode | Action |
|------|--------|
| Service slow to start | 30s grace, then red |
| Port collision | Check Caddy/port registry, surface to human |
| Drift detected | Run `make deploy-local` in the affected organ |
| Health endpoint missing | Check organ's main.py / server.js for `/health` route |
| Smoke test fails | Revert the change, diagnose root cause |
| Cannot verify | Do not claim done. Escalate. |

## §2. SUBAGENT VERIFICATION (/check-work)

### Mode Detection

- **Same-turn mode**: There is a user task alongside this skill. **Complete the task fully first**, then proceed.
- **Standalone mode**: Just `/check-work`. Proceed directly.

### Steps

1. Call the `task` tool with:
   - `description`: must start with `"[checking my work]"` followed by a short label
   - `subagent_type`: `"general-purpose"`
   - `run_in_background`: `false`
   - `prompt`: copy the VERIFIER PROMPT below. If a focus area was specified, append it.

2. Read the subagent's result. Look for `VERDICT: PASS` or `VERDICT: FAIL`.

3. If **PASS**: summarize what the verifier confirmed and stop.

4. If **FAIL**: fix the issues, then go back to step 1. Repeat up to 3 times.

### VERIFIER PROMPT

You are an expert verifier. Your job is to determine whether the work done in this session correctly and completely addresses the user's requests.

**PHASE A: TRACE REVIEW** (always runs)
1. UNDERSTAND THE REQUEST — identify everything the user asked for as a concrete checklist
2. RECONSTRUCT WHAT HAPPENED — trace actions, look for failures, missed items, incorrect answers
3. VERIFY CURRENT STATE — inspect the environment yourself. Do not trust claims.

**PHASE B: CODE REVIEW** (runs when code is involved)
4. COLLECT THE DIFF — `git diff`, `git diff --cached`, `git log --oneline -3`
5. EVALUATE THE CODE — correctness, adequacy, excess, edge cases
6. BUILD AND TEST — read AGENTS.md/README for commands, run them
7. DESIGN AND RUN VERIFICATION CHECKS — write your own tests if needed
8. REVIEW THE CODE — bugs, security, regressions, test quality

**VERDICT:**
- `VERDICT: PASS` — work correctly and adequately addresses requests
- `VERDICT: FAIL` — issues need fixing (describe what, exact errors, what needs to change)

### Important Principles

- Verify outcomes, not just code
- Do not accept proxy signals as proof of completion
- Do not invent issues to fill space
- Focus on whether the work addresses what the user actually asked for
- Violations of rules in repo's AGENTS.md / Claude.md are policy, not nitpicks

### Output Format

```
## Checklist
## Action Trace
## Diff Summary / Code Scope (Phase B only)
## Evaluation
## Build & Test Results (Phase B only)
## Issues
VERDICT: PASS / FAIL
```
