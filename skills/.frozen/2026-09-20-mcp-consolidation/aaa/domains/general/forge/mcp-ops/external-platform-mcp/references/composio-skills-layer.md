# Composio Skills Layer

**Source:** https://docs.composio.dev/docs/skills (2026-08-25)

## What It Is

Composio "skills" are NOT installable plugins. They are **execution playbooks** derived from real usage across the platform, delivered automatically inside `COMPOSIO_SEARCH_TOOLS` responses.

## How It Works

1. Agent calls `COMPOSIO_SEARCH_TOOLS` with a plain-language `use_case` query
2. Composio searches for matching tools AND matching skills simultaneously
3. Response includes tool slugs + schemas. When a skill covers the use case, the same response also includes:
   - `primary_tool_slugs` — main tools for the task
   - `related_tool_slugs` — supporting tools
   - `recommended_plan_steps` — ordered execution steps (optional)
   - `known_pitfalls` — failure modes to avoid (optional)
   - `difficulty` — complexity estimate (optional)

## Key Properties

- **Read-only** — nothing to install, enable, or configure
- **No API** — no way to list/read skills separately; they arrive through search only
- **Derived from usage** — reflect how tasks actually get completed, not ideal workflows
- **Cross-app** — a skill may span multiple toolkits (e.g., Slack + Gmail)
- **Phrasing-sensitive** — "Start a DM with someone in Slack" matches; "slack tools" does not

## Verified Status (2026-08-25 — UPDATED)

**`composio search "<use case>"` CLI command WORKS** (v0.4.0):
```bash
composio search "fetch gmail emails" --limit 3
```
Returns full execution playbook JSON with:
- `recommended_plan_steps` — ordered execution guidance (pagination, error handling, fallbacks)
- `known_pitfalls` — specific failure modes with fix patterns
- `difficulty` — e.g., "easy", "moderate"
- `primary_tool_slugs` — tools to use
- `related_tool_slugs` — supporting tools

Example output for "fetch gmail emails":
```json
{
  "recommended_plan_steps": [
    "[Prerequisite]: Resolve label name→ID using GMAIL_LIST_LABELS...",
    "[Required]: List candidate messages using GMAIL_FETCH_EMAILS...",
    "[Next Step]: Re-run with page_token until nextPageToken is absent...",
    "[Next Step]: Hydrate using GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID..."
  ],
  "known_pitfalls": [
    "[GMAIL_FETCH_EMAILS] Max ~500 messages per page; 400 'Request/Response size too large'",
    "[GMAIL_FETCH_EMAILS] Pagination quirks: nextPageToken may exist even on small pulls",
    "[GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID] 404 NOT_FOUND can indicate stale/incorrect IDs"
  ],
  "difficulty": "easy",
  "primary_tool_slugs": ["GMAIL_FETCH_EMAILS"],
  "related_tool_slugs": ["GMAIL_LIST_LABELS", "GMAIL_FETCH_MESSAGE_BY_THREAD_ID", "GMAIL_GET_ATTACHMENT"]
}
```

## Relevance to arifOS

Our social-mcp gateway wraps Composio tools with policy boundaries. The skills layer enriches execution with:
- Ordered plan steps (reduces retry tokens)
- Known pitfalls (prevents common errors from surfacing in production)
- Difficulty estimates (helps decide when to defer to human)

**Current gap:** social-mcp's `ComposioClient` calls `composio execute <SLUG>` directly — it does NOT automatically fetch skills playbooks. To enrich, future integration could:
1. Add a `composio_search_and_enrich(use_case)` helper that wraps search + execute
2. Cache playbooks locally and inject them as pre-execution guidance
3. Log the recommended_plan_steps alongside audit entries for compliance review

## Meta Tools Status (via proxy)

- `COMPOSIO_SEARCH_TOOLS` — **NOT surfaced** via proxy `tools/list` (82 tools returned, all Gmail/Reddit, no meta tools)
- `COMPOSIO_MANAGE_CONNECTIONS` — **NOT surfaced** via proxy
- `COMPOSIO_WAIT_FOR_CONNECTIONS` — **NOT surfaced** via proxy
- REST API `/api/v3/connectedAccounts` — **404** (HTML page, not JSON)

**Workaround:** Use the CLI `composio search` command directly for playbook enrichment. The proxy is only for tool execution, not meta tools.
