# GEOX-C1-CONSTITUTIONAL-INTEGRATION

**Forge Work ID:** GEOX-C1-CONSTITUTIONAL-INTEGRATION
**Created:** 2026-06-06
**Authoring session:** phase1-stabilize-2026-06-06 (continuation of SEAL-04a16cf53264461c)
**Authoring actor:** arif-fazil-af-forge
**Lane:** AGI
**Stage:** 444 — Kernel Orchestration
**Floor:** C1 (observe/advise) → C2 (execute) gated
**Reversibility:** All sub-forges reversible until GREEN-SEAL of the full forge
**Sunset policy:** Tactical bridges carry a hard sunset epoch. No tactical bridge becomes permanent.
**Precedent:** arifOS C1-MCP-NATIVE-SURFACE (sealed 2026-06-06)
**Parent canon:** GEOX-CANON-31 (sealed 2026-06-06T13:50Z, 30,402 bytes)

---

## Reality (live audit, 2026-06-06T14:06Z)

Probes run against the live GEOX MCP at `http://127.0.0.1:18081` and the OpenClaw connector (`geox_*` tool surface, 36 tools, all callable).

| Surface | Reality | Source |
|---|---|---|
| `geox_system_registry_status` | `registry_truth: PASS, tools_count: 36, contract_version: GEOX-SOVEREIGN-v2026.05.22, contract_epoch: 2026-06-05-GEOX-35TOOLS-v2.0, registry_hash: reg-hash-35d798a` | live W0 self-report |
| `session_id` field in response | `"geox-no-session"` — NOT propagated from caller | live W0 + W2 receipts |
| `actor_id` field in response | `"geox-unknown"` — NOT propagated from caller | live W0 + W2 receipts |
| `constitution_hash` field in response | `"unknown"` — GEOX does not expose its constitution hash | live W0 + W2 receipts |
| `trace_id` field in response | GEOX-generates own (`trace-06da059dfa424b9e`) — works, but disconnected from caller chain | live W0 receipt |
| `registry_hash` field | `"reg-hash-35d798a"` — GEOX has internal hash, but not exposed as constitutional chain anchor | live W0 receipt |
| `contract_epoch` field | `"2026-06-05-GEOX-35TOOLS-v2.0"` — but `tools_count: 36` ⇒ 1 new tool added since epoch bump, unbumped | **REGISTRY DRIFT (NEW FINDING)** |
| `audit_receipt.vault999_ref` | `"VAULT999-PENDING"` — GEOX emits audit receipts but no Vault write happens | live W2 receipt |
| `geox_query_intake` governance | `governance_status: QUALIFY, claim_state: INTERPRETED, maruah_flag: CLEAR` | live W2 receipt |
| Tools callable (W2 connector) | 36/36 — all pass | live W2 probe |
| Tools callable (W1 raw port 18081) | 11 `arif_*` tools — slim arifOS kernel stub, deployment gap (not canon error) | per GEOX-CANON-31 |

## Truth (the invariant)

The **GEOX substrate is solid**: 36 tools, all callable, no phantoms, `physics_guard.guard_passed: true`. The substrate does its job.

The **GEOX constitutional envelope is broken at three connector-side seams**:

1. **Session identity is dropped** — every call gets `session_id: "geox-no-session"`. Constitutional chains cannot form. F1 (Amanah) cannot track provenance per session. F11 (Authority) cannot verify caller authority.

2. **Actor identity is dropped** — every call gets `actor_id: "geox-unknown"`. arifOS's actor binding (e.g., `arif-fazil-af-forge`) does not propagate. Sovereign attribution is lost. F13 (Sovereignty) cannot enforce per-actor floors.

3. **Constitution hash is unrevealed** — every call gets `constitution_hash: "unknown"`. GEOX has internal hashes (`registry_hash`, `geox_version`, `contract_epoch`) but does not expose a constitutional hash that ties to a known external canon. F10 (Ontology) cannot cross-validate GEOX outputs against a frozen doctrine.

A **4th finding (NEW, surfaced during this audit)**: `tools_count: 36` does not match `contract_epoch: "2026-06-05-GEOX-35TOOLS-v2.0"`. One tool was added without bumping the epoch. This is registry drift — same class of defect as the `runtime_drift` issue we just resolved in arifOS. Must be folded into this forge work.

The **constitutional chain is broken end-to-end**: caller → OpenClaw connector → GEOX substrate → response → Vault. None of the three identity fields survive the journey. Every GEOX tool call is constitutionally anonymous.

## Sub-forges

### 01-connector-identity-propagation — OpenClaw → GEOX envelope
- **Priority:** P0 — **ship first**
- **Status:** SPEC DRAFT
- **Purpose:** Modify the OpenClaw GEOX connector to inject `session_id` and `actor_id` into every outbound GEOX tool call. Read from the caller's envelope (arifOS session binding or direct).
- **Spec:** `forge_work/GEOX-C1-CONSTITUTIONAL-INTEGRATION/CONNECTOR_IDENTITY.md`
- **Acceptance:** A GEOX tool call from a sealed session returns `session_id: SEAL-...` (not `"geox-no-session"`) and `actor_id: arif-fazil-af-forge` (not `"geox-unknown"`).
- **Reversible:** ✅ — connector is a tactical bridge with sunset epoch-2026.09.

