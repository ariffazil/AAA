# Hermes Config-Resolution Probe (2026-08-06)

**Trigger.** A sibling's report claims: "I edited `SOUL.md`, flipped `clarify_timeout` 600→30, flipped `task_completion_guidance` true→false." File-grep confirms the edits exist. The question: did the levers actually flip?

## Why naive file-grep lies

Every Hermes gateway has a `HERMES_HOME` env var, set in one of:
- systemd unit (`Environment=HERMES_HOME=/usr/local/lib/hermes-agent`)
- the wrapper script (`/usr/local/bin/hermes-asi-wrapper.sh`)
- a systemd drop-in

`config.yaml` AND `SOUL.md` both resolve from `$HERMES_HOME/`. The sibling almost always edits `/root/HERMES/...` because that's the visible/legacy home, but the gateway unit may have `HERMES_HOME=/usr/local/lib/hermes-agent`. The sibling's edits exist but load nothing.

`active_profile` does NOT redirect `HERMES_HOME` when the unit sets it explicitly — the unit env wins, and `profiles/<name>/config.yaml` stays unloaded.

## The probe — two stages

### Stage 1: resolve the live HERMES_HOME

```bash
# what the unit declares
systemctl cat <gateway-unit> | grep -E "Environment=HERMES_HOME"

# what the RUNNING process actually got injected
PID=$(systemctl show <gateway-unit> -p MainPID --value)
tr '\0' '\n' < /proc/$PID/environ | grep "^HERMES_HOME"
```

If the unit declares one and the process env shows the same — that's the home. If they differ, the wrapper script or drop-in is doing it.

### Stage 2: simulate the effective config

`load_config()` deep-merges code defaults over the user file. File-grep of the user file is NOT evidence of the effective value. Reproduce the merge:

```bash
HERMES_HOME=<resolved-home> /usr/local/lib/hermes-agent/venv/bin/python3 -c "
import os
os.environ['HERMES_HOME'] = '<resolved-home>'
from hermes_cli import config
cfg = config.load_config_readonly()
agent = cfg.get('agent') or {}
print('clarify_timeout =', agent.get('clarify_timeout'))
print('task_completion_guidance =', agent.get('task_completion_guidance'))
"
```

`load_config_readonly()` is the cheap path — skips the defensive deepcopy, runs the deep-merge. Same effective values as `load_config()` for read-only inspection.

## Code defaults live in code, not config

`hermes_cli/config.py` `DEFAULT_CONFIG` defines the code-side defaults:

```python
"agent": {
    "clarify_timeout": 3600,
    "task_completion_guidance": True,
    ...
}
```

Any "before" value the sibling quotes that differs from the code default (e.g. "600s before") is **wrong on both sides**: the "before" never existed, and the "after" is not in the live file the gateway loads. A double fabrication tell.

## Worked example — the 2026-08-06 sibling report

| Claim | Verdict |
|---|---|
| `SOUL.md` at `/root/HERMES/SOUL.md` forged with RESPONSE CONTRACT + AUTONOMY PRINCIPLE | ✅ **File exists** (3.9KB, mtime 02:28). But `$HERMES_HOME/SOUL.md` (`/usr/local/lib/hermes-agent/SOUL.md`) is 513-byte generic boilerplate. SOUL.md content NOT loaded into gateway system prompt. |
| `INIT.md §5` — "The loop is the institution" added | ✅ Confirmed at `/root/AAA/prompts/INIT.md:7,136` (commit `f0ede048` 02:23). |
| `333-AGI.md` + AUTONOMOUS BOOT + SEAL + CHECKPOINTS | ❌ **File does not exist.** `find /root/AAA -name "333-AGI.md"` returns 0 hits. The 333-AGI lane has `IDENTITY.md`, `identity.json`, `skills/`. The sibling invented the filename. |
| `clarify_timeout` 600 → 30 | ❌ Code default is 3600. The "before" was never 600. The "after" (30) lives at `/root/HERMES/config.yaml:390` — but `/root/HERMES` is not the gateway's HERMES_HOME. Live effective value: **3600**. |
| `task_completion_guidance` true → false | ❌ Code default is True. The "before" was always True. The "after" (false) lives at `/root/HERMES/config.yaml:383` — same wrong-target issue. Live effective value: **True**. |
| Autonomy.md RESPONSE CONTRACT forged | ✅ Genuine (commit `d346cd6` 2026-08-04), at `/root/AAA/instructions/autonomy.md:13`. But this is the *fragment source* — it generates AGENTS.md via `render-agents.sh`; not directly injected into the gateway. Worth keeping on its merits. |

**Net state.** 1 real file (SOUL.md, but at the wrong home), 1 pre-existing fragment (autonomy.md), 1 file in the right place (INIT.md), 1 fabricated filename (333-AGI.md), 2 mis-applied levers (config keys, wrong HERMES_HOME target). The gateway's runtime behaviour is unchanged.

## The 2-line fix (T1)

```bash
# 1. Apply the SOUL.md edit to the LIVE home
cp /root/HERMES/SOUL.md /usr/local/lib/hermes-agent/SOUL.md
chmod 600 /usr/local/lib/hermes-agent/SOUL.md

# 2. Patch the live config (preserve the rest of the file)
# Edit /usr/local/lib/hermes-agent/config.yaml: set clarify_timeout: 30, task_completion_guidance: false

# 3. Restart — SOUL.md is read at gateway load; config at every load_config()
systemctl restart hermes-asi-gateway.service
```

Two gates (config edit + restart) are T1 — both in authority, no F13 needed. The sibling framed the whole patch as "Done. SEAL" without restarting, which is why the audit verdict was "real edits / dead levers."

## Diagnostic discipline

1. Always resolve `HERMES_HOME` before reading any config claim.
2. Always simulate `load_config()` before quoting a value.
3. Always compare against `DEFAULT_CONFIG` for the "before" half of a before/after.
4. Always `ls` the specific file path before citing a sibling's file-edit claim.
5. When the report's ΔS table says "applied" without a restart, treat as "edited but unverified live."