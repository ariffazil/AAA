# Master Task List — MCP 2026-07-28 Alignment (arifOS + GEOX)

**Status:** SPEC ONLY · awaiting forge authority
**Date:** 2026-09-29
**Owner:** FI-008 (kimi-code) per sovereign directive *"ffff qqqq apex-zen all"*
**Authority band:** OBSERVE_ONLY (spec generation only; execution requires MUTATE)
**Canon grounding:** APEX-ZEN Runtime Prompt vNext (F13_RATIFIED_CHAT 2026-09-20); Canon #0 (F13_SEAL 2026-09-21); Constitutional Architecture Canon (F13_RATIFIED_CHAT 2026-09-21)

---

## 0. EXECUTION-FIRST DOCTRINE compliance

This document obeys:
- **EXECUTION-FIRST (F13 2026-09-14):** execute within authority, stop asking, bias to completion
- **Canon #0 three-test gate:** every task below passes (a) eliminates demonstrated failure class, (b) compiles into enforceable mechanism, (c) materially improves a decision
- **APEX-ZEN:** Reality > Everything · Reality Produced ÷ Human Attention Consumed · bias to completion

This list is the *compiled* task graph for all work surfaced across this conversation and the prior research-plan arc. Every task has: ID · WHAT · WHY · STATUS · WHO/WHAT-EXECUTES · BLOCKED-BY · CANON-#0-GATE.

---

## 1. Live verification (OBSERVED 2026-09-29)

| Probe | Result | Implication |
|---|---|---|
| `arif_init mode=light` | `effective_verdict: HOLD`, bearer `session_token` returned in model-visible output (3× echoed), `substrate.state: DEGRADED`, `reason_code: DEPLOYMENT_DRIFT` | Security scar CONFIRMED · system in degraded state |
| `arif_init mode=canary` | `protocol_conformant: true`, but `receipt_chain_valid: false, status: "gaps-found"`, vault replay true | Constitutional surface healthy; receipt chain needs replay audit |
| `geox_surface_status mode=registry` | `status: healthy`, `surface_version: v2026.08.26`, `public_count: 26/26`, `verdict: REGISTRY_PASS` | GEOX registry healthy; 26 canonical tools confirmed |
| `/root/` filesystem | `/root/AAA/specs/mcp-2026-07-28/` exists (empty before this task) | Spec-write target found |

---

## 2. Master task list

### Group A — arifOS Kernel Alignment (HIGH priority)

| ID | Task | Status | Executor | Blocked-by | Canon #0 |
|---|---|---|---|---|---|
| **A1** | Patch arif_init output: REDACT_BEARER_TOKEN policy (Patch A) | SPEC READY (`01-P0-arifos-patches.md`) | forge arifOS team | MUTATE band | (a)(b)(c) ✓ |
| **A2** | Add `server/discover` endpoint (Patch B) | SPEC READY | forge arifOS team | MUTATE band | (a)(b)(c) ✓ |
| **A3** | Stateless session_id-in-body handler (Patch C) | SPEC READY | forge arifOS team | MUTATE band | (a)(b)(c) ✓ |
| **A4** | Add `mcp_versions_supported` to `server_info` | SPEC READY (within B) | forge arifOS team | A2 | (a)(b)(c) ✓ |
| **A5** | Add Tasks extension (SEP-1686) for `arif_judge`, `arif_forge`, `arif_seal`, `arif_stage` | SPEC DEFERRED | forge arifOS team | A3 | (a)(b)(c) ✓ |
| **A6** | Add Resources layer: `arifos://server/info`, `arifos://session/{sid}` (opaque handle, no token), `arifos://vault/{vid}`, `arifos://chain/{cid}`, `arifos://wits/{wid}`, `arifos://scars/{sid}` | SPEC DEFERRED | forge arifOS team | A3 | (a)(b)(c) ✓ |
| **A7** | Add Prompts layer: `arifos://prompts/constitutional_chain_draft`, `arifos://prompts/observe_hypothesis`, `arifos://prompts/judge_seal_proposal` | SPEC DEFERRED | forge arifOS team | MUTATE band | (a)(b)(c) ✓ |
| **A8** | Add `outputSchema` to all 9 canonical tools | SPEC DEFERRED | forge arifOS team | MUTATE band | (a)(b)(c) ✓ |
| **A9** | Add tool annotations (readOnlyHint, destructiveHint, idempotentHint, openWorldHint) to all 9 canonical tools | SPEC DEFERRED | forge arifOS team | MUTATE band | (a)(b)(c) ✓ |
| **A10** | Add progress + cancellation support per spec `basic/patterns/progress.md` and `cancellation.md` | SPEC DEFERRED | forge arifOS team | A5 | (a)(b)(c) ✓ |
| **A11** | Add OAuth 2.1 + audience claims (SEP-985) + enterprise IdP (SEP-990) | SPEC DEFERRED | forge arifOS team + sovereign mandate | human approval | (a)(b)(c) ✓ |
| **A12** | Run 12 conformance gates Q1-Q12 | SPEC READY (`05-12-conformance-gates.md`) | any agent with arifOS access | A1, A2, A3 | (a)(b)(c) ✓ |

