# State-Store Queries (behavioural record, read-only)

Probes for what the harness actually did — separate from storage size and surface inventory. Read-only
throughout; open stores immutable so a live gateway keeps its write lock.

```python
import sqlite3
con = sqlite3.connect("file:/root/.hermes/state.db?mode=ro", uri=True)
cur = con.cursor()
```

## Tool-call frequency — the exact table

```sql
SELECT tool_name, COUNT(*) FROM messages
WHERE tool_name IS NOT NULL AND tool_name != ''
GROUP BY 1 ORDER BY 2 DESC LIMIT 30;
```

`tool_name` is populated on tool messages. Do not regex `content` for `"name":` — that over-counts
repeated mentions and skips calls whose payload was compacted away.

## Session timeline — the epoch trap

`sessions.started_at` is a UNIX epoch **string**, not ISO-8601. `substr(started_at,1,10)` returns epoch
digits and silently yields a garbage date axis.

```python
import datetime, collections
days = collections.Counter()
for (sid,) in cur.execute("SELECT started_at FROM sessions"):
    try:
        days[datetime.datetime.fromtimestamp(float(sid), datetime.UTC).strftime("%Y-%m-%d")] += 1
    except (ValueError, TypeError):
        continue      # some rows carry ISO-8601; skip, do not crash the scan
```

`sessions.source` splits telegram / cron / subagent / cli — the channel mix matters more than the total.
`sessions.tool_call_count` ranks the heaviest working sessions, and `session_model_usage` shows which
models carried load versus which are merely configured.

## Delegation history without flooding the context

`async_delegations.event_json` and `result_json` hold whole subagent transcripts. Never `SELECT *`.

```sql
SELECT state, delivery_state, COUNT(*) FROM async_delegations GROUP BY 1,2;
```

Pull `result_json` for at most one delegation, and only when its content is the evidence under audit.

## Scheduler: enabled is not firing

```python
import json
jobs = json.load(open("/root/.hermes/cron/jobs.json"))["jobs"]
enabled = {j["id"]: j for j in jobs if j.get("enabled")}
```

```sql
SELECT job_id, COUNT(*), MAX(finished_at) FROM executions GROUP BY job_id;
```

A job with `enabled: true`, a stale `last_run_at` and no execution rows is dark. `last_status` is written
on completion, so a job that stopped firing keeps its last `ok` forever — never use status alone as
liveness. Disabled jobs carry `state` + `paused_reason`: `migrated` / `migrated-system-cron` means
deliberately moved off this host (not a defect); a bare `paused` with an empty reason is a deliberate
stop. Cross-substrate procedure: `federation-scheduler-audit`.

## Delivery: what actually reached a human

```sql
SELECT state, COUNT(*) FROM delivery_obligations GROUP BY 1;
SELECT chat_id, COUNT(*) FROM delivery_obligations
WHERE state != 'delivered' GROUP BY 1 ORDER BY 2 DESC;
```

Group by destination before drawing any conclusion. A blocked bot-to-bot DM channel can hold every
failure while human delivery is 100%. Read a sample of `last_error` before theorising about cause.

## Surface state — declared vs reachable

`MCP_HEALTH.json` is generated from config plus a live probe and carries `counts` plus per-server
`status` / `routable`. Read it instead of re-deriving. `stdio_present` with `routable: false` means the
server exists on disk but is not attached to the session's MCP surface — a different fact from "down".

For a raw check, read the code before calling anything down:

| Result | Meaning |
|---|---|
| connection refused / timeout | down |
| `400` / `406` | reachable; the probe's shape is wrong (e.g. GET on an MCP path) |
| `401` / `403` | up, auth-gated |
| `200` | up |

Only the first is evidence of absence. A service can be healthy while its MCP route is detached — state
which layer you tested.

## Dead governance gates and dangling pointers

```bash
ls /root/.hermes/hooks/<name>/
```

Only `*.bak` / `*.phase1.bak` present → the hook is retired while still listed as configured. The same
shape appears for an unwired plugin: present in `plugins/`, absent from the enabled list in `config.yaml`.

```python
import os
for p in ("/root/.hermes/carry_forward.json", "/root/.hermes/SOUL.md"):
    print(p, os.readlink(p) if os.path.islink(p) else "regular file", os.path.exists(p))
```

A continuity pointer that resolves nowhere is a broken handoff, not cosmetics — it needs its own line in
the report rather than being folded into a general "all healthy".

## Skill-library census

```bash
find /root/AAA/skills      -name 'SKILL.md' | wc -l
find /root/.hermes/skills  -name 'SKILL.md' | wc -l
```

Count each root separately and state which root you counted — the roots overlap (symlinked homes, flat
layout vs `domains/` layout) and a single total is meaningless without its root named. Content-hash the
`SKILL.md` set to find true duplicates rather than trusting filenames.
