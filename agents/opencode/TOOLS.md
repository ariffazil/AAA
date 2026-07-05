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
| **chrome-devtools** | local | browser snapshot, click, eval, network | Browser automation, web debugging |
| **exa** | local | web search, URL fetch | Web content extraction, search |
| **fetch** | local | fetch_html, fetch_markdown, fetch_txt, fetch_json, fetch_readable, fetch_youtube_transcript | URL content extraction (Readability for articles, YouTube captions) |

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
Need to fetch/read a URL?       → fetch (fetch_readable for articles, fetch_json for APIs)
Need library docs?              → context7
Need to manage containers?      → docker
Need to manage VPS?             → hostinger-vps (governed)
Need to manage GitHub?          → github (governed)
Need multi-step reasoning?      → sequential-thinking
Need browser automation?        → chrome-devtools
Need web content extraction?    → exa
```

## MCP Tool Pre-Flight

Before calling any MCP tool, verify the server is alive:
```bash
curl -sf http://localhost:8088/health && echo "arifos OK" || echo "arifos DOWN"
curl -sf http://localhost:7071/health && echo "aforge OK" || echo "aforge DOWN"
# ... etc for each organ
```

If a server is DOWN, proceed read-only on live servers. Do NOT assume dead server config is valid.

## Model Rotation (2026-07-02 — corrected)

| Agent | Model | Provider | Why |
|-------|-------|----------|-----|
| Main (OpenCode) | MiMo V2.5 Pro | Xiaomi token-plan-sgp | Flagship reasoning, 1M ctx, tool_call |
| FORGE | GLM-5.2 | Bailian token-plan | 200K ctx, tool_call + reasoning |
| AUDITOR | DeepSeek V4 Pro | Bailian token-plan | 1M ctx, deep reasoning |
| OPS | MiniMax M2.7 Highspeed | MiniMax direct | Fast + reasoning, 200K, monitoring |
| PLAN | Kimi K2.7 Code | Bailian token-plan | 256K ctx, agentic planning |
| Small | Qwen 3.6 Flash | Bailian token-plan | 128K ctx, fast, vision |

### MiniMax Tier Map (corrected 2026-07-02)

| Model | Context | Use Case | Cost per M |
|-------|---------|----------|------------|
| M3 | **1M** | Flagship, long-context, multimodal | $0.30/$1.20 promo → $0.60/$2.40 |
| M2.7 | **200K** | Workhorse, tool_call, reasoning | $0.30/$1.20 |
| M2.7 Highspeed | **200K** | Fast workhorse, ops/monitoring | ~$0.30/$1.20 |
| M2.5 Highspeed | 131K | Cheapest, text-only, basic ops | $0.15/M |

---

*Forged: 2026-06-25 · Model rotation corrected: 2026-07-02*
*DITEMPA BUKAN DIBERI*
