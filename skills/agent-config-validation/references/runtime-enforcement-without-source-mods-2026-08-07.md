# Runtime enforcement without modifying source

Three new pitfalls and one runtime-enforcement pattern from the 2026-08-07 session that aren't yet in the umbrella SKILL.md.

## Pitfall: `small_model` mismatch

`small_model: ollama/qwen2.5-coder:3b` fails silently at schema validation. The `-coder` variant must be explicitly pulled:

```bash
curl -sf http://127.0.0.1:11434/api/tags | grep <small_model>
# If missing: ollama pull qwen2.5-coder:3b
```

Symptom: `AI_APICallError: model 'qwen2.5-coder:3b' not found` on every `agent=title, mode=primary, small=true` call. Schema-valid config, runtime-broken.

## Pitfall: kernel restart breaks session bindings

After `arifOS :8088` or AAA A2A `:3001` restart, every `task` / `@subagent` invocation fails with "session not bound" / "no-session-token". Cause: `session_id` cache is per-process; the new kernel has no record of the agent's session.

Fix: reload the agent TUI (not the kernel). The new kernel session rebinds automatically on next `arif_init`. Do not waste cycles trying to fix the kernel — it's the agent's cache that's stale.

## Pitfall: sibling-write concurrency

Two agents (or a sibling + you) writing the same canonical artifact to different paths concurrently passes JSON validation on both files but creates a constitutional violation that has no receipt. The skill covers this; the operational rule is:

After every canonical write, immediately run:

```bash
ls -la /root/AAA/federation/   # check for sibling files
git -C /root/AAA status --short
```

If found, archive one with written reason to `_archive/2026-MM-DD-pre-canon-merge/`. Never silently `rm` — the silent delete is itself a violation.

## Pattern: Hermes `pre_tool_call` shell-hook gate (K-02 transition)

Hermes has no plugin-hook architecture like OpenCode. To add a constitutional gate without forking Hermes source, append this to `/usr/local/lib/hermes-agent/profiles/aaa-hermes/config.yaml`:

```yaml
hooks:
  pre_tool_call:
    - matcher: "*"
      command: /root/AAA/federation/protocols/arifos-hermes-gate-hook.py
      accept_hooks: true
```

Wire protocol (per Hermes `agent/shell_hooks.py`):

- **stdin**: JSON `{"hook_event_name":"pre_tool_call","tool_name":"...","tool_input":{...},"session_id":"..."}`
- **stdout**: `{"decision":"block","reason":"..."}` to deny; empty = allow
- **exit code**: `2` for block, `0` for allow/passthrough

Classification logic (in `/root/AAA/federation/protocols/arifos-hermes-gate-hook.py`):

| Tool tier | Examples | Action |
|---|---|---|
| OBSERVE | `read_file`, `web_search`, `search_files`, `vision_analyze`, etc. | passthrough (no output, exit 0) |
| T2 mutation | `write_file`, `patch`, `terminal` (non-T3 args), `cronjob`, `delegate_task` | WITNESSED + receipt |
| T3 | secret path, vault integrity, `chattr -i` on vault, `rm -rf /root`, force-push, DROP | BLOCKED + receipt + exit 2 |

T3 patterns (regex, hardcoded):
- `/root/.secrets/`, `kunci-mas`, `vault\.env`, `\.signing_key`, `tokenrouter`
- `chattr -i` on VAULT999
- `rm -rf /root`, `mkfs.`, `dd if=...of=/dev/`
- `git push ... --force ... main|master`
- `DROP TABLE|DATABASE`

Receipts append to `/root/.local/share/arifos/hermes_hook_receipts.jsonl`, tagged `"k02_transition": true` to mark first enforcement.

Tested live (2026-08-07, 4 scenarios):

| Tool | Args | Decision | Exit |
|---|---|---|---|
| `terminal` | `cat /root/.secrets/kunci-mas.env` | BLOCKED | 2 |
| `write_file` | `/tmp/test.txt` | WITNESSED | 0 |
| `terminal` | `chattr -i /root/arifOS/VAULT999/outcomes.jsonl` | BLOCKED | 2 |
| `read_file` | `/etc/hostname` | passthrough | 0 |

This is the K-02 transition (Witness → Enforcer) — first time a constitutional invariant changed runtime outcome rather than merely recording it. The Python script is 4.2KB, single file, no dependencies beyond stdlib. Reversible: remove the `hooks:` block and restart the profile.

For other harnesses (OpenCode, Kimi Code) the pattern is the same but the wiring differs:
- **OpenCode**: edit `~/.config/opencode/plugins/arifos-judge-gate.ts` (already in production, 358 lines)
- **Kimi Code**: extend `config.toml` PreToolUse matcher to include mutation patterns + secret paths
- **Hermes**: this `hooks.pre_tool_call` shell-hook approach (no source mod)

## When to load this reference

- You're about to add a `small_model` field and want to know if the model is actually pulled
- An agent TUI shows the right schema-valid config but mutations get "no-session-token" rejections (probably kernel restart, fix the agent not the kernel)
- Two agents just wrote to the same canonical path and you need to archive one safely
- You need to add runtime enforcement to Hermes without forking it
- You want the minimum-viable governance gate pattern that survives profile reload