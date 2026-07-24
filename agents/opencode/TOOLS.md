# ⚒️ OPENCODE — Tools

> **DITEMPA BUKAN DIBERI** — Forged, Not Given.
> **Aligned:** 2026-07-23 — live probe against 114 A-FORGE, 31 GEOX, 20 WEALTH, 8 arifOS tools.
> **Cross-ref:** `BOOTSTRAP.md` (boot probes) · `HEARTBEAT.md` (cost tracking) · `AGENTS.md` (federation map)

---

## Agentic Kernel — Tool Lane Architecture

```
FLAME (RM0, free)  →  stateless inference: fact_check, epistemic_check, plan_review
A-FORGE (governed) →  execution: forge_* shell, filesystem, git, docker, vault, browser
arifOS (kernel)    →  governance: arif_init, arif_judge, arif_seal, arif_route, arif_memory
GEOX/WEALTH/WELL   →  domain evidence: compute-only, never mutate
GitHub/Docker/etc  →  infrastructure: governed access through A-FORGE gates
```

**Route least power first:** FLAME → A-FORGE → arifOS. Never use a governed tool when a free tool suffices.

---

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
| `skill` | Load specialized skill | Check available_skills first |
| `question` | Ask Arif clarifying question | Only when intent is genuinely ambiguous |

---

## MCP Servers — Federation Organs (Primary)

| Server | Port | Tools | Use When |
|--------|------|-------|----------|
| **arifos** | :8088 | `arif_init`, `arif_observe`, `arif_think`, `arif_route`, `arif_memory`, `arif_judge`, `arif_forge`, `arif_seal` | Governance, judgment, session binding, constitutional verdict |
| **aforge** | :7072 | `forge_*` (114 tools — shell, filesystem, git, docker, browser, vault, postgres, github, chart, document, parallel, predict, scan, policy) | Building, deploying, executing, browser automation, file ops |
| **geox** | :8081 | `geox_basin`, `geox_seismic_*`, `geox_prospect`, `geox_petrophysics`, `geox_falsify`, `geox_claim_*`, `geox_well_*`, `geox_map_*`, `geox_evidence`, `geox_contradiction_scan` (31 tools) | Geoscience, seismic, basin, petrophysics, prospect evaluation |
| **wealth** | :18082 | `capital_primitive` (npv/irr/emv/mc/kelly/markowitz), `capital_market` (fx/commodity/gold/oil/gas), `capital_health`, `capital_diagnose`, `capital_entropy`, `capital_wisdom`, `capital_ledger` (20 tools) | Capital math, market data, risk, portfolio, institutional stress |
| **well** | :18083 | `well_assess_homeostasis`, `well_validate_vitality`, `well_guard_dignity`, `well_classify_substrate`, `well_trace_lineage`, `well_check_repair`, `well_assess_reliability` | Human readiness, vitality, fatigue, dignity (REFLECT_ONLY) |

---

## MCP Servers — Free Inference Lane (FLAME)

| Server | Port | Tools | Use When |
|--------|------|-------|----------|
| **hermes** (FLAME) | :18901 | `hermes_fact_check`, `hermes_epistemic_check`, `hermes_plan_review`, `hermes_memory_steward`, `hermes_cross_verify`, `hermes_system_status`, `hermes_health` | Claim verification, plan safety, memory classification — FREE, stateless |

**FLAME routing rule:** All `hermes_*` tools are RM0 (free tier). Route here first before burning governed tokens. FLAME is live at `:18901/health`.

---

## MCP Servers — Research & Analysis

