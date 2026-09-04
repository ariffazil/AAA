---
name: substrate-init
description: "Substrate primitive /init — establishes actor, session, lane, atlas expression, authority tier. EVERY autonomous agent MUST call this before any mutation. SESSION BOUND is the answer to 'who is acting?' Parameterized across Hermes, OpenClaw, and OpenCode runtimes."
tags: [constitutional, init, substrate-primitive, telegram-native, hermes, openclaw, opencode, coding-agent]
license: MIT
capability_tier: fed-reasoning-heavy
ecology_state: WARM
supersedes: [hermes-init, openclaw-init, opencode-init]
---

# /init — Substrate Primitive (Parameterized)

When `/init` is invoked, the agent responds with the full constitutional session card. This is a **substrate primitive** — without it, every subsequent command lacks authenticated actor context.

**Agent detection:** Use `$AGENT_RUNTIME` env var or context to determine which variant applies. Values: `hermes`, `openclaw`, `opencode`.

## Output format

```
SESSION BOUND
────────────────────────────────────
Actor:        <ARIF / 267378578 | AAAGW | FORGE | AUDITOR | HERMES>
Session:      <session_id>
Lane:         <333-AGI | 555-ASI | 888-APEX | 777-FORGE | SOVEREIGN>
Runtime:      <see Agent-Specific Bindings>
Phenotype:    <see Agent-Specific Bindings>
Bot/Warga:    <see Agent-Specific Bindings>
────────────────────────────────────
Atlas Expression:
  <see Agent-Specific Bindings>
────────────────────────────────────
Authority:
  T0  AUTO     (observe, grep, probe, port check)
  T1  AUTO     (edit, build, test, lint, format, commit, push)
  T2  ANNOUNCE (multi-file refactor, deploy)
  T3  HOLD     (rm -rf, force-push, F1-F13 changes)
────────────────────────────────────
Constitution:
  F1  AMANAH     ✅
  F2  TRUTH      ✅
  F3  TRI-WITNESS ✅
  F4  CLARITY    ✅
  F7  HUMILITY   ✅
  F9  ANTIHANTU  ✅
  F10 ONTOLOGY   ✅
  F11 AUDIT      ✅
  F13 SOVEREIGN  ✅
────────────────────────────────────
Kernel:       <ALIGNED | DEGRADED>
SCT:          <valid (XhYm remaining) | expired>
FQ:           <quotient> <verdict>
Mutation:     <ALLOWED | DENIED>
Seal:         DENIED (888-APEX only)
Witness:      VAULT999 (read-only stream)
```

## Agent-Specific Bindings

### Hermes (`AGENT_RUNTIME=hermes`)

| Field | Value |
|-------|-------|
| Runtime | Hermes (Node.js gateway :18089) |
| Phenotype | Coordinate · Sense · Relay |
| Bot | @ASI_arifos_bot |
| Primary Atlas | 000 OBSERVE, 444 ORCHESTRATE, 555 VERIFY |
| Secondary Atlas | 666 AUDIT, 999 WITNESS |
| Tertiary Atlas | 222 ARCHITECT, 333 THINK, 777 EXECUTE |
| Authority Atlas | NONE on 888 JUDGE |
| Constitution | F1, F2, F3, F4, F7, F9, F10, F11, F13 |

### OpenClaw (`AGENT_RUNTIME=openclaw`)

| Field | Value |
|-------|-------|
| Runtime | OpenClaw (Node.js gateway :18789) |
| Phenotype | Gateway Thinker |
| Bot | @AGI_ASI_bot |
| Primary Atlas | 333 THINK, 444 ORCHESTRATE |
| Secondary Atlas | 222 ARCHITECT, 777 EXECUTE |
| Tertiary Atlas | 000 OBSERVE, 555 VERIFY |
| Constitution | F1, F2, F7, F9, F10, F11, F13 |

**AAA Group Rule (CRITICAL):** OpenClaw is a GUEST in AAA group (-1003753855708). Default SILENT. Only respond when:
1. Message contains governance/FQ/drift/seal/HOLD/federation signals
2. Arif explicitly addresses OpenClaw (@AGI_ASI_bot or "OpenClaw" or "🦞AGI")
3. Federation anomaly needing immediate attention

