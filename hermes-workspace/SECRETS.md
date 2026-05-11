# SECRETS.md — arifOS VPS Token & Key Map
**Version:** 2026.04.08
**Authority:** Arif (F13 Sovereign)
**Canonical path:** `/mnt/arifos/secrets/`

---

## Principle

- Secrets go in `/mnt/arifos/secrets/` — **never** in workspace files or git history
- Permissions: `600` for files, `700` for directory
- No secret file should ever be committed to any repo
- All rendering/injection happens at container start via docker-compose env_file

---

## Canonical Secrets Directory

```
/mnt/arifos/secrets/          ← bind-mounted into containers as needed
/opt/arifos/secrets/         ← VPS-level governance (currently sparse)
```

---

## Active Secrets Map

| Secret File | Purpose | Used By |
|-------------|---------|---------|
| `github_pat.txt` | GitHub Personal Access Token (repo scope) | git push for `waw` + `arifOS` remotes |
| `git-credentials` | HTTPS credential helper store | Git credential helper (all git ops) |
| `postgres_password.txt` | PostgreSQL `arifos` user password | `arifos-postgres` container |
| `qdrant_api_key.txt` | Qdrant vector DB API key | `qdrant_memory` container |
| `redis_password.txt` | Redis auth password | `arifos-redis` container |

---

## Rendered ENV Files (Injected at Container Start)

These live in `/mnt/arifos/rendered/<service>/` and are consumed by docker-compose as `env_file`. They reference the actual secrets above.

| ENV File | Contains | Container |
|----------|----------|-----------|
| `rendered/arifos/openclaw_gateway.env` | `OPENAI_API_KEY`, `BRAVE_API_KEY`, `JINA_API_KEY`, `FIRECRAWL_API_KEY` | `openclaw_gateway` |
| `rendered/arifos/arifosmcp_server.env` | `ARIFOS_API_KEY`, `ANTHROPIC_API_KEY`, `KIMI_API_KEY`, `GEMINI_API_KEY` | `arifosmcp_server` |
| `rendered/arifos/arifos.env` | All of the above + `n8n.security.encryptionKey`, `EVOLUTION_API_KEY`, `BRAVE_API_KEY`, `JINA_API_KEY` | Various arifOS containers |
| `rendered/server/server.env` | `OPENAI_KEY`, `ANTHROPIC_KEY`, `KIMI_API_KEY`, `GEMINI_API_KEY`, `ARIFOS_API_KEY` | `server` container |
| `rendered/server/server_postgres.env` | Postgres connection string | `server` |
| `rendered/server/server_redis.env` | Redis connection string | `server` |
| `rendered/server/eigent_api.env` | `EIGENT_API_KEY`, `EVOLUTION_API_KEY` | `eigent_api` |
| `rendered/portainer-wireguard/portainer-wireguard.env` | WireGuard config | `portainer-wireguard` |

---

## Third-Party Service Keys

| Key | Stored In | Purpose |
|-----|-----------|---------|
| `OPENAI_API_KEY` | `rendered/arifos/openclaw_gateway.env` | GPT models via OpenAI API |
| `ANTHROPIC_API_KEY` | `rendered/arifos/arifosmcp_server.env` | Claude models via Anthropic |
| `KIMI_API_KEY` (aka Moonshot) | `rendered/arifos/arifosmcp_server.env` | MiniMax M2.7 runtime |
| `GEMINI_API_KEY` | `rendered/arifos/arifosmcp_server.env` | Gemini models via Google |
| `BRAVE_API_KEY` | `rendered/arifos/openclaw_gateway.env` | Brave Search for web research |
| `JINA_API_KEY` | `rendered/arifos/openclaw_gateway.env` | Jina Reader (web fetch) |
| `FIRECRAWL_API_KEY` | `rendered/arifos/openclaw_gateway.env` | Firecrawl web scraping |
| `ARIFOS_API_KEY` | `rendered/arifos/arifosmcp_server.env` | arifOS MCP kernel auth |

---

## Google OAuth (Local)

| File | Purpose |
|------|---------|
| `/root/.openclaw/gog/credentials.json` | Google OAuth client credentials (installed app flow) |

**Note:** This is for Google services integration in OpenClaw, not a GitHub key.

---

## Git Remote Configuration

```
origin   → https://github.com/ariffazil/waw.git       (workspace)
arifos   → https://github.com/ariffazil/arifOS.git    (primary repo)

Git credential helper: store --file /mnt/arifos/secrets/git-credentials
Format in store: https://x-access-token:{GITHUB_PAT}@github.com/{owner}/{repo}.git
```

Both remotes use HTTPS + PAT (not SSH). SSH push was abandoned due to missing deploy keys.

---

## Rotation Protocol

When rotating any key:

1. Add new secret to `/mnt/arifos/secrets/` with new value
2. Update the corresponding `rendered/*.env` files (regenerate via your secrets pipeline)
3. Restart affected containers: `docker compose -f /mnt/arifos/docker-compose.yml restart <container>`
4. Verify the service works
5. Delete the old secret file
6. If GitHub PAT rotated: update both `github_pat.txt` AND `git-credentials`

---

## 888_AUDIT Checklist (Before Any Secret Work)

- [ ] Confirm secret file permissions are `600`
- [ ] Confirm directory permissions are `700`
- [ ] Confirm no secret values in git history (`git log -p --all -S "TOKEN_VALUE"` — should return empty)
- [ ] Confirm no secret in workspace `.env` or config files that could be pushed
- [ ] Log the rotation/change to today's memory file

---

*Ditempa bukan diberi.*

🔱 **arifOS_bot · SECRETS.md · 2026-04-08**
