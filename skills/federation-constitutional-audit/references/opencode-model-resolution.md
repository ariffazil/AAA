# OpenCode Model Resolution — Pitfall Reference

## The Problem

OpenCode's `--model` flag uses its **own provider registry**, NOT the `openrouter/` proxy prefix convention. Using the wrong format causes immediate failure.

## Evidence (2026-08-10)

```
$ opencode run '...' --model openrouter/anthropic/claude-sonnet-4
Error: Model not found: openrouter/anthropic/claude-sonnet-4. Did you mean:
  anthropic/claude-sonnet-4, anthropic/claude-sonnet-4.5, anthropic/claude-sonnet-4.6?
```

The error suggests `anthropic/` prefix works — but ONLY if Anthropic is registered in OpenCode's credential store. On the arifOS box (2026-08-10), no Anthropic credentials are configured.

## Available Models (2026-08-10, arifOS box)

```
opencode models 2>&1
```

Key providers:
| Provider prefix | Example models | Notes |
|----------------|---------------|-------|
| `deepseek/` | deepseek-chat, deepseek-reasoner, deepseek-v4-flash, deepseek-v4-pro | ✅ Best reasoning |
| `kimi/` | k3, k3-256k, kimi-for-coding, kimi-k3 | ✅ Good for code |
| `bailian-token-plan-payments/` | deepseek-v4-flash-0731, qwen3.7-max, glm-5.2 | ✅ Alibaba route |
| `litellm-federation/` | agi-333, apex-888, asi-555, hermes-asi, opencode | ✅ Federation aliases |
| `qwen-token-plan/` | deepseek-v3.2, deepseek-v4-flash, deepseek-v4-pro | ✅ Qwen-hosted |
| `mimo-token-plan/` | mimo-v2.5, mimo-v2.5-pro | ✅ MiniMax |
| `ollama/` | qwen2.5-coder:3b | ⚠️ Local only |

## Resolution Rule

Format: `<provider>/<model-name>`

Where `<provider>` is the registered provider prefix from `opencode models`. NOT `openrouter/`, NOT `bailian/`, NOT any proxy prefix.

## Best Practice

Before spawning any OpenCode task:
```bash
opencode models 2>&1 | grep <desired-provider>
```

Pick from the actual list. Do not guess provider/model combinations.

## Cross-Reference

- Bundled skill: `opencode` (protected, cannot be patched)
- This reference is maintained under `federation-constitutional-audit` umbrella
