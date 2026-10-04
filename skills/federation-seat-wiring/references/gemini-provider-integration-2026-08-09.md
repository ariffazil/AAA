# Gemini Provider Integration — arifOS Federation

> **Forge:** 2026-08-09 via deep research on Google AI Studio Gemini API integration.
> **SOT:** Current litellm-config.yaml entries + web-extracted docs (ai.google.dev).
> **Related:** `fed-cognitive-allocator` / WIRING / `provider-quota-diagnostics`

## Why This Matters

The federation currently uses `GEMINI_API_KEY` through LiteLLM with the `openai/` prefix route for agi-333/opencode/codex (gemini-3.6-flash), fed/image-gen (gemini-3-flash-preview), and fed/audio. But there are two distinct integration paths with different trade-offs, and Google is actively changing their free tier.

## Path A: `openai/` prefix + Google's OpenAI-compatible proxy *(current, stable)*

```yaml
model: openai/gemini-3.6-flash
api_base: https://generativelanguage.googleapis.com/v1beta/openai
api_key: os.environ/GEMINI_API_KEY
order: 1
```

How it works: Google maintains a dedicated `/v1beta/openai` endpoint that translates standard OpenAI chat completion payloads to native Gemini format internally.

| Pros | Cons |
|---|---|
| Stable — avoids LiteLLM vertex-ai confusion bug | No access to Gemini-native features (thinking, multimodal tools, Computer Use, Remote MCP) |
| Standard OpenAI payload = works with litellm router | Translation layer may lag behind native API |
| Cost tracking works in LiteLLM | Limited image generation capability |

### Already wired in litellm-config.yaml (2026-08-09 OBS)

| Alias | Model | api_base | order | Purpose |
|---|---|---|---|---|
| agi-333 | `openai/gemini-3.6-flash` | .../v1beta/openai | 1 | Primary LLM |
| opencode | `openai/gemini-3.6-flash` | .../v1beta/openai | 1 | Primary LLM |
| codex | `openai/gemini-3.6-flash` | .../v1beta/openai | 1 | Primary LLM |
| fed/image-gen | `openai/gemini-3-flash-preview` | .../v1beta/openai | 0 | Image gen primary |
| hermes-asi | — | — | — | NOT wired |

**Gap:** `hermes-asi` has no Gemini fallback. Currently only MiMo V2.5 -> DeepSeek V4 Flash -> MiniMax-M3 chain.

## Path B: `gemini/` prefix — native LiteLLM Gemini provider

```yaml
model: gemini/gemini-3.6-flash
api_key: os.environ/GEMINI_API_KEY
# DO NOT set api_base — let LiteLLM build the correct default endpoint
```

How it works: LiteLLM sends native Gemini payloads to `generativelanguage.googleapis.com/v1beta` (NOT the `/openai` suffix). Enables thinking, multimodal tools, structured output properly.

