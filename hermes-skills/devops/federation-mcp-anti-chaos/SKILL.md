---
name: federation-mcp-anti-chaos
description: Prevent and diagnose MCP endpoint chaos, gateway slowness, and bot silence in the arifOS Federation
triggers:
  - bot silent
  - gateway slow
  - event loop P99
  - MCP URL confusion
  - "which endpoint is correct"
  - openclaw not responding
---

# Federation MCP Anti-Chaos Playbook

## Prevention Layers

### 1. MCP Endpoint Registry
- **Location:** `/root/VAULT999/MCP_ENDPOINT_REGISTRY.md`
- **Purpose:** Single source of truth for all MCP endpoints, transports, configs
- **Rule:** Update BEFORE changing any endpoint. All other refs must match.

### 2. Health Cron — federation-health-15min (job_id: 1b60179ec17e)
Every 15 min: checks all 4 public endpoints + gateway event loop P99.
Alerts Telegram home channel ONLY if something DOWN or P99 > 5000ms.

### 3. openclaw.json URL Rules
All run from VPS host (not inside container) — cannot use localhost:DockerPort.
| Service | Correct URL |
|---------|------------|
| arifOS | `https://arifos.arif-fazil.com/mcp` |
| WEALTH | `https://wealth.arif-fazil.com/mcp` |
| GEOX | `https://geox.arif-fazil.com/mcp` |
| WELL | `https://well.arif-fazil.com/mcp` |

### 4. Gateway Event Loop Thresholds
| P99 | Status | Action |
|-----|--------|--------|
| < 100ms | Healthy | None |
| 100-500ms | Elevated | Monitor |
| 500-2000ms | Warning | Investigate within 1 hour |
| 2000-10000ms | Critical | Restart gateway |
| > 10000ms | Choking | kill + restart immediately |

### 5. Transport Rule
All public endpoints = `streamable-http` at `/mcp`. No `/sse` needed. ChatGPT supports it directly.

## Diagnostic Commands

```bash
# Gateway health
curl -s http://localhost:18789/health

# Event loop P99
tail -20 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep liveness

# All endpoints
curl -s https://arifos.arif-fazil.com/health
curl -s https://geox.arif-fazil.com/health
curl -s https://wealth.arif-fazil.com/health

# openclaw.json URLs
grep '"url"' /root/.openclaw/openclaw.json | grep -v Binary

# Restart gateway
kill $(pgrep -f "openclaw.*gateway") 2>/dev/null; sleep 2
cd /tmp && nohup /usr/bin/node /usr/lib/node_modules/openclaw/dist/index.js gateway --port 18789 > /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log 2>&1 &
```

## Known Chaos Patterns

**Pattern 1: Bot silent, P99 > 10000ms**
→ MCP endpoint 404 or "Method not found" → gateway retry loop
→ Fix: Verify openclaw.json URLs vs registry. Restart gateway.

**Pattern 2: Bot silent, gateway 200 but no response**
→ Plugin initialization pile-up blocks Telegram handler
→ Fix: Restart, wait 30s before testing

**Pattern 3: "Which URL is correct?"**
→ Check `/root/VAULT999/MCP_ENDPOINT_REGISTRY.md`

**Pattern 4: ChatGPT "Method not found"**
→ Wrong transport. Use `/mcp` with `streamable-http` — not `/sse`.

**Pattern 5: Source and container diverge after live patch**
→ Container filesystem (`/app/server.py`) and source (`~/SERVICE/server.py`) are SEPARATE files.
→ Image build copies source at build time; live `docker exec` patches only the container layer.
→ Symptoms: Source looks correct, container is old (or vice versa).
→ Verify: `md5sum ~/SERVICE/server.py` vs `ssh root@af-forge "docker exec SERVICE md5sum /app/server.py"`
→ Fix: Patch both source and container, then rebuild + push image for reproducibility.

**Pattern 6: Entrypoint overrides config file**
→ Some services (e.g., WEALTH) have `entrypoint.sh` that hardcodes `transport='sse'` ignoring `fastmcp.json`.
→ Always check the actual entrypoint script, not just the config file.
→ Fix: Patch entrypoint.sh inside the container, then update source for next build.

---

**Pattern 7: NATS Docker `expose:` vs `ports:` Host Binding**

When NATS runs inside Docker Compose and you need host-side access (e.g., Python scripts on the VPS host connecting to `nats://127.0.0.1:4222`), `expose:` alone is insufficient.

| Directive | Effect |
|-----------|--------|
| `expose: [4222]` | Port reachable from other containers on the same Docker network. NOT from host. |
| `ports: ["127.0.0.1:4222:4222"]` | Port bound to host loopback. Reachable from host. F1-safe (no 0.0.0.0). |

```yaml
# Wrong — container-internal only
services:
  nats:
    image: nats:2.10
    expose:
      - "4222"

# Correct — host-accessible via 127.0.0.1 (F1-safe)
services:
  nats:
    image: nats:2.10
    ports:
      - "127.0.0.1:4222:4222"
```

Verify from host:
```bash
python3 -c "import nats; print(nats.__version__)"  # should print 1.x or 2.x
python3 -c "import asyncio; from nats import NATS; asyncio.run(NATS().connect('nats://127.0.0.1:4222')); print('connected')"
```

Note: nats-py v1.x and v2.x have different APIs:
- v2.14.0: `await nc.connect('nats://...')` — NO `timeout=` kwarg (raises TypeError)
- v1.x: `await nc.connect('nats://...')` — also no `timeout=` kwarg (same API)

---

**Pattern 9: Container Image Age Drift (Route Missing but Source Has It)**

A route is registered in source code but missing from the running container. The container wasn't patched — it was simply built from an older image that never got rebuilt.

