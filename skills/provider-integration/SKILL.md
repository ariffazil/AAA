---
name: provider-integration
description: Integrate LLM providers (litellm proxy, API keys, model aliases) with Hermes Agent, OpenClaw, Codex, CLI agents. Covers thinking-mode quirks, routing failures, fallback chains, and cross-agent config alignment.
version: 1.0.0
author: Hermes Agent
---

# Provider Integration

Integrate LLM providers into agent ecosystems (Hermes, OpenClaw, Codex, CLI tools) via litellm federation, native SDKs, or direct API calls. Covers model aliases, thinking-model quirks, routing failures, fallback chains, and cross-agent config alignment.

## Litellm Federation Proxy (:4000)

Primary model router for all AAA warga. Fronted by HAProxy :4000 → litellm-federation :4011. Config: `/root/A-FORGE/litellm-config.yaml`.

### Model Alias Pattern

```yaml
model_list:
  - model_name: hermes-asi
    litellm_params:
      model: openai/mimo-v2.5       # provider/model format
      api_base: https://.../v1
      api_key: os.environ/MIMO_API_KEY
      order: 1                        # higher priority first
    model_info:
      max_input_tokens: 1048576
      max_output_tokens: 131072
      mode: chat
      supports_function_calling: true  # enables tool_use
```

**Order = priority.** `order: 1` = primary. `order: 99` = fallback last.

### Supported Prefixes

| Prefix | Meaning | Auth |
|--------|---------|------|
| `openai/` | Forward to any OpenAI-compatible endpoint | `api_base` + `api_key` |
| `gemini/` | Google Gemini API (native transport) | `GEMINI_API_KEY` |
| `anthropic/` | Anthropic Claude | `ANTHROPIC_API_KEY` |
| `xai/` | xAI Grok | `XAI_API_KEY` |
| `deepseek/` | DeepSeek | `DEEPSEEK_API_KEY` |
| `vertex_ai/` | Vertex AI (GCP) | GCP credentials |

**Never use `vertex_ai/` prefix when you just want an API key** — use `gemini/` instead. The unprefixed form defaults to Vertex AI.

## Thinking Models — Provider Quirks

Different thinking models have different requirements for multi-turn conversations with tool calls.

### MiMo (Xiaomi) — `reasoning_content` required on replay

MiMo requires that `reasoning_content` from assistant messages be preserved and echoed back in subsequent turns when tool calls are involved.

**Error:** `"The reasoning_content in the thinking mode must be passed back to the API."`

**Workaround:** Add `thinking: {type: disabled}` to litellm params for tool-calling paths. Or disable thinking mode entirely for those seats.

**Fix (upstream):** Hermes Agent preserves `reasoning_content` in conversation history. Issue tracker: NousResearch/hermes-agent#24443.

**See also:** `references/thinking-models.md` for detailed MiMo/Gemini/Kimi comparison.

### Gemini — thought_signature via proper prefix

When using Gemini with function calling, the `gemini/` prefix handles `thought_signature` automatically. Using `openai/gemini-*` does NOT preserve signatures.

**Error:** `"Function call is missing a thought_signature in functionCall parts"`

**Fix:** Use `gemini/gemini-3.6-flash` (not `openai/gemini-3.6-flash`). Remove `api_base` field — litellm knows the Gemini endpoint natively.

### Kimi (Moonshot) — Same as MiMo pattern

Kimi models require the same `reasoning_content` preservation. Affected: kimi-k2.5, kimi-k2-thinking. Fixed in litellm ≥ v1.84+ but only for specific model names.

## Routing Failures & Diagnostics

### Checklist for "provider failed after retries" errors

1. **Check litellm logs:** `journalctl -u litellm-federation --since "10 min ago" | grep -i "error\|400\|401\|429"`
2. **Verify model name:** Does the alias resolve to a real upstream model? Check `curl :4000/v1/models`
3. **Check fallback chain:** Are ALL fallbacks also failing the same way? (Common with thinking models)
4. **Test single provider:** Bypass litellm, call upstream directly
5. **Check API status:** Rate limit? Insufficient balance? Expired key?

