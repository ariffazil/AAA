# arifOS `.git_commit` Drift — when `pip install -e .` is the wrong fix (2026-08-12)

## Context

F13 sovereign instructed: rebuild arifOS from source with `pip install -e . --no-deps --quiet` to fix `deployment_drift_status=drift_detected`. On probe:

- `/root/arifOS` HEAD = `708d4a0c` (current)
- `/opt/arifos/app` HEAD = `0f50006d3` (snapshot, weeks-old)
- `pip install -e .` failed: PEP 668 in `/root/arifOS` (no system-wide install allowed)
- `arifosmcp` lives at `/opt/arifos/venv/lib/python3.13/site-packages/arifosmcp/` (the actual wheel)
- Service ExecStart loads from `/opt/arifos/venv/bin/python`
- `/opt/arifos/app/.git_commit` = stale `65f087cd` — never refreshed because systemd `ExecStartPost` was overridden to empty

Even after a successful `pip install -e . --no-deps --quiet` in `/opt/arifos/app` + `systemctl restart arifos.service`: drift STILL true.

## The real fix (one line)

```bash
git -C /root/arifOS rev-parse HEAD > /opt/arifos/app/.git_commit
systemctl restart arifos.service
curl -sf http://127.0.0.1:8088/health | jq '.software_release | {drift, source, built}'
# Expected: drift=false, source=<hash>, built=<hash>
```

## Why `pip install -e .` was wrong

1. **PEP 668** — Python 3.13 refuses system-wide pip. `.venv` must exist in the target path.
2. **Wrong path** — service loads from `/opt/arifos/venv`, not `/root/arifos/.venv`
3. **Drift is read from `.git_commit` file**, not the wheel itself. The wheel may be current; the marker is stale.

## Drift detection mechanism

| Field | Source | Update cadence |
|---|---|---|
| `source_commit` | `git -C /root/arifOS rev-parse HEAD` | Live |
| `built_commit` | Wheel metadata at install time | Once per install |
| `.git_commit` | systemd `ExecStartPost` | Every restart (if not overridden) |
| Kernel drift verdict | Compares `.git_commit` against built_commit | Every `/health` |

## Pre-fix probe set (30 seconds)

```bash
# 1. Where is the wheel?
/opt/arifos/venv/bin/python -c "import arifosmcp; print(arifosmcp.__file__)"
# → /opt/arifos/venv/lib/python3.13/site-packages/arifosmcp/__init__.py

# 2. What's the current source HEAD?
git -C /root/arifOS rev-parse HEAD
# → 708d4a0c...

# 3. What's the marker file?
cat /opt/arifos/app/.git_commit 2>/dev/null
# → 65f087cd... ← stale

# 4. What does kernel think?
curl -sf http://127.0.0.1:8088/health | jq '.software_release | {drift, source_commit, built_commit}'
```

If step 2 disagrees with step 3, fix is one line — no rebuild.

## When to use

Any time `/health` reports `drift=true` or `deployment_drift_status=drift_detected` for an arifOS-class organ. **Probe the `.git_commit` file before reaching for pip.**

Also applies when a systemd unit has overridden `ExecStartPost=` to suppress refresh, or after multiple deploy rounds without restarting upstream.