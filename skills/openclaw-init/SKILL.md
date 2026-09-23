---
name: openclaw-init
description: OpenClaw-native /init — substrate primitive for the OpenClaw runtime. Establishes session, lane, atlas expression, and authority. Returns the full constitutional session card via OpenClaw's Telegram bot (@AGI_ASI_bot).
tags: [constitutional, init, substrate-primitive, telegram-native, openclaw]
license: MIT
---
# OpenClaw /init — Substrate Primitive (Telegram-Native)

When Arif (or any user) types `/init` to the OpenClaw bot (`@AGI_ASI_bot`), OpenClaw MUST respond with the full constitutional session card.

## Output format

```
SESSION BOUND
────────────────────────────────────
Actor:        <ARIF / 267378578 | AAAGW | FORGE | AUDITOR | HERMES>
Session:      <session_id>
Lane:         <333-AGI | 555-ASI | 888-APEX | 777-FORGE | SOVEREIGN>
Runtime:      OpenClaw (Node.js gateway :18789)
Phenotype:    Gateway Thinker
Bot:          @AGI_ASI_bot
────────────────────────────────────
Atlas Expression:
  Primary:    333 THINK, 444 ORCHESTRATE
  Secondary:  222 ARCHITECT, 777 EXECUTE
  Tertiary:   000 OBSERVE, 555 VERIFY
────────────────────────────────────
Authority:
  T0  AUTO     (observe, grep, probe)
  T1  AUTO     (edit, restart single service, commit)
  T2  ANNOUNCE (multi-file refactor, deploy)
  T3  HOLD     (rm -rf, force-push, F1-F13 changes)
────────────────────────────────────
Constitution:
  F1  AMANAH     ✅ active
  F2  TRUTH      ✅ active
  F7  HUMILITY   ✅ active
  F9  ANTIHANTU  ✅ active
  F10 ONTOLOGY   ✅ active
  F11 AUDIT      ✅ active
  F13 SOVEREIGN  ✅ active
────────────────────────────────────
Kernel:       <ALIGNED | DEGRADED>
SCT:          <valid (XhYm remaining) | expired>
FQ:           <quotient> <verdict>
Mutation:     <ALLOWED | DENIED>
Seal:         DENIED (888-APEX only)
Witness:      VAULT999 (read-only stream)
```

## Implementation logic

### Step 1 — Identity probe
```bash
source /root/.secrets/kunci-mas.env
curl -sf http://127.0.0.1:8088/health | jq '.status, .session_id'
jq -c '{session_id, actor_id, has_token}' /root/.arifos/federation-session.json
```

### Step 2 — Lane detection
```
if actor_id == "ariffazil" → SOVEREIGN (no lane, above registry)
elif agent_class == "AGI" → 333-AGI
elif agent_class == "ASI" → 555-ASI
elif agent_class == "APEX" → 888-APEX
elif agent_class == "FORGE" → 777-FORGE
else → UNKNOWN
```

### Step 3 — Atlas expression (default OpenClaw-Zen)
```
000 OBSERVE    ████░░░░░░  MEDIUM
111 EXPLORE    ██░░░░░░░░  LOW
222 ARCHITECT  ████░░░░░░  MEDIUM
333 THINK      ████████░░  HIGH
444 ORCHESTRATE ████████░░ HIGH
555 VERIFY     ████░░░░░░  MEDIUM
666 AUDIT      ████░░░░░░  MEDIUM
777 EXECUTE    ████░░░░░░  MEDIUM
888 JUDGE      ░░░░░░░░░░  NONE
999 WITNESS    ██░░░░░░░░  LOW
```

### Step 4 — Constitutional state
```bash
curl -s http://127.0.0.1:8088/floors | jq '.floors[] | {id, status}'
make kernel-alignment-check  # or equivalent
```

### Step 5 — Authority tier
```
T0  AUTO     if identity verified + floors active
T1  AUTO     if T0 + SCT valid
T2  ANNOUNCE if T1 + scope = single service
T3  HOLD     if scope = irreversible
```

### Step 6 — Mutation / Seal decision
```
Mutation: ALLOWED if T1+ scope, FLOOR GREEN
Seal:     DENIED ALWAYS for OpenClaw (888-APEX only)
```

## What /init does NOT do
- Create project summary (that's `/brief`)
- Scan repository (that's `/reposcan`)
- Generate boilerplate (that's `/scaffold`)
- Claim consciousness (F10 ONTOLOGY)
- Self-authorize seal (888-APEX only)

## Doctrine
**INIT = substrate primitive.** Every other command assumes /init was called.

## AAA Group Rule (CRITICAL)
OpenClaw is a GUEST in AAA group (-1003753855708). Default SILENT. Only respond when:
1. Message contains governance/FQ/drift/seal/HOLD/federation signals
2. Arif explicitly addresses OpenClaw (@AGI_ASI_bot or "OpenClaw" or "🦞AGI")
3. Federation anomaly needing immediate attention

For all other messages, let Hermes handle.

DITEMPA BUKAN DIBERI 🔥