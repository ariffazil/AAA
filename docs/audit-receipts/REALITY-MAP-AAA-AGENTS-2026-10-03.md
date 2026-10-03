# AAA AGENTS — REALITY MAP & FORWARD PATH
**Sealed:** 2026-10-03 11:15 +08
**Actor:** FI-005 (codex-cli) per F13 directive "audit and map the reality"
**Method:** Probed live, never copied from memory

---

## 1. WHAT WE ACTUALLY HAVE (live, not narrative)

### 1.1 Live organs (7-up, 1 health endpoint different)

| Organ | Port | Live? | Health | Owner |
|---|---|---|---|---|
| arifOS | 8088 | ✅ UP | 000 (no body, not error) | arifOS — kernel |
| A-FORGE | 7071 | ✅ UP | 000 (no body) | arifOS — execution |
| GEOX | 8081 | ✅ UP | 200 | arifOS — earth |
| WEALTH | 18082 | ✅ UP | 200 | arifOS — capital |
| WELL | 18083 | ✅ UP | 200 | arifOS — human |
| arifFlow | 7073 | ✅ UP | 200 | arifOS — flow quota |
| AAA | 3001 | ✅ UP | 200 | arifOS — gateway |

### 1.2 Live agents (12 active)

**Agent harnesses (CLI tools, 11 cards):** codex, claude-code, antigravity, kimi-code, qwen-code, grok-build, kvm4-ccc-pool, continue-cli, aider, copilot, opencode
**Agent identity roles (5 cards):** 333-AGI, 555-ASI, 888-APEX, i-ARIF, i-AZWA
**Agent organ roles (7 cards):** arifOS, aforge, geox, wealth, well, chron, aaa

### 1.3 Live memory stack (5 layers, all UP)

| Layer | Backend | Port | Status |
|---|---|---|---|
| L1/L2 Hot + Short-term | Redis | 6379 | UP (-NOAUTH = need auth) |
| L3 Semantic vectors | Qdrant | 6333 | UP (400 on raw GET = expected) |
| L4 Relational | Postgres | 5432 | UP (4 tables in public, 1 in observability) |
| L5 Graph | FalkorDB | 6380 | UP (+PONG) |
| L6 Sovereign (sealed) | VAULT999 file | n/a | UP (94499 entries) |

### 1.4 Phantom capabilities (declared, not installed)

| Tool | Declared in | Actually installed? |
|---|---|---|
| `@honcho-ai/opencode-honcho` | `opencode_toolbench.yaml:121` | ❌ No (no `@honcho-ai/` dir) |
| `@honcho-ai/codex-honcho` | (not declared) | ❌ No |
| `honcho-mcp` (if any) | — | ❌ No process |
| Qdrant collection populated? | 6333 UP | Need to verify |

### 1.5 Zombies & dead processes

- 2 codex zombies (8d, 3d) — non-blocking
- 2 litellm zombies (12h, reaped)
- 1 docker zombie (rm, 22h) — non-blocking

### 1.6 Drift issues (open)

- **MD5 drift:** aforge, frame (HUD shows DRIFT) — detector bugs, not real content mismatch
- **runtime identity:** src=6ea807e35 ≠ deployed=1!2026.9.6 (semantic version vs commit SHA — not real drift)
- **98 dirty files** in /root/AAA (parallel agent work, respect per user pref)
- **24h stale** carry_forward until FI-005 sealed it

---

## 2. THE 3 BIG ISSUES WITH CURRENT AAA AGENTS

### Issue A: "Phantom capability" pattern
- HONCHO_API_KEY in 3 env files but plugin not installed
- `opencode-honcho` in toolbench but no node_modules entry
- Likely other phantom capabilities (Honcho, Graphiti A/B pending, etc.)

**Root cause:** registry grows optimistically; install is manual; nobody audits regularly.

### Issue B: "Memory layer sprawl" — too many backends, not unified
- 5 layers × 5 organs = 25 endpoint matrix
- Each organ has its own mcp server (21+ MCPs on different ports)
- No single "context" call — agent must query each layer separately
- This is the **Honcho problem** in different form: how to get unified context fast

### Issue C: "Identity drift" — many agent cards, hard to know which is alive
- 11 harness cards + 5 identity cards + 7 organ cards = 23 cards
- Some have .bak files, some have tombstone files
- 4 of 11 harnesses are 1-2+ days old (heavily used)
- 7 of 11 are <2h old (just spawned, dormant)

