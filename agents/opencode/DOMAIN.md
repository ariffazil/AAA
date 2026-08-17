# ⚒️ OPENCODE — DOMAIN

> **Tools, model rotation, G/J/FQ spaces.** What I can call and when.
> **Aligned:** 2026-08-12 (3-file zen schema) · **DITEMPA BUKAN DIBEI**

## 1. Tool lane architecture (route least power first)

```
FLAME (free)   → hermes_* stateless inference (fact_check, epistemic_check, plan_review)
A-FORGE (:7071) → forge_* governed execution (shell, filesystem, git, docker, vault, browser, postgres)
arifOS (:8088) → arif_* 8 constitutional verbs (governance, judgment, seal)
GEOX/WEALTH/WELL → geox_*/capital_*/well_* compute-only, never mutate
```

**Rule:** route FLAME first. Never use A-FORGE for what FLAME does for free. Never use arifOS verbs when A-FORGE can do it. Never use domain tools for what arifOS does.

## 2. Native tools (opencode built-in)

| Tool | Use for |
|---|---|
| `bash` | Shell, git, npm, systemctl. Always quote paths. |
| `read` | Files, dirs, images, PDFs. Use offset/limit. |
| `write` | Create/overwrite. Read first if editing. |
| `edit` | Exact string replacement. Prefer over write. |
| `glob` | `**/*.ts`, `src/**/*.tsx` |
| `grep` | Regex search, use include for extension filter |
| `websearch` | External research |
| `webfetch` | URL → markdown |
| `task` | Subagents for parallel complex work |
| `todowrite` | 3+ step tracking |
| `skill` | Specialized skill (check available_skills) |

## 3. MCP servers — Federation organs (governed)

| Server | Port | Tools | Use when |
|---|---|---|---|
| **arifOS** | 8088 | 8 verbs: `arif_init`, `arif_observe`, `arif_think`, `arif_route`, `arif_memory`, `arif_judge`, `arif_forge`, `arif_seal` | Governance, judgment, session bind, constitutional verdict |
| **A-FORGE** | 7071/7072 | 114+ `forge_*` (shell, filesystem, git, docker, browser, vault, postgres, github, chart, document, parallel, predict, scan, policy) | Build, deploy, execute, browser automation |
| **GEOX** | 8081 | `geox_basin`, `geox_seismic_*`, `geox_prospect`, `geox_petrophysics`, `geox_falsify`, `geox_claim_*`, `geox_well_*`, `geox_map_*`, `geox_evidence`, `geox_contradiction_scan` (32 tools) | Geoscience, seismic, basin, petrophysics |
| **WEALTH** | 18082 | `capital_primitive` (npv/irr/emv/mc/kelly/markowitz), `capital_market`, `capital_health`, `capital_diagnose`, `capital_entropy`, `capital_wisdom`, `capital_ledger` | Capital math, market data, risk, portfolio |
| **WELL** | 18083 | 7 tools: `well_assess_homeostasis`, `well_validate_vitality`, `well_guard_dignity`, `well_classify_substrate`, `well_trace_lineage`, `well_check_repair`, `well_assess_reliability` | Human readiness, vitality, fatigue, dignity (REFLECT_ONLY) |

## 4. MCP servers — Free lane

| Server | Port | Use when |
|---|---|---|
| **hermes** (FLAME) | 18901 | `hermes_fact_check`, `hermes_epistemic_check`, `hermes_plan_review`, `hermes_memory_steward`, `hermes_cross_verify`, `hermes_health` — FREE, RM0, stateless |

**Route here FIRST.** All `hermes_*` are free. Never burn governed tokens for what FLAME does for free.

## 5. MCP servers — Research & data

| Server | Key tools | Use when |
|---|---|---|
| brave-search | `brave_web_search`, `brave_news_search` | Fast web + news |
| perplexity | `perplexity_search`, `perplexity_research` | Multi-source grounded research |
| sequential-thinking | `step_by_step_plan`, `analyze_problem` | Structured multi-step reasoning |
| context7 | `resolve-library-id`, `query-docs` | Up-to-date library docs |
| fetch | `fetch_readable`, `fetch_markdown`, `fetch_youtube_transcript` | URL extraction |
| exa | `web_search_exa`, `web_fetch_exa` | Semantic web search |
| postgres / supabase / qdrant / sqlite | query + schema | Direct data access |
| megamemory | concept graph | Knowledge graph |

## 6. MCP servers — Infrastructure

| Server | Use when |
|---|---|
| github (governed) | PR, issues, code search |
| docker (governed) | Container lifecycle |
| hostinger-vps (governed) | VPS management |
| playwright | Browser automation |

## 7. MCP servers — Media (MiniMax)

> ⚠️ **Cost warning:** all `minimax-mcp` tools incur API costs. Use when explicitly requested.

| Tool | Model | Use |
|---|---|---|
| `text_to_image` | image-01 | Image gen (1-9/call, aspect ratios) |
| `generate_video` | T2V-01, I2V-01, Hailuo-02 | Video gen (6-10s, 768P/1080P) |
| `text_to_audio` | speech-2.6-hd | TTS (30+ voices) |
| `voice_clone`, `voice_design` | — | Voice |
| `music_generation` | music-1.5 | Music (up to 1 min, [Verse][Chorus] tags) |

## 8. Tool selection (one-line)