### Silent fallback-chain collapse: bot alive, brain dead (2026-08-15)

**Symptom:** a Telegram bot answers instantly but replies in raw JSON, echoes/leaks the function-call schema, or turns stupid right after a `/model` switch. Transport is fine — the ENTIRE fallback chain failed silently and the terminal tier (a tiny local Ollama model, e.g. `qwen2.5-coder:1.5b`) is doing the answering. A small local model without native function calling serializes tool schemas into prose — the JSON garbage IS the tell.

**Diagnose from logs, not config — each tier has a signature:**
- `Connection error` on primary → network, not model. **Ping OK ≠ TCP OK**: ICMP passes while UFW drops the port. On the host check the proxy bind (`127.0.0.1:4000` = no other node can reach it even at 1ms ping; needs `*:4000` + `ufw allow from 100.64.0.0/10 to any port 4000`). LiteLLM may also listen on a different port (observed `:4011` on `0.0.0.0`) than the haproxy frontend the client uses — test the FRONTEND port from the remote node.
- `HTTP 400` from Gemini = Hermes tool schema rejected upstream (version-dependent `actions.items` bug) — tier unusable, skip.
- `HTTP 401` = stale key on that node; usually the service wrapper never sourcing the vault env.
- `HTTP 402` = plan exhausted, zero allocation.
- Chain terminating at Ollama local = the garbage source.

**Fix pattern (verified end-to-end, wawa node srv1642546):** expose proxy to Tailscale subnet only (haproxy injects the key, so subnet exposure is the sanctioned perimeter) → live chat-test the proxy FROM the remote node before touching config → rewrite remote primary to the verified-live proxy → **DELETE dead tiers (401/402) from the fallback chain** instead of leaving them as false safety → wrapper must source vault env → restart with `--replace` (a stale pidfile makes the fresh instance exit) → verify single process + pidfile match + `ss -tnp` ESTABLISHED to api.telegram.org. Age any scary log errors by line number before owning them — chronic node noise (Telegram connect backoff, old proxy errors) predated the change.

Full incident: `references/fallback-chain-collapse-2026-08-15.md`.

### Common HTTP Status Codes

| Code | Meaning | Fix |
|------|---------|-----|
| 400 | Bad request — model/name wrong, thinking mode mismatch | Fix model name, disable thinking |
| 401 | Unauthorized — bad/expired key | Check API key validity |
| 429 | Rate limited / insufficient balance | Wait, switch provider, top up |
| 500 | Internal server error | Retry, check provider status |
| 503 | Service unavailable | Provider down, check health |

### litellm Settings You Should Know

```yaml
litellm_settings:
  num_retries: 2                    # retry attempts before giving up
  request_timeout: 60               # seconds per request
  drop_params: true                 # drop unknown params silently
  modify_params: true               # auto-strip thinking when blocks missing
router_settings:
  routing_strategy: usage-based-routing  # round-robin, usage-based, ...
  cooldown_time: 300                # seconds to pause depleted providers
```

**Critical:** `modify_params: true` makes litellm automatically strip thinking parameters when `thinking_blocks`/`reasoning_content` are missing from conversation history. This prevents 400 errors on thinking-mode mismatch but DEGRADES output quality (no reasoning).

## Qwen Token Plan vs DashScope PAYG (verified 2026-08-10)

Two separate Alibaba Cloud endpoints with different keys, models, and billing.
**Never confuse them — wrong key on wrong endpoint = 401/404.**

