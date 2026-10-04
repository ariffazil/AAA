## Quick-start — MiniMax Media MCP

**Endpoint:** http://127.0.0.1:18100/mcp (streamable-http)
**Service:** `/etc/systemd/system/minimax-media-mcp.service` (default port 18090, blocked by hermes bridges)
**Live launcher:** `/opt/minimax-mcp-media/run_v2.py` (sets port 18100, overrides .env hardcode)
**Key:** `MINIMAX_API_KEY` in `/root/.secrets/vault.flat.env`

### Check if alive
```bash
ss -tlnp | grep 18100
```

### Python call helper (works with any script)
```python
import json, time, requests

MCP = "http://127.0.0.1:18100/mcp"

def init_mcp():
    r = requests.post(MCP, headers={
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    }, json={"jsonrpc":"2.0","method":"initialize","params":{
        "protocolVersion":"2025-11-25","capabilities":{},
        "clientInfo":{"name":"hermes","version":"1"}
    },"id":1})
    return r.headers.get("mcp-session-id","").strip()

def call_tool(sid, name, args):
    r = requests.post(MCP, headers={
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "mcp-session-id": sid
    }, json={"jsonrpc":"2.0","method":"tools/call","id":int(time.time()),
            "params":{"name":name,"arguments":args}})
    for line in r.text.splitlines():
        if line.startswith("data: "):
            return json.loads(line[6:])
```

### generate_video args
```python
{
    "model": "MiniMax-Hailuo-02",   # best quality (or T2V-01-Director for camera control)
    "prompt": "...",
    "duration": 6,                   # 6 or 10 for Hailuo-02 only
    "resolution": "1080P",           # 768P or 1080P (Hailuo-02 only)
    "output_directory": "/tmp/out",
    "async_mode": False              # sync: waits ~2-3 min for result
}
# For I2V (image-to-video): add "first_frame_image": "/path/to/img.jpg" and model="I2V-01-Director"
```

### text_to_image args — VERIFIED schema (2026-08-08)

`tools/list` confirmed live args as of 2026-08-08 — these are the inputs, not the doc-stated ones:

```python
{
    "prompt": "...",                 # required
    "model": "image-01",             # ONLY accepted value as of probe date
    "aspect_ratio": "1:1",           # ["1:1","16:9","4:3","3:2","2:3","3:4","9:16","21:9"]
    "n": 1,                          # 1-9 — set 4 to let the user pick best-of-N
    "prompt_optimizer": True,        # True/False — leave True for cleaner renders
    "output_directory": "/path/out"  # required
}
```

**Note on `prompt_optimizer`**: leave True (default). When False, the model renders prompts more literally, which can hurt the lean/mass bias workaround. Keep True unless the user wants pixel-exact prompt compliance.

### MCP tool-list probe pattern — don't skip the notification step

`tools/list` is the canonical way to discover what an MCP server exposes. Two gotchas (both hit 2026-08-08):

1. **Must send `notifications/initialized` after `initialize`.** Per the MCP spec, the client is supposed to notify the server it's ready before requesting capabilities. Without it, `tools/list` returns `{"Unknown tool": "tools/list"}` on some servers (saw this verbatim on MiniMax :18100). The helper:

```python
sid = init_mcp()
requests.post(MCP, headers={"Content-Type":"application/json","mcp-session-id":sid},
              json={"jsonrpc":"2.0","method":"notifications/initialized"})
# Now tools/list works
r = requests.post(MCP, headers={"Content-Type":"application/json",
                                "Accept":"application/json, text/event-stream",
                                "mcp-session-id":sid},
                  json={"jsonrpc":"2.0","method":"tools/list","id":2}, timeout=30)
for line in r.text.splitlines():
    if line.startswith("data: "):
        d = json.loads(line[6:])
        print(json.dumps(d, indent=2)[:4000])
        break
```

2. **List tools by extracting `name` + first description line first**, don't dump the full JSON — saves context when there are many tools:

```python
for t in d['result']['tools']:
    print(t['name'], '||', t['description'].split('\n')[0][:120])
```

3. **For a specific tool schema, filter then dump full**:

```python
for t in d['result']['tools']:
    if t['name'] == 'text_to_image':
        print(json.dumps(t, indent=2))
        break
```

### Known pitfall
`run_sse.py` hardcodes `mcp.settings.port = 18090` → conflicts with hermes bridges. Always use `run_v2.py` (port 18100). The systemd unit file points at the wrong entrypoint if someone forgets.

### Cost
- MiniMax Hailuo-02: ~$0.14-0.28 per 6s clip (billable per cloud API call)
- image-01 (MiniMax Image / wan2.7): ~$0.02 per image

### Model-name probe pattern (when in doubt)
The MCP doesn't expose `models/list`. If the doc-stated model name fails with `2013-invalid params, unsupported model`, probe in this order — DO NOT skip to the "real" one silently, log the failures so future agents can update this doc:

```python
for m in ["image-01", "wan2.7", "wan2.7-image", "wan2_7_image", "MiniMax-Image-01"]:
    ... call text_to_image with prompt="test" and m ...
```
Verified 2026-08-08: only `image-01` worked. The wan2.7 family returned `unsupported` from this MCP endpoint. When the working model name drifts again, repeat the probe and patch this doc — the underlying provider changes model strings faster than the doc gets reviewed.