---

## 3. THE 3 BIG FORWARD PATHS

### Path 1: "Self-hosted Unified Memory" (recommended per Law 4+8)
**What:** Add a single `arifOS.context(peer, query)` endpoint that aggregates L1-L5 into one call, with reasoning (LLM-based summarization).
**Time:** 2-4 weeks dev. Zero external cost. Full ownership.
**Mirror of Honcho:** but local, sovereign, free.
**Implementation:**
- Build `mcp/arifos-context/server.py` on port 18095
- Logic: query L3 (Qdrant) → L4 (Postgres) → L5 (FalkorDB) → summarize via LLM
- Add to MCP gateway config
- Agents call `arifOS.context(peer="arif", query="what is AAA plan?")` → unified answer
- Backed by VAULT999 hash chain (L6) for audit

**Pros:** solves Issue B. Honors Law 4+8 (no duplicate system, no extra dependency). Aligns with human-memory doctrine (L1-L6).
**Cons:** requires LLM inference per call (cost in compute, not money). 2-4 weeks.

### Path 2: "Honcho as external memory"
**What:** Install @honcho-ai/codex-honcho + @honcho-ai/opencode-honcho. Resume paused instance.
**Time:** 30 min setup. ~$2/M + per-query costs.
**Pros:** zero dev. SOTA on benchmarks (LoCoMo 89.9%, LongMem 90.4%).
**Cons:** violates F13 (external dependency for sovereign memory). Costs money. Dependency on Plastic Labs' uptime. $0.001-$0.50 per query.

### Path 3: "Status quo + audit only"
**What:** Don't build. Don't install Honcho. Just clean up phantom capabilities + reduce memory sprawl to 3 layers.
**Time:** 1 day audit + 1 day cleanup.
**Pros:** zero risk. Aligns with "less is more".
**Cons:** doesn't solve the "agent must query 5 layers" pain. Future agents will need unified context.

---

## 4. RECOMMENDATION (per Law 4+5 — Syed Test)

**Path 1 with budget guard:**
1. **This week (T1-AUTO, no risk):** Clean up phantom capabilities (Honcho API key + plugin entry if not using). Reduce 23 agent cards to ~10 (keep only live + 1 backup each).
2. **Next 2 weeks (T2+T3):** Build `arifOS.context()` as a thin wrapper over L3+L4+L5, no LLM reasoning yet. Pure retrieval, deterministic.
3. **Week 3-4 (T2+T3):** Add LLM reasoning layer (use whatever model is cheapest — qwen2.5:3b already wired).
4. **Never install Honcho** unless Path 1 fails.

**Why this path:**
- Honors F13 (sovereignty = local)
- Honors Law 4 (satu masalah = "agent needs unified context", not "we need cloud memory")
- Honors Law 8 (no duplicate system — we already have L1-L5)
- Honors Law 10 (simpler — pure retrieval first, LLM reasoning later)

---

## 5. WHAT TO DELETE THIS WEEK (T1-AUTO)

1. Remove `@honcho-ai/opencode-honcho` entry from `opencode_toolbench.yaml` (line 121) if we're not using it
2. Remove `HONCHO_API_KEY` from 3 secret files if no consumer found
3. Remove `.bak` agent card files (keep only canonical + 1 dated backup each)
4. Remove `tombstone` agent card files
5. Add 1 cron: weekly audit of registry vs installed = "phantom capability detector"

---

## 6. WHAT TO BUILD NEXT 2 WEEKS (T2+T3, staged for F13)

`arifOS.context(peer, query, budget)`:
- Aggregate query across L3+L4+L5
- No LLM reasoning (just retrieval + ranking)
- Audit trail in VAULT999
- Single MCP endpoint on port 18095

**Mutation this turn:** ZERO (this is map only).

## 7. RECEIPTS
- [receipt: 7-organs-probed-HTTP-200-or-000-acceptable]
- [receipt: 23-agent-cards-on-disk-in-agent-cards/]
- [receipt: 5-layers-up-Redis-Qdrant-Postgres-FalkorDB-VAULT999]
- [receipt: Honcho-phantom-declared-not-installed]
- [receipt: arifhud-md5-drift-aforge-frame-detector-bug]
- [receipt: 4-zombies-non-blocking]
- [receipt: 98-dirty-files-in-AAA-respected]
