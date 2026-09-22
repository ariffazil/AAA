---
name: background-monitor-design
description: Use when building a standing monitor or alert tripwire.
version: 1.0.0
tags: [monitoring, tripwire, cron, alerting, verification]
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# Background Monitor Design

A monitor is not merely a script on a schedule. It is a **claim about the world
that stays true until it speaks** — "nothing has changed" is the message of every
silent tick. Design it so that claim cannot be false.

## When to use

Building, repairing, or reviewing anything that watches and alerts: a news or topic
tripwire, a drift watchdog, a threshold alert, a feed monitor, a "tell me when X
happens". Load this before writing the script, not after the first false alarm.

## The one rule

> **Silence means "I checked and there is nothing to report" — never "I could not
> check."** A monitor that dies quietly is worse than no monitor, because it turns
> absence of signal into assurance.

Every design decision below follows from that rule.

## Corollary: gate the WRITER, not just the reader

The rule above is usually implemented on the read side (a gating command that
suppresses the agent). That is not enough. A monitor that writes one record per
tick regardless of change is the same defect wearing a different hat: silence is
preserved, but the pile grows, and every future sweep pays for it.

**Measured case (2026-09-20, KVM8):** a drift watchdog wrote one
`drift-<ts>.json` per 60s probe for 45 days — 38,282 files, 219.6 MB, **100% HOLD
across the full census (38,280 readable)**, a single reason class, **46% of writes
byte-identical duplicates** (17,379 of 20,903 timestamp groups held >1 file;
400/400 sampled groups identical after stripping volatile timestamps), and **zero
readers anywhere on the box**. It changed no decision in 45 days. Deleting the
writer and gating it on state transition cost one commit and reclaimed 219.6 MB.

Design rule: hash the report with volatile fields stripped (timestamps, latency,
durations) and write an event record **only when the signature differs from the
last persisted one**. Keep exactly one always-current state file (overwritten in
place) so the monitor's current view is readable without scanning a pile.

```js
// strip clock fields so the signature tracks STATE, not time
const sig = sha256(JSON.stringify(strip(report, ['checked_at','detected_at','latency_ms'])))
if (sig === readLastSignature()) return false;   // no transition -> no new record
writeEvent(report); writeLastSignature(sig);
```

Three questions before shipping any monitor:
1. **Who reads this output?** If the honest answer is "nobody yet", write to one
   current-state file and stop. A record with no reader is archive, not governance.
2. **Has this alert ever changed a decision?** Sample the whole population, not a
   convenient slice — a 500-file sample said "100% HOLD"; the full census proved it.
   If the answer is zero over a month, the alert is a wallpaper generator.
3. **Does the writer have a rotation rule?** An event-per-tick writer on a box with
   no logrotate is a disk leak with a schedule. Add the rule in the same commit.

Prefer replacing an event emitter with a **state-transition emitter**. This is
attention-kill-criterion applied to behaviour: stop verifying when additional
verification cannot change a decision.

## Corollary 2 — the ALERT path needs its own anti-storm window

Gating the writer fixes the file pile. It does **not** fix the human channel. An emitter
that notifies once per *emission* rather than once per *condition* spends the channel's
credibility even when every individual message is correct.

**Measured:** one standing condition produced **six identical P1 alerts to a human channel in
50 minutes**, each with a fresh `trace_id`. The reader could not separate "still broken"
from "broke again" — and those have opposite responses. The emitter had already computed a
perfect condition identity (`idempotency_key = sha256(source|state|action)`) and **never used
it**: the identity existed and was discarded.

```
fingerprint = sha256(source | state | action)      # a CONDITION, not an event
first occurrence              -> notify
repeat inside window          -> record suppressed=true, send to the human channel: nothing
window lapses, still broken   -> notify once        # "still broken" must stay audible
any field changes             -> new condition, notify
```

Three implementation rules, all load-bearing:

- **Compute the verdict BEFORE the durable append and store it in the record**
  (`dedup: {fingerprint, first_seen, suppressed_since}` plus `suppressed: true`). If the record
  is written first and the verdict attached afterwards, the ledger cannot distinguish
  *delivered* from *suppressed*, so the anti-storm is invisible to every later auditor — and the
  fix cannot be shown to work.
