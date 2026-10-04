# Slash Command Registration — Diagnostic Transcript (2026-08-10)

## What happened

1. Previous agent added `CommandDef("seal", ...)` at line 253 and `CommandDef("init", ...)` at line 255 to `/usr/local/lib/hermes-agent/hermes_cli/commands.py` under a "# arifOS Governance" comment block
2. The `seal-command` plugin at `profiles/aaa-hermes/plugins/seal-command/__init__.py` already existed and tried to `ctx.register_command("seal", ...)` during plugin load
3. `register_command()` called `resolve_command("seal")` → found the built-in → logged warning and returned without registering
4. Gateway processed `/seal` → `resolve_command("seal")` found the built-in CommandDef → gateway treated it as a known command → checked for plugin handler → None (rejected) → fell through to agent text → user saw "Fail"

## Key code paths

### The rejection (hermes_cli/plugins.py:562-573)
```python
def register_command(self, name, handler, ...):
    from hermes_cli.commands import resolve_command
    if resolve_command(clean) is not None:
        logger.warning(
            "Plugin '%s' tried to register command '/%s' which conflicts "
            "with a built-in command. Skipping.",
            self.manifest.name, clean,
        )
        return
    self._manager._plugin_commands[clean] = { ... }
```

### The gateway dispatch (gateway/run.py:10309-10801)
```
10310: command = event.get_command()  # "seal"
10320: _cmd_def = _resolve_cmd(command)  # finds built-in CommandDef
10321: canonical = _cmd_def.name  # "seal"
10367: is_gateway_known_command(canonical)  # True (in GATEWAY_KNOWN_COMMANDS)
       → fires command:seal hook (no handler)
10786: plugin_handler = get_plugin_command_handler("seal")  # None (rejected)
10794: if plugin_handler: → False → skip
       → falls through to agent text
```

### The fix
Remove lines 252-255 from commands.py:
```python
    # arifOS Governance
    CommandDef("seal", "Constitutional seal — judge + seal + vault receipt (arifOS)", "Governance",
               aliases=("s",)),
    CommandDef("init", "Initialize arifOS session — bind identity, probe federation, load carry-forward (arifOS)", "Governance"),
```

After removal:
- `resolve_command("seal")` returns None
- Plugin's `register_command("seal")` succeeds
- Gateway dispatches to plugin handler
- `/seal` works

## Upstream hermes-agent comparison

The upstream repo at https://github.com/nousresearch/hermes-agent does NOT have `seal` or `init` in COMMAND_REGISTRY. The local `CommandDef` dataclass also lacks upstream fields (`busy_policy`, `busy_handler`, `execute`) indicating the local install is behind the upstream version.
