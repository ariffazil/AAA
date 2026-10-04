---
name: gemini-integration
description: "Integrate Gemini API into the arifOS federation — LiteLLM model group wiring (prefix doctrine), managed agent creation via Interactions API, agy CLI (Antigravity) configuration, and MCP server registration. Trigger: 'add Gemini to FED', 'wire GEMINI_API_KEY', 'agy CLI config', 'managed agent creation', 'interactions API with previous_interaction_id', 'why does Gemini need gemini/ not openai/', or any Gemini API key/model routing task."
tags: [gemini, api-key, litellm, prefix, antigravity, interactions, mcp]
---

# Gemini API Integration

## Core lesson: prefix is NOT cosmetic

| Prefix | Endpoint | thought_signature | Tool-loop safe | Use for |
|--------|----------|-------------------|---------------|---------|
| `gemini/` | Native Gemini API (`generativelanguage.googleapis.com`) | ✅ Handled automatically by litellm | YES | Tool-calling agents, multi-turn |
| `openai/gemini-` | OpenAI-compatible `/v1beta/openai` | ❌ Not handled | NO | Single-turn, vision, image gen only |

**Rule:** Any Gemini model used for tool-calling MUST use `gemini/` prefix. The `openai/` prefix sends requests to the OpenAI-compat endpoint which doesn't handle thought_signatures.

## litellm config pattern

### Correct Gemini entry:
```yaml
- model_name: <seat-name>
  litellm_params:
    model: gemini/<model-id>          # ← gemini/ prefix
    api_key: os.environ/GEMINI_API_KEY  # ← no api_base needed
  model_info:
    max_input_tokens: 1048576
    max_output_tokens: 65536
    mode: chat
    supports_vision: true
    supports_function_calling: true
```

### WRONG (current in some seats):
```yaml
- model_name: hermes-asi
  litellm_params:
    model: openai/gemini-3.6-flash    # ← WRONG PREFIX
    api_base: https://generativelanguage.googleapis.com/v1beta/openai  # ← UNNECESSARY
    api_key: os.environ/GEMINI_API_KEY
```

## Agentic Gemini — Interactions API

The Google GenAI SDK's Interactions API handles multi-turn stateful conversations WITHOUT requiring manual handling of `thought_signature` or `reasoning_content`. Two modes:

### Mode A: Inline interaction (no setup)
```bash
curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent": "antigravity-preview-05-2026",
    "input": "Your prompt here",
    "system_instruction": "Custom instructions"
  }'
```

### Mode B: Managed agents (persistent identity)
```bash
# Create a managed agent
curl -X POST "https://generativelanguage.googleapis.com/v1beta/agents" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "my-data-analyst",
    "base_agent": "antigravity-preview-05-2026",
    "agent_config": {"type": "antigravity", "model": "gemini-3.6-flash"},
    "system_instruction": "You are a data analyst...",
    "base_environment": {
      "type": "remote",
      "sources": [
        {"type": "inline", "target": ".agents/AGENTS.md", "content": "..."},
        {"type": "inline", "target": ".agents/skills/my-skill/SKILL.md", "content": "..."}
      ]
    }
  }'

# Invoke by ID
curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"agent": "my-data-analyst", "input": "Analyze this data..."}'
```

### Stateful multi-turn
Use `previous_interaction_id` from a prior response to continue conversation — no manual reasoning state management needed.

## agy CLI (Antigravity) Configuration

### settings.json structure
Location: `~/.gemini/antigravity-cli/settings.json`

Key fields:
- `"model"`: Native model name (e.g., `"gemini-3.6-flash"`, NOT the display name `"Gemini 3.6 Flash (Low)"`)
- `"agent"`: Agent harness identifier (e.g., `"antigravity-preview-05-2026"`)
- `"systemInstruction"`: Bootstrap instruction text loaded at session start
- `"mcpServers"`: Dictionary of MCP server configs