- **Seed the window when deploying onto an already-storming condition.** Otherwise the next tick
  notifies once more and the storm you just fixed is blamed for a message it did not send.
- **Anchor the window to the last ANNOUNCEMENT, never to the first sighting.** The predicate is
  `(now − last_notify) > window`, not `(now − first_seen) > window`. Measured: a six-hour window
  computed from first-seen becomes permanently true once a condition has lived six hours, so every
  later emission notifies — dedup is not weakened but **disabled**, and disabled for exactly the
  standing conditions it exists to throttle. The function's own docstring stated the correct contract
  ("repeats inside the window are suppressed; after it lapses, re-notify once") three lines above the
  code contradicting it, so read the predicate, not the prose. A fix that introduces the dedup
  function and the wrong anchor in the same edit is still broken; verify the predicate line, not the
  file's mtime.

**Derive the alert's action text from the verdict reason, never from a fixed string.** Measured: an
alert read `ACTION=inspect <guard> HOLD on durable bus` while the failing subsystem was a cold read
on a *different* organ and the bus was healthy — its own canary reported `ok=true`, its consumer was
active. A hand-written action line points the responder at the wrong subsystem and is never
re-derived when the cause moves.

**An envelope that lists the payload's KEYS instead of carrying its values has dropped the alarm.**
Measured: every surviving alert carried `extra.payload_keys = [type, schema, subject, reason, source,
timestamp, details]` — the field names, with no `reason` and no `details` anywhere in the record. The
severity reached the channel and the finding did not, so no reader could act, and the envelope still
read as complete. Treat this as its own defect class, distinct from a missing alert:

- **Assert the alert body contains the reason STRING, not the reason's field name.** A test that
  matches on `reason` being present passes on a payload that only names it.
- **A key-list is a transformation receipt.** Where `payload_keys` appears, something mapped the
  payload to its schema and kept the schema; find the mapper, because it is silently dropping fields
  on every other message routed through it too.
- **Report the loss as the finding.** When the alarm cannot say what it is alarming about, the
  incident is unactionable *and* the record of it is gone. Say both, and never reconstruct a reason
  from the surrounding metadata.

## Corollary 3 — the SILENT state needs a real destination

The rule at the top ("silence means I checked") assumes the agent has somewhere to *be* silent.
When it does not, the only available way to demonstrate compliance with "say nothing" is to
**announce that it is being silent** — and the announcement lands in the one channel it was
supposed to stay out of.

**Measured:** nine prose compliance markers (`[silent — …]`, `[A0 SILENT — …]`) were posted into a
human channel by a lane whose own doctrine forbade exactly that, over one session. The lane's own
diagnosis was right: its silent state was a **concept, not a destination**, so talking about not
talking was the only proof of compliance available to it. That is a missing sink, not a discipline
failure — and the same shape appears whenever a monitor is told to stay quiet without being given
a place for the quiet.

Design rules:

- **Give the non-event a destination** — an append-only record, or nothing at all. Then assert the
  destination does **not** feed the human channel.
- **A sink must have a reader, or it is a slow leak.** A write-only record of non-messages is the
  corollary-1 defect again: it grows, nobody reads it, and it becomes another pile to sweep. Pair the
  sink with an aggregate that states counts by reason and a one-line verdict, and emit that to a
  human only when the distribution **changes**.
- **Do not add a compliance-marker value to a triage enum.** An enum whose question is "does a human
  need to act?" has exactly two useful answers plus a null. Adding a value meaning "the structure
  made me speak" turns a decision enum into a bag, and the bag fills with records about itself. A
  structural defect belongs in a defect note with a date and a finder — not in the record stream.
- **Retrofitting old markers into the sink is not classification.** Rewriting past announcements as
  tidy records is absolution wearing a schema; the violations stay violations in the audit trail
  that already carries them. A sink governs behaviour from its creation forward.
- **The success metric is the HUMAN CHANNEL getting quieter — not the sink getting fuller.** A sink
  that fills with "nothing happened" has renamed the noise rather than removing it.

## Corollary 4 — a monitor must DATE what it reads, not just read it

