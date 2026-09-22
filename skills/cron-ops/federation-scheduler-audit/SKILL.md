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
capability_tier: fed-long-context
ecology_state: WARM
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

## Step 1b — Enumerate by DELIVERY TARGET, never by job name

When the question is "what reaches this person / this chat", the substrates are only half the scope.
The other half is your filter, and a keyword filter is the half that hides.

Filtering job NAMES (`grep -E 'zen|chron|brief|alpha'`) silently omits every deliverer whose name
lacks the word, and the omission is invisible — the list looks complete because nothing in it is
obviously missing. Two live deliverers to the same human DM were missed exactly this way. Enumerate
by ADDRESS, then resolve each hit to a name; never the reverse:

```bash
python3 - <<'PY'
import json, pathlib
TARGET = "<destination id>"          # the address, not a topic word
for book in ("/root/.hermes/cron/jobs.json",):
    d = json.loads(pathlib.Path(book).read_text())
    for j in (d["jobs"] if isinstance(d, dict) else d):
        o = j.get("origin") or {}
        if TARGET in json.dumps(j) or "origin" == str(j.get("deliver")):
            print(f"{str(j.get('name'))[:44]:<44} {j.get('deliver')} "
                  f"origin_user={o.get('user_id')} enabled={j.get('enabled')}")
PY
# then extend the same address grep across the OTHER substrates, which hold jobs no book knows about
grep -rn "<destination id>\|cron-deliver\|sendMessage" /etc/cron.d/ /root/scripts/*.sh
```

A destination grep also catches the jobs the Hermes book cannot see — script-backed entries in
`/etc/cron.d` and the root crontab address the human directly, with no book entry at all.

**`deliver: "origin"` is a pointer, not a target.** Resolve it through the job's own
`origin.user_id` / `origin.chat_id` before counting, or one job is counted twice — once as the
literal string `origin` and once under its real address — and the total is wrong in both directions.

**A filter is a coverage claim.** State the destination and the substrates together, or "N jobs
reach this person" is an undercount presented as a total.

## Step 2 — Interpret `enabled: false` by its `state`

Hermes parks a disabled job with a machine-readable reason, and three very different meanings hide
behind `enabled: false`:

| `state` | `paused_reason` | Meaning |
|---|---|---|
| `migrated` | `MIGRATED to <host> ... do not re-enable here (double-fire risk)` | Live on another host. **Never resume here.** |
| `migrated-system-cron` | `converted to /etc/cron.d/<file>` | **Claimed** to be a raw crontab entry. The file is named but never checked — verify it (Step 2c). Re-enabling double-fires it *if the claim is true*. |
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

## Step 2c — `converted to /etc/cron.d/<file>` is a claim, and one `ls` falsifies it

Step 2b verifies the peer host for `state: migrated`. Its sibling travels unchecked: a job parked
with `converted to /etc/cron.d/<file>` **names a file nobody ever opens**. Measured on one host:
**13 jobs** carried that reason and the named prefix matched nothing — not in `/etc/cron.d/`, not in
`/etc/crontab`, not in any crontab, not on the peer host, and not even as a surviving script under
any of its likely names. The jobs had been dead 17 days while the book described them as migrated.
The same host carried `/etc/cron.d/.hermes-cron-ban-<date>/`, a directory of `.disabled` units
showing that the cron.d approach had since been **banned** — so every one of the 13 cited a
substrate that was not merely empty but retired. Three of them delivered to a person.

```bash
# every job claiming a cron.d home, then whether that home exists
python3 - <<'PY'
import json
p = '/root/.hermes/cron/jobs.json'
d = json.load(open(p))
for j in (d['jobs'] if isinstance(d, dict) else d):
    r = str(j.get('paused_reason') or '')
    if 'cron.d' in r or 'converted' in r:
        print(f"{j.get('id')}  {str(j.get('name'))[:40]:40}  {r[:60]}")
PY
ls -la /etc/cron.d/ | grep -i '<named-prefix>'
grep -rln '<named-prefix>' /etc/cron.d/ /etc/crontab /var/spool/cron/ 2>/dev/null
find / -name '*<job-slug>*' -not -path '*/proc/*' 2>/dev/null | head   # the script must exist too
```

A `paused_reason` is metadata written by whoever parked the job, in the same act of parking it. It
is **not** a statement about the target, and nothing in the toolchain re-checks it. Note the
asymmetry that hides the fault: `state: migrated` names a peer you can SSH to, so Step 2b was
written for it; `converted to <file>` names a path you can `ls` in one command, and because that is
so cheap nobody does it.

