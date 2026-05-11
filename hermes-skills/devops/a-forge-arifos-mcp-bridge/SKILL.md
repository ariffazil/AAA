---
name: a-forge-arifos-mcp-bridge
description: Wire A-FORGE TypeScript to call arifOS MCP tools (especially arif_judge_deliberate) via FastMCP JSON-RPC 2.0 HTTP transport
triggers:
  - A-FORGE needs to call arifOS kernel for constitutional adjudication
  - arifOS MCP tool call from Node.js/TypeScript
  - FastMCP streamable-http transport from A-FORGE
---

# A-FORGE → arifOS MCP Bridge Pattern

## What I Learned (2026-05-03)

### FastMCP HTTP Transport Pattern

A-FORGE is Node.js/TypeScript. arifOS MCP runs on port 8080 (env `ARIFOS_PORT`). The correct transport is **FastMCP streamable-http** at `/mcp`.

**JSON-RPC 2.0 request envelope:**
```typescript
const response = await fetch(`${arifOSUrl}/mcp`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    jsonrpc: '2.0',
    method: 'tools/call',
    params: {
      name: 'arif_judge_deliberate',  // tool name
      arguments: {
        mode: 'judge',
        candidate: JSON.stringify({ goal: '...', ... }),
        session_id: sessionId,
      },
    },
    id: Math.floor(Math.random() * 999999),
  }),
});
```

**Parsing the response:**
FastMCP returns `{ content: [{ type: 'text', text: '...' }] }` where `text` is itself a JSON string containing the actual result.

```typescript
const rpcResult = await response.json() as { result?: Record<string, unknown>; error?: {...} };
if (rpcResult.error) throw new Error(`arifOS MCP error: ${rpcResult.error.message}`);
const content = (rpcResult.result?.content as Array<{ type: string; text: string }>) ?? [];
const rawText = content[0]?.text ?? '';
const parsed = JSON.parse(rawText);
const verdictText = parsed.verdict ?? parsed.status ?? rawText;
```

### Verdict Mapping for `arif_judge_deliberate`

| arifOS verdict | SealStatus |
|----------------|-----------|
| SEAL, PASS | PASS |
| HOLD, 888_HOLD | HOLD |
| SABAR | SABAR |
| VOID | VOID |
| PARTIAL | HOLD |

### Graceful Degradation

When arifOS MCP is unreachable:
- `fallbackOnFailure: false` → return `HOLD` verdict, block the operation
- `fallbackOnFailure: true` (default) → use local PlanValidator as heuristic; `VOID` on structural failure, `HOLD` on structurally-valid

### Constructor Backward Compatibility

Existing SealService constructor was `(validator, thresholds?)`. New signature `(validator, optionsOrThresholds?)`. Use duck-typing:

```typescript
if (thresholdsOrOptions && 'arifOSUrl' in thresholdsOrOptions) {
  // New: options object
  this.arifOSUrl = opts.arifOSUrl ?? 'http://localhost:8080/mcp';
  this.timeoutMs = opts.timeoutMs ?? 10000;
  this.fallbackOnFailure = opts.fallbackOnFailure ?? true;
} else {
  // Old: thresholds or nothing
  this.arifOSUrl = 'http://localhost:8080/mcp';
  this.timeoutMs = 10000;
  this.fallbackOnFailure = true;
}
```

### Python Import Pattern

In `arifosmcp/runtime/` modules, use dual-import for `llm_client`:

```python
try:
    from arifosmcp.runtime.llm_client import LLMUnavailableError, call_llm
except ImportError:
    from .llm_client import LLMUnavailableError, call_llm  # type: ignore[assignment]
```

Handles both `python -m arifosmcp.runtime.X` (absolute) and direct execution (relative).

## Files to Reference

- `arif_judge_deliberate` signature: `/root/arifOS/arifosmcp/runtime/tools.py:4914`
- FastMCP HTTP transport: `/root/arifOS/arifosmcp/transport/http.py`
- Existing HTTP→arifOS pattern: `/root/A-FORGE/src/governance/GovernanceBridge.ts`
- arifOS port: `8080` (env `ARIFOS_PORT`)

## Env Vars

- `ARIFOS_MCP_URL=http://localhost:8080/mcp` (A-FORGE convention)
- On VPS Docker: `http://arifosmcp:8080/mcp`

## Gotchas

1. **`tsc` not found** — A-FORGE needs `npm install` first; use `npx tsc` from package scripts
2. **JSON-RPC id** — must be number or string; `Math.random()` works for one-shot calls
3. **FastMCP result is nested JSON string** — `text` field is itself JSON that must be parsed again
4. **Hermes + TypeScript** — defer TS errors to Claude Code; don't try to muscle through tsconfig errors
