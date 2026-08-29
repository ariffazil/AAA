# Gemini API Integration — Agent Configuration Reference

> **Forged:** 2026-08-10 by 333-AGI Δ MIND under F13 directive
> **Canonical:** `/root/AAA/governance/GEMINI_AGENT_INTEGRATION.md`
> **Heritage:** Google Gemini API docs · nousresearch/hermes-agent · opencode-ai/opencode · openclaw/openclaw · a2aproject/A2A
> **Binding:** All AAA agents — Hermes, OpenCode, OpenClaw, A2A gateway

---

## 1. TWO ACCESS VECTORS

### A. OpenAI Compatibility Gateway (Chat + Tools)

```
Base URL:  https://generativelanguage.googleapis.com/v1beta/openai/
Auth:      Authorization: Bearer $GEMINI_API_KEY
Schema:    OpenAI /v1/chat/completions compatible
Use:       Hermes, OpenCode, any agent using OpenAI-style client
```

### B. Native Interactions API (Image, Video, TTS, Edit)

```
Base URL:  https://generativelanguage.googleapis.com/v1beta/interactions
Auth:      x-goog-api-key: $GEMINI_API_KEY
Schema:    Gemini native (not OpenAI compatible)
Use:       Image gen (Nano Banana), Video gen (Omni Flash/Veo), TTS
```

---

## 2. AGENT-SPECIFIC CONFIGURATION

### 2.1 Hermes Agent

```bash
# Environment
export OPENAI_API_KEY="$GEMINI_API_KEY"
export OPENAI_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
export DEFAULT_MODEL="gemini-3.6-flash"

# Thinking config (injected via extra_body)
# extra_body:
#   google:
#     thinking_config:
#       thinking_level: "high"
#       include_thoughts: true
```

**⚠️ OPENAI_BASE_URL CONFLICT:**
Current value points to Qwen Token Plan. Cannot have two `OPENAI_BASE_URL` values.
**Resolution:** Gemini is a SEPARATE provider in Hermes config.yaml, NOT a replacement for OPENAI_BASE_URL:

```yaml
# /root/.hermes/config.yaml
providers:
  gemini-openai:
    api: https://generativelanguage.googleapis.com/v1beta/openai
    key_env: GEMINI_API_KEY
    capabilities: [chat, function_calling, reasoning, vision]
    transport: openai_chat
    models:
      - id: gemini-3.6-flash
        name: Gemini 3.6 Flash — fast reasoning
      - id: gemini-3.1-pro
        name: Gemini 3.1 Pro — deep reasoning
      - id: gemini-3.5-flash-lite
        name: Gemini 3.5 Flash Lite — high throughput
    extra_body:
      google:
        thinking_config:
          thinking_level: high
          include_thoughts: true
    note: DO NOT use OPENAI_BASE_URL. Register as named provider.
```

### 2.2 OpenCode

```json
// ~/.opencode/config.json or ~/.config/opencode/config.json
{
  "providers": {
    "google_gemini": {
      "type": "openai_compatible",
      "baseUrl": "https://generativelanguage.googleapis.com/v1beta/openai/",
      "apiKey": "${GEMINI_API_KEY}",
      "models": {
        "coder": "gemini-3.1-pro",
        "fast_runner": "gemini-3.6-flash",
        "lite": "gemini-3.5-flash-lite"
      }
    }
  }
}
```

### 2.3 OpenClaw

```yaml
# openclaw_config.yaml
providers:
  gemini_gateway:
    api_key_env: GEMINI_API_KEY
    endpoint: "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
    default_headers:
      Content-Type: "application/json"
    parameters:
      extra_body:
        google:
          thinking_config:
            thinking_level: "high"
            include_thoughts: true
```

### 2.4 A2A Gateway (AAA :3001)

```
Header propagation on all A2A handoffs:
  arif_trace_id:      <uuid>  — root trace
  arif_span_id:       <uuid>  — this operation
  arif_parent_span_id: <uuid>  — caller operation

Response format for deterministic deserialization:
  response_format: {"type": "json_object"}
```

---

## 3. MODEL SELECTION MATRIX