| Pros | Cons |
|---|---|
| Full Gemini-native feature access | **Known bug** (litellm#14771): May default to Vertex AI, triggering ADC credential errors |
| Thinking/reasoning properly mapped | `provider: gemini` sometimes ignored by LiteLLM |
| Better cost tracking for Gemini pricing | Requires `litellm_settings: drop_params: True` |

### Critical Bug: litellm#14771 (Sep 2025 — still unresolved in some versions)

When using `gemini/` route with a Google AI Studio key, LiteLLM can fall back to Vertex AI endpoint and expect Application Default Credentials (ADC), not an API key. Results in `DefaultCredentialsError`. The `openai/` route completely sidesteps this.

**Recommendation:** Keep Path A (`openai/`) as primary. Use Path B (`gemini/`) only if you explicitly need Gemini-native features AND you pin the `provider: gemini` parameter. Always test with a live probe before trusting.

### If you MUST use Path B, this shape works:

```yaml
- model_name: my-gemini-alias
  litellm_params:
    model: gemini/gemini-3.6-flash
    api_key: os.environ/GEMINI_API_KEY
    provider: gemini   # CRITICAL — prevents vertex-ai fallback
    order: 1
  litellm_settings:
    drop_params: True   # Suppress unsupported params for Gemini
  model_info:
    max_input_tokens: 1048576
    max_output_tokens: 131072
    mode: chat
    supports_vision: true
    supports_function_calling: true
```

**Warning:** Setting `api_base` when using `gemini/` route causes wrong URLs (missing `/v1beta` prefix -> 404 Not Found). Do NOT set `api_base` — let LiteLLM build it.

## Free Tier Reality Check (Feb 2026+)

Google gutted the free tier. What was once generous now has "Limit is 0" for most models on fresh projects.

| Model | Free Tier Status (Aug 2026) | Notes |
|---|---|---|
| gemini-2.5-flash | Available | Most reliable free option |
| gemini-2.5-flash-lite | Available | Fastest, cheapest |
| gemini-2.5-pro | 5 RPM / 50 RPD free | Too limited for real work |
| gemini-3-flash-preview | Available | Newer but free tier confirmed working |
| gemini-3.1 Pro | Paid only | Most expensive ($12/M tokens output) |
| gemini-3.6 Flash | Mixed reports | Some report free tier gone |

**Quota is project-level, not key-level.** Multiple API keys in the same Google Cloud project share one quota pool.

**Recommendation:** For production/federation use, enable billing on your Google Cloud project. The $0.05/$0.15 per million tokens for flash models makes budgeting predictable.

## Current Model Landscape (August 2026)

| Model | Context | Best For | Input/M | Output/M |
|---|---|---|---|---|
| Gemini 3.1 Pro | 2M | Flagship reasoning | $3.00 | $12.00 |
| Gemini 3.6 Flash | 1M | Balanced coding, agents | $1.50 | $7.50 |
| Gemini 3.5 Flash | 1M | Proven, cheaper | ~$1.00 | ~$4.00 |
| Gemini 3.5 Flash-Lite | 1M | High-volume, low-cost | ~$0.40 | ~$0.20 |
| Gemini 2.5 Pro | 1M | Strong reasoning (older) | $1.25 | $10.00 |
| Gemini 2.5 Flash | 1M | Budget reasoning | $0.175 | $0.70 |

Cost comparison vs our stack: MiMo V2.5 ~$0.14/$0.28 (cheapest), Gemini 2.5 Flash ~$0.175/$0.70 (close), Gemini 3.6 Flash $1.50/$7.50 (10x MiMo). FED-primary doctrine holds: Gemini in fallback, not primary.

## Native Capabilities Only Via Interactions API (Not Through LiteLLM Proxy)

These require direct `google-genai` SDK use (`from google import genai`). NOT accessible through `openai/` route:

| Feature | Access |
|---|---|
| Function calling (native) | `client.interactions.create(model=..., tools=[...])` |
| Remote MCP | Built-in: `tools=[{"name": "...", "url": "..."}]` |
| Computer Use | gemini-3-pro-preview, gemini-3-flash-preview |
| Deep Research | `agent="deep-research-pro-preview-12-2025"` + `background=True` |
| Structured output | Pydantic via Instructor integration |

For native Gemini features: create a dedicated Python script using the `google-genai` SDK that bypasses LiteLLM. `uv pip install --system google-genai` for install.

## Pitfalls (Live-Evidence Verified)

- **P1: `api_base` with `gemini/` route breaks URL construction.** Symptom: 404 Not Found. Fix: remove `api_base` or use `openai/` prefix.
- **P2: LiteLLM bug #14771 — vertex-ai fallback.** Symptom: DefaultCredentialsError with AI Studio key. Workaround: use `openai/` prefix route.
- **P3: Free tier quota is project-level.** Multiple keys = same quota bucket. Fresh projects frequently get "Limit is 0".
- **P4: Google deprecating free models rapidly.** Since Feb 2026, many models lost free access. Verify live before counting on any free tier model.
- **P5: Gemini does NOT support Union types in structured output.** Use `Literal` types or `Optional[X]` instead of `Union[A, B]`.
- **P6: Reasoning models consume output tokens in reasoning.** With `max_tokens` <= 30, entire budget goes to reasoning, `content` stays empty. Test with `max_tokens: 256+`. Same issue exists with MiMo V2.5 on our system.
- **P7: Don't auto-codify Gemini into hermes-asi primary.** Per FED-primary doctrine, reserve Gemini for vision tasks, code gen tasks, specialized reasoning that exceeds MiMo's capability. MiMo is ~10x cheaper for daily conversation.
- **P8: LiteLLM `drop_params: True` is REQUIRED for Gemini native route.** Without it, unsupported parameters (e.g. `frequency_penalty`) cause 400 errors. The `openai/` route handles this silently; the native route does not.
