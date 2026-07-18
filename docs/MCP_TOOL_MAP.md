# MCP Tool Map — Federation-Wide Inventory

> **Generated:** 2026-07-18
> **Purpose:** Complete map of all MCP tools, descriptions, prompts, and resources across the federation.
> **Feedback source:** Live agent (Claude) tool schema analysis.

---

## 1. arifOS (Port 8088) — Governance Kernel

**Status:** ✅ Healthy | **Tools:** 8 public | **Protocol:** Streamable HTTP

### Public Tools (CANONICAL-9)

| Tool | Stage | Description | Floors | Modes |
|------|-------|-------------|--------|-------|
| `arif_init` | 000 | Session ignition — binds actor, floors, audit | L01, L11, L12 | init, light, resume, validate, canary, preflight, triage, epoch_open, epoch_seal, opt_out |
| `arif_observe` | 111 | Sense reality into evidence (web, URL, vitals, repo, entropy) | L02, L03, L07, L12 | search, fetch, ingest, vitals, compass, atlas, entropy_dS |
| `arif_think` | 333 | Structured reasoning under F2/F7 | L02, L05, L06, L07, L08, L09, L10 | reason, reflect, verify, plan, plan_review, plan_approve, refactor_plan, metabolize, axioms, simulate, wonder |
| `arif_route` | 444 | Intent→organ router (GEOX/WEALTH/WELL/A-FORGE) | L01, L04, L10, L11 | route, bridge |
| `arif_memory` | 555 | Memory governor — L1–L6 stack | L01, L02, L04, L08, L11, L12, L13 | recall, inspect, attest, remember, promote, revise, forget, audit |
| `arif_judge` | 888 | Constitutional verdict — SEAL/HOLD/SABAR/VOID | L01, L02, L11, L13 | intercept, judge, validate, hold, escalate |
| `arif_forge` | 777 | Execution gate via A-FORGE | L01, L11, L13 | engineer, query, write, generate, commit, recall, dry_run |
| `arif_seal` | 999 | VAULT999 immutable append | L01, L11, L13 | seal, verify, ledger, changelog, audit |

### Resources (23)

| URI | Name |
|-----|------|
| `arifos://doctrine` | Constitutional Doctrine |
| `arifos://trinity` | AAA Trinity Lanes |
| `arifos://schema` | Canonical Schema |
| `arifos://civilization` | Civilizational Ontology |
| `arifos://seal-readiness` | Seal Readiness & Vault Integrity |
| `arifos://jurisdiction` | Jurisdiction & Autonomy Bands |
| `arifos://identity` | Sovereign Identity Manifest |
| `arifos://memory` | Memory Architecture (L1–L6) |
| `arifos://vitals` | Vitals |
| `arifos://bootstrap` | Federation Bootstrap Context |
| `arifos://loop-engineering` | 7-Stage Reality Engineering Loop |
| `arifos://quickstart` | LLM Client Quickstart |
| `arifos://mcp-alignment` | MCP Spec Conformance Matrix |
| `tree777://index` | Tree777 Index |
| `arifos://human/metabolized` | Human Metabolized |
| `arifos://reality/state` | Reality State |
| `arifos://mcp/surface-map` | MCP Surface Map |
| `arifos://wisdom/quotes/all` | Wisdom Quotes (All) |
| `arifos://wisdom/quotes/disputed` | Wisdom Quotes (Disputed) |
| `arifos://wisdom/quotes/arifos-doctrine` | Wisdom Doctrine |
| `arifos://wisdom/quotes/prohibited-uses` | Wisdom Prohibited Uses |
| `arifos://atlas333/index` | ATLAS333 Index |
| `arifos://atlas333/seal/head` | ATLAS333 Seal Head |

### Internal/Diagnostic Tools (40+)

- `arif_kernel_intercept` — Minimum Constitutional Kernel interceptor
- `arif_critique` — Ethical/dignity/risk stress (absorbed into arif_think mode=critique)
- `arif_bridge_connect` — Low-level organ call
- `arif_compose` — Final human-facing composition
- `arif_fetch` — Fetch and preserve external evidence
- `arif_canary` — Unified transport diagnostic probe (6 modes)
- `arif_vault_query` — Query VAULT999 audit ledger
- `hermes_*` (7) — Cross-verification, fact-check, vault, epistemic
- `forge_*` (3) — Pre-execution planning (dry_run, plan, query)
- `arif_lease_*` (3) — Capability lease lifecycle
- `arif_*_attest` (4) — Federation organ attestation
- `arif_*_peer_contract` (3) — P2P capability peering
- `arif_detect_*` (2) — Narrative/institutional detection
- `arif_*_diagnostic` (6) — Health probes, drift checks, budget, floor status

