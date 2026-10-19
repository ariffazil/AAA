---
name: geox-mcp-tool-invocation
version: 1.1.0
description: "How to invoke GEOX MCP tools from a shell/agent. Documents the working HTTP+streamable-HTTP session protocol (initialize → notifications/initialized → tools/call), the schema quirks (mode parameter not action; arguments not params; well_id not well), the auth header rule, and the canonical evidence-envelope output shape. Triggers on any GEOX MCP call attempt from a non-FastMCP client (Hermes shell, OpenClaw, OpenCode, custom agent)."
license: Proprietary
platforms: [linux]
---

# GEOX MCP Tool Invocation (HTTP/streamable)

Reference: GEOX v2026.07.24+ on `127.0.0.1:8081` (systemd). Other ports (8090,
8092, 8094) are NOT GEOX MCP — they are web UIs, not the canonical MCP endpoint.

## Step 1 — Open the MCP session

The endpoint is `http://127.0.0.1:8081/mcp`. It speaks MCP `2025-03-26` over
HTTP + Server-Sent-Events. The first request **must** be `initialize` — without
it, every `tools/call` returns `-32602 Invalid request parameters`.

```bash
curl -s -i -X POST "http://127.0.0.1:8081/mcp" \
  -H "Accept: application/json, text/event-stream" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":0,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"<agent>","version":"<v>"}}}' \
  | grep -i "mcp-session-id"
```

Save the `mcp-session-id` header value (e.g. `83e765d1...`). **Use it on every
subsequent request**, otherwise you get `-32602`.

## Step 2 — Acknowledge the initialization

```bash
curl -s -X POST "http://127.0.0.1:8081/mcp" \
  -H "Accept: application/json, text/event-stream" \
  -H "Content-Type: application/json" \
  -H "mcp-session-id: <SESSION>" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized"}' > /dev/null
```

This is a notification (no `id`), so it returns no body. Without this step,
the server keeps the session in `uninitialized` state and some tools may
gated against it.

## Step 3 — Call tools

```bash
curl -s -X POST "http://127.0.0.1:8081/mcp" \
  -H "Accept: application/json, text/event-stream" \
  -H "Content-Type: application/json" \
  -H "mcp-session-id: <SESSION>" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"geox_workspace","arguments":{"mode":"set","basin":"Malay","well_id":"Bekantan-1","field":"Cendor","play":"Group K"}}}' \
  -o /tmp/gw.json
```

The response is a JSON-RPC envelope. The actual tool payload is inside
`result.content[].text` as a stringified JSON. Parse with `json.loads` after
extracting the text field.

## Schema quirks (verified 2026-08-13)

| What you might guess | Actual GEOX schema |
|---|---|
| `action: "set"` | `mode: "set"` (mode is the canonical verb) |
| `well: "Bekantan-1"` | `well_id: "Bekantan-1"` |
| `basin: "Malay"` | `basin: "Malay"` — workspace accepts free name; `geox_basin` resolves aliases |
| `params: {...}` | `arguments: {...}` — FastMCP envelope |
| tools at `/tools` | `/tools` exists but is the human-readable list; MCP tools require `/mcp` JSON-RPC |

## Error codes you'll actually see

| Code | Meaning | Fix |
|---|---|---|
| `-32600` | Not Acceptable | Add `Accept: application/json, text/event-stream` |
| `-32602` | Invalid request parameters | **Most likely: missing `mcp-session-id` header, or missing `initialize` call first, or wrong schema key** |
| `-32001` | Internal tool error | Read `data.verdict` + `data.trace_id`; the tool has governance metadata |
| `EVIDENCE_SCHEMA_VIOLATION` | Tool returned SUCCESS but null evidence (Stage-1 outputSchema enforcement) | Tool needs the basin/well context set first via `geox_workspace` mode=set |

## Output envelope (canonical shape)

Every GEOX tool call returns an evidence envelope:

```json
{
  "_well_conformance": {
    "claim_state": "OBSERVED|DERIVED|HYPOTHESIS|HOLD|...",
    "witness_type": "AI|HUMAN|HYBRID",
    "organ_type": "GEOX|BASIN|PETROPHYSICS|...",
    "conformance_version": "v1.0",
    "conformant": true
  },
  "tool": "geox_basin",
  "ok": true,
  "mode": "derived|observed",
  "ext_witness_ready": false,
  "provenance": {"organ": "geox", "mode": "..."},
  "isError": false,
  "status": "OK|ERROR|...",
  "execution_status": "COMPLETED|...",
  "governance_status": "SEAL|HOLD|...",
  "confidence": 0.65,
  "authority_claim": "ADVISORY|EVIDENCE|...",
  "_evidence_envelope": {
    "_identity": {"artifact_id": "...", "session_id": "...", "actor_id": "..."},
    "_receipt": {"content_sha256": "...", "is_error": false}
  },
  "data": { ... tool-specific payload ... }
}
```

`isError: true` ≠ HTTP error. The HTTP is 200; the tool itself returns
an error inside the envelope. Always check `isError` AND `ok`.

## What the agents actually own

