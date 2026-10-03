<!-- PROVENANCE: source_skill=sovereign-search -->
<!-- original_path=/root/AAA/skills/domains/general/workshop/search-web/sovereign-search/SKILL.md -->
<!-- original_sha256=97dda63c51a3a62255769ad48fef5786012faed2c45fe17afb0b7353b3c54661 · archived_to=/root/AAA/skills/.archive/merge-20260920/web/sovereign-search/ -->
<!-- body_verbatim=true · merged_at=2026-09-20T14:39:14Z · umbrella=web-ops -->
---
name: sovereign-search
description: "Self-host web search for Hermes Agent — SearXNG deployment, Tavily/Brave migration, config unification, and zero-API-key architecture"
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [hermes, search, searxng, self-hosted, sovereign]
---

# Sovereign Search

Self-host web search backend for Hermes Agent. Eliminates external API key dependency, monthly quotas, and vendor lock-in. The principle: **own the metal, don't rent the API.**

## When to Use

- `web_search` returns 432 (quota exhausted), 401 (key invalid), or 429 (rate limited)
- Arif says "hak asasi warga AAA" for search
- You want zero-cost, zero-quota web search
- Tavily/Brave API keys are dead or about to expire

## Architecture

```
Agent → web_search → Hermes config (search_backend: searxng) → SearXNG :8080 → DuckDuckGo/Google/etc
```

SearXNG is a privacy-respecting metasearch engine. It proxies queries to upstream engines (DuckDuckGo, Google, Wikipedia, etc.) with zero API keys required for most engines.

## Quick Fix: Switch Existing Hermes to Local SearXNG

If SearXNG is already running locally (check: `curl -sI http://localhost:8080 | head -1`):

```bash
# Unify all backends to SearXNG
hermes config set web.search_backend searxng
hermes config set web.backend searxng
hermes config set web.extract_backend searxng
hermes config set search.search_backend searxng
hermes config set search.backend searxng
```

Verify no split-brain:
```bash
grep -A4 "^web:" ~/.hermes/config.yaml
grep -A3 "^search:" ~/.hermes/config.yaml
```

**Both sections must point to `searxng`.** If they differ, `web_search` may still route through the old dead backend.

Set the URL:
```bash
export SEARXNG_URL="http://127.0.0.1:8080"  # in ~/.hermes/.env or vault.env
```

**Restart required**: `/reset` the session or restart Hermes for config to take effect.

## Deploying SearXNG (if not running)

```bash
# Docker — quickest
docker run -d --name searxng \
  -p 127.0.0.1:8080:8080 \
  -v searxng-config:/etc/searxng \
  searxng/searxng:latest

# Verify
curl -s "http://127.0.0.1:8080/search?q=test&format=json" | python3 -c "import sys,json; print(len(json.load(sys.stdin)['results']), 'results')"
```

Default config uses DuckDuckGo + Google CSE. DuckDuckGo is zero-API-key. Google CSE needs a key — disable it in settings.yml if you don't have one.

## Diagnosing Dead Backend

When `web_search` fails:

1. **Check the error**: 432 = Tavily quota, 401 = invalid key, 429 = rate limit
2. **Check current config**: `grep search_backend ~/.hermes/config.yaml`
3. **Check for split-brain**: Both `web:` and `search:` sections must agree
4. **Check SearXNG alive**: `curl -sI http://localhost:8080 | head -1` → should be 200
5. **Test SearXNG directly**: `curl -s "http://127.0.0.1:8080/search?q=test&format=json"`

If SearXNG returns results but Hermes doesn't → config or restart issue. If SearXNG itself is down → Docker restart.

## Image search — the lane agents forget exists

SearXNG serves images through the same endpoint with `categories=images`. No key, no quota,
no third party. Verified live 2026-10-02 (KVM8, SearXNG in Docker at `127.0.0.1:8080`).

```bash
curl -s "http://127.0.0.1:8080/search?q=%22Sushi+Mentai%22+Sri+Petaling&format=json&categories=images" \
 | python3 -c "
import sys,json
for r in json.load(sys.stdin).get('results',[])[:10]:
    print(r.get('title','')[:60], '|', r.get('img_src',''))
"
```

`img_src` is the direct image URL; `url` is the page it came from. Download with a browser
UA (`-A "Mozilla/5.0"`) or some hosts 403. Then verify the bytes are really an image
(`file <path>`, non-trivial size) before claiming you have one — a 200 response can still
be an HTML error page.

Query discipline: quoted proper nouns keep results on-target. An unquoted multi-concept
query (`sushi mentai sri petaling sashimi maki`) drifts into stock photography and museum
catalogue pages; `"Sushi Mentai" Sri Petaling` returned the actual restaurant's plates.

