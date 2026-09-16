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
  - "cron doctor says ok but the job never ran"
  - "job skipped its schedule"
  - "silent skip / schedule silently stopped firing"
---

# Federation Scheduler Audit

Answer "is scheduled work actually running?" from evidence across every substrate, not from one
host's local view. This skill observes and reports; it does not mutate cron.

## Why this skill exists

Scheduled work here lives in **five independent substrates**, and any single-host check returns a
confident wrong answer. The expensive failure is not a job that errors — an error is visible. It is
a job that **stops silently**: its host's gateway exits cleanly, no systemd unit brings it back, the
source host's job book sits parked reporting nothing wrong, and nobody notices for days.

## Step 1 — Enumerate every scheduler substrate

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
# 5. systemd timers — invisible to every crontab-parsing check
systemctl list-timers --all --no-pager --output=json
systemctl list-unit-files --state=masked --no-pager
```

Substrate 4 is the one that cannot lie: a configured entry with no `CMD` line in today's journal
never ran. Use it to settle any dispute about whether a job is firing.

Substrate 5 is where a partial sweep goes wrong quietly. **A sensor reading only `crontab -l` does
not have a coverage gap — it has a false all-clear**: it counts its own jobs, finds them balanced,
and publishes a healthy number while every systemd timer on the host goes unmeasured. Coverage is
part of the claim. When the corpus splits across schedulers, report which substrates you read and
treat "N jobs, all healthy" as a statement about N, never about the machine. On one host, a
cron-only sweep reported 36 jobs balanced while 48 timers ran unseen.

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

## Step 2b — Verify the migration TARGET actually runs a scheduler

`state: migrated` is a **claim about another host**, and it is self-sealing: the reason string
("do not re-enable here — double-fire risk") stops every later audit from touching the job, so
nothing ever checks the target. Confirm the claim before treating it as benign:

```bash
ssh <peer> 'ls -l /root/.hermes/cron/jobs.json 2>/dev/null; \
            ps -eo pid,etimes,cmd | grep -E "[h]ermes gateway" ; \
            find /root/.hermes/cron -type f -newermt "-3 days" | head'
```

A peer whose `jobs.json` mtime is weeks old, whose gateway process is absent, and whose cron
output tree holds no recent files is **not scheduling anything** — the jobs are running nowhere,
and the migration note has been shielding the outage. Check what the peer actually runs before
assuming: an edge stack (gateway container + model proxy + automation app) with no Hermes
scheduler is the common shape. Report the jobs as **orphaned**, not migrated.

Do not resolve an orphan by quietly enabling it on the source host: a migration that never
completed also means the delivery ledger and the tool dependencies never moved. Name the finding
and let the owner choose the home.

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

## Step 3e — The job that skips silently (book healthy, ledger empty)

Distinct from 3b/3c: the job does not fail partway, it never starts. The book shows
`enabled: true`, `last_status: "ok"`, and a `next_run_at` cursor that keeps advancing — while the
execution ledger holds no row for it in weeks. A schedule that skips is worse than one that errors,
because it manufactures confidence: `hermes cron doctor` was observed reporting **"✓ found no
issues"** on a host where seven active jobs had not fired for 12–19 days.

Read the ledger the book does not consult:

```bash
hermes cron list; hermes cron doctor        # the record — necessary, never sufficient
python3 - <<'PY'
import sqlite3
c = sqlite3.connect('file:/root/.hermes/cron/executions.db?mode=ro', uri=True)
for r in c.execute("select job_id, count(*), max(finished_at) from executions "
                   "group by job_id order by 3 desc"):
    print(r)
