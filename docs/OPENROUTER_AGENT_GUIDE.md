# OpenRouter — Agent Operations Guide

> **Audience:** AAA OpenCode agent (any session). Operational reference, not strategic doctrine.
> **Strategic doctrine:** `/root/AAA/docs/OPENROUTER_ZEN_OPTIMIZATION.md` (read first if you need
> the *why*; this doc is the *what* and *how*).
> **Forged:** 2026-07-24 · **SOT:** `/root/AAA/registries/models/AGENT_MODEL_MAP.json`

---

## 0. TL;DR for the agent

OpenRouter is the federation's **unified LLM routing layer** (provider_id `openrouter`, status ACTIVE).
You can route to **343 models from 58 providers** behind one OpenAI-compatible endpoint, with
intelligent auto-classification, session stickiness, prompt caching, ZDR enforcement, and
programmable guardrails. **Use it freely for non-sovereign tasks; route MY governance, 666_JUDGE,
and 999_SEAL through DeepSeek V4 Pro direct.**

Three things you must know:

1. **Auto-router's identity is unverified** — never use it for irreversible decisions
2. **Cost/quality is a 0-10 dial**, not a global setting — set per role per request
3. **Workspace guardrails silently 404 disallowed models** — if your call returns 404, check the
   guardrail config before assuming the model is down

---

## 1. Auth — where the keys live

| Variable | Source | Used by | Notes |
|---|---|---|---|
| `OPENROUTER_API_KEY` | `/root/.secrets/vault.env` (mode 600) | All OpenAI-compatible API calls | `${env:OPENROUTER_API_KEY}` in opencode.json |
| `OPENROUTER_MANAGEMENT_KEY` | `/root/.secrets/vault.env` (mode 600) | Management API only (guardrails, key rotation) | Treat as rotation-pending F13 SOVEREIGN |

**Operational rules:**
- Read both from env, **never** from `~/.bash_history`, chat, VAULT999, or logs
- `${env:OPENROUTER_API_KEY}` is the substitution used in `opencode.json` line 96
- Management key calls go to `https://openrouter.ai/api/v1/*` (NOT `/api/v1/chat/completions`)
- Both keys are `sk-or-v1-*` prefix; treat the management key as privileged (it can mint sub-keys)
- **If rotation is in progress**: stop using the management key until F13 confirmation

**OAuth flow** (MCP server only): `https://mcp.openrouter.ai/mcp` triggers a browser OAuth on first
connect. The minted key is **scoped and 7-day expiring**. The flow is blocked pending management
key rotation (F12 INJECTION). Once unblocked, the flow:
1. Browser opens `openrouter.ai` OAuth consent
2. User approves
3. Minted key cached at `/root/.local/share/opencode/auth.json` (mode 600)
4. Refresh on subsequent calls; no re-prompt until expiry

---

## 2. Current wired state (read-only)

These are the live files — do not hand-edit; regenerate via SOT-driven renderers.

```
/root/.config/opencode/opencode.json
├── provider.openrouter        # 10 models, baseURL https://openrouter.ai/api/v1
├── provider.openrouter.headers.HTTP-Referer = "https://arif-fazil.com"
├── provider.openrouter.headers.X-Title      = "arifOS Federation"
└── mcp.openrouter.url         = "https://mcp.openrouter.ai/mcp" (enabled, remote)

/root/AAA/registries/models/AGENT_MODEL_MAP.json
├── providers[openrouter]      # status=ACTIVE, jurisdiction=US Cloudflare Workers, ZDR=true
└── models[6 entries]          # openai/gpt-5.6-sol, xai/grok-4.5,
                               # openrouter/auto-beta, openrouter/auto, openrouter/free,
                               # meta-llama/llama-3.2-3b-instruct:free
```

