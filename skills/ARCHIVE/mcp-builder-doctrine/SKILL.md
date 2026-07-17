---
id: mcp-builder-doctrine
name: mcp-builder-doctrine
version: 1.1.0-2026.07.10
description: Canonical MCP server-builder doctrine — naming laws, capability declaration discipline, _meta envelope contract, lifecycle notification rules, error envelope contract, and the 28 bindings every MCP server in arifOS federation must honour. Load before designing, scaffolding, or auditing ANY MCP server surface.
risk_tier: medium
floor_scope: [F1, F2, F3, F4, F7, F9, F11, F13]
autonomy_tier: T1
trigger_phrases:
  - "build an MCP server"
  - "register a tool/resource/prompt"
  - "audit MCP capabilities"
  - "fix MCP surface"
  - "naming for MCP"
  - "add a tool"
  - "add a resource"
  - "add a prompt"
owner: F13 SOVEREIGN — Muhammad Arif bin Fazil (888)
hermes:
  inject_as: skill
  priority: 100
---

# MCP Builder Doctrine

> **The LLM discovers and invokes tools/resources/prompts via the model + the host.**
> Your server's `name` and `description` fields are not documentation. **They are the interface contract to agentic intelligence.** Bad naming causes silent misfires — the model picks the wrong tool, fills wrong arguments, skips a tool entirely. No error is thrown. The system just produces wrong outputs.

**DITEMPA BUKAN DIBERI — Naming is the first act of creation.**

---

## 0. The Three Primitives — Who Decides What

| Primitive | Decided by | Surfaced via | GEOX example |
|---|---|---|---|
| **Tools** | Model (LLM) | `tools/call` | `geox_basin(mode='macrostrat')` |
| **Resources** | Host (Cursor/app) | `resources/read` after host injects | `geox://literature/sabah/madon-2021` |
| **Prompts** | User | `/slash_name` | `/analyse-well-log` |

**Critical split:** Resources are **application-driven** — server exposes, host decides context inclusion, server only hints via `annotations`. **DO NOT** rely on resources being model-callable. Use TOOLS for that.

---

## 1. Naming Laws — The Five Constraints

| # | Law | Consequence of violation |
|---|---|---|
| 1 | `name` is a **machine contract** — never rename after publish | every agent, cached plan, every reference breaks |
| 2 | `description` is the **model's only briefing** | vague = misfire, hallucinated args, tool skipped silently. Must be 50-300 chars. Must include "Use when..." sentence. |
| 3 | `title` and `name` must **diverge deliberately** | human readable + machine stable |
| 4 | Argument names are **semantic, not syntactic** | `latitude: float, longitude: float` — never `p1, p2` |
| 5 | Prompt names are **user vocabulary** | `/analyse-well-log` matches how a geologist thinks |

```json
{
  "name":  "query_macrostrat_columns",          // machine, snake_case, stable
  "title": "Macrostrat Geological Columns",        // human, readable, can change
  "description": "Query Macrostrat for columnar stratigraphy at lat/lon — returns columns JSON with units, lithology, age. Use when the user asks about stratigraphic columns at a location."
}
```

---

## 2. Every Field, Every Primitive — What It Does to the Model

### Tools

| Field | Role in agentic intelligence |
|---|---|
| `name` | Unique identifier — the model calls this exactly |
| `title` | Human display only — model ignores |
| `description` | **The model's decision surface** — it reads this to decide whether + how to call |
| `inputSchema.properties` | Per-parameter intent — model fills arguments from description |

### Resources

| Field | Role |
|---|---|
| `name` | Machine identifier — used in URI resolution |
| `title` | Host UI display |
| `description` | Host uses this to **decide whether to inject into context** |
| `uri` | The address — must be unambiguous, no collisions |
| `annotations.audience` | `["assistant"]` for papers; `["user"]` for index/README |
| `annotations.priority` | 0.7-0.9 papers, 1.0 LAS, 0.5 index |
| `annotations.lastModified` | ISO 8601 — clients sort by recency |
| `mimeType` | `text/plain` preferred for agents; `application/pdf` only for small blobs |
| `size` | Include byte count — clients budget context |

