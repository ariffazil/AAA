---
name: thinking-model-tool-loops
description: "Diagnose and fix thinking model + tool loop incompatibilities — the reasoning_content / thought_signature 400-error cascade. Covers MiMo, Gemini 3+, DeepSeek R1, Kimi K2, and any future thinking model that requires reasoning state to be echoed back in multi-turn tool-calling conversations. Trigger: 'reasoning_content must be passed back', 'thought_signature missing', thinking model works for first turn then fails, mid-task provider failure with thinking model, agent dies after tool call on thinking model."
tags: [thinking, reasoning, tool-loop, miimo, gemini, deepseek, litellm, 400-error]
---

# Thinking Model Tool Loops

Thinking models (MiMo, Gemini 3+, DeepSeek R1, Kimi K2) return reasoning state in their responses. When used as tool-calling agents (multi-turn conversations with function calls), this reasoning state must be preserved in conversation history. Failure = 400 error cascade that looks like auth/key issues but isn't.

## Core lesson

**400 error on thinking model after tool call ≠ key problem.** It's a reasoning-state preservation failure. Check `reasoning_content` / `thought_signature` first.

## The three-layer failure chain

| Layer | Problem | Error signature |
|-------|---------|-----------------|
| **Primary** | Client strips `reasoning_content` from assistant messages | `The reasoning_content in the thinking mode must be passed back to the API` |
| **Secondary** | Gemini uses wrong prefix (`openai/` instead of `gemini/`) | `Function call is missing a thought_signature in functionCall parts` |
| **Tertiary** | All fallbacks hit same issue → total collapse | `provider failed after retries` |

## Diagnosis recipe

```bash
# 1. Confirm the error is reasoning_content, not auth
journalctl -u litellm-federation --since "30 min ago" | grep -i "reasoning_content\|thought_signature\|BadRequest" | tail -20

# 2. Check which model is failing
grep -B5 "hermes-asi\|agi-333\|opencode" /root/A-FORGE/litellm-config.yaml | head -20

# 3. Test with thinking disabled (quick workaround)
curl -s http://127.0.0.1:4000/v1/chat/completions \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"hermes-asi","messages":[{"role":"user","content":"hi"}],"max_tokens":10}'
```

## Fix hierarchy (in priority order)

1. **Immediate:** Disable thinking mode for the affected model
   - MiMo: add `thinking: {type: disabled}` to litellm_params
   - Gemini: set `reasoning_effort: "none"` (up to 96% cheaper)
2. **Config fix:** Switch Gemini prefix from `openai/` to `gemini/` in litellm config
3. **litellm settings:** Add `modify_params: true` under `litellm_settings:` in config.yaml — automatically strips the `thinking` param when assistant message with `tool_calls` is missing reasoning state. This is the catch-all workaround that prevents thinking+tools incompatibility errors across ALL thinking models (MiMo, Gemini, Kimi, Anthropic). See litellm docs at `/docs/reasoning_content`.
4. **Remove Gemini from tool-loop agent seats.** Agent seats (hermes-asi, opencode, codex, agi-333) run chained tool calls and need models that preserve reasoning state. Gemini's `thought_signature` cannot yet be preserved by litellm or Hermes → remove from these seats. Create dedicated single-turn seats (`gemini-flash`, `gemini-pro`) instead.
5. **Long-term:** Wait for client (Hermes Agent) to preserve reasoning state natively

## Per-model requirements

| Model | Field required | Default state | Disable method |
|-------|---------------|---------------|----------------|
| MiMo v2.5 | `reasoning_content` | Thinking ON | `thinking: {type: disabled}` |
| Gemini 3+ | `thought_signature` | Thinking ON (high) | `reasoning_effort: "none"` |
| DeepSeek R1 | `reasoning_content` | Thinking ON | `reasoning_effort: "none"` |
| Kimi K2.5 | `reasoning_content` | Thinking ON | Not yet documented |

## Gemini prefix doctrine

| Prefix | Endpoint | thought_signature | Safe for tool loops |
|--------|----------|-------------------|---------------------|
| `gemini/` | Native Gemini API | ✅ Handled automatically | YES |
| `openai/gemini-` | OpenAI-compatible `/v1beta/openai` | ❌ Not handled | NO |

**Rule:** Any Gemini model used for tool-calling MUST use `gemini/` prefix.

## Known bugs

- **Hermes Agent Issue #24443**: MiMo `reasoning_content` not preserved in chat history (open, P2)
- **litellm Issue #16893**: Gemini `thought_signature` missing in streaming mode (closed, fixed v1.81+)
- **OpenClaw Issues #81419, #81990, #82118**: Same MiMo issue across OpenClaw

## Pitfalls

- **400 after tool call on thinking model ≠ key issue.** Always check reasoning_content/thought_signature first before probing auth.
- **Empty `content` + `finish_reason: length` on thinking models = reasoning consumed all tokens.** Re-probe with `max_tokens: 200+` before diagnosing as dead.
- **litellm does NOT cascade fallback on HTTP 400.** Credit exhaustion + thinking model error = silent agent death. See `provider-quota-diagnostics` for the 400-no-cascade doctrine.

## Reference files

- `references/thinking-model-tool-loop-2026-08-09.md` — full diagnostic transcript from live incident
- `references/gemini-api-integration-2026-08-09.md` — Gemini API key setup and agy CLI config
