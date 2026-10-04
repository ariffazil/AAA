# Timezone Persistence — Reference Patterns

Session-derived patterns for persisting timezone choice across AAA/Hermes sessions.
Created 2026-08-11 from live session with Arif (F13).

## The Pattern (canonical)

When Arif asks to set or change timezone:

```
1. Probe env       → check if HERMES_TIMEZONE already set
2. Probe state     → check /root/.local/share/arifos/state.json
3. Persist         → write canonical state.json (see schema below)
4. Verify          → TZ=Asia/Kuala_Lumpur python3 -c 'import time; ...'
5. Confirm         → present UTC + MYT pair to Arif
```

## State file schema (canonical)

Path: `/root/.local/share/arifos/state.json`

```json
{
  "timezone": "Asia/Kuala_Lumpur",
  "iana_tz": "Asia/Kuala_Lumpur",
  "utc_offset_hours": 8,
  "tz_alias": "MYT",
  "set_by": "arif (F13)",
  "set_at_utc": "<ISO 8601 UTC>",
  "set_at_myt": "<ISO 8601 +08:00>",
  "env_var": "HERMES_TIMEZONE",
  "rationale": "Arif di Malaysia. All timestamps MYT, convert UTC → MYT before display."
}
```

## Pitfalls observed

### 1. Hermes guard refuses profile config writes

Trying to write `timezone: Asia/Kuala_Lumpur` into `/usr/local/lib/hermes-agent/profiles/<profile>/config.yaml`:

```
Refusing to write to Hermes config file: ...
Agent cannot modify security-sensitive configuration.
Edit ~/.hermes/config.yaml directly or use 'hermes config' instead.
```

**Correct fallback**: Use state.json. The Hermes guard is intentional — it's
there for a reason. Don't try to bypass. Don't try other profile configs either.

### 2. `now` script vs raw `date`

The `/usr/local/bin/now` script wraps UTC+MYT+organs+FQ+carry_forward in one
call. Don't reach for raw `date -u` first — you'll miss organ health, FQ state,
session carry. Even simple "what time" questions are `now` triggers.

### 3. Setting TZ env inline vs persisting

Setting `TZ=Asia/Kuala_Lumpur` for one command:
```bash
TZ=Asia/Kuala_Lumpur python3 -c "..."
```
This is a **verification** — proves the conversion works. It does NOT persist.
Persistence requires the state.json write.

### 4. Env already set ≠ state persisted

In the source session, `HERMES_TIMEZONE=Asia/Kuala_Lumpur` was already in the
shell env, but no state.json existed. So the answer to "is timezone set?" is:
- Env: ✅ already there
- Persisted: ❌ missing — write state.json so next session inherits

## Live probe pattern

To verify timezone persistence works without restarting:

```bash
python3 -c "
import os
os.environ['TZ'] = 'Asia/Kuala_Lumpur'
import time
t = time.time()
print(f'UTC   : {time.strftime(\"%Y-%m-%d %H:%M:%S UTC\", time.gmtime(t))}')
print(f'MYT   : {time.strftime(\"%Y-%m-%d %H:%M:%S %Z (%z)\", time.localtime(t))}')
print(f'Day   : {time.strftime(\"%A\")}')
print(f'IsoWk : {time.strftime(\"ISO %G-W%V-%u\")}')
"
```

Note: passing `TZ=...` as a command prefix (`TZ=Asia/Kuala_Lumpur python3 ...`)
is more reliable than `os.environ['TZ'] = ...` inside Python — the latter only
works if `time.tzset()` is called explicitly.

## Display rules

| Context | Format |
|---------|--------|
| Conversation reply to Arif | MYT first, UTC in parens if needed |
| SEAL receipt timestamp | Both UTC and MYT, ISO 8601 |
| Cron job delivery | MYT (Arif's clock) |
| Log files | UTC (machine canonical) |
| VAULT999 entries | UTC (immutable, no TZ interpretation) |

## Cross-session continuity

state.json is read at session boot by AAA carry_forward loader. If you write
to state.json mid-session, the change takes effect on the NEXT session boot,
not the current one. To verify in current session: re-read state.json from
disk after write.

## Enforcement for ALL AAA agents (binding 2026-08-11)

**Rule: every AAA agent MUST source sovereign timezone from `state.json`.**

```
❌  hardcoded MYT = timezone(timedelta(hours=8))    # silent coupling — drifts if Arif changes tz
✅  MYT = timezone(timedelta(hours=_STATE["utc_offset_hours"]))    # follows state.json
```

**Single source of truth ladder** (any agent writing timestamps MUST follow this order):

| Priority | Source | File | Authority |
|---|---|---|---|
| 1 (HIGH) | `state.json.iana_tz` | `/root/.local/share/arifos/state.json` | F13 SOVEREIGN |
| 2 (MED) | `HERMES_TIMEZONE` env | shell env | session-inherited |
| 3 (LOW) | hardcoded `Asia/Kuala_Lumpur` | script default | fallback only |

**Mandatory pattern for AAA agent scripts:**

```python
# canonical loader — copy this into any AAA agent script handling timestamps
from pathlib import Path
import json
from datetime import datetime, timezone, timedelta

def _load_tz():
    """Read iana_tz + utc_offset_hours from state.json. Fallback MYT+8."""
    p = Path("/root/.local/share/arifos/state.json")
    try:
        d = json.loads(p.read_text()) if p.exists() else {}
        return (d.get("iana_tz") or "Asia/Kuala_Lumpur",
                int(d.get("utc_offset_hours") or 8))
    except Exception:
        return ("Asia/Kuala_Lumpur", 8)

_iana, _off = _load_tz()
SOVEREIGN_TZ = timezone(timedelta(hours=_off))
```

**Drift detection (optional but recommended):**

If an agent script detects timezone mismatch between state.json and its output,
it MUST surface a warning to the agent's reply and HOLD the time-sensitive
operation until reconciled.

```python
if state_offset != script_offset:
    raise RuntimeError(f"TZ drift: state.json={state_offset} vs script={script_offset}")
```

## Reference

- Skill: `temporal-anchor` (umbrella)
- F4 CLARITY: ΔS ≤ 0 — temporal disorientation is entropy
- Arif's correction: 2026-08-10, never respond raw UTC
- Source session: 2026-08-11, MYT 08:55
- Updated: 2026-08-11, MYT 09:01 — single-source-of-truth doctrine binding for all AAA agents