### Prompts

| Field | Role |
|---|---|
| `name` | Unique identifier — user types `/this-exact-name` |
| `title` | Slash command menu label |
| `description` | Tells user what the prompt does before trigger |
| `arguments[].description` | Drives autocomplete via completion API |

---

## 3. Capability Declaration — Declare or It Doesn't Exist

`/mcp initialize` response declares everything the client may use:

```json
{
  "capabilities": {
    "tools":        { "listChanged": true },
    "resources":    { "subscribe": false, "listChanged": true },
    "prompts":      { "listChanged": true },
    "logging":      {},
    "completions":  {}
  }
}
```

**Hard rules:**
- If you don't implement `subscribe`, **omit it** — don't declare `false` and silently fail.
- If you don't implement `completions`, declare `{}` to signal API presence — clients may try.
- **Only fire notifications for successfully-negotiated capabilities.**

---

## 4. Tool Errors — Two Channels

| Error type | Mechanism | When to use |
|---|---|---|
| Protocol error | JSON-RPC `error` field | unknown tool, invalid args, server crash |
| Execution error | `isError: true` in result | API timeout, bad response, business logic |

Live API failures (`isError: true`) NEVER throw protocol errors. The Macrostrat tool returns `isError: true` for API down — not JSON-RPC error.

---

## 5. External Live APIs ⇒ Tools, Not Resources

| Decision | Use |
|---|---|
| Live API call (Macrostrat, USGS, etc.) | **Tool** with strict `inputSchema` |
| Cached snapshot of API response | Resource, mimeType `application/json` |
| Schema/citation metadata only | Resource (index) |
| Tool returns URIs + content | Tool result with embedded `type: "resource"` |

Hybrid pattern: tool returns `content: [{type: "resource", resource: {uri, ...}}]` to bridge cache + freshness.

---

## 6. `_meta` Envelope — Shape A (per MCP 2025-11-25)

The `_meta` extension lives on **the contents object**, not the response envelope. Carries seal_id, evidence_class, authority, sha256 — survives client-side caching.

```json
{
  "contents": [{
    "uri": "geox://literature/sabah/madon-2021",
    "mimeType": "text/markdown",
    "text": "...",
    "_meta": {
      "seal_id": "VAULT999-2026-0731-A7",
      "evidence_class": "DERIVED",
      "authority": "EVIDENCE",
      "sha256": "c01031...",
      "contract_version": "geox.resource.v2"
    }
  }]
}
```

`audit_class` enum (F2 TRUTH): `OBSERVED` / `DERIVED` / `INTERPRETED` / `SPECULATED`.

---

## 7. Templates — URI Shapes Only, No `supportsList`

Templates are pure URI shapes for `resources/read`. Discovery = `resources/list` (with cursor pagination). Completion = `completion/complete` for `{param}` enum.

```yaml
# Templates are URI SHAPES:
geox://literature/{basin}/{paper_id}             # shape for read
geox://wells/{basin}/{well_id}/logs             # shape for read

# Discovery always via:
resources/list    → cursor-paginated list
resources/templates/list → paginated list of shapes

# Completion for parameter hints:
completion/complete {ref: "geox://literature/{basin}", argument: {name: "basin"}}
  → returns ["sabah", "malay-basin", "sarawak", ...]   (cap 100)
```

---

## 8. Lifecycle Notifications — Coarse Only

```
New tool       → notifications/tools/list_changed      (no payload)
New resource   → notifications/resources/list_changed (no payload)
New prompt     → notifications/prompts/list_changed    (no payload)
Resource update → notifications/resources/updated { uri }   (per-URI; only if subscribe: true)
```

**Discipline:** Never fire for undeclared capabilities. Client MUST send `notifications/initialized` before server sends anything except pings/logs. Timeouts on every request — use cancellation notifications; never hang.

