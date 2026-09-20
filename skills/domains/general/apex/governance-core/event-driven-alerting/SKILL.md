---
name: event-driven-alerting
description: "Use when designing what a scheduled job or monitor reports."
owner: Hermes
---
# Event-Driven Alerting

A scheduled job is a **timing** mechanism, not a **meaning** mechanism. The default
failure of monitoring is not too little signal — it is piping every run's raw output
into a channel until nobody reads it. Fix the delivery design before adding jobs.

## The one rule

**Publish on state transition, not on schedule.**

A job may run every 60 seconds; that says nothing about whether its result deserves a
message. Jobs are *evaluators*. The channel carries only material change.

## Route by consequence, not by source

The severity belongs to the *content*, not to the job that emitted it. One job can
emit any tier depending on what it found.

| Tier | Content | Route |
|---|---|---|
| P0 interrupt | security, data loss, production outage | post immediately |
| P1 receipt | a verified state change landed | one compact receipt |
| P2 digest | trend or governance context | batch daily/weekly |
| P3 telemetry | routine success, clean checks, job start/end | logs only — never the channel |

Most jobs are P3 most of the time. That is the correct outcome, not a bug.

## Route to a human only on a declared human reason

Severity answers *how urgent*; it does not answer *whose work this is*. A machine fault is machine
work, and defaulting it to the human is how an operations channel becomes a queue the sovereign has
to clear by hand.

Assign an owner to every signal, and make the human the exception:

```
NEXT_ACTOR = machine|agent     DEFAULT — any fault a lane can repair, retry, or delegate
             human             ONLY when HUMAN_REASON is one of:
                                 DECISION_REQUIRED · CONSENT_REQUIRED · COMMITMENT_DUE
                                 MATERIAL_CHANGE · SAFETY · PERSONAL_INFORMATION_REQUESTED
                                 EXCEPTION_UNRESOLVED
```

Carry both in one envelope: `STATE · SOURCE · NEXT_ACTOR · ACTION · SEVERITY · DEADLINE · TRACE_ID ·
RECEIPT_REF`. `ACTION` is a concrete repair, not a restatement of the symptom; `NEXT_ACTOR` is a
lane, not a person's name, so the recipient is routable without the sovereign deciding who owns it.
A signal with no `NEXT_ACTOR` is an orphan, and orphans accumulate on the human by default.

**Every field that names a subject must be derived from the predicate that set `STATE` — never
authored alongside it.** A hand-written `ACTION` sits next to a computed verdict and drifts from it,
and the reader has no way to tell which one is load-bearing. Measured: an alert carrying
`ACTION=inspect <guard> HOLD on durable bus` named a subsystem that was demonstrably healthy — its
own canary reported `ok`, single-digit ms, consumer attached — while the report's actual
`verdict_reason` named a different organ entirely. Two defects in one line: the route pointed at the
innocent party, and it concealed the guilty one. The detector's own computed reason is the only
subject the envelope may name; build `ACTION` by branching on `verdict_reason`, not by writing a
sentence about what this alert class usually means.

**An agent with no silent destination proves its silence by announcing it.** The A0 band
("observe and handle, do not notify") is a *destination* requirement before it is a behavioural
one: if the only surface the producer has is the channel, then "I am staying silent" is the only
available evidence of compliance, and the room fills with exactly the murmur the band was defined
to remove. Give silent work a real sink the producer can write to — an append-only record, the same
one the delta gate already uses — and name that sink in the producer's instructions, so silence is
provable by the *absence* of a channel message rather than by a message about absence.

## Delta gate — the mechanism that makes it quiet

Hash the evaluated content; post only when the hash differs from the last **successfully
delivered** post. Record the hash only after a confirmed send, so a failed delivery
retries on the next tick instead of being silently swallowed.

```bash
H=$(printf '%s' "$CONTENT" | sha256sum | cut -c1-16)
if [ -f "$STATE/$SOURCE.last_hash" ] && \
   [ "$(cat "$STATE/$SOURCE.last_hash")" = "$H" ]; then
  exit 0                      # unchanged — stay silent
fi
# … deliver …
printf '%s' "$H" > "$STATE/$SOURCE.last_hash"   # only after confirmed send
```

Dedupe key = hash(rule + host + resource + normalized condition), so one condition
cannot re-post under a new message id. Without this, a steady-state problem becomes a
daily fresh-looking alert.

