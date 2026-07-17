---
id: incident-triage
name: Incident Triage
version: 1.0.0
description: Six-step incident response playbook for federation organs and constitutional
  floor breaches.
owner: AAA
risk_tier: critical
knowledge_basis:
  language: true
  math: false
  physics: false
host_compatibility:
- claude-code
- codex
- opencode
- kimi
- kimi-code
dependencies:
  skills:
  - arifos-act
  servers:
  - arifos-mcp
  tools:
  - Bash
  - Read
  - Grep
  - mcp__arifos__arif_observe
  - mcp__arifos__arif_memory
  - mcp__arifos__arif_measure
  - mcp__arifos__arif_init
  - mcp__arifos__arif_judge
  - mcp__arifos__arif_forge
  - mcp__arifos__arif_seal
examples:
- A federation organ returns unhealthy; run the six-step playbook before patching.
- A constitutional floor trips and requires witness logging to VAULT999.
tests:
- Triage classifies scope as organ-only, federation-wide, or constitutional.
- Reversible containment precedes any patch.
version_lock:
  schema_version: '1'
  artifact_hash: pending
orthogonal_tags:
  trinitarian:
  - Ω
  - ΦΙ
  functional:
  - Ops
  - Governance
  layer: RUNTIME
  autonomy_tier: T2-T3
floor_scope:
- F1
- F2
- F3
- F4
- F6
- F11
- F13
---

# Incident Triage

The "don't panic, don't guess" playbook for federation incidents.

## Overview

This skill provides a disciplined six-step response for incidents affecting federation organs, constitutional floors, or sovereign-reported faults. It forces sensing and scoping before action, containment before diagnosis, and verification before closure. Every step leaves evidence suitable for VAULT999 witness.

## arifOS-ACT Embedding

Before using this skill on any mutating, irreversible, or high-blast-radius task:
1. **ART** — Attune (what is the real task?), Recognize (what class of power?), Test (fit · authority · evidence · blast · reversible).
2. **Kernel** — Route to arifOS for F1–F13 judgment if action class is Maker/Messenger/Mutator/Destroyer/Sovereign.
3. **ACT** — Apply narrow, Constrain scope, Trace witness, STOP before corruption.
4. **Receipt** — Leave evidence of what changed, why, and under whose authority.

## When to Use

- A federation organ is red, unreachable, or failing health checks.
- A VAULT999 entry, memory record, or constitutional artifact looks wrong.
- A constitutional floor (F1–F13) trips or is suspected to be breached.
- Arif reports a bug, anomaly, or service impact.
- A runtime alert requires immediate structured response.

## When NOT to Use

- **Do not use for curiosity or "what if" probes.** This skill is for confirmed or strongly suspected incidents only.
- **Do not use to bypass the arifOS kernel** for mutating, irreversible, or sovereign-class actions.
- **Do not apply patches** without containment, reversible staging, and kernel SEAL when required.
- If the root cause is upstream (cloud provider, OS, network), escalate instead of patching locally.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| incident_signal | yes | What failed, tripped, or was reported (service name, floor, symptom) |
| affected_organ | yes | One or more federation organs involved |
| blast_radius | yes | organ-only / federation-wide / constitutional / sovereign |
| evidence_so_far | no | Logs, screenshots, alerts, or memory references already available |
| reversibility | yes | Can the suspected change be undone safely? |

## Procedure

### Step 1: Sense

Establish observable facts before interpreting.

- Run organ health probes: `systemctl status <unit>` and `journalctl -u <unit> --since '5m ago'`.
- Use `mcp__arifos__arif_observe` mode=vitals or mode=search for federation-wide signals.
- Use `mcp__arifos__arif_measure` mode=health for thermodynamic and resource state.
- Capture timestamps, error lines, and affected service names verbatim.

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

