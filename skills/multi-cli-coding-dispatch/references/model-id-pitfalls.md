---
name: model-id-pitfalls
description: Provider/model ID gotchas for qwen-code and opencode CLIs on the arifOS VPS. Pitfalls for routing to specific models, balance errors, and provider prefix requirements. Captures the exact failure modes encountered when dispatching sovereign work to parallel coding CLIs.
forged: 2026-08-12
source: v12 DRAFT_SPEC dispatch loop (3 parallel agents)
---

# Model ID Pitfalls — qwen-code + opencode

## TL;DR

- **`qwen-code CLI`**: NEVER pass `-m qwen3-coder-plus` — that's the wrong API surface. Use `qwen -p <prompt> -o text` without `-m` (defaults to anthropic route with hermes-asi config). Result: works.
- **DeepSeek via direct `deepseek/deepseek-v4-pro`**: API balance error. Switch to `opencode-zen/deepseek-v4-pro` (zen tier has credits).
- **`gpt-5.6-luna`**: needs explicit provider prefix. Use `opencode-zen/gpt-5.6-luna` (NOT bare `gpt-5.6-luna`).
- **`qwen3-coder-plus` etc.** as model names: invalid. The qwen-code CLI uses anthropic-compatible API; qwen-specific model names like `qwen3-coder-plus` are NOT in the anthropic endpoint's model list.

## The Full Failure Matrix

| Attempted command | Error | Fix |
|-------------------|-------|-----|
| `qwen -m qwen3-coder-plus -p ...` | `anthropic_messages: Invalid model name passed in model=qwen3-coder-plus. Call /v1/models to view available models for your key.` | Drop `-m` flag, use default anthropic-routed model |
| `opencode run --model deepseek/deepseek-v4-pro ...` | `Insufficient Balance` | Use `opencode-zen/deepseek-v4-pro` |
| `opencode run --model gpt-5.6-luna ...` | `Model not found: gpt-5.6-luna/.` | Use `opencode-zen/gpt-5.6-luna` |
| `opencode run --model opencode-go/gpt-5.6-luna ...` | works | (alternative provider) |

## How to Discover Available Models

```bash
# List ALL models from ALL providers (one-shot)
opencode models

# Filter to specific provider
opencode models opencode-zen
```

The output shows `provider/model -> name` for every available model. Examples (2026-08-12):

```
opencode-zen
  gpt-5.6-luna -> GPT 5.6 Luna (Zen)
  deepseek-v4-pro -> DeepSeek V4 Pro (Zen)
  deepseek-v4-flash -> DeepSeek V4 Flash (Zen)
  claude-sonnet-5 -> Claude Sonnet 5 (Zen)
  claude-opus-5 -> Claude Opus 5 (Zen)
  gemini-3.6-flash -> Gemini 3.6 Flash (Zen)
  kimi-k3 -> Kimi K3 (Zen)
  glm-5.2 -> GLM 5.2 (Zen)

opencode-go
  deepseek-v4-pro -> DeepSeek V4 Pro (Go)
  kimi-k3 -> Kimi K3 (Go)
  glm-5.2 -> GLM-5.2 (Go)
  gpt-5.6-luna -> GPT 5.6 Luna (Go)
```

## Dispatch Recipe (Verified 2026-08-12)

```bash
# Three parallel CLIs for Gödel E3 provider diversity
# Each writes to UNIQUE output path to avoid file collision

# 1. Qwen Code (no -m flag — defaults to anthropic route)
qwen -p "Read /path/to/SPEC.md, follow EXACTLY, save HTML to /path/to/output-qwen.html" -o text

# 2. OpenCode DeepSeek via zen tier (paid balance)
opencode run --model opencode-zen/deepseek-v4-pro "Read /path/to/SPEC.md, follow EXACTLY, save HTML to /path/to/output-deepseek.html"

# 3. OpenCode gpt-5.6-luna via zen tier (explicit provider prefix)
opencode run --model opencode-zen/gpt-5.6-luna "Read /path/to/SPEC.md, follow EXACTLY, save HTML to /path/to/output-luna.html"
```

All three can be launched in parallel via `terminal(background=true, notify_on_complete=true)` for Gödel E3 independence.

## Stale Process Discipline

When re-dispatching (e.g., after F13 correction arrives mid-stream):

```bash
# 1. List running processes
ps -ef | grep -iE "(qwen|opencode)" | grep -v grep

# 2. Kill via process tool (preferred) or kill -9 <pid>
process(action="kill", session_id="proc_xxx")

# 3. Update the canonical spec file (version bump + CHANGELOG entry)
# 4. Re-launch the three dispatches
```

A stale process running with stale spec will produce HTML that violates the new corrections. Kill it. Re-dispatch.

## Why This Is Not "Just Environment"

These model ID pitfalls look like transient environment issues, but they are PATTERNS:
- The CLI surface area is the kind of thing every dispatch hits
- Provider prefixes (`opencode-zen/` vs bare) are stable conventions, not transient outages
- Balance errors are predictable when going to direct providers instead of zen tier

When the next sovereign petition forge session happens, these pitfalls WILL come up again. Capture them as a class-level skill, not as transient fix-it notes.