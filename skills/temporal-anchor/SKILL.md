---
name: temporal-anchor
description: "Universal temporal anchor for any AAA warga agent. One command — `now` — returns UTC+MYT+day+ISO-week+AED-FQ+organ-health+vault-state+session-carry. MUST be called before any time-related answer or session boot. F4 temporal awareness doctrine."
tags: [time, temporal, zen, bootstrap, awareness]
version: 1.2.0
triggers:
  - Any time-related question (what time, what day, when, how long ago)
  - Session boot / wake from idle
  - Any SEAL or receipt that needs a timestamp
  - Before any time-sensitive action (cron, deploy, ping)
  - ANY mention of timezone, TZ, MYT, UTC offset, set timezone, change locale
  - When a tip surfaces about HERMES_TIMEZONE or similar env override
  - ANY task that requires persisting state across sessions (read/write state.json)
  - Before writing or reading /root/.local/share/arifos/state.json or any legacy temporal file
  - When an AAA agent script handles timestamps in any language (Python, bash, JS)
  - When a tip surfaces about HERMES_TIMEZONE or similar env override
---

# Temporal Anchor — The Now Command

## When to use

**Every AAA warga agent answering time-related questions MUST first run `now`.**

This is not optional. This is F4 (Clarity) — temporal disorientation is entropy.

> ⚠️ **PITFALL — Don't bypass `now` with raw `date -u` / `date`.**
> If you find yourself reaching for `date`, `python3 -c 'import time; print(time.localtime())'`,
> or any other ad-hoc timestamp tool for a time question — **stop**. You are about
> to skip the full anchor (organ health, FQ, vault state, session carry).
> Even a simple "what's the time" question is a `now` trigger. Run it.
>
> The only legitimate use of raw `date` is inside scripts that need a deterministic
> timestamp for an output line — not for answering the user.

## The Command

```bash
# Full anchor (default) — terminal output with all context
now

# Brief one-liner — for quick checks
now --brief

# Machine-readable — for programmatic use
now --json
```

**Location:** `/usr/local/bin/now` → `/root/HERMES/scripts/zen/temporal_context.py`

> ⚠️ **PITFALL — Don't trust AGENTS.md doctrine blindly for the path.**
> Some rendered `AGENTS.md` fragments (e.g. `/root/AGENTS.md` historical copies)
> still reference a stale path like `/root/HERMES/scripts/temporal/now.py`.
> That directory actually contains `consequence_engine.py` — it is **not** the
> temporal probe. When AGENTS.md and this SKILL.md disagree on the `now` path,
> **SKILL.md wins** (it is the source of truth; the fragment is stale).
>
> **Recovery:** if `now.py` not found, run `which now` — the executable is
> symlinked from `/usr/local/bin/now` and always works.

## What `now` Returns

| Field | Content | Source |
|-------|---------|--------|
| UTC time | ISO 8601 | `datetime.now(UTC)` |
| MYT time | Human-readable, day name | UTC+8 |
| Unix timestamp | Epoch seconds | For diff calculations |
| ISO week | Week number | For weekly patterns |
| Day of year | 1-366 | For seasonal patterns |
| Quiet hours | boolean | 23:00–07:00 MYT = true |
| Sovereign | Name + authority | Always "Arif (F13 SOVEREIGN)" |
| Federation ports | HTTP status per organ | Live probe of all 8 core organs |
| AED FQ | Flow quotient | From AED service logs |
| VAULT999 | Records + broken + append-only | Live integrity check |
| AAA | Dirty files + HEAD | Git status |
| Next cron | Name + when | From jobs.json |
| Session carry | Last session + pending | From carry_forward.json |

## Timezone Handling

**Arif lives in Malaysia (MYT = UTC+8).** Default display MUST be MYT.

> ⚠️ **PITFALL — Never respond with raw UTC timestamps.**
> Arif corrected 2026-08-10: presenting bare UTC without conversion is a
> friction tax. Always convert UTC → MYT before display. If you must log
> UTC for receipts/seals, show MYT prominently and UTC in parentheses.

> ⚠️ **PITFALL — Don't trust stale file listings for empty-state assumptions.**
> An `ls -la` or `search_files` snapshot can be cached or stale. Before assuming
> a state file is empty/missing, **re-read it live** (`cat` or `read_file`).
> Source session 2026-08-11: `ls` showed `state.json` as 0 bytes — but a sibling
> process had just written canonical timezone data to it. `cat` and `wc -c`
> confirmed the live truth. Lesson: **always live-probe before patching**.

