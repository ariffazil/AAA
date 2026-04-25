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
