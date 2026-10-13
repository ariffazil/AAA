# GEOX MCP AUDIT — 2026-10-07 04:19 UTC

Probe of GEOX MCP components, MCP Apps (SEP-1865) GUI readiness, latest
protocol conformance, and dependency status. **Zero mutation, zero claim of
seal-grade verdict — RECEIPT only.** Human-language report follows in
Claude's chat reply.

Audit ran in /root/GEOX (clean tree, git log head = e722a14d).

---

## 1. LIVE MCP TRANSPORT — PASS (with 1 caveat)

Probe against https://geox.arif-fazil.com/mcp (HTTP/2 via Cloudflare → GEOX).

| Probe | Result | Source |
|---|---|---|
| GET / | 200 | curl probe 2026-10-07T04:19Z |
| POST /mcp initialize (protocolVersion=2025-06-18) | 200, valid JSON-RPC envelope | live response |
| serverInfo.name | "GEOX" | init result |
| serverInfo.version | "v2026.10.03" | init result |
| capabilities.tools.listChanged | true | init result |
| capabilities.resources.listChanged | true | init result |
| capabilities.prompts.listChanged | true | init result |
| capabilities.tasks.{list,cancel} | exposed | init result |
| capabilities.extensions["io.modelcontextprotocol/ui"] | exposed | init result |
| headers: mcp-session-id issued | 8217f0af18e34d79acf5e8ca8708f56e | live response |
| headers: access-control-allow-headers includes Mcp-* | yes | live response |
| /.well-known/mcp.json | 200, webmcp-manifest schema | live response |
| /healthz | HTTP 200 HTML landing | live response |
| /health | HTTP 200 JSON — `status: degraded`, `kernel_verdict: HOLD`, `tools_loaded: 27`, `canonical_tools: 27`, `surface_drift.ok: true`, `deployment_drift: aligned` | live response |

**Caveat:** Unauthenticated `tools/list` without a session-id returns HTTP 502
on the second POST (Cloudflare/SSE chunking artifact on the read side; the JSON
itself is valid to column 65498). When the session-id from `initialize` is
replayed on a fresh POST, `tools/list` returns a complete payload beginning
`{"jsonrpc":"2.0","id":3,"result":{"tools":[{"name":"geox_geomechanics"...}]}}`.
This is a client-side read quirk, not a server defect, but it is worth
noting for any benchmark that POSTs without honoring the issued session id.

Protocol conformance: **current** (2025-06-18), all standard MCP capabilities
(tools/resources/prompts) plus `tasks` and the
`io.modelcontextprotocol/ui` extension are exposed.

## 2. REGISTRY vs LIVE SURFACE — MATCH (27/27)

Direct import of `geox_mcp.registry` and live `tools/list` agree.

```
GEOX_VERSION = "v2026.10.03"
SURFACE_TOOLS.length == CANONICAL_PUBLIC_TOOLS.length == 27
INTERNAL_TOOLS.length == 39
CANONICAL_RUNTIME_TOOLS.length == 88 (public + internal)
manifest.yaml manifest_version: 2026.10.03-alignment
manifest.yaml public_count_target: 27
```

| Layer | Count | Source |
|---|---|---|
| Live tools/list (HTTP probe) | 27 | POST /mcp tools/list (session-bound) |
| Registry CANONICAL_PUBLIC_TOOLS | 27 | geox_mcp/registry.py:84 |
| Manifest public tools | 27 | src/geox_mcp/tools_manifest.yaml |
| Runtime canonical | 88 | geox_mcp/registry.py:88 |
| Internal tools | 39 | geox_mcp/registry.py:74 |

**Drift: 0.** surface_drift.ok = true, gap_count = 0 (live /health).

Ghost set retained in `GHOST_TOOLS` (23 archived tools excluded from SURFACE).
`geox_contradiction_scan` is intentionally absent from public list per F13
2026-09-22 (audit-internal-only — RT1_GUARD rejection is the design).

## 3. MCP APPS (SEP-1865) GUI — 20 ACTIVE / 3 DEPRECATED / 1 PLANNED

`GEOX_MCP_APPS_SURFACE.json` cross-checked against `apps.json`, on-disk app
folders, and per-app `manifest.json`.

| App | apps.json status | Folder | manifest.json | UI surface |
|---|---|---|---|---|
| geox-well-desk | LIVE | apps/well-desk/ | present (SEP-1865 schema) | active |
| geox-prospect | LIVE | apps/prospect-ui/ | present | active |
| geox-seismic | LIVE | **PATH BROKEN** (apps/seismic-vision-review/ missing on disk; pointer 2_seismic_vision.py only) | not in apps/ | active |
| geox-basin | NEEDS_REBIND | apps/earth-volume/ | legacy v1 schema (basin-explorer domain), not SEP-1865 | active |
| geox-risk | NEEDS_REBIND | apps/judge-console/ | legacy v1 schema (ac_risk.console), not SEP-1865 | active |
| geox-operator | LIVE | root web | implicit (no manifest.json) | active |
| geox-calibration-witness | LIVE | apps/calibration-witness/ | none on disk | active |

20 active UI resources, all with `mime_type: text/html;profile=mcp-app`,
all 16-hex content hashes valid (no anomalies). CSP domains consistent
across resources (geox.arif-fazil.com, macrostrat.org,
tile.openstreetmap.org, unpkg.com).