**A ban directory is the strongest signal in the sweep.** Finding `/etc/cron.d/.hermes-cron-ban-<date>/`
means an operator deliberately retired that substrate *after* the jobs were parked there — so every
job still citing it as its new home is orphaned by construction, not migrated. Report them as
**orphaned — target substrate retired**, name the count and the human-facing ones, and do not offer
to resume them on the source host: they were parked for a reason that predates the ban, and the
reasons for both decisions live with their owners.

**Do not quietly re-create them either.** Re-creating a job whose script no longer exists on disk
produces a fresh registry entry that fails on first fire — a second silent outage with a green
book. Confirm the payload exists before proposing a home.

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

**Run a positive control before trusting any zero.** Pick two or three jobs whose `last_run_at` is
recent and confirm the ledger returns ≥1 row for each. If a job that demonstrably ran also has no
row, the join itself is broken (wrong key, wrong store) and every zero you are about to report is an
artifact of the probe. Only once the control passes does a zero row count carry information.

**Group by `source` before calling anything an orphan.** The executions store is not exclusively the
gateway book's ledger — its `source` column also carries scheduler-internal fires (`builtin`,
`direct`) that have no `jobs.json` entry by design. So a set difference (N job ids present in the
ledger and absent from the book) is normally that second population, **not** registry drift. Run both
directions of the census and keep them separate, with the `source` breakdown attached:

```sql
select source, count(distinct job_id) from executions group by source;   -- populations, first
select count(*) from executions where job_id='<recent-job-id>';          -- positive control
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
- **A header comment in a scheduled *script* is a claim, not a schedule fact.** The `Description` rule
  above applies verbatim to shell and cron payloads. A script banner reading
  `Runs at 06:00 UTC (14:00 MYT)` described a job that actually fired at **06:00 system-local** — a
  crontab inherits the host's `TZ` unless the entry sets its own, so a timezone word in a comment is
  usually the author's assumption, not a measured offset. Settle the firing time from two artifacts
  the machine wrote, never from the banner:

  ```bash
  grep -E '^\[?=== ' <job>.log | tail -1      # the script's own stamped header (a `date -u` line gives the offset directly)
  stat -c '%y %n' <artifact it produced>      # the product's mtime, in local time
  ```

  A log header reading `22:00Z` beside a product mtime of `06:00` is the whole proof. Report the time
  you measured; reading the banner instead republishes the author's bug into your own report.

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

## Step 3k — Declaring two jobs redundant: compare DESTINATION and PRODUCT, never name or schedule

Retiring a "duplicate" job is a mutation, and the cheap discriminator is wrong. Three jobs named like
briefs, at overlapping morning slots, resolved to **three different products on three different
surfaces**:

| shape | destination | product |
|---|---|---|
| script-backed brief | Telegram **group** (a topic id, not the human's DM) | text, plus a sidecar JSON consumed downstream |
| systemd timer brief | Telegram DM | text |
| `/etc/cron.d` brief | a static **web page on disk** | HTML — no Telegram at all |

Only the DM pair were actually redundant. Compare on **destination ID + artifact type** before
proposing a merge:

```bash
grep -nE 'deliver|chat_id|TELEGRAM_.*TARGET|MEDIA' <job script | jobs.json entry>   # where it addresses
python3 -c "import json,sys;d=json.load(open('/root/.hermes/channel_directory.json'));\
  print([c for c in d['platforms']['telegram'] if str(c['id']).split(':')[0]==sys.argv[1]])" <chat_id>
