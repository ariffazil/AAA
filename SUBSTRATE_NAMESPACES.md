# SUBSTRATE NAMESPACES — Canon of MCP Tool Naming

> **Ratified:** 2026-06-15 17:55 UTC by FORGE-000Ω
> **Status:** ACTIVE CANON (aligned with F13 SOVEREIGN ruling 2026-06-14)
> **Authority:** "name is the first act of creation"

This document declares the canonical namespace discipline for every MCP tool in the arifOS federation. **All tools must carry an organ or peer-agent prefix.**

---

## 0. The Iron Rule (F13 SOVEREIGN ruling 2026-06-14)

Per `arifOS/AGENTS.md` "Namespace ruling":

| Prefix | Status | Owner |
|--------|:------:|-------|
| `arif_*` | ✅ SANCTIONED | arifOS kernel + diagnostic |
| `hermes_*` | ✅ SANCTIONED | Hermes ASI peer agent (port 18001) |
| `forge_*` | ✅ SANCTIONED | A-FORGE pre-execution (exposed via arifOS surface) |
| `mcp_*` | ✅ SANCTIONED | MCP utility / operational diagnostics |
| `wealth_*` | ✅ SANCTIONED | WEALTH capital-intelligence organ |
| `geox_*` | ✅ SANCTIONED | GEOX earth-intelligence organ |
| `well_*` | ✅ SANCTIONED | WELL human-readiness organ |
| `aforge_*` | 🟡 RESERVED | A-FORGE organ (currently HTTP REST on :7071) |
| `arifos_*` | ❌ BLOCKED | Internal-only prefix, **never** exposed on public MCP |

---

## 1. Live Ratification (2026-06-15 17:54 UTC)

**157 tools probed across 8 namespaces. 0 invalid. 18 legacy redirects. Discipline: VALID.**

| Namespace | Tools | Invalid | Legacy | Latency | Status |
|-----------|------:|:-------:|:------:|--------:|:------:|
| arifOS (arif_*) | 39 | 0 | 0 | 460ms | ✅ |
| WEALTH (wealth_*) | 21 | 0 | 0 | 14ms | ✅ |
| GEOX (geox_*) | 40 | 0 | 17 | 44ms | ✅ |
| WELL (well_*) | 18 | 0 | 1 | 23ms | ✅ |
| A-FORGE (aforge_*) | 0 | 0 | 0 | 19ms | 🟡 HTTP REST (not MCP) |
| Hermes (hermes_*) | 0 (exposed via arifOS) | 0 | 0 | 422ms | ✅ |
| A-FORGE pre-exec (forge_*) | 3 (exposed via arifOS) | 0 | 0 | 933ms | ✅ |
| MCP utility (mcp_*) | 1 (mcp_drift_check) | 0 | 0 | 6ms | ✅ |

**Registry hash:** `b3:8dbc44065af0d2b672421929d2998...` (BLAKE3 of canonical namespaces + legacy aliases)

---

## 2. Legacy Aliases (18 total)

Per GEOX's existing `LEGACY_ALIAS_MAP` plus future-proofing:

```
GEOX consolidation (17):
  geox_deviation_survey_inspect → geox_header_inspect
  geox_tops_inspect             → geox_header_inspect
  geox_seismic_inspect          → geox_header_inspect
  geox_ingest_bundle            → geox_data_ingest_bundle
  geox_qc_bundle                → geox_data_qc_bundle
  geox_anomalous_contrast       → geox_ac_detector
  geox_evidence_summarize_cross → geox_evidence_reason
  geox_process_abduction        → geox_evidence_reason
  geox_evidence_contradiction_scan → geox_evidence_reason
  geox_well_compute_gr_bins     → geox_sequence_stratigraphy
  geox_well_build_packages      → geox_sequence_stratigraphy
  geox_well_infer_seq_strat     → geox_sequence_stratigraphy
  geox_well_analyze_sequence    → geox_sequence_stratigraphy
  geox_seismic_tie              → geox_seismic_compute
  geox_seismic_analyze_volume   → geox_seismic_compute
  geox_td_anchor                → geox_seismic_compute
  geox_forward_model            → geox_seismic_compute
  geox_petrophysics             → geox_subsurface_generate_candidates
  geox_section_interpret_correlation → geox_sequence_interpret
  geox_stratigraphy_preview_config  → geox_sequence_interpret
  geox_stratigraphy_run_pipeline    → geox_sequence_interpret
  geox_subsurface_candidates    → geox_subsurface_generate_candidates
  geox_prospect_judge_preview   → geox_prospect_evaluate
  geox_prospect_judge_seal      → geox_prospect_evaluate
  geox_prospect_judge_verdict   → geox_prospect_evaluate
  geox_abstraction_guard        → geox_query_intake
  geox_vision_minimax_inference → geox_vision_perceptual_inventory
  geox_vision_calibrate         → geox_vision_perceptual_inventory
  geox_vision_audit             → geox_vision_perceptual_inventory
  geox_attribute_registry_list_tool → geox_attribute_registry_list
  geox_blend_volume_tool        → geox_blend_volume
  geox_blockspace_resolution_tool → geox_blockspace_resolution
  geox_coord_transform_tool     → geox_coord_transform
  geox_fault_stick_ingest_tool  → geox_fault_stick_ingest
  geox_segy_export_tool         → geox_segy_export
  geox_seismic_compute_attribute_tool → geox_seismic_compute
  geox_volume_frame_tool        → geox_volume_frame
  geox_dst_ingest_test          → geox_dst_ingest
  geox_literature_ingest        → geox_evidence_discover
  geox_las_inspect              → geox_header_inspect
  geox_seismic_segy_inspect     → geox_header_inspect
  geox_registry                 → geox_system_registry_status
  geox_report_to_workflow       → geox_query_intake

WELL diagnostic exception (1):
  mcp_health_check (deprecated; use well_assess_reliability(mode='health'))
```

---

## 3. Per-Namespace Lane Discipline

### arifOS lanes (6)
- `discovery` (5): arif_ping, arif_organ_attest, arif_system_status, arif_conformance_report, arif_initialize_probe
- `evidence` (5): arif_sense_observe, arif_evidence_fetch, arif_memory_recall, arif_ops_measure, arif_schema_echo
- `reasoning` (3): arif_mind_reason, arif_heart_critique, arif_reply_compose
- `judgment` (3): arif_judge_deliberate, arif_vault_seal, arif_forge_execute
- `governance` (4): arif_kernel_route, arif_lease_issue, arif_lease_inspect, arif_lease_revoke
- `transport` (4): arif_session_init, arif_gateway_connect, arif_transport_echo, arif_version_echo + canary

### WEALTH lanes (4)
- `wealth_calculate` (16+): conservation, flow, entropy, gradient, energy, time, inertia, field, signal, game, boundary, omni_wisdom, agent_path, inequality_kernel, institutional_entropy_scorer, role_scarcity_risk
- `wealth_audit` (15+): stock_analysis, pre_trade, fundamentals, verify_math, position_size, bursa_evidence, bursa_snapshot, bursa_screen, bursa_cost, tac9, contrast, confluence, separate_pl, r_multiple, exposure
- `wealth_data` (3+): market_data, personal_finance, survival_engine
- `wealth_meta` (3+): system_registry_status, governance_verdict, synthesize

### GEOX lanes (4 — per GEOX.yaml §3)
- `geox_discovery` (5): system_registry_status, basin_resolve, query_intake, query_macrostrat, report_to_workflow
- `geox_evidence` (13): data_ingest_bundle, data_qc_bundle, evidence_discover, evidence_attach, claim_create, claim_challenge, ...
- `geox_reasoning` (17): seismic_compute, horizon_contrast_surface, subsurface_generate_candidates, evidence_reason, vision_*, ...
- `geox_judgment` (5): claim_validate, claim_seal, prospect_judge_verdict, prospect_evaluate, subsurface_verify_integrity