**Exclude the trace id from the key, and gate the RECORD with the key too — not only the delivery.**
A per-emission `trace_id` is unique by construction, so minting a fresh one per firing makes every
repeat look like a new event. Measured: one unchanged condition wrote four separate entries into the
append-only event log inside half an hour, each with its own trace id, no two deduplicable. If the key
guards only the channel, the audit log becomes the repeat generator and the next reader counts four
incidents where there was one. Hash the condition, write that key into the record, and skip both the
record and the message when it is unchanged.

**Compute the dedup verdict BEFORE the record is written.** A durable entry appended without its
verdict cannot answer the one question a reader has — delivered, or suppressed? — and a ledger of
unlabelled repeats reproduces the exact false incident-count the key exists to prevent. Order the
emitter as: hash the condition → decide → stamp the decision into the record → then act on it. If you
drop the repeat entirely rather than recording it, that requirement still holds: the absence must be
the designed behaviour, never a side effect of deciding after the append.

**Give the key a window, or a standing condition never re-announces itself.** Repeating an unchanged
condition on a schedule is escalation policy or nothing — so pick one deliberately. The contract that
works:

```
first occurrence of a condition         -> notify   (a new fault must always be heard)
repeat inside the window                -> record suppressed=true, do NOT notify
condition changes (source|state|action) -> notify   (a different thing is wrong)
window lapses, condition still open     -> notify once (still broken is news)
```

The identity is `sha256(source|state|action)` — cheap, stable, and computable at the emitter without
any new state beyond a small per-fingerprint file. Without a window the only two reachable designs
are a storm and a permanently silenced fault; the window is what makes "quiet" and "still broken"
distinguishable. Seed the window when you deploy it, or the standing condition re-announces once more
before the new code takes effect. Also note that a long-lived worker caches the emitter module in
memory: the change is not live until that worker restarts, so the storm you are observing may be
the *old* code (see `live-service-ops` on census and on crediting an intervention).

## The record is the log; the channel is a projection

Write an append-only event record **first**, then deliver. Never let the chat channel
be the only trace of what fired — it is not queryable, not diffable, and not audit.

The record is what a later audit reads. The message is a courtesy to a human.

## Message contract

Machine-parseable header, human-readable body, one screen:

```
FORGE | <severity> | <event_type>
event: <id>            scope: node|federation
host: <host_id>        source: <job>
dedupe: <hash>         time: <ISO-8601 UTC>

<what changed, before -> after, evidence path>
```

Always carry `host_id` and `scope`. A claim about a service without a node qualifier is
a rumour, not a finding.

## Name the relation, not just the value

Every field in an alert must carry the *relation* that produced it. A bare arrow
(`PATTERN → /path`) is read as "the thing is wrong at /path" by every reader — humans
and agents alike — no matter what the emitter meant. If the path is actually a
destination, a registry key, or an owning skill, say so in the label:

```
BAD   SILENT_FAIL → /root/.hermes/skills/.../federation-organ-recovery
GOOD  SILENT_FAIL  lesson→owner_skill: /root/.hermes/skills/.../federation-organ-recovery
```

Why it matters more for agents than humans: a misread destination reads as a *defect*,
and the natural remediation is to "repair" a path that is already correct — converting a
cosmetic ambiguity into a real broken reference. Verify the emitter's own semantics
(`grep` the line that builds the string) before acting on any arrow-shaped field.

**Surface the check you already performed.** If the emitter resolved, validated, or
existence-checked the value before printing it, print that result. An emitter that
silently drops the outcome of its own check forces every reader to re-run the probe to
answer "is this even resolvable?" — and readers on another host, without the same tree
or credentials, will answer it differently. Carry the checked state in the payload and
carry the negative case explicitly (`[UNRESOLVED at emit]`, not an empty string), so the
field is self-describing. A field whose validity each reader must re-derive is a field
that will be misread.

**But test the check against every SHAPE the field can carry — a check run on the wrong
shape manufactures a false negative, which is the same failure class it was added to
prevent.** Measured 2026-09-16: an existence check on a target field reported two live
entries as `[UNRESOLVED at emit]` because the field has two shapes — a plain path, and
`container.json#fragment` — and `os.path.exists()` was being run on the whole string
including the `#fragment`. The values were right; the relation the check assumed was
wrong. The fix is to split the shape before checking and to state the scope honestly:

```python
path, _, frag = str(target).partition("#")
if not os.path.exists(path):     return "  [UNRESOLVED at emit]"
if frag:                          return "  [container exists; #fragment not path-checked]"
return ""
```

A marker that over-claims (`UNRESOLVED` on something present) trains readers to ignore it,
which costs more than the ambiguity it replaced. When the check can only cover part of the
value, say which part — never let the marker imply more than was verified.

**Root rule, sharper than "value right, relation wrong": the instrument never lies — the
narrative laid over its output does.** `curl` honestly refused `127.0.0.1:8088`; `exists()`
honestly said a string containing `#fragment` is not a path. Both outputs were true, and a
failure story was told on top of each. So test every marker by one question:

> Can this string be traced back to the literal predicate that produced it — and to nothing
> else?

`[container exists; #fragment not path-checked]` names its predicate and its scope. It is a
measurement report. `[UNRESOLVED at emit]` on a live entry is a *conclusion* — it asserts a
state of the world that the predicate never tested. Markers must state the measurement, not
the meaning: scope, not verdict. A reader who must re-derive the predicate from the label is
back to forensics, which is the cost the marker was added to remove.

### Read the operands, not the label — a satisfied-shaped line can be a failed comparison

The same defect appears inside threshold and status *values*, where it is quieter than a bad
marker because the line looks like a measurement. Three measured shapes from three layers of one
system, each read as a pass by every consumer:

```
L02: Truth Score: 0.960 >= 0.99             a FAILED threshold printed with a satisfied operator
OK wealth: src=eaa87d5a deployed=UNKNOWN    a sentinel (unmeasured) printed under a pass label
<notifier> FAIL … (result=success)          the disposition word compared against the wrong variable
```

- **`a >= b` must actually satisfy `a >= b`.** A reason string that renders the comparison is still
  a claim: check the operands. A producer that formats a threshold as "met" regardless of outcome
  reports the same string whether the floor passed or failed.
- **A sentinel is not a pass.** `UNKNOWN` / `None` / `n/a` / empty means the field was never
  measured, so a green label beside it converts a missing measurement into a false assertion — the
  exact inversion the label exists to prevent.
- **The disposition word is a word, not a status.** Confirm which variable the notifier compared
  before believing its polarity; a notifier can be correct about the value it read and wrong about
  the thing the reader assumes it read.

When you find one, report the **class**, not the instance: the same formatting defect usually exists
wherever that producer writes thresholds, and repairing one call site leaves the others lying.

Self-test before shipping an alert format: strip the emitter and hand the line to
someone who has never read the code. If they cannot state what each token's role is,
the format is not finished.

### A ratio moves for two reasons; report both, or the trend lies

A compliance percentage that falls can mean the numerator got worse *or* the denominator
got smaller. Reading the ratio as a trend is how a housekeeping sweep gets reported as a
governance collapse. Always publish the pair (`31/190 → 37/149`) next to the percentage,
and state which side moved: "six new entries arrived without the declaration, while the
population shrank by 41" is a finding; "compliance dropped 12 points" is a rumour about a
number.

**Read the predicate before trusting the metric's name.** A check implemented as a case-
insensitive grep for `F1|F2|F4|floors` over a whole file measures *mention*, not
*declaration* — any file that names a floor in prose passes. The metric is honest about
what it tested and wrong about what its label claims. Before acting on any compliance
figure, open the line that computes it and say aloud what predicate it actually runs; then
report the number under that name ("mentions a floor"), not the label's name ("declares
floor_scope").

**Do not fix a metric by satisfying its predicate.** Stamping the missing field across every
failing file raises the score and the underlying binding stays absent — a declaration nobody
enforced is a false record, and it is the same act as silently reconciling two disagreeing
numbers. Per-item fields that carry real meaning get set per item, by whoever owns the item;
a sweep is only legitimate for genuinely mechanical, meaning-free normalisation. Say which
case you are in rather than letting the count drop speak for itself.

## Survey before routing

Jobs live on independent surfaces that do not reconcile with each other — Hermes cron
(`cronjob_manage action=list`), systemd timers, system cron (`crontab -l`,
`/etc/crontab`, `/etc/cron.d/*`), and any registry file. A delivery design built from
one surface silently misses the others. Enumerate all of them first.

## A monitor's threshold must equal the published promise