**Configured OpenRouter models in opencode.json** (10): `auto-beta`, `auto`, `free`,
`meta-llama/llama-3.2-3b-instruct:free`, plus 2 DeepSeek R1 + 2 latest-alias entries from the
2026-07-24 integration. **Configured in SOT** (6 — the canonical set): the same plus
`openai/gpt-5.6-sol` (Codex agent primary via OpenRouter) and `xai/grok-4.5` (Grok agent).

**Routing rules referencing OpenRouter in SOT** (4 priorities):
- `openrouter/auto-beta` is fallback priority 2 in Hermes, OpenClaw, Forge, FORGE primary chains
- `openrouter/free` is fallback priority 3 in Hermes, OpenClaw chains (RM0 last remote tier)
- Conditions: `minimax_429_or_unavailable`, `mimo_unavailable`, `bailian_unavailable`,
  `openrouter_unavailable_or_budget`, `all_remote_down`
- `cost_quality_tradeoff`: 9 (cheap) for all OpenRouter fallbacks

---

## 3. The 343-model catalog (highlights for AAA)

OpenRouter exposes 343 models across 58 providers. Live count is from
`GET https://openrouter.ai/api/v1/models` (no auth required).

### 3.1 Top providers by count

| Provider | Models | Jurisdiction | ZDR-safe? |
|---|---|---|---|
| `openai` | 67 | US | partial |
| `qwen` | 47 | CN | yes |
| `google` | 30 | US | partial |
| `mistralai` | 19 | EU/FR | yes |
| `anthropic` | 15 | US | partial |
| `z-ai` | 12 | CN | yes |
| `deepseek` | 11 | CN | yes |
| `nvidia` | 10 | US | yes (free tiers) |
| `meta-llama` | 8 | US | yes |
| `minimax` | 8 | CN | **NO** (SHADOW-MM-001) |
| `moonshotai` | 7 | CN | yes |
| `poolside` | 6 | US | partial |
| `x-ai` | 5 | US | yes |
| `cohere` | 5 | US | partial |

### 3.2 Free models (~50, RM0) — AAA FLAME candidates

Top free picks by context + capability:

```
inclusionai/ling-3.0-flash:free         ctx=262K   MoE 124B/5.1B active, agentic-optimized
nvidia/nemotron-3-super-120b-a12b:free  ctx=1M     MoE 120B/12B active, 1M context
nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free  ctx=256K   reasoning + multimodal
google/gemma-4-31b-it:free             ctx=262K   31B dense, multimodal
google/gemma-4-26b-a4b-it:free          ctx=262K   26B MoE
poolside/laguna-s-2.1:free              ctx=262K   118B/8B coding agent
poolside/laguna-xs-2.1:free             ctx=262K   coding, lightweight
nvidia/nemotron-3-ultra-550b-a55b:free  ctx=1M     550B/55B, hard-reasoning
openai/gpt-oss-20b:free                 ctx=131K   reasoning
cohere/north-mini-code:free             ctx=256K   coding, small
meta-llama/llama-3.2-3b-instruct:free   ctx=131K   3B, trivial tasks only
openrouter/free                         ctx=200K   auto-router over free models
```

### 3.3 Reasoning models with thinking modes (~70+)

Mandatory or default-enabled reasoning. Examples:
`google/gemini-3.6-flash`, `x-ai/grok-4.5`, `anthropic/claude-fable-5`, `openai/gpt-5.6-luna-pro`,
`qwen/qwen3.7-max`, `z-ai/glm-5.2`, `moonshotai/kimi-k2.7-code`, `sakana/fugu-ultra`,
`inclusionai/ring-2.6-1t`, `moonshotai/kimi-k2-thinking`, `allenai/olmo-3-32b-think`,
`qwen/qwen3-vl-235b-a22b-thinking`, `moonshotai/kimi-k3`.

### 3.4 Top-quality paid (Anthropic + OpenAI premium, US jurisdiction)

