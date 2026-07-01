# TOOLS.md — OpenCode Tool Surface

> **DITEMPA BUKAN DIBERI** — Forged, Not Given.

## Native Tools

| Tool | Use For | Notes |
|------|---------|-------|
| `bash` | Shell commands, git, npm, systemctl | Always quote paths with spaces |
| `read` | Read files, directories, images, PDFs | Use offset/limit for large files |
| `write` | Create/overwrite files | Must read first if editing existing |
| `edit` | Exact string replacement | Prefer over write for existing files |
| `glob` | Find files by pattern | `**/*.ts`, `src/**/*.tsx` |
| `grep` | Search file contents (regex) | Use include to filter by extension |
| `websearch` | Web search | For external research |
| `webfetch` | Fetch URL content | Returns markdown by default |
| `task` | Spawn subagents | Use for parallel, complex work |
| `todowrite` | Task tracking | Use for 3+ step tasks |

## MCP Servers — Organ Map

### Federation Organs (Primary)

| Server | Port | Transport | Key Tools | Use When |
|--------|------|-----------|-----------|----------|
| **arifos** | :8088 | remote | session_init, judge, vault_seal, mind_reason, sense_observe | Governance, judgment, session binding |
| **aforge** | :7072 | stdio | forge_dry_run, forge_approve, forge_execute, forge_run | Building, deploying, executing code |
| **geox** | :8081 | remote | basin_resolve, seismic_compute, prospect_evaluate, claim_create | Geoscience, earth intelligence |
| **wealth** | :18082 | remote | conservation, flow, entropy, signal, game, boundary | Capital, finance, risk |
| **well** | :18083 | remote | assess_homeostasis, validate_vitality, guard_dignity | Human readiness, vitality |

### Infrastructure & Tools

| Server | Transport | Key Tools | Use When |
|--------|-----------|-----------|----------|
| **github** | local (gate) | repo ops, PRs, issues, code search | GitHub operations (governed) |
| **docker** | local | container lifecycle, file ops | Container management |
| **hostinger-vps** | local | VPS lifecycle (17 tools) | VPS management (governed) |
| **cloudflare** | local | DNS, Workers, R2, Pages | Cloudflare operations |

### Research & Analysis

| Server | Transport | Key Tools | Use When |
|--------|-----------|-----------|----------|
| **meyhem** | remote | MCP discovery, ranked search | Tool discovery, web research |
| **brave-search** | local | web + local search | Fast web research |
| **perplexity** | local | web-grounded AI research | Deep research |
| **sequential-thinking** | local | multi-step reasoning chains | Complex debugging |
| **context7** | local | library docs (npm/pip/Go) | Up-to-date library docs |

### Data

| Server | Transport | Key Tools | Use When |
|--------|-----------|-----------|----------|
| **postgres** | local | raw SQL, schema inspection | Direct DB access |
| **supabase** | local | managed DB, Auth, Edge Functions | Supabase operations |
| **qdrant** | local | vector search, collections | Similarity search |

### Media (MiniMax)

| Server | Port | Key Tools | Use When |
|--------|------|-----------|----------|
| **minimax-media** | :18090 | TTS, video, image, voice, music | Media generation |
| **minimax-code** | :18091 | web_search, understand_image | Image analysis, web search |

## Tool Selection Guide

```
Need to build/deploy code?     → aforge (forge_*)
Need governance/judgment?       → arifos (arif_*)
Need geology/seismic?           → geox (geox_*)
Need finance/risk?              → wealth (wealth_*)
Need health/vitality?           → well (well_*)
Need to search the web?         → meyhem or brave-search
Need library docs?              → context7
Need to manage containers?      → docker
Need to manage VPS?             → hostinger-vps (governed)
Need to manage GitHub?          → github (governed)
Need multi-step reasoning?      → sequential-thinking
```

## MCP Tool Pre-Flight

Before calling any MCP tool, verify the server is alive:
```bash
curl -sf http://localhost:8088/health && echo "arifos OK" || echo "arifos DOWN"
curl -sf http://localhost:7071/health && echo "aforge OK" || echo "aforge DOWN"
# ... etc for each organ
```

If a server is DOWN, proceed read-only on live servers. Do NOT assume dead server config is valid.

## Model Rotation (2026-07-01)

| Agent | Model | Why |
|-------|-------|-----|
| Main (OpenCode) | MiMo v2.5 Pro | 1M context, reasoning, tool_call |
| FORGE | MiniMax M2.7 | Tool execution + reasoning |
| AUDITOR | DeepSeek V4 Pro | 1M ctx, deep reasoning |
| OPS | MiniMax M2.5-HS | Fast monitoring |
| PLAN | Kimi K2.7 Code | 256K ctx, agentic planning |
| Small tasks | Azure GPT-4.1-mini | Cheap, fast |

---

*Forged: 2026-06-25*
*DITEMPA BUKAN DIBERI*