---

## 2. A-FORGE (Port 7071) — Engineering Actuator

**Status:** ✅ Healthy | **Tools:** 111 total (22 stateless HTTP, 89 session-required) | **Protocol:** Streamable HTTP

### Core Forge Tools

| Tool | Description | Class |
|------|-------------|-------|
| `forge_skill` | Dynamic tool forge — generates new MCP tool via LLM | EXECUTE |
| `forge_seal` | Seal Tri-Witness validated skill into VAULT999 | IRREVERSIBLE |
| `forge_registry` | Dynamic skill registry (list, get, scars, fingerprint, scan) | OBSERVE |
| `forge_evaluate` | APEX v36Ω evaluation gate (G = A·P·E·X·Φ) | ANALYZE |
| `forge_witness` | APEX v36Ω tri-witness consensus gate (W³) | ANALYZE |
| `forge_scar` | APEX v36Ω scar metabolization gate | ANALYZE |
| `forge_register` | APEX v36Ω gated registration | MUTATE |
| `forge_reality_loop` | 7-stage state-tracking ledger | EXECUTE |
| `forge_predict` | Pre-action simulation layer | ANALYZE |

### Gateway Tools (External MCP Integration)

| Tool | Description | Class |
|------|-------------|-------|
| `forge_research` | Governed research across web sources | OBSERVE |
| `forge_search` | Governed web search via Brave | OBSERVE |
| `forge_docs_lookup` | Governed docs lookup via Context7 | OBSERVE |
| `forge_browser_navigate` | Navigate browser to URL | OBSERVE |
| `forge_browser_click` | Click a browser element | OBSERVE |
| `forge_browser_type` | Type text into browser element | OBSERVE |
| `forge_browser_screenshot` | Take browser screenshot | OBSERVE |
| `forge_browser_extract_text` | Extract text from browser page | OBSERVE |
| `forge_browser_evaluate_js` | Evaluate JS in browser context | OBSERVE |
| `forge_github_search_code` | Search GitHub code | OBSERVE |
| `forge_github_search_repos` | Search GitHub repositories | OBSERVE |
| `forge_github_get_file` | Read file from GitHub | OBSERVE |
| `forge_github_create_or_update_file` | Create/update file on GitHub | MUTATE |
| `forge_github_create_issue` | Create GitHub issue | MUTATE |
| `forge_github_create_pull_request` | Create GitHub pull request | MUTATE |
| `forge_worktree` | Local git physics sensor | OBSERVE |
| `forge_netdata_alarms` | Read Netdata alarms | OBSERVE |
| `forge_netdata_metrics` | Read Netdata chart data | OBSERVE |
| `forge_minimax_search` | Search web via MiniMax | OBSERVE |

### Forge8 Execution Verbs

| Tool | Description |
|------|-------------|
| `forge_synthesize` | Generate code from intent |
| `forge_stage` | Stage artifact for execution |
| `forge_sandbox_run` | Run in sandbox |
| `forge_scar_scan` | Scan for scar patterns |
| `forge_skillstore_sync` | Sync to skillstore |
| `forge_tier_bind` | Bind to trust tier |
| `forge_docket_prep` | Prepare execution docket |
| `forge_execute` | Execute with governance |

### Infrastructure Tools

| Tool | Description |
|------|-------------|
| `forge_shell` | Canonical governed shell execution |
| `forge_shell_dryrun` | Preview shell command without executing |
| `forge_shell_status` | Shell subsystem health |
| `forge_shell_ledger` | Query ArifSeal hash-chain ledger |
| `forge_shell_alert_history` | View ArifJudge alert history |
| `forge_journalctl` | Query systemd journal logs (read-only, PII-redacted) |
| `forge_vps_ports` | Machine Constitution port registry |
| `forge_vps_services` | Machine Constitution service registry |
| `forge_vps_cron` | Machine Constitution cron registry |
| `forge_security_drift_scan` | Production security telemetry |

### Governance Tools

