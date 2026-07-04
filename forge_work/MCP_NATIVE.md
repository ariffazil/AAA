# C1-MCP-NATIVE-SURFACE

**Forge Work ID:** C1-MCP-NATIVE-SURFACE
**Created:** 2026-06-06
**Authoring session:** SEAL-91e12b6644f64589
**Authoring actor:** arif-fazil-af-forge
**Floor:** C1 (observe/advise) → C2 (execute) gated
**Reversibility:** All sub-forges reversible until GREEN-SEAL of the full forge
**Sunset policy:** Tactical bridges carry a hard sunset epoch. No tactical bridge becomes permanent.

---

## Reality (live audit, 2026-06-06)

Probes run against the live arifOS MCP at `https://mcp.arif-fazil.com/mcp` and local `http://127.0.0.1:8088`:

| Surface | Reality | Source |
|---|---|---|
| `tools/list` | 13/13 canonical tools bound | `arif_kernel_route(mode=list)` |
| `prompts/list` | NOT EXPOSED | absent from MCP server contract |
| `prompts/get` | NOT EXPOSED | absent from MCP server contract |
| `resources/list` | NOT EXPOSED | absent from MCP server contract |
| `resources/read` | NOT EXPOSED — and `arif_evidence_fetch` rejects `resource://` under F12 | live error: `failed_floors: ["F12"]` |
| `arif_mind_reason` (10 modes) | Tool executes; degrades to HOLD when LLM output is non-dict | live error: `truth_verdict: HYPOTHESIS, final_verdict: HOLD, reason: LLM returned non-dict` |
| `arif_judge_deliberate` (safe modes) | BLOCKED with `LEGACY_WRAP cannot execute ATOMIC` | live error: 888_HOLD on `explain`, `compare`, `history` |
| `arif_gateway_connect(mode=discover)` | SEAL — 7 agents reachable | live: `[firecrawl, gemini, kimi, tavily, claude, exa, minimax]` |
| `arif_gateway_connect(mode=relay)` | HOLD (gated, requires L11 + judge_state_hash) | per `arif_kernel_route(mode=list)` |
| `arif_evidence_fetch(url="resource://...")` | HOLD with F12 — `Invalid URL scheme: resource://` | live error |
| Runtime health | CPU 57.2% mod, MEM 72.9% mod, DISK 43.1% low | `arif_ops_measure(mode=health)` |
| Schema discipline (F10) | HEALTHY — unknown fields rejected, unknown modes rejected | per live probes |

## Truth (the invariant)

The **arifOS canonical13 tool layer is healthy and self-aware**: it knows its own surface, respects floors, does not over-claim authority, and fail-closes on malformed input.

The **MCP-native prompts/resources layer is intentionally incomplete (Phase-2 surface gap, not regression)**. Stage labels exist as metadata in tool responses, but the MCP server does not yet expose `prompts/list`, `prompts/get`, `resources/list`, `resources/read` as first-class primitives.

There is a **contract mismatch** between advertised internal resources (`resource://agent/capabilities/raw` in `arif_session_init.raw_manifest_location`) and the read path (`arif_evidence_fetch` rejects `resource://` under F12).

There is a **connector-level bug** in `arif_judge_deliberate` that blocks safe read-only modes (explain, compare, history) behind a `LEGACY_WRAP` gate, which prevents C1→C2 transition.

## Sub-forges (final state, after W1 verification and canon-13 doctrine)

### 00-surface-truth — `arif_kernel_route(mode="surface_truth")` truth adapter
- **Priority:** P0 — **ship first**
- **Status:** Spec drafted, W1-verified, response shape updated with `canonical_tools: 13`, `server_exposed_tools: 16`, `canonical_map` field.
- **Purpose:** Expose a self-orienting truth surface so any future connector (human or AI) can verify what they are and are not seeing through the projected tool surface.
- **Spec:** `forge_work/C1-MCP-NATIVE-SURFACE/SURFACE_TRUTH.md`

### 02-prompts-inventory — 5 Trinity prompts (decision: keep as-is)
- **Priority:** P1
- **Status:** Decision made — 5 prompts, organized by AAA Trinity lane (AGI/ASI/APEX/GATEWAY-IN/GATEWAY-OUT), not 13.
- **Reasoning:** 13 tools = constitutional primitives (per stage). 5 prompts = constitutional roles (per lane). These are different axes, not conflicting counts. Both are valid.
- **The 5:** `000_init` (GATEWAY entry), `111_agi` (AGI tactical), `444_asi` (ASI strategic), `888_apex` (APEX authority), `999_seal` (GATEWAY exit).
- **Spec:** Inline in this manifest. No separate spec file needed.

### 03-mindreason — Schema-locked structured output
- **Priority:** P2
- **Status:** Still needed. LLM-side adaptation, F10 strict-schema stays.
- **Modes:** reason, reflect, verify, critique, debate, socratic, plan, plan_review, plan_ready, axioms (10 modes)

### 04-fl-naming — F/L naming normalization
- **Priority:** P3
- **Status:** Still needed. Migrate L-prefix → F-prefix in error payloads.

### 05-contract-tests — Test harness
- **Priority:** P4
- **Status:** Still needed. Lock the four-witness truth.

### 06-connector-canon-respecting — Connectors report canon, not substrate
- **Priority:** P5
- **Status:** New sub-forge. The OpenClaw connector and others should expose the 13 canon, not the 16 substrate. The `canonical_map` field in surface_truth makes the substrate aliases discoverable but not promoted.

## Sub-forges DELETED (W1 verification showed server already complete)

