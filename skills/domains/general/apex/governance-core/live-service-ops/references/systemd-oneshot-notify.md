# Notify hooks on `Type=oneshot` units

A job that cannot report its own failure is not monitored — it is silent. These are the traps hit
when wiring `ExecStartPost` / `ExecStopPost` onto a oneshot unit so that it speaks.

## Which hook fires when

| Hook | Fires |
|---|---|
| `ExecStartPost` | only when `ExecStart` exited 0 |
| `ExecStopPost` | **every** exit — success, failure, deliberate stop, and restart |

`ExecStopPost` is the only hook that can report a failure, and for the same reason it is the one that
will report a success as a failure. Never alert unconditionally from it.

## The variables, and which one is authoritative

Probe what systemd actually passes rather than reasoning about it:

```bash
# /tmp/envprobe.sh writes the three vars to /tmp/envprobe.txt
systemd-run --unit=envprobe --collect --property=Type=oneshot \
  --property=ExecStopPost=/tmp/envprobe.sh /bin/true
```

On a **successful** oneshot the environment carries:

```
SERVICE_RESULT=success        # authoritative lifecycle verdict
EXIT_CODE=exited              # a disposition WORD — not a number
EXIT_STATUS=0                 # the numeric exit status
```

- `SERVICE_RESULT` is the verdict: `success`, `exit-code`, `signal`, `timeout`, `watchdog`,
  `core-dump`.
- `EXIT_CODE` is a **word** (`exited`, `killed`). Comparing it to `"0"` is always false, so a run
  that succeeded is announced as a failure — on a unit that was working correctly the whole time.
  The script's own log will then contain the two contradictory facts side by side
  (`service_result=success` on the same line as `result=FAILURE`), which is the proof the comparison
  is wrong, not the job.
- The numeric status is `EXIT_STATUS`. Test `SERVICE_RESULT` first; consult the status only as a
  secondary signal.

## `$SECONDS` is always ~0 in a hook

`SECONDS` counts from the start of *the shell running the hook*, and a short-lived `ExecStopPost`
starts fresh — so a duration computed from it reports `0s` no matter how long the job ran. A
fabricated duration is worse than no duration, because it reads as a measurement. Log
`see systemd journal for dur` instead, and take the real span from the unit's own timestamps:

```bash
systemctl show <unit> -p ExecMainStartTimestamp -p ExecMainExitTimestamp
```

## Separate a deliberate stop from a failure

A restart, a manual start, and an operator cleaning up all fire `ExecStopPost`. Without a state flag
they are indistinguishable from a crash, so every maintenance action pings the alert channel with a
false FAIL. Gate the alert on the lifecycle verdict, and treat a non-zero `SERVICE_RESULT` as the
only alarm condition.

## Test the hook on all three branches

A notify path is verified only when each branch has been exercised: clean success, non-zero exit,
and signal. Drive them deliberately rather than waiting for a real failure to arrive.

**Route test output away from the production channel.** A self-test that writes into the channel the
alarm uses turns that channel into a junk drawer, and the first real alert lands after the reader has
already learned to ignore it. Test into a local log or a scratch target; the production channel
carries real verdicts only.

## What good output looks like

One line, naming the state achieved — not a bare emoji plus a timestamp:

```
✅ <job> OK @ <ISO ts> (<SERVICE_RESULT>)
❌ <job> FAIL @ <ISO ts> result=<SERVICE_RESULT> status=<EXIT_STATUS>
```

Carry the invocation identifier so a reader can join the line to the unit's journal entry. A verdict
with no joinable ID is an event, not a receipt.

## Confirm the run finished, not just that it started

`ExecStartPost` fires the moment `ExecStart` exits, and a long job may still be writing. Judge the
outcome from the artefact the job produces — the new output file, the advanced counter, the sealed
record — never from the hook's own early line.
