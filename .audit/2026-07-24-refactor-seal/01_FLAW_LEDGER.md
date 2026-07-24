# Tool Refinement & Seal — Flaw Ledger (Phase 1 Audit)
**Date:** 2026-07-24T03:37–03:42 UTC
**Actor:** ARIF (canonical, allowlist-confirmed) | **arifOS session:** `SEAL-06af5307b30846ed` (SOVEREIGN, persistent_bound, actor_bound=true)
**Mode:** OBSERVE_ONLY (audit). No mutations performed.
**Authority:** `arifOS` kernel epoch `2026-07-03`, release `a118178`.

---

## 0. EXECUTIVE STATUS

> **HOLD per F1 AMANAH (Reversibility) and the FAIL-CLOSED rule in the task spec.** This ledger enumerates defects and *proposes* repairs. **No tool code, affordance files, or any production path has been mutated.** Phase 2 (Repair) requires explicit **888_HOLD approval** per F13 SOVEREIGN, and Phase 3 (Seal) requires successful verification.

---

## 1. AUDIT METHOD

Read-only scans of:
- A-FORGE: `forge_surface_audit(organ=all, mode=audit)` — 70 tools vs affordances
- GEOX: `geox_surface_status(mode=registry)` — 79 intended, 31 public, 48 internal
- WEALTH: `capital_registry(mode=domains/schema)` — 7 canonical
- WELL: `well_registry_status(mode=full)` — 8 canonical + 14 callable + 6 deprecated
- Direct calls against 9 known-flawed tools (this session + prior benchmarks)
- A-FORGE bug catalog from prior benchmarks (8 known engine pre-check failures)

---

## 2. FLAW CATALOG

### 2.1 [REPAIRABLE] Server runtime bugs

| # | Tool | Organ | Bug | Error | Falsifiable? | Repair class |
|---|---|---|---|---|---|---|
| R-01 | `forge_isomorphism_check` | A-FORGE | engine pre-check TypeError | `Cannot read properties of undefined (reading 'requires_human_approval')` | Yes | actionClassifier.ts: add `requires_human_approval` field |
| R-02 | `forge_fingerprint_check` | A-FORGE | PolicyGate pre-check TypeError | same `requires_human_approval` | Yes | same as R-01 |
| R-03 | `forge_vps_ports` | A-FORGE | PolicyGate pre-check TypeError | same | Yes | same as R-01 |
| R-04 | `forge_vps_services` | A-FORGE | PolicyGate pre-check TypeError | same | Yes | same as R-01 |
| R-05 | `forge_vps_cron` | A-FORGE | PolicyGate pre-check TypeError | same | Yes | same as R-01 |
| R-06 | `forge_status` | A-FORGE | PolicyGate pre-check TypeError | different field: `'length'` | Yes | actionClassifier.ts: array `length` guard |
| R-07 | `forge_filesystem_read` | A-FORGE | PolicyGate pre-check TypeError | same `requires_human_approval` | Yes | same as R-01 |
| R-08 | `forge_skillstore_read` | A-FORGE | PolicyGate pre-check TypeError | same | Yes | same as R-01 |
| R-09 | `forge_wm_quality` | A-FORGE | L4b CLASSIFY UNKNOWN_TOOL | tool not in actionClassifier | Yes | actionClassifier.ts: add forge_wm_quality entry |
| R-10 | `geox_geomechanics` | GEOX | output validation: `None is not of type 'object'` | server bug in `derive_moduli` | Yes | geox_mcp: enforce object return |
| R-11 | `geox_seismic_ingest` | GEOX | server TypeError in segy_metadata handler | `'<=' not supported between 'str' and 'int'` | Yes | geox_mcp: type-coerce numeric fields |
| R-12 | `capital_primitive` (mode=monte_carlo) | WEALTH | alias mismatch | `Unknown mode 'monte_carlo'`. Valid list includes `'mc'` | Yes | wealth_mcp: accept `monte_carlo` as alias for `mc` |
| R-13 | `capital_health` (mode=conservation) | WEALTH | server TypeError in `compute_conservation` | `unsupported operand type(s) for +: 'int' and 'str'` | Yes | wealth_core: defensive type coercion in `compute_conservation` |

**Total: 13 REPAIRABLE bugs. R-01..R-08 share root cause; R-12/R-13 are user-facing.**

### 2.2 [STREAMLINE] Description bloat and description-quality issues

Per the directive: *"Enforce concise 1-line tool descriptions (Use when… prose tax removed)."*

