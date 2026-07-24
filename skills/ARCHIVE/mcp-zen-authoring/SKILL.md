---
id: mcp-zen-authoring
name: mcp-zen-authoring
version: 1.0.0-2026.07.03
description: Keep MCP servers minimal, schema-first, and governance-free
owner: F13 SOVEREIGN — Muhammad Arif bin Fazil (888)
risk_tier: medium
floor_scope: [F2, F4, F8, F11, F13]
autonomy_tier: T1
trigger_phrases:
  - "mcp-zen-authoring"
  - "build an MCP server"
  - "MCP zen"
dependencies:
  mcp_servers: []
  skills: []
inputs:
  - server_scope
  - tool_design
outputs:
  - minimal_server_guidance
  - anti_pattern_checklist
version_lock:
  schema_version: "1"
  artifact_hash: pending
---

# MCP Zen Authoring

> **Load this BEFORE building any MCP server.** Stops the coder paradox — the
> disease where coding agents grow 800-line midddleware stacks when the job
> asked for a 50-line tool.

## The Core Message

MCP is a pipe, not a brain.

```
Your MCP server = hands (does things)
arifOS kernel   = brain (governs things)   ← :8088
Agent (LLM)     = intent (decides what to do)
User             = sovereign (final veto)
```

If your server is *thinking*, *judging*, or *blocking* — you put the brain in
the wrong place. Stop. Strip it back.

## The 3 Rules

1. **Expose, don't govern.** Return data. Let arifOS judge via `arif_judge`.
   Don't build risk engines inside your MCP server.
2. **Schema = contract.** Declare input/output clearly. Trust the agent to
   read it. Don't add 5 validation layers.
3. **Dumb pipes, smart kernel.** Your server is a tool. arifOS :8088 is the
   brain. Don't make your server think.

## The Minimal FastMCP Server (copy-paste)

```python
from fastmcp import FastMCP
mcp = FastMCP("my-organ")

@mcp.tool()
def my_tool(query: str) -> dict:
    """Clear description of what this does."""
    # do the thing
    return {"result": "data here"}

mcp.run(transport="stdio")
```

That's it. That's the whole template. Resist the urge to add more.

## Anti-Patterns — DO NOT BUILD

| File you were about to write | Why you don't need it |
|---|---|
| `middleware_stack.py` (800 lines) | arifOS kernel handles request scoping |
| `auth_handler.py` | arifOS F11 AUTH handles identity |
| `risk_classifier.py` | `arif_judge_deliberate` does this |
| `retry_with_backoff.py` | Agent handles retries |
| `circuit_breaker.py` | Overkill for local MCP |
| `custom_error_handler.py` | Return clear errors, let agent read them |
| `api_gateway.py` | You ARE the tool, not a gateway |

*Wah, you want to write a gateway? For what, bro? The agent already speaks MCP.*

## The Zen Checklist

Before you call it done:

- Does it expose tools with clear schemas?
- Does each tool do **ONE** thing?
- Is the transport working (`stdio` or HTTP)?
- Are error messages readable by an agent?
- Is governance delegated to arifOS, not embedded here?
- Total lines under 500 for a simple organ?

If any answer is "no" — go back. Don't ship.

## When NOT to Flag Bloat (Forged 2026-07-08)

The zen rule (expose, don't govern) targets the **brain-in-MCP antipattern**. But
before flagging a file as bloat, do the four-step read:

```
1. Read the file fully.
2. Check server.py / __main__.py imports — is it actually wired into the live tool?
3. Identify what class of work it implements:
   - Auth middleware?         → load-bearing governance
   - Audit / logging?          → load-bearing F11 AUDIT
   - Tool registration glue?   → load-bearing F11 AUTH
   - Migration fossil / alias? → load-bearing for backward compat
   - Real computation?         → obviously load-bearing
4. If load-bearing governance → NOT bloat. Don't delete.
```

**Correct zen move for load-bearing governance:** delegate to arifOS kernel, not
delete. That's a T3 refactor requiring 888_HOLD per organ AGENTS.md (tool registry
changes are sovereign-gated).

**Real-world trap (GEOX 2026-07-08):** flagged `geox_middleware.py` (415 lines) +
`tools_wiring.py` (1638 lines) + `surface_migration.py` (293 lines) as bloat. Re-read
showed:
- `geox_middleware.py`: GeoxGovernanceMiddleware + GeoxToolListTtlMiddleware (live)
- `tools_wiring.py`: `register_tools_on` — core tool registration (live)
- `surface_migration.py`: migration audit receipt (test-only fossil record)

None were bloat. All were load-bearing or fossil records. The right move is
**delegate wiring/middleware to arifOS**, not delete. That's a separate refactor.

**Anti-pattern:** If you delete load-bearing governance thinking "it's middleware,
kill it," you crash the live organ on restart. The blast radius is the entire
federation surface. **Always read first, then judge.**

## Where the 4 Problems Get Solved

| Problem | Who fixes it | Your MCP server's role |
|---|---|---|
| Unclear instructions | User + MCP Prompts | Expose `prompts/` that standardize common requests |
| No verification loop | MCP Tools | Expose `run_tests()`, `check_build()`, `read_logs()` |
| No project memory | MCP Resources | Expose `resources://` pointing to docs, schema, conventions |
| No understanding | Not your problem | That's the model's ceiling, lah |

## Federation Naming

```
arif_*    = external MCP tools (human-facing, FastMCP-exposed)
arifos_*  = internal daemon tools (not MCP-exposed)

Organ prefix:
  geox_*     (GEOX organ — geoscience, :8081)
  wealth_*   (WEALTH organ — capital, :18082)
  well_*     (WELL organ — readiness, :18083)
  aforge_*   (A-FORGE organ — execution, :7071/7072)
  aaa_*      (AAA cockpit — observability, :3001)

Convention: {organ}_{action}_{resource}
Example:    geox_well_analyze_log
```

## When NOT to Use This Zen Path

This skill is for **simple MCP servers**. If you are adding a tool to:

- the **arifOS constitutional surface** (the 13-tool interface)
- a **VAULT999 sealing pipeline**
- a **federation bridge** (cross-organ routing)
- any tool where F11 AUTH + F12 INJECTION + F13 SOVEREIGN floors apply

→ Then load `arif-os-mcp-tool-authoring` instead. That surface has multi-layer
governance. This zen path is for everything else.

## Quick Decision Tree

```
Building an MCP server?
│
├─ Adding to arifOS constitutional surface (13-tool)?
│   └─ Load: arif-os-mcp-tool-authoring (heavy, multi-layer)
│
└─ Building a tool for a new organ / domain?
    └─ THIS skill — keep it under 500 lines, expose, don't govern.
```

*Simple like nasi lemak — one plate, got rice, sambal, egg, cucumber. Don't
add wagyu. The customer didn't ask for wagyu.*
