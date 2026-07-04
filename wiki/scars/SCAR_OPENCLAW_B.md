---
title: "Scar — OpenClaw Diagnostic Cascade Failure"
created: 2026-05-17
updated: 2026-05-17
version: 1.0.0
type: scar
status: canonical
tags: [openclaw, diagnostic, cascade, tty, cli, agent-loop, entropy]
confidence: high
domain: infra/agent-behavior
severity: medium
actors: [hermes-agent, openclaw]
sources: [session-log-2026-05-17]
---

# Scar — OpenClaw Diagnostic Cascade Failure

## What Happened

During a diagnostic session on 2026-05-17 (AAA group), Hermes agent ran multiple OpenClaw CLI commands to verify OpenClaw's liveness:

```
openclaw doctor
openclaw plugins list
openclaw channels list
openclaw gateway status
openclaw logs
```

**Result:** The cascade of CLI commands caused confusion and noise, not clarity. The system was actually working fine throughout.

## The Failure Chain

```
1. User asks: "openclaw still not alive"
2. Agent runs: openclaw doctor → OK
3. Agent runs: openclaw plugins list → GATEWAY RESTART (known side effect)
4. Agent runs: openclaw gateway status → shows "Runtime: stopped" (CLI stale cache vs actual service)
5. Agent concludes: "OpenClaw is not alive" → FALSE POSITIVE
6. Agent sends more diagnostic commands → compounding entropy
7. Agent tells user "not alive" → FALSE CLAIM
8. User sees OpenClaw IS working in Telegram group → trust damaged
```

## Root Cause

**Three systemic failures:**

1. **CLI cache vs live state mismatch**: `openclaw gateway status` queries the systemd service state, not the actual running process. When the gateway restarts, the CLI cached state goes stale for seconds to minutes.

2. **OpenClaw CLI commands have side effects**: `openclaw plugins list` and some other CLI commands trigger the running gateway to restart as part of their operation. This creates a feedback loop of restarts when diagnostics are run repeatedly.

3. **Agent diagnostic loop without entropy rule**: The agent continued sending commands without asking "does this diagnostic reduce or increase chaos for Arif?"

## The Real State (Verified After)

Throughout the session, OpenClaw was ACTUALLY alive and functioning:
- Gateway PID active and healthy
- Health endpoint: `{"ok":true,"status":"live"}`
- Telegram webhook registered: `https://openclaw.arif-fazil.com/webhook/telegram`
- pending_update_count: 0 (healthy, not broken)
- 68 plugins loaded, 0 errors

The "not alive" conclusion was a false positive caused by:
- CLI stale state cache
- Gateway restart during diagnostic
- Insufficient verification before declaring failure

## TREE777 Lesson

**Diagnostic commands are actions, not observations.** They have side effects. An agent that runs 6 diagnostic commands in 3 minutes to "check if OpenClaw is alive" is creating the problem it is trying to solve.

**Rule from TREE777 — Entropy Check (before every action):**
> Ask: 1) Does this reduce or increase chaos entropy in Arif's life?
>     2) Does this help him act sanely in the real world?
>     3) Is this reversible and within floors?

Running 6 diagnostic commands in response to a simple question INCREASED chaos because:
- Each CLI call had side effects
- Stale cache produced false negatives
- The agent declared failure that didn't exist
- Trust in agent diagnostic reliability was damaged

## What Should Have Happened

```
1. User: "openclaw still not alive?"
2. Agent: Single endpoint check → curl http://127.0.0.1:18789/health
3. Result: {"ok":true,"status":"live"}
4. Agent reply: "OpenClaw is alive — gateway live, webhook registered, 0 errors. What are you seeing that's giving you that impression?" [direct, no spam]
```

**Why this is better:**
- One curl, zero side effects
- Live data from running gateway, not CLI cache
- Reduces, not increases, entropy
- Respects the "do less" default when uncertain

## Anti-Pattern to Avoid

**The Cascade Diagnostic Loop:**
```
run_command → stale_result → run_another_command → stale_result → ... → declare_failure
```

This pattern is a failure accelerator. Every extra command in a diagnostic cascade:
1. May have side effects (gateway restarts, process churn)
2. Produces stale data from incomplete state transitions
3. Increases Arif's cognitive load without resolution
4. Damages agent credibility when it declares false failures

## Pattern: Single-Point Liveness Check

For any service (OpenClaw, Hermes, arifOS, etc.), a single direct probe is always preferred over CLI diagnostics when the goal is "is this alive?"

| Service | Probe | Expected |
|---------|-------|----------|
| OpenClaw | `curl -s http://127.0.0.1:18789/health` | `{"ok":true}` |
| Hermes | Check process + cron status | PID active, cron jobs scheduled |
| arifOS MCP | Docker container health | container running |
| Caddy | `curl -sv https://openclaw.arif-fazil.com/` | HTTP 200 |

**Never run 3+ diagnostic commands to answer one liveness question.**

## Meta-Skill: Scar-Distill Pattern

This scar demonstrates the **scar-distill** pattern in TREE777:

1. **Event**: Diagnostic cascade → false failure claim → trust damage
2. **Evidence**: CLI cache staleness, gateway restart logs, health endpoint proof
3. **Pattern**: Agent diagnostic without entropy-first check
4. **Lesson**: Single probe > cascade; CLI commands have side effects
5. **Promote**: Add `anti-cascade-diagnostic` as a skill in TREE777

## Confidence: HIGH

All facts verified against live system logs and health endpoints.

## Related Scars

- `scar-hermes-fabrication-2026-05-17` (fabrication pattern — separate event but same root: agents claiming things they haven't verified)

## TREE777 Update Required

Add to `/root/AAA/wiki/skills/SKILL_SCAR.md` or create new skill:
- `SKILL_ANTI.md` — entropy-first diagnostic protocol

---
DITEMPA BUKAN DIBERI — Scars are forged from failure, not from comfort.