| Tool | Description |
|------|-------------|
| `forge_session_init` | Constitutional session ignition (proxies to arifOS) |
| `forge_health_check` | A-FORGE server health |
| `forge_approve` | Refuses approval — routes to arifOS |
| `forge_judge_proxy` | Proxy to arifOS constitutional judge |
| `forge_transfer_confirm` | Transfer funds with human confirmation |
| `forge_send_confirm` | Send data with human confirmation |
| `forge_wealth` | Route to WEALTH capital intelligence |
| `forge_kernel` | Constitutional kernel proxy |
| `forge_chart` | Agentic charting + quantum eureka discovery |
| `forge_probe` | Probe web site or cockpit surface |
| `forge_receipt_draft` | Draft structured compliance receipt |
| `forge_policy` | Governed MCP Policy Engine |

### Parallel/Agent Tools

| Tool | Description |
|------|-------------|
| `forge_parallel` | Spawn N concurrent A2A tasks |
| `forge_parallel_status` | Query parallel task group status |
| `forge_parallel_cancel` | Cancel running agents in group |
| `forge_parallel_list` | List all task groups |
| `forge_agent` | Agent identity management |
| `forge_lease` | Lease lifecycle |
| `forge_registry_status` | Full A-FORGE tool registry |
| `forge_fingerprint_check` | Compute/verify tool fingerprints |
| `forge_isomorphism_check` | J-space manifold stability check |
| `forge_job` | Background job system |
| `forge_status` | Active execution state |
| `forge_abort` | Safe stop + rollback |

### Surface Guard Tools

| Tool | Description |
|------|-------------|
| `forge_surface_guard` | MCP Surface Guard — schema fingerprinting + drift detection |
| `forge_surface_audit` | Audit MCP tool surface |
| `forge_runtime_verify` | Verify runtime consistency |
| `forge_verify_timeline` | Verify timeline claims |
| `forge_cool_drift` | Emit COOLING_RECEIPT with convergence signal |
| `forge_cool_pattern` | Emit COOLING_RECEIPT from failure recurrence |
| `forge_document_ingest` | Document ingest |

---

## 3. GEOX (Port 8081) — Earth Intelligence

**Status:** ✅ Healthy | **Protocol:** SSE (text/event-stream required)

### Public Tools (14 canonical after ZEN-14 consolidation)

| Tool | Domain | Axis | Description |
|------|--------|------|-------------|
| `geox_well_ingest` | earth.well | observe | Load well log data from LAS, SEG-Y, DST, deviation, or tops files |
| `geox_petrophysics` | earth.petrophysics | reason | Unified petrophysics: Vsh, porosity, Sw, permeability, net pay, LEM inference, QC |
| `geox_seismic_ingest` | earth.seismic | observe | SEG-Y I/O, header inspection, export |
| `geox_seismic_compute` | earth.seismic | compute | Seismic computation: forward model, well tie, attributes, wavelet extraction, inversion |
| `geox_seismic_interpret` | earth.seismic | reason | Unified seismic interpretation: horizon/fault picking, RSI pipeline, vision, contrast detection |
| `geox_subsurface_model` | earth.model | reason | Subsurface modeling |
| `geox_basin` | earth.basin | reason | Basin analysis |
| `geox_sequence` | earth.sequence | reason | Sequence stratigraphy |
| `geox_geomechanics` | earth.geomechanics | reason | Geomechanical analysis |
| `geox_deep_time_state` | earth.time | reason | Deep time state |
| `geox_claim` | earth.claim | verify | Claim lifecycle |
| `geox_prospect` | earth.prospect | judge | Prospect evaluation |
| `geox_gravmag_studio` | earth.gravmag | compute | Gravity/magnetic studio |
| `geox_well_desk` | earth.well | observe | Well desk |
| `geox_surface_status` | earth.status | observe | Surface status |
| `geox_evidence` | earth.evidence | verify | Evidence management |

### Additional Public Tools

| Tool | Description |
|------|-------------|
| `geox_basin_backstrip` | Basin backstripping |
| `geox_sediment_mass_balance` | Sediment mass balance |
| `geox_thermal_maturity_history` | Thermal maturity history |
| `geox_claim_graph_evaluate` | Claim graph evaluation |
| `geox_falsify` | Falsification testing |
| `geox_contradiction_scan` | Contradiction scanning |
| `geox_lem_predict` | LEM prediction |
| `geox_to_wealth_bridge` | GEOX→WEALTH bridge |
| `geox_well_tie_compute` | Well tie computation |
| `geox_wealth_bridge_run` | Wealth bridge execution |
| `geox_doctrine` | GEOX doctrine |

### EGS (Earth Grounding System) Tools