Observed bloat:
- 22+ tools have multi-line descriptions that include the "Use when…" pattern repeated across the tool list.
- The standard 1-line form would reduce description bloat by ~60-70% on average (4-7 lines → 1 line).

Estimated lines of bloat removable: **~140 lines** of duplicated "Use when…" / "OBSERVE-class" / "P2.x canonical gap fill" prose across the federation's tool description surface (counting shared phrases).

**Not in scope for this audit** (no in-place measurements yet): the actual line-count delta must be measured on the per-tool description set in each organ's MCP server. **A-FORGE has 70 tools** (most have rich descriptions); **GEOX 31 public + 48 internal**; **WEALTH 7 canonical + sub-tools**; **WELL 8 canonical + 6 deprecated aliases**.

### 2.3 [DEAD-WEIGHT] Deprecated / duplicate / legacy

| # | Item | Organ | Status | Proposed action |
|---|---|---|---|---|
| D-01 | 6 deprecated_callable: `well_assess_governance`, `well_get_health`, `well_init`, `well_machine_state`, `well_readiness`, `well_state` | WELL | Scheduled for removal 2026-09-01 (per legacy_alias_map) | **Wait for 2026-09-01 per WELL's own deprecation schedule.** No early action — the schedule is sovereign-set. |
| D-02 | 12 internal aliases: `well_000_init`, `well_000_ops`, `well_111_sense`, `well_222_fetch`, `well_333_mind`, `well_444_gateway`, `well_444_kernel`, `well_444_reply`, `well_555_memory`, `well_666_heart`, `well_777_forge`, `well_888_judge`, `well_999_vault` | WELL | Internal only, not in public surface | **Document.** Not dead-weight; canonical GWT-style numbered binding. Leave. |
| D-03 | 48 GEOX internal tools (e.g., `geox_3d_model`, `geox_egs_*`, `geox_simulate_*`, `geox_well_tie_*`, `geox_seismic_cognition`, `geox_visual_enhance`) | GEOX | Internal-only — not in public callable | **Audit each.** Many appear production-grade (EGS claim system, biostrat NN, 3D model) and should be either exposed or removed. **Falsifiable: each must be classified (keep-internal / expose / remove) by 888.** |
| D-04 | `plugin_export_only_tools`: 6 GEOX tools (map_*, visual_*) | GEOX | Exposed in MCP but NOT in app export | **Document discrepancy.** Decide per 888. |
| D-05 | `wealth_cascade_model`, `wealth_institutional_stress_index`, `wealth_governance_capacity`, `wealth_external_exploitation_detect`, `wealth_bridge_run` (when used) | WEALTH | 5 sub-tools callable but not in 7 canonical | **Document.** They appear to be sub-tools of `capital_diagnose`. Confirm and either add to canonical or proxy. |
| D-06 | WEALTH `preload_mechanism: REMOVED_2026-07-07` | WEALTH | Legacy config artifact | **Already removed.** Audit-confirmed. |
| D-07 | `geox_3d_model` (and `geox_3d_model_build`) | GEOX | Internal — appears production | **Verify with 888.** |
| D-08 | 94 PHANTOM findings (per `forge_surface_audit`) | GEOX | The audit says "in affordances.yaml but NOT in registry"; **direct testing contradicts** — these tools are in the registry. Most likely the affordance checker has a stale view, OR the affordances.yaml is incomplete and the description in the audit is inverted. | **Investigate root cause.** Direct evidence: I successfully invoked `geox_petrophysics`, `geox_seismic_compute`, `geox_well_ingest` in the prior benchmark. They exist in the registry. The 94 findings need ground-truthing before any repair. |

### 2.4 [OBSOLETE / DUPLICATE] Possibly

None confirmed in this audit. The aliases in WEALTH (e.g., `mc` vs `monte_carlo`) and WELL (legacy_alias_map) are managed and dated. No true duplicates found.

### 2.5 [STRUCTURAL] Cross-organ issues