The one rule ("silence means I checked") has a sibling failure: **the monitor checked
something that was itself frozen.** A count read from a file the monitor never dates renders
identically whether that file is live or has not been written in days, so the monitor reports a
healthy subsystem forever while its subject has stopped.

Observed: a daily compliance report printed `Seal chain: 267 entries, last seq=40`. Five
consecutive daily reports printed the identical line. The file's mtime was four days old and its
final entry timestamp matched — the chain had stopped being written, and the report had no way to
say so. Live seal activity was being recorded in a *different* file the report never read.

Three rules follow:

- **Print the source's age beside its value** (`entries: 267 (written 4d ago)`), and emit `STALE`
  past a declared threshold instead of a bare count. A number without a clock is not a reading.
- **Assert freshness in the monitor itself.** No downstream reader can recover a timestamp the
  report did not emit, so this cannot be delegated to whoever consumes the output.
- **When a subsystem has more than one candidate store, confirm which one the WRITER appends to
  before treating a quiet store as health.** A frozen mirror and a healthy pipeline are
  indistinguishable from the reading side; only the writer's target separates them.

## Corollary 5 — a metric must be computed on one unit

A score is meaningful only if its numerator and denominator count the same thing. When the
denominator counts **subjects** while the numerator is decremented once per **failure axis** per
subject, one subject with two faults removes two from the top and adds one to the bottom — and the
score can print negative.

Observed: a compliance percentage computed `passing = checks − issues − warnings`, where `checks`
counted each skill once while `warnings` incremented once per missing field per skill. With 286
skills and two possible warnings each, the worst case is 572 warnings against 316 checks → −81%.
The arithmetic on the day was internally consistent; the defect was semantic and would only surface
at scale.

- **Score per axis, or score per subject — never mix.** Either the denominator counts every axis,
  or the numerator loses at most one point per subject.
- **Clamp and label a ratio of unlike quantities** (`coverage 0.00 [ratio, not calibrated]`) rather
  than letting it print a negative percentage.
- **Sanity-bound every derived percentage before shipping it** — `0 ≤ pct ≤ 100`, asserted in code,
  not assumed from the domain.

## Corollary 6 — a status table may contain only rows something computed

A report that prints a pass mark for a check it never ran is a **false attestation**, and it is
worse than an absent row: a reader greps the table, finds the control, and concludes the control
exists.

Observed: a compliance report's "Floor Compliance Matrix" printed literal pass marks for six of its
seven rows — the marks were strings written into the generator, not produced by any check. Only the
seventh row was computed. None of the six could ever have failed.

- **Emit a row only where a check feeds it.** No check → the row reads `NOT_MEASURED`, or the row
  is removed. Never a literal in a table headed "compliance".
- **Audit a self-measurement report by reading its generator, not its output.** Four defect classes
  to look for, in this order: literal pass marks; checks whose search space cannot see what they
  claim to check; denominators that do not match the axes being scored; and reads with no freshness
  assertion (Corollary 4).
- **Do not repair another organ's self-measurement instrument.** Specify the repair and hand it
  over — editing what an institution reads about itself is a change to its self-knowledge, and it
  belongs to that organ's owner, not to the auditor who found the defect. Report the defect, name
  the fix, stop there.

## Corollary 7 — a window check must read the subject's own schedule

A reconciliation that asks "did this fire today?" — evaluated at a time of its own choosing — flags
every subject whose fire time is still in the future. The alarm is not merely noisy; it is **wrong by
construction**, and it repeats identically every single day.

Observed: a daily declared-vs-observed reconciliation ran at 06:50 and listed two enabled daily jobs
(one firing 07:15, one 14:00) under "enabled jobs that did not fire today". Both fired normally, hours
later, every day. The check compared against the **elapsed calendar day** instead of against **each
subject's own scheduled instant**.

Rules:

- **Compare against the subject's schedule, not against the window you happen to run in.** A subject
  whose fire time has not yet passed is `PENDING_TODAY`, never `MISSING`. Anything else makes the
  monitor permanently red, and a permanently-red monitor stops being read — which loses the real signal
  it existed to carry. An alarm that always fires is not an alarm.
