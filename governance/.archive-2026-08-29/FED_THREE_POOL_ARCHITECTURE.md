# FED THREE-POOL ARCHITECTURE — MiniMax · Qwen · Gemini

> **Forged:** 2026-08-10 by 333-AGI under F13 directive
> **Canonical:** `/root/AAA/governance/FED_THREE_POOL_ARCHITECTURE.md`
> **Heritage:** FED FLAME FRAME v2 · LiteLLM proxy · Unified Provider Registry
> **Binding:** FED Router :7074 · LiteLLM :4000 · All AAA agents

---

## THE THREE POOLS

```
                    ┌──────────────────────────────────────┐
                    │        FED ROUTER (:7074)            │
                    │    Capability Signature Routing       │
                    └──────────────────┬───────────────────┘
                                       │
       ┌───────────────────────────────┼───────────────────────────────┐
       ▼                               ▼                               ▼
┌──────────────────┐        ┌──────────────────┐        ┌──────────────────┐
│   QWEN POOL      │        │  GEMINI POOL     │        │  MINIMAX POOL    │
│   Deep Reasoning │        │  Multimodal      │        │  High-Throughput │
├──────────────────┤        ├──────────────────┤        ├──────────────────┤
│ Credentials      │        │ Credentials      │        │ Credentials      │
│  sk-sp (Token)   │        │  GEMINI_API_KEY  │        │  sk-cp (Subscr)  │
│  sk-ws (PAYG)    │        │                  │        │                  │
├──────────────────┤        ├──────────────────┤        ├──────────────────┤
│ Capacity         │        │ Capacity         │        │ Capacity         │
│  TokenPlan:22mdl │        │  PAYG            │        │  5.1B tok/month  │
│  PAYG: 156mdl    │        │  Free tier avail │        │  4-5 concurrent  │
├──────────────────┤        ├──────────────────┤        ├──────────────────┤
│ Primary Role     │        │ Primary Role     │        │ Primary Role     │
│  Deep reasoning  │        │  Image gen/edit  │        │  Background tasks│
│  Hard coding     │        │  Video gen       │        │  Repo scanning   │
│  Math/proof      │        │  TTS (30 voices) │        │  Long-context    │
│  Image gen(wan)  │        │  Search ground   │        │  High-frequency  │
│  Vision (vl-max) │        │  1M+ context     │        │  Agent fleets    │
│                  │        │  Code execution  │        │  Speech/Music    │
├──────────────────┤        ├──────────────────┤        ├──────────────────┤
│ Key Models       │        │ Key Models       │        │ Key Models       │
│  deepseek-v4-pro │        │  gemini-3.6-flash│        │  MiniMax-M3      │
│  qwen3.8-max     │        │  gemini-3.1-pro  │        │  MiniMax-M2.7    │
│  qwen3.6-flash   │        │  gemini-3.5-lite │        │  Hailuo-02(video)│
│  qwen-vl-max     │        │  NanoBanana(img) │        │  T2V-01 (video)  │
│  wan2.7 (img)    │        │  OmniFlash(video)│        │  I2V-01 (video)  │
│                  │        │  Veo3.1 (4K vid) │        │  Music gen       │
├──────────────────┤        ├──────────────────┤        ├──────────────────┤
│ Cost             │        │ Cost             │        │ Cost             │
│  Credits-based   │        │  PAYG            │        │  $50/mo flat     │
│  Quota windows   │        │  Free tier: 1.5K │        │  Renews Sep 3    │
└──────────────────┘        └──────────────────┘        └──────────────────┘
```

---

## POOL-SPECIFIC ROUTING RULES

### QWEN POOL — Deep Reasoning

```
Route WHEN:
  - Task requires deep multi-step reasoning
  - Complex code generation / refactoring
  - Mathematical proof / formal verification
  - Heavy tool-calling loops (OpenCode)
  - Image generation via wan2.7

DO NOT route WHEN:
  - Task needs >128K context (use Gemini or MiniMax)
  - Audio/video generation needed
  - Real-time search grounding needed

Endpoint: token-plan.ap-southeast-1.maas.aliyuncs.com (Token Plan)
          ws-wlab8klalfojzq7i.ap-southeast-1.maas.aliyuncs.com (PAYG)
          dashscope-intl.aliyuncs.com (DashScope PAYG)
```

### GEMINI POOL — Multimodal & Search

