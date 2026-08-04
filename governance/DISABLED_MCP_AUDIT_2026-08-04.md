# Disabled MCP Audit — 2026-08-04

> **STATUS:** SEAL
> **DATE:** 2026-08-04
> **DOCTRINE:** Separation of Powers in Agent Tool Use
> **METHODOLOGY:** Source-level audit of all 6 disabled MCP servers in opencode.json
> **DITEMPA BUKAN DIBERI**

---

## 0. Constitutional Principle

```
Disabled ≠ broken
Disabled = unratified capability surface
```

No disabled server is activated without constitutional classification.
Every server maps to the Five Powers before enablement.

---

## 1. Classification Framework

### Verdict Types

| Verdict | Meaning | Action |
|---------|---------|--------|
| `SEAL_READONLY` | Read-only, safe to enable | Enable with no restrictions |
| `SEAL_GOVERNED` | Useful but write-capable | Enable read-only subset only |
| `HOLD` | Dangerous without scope boundaries | Keep disabled until governance |
| `VOID` | Fundamentally incompatible with separation of powers | Never enable in current form |
| `CLEANUP` | No longer needed | Remove from config |

### Power Mapping

Each server's tools map to the Five Powers:

| Power | Relevant Tools |
|-------|---------------|
| **Proposal** | Tools that identify gaps or suggest actions |
| **Verification** | Tools that search, inspect, or analyze |
| **Judgment** | Tools that decide or authorize |
| **Execution** | Tools that mutate state, create/destroy data |
| **Witnessing** | Tools that log, record, or audit |

---

## 2. Per-Server Audit

### 2.1 capability-index

```
Source:   /root/arifOS/core/capability_index/mcp_server.py
Status:   Not running (venv exists)
Tools:    2 (capability_search, capability_select)
R/W:      READ-ONLY
State:    NO persistent state
Risk:     LOW
```

**Tools:**

| Tool | Write? | Power |
|------|--------|-------|
| `capability_search` | No | Verification |
| `capability_select` | No | Verification |

**Constitutional notes:**
- Pure query service over 97-tool index
- Has built-in risk-tier filter that blocks HYPOTHESIS-tier tools at low risk
- No mutations, no persistence, no side effects
- **Already has separation-of-powers awareness** via risk-tier gating

```
VERDICT: SEAL_READONLY
REASON: Pure read-only. Safe to enable for all agents.
POWER: Verification only.
```

---

### 2.2 repomapper

```
Source:   /root/arifos/agents/forge/RepoMapper/repomap_server.py
Status:   Not running (venv at /root/venvs/repomapper/)
Tools:    2 (repo_map, search_identifiers)
R/W:      READ-ONLY by design
State:    NO persistent state (in-memory cache only)
Risk:     LOW
```

**Tools:**

| Tool | Write? | Power |
|------|--------|-------|
| `repo_map` | No | Verification |
| `search_identifiers` | No | Verification |

**Constitutional notes:**
- tree-sitter + PageRank analysis — pure code intelligence
- Launcher explicitly states: "Read-only by design"
- `force_refresh` only invalidates in-memory cache, no disk writes
- Produces text output only

```
VERDICT: SEAL_READONLY
REASON: Pure read-only. Safe to enable for all agents.
POWER: Verification only.
```

---

### 2.3 sqlite

```
Source:   /usr/bin/mcp-server-sqlite (binary v1.0.0)
Status:   Not running
DB:       /root/.local/share/arifos/local.db (exists, EMPTY — 0 bytes)
Tools:    10
R/W:      WRITE-CAPABLE (7/10 tools mutate)
State:    YES — persistent SQLite database
Risk:     MEDIUM
```

**Tools:**

| Tool | Write? | Power | Risk |
|------|--------|-------|------|
| `query` | No | Verification | Low |
| `describe-table` | No | Verification | Low |
| `list-tables` | No | Verification | Low |
| `execute` | **YES** | Execution | **High** — arbitrary SQL |
| `create-table` | **YES** | Execution | Medium |
| `drop-table` | **YES** | Execution | **High** — F1-class |
| `insert-record` | **YES** | Execution | Medium |
| `update-record` | **YES** | Execution | Medium |
| `delete-record` | **YES** | Execution | Medium |
| `transaction` | **YES** | Execution | **High** — multi-statement |