When an alarm guards a commitment made in a document ("acknowledgment within N hours",
"response within N days"), the threshold is not a tuning knob — it is a copy of that
document, and the copy drifts.

**First find out which copy the outsider reads.** In a multi-repo federation one promise
exists in many files and they disagree. Measured on one host, 2026-09-16: the public repo
`arifOS/SECURITY.md` (and its `origin/main`) promised **72h** — and that is the file the
unit's own `Documentation=` URL points at — while **eight** internal mirrors (AAA, GEOX,
WEALTH, A-FORGE, WELL, arifFlow, FRAME, browser-poc) each said **48h**. Both numbers were
real, in different files; a "no such number exists anywhere" conclusion came from grepping
one file and generalising.

**Read the number from the artefact, never from a summary of it.** A summary, a memory,
and another agent's confident reading are one failure class: a copy that cannot disagree
with its source. Open the file. Then open the *other* files — a single-file grep is how a
second published number stays invisible.

- Enforce the **reader-facing** number. An alert citing a window the reader cannot find in
  the public document is its own falsehood, and erodes trust in the alarm.
- Record the drift inline, naming both families, so the next agent does not re-derive it
  and flip the constant back and forth.
- Enforcement *looser* than the promise the reporter holds is the dangerous direction: the
  report reads clean while the promise is already broken.
- Wanting a stricter internal standard is a reason to tighten the **document**, not to let
  the watchdog measure something other than what was promised.
- Changing a public commitment is a sovereign decision, not a code cleanup: surface it
  rather than picking a number silently.
- On finding a second agent's edit to a constant you set, verify the premise from source
  before deferring to it. Deference to a wrong edit is how a false fact becomes permanent.

## Drills must be marked at the transport boundary

A synthetic-failure drill is only useful if it traverses the real path end to end; but an
unmarked drill is byte-identical to a real P0 and every reader must open forensics on a
system that is actually healthy. Two alarms, one drill, three agents investigating — the
cost lands on exactly the attention the alerting was built to protect.

Mark at the edge, not in the message body: a single env flag (e.g. `DRILL=1`) read once
and prefixed inside the notify function, so the production path stays byte-identical when
it is unset and the marker cannot be edited away per-drill. Verify both branches — drill
marked, unset unchanged — by capturing the composed payload to a harmless sink before
shipping.

## Match the conversation, not the platform's thread id

When a monitor decides "has this been answered?" from a platform object id (Gmail
`threadId`, a ticket id, a chat thread), assume the platform will split one human
conversation across several of them. Gmail splits threads; a reporter's follow-up can
arrive under a fresh `threadId` while the reply sits in the original. A per-thread check
then reads an answered conversation as unanswered and, at the deadline, fires a P0 on the
reporter who already thanked you — a false alarm manufactured by an id, on a person.

Observed 2026-09-16: message `1a0a3f0cffd5eae8` ("Re: SSRF in arif_fetch") got its own
thread while the answer lived in `1a034a0dc7d3bfc5`; 72h later the watch would have
alarmed on a satisfied correspondent.

- When the primary check says "no", fall back to a **conversation-level** match —
  normalized subject (strip `Re:`/`Fwd:`/`[tags]`, casefold, collapse whitespace) across
  sibling threads — before raising anything.
- Run the fallback on the alarm path only, so a clean run costs nothing extra.
- Return three states, never two: answered / not-answered / **cannot-tell**. A lookup
  failure must be cannot-tell; a silent `False` turns an API hiccup into an accusation.
- Record *how* it was resolved (`acknowledged_via`) so the next reader can audit the
  decision instead of re-deriving it.
- Same rule for any "does a reply exist?" probe: identity is the conversation, the id is
  a hint.

## Silence must be witnessable, or it is indistinguishable from death

The counter-rule "a silent job is not a broken job" holds only while the job is *capable* of
speaking. A job that exits early with no output when it finds nothing to do cannot be witnessed at
all: over any window its log is byte-identical whether it ran cleanly every tick or died weeks ago.

Measured on one host: a `*/30` entry whose log had not grown in 11.6h, while the scheduler fired it
at 09:00, 09:30, 10:00, 10:30 and 11:00. The job's empty-queue branch exited silently by design, so
the log had never been the schedule's output — its only two records came from manual runs, and
grepping the emitted status string across every owning repo returned **zero writers**. A stale log is
not evidence of death until you prove the job writes that log.

Two steps before raising (or dismissing) a silence finding:

```bash
# 1. Does the job write this log at all?  Zero writers = decoy log, wrong alarm.
grep -rl "<the emitted marker>" <owning repos> --include='*.py' --include='*.sh'

# 2. Does the schedule actually fire?  Ask the scheduler, not the file.
journalctl -u cron --since "12 hours ago" | grep "<script>"
```

3. Then decide. Cron firing + a stale log is the signature of an **unwitnessable** job, not a dead
   one. A job that cannot be probed at all reports `UNMEASURED`, never "healthy".

**Rule: the idle path must still emit a marker.** One line per tick (~4 KB/day) on the
nothing-to-do branch — the value is not the content, it is that the *absence* of the line becomes
evidence. Make it distinguishable from real work so a later reader can tell idleness from activity:

```json
{"tool": "…", "ts": "…", "status": "NO_INTAKE", "state_written": false,
 "note": "queue empty — heartbeat; state NOT advanced"}
```

Keep the genuinely-absent case silent — a directory not yet provisioned or a missing dependency IS
a provisioning signal, and a heartbeat there is noise. Heartbeat the *idle* branch, not the
*broken* branch.

**Then a silence check can be honest.** Compare each job's *own* firing cadence (derived from its
cron expression, per job) against its log mtime, and report three states — `SILENT` (used to grow,
stopped), `UNWITNESSED` (0-byte log: no data is not all-clear), `UNMEASURED` (no redirect, so the
job cannot be judged). A two-state healthy/broken checker reports a job as healthy precisely because
nothing could look at it, which is the failure the monitor exists to prevent.

### Parsing a crontab is where this check goes wrong

Two false-positive generators, each caught only by reading the output count:

- **`2>&1` is not a destination.** A regex like `>>?\s*(\S+)` captures `&1` from every line that
  closes stderr and then reports the whole crontab against a path named `/root/&1` — 39 false
  `NEVER_WROTE` findings in one run. Match `(?:>>?|1>|2>)\s*([^\s&|;)]+)` and drop `&1`, `&2`,
  `/dev/null`, and anything starting with `&`.
- **A trailing `#` comment can contain an arrow.** An operator note ending `… gate -> STALE …`
  yielded the target `gate` — a comment parsed as a log path. Split on `\s#` before scanning the line.
- **Derive the expected cadence per job** from its own five fields: `*/N`, lists, ranges, and the
  vixie-cron rule that a day matches when *either* day-of-month or day-of-week is restricted. Allow
  roughly one missed cycle. A single global tolerance fires on monthly jobs and stays quiet on `*/5`.

**Count the findings before believing them.** A first run reporting every job broken is a parser bug,
not a systemic outage; the tell is that the finding count equals the crontab length.

### Resolve absence in a fixed order, and let positive evidence win first

A single 0-byte log corresponds to several different worlds, so one "unwitnessed" bucket is not
enough. Use explicit states and a fixed resolution order:

```
ALIVE          log grew, or a declared witness artifact is fresh
SILENT         log used to grow and stopped
NOT_YET_DUE    no scheduled firing has happened since the log was created
NOOP_UNPROVEN  0-byte log, a firing has passed, and no witness is declared
NEVER_WROTE    the redirect target has never existed
UNMEASURED     no redirect, or the source itself could not be read — the job cannot be judged
MASKED         deliberately retired by the operator
```

**Order matters, and the wrong order produces a check that cannot fail.** Measured 2026-09-16: a first
version tested `NOT_YET_DUE` before the declared witness, so four jobs that were demonstrably alive
(a fresh artifact each) were all reported "not due yet" — a classifier resolving every absence to a
benign state is decoration. Resolve: **declared witness first** (a fresh artifact proves the job ran,
regardless of whether the log could have shown it), then absence-of-opportunity, and only then report
the ambiguity by name.

**Declare the witness, do not infer it.** A job whose output is a side effect rather than stdout is
not unwitnessed — it has an artifact, and the artifact's mtime is the evidence. Keep a small reviewed
map of `job -> witness artifact` (the same shape as a declared-shells list): a `*/15` job writing no
stdout is ALIVE if its declared output file is fresh. Everything not on that map and logging 0 bytes
is `NOOP_UNPROVEN` — "ran and correctly did nothing" and "never ran" are observationally identical,
and asserting either one is the defect. Every `UNMEASURED`/`NOOP_UNPROVEN` line must be printed, never
dropped: a job silently absent from the report reads as healthy.

