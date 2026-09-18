---
name: background-monitor-design
description: Use when building a standing monitor or alert tripwire.
version: 1.0.0
tags: [monitoring, tripwire, cron, alerting, verification]
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
- **Do not let the monitor act.** A monitor reports; remediation is a separate,
  separately-authorised step. A self-healing watchdog that patches what it watches is
  a mutation with no gate in front of it.

## Reference implementation

- `templates/monitor.py` — working skeleton implementing the silence contract,
  baseline mode, dedupe with bounded state, the void guard, and `--health`. Copy it
  and edit the config block at the top.