PY
```

Then test **staleness**, not status. Derive the expected period from the 5-field expression —
day-of-week restricted → 7d, day-of-month restricted → 31d, else 1d — and flag
`now - last_run_at > max(2 × period, period + 2d)` as SILENT regardless of `last_status`.

Two ways to be wrong about an empty ledger:

- `executions.db` only covers from the date the ledger was first written. A job whose `last_run_at`
  predates `MIN(finished_at)` cannot be judged from rows at all — judge it on `last_run_at` vs
  period, and use the ledger as corroboration only for the window it does cover. State the window.
- Only Hermes-gateway jobs appear there. System-cron work is substrate 3 and needs substrate 4 (the
  fork log) to settle.

## Step 3f — A job that cannot be witnessed: NOOP ≠ MISSING

Before reading a job's log as evidence, prove the log can witness the job at all. A job that exits
with no output on its idle path — a clean `sys.exit(0)` when the queue is empty, a script that skips
a missing input — writes nothing, so an empty or stale log is not evidence of death. Three worlds
produce the same observation:

```
W1  ran and correctly did nothing                  NOOP
W2  never ran                                      MISSING
W3  no scheduled firing since the log existed      NOT DUE
```

Resolve in this order. **The order is the whole safeguard.**

1. **Positive evidence wins.** Check the job's DECLARED WITNESS — the artifact it produces as a side
effect (a status JSON, a rendered report, a delivered file). If that artifact is fresh within the
job's own cadence tolerance, the job **ran**, whatever its log says and whether or not a firing was
due.
2. **Absence of opportunity is not absence of execution.** Derive the last expected firing from the
5-field expression (not assumed) and compare it to the log's own creation time. If no firing has
happened since the log came into existence, the answer is NOT_YET_DUE — a weekly job whose log was
created after its last Monday has not failed.
3. **Only then report the ambiguity as ambiguity** — `NOOP_UNPROVEN` — naming the gap instead of
filling it. Never resolve it to healthy, never to dead.

Keep the declared-witness list **explicit and reviewed**, one entry per job, exactly like a linter's
exclusion list: a job whose witness is not declared is not silently excused, it is reported.

**Reaching any of these conclusions requires opening the script, not just the log.** In one pass,
five zero-byte logs resolved to four different verdicts, and every one needed a probe — reading the
exit path, the side-effect target, and the cron entry's creation date. A taxonomy applied without a
probe is the same class of error as a stale log read as evidence.

**Fix the unwitnessable class, not the instance.** A job silent on its idle path can never prove it
ran, so it is indistinguishable from one dead for days and **no monitor can tell you which**. One
heartbeat line per tick on the empty path (~4 KB/day for a `*/30` job) buys the only property the
old shape lacked: the job can now **fail to appear**. Keep the genuinely un-provisioned case
silent — a missing input root is a provisioning signal, not a heartbeat case. See
`references/job-observability-classification.md` for the full taxonomy, the cadence-derivation and
log-target parsing traps, and the level ladder.

## Step 3g — A timer can be ACTIVE and still not be armed

`systemctl is-active <unit>.service` cannot answer "is this scheduled work alive". A oneshot unit is
`inactive` between its timer's firings, so the same query returns the same word for a healthy idle
job and a dead one — an audit that classified units this way reported "three heartbeat units loaded
and dead" when only two were genuinely unarmed and the rest were simply between runs. Classify from
the **timer**:

| status | shape | meaning |
|---|---|---|
| `ARMED` | next elapse + a last firing | normal |
| `STALLED` | timer active, `next` empty, old `last` | **fired once, never rescheduled** |
| `UNARMED` | `next` empty, never fired | never armed |
| `MASKED` | symlinked to `/dev/null` | retired on purpose — a decision, not a defect |
| `NO_FIRE_RECORDED` | armed, no firing ever | newly armed, or the unit has never started |

`STALLED` is the one that hides: `systemctl status` shows `Active: active (running)`, so a timer
that fired once and never came back reads as healthy. Settle it with `NextElapseUSecRealtime`
(empty == no next firing), `LastTriggerUSec`, and the unit's own exit status — a service can sit at
`status=1/FAILURE` for weeks behind an active-looking timer and nothing reports it. See
`references/job-observability-classification.md` for the two false positives to guard (sub-grace
recompute, and masked-parsing) before wiring this into a recurring check.

Two more traps in the same read, both of which made a `STALLED` timer look settled when it was not:

- **Read `OnCalendar`, never the unit `Description`.** A timer described `(daily09:00 MYT)` carried
  `OnCalendar=*-*-* 01:00:00` — firing eight hours off its own label. The description is prose an
  author typed once; the calendar line is what systemd obeys. Any "when does this run" answer taken
  from a description is unverified.
- **`SuccessExitStatus` can make a failing verdict look like a successful unit start.** A probe unit
  carrying `SuccessExitStatus=0 1` reports a run that found 1-of-5 surfaces healthy as a *successful*
  start, so `systemctl status` is green and the exit status says nothing. This is defensible — the
  probe ran and reported; the threshold verdict is data, not a crash — but it means the verdict lives
  in the **journal**, and `systemctl status` is not the witness for a job whose failure is a verdict
  rather than an exception.

## Step 3h — Repairing a STALLED timer, and revert-falsifying the cause you were handed

A `STALLED` timer (active, no next elapse, old last firing) is usually a **stuck unit**, not a bad
unit file. Reset the state before editing anything:

```bash
systemctl stop  <unit>.timer
systemctl reset-failed <unit>.timer <unit>.service   # clears the failed/stuck state
systemctl start <unit>.timer
sleep 3
systemctl show <unit>.timer -p NextElapseUSecRealtime -p ActiveState -p SubState   # expect active/waiting + a real next
```

**A supplied root cause is a claim, and it is cheap to falsify — so falsify it before you record it.**
When a peer, an external audit, or your own first read hands you the cause ("`RemainAfterExit=yes` on
a oneshot keeps the unit active so the timer clears its schedule"), the test is a **revert**: put the
suspected setting back, change nothing else, reset, restart, and re-measure.

```bash
# restore ONLY the suspected setting, then re-run the same reset + restart + show
sed -i 's/^RemainAfterExit=no/RemainAfterExit=yes/' /etc/systemd/system/<unit>.service
systemctl daemon-reload && systemctl reset-failed <unit>.timer <unit>.service && systemctl start <unit>.timer
sleep 3; systemctl show <unit>.timer -p NextElapseUSecRealtime
```

If the timer arms anyway, the supplied cause is **disproven**, and recording it in a canonical
receipt would plant a permanent wrong explanation that every later reader inherits. State the
repair that actually worked (here: the reset, not the unit-file edit) and demote the suspected
setting to what it really is — an improvement for a different reason, if you keep it at all. Keep
it only when you can name that reason; `RemainAfterExit=yes` makes `is-active` return `active` for a
unit that finished eleven days ago, which is a lying status surface and worth removing on its own
merits — say *that*, not "it caused the stall".

Snapshot the unit file before editing (`cp -p` to a backup dir) and quote the backup path in the
receipt, so the edit is reversible by someone who was not in the session.

**Test the detector against a known-bad input, not just its unit tests.** A classifier of
absence-states can pass every table-driven case and still fail end-to-end. Make the tool's input
source injectable (`CRONTAB_FILE`-style env override, a fixture dir argument) so the production path
— parse the expression, derive the cadence, resolve the log, classify, set the exit code — can be run
as a subprocess against a synthetic job you have broken on purpose, with no real log or crontab
touched. Assert the known-dead job surfaces as dead, not as merely not-yet-due. Do the same for
whatever is consumed downstream: a classification omitted from the machine-readable output is a
classification that was never published, and the consumer will read the next field as a healthy
total.

## Step 3i — Fired ≠ Delivered: read the obligation ledger

The ladder does not stop at execution:

```
Scheduled ≠ Ran ≠ Delivered ≠ Effective
```

Execution proves the job started. It says nothing about whether the output reached anyone, and a job
can run cleanly for weeks while every message it produces dies. Delivery has its own store:

```bash
sqlite3 /root/.hermes/state.db \
  "select state, count(*) from delivery_obligations group by state;"
