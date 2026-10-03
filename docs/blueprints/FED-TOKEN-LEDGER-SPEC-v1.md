# FED Token Ledger — Spec v1 (1 page, no build)

**Status:** SPEC ONLY. F13-stage. No code yet.
**Goal:** Make token cost data actually exist so future agents can bind (per HERMES item #2).
**Why now:** `token_bank.db` files exist but all are 0 bytes. Cost is untrackable. This spec defines the missing infra so it stops being missing.

## What needs to exist (3 thin things)

1. **Write hook in litellm container** — every request logs `tokens_in, tokens_out, model, cost_usd, ts, actor_id, session_id` to SQLite at `/root/A-FORGE/data/token_bank.db`. LiteLLM has `litellm.proxy.hooks.PromptLoggingHook`; spec it to write to that path.
2. **Read API on arifOS** — one new tool `arif_cost_summary(since: str)` returns `{"total_tokens_in": N, "total_tokens_out": M, "total_cost_usd": X, "by_model": {...}, "by_day": {...}}`. Backed by `sqlite3` read on the same db file.
3. **Wire to audit log** — `arif_memory` recall handler adds `cost_usd: float` to its existing audit-log entry (one extra field, no schema change).

## Schema (token_log table)

```sql
CREATE TABLE token_log (
  id INTEGER PRIMARY KEY,
  ts TEXT NOT NULL,         -- ISO-8601 UTC
  actor_id TEXT,             -- "fi-005-eval" or "anonymous"
  session_id TEXT,
  model TEXT NOT NULL,       -- "deepseek-v3.2", "qwen-coder", "hermes-default"
  tokens_in INTEGER NOT NULL,
  tokens_out INTEGER NOT NULL,
  cost_usd REAL NOT NULL,    -- computed at write time from model rate card
  tool TEXT                  -- "arif_memory", "arif_judge", etc.
);
CREATE INDEX idx_token_log_ts ON token_log(ts);
CREATE INDEX idx_token_log_actor ON token_log(actor_id);
```

## Model rate card (where cost_usd comes from)

| model | input $/1M | output $/1M |
|---|---|---|
| deepseek-v3.2 | 0.27 | 1.10 |
| qwen-coder | 0.30 | 0.60 |
| hermes-default | 0.50 | 1.50 |
| agi-333 | 0.40 | 1.20 |
| asi-555 | 0.40 | 1.20 |
| apex-888 | 0.50 | 1.50 |
| forge-scout | 0.20 | 0.60 |
| forge-scout-pro | 0.50 | 1.50 |
| forge-builder | 1.00 | 3.00 |
| (new models added as needed) | | |

## Acceptance criteria

- After 1 day of write-hook deployment, `arif_cost_summary(since="1d")` returns non-zero
- Audit log entries show `cost_usd` field populated
- arifOS doctor.sh adds a line: `✅ FED cost ledger: <N> rows, <X.XX> USD (24h)`

## Reversibility

- All 3 components have a `--dry-run` mode
- DB file is single SQLite — `cp` to backup
- Read API has no side effects
- Total LOC estimate: ~120 (write hook 50, read API 30, audit log patch 5, tests 35)

## What this spec does NOT do (per Law 10)

- ❌ Does not write any code now
- ❌ Does not require new pip deps (sqlite3 stdlib)
- ❌ Does not change the door (arif_memory stays the single public surface)
- ❌ Does not touch Falkor
- ❌ Does not change bge-m3 (FROZEN)

## F13 ask (when ready)

Approve the 3-component build. Estimated 2-3 hours of FI-008 or similar work. Once deployed, HERMES item #2 (bind cost to session) becomes executable by future agents without re-spec.