---

## 9. Annotations — Tuned Per Resource Type

| Type | audience | priority |
|---|---|---|
| Published papers | `["assistant"]` | 0.7–0.9 |
| LAS well data | `["assistant"]` | 1.0 |
| README/index | `["user"]` | 0.5 |
| Internal analyses | `["user","assistant"]` | 0.8 |
| Operator-private wells (F13) | `["assistant"]` | 0.95 |

Always include `lastModified` for recency sort.

---

## 10. Transport — What Lives Where

| Surface | Mechanism | Authority |
|---|---|---|
| Client fetches directly | `https://` URI allowed | Client + server both see bytes |
| Server proxies | `geox://` (custom scheme) + URL field | Server-stamped sha256 |
| File-backed (real or virtual) | `file://` (no real FS required per spec) | Per organ |
| Version control | `git://` built-in | For VCS integration |

For paywalled/internal papers: NEVER fake `https://` you'll proxy. Use `geox://` + server-side sha256.

---

## 11. Cursors — Opaque, Session-Scoped, Server-Controlled

```python
cursor = base64url(json.dumps({
  "p": page_idx,      # 0-indexed
  "f": filter_hash,   # sha256 of filter args
  "s": page_size,
  "v": 1              # version
}))
```

Clients MUST NOT persist cursors across sessions. Server chooses page size dynamically under load; clients handle silently.

---

## 12. Error Code — Echo the URI

```json
{ "code": -32002, "message": "Resource not found", "data": { "uri": "geox://..." } }
```

JSON-RPC codes for MCP:
- `-32002` not found
- `-32003` forbidden (F13 gate)
- `-32602` invalid params
- `-32603` internal
- `-32601` method not found

---

## 13. The 28 Bindings (Authoritative List)

1. Resources = application-driven (host decides), Tools = model-driven (LLM decides), Prompts = user-driven
2. `name` is machine contract — never change after publish
3. `description` is model's only briefing — vague = silent misfire. Must be 50-300 chars, include "Use when..." sentence
4. `title` and `name` must diverge deliberately
5. Argument names semantic, not syntactic
6. Prompt names in user vocabulary
7. Capabilities declared or they don't exist (`/mcp initialize`)
8. `subscribe: false` declared ONLY if not implemented; omit otherwise
9. Only fire notifications for successfully-negotiated capabilities
10. Tool errors: `isError: true` for execution vs JSON-RPC `error` for protocol
11. External live APIs ⇒ Tools, not Resources
12. `_meta` Shape A on contents object (not envelope)
13. Templates are URI shapes only, no `supportsList`
14. Annotations: audience/priority/lastModified per resource type
15. Coarse `list_changed` notifications have no payload
16. `resources/updated` per-URI fires only if `subscribe: true` negotiated
17. Cursors opaque + session-scoped + server-controlled page size
18. `https://` only when client fetches directly — never fake for proxy
19. `file://` no real FS required
20. `git://` built-in for VCS integration
21. Error data echoes the URI (code -32002 + `data: {uri}`)
22. Bundle returns (multi-contents) when context needs multiple pieces

### Session-Learned Bindings (Forged 2026-07-10)

23. **Prompts returning `messages[]` can embed `type: "resource"` content blocks** — pre-loads context before model reasoning (MCP 2025-06-18 spec)
24. **Prompt arguments inferred from function signature** — FastMCP auto-generates `PromptArgument[]`; no-default = required, has-default = optional
25. **Docstring `Args:` section becomes argument `description`** — drives completion API autocomplete
26. **Workflow prompts MUST embed resources** — model starts cold without data; embedding LAS/papers/basin profiles into prompt messages gives context before first tool call

### Hardening Bindings (Forged 2026-07-10 — FreeCodeCamp contrast)