- **Prove it with two fixtures, in both directions.** A subject scheduled later today must NOT be
  flagged; a subject whose time has passed and which genuinely did not run MUST be flagged. One fixture
  without the other proves nothing, because a check that flags nothing also passes the first case.
- **Existence is not execution.** An output directory, a log file or a state blob persists forever, so
  `ls` over it answers "has this ever run", not "did it run inside the window under test". Take the
  timestamp from an execution record and bound it to the window. A leftover artifact is precisely what a
  stale subject leaves behind, so the two are indistinguishable from the filesystem alone.
- **A disagreement between two observers is information; the silence around it is the defect.** When a
  health surface and a reconciliation surface over one system carry opposite verdicts, do NOT reconcile
  them by editing one to match the other — that destroys an independent witness. Make the disagreement
  an explicit field with its own severity class, so neither surface can be read alone without seeing it.

## Corollary 8 — the side effect goes AFTER the acknowledgement

A consumer that does its irreversible work before acking turns every redelivery into a duplicate
delivery. With `ack_wait=30` and `max_deliver=5`, one message can fire the side effect five times with
no restart at all — and recreating the consumer on restart resets the delivery count, so the
amplification is unbounded across restarts.

Measured: a governance alarm appended to a ledger and notified a human channel **before** `msg.ack()`.
A service restart at T produced re-emissions at exactly T+30s — the `ack_wait`, on the clock, not
inferred. One underlying condition reached the ledger 53 times under 53 distinct `trace_id`s, because
the identity was minted inside the emitter instead of carried from the message.

- **Ack before the side effect, or key the side effect on the transport's own message id.** Either
  ordering or idempotent keying works; neither is optional.
- **Never mint the correlation id inside the emitter.** A fresh `trace_id` per pass makes one
  condition look like N first-occurrences to every consumer that keys on trace — and trace is the
  field the doctrine tells consumers to key on. Carry the id from the message.
- **A bounded idempotency window over an unbounded store is not idempotent.** `readlines()[-1000:]`
  against a 93k-line append-only ledger left 82.5% of prior records invisible to the guard, so each
  pass re-sealed them: 73 duplicated ids, 103 excess records — permanent, because the ledger was
  `chattr +a` and duplicates in an append-only store can only be marked superseded, never removed.
  Scan the whole store, or keep the seen-set in its own bounded index; never in a tail window of the
  thing you are appending to.
- **A quiet alarm is not a fixed alarm.** Those emissions stopped because the redelivery cap was
  reached, not because anything was repaired, and the loop resumed on the next restart. Before
  reporting a storm as over, check whether the *cause* changed (the predicate line, the file mtime)
  or only the *counter* ran out.
- **A detection that auto-spawns work is an amplifier.** When "DOWN detected" creates an
  investigate-task, one transient becomes consumed human and agent attention. Gate the spawn on the
  same confirmation the alert needs, or the monitor manufactures the workload it exists to prevent.
- **Two independent causes need two fixes.** This loop had both an emit-before-ack ordering defect and
  an inverted dedup window; repairing either alone left the other firing. Before declaring a storm
  root-caused, ask what else could produce the same emission and check it separately.

## Procedure

1. **Decide the detection, then the delivery.** Write down (a) the precise
   observable that constitutes a hit, and (b) who must be told, and how soon. A
   monitor without a named reader becomes a log nobody opens.

2. **Prefer a deterministic script as the change-detector.** Where the scheduler
   supports a cheap gating command (Hermes cron: the `monitor` field), use it. It
   runs each tick at zero token cost; byte-identical output suppresses the agent
   entirely and only a real diff wakes it. Reasoning is then spent on the diff, not
   on deciding that nothing happened.

   The gated output MUST be stable byte-for-byte when nothing changed. A timestamp
   or non-deterministic ordering on that path makes every tick look changed and
   defeats the gate completely.

3. **Seed the baseline before the first scheduled run.** A cold start has no
   seen-set, so every historical item matches and the first tick dumps everything at
   once — which destroys the channel's credibility on day one. Ship a `--baseline`
   mode that records current items silently, and run it once.

   ```bash
   python3 <script> --baseline    # seed seen-set, print nothing
   python3 <script>               # now silent unless genuinely new
   ```