| Dimension | Token Plan | DashScope PAYG |
|---|---|---|
| **Endpoint** | `token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` | `ws-wlab8klalfojzq7i.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| **Key format** | `sk-sp-H.xxx` (Individual) or `sk-sp-H.IEHM...` (Team) | `sk-ws-H.YLXYLM...` |
| **Models** | 22 models (qwen3.8-max, qwen3.7-max, deepseek-v4-pro, wan2.7-image) | 156 models (all Token Plan + qwen-vl-max, qwen-image-3.0-pro, qwen3.5-flash, etc.) |
| **Billing** | Credits-based, 5-hour rolling windows | Pay-as-you-go, per-request |
| **Rate limit** | Shared multi-tenant queue | Isolated, guaranteed zero-queue |
| **Image gen endpoint** | ❌ `/images/generations` returns 404 | ✅ Works via chat completions with `qwen-image-3.0-pro` |
| **Vision models** | ❌ No qwen-vl-max | ✅ qwen-vl-max available |

**Key isolation rule:** `sk-xxx` (standard ModelStudio) keys throw 401 on Token Plan endpoints. Always use `sk-sp-` prefix keys for Token Plan.

**Routing strategy:**
- Token Plan → background agent processes (OpenCode, OpenClaw daemons) — cheaper, Credits-based
- PAYG → interactive sessions, multimodal tasks (vision, image gen) — more models, per-request
- Gemini → multimodal, long-context, search-augmented, video gen

**⚠️ Spec hallucination warning:** Some integration specs claim `dashscope.aliyuncs.com/compatible-mode/v1` as the endpoint. This returns `invalid_api_key` for PAYG keys. The actual endpoints are tenant-specific subdomains. Always verify with a live probe before configuring.

## Cross-Agent Config Alignment

Different agents may route to different providers. Keep them aligned:

1. **HERMES → hermes-asi** → picks from ordered litellm pool
2. **OpenCode → opencode** → separate seat in litellm config
3. **Codex → codex** → another seat
4. **AGY → agy** → Gemini-native (separate from litellm)

**Rule:** Each agent seat should have independent ordering. Don't force all agents through the same primary — if Gemini exhausts budget, hermes-asi shouldn't starve too.

## Dual-Provider Architecture (FED Router)

FED (:7074) routes by **capability signature**, not by default provider:

```
QWEN POOL (Deep Reasoning): deepseek-v4-pro, qwen3.8-max, qwen3.7-max
GEMINI POOL (Multimodal): gemini-3.1-pro, gemini-3.6-flash, Veo 3.1, image-01
```

| Task Type | Route To | Why |
|---|---|---|
| Deep reasoning / coding | Qwen | Strongest code/reasoning models |
| Image generation | Gemini | Native multimodal (gemini-3-pro-image) |
| Video generation | Gemini | Only video-capable (Veo 3.1) |
| Web search + reasoning | Gemini | Native search tool |
| Long context (>100K) | Gemini | 1M+ token window |
| Fast sub-agent tasks | Gemini | gemini-3.5-flash-lite, cheapest |

Spec: `/root/AAA/governance/GEMINI_AGENTIC_INTEGRATION_SPEC.md`

## Provider Retirement Hygiene

When a provider dies (quota exhausted, key revoked, endpoint deprecated, free tier eliminated), the federation scatters references across docs, configs, skills, and cron jobs. A retirement sweep must classify each hit before mutating.

### Discovery sweep (search all surfaces)

```bash
# 1. Search the whole federation for the provider name (case-insensitive)
search_files --target=content --path=/root --pattern='<provider>' --limit=30 --output_mode=files_only

# 2. Check env vars and secrets
grep -ri '<PROVIDER>' /root/.secrets/ 2>/dev/null

# 3. Check live runtime processes
ps auxw | grep -i <provider> | grep -v grep

# 4. Check litellm config for model_list entries
grep -i '<provider>' /root/A-FORGE/litellm-config.yaml 2>/dev/null

