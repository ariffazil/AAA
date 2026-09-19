# Scheduler Coverage Audit — four schedulers, one number

For any "which recurring tasks run?" question. The failure this file exists to prevent: auditing one
scheduler and reporting its count as the estate's count.

## Rule 1 — four schedulers run in parallel; enumerate all four

```
HERMES CRON    hermes cronjob -> <hermes>/cron/jobs.json     LLM + script-only jobs
ROOT CRONTAB   crontab -l                                     jitu-guard / wrapper chains
/etc/cron.d/   one file per concern                           raw infra, one owner each
SYSTEMD TIMERS systemctl list-timers                          <-- the layer everyone forgets
```

Systemd timers are missed because they are not called "cron", and they usually carry the majority of
recurring work (backups, verifiers, drift detectors, briefings). A migrated legacy scheduler may also
survive as a `jobs.json.migrated`-style file — include it only when the question is "what did we
retire".

## Rule 2 — extract by the schedule field, never by name or comment

```bash
# root crontab — weekly: 5th field is a digit/name, not *
crontab -l | grep -vE '^\s*#|^\s*$' | awk '$5 ~ /^[0-9]/ {print}'

# /etc/cron.d — one schedule line per file; skip SHELL/PATH/MAILTO/TZ headers
for f in /etc/cron.d/*; do
  [ -f "$f" ] || continue
  b=$(basename "$f"); [ "${b:0:1}" = "." ] && continue
  line=$(grep -vE '^\s*#|^\s*$|^SHELL|^PATH|^MAILTO|^TZ=' "$f" | head -1)
  case "$line" in *" * * "[0-9]" "*) echo "$b :: $line";; esac
done

# systemd — weekly entries show a weekday name, not "min/s ago"
systemctl list-timers --all --no-pager
grep -h 'OnCalendar=' /etc/systemd/system/*.timer | sort | uniq -c | sort -rn

# jobs.json — 5th field of the schedule expr is dow; schedule may be a dict or a string
python3 -c "import json;d=json.load(open('<hermes>/cron/jobs.json'));\
[print(j['id'][:9], j['name'][:34], j['enabled'], j.get('schedule'), j.get('deliver')) for j in d['jobs']]"
```

State the extraction limit you accepted. A wrapped line, an `@weekly` macro, or a day-of-week written
inside a shell string will not match — say so rather than implying the list is exhaustive.

## Rule 3 — evidence, in order of authority

1. **The execution ledger** (an openable sqlite beside the job store, or the scheduler's own run log).
   Group by job id:

   ```sql
   select job_id, count(*), max(started_at), max(status) from executions group by job_id
   ```

   A job with **zero rows** has never fired, whatever the job file says.
2. **A dated output artifact** — a file whose *name* carries the run date is the strongest proof a run
   happened and finished.
3. **Log mtime**, judged against the task's own period.

A job's own `last_status` field is the weakest of the four and is usually the only one consulted: it is
written on completion and never expires, so a task that stopped firing keeps its last `ok` forever.
Never quote it as evidence a job runs.

## Rule 4 — judge freshness against the period, and report coverage

Healthy is relative: six hours is stale for an hourly job and fresh for a weekly one. Judge every
receipt against the cadence that produced it, then report the fraction:

```
coverage = tasks with a fresh in-period receipt  ÷  tasks declared at that cadence
```

Split the fraction by owner (harness / agent / organ / OS): the interesting shape is almost always a
wide gap between layers, not a uniform failure. "3 of my 12 weekly jobs fire" is the finding; "12
weekly jobs" is inventory.

## Rule 5 — the invariant to state under the table

> Maintenance a **scheduler** owns runs. Maintenance a **doctrine** owns does not.

The recurring high-cost finding in this class is a **designed-but-never-wired ritual**: a script that
exists, is documented, is commented with its intended schedule, and is installed into nothing.

```bash
grep -rn '<ritual-name>' /etc/cron.d/ /etc/crontab ; crontab -l | grep '<ritual-name>'
```

Zero hits with a working script on disk is not "pending" — it is a capability that never ran. The
related shape is the ritual that *was* hand-run: dated output files in the store, none of them produced
by the scheduled slot. Distinguish by comparing the producer's log mtime (or absent log) against the
artifacts' mtimes, and report both in the same finding.

## Rule 6 — a missing log is not a dead job

A 0-byte log with an old mtime cannot distinguish "ran, found nothing" from "never ran". Where a dated
artifact exists (or provably does not), you can decide; where neither exists, report **unverified** and
name the artifact that would settle it. Never upgrade an ambiguity into a verdict, and never delete a
job on the strength of an ambiguous log — a coverage probe is not a licence to remove work.
