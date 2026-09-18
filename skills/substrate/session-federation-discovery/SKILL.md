---
name: session-federation-discovery
description: "Use when searching Hermes session history via MCP :18088."
version: 1.0.0
---

# Session Federation Discovery

Federated session access for all AAA agents. One MCP endpoint, read-only, covers the entire Hermes session store.

## When to Load

- Agent needs to recall a past conversation or decision
- Agent needs to search session history by keyword
- Agent needs session statistics or health
- Agent needs to find related sessions (lineage, siblings)
- Any question starting with "what did we say about X" or "where did we discuss Y"

## MCP Endpoint

```
http://127.0.0.1:18088/mcp
```

Service: `session-federation.service` (systemd, auto-restart)
Source: `/root/.hermes/mcp/session-federation/server.py`
DB: `/root/.hermes/state.db` (read-only)

## Available Tools (6)

| Tool | Purpose | Key Args |
|------|---------|----------|
| `session_list` | Browse recent sessions by metadata | `source`, `limit`, `model`, `title_contains` |
| `session_search` | FTS5 keyword search across all messages | `query`, `limit`, `source`, `role` |
| `session_read` | Read a session's messages | `session_id`, `limit`, `offset`, `role_filter` |
| `session_stats` | Aggregate statistics | (none) |
| `session_related` | Find related sessions by lineage/topic | `session_id`, `direction`, `limit` |
| `federation_health` | DB health check | (none) |

## Usage Patterns

### Find past discussions
```python
# Search by keyword
session_search(query="PETRONAS basin evaluation", limit=5)

# Browse recent telegram sessions
session_list(source="telegram", limit=10)

# Read a specific session
session_read(session_id="20260916_135320_bf4990ab", limit=30)
```

### Check store health
```python
federation_health()  # DB integrity, WAL state, table counts
session_stats()      # Source breakdown, model usage, costs
```

### Find session lineage
```python
session_related(session_id="20260916_135320_bf4990ab", direction="both")
```

## Pitfalls

- **Read-only**: This server never writes to state.db. Use `hermes sessions` CLI for mutations.
- **FTS5 syntax**: Search supports AND, OR, NOT, quoted phrases, prefix*. Hyphenated terms auto-quoted.
- **Profile isolation**: All profiles share one state.db on KVM8. Profile-specific DBs exist but are empty.
- **Schema v30**: Current schema. Recovery tooling regenerates FTS indexes.
- **Active rows**: Messages with `active=0` are compaction archives — search includes them but `session_read` defaults to `active=1`.

## Direct SQLite Access (fallback)

If MCP is down, read directly:
```python
import sqlite3
con = sqlite3.connect("file:/root/.hermes/state.db?mode=ro", uri=True)
```

## Service Management

Service name: `session-federation`
Config: `/root/.hermes/config.yaml` (mcp_servers.session-federation)
Logs: `journalctl -u session-federation`