# TOOLS – VPS Full Capability Map
**Version:** 2026.03.07-EXEC-SEALED

---

## 1. Tool Groups Now Active (profile: full)

| Group | Tools | Status |
|-------|-------|--------|
| `group:runtime` | exec, process, bash | ACTIVE |
| `group:fs` | read, write, edit, apply_patch | ACTIVE |
| `group:sessions` | sessions_list/history/send/spawn, session_status | ACTIVE |
| `group:memory` | memory_search, memory_get | ACTIVE |
| `group:web` | web_search, web_fetch | ACTIVE |
| `group:ui` | browser (→ headless_browser:3000), canvas | ACTIVE |
| `group:automation` | cron, gateway | ACTIVE |
| `group:messaging` | message (Telegram live) | ACTIVE |
| `group:nodes` | nodes | ACTIVE |
| `group:openclaw` | all built-in tools | ACTIVE |

Browser is wired to: `http://headless_browser:3000` (Chromium/Browserless internal)

---

## 2. VPS Services — Internal Docker DNS

Network: `arifos_trinity` (10.0.10.0/24)

| Service | Internal URL | External URL | Notes |
|---------|-------------|--------------|-------|
| arifOS MCP | `http://arifosmcp_server:8080` | `https://arifosmcp.arif-fazil.com` | 13 constitutional tools |
| arifOS health | `http://arifosmcp_server:8080/health` | — | JSON health endpoint |
| arifOS MCP endpoint | `http://arifosmcp_server:8080/mcp` | — | Streamable-HTTP MCP |
| Headless Browser | `http://headless_browser:3000` | — | Chromium DOM, Browserless API |
| Qdrant | `http://qdrant_memory:6333` | — | Vector store, REST API |
| Ollama | `http://ollama_engine:11434` | — | Local LLM (OpenAI-compat API) |
| n8n | `http://arifos_n8n:5678` | `https://flow.arifosmcp.arif-fazil.com` | Workflow automation |
| Prometheus | `http://arifos_prometheus:9090` | — | Metrics scraper |
| Grafana | `http://arifos_grafana:3000` | `https://monitor.arifosmcp.arif-fazil.com` | Dashboards |
| Webhook | — | `https://hook.arifosmcp.arif-fazil.com/hooks/deploy-arifos` | CI/CD trigger |
| PostgreSQL | `postgresql://arifos-postgres:5432` | localhost:5432 (host-only) | Primary DB |
| Redis | `redis://arifos-redis:6379` | localhost:6379 (host-only) | Cache + sessions |

---

## 3. Mounted Paths

| Container Path | Host Path | Contents |
|----------------|-----------|----------|
| `/mnt/arifos` | `/srv/arifOS` | Full arifOS repo (kernel, MCP, docker-compose) |
| `/mnt/apex` | `/opt/arifos/APEX-THEORY` | APEX-THEORY (thermodynamic AI theory) |
| `/var/run/docker.sock` | `/var/run/docker.sock` | Docker socket — full container management |
| `/home/node/.openclaw` | `/opt/arifos/data/openclaw` | OpenClaw config, workspace, models |

---

## 4. Environment API Keys

| Env Var | Service | Use for |
|---------|---------|---------|
| `KIMI_API_KEY` | Moonshot Kimi K2.5 | Primary reasoning model |
| `ANTHROPIC_API_KEY` | Claude Opus 4.6 | Constitutional analysis fallback |
| `OPENROUTER_API_KEY` | OpenRouter | Multi-model routing fallback |
| `VENICE_API_KEY` | Venice/DeepSeek | Coding fallback |
| `FIRECRAWL_API_KEY` | Firecrawl | Web scraping (fc-733871f3...) |
| `GH_TOKEN` | GitHub PAT | Repo reads, PR, issues |
| `BROWSERLESS_URL` | `http://headless_browser:3000` | Browser automation |
| `OLLAMA_URL` | `http://ollama_engine:11434` | Local LLM |
| `REDIS_URL` | `redis://arifos-redis:6379` | Cache/session access |
| `OPENCLAW_GATEWAY_TOKEN` | Gateway auth | Internal gateway API calls |