```
anthropic/claude-opus-4.8        ctx=1M   reasoning + tools
anthropic/claude-opus-4.7-fast   ctx=1M   fast variant
anthropic/claude-opus-4.6        ctx=1M   previous-gen flagship
openai/gpt-5.5-pro               ctx=1.05M
openai/gpt-5.4-pro               ctx=1.05M
openai/o1-pro / o3-pro           ctx=200K   reasoning-specific
```

⚠️ All US jurisdiction (Cloud Act exposed). Use ZDR + per-request guardrails for any
sovereign-adjacent content.

### 3.5 Long-context (1M+) cheap models

```
xiaomi/mimo-v2.5                          $0.0000/M  ctx=1050K   ZDR-safe, CN
meta-llama/llama-4-scout                  $0.0000/M  ctx=1310K   ZDR-safe, open weights
meta-llama/llama-4-maverick               $0.0000/M  ctx=1048K   open weights
deepseek/deepseek-v4-flash                $0.0000/M  ctx=1048K   CN, ZDR-safe
qwen/qwen3.5-flash-02-23                  $0.0000/M  ctx=1000K   ZDR-safe
google/gemini-2.5-flash-lite              $0.0000/M  ctx=1048K   US
poolside/laguna-s-2.1                     $0.0000/M  ctx=1048K   coding agent
```

---

## 4. The Auto Router (your primary abstraction)

`openrouter/auto-beta` is the federation's smart fallback. Powered by OpenRouter's task-type
rankings (community spend share, 7-day rolling window), not NotDiamond.

### 4.1 How it picks

1. **Classify** the prompt into ~30 fine-grained task types (`code:debugging`,
   `agent:multi_step_planning`, `qa_knowledge`, `math`, `customer_support`, `research_report`, etc.)
2. **Rank** candidate models by trailing-7-day spend share for that task type
3. **Filter** by your `cost_quality_tradeoff` setting (cost-percentile ceiling)
4. **Route** with fallbacks; honor `allowed_models` and output-modality requirements
5. **Pin** model + provider per `session_id` for 5-minute stickiness

### 4.2 Cost/Quality Tradeoff (CQT) — set per role

```
0  = pure quality   (always picks most capable, up to 90th cost percentile)
3  = quality-leaning
5  = balanced       (default for FORGE work)
7  = cost-leaning   (auto-router deprecated default)
9  = RM-leaning     (auto-beta default, cheap model wins)
10 = cheapest decile only
```

**The scale is INVERTED from intuition:** higher = cheaper. AAA per-role settings:

| Role | CQT |
|---|---|
| 666_JUDGE / 999_SEAL | **never use auto-router** |
| 333_THINK (constitutional) | 3 |
| 777_FORGE | 5 |
| 555_MEMORY | 5 |
| 444_ROUTE | 9 |
| 111_OBSERVE | 10 |
| FLAME / tool tasks | 10 |

### 4.3 Allowed models (the most important knob)

Restrict the candidate pool via `allowed_models` with wildcards:

```json
"plugins": [{
  "id": "auto-router",
  "allowed_models": [
    "z-ai/*", "mistralai/*", "x-ai/*", "meta-llama/*",
    "deepseek/*", "qwen/*", "xiaomi/*"
  ],
  "cost_quality_tradeoff": 5
}]
```

| Pattern | Matches |
|---|---|
| `anthropic/*` | All Anthropic models |
| `openai/gpt-5*` | All GPT-5 variants |
| `google/*` | All Google models |
| `openai/gpt-5.1` | Exact match only |
| `*/claude-*` | Any provider with claude in name |

### 4.4 Session stickiness

```python
import uuid
session_id = f"aaa-{AGENT_ID}-{uuid.uuid4()}"

response = openrouter.chat.send(
    model="openrouter/auto-beta",
    session_id=session_id,  # or x-session-id header
    ...
)
```

