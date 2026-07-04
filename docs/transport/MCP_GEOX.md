# MCP_GEOX.md

**Role:** Nervous system for governed agentic federation (EGS + arifOS + LLM + WEALTH + WELL)
**Doctrine:** Forge schemas, flow evidence, gate action, seal only after judgment.
**Status:** TRANSPORT WIRING — maps ChatGPT's spine proposal to existing infra, identifies real gaps

---

## §0 Existing vs Proposed — Truth Table

Before anything: **9/10 sections of ChatGPT's spine already exist across the federation.** The work is not building new infrastructure — it's unifying transport conventions.

| § | Spine Section | Existing Status | What's Wired | What's Missing |
|---|--------------|----------------|--------------|----------------|
| 1 | MCP lifecycle | ✅ LIVE | All organs implement initialize/active/teardown via FastMCP/MCP SDK | No unified lifecycle contract doc |
| 2 | Organ boundaries | ✅ LIVE | BRAIN/HANDS contract, PeerContractService, constitutional_map.py | Boundary not annotated on every tool at transport level |
| 3 | Resource URI map | ✅ LIVE (6 schemes) | `geox://`, `arifos://`, `forge://`, `well://`, `wealth://`, `tree777://` | URIs don't follow EGS naming; `egs://` not registered; receipts use `source://`/`receipt://` not `arifos://receipts/` |
| 4 | Tool registry | ✅ LIVE (all tools exist) | A-FORGE ~59, GEOX 18, arifOS 21+ | No unified v0.1 minimum spine list enforced cross-organ |
| 5 | JSON schemas | ✅ LIVE (all exist) | `ClaimEnvelope`, `EarthMemoryEnvelope`, `forge_session.schema.json`, `common.schema.json` | Some tool schemas don't carry authority_class |
| 6 | Error semantics | ✅ LIVE (per-organ) | `isError` in A-FORGE (54 call sites), `status: OK/ERROR/HOLD/VOID` in GEOX, `status: void` in arifOS | **NOT UNIFIED** — 3 different error formats across organs |
| 7 | Authority gates | ✅ LIVE (per-organ) | A-FORGE 8-class, arifOS 10-class, GEOX 3-flag, PeerContractService 5-class | **NOT UNIFIED** — 4 different classification systems |
| 8 | Receipt format | ✅ LIVE (per-organ) | VAULT999 receipts, forge receipts, arifOS receipts | **NOT UNIFIED** — no single receipt_id format |
| 9 | Security floor | ✅ LIVE (partial) | OriginValidationMiddleware (arifOS), scoped tokens (ad-hoc) | No cross-organ security spec; rate limits ad-hoc |
| 10 | Test probes | ❌ PROPOSED | Individual tests exist (34 in A-FORGE, contract parity in AAA) | No cross-organ spine probe battery |

---

## §1 MCP Lifecycle Contract (Wiring)

### Existing State

| Organ | Framework | Transport | Lifecycle Hooks |
|-------|-----------|-----------|-----------------|
| GEOX | FastMCP 3.4.2 | StreamableHTTP (8081) + stdio | No custom hooks (uses FastMCP built-in) |
| arifOS | FastMCP | StreamableHTTP (8088) + stdio | Starlette lifespan — `_startup_nats_event_bus()`, `_shutdown_nats_event_bus()` |
| A-FORGE 7071 | Express + MCP SDK | HTTP REST + MCP | Express lifecycle |
| A-FORGE 7072 | MCP SDK 1.29.0 | StreamableHTTP + stdio | MCP SDK built-in |
| WEALTH | FastMCP | StreamableHTTP (18082) | — |
| WELL | FastMCP | StreamableHTTP (18083) | — |

### Wiring Required (Low Effort)

| What | Who | Change |
|------|-----|--------|
| Add `initialize`/`teardown` log line | ALL organs | 1 line each — emit structured log at startup/shutdown |
| Document lifecycle contract | NEW FILE | 1-page contract in `/root/AAA/contracts/mcp-lifecycle.md` |

**No code changes to lifecycle behavior.** Everything already works. Just document.

---

## §2 Organ Boundaries (Wiring)