# 5. Check cron jobs for provider references
grep -i '<provider>' /usr/local/lib/hermes-agent/profiles/aaa-hermes/cron/jobs.json 2>/dev/null
```

### Classification matrix — decide before mutating

| Hit location | Type | Action |
|---|---|---|
| `.env` / secrets file | Active config | Remove key entry. Mark `# RETIRED <date>: <reason>` |
| `litellm-config.yaml` model_list | Active routing | Remove entry. Restart litellm-federation. |
| Cron job prompt (`jobs.json`) | Active consumer | Update prompt to use sovereign primary. Verify next fire. |
| Skill SKILL.md provider table | Reference doc | Mark retired: `~~Provider~~ \| ~~`KEY`~~ \| **RETIRED <date>** — <reason>. Sovereign primary: <replacement>. \|` |
| Reference doc env var table | Reference doc | Same strikethrough pattern |
| Enum value list (`MCP_SEARCH_PROVIDER`) | Option space | Leave as-is or annotate: `searxng`, `model`, `brave` (~~tavily~~ retired <date>) |
| VAULT999 historical receipts | Immutable truth | **NEVER touch.** Historical evidence of what was. |
| Skill pitfall/lesson entries | Institutional scar | **NEVER remove.** The lesson survives even if the provider doesn't. |

### The marking convention

Three elements: strikethrough on name + key, bold RETIRED tag with date, reason + replacement. Example:

```
| ~~Tavily~~ | ~~`TAVILY_API_KEY`~~ | **RETIRED 2026-08-12** — dev plan exhausted (HTTP 432). SearXNG is sovereign primary. |
```

Future agents scanning the table see the retirement, not a gap.

### Iron rules

- **Reference docs describing option space are NOT active config.** A doc that lists Tavily as one of five search backends is educational, not a runtime dependency. Removing it falsifies the reference.
- **Historical receipts (VAULT999) are immutable truth.** A retirement never rewrites what was sealed.
- **Lessons survive retirement.** A pitfall about Tavily rate-limiting stays in the skill even after Tavily is retired — the pattern (provider quota exhaustion → pivot to sovereign infra) generalizes.
- **Pivot to sovereign infrastructure first.** Tavily (paid, external) → SearXNG (self-hosted, $0). This is the F1 Amanah preference: sovereign > dependent.

Worked example (Tavily cleanup 2026-08-12): `references/provider-retirement-tavily-2026-08-12.md`

## Direct Provider Pattern (BYOK Sovereign Path)

When a provider offers a direct OpenAI-compatible endpoint and the sovereign holds a BYOK key, add it as a **direct provider** to agent configs — bypassing all middlemen (OpenCode Zen, OpenRouter, TokenRouter).

**Dual-path doctrine:** Both paths coexist:
- **Direct** (`zai/glm-5.2` in OpenCode) → lowest latency, sovereign BYOK, no proxy overhead
- **Proxy** (`zai-pro` alias in FED/LiteLLM) → mesh diversity, FED routing intelligence, fallback resilience

**Rule:** When sovereignty matters (F13-grade work), prefer direct. When mesh diversity matters (Gödel E3), prefer proxy. Both must be live — not either/or.

**Integration checklist:**
1. Probe the provider's endpoint with the key → verify live + list models
2. Add `provider.<name>` entry to OpenCode `opencode.json` with `baseURL`, `apiKey: {env:KEY}`, model definitions
3. Add to `enabled_providers` list
4. Verify FED/LiteLLM has a corresponding alias (may already exist)
5. Test both paths: direct via OpenCode config + proxy via `curl :4000/v1/chat/completions`

Worked example (Z.AI direct, 2026-08-12): `references/provider-direct-zai-2026-08-12.md`

Worked example (FLAME stage routing, 2026-08-12): `references/flame-stage-routing-2026-08-12.md`

## References

- `references/thinking-models.md` — Provider-specific quirks (MiMo reasoning_content, Gemini thought_signature, Kimi compatibility)
- `references/qwen-provider-audit-2026-08-10.md` — Qwen Token Plan vs DashScope PAYG audit
- `references/provider-retirement-tavily-2026-08-12.md` — Tavily retirement worked example: multi-surface sweep, classification, marking convention