| Tool | Description |
|------|-------------|
| `geox_egs_query_entity` | Query earth graph entities |
| `geox_egs_query_claim` | Query claims |
| `geox_egs_query_uncertainty` | Query uncertainty |
| `geox_egs_query_provenance` | Query provenance |
| `geox_egs_claim_create` | Create claim |
| `geox_egs_claim_challenge` | Challenge claim |
| `geox_egs_evidence_attach` | Attach evidence |
| `geox_egs_evidence_reason` | Evidence reasoning |
| `geox_egs_seismic_compute` | Seismic computation (deprecated → geox_seismic_compute) |
| `geox_egs_rock_physics` | Rock physics |
| `geox_egs_data_qc_bundle` | Data QC bundle |
| `geox_egs_scenario_audit` | Scenario audit |

### Ghost Tools (Archived — require F13 SOVEREIGN ack to reactivate)

- `geox_3d_model`, `geox_3d_model_build`, `geox_atlas`, `geox_bid_round_screener`
- `geox_biostrat_nn_age`, `geox_biostrat_ruling_check`, `geox_cognitive_rank_hypotheses`
- `geox_forbidden_claims_scan`, `geox_geological_cognition_run`, `geox_macrostrat_calibrate`
- `geox_map_export_package`, `geox_panel_d_render`, `geox_panel_d_render_mcp`
- `geox_physical_reality_interpret`, `geox_render_audit`, `geox_rsi_interpret`
- `geox_segy_audit`, `geox_segy_trace_audit`, `geox_seismic_cognition`, `geox_well_desurvey`

---

## 4. WEALTH (Port 18082) — Capital Intelligence

**Status:** ✅ Healthy | **Protocol:** SSE (text/event-stream required)

### Canonical Tools (7 mode-dispatched)

| Tool | Description | Modes |
|------|-------------|-------|
| `capital_primitive` | Deductive capital math primitives | npv, irr, emv, evoi, mc, kelly, markowitz, robust, chance_constrained, two_stage |
| `capital_health` | Capital health assessment | health, vitals, diagnosis |
| `capital_diagnose` | Capital diagnosis | diagnose, analyze, recommend |
| `capital_wisdom` | Capital wisdom | wisdom, insight, lesson |
| `capital_market` | Market intelligence | market, stock, sector, macro |
| `capital_ledger` | Capital ledger | ledger, transaction, audit |
| `capital_registry` | Capital registry | registry, list, search |
| `capital_entropy` | Capital entropy | entropy, drift, stability |

### Institutional Tools

| Tool | Description |
|------|-------------|
| `wealth_institutional_stress_index` | Institutional stress index |
| `wealth_cascade_model` | Cascade model |
| `wealth_governance_capacity` | Governance capacity |
| `wealth_external_exploitation_detect` | External exploitation detection |

### Resource/Info Tools

| Tool | Description |
|------|-------------|
| `wealth_schema` | WEALTH schema |
| `wealth_tools_registry` | Tools registry |
| `wealth_prompts_index` | Prompts index |
| `wealth_domains_index` | Domains index |
| `wealth_runtime_policy` | Runtime policy |
| `wealth_canon_002_human_law` | Canon 002: Human Law |
| `wealth_glossary` | Glossary |
| `wealth_federation_contract` | Federation contract |
| `wealth_health` | Health check |
| `wealth_reality_context` | Reality context |
| `wealth_market_sources` | Market sources |
| `wealth_risk_thresholds` | Risk thresholds |
| `wealth_affordance_contracts` | Affordance contracts |
| `wealth_handoff_arifos_schema` | Handoff to arifOS schema |
| `wealth_replay_receipt_schema` | Replay receipt schema |

### Loop Tools

| Tool | Description |
|------|-------------|
| `wealth_reality_intake_loop` | Reality intake loop |
| `wealth_capital_diagnosis_loop` | Capital diagnosis loop |
| `wealth_risk_downside_loop` | Risk downside loop |
| `wealth_market_reality_loop` | Market reality loop |
| `wealth_allocation_judgment_loop` | Allocation judgment loop |
| `wealth_institutional_power_loop` | Institutional power loop |
| `wealth_arifos_handoff_loop` | arifOS handoff loop |

---

## 5. WELL (Port 18083) — Vitality Guard

**Status:** ✅ Healthy | **Protocol:** SSE (text/event-stream required)

### Public Tools