## Do not "fix" a working lane by bypassing its governance layer

`web.backend: aaa-state` routes search/extract through A-FORGE (`AAA_WEB_GATEWAY_URL`,
default `http://127.0.0.1:7072/mcp`) → `forge_search` / `forge_web_extract`, which adds
evidence tracking and audit receipts, with Brave primary and SearXNG fallback. That is a
deliberate design, not a misconfiguration.

The `hermes config set web.*_backend searxng` recipe above is for the case where `aaa-state`
itself is dead. Before repointing anything, probe the configured lane end to end:

```bash
curl -sS -m 20 -X POST http://127.0.0.1:7072/mcp \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"forge_search",
       "arguments":{"query":"<real query>","source":"web","count":3,"request_id":"probe"}}}'
```

`status: OK` with results means the lane is alive — switching to bare `searxng` would trade a
governed, audited path for an ungoverned one to fix nothing.

## Pitfalls

- **FALSE-ABSENCE CLAIM — the lane is alive and the agent said it wasn't (2026-10-02, measured)**: Hermes reported "web lanes ke laut (cert path rosak + MCP firecrawl down)" and told the sovereign to Google it himself. Every leg of that claim was false: TLS verified clean (`ssl_verify=0`, CA bundle present, target site HTTP 200); `mcp.firecrawl.dev` returned 405, which is a *live* POST-only MCP endpoint answering a GET; `FIRECRAWL_API_KEY` was present in ten secret stores; and the configured backend wasn't even firecrawl. The real lane (`aaa-state` → `:7072` → `forge_search`) returned correct results on the first probe, and `forge_web_extract` returned `status: ok`. **Before any claim of "no web access", "cert broken", or "MCP down", run the probe above and report what it returned.** An unprobed absence claim that ends with the human doing the work is a HARAM-1/HARAM-3 violation, not an honest limit. Note `firecrawl_scrape` genuinely refuses *some* sites ("we do not support this site") — that is a per-site limitation of the hosted lane, not an outage, and `forge_web_extract` is the fallback.

- **SILENT ARCHIVED BACKEND — the "agent looks broken" trap**: Config can point at `searxng` while the container no longer runs. On homelab entropy sweeps, SearXNG gets moved to `_archive/<date>/searxng/` (compose + settings + README) and the container is removed — but `web.backend: searxng` stays in config. Result: `web_search` fails **silently** (no quota error, no HTTP 4xx surfacing), the agent can't answer, and to humans it looks like a regression in agent intelligence when it's actually dead infra. **When a user says "agent X is useless / broken / keeps asking me to search myself", FIRST probe the search backend before touching persona/doctrine.** Check: `docker ps --filter name=searxng` (empty = down), `docker compose ls` (is the project there?), `ls /root/_archive/*/searxng/` (did it get archived?). The fix is a restore, not a behavioral patch.
- **Configured-vs-running split**: Two independent states — (a) config points at searxng, (b) searxng actually runs. They drift independently. Diagnose BOTH:
  - config: `grep -A4 "^web:" ~/.hermes/config.yaml`
  - running: `docker ps --filter name=searxng --format '{{.Names}}\t{{.Status}}'`
