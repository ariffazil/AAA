# Gemini API Integration Session — 2026-08-09

## Context

Mid-session incident: Hermes Agent (hermes-asi) repeatedly failed with "provider failed after retries". Root cause traced to thinking model tool-loop incompatibility (MiMo `reasoning_content` + Gemini `thought_signature`). This session documented the fix path and broader Gemini API integration patterns.

## Key Findings

### 1. Prefix doctrine (confirmed)
- `gemini/` prefix = native Gemini API with automatic thought_signature handling
- `openai/gemini-` prefix = OpenAI-compatible endpoint, NO thought_signature handling
- Tool-loop agents MUST use `gemini/` prefix

### 2. Agentic patterns
- **Interactions API** = stateful multi-turn without manual reasoning state
- **Managed agents** = persistent identity via `agents.create()` + invoke by ID
- **File mounting** = inline sources for AGENTS.md, SKILL.md at interaction time
- **previous_interaction_id** = conversation continuation without signature management

### 3. agy CLI specifics
- Model naming: use native ID (`gemini-3.6-flash`), not display name
- settings.json location: `~/.gemini/antigravity-cli/settings.json`
- MCP surface: mount federation organs as HTTP servers under `mcpServers`

### 4. litellm fixes applied
- Disabled thinking for MiMo on tool-loop seats
- Changed Gemini to `gemini/` prefix
- Added `modify_params: true`
- Removed Gemini from hermes-asi, opencode, codex, agi-333
- Created dedicated `gemini-flash`, `gemini-pro` seats

## References

- Gemini coding agents docs: https://ai.google.dev/gemini-api/docs/coding-agents
- litellm Gemini provider docs: https://docs.litellm.ai/docs/providers/gemini
- Interactions API overview: https://ai.google.dev/gemini-api/docs/interactions-overview
- Agent environments: https://ai.google.dev/gemini-api/docs/agent-environment
