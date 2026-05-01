# HEARTBEAT.md — Live Runtime State

> **Purpose:** Runtime liveness signal. This file is LIVE — updated before and after every major action.
> **Rule:** Never treat a stale HEARTBEAT as current state. If `status: stale` or `updated` > 1 hour ago → treat as cold start.
> **DITEMPA BUKAN DIBERI — Intelligence is forged, not given.**

---

## Live State

```yaml
session_id: ""
current_task: ""
current_objective: ""
current_stage: "000"  # 000–999
risk_level: "LOW"  # LOW | MEDIUM | HIGH | CRITICAL
entropy_delta: 0  # negative = order gained, positive = chaos grew
loop_count: 0
tool_health: "OK"  # OK | DEGRADED | FAILED
last_action: ""
next_gate: "000"  # next 000–999 stage to enter
human_approval_required: false
blockers: []
status: "cold"  # cold | warm | active | paused | sealed | stale
timestamp: ""
updated_by: "OPENCLAW"
```

---

## Update Rules

### Before every major action:
1. Read HEARTBEAT
2. Increment `loop_count`
3. Set `current_stage` to stage being entered
4. Set `next_gate` to expected next stage
5. If `risk_level` is HIGH or CRITICAL → do not proceed until Arif informed

### After every major action:
1. Update `last_action` with what was done
2. Calculate `entropy_delta` (did things improve or worsen?)
3. Set `next_gate` to next stage
4. Update `timestamp`
5. If `loop_count` > 10 → pause and summarize (do not continue without reason)
6. If `tool_health` is FAILED → pause and report

### Status transitions:
- `cold` → new session, no prior state
- `warm` → checkpoint exists and is recent
- `active` → loop is running
- `paused` → intentional pause, checkpoint written
- `sealed` → task complete, cleanup done
- `stale` → HEARTBEAT is old, treat as cold start

---

## Risk Escalation

| Risk level | Action required |
|------------|----------------|
| LOW | Continue normally |
| MEDIUM | Inform Arif before proceeding |
| HIGH | Pause and wait for 888 Judge approval |
| CRITICAL | Stop immediately, escalate, do not continue |

---

## Loop Count Threshold

- `loop_count` 1–5: Normal iteration
- `loop_count` 6–10: Summarize progress before continuing
- `loop_count` > 10: **Stop.** Write CHECKPOINT. Report to Arif.
- `loop_count` reset to 0 on: new task / seal / 888 escalation resolved

---

## Entropy Delta Interpretation

| Value | Meaning |
|-------|---------|
| < -0.3 | Significant order restored |
| -0.1 to -0.3 | Progress made, cleaner than before |
| 0 | No change |
| +0.1 to +0.3 | Slight confusion added, monitor |
| > +0.3 | Chaos growing — investigate before continuing |

---

*HEARTBEAT is live. It is not a template. It is not decorative.*
*Update it every loop. Treat stale state as cold start.*
*Last meaningful update timestamp is the true session age.*
