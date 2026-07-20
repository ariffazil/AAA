---
id: mcp-smoke-test
name: FORGE-mcp-smoke-test
version: 1.1.0
description: Validate that MCP servers respond correctly to health probes and basic tool calls. Detect down servers, mismatched schemas, and transport errors.
owner: AAA
risk_tier: low
host_compatibility:
  - claude-code
  - codex
  - opencode
  - kimi
  - kimi-code
version_lock: pending
trinitarian:
  - Ω
functional_tags:
  - Ops
  - Audit
layer: RUNTIME
autonomy_tier: T1
floor_scope:
  - F2
  - F4
  - F11
---

# MCP Server Smoke Test

Validate that MCP servers respond correctly to health probes and basic tool calls. Detect down servers, mismatched schemas, and transport errors.

## Usage

Run smoke tests against all federation MCP endpoints to verify liveness and schema compliance.

## Targets

- arifOS :8088
- A-FORGE :7071
- GEOX :8081
- WEALTH :18082
- WELL :18083

## ChatGPT/MCP-Apps Conformance Matrix

App-surface extension of the generic smoke test above, for servers exposing
MCP-App (`ui://`) surfaces. Authoritative contract: the sovereign GEOX
blueprint at `/root/forge_work/2026-07-20/GEOX-CHATGPT-MCP-GUI-BLUEPRINT.md`
(contracts #2, #4, #8, #9, #10). The generic health/smoke layers remain the
floor; a server that advertises `_meta.ui.resourceUri` on any tool passes
only when all five layers below also pass. GEOX :8081 is the first target.

### Layer A — Deterministic boot-contract invariants (blueprint #2)

The server must fail startup if a UI-bound tool references a `ui://`
resource that `resources/read` cannot serve; the smoke test asserts the same
at runtime:

1. `tools/list` names == canonical app registry (the single source of truth
   that generates the tool manifest — never a hand-edited copy).
2. `resources/list` covers every `ui://` URI referenced by any tool's
   `_meta.ui.resourceUri`.
3. `resources/read` on each of those URIs returns MIME
   `text/html;profile=mcp-app`.

Compact pytest example (raw JSON-RPC over the MCP endpoint):

```python
import httpx

MCP_URL = "http://localhost:8081/mcp"   # GEOX app-surface endpoint
HEADERS = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
UI_MIME = "text/html;profile=mcp-app"

def rpc(method: str, params: dict | None = None) -> dict:
    body = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}}
    resp = httpx.post(MCP_URL, json=body, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return resp.json()["result"]

def test_boot_contract(registry_tool_names: set[str]):
    tools = rpc("tools/list")["tools"]
    # 1. tools/list names == canonical app registry
    assert {t["name"] for t in tools} == registry_tool_names
    # 2. resources/list covers every ui:// URI referenced by _meta.ui.resourceUri
    bound = {
        t["_meta"]["ui"]["resourceUri"]
        for t in tools
        if t.get("_meta", {}).get("ui", {}).get("resourceUri")
    }
    listed = {r["uri"] for r in rpc("resources/list")["resources"]}
    assert bound <= listed
    # 3. every ui:// read returns text/html;profile=mcp-app
    for uri in bound:
        contents = rpc("resources/read", {"uri": uri})["contents"]
        assert any(c["mimeType"] == UI_MIME for c in contents), uri
```

### Layer B — structuredContent vs outputSchema (blueprint #4)

On the `tools/call` happy path, every tool returning `structuredContent`
must declare an `outputSchema` from the pinned families (GeoxStatusResult,
GeoxArtifactResult, GeoxWellResult, GeoxSeismicResult, GeoxMapResult,
GeoxProspectResult, GeoxClaimResult, GeoxEvidenceResult) and the returned
`structuredContent` must validate against it (jsonschema). Schemas carry
`additionalProperties: false` with required fields pinned; smoke must also
reject secrets, trace IDs, and dense arrays in `structuredContent`.

### Layer C — Error surface (blueprint #9)

Tool-originated failures return `CallToolResult` with `isError: true` so the
model can self-correct — never a protocol crash. Smoke: trigger a known-bad
input on a protected tool and assert `isError: true` with no JSON-RPC
error envelope and no transport failure.

### Layer D — Auth matrix (blueprint #8)

OAuth 2.1 resource server with RFC 9728 protected-resource metadata and a
canonical `resource` identity identical across the MCP endpoint, PRM URL,
OAuth `resource` param, and token audience validation. Smoke asserts:

- Unauthenticated call to a protected tool → 401 with a valid
  `WWW-Authenticate` header carrying a `resource_metadata` pointer to the
  PRM document (`authorization_servers` present there).
- Wrong-audience token → hard 401.
- Expired token → hard 401.
- Missing scope (per-tool `securitySchemes` / scope map) → fail closed
  (401/403), never a silent success.

### Layer E — Host-surface evidence gates (blueprint #10)

Submission-path gates, in order; each is a precondition for the next:

1. Developer Mode golden prompts — direct, indirect, and negative prompt
   sets all pass against the live server.
2. API Playground — raw JSON-RPC log check confirms the expected
   `tools/list` / `tools/call` / `resources/read` exchange with no schema
   or MIME drift.
3. Web + Android + iOS — render, resize, and state-persistence evidence
   captured per surface.

The plugin submission package (verified publisher, exact CSP, unique widget
domain, privacy policy, support contact, reviewed metadata snapshots,
screenshots, rollback note) is gated on all prior layers passing — never
assembled early.