**Implicit stickiness:** OpenRouter derives a fingerprint from system + first user messages
once the upstream reports cache usage. **Explicit stickiness:** `session_id` pin kicks in
on first successful response. Both expire after 5 minutes of inactivity. Provider errors do
NOT update the cache (next request can re-route).

### 4.5 The `model` response field

Every response includes the actual model selected:

```json
{
  "id": "gen-...",
  "model": "anthropic/claude-sonnet-4.5",  // ← actual model used
  "choices": [...],
  "usage": {...}
}
```

**Audit this field.** Log it. Compare against expected. Auto-router drift detection.

---

## 5. Guardrails (Management-key gated)

Five categories, all configurable via Management API or Workspaces > Guardrails UI:

| Type | What it does | AAA use |
|---|---|---|
| **Budget** | Per-entity USD caps, daily/weekly/monthly | $50/day per guardrail ceiling |
| **ZDR** | Per-account / per-model / per-request Zero Data Retention | Sovereign workloads: ALWAYS on |
| **Model/provider restrictions** | Allowlist or blocklist | Closed allowlist for sovereign work |
| **Prompt injection defense** | 30+ OWASP-derived regex patterns, 3 actions (flag/redact/block) | `block` for production |
| **DLP** | 7 built-in PII types + custom regex | Email/phone redact, IP block |

Actions for filter hits: **flag** (log only), **redact** (replace with `[SLUG]`), **block** (403).

### 5.1 Recommended AAA baseline (when provisioning)

```json
{
  "name": "aaa-sovereign-guardrail",
  "limit_usd": 50,
  "reset_interval": "daily",
  "allowed_models": [
    "z-ai/*", "mistralai/*", "x-ai/*", "meta-llama/*",
    "deepseek/*", "qwen/*", "xiaomi/*",
    "google/gemma-4-31b-it:free",
    "google/gemma-4-26b-a4b-it:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
    "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b:free"
  ],
  "blocked_models": ["minimax/*"],
  "content_filter_builtins": [
    {"slug": "regex-prompt-injection", "action": "block"},
    {"slug": "email", "action": "redact"},
    {"slug": "phone", "action": "redact"},
    {"slug": "ip_address", "action": "redact"}
  ],
  "zdr": true
}
```

### 5.2 Blast-radius warning (READ THIS)

**Workspace guardrails can only be MORE restrictive than account-wide settings.** Disallowed
requests fail with **silent 404**, not 401/403. Affected callers get no diagnostic signal.

Before provisioning the blocklist, audit agents whose fallback chains include blocked models
(OPS, OpenClaw) and re-route them first. See §11 for the audit table.

### 5.3 Management API calls

```
POST   /api/v1/guardrails        # create
GET    /api/v1/guardrails        # list
PATCH  /api/v1/guardrails/{id}   # update
DELETE /api/v1/guardrails/{id}   # delete
POST   /api/v1/keys/{key_id}/rotate   # rotate sub-keys
DELETE /api/v1/keys/{key_id}          # revoke sub-keys

Headers: Authorization: Bearer $OPENROUTER_MANAGEMENT_KEY
```

Provisioning script lives in `/root/AAA/scripts/provision-openrouter-guardrail.py`
(written 2026-07-24; pending F13 rotation before execution).

---

## 6. The MCP Server (`https://mcp.openrouter.ai/mcp`)

OAuth-authenticated remote MCP. **15 tools** (per `_added_reason` in opencode.json line 1288):

| Tool | Purpose |
|---|---|
| `list-models` | Enumerate catalog (343 models) |
| `get-model` | Detail on one model (pricing, capabilities, ZDR) |
| `list-benchmarks` | Cross-provider benchmark rankings |
| `get-credits` | Real-time credit balance |
| `get-generation` | Per-request cost breakdown |
| `list-daily-model-rankings` | Auto-router spend-share history |
| `list-task-classifications` | The 30 task types the router knows |
| `search-docs` | Search OpenRouter docs |
| `send-message` | Test inference without leaving editor |
| (others) | Provider stats, generation metadata |

