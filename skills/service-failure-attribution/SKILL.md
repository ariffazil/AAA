---
name: service-failure-attribution
description: Use when a service died or a monitor cries crash-loop.
version: 1.0.0
tags: [systemd, incident, attribution, journal, service, restart, forensics]
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# Service Failure Attribution

> A restart that lands before attribution converts an explained death into an unexplained
> recurrence. Repair is the last step, not the first.

When a unit reports `failed`, a monitor cries "crash-loop", or a supervisor proposes a restart,
the useful output is **who ended it and why** — not a green status afterwards. This skill is the
order of evidence: journal before action, mechanism before blame, guarded repair last.

## When to use

Any `systemctl status` showing `failed`, any `OnFailure=` alert, any "service X is down" claim from
a peer or monitor, and any proposal to auto-restart. Also when several units are found `inactive`
with no alert at all — that is the silent class and it looks like a clean shutdown.

## Rule 1 — read the lines BEFORE the failure, never after

```bash
journalctl -u "$UNIT" --since '-30 min' --no-pager | grep -nE 'Triggering OnFailure|Main process exited|Consumed'
# then read upward from the FIRST of those lines
```

- The cause sits *above* `Triggering OnFailure`; everything below it is the restart, i.e. the corpse
  moving. Quote the last few lines before the trigger and nothing after.
- **Separate signal from exit code.** `Main process exited, code=exited, status=1/FAILURE` after a
  clean drain is a SIGTERM stop being reported as a failure — a deliberate stop and a crash are
  different verdicts with the same exit code.
- Look for `Shutdown context: signal=SIGTERM under_systemd=yes` in the app's own log. That line, not
  the failed unit state, tells you the process was asked to leave rather than dying.

## Rule 2 — `Stopping <unit>` present or absent is the discriminator

| Journal shows | Mechanism |
|---|---|
| `Stopping <unit>.service` | `systemctl stop/restart` — a job was queued, the unit manager did it |
| `Deactivated successfully` with **no** `Stopping` line | SIGTERM delivered straight to the PID — killed by a process, outside the unit manager |

- Absence of a `Stopping` line is positive evidence of a direct kill, not missing data. Count it:
  `journalctl --since '-6h' | grep -c "Stopping $UNIT"` → 0 means nobody asked systemd.
- A direct kill leaves **no unit-scope trail in the journal**, so stop grepping the journal for a
  culprit. Pivot to the sender's cgroup (Rule 3).
- Order of kills matters: several units dying seconds apart with no `Stopping` lines is one actor
  cleaning house, not several coincidences. Report it as one event.

## Rule 3 — attribute a direct kill through the session cgroup

```bash
journalctl --since '-30 min' | grep -i 'systemctl'      # caller PID + its scope
# e.g. Reload requested from client PID 2831849 (unit session-28790.scope)
cat /sys/fs/cgroup/user.slice/user-0.slice/session-28790.scope/cgroup.procs \
  | while read p; do ps -p "$p" -o pid=,ppid=,comm=,etime=; done | awk '$2==1'
```

- The **PPID=1 process inside the scope is the owner**: a long-lived agent/daemon started from that
  session is the actor, not the shell that typed the command.
- A transient scope stays `active (abandoned)` long after its command exited — the scope name and its
  live descendants are still the attribution, so read them before the scope is reaped.
- When the actor is an **agent doing auto-recovery**, the finding is not malice and not a mystery: it
  is a second automation racing the first. Name the PID and skip the hunt for an intruder.
- If the trail is genuinely absent (no scope line, no auditd, empty shell ledger, no matching cron or
  timer), write `UNKNOWN` with the list of places you looked. An honest unknown beats a plausible
  culprit; false attribution gets a working agent blamed and left running.

## Rule 4 — memory peak in a stop line is not a leak

`Consumed 23min CPU time, 6G memory peak, 567M memory swap peak` is a **lifetime** high-water mark
for that process incarnation. A process that lived for hours and served bursts reaches a large peak
while being perfectly stable.

- A leak claim needs a **trend**: repeated RSS samples rising without a matching load rise, or a kill
  by the kernel (`oom-killer`, `Killed process`). Without either, peak is capacity data, not cause.