| # | Issue | Where | Action |
|---|---|---|---|
| S-01 | `arif_init` mode enum: rejects `internal`, `observe`, `default` (only absence-of-mode works) | arifOS kernel | Document valid modes or drop the parameter |
| S-02 | L11_AUTH in WEALTH has different sub-tool gate paths (some accept session, some don't) | WEALTH | Standardize — every WEALTH sub-tool should require session uniformly |
| S-03 | LANE_ENFORCEMENT and P0_IDENTITY_PROPAGATION overlap in GEOX | GEOX MCP | Consolidate into one lane+identity check |
| S-04 | A-FORGE `forge_registry(mode=list)` returns empty despite A-FORGE having 114 tools | A-FORGE | Server bug — `mode='list'` should return tool list, not empty array |

---

## 3. PROPOSED REPAIR PLAN (NOT YET EXECUTED)

### Phase A — Server runtime bugs (1-line fixes mostly)

For R-01..R-08: a single config patch in `actionClassifier.ts` (or equivalent) to populate `requires_human_approval: false` and array `length` guards. **Falsifiable:** after patch, the 8 tools return data instead of pre-check TypeError.

For R-09: add `forge_wm_quality` to the actionClassifier with action_class=OBSERVE (it's a quality report, not an MUTATE). **Falsifiable:** tool returns report instead of L4b UNKNOWN_TOOL.

For R-10: enforce object return from `geox_geomechanics.derive_moduli`. **Falsifiable:** tool returns a dict with moduli fields.

For R-11: type-coerce numeric fields in `geox_seismic_ingest` segy_metadata handler. **Falsifiable:** tool accepts integer params.

For R-12: add `monte_carlo` to alias map → `mc` in `wealth_mcp`. **Falsifiable:** `mode='monte_carlo'` returns the same as `mode='mc'`.

For R-13: defensive type coercion in `compute_conservation` for asset `value` fields (int→float ok, str→reject with clear error). **Falsifiable:** clean input returns conservation; malformed input returns a structured error, not TypeError.

### Phase B — Affordance drift (94 GEOX findings)

D-08 is the real repair: **investigate the source-of-truth.** Either:
1. Add the missing 70 GEOX tool entries to `tools_sot.yaml`, OR
2. Fix the audit's logic so "PHANTOM" doesn't false-positive.

Direct evidence supports option 1 (the tools work). **Falsifiable:** after patch, `forge_surface_audit` returns 0 drift for GEOX.

### Phase C — Streamline (1-line descriptions)

Edit each tool's `description` in its server source. Replace multi-line with one line. **Falsifiable:** `tools/list` returns descriptions ≤ 200 chars.

### Phase D — Seal verification

For each tool repaired: invoke once successfully, capture chain_hash, verify `_epistemic.envelope` is intact.

---

## 4. ENTROPY DELTA — ESTIMATED (PRE-REPAIR)

| Stream | Lines / items | ΔS |
|---|---:|---:|
| A-FORGE PolicyGate pre-check bugs (8 tools) | 8 source lines | −8 (single config patch removes 8 errors) |
| WEALTH alias + TypeError (2 bugs) | 2 source lines | −2 |
| GEOX None validation (1 bug) | ~5 source lines | −5 |
| GEOX affordance.yaml drift (94 findings) | 94 yaml lines | −94 (if adding 70 missing entries) |
| Tool description bloat | ~140 lines | −140 (if shortening to 1-line) |
| WELL deprecated legacy (6) | 0 | 0 (wait for 2026-09-01) |
| **Total estimated ΔS (lower entropy)** | | **−249** |

Verification gate: every line counted must have a chain_hash audit record (F11).

---

## 5. HOLD PROTOCOL

> Per F1 AMANAH and the task's HARD CONSTRAINT #3: **"Any high-risk or irreversible system mutation MUST be placed on HOLD for 888 confirmation."**

This audit ledger is the **proposed plan**. **No mutations have been made.** The plan requires explicit sovereign approval before Phase A (server runtime bugs) and Phase B (affordance drift) execute. Phase C (description streamline) is **technically reversible** (each tool description can be reverted from git) but still requires approval per the FAIL-CLOSED principle.

**I request one of the following from F13 SOVEREIGN:**

1. **APPROVE all 4 phases** → I will execute per-organ with verification, then seal.
2. **APPROVE Phase A only** (server runtime bugs, 1-line fixes) → Defer Phase B, C to a separate request.
3. **APPROVE Phase A + specific tools in Phase B** → I will execute a narrow scope.
4. **HOLD — review the plan, do not execute** → I will leave the federation in its current state and await further instruction.
5. **REJECT the plan** → I will discard.

**Until sovereign confirmation, no tool is repaired, no tool is sealed, no tool is removed.**

**Live receipts (OBSERVE_ONLY chain):**
- audit session: `SEAL-06af5307b30846ed`
- audit timestamp: 2026-07-24T03:37–03:42 UTC
- audit chain_hashes: see MODE B audit receipts in `/root/AAA/.audit/2026-07-24-domain-benchmark/`

DITEMPA BUKAN DIBERI.
