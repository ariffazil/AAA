# Satellite Hermes Upgrade Drill — wawa node v0.17.0 → v0.20.1 carry fork (2026-08-15)

> Node: srv1642546 (azwaos, 100.64.0.4, tag:flow-dmz). Service: `hermes-agent.service`
> (system-level, ExecStart=/usr/local/bin/hermes-wrapper.sh). Situation: remote satellite
> on stock upstream Hermes (origin=NousResearch, v0.17.0) while the federation canonical
> runs the ariffazil fork (carry-v0.20.1). Goal: fork parity via GitHub, NOT `hermes update`.

## Why fork parity for a satellite

Satellites inherit every fix the carry branch carries (Gemini tool-schema 400 fix,
dialog_policy raise-not-fallback, gateway improvements) and keep the fleet on ONE
codebase — config drift between versions is the silent killer when diagnosing
cross-node issues ("works on af-forge, broken on wawa" = version skew, not config).

## Pre-flight (all must be green before touching anything)

```bash
# On the satellite:
/usr/local/lib/hermes-agent/venv/bin/python --version   # venv python + version pin
which uv || ls /root/.local/bin/uv                       # uv present + PATH source
git -C /usr/local/lib/hermes-agent remote -v             # know origin
git ls-remote https://github.com/ariffazil/hermes-agent.git | grep carry  # fork reachable
df -h /usr   # venv rebuild needs ~1.5GB free
```

Python range note: fork requires `>=3.11,<3.14`. System python was 3.14 (too new) but a
uv-managed 3.11.15 already existed at
`/root/.local/share/uv/python/cpython-3.11.15-linux-x86_64-gnu/` — pass it via
`export UV_PYTHON=...` before `uv sync`.

## The drill

1. **Preserve state:** backup config + git status + diff + stash list to a dated dir
   (`/root/forge_work/<node>-upgrade-backup/`).
2. **Anchor rollback:** `git branch <node>-pre-upgrade HEAD` AND
   `mv venv venv.v0.17.old` happens only at the rebuild step (keep old venv until the new
   one passes verification).
3. **Fetch fork:** `git remote add ariffazil-fork https://github.com/ariffazil/hermes-agent.git &&
   git fetch ariffazil-fork carry-v0.20.1 --depth 50`.
4. **Checkout:** `git checkout -f -B carry-v0.20.1 ariffazil-fork/carry-v0.20.1`
   (`-f` — the dirty tree WILL block a plain checkout).
5. **Stop service** → `mv venv venv.old` → `uv sync --frozen` (with `UV_PYTHON` + PATH
   exported) → **`ln -s .venv venv`** (the step that saves all wrapper edits).
6. **Verify binary:** `./venv/bin/hermes --version` → v0.20.1.
7. **Start service**, then walk the verification ladder below.
8. **Do NOT run `hermes gateway install --force`** on a server node unless you intend to
   switch to user units — it silently adds a second, parallel gateway (see incident log).

## Verification ladder (in order, each must pass)

```
hermes --version                          # expected fork version
systemctl is-active hermes-agent.service  # active
ps aux | grep 'hermes_cli.main gateway'   # EXACTLY ONE process
tail log | grep -E '401|402|parse'        # zero fresh auth/parse errors
functional probe                          # real search/chat through the node's provider
ss -tnp | grep <gateway pid>              # ESTABLISHED to api.telegram.org
```

## Incident log from this session (what went wrong, in order)

1. First patch script aborted at checkout (dirty tree, no `-f`) but had ALREADY run
   `mv venv venv.old` → bot dark ~2 min with no venv. Lesson: order the script
   checkout → THEN stop/move/rebuild; never move the venv before checkout succeeds.
2. `uv: command not found` inside SSH heredoc (PATH). Lesson: `export PATH=/root/.local/bin:$PATH` first line.
3. `./venv/bin/hermes` missing after sync → uv built `.venv`. Lesson: `ln -s .venv venv`.
4. Wrapper pointed at old `venv` path → service restart-looped in "activating". Same fix (symlink).
5. Ran `hermes gateway install --force` to fix a TimeoutStopSec warning → spawned a
   USER-level hermes-gateway unit alongside the system unit → TWO gateway processes on one
   bot token. Fix: `systemctl --user stop/disable`, rm unit file, daemon-reload, restart
   system unit. The TimeoutStopSec warning is cosmetic; fix it by editing the system unit
   directly (sed TimeoutStopSec=240s + daemon-reload), not via gateway install.

## Wrapper contract (satellite)

```bash
#!/bin/bash
if [ -f /root/.secrets/kunci-mas.env ]; then
  set -a; . /root/.secrets/kunci-mas.env; set +a
elif [ -f /root/.secrets/kunci-mas.flat.env ]; then
  set -a; . /root/.secrets/kunci-mas.flat.env; set +a
fi
cd /usr/local/lib/hermes-agent
exec /usr/local/lib/hermes-agent/venv/bin/python -m hermes_cli.main gateway run --replace
```

Without the vault source: provider keys missing → 401 cascade down the fallback chain →
silent degradation to blind-survival Ollama. Without `--replace`: stale pidfile blocks
restarts after crashes.

## Post-upgrade hardening (same session, all reversible)

- aux routing (title_generation/compression/triage) → FED dispatch via mesh (stops a
  dead-provider 402 retry loop every 10 min)
- `tool_loop_guardrails.hard_stop_enabled: true` (limits 5/8/5)
- logrotate for /var/log/hermes-agent.log (48MB unrotated → weekly/20M/8 copies)
- systemd TimeoutStopSec 240s ≥ drain_timeout 180s + 60
- watchdog rewritten: "systemd is truth" — `systemctl start` on failure, never a bare
  `nohup hermes gateway run` (which spawns env-less, key-less processes)
- node-local skills (student-life, ukm-artifact-integrity) + WAWA_UPDATE_DRILL.md on-node

## LOCAL PATCHES wiped by upgrade — re-apply

```
# searxng plugin timeout (cold-cache queries exceed 15s default):
sed -i 's/timeout=15,/timeout=45,/' /usr/local/lib/hermes-agent/plugins/web/searxng/provider.py
```
Keep this list in the node's own drill file; upgrades reset the repo tree.
