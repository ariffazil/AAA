# OpenClaw Canonical Layout

> OpenClaw is the AGI-level routing gateway. Spec in AAA; source outside AAA.

## Spec (in AAA/agents/openclaw/)

| File | Purpose |
|------|---------|
| `AGENTS.md` | Operational protocol |
| `IDENTITY.md` | Who/what/why |
| `SOUL.md` | Voice |
| `TOOLS.md` | Tool surface |
| `agent-card.json` | A2A agent card |
| `config/handoff-protocol.yaml` | Handoff rules |

## Runtime (live)

| Path | Purpose |
|------|---------|
| `/usr/lib/node_modules/openclaw/` | Installed runtime |
| `/usr/local/bin/openclaw*` | Wrapper scripts |
| `/root/.openclaw/` | Workspace state |

## Source

| Path | Purpose |
|------|---------|
| `/root/src/openclaw/` | Source tree (moved from `/root/oo0-STATE/openclaw/`) |

## Notes

- OpenClaw gateway runs from system node_modules, not from source tree.
- `/root/oo0-STATE/openclaw/` is a stale copy to be relocated.
