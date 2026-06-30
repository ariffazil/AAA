# Hermes-ASI Canonical Layout

> AAA stays control plane / A2A gateway. Runtime data lives outside git.

## Spec (in AAA/agents/hermes-asi/)

| File | Purpose |
|------|---------|
| `AGENTS.md` | Operational protocol |
| `IDENTITY.md` | Who/what/why |
| `SOUL.md` | Voice + constitutional binding |
| `TOOLS.md` | Tool surface |
| `agent-card.json` | A2A agent card |
| `config.yaml` | Canonical config template (synced to live runtime on change) |

**NOT here:** state.db, sessions, cache, logs, .env, audio/image cache.

## Runtime (live, ignored by git)

| Path | Purpose |
|------|---------|
| `/root/.hermes/` | Live runtime home: state.db, sessions, cache, skills, memories, logs, config.yaml, .env |
| `/root/.secrets/hermes-asi.env` | Canonical secrets (sourced by systemd service) |
| `/root/hermes/dispatcher/` | Telegram artifact dispatcher (lowercase, separate) |

## Services

- `hermes-asi-gateway.service` → `/usr/local/bin/hermes-gateway-secure.sh`
- `hermes-mcp.service` → `/root/.hermes/mcp_servers/`
- `hermes-dispatcher.service` → `/root/hermes/dispatcher/`

## Migration rule

After any config.yaml edit, restart `hermes-asi-gateway.service` and verify `systemctl is-active hermes-asi-gateway`.