| Tool | Description |
|------|-------------|
| `well_health_check` | Health check |
| `well_state` | Current state |
| `well_log` | Log entry |
| `well_check_floors` | Check constitutional floors |
| `well_log_state` | Log state |
| `well_get_readiness` | Get readiness |
| `well_check_floor` | Check specific floor |
| `well_list_log` | List log entries |
| `well_seal_vault` | Seal to vault |
| `well_trend_analysis` | Trend analysis |
| `well_bandwidth_recommendation` | Bandwidth recommendation |
| `well_recovery_protocol` | Recovery protocol |
| `well_niat_check` | Niat (intention) check |

---

## 6. Naming Issues Identified (Claude Feedback)

### Canonical Stage Codes (arifOS Kernel Pipeline)

| Stage | Code | Tool | Description |
|-------|------|------|-------------|
| 000 | INIT | `arif_init` | Session ignition |
| 111 | OBSERVE | `arif_observe` | Sense reality |
| 333 | MIND | `arif_think` | Structured reasoning |
| 444 | ROUTE | `arif_route` | Intent router |
| 555 | MEMORY | `arif_memory` | Memory governor |
| 666 | HEART | `arif_heart_critique` | Ethical/risk critique |
| 777 | FORGE | `arif_forge` | Execution gate |
| 888 | JUDGE | `arif_judge` | Constitutional verdict |
| 999 | SEAL | `arif_seal` | VAULT999 immutable append |

### Issue 1: Numbering Inconsistency — FIXED 2026-07-18
- **arif_judge** stage was listed as 666 in this map — WRONG.
- **Kernel source** (`tools.py`) uses `888_JUDGE` for judge, `666_HEART` for heart_critique.
- **Canonical stage codes:** 000=init, 111=observe, 333=think, 444=route, 555=memory, 666=heart_critique, 777=forge, 888=judge, 999=seal.
- **Fix applied:** `arif_judge` stage corrected from 666 → 888. 666 belongs to `arif_heart_critique`.

### Issue 2: WEALTH Dual Prefix — OPEN
- `capital_*` and `wealth_*` coexist in WEALTH
- `capital_primitive` is opaque — should be `capital_compute` or `wealth_capital_compute` (verb+object per P3)
- **Fix:** Standardize on `wealth_*` prefix. Rename `capital_primitive` → `wealth_capital_compute`.

### Issue 3: WELL vs Wells Collision — REJECTED 2026-07-18
- `well_registry_status` (WELL organ) vs `geox_well_desk`/`geox_well_ingest` (GEOX organ)
- **Sovereign ruling:** `well_*` is organ prefix (consistent with `geox_*`, `forge_*`, `arif_*`). "Well" in geoscience = borehole; "Well" in organ = vitality. Domain overlap, not naming collision. `arif_route` scopes by organ.
- **No rename.** Fix routing discipline instead.

### Issue 4: GEOX Mega-Tools Overlap
- `geox_seismic_compute` contains modes (ingest, interpret, tengok, agak)
- `geox_seismic_ingest` and `geox_seismic_interpret` also exist as standalone tools
- **Fix:** Consolidate into mode-dispatched tools OR remove standalone duplicates.

### Issue 5: Description Bugs
- Several GEOX descriptions have generation bugs ("Use when: Use when you need basin evidence")
- `lem_predict` is an unexpanded acronym
- **Fix:** Audit and fix all descriptions.

### Issue 6: Duplicate WEALTH Server — FALSE POSITIVE 2026-07-18
- Only ONE entry in opencode.json (`wealth`), ONE service (`wealth-organ.service`), ONE port (18082).
- Map label "WEALTH" vs "WEALTH MCP" is documentation artifact, not actual duplicate server.
- **No fix needed.** Clean up map labels if desired.

---

## 7. Prompts & Resources

### arifOS
- **Prompts:** 0 (none registered)
- **Resources:** 23 (see §1 above)

### A-FORGE
- **Prompts:** 0 (none registered)
- **Resources:** 0 (none registered)

### GEOX
- **Prompts:** 0 (none registered)
- **Resources:** Requires SSE transport — not enumerated

### WEALTH
- **Prompts:** 5 (local files)
  - `wealth_intake.md` — Intake prompt
  - `wealth_institutional_power.md` — Institutional power
  - `wealth_arifos_handoff.md` — arifOS handoff
  - `wealth_market_reality.md` — Market reality
  - `wealth_capital_diagnosis.md` — Capital diagnosis
- **Resources:** Requires SSE transport — not enumerated

### WELL
- **Prompts:** 0 (none registered)
- **Resources:** Requires SSE transport — not enumerated

