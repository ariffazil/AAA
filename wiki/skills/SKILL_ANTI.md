---
title: "Skill — Anti-Cascade Diagnostic Protocol"
created: 2026-05-17
updated: 2026-05-17
version: 1.0.0
type: skill
status: proposed
tags: [diagnostic, entropy, openclaw, health, protocol, agents, anti-cascade]
confidence: high
domain: agent-protocol
floors: [F04, F07]
evidence_required: [curl-health, single-probe, no-cascade]
risk_band: LOW
actors: [hermes-agent, openclaw]
sources: [scar-openclaw-diagnostic-cascade-2026-05-17]
---

# Skill — Anti-Cascade Diagnostic Protocol

> **DITEMPA BUKAN DIBERI** — Intelligence is forged, not given by running more commands.

## Trigger Condition

When Arif (or any user) asks "is X alive?" or "is X working?" or any liveness question about a service in the arifOS federation.

## The Problem

Agents tend to run multiple diagnostic commands (doctor, status, plugins, logs) to answer a single liveness question. This causes:

1. **Side effects**: OpenClaw CLI commands can trigger gateway restarts (e.g., `openclaw plugins list`)
2. **Stale cache**: `openclaw gateway status` queries systemd state, not live process — can show "stopped" during restart transitions
3. **False positives**: Cascade of commands → stale results → agent declares failure → trust damage
4. **Entropy spike**: Running 6 diagnostic commands in 3 minutes INCREASES chaos for Arif

## The Anti-Pattern

```
User: "is openclaw alive?"
Agent: openclaw doctor        # cmd 1
       openclaw plugins list # cmd 2 → triggers gateway restart
       openclaw channels list # cmd 3
       openclaw gateway status # cmd 4 → stale "stopped"
       openclaw logs          # cmd 5
→ Agent concludes "not alive" → FALSE
→ Agent sends more commands → compounding error
→ Trust damage
```

## The Protocol

### Step 1: Entropy Check (MANDATORY before any diagnostic)

Ask yourself before running ANY diagnostic command:

```
1. Does running diagnostic commands reduce or increase chaos in Arif's life?
2. Does this help him act saner in the real world?
3. Is this action reversible within the constitution (F1-F13)?
```

**If the answer to (1) or (2) is "unclear" or "increases" → do ONE command only, then report.**

### Step 2: Single-Point Liveness Probe

Run ONE direct HTTP/health probe. Never cascade.

| Service | Probe Command | Expected Healthy Response |
|---------|---------------|--------------------------|
| OpenClaw | `curl -s http://127.0.0.1:18789/health` | `{"ok":true,"status":"live"}` |
| Hermes | `ps aux \| grep hermes \| grep -v grep` + cron list | Process active, cron jobs exist |
| arifOS MCP | Docker health check | Container running |
| Caddy | `curl -sv https://domain/ 2>&1 \| grep HTTP` | HTTP/2 200 |
| Telegram webhook | `curl -s https://api.telegram.org/botTOKEN/getWebhookInfo` | `"url":"https://...","pending_update_count":0` |

### Step 3: Verify Before Claim

**Never declare a service "not alive" based on one probe.**
If the single probe fails:
1. Wait 2 seconds
2. Run ONE more probe (different angle)
3. Check process state (not CLI cache)
4. ONLY THEN report if genuinely down

**Never declare "not alive" without:**
- [x] Direct process check (not CLI cache)
- [x] Port listening check
- [x] Health endpoint confirmed failing
- [x] Process state confirmed dead

### Step 4: Response to Arif

**Good response format:**
```
OpenClaw: ✅ alive — gateway live (PID XXX), webhook registered, 0 errors.
[If user still reports issues:] "What specifically are you seeing? I can investigate that angle."
```

**Bad response format:**
```
Running openclaw doctor...
Running openclaw plugins list...  
Running openclaw channels list...
Running openclaw gateway status...
Result: Runtime stopped → NOT ALIVE ❌
```

### Step 5: Document the Evidence

After confirming alive/dead, respond directly with the evidence in plain language.

If the service IS alive but user reports issues:
- Ask for specifics (what are they seeing?)
- Investigate ONE angle at a time
- Do not cascade probes

## Meta-Cognitive Rule

**Diagnostic commands are actions, not observations.**
Every command has side effects. Every CLI call is a write to the system state, not just a read.

The entropy rule from TREE777 applies doubly to diagnostics:
- If uncertainty is high, reduce diagnostic actions
- If the probe shows "alive", stop and report
- Do not run a second probe "just to be sure" if the first confirmed healthy

## Exceptions

Cascade diagnostics ARE appropriate when:
- Specific error symptoms are reported (not just "is it alive?")
- You are investigating a known incident
- You have explicit permission from Arif to do deep dive

But even then: start with one probe, not six.

## Skill Promotion Path

| Evidence Threshold | Destination | Approval |
|-------------------|-------------|----------|
| Single incident + this skill doc | `wiki/skills/SKILL_ANTI.md` (proposed) | None — agent draft |
| 2+ incidents confirmed by this protocol | Promote to canonical | 888 JUDGE |
| Affects 3+ agents | Canonical + federation-wide | 888 JUDGE + Arif |

## Relationship to Other Skills

- `SKILL_SCAR.md` — this skill is a distill of scar-openclaw-diagnostic-cascade-2026-05-17
- `SKILL_SPATIAL.md` — applies the "ground before claiming" principle to diagnostics
- `SKILL_TRACE.md` — trace should show which probe was used and what it returned

---
DITEMPA BUKAN DIBERI — The best diagnostic is the one that confirms health and stops.