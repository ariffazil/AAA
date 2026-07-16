# MCP TOOL MANIFEST — All 7 Federation Organs

> **DITEMPA BUKAN DIBERI** — Forged, Not Given.
> **Canonical reference:** Live `tools/list` + `/health` endpoints on each organ.
> **Truth rule:** Probe beats prose. This manifest is a snapshot; verify via `tools/list`.
> **Last verified:** 2026-07-16

---

## Contents

1. [arifOS — Constitutional Kernel (:8088)](#1-arifos--constitutional-kernel-8088)
2. [GEOX — Earth Intelligence (:8081)](#2-geox--earth-intelligence-8081)
3. [WEALTH — Capital Intelligence (:18082)](#3-wealth--capital-intelligence-18082)
4. [WELL — Human Readiness (:18083)](#4-well--human-readiness-18083)
5. [AAA — Control Plane (:3001)](#5-aaa--control-plane-3001)
6. [A-FORGE — Execution Shell (:7071/:7072)](#6-a-forge--execution-shell-70717072)
7. [VAULT999 — Immutable Ledger (:8100/:5001)](#7-vault999--immutable-ledger-8100)
8. [Federation Summary Table](#8-federation-summary-table)

---

## 1. arifOS — Constitutional Kernel (:8088)

| Field | Value |
|-------|-------|
| **Port** | 8088 |
| **Transport** | Streamable HTTP (MCP v2025-11-25) |
| **Protocol** | JSON-RPC 2.0 + MCP |
| **Total public tools** | 8 |
| **Total internal tools** | 25 (canonical superset with 17 named kernel verbs) |
| **Health endpoint** | `GET /health` |
| **Tool discovery** | `POST /mcp` with `{"method":"tools/list"}` |
| **Affordance manifest** | `GET /tools.json` |
| **Floor gate** | F1–F13 all active; enforcement varies per tool |

### Public MCP Surface (8 tools)

| # | Tool | Modes | Description | Action Class | Floor Gate |
|---|------|-------|-------------|-------------|------------|
| 1 | `arif_init` | ping/light/init/resume/validate/canary/preflight/triage/epoch_open/epoch_seal | KERNEL 000 — Session ignition. Binds actor, floors, audit. Without session_id, caller is OBSERVE_ONLY. | OBSERVE | L10, L11 |
| 2 | `arif_observe` | search/fetch/hybrid_discovery/ingest/compass/atlas/entropy_dS/vitals | KERNEL 111 — Sense reality into evidence. Web/URL/ingest/vitals. Not reasoning or judgment. | OBSERVE | L02, L03, L05, L12 |
| 3 | `arif_think` | reason/reflect/verify/axioms/plan/plan_review/plan_approve/refactor_plan/metabolize/simulate | KERNEL 333 — Mind. Structured reasoning under F2/F7. Not chat, not verdict. | OBSERVE | L02, L07, L09 |
| 4 | `arif_route` | intent→organ dispatch | KERNEL 444 — Intent→organ router. Default path to GEOX/WEALTH/WELL/A-FORGE. | OBSERVE | L04 |
| 5 | `arif_memory` | recall/inspect/attest/remember/promote/revise/forget/audit | KERNEL memory governor — L1–L6 under F1/F2/F4/F11. Not a free notepad. | OBSERVE | L01, L02, L04, L11 |
| 6 | `arif_judge` | constitutional verdict | KERNEL 888 — Constitutional verdict. Only organ that SEAL/HOLD/SABAR/VOIDs. Requires actor, intent, domain, reversibility, blast radius. | MUTATE | L01, L11, L13 |
| 7 | `arif_forge` | dry_run/engineer/query/write/generate/commit/recall | KERNEL 777 — Execution gate via A-FORGE. Mutates only after arif_judge SEAL + lease/chain IDs. | MUTATE | L01, L11, L13 |
| 8 | `arif_seal` | seal/verify/ledger/changelog/audit | KERNEL 999 — VAULT999 immutable append. Irreversible civilizational memory. Requires `ack_irreversible`. | IRREVERSIBLE | L01, L11, L13 |

### Internal Kernel Verbs (17 additional — not on public wire)

| # | Tool | Stage | Floor Gate | Exposed |
|---|------|-------|------------|---------|
| 1 | `arif_act` | 777 (AGI) | L01, L11, L13 | Alias for arif_forge |
| 2 | `arif_bridge_connect` | 444 (AGI) | L01, L11, L10 | Internal only |
| 3 | `arif_challenge` | 000 (AGI) | L01, L02, L11, L12 | Ed25519 identity nonce |
| 4 | `arif_compose` | 888 (AGI) | L02, L04, L06, L09 | Final human-facing output |
| 5 | `arif_consequence_trace` | 111 (AGI) | L01, L06, L11 | Decision trace |
| 6 | `arif_correction_probe` | 666 (AGI) | L01, L02, L11 | Correction challenge |
| 7 | `arif_critique` | 555 (ASI) | L05, L06, L09 | Ethical/dignity/risk stress |
| 8 | `arif_entropy_observe` | 111 (AGI) | L09, L02, L11 | Entropy observation |
| 9 | `arif_entropy_route` | 444 (AGI) | L04 | Domain routing |
| 10 | `arif_fetch` | 111 (AGI) | L02, L03, L05, L12 | URL fetch + evidence |
| 11 | `arif_j_gate` | 666 (AGI) | L01, L13, L09 | J-state→action posture |
| 12 | `arif_j_state_assess` | 666 (AGI) | L09, L02, L04 | Judgment-integrity map |
| 13 | `arif_judge_deliberate` | 666 (ASI) | L01, L11, L13 | Nuanced deliberation |
| 14 | `arif_kernel_intercept` | 666 (ASI) | L13 | Brutalist interceptor |
| 15 | `arif_measure` | 111 (AGI) | L02, L04 | Runtime health only |
| 16 | `arif_triage` | 000 (AGI) | L04, L10 | DEPRECATED — use arif_init |
| 17 | `arif_verify` | — | — | Ed25519 signature verify |

### Key Tool Detail — arif_judge

```
Input:    { actor, intent, domain, reversibility_level, blast_radius,
            evidence[], epistemic_state, authority_token }
Output:   { verdict: "SEAL"|"HOLD"|"SABAR"|"VOID",
            receipts[], next_safe_action, floor_violations[] }
Gate:     F1 AMANAH (reversibility), F11 AUDIT, F13 SOVEREIGN
Blast:    FEDERATION-wide when SEAL'd; irreversible action
```

### Key Tool Detail — arif_seal

```
Input:    { payload, mode, witness_type, constitutional_chain_id,
            judge_state_hash, actor_signature, nonce }
Output:   { receipt_id, seq, hash, chain_head }
Gate:     F1 (irreversible), F11 (audit), F13 (sovereign)
Blast:    IRREVERSIBLE — permanent civilizational memory
```

---

## 2. GEOX — Earth Intelligence (:8081)

| Field | Value |
|-------|-------|
| **Port** | 8081 |
| **Transport** | Streamable HTTP (MCP) |
| **Protocol** | JSON-RPC 2.0 + MCP |
| **Total tools** | 15 |
| **Health endpoint** | `GET /health` |
| **Tool discovery** | `POST /mcp` tools/list (session required) |
| **Domain law** | NATURAL_LAW |
| **Floor gate** | F2 (evidence), F9 (anti-hantu), F11 (audit) — organ-level |
| **Tool prefix** | `geox_` |

### Canonical Tools (15)

| # | Tool | Modes | Description | Action Class | Input Summary |
|---|------|-------|-------------|-------------|--------------|
| 1 | `geox_basin` | profile/resolve/macrostrat/backstrip/mass_balance/thermal/reconstruct/rift | Unified basin intelligence. Profile, 2D backstripping, mass balance, thermal maturity, tectonic reconstruction. | OBSERVE | basin_name, lat, lng, age_ma, macrostrat_mode |
| 2 | `geox_claim` | create/validate/challenge/seal/evidence/consequence/optionality/cascade/feedback/truth | Unified claim lifecycle. Creates, validates, challenges geological claims with evidence gates. | OBSERVE | claim_text, truth_class, evidence_ids, alternatives |
| 3 | `geox_deep_time_state` | GPTS/CO2/sea_level/temperature/paleogeography | Earth State Vector through deep time. | OBSERVE | age_ma, period, query, biozone |
| 4 | `geox_geomechanics` | derive_moduli/gradients/stress_polygon | Bulk/shear/Young modulus, Poisson ratio, AI, stress polygon. | OBSERVE | depth_m, Sv, Pp, rho |
| 5 | `geox_gravmag_studio` | open/screen | Gravity/magnetic forward modeling and screening. | OBSERVE | survey_type, prisms, magnetization |
| 6 | `geox_petrophysics` | generate/verify/lem_inference/stoip_feed/qc | Vsh, porosity, Sw, permeability, net pay, LEM inference, QC. | OBSERVE | GR, rho, Rt, Rw, Vsh/Phi/Sw cutoffs |
| 7 | `geox_prospect` | screen/evaluate | Prospect evaluation: volumetrics, POS, EVOI, risk assessment. | OBSERVE | prospect_ref, evidence_refs, verdict |
| 8 | `geox_seismic_compute` | synthetic/well_tie/time_depth/anomalous_contrast/attribute/inversion/ingest | Unified seismic computation: forward models, well-tie, AVO, PINN inversion. | OBSERVE | mode, wavelet, vp, rho, depth |
| 9 | `geox_seismic_ingest` | inspect_segy/write_header/export | SEG-Y I/O, header inspection, export. | OBSERVE | volume_ref, output_path, text_header |
| 10 | `geox_seismic_interpret` | horizon_contrast/fault_sticks/volume_frame/blend/rsi/vision | Unified seismic interpretation: horizon/fault picking, RSI pipeline, vision. | OBSERVE | source_uri, volume_ref, horizon_query |
| 11 | `geox_sequence` | correlation/biostrat_parse/biostrat_falsify | Unified stratigraphy: sequence analysis, biostrat parsing, falsification. | OBSERVE | worklow, zone_top/base, depo_env |
| 12 | `geox_subsurface_model` | joint_inversion/gravity_forward/magnetic_forward/mt_forward | Subsurface model building: joint inversion, potential fields, MT. | OBSERVE | survey_type, prisms, layers |
| 13 | `geox_surface_status` | registry | Federation-standard registry probe. Tool discovery and health. | OBSERVE | mode |
| 14 | `geox_well_desk` | open/publish/render | Well desk: interactive view, publish rendered panel, render well panel. | OBSERVE | well_id, curves, depth range |
| 15 | `geox_well_ingest` | auto/LAS/SEG-Y/DST/deviation/tops | Load well log data from LAS, SEG-Y, DST, deviation, tops. Auto-detects format. | OBSERVE | source_uri, well_id, standardize_curves |

### Key Tool Detail — geox_seismic_compute

```
Input:    { mode, wavelet_type, wavelet_freq, vp[], rho[], depth[],
            reflectivity[], well_id, output_format }
Output:   { synthetic_trace[], correlation_score, time_depth_pairs[],
            anomalous_contrast[], attributes{} }
Gate:     F2 (OBS/DER/INT/SPEC labels), F9 (anti-hallucination)
Blast:    SESSION — read-only computation
```

---

## 3. WEALTH — Capital Intelligence (:18082)

| Field | Value |
|-------|-------|
| **Port** | 18082 |
| **Transport** | Streamable HTTP (MCP) |
| **Protocol** | JSON-RPC 2.0 + MCP |
| **Total tools** | 12 |
| **Health endpoint** | `GET /health` |
| **Tool discovery** | `POST /mcp` tools/list |
| **Domain law** | CAPITAL_LAW |
| **Floor gate** | F2 (evidence), F4 (clarity), F8 (genius), F11 (audit) |
| **Tool prefix** | `wealth_` |

### Canonical Tools (12)

| # | Tool | Modes | Description | Action Class | Input Summary |
|---|------|-------|-------------|-------------|--------------|
| 1 | `wealth_capital_health` | conservation/flow/runway/survival/fiscal_breakeven/confluence/asymmetry | Financial health metrics. Net worth, cash flow, runway, burn rate, breakeven oil price. | OBSERVE | assets[], liabilities[], income[], expenses[] |
| 2 | `wealth_capital_primitive` | npv/irr/emv/evoi/mc/kelly/markowitz/robust/chance_constrained/two_stage | Deductive capital math. Pure computation — no inference. Golden-tested. | OBSERVE | cash_flows, discount_rate, outcomes, probabilities |
| 3 | `wealth_capital_wisdom` | wisdom/omni/epistemic | Capital wisdom synthesis. Evaluates proposals across dignity, sovereignty, resilience, optionality. Advisory only. | OBSERVE | proposal, capital_type, context |
| 4 | `wealth_capital_market` | fx/commodity/indicator/stock | Market data and stock analysis. Observational only. | OBSERVE | base, targets, commodity, indicator |
| 5 | `wealth_capital_entropy` | power_consequence_map/metric_purpose_audit/responsibility_ledger/trust_capital_decay | Capital and institutional entropy analysis. Measures information loss, consequence displacement. | OBSERVE | decision_makers, beneficiaries, cost_bearers |
| 6 | `wealth_capital_diagnose` | stress_index/governance_capacity/cascade_model/exploitation_detect/collapse_signature | Abductive institutional diagnostics. Inference from partial evidence. | OBSERVE | mode, domain_scope, payload |
| 7 | `wealth_capital_ledger` | query/write | VAULT999 immutable ledger access. Query read-only. Write requires ack_irreversible. | OBSERVE/MUTATE | query, asset_id, tx_type |
| 8 | `wealth_capital_registry` | status/schema/domains/health | WEALTH meta/introspection. Registry status, schema, domain index. | OBSERVE | mode |
| 9 | `wealth_wealth_institutional_stress_index` | — | Composite institutional stress index (0-1). Financial + governance + workforce + legal + exploitation. | OBSERVE | org_name, financial_signals, governance_signals |
| 10 | `wealth_wealth_governance_capacity` | — | Monitor board governance capacity relative to stress level. | OBSERVE | board_members[], committees[], stress_level |
| 11 | `wealth_wealth_external_exploitation_detect` | — | Detect "simulative neutral" counterparty behavior. | OBSERVE | counterparty_actions[], institution_state |
| 12 | `wealth_wealth_cascade_model` | — | Model feedback loops between institutional stress dimensions. | OBSERVE | timeline[], intervention_scenario |

### Key Tool Detail — wealth_capital_primitive

```
Input:    { mode: "npv"|"irr"|"emv"|"evoi"|"mc"|"kelly"|"markowitz",
            cash_flows[], discount_rate, outcomes[], probabilities[],
            simulations, risk_aversion }
Output:   { result, confidence_interval, sensitivity[] }
Gate:     F2 (deductive — no inference), F8 (simplest correct path)
Blast:    SESSION — pure compute, zero side effects
```

---

## 4. WELL — Human Readiness (:18083)

| Field | Value |
|-------|-------|
| **Port** | 18083 |
| **Transport** | Streamable HTTP (MCP) |
| **Protocol** | JSON-RPC 2.0 + MCP |
| **Total tools** | 27 (live count) |
| **Health endpoint** | `GET /health` |
| **Tool discovery** | `POST /mcp` tools/list |
| **Domain law** | SUBSTRATE_LAW |
| **Authority** | REFLECT_ONLY — never diagnostic |
| **Floor gate** | F2 (reflection), F6 (dignity), F9 (anti-hantu), F11 (audit) |
| **Tool prefix** | `well_` |

### Canonical Tools (27)

| # | Tool | Description | Action Class | Floor Gate |
|---|------|-------------|-------------|------------|
| 1 | `well_health_check` | WELL organ health with provenance and schema version. | OBSERVE | F2 |
| 2 | `well_medical_boundary` | Explicit non-diagnosis guard. Not a doctor/therapist/diagnostic authority. | OBSERVE | F6, F9 |
| 3 | `well_signal_coverage` | DREAM ENGINE: audit WELL's coverage of canonical human substrate signals. | OBSERVE | F2, F4 |
| 4 | `well_handoff_dignity_to_arifos` | Ω-WELL-FED-S12: handoff S12 signal → arifOS 888_JUDGE. | OBSERVE | F6, F11 |
| 5 | `well_handoff_livelihood_to_wealth` | Ω-WELL-FED-S13: handoff S13 signal → WEALTH for capital evidence. | OBSERVE | F6, F11 |
| 6 | `well_attest_to_kernel` | Ω-WELL-FED-ATTEST: active organ attestation → arifOS kernel. | OBSERVE | F11 |
| 7 | `well_classify_substrate` | Ω-WELL-01: substrate classification and boundary sensing. | OBSERVE | F2, F9 |
| 8 | `well_trace_lineage` | Ω-WELL-02: memory, trend, ledger, vault chain tracing. | OBSERVE | F2, F11 |
| 9 | `well_detect_boundary` | Ω-WELL-03: boundary detection across membrane, body, machine, federation. | OBSERVE | F6, F9 |
| 10 | `well_measure_gradient` | Ω-WELL-04: measure chemical, energy, pressure, attention, compute gradients. | OBSERVE | F2 |
| 11 | `well_assess_metabolism` | Ω-WELL-05: assess biological metabolism and system throughput. | OBSERVE | F9 |
| 12 | `well_assess_homeostasis` | Ω-WELL-06: assess regulation, stability, empathic balance. Fatigue mode accepts biometric overrides. | OBSERVE | F6, F9 |
| 13 | `well_check_repair` | Ω-WELL-07: check repair, recovery, resilience, forge cycle integrity. | OBSERVE | F1 |
| 14 | `well_validate_vitality` | Ω-WELL-08: validate vitality, readiness, NIAT. Floor compliance removed (arifOS adjudicates). | OBSERVE | F6 |
| 15 | `well_assess_livelihood` | Ω-WELL-09: assess human wellness, role, dignity, support, meaning. ZEN: voluntary vs imposed burden. | OBSERVE | F6 |
| 16 | `well_assess_reliability` | Ω-WELL-10: assess machine, tool, institution, operational reliability. | OBSERVE | F2, F10 |
| 17 | `well_compute_metabolic_flux` | Ω-WELL-10b: compute unified thermodynamic entropy rate (0.0-1.0). Triggers reallocation at >=0.65, hold at >=0.85. | OBSERVE | F2, F4 |
| 18 | `well_assess_sovereign_entropy` | Ω-WELL-SE: measure sovereign's resistance to behavioral modeling. High = unmodelable, safe. | OBSERVE | F10, F13 |
| 19 | `well_dark_geometry_mirror` | Ω-WELL-DG: mirror language and behavioral signals for dark geometry patterns. Content metabolism block. | OBSERVE | F6, F9 |
| 20 | `well_guard_dignity` | Ω-WELL-12: guard soul, personhood, meaning, symbolic boundaries. | OBSERVE | F6 |
| 21 | `well_registry_status` | WELL registry truth diagnostic. Live callable tests vs blueprint. | OBSERVE | F2, F4 |
| 22 | `well_classify_state` | Classify human psychological state from message. Polyvagal + SDT. REFLECT_ONLY. | OBSERVE | F6, F9 |
| 23 | `well_sabar_latency` | Ω-WELL-SL: measure temporal compression between stimulus and response. | OBSERVE | F6 |
| 24 | `well_trust_compression` | Ω-WELL-TC: detect narrowing trust patterns. All-or-nothing, universal threat. | OBSERVE | F6 |
| 25 | `well_niat_impact_mirror` | Ω-WELL-NIM: compare declared niat with acknowledged impact. | OBSERVE | F2, F6 |
| 26 | `well_correction_capacity` | Ω-WELL-CC: score observable correctability. | OBSERVE | F6 |
| 27 | `well_regulation_recovery` | Ω-WELL-RR: measure recovery after activation. | OBSERVE | F2 |

### Key Tool Detail — well_assess_homeostasis

```
Input:    { mode, sleep_hours, sleep_debt_days, cognitive_clarity,
            decision_fatigue, stress_load, hrv_status, emotional_state,
            chronic_fatigue, decision_class }
Output:   { homeostasis_verdict, readiness, vitality_index,
            restriction, signal }
Gate:     F6 (maruah — dignity first), F9 (anti-hantu — no consciousness)
Blast:    SESSION — reflect only, never diagnostic
```

---

## 5. AAA — Control Plane (:3001)

| Field | Value |
|-------|-------|
| **Port** | 3001 |
| **Transport** | HTTP (A2A v1.0.0) |
| **Protocol** | A2A JSON-RPC 2.0 + MCP |
| **Total tools** | A2A task lifecycle + agent card registry |
| **Health endpoint** | `GET /health` |
| **Tool discovery** | `GET /.well-known/agent.json`, `/a2a/discover` |
| **Domain** | A2A control plane, identity, cockpit display |
| **Floor gate** | F11 (audit), F4 (clarity) |
| **A2A version required** | `A2A-Version: 1.0` header |

### A2A Surface

| Resource/Endpoint | Description | Action Class | Gate |
|-------------------|-------------|-------------|------|
| `GET /.well-known/agent.json` | Federation agent card — canonical identity | OBSERVE | None |
| `GET /a2a/discover` | Agent discovery — returns all registered agent cards | OBSERVE | None |
| `GET /a2a/agent-cards/:id` | Individual agent card by ID | OBSERVE | None |
| `POST /a2a/tasks/send` | Submit a new A2A task | OBSERVE | F11 |
| `GET /a2a/tasks/:id` | Get task status and result | OBSERVE | None |
| `POST /a2a/tasks/:id/cancel` | Cancel a running task | MUTATE | F1 |
| `GET /a2a/tasks` | List tasks with optional status filter | OBSERVE | None |
| `POST /a2a/message/send` | Send message to an agent | OBSERVE | F11 |

### Agent Card Registry (8 registered agents)

| Agent ID | Class | Capabilities |
|----------|-------|-------------|
| `333-AGI` | AGI (C2) | Reasoning, execution, planning, tool orchestration |
| `555-ASI` | ASI (C2) | Memory, synthesis, ethical critique, knowledge graph |
| `888-APEX` | APEX (C1) | Constitutional verdicts, deliberation, judgment |
| `A-AUDIT` | Oversight (C2) | Anomaly detection, drift detection, post-seal sweep |
| `A-ARCHIVE` | Service (C2) | Vault operations, seal chain management |
| `OpenCode` | Forge worker (C2) | Code execution, file operations, federation tools |
| `OpenClaw` | Legacy (C3) | Reasoning engine (deprecated) |
| `Hermes` | ASI (C1) | Telegram conversational surface, media/creative routing |

### Key Resource Detail — Agent Card Schema

```json
{
  "agentId": "333-AGI",
  "name": "Delta MIND",
  "description": "Primary reasoning agent for arifOS federation",
  "url": "http://localhost:3001/a2a/agents/333-AGI",
  "capabilities": {
    "reasoning": true, "execution": true, "planning": true
  },
  "auth": { "schemes": [], "bearer": false },
  "defaultInputModes": ["text"],
  "defaultOutputModes": ["text"],
  "skills": ["kernel-bind", "observe-ground", "route-dispatch", "AGI-plan-dag"]
}
```

---

## 6. A-FORGE — Execution Shell (:7071/:7072)

| Field | Value |
|-------|-------|
| **Port** | 7071 (Express) / 7072 (MCP gateway) |
| **Transport** | Streamable HTTP (MCP), Stdio |
| **Protocol** | JSON-RPC 2.0 + MCP |
| **Total tools** | 109 (live count — 52 stateless) |
| **Health endpoint** | `GET /health` (:7071 and :7072) |
| **Tool discovery** | `POST /mcp` tools/list on :7072 |
| **Domain** | Execution shell — filesystem, shell, git, docker, vault, research, browser, governance |
| **Floor gate** | Tool-specific; governed by MCP Policy Engine + ArifJudge |
| **Tool prefix** | `forge_` |

### Tool Categories

#### Filesystem (8 tools)

| # | Tool | Description | Action Class | Gate |
|---|------|-------------|-------------|------|
| 1 | `forge_filesystem` | Canonical governed fs: read, write, patch, glob, grep, stat, tree, move, delete, restore | OBSERVE/MUTATE | F8 scoped |
| 2 | `forge_filesystem_read` | Read file / list directory. No session required. | OBSERVE | None |
| 3 | `forge_filesystem_write` | Create/overwrite file. F1 backup before overwrite. | MUTATE | F1 |
| 4 | `forge_filesystem_patch` | Surgical text replacement. Returns diff preview in dry_run. | MUTATE | F1 |
| 5 | `forge_filesystem_tree` | List directory tree structure. | OBSERVE | None |
| 6 | `forge_filesystem_search` | Search file contents by regex. | OBSERVE | None |
| 7 | `forge_filesystem_stat` | File/directory metadata including sha256 hash. | OBSERVE | None |
| 8 | `forge_filesystem_move` | Move file/directory. EXECUTE-class. | MUTATE | F1 |
| 9 | `forge_filesystem_delete` | Delete (quarantine by default). Hard delete = IRREVERSIBLE. | MUTATE | 888_HOLD |

#### Shell (5 tools)

| # | Tool | Description | Action Class | Gate |
|---|------|-------------|-------------|------|
| 1 | `forge_shell` | Canonical governed shell. Constitutional gate + hash-chain audit. DENY patterns hard-blocked. | MUTATE | F1, F11, ArifJudge |
| 2 | `forge_shell_dryrun` | Preview output WITHOUT executing. F1 AMANAH. | OBSERVE | None |
| 3 | `forge_shell_status` | Check subsystem health: ledger, judge patterns, defaults. | OBSERVE | None |
| 4 | `forge_shell_ledger` | Query ArifSeal hash-chain ledger. | OBSERVE | None |
| 5 | `forge_shell_alert_history` | View ArifJudge DENY/GATE/self-mod history. | OBSERVE | None |

#### Git & GitHub (12 tools)

| # | Tool | Description | Action Class | Gate |
|---|------|-------------|-------------|------|
| 1 | `forge_git` | Canonical git: status, diff, log, commit. Mutations floor-gated. | OBSERVE/MUTATE | F1 |
| 2 | `forge_git_commit` | Governed commit with optional pre-commit checks. | MUTATE | F1, F11 |
| 3 | `forge_worktree` | Local git physics sensor: branch, dirty state, conflicts, blast radius. | OBSERVE | None |
| 4 | `forge_github` | Canonical GitHub: search, pr. | OBSERVE | F11 |
| 5 | `forge_github_search_code` | Search GitHub code. | OBSERVE | None |
| 6 | `forge_github_search_repos` | Search GitHub repositories. | OBSERVE | None |
| 7 | `forge_github_get_file` | Read file from GitHub. | OBSERVE | None |
| 8 | `forge_github_create_or_update_file` | Create/update file on GitHub. | MUTATE | F11 |
| 9 | `forge_github_create_issue` | Create GitHub issue. | MUTATE | F11 |
| 10 | `forge_github_create_pull_request` | Create GitHub PR. | MUTATE | F11 |
| 11 | `forge_github_create_repository` | Create GitHub repository. | MUTATE | F11, F13 |
| 12 | `forge_fork_repository` | Fork a GitHub repo. | MUTATE | F11 |

#### Research & Fetch (8 tools)

| # | Tool | Description | Action Class | Gate |
|---|------|-------------|-------------|------|
| 1 | `forge_fetch` | Governed URL evidence + self-hosted SearxNG search. SSRF-protected. | OBSERVE | F2, F12 |
| 2 | `forge_fetch_url` | Fetch URL → markdown (Readability). | OBSERVE | F12 |
| 3 | `forge_fetch_json` | Fetch URL → JSON. | OBSERVE | F12 |
| 4 | `forge_fetch_metadata` | Fetch URL metadata (title, author, description). | OBSERVE | F12 |
| 5 | `forge_fetch_links` | Extract all links from URL. | OBSERVE | F12 |
| 6 | `forge_search` | Governed web search via Brave. | OBSERVE | None |
| 7 | `forge_research` | Governed research across web sources. | OBSERVE | None |
| 8 | `forge_docs_lookup` | Governed docs lookup via Context7. | OBSERVE | None |
| 9 | `forge_minimax_search` | Search web via MiniMax. | OBSERVE | None |

#### Browser (6 tools)

| # | Tool | Description | Action Class | Gate |
|---|------|-------------|-------------|------|
| 1 | `forge_browser_navigate` | Navigate browser to URL. | MUTATE | CONTEXT A/B |
| 2 | `forge_browser_click` | Click browser element. | MUTATE | CONTEXT A/B |
| 3 | `forge_browser_type` | Type text into element. | MUTATE | CONTEXT A/B |
| 4 | `forge_browser_screenshot` | Take browser screenshot. | OBSERVE | CONTEXT A/B |
| 5 | `forge_browser_extract_text` | Extract text from page. | OBSERVE | CONTEXT A/B |
| 6 | `forge_browser_evaluate_js` | Evaluate JS in browser context. | MUTATE | CONTEXT A/B |

#### Docker & VPS (7 tools)

| # | Tool | Description | Action Class | Gate |
|---|------|-------------|-------------|------|
| 1 | `forge_docker` | Canonical Docker: ps, logs, exec, images. Destructive ops excluded. | MUTATE | F1 |
| 2 | `forge_journalctl` | Query systemd journal (read-only, PII-redacted). | OBSERVE | F11 |
| 3 | `forge_vps_ports` | Machine Constitution port registry: scan/registry/assert. | OBSERVE | None |
| 4 | `forge_vps_services` | Machine Constitution service registry: scan/registry/assert. | OBSERVE | None |
| 5 | `forge_vps_cron` | Machine Constitution cron registry: scan/registry/assert. | OBSERVE | None |
| 6 | `forge_security_drift_scan` | Production security telemetry: ports, services, containers, cron. | OBSERVE | F2 |
| 7 | `forge_netdata_alarms` | Read Netdata alarms. | OBSERVE | None |
| 8 | `forge_netdata_metrics` | Read Netdata chart data. | OBSERVE | None |

#### Vault & Memory (8 tools)

| # | Tool | Description | Action Class | Gate |
|---|------|-------------|-------------|------|
| 1 | `forge_vault` | VAULT999 primitive: read, list, write, seal. | OBSERVE/MUTATE | F1, F11 |
| 2 | `forge_memory` | Canonical memory: recall. Reads VAULT999 local + API. | OBSERVE | F2 |
| 3 | `forge_seal` | Seal Tri-Witness validated skill → VAULT999. Irreversible. | IRREVERSIBLE | F3, F13 |
| 4 | `forge_receipt_draft` | Draft structured compliance receipt. | OBSERVE | F11 |
| 5 | `forge_scar` | APEX v36Ω scar metabolization: seal/list/consult failures. | OBSERVE/MUTATE | F1 |
| 6 | `forge_scar_scan` | Check artifact against SCAR database. | OBSERVE | F1 |
| 7 | `forge_stage` | Move artifact to quarantine staging. Immutable after staging. | MUTATE | F1 |
| 8 | `forge_skillstore_read` | Query artifact store with semantic search. | OBSERVE | None |
| 9 | `forge_skillstore_write` | Store artifact with provenance. | MUTATE | F1, F11 |

#### Governance & Security (15 tools)

| # | Tool | Description | Action Class | Gate |
|---|------|-------------|-------------|------|
| 1 | `forge_session_init` | Constitutional session ignition. Proxies to arifOS kernel. | OBSERVE | L10, L11 |
| 2 | `forge_judge_proxy` | Proxy forwarder to arifOS constitutional judge. | OBSERVE | F11 |
| 3 | `forge_approve` | Refuses approval — A-FORGE cannot self-authorize. | MUTATE | F13 |
| 4 | `forge_check_governance` | Constitutional governance check, delegates to arifOS. | OBSERVE | F1-F13 |
| 5 | `forge_heart_critique` | Risk/ethical review, delegates to arifOS 666 HEART. | OBSERVE | F5, F6 |
| 6 | `forge_witness` | APEX v36Ω tri-witness: W³ = ∛(Human × AI × External). | OBSERVE | F3 |
| 7 | `forge_evaluate` | APEX v36Ω evaluation: G = A·P·E·X·Φ, C_dark = A·(1-P)·(1-X). | OBSERVE | F8, F9 |
| 8 | `forge_register` | APEX v36Ω gated registration. | MUTATE | F8, F9, F11 |
| 9 | `forge_reality_loop` | Intent compiler: 7-stage state-tracking ledger. | OBSERVE/MUTATE | F1-F13 |
| 10 | `forge_policy` | Governed MCP Policy Engine. | OBSERVE/MUTATE | F1, F8, F11, F13 |
| 11 | `forge_lock` | Amanah/F1 lock primitive: acquire/release. | OBSERVE/MUTATE | F1 |
| 12 | `forge_send_confirm` | Send data with human confirmation via elicitation. | MUTATE | F13 |
| 13 | `forge_transfer_confirm` | Transfer funds with human confirmation. | MUTATE | F13 |
| 14 | `forge_scan` | Security scan file/directory for dangerous patterns. | OBSERVE | F12 |
| 15 | `forge_verify_timeline` | Verify timeline claims require ≥2 independent sources. | OBSERVE | F2 |

#### Execute & Pipeline (8 tools)

| # | Tool | Description | Action Class | Gate |
|---|------|-------------|-------------|------|
| 1 | `forge_execute` | Execution and motor cortex. Requires cc_id for mutations. | MUTATE | F1, F11 |
| 2 | `forge_execute_sealed` | Execute with VAULT999 seal. Fails without valid seal. | MUTATE | F1, F11, F13 |
| 3 | `forge_pipeline_run` | Autonomous intelligence pipeline: route → witness → compute → judge → seal. | MUTATE | F1, F11 |
| 4 | `forge_job` | Background job system: submit, status. | OBSERVE | F1 |
| 5 | `forge_abort` | Safe stop + rollback for running execution. | MUTATE | F1 |
| 6 | `forge_sandbox_run` | Execute staged artifact in isolated sandbox. | MUTATE | F1 |
| 7 | `forge_predict` | Pre-action simulation: GEOX/WEALTH forward models. | OBSERVE | F2 |
| 8 | `forge_parallel` | Spawn N concurrent A2A tasks + collect results. | OBSERVE | F1, F11 |

#### Registry & Agent (10 tools)

| # | Tool | Description | Action Class | Gate |
|---|------|-------------|-------------|------|
| 1 | `forge_agent` | Agent identity: register/status/list/kill. | OBSERVE/MUTATE | F11 |
| 2 | `forge_lease` | Lease lifecycle: request/status/revoke. arifOS mints. | OBSERVE/MUTATE | F1, F11 |
| 3 | `forge_registry` | Dynamic skill registry: list/get/scars/fingerprint/scan. | OBSERVE | F2 |
| 4 | `forge_registry_status` | Full registry: callable/blocked/degraded/drift status. | OBSERVE | None |
| 5 | `forge_status` | Active execution state: jobs, leases, agents. | OBSERVE | None |
| 6 | `forge_fingerprint_check` | Compute + verify tool fingerprints. | OBSERVE | F2 |
| 7 | `forge_tier_bind` | Set trust tier LOWER BOUND only (A-FORGE cannot promote). | OBSERVE/MUTATE | F8 |
| 8 | `forge_skill` | Dynamic tool forge. LLM generates new tool, HARAM-scanned, gated. | MUTATE | F8, F9, F13 |
| 9 | `forge_synthesize` | Create artifact from intent. Code → temp buffer only. | MUTATE | F1 |
| 10 | `forge_surface_audit` | Audit MCP tool surface vs affordances.yaml. | OBSERVE | F2 |
| 11 | `forge_surface_guard` | Schema fingerprinting + drift detection. | OBSERVE | F1, F2, F8, F11 |

#### Probe & Observability (8 tools)

| # | Tool | Description | Action Class | Gate |
|---|------|-------------|-------------|------|
| 1 | `forge_health_check` | A-FORGE health + constitutional genome status. | OBSERVE | None |
| 2 | `forge_probe` | Federation organ liveness: all 5 organs + latency. | OBSERVE | None |
| 3 | `forge_probe_site` | Probe web site / cockpit surface for resilience. | OBSERVE | None |
| 4 | `forge_runtime_verify` | Source commit vs wheel vs import path. | OBSERVE | F2 |
| 5 | `forge_isomorphism_check` | J-space manifold stability: GEOX ↔ arifOS isomorphism. | OBSERVE | F2 |
| 6 | `forge_entropy_sweep` | Measure workspace entropy (ΔS) across federation. | OBSERVE | F4 |
| 7 | `forge_cool_drift` | COOLING_RECEIPT with convergence signal. | OBSERVE | F11 |
| 8 | `forge_cool_pattern` | COOLING_RECEIPT from failure recurrence. | OBSERVE | F11 |
| 9 | `forge_chart` | Agentic charting + quantum eureka patterns. | OBSERVE | F2 |

#### Document Intelligence (1 tool)

| # | Tool | Description | Action Class | Gate |
|---|------|-------------|-------------|------|
| 1 | `forge_document_ingest` | Layout-first parsing: analyze/extract/chunk/compare. PDF + images + text. | OBSERVE | F2 |

#### Organ Bridges (2 tools)

| # | Tool | Description | Action Class | Gate |
|---|------|-------------|-------------|------|
| 1 | `forge_wealth` | Route to WEALTH capital intelligence organ. | OBSERVE | F2 |
| 2 | `forge_well` | WELL relay: state, readiness, floors, anchor. | OBSERVE | F6 |

#### Kernel Proxy (1 tool)

| # | Tool | Description | Action Class | Gate |
|---|------|-------------|-------------|------|
| 1 | `forge_kernel` | Constitutional kernel proxy → arifOS :8088/mcp. | OBSERVE/MUTATE | Per proxied tool |

### Key Tool Detail — forge_shell

```
Input:    { command, cwd, timeout }
Output:   { stdout, stderr, exit_code, sealed_ledger_entry }
Gate:     ArifJudge (constitutional gate + pattern matching),
          ArifSeal (hash-chain audit to VAULT999)
Blast:    SESSION to HOST — command execution with file/net impact
          DENY patterns are hard-blocked. GATE patterns require approval.
```

### Key Tool Detail — forge_execute

```
Input:    { task, mode, constitutional_chain_id, prediction_context,
            evidence_receipt }
Output:   { exit_code, artifacts[], receipts[] }
Gate:     F1 (reversibility check), F11 (audit), cc_id from arif_judge
Blast:    SESSION to FEDERATION — can touch multiple organs
```

---

## 7. VAULT999 — Immutable Ledger (:8100)

| Field | Value |
|-------|-------|
| **Port** | 8100 (vault999-api) |
| **Transport** | HTTP (FastAPI) |
| **Protocol** | REST + Supabase Postgres backend |
| **Total seals** | 298 (as of 2026-07-16) |
| **Health endpoint** | `GET /health` |
| **DSN** | Supabase Postgres (SSL required) |
| **Floor gate** | F1 (append-only), F2 (hash chain), F11 (audit) |
| **Access patterns** | Direct API + `forge_vault` + `arif_seal` |

### Operations

| Operation | Endpoint / Tool | Description | Action Class | Gate |
|-----------|----------------|-------------|-------------|------|
| Read | `forge_vault(mode=read)` / `GET /seals/:id` | Read seal entry by ID | OBSERVE | None |
| List | `forge_vault(mode=list)` / `GET /seals` | List recent seal entries | OBSERVE | None |
| Write | `forge_vault(mode=write)` | Write structured record | MUTATE | F1, F11 |
| Seal | `arif_seal` / `forge_vault(mode=seal)` | Append to hash chain | IRREVERSIBLE | F1, F11, F13 |
| Verify | `arif_seal(mode=verify)` | Verify chain integrity | OBSERVE | F2 |
| Chain | `arif_seal(mode=chain)` | Show chain head + seq | OBSERVE | None |
| Ledger | `arif_seal(mode=ledger)` | Query ledger entries | OBSERVE | F2 |

### Seal Chain Format

```json
{
  "seq": 9922,
  "hash": "sha256:3f5559ae13a1f08ecb9d6b54c5426a58f1ef0043d4c6e6f94bd3acede112baea",
  "epoch": "2026-07-15T02:10:21.354Z",
  "actor": "aaa-gateway",
  "verdict": "HOLD",
  "payload": {},
  "previous_hash": "sha256:..."
}
```

---

## 8. Federation Summary Table

| Organ | Port | Transport | Tools | Tool Prefix | Domain | Primary Gate | Discovery |
|-------|------|-----------|-------|-------------|--------|-------------|-----------|
| **arifOS** | 8088 | Streamable HTTP (MCP) | 8 public / 25 internal | `arif_` | Constitutional kernel | F1 (Amanah), F11 (Audit), F13 (Sovereign) | `POST /mcp` tools/list, `GET /tools.json` |
| **GEOX** | 8081 | Streamable HTTP (MCP) | 15 | `geox_` | Earth intelligence | F2 (Evidence), F9 (Anti-hantu) | `POST /mcp` tools/list (session) |
| **WEALTH** | 18082 | Streamable HTTP (MCP) | 12 | `wealth_` | Capital intelligence | F2 (Deductive), F4 (Clarity) | `POST /mcp` tools/list |
| **WELL** | 18083 | Streamable HTTP (MCP) | 27 | `well_` | Human readiness | F6 (Maruah), F9 (Anti-hantu) | `POST /mcp` tools/list |
| **AAA** | 3001 | HTTP (A2A v1.0) | 7 endpoints + 8 agent cards | `a2a/*` | Control plane | F11 (Audit), F4 (Clarity) | `GET /.well-known/agent.json`, `GET /a2a/discover` |
| **A-FORGE** | 7071/7072 | Streamable HTTP (MCP) + Stdio | 109 (52 stateless) | `forge_` | Execution shell | Per-tool: ArifJudge + ArifSeal | `POST /mcp` tools/list on :7072 |
| **VAULT999** | 8100 | HTTP (REST) + Supabase | 5 operations | `forge_vault`/`arif_seal` | Immutable ledger | F1 (Append-only), F11 (Audit) | `GET /health`, `GET /seals` |

### Federation Totals

| Metric | Value |
|--------|-------|
| **Total MCP tools** | ~200 (across all organs) |
| **Total A2A agents** | 8 registered in AAA |
| **Total seal chain entries** | 9,922 (as of 2026-07-16) |
| **MCP protocol versions supported** | 2025-11-25, 2025-03-26, 2024-11-05 |
| **Federation schema version** | 2.0.0 |
| **Constitutional floors** | F1–F13 (all active) |

### Tool Naming Convention

```
Prefix: <organ>_<domain>_<verb>
  arif_    → arifOS constitutional kernel
  geox_    → GEOX earth intelligence
  wealth_  → WEALTH capital intelligence
  well_    → WELL human readiness
  forge_   → A-FORGE execution shell
```

### Authority Ceilings

| Organ | Authority | Can self-authorize? |
|-------|-----------|-------------------|
| arifOS | JUDGE | No — judges only through F1-F13 |
| GEOX | COMPUTE | No — evidence only |
| WEALTH | COMPUTE | No — compute only |
| WELL | REFLECT_ONLY | No — reflects only |
| AAA | ROUTE | No — displays governed state |
| A-FORGE | EXECUTE | No — requires arif_judge SEAL + lease |
| VAULT999 | APPEND | No — immutable ledger |

### Blast Radius Classification

| Radius | Scope | Examples |
|--------|-------|---------|
| **SESSION** | Current agent session only | Reads, searches, observations |
| **ORGAN** | Single organ state | Write to organ registry, cache |
| **FEDERATION** | Cross-organ impact | Multi-organ pipeline, shared state |
| **HOST** | VPS-level impact | Shell command, filesystem, Docker |
| **IRREVERSIBLE** | Permanent state change | VAULT999 seal, production deploy |

### Floor Gate Legend

| Floor | Name | Application |
|-------|------|-------------|
| **F1** | AMANAH | Reversible-first. Backup before mutate. |
| **F2** | TRUTH | OBS/DER/INT/SPEC labels. Cap confidence 0.90. |
| **F3** | WITNESS | Tri-witness W³ for SEAL. |
| **F4** | CLARITY | ΔS ≤ 0. Leave workspace cleaner. |
| **F5** | PEACE² | De-escalate. Guard weakest. |
| **F6** | MARUAH | Dignity-first. ASEAN/MY context. |
| **F7** | HUMILITY | Declare unknowns. Cap confidence. |
| **F8** | GENIUS | Simplest correct path. |
| **F9** | ANTI-HANTU | No hallucination. No consciousness claims. |
| **F10** | ONTOLOGY | AI-only ontology. Substrate ≠ being. |
| **F11** | AUDIT | Every action leaves trace. |
| **F12** | INJECTION | Sanitize inputs. External ≠ authority. |
| **F13** | SOVEREIGN | Arif holds final veto. |

---

*Canonical MCP Tool Manifest for the arifOS Federation.*
*Generated from live `/health` and `tools/list` probes on all 7 organs.*
*Next verification: on organ restart or manifest publish.*
*DITEMPA BUKAN DIBERI — Forged, Not Given.*
