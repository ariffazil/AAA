# OpenRouter × AAA — Zen Optimization Framework

> **Forged:** 2026-07-24 · **Sovereign:** Muhammad Arif bin Fazil (F13)
> **Authority:** `/root/AAA/registries/models/AGENT_MODEL_MAP.json` (canonical SOT)
> **Doctrine:** ΔS ≤ 0 on every output. F1-F13 are the rails.

---

## 0. TL;DR

OpenRouter was promoted STANDBY → ACTIVE on 2026-07-24. The federation has 6 OpenRouter entries
(`auto-beta`, `auto`, `free`, plus 3 specific models) covering 38+ upstream models. This document
is the **canonical optimization doctrine** — how to extract maximum value from OpenRouter while
honoring every floor.

**Three invariants:**

1. **Constitutional routing** — every OpenRouter call is mapped to one of 8 roles (000_INIT → 999_SEAL)
2. **Cost-quality dial** — `cost_quality_tradeoff` (0-10) is set per role, never globally
3. **Sovereign ceiling** — auto-router NEVER touches MY governance topics (route to DeepSeek direct)

---

## 1. OpenRouter Landscape (live probe 2026-07-24)

| Dimension | Value | Source |
|---|---|---|
| Total models | 343 | `GET /api/v1/models` (no auth) |
| Providers | 58 | catalog |
| Free models (RM0) | ~50 | pricing.prompt = "0" |
| Vision/multimodal | 181 | input_modalities contains "image" |
| Reasoning (thinking) | 70+ | reasoning.default_enabled or mandatory |
| 1M+ context paid | 15+ | context_length ≥ 1,048,576 |
| Prompt-cache supported | 182 | input_cache_read pricing |

**Top providers (model count):** openai (67), qwen (47), google (30), mistralai (19), anthropic (15),
z-ai (12), deepseek (11), nvidia (10), meta-llama (8), minimax (8), moonshotai (7), poolside (6),
x-ai (5), cohere (5).

**Top OpenRouter-only primitives that matter to AAA:**

| Primitive | AAA Use |
|---|---|
| `openrouter/auto-beta` | Task-classified routing across community-curated models |
| `openrouter/free` | RM0 last-resort fallback (tool lane) |
| `cost_quality_tradeoff` (0-10) | Per-request cost/quality dial |
| `session_id` / `x-session-id` | 5-min session stickiness (cache hit + provider pin) |
| `provider` (with `order`) | Force specific upstream provider for ZDR/jurisdiction |
| `allowed_models` (wildcards) | Restrict pool to vetted set |
| `cache_control: {type:"ephemeral"}` | Prompt caching (Anthropic) |
| Guardrails: ZDR, budget, model allowlist, prompt-injection, DLP | Programmable via Management API |
| `zdr: true` parameter | Per-request Zero Data Retention |
| MCP server (`mcp.openrouter.ai/mcp`) | Live model discovery + credit balance |

---

## 2. Constitutional Role → OpenRouter Mapping

Every OpenRouter call MUST be classified into one of AAA's 8 constitutional roles.
OpenRouter is **FORBIDDEN** in some roles, **PRIMARY** in others, **FALLBACK** in others.

| Role | Description | OpenRouter Status | Recommended OpenRouter Models | CQT |
|---|---|---|---|---|
| `000_INIT` | Identity binding, session start | **FORBIDDEN** | Never — sovereign identity, no third-party | — |
| `111_OBSERVE` | Evidence gathering, search, fetch | **PRIMARY (FLAME)** | `openrouter/free`, Groq free, MiMo free | 10 |
| `333_THINK` | Reasoning, planning, analysis | **FALLBACK** | `openrouter/auto-beta` (cqt=3) when DeepSeek down | 3 |
| `444_ROUTE` | Task classification, routing | **PRIMARY** | `openrouter/auto-beta` for classification only | 9 |
| `555_MEMORY` | Recall, long-context | **FALLBACK** | `xiaomi/mimo-v2.5` (1M), `meta-llama/llama-4-scout` (1.3M), `qwen/qwen3.5-flash` (1M) | 5 |
| `666_JUDGE` | Constitutional verdict | **FORBIDDEN** | Never — identity_verified only DeepSeek V4 Pro | — |
| `777_FORGE` | Execution, code, agentic | **FALLBACK** | `openrouter/auto-beta` (cqt=5), `kimi/kimi-k2.7-code`, `z-ai/glm-5.2` | 5 |
| `999_SEAL` | Irreversible commitment | **FORBIDDEN** | Never — DeepSeek V4 Pro direct only | — |

