---
name: hermes-config-mutation
description: "Use when an agent must change Hermes runtime config."
version: 1.0.0
author: HERMES
owner: AAA
license: proprietary
risk_tier: medium
tags: [hermes, config, mcp, runtime, permission]
metadata:
  hermes:
    tags: [hermes, config, mcp, runtime, permission]
    related_skills: [mcp-ops, hermes-runtime-audit]
---

# Hermes Config Mutation — the writable path when the file is protected

## When to Use

- A request needs a new MCP server, provider, model seat, or setting added to the live Hermes runtime.
- `patch` / `write_file` answered **"Refusing to write to Hermes config file … Agent cannot modify security-sensitive configuration"**.
- You changed a config value and now need to know whether it is live (it usually is not yet).

## The rule

`~/.hermes/config.yaml` is **agent-read-only**. That refusal is a guardrail, not a bug: do not route around it with `sed`, `tee`, or a python file write. The governed write path is the CLI, and it validates and re-serialises the YAML for you.

```bash
hermes config path                     # which file this profile actually uses
hermes config get  <dotted.key>
hermes config set  <dotted.key> <value>
hermes config unset <dotted.key>
hermes config check                    # env/known-key audit after a change
```

Dotted keys create the nested map if it is absent, so a fresh server needs three calls, not a YAML edit:

```bash
hermes config set mcp_servers.<name>.url https://host/mcp
hermes config set mcp_servers.<name>.enabled true
hermes config set mcp_servers.<name>.timeout 60
```

## Verification ladder (do all three)

1. **Read back** — `hermes config get <dotted.key>` shows the resolved value, not just a success message.
2. **Exercise it** — for an MCP server: `hermes mcp list` (registry), `hermes mcp test <name>` (transport + auth + `tools/list`), then **call one tool**. A server that lists tools but errors on call is a half-install; the config key existing proves nothing.
3. **Reach the live surface** — config is read at process start. Prompt, lane, and output-contract changes need a **gateway restart**; restarting the MCP process alone does not reach Telegram sessions. Say "set, not yet live" until the owning process has restarted.

## Other protected surfaces

- Canon trees (`/root/AAA/governance`, `/root/AAA/canon`, `/root/arifOS/GENESIS`) are immutable-flagged: mutate only through `/root/scripts/canon-mutate run <tree> -- <cmd>`.
- Skill trees under `skills.external_dirs` are read-only to autonomous curation — a refused `skill_manage` patch there is ownership, not failure. New skills can still be created; existing ones cannot be edited from a background pass.
- For a config write that must preserve provenance comments or interpolate `${VAR}` values, use the governed writer `/root/scripts/hermes_mcp_wire.py` (`plan | apply --sanitize | verify`) instead of `config set`.

## Pitfalls

- **Success message ≠ applied.** Always read the key back; a typo in the dotted path silently creates a sibling key.
- **Booleans and numbers are strings unless the CLI coerces them** — set `true` / `60`, then `get` to confirm the type the runtime will see.
- **Never hand-edit a protected file to "just add one line"**: the write is refused, and a workaround through the shell produces a file the runtime never validated.
- **One profile only.** `hermes config` acts on the active profile; another profile's config and skills are out of scope unless the human names it.