- Clean the instrument before the absence claim:
  `journalctl ... | grep -ciE 'oom|killed process|address already in use|MemoryError'` — a zero from a
  pattern you have **proven** matches on a known-positive sample is evidence; a zero from an untested
  pattern is not (see Rule 6).
- Do not add a `MemoryMax` cap as the first response to an exit already attributed to an external
  signal — that treats a symptom of someone else's behaviour.

## Rule 5 — classify on lifecycle events, not on words in the log

A diagnostic that greps the whole journal for `traceback`, `error`, or `timeout` will classify a
healthy unit as broken, because a long-lived service's journal contains **its own agents'** tool
errors. Observed shape: unit `running/active` while the classifier returned `traceback` — the string
came from a failed tool call inside the service, not from the service failing.

- Restrict matching to lifecycle vocabulary: `SIGTERM`, `Stopping`, `oom-killer`, `Main process
  exited`, `Start request repeated`, `Failed with result`.
- Classify by **what recurs**, not by what is loudest. If the journal is 45% one repeated warning and
  one line of `Traceback`, the recurring condition is the finding and the traceback is an echo.
- Never let a classifier's label drive a restart recommendation on its own. `status=running` plus
  `classification=traceback` is a contradiction to surface, not an instruction to act.
- Same rule for fleet digests: "all organs healthy" is false the moment any member of the set was not
  reached. Name the unreached ones or downgrade the sentence.

## Rule 6 — validate the measuring command before reporting a zero

Every negative finding ("0 OOM lines", "no remaining hardcoded entries", "nothing commented out")
is a claim about your instrument. Prove the pattern on a known-positive line first.

- **Anchor the pattern on a line you have already seen.** A regex demanding a leading `-` before
  `api_base:` returns 0 against a file that indents it without the dash — the config was restored, the
  grep was wrong. Print one matching sample from a file you know contains it before believing a zero.
- **Never count status digits in a log that also prints ports.** `grep -c '402'` matches `:54402` and
  `:47402`; real failures can be zero while the digit count is 23. Match the **message text**
  (`Insufficient Balance`, `Authentication Error`), and use a strict form (`" 402 `) if you need both.
- State the pattern alongside the count, so the next reader can falsify the instrument rather than
  the system.

## Rule 7 — repair is guarded and last

- `systemctl stop` → `reset-failed` → `start` is not a repair; it clears the evidence of the cause,
  and `reset-failed` also clears the counters a rate guard depends on. Evidence first, then one
  deliberate restart, attributed in the receipt.
- **A planned stop must not trigger a crash-loop alert.** `OnFailure=` fires on `exit=1`, which a clean
  SIGTERM drain produces. Guard the alert script:

```bash
if journalctl -u "$UNIT" --since '-10 min' --no-pager -q | grep -q "Stopping $UNIT"; then
  echo "planned-stop guard: suppressed" >> /var/log/<alert>.suppressed.log; exit 0
fi
```

  Real crash loops auto-restart **without** a `Stopping` line, so they still alert. Test both branches
  before shipping (`bash -n` plus one synthetic line each way).
- After any restart, report the discriminating three: unit state, the reason string, and the counter
  that would expose a second death — not just `active`.
- Restarting a unit whose failure you attributed to an **external killer** buys time and nothing else;
  say that out loud instead of presenting green as resolution.

## Counting depth (inline, no reference file)

- **Window is part of the number.** `--since/--until` gives the real window; `-n 40` is a slice; a
  classifier fed a narrow tail sees 3 lines where 43 exist. State the window next to every count. A
  spec's "last 40 lines" is a **ceiling**, not a promise — fewer lines may exist.
- **Two sources, two numbers.** A unit journal and an app error log are different instruments over
  the same events; when they disagree, report both with their scope rather than picking the nicer one.
- **Quote the seam, not the wall:** 3–6 lines around the decision point (`Stopping`, `SIGTERM`,
  `Main process exited`, `Triggering OnFailure`) plus a count for the rest. A pasted log wall trains
  the reader to skim.

## Related

`probe-instrument-trust` (making the probe itself trustworthy), `restart-boundary-verification`
(verifying state on the far side of a reload), `silent-failure-detection` (systems that claim success
without landing it), `incident-response` (escalation once attribution is settled).
