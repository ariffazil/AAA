---
name: incident-response
id: incident-response
version: 2.0.0
description: >
  Full incident lifecycle: detect → triage → escalate → resolve. Six-step incident
  response playbook with structured logging, backoff/circuit-breaker for restart loops,
  verification-as-terminal-state, severity classification, and canonical escalation ladder.
  Lower machine entropy.
owner: AAA
risk_tier: critical
autonomy_tier: T1
floor_scope: [F1, F2, F3, F4, F6, F11, F13]
tags: [incident, triage, escalation, response, restart-loop, circuit-breaker, postmortem, severity]
capability_tier: fed-long-context
ecology_state: WARM
---

# Incident Response — Full Lifecycle

> **Don't panic, don't guess, lower machine entropy.**

## What This Skill Is

A unified incident response skill covering the full lifecycle:

1. **Triage** — six-step playbook with structured logging, backoff/circuit-breaker, and verification-as-terminal-state
2. **Escalation** — severity classification and canonical escalation ladder
3. **Resolution** — postmortem, institutional memory, and prevention

## When to Use

- A federation organ is red, unreachable, or failing health checks
- A VAULT999 entry, memory record, or constitutional artifact looks wrong
- A constitutional floor (F1–F13) trips or is suspected to be breached
- Arif reports a bug, anomaly, or service impact
- A runtime alert requires immediate structured response
- Service outages, security breaches, constitutional violations, or agent misbehavior

## When NOT to Use

- **Do not use for curiosity or "what if" probes.** Confirmed or strongly suspected incidents only.
- **Do not use to bypass the arifOS kernel** for mutating, irreversible, or sovereign-class actions.
- **Do not apply patches** without containment, reversible staging, and kernel SEAL when required.
- If the root cause is upstream (cloud provider, OS, network), escalate instead of patching locally.

## §1. INCIDENT SEVERITY

| Level | Name | Examples | Response Time |
|-------|------|----------|---------------|
| 1 | info | Minor drift, stale docs | Next business day |
| 2 | warning | Service slow, test flaky | 4 hours |
| 3 | error | Service down, agent confused | 1 hour |
| 4 | critical | Security breach, data loss, constitutional violation | 15 minutes |
| 5 | emergency | Active attack, irreversible damage in progress | Immediate |

When in doubt, escalate one level higher.

## §2. SIX-STEP PLAYBOOK

### Step 0: Detect Restart Loop (Circuit Breaker)

Before doing anything else, check if the service is in a restart loop.

```bash
systemctl show <service> -p NRestarts 2>/dev/null
```

**Circuit breaker rules:**
- `NRestarts > 5` in 5 minutes → **STOP THE LOOP**: `systemctl stop <service>`
- `NRestarts > 20` in 1 hour → escalate to 888_HOLD
- Log the circuit breaker event
- Do NOT restart until root cause is found

### Step 1: Sense

Establish observable facts before interpreting.

- Run organ health probes: `systemctl status <unit>` and `journalctl -u <unit> --since '5m ago'`
- Use `arif_observe` mode=vitals or mode=search for federation-wide signals
- Capture timestamps, error lines, and affected service names verbatim
- **Log every probe**: `{who, what: "sense", why: <incident>, result: <findings>}`

### Step 2: Scope

Classify the incident to prevent scope creep.

| Scope | Definition | Response |
|-------|------------|----------|
| Organ-only | One service or repo affected | Local containment + organ owner |
| Federation-wide | Multiple organs or A2A/MCP transport impacted | Federation ops + kernel notice |
| Constitutional | F-floor tripped or governance invariant violated | arifOS 888_JUDGE + witness |
| Sovereign | Human authority, safety, or dignity at risk | 888 HOLD + Arif |

Stop if scope starts expanding mid-diagnosis. Re-scope and re-authorize.

### Step 3: Contain

Protect recoverability before changing anything.

- If data-loss risk exists: snapshot DB / vault / git state / config before any patch
- If no data-loss risk: document current state and defer containment
- For irreversible changes: route through arifOS kernel and obtain SEAL or sovereign ack
- Apply the minimum change that stops active damage

### Step 4: Diagnose

Read, recall, and correlate. Stop hypothesizing when evidence explains the symptom.

- Read recent logs and config diffs
- Recall prior incidents and deployments with `arif_memory` mode=recall
- Check recent git commits, deploys, and dependency changes
- **Check for patterns**: same symptom in last 7 days? → partial-fix, not new incident
- Name the root cause with confidence level and supporting evidence

### Step 5: Patch — One Change at a Time