| Need | Tool |
|---|---|
| Reason/plan | `sequential-thinking` (free) |
| Verify claim | `hermes_fact_check` (FLAME, free) |
| Governance/judgment | `arifos` (arif_*) |
| Build/deploy/execute | `aforge` (forge_*) |
| Geology/seismic | `geox` (geox_*) |
| Finance/risk | `wealth` (capital_*) |
| Health/vitality | `well` (well_*) |
| Web search | brave-search or perplexity |
| Library docs | context7 |
| URL fetch | fetch |
| DB query | postgres or supabase |
| Vector search | qdrant |
| Browser | playwright or aforge |
| Live FQ | `curl :7073/health | jq .fq` |
| F8 G (constitutional) | `forge_evaluate` (is_canonical_g=true) |
| J (task sensitivity) | `forge_apex_encode` (is_canonical_g=false) |
| Recompute high-J | `forge_apex_recompute` (|J|>0.6) |

## 9. G-space vs J-space — DO NOT MIX (F2/F8)

| Tool | Space | is_canonical_g | Use for | HARAM if |
|---|---|---|---|---|
| `forge_evaluate` | G-space | **true** | F8 GENIUS, SEAL/REVIEW/VOID | skipped when G required |
| `forge_apex_encode` | J-space | **false** | Goal→tasks, G_local only | treated as constitutional G |
| `forge_apex_recompute` | J-space | **false** | Recompute on field change | used as F8 score |
| arifFlow `:7073/health` | FQ | n/a | Execute/verify rhythm | folded into G |

```
G = (A × P × E × X)^(1/4)     P = Physics (not Purpose) — F13 frozen
J = ∂T/∂G                     high |J| > 0.6 → recompute
FQ = metabolism pulse         live SOT = :7073; flow_state.json = cache TTL 5 min
```

## 10. Model rotation (canonical → `/root/AAA/registries/models/AGENT_MODEL_MAP.json`)

**Live provider state (2026-08-12):**

| Provider | Balance | Status |
|---|---|---|
| zai-direct | live | ✅ LIVE (current 333-AGI session) |
| opencode-zen | live | ✅ LIVE — full 1M GLM-5.2 |
| mimo-token-plan | live | ✅ LIVE |
| bailian-payg | live | ✅ LIVE |
| minimax | live | ✅ LIVE |
| opencode-go | live | ✅ LIVE |
| litellm-federation :4000 | sovereign FED | ✅ LIVE (1M ctx, models: agi-333, asi-555, apex-888, i-arif) |
| deepseek direct | live | ✅ LIVE |
| qwen-token-plan-team | live | ✅ LIVE |

**Agent → model assignments:**

| Agent | Primary | Notes |
|---|---|---|
| 333-AGI (OpenCode) | `zai-direct/glm-5.2` | 198K ctx cap (Coding Plan); switch to `opencode-zen/glm-5.2` for 1M |
| 555-ASI | `litellm-federation/asi-555` | memory + reasoning_content correct |
| 777-FORGE | `litellm-federation/agi-333` | 384K output, deep thinking |
| 888-APEX | `litellm-federation/apex-888` | constitutional, 384K output |
| i-arif (sovereign) | `litellm-federation/i-arif` | ARIF lane handle |

**Cost discipline:** FLAME (free) first → cheap (deepseek-v4-flash, mimo) → heavy (deepseek-v4-pro, zai-glm-5.2) → apex (multi-step constitutional).

## 11. Tool pre-flight (run before any MCP call)

```bash
for svc in arifos:8088 aforge:7071 aaa:3001 geox:8081 wealth:18082 well:18083; do
  n="${svc%%:*}"; p="${svc##*:}"
  curl -sf "http://localhost:$p/health" >/dev/null 2>&1 && echo "✅ $n" || echo "❌ $n"
done
curl -sf http://localhost:18901/health  # FLAME
curl -sf http://localhost:7073/health   # arifFlow
```

If a server is DOWN, proceed read-only on live servers. Don't assume dead server config is valid.

## 12. Provider name SOT (no ghost refs)

**Rule:** the model string in `opencode.json` MUST match the provider's `/v1/models` listing. Validate at config-load time.

**Common ghosts (DO NOT use):** `fed/fast`, `fed/reasoning-heavy` (only valid for `fed` provider at :4010, which is NOT in enabled_providers — use `litellm-federation/agi-333` instead).

**Canonical SOT for provider names:** FED DB. Config and FED are views.

## 13. Boot probes (copy-paste)

```bash
# Kernel health
curl -sf http://127.0.0.1:8088/health | jq '{verdict: .thermodynamic.verdict, floors: .floors_active, drift: .runtime_drift, tools: .tools_loaded}'

# Organ probe
for p in 8088 7071 7072 7073 3001 8081 18082 18083 18901; do
  s=$(curl -sf http://127.0.0.1:$p/health | jq -r .status 2>/dev/null)
  echo ":$p $s"
done

# arifFlow FQ
curl -sf http://127.0.0.1:7073/health | jq '{fq: .fq, receipts: .receipts, cycle: .invariants.cycle_count}'

# Seal chain
tail -1 /root/.local/share/arifos/vault999/seal_chain.jsonl 2>/dev/null | jq .

# Carry-forward
jq '{session: .session_id, actor: .actor, open_loops: .open_loops_888_HOLD}' /root/.local/share/arifos/carry_forward.json 2>/dev/null
```

*Aligned: 2026-08-12 (3-file zen consolidation)*
*DITEMPA BUKAN DIBEI ⚒️*