### Model naming quirk
litellm alias `"hermes-asi"` → resolves to `openai/mimo-v2.5` → upstream display name `"Gemini 3.6 Flash (Low)"`. But the ACTUAL native model name is `gemini-3.6-flash`. Never use the display name when specifying models programmatically.

### MCP surface mounting
Add servers under `mcpServers` dict:
```json
{
  "arifos": {"url": "http://localhost:8088/mcp", "type": "http"},
  "ariff flow": {"command": "python3", "args": ["/root/arifFlow/mcp/arifflow-mcp.py"]},
  "gemini-docs": {"url": "https://gemini-api-docs-mcp.dev", "type": "http"}
}
```

## MCP Server Registration

Google provides a public **Gemini Docs MCP** server at `https://gemini-api-docs-mcp.dev`. Adds a `search_documentation` function that retrieves real-time Gemini API documentation. Add to FED's MCP registry or individual agent configurations.

## Pitfalls

- **Never use `openai/` prefix for Gemini tool-calling.** It breaks thought_signatures. Only use for single-turn/vision where signatures aren't needed.
- **Gemini must NOT be a primary seat for multi-turn tool-loop agents.** Agent seats (hermes-asi, opencode, codex, agi-333) that run chained tool calls need models preserving reasoning state natively. Until litellm/Hermes preserves `thought_signature` across turns, Gemini's only role in FED is single-turn/vision/image-gen via dedicated seats (`gemini-flash`, `gemini-pro`). Tool-loop + Gemini = 400 cascade.
- **Display names ≠ model IDs.** `Gemini 3.6 Flash (Low)` is a display label. The actual model ID is `gemini-3.6-flash`. Using display names in code/api calls fails.
- **Temperature must be 1.0 for Gemini 3+ models.** Lower temps can cause infinite loops and degraded performance. litellm sets this automatically if unspecified.
- **Interactions API = stateful without manual reasoning state.** Use `previous_interaction_id` for multi-tool Gemini instead of trying to preserve `thought_signature` manually through litellm.
- **Free tier gutted by Google (Feb 2026).** Many models now return `429` with `"limit: 0"` on free accounts. Verify quota BEFORE wiring — do not deploy a free-tier seat expecting production capacity. Enable paid tier billing for sustained agent use.
- **Antigravity requires `"environment": "remote"`.** Missing this field → HTTP 400 error. Always include when interacting with Antigravity agents.
- **agy CLI requires TTY /dev/tty.** Uses bubbletea terminal UI. Fails with `bubbletea: could not open TTY` in non-interactive contexts (cron, SSH, headless). For headless operations, use REST API directly: `curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions"`. agy version: 1.1.11.
- **agy CLI model names are display names, not API IDs.** `agy -p` accepts `--model` with human-readable display names like `"Claude Sonnet 4.6 (Thinking)"`, `"Gemini 3.6 Flash (High)"`, `"GPT-OSS 120B (Medium)"` — NOT the standard `provider/model-id` format (`anthropic/claude-sonnet-4` will error `model not recognized`). Run `agy --help` output to see available models. The mapping is: display name → internal model ID managed by Antigravity's backend.
- **Managed agent `id` restrictions.** Must be unique within your project. Cannot start with reserved prefixes (`google-`, `gemini-`). Use descriptive IDs like `federation-agent`, `data-analyst`, `issue-resolver`.
- **Environment size limits for managed agents.** Each source content >1MB is skipped. Total payload per interaction limited by the underlying model's input context window. Split large files into workspace directories rather than inlining.
- **Managed agents provision fresh sandbox on every invocation.** Files are loaded from `base_environment.sources` on each call. No persistent state between interactions unless you seed workspace files and rely on file system persistence within the same interaction turn.
- **`agent`: "antigravity-preview-05-2026"** is the base harness ID. Use this in `base_agent` for managed agents and in the `agy` CLI settings as the default agent harness.

## Reference files

- `references/thinking-model-tool-loop-2026-08-09.md` — full diagnostic of thinking model failures that led to this integration