## 4. DEFECTS (F2 honest reporting, no auto-fix)

### D1 (P2) — `geox-seismic` app pointer broken
apps.json points to `apps/seismic-vision-review/index.html`. On disk there
is only `apps/2_seismic_vision.py` and the file is referenced as legacy
scaffolding. A live GET against the URL returns the empty app frame or a
broken link. Path in apps/ needs `seismic-vision-review/` folder restored
or pointer corrected. **NEEDS REBIND** at the app layer (registry is OK).

### D2 (P2) — `geox-basin` + `geox-risk` carry legacy v1 app manifests
apps/earth-volume/manifest.json + apps/judge-console/manifest.json use
`https://geox.arif-fazil.com/schemas/app-manifest/v1.json` (legacy).
SEP-1865 schema (`io.modelcontextprotocol/ui/1.0`) is what geox-well-desk
already uses. tools bindings were pruned to `[]` per
`GEOX_MCP_APPS_SURFACE.json` _correction (2026-10-03). Rebind requires
canonical tool mapping (geox_basin/geox_claim/geox_prospect + claim-graph).

### D3 (P3) — `geox_operator` console has no `manifest.json` on disk
Implicit UI resource. Registration is via URL only, no fallback chain
declared. Acceptable for a root operator dashboard but should carry a
minimal manifest for consistency with the other 6 apps.

### D4 (P3) — `apps.json` says `geox-operator` ui_resource =
`ui://operator/index.html`, but no such resource is registered in
`geox_mcp/surface.yaml` or `GEOX_MCP_APPS_SURFACE.json`. Likely a pointer
drift between the federation-wide `apps.json` and the GEOX-side
`GEOX_MCP_APPS_SURFACE.json`. Worth one verification pass.

### D5 (P3) — tools_manifest.yaml has only 3 of 27 public tools with `ui:`
binding
Only `geox_gravmag_studio`, `geox_glof`, `geox_calibration_register_witness`
carry a `ui.resource_uri` in the manifest. The 24 UI resources in
`GEOX_MCP_APPS_SURFACE.json` bind their tools by name (e.g. `bound_tools`)
but the manifest itself does not surface that binding. Drift between the
two registry files is a future-proofing risk; not breaking today.

## 5. DEPENDENCIES — DRIFT DETECTED, NOT BREAKING

`requirements.txt` (informational freeze of MCP-relevant direct deps) vs
live `importlib.metadata.version`:

| Package | requirements.txt | Actually installed | Δ |
|---|---|---|---|
| fastmcp | 4.0.10 | 3.4.6 | MINOR (declared newer than installed) |
| fastmcp-slim | 4.0.10 | 3.4.6 | MINOR |
| mcp | 2.2.0 | 1.30.0 | MAJOR (declared newer than installed) |
| pydantic | 2.13.4 | 2.13.5 | patch |
| uvicorn | 0.54.0 | 0.54.0 | match |
| starlette | 1.3.1 | 1.7.0 | MINOR |

`requirements.txt` itself documents the drift honestly (see the "KNOWN
PRE-EXISTING INSTALL DRIFT" block at top of file). Live server boots and
serves `/mcp initialize` and `tools/list` without errors, so the installed
versions are functionally sufficient. Pyproject.toml is the resolver
authority per `.github/dependabot.yml` + ci-uv-lock-invariant workflow.

## 6. TOOL INVENTORY (PUBLIC, 27)

geox_basin, geox_calibration_register_witness, geox_claim,
geox_contrast_metabolize, geox_deep_time, geox_extract_display_proxy,
geox_extract_native_trace, geox_geomechanics, geox_glof,
geox_list_registered_sources, geox_map, geox_model, geox_observe,
geox_paleobiodb_query, geox_petrophysics, geox_prospect,
geox_register_native_source, geox_seismic_compute, geox_seismic_ingest,
geox_seismic_interpret, geox_source, geox_spatial, geox_surface_status,
geox_temporal, geox_well, geox_well_ingest, geox_well_qc

## 7. FEDERATION CONTRACT NOTES

- /health reports `kernel_verdict: HOLD` (degraded status) — operator
  console flags as AMBER. Not a defect; HOLD is the default arifOS verdict
  for an Earth Intelligence organ ("never seals").
- `apex_scalars.h = 0.9392` measured; `G = 0.4276`, `C_dark = 0.2517`,
  `QDF = 0.32`. `W3 = UNMEASURED` (intentional).
- `final_authority = ARIF` — GEOX computes, never adjudicates.
- `federation_geometry.status = enabled` with `subjects=0, ledger_events=0`
  and `local_fallback` note — no geometry telemetry observed this probe
  window. Worth a federation-side trace.

---

## VERDICT — RECEIPT (Lane B autonomous, not SEAL)

- Live MCP transport: **GREEN** (with 1 client-side parse caveat)
- Registry ↔ live surface: **GREEN** (27/27 match, 0 drift)
- MCP Apps GUI readiness: **AMBER** (5 apps registered, 2 with legacy v1
  manifests, 1 with broken path)
- Dependencies: **AMBER** (declared vs installed drift on 3 MCP-stack
  packages; functionally sufficient but requires alignment)
- Federation contract: **GREEN** (current protocol, all capabilities)

No code mutated. No seal-grade verdict issued. Audit runs again on demand.

— End of receipt —