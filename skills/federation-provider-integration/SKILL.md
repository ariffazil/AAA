---
name: federation-provider-integration
description: "Integrate new LLM providers into the arifOS federation: LiteLLM FED seat configuration, security key management, tool-loop avoidance, model landscape, pricing, and provider-specific quirks. Use whenever adding a new provider (Gemini, Anthropic, etc.) or diagnosing provider integration failures."
floor_scope: F1/F2/F7/F13
tags: [provider, litellm, integration, security, gemini, api-key]
---

# Federation Provider Integration

How to add a new LLM provider to the arifOS federation. Covers LiteLLM FED seat configuration, security key management, tool-loop avoidance, provider-specific quirks, and the two integration paths (OpenAI-compat proxy vs native provider route).

## Two Integration Paths

| Path | Prefix | Route | Best For |
|------|--------|-------|----------|
| **A: OpenAI-compat proxy** | `openai/` | Provider's OpenAI-compatible endpoint (e.g. Google's `/v1beta/openai`) | Stability. Avoids LiteLLM native provider bugs |
| **B: Native provider route** | `gemini/`, `anthropic/`, etc. | LiteLLM auto-builds native endpoint | Full native feature access (thinking, multimodal tools, Computer Use, MCP) |

**Recommendation:** Use Path A (openai/) as the primary FED seat for reliability. Add Path B (native) for pass-through or dedicated Python scripts using the provider's SDK.

## LiteLLM Configuration Pattern

```yaml
# Path A: OpenAI-compat proxy (stable)
- model_name: <seat-alias>
  litellm_params:
    model: openai/<model-name>
    api_base: <provider-openai-compat-endpoint>
    api_key: os.environ/<PROVIDER_KEY_NAME>
    order: <priority>
  model_info:
    max_input_tokens: <context-window>
    max_output_tokens: <max-output>
    mode: chat

# Path B: Native provider route
- model_name: <seat-alias>
  litellm_params:
    model: <provider>/<model-name>  # e.g. gemini/gemini-3.6-flash
    api_key: os.environ/<PROVIDER_KEY_NAME>
    order: <priority>
  model_info:
    ...
```

## Known LiteLLM Bugs

**Bug #14771 (Sep 2025, Gemini):** When using `gemini/` native route with a Google AI Studio key, LiteLLM sometimes falls back to Vertex AI endpoint and expects Application Default Credentials (ADC), not an API key. The `openai/` route with Google's OpenAI-compatible endpoint at `generativelanguage.googleapis.com/v1beta/openai` completely sidesteps this.

**Mitigation:** Never set `api_base` when using native `gemini/` route — let LiteLLM build the URL. Add `drop_params: True` in `litellm_settings`.

**PyYAML duplicate blocks:** litellm-config.yaml can have duplicate YAML blocks from earlier edits. Patching via `old_string`/`new_string` can fail silently if matching hits wrong block. Use PyYAML (execute_code) not patch tool.

## Security Architecture

| Requirement | Implementation |
|-------------|----------------|
| Key storage | `/root/.secrets/kunci-mas.env` (mode 600, never expose) |
| Key exposure | Redacted in chat output and logs |
| Key type | Provider-specific (Google AI Studio = API key; Anthropic = API key) |
| Quota model | Per-project, not per-key. Multiple keys in same project share quota |
| NEVER use | `/etc/environment` (mode 644, world-readable) |

## Tool-Loop Avoidance Doctrine

> **Locked-in doctrine (2026-08-09, Arif):** Gemini must NOT be in the hermes-asi / opencode / codex / agi-333 tool loop path.

Reasoning: Gemini thinking models can return empty content when reasoning is parked in thought blocks. Tool loops break when the response content is empty. MiMo and Qwen handle this correctly with `reasoning_content` padding.

**Seats that MUST NOT use Gemini in tool loop path:**
- `hermes-asi` — MiMo primary, Qwen secondary
- `opencode` — Gemini single-turn only (order:1), NOT for tool loops
- `codex` — Gemini single-turn only (order:1), NOT for tool loops
- `agi-333` — Gemini single-turn only (order:1), NOT for tool loops

**Seats where Gemini IS primary:**
- `gemini-flash` — OpenAI-compat or native → single-turn, vision, image
- `gemini-pro` — OpenAI-compat or native → single-turn, vision, image
- `fed/image-gen` — Gemini 3-flash-preview (order:0)
- `fed/vision` — Gemini 3.6 Flash (order:50, secondary multimodal)

## Interactions API Sidecar (future)

For multi-turn tool work with Gemini, build a thin Interactions adapter rather than adding Gemini back to tool-loop seats. Google's own rule: stateful Interactions = you do nothing with signatures; stateless = you must resend every thought block.

## Free Tier Reality Check

Google gutted the free tier (Feb 2026). Many models return `429 with "limit: 0"` on free accounts.

| Model | Free Tier | Paid Pricing | Use Case |
|-------|-----------|-------------|----------|
| Gemini 3.6 Flash | Limited | $1.50/$7.50 per M | Agents, coding, balanced |
| Gemini 3.1 Pro | ❌ Paid only | $3.00/$12.00 per M | Flagship reasoning |
| Gemini 3.5 Flash | ✅ Yes | $1.00/$4.00 per M | Budget balanced |
| Gemini 3.5 Flash-Lite | ✅ Yes | $0.40 per M | High-volume, low-cost |
| Gemini 2.5 Flash | ✅ Yes | $0.075/$0.30 per M | Cheapest reasoning |

