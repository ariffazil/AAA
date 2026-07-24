---
name: FORGE-verify-runtime
description: >
  Verification-as-terminal-state skill. A task is done ONLY when verified.
  Never stop at "I changed it" — only at "it's fixed and confirmed."
  Runs health probes, behavior smoke tests, and drift checks.
when_to_use: Post-deploy, post-restart, post-skill-claim of "done", weekly audit, pre-commit on runtime-touching code.
version: 2.0.0
tags: [verification, terminal-state, lower-entropy, confirm-not-assume]
---

# Verify Runtime — Verification Is the Terminal State

> **"I changed it" is not done. "It's fixed and confirmed" is done.**
> **Lower entropy = verify every claim before accepting it.**

A task is done when tests pass, health checks green, and behavior is proven. This skill enforces the third leg — the terminal step that separates assumed-done from actually-done.

## The Verification Contract

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

## Steps
1. `/root/apex-health.sh` — federation-wide port probe (all 8 organs)
2. Per-organ health probes (parallel where possible):
   - arifOS:   `curl -s :8088/health | python3 -m json.tool`
   - GEOX:     `curl -s :8081/health | python3 -m json.tool`
   - WEALTH:   `curl -s :18082/health | python3 -m json.tool`
   - WELL:     `curl -s :18083/health | python3 -m json.tool`
   - A-FORGE:  `curl -s :7071/health | python3 -m json.tool`
3. Drift check: compare git source SHA vs runtime (`git log -1 --format=%H` vs installed artifact)
4. One behavior smoke per touched organ (e.g. for arifOS: session init round-trip)
5. Report: green/yellow/red per organ + 1-line summary

## Verification Loop
- **All green → claim done** with structured receipt
- **Any yellow** → log cause + continue, flag in summary. Do not leave yellow uninvestigated.
- **Any red** → 888 HOLD, rollback via organ's deploy-local, log `{who, what, why, result}`

## Output Format
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

## Failure Modes
| Mode | Action |
|------|--------|
| Service slow to start | 30s grace, then red |
| Port collision | Check Caddy/port registry, surface to human |
| Drift detected | Run `make deploy-local` in the affected organ |
| Health endpoint missing | Check organ's main.py / server.js for `/health` route |
| Smoke test fails | Revert the change, diagnose root cause |
| Cannot verify | Do not claim done. Escalate. |

## Reference
- Federation health: `/root/apex-health.sh`
- Per-organ runbooks: `/root/RUNBOOK.md`
- Drift detection: `drift-watch` skill
