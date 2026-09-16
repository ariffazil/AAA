---
name: federation-scheduler-audit
description: Use when scheduled work may have stopped across hosts.
version: 1.0.0
owner: Hermes (curator-managed)
risk_tier: low
autonomy_tier: T0
floor_scope: [F1, F2, F7, F11]
tags: [cron, scheduler, federation, migration, audit, multi-host]
triggers:
  - "is cron running"
  - "did my jobs stop"
  - "scheduled work stopped"
  - "cron jobs stopped after the move"
  - "who owns the scheduled jobs"
  - "migrated cron job book"
  - "audit the schedulers"
---

# Federation Scheduler Audit

Answer "is scheduled work actually running?" from evidence across every substrate, not from one
host's local view. This skill observes and reports; it does not mutate cron.

## Why this skill exists

Scheduled work here lives in **four independent places**, and any single-host check returns a
confident wrong answer. The expensive failure is not a job that errors — an error is visible. It is
a job that **stops silently**: its host's gateway exits cleanly, no systemd unit brings it back, the
source host's job book sits parked reporting nothing wrong, and nobody notices for days.

## Step 1 — Enumerate all four substrates

Run `scripts/scheduler_substrate_sweep.py` (optional peer args: `python3
scripts/scheduler_substrate_sweep.py 100.64.0.5`). It covers all four in one pass. The underlying
commands, if you need them individually:

```bash
# 1. Hermes gateway book (this host) — read `state` + `paused_reason`, never just `enabled`
python3 -c "import json;d=json.load(open('/root/.hermes/cron/jobs.json'));\
i=d if isinstance(d,list) else d['jobs'];\
[print(x.get('enabled'), x.get('state'), str(x.get('name'))[:40], x.get('paused_reason') or '') for x in i]"
hermes cron status
# 2. peer-host books — after a migration the TARGET is often the live owner
ssh <peer> cat /root/.hermes/cron/jobs.json     # parse locally; avoids nested-quote pain
# 3. system cron — the raw entries
ls /etc/cron.d/; crontab -l
# 4. proof of life — what actually FORKED, not what is configured
journalctl -u cron --since today --no-pager | grep -oE 'CMD \([^)]*\)' | sort | uniq -c | sort -rn | head -20
```

Substrate 4 is the one that cannot lie: a configured entry with no `CMD` line in today's journal
never ran. Use it to settle any dispute about whether a job is firing.

## Step 2 — Interpret `enabled: false` by its `state`

Hermes parks a disabled job with a machine-readable reason, and three very different meanings hide
behind `enabled: false`:

| `state` | `paused_reason` | Meaning |
|---|---|---|
| `migrated` | `MIGRATED to <host> ... do not re-enable here (double-fire risk)` | Live on another host. **Never resume here.** |
| `migrated-system-cron` | `converted to /etc/cron.d/<file>` | Now a raw crontab entry. Re-enabling double-fires it. |
| `paused` | empty | A deliberate stop. Ask before touching. |

A job may be resumed on the source host only once the target provably no longer schedules it.
A `paused` job with an empty reason is not a migration — leave it and ask.

## Step 3 — Check the owner host is supervised

Moving work between hosts does not move the responsibility to notice when it stops.

- `systemctl is-enabled <unit>` on the target. `not-found` means a clean exit is permanent — the
  gateway will not come back on its own, and nothing on the source host will notice.
- Check the target's scheduler **heartbeat file mtime**, not merely that a process existed the last
  time someone looked.
- Confirm the target holds its **own** Telegram bot (`telegram.bot_username` / `bot_token_env`). Two
  gateways polling one bot token collide — Telegram answers 409 Conflict and delivery goes
  nondeterministic. Read both configs before starting a gateway.
- When work was stranded by a dead host, restore it to the host that owns the tools and the delivery
  ledger rather than reviving a host retired for a reason.

## Step 3b — Audit by ARTIFACT COMPLETION MARKER, not job status

A job's `last_status: "ok"` is a statement about the **agent turn**, not about the work. In a
script-backed job the agent can run a failing script, narrate the result, and still close green — so
`ok` and `last_run_at` can both look healthy for weeks while the artifact never gets produced.

Count the artifact's own markers instead. For any job that appends to a log or writes a file, the
script's header line is written by a shell that got as far as line 1, and the completion line by a
shell that reached the end. Diff them:

```bash
grep -c "<run-header-marker>"     /var/log/<job>.log
  grep -c "<completion-marker>"   /var/log/<job>.log
  grep -n "<run-header-marker>\|<completion-marker>\|<folder/id marker>" /var/log/<job>.log | tail -30
```

Headers ≫ completions = the job is failing partway, every time. Headers simply absent across a date
range = the job is not firing at all (a different fault, different fix). Then confirm the product
remotely — list the destination folder/table and check for today's dated entry with a real size. A
successful exit code plus a rendered summary is not the artifact.

