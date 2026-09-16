---
name: tokenrouter-guide
description: "How Hermes uses TokenRouter — model selection, auto-routing, cost strategy, FREE tier, sovereign anchor"
---

# 🪙 TokenRouter Guide for Hermes

> ## ⛔ STALE — DO NOT ROUTE FROM THIS PAGE (verified 2026-09-15)
> Balance/model figures below are unverified or expired: **`z-ai/glm-5.2` "FREE until July 25" is over**
> (z.ai now returns `429 code 1310` on the coding endpoint and `429 code 1113 insufficient balance` on
> paas); **"95 text models"** is a marketing figure — the live FED config carries 114 entries,
> 33 lane names, **4 live provider families of 19 configured lanes**.
> Hermes' real routing is **`/root/.hermes/config.yaml`** → `model.default: i-arif`,
> `provider: custom:fed-federation`, `base_url http://127.0.0.1:4012/v1` (local KVM8 litellm).
> Its `fallback_providers` carries **two dead z.ai rungs** (`glm-5.3`, `glm-5.3-flash`).
> Model truth lives in `/root/A-FORGE/litellm-config.yaml` + `/root/.config/federation-models.json`;
> re-verify with a direct provider probe before quoting any model or balance from this page.
> Retained for its **routing-philosophy** sections only.

> **Your config is already wired.** TokenRouter is provider `tokenrouter` in `/root/HERMES/config.yaml`.
> **SOT:** 2026-07-20 | **Balance:** $59.96 + $25.61 vouchers | **GLM 5.2:** FREE until July 25

---

## ⚠️ 2026-08-01 UPDATE — Primary moved off TokenRouter

The 5-tier hierarchy below is HISTORICAL. As of 2026-08-01 Hermes
**primary = `qwen-token-plan` / `qwen3.7-plus`** (Qwen Token Plan TEAM
seat — flat monthly, RM0 marginal, 21 models incl. vision + image +
TTS). TokenRouter remains a valid fallback/backup gateway, not the
primary. Canonical current routing: `/root/.hermes/model-picker.yaml`
+ `fallback_providers` in `/root/.hermes/config.yaml`.

---

## ⛔ 2026-09-15 LIVE REALITY — QWEN TOKEN PLAN IS QUOTA-EXHAUSTED, NOT RM0

> Probe-verified 2026-09-15 01:42–02:00 +08 from KVM8. **A flat monthly seat is not
> the same thing as available quota.** "RM0 marginal" describes the *price model*;
> it says nothing about whether the window has anything left in it.

| Seat | Live answer | Body |
|---|---|---|
| `QWEN_TEAM_OWNER_API_KEY` | **429** | `Your token-plan quota has been exhausted.` |
| `QWEN_INDIVIDUAL_API_KEY` | **429 ↔ 200** (flaps) | `Your token-plan 1-week quota has been exhausted. The quota will reset at 09-18 04:10:00 UTC.` — the **same key/model returned `200 qwen3.8-max` ten minutes later**, then 3 of 4 follow-up calls timed out at 30 s |
| `QWEN_HERMES_API_KEY` | **429** | `Your token-plan quota has been exhausted.` |
| `QWEN_ARIFOS_API_KEY` | **429** | `Your token-plan quota has been exhausted.` |

**Consequence, measured:** Hermes's live primary is `model.default: i-arif`
(`provider: custom:fed-federation`, base `http://127.0.0.1:4012/v1`). Seven consecutive
cache-defeated probes of lane `i-arif` returned **`"model": "deepseek-flash"`** — the lane
fell out of its whole body (all rungs ride the four seats above) and landed on its first
*fallback*. **Hermes is running on its emergency tail and reporting nothing.**

**Other lanes, same sweep:** `glm-5.3` → `mimo-v2.5` (20 s); `glm-5.2` and `kimi-k3` →
**timeout at 40 s**; `gemini-3.6-flash` → 429 `prepayment credits are depleted`;
`asi-555`/`qwen3.8-max` → served. Live upstreams that answered 200: **DeepSeek, MiniMax,
Xiaomi MiMo Token Plan (SGP), SEA-LION** — four, out of 114 deployments.

