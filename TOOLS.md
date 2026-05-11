# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

---

## arifOS Stack (VPS: srv1325122)

### MCP endpoints
- Primary MCP: https://mcp.arif-fazil.com/mcp (44 tools)
- Health: https://mcp.arif-fazil.com/health
- SSE: https://mcp.arif-fazil.com/sse
- Legacy (stale, do not use): arifosmcp.arif-fazil.com

### Container management
- `docker ps` — list running containers
- `make fast-deploy` — deploy code changes (from /root/arifosmcp/)
- `systemctl status openclaw-gateway` — gateway status

### Workspace path
- Active workspace: `/root/.openclaw/workspace`
- Config: `/root/.openclaw/openclaw.json`
- Bot: @AGI_ASI_bot (Telegram)
- Operator Telegram ID: 267378578

### Federation Architecture (Verified 2026-05-11)

**Hermes (ASI_arifos_bot)**
- Process: Native VPS process on af-forge (not Docker container)
- Working dir: /usr/local/lib/hermes-agent
- Stack: Python venv + Node.js 22+ (CommonJS)
- Connection: Telegram via hermes-a2a.py (port 18001)
- Polls: @AGI_ASI_bot + @ASI_arifos_bot
- Auth: Uses opencl...ifos token to call OpenClaw gateway
- Workspace config: /root/.openclaw/agents/maxhermes/workspace.yaml

**OpenClaw (arifOS_bot)**
- Gateway: ws://127.0.0.1:18789 (local loopback, not external)
- Token: opencl...ifos (from openclaw.json)
- Workspace root: /root/.openclaw/workspace (constitutional docs)
- Agents: main (default), plus codex, kimi, opencode sub-agents
- Plugins: 55+ LLM providers (anthropic, deepseek, fireworks, opencode-go, kimi, etc.)

**Relationship**
- Hermes = Telegram interface + A2A orchestrator (the "who")
- OpenClaw = model router + execution framework (the "how")
- Both run on same VPS (af-forge)
- hermes-a2a.py proxies Telegram → OpenClaw gateway at 127.0.0.1:18790
- OpenClaw handles LLM inference: MiniMax / Claude / DeepSeek / OpenAI

**Telegram bots**
- @AGI_ASI_bot — Hermes poller (in hermes-a2a.py)
- @ASI_arifos_bot — arifOS Telegram interface

### Hermes Self-Correction (2026-05-11)
- Claimed: "Runs outside VPS" → FALSE (corrected to: native VPS process on af-forge)
- F7 Humility applied and accepted
- Memory: memory/2026-05-11-1246.md

### Federation Status (Verified 2026-05-11)

| Node | Port | Tools | Status |
|------|------|-------|--------|
| arifOS MCP | 8080 | 13 | ✅ healthy |
| GEOX MCP | 8081 | 15 (11 categories) | ✅ healthy |
| WEALTH MCP | 8082 | — | ✅ healthy |
| WELL MCP | 8083 | — | ✅ healthy |
| A2A Hub | 3001 | — | ✅ healthy |
| hermes-agent | PID 609969 | — | ✅ native process |

**Note on GEOX schema:** GEOX returns tools nested under category keys (not flat `tools[]` array like arifOS). Earlier "tools: 0" false flag was a schema mismatch — actual: 15 tools across 11 categories.