### 02-constitution-hash-exposure — GEOX constitutional anchoring
- **Priority:** P1
- **Status:** SPEC DRAFT
- **Purpose:** GEOX exposes its own constitutional anchor — a `constitution_hash` derived from the frozen doctrine file (e.g., `sha256(GEOX_CANON.md)`). Either compute at response time (slow but fresh) or embed at deploy (fast, frozen).
- **Spec:** `forge_work/GEOX-C1-CONSTITUTIONAL-INTEGRATION/CONSTITUTION_HASH.md`
- **Acceptance:** Every GEOX response includes `constitution_hash: sha256:...` matching the hash of the deployed `GEOX_CANON.md`. Mismatch → `888_HOLD`.
- **Two design options:**
  - (a) **Frozen at deploy** — hash computed at install time, baked into response. Fast, deterministic.
  - (b) **Live digest** — hash computed from doctrine file at response time. Fresh, but ~5-10ms overhead per call.
  - **Recommendation:** (a) Frozen. Doctrines are sealed, not edited mid-flight.
- **Reversible:** ✅ — the hash is a metadata field, not a behavior change.

### 03-registry-drift-fix — `tools_count` ↔ `contract_epoch` alignment
- **Priority:** P1
- **Status:** SPEC DRAFT
- **Purpose:** Fix the registry drift: `tools_count: 36` vs `contract_epoch: 35TOOLS-v2.0`. Add CI guard that fails the build if `tools_count` ≠ epoch-implied count. Bump `contract_epoch` to `2026-06-06-GEOX-36TOOLS-v2.1` to absorb the new tool.
- **Spec:** `forge_work/GEOX-C1-CONSTITUTIONAL-INTEGRATION/REGISTRY_DRIFT.md`
- **Acceptance:** `geox_system_registry_status` reports `tools_count == 36` AND `contract_epoch` ends with `36TOOLS`. Mismatch → `888_HOLD` (consistent with arifOS drift detection pattern).
- **Reversible:** ✅ — pure metadata fix.

### 04-vault-receipt-completion — close the audit loop
- **Priority:** P2
- **Status:** SPEC DRAFT
- **Purpose:** GEOX emits `audit_receipt.vault999_ref: "VAULT999-PENDING"`. The Vault write never happens. Two options:
  - (a) **OpenClaw connector proxies the Vault write** — connector receives GEOX audit receipt, forwards to arifOS Vault999. Closer integration, more code.
  - (b) **GEOX writes to a local SQLite/JSONL queue** — local receipt store, picked up by a federation cron. Looser integration, no federation surface.
  - **Recommendation:** (b) for now. Same pattern as arifOS's local outcomes.jsonl. Federation-level Vault sealing is a Phase 3 concern.
- **Spec:** `forge_work/GEOX-C1-CONSTITUTIONAL-INTEGRATION/VAULT_RECEIPT.md`
- **Acceptance:** Every GEOX tool call produces a record in `/var/log/geox/receipts.jsonl` (or similar). Format: `{timestamp, session_id, actor_id, tool_name, claim_id, vault_ref: VAULT999-PENDING-or-sealed}`. Federation cron rolls up PENDING → sealed on `arif_vault_seal` success.
- **Reversible:** ✅ — local queue, no federation contract change.

### 05-contract-tests — four-witness lock
- **Priority:** P3
- **Status:** PENDING (gated on 01-04)
- **Purpose:** Lock the new envelope with contract tests. 1 test per sub-forge × 4 witnesses = 16 tests. Pattern mirrors arifOS C1-MCP-NATIVE-SURFACE `05-contract-tests`.
- **Spec:** `forge_work/GEOX-C1-CONSTITUTIONAL-INTEGRATION/05-contract-tests-spec.md`
- **Acceptance:** All 16 tests pass. Any test failure → forge is HELD.
- **Reversible:** ✅ — tests are additive.

## Constraints (non-negotiable, sealed into the work)

- **Do not break the 36-tool callable surface.** All existing `geox_*` calls must keep working.
- **Do not loosen `physics_guard`.** `guard_passed: true` stays. The 5th affordance (`dim_spot_flag`) stays encoded.
- **Do not collapse the 3 truth classes** (FACT / INTERPRETATION / SPECULATION). The `claim_state` semantics stay.
- **Do not allow GEOX to compute on non-geological inputs.** The metaphor boundary clause (`F10 ONTOLOGY` floor) is constitutional, not a feature flag.
- **Do not promote tactical bridges to permanent debt.** The OpenClaw connector, the slim arifOS at port 18081, and any new local-receipt queue all carry a sunset epoch.
- **All sub-forges are reversible** until the full forge work GEOX-C1-CONSTITUTIONAL-INTEGRATION is GREEN-SEALED.

## Validation protocol — four-witness model

Same as C1-MCP-NATIVE-SURFACE. Every sub-forge is validated against four independent witnesses.