4. **Dedupe on a stable identity, and bound the seen-set.** Hash the link (or a
   normalised title), never the position. Cap the set and evict oldest-first so
   state cannot grow without limit.

5. **Guard the void explicitly.** If every source fails, emit a loud CANNOT-WITNESS
   line. Never let total source failure produce an empty tick. Where one upstream is
   all you have, wire a fallback and record which lane answered — partial loss stays
   quiet but stays recorded, so degradation is visible without alert spam.

6. **Fire-test the alarm** — see the next section. A monitor whose alarm path has
   never executed is untested code wearing the shape of a safeguard.

7. **Pair it with an unconditional heartbeat.** A separate job reporting health on a
   fixed schedule whether or not anything happened, so the *absence* of that report
   is itself the signal that the engine died. Keep state in a queryable file with a
   `--health` probe so the heartbeat is a single command with no parsing.

8. **Wire the schedule to the real cadence of the underlying event**, not to
   convenience. A daily check on something that changes hourly is a sampling error,
   not a monitor.

## Testing the alarm — both directions

```
1. Let it run clean once.     Expect: silence.
2. Un-seed exactly one known item.
3. Run.                       Expect: exactly one hit, naming that item.
4. Run again.                 Expect: silence.
```

Step 3 proves the alarm can fire. Step 4 proves it does not re-fire — a monitor that
re-alerts the same item every tick gets muted by its reader, and a muted monitor is
dead. Skip either step and you have an assertion, not a monitor.

### Prove the RECEIVER, not just the sender

A log line saying `alert published` proves the publisher ran. It proves nothing about
whether anyone heard — and a log is exactly where a dead alert path hides, because it
reads like success. **Enumerate the live subscribers on the exact channel before
trusting the path**, then prove the lane end-to-end with a synthetic message.

```bash
# e.g. NATS: map subject -> connection. A subject no connection holds = a void.
curl -s 'http://127.0.0.1:4222/connz?subs=1'   # or the transport's own subscriber census
```

Measured: a drift watchdog published `888_HOLD` on every drift for months, logging
success each time. A subscriber census found **zero** listeners on that subject while a
live consumer sat on a differently-named subject, 42k messages deep. The alarm was
real on the wire and reached nobody. Repointing the subject and publishing one test
envelope — then reading the *consumer's* log to see it arrive — turned it live.

**Keep verdict semantics in the PAYLOAD, not in the channel name.** Encode what kind of
alarm it is as fields inside the message (`type`, `schema`, `subject`). A channel whose
meaning exists only in its name is a channel that gets renamed into silence, and any
consumer has to reverse-engineer the type from the address.

## Failure taxonomy — do not collapse these

| State | Means | Action |
|---|---|---|
| SILENT | checked, nothing new | none — this is the normal state |
| HIT | new matching item found | judge churn, then report |
| CANNOT WITNESS | every source failed | alarm: the monitor is blind |
| DEGRADED | some sources failed, others answered | record it, stay silent |
| DEAD | consecutive total failures past threshold | alarm via the heartbeat path |

Reporting DEGRADED as SILENT is the defect that makes a monitor dangerous.

## Precision beats sensitivity

A monitor that pages on every tangential match trains its reader to ignore it. A
false alarm costs more than a missed one because it spends the channel's
credibility, and a discredited channel cannot be spent again.

Where the domain has natural two-part structure (a subject AND an action), require
co-occurrence rather than either term alone. Tell the woken agent to judge churn
before it reports, and give it explicit permission to answer "churn, ignoring" so
that saying nothing is a valid, expected outcome rather than a failure.

## Pitfalls

- **"Alert published" in the log is not delivery.** Prove the receiver: enumerate the
  live subscribers on the exact channel and watch a synthetic message land in the
  consumer's own log. A path with no subscriber reads as healthy forever.
- **A `last_status=error` from an older run is not a current failure.** Compare the
  monitor's `last_run_at` against the mtime of the artefact it guards; if the fix
  landed after that run, the error is stale and clears at the next fire.