**Auth:** OAuth PKCE, browser-driven. Token cached at `/root/.local/share/opencode/auth.json`
(mode 600). Minted key is scoped ($10 cap, 7-day expiry). Status: **blocked pending
management key rotation.**

Once unblocked, agent workflow:
1. Call `list-models` to enumerate
2. Filter by capability, context, ZDR
3. Call `get-credits` before large batches
4. Call `get-generation` after each call for cost attribution

---

## 7. Server-side tools (in `/v1/chat/completions`)

Available via plugins in the request body. Compute on OpenRouter's edge, no client work.

| Tool | What it does |
|---|---|
| **advisor** | Consult a stronger model mid-generation |
| **subagent** | Delegate sub-task to a cheaper model |
| **fusion** | Multi-model panel — query N models, synthesize to one answer |
| **web_search** | OpenRouter-managed web search augmentation |

Plugins go in the `plugins` array. Example for fusion:

```json
{
  "model": "openrouter/fusion",
  "plugins": [{"id": "fusion", "preset": "general-budget"}],
  "messages": [...]
}
```

Fusion presets: `<task>-<tier>` where `tier` is `high` / `budget` / `fast`.

---

## 8. Constitutional role mapping (operational summary)

This is the SOT-condensed view. Full version: `/root/AAA/docs/OPENROUTER_ZEN_OPTIMIZATION.md` §2.

| Role | OpenRouter usage |
|---|---|
| 000_INIT | **NEVER** — sovereign identity, no third party |
| 111_OBSERVE | `openrouter/free` (cqt=10), Groq, MiMo free |
| 333_THINK | `openrouter/auto-beta` (cqt=3) when DeepSeek down |
| 444_ROUTE | `openrouter/auto-beta` for classification only (cqt=9) |
| 555_MEMORY | `xiaomi/mimo-v2.5` (1M), `meta-llama/llama-4-scout` (1.3M) |
| 666_JUDGE | **NEVER** — DeepSeek V4 Pro direct only |
| 777_FORGE | `openrouter/auto-beta` (cqt=5), `z-ai/glm-5.2` |
| 999_SEAL | **NEVER** — DeepSeek V4 Pro direct only |

---

## 9. Sovereignty & censorship

### 9.1 ZDR — Zero Data Retention

| Data class | ZDR required | Mechanism |
|---|---|---|
| MY governance / PETRONAS / 1MDB | YES | `zdr: true` per request + provider allowlist |
| PII (myKad, phone, email) | YES | DLP guardrail + `zdr: true` |
| Constitutional content | YES | Workspace-level ZDR enforced |
| Public web fetches | NO | Standard routing |
| Free-tier tool tasks | NO | Standard routing |

ZDR-safe provider allowlist: `z-ai`, `mistralai`, `x-ai`, `meta-llama`, `deepseek`, `qwen`, `xiaomi`.

**EU residency:** `eu.openrouter.ai` endpoint (when available).

### 9.2 Censorship shadows to know

| Shadow | Model | Severity | What to do |
|---|---|---|---|
| SHADOW-MM-001 | `minimax/*` | CRITICAL | NEVER for MY governance; censored content masquerades as ignorance |
| SHADOW-DS-001 | `deepseek/*` | HIGH | BM proper nouns may fabricate; verify against sources |
| SHADOW-OR-001 (drafted) | `openrouter/auto-beta` | HIGH | Community-spend may route to censored vendor; allowlist bypasses |

### 9.3 Sovereign-task hard rules

For ANY task touching MY governance, PETRONAS, 1MDB, Najib, Jho Low, myKad:
1. **Route to DeepSeek V4 Pro DIRECT** (not via OpenRouter)
2. Set `zdr: true` even if going direct
3. Custom regex guardrails: `Najib|1MDB|PETRONAS|Jho_Low|Malaysian_governance`
4. Log call for F11 audit

