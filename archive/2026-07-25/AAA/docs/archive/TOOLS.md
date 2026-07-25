# TOOLS.md - Local Notes

> ⚠️ SPATIAL RULE — READ BEFORE EVERY SESSION
> **YOU ARE ALREADY ON THE VPS (af-forge, 72.62.71.199).**
> - Execution environment: native VPS shell (root@af-forge)
> - SSH NOT NEEDED — you are already inside the target machine
> - All commands execute locally via bash/exec tool
> - File paths are native: `/root/`, `/data/`, `/root/arifOS/`, `/root/AAA/`
> - Network services are on localhost (127.0.0.1:5432, :8080, :18081, etc.)
> - No SCP, no SSH tunneling, no remote file transfer needed
> - When someone says "VPS" or "server" — you are already there

---

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
- Local: http://127.0.0.1:8088 (arifos.service, systemd managed)

### Service management
- `systemctl status arifos` — arifOS MCP service status
- `systemctl restart arifos` — restart arifOS MCP
- Service name: `arifos.service` (NOT `arifosmcp` — that's the legacy Docker-era name, quarantined)
- Port: 0.0.0.0:8088, PID 841099 (as of 09:24 UTC)
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

| Node | Port | Process | Status |
|------|------|-------|--------|
| arifOS MCP | 8088 | arifos.service (python) | ✅ healthy |
| GEOX MCP | 18081 | arifosd.py (python) | ✅ healthy |
| WEALTH MCP | 18082 | wealth-organ.service (python) | ✅ healthy |
| WELL MCP | 18083 | well.service (python) | ✅ healthy |
| APEX | — | External (MiniMax-hosted) | ✅ |
| A2A Hub | — | NOT DEPLOYED (A2A via hermes-a2a bridge) | ❌ |
| OpenClaw Gateway | 18789 | node (systemd) | ✅ healthy |
| hermes-agent | PID 798391 | native (systemd) | ✅ native process |
| A-FORGE | 7071 | a-forge.service (node) | ✅ healthy |

**Note on GEOX schema:** GEOX returns tools nested under category keys (not flat `tools[]` array like arifOS). Earlier "tools: 0" false flag was a schema mismatch — actual: 15 tools across 11 categories.

### srv1642546 (Kodee's VPS — Azwa's server)
- **Host:** srv1642546.hstgr.cloud | 72.61.126.65
- **SSH:** `ssh srv1642546` (key-based, `.ssh/config` alias)
- **SSH key:** `~/.ssh/id_ed25519` (arif-forge-push)
- **Root password (Hostinger panel):** `UgBJQDb8v2x4NwB3kZk8bPpNoUPSBt3wUpOMiOYZf296e839`
- **Purpose:** Azwa Fazil's server (hermes-agent, SAF MCP, ollama)
- **OS:** Ubuntu 26.04, 2x AMD EPYC 9355P, 8GB RAM