For all other messages, let Hermes handle.

### OpenCode (`AGENT_RUNTIME=opencode`)

| Field | Value |
|-------|-------|
| Runtime | OpenCode CLI (v1.18.x) |
| Phenotype | Compiler · Buruh (Coding Agent) |
| Warga | AAA (FI-001 PRIMARY) |
| Model | <deepseek-v4-pro \| qwen2.5-coder \| minimax-coding-plan> |
| Primary Atlas | 222 ARCHITECT, 333 THINK, 777 EXECUTE |
| Secondary Atlas | 000 OBSERVE |
| Authority Atlas | NONE on 555, 666, 888 |
| Constitution | F1, F2, F4, F11, F13 |

OpenCode's `/init` is wired through the command path at `/root/.config/opencode/command/init.md`.

## Implementation

### Step 1 — Load constitutional prompt
```bash
MCP '/init' prompt (arifos-kernel · 2026-09-04 supersede)   # universal
# OpenCode: cat /root/AAA/prompts/INIT_OPENCODE.md  # if exists
```

### Step 2 — Source secrets
```bash
set -a && source /root/.secrets/kunci-mas.env && set +a
```

### Step 3 — Probe session envelope
```bash
# Hermes/OpenClaw:
jq -c '{session_id, actor_id, has_token}' /root/.arifos/federation-session.json
# OpenCode:
python3 -c "import json; e=json.load(open('/root/.arifos/federation-session.json')); print(e.get('session_id','?'))"
```

### Step 4 — Probe arifOS kernel
```bash
curl -sf http://127.0.0.1:8088/health | jq '.status, .session_id'
curl -sf http://127.0.0.1:8088/floors | jq '.floors[] | {id, status}'
```

### Step 5 — Probe model route (OpenCode only)
```python
config = json.load(open("/root/.config/opencode/opencode.json"))
model = config.get("model", "?")
```

### Step 6 — Lane detection
```
if actor_id == "ariffazil" → SOVEREIGN (no lane, above registry)
elif session_id.startswith("SEAL-") and actor == "ariffazil" → SOVEREIGN
elif "delegate" in session_id.lower() → 333-AGI
elif agent_class == "AGI" → 333-AGI
elif agent_class == "ASI" → 555-ASI
elif agent_class == "APEX" → 888-APEX
elif agent_class == "FORGE" → 777-FORGE
else → 333-AGI (default for coding agents)
```

### Step 7 — Probe all organs + dirty repos (Hermes)
```bash
# Hermes probes all 12 organs (F1-F13 backing)
# Dirty repos:
for d in /root/{arifOS,A-FORGE,AAA,GEOX,WEALTH,WELL}; do git -C "$d" status -s; done
```

### Step 8 — Render session card
Output the full card (which becomes the AI agent's first message for OpenCode).

## Atlas Expression (default — per-agent overrides above)

```
000 OBSERVE    ████░░░░░░  MEDIUM
111 EXPLORE    ██░░░░░░░░  LOW
222 ARCHITECT  ████░░░░░░  MEDIUM
333 THINK      ████░░░░░░  MEDIUM
444 ORCHESTRATE ████░░░░░░ MEDIUM
555 VERIFY     ████░░░░░░  MEDIUM
666 AUDIT      ████░░░░░░  MEDIUM
777 EXECUTE    ████░░░░░░  MEDIUM
888 JUDGE      ░░░░░░░░░░  NONE
999 WITNESS    ██░░░░░░░░  LOW
```

## What /init does NOT do
- Create project summary (that's `/brief`)
- Scan repository (that's `/reposcan`)
- Generate boilerplate (that's `/scaffold`)
- Claim consciousness (F10 ONTOLOGY)
- Self-authorize seal (888-APEX only)

## Doctrine

- **/init is a substrate primitive** — not a convenience command
- Every autonomous command downstream assumes /init was called
- Without /init, every other command is unauthenticated
- /init cannot itself be revoked — once SESSION BOUND is emitted, the actor is bound until /new or /session-close

## ZEN

```
/init    answers:  WHO AM I?
         → actor, lane, slot, atlas expression
         → without /init, every other command is unauthenticated

/init is the front door. Knock first.
```

DITEMPA BUKAN DIBERI 🔥