- **Do not resolve an unacknowledged signal by silently re-baselining.** Preserve the
  prior baseline as a receipt naming what was acknowledged and what was *not*
  independently verified; then re-baseline. Erasing the signal is the failure the
  monitor existed to prevent, and a gate that can only stay red stops being read.
- **A timestamp anywhere in the gated output makes every tick look changed.** Strip
  clocks from the deterministic path; keep timing in a log, outside the gate.
- **Do not point delivery at a shared channel by default.** Alerts about a standing
  risk go to the operator who owns the risk. A group channel turns a false alarm into
  a social cost, which pressures future tuning toward silence.
- **Verify the source resolves before trusting its content.** A feed that answers
  proves the feed exists — not that its items support the claim you attach to them.
  Keep resolution-checking and content-judging as separate steps.
- **One upstream is a single point of blindness.** If it goes down you cannot
  distinguish quiet from broken — the exact failure the whole design exists to prevent.
- **Naming an artefact after a guarded vocabulary word** can make every later command
  that references it fail an unrelated content gate. Name for the concept, not for the
  noun that trips the guard.
- **An empty capability list from a live service is a failed read, never a removal.** A watchdog
  that probes once and sees zero tools will emit `TOOL_REMOVED` at CRITICAL. Require a confirm
  probe before emitting drift: a service that answers with a full list on the retry was cold, not
  broken. A "differed-then-matched" transient filter **cannot** catch this — a consistently cold
 first read never differs from the cold baseline, so it presents as a permanent change. Never pin
 a cold read; if a known-cold endpoint exists, warm it or widen the probe, do not report it.
 Generalise to every negative verdict: **confirm across lanes, not only across time.** A single HTTP
 probe on a 3s timeout, fired while several timers cold-start together, reports DOWN for healthy
 organs. Retry, then fall back to a *different* lane — a bare TCP connect separates "process gone"
 (refused) from "endpoint slow" (accepted). Only when every lane fails is the subject down. Prove the
 fix in both directions with two fixtures: inject a transient first-failure and assert the verdict
 stays UP; then fail every lane and assert it still reports DOWN. Testing only the first direction
 cannot tell a hardened probe from a probe that lost its detection entirely.
 - **A doctrine that lives only in prose is not wired into the probe.** An alternate-lane rule can be
 ratified, documented, and cited while the monitoring code still does one `urlopen` and labels the
 result. When a false negative survives a rule that should have prevented it, grep the *code path*
 for the rule before concluding the rule is wrong — the usual finding is that nobody connected them.
 Wiring an existing rule into the path that runs is not adding a rule.
- **Isolate EVERY output path before you exercise an emitter.** A test that redirects the state
  directory but not the receipt log writes its fixtures into a production ledger. Enumerate the
  paths from the source (`grep -n 'Path(\|\.open(\|append' <module>`) and redirect all of them,
  rather than redirecting the one you happen to remember. Repair by **quarantine with a manifest**
  — move the records out and record their original location — never by deletion: the ledger is
  evidence about the emitter, including about its own test pollution.
- **A monitor that reports a healthy subsystem as the cause is a reporting defect, not a
  monitoring one.** When the alert text and the verdict disagree about which object failed, the
  alert is wrong by construction. Derive the action/source fields from the measured verdict.
- **Verify the schedule before naming a cause — especially in a comment.** A cause written into a
  source comment outlives the session and is read as established fact by everyone after. Measured: a
  "three timers cold-start together" explanation went into a fix's docstring, then was falsified by
  reading the timers — one of the three fired a quarter-hour earlier and could not have collided.
  Read each subject's own fire time (Corollary 7) before asserting a collision. Where the cause is
  genuinely unresolved, write `CAUSE NOT FULLY ESTABLISHED` plus what was excluded, and make the fix
  robust to any single-lane transient so its correctness does not depend on the open question.
- **A repeated alarm from a peer is a mirror, not new evidence.** When the Nth relay of one finding
  arrives, do not produce another layer of analysis; confirm what changed since the last reading and
  stop. Re-reporting a symptom you already root-caused adds the auditor's own noise to the storm.

## Reference implementation

- `templates/monitor.py` — working skeleton implementing the silence contract,
  baseline mode, dedupe with bounded state, the void guard, and `--health`. Copy it
  and edit the config block at the top.