**Constitutional notes:**
- DB is empty — no damage done yet
- `execute` allows arbitrary INSERT/UPDATE/DELETE/CREATE/DROP
- `drop-table` is F1-class irreversible within the database
- `transaction` wraps multiple mutations in atomic operations
- No separation-of-powers gating — any agent with access can execute any tool

```
VERDICT: HOLD
REASON: 7/10 tools mutate. No scope boundaries. Requires either:
  (a) Restrict to read-only tools (query, describe-table, list-tables)
  (b) Enable with 888 judgment gate on write tools
  (c) Scope to specific tables with allowlist
POWER: Verification (read tools) / Execution (write tools — needs governance)
```

---

### 2.4 graphiti

```
Source:   Docker — zepai/knowledge-graph-mcp:latest
Status:   RUNNING (healthy)
Backend:  FalkorDB via Redis (falkordb:6379, db: arifos)
LLM:      Ollama (host.docker.internal:11434) for entity extraction
Tools:    9
R/W:      WRITE-CAPABLE (4/9 tools)
State:    YES — persistent knowledge graph in FalkorDB
Risk:     HIGH
```

**Tools:**

| Tool | Write? | Power | Risk |
|------|--------|-------|------|
| `search_nodes` | No | Verification | Low |
| `search_memory_facts` | No | Verification | Low |
| `get_entity_edge` | No | Verification | Low |
| `get_episodes` | No | Verification | Low |
| `get_status` | No | Verification | Low |
| `add_memory` | **YES** | Execution | **High** — graph mutation, async |
| `delete_entity_edge` | **YES** | Execution | **High** — irreversible |
| `delete_episode` | **YES** | Execution | **High** — irreversible |
| `clear_graph` | **YES** | Execution | **CRITICAL** — nukes all data |

**Constitutional notes:**
- `clear_graph` can destroy all knowledge graph data for any group_id
- `add_memory` creates knowledge graph entries that influence future agent reasoning
- No tool annotations set (all empty `{}`) — no readOnlyHint/destructiveHint
- Entity extraction via Ollama means content is processed by an external LLM
- `group_id` parameter lets it target `af_forge` or any other group
- **Memory authority risk:** False memories injected here propagate to all agents querying the graph

```
VERDICT: HOLD
REASON: clear_graph is F1-class catastrophic. add_memory is F2-class (false memory injection).
  Requires: (a) Expose read-only subset only (5 search/get tools)
  (b) Gate add_memory behind 888 judgment
  (c) Never expose clear_graph to agents
POWER: Verification (read tools) / Execution (write tools — needs governance)
```

---

### 2.5 hindsight

```
Source:   Docker — ghcr.io/vectorize-io/hindsight:latest (v0.8.6)
Status:   RUNNING (healthy, database connected)
Backend:  PostgreSQL with pgvector (via .pg0)
LLM:      Aliyun MaaS API
Tools:    32
R/W:      HEAVILY WRITE-CAPABLE (17/32 tools)
State:    YES — persistent memory banks in PostgreSQL
Risk:     HIGH
```

**Write tools (17):**

| Tool | Write? | Destructive? | Power | Risk |
|------|--------|-------------|-------|------|
| `retain` | YES | No | Execution | **High** — persistent memory |
| `sync_retain` | YES | No | Execution | **High** — sync version |
| `create_bank` | YES | No | Execution | Medium |
| `update_bank` | YES | No | Execution | Medium |
| `create_mental_model` | YES | No | Execution | Medium |
| `update_mental_model` | YES | No | Execution | Medium |
| `refresh_mental_model` | YES | No | Execution | Medium |
| `create_directive` | YES | No | Execution | **High** — influences LLM reasoning |
| `update_memory` | YES | No | Execution | Medium |
| `cancel_operation` | YES | No | Execution | Low |
| `delete_mental_model` | YES | **YES** | Execution | High |
| `clear_mental_model` | YES | **YES** | Execution | High |
| `delete_directive` | YES | **YES** | Execution | High |
| `invalidate_memory` | YES | **YES** | Execution | High |
| `delete_document` | YES | **YES** | Execution | High |
| `clear_memories` | YES | **YES** | Execution | **Critical** |
| `delete_bank` | YES | **YES** | Execution | **CRITICAL** — destroys all data |