### WELL lanes (1)
- `well_measure` (18): assess_homeostasis, assess_metabolism, assess_livelihood, validate_vitality, guard_dignity, measure_gradient, classify_substrate, detect_boundary, compute_metabolic_flux, assess_sovereign_entropy, assess_reliability, trace_lineage, 13_signal_coverage, check_repair, medical_boundary, well_registry_status, system_registry_status, mcp_health_check

### Hermes lanes (3 — ASI peer agent)
- `asi_observation`: hermes_system_status, hermes_vault_query
- `asi_judgment`: hermes_judge_deliberate (?), hermes_fact_check, hermes_epistemic_check
- `asi_deliberation`: hermes_plan_review, hermes_memory_steward, hermes_cross_verify

### forge lanes (1 — A-FORGE pre-exec)
- `forge_sub_execution`: forge_plan, forge_dry_run, forge_query

### mcp lanes (1 — utility)
- `mcp_diagnostic`: mcp_drift_check

---

## 4. Cross-Organ Tool Routing

`arif_kernel_route(mode=route, target=tool_name)` is the unified router:

```
parse namespace: "wealth" | "geox" | "well" | "arif" | "hermes" | "forge" | "mcp"
    ↓
route to organ/peer:
    wealth_* → WEALTH :18082
    geox_*   → GEOX :8081
    well_*   → WELL :18083
    arif_*   → arifOS :8088
    hermes_* → Hermes :18001 (via arifOS surface)
    forge_*  → A-FORGE :7071 (via arifOS surface)
    mcp_*    → operational diagnostic (via arifOS)
    ↓
OPA policy: arifos/tool_policy.rego (lane-aware)
    ↓
wrapped in arifOS kernel envelope
    ↓
return to caller
```

If the tool name has no valid namespace → `MATH_ERROR / VOID / SABAR`.

---

## 5. NamespaceGuard (linter)

`arifOS/arifosmcp/arifos_registry/namespace_guard.py` enforces:

```python
CANONICAL_NAMESPACES = ("arif", "wealth", "geox", "well", "hermes", "forge", "mcp")
CANONICAL_ORGAN_PREFIXES = CANONICAL_NAMESPACES + ("aforge",)
BLOCKED_PUBLIC_PREFIXES = ("arifos",)  # internal-only, never exposed

def validate(name: str) -> NamespaceGuardResult:
    if not SNAKE_CASE.match(name): return INVALID
    ns = name.split("_")[0]
    if ns in BLOCKED_PUBLIC_PREFIXES: return INVALID  # arifos_ is blocked
    if ns not in CANONICAL_ORGAN_PREFIXES: return INVALID
    organ = registry.resolve_organ_for_tool(name)
    if organ is None: return INVALID
    if name.startswith(f"{ns}_{ns}_"): return INVALID  # double prefix
    return VALID
```

A tool that fails this check is rejected at registration time.

---

## 6. References

- `arifOS/AGENTS.md` "Namespace ruling (F13 SOVEREIGN 2026-06-14)" — authoritative canon
- `/root/AAA/REPO_AUTHORITY_MATRIX.md` — per-organ authority
- `/root/AAA/schemas/agent_card.schema.json` — namespace_scope in agent cards
- `/root/arifOS/arifosmcp/arifos_policy/rego/tool_policy.rego` — OPA namespace policy
- `/root/arifOS/arifosmcp/arifos_registry/mcp_tool_registry.py` — tool manifest
- `/root/arifOS/arifosmcp/arifos_registry/substrate_namespace_registry.py` — single source of truth
- `/root/arifOS/arifosmcp/arifos_registry/namespace_guard.py` — linter
- `/root/arifOS/arifosmcp/arifos_registry/substrate_ratification.py` — live probe
- `/root/geox/src/geox_mcp/registry.py` — GEOX canonical + legacy map
- `/root/WEALTH/internal/monolith.py` — WEALTH tool definitions
- `/root/WELL/server.py` — WELL tool definitions

---

*Ratified 2026-06-15 17:55 UTC by FORGE-000Ω. DITEMPA BUKAN DIBERI.*
