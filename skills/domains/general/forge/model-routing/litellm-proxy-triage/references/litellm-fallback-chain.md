# LiteLLM Fallback Chain — Layout Reference

> Snapshot 2026-08-27. Source: `/root/A-FORGE/litellm-config.yaml` lines 1896-1910.
> Verify against live config before relying on this.

## Router Settings — `context_window_fallbacks`

When the primary model in a model_group exceeds its `max_input_tokens`,
litellm walks this chain. The chain MUST terminate at a model with
`max_input_tokens >= 1048576` (1M ctx), otherwise overflow cascades
through every entry and dies.

Current shape:

```yaml
router_settings:
  context_window_fallbacks:
    - agi-333:    [apex-888, i-arif, forge-777]
    - forge-777:  [agi-333, apex-888, i-arif]
    - i-arif:     [apex-888, forge-777, agi-333]
    - asi-555:    [apex-888, agi-333, i-arif]
```

## 1M-ctx Anchor Models (the only safe terminal nodes)

| Model | Provider | Source line | Notes |
|---|---|---|---|
| `gemini-2.5-pro` | Gemini | 14-33 | apex-888 order 1, FREE tier, primary judge |
| `gemini-3.6-flash` | Gemini | 34-53 | apex-888 order 2, fast multimodal fallback |
| `qwen3.8-max` (Team Owner seat) | Qwen Token Plan | 102-114 | apex-888 order 99, vision + tools |
| `qwen3.8-max` (Individual seat) | Qwen Token Plan | 314-325 | i-arif, 36d runway, PRIMARY individual |
| `kimi-k3` (Moonshot direct) | Moonshot API | 221-232 | 1M ctx, coding specialist |
| `deepseek-v4-pro` (OpenCode Go) | OpenCode Go | 234-243 | 1M ctx, $10/mo Go tier |
| `MiniMax-M3` | MiniMax Token Plan | 209-218, 303-312 | 1M ctx, $50/mo, has quota windows |

## 131k-cap Models (DO NOT put as sole terminal fallback)

These all cap at 131072 tokens. If a 138k-token session routes here, it dies
with `ContextWindowExceededError` and the chain must continue.

- `deepseek-v4-pro` via Qwen Token Plan (line 56-64, 110-1109, etc.)
- `deepseek-v3.2` via Qwen Token Plan
- `glm-5`, `glm-5.1`, `glm-5.2`, `glm-5.3` via Qwen Token Plan
- `kimi-k2.5`, `kimi-k2.6` via Qwen Token Plan

If the entire fallback chain only contains 131k-cap models (the bug seen
2026-08-27), every overflow crashes the federation.

## apex-888 Entry Shape (reference)

```yaml
- model_name: apex-888
  litellm_params:
    model: gemini/gemini-2.5-pro
    api_key: os.environ/GEMINI_API_KEY
    safety_settings:
      - category: HARM_CATEGORY_HARASSMENT
        threshold: BLOCK_NONE
      # ... BLOCK_NONE for all categories (F1-F13 is our safety layer)
    order: 1
  model_info:
    max_input_tokens: 1048576
    max_output_tokens: 65536
    mode: chat
    supports_vision: true
```

`BLOCK_NONE` is intentional — arifOS kernel (port 8088) is the
constitutional guard, not litellm.

## Editing Discipline

1. Always `cp litellm-config.yaml litellm-config.yaml.bak-<UTC-timestamp>` first.
2. Validate YAML syntax: `python3 -c "import yaml; yaml.safe_load(open('/root/A-FORGE/litellm-config.yaml'))"`
3. Restart via systemd: `systemctl restart litellm-federation` (NOT nohup).
4. Verify: `systemctl status litellm-federation` shows `Active: active`, then `ss -tlnp | grep :4011`.
5. Health check: `curl -s http://127.0.0.1:4011/health -H "Authorization: Bearer $LITELLM_MASTER_KEY" | jq '.healthy_count'`.