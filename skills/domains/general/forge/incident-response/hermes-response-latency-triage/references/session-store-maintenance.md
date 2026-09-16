# Hermes Session Store — measuring and compacting `state.db`

Depth for Step 3 of the triage. The store is the agent's conversation history: **back it up before any write**, and treat deletion or rotation as a sovereign decision.

## Where it lives

- DB: `/root/.hermes/state.db` (SQLite). Tables: `sessions`, `messages`, plus FTS search indexes (`messages_fts*`, `messages_fts_trigram*`).
- `compression_locks` and `async_delegations` also exist — there IS a compaction path; check it before assuming the store is unmanaged.
- `sessions.db` in the same directory can be a 0-byte decoy. `state.db` is the real store.

## Measure first

```bash
hermes sessions stats      # total sessions / messages, per-source split, DB size
du -h /root/.hermes/state.db
```

Finding the sessions that actually hurt — a single multi-thousand-message session, not the store total:

```bash
sqlite3 /root/.hermes/state.db \
  "SELECT session_id, COUNT(*) c FROM messages GROUP BY session_id ORDER BY c DESC LIMIT 10;"
sqlite3 /root/.hermes/state.db "SELECT COUNT(*) FROM messages;"
sqlite3 /root/.hermes/state.db "PRAGMA page_count; PRAGMA page_size; PRAGMA freelist_count;"
sqlite3 /root/.hermes/state.db "PRAGMA quick_check;"     # expect 'ok' — cheap, run it before blaming the DB
```

Read the page math before promising anything: `freelist_count` near zero means the file size is **real content**, not deletable bloat, so VACUUM will reclaim almost nothing.

## Compact (safe, no data change)

```bash
cp -a /root/.hermes/state.db /root/.hermes/state.db.bak-<reason>
hermes sessions optimize                     # merge FTS5 segments + VACUUM
echo y | hermes sessions optimize-storage    # search index -> compact layout; asks y/N, so pipe the y
```

Expectations, so the result is reported honestly:

- `optimize` merges indexes only. On a store whose size is genuine content it reclaims a trivial amount (single-digit MB on a few-hundred-MB DB). That is a **confirmation the data is real**, not a failed fix.
- `optimize-storage` rebuilds the search index and reclaims materially more (on the order of 15–20% of the file) and takes longer — it prints per-row progress. Give it minutes and a generous timeout.
- Neither changes data. Neither fixes an oversized **context**: they make lookups cheaper. Session bloat is cured by rotation, not by VACUUM.

## Subcommands worth knowing

`hermes sessions {list,export,delete,prune,archive,optimize,optimize-storage,repair,repair-routing,recover,stats,rename,pin,unpin,pinned,browse,import}`

- `archive` is soft-hide (no deletion). `prune` and `delete` are destructive.
- `repair-routing` re-stamps gateway sessions that lost routing identity.
- `recover` rebuilds canonical data into a **separate** DB — the non-destructive escape hatch if `state.db` is ever suspected corrupt.
- `pin` exempts a session from auto-archive; check `pinned` before proposing anything that would touch an important conversation.

## Pitfalls

- Never run a destructive subcommand just to make a number smaller. Store size is almost never the user's actual problem; per-turn context is.
- Do not read a large DB as corruption. `PRAGMA quick_check` is one command — run it instead of speculating.
- A hard `MemoryMax` on the gateway unit combined with a large store can make the process look like the culprit when the store is only a symptom.
- Rotating the session that holds the user's main conversation loses in-session continuity even though memory and persona persist — always offer it as a choice with the trade-off stated.