## Step 3c — Scheduled scripts fail silently under `set -e` + command substitution

The most expensive scheduled failure is invisible in the log. A script that does
`X=$(cmd | filter | parser)` with `set -e` aborts when the pipeline fails, but **the pipeline's
stderr was consumed into the variable** — so the log gets the header, nothing else, and no error.
The job reports `ok` and the outage runs for weeks.

Bad (failures swallowed):

```bash
set -e
ID=$(somecli create --json "..." 2>&1 | grep -v noise | python3 -c "import json,sys;print(json.load(sys.stdin)['id'])")
```

Good (failure is recorded and loud):

```bash
somecli create --json "..." >"$TMP/out.json" 2>&1 || true
ID=$(clean <"$TMP/out.json" | python3 -c "..." 2>/dev/null) \
  || { cat "$TMP/out.json" | tee -a "$LOG"; echo "!!! FAILED: ..." | tee -a "$LOG" >&2; exit 1; }
```

Also log an explicit line for any input that was *expected but missing* (`SKIP (not on disk): X`).
A silent skip is indistinguishable from a successful upload in most upload scripts, and it is how a
whole category of files quietly drops out of a backup after a directory reorganises.

## Step 3d — A job can vanish from the book entirely (not just pause)

Check the job exists at all, and check whether it existed at the time it should have fired. Backup
snapshots of the book are the evidence: if the job is absent from `jobs.json.bak-*` and
`jobs.json.proposed.json` dated inside the outage window but present in the live book, the outage
was a **registry drop during a book rebuild/migration** — not an auth or script fault. Enumerate the
book and diff it against the newest snapshots before theorising about token expiry:

```bash
python3 - <<'EOF'
import json, glob, os
for f in ['/root/.hermes/cron/jobs.json'] + sorted(glob.glob('/root/.hermes/cron/jobs.json.bak*')):
    d = json.load(open(f)); l = d if isinstance(d, list) else d.get('jobs', d)
    if isinstance(l, dict): l = list(l.values())
    print(os.path.basename(f), len(l), 'HAS' if any('JOBNAME' in json.dumps(x) for x in l) else 'ABSENT')
EOF
```

## Step 4 — Snapshot before any resume

`cp jobs.json jobs.json.bak-<ts>` first. A resume batch is reversible only while the prior book
still exists. Then re-read the book and confirm each job shows a `next_run_at`.

## Cron expression trap: hour-field steps are modulo 24

`0 */72 * * *` does not mean every 72 hours. The hour field spans 0–23, so `*/72` resolves to `0`
and the job runs **daily at 00:00**. For any multi-day cadence step day-of-month instead:
`0 3 */3 * *` is every third day. Before trusting a non-standard expression, ask what it expands to
inside a 24h window — a migrated expression is rarely re-validated by whoever copied it.

## Pitfalls

- **Never report `hermes cron status` as a federation-level fact.** "No active jobs" is a host-local
  statement about one book; jobs may be running on a peer or under system cron. Say which substrate
  you actually read.
- **`last_run_at` is not proof of current health.** It is the last time the job fired, possibly
  before the host died. Pair it with substrate 4 (today's fork log).
- **`last_status: "ok"` is not proof the work happened.** See Step 3b: for script-backed jobs the
  status describes the agent turn. Only the artifact's completion marker settles it. A job can also
  carry `repeat.completed: 9` in the book while only 3 of those runs produced output.
- **A recent fire with no error and no artifact is the signature of a swallowed pipeline failure**
  under `set -e` (Step 3c), not of a healthy job. Check the raw output capture before blaming the
  scheduler.
- **A missing job is not a paused job.** An absent registry entry (Step 3d) needs a re-create, and
  re-creating it is a trigger to also confirm the script it calls still works on its hot path.
- **A job that has never had a single execution row is not necessarily new** — it may have been
  dropped and restored. Check `executions.db` row count for the job id, not just `created_at`.
- **A fresh heartbeat file does not mean the jobs are healthy** — it means the ticker runs. A
  scheduler can tick happily with an empty book.
- **Do not fix a stranded job by enabling it on both hosts "to be safe".** That is the double-fire the
  `migrated` reason exists to prevent; the human receives every message twice.
- **A job book that looks "all off" may be entirely migrated**, not abandoned. Read the reasons
  before concluding anything was lost.

## Related

- `hermes-cron-zen` (user-owned) — jobs.json internals, the validator, the script-path resolver, and
  LLM→script conversion. Use it for editing the book correctly; use THIS skill for cross-host
  ownership and completion auditing.
- `scripts/scheduler_substrate_sweep.py` — the one-shot read-only sweep across all four substrates.
- `federation-machine-verification` — confirm which host you are actually on before naming it.