```

`delivered` / `failed` / `abandoned` / `attempting` are the real delivery states. Any standing
`failed` or `abandoned` volume is delivery debt that no scheduler view surfaces — the job shows
`last_status: ok` because the *turn* succeeded.

**The self-addressed origin trap.** A job's `origin.chat_id` is the address it replies to. When it
holds the **bot's own Telegram user id** — commonly copied from the session origin when the job was
created from inside a self-DM — every reply becomes a bot-to-bot DM, which Telegram refuses with
`Forbidden: the bot can't send messages to the bot`. Nothing in `is-active`, `last_status`, or
`hermes cron doctor` reveals it; the only trace is the obligation ledger.

```bash
grep -o '"id": [0-9]*' /root/.hermes/IDENTITY_LOCK.json        # the bot's own uid, read live
sqlite3 /root/.hermes/state.db \
  "select state, count(*) from delivery_obligations where chat_id='<bot_uid>' group by state;"
```

Repair a mis-seeded origin with a backup first (`cp -a cron/jobs.json cron/jobs.json.bak-<ts>`):

1. Repoint every `origin.chat_id` equal to the bot uid at the human's id, recording why in the entry.
2. Drop the self-DM entry from `channel_directory.json` so it cannot be re-selected as a target.
3. Re-grep both files to prove none remains, then confirm the terminal count stops growing.