---

## 5. CLI Tools in PATH

All in `/home/node/.local/bin/`:

| Tool | Purpose |
|------|---------|
| `arifos` | Bridge to arifOS MCP (HTTP, 13 constitutional tools) |
| `openclaw` | OpenClaw CLI (gateway, agents, models, memory) |
| `docker` / via socket | Full container management |
| `gh` | GitHub CLI |
| `jq` | JSON processing |
| `rg` | ripgrep fast search |
| `ffmpeg` / `ffprobe` | Media processing |
| `oracle-mcp` | MCP server bridge |
| `mcporter` | MCP porter/proxy |
| `nano-pdf` | PDF handling |
| `xurl` | Enhanced URL fetcher |

---

## 6. arifOS CLI Bridge

`arifos` CLI talks to `http://arifosmcp_server:8080` internally.

```bash
arifos health                    # → {"status":"healthy","tools_loaded":13,...}
arifos list                      # → list all 13 MCP tools
arifos anchor                    # → anchor_session (000 BOOTLOADER)
arifos reason                    # → reason_mind (333 AGI reasoning)
arifos memory "query text"       # → vector_memory (555 Qdrant search)
arifos judge                     # → apex_judge (888 constitutional verdict)
arifos seal                      # → seal_vault (999 VAULT999 ledger)
arifos search "query"            # → search_reality (multi-source web)
arifos audit                     # → audit_rules (floor audit)
```

---

## 7. Docker Management via Socket

```bash
# Container overview
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Service management
docker compose -f /mnt/arifos/docker-compose.yml up -d <service>
docker compose -f /mnt/arifos/docker-compose.yml restart <service>
docker compose -f /mnt/arifos/docker-compose.yml logs <service> --tail 50

# Resource monitoring
docker stats --no-stream
docker system df

# Execute inside containers
docker exec arifosmcp_server python3 -c "..."
docker exec arifos-postgres psql -U arifos -c "SELECT version();"
docker exec arifos-redis redis-cli INFO server
docker exec qdrant_memory curl -s http://localhost:6333/collections | jq
```

---

## 8. arifOS Repo (at /mnt/arifos)

```
/mnt/arifos/
├── core/           # Kernel: floors, physics, organs, governance
├── aaa_mcp/        # Transport: server.py (13 MCP tools), sessions
├── aclip_cai/      # Intelligence: triad backends, embeddings, tools
├── arifos_aaa_mcp/ # PyPI package entry point
├── tests/          # 437+ tests (run: cd /mnt/arifos && pytest tests/ -v)
├── docker-compose.yml  # Full stack compose
├── .env            # Secrets (never commit; contains all API keys)
└── CLAUDE.md       # Primary architecture + commands reference
```

---

## 9. Web Search Capabilities

`web_search` supports:
- Perplexity (if PPLX_API_KEY set — check env)
- Brave (if BRAVE_API_KEY set — check env)
- Kimi (uses KIMI_API_KEY)

`web_fetch` + `browser` tool:
- Jina reader for clean markdown extraction
- Browser tool → headless_browser:3000 → full Chromium render
- Firecrawl for deep crawls (FIRECRAWL_API_KEY available)

---

## 10. Skills Available

| Skill | Trigger patterns | What it does |
|-------|-----------------|--------------|
| `arifos-status` | "status", "check health" | arifOS + Docker status check |
| `list-models` | "list models", "models" | Available AI models |
| `memory-search` | "search memory" | Search workspace memory |
| `restart-gateway` | "restart gateway" | Restart openclaw gateway |
| `vps-docker` | "docker", "containers" | Full Docker status + management |
| `arifos-mcp-call` | "call arifos", "mcp" | Direct arifOS MCP tool invocation |
