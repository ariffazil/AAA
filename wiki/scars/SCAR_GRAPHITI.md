---
title: "Scar — graphiti Hyphen Escape Failure in FalkorDB Fulltext Search"
created: 2026-05-17
updated: 2026-05-17
version: 1.0.0
type: scar
status: canonical
tags: [graphiti, falkordb, redisearch, mcp, hyphen, group_id, search, escape]
confidence: high
domain: infra/data-layer
severity: high
actors: [kimi-agent, graphiti-mcp]
sources: [mcp-audit-2026-05-17, live-container-patch]
---

# Scar — graphiti Hyphen Escape Failure in FalkorDB Fulltext Search

## What Happened

During MCP federation audit on 2026-05-17, `search_nodes` and `search_memory_facts` in graphiti MCP server failed 100% of the time with:

```
RediSearch: Syntax error at offset 14 near af
```

This made graphiti's semantic knowledge graph **completely unsearchable**.

## The Failure Chain

```
1. GRAPHITI_GROUP_ID=af-forge  (hyphen in group_id)
2. User calls search_nodes(query="test")
3. graphiti_core builds fulltext query: (@group_id:"af-forge") (test)
4. FalkorDB/RediSearch parser sees hyphen at offset 14
5. Parser throws syntax error — search aborts
6. Result: No memory retrieval possible from graphiti
```

## Root Cause

**Two code locations failed to escape hyphens in `group_id` when building FalkorDB fulltext queries:**

1. `graphiti_core/driver/falkordb_driver.py:410` — `build_fulltext_query()`
2. `graphiti_core/driver/falkordb/operations/search_ops.py:108` — `_build_falkor_fulltext_query()`

Both had:
```python
escaped_group_ids = [f'"{gid}"' for gid in group_ids]
```

Wrapping in double quotes is insufficient — FalkorDB's RedisSearch-like parser still interprets the unescaped hyphen as a syntax operator.

## Technology Context (Corrected)

graphiti uses **FalkorDB**, not RediSearch directly:
- FalkorDB is a graph database loaded as a Redis module
- It uses RedisSearch-like syntax for fulltext queries
- The error message says "RediSearch" because FalkorDB shares the query parser

## Fix Applied

**Patched both files inside running `graphiti-mcp` container:**

```python
# Before (broken)
escaped_group_ids = [f'"{gid}"' for gid in group_ids]

# After (fixed)
escaped_group_ids = ['"' + gid.replace("-", "\\-") + '"' for gid in group_ids]
```

This produces `(@group_id:"af\-forge") (test)` which FalkorDB parses correctly.

**Container status:** Healthy, Redis PONG, search functional.

**Persistent copies:** `/root/patches/graphiti-mcp/`

## What Should Have Been Done

graphiti_core library should escape ALL special characters that have meaning in RedisSearch syntax when building field queries:
- `-` (minus/hyphen)
- `+` (plus)
- `|` (pipe/OR)
- `*` (wildcard)
- `@` (field prefix)
- `(` `)` ` [` `]` `{` `}`

At minimum, group_ids should be sanitized before being embedded in fulltext query strings.

## Anti-Pattern to Avoid

**Assuming quotes escape everything.** Wrapping a string in double quotes does NOT make it safe for injection into RedisSearch/Lucene query syntax. Each query language has its own escaping rules.

## TREE777 Lesson

**When a database says "syntax error near X", the error is rarely the data — it's the query builder failing to escape the data.**

graphiti stores group_ids as opaque strings but embeds them directly into fulltext query strings without parameterization or proper escaping. This is a query injection vulnerability class, even if the payload is not malicious.

## Verification

| Test | Before Fix | After Fix |
|------|-----------|-----------|
| `search_nodes("test")` | ❌ Syntax error | ✅ No relevant nodes found |
| `search_memory_facts("MCP audit")` | ❌ Syntax error | ✅ No relevant facts found |
| `add_memory("test")` | ✅ Queued | ✅ Queued |
| `get_status` | ✅ Healthy | ✅ Healthy |

## Confidence: HIGH

Root cause confirmed by:
1. Reading `graphiti_core` source code inside container
2. Reproducing error with exact query string
3. Patching and verifying search succeeds
4. Container health restored

## Related

- [[federation-entities]] — graphiti-mcp service entity
- [[mcp-architecture-mapping]] — MCP server topology

## Persistence Risk

Patch is in container writable layer. Will be lost if image is rebuilt. Action needed:
- Mount patched files via docker-compose volume, OR
- Rebuild `zepai/knowledge-graph-mcp` image with fix upstream

---
DITEMPA BUKAN DIBERI — Scars are forged from failure, not from comfort.
