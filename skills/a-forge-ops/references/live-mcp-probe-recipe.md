# Live MCP Probe Recipe for A-FORGE

## Why bare curl doesn't work

A-FORGE MCP (`:7072`) uses `streamable-http` transport. A bare `curl -X POST /mcp` returns empty
because the response is SSE (Server-Sent Events), not plain JSON. You need the official MCP SDK client
to talk to it, or accept `text/event-stream` content type.

## MCP SDK probe (recommended)

```javascript
// /tmp/aforge-mcp-probe.mjs
import { Client } from "/root/A-FORGE/node_modules/@modelcontextprotocol/sdk/dist/esm/client/index.js";
import { StreamableHTTPClientTransport } from "/root/A-FORGE/node_modules/@modelcontextprotocol/sdk/dist/esm/client/streamableHttp.js";

const client = new Client({ name: "aforge-probe", version: "1.0" });
const transport = new StreamableHTTPClientTransport(new URL("http://127.0.0.1:7072/mcp"));
await client.connect(transport);

// Test: egress_profile=mubeng → BLOCKED
const r = await client.callTool({ name: "forge_fetch", arguments: {
  url: "https://example.com",
  mode: "text",
  max_chars: 200,
  cache_ttl_seconds: 0,
  scan_injection: false,
  egress_profile: "mubeng"
}});
const body = JSON.parse(r.content[0].text);
// Expected: { status: "ERROR", data: { status: "BLOCKED", reason: "egress profile 'mubeng' not yet configured..." } }
console.log("mubeng:", body.data.status, body.data.reason?.slice(0, 80));

// Test: default profile → works (byte-identical to pre-forge)
const r2 = await client.callTool({ name: "forge_fetch", arguments: {
  url: "https://example.com",
  mode: "text",
  max_chars: 200,
  cache_ttl_seconds: 0,
  scan_injection: false
}});
const body2 = JSON.parse(r2.content[0].text);
// Expected: { status: "SEAL", data: { egress: { profile: "default", provider: "direct", ... } } }
console.log("default:", body2.status, "egress=", JSON.stringify(body2.data?.egress));

await client.close();
```

Run with: `node /tmp/aforge-mcp-probe.mjs 2>&1`

## Deployment-health verification protocol

```bash
# Step 1: Confirm deployed commit (canonical truth: :7071)
curl -sf --max-time 8 http://127.0.0.1:7071/health | \
  python3 -c "import sys,json; d=json.load(sys.stdin); \
    print('deployed:', d.get('deployed_commit'), \
          'source:', d.get('source_commit'), \
          'drift:', d.get('deployment_drift'), \
          'tools:', d.get('tool_count'))"

# Step 2: Confirm runtime binary exists
ls -la /opt/a-forge/app/dist/src/infrastructure/egress/EgressPolicy.js

# Step 3: Live MCP roundtrip (SDK probe — definitive)
node /tmp/aforge-mcp-probe.mjs
```

The three steps are independent — run in parallel. Step 1 confirms rsync + restart.
Step 2 confirms the new file exists at the expected runtime path. Step 3 confirms
the new behavior is actually wired and serving.
