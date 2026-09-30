---
name: live-worker-session-relay
version: 1.0.0
description: "Use when relaying a decision into a live worker session."
tags: [worker, checkpoint, relay, pty, self-report, evidence, agent-orchestration]
risk_tier: medium
floor_scope: [F2, F4, F7, F11]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Live Worker Session Relay

Class: a worker agent (coding CLI, subagent lane, cron-driven agent) is running, has paused
mid-execution and posted a checkpoint, and the human answers it. Two jobs, in this order —
**verify what the checkpoint claims, then get the answer into the session that is still
running.** Skipping the first job means relaying a wrong diagnosis as an order; skipping the
second means the answer never arrives and the worker stalls on a question already answered.

## Job 1 — a checkpoint is a self-report, not sensor data

A worker reporting its own state is emitting prose. Banners, dashboards and status files are
narratives; only the machine surface is a witness. Before endorsing, relaying, or acting on a
checkpoint's diagnosis:

1. **Trace the verdict to the authority surface, not the worker's paraphrase.** Consequential
   states carry their own `reason_code` and `reason_evidence` with an evidence tier
   (`MEASURED_FACT` vs `DERIVED`). That field outranks the narrative wrapped around it. A worker
   can report "state X because thresholds p/q" while the authority surface says the cause is
   something else entirely — and the two fixes are different.
2. **Separate federation-wide baseline scalars from the actor's own scores.** A baseline
   windowed over days and labelled as a reference is not the current session's number. Quoting
   the baseline as the session's score invents a threshold breach that is not there; quoting the
   session's score as the federated one invents a pass. Read the label.
3. **Re-probe every component the worker named** — done, down, blocked, reloaded. `docker ps`,
   `systemctl is-active`, the organ's own `/health`. One probe settles each of them, and the
   worker's own report is not the probe.
4. **Check whether the claimed blocker is even causal.** A worker's plan can contain a fix for a
   mechanism it never verified. If the named cause and the named fix are not connected, the step
   is theatre and completing it produces a false green.

### Never relay a step that clears a hold to move a scalar

When a worker's plan contains an item like *"release the held actor in <organ> to boost
<scalar>"*, three checks before it goes through:

- **The actor.** Query the organ's own health surface for its restricted/held list. The actor
  named in the plan is frequently *not* the one actually held.
- **The causality.** A scalar composed as a geometric mean over a measurement window cannot be
  moved by clearing a hold. No mechanism means no outcome.
- **The legitimacy.** A hold is an anti-simulation lock earned by execute-without-verify history.
  Clearing it so a number passes is metric gaming, not recovery — and it destroys a control that
  was working.

Correct the worker through the channel in Job 2, and surface the finding to the human in one
line. Do not silently drop it, and do not execute it.

## Job 2 — reach the session that is already running

Interactive workers often run on a pty the orchestrator opened from a *different* conversation,
so process controls that resolve against the current conversation's registry may not see them.
The compact procedure:

```bash
# 1. locate — PID, then the pty that PID owns
ps aux | grep -i '<worker-bin>' | grep -v grep
ps -o pid,ppid,tty,stat,lstart,cmd -p <PID>          # -> pts/N

# 2. is it mid-turn, or waiting at its prompt?
tail -3 <CLI_HOME>/sessions/<slug>/session_<uuid>/logs/<cli>.log   # turnStep recency

# 3. precondition before any blind write: no live permission prompt
grep -n 'permission_mode\|dangerous_command_guard' <CLI_HOME>/config.toml

# 4. deliver — one write, one line, one newline
python3 -c "open('/dev/pts/N','w').write('<answer + evidence-backed corrections>' + chr(10))"

# 5. confirm read-side, not write-side
grep -c '<unique phrase>' <session>/agents/main/wire.jsonl          # 0 -> not yet OBSERVED
```

### Detail that decides whether the relay works

- **Conversation-scoped process registry.** The management surface that backs background
  process control resolves ids against the *owning conversation's* registry, so a pty opened by
  another conversation can answer `No process with ID ...` while the process is alive. That is a
  registry-scope result, not evidence the worker is gone — confirm liveness with `ps` first.
- **Session record.** The orchestrator records every pty it opens under
  `~/.hermes/terminal-sessions/tty-dev-pts-<N>` as `{"session_id", "cwd", "ts"}`. Match the
  PID's own `tty` to that file before trusting it; pts numbers are reused across time.
- **Most agent CLIs have no message-injection subcommand.** Several expose only `list`,
  `export` and `fork`; check before assuming, then the pty write is the relay.
- **Check the approval mode before writing.** Blind-write only when it is `never_ask` (or
  equivalent) and the dangerous-command guard is off, so no permission prompt can be live. If
  the worker *can* raise prompts, do not inject — a stray newline can answer a prompt on the
  human's behalf. Resume non-interactively instead (`<cli> -S <session-id> -p '<prompt>'`).
- **A write during a turn is queued, not lost.** Delivery lands as a user message at the next
  turn/prompt boundary. Judge "still working" from the worker log tail and its transcript
  (`agents/main/wire.jsonl`), never from `state.json` alone — its `updatedAt` lags the log.
- **One message, one paragraph, one newline.** Multiple newlines inside the message submit
  partial text and the worker reads the remainder as further prompts. Stamp the message as a
  relay with a time so the transcript keeps provenance for the instruction.

**State your own chain position.** Bytes written to a terminal are `PRODUCED`; accepted and
queued by the worker is `DELIVERED`; appearing in the worker's transcript is `OBSERVED`. Never
report a relay as delivered when you only achieved produced — re-read the wire first.

## Reporting back to the human

- **The answer to a checkpoint is not a report.** If the human's reply was a one-letter binary,
  the useful response is short: what you verified yourself, which claims in the checkpoint were
  wrong and their evidence, and the one item that genuinely still needs them.
- **Do not re-ask what the worker already asked.** A question the worker raised and the human
  ignored is not now owed as a menu. If it is authority-class (external ports, irreversible
  mutation, direction of record), state that it stays untouched and stop — do not enumerate the
  options again.
- **Say which corrections you actually delivered.** If the relay is still queued in the worker's
  input buffer, say that, rather than implying the worker has acted on it.
- **Close the loop with one line and stop.** No offer of next steps, no summary of your own
  process.

## Pitfalls

- **A checkpoint's precise-looking numbers are not evidence of correctness.** Quoting exact
  decimals is cheap; the authority surface is the witness. Verify, then relay.
- **A relayed order is not a licence to widen scope.** Carry the human's words plus only the
  corrections you can evidence. Do not append new tasks of your own to a worker's queue, and do
  not soften a binary into a menu.
- **Do not stop a working worker to deliver.** If it is mid-turn and progressing on the same
  instruction, let the queued relay land — killing a working turn costs more than the delivery
  latency.
- **One binary answer can be ambiguous across two questions.** When a worker has asked two
  different things with their own option letters, the human's letter answers the one he replied
  to — not both. Resolve it by position in the thread, not by assuming the tidier reading.