27. **Error Envelope Contract** — every tool MUST return structured errors, never raw tracebacks. Minimum shape:
    ```json
    {
      "error_code": "EXTERNAL_API_TIMEOUT",
      "message": "Macrostrat API did not respond within 5s",
      "retry_allowed": true,
      "suggested_action": "Retry with shorter timeout or check Macrostrat status page"
    }
    ```
    Rules:
    - `error_code` = UPPER_SNAKE_CASE, domain-prefixed (e.g., `GEOX_*`, `WEALTH_*`, `FORGE_*`)
    - `message` = human-readable, one sentence, no stack traces
    - `retry_allowed` = boolean — model uses this to decide whether to retry
    - `suggested_action` = what the model should tell the user OR try next
    - `isError: true` in MCP result envelope (per binding 10) wraps this payload
    - Protocol errors (unknown tool, invalid args) still use JSON-RPC `error` field (binding 10)

28. **External MCP Ingress** — connecting to third-party MCP servers (e.g., DeepWiki, public MCP endpoints) MUST go through an ingress boundary:
    - SSRF guard: validate URL against `forge_fetch` SSRF rules (no internal IPs, no metadata endpoints)
    - F12 injection: sanitize tool descriptions from external servers before LLM sees them (external ≠ authority)
    - Trust boundary: external tools start at UNTRUSTED state (per CONSTITUTIONAL_REFLEX §1 tool states)
    - Schema pin: fingerprint external tool schemas on first connect; alert on drift
    - Auth: never forward federation session tokens to external servers
    - Rate limit: cap external tool calls per session (default: 20/turn)
    - Audit: log all external tool invocations to `forge_work/` receipt

---

## 14. Self-Audit Checklist (Use Before Any MCP Surface Change)

```
□ name field present + snake_case + stable across versions?
□ description field rich enough to brief an LLM in isolation? (50-300 chars, includes "Use when..." sentence)
□ title distinct from name (human ≠ machine)?
□ inputSchema properties each described (intent, not just type)?
□ capability declared in /mcp initialize response?
□ subscribe omitted if not implemented (NOT false)?
□ external live API — using TOOL not RESOURCE?
□ _meta lives on contents object (not envelope)?
□ template is URI shape only (no supportsList)?
□ annotations cover audience + priority + lastModified?
□ error codes include data.uri (per JSON-RPC convention)?
□ tool execution errors use structured envelope (error_code, message, retry_allowed, suggested_action)?
□ external MCP connections go through ingress boundary (SSRF + F12 + trust state)?
□ ISO 8601 timestamps (lastModified, read_at_iso, etc.)?
□ F2 evidence label (OBS/DERIVED/INT/SPEC) in every output?
□ F11 audit trail maintained (read ledger append, sha256, actor)?
□ F13 sensitive resource requires actor_signature?
□ cursor opaque + non-traversable + session-scoped?
```

---

## 15. F1-F13 Compliance Checklist

| Floor | MCP binding |
|---|---|
| F1 AMANAH | reversible-first; backups before edits; irrefutable ops explicit |
| F2 TRUTH | evidence labels in `_meta`; capability declaration honest |
| F3 WITNESS | tri-witness on SEAL-grade claims; `_meta.actor_signature` slot |
| F4 CLARITY | single-URI-namespace; templates fixed param order |
| F5 PEACE² | de-escalate in `description`; never weaponize "must" |
| F6 MARUAH | `pii_redacted` field; dignity in error messages; error envelope never exposes internals |
| F7 HUMILITY | confidence cap 0.90 on claims; declare unknowns in `description` |
| F8 GENIUS | simplest correct path: `description` first, code second |
| F9 ANTI-HANTU | no soul claims; bundled cross-checks; tier caps on blobs |
| F10 ONTOLOGY | categorical scope: AI-only, substrate ≠ being |
| F11 AUDIT | every read appended to ledger; sha256 verified |
| F12 INJECTION | sanitize inputs; external ≠ authority |
| F13 SOVEREIGN | operator-private resources gated by `actor_signature` |

---

## 16. FastMCP / Real-World Pattern