**Z.ai is quota-dead too**, on both paths:
```
/api/coding/paas/v4 -> 429 {"code":"1310","message":"Weekly/Monthly Limit Exhausted.
                                Your limit will reset at 2026-09-15 16:13:25"}
/api/paas/v4        -> 429 {"code":"1113","message":"Insufficient balance or no
                                resource package. Please recharge."}
```

**Rule this teaches:** before calling a seat "primary", probe a **1-token completion**
against that seat's own base URL and read the BODY — `/v1/models` 200 proves only that the
key authenticates. And **sample ≥3 times**: `QWEN_INDIVIDUAL` moved 429→200→timeout inside
10 minutes, so any single sample is worthless in both directions.
Runnable probes: `/root/forge_work/harden-20260915/model/probe-providers.sh` and
`probe-model-layer.sh`.

**Endpoint correction:** KVM8's LiteLLM is **`:4013`** (host-net container
`litellm-federation`), reached by Hermes via the `:4012` zen passthrough. `:4011` — cited
throughout older notes — does not exist on KVM8.

**Fallback-chain principle (proven 2026-08-01):** a fallback chain where
every entry rides the SAME provider → SAME key is theatre. One dead key
(placeholder `PASTE_*`, quota-drained seat, 401) kills the whole chain.
Real chains diversify providers AND keys: qwen-token-plan → mulerouter
→ ollama local. When auditing a "fallback chain", verify each hop has an
independent credential, not just a different model name.

Seat wiring detail: `references/qwen-token-plan-seat-wiring.md`.

---

## ⚡ 5-DAY PULUN WINDOW (July 20–25, 2026)

**GLM 5.2 FREE tier is active NOW. Expires July 25. 120 hours remaining.**

### Containment Paradox (F2)

US Entity List + chip restrictions forced Zhipu AI onto Huawei Ascend silicon → architectural independence from Nvidia → fully open MIT weights with no regional restrictions → uncontrollable open-source release → now operating inside the sovereign federation it was meant to exclude. **The containment strategy inverted itself.** The geopolitical wall created the asset.

### Tactical: Pulun Habis

| Window | Strategy |
|---|---|
| **Now → Jul 25** | `z-ai/glm-5.2` as PRIMARY for background/volume tasks. Exploit 1M context, zero cost. |
| **Jul 25 → onward** | Falls back to `z-ai/glm-5.2` (paid, $1.20/$4.10 MTok) or `MiniMax-M3` |

**Context saturation:** Push entire repos, sync logs, dense documentation into single 1M-token prompts.
**Token discipline:** GLM 5.2 generates long execution traces. Structure prompts for CONCISE output to maximize throughput before route closure.

Cron `c4d4b95ed026` fires 8am July 25 — detects 402/403, swaps chain back to paid mode.

---

## 5-Tier Sovereign Routing Hierarchy

The routing DNA is **deliberate**, not a bug. Each tier exists for a distinct reason. Canonical source: `/root/AGENTS.md` §6.6. Do not collapse tiers without understanding the WHY.

| Tier | Scope | Model | Why this tier |
|---|---|---|---|
| **Hermes PRIMARY** | Hermes | `deepseek/deepseek-v4-pro` | Maximum logic capacity + strict JSON schema adherence. Schema drift here corrupts downstream judges. |
| **Hermes FALLBACK** | Hermes | `MiniMax-M3` | Multimodal continuity. Hermes ingests vision/audio — fallback must preserve multimodal capacity, not just be a cheaper text clone. |
| **arifOS kernel** | arifOS | `google/gemini-3.5-flash` | Set via `TOKENROUTER_MODEL` in `/root/.secrets/tokenrouter.env`. Overrides the `MiniMax-M3` default. |
| **Tertiary (all agents)** | All | `z-ai/glm-5.2` (FREE→paid) | Zero-cost volume node until Jul 25. After expiry: $1.20/$4.10 MTok. Absorbs bulk/low-stakes traffic. |
| **Sovereign anchor (all)** | All | `qwen2.5-coder:3b` (Ollama, local) | Blind CLI survival. No TokenRouter, no WAN, no external API. Keeps the federation governable during total egress failure. |

