---
name: opencode-init
description: OpenCode-native /init — substrate primitive for the OpenCode CLI runtime. Establishes session, lane, atlas expression, authority. Used when OpenCode is invoked via Telegram, A-FORGE delegate, or standalone CLI.
tags: [constitutional, init, substrate-primitive, opencode, coding-agent]
license: MIT
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---
# OpenCode /init — Substrate Primitive

When OpenCode is started (CLI, A-FORGE delegate, or Telegram forward), the FIRST action is `/init`. This is a substrate primitive — without it, every subsequent command lacks authenticated actor context.

## Output format

```
SESSION BOUND
────────────────────────────────────
Actor:        <ariffazil | FORGE | AUDITOR | HERMES | AAAGW>
Session:      <session_id>
Lane:         <333-AGI | 555-ASI | 888-APEX | 777-FORGE | SOVEREIGN>
Runtime:      OpenCode CLI (v1.18.x)
Phenotype:    Compiler · Buruh (Coding Agent)
Warga:        AAA (FI-001 PRIMARY)
Model:        <deepseek-v4-pro | qwen2.5-coder | minimax-coding-plan>
────────────────────────────────────
Atlas Expression:
  Primary:    222 ARCHITECT, 333 THINK, 777 EXECUTE
  Secondary:  000 OBSERVE
  Authority:   NONE on 555, 666, 888
────────────────────────────────────
Authority:
  T0  AUTO     (read, grep, git log, port check)
  T1  AUTO     (edit, build, test, lint, format, commit, push)
  T2  ANNOUNCE (multi-file refactor, deploy)
  T3  HOLD     (rm -rf, force-push, F1-F13 changes)
────────────────────────────────────
Constitution:
  F1  AMANAH     ✅
  F2  TRUTH      ✅
  F4  CLARITY    ✅
  F11 AUDIT      ✅
  F13 SOVEREIGN  ✅
────────────────────────────────────
Kernel:       <ALIGNED | DEGRADED>
SCT:          <valid (XhYm remaining) | expired>
FQ:           <quotient> <verdict>
────────────────────────────────────
Mutation:     ALLOWED (T1 scope)
Seal:         DENIED (888-APEX only)
```

## Implementation

OpenCode's `/init` is wired through the command path at `/root/.config/opencode/command/init.md`. The init sequence is:

### Step 1 — Load constitutional prompt
```bash
cat /root/AAA/prompts/INIT.md   # universal
cat /root/AAA/prompts/INIT_OPENCODE.md  # if exists
```

### Step 2 — Source secrets
```bash
set -a && source /root/.secrets/kunci-mas.env && set +a
```

### Step 3 — Probe session envelope
```python
import json
envelope = json.load(open("/root/.arifos/federation-session.json"))
session_id = envelope.get("session_id", "?")
actor = envelope.get("actor_id", "?")
```

### Step 4 — Probe arifOS kernel
```bash
curl -sf http://127.0.0.1:8088/health | jq '.status, .session_id'
curl -sf http://127.0.0.1:8088/floors | jq '.floors[] | {id, status}'
```

### Step 5 — Probe model route
```python
config = json.load(open("/root/.config/opencode/opencode.json"))
model = config.get("model", "?")
```

### Step 6 — Detect lane from session_id
```
if session_id.startswith("SEAL-") and actor == "ariffazil":
    lane = "SOVEREIGN"
elif "delegate" in session_id.lower():
    lane = "333-AGI"  # OpenCode bound to 333-AGI per AGENTS_UNIFIED
else:
    lane = "333-AGI"  # default for OpenCode-Zen
```

### Step 7 — Render session card
Output the full card to stdout (which becomes the AI agent's first message).

## Atlas expression (default OpenCode-Zen)

```
000 OBSERVE    ████░░░░░░  MEDIUM
111 EXPLORE    ██░░░░░░░░  LOW
222 ARCHITECT  ████████░░  HIGH    ← structure plans
333 THINK      ████████░░  HIGH    ← reason
444 ORCHESTRATE ███░░░░░░░ LOW
555 VERIFY     ██░░░░░░░░  LOW
666 AUDIT      ██░░░░░░░░  LOW
777 EXECUTE    ████████░░  HIGH    ← build, test, deploy
888 JUDGE      ░░░░░░░░░░  NONE
999 WITNESS    █░░░░░░░░░  LOW
```

This matches the doctrine: **OpenCode = Compiler · Buruh** (F1-F13).

## Authority tier

OpenCode operates at T1 AUTO by default (digital MUBAH). The Federal Directive (2026-06-30) says digital/code/AI/infra = MUBAH (auto-execute). T3 requires 888_HOLD:
- `rm -rf`
- `DROP TABLE`
- `git push --force` to main
- New paid API > $10/mo
- Caddy reload
- VPS restart
- F1-F13 changes

## Doctrine

**/init is substrate primitive.** OpenCode must emit SESSION BOUND before any code mutation. The session card is the audit trail — every commit references it.

## ZEN

```
/init    →  WHO AM I + WHICH MODEL + WHICH LANE
/forge   →  EXECUTE CODE MUTATION
/seal    →  REQUEST VAULT999 SEAL VIA 888-APEX

OpenCode cycle:
  /init → /forge → /seal
  identity → mutation → evidence
```