```python
from fastmcp import FastMCP
from mcp.types import EmbeddedResource, TextResourceContents
from fastmcp.prompts.base import Message
from pydantic import AnyUrl

mcp = FastMCP("organ-name", version="v2026.07.x")

# Tool
@mcp.tool(name="query_macrostrat_columns",
          annotations={"readOnlyHint": True, "openWorldHint": True})
async def query_macrostrat_columns(latitude: float, longitude: float) -> str:
    """Query Macrostrat for columnar stratigraphy at lat/lon — returns columns JSON ..."""
    ...

# Resource
@mcp.resource("geox://literature/{basin}/{paper_id}",
              name="geox-literature-paper",
              title="Geological Literature Paper",
              mime_type="text/markdown",
              annotations={"audience": ["assistant"], "priority": 0.85})
async def read_paper(basin: str, paper_id: str) -> str:
    ...

# Prompt — SIMPLE (string return, no args)
@mcp.prompt(name="geox_guard",
            description="CONSTRAIN: F10 ontology enforcement.")
async def guard() -> str:
    return GUARD_PROMPT_TEXT

# Prompt — SPEC-ALIGNED (messages[] with embedded resources + arguments)
# FastMCP infers PromptArgument[] from function signature automatically.
# Parameters with defaults = optional. Parameters without = required.
@mcp.prompt(name="analyse-well-log",
            description="ANALYSE: single-well petrophysics + interpretation...")
async def analyse_well_log(las_path: str, well_name: str = "") -> list[Message]:
    """Analyse a single well log end-to-end.

    Args:
        las_path: Path to the LAS file
        well_name: Well identifier for URI resolution
    """
    return [
        Message(f"Analyse this well log:\n\n{PROMPT_TEXT}", role="user"),
        Message(
            EmbeddedResource(
                type="resource",
                resource=TextResourceContents(
                    uri=AnyUrl(f"las://{well_name or 'unknown'}"),
                    mimeType="text/plain",
                    text=f"LAS path: {las_path}\nWell: {well_name}",
                ),
            ),
            role="user",
        ),
    ]
```

### Error Envelope — The Pattern (Binding 27)

```python
import json
import httpx

# Tool with structured error envelope
@mcp.tool(name="fetch_external_data",
          annotations={"readOnlyHint": True, "openWorldHint": True})
async def fetch_external_data(url: str) -> str:
    """Fetch data from an external API with governed error handling.
    Use when the user requests data from a specific external source.
    Returns JSON on success, structured error envelope on failure.
    """
    try:
        result = await httpx.get(url, timeout=5)
        result.raise_for_status()
        return result.text
    except httpx.TimeoutException:
        return json.dumps({
            "error_code": "EXTERNAL_API_TIMEOUT",
            "message": f"Request to {url} timed out after 5s",
            "retry_allowed": True,
            "suggested_action": "Retry with shorter timeout or check if the URL is reachable"
        })
    except httpx.HTTPStatusError as e:
        return json.dumps({
            "error_code": f"EXTERNAL_API_{e.response.status_code}",
            "message": f"External API returned {e.response.status_code}",
            "retry_allowed": e.response.status_code >= 500,
            "suggested_action": "Check URL validity or try again later" if e.response.status_code >= 500 else "Do not retry — client error"
        })
```

**Why this matters:** The FreeCodeCamp pattern returns raw text/errors. The model sees `isError: true` with a Python traceback and has to guess whether to retry. Our envelope tells the model: "here's what went wrong, here's whether you can retry, here's what to do next." The model makes better decisions. Fewer hallucinated retry loops.

### Prompt Resource Embedding — The Pattern (Forged 2026-07-10)

Per MCP 2025-06-18 spec: `prompts/get` response `messages[]` supports `type: "resource"` content blocks. This lets prompts **pre-load context** before the model touches any tool.

**When to embed resources in prompts:**
- Workflow prompts that reference specific data (LAS, papers, basins)
- Pipeline prompts that need capability context (tools available, URI schemes)
- Any prompt where the host should have data in context before model reasoning

