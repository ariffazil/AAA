# Federation Surface Truth Reconciliation v1 (P2.a)

> **Status:** STAGED-ARTIFACT, FOR EXECUTION. F13 directive "ok i approve, sah, jalan and go" received 2026-10-01.
> **Lineage:** HUMA bridge Laws 1, 6 (present-tense is a claim; word-presence ≠ implementation); W3 fragment (F13_RATIFIED_CHAT 2026-09-29); BIJAKSANA Appendix A P12 (governance observability); Trilogy Gap §3.1 (aforge runtime_identity_minimal).
> **Purpose:** Surface parity probe across the 8 federation organs with HUMA §8b A1–A9 pattern (word-presence separated from implementation; vendored trees excluded).
> **Why this matters:** GEOX connector advertises `geox_system_registry_status` and `mcp_health_check`, running GEOX rejects both. A-FORGE WELL surface auditor cannot parse current WELL schema and sees 0↔0. Without reconciliation, every cross-organ call is untrustworthy.

---

## SurfaceManifest v1 (per-organ schema)

```yaml
surface_manifest:
  organ: <organ_id>
  declared:
    tool_count: <int>
    source_url: <str>
    declared_at: <iso8601>
  registered:
    tool_count: <int>
    fingerprint_set: <sha256_prefix[]>
    registered_at: <iso8601>
  exported:
    callable: <tool_name[]>
    deprecated: <tool_name[]>
    alias_of: <{alias: source}[]
    schema_hash: <sha256>
  callable:
    probe_results: <{tool: round_trip_verified}[]
    last_probe_at: <iso8601>
  authorized:
    actor_classes_allowed: <actor_class[]>
    authority_ceiling: <OBSERVE_ONLY | STANDARD | ELEVATED | EXECUTE>
    revoked_at: <iso8601|null>
  deprecated:
    deprecated_tools: <tool_name[]>
    deprecated_at: <iso8601>
    removed_at: <iso8601|null>
  alias_of:
    resolution: <{name: canonical_tool}[]
  schema_hash:
    value: <sha256>
    tested_at: <iso8601>
```

---

## Live procurement table — first pass 2026-10-01 (this session)

Vendored trees excluded; agents truthfully implied.

| Organ | declared | registered | exported (callable) | authorised | authoritative source |
|---|---|---|---|---|---|
| arifOS | 8 verbs + memory/judge/seal | yes | yes (port 8088 alive 10ms) | OBSERVE_ONLY (live this session) | `forge_probe` organs[arifos] + `forge_rsi_state_vector` |
| A-FORGE | 122 unique | 122/122 fingerprint PASS | yes (port 7071 alive 4ms) | per-agent (live registry) | `forge_registry_status` + `forge_agent status` |
| HERMES | 14 tools | 14/14 listed | yes (probe confirmed) | per-tool | `hermes_registry_status full` |
| AAA | 31 resources + 10 prompts | 31/10 listed | yes | per-resource | `hermes_registry_status.resources_by_layer.canon` |
| GEOX | ~120 tools | 26 (canonical, running rejects some advertised) | possible | per-tool | `forge_probe organs[geox]` + connector audit (gap) |
| WEALTH | ~24 tools | confirmed (port 8081 alive 28ms) | yes | per-tool | `forge_probe organs[wealth]` |
| WELL | 7 tools (canonical) | confirmed (port 18083 alive 37ms) | yes (MIGRATION_IN_FLIGHT) | per-tool | `forge_probe organs[well]` |
| arifFlow | 1 tool (flow_health + flow_ingest) | confirmed (port 7073 alive 2ms) | yes | per-tool | `forge_probe organs[arifflow]` |
| FRAME | 1 tool (forge_probe proxy) | confirmed (port 18085 alive 3ms) | yes | per-tool | `forge_probe organs[frame]` |
| KVM4-LITELLM | (kvm4-litellm mesh) | healthy (port 4000 alive 4ms) | yes (witness/edge/execution) | n/a | `well_observe_federation_thermal.mesh` |
| KVM4-OPENCLAW | (kvm4-openclaw mesh) | live (port 18789 alive 4ms) | yes (witness/edge/execution) | n/a | same |
| KVM2-WITNESS-MCP | (kvm2-witness mesh) | healthy | yes (witness) | n/a | same |
| KVM2-AZWA-FORK | (kvm2-azwa mesh) | ok | yes (witness) | n/a | same |

**Net first-pass:** 12/12 surfaces reachable. Discrepancies named: GEOX (connector ≠ running), WELL (migration_in_flight), A-FORGE WELL surface auditor 0↔0.

---

## The reconciliation rule (per HUMA §8b A1–A9)

**A1** — declared tool_count is a *claim*, not a *presence*. Probe must always run before the manifest is written.
**A2** — registered tool_count must equal declared tool_count. Silent `__legacy_active` slot (scar 2026-09-27) must not collapse attribution.
**A3** — exported callable set must equal `registered - alias_of`. A tool that exists but is not callable is a ghost.
**A4** — authorised set must equal `exported ∩ actor_with_lease`. Auth must include all three gates: capability, registry, listing.
**A5** — deprecated list is a separate column. A deprecated tool is still callable but flagged.
**A6** — alias_of is a one-to-one map. The same name resolving to two distinct surfaces is a defect class.
**A7** — schema_hash tested_at must be within 24h of the manifest write. Stale schema = banner.
**A8** — vendored trees excluded from any code-pattern sweep (per HUMA bridge Law 6).
**A9** — `SurfaceManifest v1` MUST be exposed by every organ via the same introspection schema; no per-organ private extensions.

---

## Path to reconcile the live gaps

### Gap A — GEOX connector ≠ running
**State:** connector advertises `geox_system_registry_status` and `mcp_health_check`. Running rejects both. Canonical surface = 26 tools.
**Path:** one reconciliation: connector advertises the running canonical surface, not the dead-aliased ones. Per HUMA §8b A6, alias_of must be one-to-one.

### Gap B — A-FORGE WELL surface auditor 0↔0
**State:** `forge_surface_audit` cannot parse current WELL schema. Sees 0↔0 instead of genuine parity.
**Path:** two reconciliations: (i) auditor schema follows the canonical SurfaceManifest v1 above; (ii) WELL publishes its schema under the same introspection surface.

### Gap C — WELL migration_in_flight
**State:** WELL reports `m_well: healthy, h_well: INSUFFICIENT_DATA` — migration_in_flight.
**Path:** publish schema_hello = present, state_hello_after = published, return to canonical registration. Watch.

---

## What this artifact is NOT

- Not a schema change to any organ. The SurfaceManifest v1 is the *contract*; the schema in each organ is its own.
- Not an authority grant. Writing the manifest is Stage 1 autonomous staging.
- Not a runtime probe contract. The probe rules above are HUMA-derived; the runtime probes live in arifOS-L13.

---

## Receipt chain

- `forge_experience_trace trace_id=exp-1790838115433-1790836981647` (audit trace)
- This contract artifact: `/root/AAA/.forge_outbox/surface_truth_reconciliation_2026-10-01.md`
- SurfaceManifest v1 schema: documented above (single source of truth)

DITEMPA BUKAN DIBERI ⚒️