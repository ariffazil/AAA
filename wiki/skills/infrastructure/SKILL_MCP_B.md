---
title: "SKILL: MCP Server Builder"
type: skill
version: 1.0.0
category: engineering
risk_band: MEDIUM
floors: []
evidence_required: false
sources: [/root/.opencode/skills/mcp-builder/SKILL.md]
confidence: high
---

# SKILL: MCP Server Builder

> **DITEMPA BUKAN DIBERI — Build, ship, evaluate any MCP server.**
> **Source:** `/root/.opencode/skills/mcp-builder/SKILL.md`
> **Agent:** OpenCode (Ω-FORGE)
> **Forged:** 2026-05-17

---

## Trigger Conditions

- Building a new MCP server from scratch
- Adding tools to existing MCP server
- Choosing between Python (FastMCP) or TypeScript (MCP SDK)
- Designing tool schemas and naming conventions
- Setting up testing and evaluation
- Keywords: MCP server, FastMCP, MCP SDK, tools

---

## The 4-Phase Workflow

| Phase | Focus | Key Output |
|-------|-------|-----------|
| **🔍 Phase 1 — Research** | API docs, tool selection, schema design | Implementation plan |
| **⚙️ Phase 2 — Build** | Code, tests, quality gates | Working server |
| **🔍 Phase 3 — Review** | Security, composability, error handling | Quality pass |
| **📋 Phase 4 — Evaluate** | Real LLM usage testing | 10-question eval suite |

---

## Transport Options

| Transport | Best For | Command |
|-----------|----------|---------|
| streamable-http | Remote servers, multi-client | `mcp.run(transport="streamable_http", port=8000)` |
| stdio | Local clients, CLI tools | `mcp.run()` |
| SSE | Real-time streaming | Legacy; prefer HTTP |

---

## Tool Naming Convention

```
{service}_{action}_{resource}
Example: github_create_issue, slack_send_message, geox_lithos_interpret
```

---

## Server Naming

| Language | Format | Example |
|----------|--------|---------|
| Python | `{service}_mcp` | `geox_mcp` |
| TypeScript | `{service}-mcp-server` | `geox-mcp-server` |

---

## Python (FastMCP 3.x) Pattern

```python
from fastmcp import FastMCP, Context
from pydantic import BaseModel, Field
from typing import Annotated

mcp = FastMCP("service_mcp", strict_input_validation=True)

@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def search_items(query: Annotated[str, Field(description="Search query")], ctx: Context) -> str:
    """Search for items matching the query."""
    await ctx.info(f"Searching: {query}")
    results = []
    return json.dumps(results)
```

---

## TypeScript (MCP SDK) Pattern

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({ name: "service-mcp-server", version: "1.0.0" });

server.registerTool("service_search", {
  title: "Search Items",
  description: "Search for items...",
  inputSchema: z.object({ query: z.string().min(2) }),
  annotations: { readOnlyHint: true, openWorldHint: true }
}, async (params) => {
  return { content: [{ type: "text", text: JSON.stringify(results) }] };
});
```

---

## Quality Checklist

- [ ] Tool names follow `{service}_{action}_{resource}` pattern
- [ ] Response formats support JSON and Markdown
- [ ] Pagination: `has_more`, `next_offset`, `total_count`
- [ ] Character limit enforced (25,000 default)
- [ ] Error messages are actionable
- [ ] Annotations correctly set (readOnlyHint, destructiveHint)
- [ ] All inputs validated with Pydantic (Python) or Zod (TS)
- [ ] Async/await for all I/O operations
- [ ] Tests pass

---

## Code Quality Gates

| Gate | Python | TypeScript |
|------|--------|------------|
| Lint | `ruff check .` | `npm run build` |
| Format | `ruff format .` | `npm run build` |
| Type-check | `mypy .` | `tsc --noEmit` |
| Test | `pytest tests/ -q` | `npm test` |

---

## arifOS Constitutional Overlay

| Floor | Tool Stage | Requirement |
|-------|-----------|-------------|
| F01 AMANAH | 999_VAULT | No irreversible writes without ack |
| F02 TRUTH | 222_FETCH | Ground claims in evidence |
| F09 ANTIHANTU | Any | Refuse manipulation claims |
| F11 AUTH | 888_JUDGE | Verify identity before sensitive ops |
| F12 INJECTION | Any | Sanitize all inputs |
| F13 SOVEREIGN | Any | Human veto is absolute |

---

## Related Pages

- [[skill-fastmcp-deploy]] — FastMCP deployment
- [[skill-staff-engineer-review]] — code review
- [[concept-tools-and-embodiment]] — tools as primitives
- [[SCHEMA.md]] — TREE777 governance schema

---

*DITEMPA BUKAN DIBERI — MCP built. Quality verified.*
