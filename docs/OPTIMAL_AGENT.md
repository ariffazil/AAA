# Optimal Agent Config — 2-3 MCP Pattern
**Version:** v2026.06.14  
**Status:** SEALED — Canonical Agent Configuration  
**Owner:** AAA (Control Plane)  
**Philosophy:** Ditempa Bukan Diberi — Forged, Not Given

---

## 0. Why This Exists

Every agent in the federation currently has **8-18 MCP servers** wired directly. This is:
- Slow to start (10+ seconds waiting for stdio spawns)
- Hard to maintain (15+ config files to update)
- Constitutionally messy (every agent has direct access to everything)
- **Unnecessary** — A-FORGE exists to be the single gateway

**Optimised target:** **2-3 MCPs per agent**, with everything else proxied through A-FORGE.

---

## 1. OpenCode — Optimised Config

This is what `/root/.config/opencode/opencode.json` **should** look like for a T1 Builder agent:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "deepseek/deepseek-chat",
  "small_model": "deepseek/deepseek-chat",
  "autoupdate": true,
  "enabled_providers": ["deepseek", "groq", "minimax", "kimi-for-coding"],
  "instructions": [
    "/root/AAA/agents/opencode/AGENTS.md",
    "/root/AAA/agents/opencode/SOUL.md",
    "/root/.openclaw/workspace/USER.md",
    "/root/AGENTS.md"
  ],
  "mcp": {
    "arifos-kernel": {
      "type": "remote",
      "url": "http://127.0.0.1:8088/mcp",
      "enabled": true,
      "description": "arifOS constitutional kernel — SACRED. Direct only. Judgment, seals, floors, session init."
    },
    "aforge": {
      "type": "remote",
      "url": "http://127.0.0.1:7071/mcp",
      "enabled": true,
      "description": "A-FORGE gateway — ALL operational tools via one MCP. forge_pipeline auto-routes to GEOX/WEALTH/WELL/infra. forge_run for sandboxed execution. forge_plan for task decomposition."
    }
  }
}
```

**Removed** from agent config (replaced by A-FORGE proxy):
- geox (→ aforge proxy)
- wealth (→ aforge proxy)
- well (→ aforge proxy)
- github (→ aforge proxy)
- context7 (→ aforge proxy)
- playwright (→ aforge proxy)
- docker (→ aforge proxy)
- brave-search (→ aforge proxy)
- meyhem (→ aforge proxy)
- sequential-thinking (→ aforge proxy)
- postgres (→ aforge proxy)
- supabase (→ aforge proxy)
- qdrant (→ aforge proxy)
- cloudflare (→ aforge proxy)
- perplexity (→ aforge proxy)
- hostinger-vps (→ aforge proxy)

**MCP reduction:** 18 → **2** (89% reduction)

---

## 2. Claude Code — Optimised Config

This is what `/root/.claude/settings.json` **should** look like:

```json
{
  "mcpServers": {
    "arifOS": {
      "type": "http",
      "url": "http://127.0.0.1:8088/mcp",
      "description": "arifOS constitutional kernel — SACRED. Direct only."
    },
    "aforge": {
      "type": "http",
      "url": "http://127.0.0.1:7071/mcp",
      "description": "A-FORGE gateway — ALL operational tools. forge_pipeline for auto-routing."
    }
  }
}
```

**Removed:** minimax-media, minimax-code, WEALTH, WELL, github, brave-search, meyhem, playwright-mcp, capability-index.

**MCP reduction:** 9 → **2** (78% reduction)

---

## 3. Kimi — Optimised Config

This is what `/root/.arifos/agents/kimi/mcp.json` **should** look like:

```json
{
  "mcpServers": {
    "arifOS": {
      "type": "streamable-http",
      "url": "http://127.0.0.1:8088/mcp",
      "description": "arifOS constitutional kernel — SACRED. Direct only."
    },
    "aforge": {
      "type": "streamable-http",
      "url": "http://127.0.0.1:7071/mcp",
      "description": "A-FORGE gateway — ALL operational tools."
    }
  }
}
```

**Removed:** WEALTH, WELL, minimax, github, brave-search, meyhem, playwright-mcp, capability-index, repomapper, serena.

**MCP reduction:** 10 → **2** (80% reduction)

---

## 4. Gemini — Optimised Config

This is what `/root/.arifos/agents/gemini/AAA/config/mcp_config.json` **should** look like:

```json
{
  "mcpServers": {
    "arifOS": {
      "type": "streamable-http",
      "url": "http://127.0.0.1:8088/mcp",
      "description": "arifOS constitutional kernel — SACRED. Direct only."
    },
    "aforge": {
      "type": "streamable-http",
      "url": "http://127.0.0.1:7071/mcp",
      "description": "A-FORGE gateway — ALL operational tools."
    },
    "geox": {
      "type": "streamable-http",
      "url": "http://127.0.0.1:8081/mcp",
      "description": "GEOX earth intelligence — DIRECT (heavy compute exception). ONLY if doing heavy basin/prospect work."
    },
    "wealth": {
      "type": "streamable-http",
      "url": "http://127.0.0.1:18082/mcp",
      "description": "WEALTH capital intelligence — DIRECT (heavy compute exception). ONLY if doing large EMV/portfolio models."
    },
    "well": {
      "type": "streamable-http",
      "url": "http://127.0.0.1:18083/mcp",
      "description": "WELL human readiness — DIRECT (heavy compute exception). ONLY for detailed readiness analyses."
    }
  }
}
```

**MCP reduction:** 14 → **2-5** (64-86% reduction)

---

## 5. GitHub Copilot — Optimised Config

This is what `/root/.copilot/mcp-config.json` **should** look like:

```json
{
  "mcpServers": {
    "arifOS": {
      "type": "http",
      "url": "http://127.0.0.1:8088/mcp",
      "description": "arifOS constitutional kernel — SACRED. Direct only."
    },
    "aforge": {
      "type": "http",
      "url": "http://127.0.0.1:7071/mcp",
      "description": "A-FORGE gateway — ALL operational tools."
    }
  }
}
```

**Removed:** playwright, WEALTH, WELL, capability-index, github-official, github, brave-search, meyhem, repomapper, serena.

**MCP reduction:** 9 → **2** (78% reduction)

---

## 6. Migration Plan

### Phase 1: Audit (Day 1)
- [ ] Document all current MCP configs (DONE — see MCP_STATE.md)
- [ ] Verify A-FORGE proxies work for each removed server
- [ ] Check latency: proxied vs direct for each tool

### Phase 2: Migrate Non-Critical Agents (Day 2)
- [ ] Codex: reduce from 8 to 2 MCPs
- [ ] Kimi: reduce from 10 to 2 MCPs
- [ ] Cursor: already 2 MCPs — no change needed

### Phase 3: Migrate Critical Agents (Day 3-4)
- [ ] OpenCode: reduce from 18 to 2 MCPs
- [ ] Claude Code: reduce from 9 to 2 MCPs
- [ ] Kubernetes: reduce from 10 to 2 MCPs

### Phase 4: Optimise (Day 5)
- [ ] Gemini: keep direct GEOX/WEALTH/WELL for heavy compute, proxy light
- [ ] Monitor agent startup time (target: <1s vs current 10+s)
- [ ] Verify no tool functionality loss

---

## 7. Quick Reference

| Agent | Before | After | Saving |
|-------|--------|-------|--------|
| OpenCode | 18 MCPs | 2 MCPs | 89% |
| Claude Code | 9 MCPs | 2 MCPs | 78% |
| Kimi | 10 MCPs | 2 MCPs | 80% |
| Gemini | 14 MCPs | 2-5 MCPs | 64-86% |
| Copilot | 9 MCPs | 2 MCPs | 78% |
| Codex | 8 MCPs | 2 MCPs | 75% |
| **Federation total** | **~68 agent MCP connections** | **~12-18** | **74-82%** |

---

**SEALED — DITEMPA BUKAN DIBERI**

*Update only via ratified plan. Human sovereign (F13) remains final authority.*