### A timer needs its own taxonomy, and `is-active` lies for oneshot units

`systemctl is-active <service>` cannot separate healthy-idle from dead when the unit is `Type=oneshot`:
it is `inactive` between firings by design. Ask the **timer**, and classify:

```
ARMED            active, next elapse set, last firing recorded
STALLED          active, NO next elapse, last firing old  -> fired once and never rescheduled
UNARMED          no next elapse and no firing ever recorded
MASKED           symlinked to /dev/null: an operator decision, not a defect
NO_FIRE_RECORDED armed but never fired
```

- **`MASKED` and `UNARMED` must not share a level.** Parse `systemctl list-unit-files --state=masked`
  by column: the line reads `NAME.timer  masked  enabled`, so the state is the *second* field. Testing
  `.endswith("masked")` matches nothing and dresses every retired unit as a defect.
- **A timer whose `NextElapseUSecRealtime` is briefly empty right after firing is not stalled** — that
  is systemd recomputing. Without a grace window (order of minutes), every frequently-firing timer
  reads as stalled on some % of runs: a flapping false alarm.
- **`STALLED` is the one worth having.** A timer that fired once and never rescheduled reports
  `ActiveState=active` and looks identical to a healthy one in every status surface, while the unit it
  activates has not run for days. Check the unit's exit status before calling the schedule healthy.
- Reuse this taxonomy wherever a oneshot unit is monitored; a "dead daemon" claim about a
  timer-driven unit is usually just a service resting between runs.

### Extract the classifier, then run it against a known-broken input

A sensor whose logic lives inline in a scan loop cannot be shown to fail, and a check that cannot
fail is decoration. Three levels, all needed:

1. **Pure decision function** — `classify(size, log_mtime, fires, witness_exists, witness_mtime,
   expected, now) -> (status, why)`, so every branch including the negative ones is testable.
2. **Env override for the input source** — e.g. `CRONTAB_FILE=<path>` so the *production* path
   (parse spec -> derive cadence -> resolve log -> classify -> exit code) runs as a subprocess against
   a synthetic fixture, touching no real log and no real crontab.
3. **Unit cases prove the function; a harness test proves the runner; NEITHER proves end-to-end.** Run
   the tool against a fixture containing a known-DEAD job and assert it reports `SILENT` and exits
   non-zero. Unit tests and the harness are both upstream of the thing that matters.

And prove failability directly: plant one wrong assertion in the suite, confirm the runner returns
FAIL with a non-zero code, restore it. A suite that has never been seen to fail has not been tested.

## A new notifier is untested until BOTH branches have fired

Wiring a voice onto a previously silent job is an improvement only if the voice tells the truth. A
pass/fail wrapper's *failure* branch is the one that gets exercised by accident during setup (the
unit is restarted, the log fills, something fires), so it is the *success* branch that reaches
production unproven — and an inverted predicate lives there invisibly for as long as nothing
succeeds.

**Prove each branch by running the real path and reading what it printed.** A wrapper whose success
branch has never executed is a wrapper whose failure branch you are reading; there is no "probably
fine". See both verdicts once, from the unit's own exit, before the channel is trusted.

### systemd oneshot wrappers: read the variable the manager actually sets

`ExecStartPost=` / `ExecStopPost=` receive the outcome as environment, and the names are not
interchangeable:

| variable | value on a clean run |
|---|---|
| `$SERVICE_RESULT` | `success` |
| `$EXIT_CODE` | `exited` — a *word*, not a status |
| `$EXIT_STATUS` | `0` — the numeric status |

So the ubiquitous test `[ "$EXIT_CODE" = "0" ]` is false on success and **never** true, making every
run alert FAIL. Compare `$SERVICE_RESULT` first, then `$EXIT_STATUS`.

**`ExecStopPost=` fires on every exit of a oneshot unit — including a successful start.** It is not a
stop hook; it is an "any exit" hook. A wrapper placed there must expect to run after
`systemctl start <unit>` in a healthy case, and must not read that as a stop.

Probe the manager's own contract instead of guessing it:

```bash
# /tmp/envprobe.sh:  { echo "SERVICE_RESULT=[${SERVICE_RESULT:-<unset>}]"; \
#                      echo "EXIT_CODE=[${EXIT_CODE:-<unset>}]"; \
#                      echo "EXIT_STATUS=[${EXIT_STATUS:-<unset>}]"; }
chmod +x /tmp/envprobe.sh
systemd-run --unit=envprobe --collect --property=Type=oneshot \
  --property=ExecStopPost=/tmp/envprobe.sh /bin/true
cat /tmp/envprobe.txt
```

### Never measure elapsed time from inside the notifier

`$SECONDS` counts from the start of the shell that reads it. A wrapper is a *new* shell, so `$SECONDS`
is ~0 there no matter how long the unit ran — every alert then carries a fabricated duration, and a
monitoring field that cannot be non-zero is worse than an absent one because it looks measured. Take
the duration from the manager (`ExecMainStartTimestamp` / `ExecMainExitTimestamp`, or
`$MONOTONIC_USEC`), or drop the field.

**This is the same defect class as a metric whose predicate does not test what its label claims:** the
number is honest, the meaning laid over it is not. Before a wrapper prints any derived figure, name
the predicate that produced it and confirm it can take a non-default value.

### One run, one verdict

A per-run notifier fired from two hooks emits two messages that can disagree — a `success-so-far` echo
followed seconds later by `FAIL` for the same run. The reader cannot resolve which to believe, and the
contradictory pair trains them to ignore both. Gate the channel on the run identity
(`Invocation`/`MainPID`, or a hash of the verdict) so one run yields exactly one message, and let the
**log** carry the intermediate phase.

**A false alarm is strictly worse than the silence it replaced.** Silence costs attention once, when
someone notices the absence; an alarm that lies spends the credibility every future alert depends on,
and the third false positive is when the true one stops being read. Say this plainly rather than
shipping the notifier anyway — and never let a success branch ship unobserved simply because the
failure branch was loud enough to look like evidence.

## Counter-rules

- A clean run is P3. "X succeeded" is not news.
- A job that only *starts* something is not a receipt — a receipt needs verified end state.
- **A verifier that exits 0 having checked nothing has reported SCHEDULER_SUCCESS, not
  OUTCOME_SUCCESS.** Keep the two names separate in the output: a due-count of zero makes the run
  indistinguishable from a successful verification of zero items, and it is the *pair* (`due=0`,
  `status=success`) that lets a reader tell "nothing was due" from "the thing was verified".
- **A stage that can complete with no output needs a named terminal state.** Low counts are healthy
  when an outcome was correct and unsurprising; an unexplained absence never is. Require
  `VERIFIED → {OUTCOME_RECORDED | NO_RECORD_REASON=<measured>}`, or a broken extractor and an accurate
  predictor both report the same zero and neither is auditable.
- Repeating an unchanged condition on a schedule is escalation policy or nothing.
- A silent job is not a broken job. Silence is the designed state for P3.
- Do not notify on the mechanism working as intended; notify on the world changing.
- **A metric whose subject is a human's burden is INFO, never a gate.** Interruptions per completed
  objective, decisions per hour of human attention, questions per unit of machine work — measure it,
  trend it, and never let it fail a build. Gating such a number creates a gradient toward the failure
  mode it measures, because the cheapest way to improve the ratio is to stop reporting. Keep the
  irreversible / authority-bearing class outside the metric's reach entirely (constitutional lanes
  must reach the human regardless of any attention calculus), so the ratio can never be optimised by
  suppressing an escalation. The number is also only a proxy — a turn count is not attention — so it
  is a baseline to compare against, never a verdict about a human.

## Probe the function, not the health endpoint

A monitor that reads a service's own `/health` inherits that service's optimism. Observed
on one host, same hour: four bridges reported `active (running)` in systemd and
`READY`-shaped health JSON, while their credential file was a placeholder and their
functional status was `AWAITING_CREDENTIALS`. A green unit is not a working lane.

For any lane whose failure mode is *silence* (mail send, webhook, queue drain), the probe
must perform the smallest real operation that fails when the lane is broken — an
authenticated API call that returns the account identity, a read of the surface itself —
and must report `CANNOT_WITNESS` rather than `OK` when it cannot tell.

## Before authoring a monitor, look for the existing one

The real over-engineering signal is not size — it is duplication. Two agent sessions on
one host wrote a watcher for the same lane, in two directories, within the same hour;
neither was installed, and the host already carried 47 timers and 37 cron files. Search
systemd units, `/etc/cron.d`, crontab, and any duties/ directory for the condition you are
about to watch. If two exist, delete one — an uninstalled duplicate is cheaper to lose
than a second monitor that will drift from the first.