```
Route WHEN:
  - Image generation / editing needed
  - Video generation (T2V, I2V)
  - Text-to-speech (30 voices, Malay supported)
  - Real-time Google Search grounding
  - Context >1M tokens
  - Sandboxed code execution
  - Multi-turn image/video editing

DO NOT route WHEN:
  - All video credits exhausted (3/day on MiniMax)
  - Simple text tasks (use Qwen or MiniMax)

Endpoint: generativelanguage.googleapis.com/v1beta (native)
          generativelanguage.googleapis.com/v1beta/openai (compat gateway)
```

### MINIMAX POOL — High-Throughput Agent Fleet

```
Route WHEN:
  - Background agent tasks (repo scanning, polling, monitoring)
  - High-frequency low-latency calls
  - Long-context document processing (1M ctx)
  - Speech / music generation
  - Video generation (3 clips/day — use sparingly)
  - Need to conserve pay-as-you-go credits

DO NOT route WHEN:
  - Task requires Google Search grounding
  - High-res video needed (use Gemini Veo)
  - Video quota exhausted (3/day)

Endpoint: api.minimax.io/v1 (OpenAI compatible)
          api.minimax.io/anthropic (Anthropic compatible)
Key type: sk-cp (Subscription Key — NOT pay-as-you-go)
```

---

## KEY ISOLATION RULES

| Key Prefix | Pool | Endpoint | Must NOT route to |
|------------|------|----------|-------------------|
| sk-sp- | Qwen Token Plan | token-plan.maas.aliyuncs.com | DashScope Intl |
| sk-ws- | Qwen PAYG | dashscope-intl.aliyuncs.com | Token Plan |
| sk-cp- | MiniMax Subscription | api.minimax.io | Pay-as-you-go endpoints |
| GEMINI_API_KEY | Gemini | generativelanguage.googleapis.com | Any Qwen endpoint |

**Violation consequence:** 401 InvalidApiKey. Keys and endpoints MUST match.

---

## LITELLM CONFIG STATUS

```
LiteLLM :4000 — 16 model_names, 42 routing entries

Model aliases:
  agi-333        → DeepSeek V4 Pro (order:1) → MiMo (disabled:99) → MiniMax M3 → Qwen 3.8
  hermes-asi     → MiMo (disabled:99) → Qwen 3.8 → DeepSeek V4 Flash → MiniMax M3
  asi-555        → Qwen 3.6 Flash → Qwen 3.8 → DeepSeek V4 Flash → MiMo (disabled:99)
  apex-888       → MiniMax M3 → DeepSeek V4 Pro → MiMo (disabled:99)
  opencode       → DeepSeek V4 Pro → Qwen 3.8 → MiMo (disabled:99) → MiniMax M3
  gemini-flash   → Gemini 3.6 Flash (OpenAI gw) → Gemini 2.5 Flash
  gemini-flash-lite → Gemini 3.5 Flash Lite (OpenAI gw)
  gemini-pro     → Gemini 3.1 Pro (OpenAI gw)
  fed/image-gen  → Gemini 3.1 Flash Image → wan2.7-pro → wan2.7
  fed/vision     → Qwen VL Max → MiniMax M3 → MiMo (disabled:99) → Gemini 3.6 Flash
  fed/audio      → MiMo (disabled:99) → MiMo (disabled:99)

Dead entries: 12 MiMo (order:99 — disabled, not removed)
Retries: 3 (fail-closed)
```

---

## AGENT POOL ASSIGNMENT

| Agent | Primary Pool | Fallback |
|-------|-------------|----------|
| 333-AGI | QWEN (deepseek-v4-pro) | MiniMax M3 → Gemini Pro |
| 555-ASI | QWEN (qwen3.6-flash) | Gemini Flash → MiniMax |
| 888-APEX | MINIMAX (M3) | Gemini Pro → QWEN deepseek |
| Hermes | MINIMAX (M3) | QWEN → Gemini Flash |
| OpenCode | QWEN (deepseek-v4-pro) | Gemini Flash → MiniMax M3 |
| OpenClaw | GEMINI (3.6-flash) | MiniMax M3 → QWEN |
| Dispatch | QWEN (3.6-flash) | MiniMax M3 → Gemini Lite |

---

## SOT

| What | Where |
|------|-------|
| LiteLLM config | `/root/A-FORGE/litellm-config.yaml` |
| Hermes providers | `/root/.hermes/config.yaml` |
| Unified registry | `/root/AAA/registries/models/UNIFIED_PROVIDER_REGISTRY.yaml` |
| Agent model map | `/root/AAA/registries/models/AGENT_MODEL_MAP.json` |
| FED health | `http://127.0.0.1:7074/health` |
| LiteLLM models | `http://127.0.0.1:4000/v1/models` |

---

*DITEMPA BUKAN DIBERI — three pools, one FED, zero single points of failure.* ⚒️