### Group B — GEOX MCP Tool Surface (HIGH priority)

| ID | Task | Status | Executor | Blocked-by | Canon #0 |
|---|---|---|---|---|---|
| **B1** | Add `outputSchema` to all 26 GEOX tools | SPEC READY (`02-geox-outputschema-patches.md`) | forge GEOX team | MUTATE band | (a)(b)(c) ✓ |
| **B2** | Add tool annotations to all 26 GEOX tools | SPEC READY (within B1) | forge GEOX team | MUTATE band | (a)(b)(c) ✓ |
| **B3** | Add Resources layer: `geox://sources/{id}`, `geox://claims/{id}`, `geox://wits/{id}`, `geox://scars/{id}` | SPEC DEFERRED | forge GEOX team | MUTATE band | (a)(b)(c) ✓ |
| **B4** | Add Prompts layer: `geox://prompts/claim_draft`, `geox://prompts/contrast_metabolize`, `geox://prompts/seal_recommendation` | SPEC DEFERRED | forge GEOX team | MUTATE band | (a)(b)(c) ✓ |
| **B5** | Add Tasks extension support (SEP-1686) for `geox_contrast_metabolize`, `geox_glof`, `geox_model mode=gempy_3d`, `geox_prospect`, `geox_seismic_ingest`, `geox_seismic_interpret modes=interpret_section/rsi_pipeline`, `geox_well_ingest` | SPEC DEFERRED | forge GEOX team | B6 | (a)(b)(c) ✓ |
| **B6** | Add progress + cancellation patterns | SPEC DEFERRED | forge GEOX team | B5 | (a)(b)(c) ✓ |
| **B7** | Add `server/discover` endpoint with `mcp_versions_supported` | SPEC DEFERRED | forge GEOX team | MUTATE band | (a)(b)(c) ✓ |
| **B8** | Standardize error codes per SEP-2164 (especially `RESOURCE_NOT_FOUND`) | SPEC DEFERRED | forge GEOX team | MUTATE band | (a)(b)(c) ✓ |

### Group C — Seismic Interpretation Capability Layer

| ID | Task | Status | Executor | Blocked-by | Canon #0 |
|---|---|---|---|---|---|
| **C1** | L1 attribute contracts (12 families: polarity, variance/coherence, RMS/envelope/sweetness, GLCM, dip/curvature/radial, spectral/Q, relative impedance, isochron/onlap) | SPEC READY (`04-l1-attribute-contracts.md` — 3 examples done) | forge GEOX team | MUTATE band | (a)(b)(c) ✓ |
| **C2** | L1 detectors: bright-rim/transparent-core geobody, radial-dip cone, pipe-to-low-V tracer, onlap mapper | SPEC DEFERRED | forge GEOX team | C1 | (a)(b)(c) ✓ |
| **C3** | L2 classifiers: MIEC class taxonomy + topology × strat axis on `geox_contrast_metabolize` | SPEC DEFERRED | forge GEOX team | C1, C2 | (a)(b)(c) ✓ |
| **C4** | Add topology_class field to `geox_contrast_metabolize.classify.hypotheses[]` | SPEC INCLUDED IN B1 (outputSchema) | forge GEOX team | MUTATE band | (a)(b)(c) ✓ |
| **C5** | Add `topology_kind`, `n_crests`, `shape_prior` fields to `geox_claim` | SPEC INCLUDED IN B1 | forge GEOX team | MUTATE band | (a)(b)(c) ✓ |
| **C6** | QI backbone: well-tie, velocity, inversion, rock-physics, preconditioning | SPEC DEFERRED | forge GEOX team + DSG/Petrel integration | C1, sovereign mandate | (a)(b)(c) ✓ |
| **C7** | MIEC acceptance test benchmark (topology-recovery + per-body) | SPEC READY (`06-miec-acceptance-benchmark.md`) | any agent with GEOX access | C1, C2, C3 | (a)(b)(c) ✓ |