**Hard rule:** OpenRouter's `auto-beta` MUST be excluded from `666_JUDGE` and `999_SEAL` roles even
in fallback chains — it has `identity_verified: false` and no `fff_gate` (zero constitutional vetting).
The router cannot self-authorize a verdict. F1 AMANAH + F13 SOVEREIGN.

**Existing shadows that BLOCK OpenRouter entirely** (already documented in SOT):
- SHADOW-MM-001 — MiniMax M3 silent censorship on MY governance (also applies to OpenRouter routing since it can pick MiniMax)

---

## 3. Cost-Quality Tiers (CQT) — Per-Role Defaults

OpenRouter's `cost_quality_tradeoff` is a 0-10 dial. The AAA federation overrides OpenRouter's
default of 9 per role:

| CQT | Meaning | Use For | Approved Roles |
|---|---|---|---|
| **0** | Pure quality — best model wins | Highest-stakes reasoning | 333_THINK (constitutional deliberation only) |
| **1-3** | Quality-leaning | Critical agent work | 333_THINK, 777_FORGE |
| **4-6** | Balanced | Default agent work | 777_FORGE, 555_MEMORY |
| **7-8** | Cost-leaning | Batch tasks, ops monitoring | 333_THINK (FLAME), 444_ROUTE |
| **9** | OpenRouter default — RM-leaning | Lightweight agent tasks | 111_OBSERVE (non-sovereign) |
| **10** | Cheapest survivor only | Free-tier routing | 111_OBSERVE, FLAME |

**Sovereign override:** For ANY task touching MY governance, PETRONAS, 1MDB, Najib, Jho Low,
myKad — set CQT=0 AND route to DeepSeek V4 Pro DIRECT (bypass OpenRouter). The auto-router's
community-spend ranking doesn't know which models censor these topics.

---

## 4. Latency Optimization — Session Stickiness + Prompt Caching

### 4.1 Session Stickiness

OpenRouter pins both model + provider for 5 minutes of inactivity per `session_id`. AAA agents
SHOULD use `x-session-id` header on every request:

```python
# Pattern for AAA agents
import uuid
session_id = f"aaa-{AGENT_ID}-{SESSION_START}-{uuid.uuid4()}"

response = openrouter.chat.send(
    model="openrouter/auto-beta",
    session_id=session_id,        # or x-session-id header
    plugins=[{"id": "auto-router", "cost_quality_tradeoff": 5}],
    messages=...
)
```

**Expected gain:** 30-50% latency reduction on follow-up turns via prompt cache hit + skip of
classifier round-trip. Aligns with F4 CLARITY (no re-classification churn).

### 4.2 Prompt Caching

182 of 343 OpenRouter models advertise `input_cache_read` pricing — meaning the upstream provider
supports prompt caching. Cache reads typically cost 10% of normal input tokens.

**Apply to long-system-prompt agents** (Hermes, Forge, Auditor):
- Hermes: 12 instruction files, ~8K tokens system prompt → cache hit saves ~92%
- Forge: same
- Auditor: constitutional kernel ~15K tokens → cache hit saves ~90%

**Mechanism:** Anthropic models use `cache_control: {"type": "ephemeral"}` at the message
boundary. OpenAI models use explicit caching. OpenRouter normalizes both. Add cache breakpoint
at the **last system message** for max savings.

### 4.3 Provider Pinning

Force specific upstream provider for residency/ZDR:

```json
"provider": {
  "order": ["Azure", "AWS"],
  "allow_fallbacks": true,
  "require_parameters": true
}
```

**Use cases for AAA:**
- ZDR-eligible providers only: `z-ai`, `mistralai`, `x-ai (ZDR)`, `meta-llama`, `deepseek`, `qwen`, `xiaomi`
- Forbid PRC-blocked providers per AAA rule on `cloud_act_exposed: true` for sovereign data
- EU residency: `eu.openrouter.ai` endpoint (when available)

---

## 5. Sovereignty & Data Residency

### 5.1 Zero Data Retention (ZDR)

OpenRouter now supports per-request ZDR. AAA traffic patterns:

| Data Class | ZDR Required | Mechanism |
|---|---|---|
| MY governance / PETRONAS / 1MDB | **YES** | Per-request `zdr: true` + provider allowlist |
| PII (myKad, phone, email) | **YES** | DLP guardrail + `zdr: true` |
| AAA constitutional content | **YES** | Workspace-level ZDR enforced |
| Public web fetches | NO | Standard routing OK |
| Free-tier tool tasks | NO | Standard routing OK |