### Existing State

Already wired:
- **A-FORGE:** `PeerContractService.ts` enforces `authority_class` mapping — `judge` is exclusive to arifOS, A-FORGE must have `execute`
- **arifOS:** `constitutional_map.py` maps tools to stages — GEOX tools cannot issue SEAL verdicts
- **GEOX:** `geox_surface_status` annotates `final_authority` per tool
- **Genesis:** `009_MCP_BOUNDARY.md` + `010_ADAT_AGENTIC.md` define the doctrinal separation

### Wiring Required (Medium Effort)

| What | Who | Change |
|------|-----|--------|
| Add `organ_boundary` annotation to every MCP tool response | ALL organs | Add `_organ_boundary: { organ: "GEOX", authority: "EVIDENCE_ONLY", cannot_do: ["JUDGE", "SEAL"] }` |

**This is the key gap.** Currently boundaries are enforced at the governance layer (PeerContractService, constitutional_map) but NOT annotated on every tool response. Without this, the LLM receiving the response has no way to know which organ produced it and what authority it carries.

**Implementation pattern** (1 field added to every tool response envelope):

```jsonc
{
  // existing fields...
  "_organ_boundary": {
    "organ": "GEOX",
    "authority": "EVIDENCE_ONLY",
    "cannot": ["JUDGE", "SEAL", "IRREVERSIBLE_ACTION"]
  }
}
```

---

## §3 Resource URI Map (Wiring)

### Existing State

6 URI schemes, ~100+ endpoints. The schemes are close to ChatGPT's proposal but naming is inconsistent:

| Proposed URI | Existing URI | Status |
|-------------|-------------|--------|
| `egs://basins/{basin_id}` | `geox://basins/malay-basin/profile` | ✅ EXISTS (different scheme) |
| `egs://claims/{claim_id}` | `geox://claims/index` | ✅ EXISTS (different scheme) |
| `egs://evidence/{evidence_id}` | `geox://resources/{category}/{name}` | ✅ EXISTS (generic) |
| `egs://scenarios/{scenario_id}` | ❌ | ❌ DOES NOT EXIST |
| `arifos://receipts/{receipt_id}` | `source://{hash}`, `receipt://web/{id}`, `runner://receipt/{run_id}` | ✅ EXISTS (3 parallel schemes) |
| `arifos://sessions/{session_id}` | ❌ | ❌ DOES NOT EXIST |

### Wiring Required (Low-medium Effort)

**Decision needed:** Which URI convention wins? Options:
1. **Keep existing** — `geox://`, `arifos://`, `forge://`, `well://`, `wealth://` — each organ has its own
2. **Converge to EGS** — add `egs://` as alias for GEOX resources, keep `arifos://` for governance

**Recommendation:** Keep existing schemes. Add `egs://` as secondary alias for GEOX resources. No urgent need to rename working URIs.

| What | Who | Change |
|------|-----|--------|
| Add `egs://` resource aliases for `geox://` | GEOX | Register `egs://claims/{claim_id}`, `egs://basins/{basin_id}`, `egs://evidence/{evidence_id}`, `egs://assets/{asset_id}`, `egs://scenarios/{id}` |
| Add `arifos://receipts/{receipt_id}` | arifOS | Register resource template pointing to VAULT999 receipt store |
| Add `arifos://sessions/{session_id}` | arifOS | Register resource template for session state |

---

## §4 Tool Registry — Minimum Spine (Wiring)

### Existing State

ChatGPT proposed a 9-tool minimum spine. Here's the 1:1 mapping to existing tools:

| # | Proposed Tool | Existing Tool(s) | Status |
|---|--------------|-------------------|--------|
| 1 | `geox_data_qc_bundle` | `geox_well_qc` + `geox_well_ingest` | ✅ EXISTS (two tools, same function) |
| 2 | `geox_claim_create` | `geox_claim(mode=create)` | ✅ EXISTS |
| 3 | `geox_claim_challenge` | `geox_evidence(mode=contradict)` + `geox_claim(mode=challenge)` | ✅ EXISTS |
| 4 | `geox_evidence_attach` | `geox_claim(mode=attach)` | ✅ EXISTS |
| 5 | `geox_evidence_reason` | `geox_evidence(mode=synthesize, abduct)` | ✅ EXISTS |
| 6 | `geox_seismic_compute` | `geox_seismic_compute` (modes: synthetic, well_tie, AVO, attribute) | ✅ EXISTS |
| 7 | `arif_triage` | `arif_route` (mode=intent classification) | ✅ EXISTS (different name) |
| 8 | `arif_judge` | `arif_judge` | ✅ EXISTS |
| 9 | `arif_receipt_create` | `arif_seal` + `forge_vault` + VAULT999 | ✅ EXISTS (3 paths) |

**Finding:** ALL 9 proposed tools exist. The spine is already wired. No new tools needed.

### Wiring Required (Low Effort)

| What | Who | Change |
|------|-----|--------|
| Document the spine mapping | NEW FILE | Table showing proposed → existing tool names |
| Add `arif_triage` as alias for `arif_route(mode=auto)` | arifOS | 1-line alias registration (not a new tool — just a route mode) |

---

## §5 JSON Schemas (Wiring)

### Existing State

ChatGPT proposed 3 schemas:

**`geox_claim_create` schema** — Already exists as `ClaimEnvelope` in `/root/geox/src/geox_core/schemas/claim_envelope.py` (441 lines). The fields match: `claim_text` (exists as `claim` field in EarthMemoryEnvelope), `claim_type` (exists as `claim_type`), `truth_class` (exists as `truth_class` enum: FACT/INTERPRETATION/SPECULATION → but GEOX uses OBSERVED/DERIVED/ESTIMATE/HYPOTHESIS/PLAUSIBLE/UNKNOWN — close alignment), `evidence_ids` (exists as `evidence_for`/`evidence_against`), `uncertainty_p10/p50/p90` (exists as `uncertainty` field in ClaimEnvelope with `interval: [min, max]` and `confidence`).

**`geox_query_claim` schema** — Already exists as `geox_claim(mode=read)` or via `geox://claims/{claim_id}` resource.

**`arif_judge` schema** — Already exists in `arif_judge` tool definition. The proposed schema is SIMPLER than what already exists (existing arif_judge has session_id, actor_id, authority_token, blast_radius, domain, evidence, intent, etc.).

### Wiring Required (Low Effort)

**Decision needed:** Should GEOX use ChatGPT's `truth_class` enum (FACT/INTERPRETATION/SPECULATION) or the existing `ClaimState` epistemic ladder (OBSERVED/DERIVED/ESTIMATE/HYPOTHESIS/PLAUSIBLE/UNKNOWN)?

**Recommendation:** Keep existing `ClaimState`/`EpistemicLabel` system. It's more nuanced (6 tiers vs 3). Add `truth_class` as a compatibility alias if external clients use it.

| What | Who | Change |
|------|-----|--------|
| Add `truth_class` as alias field on ClaimEnvelope | GEOX | 5-line mapping: FACT→SEALED, INTERPRETATION→INTERPRETED, SPECULATION→HYPOTHESIS |
| Add `authority_class` field to arif_judge input | arifOS | 1 field addition — accepts ADVISORY/MUTATION/IRREVERSIBLE |

---

## §6 Error Semantics (Wiring — REAL GAP)

### Existing State

**3 different error formats across organs:**

```
A-FORGE:     { content: [...], isError: true | false }
GEOX:        { status: "OK" | "ERROR" | "HOLD" | "VOID", message: "..." }
arifOS:      { status: "void", error: "...", recoverable: true | false }
```

This is the **biggest transport gap**. An LLM receiving responses from different organs must handle 3 different error shapes.

### Wiring Required (Medium Effort)

**Standardize to one format across ALL organs.** Proposed standard (minimal change from existing):

```jsonc
// UNIFIED ERROR RESPONSE
{
  "isError": true,                    // MCP SDK standard field
  "errorCode": "EVIDENCE_NOT_FOUND",  // machine-readable
  "errorMessage": "Claim ID CLM_001 not found in Earth memory",  // human-readable
  "recoverable": true,                // can the LLM retry/fix?
  "authority": "ADVISORY_ONLY"        // what class was this operation?
}
```