| Witness | Source | What it sees | Authority |
|---|---|---|---|
| **W0** | GEOX self-report via `geox_system_registry_status` | What GEOX says about itself | Self-report — honest, unverified |
| **W1** | Raw MCP at `http://127.0.0.1:18081` (direct JSON-RPC) | Raw protocol: tool names, response envelopes | Protocol truth |
| **W2** | OpenClaw connector (the 36 `geox_*` tools) | What AI agents actually see | Agent execution truth |
| **W3** | DEFERRED — see GEOX-C6-PROJECTION-CHECK | Projected connector view (e.g., ChatGPT) | Compatibility — out of scope for C1 |

**Scenarios:**
1. **W0 = W1 = W2** — Truth is solid. Sub-forge is GREEN.
2. **W0 says X, W2 says Y** — Connector is dropping the identity field. **Critical defect — HELD until 01-connector-identity-propagation lands.**
3. **W0 reports new tool but epoch not bumped** — Registry drift. **HELD until 03-registry-drift-fix lands.**
4. **W1 raw sees different tool count than W2 connector** — Slim arifOS kernel stub at port 18081. **Documented as deployment gap, not canon error** (per GEOX-CANON-31).

**Per-sub-forge acceptance additions:**
- 01-connector: "W2 connector call from a sealed session returns `session_id != 'geox-no-session'` AND `actor_id != 'geox-unknown'`."
- 02-constitution-hash: "W0 + W1 + W2 all return the same `constitution_hash` value."
- 03-registry-drift: "W0 reports `tools_count == N` AND `contract_epoch` contains `NTOOLS`."
- 04-vault-receipt: "Local receipt queue row count == W2 tool call count (within 60s window)."
- 05-contract-tests: "16/16 tests pass."

## Sequencing

| Day | Sub-forge | Reversible? | Notes |
|---|---|---|---|
| **0** | 01-connector-identity-propagation | ✅ | Bounded. Single connector change. **Ship first** — every other fix is safer once caller identity survives. |
| 0 | 03-registry-drift-fix | ✅ | Bounded. Metadata only. Can ship same day as 01. |
| 1 | 02-constitution-hash-exposure | ✅ | Bounded. Doctrine hash embedding. |
| 1-2 | 04-vault-receipt-completion | ✅ | Local queue + federation cron. No federation contract change. |
| 2 | 05-contract-tests | ✅ | Locks the truth. |
| 2 | GREEN-SEAL of GEOX-C1-CONSTITUTIONAL-INTEGRATION | ⚠️ | **Point of no return.** Sub-for 08 (claim lifecycle) and arifOS `arif_judge_deliberate` upgrade unblock. |
| 3+ | GEOX-C2 through GEOX-C8 | — | Federation adoption begins. |

## Sealing protocol

1. **Draft** — Each sub-forge spec is drafted in the workspace (this file + siblings).
2. **Review** — Arif reviews. Hermes interprets. APEXMax audits. (Per Phase Model.)
3. **Seal** — Sub-forge spec is sealed via `arif_vault_seal` with `ack_irreversible=true` and a `judge_state_hash` from a prior SEAL judgment.
4. **Execute** — `arif_forge_execute(mode=engineer)` lands the code per sealed spec.
5. **Verify** — Sub-forge contract tests pass.
6. **Iterate** — Repeat for each sub-forge.
7. **GREEN-SEAL** — When all sub-forges are sealed and tested, the full forge GEOX-C1-CONSTITUTIONAL-INTEGRATION is sealed. Phase 1 GREEN-SEAL unblocks. Phase 2 (GEOX-C2 through C8) begins.

## What this forge does NOT do

- Does not add new tools to GEOX. The 36 are the canon; this forge only fixes the envelope.
- Does not change GEOX behavior or `physics_guard` semantics. Pure envelope hardening.
- Does not promote the OpenClaw connector to permanent. Sunset epoch-2026.09 holds.
- Does not federate Vault999 across organs. Local receipt queue, not federation contract.
- Does not bump the GEOX canon count. Still 36 tools, still 5 affordances, still 1 metaphor boundary clause.
- Does not collapse truth classes or weaken F1-F13 floors. Floors stay strict.

## Identity one-liner (re-affirmed from canon-31)

> "GEOX is a physics leash that lets AI agents touch earth evidence without pretending language is geology."

This forge work makes the leash **traceable**: every call now carries the identity of who is holding it.

## Status

**DRAFT — 2026-06-06T14:07Z**

**Next action:** Generate sub-forge specs in `forge_work/GEOX-C1-CONSTITUTIONAL-INTEGRATION/`. Ship 01-connector-identity-propagation first (P0).

**Blocked:** `arif_judge_deliberate` SEAL/AT_* modes still return 888_HOLD (LEGACY_WRAP gate). Same F11 FederationEnvelope gate as the arifOS canon-13 work. This forge does not unblock the judge; it unblocks GEOX identity propagation, which is a prerequisite for the judge upgrade.

---

**Forge Work P1 of GEOX forge stack (P1-P8).** Closes the 3 connector-side constitutional gaps + the new registry drift finding.