**Symptoms:**
- `GET /mcp/stream` returns `404 Not Found` even though `server.py` source has `Route("/mcp/stream", ...)`
- `POST /mcp` (JSON) works fine — the SSE route specifically is missing
- Source code is newer than container filesystem
- No recent `docker exec` patches were applied

**Diagnosis:**
```bash
# Check container image build date
docker inspect CONTAINER_NAME --format '{{.Config.Image}} {{.Created}}'

# Check source file for the route
grep -n "/mcp/stream" /root/GEox/server.py

# Check container filesystem for the route
docker exec GEOX_CONTAINER grep "/mcp/stream" /app/server.py

# Compare dates
# Image created: 2026-05-06T11:29:27 — source was updated 2026-05-07
# → Container was built BEFORE the route was added to source
```

**Fix:** Requires image rebuild + `docker compose up -d --force-recreate`. This is a structural change (SEAL-blocked without 888 override for production systems).

**Prevention:** After any source change to server routes, always rebuild and push the image immediately. Do not leave old images deployed.

---

**Pattern 8: Adding `/tools` Discovery Endpoint to FastMCP Servers**

Federation Phase 1 requires all MCP servers to expose a REST `/tools` endpoint for federation-wide tool discovery. GEOX has it natively. WEALTH and WELL needed it added.

### When to use
- Server has no `GET /tools` endpoint
- Federation scanner returns `tools: []` or `schema: ?`
- Phase 1 federation work (tool discovery before real gateway)

### What `/tools` returns
```json
{
  "organ": "WEALTH",
  "role": "Capital Intelligence / NPV + EMV + Crisis Triage",
  "schema": "wealth-federation-v2026.05.07",
  "version": "2026.05.02",
  "count": 50,
  "danger_taxonomy": {
    "L4": "irreversible / operational mutation — fail-closed mandatory",
    "L3": "routing / memory / judgment — fail-closed mandatory",
    "L2": "session state — fail-open with constraint",
    "L1": "observe / degraded output — fail-open with constraint"
  },
  "fail_open_constraint": "may degrade output, must not elevate authority",
  "tools": [
    {
      "name": "wealth_vault_seal",
      "description": "...",
      "inputSchema": {},
      "outputSchema": {},
      "danger_level": "L4",
      "fail_posture": "fail-closed",
      "fail_open_constraint": null
    }
  ]
}
```

### Implementation template (Starlette + FastMCP)

In the `if __name__ == "__main__":` block of the server file:

```python
async def tools_handler(request):
    """Federation tool discovery — flat tool registry with danger/fail metadata."""
    all_tools = await mcp.list_tools()
    _DANGER_MAP = {
        # L4 — irreversible
        "tool_name_L4": {"danger_level": "L4", "fail_posture": "fail-closed"},
        # L3 — routing / judgment
        "tool_name_L3": {"danger_level": "L3", "fail_posture": "fail-closed"},
        # L2 — session state
        "tool_name_L2": {"danger_level": "L2", "fail_posture": "fail-open"},
        # L1 — observe
        "tool_name_L1": {"danger_level": "L1", "fail_posture": "fail-open"},
    }
    _FAIL_OPEN_CONSTRAINT = "may degrade output, must not elevate authority"
    tools = []
    for t in all_tools:
        name = t.name
        meta = _DANGER_MAP.get(name, {"danger_level": "L2", "fail_posture": "fail-open"})
        tools.append({
            "name": name,
            "description": getattr(t, "description", "") or "",
            "inputSchema": getattr(t, "inputSchema", {}),
            "outputSchema": getattr(t, "output_schema", {}),
            "danger_level": meta["danger_level"],
            "fail_posture": meta["fail_posture"],
            "fail_open_constraint": _FAIL_OPEN_CONSTRAINT if meta["fail_posture"] == "fail-open" else None,
        })
    return JSONResponse({
        "organ": "ORGAN_NAME",
        "role": "Role description",
        "schema": "organ-federation-vYYYY.MM.DD",
        "version": __version__,
        "count": len(tools),
        "danger_taxonomy": {
            "L4": "irreversible / operational mutation — fail-closed mandatory",
            "L3": "routing / memory / judgment — fail-closed mandatory",
            "L2": "session state — fail-open with constraint",
            "L1": "observe / degraded output — fail-open with constraint",
        },
        "fail_open_constraint": _FAIL_OPEN_CONSTRAINT,
        "tools": tools,
    })

# In Starlette routes (before uvicorn.run):
app.add_route("/tools", tools_handler, methods=["GET"])
```

### Verify after deploy
```bash
# Local
curl -s http://localhost:PORT/tools | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('organ:', d.get('organ'))
print('count:', d.get('count'))
print('schema:', d.get('schema'))
print('sample:', d['tools'][0]['name'], d['tools'][0]['danger_level'])
"
```

### Image + deploy workflow
```bash
# 1. Build
docker build -t ghcr.io/ariffazil/ORGAN:phase1-tools .

# 2. Push
docker push ghcr.io/ariffazil/ORGAN:phase1-tools

# 3. Restart
docker stop ORGAN-container && docker rm ORGAN-container
docker run -d --name ORGAN-container --restart unless-stopped -p PORT:PORT ghcr.io/ariffazil/ORGAN:phase1-tools

# 4. Verify
sleep 3 && curl -s http://localhost:PORT/tools | python3 -c "..."
```

### Also update
- `MCP_ENDPOINT_REGISTRY` at `/root/VAULT999/MCP_ENDPOINT_REGISTRY.md`
- `phase_status` in `arifOS/arifosmcp/tool_registry.json` → `federation_topology`
- Commit source + push to GitHub main

DITEMPA BUKAN DIBERI — Forged, not given.
DITEMPA BUKAN DIBERI — Forged, not given.