```

Resolve the id to a **name** before calling anything a duplicate: a group topic and a DM look
identical in a jobs book and are different readers.

**A job whose output another job consumes is an upstream stage, not a duplicate.** Retiring it starves
the consumer silently — the downstream loop simply stops having input and reports nothing. Grep for a
file the job writes before proposing to kill it:

```bash
grep -nE 'Path\(|\.json|\.jsonl|\.md' <job script> | head    # sidecars and their consumers
```

**The other direction is the expensive one: two lanes can pause each other into zero.** When two
sessions independently notice the same duplication and each retires the *other's* job, the result is
not one brief — it is **none**, and both operators report success. After any redundancy action,
re-read the whole surface and assert the surviving count is exactly one, naming the substrate you
counted:

```bash
# enumerate every enabled deliverer from ALL substrates (see Step 1), then count those reaching the human
```

State the **count you observed**, not the change you made. "Paused the duplicate" is not a delivery
claim; "exactly one job now delivers to this destination" is.

### Choosing which duplicate survives

Finding the duplicate is half the job; deciding which one lives is the other half, and the instinct
here is wrong. **The survivor should be the stronger ENGINE, not the lane you happened to build.**
Two lanes were built for the same deliverable within a minute of each other; the one that lost the
scheduling race also had the better state layer, the real test suite, and the theme support — and the
correct move was consolidating onto it and deleting the other implementation rather than defending
your own. Keeping your version because it is yours leaves the weaker engine in production and
doubles the maintenance surface.

Evaluate on evidence, never authorship:

- Does it have a **claim/state store with a stable join key**, or only a list of artifact hashes? The
  one that can express "this claim MOVED" is the one that can learn.
- Does it have a **real test suite**? Run both, right now, before choosing.
- Does it keep **content and presentation separable** (more than one theme/engine)?
- Is a **second writer actively improving it**? A lane under active development will simply be
  rebuilt tomorrow if you retire it — consolidation that ignores this resets the race.

**Retire the trigger, keep the code.** Switch off the losing lane's schedule; do not delete its work.
It is often the better source of a component even when it is the worse orchestrator.

**Then break every dependency on the retired lane.** A survivor that reads the loser's output — a
sidecar, a state file, a "run after that one" note — waits forever on a file that no longer updates,
and reports nothing. Grep the survivor for the retired lane's paths before declaring done.

**Two writers in one store will collide, and the failure is deferred.** A second writer declaring the
same table name with a different column set in a shared SQLite file is not rejected: `CREATE TABLE IF
NOT EXISTS` silently no-ops, so the owning module's schema never exists and its first query dies much
later with a misleading error (`no such column: <x>`) far from the cause. When two lanes share a
store, **check the schema you are about to rely on is the one that actually got created**, and fix a
collision by **renaming the conflicting table and preserving the rows** — never by dropping it, which
destroys the evidence of what those rows were.

## Step 3l — A whole job book can be DORMANT (enabled, frozen cursor)

The reverse of Step 3e. There the cursor advances while nothing executes. Here the cursor is
**frozen in the past** while every job in the book reports `enabled: true`, because the runtime
that reads the book is dead. Such jobs are not paused, not migrated, and not failing — they are
**dormant**, and the book gives no hint of it. `enabled: true` is a field about intent, never
about a live reader.

```bash
python3 - <<'PY'
import json, datetime
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
for p in ('/root/.hermes/cron/jobs.json',
          '/root/AAA/agents/hermes-asi/runtime/cron/jobs.json'):
    try:
        d = json.load(open(p))
    except Exception:
        continue
    jobs = d if isinstance(d, list) else d.get('jobs', [])
    en = [j for j in jobs if j.get('enabled')]
    stale = [j for j in en if str(j.get('next_run_at') or '') < now]
    print(p, f'{len(en)} enabled / {len(jobs)} total, {len(stale)} with a PAST next_run_at')
