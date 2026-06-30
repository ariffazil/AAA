# OpenCode Canonical Layout

> OpenCode is the forge worker bound to 333-AGI. Spec in AAA; source outside AAA.

## Spec (in AAA/agents/opencode/)

| File | Purpose |
|------|---------|
| `AGENTS.md` | Operational protocol |
| `IDENTITY.md` | Who/what/why |
| `SOUL.md` | Voice |
| `TOOLS.md` | Tool surface |
| `agent-card.json` | A2A agent card |

## Runtime / config (live)

| Path | Purpose |
|------|---------|
| `/root/.config/opencode/opencode.json` | Canonical user config |
| `/root/.config/opencode/node_modules/` | Local CLI install |
| `/usr/local/bin/opencode` → `/root/.npm-global/lib/node_modules/opencode-ai/bin/opencode.exe` | Installed binary |

## Source

| Path | Purpose |
|------|---------|
| `/root/src/opencode/` | Source tree (moved from `/root/oo0-STATE/opencode/`) |

## Notes

- Do not commit `/root/.config/opencode/` or `/root/src/opencode/` into AAA.
- Opencode CLI runs from npm global install; source tree is for development only.
