# OpenCode Model-Slug Resolution Pitfalls

Collected during arifOS E2E MCP probe session 2026-08-07.
Use when dispatching OpenCode for audit/code tasks on this box.

## The rule: always run `opencode models` first

OpenCode's `--model` takes `provider/model-id` but exact format varies per auth config.

## What failed this session (3 dispatches, 3 errors)

```
# FAILED — "Model not found: openrouter/anthropic/claude-sonnet-4"
opencode run '...' --model openrouter/anthropic/claude-sonnet-4

# FAILED — "Model not found: anthropic/claude-sonnet-4"
opencode run '...' --model anthropic/claude-sonnet-4

# FAILED — "Model not found: claude-sonnet-4-6/." (trailing slash in error)
opencode run '...' -m claude-sonnet-4-6
```

## What worked

```
# WORKED — minimax/MiniMax-M2.7 was the first successful model
opencode run '...' -m minimax/MiniMax-M2.7
```

## Claude on this box

No direct Anthropic API key. Claude-class routing is federation-routed:
- `litellm-federation/agi-333` (333-AGI role)
- `litellm-federation/asi-555` (555-ASI role)
- `litellm-federation/apex-888` (888-APEX role)
- `litellm-federation/hermes-asi` (main Hermes model)

Use these slugs for Claude-class tasks via OpenCode, not bare `anthropic/...`.

## Coding-tuned model slugs on this box

| Slug | Notes |
|---|---|
| `kimi/kimi-for-coding` | Coding-tuned, quota may be exhausted |
| `kimi/kimi-k3` | Stronger variant, same quota concern |
| `minimax/MiniMax-M2.7` | Default substrate, reliable |
| `deepseek/deepseek-v4-pro` | Reasoning + coding |
| `qwen-token-plan/qwen3.7-max` | Strong for code tasks |
| `mimo-token-plan/mimo-v2.5` | Xiaomi MiMo, fast |

## Quota exhaustion shape

Some providers return `404 Model not found` when quota is exhausted, not `429`.
Always read full stderr — the first `Error:` may mask a second line with the real cause.

```
# KIMI K3 quota exhaustion example:
# Error: Model not found: kimi/kimi-for-coding/
# Error: {"message": "You've reached your usage limit..."}
# The second line is the real cause.
```

## Tee output pitfall

`2>&1 | tee path` after starting a background process uses `workdir` for relative paths.
Create the tee path with `mkdir -p $(dirname <path>)` IMMEDIATELY before the command,
not in a separate `terminal()` call earlier — the mkdir runs in a fresh shell.

```bash
# CORRECT: mkdir and tee in same command
mkdir -p /tmp/log-dir && opencode run '...' 2>&1 | tee /tmp/log-dir/output.log

# WRONG: separate mkdir, then background with tee
# mkdir -p /tmp/log-dir  ← separate command, different shell context
# opencode run '...' 2>&1 | tee /tmp/log-dir/output.log  ← tee fails, "No such file"
```
