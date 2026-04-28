---
name: arifos-mcp-meta-override
description: Override FastMCP's built-in /tools endpoint to expose tool meta (stage_code, risk_tier, use_when, authority_boundary) from tool_manifest.py in arifOS MCP servers. Also covers HEALTHCHECK /sse bug and bind mount docker cp Gotchas.
triggers:
  - FastMCP /tools returns no 'meta' field despite tools having annotations
  - tool_manifest.py exists but meta doesn't appear in HTTP /tools response
  - MCP client can't see stage_code, risk_tier, use_when, etc.
  - arifOS MCP container marked unhealthy with 404 on /sse
  - Docker cp permission denied with bind mountrw containers
code_version: 2026.04.26-KANON
status: verified-working
---

# Problem 1: FastMCP Built-in /tools Strips Meta

FastMCP v2's built-in `/tools` HTTP endpoint only exposes `name`, `description`, `parameters`. Any `meta` or `annotations` fields passed during tool registration are **silently dropped**. Constitutional metadata (stage_code, risk_tier, use_when, authority_boundary) from `tool_manifest.py` is invisible to HTTP MCP clients.

## Root Cause
FastMCP v2's HTTP app has built-in routes for `/tools` that read only core fields. `mcp._tool_manager` (v1) doesn't exist in v2 — the accessor is `mcp._local_provider._components`. `app.add_route("/tools", ...)` does NOT override existing routes — both coexist and FastMCP's built-in matches first.

## Solution: Custom Route Override in server.py

Add in the FastMCP HTTP app setup block. Must **prepend** at index 0 to override FastMCP's built-in:

```python
from starlette.routing import Route

async def tools_with_meta(request: Request) -> JSONResponse:
    from arifosmcp.tool_manifest import TOOL_MANIFEST
    from arifosmcp.server import mcp

    tool_summaries = []
    lp = mcp._local_provider
    for key, tool in lp._components.items():
        if not key.startswith("tool:"):
            continue
        raw = getattr(tool, "raw_tool", None) or getattr(tool, "_tool", None)
        if raw is None:
            continue
        tool_name = raw.name
        desc = getattr(raw, "description", "") or ""
        inp = getattr(raw, "inputSchema", {}) or {}
        stage = getattr(raw, "stage", "")
        lane = getattr(raw, "lane", "")
        manifest = TOOL_MANIFEST.get(tool_name, {})
        meta_dict = getattr(tool, "meta", None) or {}
        arifos_m = meta_dict.get("arifos_manifest", {}) or manifest
        entry = {
            "name": tool_name,
            "description": desc,
            "parameters": inp,
            "stage": arifos_m.get("stage_code", ""),
            "lane": arifos_m.get("lane", ""),
            "meta": {
                "arifos_manifest": arifos_m,
                "stage_code": meta_dict.get("stage_code", arifos_m.get("stage_code", "")),
                "stage_name": meta_dict.get("stage_name", arifos_m.get("stage_name", "")),
                "risk_tier": meta_dict.get("risk_tier", arifos_m.get("risk", {}).get("tier", "low")),
                "irreversible": meta_dict.get("irreversible", arifos_m.get("risk", {}).get("irreversible", False)),
                "requires_human_ack": meta_dict.get("requires_human_ack", arifos_m.get("risk", {}).get("requires_human_ack", False)),
                "use_when": arifos_m.get("use_when", []),
                "do_not_use_when": arifos_m.get("do_not_use_when", []),
                "next_recommended_tools": arifos_m.get("next_recommended_tools", []),
                "authority_boundary": arifos_m.get("authority_boundary", {}),
                "privacy_scope": arifos_m.get("privacy_scope", []),
            }
        }
        tool_summaries.append(entry)
    return JSONResponse({"tools": tool_summaries, "count": len(tool_summaries)})

# Prepend at index 0 to override FastMCP's built-in /tools
app.router.routes.insert(0, Route("/tools", tools_with_meta, methods=["GET"]))
```

---

# Problem 2: Dockerfile HEALTHCHECK Uses /sse on streamable-http

**Symptom:** Container marked `(unhealthy)` with 404 errors. Caddy's reverse proxy intermittently returns 404 for `mcp.arif-fazil.com` and `arifosmcp.arif-fazil.com`. External health monitors fire alerts.

**Root Cause:** Dockerfile's HEALTHCHECK hits `/sse` — an SSE transport endpoint. But arifOS MCP runs `streamable-http` transport. FastMCP returns 404 → Docker marks container unhealthy → Caddy's `handle /mcp*` routes become unreliable.

```dockerfile
# WRONG — /sse does not exist on streamable-http transport
HEALTHCHECK --interval=20s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -fsS --max-time 3 http://localhost:8080/sse || exit 1

# CORRECT — use /health
HEALTHCHECK --interval=20s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -fsS --max-time 3 http://localhost:8080/health || exit 1
```