**When NOT to embed:**
- Simple guard/constraint prompts (return string)
- Prompts with no data dependency
- Prompts where the model should discover data via tools (not pre-loaded)

**FastMCP argument inference:**
- `async def fn(las_path: str)` → `PromptArgument(name="las_path", required=True)`
- `async def fn(name: str = "")` → `PromptArgument(name="name", required=False)`
- Docstring `Args:` section → `description` field on each argument
- Completion API auto-serves these to clients

---

## 17. Anti-Patterns (Refuse to Ship)

- ❌ Tool `name` containing spaces, hyphens, or capitals
- ❌ Tool `description` < 50 chars (model's only briefing — must be 50-300 chars)
- ❌ Tool `description` missing "Use when..." sentence (model needs trigger guidance)
- ❌ Tool `description` > 300 chars (model skims, not reads — long descriptions get truncated mentally)
- ❌ Resource `uri` mapping to `https://` you'll proxy
- ❌ `subscribe: true` declared when handler not implemented
- ❌ External live API exposed as Resource (not Tool)
- ❌ `_meta` on envelope instead of contents
- ❌ Template with mutable backing state (should be URI shape only)
- ❌ Cursor encode filter args server-side (clients can't re-use; OK)
- ❌ Cursor visible base64 of business fields (PII leak)
- ❌ List_changed notification with payload (forbidden)
- ❌ Hard-coded `title:` matching `name` (must diverge)
- ❌ Argument names `p1, p2, x, y, data` (use semantic names)
- ❌ Prompt returning string when it references specific data (embed resource)
- ❌ Prompt with no arguments when it accepts user input (add args to signature)
- ❌ Workflow prompt without resource embedding (model starts cold, no context)
- ❌ Tool returning raw Python/JS traceback as error message (use structured envelope: error_code, message, retry_allowed, suggested_action)
- ❌ Connecting to external MCP server without SSRF validation + trust boundary
- ❌ Forwarding federation session tokens to external MCP servers

---

## 18. The Receipt — Every MCP Change Must Document

| Field | Value |
|---|---|
| Name | unchanged since stable |
| Description | brief on its own |
| Capability declaration | honest |
| Evidence class | OBS / DER / INT / SPEC |
| Floor active | F1, F2, F11 (always); F13 if sensitive |
| Audit trail | append-only ledger entry per read |

`forge_work/YYYY-MM-DD/MCP-AUDIT-<organ>.md` is the canonical receipt.

---

## 19. Receipt Forge Location for arifOS Federation

For every MCP-related change:
- `forge_work/YYYY-MM-DD/MCP-AUDIT-<organ>.md` (per organ audit receipt)
- `forge_work/YYYY-MM-DD/MCP-CONSOLIDATED.md` (cross-organ summary)

---

## 20. Floor mapping (quick reference)

```
F1  AMANAH    → /mcp read = non-mutating
F2  TRUTH     → _meta.evidence_class present
F3  WITNESS   → _meta.actor_signature on sealed claims
F4  CLARITY   → no double registrations, no duplicate URIs
F5  PEACE²    → de-escalate in tool descriptions
F6  MARUAH    → pii_redacted + dignity-first error messages
F7  HUMILITY  → confidence cap in description (never claim certainty)
F8  GENIUS    → simplest correct path: description-first
F9  ANTI-HANTU → never claim consciousness via tool output
F10 ONTOLOGY  → AI-vs-human categories preserved
F11 AUDIT     → read_ledger.append + sha256 verified
F12 INJECTION → input sanitized; external ≠ authority
F13 SOVEREIGN → actor_signature on operator-private URIs
```

---

## 21. Citation Anchors (MCP Spec, Federal Procurement)

These bindings are derived from MCP 2025-06-18 spec text + 2025-11-25 server-card extensions + docs-agent 2026-07-10 consensus. Every binding cites its source primitive.

---

## 22. DITEMPA BUKAN DIBERI

**Naming is the first act of creation.** Every server registers a contract with the model. Honour it.

