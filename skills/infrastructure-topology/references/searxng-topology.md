# SearXNG Sovereign Search — Federation Wiring Topology

> Verified 2026-08-12 by live probe. Canonical reference for all agents that use web search.

## Architecture Principle

```
Layer Atas (Federated)  : Gemini 3.6 Flash + DashScope PAYG (model reasoning)
Layer Bawah (Owned)     : SearXNG :8080 (search), VAULT999 (truth), A-FORGE (execution)
Decoupling             : Search layer survives model layer outage
```

## The Wiring Chain (every link verified)

### 1. Docker Service (source)
- Container: `searxng` (Docker, via `docker-proxy`)
- Port: `127.0.0.1:8080` (localhost-only, not exposed externally)
- Image: `searxng/searxng:2026.7.7+f69b22c45`
- Network: `arifos_core_network`
- Running since: Jul 23 (stable)
- Worker: `searxng worker-1` (pid 6213, started Jul 23)

### 2. Verify the service
```bash
# Process check
ps aux | grep searxng | grep -v grep

# Port binding
ss -tlnp | grep :8080

# Functional test — returns JSON with results
curl -s "http://localhost:8080/search?q=test&format=json" | python3 -c "
import sys,json; d=json.load(sys.stdin)
print(f'results={len(d.get(\"results\",[]))} unresponsive={d.get(\"unresponsive_engines\",[])}')
"

# HTML interface check
curl -s -o /dev/null -w "HTTP:%{http_code} SIZE:%{size_download}\n" "http://localhost:8080/"
# Should return HTTP:200 SIZE:~6306
```

### 3. Hermes Global Config
File: `/root/.hermes/config.yaml`
```yaml
web:
  backend: searxng
  search_backend: searxng
  extract_backend: searxng
```

### 4. Hermes Per-Profile Configs
All profiles wired identically (no split-brain):
- `/root/.hermes/profiles/hermes_forge/config.yaml` — `search_backend: searxng`
- `/root/.hermes/profiles/hermes_apex/config.yaml` — `search_backend: searxng`
- `/root/.hermes/profiles/aaa-hermes/config.yaml` — (inherits global)

### 5. A-FORGE MCP (forge_fetch / forge_search)
File: `/root/A-FORGE/src/interfaces/mcp/proxyTools.ts` (line 1129)
```typescript
const searxngBase = (params.searxng_url || params.url || "http://localhost:8080");
```
Default URL is hardcoded to localhost:8080. forge_fetch queries go directly to SearXNG.

### 6. Environment Variables
File: `/root/.secrets/kunci-mas.env`
```
SEARXNG_SECRET=<sha256-hex>
SEARXNG_URL=http://127.0.0.1:8080
```
Also in `/root/.secrets/kunci-mas.flat.env` (consumed by systemd).

### 7. Systemd Services (consume env at boot)
- `hermes-asi-gateway.service` — loads `kunci-mas.flat.env` via `EnvironmentFiles=`
- `aforge.service` — loads `kunci-mas.flat.env`
- `hermes-agent-mcp.service` — loads `kunci-mas.flat.env`

## Upstream Engines (SearXNG aggregates)

SearXNG combines results from multiple engines. One engine failing ≠ search failing.

| Engine | Status (2026-08-12) | Notes |
|---|---|---|
| Google CSE | ✅ Live | Primary results source |
| DuckDuckGo | ✅ Live | Secondary, good for MY-specific |
| Wikipedia | ✅ Live | Infoboxes |
| Startpage | ⚠️ CAPTCHA | Suspended intermittently, normal |

Check `unresponsive_engines` in JSON response for current engine status.

## Troubleshooting

### SearXNG returns empty JSON
1. Check process: `ps aux | grep searxng`
2. Check port: `ss -tlnp | grep :8080`
3. Check container: `docker ps | grep searxng`
4. Restart: `docker restart searxng`
5. Check logs: `docker logs searxng --tail 50`

### Search results missing despite SearXNG running
- Check `unresponsive_engines` in JSON response
- One engine failing ≠ SearXNG failing
- Startpage `Suspended: CAPTCHA` is normal — other engines compensate

### Provider outage ≠ search outage
The whole point: if Gemini/OpenAI/etc. go down, SearXNG still works. If search is broken, models still reason. They are decoupled by design.