---

## 10. Cost optimization patterns

### 10.1 Per-call CQT

```python
# Default for general agent work
openrouter.chat.send(model="openrouter/auto-beta",
                     plugins=[{"id": "auto-router", "cost_quality_tradeoff": 5}])

# Cheap bulk work
openrouter.chat.send(model="openrouter/auto-beta",
                     plugins=[{"id": "auto-router", "cost_quality_tradeoff": 9}])

# Quality-leaning reasoning
openrouter.chat.send(model="openrouter/auto-beta",
                     plugins=[{"id": "auto-router", "cost_quality_tradeoff": 3}])
```

### 10.2 Prompt caching (Anthropic models)

182 of 343 models support prompt caching. Cache reads typically cost 10% of normal input.
Add `cache_control: {"type": "ephemeral"}` at the last cacheable block:

```json
{
  "messages": [
    {"role": "system", "content": "...12 files of kernel...",
     "cache_control": {"type": "ephemeral"}},
    {"role": "user", "content": "..."}
  ]
}
```

Apply to Hermes (12-file kernel, ~8K tokens), Forge, Auditor. **Expected savings: 70-90% on
repeat system prompts.**

### 10.3 Provider pinning

Force specific upstream for residency / ZDR / cost:

```json
"provider": {
  "order": ["Azure", "AWS"],
  "allow_fallbacks": true,
  "require_parameters": true
}
```

Use cases:
- ZDR-safe providers only
- Forbid PRC-blocked providers for sovereign data
- Pin to cheapest upstream for free-tier models

### 10.4 Free router fallback

For RM0 last-resort: `openrouter/free` (cqt=10, auto-routes over free models only).
Routes to NVIDIA Nemotron free tier, Gemma 4 free, Poolside free, etc.

---

## 11. Latency optimization

### 11.1 Session stickiness — see §4.4

`x-session-id` header or `session_id` field. 5-min TTL. Saves ~30% on follow-up turns via
provider pin + prompt cache hit.

### 11.2 Streaming

Supported across all standard OpenRouter features. Set `"stream": true`.

### 11.3 Fallback chain ordering

OpenRouter sorts candidate models by your cqt ranking + community spend share, then
transparently fails over on 5xx/429/network errors. Failure modes:

| Error | OpenRouter response | Recovery |
|---|---|---|
| Model 404 | `{"error": {"code": 404}}` | Check guardrail — likely silently blocked |
| Model 429 | Rate limit, retries upstream | Backoff; circuit breaker kicks in |
| Model 500 | Upstream outage | Auto-failover to next in rank |
| All down | Returns error | Agent fallback chain kicks in (FLAME, ollama) |

---

## 12. Forbidden patterns

| Pattern | Forbidden? | Why |
|---|---|---|
| Auto-router for 666_JUDGE / 999_SEAL | YES | identity_verified: false, no fff_gate |
| Auto-router for MY governance | YES | Censorship risk via MiniMax in pool |
| Auto-router with ZDR disabled for PII | YES | F2 TRUTH + sovereign exposure |
| `minimax/*` for any topic | YES | SHADOW-MM-001 |
| OAuth flow / Management API with chat-exposed keys | YES | F12 INJECTION — rotate first |
| Workspace guardrail tighter than any agent needs | AVOID | Silent 404s, no caller signal |
| Hand-edit `opencode.json` after SOT setup | AVOID | Drift; use `opencode_render.py --write` |
| Use `auto-beta` to "discover" the best model | AVOID | F11 AUDITABILITY — use static SOT |
| Skip the `model` response field logging | AVOID | Lose audit trail; can't detect drift |
| Read API/management keys into logs/VAULT999/chat | YES | F12 INJECTION + LOCALHOST_IS_PASSWORD |

---

## 13. Operational status (live)