- `geox_workspace` (mode=set|view|history|evidence|reset|relations)
- `geox_basin` (mode=profile|resolve|macrostrat|backstrip|...)
- `geox_well_ingest` (LAS/SEG-Y/DST load)
- `geox_petrophysics`, `geox_geomechanics`, `geox_source`, `geox_seismic_*`, `geox_prospect`, `geox_model`, `geox_claim`, `geox_spatial`, `geox_map`, `geox_temporal`, `geox_deep_time`, `geox_well`, `geox_well_qc`

18 tools total. Web UI enumeration: `GET /webmcp/tools` returns a categorized list (use for discovery, not for calling).

## Pitfalls (verified 2026-08-13)

1. **DON'T call `/tools/call` directly** — returns 404. Must use `/mcp` JSON-RPC.
2. **DON'T skip `initialize`** — every tool call returns `-32602` without it.
3. **DON'T forget the `mcp-session-id` header** — same `-32602` error.
4. **DON'T use `Accept: application/json` alone** — server needs `text/event-stream` too.
5. **DON'T call `geox_basin(mode="profile")` without workspace context** — returns EVIDENCE_SCHEMA_VIOLATION. Set workspace first.
6. **DON'T use `subprocess` inside `execute_code`** — security policy blocks it. Write a Python script and run via `terminal`.
7. **Empty `GEOX_SECRET_TOKEN` env → stdio-bypass fallback** — but HTTP requests still need to follow the protocol above. The "stdio-bypass" path is for stdio transport only.
8. **Process PID 1237 = port 8090 (static web)**. PID varies for 8081. Check `ss -tlnp | grep ":8081"`.

## Reusable recipe (Python script)

When calling from a shell agent that needs >2 tool calls, write a script:

```python
import json, subprocess
SESSION = "<from initialize response>"
BASE = "http://127.0.0.1:8081/mcp"

def geox_call(tool_id, tool_name, args, session=SESSION, base=BASE):
    payload = json.dumps({"jsonrpc":"2.0","id":tool_id,"method":"tools/call",
                          "params":{"name":tool_name,"arguments":args}})
    r = subprocess.run(["curl","-s","-X","POST",base,
                        "-H","Accept: application/json, text/event-stream",
                        "-H","Content-Type: application/json",
                        "-H",f"mcp-session-id: {session}",
                        "-d",payload],
                       capture_output=True, text=True, timeout=60)
    data = json.loads(r.stdout)
    for item in data.get("result", {}).get("content", []):
        if item.get("type") == "text":
            return json.loads(item["text"])
    return data
```

This is what works. Verified 2026-08-13.

## Reference

- GEOX MCP server source: `/root/GEOX/src/geox_mcp/server.py`
- GEOX ontology: `/root/GEOX/resources/ontology/{formation_water,pressure_states,...}.yaml`
- GEOX basin profile: `/root/GEOX/resources/basins/malay_basin/basin_profile.yaml`
- arifOS meridian for tool emission: `/root/AAA/governance/` (F2/F7/F9/F11 floors)

*DITEMPA BUKAN DIBERI — Tool invocation is forged, not guessed.*
## Tool coverage — the 7 tools no other skill documents (2026-10-20)

Verified against the live `tools/list` schema and by calling each one. Zero other
GEOX skills mention these names, so an agent had no procedure and re-derived from
priors. Use these exact shapes.

| Tool | Minimal working call | Returns | Gate |
|---|---|---|---|
| `geox_list_registered_sources` | `{}` | registered native SEG-Y sources | none — safe read |
| `geox_observe` | `{"modality_hint":"map"}` | EarthObservationPacket | **HOLD** without `artifact_ref`; vision output is EVIDENCE, interpretation stays HYPOTHESIS |
| `geox_register_native_source` | `{"source_uri":"/abs/path.segy","source_id":"SRC-1","classification":"public","authority":"registrant"}` | registration receipt + SHA-256 + binary header | validates file existence; does NOT load traces |
| `geox_extract_native_trace` | `{"source_id":"SRC-1","trace_index":0}` | NativeTraceRef + permitted/prohibited uses | HOLD if source unregistered, authority insufficient, or classification disallows |
| `geox_calibration_register_witness` | `{"witness":{"type":"structural","datum":"WGS84","vertical_datum":"MSL","estimated_depth_uncertainty_m":25,"calibration_method":"literature","reference":"Madon 2006"}}` | witness registration | without a witness, structural gates return **UNMEASURED** |
| `geox_glof` | `{"mode":"run"}` | multi-phase cascade result | modes: run / inverse / mcmc / propagate / phase |
| `geox_paleobiodb_query` | `{"mode":"taxa","name":"Tyrannosaurus"}` | PBDB taxa / occurrence / zone | public-domain; literature-derived, unevenly sampled |

**Chain rule.** `register_native_source` → `list_registered_sources` → `extract_native_trace`
is the only order that works; each step writes the handle the next one reads. Registering
without extracting leaves the lane empty (that is why the source registry read 0 entries).

**Do not** call `geox_observe` expecting pixels without an artifact, and do not treat a
returned `HOLD` as a failure — it is the gate working.