**Fallback order:** PRIMARY → FALLBACK → Tertiary → Sovereign anchor. A drop to a lower tier is a capacity decision, never an authority change — F1–F13 gates apply identically regardless of which model generated the text.

> **Reference:** `references/glm-5.2-deep-dive.md` — full GLM 5.2 technical specs, benchmarks, architecture (IndexShare), lineage, pricing, scar shadow paradox, and geopolitical context.

---

## How to call TokenRouter directly (when you want a specific model)

TokenRouter is OpenAI-compatible. From any code or curl:

```bash
source /root/.secrets/vault.env

curl -s https://api.tokenrouter.com/v1/chat/completions \
  -H "Authorization: Bearer $TOKENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek/deepseek-v4-pro",
    "messages": [{"role": "user", "content": "Your task here"}],
    "max_tokens": 1000
  }'
```

---

## Model Selection — which model for which task

| Task | Best Model | Why | Cost |
|------|-----------|-----|------|
| **Geology dossiers** | `deepseek/deepseek-v4-pro` | High reasoning, 1M context | $$ |
| **Prospect evaluation** | `deepseek/deepseek-v4-pro` | Needs deep domain knowledge | $$ |
| **Code review/PR** | `MiniMax-M3` or `deepseek/deepseek-v4-flash` | Fast, good code understanding | $ |
| **Daily briefing** | `z-ai/glm-5.2` | **FREE until July 25** | FREE |
| **Memory compression** | `z-ai/glm-5.2` | Simple summarization, cheap | FREE |
| **Health summary** | `z-ai/glm-5.2` | 4-sentence output, no need for heavy model | FREE |
| **Quick Q&A** | `deepseek/deepseek-v4-flash` | Fastest, cheapest paid option | $ |
| **Multimodal (images)** | `MiniMax-M3` or `xiaomi/mimo-v2.5` | Vision-capable | $$ |
| **Sovereign decisions** | `deepseek/deepseek-v4-pro` | Never cheap out on governance | $$ |

---

## Auto-Routing (let TokenRouter pick)

Instead of specifying a model, use auto-routing:

```json
{"model": "auto:balance"}   // Best overall (default)
{"model": "auto:cost"}      // Cheapest that can handle the task
{"model": "auto:quality"}   // Best available model
{"model": "auto:latency"}   // Fastest response
```

For background tasks (memory bridge, health checks): `auto:cost`
For Arif-facing responses: `auto:quality` or explicit `deepseek/deepseek-v4-pro`

---

## 95 Text Models Available

Key ones to know:
- `deepseek/deepseek-v4-pro` — your primary (best reasoning)
- `deepseek/deepseek-v4-flash` — fast/cheap DeepSeek
- `MiniMax-M3` — multimodal, 1M context
- `z-ai/glm-5.2` — FREE tier ⭐
- `xiaomi/mimo-v2.5-pro` — strong coding specialist
- `openai/gpt-5.6-sol` — Codex's primary, available as backup
- `moonshotai/kimi-k3` — latest Kimi
- `anthropic/claude-opus-4.8` — Claude family (premium)
- `google/gemini-3.5-flash` — Gemini for Antigravity-style tasks

---

## Cost Strategy

```
FREE (GLM 5.2)     → background tasks, memory, health checks
CHEAP (v4-flash)    → quick Q&A, code review, simple tasks
PREMIUM (v4-pro)    → geology, sovereign decisions, Arif-facing output
```

Your config already does this via the 5-tier routing hierarchy. TokenRouter auto-bills to one account — no per-provider tracking needed.
