---
name: prompts-chat-library
description: Access thousands of curated AI system prompts, role personas, task templates, and variable substitution templates directly via prompts.chat MCP server (@fkadev/prompts.chat-mcp).
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Prompts.chat System Prompt Library Skill (`prompts-chat`)

The `prompts-chat` MCP server grants AI agents direct access to thousands of curated system prompts, role-playing personas, coding instructions, and specialized task templates from `prompts.chat`.

## Primary Capabilities & Tools

1. **`search_prompts`**: Search AI prompts by keyword, category (e.g. `coding`, `productivity`, `cybersecurity`), or tag.
2. **`get_prompt`**: Retrieve prompt details by ID with template variable substitution (`${variable}`).
3. **`save_prompt`**: Save new prompt templates to account registry for team reuse (requires `PROMPTS_API_KEY`).
4. **Native MCP Prompts**: Exposes `prompts/list` and `prompts/get` for automatic prompt picker integration in supported editors.

---

## Best Practices for Federation Agents

1. **Dynamic Persona Activation**: Use `search_prompts` when spawning subagents or executing specialized domain roles (e.g. Linux Terminal, Security Auditor, Code Reviewer, Technical Writer) to fetch refined system prompt templates.
2. **Variable Substitution**: Pass parameters to `get_prompt` to populate template variables dynamically.
