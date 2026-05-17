---
title: "SKILL: Claude Code Operations"
type: skill
version: 1.0.0
category: infra
risk_band: MEDIUM
floors: [F1, F11]
evidence_required: true
sources: [/root/.opencode/skills/claude-code-ops/SKILL.md]
confidence: high
---

# SKILL: Claude Code Operations

> **Source:** `/root/.opencode/skills/claude-code-ops/SKILL.md`
> **Agent:** OpenCode (Ω-FORGE)
> **Forged:** 2026-05-17

---

## Trigger Conditions

- Claude Code broken, Bash tool fails
- Permissions need updating, MCP servers need configuration
- Settings need tuning, Claude Code needs upgrading
- Keywords: Claude Code, claude, .claude, settings.json, CLAUDE.md, MCP config

---

## Emergency Fixes

### Bash Tool Fails (ENOENT session-env)

**Symptom:** Every Bash command fails with `ENOENT: no such file or directory, mkdir '/root/.claude/session-env/<uuid>'`

**Fix:**
```bash
file /root/.claude
# If symlink broken:
rm /root/.claude
mkdir -p /root/.claude/session-env /root/.claude/memory /root/.claude/commands
```

### Permission Prompts Won't Stop

```bash
python3 -c "import json; d=json.load(open('/root/.claude/settings.json')); print(d['permissions']['defaultMode'])"
# Should output: "bypassPermissions"
```

---

## Key Files (Protect These)

| File | Purpose | Protect |
|------|---------|---------|
| `/root/.claude.json` | Auth tokens, OAuth state, MCP config | **NEVER modify without Arif approval** |
| `/root/.claude/settings.json` | Permission mode, allowed tools | Safe to edit |
| `/root/CLAUDE.md` | Arif's global profile and agent mandate | Safe to edit |
| `/root/.mcp.json` | 16 MCP server definitions | Safe to edit |

---

## Permission Mode: bypassPermissions

- Zero prompts for all tools
- Protected paths (.git/, .claude/) are writable (v2.1.142+)
- `rm -rf /` and `rm -rf ~` still prompt (hardware circuit breaker)

---

## MCP Servers (16 total)

Configured in `/root/.mcp.json`:
- **Local:** arifOS (8080), supabase (HTTP)
- **Search:** brave-search, exa, firecrawl, tavily, context7
- **Engineering:** github, docker, postgres, playwright, chrome-devtools
- **AI:** sequential-thinking, memory, minimax
- **Productivity:** jira

---

## Health Check

```bash
claude --version
ls -la /root/.claude/
file /root/.claude
env | grep ANTHROPIC_API_KEY
```

---

## Agent Mandate (from CLAUDE.md)

- **Maximum agency.** Full root VPS access.
- **Never say "I cannot" or "I don't know"** without trying 3 approaches first.
- **Find a way.** There is always a path.
- **Execute, don't ask.** Zero permission prompts.

---

## Related Pages

- [[federation-entities]] — Claude as federation agent
- [[skill-spatial-grounding]] — VPS context grounding
- [[concept-tools-and-embodiment]] — Claude as soft embodiment
- [[SCHEMA.md]] — TREE777 governance schema

---

*DITEMPA BUKAN DIBERI — Claude Code operational. Agent empowered.*