Minimum reversible change, committed and verified.

- Draft the smallest fix that addresses the root cause
- **One mutation per step.** Never batch 3 fixes and restart
- Prefer commits over manual edits
- Deploy through the organ's standard path
- **Verify after EVERY change** — if the fix didn't work, revert and try next hypothesis
- **Backoff strategy**: 1st retry: 5s, 2nd: 30s, 3rd: 120s (escalate)
- If the patch is irreversible, apply 888 HOLD before continuing

### Step 6: Postmortem + Structured Log

Close the loop with institutional memory.

- If a floor was breached, seal the postmortem to VAULT999 as witness
- Write postmortem to `/root/INCIDENTS/<YYYY-MM-DD>-<slug>.md` with:
  - Trigger, Scope classification, Root cause and evidence, Fix applied, Verification result, Prevention measures
- If the same symptom recurs within 7 days, treat as partial-fix pattern, not new incident
- **Final structured log**: `{who, what: "postmortem", why: <incident>, result: {...}}`

## §3. ESCALATION LADDER

```
Agent detects incident
    ↓
Agent applies skill (if trained)
    ↓
Escalate to domain agent (GEOX/WEALTH/WELL/A-FORGE)
    ↓
Escalate to AAA control plane (routing + visibility)
    ↓
Escalate to arifOS 888_JUDGE (constitutional / irreversible)
    ↓
Escalate to Arif (human sovereign)
```

### Notification Matrix

| Level | Notify |
|-------|--------|
| 1-2 | Log + dashboard |
| 3 | Domain agent + AAA |
| 4 | arifOS judge + Arif (Telegram) |
| 5 | Arif immediately + all agents |

### Investigation Skills

- Service down → `vps-ops` health probes
- Secret leaked → `FORGE-secret-hygiene`
- Agent misbehaving → re-read SOUL.md
- Constitutional violation → authority detection

## §4. FIRE-TIME REAUTHORIZATION (WAJIB 5)

A decision made at *write-time* is NOT automatically valid at *fire-time*. Authorization must be re-judged.

### Affected surfaces

Cron jobs, queued workers, dependency-update PRs, scheduled deployments, delayed shell jobs, retry queues, event-triggered automation, long-running MCP tasks.

### The required invariant

Every deferred mutation must be judged TWICE: write-time + fire-time.

At fire time, re-check: identity/session validity, lease expiry, current branch/commit, current target state, changed blast radius, new evidence, human approval validity, dependency health, rollback availability, revocation status.

### Failure behavior

A scheduled action with **expired authority MUST become HOLD**.

`write_time_authorization.expiry < now()` → return 888_HOLD at fire time.

## §5. ORGAN DISAGREEMENT DOCTRINE (WAJIB 7)

When GEOX, WEALTH, and WELL recommend incompatible actions, the resolution order:

1. **Hard veto conditions** (any organ may trigger HOLD with evidence)
2. **Blast-radius precedence** (organ owning dominant irreversible consequence)
3. **Pareto search** (seek alternative satisfying all hard constraints)
4. **F13 escalation** (if no acceptable option → escalate to Arif)

### Hard veto table

| Organ | May veto when | Release condition |
|---|---|---|
| GEOX | Physical infeasibility OR unacceptable earth uncertainty | New data or revised interpretation |
| WELL | Unsafe human or operational readiness | Confirmed safe capacity + witness |
| WEALTH | Insolvency, unaffordable exposure | Restructured deal OR capital limit raised |
| arifOS | Authority, law, or constitutional violation | Ratified exception OR constitutional amendment |

## Forbidden Actions

- **NEVER** cover up an incident
- **NEVER** delay escalation to avoid "bothering" someone
- **NEVER** destroy logs or evidence
- **NEVER** restart a service without understanding why it failed
- **NEVER** patch a production organ without sensing, scoping, and containing first
- **NEVER** apply an irreversible patch without 888 HOLD / sovereign ack
- **NEVER** skip the postmortem for constitutional or repeated incidents
- **NEVER** suppress or omit Ω₀ (uncertainty) in incident receipts

## Escalation Path

| Condition | Escalate To | Method |
|-----------|-------------|--------|
| Constitutional floor tripped | arifOS 888_JUDGE | A2A verdict_request / MCP arif_judge |
| Irreversible action needed | Arif (F13 SOVEREIGN) | 888 HOLD |
| Root cause upstream | Federation ops + A-FORGE | A2A ops channel |
| Scope creep during response | STOP + re-authorize via kernel | new ART cycle |
| Same incident within 7 days | Senior ops + postmortem review | incident registry |