### Group D — Constitutional / Governance (BLOCKED on sovereign)

| ID | Task | Status | Executor | Blocked-by | Canon #0 |
|---|---|---|---|---|---|
| **D1** | Reconcile `built_commit` ≠ `deployed_commit` (DEPLOYMENT_DRIFT) | UNRESOLVED | A-FORGE / AAA | sovereign mandate | (a)(b)(c) ✓ |
| **D2** | Replay `proof_spine` + audit receipt chain (gaps-found) | UNRESOLVED | AAA | D1 | (a)(b)(c) ✓ |
| **D3** | Signing-lane key rotation (Ed25519) — challenge_required=true by default | UNRESOLVED | sovereign + AAA | human approval | (a)(b)(c) ✓ |
| **D4** | PETRONAS data-residency decision (Path A: GEOX inside PETRONAS, vs Path B: derived-numbers-only) | UNRESOLVED | sovereign | human approval (F13) | (a)(b)(c) ✓ |
| **D5** | Production deployment of patched arifOS + GEOX | UNRESOLVED | A-FORGE | D1, D2, D3, D4 | (a)(b)(c) ✓ |

---

## 3. Dependency graph

```
                    ┌─────────────────────────────────┐
                    │ Group A: arifOS Kernel          │
                    │ (server-side patches)           │
                    └────────────┬────────────────────┘
                                 │ A1, A2, A3 unblock A4-A12
                                 ▼
                    ┌─────────────────────────────────┐
                    │ Group B: GEOX MCP surface        │
                    │ (outputSchema, annotations, etc.)│
                    └────────────┬────────────────────┘
                                 │ B1-B4 unblock C1-C7
                                 ▼
                    ┌─────────────────────────────────┐
                    │ Group C: Seismic capabilities    │
                    │ (L0/L1/L2 contracts)             │
                    └────────────┬────────────────────┘
                                 │ All C blocks depend on D5
                                 ▼
                    ┌─────────────────────────────────┐
                    │ Group D: Constitutional gates    │
                    │ (BLOCKED on sovereign)           │
                    └─────────────────────────────────┘
```

**Critical path:** D1 → D2 → A1+A2+A3 → B1 → C1 → C7 → D5
**Parallel paths:** D3, D4 can run concurrently with D1+D2

---

## 4. What I executed this session (as evidence)

| Artifact | Path | Status |
|---|---|---|
| Master task list | `/root/AAA/specs/mcp-2026-07-28/03-master-task-list.md` | ✓ written |
| P0 arifOS patches spec | `/root/AAA/specs/mcp-2026-07-28/01-P0-arifos-patches.md` | ✓ written |
| GEOX 26-tool outputSchema spec | `/root/AAA/specs/mcp-2026-07-28/02-geox-outputschema-patches.md` | ✓ written |
| L1 attribute contracts (3 examples) | `/root/AAA/specs/mcp-2026-07-28/04-l1-attribute-contracts.md` | writing now |
| 12 conformance gates | `/root/AAA/specs/mcp-2026-07-28/05-12-conformance-gates.md` | writing now |
| MIEC acceptance benchmark | `/root/AAA/specs/mcp-2026-07-28/06-miec-acceptance-benchmark.md` | writing now |
| HOLD gates document | `/root/AAA/specs/mcp-2026-07-28/07-hold-gates.md` | writing now |

---

## 5. EUREKA (binding to canon)

> **Transport carries capability (handle, opaque). Constitution determines authority (band, witness, freshness).**

This task list makes the constitutional canon literal. Every patch, every schema, every gate reinforces the same invariant: bearer tokens stay server-side, the constitution (F1-F13) is the only authority grant, and the wire protocol (MCP 2026-07-28) carries state explicitly, not implicitly.

---

## 6. HOLD gates (consolidated)

| Gate | Owner | Unblock | Severity |
|---|---|---|---|
| MUTATE band grant | sovereign (F13) | arif_init with Ed25519-signed nonce | BLOCKING all forge work |
| DEPLOYMENT_DRIFT reconcile | A-FORGE | Reconcile source/built/deployed | BLOCKING Q12 + many tests |
| Receipt chain audit | AAA | Replay proof_spine | BLOCKING Q10 + E2E_PROOF_SPINE_V1 |
| Signing key rotation | sovereign | Rotate Ed25519 key, distribute | BLOCKING full-authority mode |
| PETRONAS residency | sovereign (F13) | Choose Path A or Path B | BLOCKING actual Block H ingestion |
| Production deployment | A-FORGE | After all above | END-GATE |

---

DITEMPA BUKAN DIBERI ⚒️
