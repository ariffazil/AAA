---
name: contextstream-memory-code-search
description: Persistent conversational memory, semantic code search, dependency graph mapping, pre-compaction session capture, and workspace Q&A via ContextStream MCP server (mcp.contextstream.io/mcp).
capability_tier: fed-long-context
ecology_state: WARM
---

# ContextStream Persistent Memory & Code Search Skill (`contextstream`)

ContextStream provides AI coding assistants with long-term cross-session memory, semantic codebase search, dependency graph analysis, pre-compaction state checkpointing, and team knowledge integration via `https://mcp.contextstream.io/mcp`.

## Domain Tool Surface

1. **`search`**: Hybrid semantic + keyword code search with exact-token symbol fusion.
2. **`memory`**: Persists decisions, lessons, conventions, runbooks, and project plans across sessions.
3. **`session`**: Captures critical state before context window compaction; lists and recalls past session transcripts.
4. **`qa`**: Grounded Q&A over project memory and conventions with citation receipts.
5. **`graph`**: Codebase dependency mapping, impact analysis, dead code, and circular dependency detection.
6. **`capsule`**: Packages project state into portable, shareable context snapshots for agent handoffs.

---

## Best Practices for AI Agents

1. **Pre-Compaction Capture**: Automatically trigger `session` state capture before context window compaction to prevent losing design intent and architecture decisions.
2. **Semantic Search**: Use `search` for intent-based queries ("where do we handle auth") instead of brute-force file scanning.
3. Optional `CONTEXTSTREAM_API_KEY` for index scale, graph features, and team integrations.
