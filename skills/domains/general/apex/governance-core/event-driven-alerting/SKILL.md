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

Self-test before shipping an alert format: strip the emitter and hand the line to
someone who has never read the code. If they cannot state what each token's role is,
the format is not finished.

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

## Counter-rules

- A clean run is P3. "X succeeded" is not news.
- A job that only *starts* something is not a receipt — a receipt needs verified end state.
- Repeating an unchanged condition on a schedule is escalation policy or nothing.
- A silent job is not a broken job. Silence is the designed state for P3.
- Do not notify on the mechanism working as intended; notify on the world changing.

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

---
*DITEMPA BUKAN DIBERI*