**Read tools (15):** recall, reflect, list_*, get_*

**Constitutional notes:**
- `retain`/`sync_retain` create persistent memories that influence all future interactions
- `create_directive` can inject instructions that alter future LLM reasoning — **F12 injection risk**
- `delete_bank` destroys entire memory banks — F1-class catastrophic
- `clear_memories` destroys all memories in a bank — F1-class catastrophic
- Properly annotated (destructiveHint: true on destructive tools) — better than graphiti
- **Narrative authority risk:** This service shapes what agents "remember" and "believe"

```
VERDICT: HOLD
REASON: 17/32 tools mutate. create_directive = F12 injection risk.
  delete_bank/clear_memories = F1-class catastrophic.
  Requires: (a) Expose read-only subset only (recall, reflect, list_*, get_*)
  (b) Gate retain behind 555 verification + 888 judgment
  (c) Never expose delete_bank, clear_memories to agents
  (d) create_directive requires SOVEREIGN-level authorization
POWER: Verification (read tools) / Execution (write tools — needs governance)
```

---

### 2.6 serena

```
Source:   uvx --from serena-agent serena start-mcp-server --mode no-memories
Package:  serena-agent v1.5.3 (uvx cache)
Status:   Not running
Mode:     --mode no-memories (excludes 7 memory tools)
Tools:    ~33 total (~15 read, ~18 write)
R/W:      WRITE-CAPABLE (even with no-memories)
State:    YES — can create/modify/delete files, execute shell
Risk:     CRITICAL
```

**Critical write tools (still loaded with --mode no-memories):**

| Tool | Write? | Power | Risk |
|------|--------|-------|------|
| `create_text_file` | **YES** | Execution | **Critical** — arbitrary file creation |
| `replace_content` | **YES** | Execution | **Critical** — regex replacement in files |
| `replace_in_files` | **YES** | Execution | **Critical** — bulk replacement across files |
| `replace_symbol_body` | **YES** | Execution | High — code mutation |
| `insert_after_symbol` | **YES** | Execution | High — code injection |
| `insert_before_symbol` | **YES** | Execution | High — code injection |
| `rename_symbol` | **YES** | Execution | High |
| `safe_delete_symbol` | **YES** | Execution | High |
| `execute_shell_command` | **YES** | Execution | **CRITICAL** — unrestricted shell |

**Read tools (~15):** get_symbols_overview, find_symbol, find_referencing_symbols, find_implementations, find_declaration, get_diagnostics_*, read_file, list_dir, find_file, search_for_pattern, query_project, get_current_config, serena_info

**no-memories mode excludes (7):** write_memory, read_memory, delete_memory, edit_memory, rename_memory, list_memories, onboarding

**Constitutional notes:**
- `execute_shell_command` bypasses ALL MCP-level controls — it is essentially an unrestricted shell
- `replace_in_files` can modify any file in the repository
- `create_text_file` can create arbitrary files anywhere
- The defense is purely policy-based (888_JUDGE catches violations), not tool-level
- This is **the only server where the defense against dangerous tools is a policy comment**, not a technical restriction
- Launcher comment says: "Write tools are still loaded by Serena by default but the repo-eureka policy forbids invoking them" — **policy, not architecture**

```
VERDICT: VOID (in current form)
REASON: execute_shell_command + file mutation tools = separation-of-powers collapse.
  Any agent with serena access can execute arbitrary code without A-FORGE.
  Policy-based defense is insufficient for tools this dangerous.
  Requires: (a) Configure excluded_tools to block all write tools
  (b) OR use fixed_tools to restrict to read-only subset
  (c) OR keep disabled permanently
POWER: Verification (read tools) / Execution (write tools — CONSTITUTIONAL HAZARD)
```