- **Archived restore needs the redis sidecar**: `settings.yml` references `redis: url: unix:///run/redis-searxng/redis.sock?db=0` for search caching, but the archived compose file often does NOT declare a redis service. SearXNG starts anyway (HTTP 200) but redis crash-loops with `Failed opening Unix socket: bind: Permission denied`. Restore requires adding a redis:7-alpine sidecar sharing a `searxng-redis-run` volume, mounted into BOTH containers at `/run/redis-searxng`, with `command: sh -c "chmod 777 /run/redis-searxng && exec redis-server --unixsocket /run/redis-searxng/redis.sock --unixsocketperm 766"`. Full recipe: `references/searxng-archive-restore.md`.
- **"unhealthy" docker state despite HTTP 200 — wget/curl healthcheck trap**: The `searxng/searxng:latest` image ships `wget` but NOT `curl`. A compose healthcheck like `test: ["CMD", "curl", "-f", "..."]` will fail every time → docker reports `Up X (unhealthy)` while the search endpoint genuinely returns HTTP 200. The service works; only the healthcheck lies. Fix: swap the healthcheck to wget: `test: ["CMD", "wget", "-q", "--spider", "http://localhost:8080/search?q=test&format=json"]`. Verify the image's binary before writing a healthcheck: `docker exec searxng sh -c 'which curl wget'`. Don't trust `docker ps` "health" alone — always `curl` the endpoint directly.
- **COMPOSE_PROJECT_NAME namespace leak**: If an env var `COMPOSE_PROJECT_NAME=af-forge` is exported in the shell, `docker compose up` from `/root/searxng/` resolves the project to `af-forge` and pollutes the A-FORGE stack namespace (`af-forge_searxng-redis-*` volumes, orphan warnings). Always pin explicitly: `docker compose -p searxng up -d`. If you already created orphaned containers/volumes under the wrong namespace, `docker rm -f <name>` + `docker volume rm -f <vol>` before re-up.
- **Tavily 432 + DDG CAPTCHA Cascade & F2/F9 Constitutional Refusal**: If `web.extract_backend` or `web.search_backend` defaults to Tavily, hitting Tavily's quota limit returns `HTTP 432 Client Error`. If the agent then attempts direct curl/python scraping against DuckDuckGo, DDG blocks with a CAPTCHA challenge. Under F2 TRUTH / F9 ANTI-HANTU doctrines (`unknown_beats_invented: true`), the agent will refuse to fabricate and output an honest infra failure report ("Abang, semua jalan mati..."). **Important Architectural Distinction**: This refusal is NOT a bug — it is **F2/F9 working as designed** (preventing hallucinations like "sapu flanil = sauna"). Fix the infra layer by unifying `web.*` config keys (`web.backend`, `web.search_backend`, `web.extract_backend`) to `searxng` and restarting `hermes-asi-gateway.service`. F2/F9 remains the permanent constitutional backstop if SearXNG or upstream search ever fails in the future.
- **Split-brain config**: `web.search_backend` and `search.search_backend` are DIFFERENT config keys. The `web_search` tool uses `web.*` section. Unify both.
- **Restart required**: Config changes don't take effect mid-session. Need `/reset` or Hermes restart.
- **SearXNG engine failures**: Individual upstream engines (Brave, Startpage) may rate-limit. DuckDuckGo is most reliable free engine.
- **`use_default_settings: true` pitfall**: If Brave engine is enabled in settings.yml but API key doesn't propagate, check if `use_default_settings: true` is overriding custom engine configs. Add `disabled: false` and `api_key` explicitly, then `docker restart searxng`.
- **Docker bind-mount**: If settings.yml is bind-mounted (check: `docker inspect searxng --format '{{json .Mounts}}'`), edit the HOST file (e.g. `/root/searxng/settings.yml`) then `docker restart searxng`. Do NOT edit inside the container — bind mounts are read-only.
- **DuckDuckGo IP block risk**: If 5+ agents hammer SearXNG concurrently, DuckDuckGo may block the homelab IP. Enable MULTIPLE engines for resilience — SearXNG silently rotates to the next engine if one fails.
- **Datacenter-IP scraper block cascade (2026-08-14)**: Over time ALL free scrapers (ddg timeout, google cse "too many requests", startpage CAPTCHA, qwant/mojeek/wikipedia 0) die from one flagged VPS IP while the instance stays HTTP 200. The sovereign backstop is an API-KEY engine (Brave) — keys are immune to IP reputation. Keep `brave` enabled with `api_key:` inline in settings.yml (root-only file; the container has no env). Suspended scrapers auto-resume later and rejoin rotation.
- **Secrets never round-trip through the terminal**: the terminal tool masks env secret values in output. Do NOT copy a masked value into config — inject via `set -a; source env; python3` reading `os.environ` directly, then `chmod 600` the settings file.

## Verification

```bash
# 1. SearXNG alive
curl -sI http://localhost:8080 | head -1  # HTTP/1.1 200 OK

# 2. Config unified
grep -A4 "^web:" ~/.hermes/config.yaml | grep backend  # all "searxng"

# 3. Multi-engine health check (count + which engines responded)
curl -s "http://localhost:8080/search?q=test&format=json" | python3 -c "
import sys,json
d=json.load(sys.stdin)
engines=set(r.get('engine','?') for r in d.get('results',[]))
print(f'{len(d.get(\"results\",[]))} results from engines: {engines}')
"
# Expected: >5 results from {duckduckgo, google cse} or similar
# If only 0-2 results or one engine → investigate Docker logs

# 4. Live test (after /reset)
# Use web_search in-session — should return results without quota errors
```

### Full sovereign bootstrap (SearXNG + WM + A-FORGE)

For a complete autonomous deployment mission — 5 phases: clone, build, test, Docker SearXNG, Hermes config, WM verification, report — see the reusable prompt template at:
- `references/autonomous-bootstrap-template.md`

## References

- `references/autonomous-bootstrap-template.md` — reusable prompt template for a full autonomous SearXNG deployment mission (5 phases)
- `references/searxng-archive-restore.md` — full recipe for restoring an archived SearXNG (redis sidecar + COMPOSE_PROJECT_NAME pin + verification)
- `references/settings-multi-engine.yml` — production SearXNG config with DuckDuckGo + Brave + Google + Redis caching