| What | Who | Change |
|------|-----|--------|
| Standardize GEOX error format to `isError` | GEOX | Wrap `status` → `isError` in response envelope (~5 lines in run_legacy_tool) |
| Standardize arifOS error format to `isError` | arifOS | Add `isError` alongside existing `status` (~3 lines in GlobalPanicMiddleware) |
| Add `recoverable` flag | ALL organs | 1 field per error response |
| Add `authority` to error response | ALL organs | 1 field per error response |

---

## §7 Authority Gates (Wiring — REAL GAP)

### Existing State

**4 different classification systems:**

```
A-FORGE actionClassifier:    8 classes  (OBSERVE→IRREVERSIBLE)
A-FORGE PeerContractService: 5 classes  (evidence/advisory/route/execute/judge)
arifOS canonical_envelope:   10 classes (UNKNOWN→EXTERNAL)
arifOS mcp_gate_v0:          8 classes  (aligned with A-FORGE on 2026-06-23)
GEOX geox_surface_status:    3 flags    (mutation/irreversible/888_hold)
ChatGPT proposal:            4 classes  (ADVISORY_ONLY/MUTATION_ALLOWED/IRREVERSIBLE_PROPOSED/IRREVERSIBLE_SEALED)
```

### Wiring Required (Medium Effort)

**Decision needed:** Which classification system to standardize on?

**Recommendation:** Use A-FORGE's 8-class `actionClassifier` as the canonical system (already aligned with arifOS `mcp_gate_v0`). Add ChatGPT's 4-class `authority_class` as a **compatibility projection** on top.

The 4-class → 8-class mapping:

| authority_class (ChatGPT) | action_class (A-FORGE) | Meaning |
|--------------------------|----------------------|---------|
| ADVISORY_ONLY | OBSERVE, SUGGEST, SIMULATE, DRAFT | Read-only, suggestions, simulations |
| MUTATION_ALLOWED | QUEUE, EXECUTE_REVERSIBLE | Mutable but reversible |
| IRREVERSIBLE_PROPOSED | EXECUTE_HIGH_IMPACT | Proposed irreversible — needs gate |
| IRREVERSIBLE_SEALED | IRREVERSIBLE | Executed and sealed — permanent |

| What | Who | Change |
|------|-----|--------|
| Add `authority_class` field to every tool response | ALL organs | 1 field — `authority_class: "ADVISORY_ONLY"` |
| Map ChatGPT's 4-class to existing 8-class | ALL organs | Document the projection |

---

## §8 Receipt Format (Wiring — REAL GAP)

### Existing State

ChatGPT proposed a receipt format with: `receipt_id`, `timestamp`, `actor`, `session_id`, `tool_name`, `input`, `output_summary`, `uncertainty_summary`, `authority_class`, `blast_radius`, `links`.

Existing receipt-like structures:
- **VAULT999:** `vault999_event.schema.json` — hash-chained, immutable
- **A-FORGE:** `forge://work/{receipt_id}` — forge work receipts
- **arifOS:** `arif_seal` output — sealed verdict records
- **GEOX:** ClaimEnvelope — not a receipt but contains most receipt fields

**No single receipt_id format** exists. arifOS uses `sha256:...`, A-FORGE uses UUID, VAULT999 uses sequential integers.

### Wiring Required (Medium Effort)

| What | Who | Change |
|------|-----|--------|
| Define canonical receipt schema | NEW FILE | `/root/AAA/schemas/receipt.schema.json` — merge existing vault + forge + arifOS formats |
| Standardize receipt_id format | ALL organs | Use `RCP_` prefix + UUIDv4 (e.g., `RCP_a1b2c3d4-...`) |
| Add `authority_class` + `blast_radius` to receipts | ALL organs | 2 fields per receipt |

---

## §9 Security Floor (Wiring)

### Existing State

