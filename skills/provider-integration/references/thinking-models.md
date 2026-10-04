# Thinking Models — Provider Quirks

Different thinking/reasoning models have different requirements for multi-turn conversations with tool calls. This reference captures the specific quirks discovered 2026-08-09 when diagnosing mid-task failures in Hermes Agent → litellm federation.

## The Core Problem

When Hermes Agent calls a thinking model (MiMo, Kimi, Gemini) that returns `reasoning_content` in responses, subsequent turns after tool calls can fail because `reasoning_content` is not preserved in conversation history.

**Root cause:** Hermes Agent normalizes assistant messages to `role`/`content`/`tool_calls` but drops `reasoning_content`. The upstream provider then rejects the request because the required reasoning state is missing.

## Provider Comparison

| Provider | Field Required | Affected Models | litellm Fix Available? | Hermes Agent Fix? |
|----------|---------------|-----------------|----------------------|-------------------|
| **MiMo (Xiaomi)** | `reasoning_content` | mimo-v2.5, mimo-v2.5-pro, MiMo-V2-Pro, MiMo-V2-Omni, MiMo-V2-Flash | ⚠️ Partial (only specific model names in model_prices.json) | ❌ Open (Issue #24443) |
| **Kimi (Moonshot)** | `reasoning_content` | kimi-k2.5, kimi-k2-thinking, kimi-k2-thinking-turbo | ✅ Fixed in v1.84+ (kimi only) | ❌ Open |
| **Gemini** | `thought_signature` (via `provider_specific_fields`) | gemini-3.x, gemini-2.5-flash | ✅ Fixed (gemini/ prefix handles it) | N/A (use gemini/ prefix) |
| **DeepSeek** | `reasoning_content` | deepseek-reasoner, deepseek-r1 | ⚠️ Partial | ❌ Open |
| **Anthropic** | `thinking_blocks` (list of blocks) | claude-3.7-sonnet, claude-sonnet-4 | ✅ Full (native support) | ✅ Full |
| **OpenAI** | Internal (server-side) | o1, o3, o4-mini | N/A | N/A (stateless) |

## MiMo Details

**Error message:**
```
BadRequestError: OpenAIException - The reasoning_content in the thinking mode must be passed back to the API.
```

**When it happens:** After a tool call completes and Hermes builds the next turn's conversation history. The assistant message with `tool_calls` is missing `reasoning_content`.

**Immediate workarounds:**

1. **Disable thinking for tool-calling seats:**
```yaml
litellm_params:
  model: openai/mimo-v2.5
  thinking: {type: disabled}
```

2. **Route tool-calling to a non-thinking model:**
```yaml
model_list:
  - model_name: hermes-asi
    litellm_params:
      model: openai/qwen3.6-flash  # non-thinking model
      api_base: https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
```

3. **Use `modify_params: true` in litellm_settings** — litellm auto-strips thinking when blocks are missing. Degrades quality but prevents 400 errors.

**Upstream fix needed:** Hermes Agent must preserve `reasoning_content` from assistant messages in conversation history and include it when constructing subsequent requests. Issue: https://github.com/NousResearch/hermes-agent/issues/24443

## Gemini Details

**The critical distinction:**

- `gemini/gemini-3.6-flash` → Native Gemini API. Thought signatures handled automatically.
- `openai/gemini-3.6-flash` → OpenAI-compatible endpoint. Does NOT preserve thought signatures.

**Error message:**
```
Function call is missing a thought_signature in functionCall parts. This is required for tools to work correctly.
```

**Fix:** Always use the `gemini/` prefix for Gemini models when function calling is involved. Remove `api_base` field — litellm knows the endpoint.

```yaml
# CORRECT
- model_name: hermes-asi
  litellm_params:
    model: gemini/gemini-3.6-flash
    api_key: os.environ/GEMINI_API_KEY
    # NO api_base field — litellm handles it

# WRONG (thought signatures broken)
- model_name: hermes-asi
  litellm_params:
    model: openai/gemini-3.6-flash
    api_base: https://generativelanguage.googleapis.com/v1beta/openai
    api_key: os.environ/GEMINI_API_KEY
```

**Also set `temperature=1.0`** for Gemini 3 models. Lower temperatures can cause infinite loops or degraded reasoning.

## Kimi Details

Same pattern as MiMo. Fixed in litellm for specific model names only:
- kimi-k2.5 ✅
- kimi-k2-thinking ✅
- kimi-k2-thinking-turbo ✅
- kimi-k2.6 ❌ (not in model_prices.json yet — requires manual `supports_reasoning: true` addition)

**Workaround:** Same as MiMo — disable thinking or use `modify_params: true`.

## Cascade Failure Pattern

When a primary thinking model fails, litellm tries fallbacks. If ALL fallbacks are also thinking models with the same issue, you get total cascade failure:

```
MiMo 400 → Gemini fallback → 400 (thought_signature missing) → DeepSeek fallback → 400 (wrong model name) → "provider failed after retries"
```

**Prevention:** Ensure at least one fallback in the chain is a non-thinking model or uses a provider that doesn't require reasoning_content preservation.

## litellm Version Notes

- v1.63.0+: `reasoning_content` standardization added
- v1.83.10: Kimi k2.5 reasoning_content fix
- v1.84+: Kimi k2.6 NOT included (must add manually)
- v1.90.2: Current version on this system — MiMo NOT fully fixed
- v1.96.0: Latest available

**Upgrade litellm** when MiMo-specific fix lands upstream. Track: https://github.com/BerriAI/litellm/issues?q=reasoning_content+mimo

## Debugging Checklist

1. Check litellm logs for the exact error message
2. Identify which provider/model is failing
3. Check if it's a thinking model (look for `reasoning_content` or `thought_signature` in error)
4. Apply appropriate workaround (disable thinking, change prefix, upgrade litellm)
5. Verify with a multi-turn test that includes tool calls