Existing obligation rows are terminal history — do not attempt to re-deliver them. If the count keeps
rising after the fix, the writer is elsewhere: sweep every live session bound to the same store
before attributing the loop to one process. A second CLI bound to the same DB writes to it too.

## Step 3j — An incident ledger without `closed_by` is a cemetery, not a metric engine

`cron_incidents` records `first_seen_at` / `last_seen_at` / `closed_at` and an error string. It does
NOT record who closed an incident or what verified the fix — so "closed" means someone stopped
looking, not that the fault was repaired:

- **Rows sharing one identical `closed_at` were swept in a batch.** Read that as one walk-past, not N
  resolutions; a single batch close can carry incidents that had been open for days each.
- **Check the timestamp columns' offsets before computing any duration.** One column can hold a local
  offset while another holds UTC in the same table, silently corrupting every MTTR figure derived
  from it.
- **"Effectively closed" needs its own probe.** Re-run the exact call the incident recorded failing.
  A close with no re-run is an administrative close, and the original fault may still be live on
  another host.

Add `closed_by` + `verified_by`, normalise to UTC, and treat the ledger as the seed of a closure
metric rather than a status feed.

## Step 4 — Snapshot before any resume

`cp jobs.json jobs.json.bak-<ts>` first. A resume batch is reversible only while the prior book
still exists. Then re-read the book and confirm each job shows a `next_run_at`.

Re-anchor a silently-skipping job (mutating — becomes a T1 change, snapshot first):

```bash
hermes cron pause <job_id> && hermes cron resume <job_id>     # NOT `resume --at <ISO>`
```

`hermes cron resume --at <ISO>` **refuses** on a recurring job (`Cannot re-arm recurring jobs:
re-arm is one-shot-only; use plain resume or cron run`) — and it refuses *after* the pause has
already applied, so a pause-then-bad-resume sequence silently leaves the job stopped. Plain
`resume` re-computes the next natural occurrence. Confirm the expected `Next run` in
`hermes cron list`, then confirm a row actually lands in `executions.db` on that slot. If it skips
again after a clean re-anchor, the ticker is at fault, not the expression.

Do not re-anchor a job whose delivery target is a human's inbox merely to prove the fix — let it
ride its natural slot once. A second forced ping costs more than a one-cycle delay.

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
- **`hermes cron doctor` returning no issues is a statement about the BOOK, not about execution.** It
  cannot see a job that holds `enabled: true` / `last_status: ok` while never firing. Pair every
  "healthy" verdict with one read of `executions.db` (Step 3e) before repeating it to a human.
- **An empty execution ledger is not proof the job never ran.** Check the ledger's own coverage
  window (`MIN(finished_at)`) against the job's `last_run_at`; if the job predates the ledger, the
  rows say nothing either way. Report the window you actually covered.