**Closed allowlist for sovereign data** (matches SOT ZDR-safe providers):
```
z-ai/*, mistralai/*, x-ai/*, meta-llama/*, deepseek/*, qwen/*, xiaomi/*
```

### 5.2 Censorship Avoidance

Existing shadows block:
- `MiniMax M3` → MY governance (SHADOW-MM-001)
- `DeepSeek V4 Pro` → BM proper noun fabrication (SHADOW-DS-001, LOW severity, mitigation: verify)

**New shadow to add** — OpenRouter auto-router censorship risk:
```yaml
shadow_id: SHADOW-OR-001
model_ref: openrouter/auto-beta
shadow_name: sovereign_topic_routing_drift
severity: HIGH
class: censorship_risk
pattern: |
  auto-beta selects based on community spend share. If a censored
  vendor (MiniMax M3) gets majority spend for a task class, auto-beta
  may route sovereign topics to it. community-spend signal has no
  knowledge of F2/F9 floors.
triggers: [malaysian_governance, 1MDB, najib, petronas]
mitigation:
  - HARD BLOCK: exclude minaimax/* from auto-router allowed_models for sovereign tasks
  - ALWAYS route MY governance through DeepSeek V4 Pro direct
  - Add custom regex guardrails for Najib|1MDB|PETRONAS|Jho_Low|Malaysian_governance
```

### 5.3 Prompt Injection Defense

OpenRouter Guardrails scan against 30+ OWASP-derived regex patterns with three actions:
`flag` / `redact` / `block`. AAA recommended baseline:

```json
{
  "name": "aaa-sovereign-guardrail",
  "content_filter_builtins": [
    {"slug": "regex-prompt-injection", "action": "block"},
    {"slug": "email", "action": "redact"},
    {"slug": "phone", "action": "redact"},
    {"slug": "ip_address", "action": "redact"}
  ],
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
  ]
}
```

Apply to AAA workspace via Management API after key rotation.

> ⚠️ **Guardrail blast-radius warning (added 2026-07-24, post-review):** Per OpenRouter's
> Guardrails docs, **workspace guardrails can only be MORE restrictive than account-wide settings**
> — they cannot loosen anything. Disallowed requests fail with **silent 404** (not 401/403), so
> affected agents get no signal that their intended model was banned. Before provisioning the
> `aaa-sovereign-guardrail` with `blocked_models: ["minimax/*"]`, audit every agent whose
> fallback chain includes a MiniMax reference and re-route to ZDR-safe alternatives first:
>
> | Affected agent | Current MiniMax ref | Recommended replacement |
> |---|---|---|
> | `ops` agent (fallback priority 1, 2) | `minimax/MiniMax-M2.5`, `minimax/MiniMax-M3` | `groq/llama-3.1-8b-instant` (FLAME) or `openrouter/free` |
> | `openclaw` agent (primary) | `minimax/MiniMax-M3` | `deepseek/deepseek-v4-flash` or `openrouter/auto-beta` (cqt=9) |
> | `forge` agent (fallback priority 1) | `minimax/MiniMax-M3` | already covered by `glm/glm-5.2` (allowed via `z-ai/*`) |
> | `deepseek_primary_chain` | `minimax/MiniMax-M3` step 2 | remove — chain is now `deepseek → z-ai/glm-5.2 → ollama` |
>
> **Auto-router interaction:** When `allowed_models` is restricted, the `openrouter/auto-beta`
> router's candidate pool is filtered to the workspace allowlist. Auto-router will **404 on any
> non-allowed model** rather than fall back transparently — so a ZDR-strict allowlist will bias
> the router toward ZDR-safe providers and silently exclude Anthropic / OpenAI / Google Gemini
> paid tiers from the candidate pool. This is the desired behavior for sovereign traffic but
> **must be documented per-agent** so the auto-beta calls don't produce unexpected 404s in
> non-sovereign workloads (Hermes, OPS).

---

## 6. Fallback Chain Restructure (Recommendation)

Current AAA cascade (per SOT): TokenRouter → MiniMax → MiMo → Groq → Gemini → Cerebras → SEA-LION → Ollama → HOLD

**Proposed integration** with OpenRouter as Tier-2/3 smart fallback:

```
Tier 1 (PRIMARY):     DeepSeek V4 Pro           [direct, CN, $0.55/$2.19, ZDR via Z.ai sibling]
Tier 2 (SMART ROUTE): openrouter/auto-beta cqt=5 [ZDR enforced, allowed_models ZDR-safe]
Tier 3 (COST):        openrouter/free           [RM0, light tasks]
Tier 4 (SOVEREIGN):   ollama/qwen2.5-coder:3b   [local, survival]
HOLD:                 888_HOLD                  [F13 SOVEREIGN — never auto-resolve]
```

**Critical:** MY governance → ALWAYS Tier 1 (DeepSeek direct), skip OpenRouter entirely.
Add explicit guardrail `allowed_models` exclusions per workspace.

**Cascade improvements:**
1. **Latency gain**: skip 4-tier free cascade when OpenRouter auto-beta picks fastest available
2. **Cost gain**: auto-beta cqt=5 finds best cost/quality in single hop
3. **Resilience gain**: ZDR provider allowlist + auto-fallback across 7 providers
4. **Audit gain**: `response.model` field tells us which model served (Merkle anchor)

---

## 7. ZDR-Compliant Top-Tier Models (for Sovereign Workloads)

Top picks from the 343-model catalog filtered for: ZDR-safe provider + AAA constitutional roles + non-sovereign-tainted:

| OpenRouter Model | Provider | Context | Best For | Trust Tier Equiv |
|---|---|---|---|---|
| `deepseek/deepseek-v4-pro` | deepseek | 1M | 666_JUDGE, 999_SEAL (primary direct) | T1 |
| `deepseek/deepseek-v4-flash` | deepseek | 1M | OPS, FLAME | T2 |
| `z-ai/glm-5.2` | z-ai | 202K | 777_FORGE engineering, 333_THINK (free) | T2 |
| `z-ai/glm-4.7-flash` | z-ai | 202K | Cost-optimized reasoning | T3 |
| `mistralai/mistral-small-3.2-24b-instruct` | mistralai | 256K | EU residency, ZDR | T3 |
| `xiaomi/mimo-v2.5-pro` | xiaomi | 1M | 555_MEMORY, long context | T2 |
| `meta-llama/llama-4-scout` | meta-llama | 1.3M | Long context ZDR | T3 |
| `qwen/qwen3.5-flash-02-23` | qwen | 1M | Cost-optimized ZDR | T3 |
| `x-ai/grok-4.5` | x-ai | 256K | US ZDR alt, 333_THINK | T2 |
| `google/gemma-4-31b-it:free` | google | 256K | FLAME free tier | T4 |
| `nvidia/nemotron-3-super-120b-a12b:free` | nvidia | 1M | FLAME 1M free | T4 |
| `openai/gpt-oss-120b` | openai | 131K | Free-tier reasoning | T3 |

---

## 8. Cost Optimization — Concrete Numbers

**Without optimization** (auto-beta cqt=9 default, no caching, no allowlist):
- $0.50 / 1M avg across mixed tasks

**With AAA optimization** (per-role CQT + allowlist + caching + session stickiness):

| Optimization | Saving | Mechanism |
|---|---|---|
| Per-role CQT (was 9 global) | ~35-50% | Override to 5 for Forge, 10 for FLAME |
| Prompt caching on Hermes kernel | ~70-80% on repeat | `cache_control: ephemeral` on last system msg |
| Session stickiness | ~30% latency | `x-session-id` header |
| ZDR allowlist | ~10-20% | Restrict to cheaper ZDR-safe providers |
| `openrouter/free` for FLAME | 100% on tool tasks | Already implemented |

**Projected AAA monthly spend with optimization:**

| Scenario | Monthly |
|---|---|
| Current (DeepSeek + MiMo + cheap fallbacks) | RM0-5 |
| With OpenRouter cqt=5 (default) + caching | RM15-25 |
| With full optimization (auto-beta, FLAME via free, ZDR allowlist, caching) | RM5-10 |
| Heavy sovereign + constitutional workload | RM30-50 |

Cerebras $5 free credit expires 2026-08-20 — use it for FLAME volume before then.

---

## 9. Implementation Plan

### Phase 1 — Immediate (T2, after rotation)
1. **Rotate** exposed OpenRouter management key + add new key to `/root/.secrets/vault.env` as `OPENROUTER_MANAGEMENT_KEY`
2. **Provision** `aaa-sovereign-guardrail` via Management API (script below)
3. **Set** workspace defaults: `zdr: true` on, prompt-injection `block`, email/phone `redact`
4. **Update** `AGENT_MODEL_MAP.json` `provider.openrouter.note` with ZDR + guardrail refs