| Server | Key Tools | Use When |
|--------|-----------|----------|
| **brave-search** | `brave_web_search`, `brave_llm_context`, `brave_local_search`, `brave_news_search` | Fast web + local + news search |
| **perplexity** | `perplexity_search`, `perplexity_ask`, `perplexity_reason`, `perplexity_research` | Web-grounded AI research, deep multi-source |
| **sequential-thinking** | `sequential_thinking`, `problem_breakdown`, `step_by_step_plan`, `analyze_problem` | Multi-step reasoning, structured analysis |
| **context7** | `resolve-library-id`, `query-docs` | Up-to-date library docs (npm/pip/Go) |
| **meyhem** | MCP discovery, ranked search | Tool discovery, web research |
| **exa** | `web_search_exa`, `web_fetch_exa` | Web content extraction, semantic search |
| **fetch** | `fetch_readable`, `fetch_markdown`, `fetch_html`, `fetch_json`, `fetch_txt`, `fetch_youtube_transcript` | URL extraction (Readability for articles, YouTube captions) |

---

## MCP Servers — Data & Storage

| Server | Key Tools | Use When |
|--------|-----------|----------|
| **postgres** | `postgres_query`, `postgres_list-schemas`, `postgres_describe-schema` | Direct DB access, schema inspection |
| **supabase** | `supabase_execute_sql`, `supabase_apply_migration`, `supabase_list_tables`, `supabase_get_logs`, `supabase_deploy_edge_function` | Managed DB, Auth, Edge Functions, migrations |
| **qdrant** | `qdrant_search`, `qdrant_collections_list`, `qdrant_count` | Vector similarity search |
| **sqlite** | `sqlite_query`, `sqlite_execute`, `sqlite_list-tables`, `sqlite_describe-table` | Local SQLite operations |
| **megamemory** | `megamemory_understand`, `megamemory_create_concept`, `megamemory_get_concept`, `megamemory_link` | Knowledge graph, concept memory |

---

## MCP Servers — Infrastructure & Operations

| Server | Key Tools | Use When |
|--------|-----------|----------|
| **github** | `github_create_pr`, `github_get_file_contents`, `github_search_code`, `github_list_issues`, `github_push_files` | GitHub operations (governed through A-FORGE) |
| **docker** | `docker_run_command` | Container lifecycle (governed through A-FORGE) |
| **hostinger-vps** | `VPS_getVirtualMachinesV1`, `VPS_getMetricsV1`, `VPS_restartVirtualMachineV1`, `VPS_getProjectListV1` (17 tools) | VPS management (governed) |
| **playwright** | `playwright_browser_navigate`, `playwright_browser_snapshot`, `playwright_browser_click`, `playwright_browser_take_screenshot`, `playwright_browser_evaluate` | Browser automation, web debugging |

---

## MCP Servers — Media

| Server | Key Tools | Use When |
|--------|-----------|----------|
| **minimax** | `minimax_web_search`, `minimax_understand_image` | Image analysis, MiniMax web search |

---

## MCP Servers — Meta

| Server | Key Tools | Use When |
|--------|-----------|----------|
| **aaa** | `aaa_measure` | Evidence-based decision recording |

---

## Tool Selection Guide

```
Need to reason/plan?              → sequential-thinking (free)
Need to verify a claim?           → hermes_fact_check (FLAME, free)
Need governance/judgment?         → arifos (arif_*)
Need to build/deploy/execute?     → aforge (forge_*) — governed
Need geology/seismic/basin?       → geox (geox_*)
Need finance/NPV/risk/market?     → wealth (capital_*)
Need health/vitality/readiness?   → well (well_*) — REFLECT_ONLY
Need web search?                  → brave-search or perplexity
Need deep research?               → perplexity_research
Need library docs?                → context7
Need to fetch a URL?              → fetch (fetch_readable for articles)
Need knowledge graph?             → megamemory
Need database query?              → postgres or supabase
Need vector search?               → qdrant
Need browser automation?          → playwright or aforge (forge_browser_*)
Need to manage containers?        → docker or aforge (forge_docker)
Need to manage GitHub?            → github (governed)
Need VPS ops?                     → hostinger-vps (governed)
Need image analysis?              → minimax_understand_image
Need multi-step reasoning?        → sequential-thinking
```

---

## MCP Tool Pre-Flight

