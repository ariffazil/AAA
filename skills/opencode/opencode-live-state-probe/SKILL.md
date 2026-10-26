---
name: opencode-live-state-probe
description: "Use when probing OpenCode session status or live state."
version: 1.0.0
risk_tier: low
autonomy_tier: T1
owner: AAA
tags: [opencode, status, probe, sqlite, git, session]
---

# OpenCode Live State Probe

Report OpenCode's real state by reconciling several live artifacts — never trust a session title or a single stale file.

## Procedure

1. **SQLite session DB** (authoritative) — `/root/.local/share/opencode/opencode.db`, read-only via `sqlite3` (can exceed 1GB; never load whole).
   - Tables: `session` (legacy) and `session_v2` (current) — query both. `session_inbox` (queued, undelivered messages) and `session_pending` (normally 0).
   - Timestamps are **ms since epoch**: `datetime(col/1000,'unixepoch','+8 hours')` → MYT.
   - `SELECT ... FROM session_v2 WHERE time_archived IS NULL ORDER BY time_updated DESC LIMIT 25;`
2. **agent_state JSON** — `/root/.config/opencode/agent_state/<agent>.json`: read `open_loops_888_HOLD[]`, `f2_receipts[]`, `session_count`, `updated_at` (stale if old).
3. **Live log** — `/root/.local/share/opencode/log/opencode.log`: grep `spawning process` (exact shell commands being run) and `mcp transport error` / `ConnectionRefused` (dead MCP servers).
4. **Running processes** — `ps aux | grep -i opencode`: expect BOTH a `serve` daemon (backend) AND a tty session (`pts/N`) — different things.
5. **Git work state** — inside the repo it works in: `.git/rebase-merge` / `.git/rebase-apply` dirs = mid-rebase hang; `git rev-list --left-right --count HEAD...origin/main` (`0 0` = aligned); `git status --short`; `git stash list`.

## Pitfalls

- Session `title` is auto-generated and often starts with `<think>` garbage — it is NOT a status. Read `time_updated`, log `spawning process` lines, and `git status` for the truth.
- Newer OpenCode writes `session_v2`; query both tables when a session appears missing.
- A large `opencode.db` + WAL means a busy live agent — keep queries read-only and short-`LIMIT`.
- A git rebase that "finished" can still leave uncommitted dirty files and parked stashes — report those separately from the rebase result.

DITEMPA BUKAN DIBERI ⚒️