PY
```

A live ticker always rewrites the cursor forward after firing, so *every* enabled job carrying a
`next_run_at` in the past is the signature. Report the book as DORMANT and name the runtime whose
death explains it.

**Dormant is not harmless — it is a loaded collision.** These jobs are still in the store and still
`enabled`. Restarting the runtime re-arms all of them at once, so a book quietly dead for months
comes back into the very slots a replacement lane now occupies, and both deliver. Before restarting
any dormant runtime, diff its enabled jobs against the live surfaces by destination and product
(Step 3k) — the restart is the injection, not the audit. Report it as a finding and let the owner
choose, exactly as with an orphaned migration (Step 2b).

**A second Hermes-family book can live on the SAME host**, under another agent's runtime directory,
and it is invisible to every peer-host check. Enumerate books by path, not by host:

```bash
find / -name jobs.json -path '*cron*' 2>/dev/null
```

Ignore `_CANONICAL`, `quarantine`, and `state-snapshots` hits — those are history, not schedulers.
"No duplicate on this host" requires having looked at every book on it, not only the one your CLI
reads. A cron-book count taken from one book is a statement about that book.

## Step 3m — Count RULES and CAPABILITIES, never files or triggers

Two counting errors make a sweep look far smaller than the surface it claims to cover, and both are
invisible because the total is plausible.

**A count of files is not a count of jobs.** One `/etc/cron.d` directory of 40 files held **106
rules** — a file-per-capability naming convention hides the fan-out. Count non-comment lines the
scheduler will actually execute, and report the unit you counted:

```bash
# substrate 3, counted as RULES (the schedulable unit), not as files
for f in /etc/cron.d/*; do [ -f "$f" ] && n=$(grep -cvE '^\s*(#|$)' "$f"); [ "${n:-0}" -gt 0 ] && echo "$n $f"; done \
  | sort -rn | awk '{s+=$1} END {print "total cron.d rules:", s}'
crontab -l | grep -cvE '^\s*(#|$)'          # user crontab rules
```

Folding all five substrates into one number before reporting is the only honest total: a measured
pass found **55 systemd timers + 106 cron.d rules + 54 user-crontab rules + 35 gateway-book jobs
(15 enabled)**, against 104 running services. Any one of those figures quoted alone is an undercount
presented as the machine.

**A count of triggers is not a count of capabilities.** The load-bearing measure is how many
triggers converge on the same *responsibility*. Extract the invoked script from every substrate and
invert the map — one target reached from several surfaces is one capability with several entries:

```python
# basename of every script each substrate invokes -> set of surfaces that invoke it
targets.setdefault(os.path.basename(p), set()).add(surface)
dup = {k: v for k, v in targets.items() if len(v) > 1}   # report these as candidate DUPLICATE_TRIGGER
```

Then widen past exact-path identity: the expensive duplicates are distinct scripts serving one
responsibility under different names. Look for families — `*reconcil*`, `*drift*`, `*verify*`,
`*census*`, `vault*`, `*digest*` — and count how many independent implementations answer each
question.

**N gates over ONE inventory in one window is DUPLICATE_WORK, not defence in depth.** Five separate
cron jobs ran against the same skill inventory inside a single 26-minute window on the same four
daily hours (`skill-matrix`, `skill-entropy-gate`, `skills-census`, `mcp-health-census`,
`skill-resolution-gate`). Five guardians, one subject, five chances to disagree and no mechanism to
reconcile them. Merge to one sweep that emits one verdict per dimension; a stacked tower of gates is
usually five authors each adding a check rather than five independent risks.

## Step 3n — Optimize the institution, not each job

The unit of optimisation is the **capability graph**, never the individual script. Cleaning N jobs
one at a time can leave the federation strictly more complicated than before, because every local
fix adds an owner, a schedule and a receipt to a graph that needed fewer of all three.

The convergence order is fixed, and each step is only reached when the one above it is impossible:

```
DELETE unnecessary → MERGE duplicate → CLARIFY ownership
  → SIMPLIFY the path → STANDARDISE the envelope → REPAIR broken → ADD a missing primitive LAST
```

Do not solve complexity by adding an orchestrator. A new coordinator above a duplicated set is the
most expensive way to keep every existing moving part.

The target is not maximum automation. It is the **smallest coherent causal graph** that observes,
routes responsibility, acts safely, verifies outcomes, learns from error and recovers — with routine
complexity absorbed below human attention. Report the DELTA in nodes, duplicate paths and sources of
truth; "I fixed 12 scripts" is not a convergence claim, and "6 drift detectors → 1 reconciler + 1
witness" is.

## Step 3o — Classify the detectors before quoting any of them

A drift/degraded label is **one scheduled process's opinion**, and nothing in the substrate
reconciles the detectors with each other. A measured pass found **six** reconciler/drift-detector
timers answering one host with independent definitions and no cross-check — at 3-minute,
15-minute and daily cadences. Six definitions of "drift" is not six times the confidence; it is zero
shared ground truth, and the loudest one wins by accident because it fires most often.

Assign every detector exactly one role, and report a count that violates it as a chaos source rather
than as extra coverage:

| role | may do | budget |
|---|---|---|
| RECONCILER | compare declared vs actual **and converge** | one per responsibility |
| DETECTOR | compare and report only | one per audience |
| WITNESS | independently attest the reconciler's result | at most one, sharing no code with either |

**A deliberate HOLD is not drift, and a declared-vs-deployed comparator cannot tell them apart.** A
deploy reconciler that pauses because `local ahead of origin (unpushed labor)` is **working
correctly** — it has deliberately refused to converge. A second detector comparing
`src=<sha> deployed=<sha>` on the same host reports that same state as `DRIFT`/`degraded`, and a
third chases the shadow. Before propagating any drift verdict, read the **actor's own log** for a hold
reason: "the reconciler declined on purpose" and "the artifact is stale" produce an identical SHA
mismatch and need opposite responses. Unpushed labor is the most common cause on this host — check
for it before calling any deploy state broken.

**Read the value beside the label, never the label.** Reporters print a status word and a payload that
can disagree, and the word is what later audits cite:

```
OK wealth: src=eaa87d5a deployed=UNKNOWN     # the one unmeasurable organ filed as healthy
L02: Truth Score: 0.960 >= 0.99              # a FAILED threshold rendered with a satisfied operator
result=success  →  labelled FAILURE          # a passing unit announced as a failure
```

Three layers, one defect: **the label is produced independently of the value, and the value is the
only part that was computed.** Practical rules: evaluate every emitted comparison operator against its
own operands before repeating the line; treat any payload that is `UNKNOWN`/`None`/`null`/`-`/empty
as **unmeasured** regardless of the word beside it (grep the report for labels adjacent to those
sentinels); and when a unit reports one verdict in a human-readable string and another in
`SERVICE_RESULT`/exit state, reconcile by field and report the disagreement instead of picking a
winner. A monitor that prints a threshold it did not evaluate converts missing measurement into a
green tick, and the green tick is exactly what the next audit cites as evidence.

**Consequence for the report you write:** never relay a detector's label as a finding. Relay the
operands, name which detector produced them, and say which of the six you actually read.

## Step 3p — A configured job whose target cannot be executed

Distinct from every failure above: the schedule is correct, the book is clean, the script exists — and
cron cannot start it. Entries call an absolute path directly, and **there is no shell doing shebang
resolution** on the far side: the file must carry the exec bit. A script written by a batch (editor,
sync, scaffold, whole-directory copy) lands mode `644`, and every single run logs the same line into
that job's own log:

```
/bin/sh: 1: /root/…/scripts/agent-cockpit/stuck_detector.py: Permission denied
```

Sweep every substrate for targets that are missing or not executable — strip the wrapper prefixes
first, or every line looks broken:

```bash
crontab -l | grep -vE '^\s*#|^\s*$' | while IFS= read -r line; do
  cmd=$(echo "$line" | sed -E 's/^[^ ]+ [^ ]+ [^ ]+ [^ ]+ [^ ]+ //; s#^/root/\.local/bin/[A-Za-z0-9_-]+ [A-Za-z0-9_-]+ && ##')
  t=$(echo "$cmd" | sed -E 's#^(\.[^;]*; *|TZ=[^ ]+ *|cd [^ ]+ && *)+##' | awk '{print $1}')
  case "$t" in /*) [ -e "$t" ] || echo "MISSING  $t"; [ -x "$t" ] || echo "NOT-EXEC $t";; esac
done
# /etc/cron.d: field 7 onward is the command (m h dom mon dow user cmd)
grep -rhE '^[^#]' /etc/cron.d/ | awk '{print $7}' | sort -u
```

The log evidence here is the exact inverse of Step 3c: there the failure is silent because stderr was
swallowed into a variable; here it is loud, in a file nobody reads. **Open the job's own log before
calling a target healthy** — twenty identical permission errors is a job that has never once run,
wearing a schedule's authority.

The repair is `chmod +x`, which is not a crontab mutation: it restores the intent of an existing line
and is reversible. Prove it by timestamp at the next slot, not by absence of fresh errors.

**After any batch write into a directory cron executes from, re-sweep exec bits.** A whole-batch copy
is precisely how a set of working monitors becomes a set of silent ones.

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
- **A `paused_reason` is a claim, and nothing in the toolchain re-checks it.** `converted to <file>`
  is falsifiable with one `ls`; a prefix matching nothing means the work has been dead since the
  migration, wearing a migration's immunity from audit (Step 2c). Read the reason, **then verify the
  target**, for every `enabled: false` job you have decided not to touch — the ones you leave alone
  are exactly the ones no later pass will examine.
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

- **A `last_run_at` that does not land on a schedule slot is a MANUAL run, not the schedule
  working.** A job with expression `0 6 * * *` whose `last_run_at` is mid-morning was triggered by
  hand; its schedule has still never fired. Cross-check `created_at`: a job created *after* its own
  slot cannot have run on it. The manual run also leaves a receipt for a **dry run** — an artifact
  reported `PRODUCED` with the payload never sent — so the ledger shows a same-day result while
  nothing reached any reader. Only a `last_run_at` sitting on a real slot is evidence about the
  schedule.
- **A scheduler count is a statement about the substrates you read, not about the host.** A count is
  also a statement about the FILTER you applied (Step 1b): a job-name grep undercounts silently,
  because a deliverer whose name lacks the keyword is absent without looking absent. A sweep
  that walks `crontab -l` and stops can publish "36 jobs, all balanced" while dozens of systemd
  timers run unmeasured on the same machine — the count looked healthy precisely because the missing
  half was invisible. Name your substrates in the verdict, and extend to a new scheduler the moment
  you learn one exists rather than treating its absence from your report as its absence.
- **Fired is not delivered.** A job can run green while every message it produces dies: read the
  `delivery_obligations` states, never the job's `last_status`. Non-zero `failed`/`abandoned` against
  the **bot's own uid** means the job's `origin.chat_id` was mis-seeded (Step 3i).
- **`enabled: true` says nothing about whether anything is reading the book.** A dead runtime leaves
  every job enabled with a `next_run_at` frozen in the past — dormant, not paused. Worse than idle:
  a restart re-arms them all into slots a replacement lane now occupies (Step 3l). And there can be
  more than one book on one host; enumerate by path, not by hostname.
- **`is-active` on a oneshot service is not a liveness check.** Oneshot units are `inactive` between
  firings, so the word is identical for healthy-idle and dead. Ask the timer (Step 3g).
- **A timezone or schedule stated in a script's own header comment is a claim.** Crontabs inherit the
  host `TZ`; settle the firing time from the script's stamped log line and its product's mtime
  (Step 3g).
- **"Same name" or "same hour" is not duplication.** Compare destination ID and artifact type, and
  check whether the job feeds a consumer before retiring it (Step 3k). Two lanes pausing each other's
  duplicate produces zero, not one — assert the surviving count from every substrate.
- **A delivery target must be DECLARED, and the grammar matters.** `hermes send -t <bare_number>`
  fails with `Unknown or unregistered plugin platform: <number>` — the bare id is parsed as a platform
  name. The `telegram:<chat_id>` form is required. A transport probe that uses the wrong grammar
  returns a **false negative** and will convince you a working path is broken, so probe with the exact
  form the job itself will use. Resolve the id to a NAME before trusting it: a group topic and a DM
  look identical in a job book and reach different readers.
- **Creating or updating a scheduled job passes through the constitutional gate — a refusal is the
  gate working, not an error to route around.** Two shapes bite. A payload asserting a critical
  variable (money/health/legal) with no admissible source is held: a URL counts as a citation SHAPE
  and must actually resolve, so prefer a **receipt id plus an on-disk evidence path**, which cannot be
  NXDOMAIN'd. A destructive command shape is refused outright: **rewrite the operation (rename and
  preserve) rather than retrying it**.
- **After any create or update, re-read the book from disk and confirm the field persisted.** The
  tool response echoing your value back is not evidence it landed in the store — and a target that
  silently reverted is indistinguishable from a working job until it fails to deliver.

- **A count of files is not a count of rules, and a count of triggers is not a count of
  capabilities.** 40 files in `/etc/cron.d` held 106 rules; five separate jobs ran against one skill
  inventory in one 26-minute window. Count the schedulable unit and invert the trigger→target map
  before reporting any total (Step 3m).
- **Six detectors agreeing is not corroboration.** One reconciler, one detector per audience, one
  independent witness — anything more is MULTIPLE_SOURCE_OF_TRUTH, and the highest-frequency detector
  wins the narrative by accident (Step 3o).
- **A status word is not a measurement, and `UNKNOWN` beside `OK` is unmeasured.** Read the operands
  and compare them against their own operator before repeating any line as a verdict (Step 3o).
- **A deliberate HOLD reports identically to drift.** Read the actor's own log for a hold reason —
  unpushed labor is the usual one — before propagating any DRIFT/DEGRADED label (Step 3o).
- **Clean N jobs one at a time and the graph can still get more complicated.** Converge on the
  capability graph in the fixed order DELETE→MERGE→CLARIFY→SIMPLIFY→STANDARDISE→REPAIR→ADD, and
  report the delta in nodes/duplicate paths/sources of truth, never a count of scripts touched
  (Step 3n).
- **A job can be enabled, scheduled, and structurally unable to start.** A non-executable target is
  neither a scheduler fault nor a script fault, and no book or doctor read reveals it — only `ls -l`
  on the exact path the entry executes, plus the job's own log (Step 3p).

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