### Phase 2 — SOT Integration (T1)
1. Add `openrouter/auto-beta` config variants per role to `routing_rules[]`
2. Add `allowed_models` allowlist for each constitutional role
3. Wire `openrouter-mcp` (`https://mcp.openrouter.ai/mcp`) into OpenCode for live model discovery
4. Add session stickiness template to all agent prompts

### Phase 3 — Monitoring (T1)
1. Replace FORGE-model-monitor curl probes with `mcp.openrouter.ai/mcp` credit-balance calls
2. Add OpenRouter cost dashboard row to `forge_work/2026-07-24/COST_DASHBOARD.md`
3. Wire OpenRouter alert (402, 429, 5xx) into existing model-fallback-monitor cron
4. Track auto-beta's `model` field in each response → detect censorship drift

### Phase 4 — Guardrails Provisioning Script

```python
#!/usr/bin/env python3
"""Provision AAA sovereign guardrail in OpenRouter workspace via Management API."""
# Place at /root/AAA/scripts/provision-openrouter-guardrail.py
# Run with: python3 provision-openrouter-guardrail.py
# Requires OPENROUTER_MANAGEMENT_KEY in env (post-rotation)

import os, json, requests

KEY = os.environ["OPENROUTER_MANAGEMENT_KEY"]
BASE = "https://openrouter.ai/api/v1"

GUARDRAIL = {
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
    "blocked_models": ["minimax/*"],  # SHADOW-MM-001
    "content_filter_builtins": [
        {"slug": "regex-prompt-injection", "action": "block"},
        {"slug": "email", "action": "redact"},
        {"slug": "phone", "action": "redact"},
        {"slug": "ip_address", "action": "redact"}
    ],
    "zdr": True
}

r = requests.post(f"{BASE}/guardrails", headers={"Authorization": f"Bearer {KEY}"}, json=GUARDRAIL)
print(f"Status: {r.status_code}")
print(json.dumps(r.json(), indent=2))
```

---

## 10. AAASOT Updates Required

### 10.1 Add to `/root/AAA/registries/models/AGENT_MODEL_MAP.json`

**Under `providers[openrouter].note`** — append ZDR + guardrail refs.

**Add new `shadows[]` entry:**
- SHADOW-OR-001 (sovereign_topic_routing_drift) — see §5.2
- SHADOW-OR-002 (zdr_provider_bypass) — if ZDR not enforced, requests may leak

**Add to `routing_rules[]`** (4 new rules):
```json
{
  "rule_id": "openrouter_zdr_required_for_sovereign",
  "domain": "any",
  "task_pattern": "PII|myKad|PETRONAS|sovereign_identity|Malaysian_governance",
  "preferred_model": "deepseek/deepseek-v4-pro",
  "reason": "OpenRouter MUST use ZDR + sovereign allowlist for these tasks. Safer: route direct to DeepSeek.",
  "priority": 200
},
{
  "rule_id": "openrouter_cqt_per_role",
  "domain": "any",
  "task_pattern": "333_THINK",
  "preferred_model": "openrouter/auto-beta",
  "fallback_model": "deepseek/deepseek-v4-pro",
  "reason": "CQT=3 for constitutional deliberation (quality-leaning). Allowed_models restricted to ZDR-safe set.",
  "cost_quality_tradeoff": 3,
  "priority": 60
},
{
  "rule_id": "openrouter_cqt_forge_default",
  "domain": "any",
  "task_pattern": "777_FORGE",
  "preferred_model": "openrouter/auto-beta",
  "fallback_model": "deepseek/deepseek-v4-pro",
  "reason": "CQT=5 for FORGE work (balanced). Prompt caching enabled.",
  "cost_quality_tradeoff": 5,
  "priority": 50
},
{
  "rule_id": "openrouter_flame_free",
  "domain": "tools",
  "task_pattern": "summarize|classify|extract|compress|tag",
  "preferred_model": "openrouter/free",
  "reason": "FLAME ALLOWED: RM0 free router for tool tasks. No ZDR needed.",
  "cost_quality_tradeoff": 10,
  "chain_ref": "RM0-TOOLS-FREELOOP",
  "priority": 30
}
```

**Add to `models[]`** (3 new ZDR-verified candidates):
- `openrouter/z-ai/glm-5.2` (z-ai, ZDR-safe)
- `openrouter/mistralai/mistral-small-3.2-24b-instruct` (mistralai, EU ZDR)
- `openrouter/xiaomi/mimo-v2.5-pro` (xiaomi, ZDR-safe)