- **Do not fix a stranded job by enabling it on both hosts "to be safe".** That is the double-fire the
  `migrated` reason exists to prevent; the human receives every message twice.
- **A job book that looks "all off" may be entirely migrated**, not abandoned. Read the reasons
  before concluding anything was lost — then verify the destination (Step 2b). `migrated` plus a
  target with no scheduler is not a migration; it is an outage wearing a migration's immunity
  from audit, and it is the one silent-stop class a "do not re-enable" note guarantees will go
  unnoticed.
- **A 0-byte log is ambiguous, not healthy and not dead** (Step 3f). Reading emptiness as either one
  is the defect; only a declared witness artifact, or the absence of any firing since the log
  existed, breaks the tie. "No data" is never "all clear".
- **A classifier that resolves every absence to a benign state is a test that cannot fail.** The
  first version of the Step 3f order checked NOT_YET_DUE *before* the declared witness, so four
  demonstrably-alive jobs were all reported as merely not due. A benign-default branch that can
  swallow every input is decoration wearing a verdict. Check positive evidence first, and prove the
  failing branch is reachable before trusting any classification the sensor emits.
- **`2>&1` is not a log path, and neither is an arrow in a comment.** Parsing a crontab line with a
  naive `>>?\s*(\S+)` captures `&1` from every line that closes stderr — one measurement reported
  39 jobs as `NEVER_WROTE` against a path named `/root/&1`. Strip trailing `#` comments first (an
  operator note reading `... -> STALE` was taken as the target `gate`), skip `&N` and `/dev/null`,
  and let an explicit `>>`/`>` target **win over** a `tee` payload: the redirect is what witnesses
  the job, the tee target is usually the job's own product. A line with no redirect at all is
  UNMEASURED — say that, rather than reading it as healthy.

- **A scheduler count is a statement about the substrates you read, not about the host.** A sweep
  that walks `crontab -l` and stops can publish "36 jobs, all balanced" while dozens of systemd
  timers run unmeasured on the same machine — the count looked healthy precisely because the missing
  half was invisible. Name your substrates in the verdict, and extend to a new scheduler the moment
  you learn one exists rather than treating its absence from your report as its absence.
- **Fired is not delivered.** A job can run green while every message it produces dies: read the
  `delivery_obligations` states, never the job's `last_status`. Non-zero `failed`/`abandoned` against
  the **bot's own uid** means the job's `origin.chat_id` was mis-seeded (Step 3i).
- **`is-active` on a oneshot service is not a liveness check.** Oneshot units are `inactive` between
  firings, so the word is identical for healthy-idle and dead. Ask the timer (Step 3g).

## Related

- `hermes-cron-zen` (user-owned) — jobs.json internals, the validator, the script-path resolver, and
  LLM→script conversion. Use it for editing the book correctly; use THIS skill for cross-host
  ownership and completion auditing.
- `scripts/scheduler_substrate_sweep.py` — the one-shot read-only sweep across all four substrates.
- `scripts/mission_health.py` — the runnable staleness verdict: expands each enabled job's 5-field
  expression, counts the fires it actually missed inside a grace band, and exits 3 on any SILENT
  job (or 2 if the book itself is unreadable). This is the check Step 3e describes, performed.
  Read its `--help` before trusting a verdict, and re-validate its parser against hand-computed
  windows after any change (see the detector self-test rule in `live-multiwriter-audit`).
- `/root/scripts/attention_governor.py` — the standing runtime that consumes this verdict: it scans
  the loop registry, scores what deserves human cognition, and reports open loops as
  decision + surprise + exception. Run it after any scheduler finding so the same fault cannot
  regrow unwatched.
- `federation-machine-verification` — confirm which host you are actually on before naming it.
- `references/job-observability-classification.md` — the NOOP/MISSING/NOT-DUE taxonomy, the
  resolution order and why it is the safeguard, cron cadence derivation traps, log-target parsing
  traps, and the level ladder. Read when a job's log is empty, stale or 0-byte and you must decide
  whether that is idleness, death, or an unwitnessable job.
