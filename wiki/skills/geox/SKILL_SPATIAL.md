---
title: "SKILL: Spatial Grounding"
created: 2026-05-17
updated: 2026-05-17
version: 1.0.0
type: skill
tags: [spatial-awareness, VPS, agent-config, grounding, federation]
category: infra
risk_band: HIGH
floors: [F1, F7, F9]
evidence_required: true
sources: [wiki/SCAR_HERMES.md]
confidence: high
---

# SKILL: Spatial Grounding

> **Skill ID:** `skill-spatial-grounding`
> **Canonical location:** `AAA/wiki/skills/SKILL_SPATIAL.md`
> **When to use:** When initializing a new agent, debugging "SSH to localhost" errors, or preventing spatial amnesia
> **Severity:** HIGH — spatial amnesia causes repeated "where am I?" confusion

---

## Summary

Embed VPS spatial context in all agent configs so agents know they execute on VPS 72.62.71.199, not a remote machine to SSH to.

---

## Trigger Conditions

- New agent binary installed (Claude, Gemini, Kimi, OpenCode, Copilot, Codex)
- Agent exhibits "SSH to localhost" or "connect to remote server" behavior
- After config file corruption or reset
- After new agent session starts without spatial awareness

---

## Procedure

### Step 1: Identify the agent and its config location

| Agent | Config File | Field/Location |
|-------|-------------|----------------|
| Hermes | `~/.hermes/hermes-human-life-agent/SYSTEM_PROMPT.md` | End of system prompt |
| Gemini | `~/.gemini/SYSTEM_MD.md` | End of system prompt |
| Kimi | `~/.kimi/kimi.json` | `system_prompt_addon` field |
| Claude | `~/.claude.json` | `spatial_context` field |
| OpenCode | `/root/.opencode/SPATIAL_LAW.md` | Separate spatial grounding file |
| Copilot | `~/.copilot/COPILOT_INSTRUCTIONS.md` | End of instructions |
| Codex | `~/.codex/config.toml` | `[context]` section |

### Step 2: Append SPATIAL_LAW to the config file

```text
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

### Step 3: Verify the patch

```bash
# For text-based configs
grep "72.62.71.199\|SPATIAL LAW" ~/.gemini/SYSTEM_MD.md
grep "72.62.71.199\|SPATIAL LAW" ~/.copilot/COPILOT_INSTRUCTIONS.md
grep "72.62.71.199\|SPATIAL LAW" ~/.codex/config.toml

# For JSON configs
grep "72.62.71.199" ~/.claude.json
grep "72.62.71.199" ~/.kimi/kimi.json

# For file-based
cat /root/.opencode/SPATIAL_LAW.md | grep "72.62.71.199"
```

### Step 4: Log the patch

Append to `AAA/wiki/LOG_MD.md`:
```
## [YYYY-MM-DD] patch | spatial-grounding: {agent-name}
- Config: {path}
- Status: VERIFIED
```

---

## Preconditions

- Agent config file exists and is writable
- Terminal access to verify patch
- VAULT999 access to log the operation

---

## Expected Outputs

- SPATIAL_LAW embedded in agent config file
- Verification command returns match
- VAULT999 outcome logged
- AAA/wiki/LOG_MD.md entry created

---

## Failure Modes

| Failure | Mitigation |
|---------|-----------|
| Config file not writable | Use `sudo` or check file permissions |
| Agent doesn't read config | Restart agent session |
| Verification returns no match | Re-patch, check file path |
| Agent still SSH's after patch | Check if agent reads multiple config files |

---

## Verification Checklist

- [ ] `grep "72.62.71.199" <config-file>` returns at least 1 match
- [ ] Agent no longer claims "SSH to VPS" in new session
- [ ] VAULT999 outcome logged
- [ ] AAA/wiki/LOG_MD.md entry added

---

## Related Pages

- [[scar-hermes-fabrication-2026-05-17]] — the incident that exposed spatial amnesia
- [[anti-fabrication-protocol]] — the protocol this skill embodies (verify-before-claim)
- [[federation-entities]] — all 7 agents and their config locations
- [[agent-skills-architecture]] — cross-platform skill format overview

---

## Adapters

This skill is ported to the following platform formats:
- Claude: `AAA/skills/spatial-grounding/claude/SKILL.md`
- OpenClaw: `AAA/skills/spatial-grounding/openclaw/SYSTEM_MD.md`
- OpenAI: `AAA/skills/spatial-grounding/openai/tool.json` (if applicable)
- MCP: `AAA/skills/spatial-grounding/mcp/manifest.json` (if applicable)

---

*DITEMPA BUKAN DIBERI — Spatial grounding is non-negotiable.*
*999 SEAL ALIVE*