| Item | State | Updated |
|---|---|---|
| Provider registration | ACTIVE in SOT | 2026-07-24 |
| 10 OpenRouter models in `opencode.json` | WIRED | 2026-07-24 |
| MCP server entry | WIRED (enabled, remote, OAuth-pending) | 2026-07-24 |
| `OPENROUTER_API_KEY` in vault.env | PRESENT | pre-2026-07-24 |
| `OPENROUTER_MANAGEMENT_KEY` in vault.env | PRESENT, **rotation-pending** | pre-2026-07-24 |
| Workspace guardrail | NOT PROVISIONED | awaiting F13 rotation |
| OAuth flow at `mcp.openrouter.ai/mcp` | NOT TRIGGERED | awaiting F13 rotation |
| SOT shadow SHADOW-OR-001 | DRAFTED in §5.2 of Zen doc | 2026-07-24 |
| Per-role CQT in SOT routing_rules | DRAFTED in §10.1 of Zen doc | 2026-07-24 |
| 4 new SOT routing rules (zdr/cqt per role) | DRAFTED, awaiting F13 approval | 2026-07-24 |

---

## 14. Operational references (paths)

| Path | Purpose |
|---|---|
| `/root/.secrets/vault.env` | OPENROUTER_API_KEY + OPENROUTER_MANAGEMENT_KEY (mode 600) |
| `/root/.config/opencode/opencode.json` | Live provider config (10 OpenRouter models + MCP) |
| `/root/AAA/registries/models/AGENT_MODEL_MAP.json` | Canonical SOT — provider, models, routing_rules |
| `/root/AAA/docs/OPENROUTER_ZEN_OPTIMIZATION.md` | Strategic doctrine (this doc's parent) |
| `/root/AAA/scripts/provision-openrouter-guardrail.py` | Management API script (pending rotation) |
| `/root/AAA/src/resolvers/opencode_render.py` | SOT → opencode.json renderer |
| `/root/.local/share/opencode/auth.json` | OAuth MCP token cache (mode 600) |
| `/root/.local/share/flame/flame_hitrate.jsonl` | FLAME call ledger |
| `/root/.local/share/arifos/flame_state.json` | FLAME dynamic state |

---

## 15. Quick reference card

```
┌─────────────────────────────────────────────────────────────┐
│  AAA × OpenRouter Decision Card (paste into system prompt)  │
├─────────────────────────────────────────────────────────────┤
│  Task → Role → Model → CQT → ZDR → Allowlist                │
│                                                             │
│  000_INIT  → DeepSeek V4 Pro direct │ no OR                 │
│  111_OBS  → openrouter/free        │ cqt=10 │ no ZDR needed │
│  333_THINK→ auto-beta OR DeepSeek   │ cqt=3  │ ZDR required │
│  444_ROUTE→ auto-beta classifier   │ cqt=9  │ ZDR required │
│  555_MEM  → xiaomi/mimo-v2.5 (1M)   │ cqt=5  │ ZDR required │
│  666_JUDGE→ DeepSeek V4 Pro DIRECT  │ never use OR          │
│  777_FORGE→ auto-beta OR kimi-k2.7  │ cqt=5  │ ZDR required │
│  999_SEAL → DeepSeek V4 Pro DIRECT  │ never use OR          │
│                                                             │
│  Always: session_id, cache_control, allowed_models ZDR-safe │
│  Never:  MY governance, 666_JUDGE, 999_SEAL via OR         │
│  Audit:  response.model field, F11 AUDITABILITY             │
└─────────────────────────────────────────────────────────────┘
```

---

## DITEMPA BUKAN DIBERI

Forged from live `/api/v1/models` probe (2026-07-24) + AAA SOT cross-reference + OpenRouter
Guardrails/Auto-Router/MCP docs. ΔS ≤ 0 on every section. **Co-Authored-By:** Kimi Code (FI-008)
for AAA OpenCode agents.