---

# Problem 3: Docker cp Permission Denied with Bind Mounts

**Symptom:** `docker cp host→container:/usr/src/app/...` fails with `Permission denied` even with root.

**Root Cause:** The compose bind mount `/root/arifOS → /usr/src/app` is `root:root` owned but the container process runs as `uid=1000(arifos)`. The mount point is mounted `rw` but the directory permissions on the host are `root:root` so the container user can't write to it.

**Two-step workaround — use /tmp as staging:**
```bash
# Copy to container's /tmp (which is writable)
docker cp server.py arifosmcp:/tmp/server_new.py

# Use root inside container to copy from /tmp to /usr/src/app
docker exec --user root arifosmcp cp /tmp/server_new.py /usr/src/app/arifosmcp/server.py

# Restart to reload
docker restart arifosmcp
```

**Or just rebuild the image** — cleaner, ensures the fix is baked in:
```bash
cd /root/arifOS
docker build -t ariffazil/arifos:2026.04.26-KANON -t compose-arifosmcp:sovereign-mirror .
docker compose -f /root/compose/docker-compose.yml up -d --build arifosmcp
```

---

# Verification

```bash
# Local /tools with meta
curl http://localhost:8080/tools | python3 -c "
import sys,json; d=json.load(sys.stdin)
t = d['tools'][0]
print('Keys:', list(t.keys()))
print('meta present:', 'meta' in t)
print('stage_code:', t.get('meta',{}).get('stage_code'))
"

# Inside container via TestClient (bypasses Caddy)
docker exec arifosmcp python3 -c "
import sys; sys.path.insert(0,'/usr/src/app')
from starlette.testclient import TestClient
from arifosmcp.server import app
client = TestClient(app)
r = client.get('/tools')
d = r.json()
print('status:', r.status_code)
print('keys:', list(d['tools'][0].keys()))
"

# Public endpoint
curl https://mcp.arif-fazil.com/tools 2>/dev/null | python3 -c "
import sys,json; d=json.load(sys.stdin)
print(f'count: {d[\"count\"]}')
print(f'first meta.stage_code: {d[\"tools\"][0][\"meta\"][\"stage_code\"]}')
"

# Container health
docker inspect arifosmcp --format '{{.State.Health.Status}}'
```

---

# Files Involved
- `arifosmcp/server.py` — where override is added
- `arifosmcp/tool_manifest.py` — `TOOL_MANIFEST` dict source
- `arifosmcp/runtime/tools.py` — `register_tools()` passes `meta={}` to FastMCP
- `Dockerfile` — HEALTHCHECK configuration (fix: `/sse` → `/health`)
- `compose/docker-compose.yml` — arifosmcp service with bind mount

---

# Lessons
1. Always verify via `TestClient` inside container — external curl routes through Caddy which can mask issues
2. FastMCP v2 doesn't expose annotations/meta in HTTP — custom route required
3. Check which `app` object is served (`runtime.server:app` vs `server:app`) — routes set at import time
4. Bind mount perms block runtime edits — rebuild image or use the /tmp workaround
5. HEALTHCHECK must use `/health` for streamable-http transport, never `/sse`
6. `app.router.routes.clear()` DELETES all routes — never use. Prepend at index 0 instead.


# Problem

FastMCP v2's built-in `/tools` HTTP endpoint only exposes `name`, `description`, `parameters`. Any `meta` or `annotations` fields passed during tool registration are **silently dropped**. Constitutional metadata (stage_code, risk_tier, use_when, authority_boundary) from `tool_manifest.py` is invisible to HTTP MCP clients.

---

# Root Cause

FastMCP v2's HTTP app has built-in routes for `/tools` that read only core fields. `mcp._tool_manager` (v1) doesn't exist in v2 — the accessor is `mcp._local_provider._components`. `app.add_route("/tools", ...)` does NOT override existing routes — both coexist and FastMCP's built-in matches first.

---

# Solution: Custom Route Override in server.py

Add in the FastMCP HTTP app setup block. Must **prepend** at index 0 to override FastMCP's built-in:

```python
async def tools_with_meta(request: Request) -> JSONResponse:
    from arifosmcp.tool_manifest import TOOL_MANIFEST
    tool_summaries = []
    try:
        lp = getattr(mcp, "_local_provider", None)
        if lp:
            raw_tools = {k: v for k, v in lp._components.items() if k.startswith("tool:")}
        else:
            raw_tools = {}
        for name, tool in raw_tools.items():
            tool_name = name.replace("tool:", "").rstrip("@")
            base = {"description": tool.description or "", "parameters": tool.parameters or {}}
            manifest = TOOL_MANIFEST.get(tool_name, {})
            meta_dict = getattr(tool, "meta", None) or {}
            arifos_m = meta_dict.get("arifos_manifest", {}) or manifest
            entry = {
                "name": tool_name,
                "description": base["description"],
                "parameters": base["parameters"],
                "stage": arifos_m.get("stage_code", ""),
                "lane": arifos_m.get("lane", ""),
                "meta": {
                    "arifos_manifest": arifos_m,
                    "stage_code": meta_dict.get("stage_code", arifos_m.get("stage_code", "")),
                    "stage_name": meta_dict.get("stage_name", arifos_m.get("stage_name", "")),
                    "risk_tier": meta_dict.get("risk_tier", arifos_m.get("risk", {}).get("tier", "low")),
                    "irreversible": meta_dict.get("irreversible", arifos_m.get("risk", {}).get("irreversible", False)),
                    "requires_human_ack": meta_dict.get("requires_human_ack", arifos_m.get("risk", {}).get("requires_human_ack", False)),
                    "use_when": arifos_m.get("use_when", []),
                    "do_not_use_when": arifos_m.get("do_not_use_when", []),
                    "next_recommended_tools": arifos_m.get("next_recommended_tools", []),
                    "authority_boundary": arifos_m.get("authority_boundary", {}),
                    "privacy_scope": arifos_m.get("privacy_scope", []),
                    "canonical_order": meta_dict.get("canonical_order", arifos_m.get("canonical_order", [])),
                }
            }
            tool_summaries.append(entry)
    except Exception as e:
        logger.warning(f"Failed to build meta-enriched tools response: {e}")
        tool_summaries = []
    return JSONResponse({"tools": tool_summaries, "count": len(tool_summaries)})

from starlette.routing import Route
tools_meta_route = Route("/tools", tools_with_meta, methods=["GET"])
app.router.routes.insert(0, tools_meta_route)  # prepend to override
```

---

# Key Discovery Points

1. **FastMCP v2 tool accessors**: `mcp._local_provider._components` (dict, keys `"tool:NAME@"`); `tool.meta` (dict with arifos_manifest); `tool.description`; `tool.parameters`
2. **Route override**: `app.add_route("/tools", ...)` does NOT override — must use `app.router.routes.insert(0, Route(...))`
3. **Bind mount permissions**: Container runs as `uid=1000(arifos)` but bind mount files are `root:root` — runtime `docker cp` and `touch` inside mount point will fail with Permission Denied. Must rebuild image to update mounted files.
4. **Two source trees**: `/root/arifOS` (primary, git repo) and `/opt/arifos/src/arifOS` (symlink target at `/root/arifos → /opt/arifos/src/arifOS`) — bind mount serves from `/opt/arifos/src/arifOS`. Keep in sync via filesystem or rebuild.
5. **Bind mount write workaround**: Container runs as `uid=1000(arifos)` but bind mount files are `root:root` (read-only for non-root). Cannot `docker cp` directly into mount point. Two valid workarounds: (a) `docker cp <file> CONTAINER:/tmp/<file> && docker exec --user root CONTAINER cp /tmp/<file> /usr/src/app/arifosmcp/<file>` then restart; (b) rebuild the image — bind mount files are updated at container start, so the new binary is in the image. Rebuild is cleaner for production.
6. **Post-rebuild bind mount update**: After `docker compose up -d --build arifosmcp`, the new image is used but the bind mount still serves the source tree files — changes to `/root/arifOS` are reflected immediately without rebuild. However if `server.py` was changed in the image, you must restart the container (`docker restart arifosmcp`) for the new Python module bytes to be loaded.

---

# Verification

```bash
curl -s http://localhost:8080/tools | python3 -c "
import sys,json; d=json.load(sys.stdin)
t = d['tools'][0]
print('Keys:', list(t.keys()), 'meta present:', 'meta' in t)
if 'meta' in t:
    m = t['meta']
    print('stage_code:', m.get('stage_code'), 'risk_tier:', m.get('risk_tier'))
print('count:', d.get('count'))
for t in d['tools']:
    m = t.get('meta',{})
    print(f'  {t[\"name\"]}: stage={m.get(\"stage_code\")} risk={m.get(\"risk_tier\")}')
"
```

---

# Files Involved

- `arifosmcp/server.py` — where override is added (in `if IS_FASTMCP_3` block)
- `arifosmcp/tool_manifest.py` — `TOOL_MANIFEST` dict source
- `arifosmcp/runtime/tools.py` — `register_tools()` passes `meta={}` to FastMCP
- `compose/docker-compose.yml` — arifosmcp service with bind mount

---

# Lessons

1. Always verify via `TestClient` inside container — external curl routes differently
2. FastMCP v2 doesn't expose annotations/meta in HTTP — custom route required
3. Check which `app` object is served (`runtime.server:app` vs `server:app`) — routes set at import time
4. Bind mount perms block runtime edits — rebuild image, don't `docker cp`

**DITEMPA BUKAN DIBERI — Forged, Not Given**