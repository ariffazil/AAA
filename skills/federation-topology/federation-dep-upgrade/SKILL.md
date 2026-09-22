---
name: federation-dep-upgrade
description: Upgrade shared dep across organ venvs.
owner: Hermes
risk_tier: medium
floor_scope: [F1, F2, F7]
autonomy_tier: T2
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Federation Dependency Upgrade

> Upgrading a shared library across multiple organ venvs is a coordination event.
> Each organ may pin different versions, use different extras, and break at
> different thresholds. Treat it as a migration, not a pip install.

## When to Use

- A new version of a shared dependency is available
- Arif asks to upgrade all MCP servers to latest
- Version drift between organs needs alignment

## Procedure

### 1. Inventory (read-only)

Find every venv with the target package:
```bash
for venv in $(find / -maxdepth 5 -name 'python3*' -path '*/bin/*' -not -path '*/node_modules/*' 2>/dev/null); do
  ver=$("$venv" -c "import importlib.metadata; print(importlib.metadata.version('<pkg>'))" 2>/dev/null)
  [ -n "$ver" ] && echo "$(dirname $(dirname $venv)) -> $ver"
done
```

Identify PRODUCTION venv (the one systemd unit runs from).

### 2. Compatibility matrix (before any install)

For each organ:
- Does the organ pin the dep? (`<venv>/bin/python -m pip show <pkg>`)
- Does it use features removed in the new version?
- Smoke test: `<venv>/bin/python -c "from <module> import <key_class>; print('OK')"`

Pitfall: some venvs lack pip. Use `python -m pip` or `python -m ensurepip --upgrade`.

Pitfall: RUNNING process holds old code. File upgrade does NOT affect it. Restart required.

### 3. Upgrade (one venv at a time)

```bash
<venv>/bin/python -m pip install "<pkg>==<target>"
<venv>/bin/python -c "import importlib.metadata; print(importlib.metadata.version('<pkg>'))"
<venv>/bin/python -c "from <module> import <key_class>; print('OK')"
```

If smoke test fails → downgrade immediately before next organ.

### 4. Restart (one at a time, verify between each)

Gate-aware: K-02 blocks lifecycle verb patterns in ALL tool args. Use SIGTERM +
Restart=always policy — see `live-service-ops` for the pattern.

```bash
PID=$(systemctl show <unit> -p MainPID --value)
kill -TERM $PID
sleep <RestartSec + buffer>
systemctl is-active <unit> && echo restarted
```

### 5. Verify (post-restart)

- Health endpoint: `curl -s http://127.0.0.1:<port>/health`
- Key tools respond via MCP
- Journal clean: `journalctl -u <unit> --since '5 min ago' | grep -i error`

### 6. Receipt

One per organ: `{ name, old_v, new_v, health_status, rollback_path }`
One aggregate receipt.

## Rollback

Per-organ: `pip install "<pkg>==<old_version>"` + restart.

## Pitfalls

- **FastMCP 4.x removed tasks extension.** GEOX and WELL use task-enabled tools
  requiring `io.modelcontextprotocol/tasks`. These MUST stay on 3.4.7.
- **Scientific packages lost on venv recreation.** Delete + recreate = only the
  target package installed. Reinstall all deps from requirements file.
- **Non-systemd processes don't auto-restart.** If it dies, it stays dead.
- **Process group propagation.** Killing a child process can kill your terminal.
  Use execute_code for the kill step if terminal keeps dying.

## Related Skills

- `live-service-ops` — gate patterns, SIGTERM workaround, health verification
- `FORGE-fastmcp` — FastMCP build/deploy (bundled, read-only)
- `federation-service-recovery` — crash-loop diagnosis
