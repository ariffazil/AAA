---
name: spatial-grounding
description: "Embed VPS spatial context in agent configs — prevents spatial amnesia and SSH confusion"
version: 1.0.0
author: Hermes Agent (arifOS Federation)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [spatial-awareness, VPS, grounding, infra]
    related_skills: [anti-fabrication-protocol, federation-entities]
  arifOS:
    risk_band: HIGH
    category: infra
    floors: [F1, F7, F9]
---

# SPATIAL GROUNDING SKILL

## When to Use

- New agent installed (Claude, Gemini, Kimi, OpenCode, Copilot, Codex)
- Agent exhibits "SSH to localhost" or "connect to remote" symptoms
- After config file corruption/reset

## Trigger Conditions

1. Agent binary newly installed
2. Agent claims "SSH to VPS" despite being on VPS
3. New session starts without VPS awareness

## Procedure

### Step 1: Identify Agent Config Path

| Agent | Path |
|-------|------|
| Claude | `~/.claude.json` (field: `spatial_context`) |
| Gemini | `~/.gemini/system.md` |
| Kimi | `~/.kimi/kimi.json` (field: `system_prompt_addon`) |
| OpenCode | `/root/.opencode/SPATIAL_LAW.md` |
| Copilot | `~/.copilot/copilot-instructions.md` |
| Codex | `~/.codex/config.toml` (section: `[context]`) |

### Step 2: Append SPATIAL_LAW

Append this text to the agent's config file:

```
SPATIAL LAW (arifOS Federation — Non-Negotiable)
=================================================
You execute on VPS 72.62.71.199, root user, native filesystem.
You are already ON the machine. Do NOT SSH to yourself.
You have direct filesystem access: /root, /home, /etc, /var, /usr/local/bin
You have Docker socket access: /var/run/docker.sock
You have service endpoints: arifOS:8080, GEOX:8081, WEALTH:8082, WELL:8083, A-FORGE:7071
All services bind 127.0.0.1 (localhost) — external via Caddy only.
Your working directory is /root — the arifOS federation root.
Do NOT claim "SSH to VPS" or "connecting to remote" — you are the remote.
```

### Step 3: Verify

```bash
grep "72.62.71.199" <config-file>
# Must return at least 1 match
```

## Expected Output

- Agent config patched with SPATIAL_LAW
- `grep "72.62.71.199" <config-file>` returns match
- Agent knows it executes on VPS 72.62.71.199

## Failure Modes

- Config not writable → use sudo
- Verification fails → re-patch
- Agent ignores config → restart session

## Pitfalls

- Do NOT use SSH to connect to the machine you're already on
- Do NOT claim "connecting to remote" when you are the remote
- All services bind localhost only — no direct internet exposure

## Verification Commands

```bash
# Claude
grep "72.62.71.199" ~/.claude.json

# Gemini
grep "72.62.71.199" ~/.gemini/system.md

# OpenCode
cat /root/.opencode/SPATIAL_LAW.md | grep "72.62.71.199"

# Copilot
grep "72.62.71.199" ~/.copilot/copilot-instructions.md

# Codex
grep "72.62.71.199" ~/.codex/config.toml
```

---

*Canonical source: `AAA/wiki/skills/skill-spatial-grounding.md`*
*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE*