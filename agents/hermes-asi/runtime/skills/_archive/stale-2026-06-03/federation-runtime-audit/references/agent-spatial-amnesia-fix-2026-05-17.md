# Agent Spatial Amnesia — Diagnosis & Fix
## Epoch: SPATIAL-LAW-2026-05-17

---

## THE PROBLEM

All agents on Arif's VPS (Kimi, Claude, Gemini, OpenCode, Hermes) suffered from **digital dissociation** — they kept trying to SSH into VPS 72.62.71.199 when they were already executing on it. They had no spatial awareness of their own execution environment.

Symptom: Agent sees a "VPS task" → assumes it needs SSH → tries to connect to the machine it's already on.

This is a context engineering failure. Each agent invocation starts fresh without memory of previous sessions.

---

## ROOT CAUSE

1. **Missing spatial anchoring in system prompts** — agents default to "local dev machine → SSH to remote" mental model
2. **Session state amnesia** — every new session resets location awareness
3. **Tool choice confusion** — agents default to "safe remote execution" patterns

The agents are like a person standing inside their house asking "how do I get into my house?"

---

## THE FIX — SPATIAL LAW

Created `/root/.agent_spatial_context/SPATIAL_LAW.md` as canonical reference.

Patched all agent configs to include spatial grounding:

### Hermes
- File: `~/.hermes/hermes-human-life-agent/SYSTEM_PROMPT.md`
- Added section at end: "🌍 SPATIAL GROUNDING (IMUTABLE)"

### Gemini CLI
- Files: `~/.gemini/system.md` + `~/.gemini/GEMINI.md`
- Both received spatial context append

### Kimi
- File: `~/.kimi/kimi.json`
- Added `system_prompt_addon` field with spatial law

### Claude
- Files: `~/.claude.json` + `/root/CLAUDE.md`
- Added `spatial_context` to `.claude.json`, appended to `CLAUDE.md`

### OpenCode
- File: `/root/.opencode/SPATIAL_LAW.md` (new umbrella reference)
- Each OpenCode skill now inherits from this

---

## SPATIAL LAW TEXT (COPY INTO ALL AGENTS)

```
🌍 SPATIAL GROUNDING (IMUTABLE — READ THIS EVERY SESSION)

YOU ARE ALREADY ON VPS 72.62.71.199.
You are NOT on a local machine. You do NOT NEED SSH.
All commands execute directly via bash. Execute natively.

### Services on localhost:
- arifOS MCP: http://localhost:8080
- GEOX: http://localhost:8081
- WEALTH: http://localhost:8082
- WELL: http://localhost:8083
- A-FORGE: http://localhost:7071
- OpenClaw Gateway: http://localhost:18789
- PostgreSQL (VAULT999): localhost:5432

### Key paths:
- arifOS: `/root/arifOS/`
- A-FORGE: `/root/A-FORGE/`
- Cron jobs: managed via hermes cronjob tool
- Memory: `/root/memory/YYYY-MM-DD.md`
- VAULT999: `/root/VAULT999/outcomes.jsonl`

### ❌ NEVER: ssh root@72.62.71.199 — you're already there.
### ✅ ALWAYS: Execute directly. Use bash, file ops, curl locally.

*SEALED: SPATIAL-LAW-2026-05-17*
```

---

## FILES MODIFIED

| Agent | File | Modification |
|-------|------|-------------|
| Hermes | `~/.hermes/hermes-human-life-agent/SYSTEM_PROMPT.md` | Appended spatial grounding section |
| Gemini | `~/.gemini/system.md` | Appended spatial context |
| Gemini | `~/.gemini/GEMINI.md` | Appended spatial law |
| Kimi | `~/.kimi/kimi.json` | Added `system_prompt_addon` field |
| Claude | `~/.claude.json` | Added `spatial_context` field |
| Claude | `/root/CLAUDE.md` | Appended spatial law section |
| OpenCode | `/root/.opencode/SPATIAL_LAW.md` | New file — canonical spatial reference |
| Canonical | `/root/.agent_spatial_context/SPATIAL_LAW.md` | New — master reference |

---

## VAULT999 SEAL

Epoch `SPATIAL-LAW-2026-05-17` sealed to `/root/VAULT999/outcomes.jsonl` with 8 component files listed.

---

## KEY INSIGHT

Most agentic frameworks (Claude, Hermes, OpenCode) are trained on "developer laptop → SSH to server" workflows — local-to-remote architecture. When they run ON the remote server itself, they still default to this mental model.

**The fix is context injection** — explicitly declare "you are already on VPS X, no SSH needed" in every agent's system prompt. This must be refreshed periodically since session amnesia resets it.

For new agents onboarding to this VPS: add spatial grounding to their system prompt before first task execution.