### ~~01-bridge~~ — DELETED
- **Original purpose:** Tactical manifest mode for `resource://agent/capabilities/raw`.
- **Reason for deletion:** W1 raw probe showed server exposes `arifos://schema`, `arifos://doctrine`, `arifos://identity`, etc. — directly readable. No bridge needed.

### ~~02-resources~~ — DELETED
- **Original purpose:** Add MCP-native resources.
- **Reason for deletion:** W1 raw probe showed 10 first-class resources + 13 URI templates already exposed. Server is complete.

## Constraints (non-negotiable, sealed into the work)

- **Do not disable F12.** F12 = evidence provenance gate.
- **Do not allow arbitrary `resource://` URLs through `arif_evidence_fetch`.** Internal resources go through `arif_kernel_route(mode="manifest")` or MCP-native `resources/read`.
- **Do not loosen strict schemas (F10).** Unknown fields → 888_HOLD. Unknown modes → 888_HOLD.
- **Do not allow gateway relay without L11 verified authority.** F13 sovereignty boundary.
- **Do not allow judge/seal/forge execution without verified authority.** F1 + F13.
- **All sub-forges are reversible** until the full forge work C1-MCP-NATIVE-SURFACE is GREEN-SEALED.
- **Tactical bridges must carry a sunset epoch.** No tactical bridge becomes permanent debt.

## Validation protocol — four-witness model

Every sub-forge is validated against four independent witnesses. All four must agree on the new exposure state, or the sub-forge is HELD until the disagreement is resolved.

| Witness | Source | What it sees | Authority |
|---|---|---|---|
| **W0** | arifOS server itself, via `arif_kernel_route(mode="surface_truth")` | What the system says about itself, pinned to `substrate_sha` | Self-report — honest, but unverified |
| **W1** | MCP Inspector (`npx @modelcontextprotocol/inspector <server>`) | Raw MCP protocol: tools, resources, prompts, notifications | Protocol truth |
| **W2** | Claude Code | Real agent host: resources `@`-referenced, prompts as slash commands, native tool calling | Agent execution truth |
| **W3** | ChatGPT / OpenAI (Responses API MCP) | Projected connector view: tool-calling subset | Compatibility / projection truth |

**Scenarios:**

1. **All 4 agree** — Truth is solid. Sub-forge is GREEN.
2. **W0-W2 agree, W3 sees projected subset Y** — Expected. Document the shadow. Sub-forge is GREEN.
3. **W0 says X, W1 sees nothing** — Server self-report is wrong. Schema mismatch, registration drift, or fabrication. **Critical defect — HELD until resolved.**
4. **W1 sees X, W0 says Y** — Server is under-reporting or W1 is over-reporting. Diagnose.

**Per-sub-forge acceptance criteria additions:**

- 00-surface-truth: "W1 (Inspector) reports `prompts_exposure` and `resources_exposure` values match what `surface_truth` returns."
- 01-bridge: "W1 (Inspector) reports `resource://agent/capabilities/raw` is fetchable via the new `manifest` mode."
- 02-05: All include W1 verification step.

**W3 (ChatGPT) role:** demoted from "MCP truth witness" to **"compatibility witness"**. Useful for cross-platform projection testing. Not the right tool for raw MCP truth.

**Constitutional chain mapping:** This operationalizes the existing `witness_type: ai | human | hybrid` schema field at the host level. The arifOS doctrine already mandates multi-witness; the four-host model is the host-level expression of that mandate.

## Sequencing

| Day | Sub-forge | Reversible? | Notes |
|---|---|---|---|
| **0 (a.m.)** | 00-surface-truth | ✅ | Bounded. Single-mode addition. **Ship first** — every other fix is safer once consumers can call this. |
| 0 (p.m.) | 01-bridge | ✅ | Bounded. Single-mode addition. Sunset epoch baked in. |
| 1 | 02-prompts-resources (sub-forge A: prompts) | ✅ | Touches MCP server contract. |
| 1-2 | 02-prompts-resources (sub-forge B: resources) | ✅ | Migrates tactical bridge. |
| 2 | 03-mindreason | ✅ | F10 strict stays. LLM-side adaptation only. |
| 2 | 04-fl-naming | ✅ | Small refactor. |
| 3 | 05-contract-tests | ✅ | Locks the truth. |
| 3 | GREEN-SEAL of C1-MCP-NATIVE-SURFACE | ⚠️ | **Point of no return.** |
| 4+ | A-FORGE/AAA expansion | — | Federation adoption begins. |

## Sealing protocol

1. **Draft** — Each sub-forge spec is drafted in the workspace (this file + siblings).
2. **Review** — Arif reviews. Hermes interprets. APEXMax audits. (Per Phase Model.)
3. **Seal** — Sub-forge spec is sealed via `arif_vault_seal` with `ack_irreversible=true` and a `judge_state_hash` from a prior SEAL judgment.
4. **Execute** — `arif_forge_execute(mode=engineer)` lands the code per sealed spec.
5. **Verify** — Sub-forge contract tests pass.
6. **Iterate** — Repeat for each sub-forge.
7. **GREEN-SEAL** — When all sub-forges are sealed and tested, the full forge C1-MCP-NATIVE-SURFACE is sealed. A-FORGE/AAA expansion unblocked.

## What this forge does NOT do

- Does not expand A-FORGE/AAA adoption. That comes after GREEN-SEAL.
- Does not change the canonical13 tool list. Tools are not added or removed; modes within tools are added.
- Does not touch GEOX/WEALTH/WELL MCP surfaces. Federation is downstream.
- Does not modify F1-F13 floors. The forge is a surface hardening, not a constitutional change.

---

**Status:** DRAFT — awaiting Arif review and seal.
**Next action:** Generate sub-forge specs in `forge_work/C1-MCP-NATIVE-SURFACE/`.
