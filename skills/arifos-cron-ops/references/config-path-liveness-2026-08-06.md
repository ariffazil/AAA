# Config-Path Liveness Case Study — Hermes Gateway (2026-08-06)

## Context

Sibling agent (333-AGI, DeepSeek V4 Pro) wrote config levers and SOUL.md during a "Trinity Mesh Forge" session. Reported "levers live, autonomy enabled." All edits were to files at `/root/HERMES/`, not the files the gateway process loads.

## Gateway load path

```bash
# hermes-asi-gateway.service ExecStart:
ExecStart=/usr/local/bin/hermes-asi-wrapper.sh
# Wrapper sets:
export HERMES_HOME=/usr/local/lib/hermes-agent

# systemd unit file (full path): /etc/systemd/system/hermes-asi-gateway.service
# HERMES_HOME=/usr/local/lib/hermes-agent (set via Environment= in unit)
```

Therefore gateway reads:
- Config: `/usr/local/lib/hermes-agent/config.yaml` (NOT `/root/HERMES/config.yaml`)
- SOUL.md: `/usr/local/lib/hermes-agent/SOUL.md` (NOT `/root/HERMES/SOUL.md`)

## Edit vs load comparison

### Config

| File | `clarify_timeout` | `task_completion_guidance` | Inode |
|---|---|---|---|
| `/root/HERMES/config.yaml` (edit target) | 30 | false | 344283 |
| `/usr/local/lib/hermes-agent/config.yaml` (gateway load) | 3600 (default) | true (default) | 2280603 |
| `/usr/local/lib/hermes-agent/profiles/aaa-hermes/config.yaml` (profile) | (empty) → defaults | (empty) → defaults | — |

`agent: {}` in the profile config means all values inherit from DEFAULT_CONFIG. The gateway also has a "readonly" profile path: `HERMES_HOME = /usr/local/lib/hermes-agent`, so the profile directory `/usr/local/lib/hermes-agent/profiles/aaa-hermes/` is not used unless explicitly configured.

### SOUL.md

| File | Bytes | Content |
|---|---|---|
| `/root/HERMES/SOUL.md` (edit target) | 3,968 | Full RESPONSE CONTRACT + AUTONOMY PRINCIPLE + ANTI-PATTERNS |
| `/usr/local/lib/hermes-agent/SOUL.md` (gateway load) | 513 | Nous Research default boilerplate |
| `/usr/local/lib/hermes-agent/profiles/aaa-hermes/SOUL.md` | 513 | Same Nous default (identical diff) |

## Active profile

```bash
cat /usr/local/lib/hermes-agent/active_profile
# → aaa-hermes
```

Active profile is `aaa-hermes`, but the gateway's `HERMES_HOME` points to the install root (`/usr/local/lib/hermes-agent`), not the profile root. The profile system uses `_get_default_hermes_home()` to locate `profiles/`, but config loading reads from `HERMES_HOME / "config.yaml"` directly.

## Runtime verification

```bash
# Gateway PID and process env
PID=$(systemctl show hermes-asi-gateway.service -p MainPID --value)
# PID=3015207
tr '\0' '\n' < /proc/$PID/environ | grep -E "^HERMES_HOME|^HERMES_PROFILE"
# → HERMES_HOME=/usr/local/lib/hermes-agent
# (no HERMES_PROFILE set)

# Gateway process age (started after config edit)
ps -o pid,lstart -p $PID | tail -1
# → 3015207 Thu Aug  6 02:29:35 2026
# (config edit at 2026-08-06 02:28:27 → gateway restarted BEFORE config edit)

# Config mtime comparison
stat -c "%y %n" /root/HERMES/config.yaml /usr/local/lib/hermes-agent/config.yaml
# → 2026-08-06 02:28:27 /root/HERMES/config.yaml
# → 2026-08-05 15:34:16 /usr/local/lib/hermes-agent/config.yaml
```

## What actually happened

1. Sibling wrote `clarify_timeout: 30` and `task_completion_guidance: false` to `/root/HERMES/config.yaml:390,383`
2. Sibling wrote SOUL.md to `/root/HERMES/SOUL.md` (94 lines, full contract)
3. Sibling reported "config levers applied, SOUL.md live"
4. Gateway `HERMES_HOME=/usr/local/lib/hermes-agent` still loads the old values
5. SOUL.md is 513 bytes Nous default — no RESPONSE CONTRACT active

## The fix

```bash
# 1. Copy levers to the gateway's load target
# (manual: edit /usr/local/lib/hermes-agent/config.yaml directly,
#  or cp the relevant sections from the source)
# 2. Restart the gateway
sudo systemctl restart hermes-asi-gateway
# 3. Verify
grep clarify_timeout /usr/local/lib/hermes-agent/config.yaml
# → 30  ← now live
wc -c /usr/local/lib/hermes-agent/SOUL.md
# → 3968  ← now live (after copy)
```

The same hazard exists for OpenCode: `/root/.config/opencode/` is not part of any git repo (runtime config), so edits there don't show up in `git status` and are invisible to repo-based audits.
