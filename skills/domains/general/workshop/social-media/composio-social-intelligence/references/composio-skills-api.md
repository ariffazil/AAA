# Composio Skills API — Runtime Playbook Mechanism

*Extracted from docs.composio.dev/docs/skills (2026-08-25)*

## Key Concepts

A **skill** in Composio is an execution playbook for one concrete task. It records:
- Which tools the task needs
- The order to call them in
- The mistakes that make it fail

## How Skills Reach Your Agent

Skills arrive through the search step a session already performs:

1. Agent has something to do → calls `COMPOSIO_SEARCH_TOOLS` with task in plain language
2. Composio searches for tools AND a skill covering that use case simultaneously
3. Response carries tool slugs + schemas. When a skill covers the use case, same response carries plan + pitfalls
4. Agent works through returned steps in order and checks pitfalls as it goes

## Response Structure

```json
{
  "primary_tool_slugs": ["SLACK_FIND_CHANNELS", "SLACK_SEND_MESSAGE"],
  "related_tool_slugs": ["SLACK_FIND_USERS"],
  "difficulty": "easy - Simple single-tool operation with known parameters",
  "recommended_plan_steps": [
    "Resolve the channel ID with SLACK_FIND_CHANNELS before posting.",
    "Send the message with SLACK_SEND_MESSAGE using the resolved ID."
  ],
  "known_pitfalls": [
    "Passing a channel name where the API expects an ID returns channel_not_found."
  ]
}
```

## Critical Behaviors

- **Skills are read-only** — no install, enable, or configure. They arrive inside search response.
- **No list API** — skills come via runtime search only. No cURL equivalent.
- **Search matches on use case, not tool name** — "Post message to Reddit subreddit" matches; "reddit tools" does not.
- **Skills ride inside search response** — no separate contract. Part of search results by default, no opt-out.
- **Derived from real usage** — Composio derives skills from actual platform usage, not hand-written.
- **Cross-app skills** — a task may span Slack + Gmail; skill covering several toolkits appears under each.

## What a Skill Contains

| Field | Description |
|-------|-------------|
| Use case | Task in plain language (what search matches against) |
| Tools | Tool slugs — primary vs supporting |
| Execution plan | Ordered steps, optional fallback paths |
| Pitfalls | Known failure modes |

## Integration Note for social-mcp Gateway

Our gateway currently calls Composio tools **directly by slug** (e.g., `REDDIT_CREATE_REDDIT_POST`). We do not yet use the `COMPOSIO_SEARCH_TOOLS` meta-tool. 

**Future enhancement**: Add search-first layer to gateway — when agent has a task, search first, get playbook + pitfalls, then execute. This would reduce retry/error by front-loading known failure modes.

## Relevance to arifOS

Composio's skill model is complementary to our AAA skill library:
- **Composio Skills** = execution playbooks for external tool chains (Slack, Gmail, Reddit workflows)
- **AAA Skills** = governance + constitutional procedures (F1-F13, evidence discipline, ART cycles)

They operate at different layers. Composio skills help our agent execute external operations correctly the first time. AAA skills govern when and how the agent is allowed to act.
