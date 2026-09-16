# Job observability classification

Topic: deciding whether a scheduled job actually ran, when its log cannot witness it. Companion to
Step 3f of the skill. Read when a job's log is empty, stale or 0-byte.

## The worlds one observation hides

```
W1  ran and correctly did nothing                 NOOP
W2  never ran                                     MISSING
W3  no scheduled firing since the log existed     NOT DUE
```

All three can present as: *a log that used to grow and stopped*. Asserting any single one without a
probe is the failure; the sensor's job is to name which, or to say it cannot tell.

## Resolution order — the order IS the safeguard

```
1. declared witness fresh within cadence tolerance   -> ALIVE
2. no firing since the log was created               -> NOT_YET_DUE
3. otherwise                                         -> NOOP_UNPROVEN
```

Swapping 1 and 2 is the bug that matters: it resolved four demonstrably-alive jobs (a `*/15` probe
whose output artifact was 42 seconds old, two daily jobs whose deliverables were fresh, one weekly
job due that morning) to `NOT_YET_DUE`. **Positive evidence must outrank absence of opportunity**,
because absence of opportunity is only a statement about the schedule while a fresh artifact is a
statement about reality.

A benign default that can absorb every input is not a classifier. Before shipping one, enumerate the
inputs that would take each branch and require the failing branch to be reachable.

## Declared witness

Some jobs legitimately write nothing to stdout. Their witness is an artifact they produce:

| job shape | witness is |
|---|---|
| a probe that publishes state | the published file's mtime |
| a delivery job that copies a digest | the delivered file's mtime |
| a pipeline that writes a report | the report's mtime |

The list must be explicit and reviewed — one entry per job, keyed by the command, like a linter's
exclusion list. A job with no declared witness and an empty log is reported as ambiguous, never
excused. Declaring a witness for a job that is in fact broken downgrades a real outage to silence,
so treat additions to the list as a reviewed change.

## Cadence derivation traps

To decide whether a job had a chance to fire, expand its 5-field expression over a lookback window
and take the last firing at or before now.

- Count only firings **at or before now**. A one-day window evaluated at noon holds half a day of
  firings, not a full day's — assert `49` for `*/15`, not `96`.
- Day-of-week: cron numbers **Sunday = 0**, Python's `weekday()` is **Monday = 0**. Convert, or a
  weekly job is checked against the wrong day.
- When **both** day-of-month and day-of-week are restricted, vixie-cron matches if **either**
  matches — not both.
- Steps in the HOUR field are modulo 24: `0 */72 * * *` is daily at 00:00, not every 72 hours.
- Derive the period from the expression; never ask the book for it.

## Log-target parsing traps

Each of these produced a false alarm in practice:

- `2>&1` is **not** a path. A naive `>>?\s*(\S+)` captures `&1` on every line that closes stderr.
- Strip trailing `#` comments **first** — an operator note containing an arrow (`... -> STALE`) was
  captured as the target `gate`.
- An explicit `>>` / `>` / `1>` target **beats** a `tee` payload. The redirect is what the operator
  wrote to witness the job; the tee target is usually the job's own product.
- `/dev/null` and `&N` are not logs.
- No redirect at all → `UNMEASURED`. Report it as unmeasured rather than reading the absence as health.

## Levels

```
ALIVE / NOT_YET_DUE / NOOP_UNPROVEN / UNMEASURED   INFO   (report, trend, never gate)
SILENT                                              WARN  (a witness existed and stopped)
```

`WARN` is reserved for a witness that existed and then stopped. Everything else is a record. A level
that can never clear stops being read, and a by-design property belongs at `INFO` with its
instruction text intact — drop the level, keep the reason.

## Scheduler armed state (systemd timers)

The same discipline applied to the other scheduler. Read it from the timer, never from the service:

```bash
systemctl list-timers --all --no-pager --output=json     # next/last are µs epochs; 0 == never
systemctl list-unit-files --state=masked --no-pager
```

```
ARMED             next elapse + a last firing
STALLED           timer active, no next elapse, old last firing   <- the one that hides
UNARMED           no next elapse, never fired
MASKED            symlinked to /dev/null — retired deliberately
NO_FIRE_RECORDED  armed but never fired
```

`STALLED` is invisible to `systemctl status`, which prints `Active: active (running)` for a timer
that fired once and never rescheduled. Corroborate with `NextElapseUSecRealtime` (empty string ==
no next firing), `LastTriggerUSec`, and the unit's exit status — a `status=1/FAILURE` service
behind an active timer is the signature of "fired, failed, never came back".

Two false positives, both the same shape as the log classification above:

- **A firing seconds ago with no next elapse yet is a recompute, not a stall.** Require a grace
  window (~10 min) before calling it STALLED, or a minute-cadence timer reports as stalled on every
  run.
- **MASKED is a decision, not a defect.** Parse the state *column* of `list-unit-files`, not the end
  of the line: an `endswith` test matches nothing and re-reports every deliberately-retired timer as
  unarmed, which dresses a decision as a fault.

## Implementation in the federation

- `/root/scripts/attention-metrics.py` — `A1 scheduled_silence`. The classification is extracted
  into a pure function (`classify_job`) precisely so it can be regression-tested; logic buried
  inside a scan loop cannot be shown to fail.
- `/root/scripts/tests/test_attention_metrics.py` — 19 cases pinning the branches that must fire
  **and** the ones that must not (witness-before-not-yet-due ordering, the `2>&1` and
  comment-arrow false positives, tee-vs-redirect precedence).
- `/root/scripts/tests/test_attention_metrics_e2e.py` — the **negative control**. Unit cases prove
  the decision function discriminates; a planted-assertion run proves the runner can return FAIL;
  neither proves the end-to-end classification, because both sit upstream of it. This suite drives
  the shipping CLI as a subprocess against a synthetic crontab and asserts that a known-dead job
  surfaces as dead. Without it the detector's verdict on reality is untested, not merely
  under-tested.
- To make the production path testable, give the tool an **environment override** for its input
  source (a `*_FILE` variable that replaces the real crontab/config/ledger with a fixture). The
  alternative — importing the module and calling internals — skips the parse → derive → resolve →
  classify → exit-code path that is the thing you actually ship, and cannot catch a fault in the
  wiring between those stages.
- Wired into `/root/scripts/hermes-chaos-sweep.py` under `C12 sensor_regression`, so a later edit
  that softens the classifier is caught by the sweep instead of by the next missed outage. An
  unwired test is prose in a `.py` file.

**Prove the sensor can fail after every change**: plant one wrong assertion, confirm the sweep
returns FAIL with exit 1, then restore. A suite that cannot be made red is not evidence of anything.

**Prove the report publishes every class it computes.** A machine-readable output that omits one of
the statuses the classifier can emit makes jobs in that class vanish from everything downstream —
the classification existed and the publication did not, which is the same produced-≠-delivered gap
the classifier was written to detect. Enumerate the statuses the tool can emit and assert each one
appears in the machine-readable output.