---

## 3. Summary Matrix

| Server | Tools | R/W | Persistent State | Verdict | Priority |
|--------|-------|-----|-----------------|---------|----------|
| **capability-index** | 2 | Read-only | No | `SEAL_READONLY` | Enable now |
| **repomapper** | 2 | Read-only | No | `SEAL_READONLY` | Enable now |
| **sqlite** | 10 | 7 write | Yes (local.db) | `HOLD` | Scope write tools |
| **graphiti** | 9 | 4 write | Yes (FalkorDB) | `HOLD` | Expose read-only |
| **hindsight** | 32 | 17 write | Yes (PostgreSQL) | `HOLD` | Expose read-only |
| **serena** | ~33 | 18 write+shell | Yes (files) | `VOID` | Keep disabled or harden |

---

## 4. Recommended Actions

### Immediate — Enable (TIER 1)

```
1. Enable capability-index
   Reason: Pure read-only tool discovery. Benefits all agents.
   Power: Verification only.

2. Enable repomapper
   Reason: Pure read-only code intelligence. Benefits all agents.
   Power: Verification only.
```

### Near-term — Enable Read-Only Subset (TIER 2)

```
3. Graphiti — expose 5 read-only tools
   Enable: search_nodes, search_memory_facts, get_entity_edge, get_episodes, get_status
   Block: add_memory, delete_entity_edge, delete_episode, clear_graph
   Gate: add_memory requires 555 verification + 888 SEAL

4. Hindsight — expose 15 read-only tools
   Enable: recall, reflect, list_*, get_*
   Block: retain, sync_retain, create_*, delete_*, clear_*, invalidate_*, update_*, cancel_*
   Gate: retain requires 555 verification + 888 SEAL
   Gate: create_directive requires SOVEREIGN authorization

5. SQLite — expose 3 read-only tools
   Enable: query, describe-table, list-tables
   Block: execute, create-table, drop-table, insert-record, update-record, delete-record, transaction
   Gate: write tools require 888 SEAL
```

### Hold — Keep Disabled (TIER 3)

```
6. Serena — keep disabled
   Reason: execute_shell_command + file mutation = separation-of-powers collapse
   Escape hatch: Configure excluded_tools to block:
     execute_shell_command, create_text_file, replace_content,
     replace_in_files, replace_symbol_body, insert_after_symbol,
     insert_before_symbol, rename_symbol, safe_delete_symbol
   If hardened: enable with read-only subset only
```

---

## 5. Disabled MCP Doctrine

```text
DISABLED_MCP_DOCTRINE::v0.1

1. Disabled ≠ broken.
2. Disabled = unratified capability surface.
3. No disabled server is activated without constitutional classification.
4. Read-only servers may be enabled under least-privilege.
5. Write-capable servers require explicit scope boundaries.
6. Memory authority servers require provenance policy.
7. Mutation servers require 888 judgment and receipt requirements.
8. Shell execution tools are ALWAYS Tier 3 — never enabled without SOVEREIGN.
```

---

## 6. Separation of Powers Mapping

Each enabled server should expose tools matching exactly one power:

```
capability-index  → Verification (tool discovery, risk filtering)
repomapper        → Verification (code analysis, repo mapping)
graphiti (read)   → Verification (knowledge graph search)
hindsight (read)  → Verification (memory recall, reflection)
sqlite (read)     → Verification (data query)

graphiti (write)  → Execution (requires 888 SEAL)
hindsight (write) → Execution (requires 888 SEAL)
sqlite (write)    → Execution (requires 888 SEAL)
serena (write)    → Execution (VOID — violates separation of powers)
```

**No server may serve both Verification and Execution simultaneously
without explicit governance gating on the Execution tools.**

---

*Forged 2026-08-04. Source-level audit of 6 disabled MCP servers.
Cross-referenced against AAA_TOOL_RIGHTS_POLICY_v0.2 and SEPARATION_OF_POWERS_TOOL_USE.md.*
*DITEMPA BUKAN DIBERI ⚒️*