### A-FORGE (docs/prompts/)
- `geox-eureka-zahid-forge-brief.md` — GEOX Eureka Zahid forge brief
- `research-intelligence-machine.md` — Research intelligence machine

---

## 8. Tool Count Summary (Verified 2026-07-18)

| Organ | Map Count | Live Count | Status |
|-------|-----------|------------|--------|
| arifOS | 8 public | 8 | ✅ verified |
| A-FORGE | 111 (health endpoint) | ~80 (69 MCP files + 11 core.ts) | ⚠️ delta -31 |
| GEOX | 14+12=26 | 58 active (78 manifest - 20 ghost) | ⚠️ delta +32 |
| WEALTH | 8+4=12 | 12 | ✅ verified |
| WELL | 13 | 89 | ⚠️ delta +76 |
| **Total** | **170** | **~247** | |

**Notes:**
- A-FORGE health endpoint reports 111 but MCP files register ~80. Difference may be session-required tools not in stateless count.
- GEOX has 78 tools in manifest, 20 archived as ghost (F13 ack required), 58 active surface.
- WELL has 89 tools (not 13 as initially counted). Initial count only captured @mcp.tool decorators, not all registered tools.

### Description Quality Audit

**Result:** Zero "Use when: Use when" generation bugs found across all organs. Clean.

### Cross-Organ Semantic Overlap

| Overlap | Tools | Assessment |
|---------|-------|------------|
| Prediction/Prospect | `forge_predict` (A-FORGE), `geox_prospect` (GEOX) | Acceptable — different domains (simulation vs geology) |
| Health/Status | `arif_health`, `forge_health_check`, `geox_surface_status`, `wealth_health`, `well_health_check` | Acceptable — each organ owns its health |
| Registry | `forge_registry`, `forge_registry_status` (A-FORGE) | Acceptable — A-FORGE owns skill registry |
| Seal/Vault | `arif_seal` (VAULT999), `forge_seal` (skill seal), `well_seal_vault` (well state) | Acceptable — different scopes |

**Note:** Cross-organ overlap is acceptable when:
1. Each organ owns its domain (governance, engineering, earth, capital, vitality)
2. Agent routing uses organ prefix, not semantic matching
3. arif_route dispatches by intent, not by tool name similarity

---

## 9. Recommended Rename Map (Sovereign Feedback Applied)

### Issue 1: arif_judge 666 vs 888 — FIX NOW
- **Action:** Standardize stage_code=666 in metadata, authority_level=888 in description
- **Blast:** Zero — label alignment only, no code change
- **Rule:** Tool name = stage code. Authority lane = metadata.

### Issue 2: WEALTH dual prefix — T2 (Medium blast)
- **Action:** Keep `capital_*` as internal, expose `wealth_*` as canonical public
- **Rename:** `capital_primitive` → `wealth_capital_compute` (verb + object, P3 compliant)
- **Alias window:** 30 days — old names emit deprecation warnings
- **CI:** Namespace lint rejects `capital_*` on public wire after alias window

### Issue 3: WELL vs geox_well_* — REJECT rename
- **Sovereign decision:** `well_*` stays. Organ prefix consistency > semantic collision.
- **Fix:** Ensure agent routing uses organ prefix (arif_route), not semantic matching on "well"
- **Rule:** `well_*` = vitality organ. `geox_well_*` = borehole data. Two organs, two domains.

### Issue 4: GEOX seismic overlap — T3 (Low blast)
- **Action:** Audit whether `geox_seismic_compute` modes duplicate standalone tools
- **If yes:** Remove standalone duplicates, keep mode-dispatched tool
- **If no:** Document why both exist

### Issue 5: Description bugs — T1 (Zero blast, immediate fix)
- **Status:** Zero "Use when: Use when" bugs found. Clean.
- **Action:** None needed.

### Issue 6: Duplicate WEALTH server — FIX NOW
- **Action:** Remove "WEALTH MCP" duplicate connection
- **Blast:** Zero — just connection cleanup

### Migration Shape (Perplexity guidance)
1. **Layer 1: Canonical registry** — one canonical name per public tool, aliases deprecated
2. **Layer 2: Compatibility shim** — old names forward to canonical with deprecation warnings
3. **Layer 3: CI audit** — phantom names, duplicate exposures, description lint, namespace collisions

---

*Forged 2026-07-18 by AAA Control Plane. DITEMPA BUKAN DIBERI.*