| Security Measure | GEOX | arifOS | A-FORGE | WEALTH | WELL |
|-----------------|------|--------|---------|--------|------|
| Origin validation | ❌ | ✅ (OriginValidationMiddleware) | ❌ | ❌ | ❌ |
| Scoped tokens | ✅ (token bypass for stdio) | ✅ | ✅ (env-based) | ✅ | ✅ |
| Rate limits | ❌ | ❌ | ❌ | ❌ | ❌ |
| Public exposure | ✅ (https://geox.arif-fazil.com) | ✅ (https://arifos.arif-fazil.com) | ❌ (localhost only) | ✅ | ✅ |

### Wiring Required (Low-medium Effort)

**Check:** Are any organs exposed to public internet without origin validation?

**Yes.** GEOX, arifOS, WEALTH, and WELL are all publicly accessible via subdomains. Only arifOS has `OriginValidationMiddleware`.

| What | Who | Change |
|------|-----|--------|
| Add origin validation to GEOX | GEOX | Copy `OriginValidationMiddleware` pattern from arifOS — allowlist known origins |
| Add origin validation to WEALTH/WELL | WEALTH, WELL | Same pattern |
| Document allowed origins | NEW FILE | `/root/AAA/contracts/allowed-origins.yaml` |

---

## §10 Test Probes (BUILD)

### Existing State

No cross-organ spine probe battery exists. However:
- **A-FORGE:** 34 test files covering governance, engine, planner, approval, MCP
- **AAA:** Contract parity tests (947 lines) validating canonical tool outputs
- **GEOX:** 810+ tests

### Build Required (Medium Effort)

ChatGPT proposed 5 probes. Implementation:

| Probe | What it tests | How to implement |
|-------|--------------|-----------------|
| 1 — Read-only discipline | GEOX query tools never mutate state | Run `geox_query_*`, verify receipt has `authority_class: ADVISORY_ONLY` |
| 2 — Claim lifecycle | Full claim lifecycle: create → challenge → evidence → judge → receipt | E2E test calling real endpoints |
| 3 — Authority leak | Try to seal via EGS tools, confirm only arifOS can | Negative test — attempt seal via GEOX, expect 888_HOLD |
| 4 — LLM misbehavior | LLM invents geology, MCP + EGS route to governance | Integration test with mock LLM |
| 5 — ASAL geometry audit | Run ASAL against different models, confirm spine exposes differences | Call `asal_score_probe.py` via MCP |

**Build priority:** Probes 1-3 are v0.1. Probes 4-5 are v0.2.

---

## §11 One-Line Wiring Summary

> **Everything exists. The work is unifying 4 classification systems, 3 error formats, and 6 URI schemes into one transport convention that every organ speaks.**

---

## Appendix A: Existing Resource URI Reference (All Organs)

### GEOX — `geox://` (20+ URIs)
```
geox://reality/context          — current Earth reality context
geox://identity                 — GEOX organ identity
geox://registry/apps            — registered apps
geox://profile/status           — organ profile
geox://capabilities             — tool capability map
geox://resources/{category}/{name}  — generic resource access
geox://resources/index          — resource directory
geox://surface/truth            — surface truth state
geox://claims/index             — claim directory
geox://claims/graph             — claim relationship graph
geox://artifacts/index          — artifact directory
geox://basins/index             — basin directory
geox://basins/malay-basin/profile — specific basin profile
geox://literature/{ref}         — literature references
geox://render/surfaces/{surface_id} — surface render
geox://render/cubes/{cube_id}/manifest — cube data manifest
geox://render/cubes/{cube_id}/lod/{lod}/brick/{ix}/{iy}/{iz} — cube brick streaming
geox://render/payload-schema/{version} — render schema
geox://resources/prompts/index  — prompt templates
geox://resources/playbooks/index — playbooks
geox://resources/ontology/index — ontology
geox://resources/schemas/index  — schemas
```

### arifOS — `arifos://` (16+ URIs)
```
arifos://doctrine               — constitutional doctrine
arifos://trinity                — ΔΩΨ trinity state
arifos://schema                 — canonical schemas
arifos://civilization           — civilizational memory
arifos://seal-readiness         — seal readiness state
arifos://jurisdiction           — jurisdiction map
arifos://identity               — kernel identity
arifos://memory                 — memory state
arifos://vitals                 — kernel vital signs
arifos://bootstrap              — bootstrap state
arifos://human/metabolized      — human substrate
arifos://loop-engineering       — loop engineering state
arifos://quickstart             — quickstart guide
arifos://mcp-alignment          — MCP alignment spec
arifos://resources/index        — resource index
arifos://skills-catalog         — skills catalog
arifos://tools/self-model/{view}    — tool self-model
arifos://tools/permissions/{scope}  — tool permissions
arifos://tools/composition-matrix/{format} — tool composition
arifos://witness/log/{filter}   — witness logs
arifos://witness/stats/{period} — witness statistics
arifos://boundaries/domain/{domain_id} — domain boundaries

Additional schemes:
source://{hash}                 — source evidence
receipt://web/{id}              — web receipts
contrast://{id}                 — contrast records
void://{id}                     — voided records
runner://receipt/{run_id}       — runner receipts
runner://policy/v1              — runner policy
skill://{name}/SKILL.md         — skills (49+ entries)
```

### A-FORGE — `forge://` (8 URIs)
```
forge://governance/floors       — F1-F13 floor state
forge://approvals/pending       — pending hold queue
forge://memory/working          — working memory state
forge://identity/contract       — organ identity contract
forge://vault/records/{category} — vault records by category
forge://vault/categories        — vault category list
forge://registry/{organ}        — organ tool registry
forge://work/{receipt_id}       — forge work receipts
forge://well/state              — well organ state
```

### WELL — `well://` (18 URIs)
```
well://identity                 — organ identity
well://registry                 — tool registry
well://bio/signals              — biological signals
well://doctrine                 — doctrine
well://human/substrate          — human substrate state
well://bridge/geox              — GEOX bridge state
well://bridge/arifos-kernel     — arifOS bridge state
well://bridge/wealth            — WEALTH bridge state
... (10 more bridge/resources)
```

### WEALTH — `wealth://` (14 URIs)
```
wealth://schema                 — canonical schema
wealth://tools/registry         — tool registry
wealth://health                 — organ health
wealth://reality/context        — capital reality context
wealth://market/sources         — market data sources
wealth://risk/thresholds        — risk thresholds
wealth://handoff/arifos-schema  — arifOS handoff schema
... (7 more)
```

---

## Appendix B: Spine Tools — Existing Mapping

| Proposed | Existing | Organ | Justification |
|----------|----------|-------|-------------|
| `geox_data_qc_bundle` | `geox_well_qc` + `geox_well_ingest` | GEOX | QC + ingest = data bundle |
| `geox_claim_create` | `geox_claim(mode=create)` | GEOX | Exact match |
| `geox_claim_challenge` | `geox_evidence(mode=contradict)` + `geox_claim(mode=challenge)` | GEOX | Challenge = contradict + challenge |
| `geox_evidence_attach` | `geox_claim(mode=attach)` | GEOX | Exact match |
| `geox_evidence_reason` | `geox_evidence(mode=synthesize, abduct)` | GEOX | Reason = synthesize + abduct |
| `geox_seismic_compute` | `geox_seismic_compute` (multi-mode) | GEOX | Exact match |
| `arif_triage` | `arif_route(mode=auto)` | arifOS | Intent classification |
| `arif_judge` | `arif_judge` | arifOS | Exact match |
| `arif_receipt_create` | `arif_seal` + `forge_vault` | arifOS/A-FORGE | Receipt = seal or vault write |

---

## Appendix C: One-Line Doctrines

> Forge schemas, flow evidence, gate action, seal only after judgment.

> MCP should expose capability. arifOS should decide authority. EGS should expose Earth truth-state. LLM should explain, not invent.

> The spine is already wired. The work is unifying transport conventions — 4 classification systems → 1, 3 error formats → 1, 6 URI schemes → discoverable.

> Do not start with 50 tools. Nine tools are enough to prove the architecture. (They already exist.)

---

*DITEMPA BUKAN DIBERI — Forged, Not Given.*  
*MCP Spine v0.1 · 2026-06-28*  
*Wires ChatGPT's proposal to existing arifOS federation transport*