### Duplication is counted by invoked target, not by name

Names lie; the entry's invoked target does not. Extract the script or unit each entry actually runs,
across **every** surface, and group by that — the grouping is the duplication test. Several jobs
firing one script are one capability with competing implementations, not N capabilities.

Measured on one estate: 55 systemd timers · 40 `/etc/cron.d` files holding 106 rules · 54 root
crontab rules · 35 registry jobs · 100+ running services. A total taken from one surface understates
the estate by an order of magnitude, and the understatement is invisible because each surface looks
complete on its own.

**The instructive duplication is not the same script twice — it is N scripts answering one
question.** Two shapes worth counting explicitly, because neither is visible in any single file:

- **Reconciler fan-out.** Measured: six separate drift/reconciler units scheduled on one host, each
  carrying its own definition of drift, none cross-checking another. Their disagreements are
  unresolvable and every downstream reader picks one. Count per *question*, not per script name.
- **Gate towers.** Five independent gates inspecting one artefact, four of them inside a single
  26-minute window on the same cadence, is five chances to disagree about one fact.

**A stated reason is a claim, not evidence.** Paused and disabled entries carry a reason string, and
the reason can name a destination that does not resolve. Measured: a batch paused as "converted to
`/etc/cron.d/<name>`" where neither the file nor the prefix existed anywhere on the host — the work
had stopped silently while the record read healthy. Resolve the named destination before accepting
the pause, then classify rather than repeat: `LIVE` · `MIGRATED` (destination resolves **and**
contains the work) · `FALSE_MIGRATION` (destination absent — the work is gone) · `PAUSED_INTENTIONAL`
(the decider is named) · `ORPHAN`. `FALSE_MIGRATION` is the highest-value finding available: silent
death wearing a healthy record.

### Convergence order — never add to reduce complexity

1. **DELETE** entries that cannot justify an outcome — a job existing is not value.
2. **MERGE** physical entries serving one logical capability.
3. **CLARIFY ownership** when two surfaces claim one responsibility (`DUAL_ACTIVE_DRIFT`).
4. **SIMPLIFY the path** — fewer hops between trigger and effect.
5. **STANDARDISE the envelope** so every signal is routable by the same fields.
6. **REPAIR** what is genuinely broken.
7. **ADD a missing primitive — LAST.** Never solve complexity by adding another orchestrator.

**Optimise the institution, not each script independently.** Fifty individually clean jobs can leave
an estate more complicated than before if no step above reduced the moving parts, duplicate owners,
or sources of truth. The before→after must name the deltas — duplicate paths, sources of truth per
question, unowned work, human notifications — not the number of jobs tidied.

Then trim the design to the scar. A user asking "is this not over-engineering?" is usually
right. Cut, in this order: any list that reimplements what the platform already provides
(mail categories over a hand-built sender regex); prose ceremony in docstrings; and every
branch not tied to a named failure. Keep the branches that map to a failure you can point
at — for a disclosure watch, "can the lane read at all" and "was the reply actually sent"
are untrimmable; a severity-scoring scheme is not.

**But do not merge two unrelated concerns to avoid a timer.** Hosting a mail-credential
probe inside the machine-health probe was reverted for a real reason: a dead OAuth token
then reports `CANNOT_WITNESS` about the *host*, which is a false signal about the wrong
object. Reuse the existing **channel and conventions**; keep the concern in its own unit.
One more timer for a genuinely distinct failure is cheaper than a corrupted health signal.

## Support files

- `scripts/event-bridge.sh` — working adapter: delta gate, consequence-based severity,
  content-hash dedupe, append-only event log. Set `NOTIFY` and `STATE_DIR` at the top;
  wire as a separate cron entry one minute *after* the job producing the content so the
  two never race.

**Installed, not forked:** the silence/cadence probe described above already runs as
`/root/scripts/attention-metrics.py` (cron 4×/day, and wired into `hermes-chaos-sweep.py` as C21).
Run it by path — never copy it into another skill, which re-creates the drift the probe exists to
detect.

```bash
python3 /root/scripts/attention-metrics.py          # human report; exit 1 on any SILENT job
python3 /root/scripts/attention-metrics.py --json   # machine report
```

---
*DITEMPA BUKAN DIBERI*