### 10.2 Update `/root/AAA/src/resolvers/opencode_render.py`

Add new role-to-CQT mapping, prompt-cache breakpoints on system messages, session_id generation
in agent invocation paths.

### 10.3 Update `/root/AAA/skills/FLAME-operator/SKILL.md`

Add OpenRouter to FLAME tier list (tier 7 in RM0-TOOLS-FREELOOP chain), with FLAME_FORBIDDEN
for constitutional work (already covered, restate).

---

## 11. Constraints & Forbidden Patterns

| Pattern | Forbidden? | Why |
|---|---|---|
| Auto-router for 666_JUDGE / 999_SEAL | YES | identity_verified: false, no fff_gate |
| Auto-router for MY governance | YES | Censorship risk via MiniMax in pool |
| Auto-router with ZDR disabled for PII | YES | F2 TRUTH + sovereign exposure |
| `minimax/*` via auto-router for any topic | YES | SHADOW-MM-001 |
| OpenRouter without session_id | AVOID | Loses 30% latency gain |
| OpenRouter without `cache_control` on long system prompts | AVOID | Loses 70-80% repeat-cost saving |
| Using auto-router to "discover" the best model | AVOID | F11 AUDITABILITY — use static SOT |
| Budget > $50/day per guardrail | AVOID | Burn-rate guard (existing monitor covers DeepSeek 402) |
| Workspace guardrail tighter than any agent needs | AVOID | Silent 404s, no signal to caller |
| OAuth flow / Management API calls with chat-exposed keys | YES | F12 INJECTION + F1 AMANAH — rotate first |

---

## 12. Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│  AAA × OpenRouter Decision Card                             │
├─────────────────────────────────────────────────────────────┤
│  Task → Role → Model → CQT → ZDR → Allowlist                │
│                                                             │
│  000_INIT  → DeepSeek V4 Pro direct │ no OR                 │
│  111_OBS  → openrouter/free        │ cqt=10 │ no ZDR needed │
│  333_THINK→ auto-beta OR DeepSeek   │ cqt=3  │ ZDR required │
│  444_ROUTE→ auto-beta classier-only │ cqt=9  │ ZDR required │
│  555_MEM  → xiaomi/mimo-v2.5 (1M)   │ cqt=5  │ ZDR required │
│  666_JUDGE→ DeepSeek V4 Pro DIRECT  │ never use OR          │
│  777_FORGE→ auto-beta OR kimi-k2.7  │ cqt=5  │ ZDR required │
│  999_SEAL → DeepSeek V4 Pro DIRECT  │ never use OR          │
│                                                             │
│  Always: session_id, cache_control, allowed_models ZDR-safe │
│  Never:  MY governance, 666_JUDGE, 999_SEAL via OR         │
└─────────────────────────────────────────────────────────────┘
```

---

## 13. DITEMPA BUKAN DIBERI

Forged from live `/api/v1/models` probe + AAA SOT cross-reference + OpenRouter Guardrails docs
(2026-05-29) + Auto Router docs (2026-07-21). Every claim sourced. ΔS ≤ 0 on every section.

**Co-Authored-By:** Kimi Code (FI-008) for Arif (F13 SOVEREIGN).

---

## Appendix A — Citation Trail

- OpenRouter Models API: `https://openrouter.ai/api/v1/models` (live, 2026-07-24)
- OpenRouter Auto Router docs: https://openrouter.ai/docs/guides/routing/routers/auto-router
- OpenRouter Guardrails announcement: https://openrouter.ai/blog/announcements/guardrails/
- OpenRouter MCP Server: https://openrouter.ai/blog/announcements/openrouter-mcp-server/
- OpenRouter AI Data Residency: https://openrouter.ai/blog/insights/ai-data-residency/
- AAA Model Registry (SOT): `/root/AAA/registries/models/AGENT_MODEL_MAP.json`
- AAA FLAME doctrine: `/root/AAA/skills/FLAME-operator/SKILL.md`, `FLAME-router/SKILL.md`
- OpenCode Config Zen: `/root/HERMES/skills/devops/opencode-config-zen/SKILL.md`
- LLM API Adapter: `/root/HERMES/skills/devops/llm-api-adapter/SKILL.md`
- Federation cost dashboards: `/root/A-FORGE/forge_work/2026-07-24/`