Before calling any MCP tool, verify the server is alive:
```bash
# One-shot probe
for svc in arifos:8088 aforge:7071 aaa:3001 geox:8081 wealth:18082 well:18083; do
  n="${svc%%:*}"; p="${svc##*:}"
  curl -sf "http://localhost:$p/health" >/dev/null 2>&1 && echo "✅ $n" || echo "❌ $n"
done

# FLAME free loop
curl -sf http://localhost:18901/health | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'FLAME: {d[\"status\"]}')"
```

If a server is DOWN, proceed read-only on live servers. Do NOT assume dead server config is valid.

---

## Model Rotation (canonical reference — 2026-07-23)

> **CANONICAL SOURCE:** `/root/AAA/registries/models/AGENT_MODEL_MAP.json`
> 
> This section is a cached summary. The JSON registry is authoritative.
>
> Quick lookup: `python3 -c "import json; d=json.load(open('/root/AAA/registries/models/AGENT_MODEL_MAP.json')); [print(f'{a[\"agent_id\"]}: {a[\"primary_model\"]}') for a in d['agents']]"`

### Current Agent Model Assignments (live 2026-07-23)

| Agent | Primary Model | Fallback Chain |
|-------|--------------|----------------|
| **OpenCode** | `deepseek/deepseek-v4-pro` | MiniMax-M3 → GLM-5.2 → Ollama qwen2.5-coder |
| **FORGE (000Ω)** | `deepseek/deepseek-v4-pro` | GLM-5.2 → MiniMax-M3 |
| **AUDITOR (Ψ)** | `deepseek/deepseek-v4-pro` | MiMo V2.5 Pro → MiniMax-M3 |
| **OPS (🌐)** | `deepseek/deepseek-v4-flash` | MiniMax M2.5 → MiniMax M3 |
| **PLAN (Ω)** | `kimi/kimi-for-coding` | DeepSeek V4 Pro → MiMo V2.5 Pro |
| **Hermes** | `mimo/mimo-v2.5-pro-ultraspeed` | MiMo Pro → DeepSeek V4 Pro → Groq |
| **OpenClaw** | `minimax/MiniMax-M3` | Groq Llama → Groq 70B → Gemini Flash |
| **Claude Code** | `deepseek/deepseek-v4-pro` | — |
| **Copilot** | `deepseek/deepseek-v4-pro` | — |
| **Kimi Code** | `kimi/k3` | Kimi K2.7 Code |
| **Codex** | `openai/gpt-5.6-sol` | DeepSeek V4 Pro |
| **Recovery** | `ollama/qwen2.5-coder:3b` | — |

**Constitutional rule:** `deepseek/deepseek-v4-pro` is the only model eligible to provide deliberative compute for 666_JUDGE and 999_SEAL roles. It does NOT possess independent authority to judge or seal — arifOS kernel adjudicates admissibility and verdict, F13/authorised actor supplies required authority or acknowledgement, VAULT999 performs the immutable append. 16 models are ineligible for constitutional deliberation.

### Cost Discipline

- **Default:** Use FLAME (free) for fact checks, plan reviews, memory classification
- **Cheap tier:** `deepseek-v4-flash` for ops/monitoring/summarization
- **Heavy tier:** `deepseek-v4-pro` for coding, complex reasoning, judgment
- **Apex tier:** Only when earned (multi-step constitutional reasoning, SEAL-grade work)
- **Daily budget:** $2.00/session

---

## Capability Discovery

When in doubt about what tools exist:
```bash
# A-FORGE registry (most comprehensive)
curl -sf http://localhost:7072/mcp -X POST -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | python3 -c \
  "import json,sys; tools=json.load(sys.stdin)['result']['tools']; print(f'{len(tools)} tools')"

# Route unknown intent
arifos_arif_route(intent="describe what you need")
```

**HARAM:** "I don't have that tool" without probing first. Probe the full MCP surface before declaring absence.

---

*Aligned: 2026-07-23 by FORGE (000Ω). Live probe: 114 A-FORGE, 31 GEOX, 20 WEALTH, 8 arifOS, 7 hermes.*
*Agentic kernel layer: CAPABILITY (layer 3/7). Next: BOOTSTRAP.md (layer 2 — boot probes).*
*DITEMPA BUKAN DIBERI*
