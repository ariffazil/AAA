---
name: a-forge-tool-wiring
description: Add a tool to all A-FORGE entry points (CLI, MCP forge, MCP direct) — requires 3 simultaneous registrations. Created during MiniMax MCP integration 2026-04-30.
category: devops
tags: [a-forge, typescript, mcp, tool-registry]
---

# A-FORGE Tool Wiring — Adding Tools to All Entry Points

> Adding a tool to A-FORGE requires wiring in THREE places.
> Missing one = tool works in CLI but not MCP, or not in forge handler, etc.
> Discovered 2026-04-30 during MiniMax tools integration.

## Trigger

When adding a tool (MCP client wrapper, truth-lane delegate, native tool) to A-FORGE.

## Three Registration Points

### 1. `src/cli.ts` — `buildToolRegistry()` (CLI entry)
```typescript
import { MyNewTool } from "./tools/MyNewTool.js";
// ...
registry.register(new MyNewTool());
```
Use for: CLI `explore` command, direct `node dist/src/cli.js` runs.

### 2. `src/mcp/core.ts` — forge handler inline registry (MCP forge execution)
```typescript
import { MyNewTool } from "../tools/MyNewTool.js";
// inside forgeHandler:
registry.register(new MyNewTool());
```
Use for: `arif_forge_execute`, `forge_run` MCP calls that spin up AgentEngine.

### 3. `src/mcp/core.ts` — `server.tool()` (direct MCP exposure)
```typescript
server.tool(
  "my_new_tool",
  "Description for external MCP clients.",
  { arg1: z.string(), arg2: z.string().optional().default("") },
  async ({ arg1, arg2 }) => {
    try {
      const output = await getMyToolClient().call(arg1, arg2);
      return { content: [{ type: "text" as const, text: output }] };
    } catch (err) {
      return { content: [{ type: "text" as const, text: `ERROR: ${err instanceof Error ? err.message : String(err)}` }], isError: true };
    }
  }
);
```
Use for: external MCP clients calling A-FORGE MCP server directly.

## MCP Subprocess Client Pattern

For tools that run as a stdio MCP subprocess (like MiniMax):

```typescript
// src/tools/MyMcpClient.ts
import { spawn } from "node:child_process";

export class MyMcpClient {
  private proc: ReturnType<typeof spawn> | null = null;
  private requestId = 0;

  private async init(): Promise<void> { /* spawn, initialize handshake */ }
  private async call(method: string, params: Record<string, unknown>): Promise<unknown> {
    if (!this.proc) await this.init();
    const id = ++this.requestId;
    this.proc!.stdin!.write(JSON.stringify({ jsonrpc: "2.0", id, method, params }) + "\n");
    // ... read response, handle timeout
  }

  async myMethod(arg: string): Promise<string> {
    const result = await this.call("tools/call", { name: "my_method", arguments: { arg } }) as any;
    return result?.content?.[0]?.text ?? "";
  }

  close(): void { this.proc?.kill(); }
}

let _client: MyMcpClient | null = null;
export function getMyClient(): MyMcpClient {
  if (!_client) _client = new MyMcpClient();
  return _client;
}
```

## Pre-existing TS Build Noise

A-FORGE has pre-existing TypeScript lint errors from `zod` esModuleInterop and `Map`/`Set` iteration that do NOT block the actual `npm run build` compilation. These are lint-only warnings from `node_modules/`, not from A-FORGE source code. The build (`tsc -p tsconfig.json`) succeeds with exit code 0 even when these lint errors appear.

## Verification

```bash
cd /root/A-FORGE
npm run build    # must exit 0
npm test         # all tests pass
```

## Files Created (example: MiniMax)

- `src/tools/MiniMaxMcpClient.ts` — subprocess stdio bridge
- `src/tools/MiniMaxTools.ts` — `BaseTool` subclasses