- If data-loss risk exists: snapshot DB / vault / git state / config before any patch.
- If no data-loss risk: document current state and defer containment.
- For irreversible changes: route through arifOS kernel and obtain SEAL or sovereign ack.
- Apply the minimum change that stops active damage (e.g., restart, scale, toggle feature flag).

### Step 4: Diagnose

Read, recall, and correlate. Stop hypothesizing when evidence explains the symptom.

- Read recent logs and config diffs with `Read` and `Grep`.
- Recall prior incidents and deployments with `mcp__arifos__arif_memory` mode=recall.
- Check recent git commits, deploys, and dependency changes.
- Name the root cause with confidence level and supporting evidence.

### Step 5: Patch

Minimum reversible change, committed and verified.

- Draft the smallest fix that addresses the root cause.
- Prefer commits over manual edits. Include a clear commit message.
- Deploy through the organ's standard path (systemd restart, service reload, etc.).
- Verify with health probes and, where available, `verify-runtime` or organ smoke tests.
- If the patch is irreversible, apply 888 HOLD before continuing.

### Step 6: Postmortem

Close the loop with institutional memory.

- If a floor was breached, seal the postmortem to VAULT999 as witness.
- Write postmortem to `/root/INCIDENTS/<YYYY-MM-DD>-<slug>.md` with:
  - Trigger
  - Scope classification
  - Root cause and evidence
  - Fix applied
  - Prevention measures
- If the same symptom recurs within 7 days, treat it as a partial-fix pattern, not a new incident.

## Allowed Tools

| Tool | Purpose |
|------|---------|
| `Bash` | Run system commands, health scripts, and log inspection |
| `Read` | Inspect config files, unit files, and incident logs |
| `Grep` | Search code, logs, and configs for root-cause signals |
| `mcp__arifos__arif_observe` | Federation vitals, web/entropy signals, repository state |
| `mcp__arifos__arif_memory` | Recall prior incidents, deploys, and decisions |
| `mcp__arifos__arif_measure` | Health, cost, drift, and topology checks |
| `mcp__arifos__arif_init` | Start governed constitutional session before high-risk actions |
| `mcp__arifos__arif_judge` | Request SEAL / SABAR / VOID verdict from arifOS |
| `mcp__arifos__arif_forge` | Execute bounded, SEAL-authorized changes |
| `mcp__arifos__arif_seal` | Append incident witness receipt to VAULT999 |

## Forbidden Actions

- **NEVER** patch a production organ without first sensing, scoping, and containing.
- **NEVER** apply an irreversible patch without 888 HOLD / sovereign ack and kernel SEAL.
- **NEVER** skip the postmortem for constitutional or repeated incidents.
- **NEVER** treat scope creep as normal; STOP and re-scope.
- **NEVER** suppress or omit Ω₀ (uncertainty) in incident receipts.
- Escalate to **arifOS 888_JUDGE** if a constitutional floor is breached or two floors disagree.

## Output Format

```markdown
## Skill Result: incident-triage

### Summary
One-paragraph summary of the incident, scope, root cause, and current status.

### Evidence
- Symptom: <what failed>
- Scope: <organ-only / federation-wide / constitutional / sovereign>
- Root cause: <finding with confidence>
- Containment: <what was preserved>
- Patch: <change applied or deferred>

### Recommendations
- Immediate verification step
- Prevention or monitoring improvement

### Escalations
- None / <list with owner and method>
```

## Escalation Path

| Condition | Escalate To | Method |
|-----------|-------------|--------|
| Constitutional floor tripped | arifOS 888_JUDGE | A2A verdict_request / MCP arif_judge |
| Irreversible action needed | Arif (F13 SOVEREIGN) | 888 HOLD |
| Root cause upstream (provider/OS/network) | Federation ops + A-FORGE | A2A ops channel |
| Scope creep during response | STOP + re-authorize via kernel | new ART cycle |
| Same incident within 7 days | Senior ops + postmortem review | incident registry |

---

*Skill version 1.0.0 — AAA Skill Library*