| Task | Model | Why |
|------|-------|-----|
| Complex reasoning | `gemini-3.1-pro` | Deep thinking, 1M context |
| Fast coding | `gemini-3.6-flash` | Speed + quality balance |
| High throughput | `gemini-3.5-flash-lite` | Budget, parallel sub-agents |
| Image generation | `gemini-3.1-flash-image` | Nano Banana 2 — 4K, 14 ref images |
| Premium image | `gemini-3-pro-image` | Nano Banana Pro — complex scenes |
| Budget image | `gemini-3.1-flash-lite-image` | Nano Banana 2 Lite — speed |
| Video generation | `gemini-omni-flash-preview` | Omni Flash — sync, editable |
| Premium video | `veo-3.1-generate-preview` | Veo 3.1 — 4K, async |
| TTS (single) | `gemini-3.1-flash-tts-preview` | 30 voices, Malay supported |
| TTS (multi) | `gemini-3.1-flash-tts-preview` | 2-speaker podcast style |

---

## 4. ADVANCED FEATURES

| Feature | API Parameter | Use |
|---------|--------------|-----|
| **Thinking mode** | `thinking_config.thinking_level: "high"` | Extended reasoning for complex tasks |
| **Thought summary** | `include_thoughts: true` | See reasoning chain before final answer |
| **Web search** | `tools: [{"googleSearch": {}}]` | Real-time grounded search |
| **Image search** | `tools: [{"googleSearch": {"search_types": ["image_search"]}}]` | Web images as visual context |
| **Code execution** | `tools: [{"codeExecution": {}}]` | Sandboxed Python execution |
| **Context caching** | Context Caching API | Reusable codebase for multi-turn |
| **URI delivery** | `response_format: {delivery: "uri"}` | Large files (>4MB) |

---

## 5. PROVIDER ROUTING STRATEGY

```
                    ┌──────────────────────────┐
                    │       FED :7074           │
                    │   Capability Router       │
                    └──────────┬───────────────┘
                               │
          ┌────────────────────┼────────────────────┐
          ▼                    ▼                    ▼
   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
   │  Qwen Pool   │    │  Gemini Pool │    │  MiniMax Pool│
   │  (text)      │    │  (all modal) │    │  (text+video)│
   └──────────────┘    └──────────────┘    └──────────────┘
        │                     │                    │
   deepseek-v4-pro     gemini-3.6-flash      MiniMax-M3
   qwen3.8-max         gemini-3.1-pro        Hailuo-02 (video)
   qwen-vl-max         Nano Banana (image)   T2V-01 (video)
   wan2.7 (image)      Omni Flash (video)
                        Veo 3.1 (video)
```

---

## 6. INTEGRATION GAPS & PRIORITY

| # | Gap | Priority | Action |
|---|-----|----------|--------|
| P0 | Hermes OPENAI_BASE_URL conflict | HIGH | Register Gemini as named provider in config.yaml, not via env |
| P0 | Gemini provider entry in Hermes config | HIGH | Add `gemini-openai:` provider block |
| P1 | OpenCode google_gemini provider | MEDIUM | Create provider config entry |
| P1 | FED routing for Gemini models | MEDIUM | Add Gemini models to FED route table |
| P2 | OpenClaw YAML routing | LOW | Configure openclaw_config.yaml |
| P2 | A2A trace propagation | LOW | Inject arif_trace_id in A2A headers |
| P3 | Context caching setup | LOW | Register repos for 1M context reuse |

---

## 7. CONSTITUTIONAL RULES

- **F1 AMANAH**: All Gemini API calls are REVERSIBLE (generation, not destruction). AUTO-DO.
- **F2 TRUTH**: Epistemic labels required on all Gemini outputs. Image/video = DER (derived from model).
- **F9 ANTI-HANTU**: Gemini is not conscious. Generated content carries SynthID watermark.
- **F11 AUDIT**: Every Gemini API call auto-ingested to arifFlow via sidecar.
- **F13 SOVEREIGN**: Arif's GEMINI_API_KEY. His credits. His veto on paid tiers.

---

## 8. SOT

| What | Where |
|------|-------|
| Gemini API docs | https://ai.google.dev/gemini-api/docs |
| Provider registry | `/root/AAA/registries/models/UNIFIED_PROVIDER_REGISTRY.yaml` |
| Agent model map | `/root/AAA/registries/models/AGENT_MODEL_MAP.json` |
| Hermes config | `/root/.hermes/config.yaml` |
| FED routing | `http://127.0.0.1:7074/health` |

---

*DITEMPA BUKAN DIBERI — integration is forged, not given.* ⚒️
