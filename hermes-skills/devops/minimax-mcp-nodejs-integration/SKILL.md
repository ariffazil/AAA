---
name: minimax-mcp-nodejs-integration
description: Wire MiniMax MCP subprocess (minimax-coding-plan-mcp) into a Node.js TypeScript project — spawn once, keep alive, line-buffer async JSON-RPC.
tags: [minimax, mcp, nodejs, stdio, typescript]
last_updated: 2026-05-07
---

# MiniMax MCP Node.js Integration

## Critical Discovery (2026-05-07) — API Key Formats & Endpoints

MiniMax has **two distinct API key formats** that determine which endpoint to use:

| Key Prefix | Endpoint | Status Code on Failure | Verified |
|------------|----------|----------------------|----------|
| `sk-cp-...` (cookie-based) | `https://api.minimax.io` | 2049 = invalid key | ✅ 2026-05-07 empirically confirmed |
| `sk-api-...` (token-based) | `https://api.minimax.io` | 2049 = invalid key, 1008 = valid but 0 credits | — |

### Testing Pattern (Verified 2026-05-07)
```bash
# sk-cp-... keys work with api.minimax.io (NOT api.minimaxi.com)
curl -s -X POST https://api.minimax.io/v1/text/chatcompletion_v2 \
  -H "Authorization: Bearer sk-cp-BJtUy..." \
  -H "Content-Type: application/json" \
  -d '{"model":"MiniMax-M2.7","messages":[{"role":"user","content":"hi"}],"max_tokens":5}'

# sk-api-... keys also use api.minimax.io
curl -s -X POST https://api.minimax.io/v1/text/chatcompletion_v2 \
  -H "Authorization: Bearer sk-api-BbfN..." \
  -H "Content-Type: application/json" \
  -d '{"model":"MiniMax-M2.7","messages":[{"role":"user","content":"hi"}],"max_tokens":5}'
```

### Error Codes
- **2049**: `invalid api key` — key is revoked/rotated or format wrong
- **1008**: `insufficient balance` — key is valid but account has 0 credits
- **200**: Success

### In openclaw.json
- All current keys (`sk-cp-...` and `sk-api-...`) → `MINIMAX_API_HOST: https://api.minimax.io`
- **Note:** Earlier documentation suggested `sk-cp-...` required `api.minimaxi.com`; empirical testing on 2026-05-07 disproved this.

### In /etc/environment or systemd env
- `MINIMAX_API_KEY=sk-cp-...` + `MINIMAX_API_HOST=https://api.minimax.io`

---

## Previous content below — MCP Node.js integration

## Context
MiniMax MCP (`minimax-coding-plan-mcp --transport stdio`) provides `web_search` and `understand_image` tools.
arifOS A-FORGE (Node.js/TypeScript) needs to invoke these as both MCP server tools and ToolRegistry tools.

## Key Discovery
**Re-spawning the subprocess after init causes hangs.** The correct pattern: spawn once, keep alive, use async line-buffer with pending request map.

## Implementation Pattern

### MiniMaxMcpClient.ts (correct pattern)
```typescript
import { spawn } from "node:child_process";

export class MiniMaxMcpClient {
  private proc: ReturnType<typeof spawn> | null = null;
  private requestId = 0;
  private pending = new Map<number, { resolve: (v: unknown) => void; reject: (e: unknown) => void }>();
  private ready = false;
  private buf = "";

  private async init(): Promise<void> {
    if (this.ready) return;
    const apiKey = process.env.MINIMAX_API_KEY;
    if (!apiKey) throw new Error("MINIMAX_API_KEY not set");

    this.proc = spawn("minimax-coding-plan-mcp", ["--transport", "stdio"], {
      env: { ...process.env, MINIMAX_API_KEY: apiKey },
      stdio: ["pipe", "pipe", "pipe"],
    });

    const stdin = this.proc.stdin!;
    const stdout = this.proc.stdout!;

    // Line-buffered async response handler — key insight
    stdout.on("data", (chunk: Buffer) => {
      this.buf += chunk.toString();
      const lines = this.buf.split("\n");
      this.buf = lines.pop() || "";
      for (const line of lines) {
        if (!line.trim()) continue;
        try {
          const resp = JSON.parse(line);
          const p = this.pending.get(resp.id);
          if (p) { this.pending.delete(resp.id); resp.error ? p.reject(...) : p.resolve(resp.result); }
        } catch {}
      }
    });

    // Initialize — wait for response via pending map
    const initId = ++this.requestId;
    await new Promise((resolve, reject) => {
      this.pending.set(initId, { resolve, reject });
      stdin.write(JSON.stringify({ jsonrpc: "2.0", id: initId, method: "initialize", params: { protocolVersion: "2024-11-05", capabilities: {}, clientInfo: { name: "A-FORGE", version: "2026.04.30" } } }) + "\n");
      setTimeout(() => reject(new Error("init timeout")), 10000);
    });

    stdin.write(JSON.stringify({ jsonrpc: "2.0", method: "notifications/initialized", params: {} }) + "\n");
    this.ready = true;
  }

  async webSearch(query: string): Promise<string> {
    await this.init();
    const id = ++this.requestId;
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve: (result) => { /* parse result */ }, reject });
      this.proc!.stdin!.write(JSON.stringify({ jsonrpc: "2.0", id, method: "tools/call", params: { name: "web_search", arguments: { query } } }) + "\n");
      setTimeout(() => { if (this.pending.has(id)) { this.pending.delete(id); reject(new Error("timeout")); } }, 60000);
    });
  }
}
```

### What NOT to do
- Do NOT re-spawn the process after init — causes orphan response consumption and hangs
- Do NOT use synchronous read loop — blocks the event loop
- Do NOT call `recvRaw()` after already consuming init response lines

## File Locations (arifOS A-FORGE)
- Client: `/root/A-FORGE/src/tools/MiniMaxMcpClient.ts`
- Tools: `/root/A-FORGE/src/tools/MiniMaxTools.ts`
- Wire-in: `/root/A-FORGE/src/mcp/core.ts` (MCP tools + forge handler registry)
- Wire-in: `/root/A-FORGE/src/cli.ts` (ToolRegistry)

## Tool Names (MCP namespace)
- `minimax_web_search` — web grounding for Stage 111 SENSE
- `minimax_understand_image` — image analysis for Stage 111 SENSE

## Verification
```bash
# Direct subprocess test
MINIMAX_API_KEY=$MINIMAX_API_KEY minimax-coding-plan-mcp --transport stdio <<'EOF'
{"jsonrpc":"2.0","id":0,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}
{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}
{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"web_search","arguments":{"query":"arifOS AI"}}}
EOF

# Via A-FORGE MCP server (build first)
cd /root/A-FORGE && npm run build
```