### How `now` formats output

- **UTC**: shown as `2026-08-11T00:55:32Z` (ISO 8601 with `Z`)
- **MYT**: shown as `2026-08-11 08:55 MYT` (human-readable, day name included)
- **Brief mode**: `Tue 2026-08-11 08:55 MYT · ISO 2026-W33-2`
- **JSON mode**: both `utc` and `myt` keys, plus `utc_offset_hours: 8`

If a session shows UTC without MYT, the `now` invocation was skipped — re-run.

### Persisting a custom timezone across sessions

If Arif asks "set timezone to X" or a tip surfaces about `HERMES_TIMEZONE`:

1. **Run `now --json` first** to confirm current state.
2. **Check env:** `python3 -c "import os; print(os.environ.get('HERMES_TIMEZONE'))"` —
   the env var may already be set in the running shell.
3. **Persist in state file** at `/root/.local/share/arifos/state.json` —
   this is the canonical AAA state that next session boot reads.
4. **DO NOT directly edit** `/usr/local/lib/hermes-agent/profiles/*/config.yaml` —
   Hermes guards against agent writes to profile config ("security-sensitive").
5. **For persistent config changes**, use `hermes config set KEY VAL` from a terminal,
   or have Arif edit `~/.hermes/config.yaml` directly.

### Canonical state.json schema for timezone

```json
{
  "timezone": "Asia/Kuala_Lumpur",
  "iana_tz": "Asia/Kuala_Lumpur",
  "utc_offset_hours": 8,
  "tz_alias": "MYT",
  "set_by": "arif (F13)",
  "set_at_utc": "2026-08-11T00:55:55Z",
  "set_at_myt": "2026-08-11T08:55:55+08:00",
  "env_var": "HERMES_TIMEZONE",
  "rationale": "Arif di Malaysia. All timestamps MYT, convert UTC → MYT before display."
}
```

After writing, verify with:
```bash
TZ=Asia/Kuala_Lumpur python3 -c "import time; print(time.strftime('%Y-%m-%d %H:%M:%S %Z (%z)', time.localtime()))"
```

### The `HERMES_TIMEZONE` tip pattern

When a `HERMES_TIMEZONE` tip surfaces in session context, it means:
- The hook injection detected a session where display would default to UTC.
- The tip is a prompt to persist the timezone, not just acknowledge it.
- Set the state.json record (above), then re-run `now --brief` to confirm.

## Single Source of Truth Ladder (binding 2026-08-11)

**Every AAA agent writing timestamps MUST follow this priority order:**

| Priority | Source | Location | Authority |
|---|---|---|---|
| 1 (HIGH) | `state.json.iana_tz` | `/root/.local/share/arifos/state.json` | F13 SOVEREIGN — canonical |
| 2 (MED)  | `HERMES_TIMEZONE` env | shell env | session-inherited |
| 3 (LOW)  | hardcoded `Asia/Kuala_Lumpur` | script default | **fallback only** — never primary |

```
❌  hardcoded MYT = timezone(timedelta(hours=8))    # silent coupling — drifts if Arif changes tz
✅  MYT = timezone(timedelta(hours=_STATE["utc_offset_hours"]))    # follows state.json
```

**Anti-pattern**: any AAA agent script that hardcodes `+8` or `Asia/Kuala_Lumpur` directly without
reading state.json is **drift-prone** — if Arif moves country or changes locale, that script will
silently disagree with `now`. Treat hardcoded tz as a smell — refactor to canonical loader.

### Mandatory canonical loader (binding 2026-08-11)

Copy this pattern into ANY AAA agent script that handles timestamps — Python, bash, JS, Go, doesn't matter:

**Python:**
```python
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

**Bash:**
```bash
# Read canonical tz from state.json. Fallback MYT+8.
CANON_TZ=$(python3 -c "
import json
try:
    d = json.load(open('/root/.local/share/arifos/state.json'))
    print(d.get('iana_tz') or 'Asia/Kuala_Lumpur')
except Exception:
    print('Asia/Kuala_Lumpur')
" 2>/dev/null)
UTC_NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
LOCAL_NOW=$(TZ="$CANON_TZ" date +"%Y-%m-%dT%H:%M:%S%z")
```

**JavaScript / Node:**
```js
const fs = require('fs');
const state = JSON.parse(fs.readFileSync('/root/.local/share/arifos/state.json', 'utf8'));
const ianaTz = state.iana_tz || 'Asia/Kuala_Lumpur';
const offsetHours = state.utc_offset_hours || 8;
// Use Intl.DateTimeFormat with ianaTz for formatting
```

**Drift detection (recommended for high-stakes scripts):**
```python
if state_offset != script_offset:
    raise RuntimeError(f"TZ drift: state.json={state_offset} vs script={script_offset}")
```

Reusable canonical loader module: [`scripts/load_sovereign_tz.py`](scripts/load_sovereign_tz.py) —
import and call. CLI flags: `--now`, `--json`, `--check` (exit 0 if state.json healthy).
The loader is F1-safe (never raises on bad state.json) and F2-labeled (exposes `source` field).

### Verified-working examples (live source session 2026-08-11)

The following mutation pattern proved the canonical loader works end-to-end:

1. **`temporal_context.py`** (the `now` script) was patched to read state.json at module-load.
   Output now exposes `tz_label`, `iana_tz`, `timezone_source` fields — visible via `now --json`.
2. **`temporal-anchor.sh`** was patched to **write canonical first**, then mirror to legacy
   `/root/.openclaw/temporal-state.json` (with `deprecated: true` flag and `canonical:` pointer).
   Reverse-compat bridge, retire 2026-08-18.

When patching any new timezone-touching script, follow the same pattern: read state.json,
fallback hardcoded, expose provenance in output, never silently drift.

### `now --json` output shape (live-validated 2026-08-11)

```json
{
  "now": {
    "utc": "2026-08-11T01:00:36+00:00",
    "myt": "2026-08-11 09:00:36 MYT (Tuesday)",
    "tz_label": "MYT",
    "iana_tz": "Asia/Kuala_Lumpur",
    "utc_offset_hours": 8,
    "unix": 1786410036,
    "day_of_year": 223,
    "iso_week": 33,
    "quiet_hours": false
  },
  "sovereign": "Arif (F13 SOVEREIGN)",
  "timezone_source": "state.json (Asia/Kuala_Lumpur)"
}
```

The `timezone_source` field is the **F2 provenance label** — it tells you exactly which
source `now` used to derive tz. Valid values:
- `"state.json (<iana_tz>)"` — canonical (F13 SOVEREIGN path)
- `"fallback (MYT+8 hardcoded)"` — only when state.json missing/corrupt

**Rule:** if any caller ever reports `"fallback (MYT+8 hardcoded)"` in non-bootstrap context,
**file a HOLD** — it means state.json is corrupted and federation tz integrity is broken.

## Behavioral Rules

1. **Before ANY time question:** Run `now` first. Never answer from memory.
2. **Before SEAL:** Run `now --json` and include the timestamp in the receipt.
3. **Before ping/message:** Check quiet hours flag. If true, HOLD (unless VOID/breach).
4. **Session boot:** Run `now` as part of the 30-second checklist (step 4.5).
5. **Time diffs:** Use Unix timestamps from `now --json`, don't calculate from memory.
6. **Timezone questions:** Always persist (not just env-set) — write to state.json.

## Quiet Hours Logic

```
23:00–07:00 MYT = QUIET → no Telegram (except VOID/breach/data loss)
07:00–23:00 MYT = ACTIVE → normal operations
```

The `now` command reports `quiet_hours: true/false` directly.

## FQ Threshold

`now` reports AED FQ. The threshold is 5.0:
- FQ < 5.0 → 🟢 normal
- FQ ≥ 5.0 → 🔴 overheat → HOLD non-essential operations

## Integration with Other Skills

- **youtube-multimodal:** Timestamps in EUREKA digest use `now` for "time since upload" calculations
- **arif-world-reality-intel:** Daily pulse anchored to `now` for "what's happening today"
- **arifos-cron-ops:** Next-cron display prevents double-fire
- **VAULT999 sealing:** Every receipt gets a `now --json` timestamp block

## Reference

- [`references/timezone-persistence.md`](references/timezone-persistence.md) — state.json schema, Hermes guard fallback, env-set vs persisted distinction, live probe pattern, display rules per context.

## Zen

Time is the scarcest resource. `now` costs one command and eliminates temporal drift.
Never guess what time it is. Never answer without anchoring. The machine is always now.