## Model Landscape (Aug 2026)

| Model | Context | Speed | Best For |
|-------|---------|-------|----------|
| Gemini 3.1 Pro | 2M tokens | Slow | Flagship reasoning, complex analysis |
| Gemini 3.6 Flash | 1M tokens | Fast | Balanced performance, coding, agents |
| Gemini 3.5 Flash | 1M tokens | Fast | Proven, cheaper than 3.6 Flash |
| Gemini 3.5 Flash-Lite | 1M tokens | Fastest | High-volume, low-cost tasks |
| Gemini 2.5 Pro | 1M tokens | Slow | Strong reasoning, older but reliable |
| Gemini 2.5 Flash | 1M tokens | Fast | Budget reasoning |

## The Interactions API

Google's newer primary interface for Gemini. Key capabilities NOT available through OpenAI-compat proxy:

| Feature | Via Interactions API | Via OpenAI proxy |
|---------|---------------------|------------------|
| Function calling | ✅ Native | ⚠️ Translated |
| Remote MCP | ✅ Built-in | ❌ Not supported |
| Computer Use | ✅ gemini-3-pro-preview | ❌ Not supported |
| Deep Research agent | ✅ `background=True` | ❌ Not supported |
| Thinking modes | ✅ Full control | ⚠️ `reasoning_effort` only |
| Image generation | ✅ Native multimodal | ⚠️ Limited |
| Video input (Veo 3.1) | ✅ Via pass-through | ❌ Not supported |

## Antigravity Managed Agent

Antigravity is Google's hosted coding agent runtime. Deploy managed agents with `client.agents.create()` via the Interactions API.

**Key parameters:**
- `id`: agent identifier (must be unique, no `google-`/`gemini-` prefix)
- `base_agent`: `antigravity-preview-05-2026`
- `agent_config`: `{"type": "antigravity", "model": "gemini-3.6-flash"}`
- `system_instruction`: your agent's behavior rules
- `base_environment`: `{"type": "remote", "sources": [...]}` — inline AGENTS.md + SKILL.md

**File handling:**
- Text files (`.md`, `.py`, `.json`, `.yaml`): inlined as UTF-8
- Binary files (`.pdf`, `.png`, `.jpg`): base64-encoded
- Files > 1 MB: skipped
- Only `AGENTS.md`, `workspace/`, and `skills/` are inlined

**Known limitation:** Antigravity sandbox requires `"environment": "remote"` in every interaction. Missing this field → 400 error.

## Pitfalls

- **Gemini shared credit pool (verified 2026-08-10):** ALL Gemini generation (image gen, Omni Flash video, Veo 3.1) shares ONE prepayment credit pool. One heavy session can exhaust all routes simultaneously. Top up at ai.google.dev before critical video/image tasks.
- **Gemini OpenAI gateway confirmed (verified 2026-08-10):** `POST https://generativelanguage.googleapis.com/v1beta/openai/chat/completions` with `Authorization: Bearer $GEMINI_API_KEY` works. Model `gemini-3.6-flash` responds correctly. This is the recommended Path A for FED integration.
- **Kimi endpoint is `api.kimi.com/coding/v1`**, NOT `api.moonshot.ai/v1` (which fails). See `references/provider-endpoints-2026-08-10.md` for full corrected endpoint map.
- **OpenCode Go is DEAD** (401 Insufficient balance). Do not register as a live pool.
- **Qwen Token Plan seats EXHAUSTED** until Sept 1, 2026. All requests return 429. Use DeepSeek Direct + Gemini as primary until credits reset.
- **Free tier per-project quota:** Multiple API keys in the same project share the same quota. Creating 3 keys doesn't give you 3x quota.
- **Gemini models don't support Union types** in structured output — use `Literal` types or `Optional` instead.
- **`drop_params: True`** needed in litellm_settings to avoid unsupported parameter errors from non-standard providers.
- **Context windows differ across providers:** Same model can have different limits via different providers (e.g. MiMo V2.5 = 1M via Xiaomi token plan, 262k via HuggingFace).
- **Gemini `thoughtSignature` in responses:** Gemini thinking models return `thoughtSignature` fields in response. OpenAI-compat proxy strips these correctly, but native route may not.
- **agyg CLI requires TTY:** The `agy` CLI (Gemini API CLI) uses bubbletea and requires `/dev/tty`. Does not work in non-interactive terminal contexts. Use REST API directly for headless operations. See `/root/AAA/skills/gemini-integration/references/session-2026-08-09-layer-separation.md` for antigravity managed agent deployment patterns.

## Related Skills

- `gemini-integration` — **Use this instead of inline Gemini details.** Handles LiteLLM prefix doctrine, Interactions API, managed agents (`antigravity-preview-05-2026`), agy CLI config, and all Gemini-specific pitfalls. This skill covers general multi-provider patterns; delegate Gemini questions to `gemini-integration`.

## Verification

After adding a new provider:
1. `curl -sf http://127.0.0.1:4000/v1/models -H "Authorization: Bearer $LITELLM_MASTER_KEY"` — verify model appears
2. Send a simple chat completion request — verify response
3. Check for empty content (Gemini thinking model issue)
4. Verify cost tracking in litellm logs

## Reference files

- `references/gemini-integration-2026-08-09.md` — Session-specific Gemini findings: full model landscape, pricing table, free-tier reality check, Interactions API capabilities, Antigravity managed agent deployment, and the complete integration research.
