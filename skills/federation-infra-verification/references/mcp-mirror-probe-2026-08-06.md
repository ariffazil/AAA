# Mirror-MCP Verification — Local ↔ Public Endpoint Identity

When the federation claims a "mirror" structure (local port + public URL exposing the same MCP surface),
this probe confirms the mirror is real, not aspirational. Used in the 2026-08-06 arifOS audit
when Arif asked: *"do we have mirror MCP structure or what?"*

## The mirror pattern

Each federation organ that exposes MCP has two endpoints:

```
LOCAL    http://127.0.0.1:<port>/mcp
PUBLIC   https://<sub>.arif-fazil.com/mcp
```

A true mirror means: same tool list, same version hash, same contract — accessible from either.

A non-mirror (drift) means: local serves current tools, public serves stale snapshot (or vice versa).

## Probe recipe (verified 2026-08-06, arifOS)

```python
import json, urllib.request

def tools_at(url, label):
    """MCP handshake: initialize, then tools/list, return tool names."""
    init = {"jsonrpc":"2.0","id":1,"method":"initialize","params":{
        "protocolVersion":"2025-11-25","capabilities":{},
        "clientInfo":{"name":"mirror-probe","version":"1.0"}}}
    req = urllib.request.Request(url, data=json.dumps(init).encode(),
        headers={"Content-Type":"application/json","Accept":"application/json"})
    r = urllib.request.urlopen(req, timeout=10)
    init_resp = json.loads(r.read().decode())
    server = init_resp["result"]["serverInfo"]

    # tools/list (no session header needed if server uses plain JSON transport)
    tl = {"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}
    req2 = urllib.request.Request(url, data=json.dumps(tl).encode(),
        headers={"Content-Type":"application/json","Accept":"application/json"})
    r2 = urllib.request.urlopen(req2, timeout=10)
    tools_resp = json.loads(r2.read().decode())
    tools = [t["name"] for t in tools_resp.get("result",{}).get("tools",[])]

    return server, sorted(tools)

# Probe both endpoints
local_srv, local_tools = tools_at("http://127.0.0.1:8088/mcp", "LOCAL")
pub_srv,   pub_tools   = tools_at("https://arifos.arif-fazil.com/mcp", "PUBLIC")

# Compare
print(f"server name match:   {local_srv['name'] == pub_srv['name']}")
print(f"server version match: {local_srv['version'] == pub_srv['version']}")
print(f"tool count match:    {len(local_tools) == len(pub_tools)}")
print(f"tool set match:      {local_tools == pub_tools}")
```

### Why this recipe works (the trap it avoids)

The MCP-spec transport is `text/event-stream` (SSE), but `arifOS` answers with **plain JSON** instead —
content-type `application/json`, no session header, no SSE framing. If you send `Accept: text/event-stream`
the kernel still answers plain JSON, but if you try to parse SSE (`data: {...}` lines) you get 0 tools
and conclude the kernel is broken. It's not — it's a transport variant.

**The fix:** set `Accept: application/json` (single header, no SSE) and parse JSON directly. Don't try to
read SSE lines from a plain-JSON response.

### What the mirror probe should show

| Field | Expected |
|---|---|
| `serverInfo.name` | `"ARIFOS MCP"` (both endpoints) |
| `serverInfo.version` | Same git hash, e.g. `kanon-2026.08.06+64bd2f8` |
| Tool count | Same number on both endpoints |
| Tool set | Identical sorted list |

If version hashes differ between local and public, the public deployment is stale. If the tool set
differs, someone added a tool to one side without mirroring.

### Verified result (2026-08-06, arifOS)

```
server name match:     True
server version match:  True (kanon-2026.08.06+64bd2f8)
tool count match:      True (8 = 8)
tool set match:        True (sorted identical: arif_forge, arif_init, arif_judge,
                        arif_memory, arif_observe, arif_route, arif_seal, arif_think)
```

Net: mirror is real, byte-for-byte. Single source of truth behind two transports.

## Edge cases

1. **Cloudflare Tunnel cache.** Public endpoint may serve a Cloudflare-edge cached response stale by
   minutes-to-hours. If the version mismatches by commit hash, force a fresh fetch with `Cache-Control: no-cache`
   header or check Cloudflare cache rules.

2. **Self-signed TLS on local.** Public endpoints go through Cloudflare and have valid certs. Local probes
   over HTTP, no cert issue.

3. **Behind Cloudflare Access.** Some federation subdomains sit behind Cloudflare Access with email OTP.
   If `https://<sub>.arif-fazil.com/mcp` returns 403, the subdomain has Access enabled — needs the
   user-level token in a `cf-access-token` header. arifOS public is currently NOT behind Access (verified).

4. **Timeout on first handshake.** Public endpoint first call can take 2-3s for TLS handshake + CDN warm.
   Set `timeout=10` for safety.

## When the mirror is NOT real

If local serves 8 tools but public serves 6, the public is stale. Causes:
- Deploy ran only on local (e.g. `make deploy-local` but no `rsync` to deploy root)
- Cloudflare cache held old response
- Public route wasn't registered in Caddyfile / Cloudflare config

Fix recipe: re-run the organ's deploy script (`make deploy-full` from the organ's repo), wait 60s for
edge cache to expire, re-probe.

## Quick single-line check (if you trust the MCP service to be uniform)

```bash
# Compare tool names between local and public, side by side
diff <(curl -s http://127.0.0.1:8088/mcp -X POST -H 'Content-Type: application/json' \
       -H 'Accept: application/json' -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"x","version":"1"}}}' \
       | python3 -c "import sys,json,urllib.request; r=urllib.request.urlopen('http://127.0.0.1:8088/mcp'); print(r.read())" 2>/dev/null) \
     <(curl -s https://arifos.arif-fazil.com/mcp ... )
```

The single-line version is brittle. Use the Python recipe above — it works, it's 20 lines, and the
version hash comparison catches drift the diff alone would miss.

## Federation topology expected mirrors

Per `AAA/docs/ORGAN.md`:

| Organ | Local port | Public subdomain |
|---|---|---|
| arifOS | :8088 | https://arifos.arif-fazil.com/mcp |
| A-FORGE | :7071 / :7072 | https://mcp.arif-fazil.com/mcp |
| AAA | :3001 | https://aaa.arif-fazil.com |
| GEOX | :8081 | https://geox.arif-fazil.com/mcp |
| WEALTH | :18082 | https://wealth.arif-fazil.com/mcp |
| WELL | :18083 | https://well.arif-fazil.com/mcp |

Verify as many of these as needed by changing the URL pair in the recipe. Each pair should show:
- Same server name
- Same version hash
- Same tool set
- Same number of tools

If a pair diverges, the public is stale — re-deploy the organ.
