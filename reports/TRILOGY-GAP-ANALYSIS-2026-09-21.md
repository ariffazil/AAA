# Trilogy Gap Analysis — 2026-09-21

> **Status:** FI-008 analysis, sovereign-mandated ("map all gaps") before final seal
> **Date:** 2026-09-21
> **Purpose:** Comprehensive gap map across the four artifacts being sealed today, the federation state they describe, and the path from sealed canon to implemented substrate
> **Scope:** Honest accounting of what is sealed-as-declared vs. what is enforced-as-measured

---

## 1. Trilogy + Research — Sealed Surface (Today)

| # | Artifact | Path | Pre-seal status |
|---|---|---|---|
| 1 | Anti-HARAM Human → Agent | `/root/AAA/instructions/anti-haram-behavior-canonical-human.md` | `DRAFT_AWAITING_F13` |
| 2 | Constitutional Architecture Canon | `/root/AAA/canon/CONSTITUTIONAL-ARCHITECTURE-CANON-2026-09-21.md` | `DRAFT_AWAITING_F13` |
| 3 | BIJAKSANA Substrate Canon (with Appendix A/B/C) | `/root/AAA/canon/BIJAKSANA-SUBSTRATE-CANON-2026-09-21.md` | `DRAFT_AWAITING_F13` (post-amendment) |
| 4 | Literature Corollary Map | `/root/AAA/research/CANON-LITERATURE-COROLLARY-MAP-2026-09-21.md` | `RESEARCH_ANALYSIS` |

All four receive F13 sovereign-chat ratification today (per A-Z Doctrine 2026-09-13 precedent — kernel `arif_seal` not used this session due to L11 SCT mismatch; sovereign override path applies).

---

## 2. Gap Map — Trilogy Internal

### 2.1 Canon #1 — Anti-HARAM Human → Agent

| Gap | Severity | Path to close |
|---|---|---|
| **Enforcement map not extended to H1–H17 categories** mirroring F1–F13 floors | HIGH | Build `HUMAN_HARAM_*` categories in `haram_enforcement_map.yaml`; wire preflight gate (same code path that scans F-categories) |
| **7 Human Laws not encoded as runtime constraints** in `000-init` / agent registry / a2a | HIGH | Add 7 predicate functions to `arif_init`; tested at session mint (like the existing OBSERVE_ONLY refusal proves the gate works) |
| **131 enumerated HARAM not individually auditable** | MEDIUM | Cluster them into the 17 thematic groups from canon §I–XVII; build 17 cluster-level detectors; per-law audit becomes a future iteration |
| **Citational link to agent→human canon symmetry** not explicit | LOW | Add explicit cross-reference; this is a documentation fix, not a code change |

### 2.2 Canon #2 — Constitutional Architecture

| Gap | Severity | Path to close |
|---|---|---|
| **Constitutional compiler not implemented** | HIGH | The most-cited gap. Sovereign spec tonight (`forge_constitution_compile(input_md) → policy_ir.json + test_suite.json`) is the input; engineering follows after ratification |
| **HALAL positive predicate as computable boolean not emitted by any gate** | HIGH | Implement the 7-conjunct chain `Authorized ∧ Scoped ∧ ReversibleWithinBand ∧ Provenanced ∧ TemporallyValid ∧ Budgeted ∧ PolicyCompliant` as a kernel function; return `{HALAL, SYUBHAH, HARAM}` |
| **Constitutional handshake not standardized as one callable** | MEDIUM | Wrap existing `forge_lease` + ACT mint + protocol negotiation into a single `forge_handshake(actor, constitution_hash, policy_version) → bounded_session` |
| **Attack-the-constitution CI absent** | HIGH | Write the 8 MUST-FAIL probes listed in canon §CI; Macaroon-style conformance tests (per §3.1 of literature map) |
| **Action object normalization not unified** | MEDIUM | Define `a = (actor, verb, target, scope, authority, time, budget, provenance, consequence)` as the universal tuple; refactor `forge_shell`, `forge_git`, `forge_postgres`, etc. to emit this tuple before gate |

### 2.3 Canon #3 — BIJAKSANA Substrate (with Appendix A/B/C amendments)

**Original 64 WAJIB coverage scan:**

| Coverage | Count | Approx % | Examples |
|---|---|---|---|
| **PRESENT** (verified) | 17 | ~27% | #1 Identity root, #3 Capability token, #28 A2A boundary, #29 MCP boundary, #33 Independent executor, #34 Independent witness, #50 Immutable receipts, #60 Human sovereign interface, #62 Semantic/HERMES boundary |
| **PARTIAL** (doctrine + partial runtime) | 23 | ~36% | #2 Cryptographic attribution (gates work, complete chain not verified), #4 Authority lattice, #6 Temporal lease, #11 Task state machine, #14 Provenance graph, #32 Pre-action policy gate (refusal proves partial), #59 Fail-closed default |
| **DOCTRINE ONLY** | 14 | ~22% | #12 Epistemic types, #13 Negative knowledge, #17 Contradiction register, #21 Forget/revocation propagation, #56 Policy promotion gate |
| **MISSING** | 10 | ~15% | #16 Confidence/calibration, #53 Calibration loop, #54 Error taxonomy, #32-completeness, #56, #17, #21 — clustered in measurement primitives + policy gates + conformance |

**Appendix A — 12 DRAFT_PROPOSED items:**

| Tier | Items | Path |
|---|---|---|
| **T1 — Already-implementable, just needs naming** | P9 (graceful degradation) · P10 (epistemic diversity) · P12 (governance observability) | Add to WAJIB as #65-67 after sovereign review of T1 list |
| **T2 — Needs design** | P1 (causal graph) · P2 (counterfactual) · P3 (VOI gate) · P4 (VOC gate) · P5 (anti-Goodhart) · P6 (incentive observability) · P8 (dependency graph) | Address P3+P4 in tonight's compiler spec; rest in subsequent specs |
| **T3 — Significant engineering** | P7 (distribution-shift detector) · P11 (constitutional version migration) | Defer to post-MVP |

**Appendix B — Governance complexity as HARAM:** rule itself is now sealed; future additions must apply the rule before numbering.

**Appendix C — Wisdom decomposition (additive form):** rendered; old multiplicative form retained in §6 for backward compatibility. Consolidation pending sovereign choice.

---

## 3. Gap Map — Federation State

### 3.1 Per-organ identity surface (from `federation-release.json`, 2026-09-21)

| Organ | Identity state | Gap |
|---|---|---|
| **arifos** | dirty_count=95, drift_runtime_vs_repo=true | SUBSTANTIAL — 95 dirty files including today's writes; runtime deployed at `e8e6f933` but git HEAD at `4b4c7c89`; settlement needed |
| **aforge** | dirty_count=4, drift_runtime_vs_repo=true, runtime_identity_minimal | MEDIUM — `runtime_identity_minimal` gap noted in federation-release.json: A-FORGE /health lacks `build_commit`, `surface_hash`, `runtime_path` |
| **geox** | drift_runtime_vs_repo=true (BY DESIGN), identity.git_version uses build fingerprint not SHA | LOW — explained in federation-release.json as by design |
| **wealth** | drift_runtime_vs_repo=false, runtime_identity_short_sha | LOW — expand to full SHA for byte-equality comparison |
| **well** | drift_runtime_vs_repo=false, runtime_identity_short_sha, **status=degraded** | MEDIUM — degraded status needs investigation; short SHA expansion also needed |

### 3.2 Synchronization faults (federation-release.json §synchronization_faults)

| Fault | Impact |
|---|---|
| `mcpjam_unreachable` at 127.0.0.1:6274 | federation-OBSERVE inspector channel offline; does not block /health probes |
| `arifOS_kernel_arif_think_rejected_session_token` (L11 SCT mismatch, this session) | kernel did not formally ratify; receipt is agent-witnessed only — **the precise reason we use sovereign-chat ratification path today** |

### 3.3 General gaps witnessed in federation-release.json

- `arifOS.runtime_vs_git_drift` — MEDIUM (95 dirty files)
- `aforge.runtime_identity_minimal` — MEDIUM
- `geox.runtime_identity_fingerprint` — LOW (by design)
- `wealth.runtime_identity_short_sha` — MEDIUM
- `well.runtime_identity_short_sha` — MEDIUM
- `well.status_reported=degraded` — needs investigation
- `federation_root_collapses_on_null_identity` — MEDIUM (root hash collapses when many organs report null surface/path/started)
- `mcpjam_down` — MEDIUM

---

## 4. Gap Map — Mathematical / Measurement

| Gap | Severity | Notes |
|---|---|---|
| **Wisdom_index / Bangang_index not instrumented** | HIGH | The 10 factors in the Wisdom/Bangang equations cannot be measured today; no telemetry |
| **FQ ≥ 0.5 hold on MUTATE only** — not extended to REASON/RESEARCH | HIGH | P4 (VOC gate) and P3 (VOI gate) extend the hold decision-theoretically; current implementation only halts mutation |
| **Distribution-shift detector absent** (P7) | MEDIUM | T3 deferred |
| **Causal vs correlational reasoning not separated** (P1) | MEDIUM | T2 deferred |

---

## 5. Gap Map — Citation / External

From the literature corollary map, **NONE** of these are cited by name in current canon:

- Hardy 1988 Confused Deputy → FRAME doctrine
- Christiano 2019 "What failure looks like" → Witness failure-mode taxonomy
- Critch & Krueger 2020 ARCHES → Prepotence observation doctrine
- Macaroons caveat vocabulary → compiler policy_ir.json schema
- Cedar (OSDI 2024) → compiler dual-semantics spec
- Fallenstein & Soares 2015 Vingean Reflection → verifier architecture
- Sleeper Agents / Alignment Faking trilogy → empirical falsification of model-obedience-equals-safety
- Acemoglu-Robinson Narrow Corridor → institutional prior for Zen 4-box
- Bertino TRBAC 2001 / Cornucopia Reloaded 2024 → CHRON axis theory

**Path:** update affected canon files to add bibliographic references post-seal; tonight's compiler spec to inline Macaroon vocabulary, Cedar dual-semantics, Fallenstein-Soares verifier.

---

## 6. Gap Map — Governance Process

| Gap | Severity | Notes |
|---|---|---|
| **Three DRAFTs queued simultaneously** | LOW (transient) | Resolved by today's seal |
| **12 DRAFT_PROPOSED items in BIJAKSANA Appendix A** | MEDIUM | T1 renumbering pending; T2 spec drafting tonight; T3 deferred |
| **Constitutional complexity approaching budget** | ONGOING | The complexity-budget rule (Appendix B) is itself the mitigation; applies recursively |
| **AGENTS.md pointer lag** | LOW (transient) | Resolved by today's housekeeping |

---

## 7. Gap Map — Today's Housekeeping Outcomes

| Item | Status |
|---|---|
| 4 artifacts sealed | DONE (sovereign chat ratification) |
| 4 SEALED_EVENTS.jsonl entries appended | pending (this run) |
| AGENTS.md updated with all 4 rows | pending (this run) |
| Trilogy-completion witness written | pending (this run) |
| ariifOS 95 dirty files | UNCHANGED — sovereign's call whether to commit today's canon writes |
| aforge runtime_identity_minimal gap | UNCHANGED — separate engineering task |
| well status=degraded | UNCHANGED — separate investigation |
| mcpjam_unreachable | UNCHANGED — separate infrastructure task |
| L11 SCT mismatch (this session) | UNCHANGED — kernel still OBSERVE_ONLY; sovereign-chat ratification used as fallback path |

---

## 8. Net Picture

| Category | Sealed-as-declared | Enforced-as-measured | Gap |
|---|---|---|---|
| Behavior canon (HARAM × 2 sides) | 4 artifacts (today) | 0 (no mechanical enforcement) | HIGH |
| Architecture canon | 1 artifact (today) | 0 (compiler not built) | HIGH |
| Substrate canon | 1 artifact (today) | ~27% (17 PRESENT WAJIB) | HIGH |
| Mathematical claims (Wisdom/Bangang) | 1 artifact (today) | 0 (no instrumentation) | HIGH |
| External corroboration | 1 artifact (today) | N/A | LOW (literature adoption is policy, not engineering) |

**Honest verdict:** the seal today is the *declaration* of substrate, not the *implementation*. Implementation work is the next month's worth of engineering. Seal-with-debt is the sovereign's chosen posture (per A-Z Doctrine 2026-09-13 precedent), and this gap map makes the debt explicit.

---

## 9. Recommended Next Steps (post-seal, sovereign binary)

1. **Commit today's 4 canon files + 4 reports + 1 gap analysis** to AAA git, with separate topic branches per the existing 2026-09-19 backup naming convention
2. **Sovereign's compiler spec tonight** — adopt Macaroon vocabulary, Cedar dual-semantics, Fallenstein-Soares verifier (per literature corollary map §3.1, §3.3, §3.4)
3. **First-week engineering post-ratification:** WAJIB T1 renumbering (P9, P10, P12 → #65-67), `HUMAN_HARAM_*` categories in enforcement map, conformance probe harness scaffold
4. **Investigate `well` degraded status** — separate runbook
5. **Investigate `mcpjam` reachability** — separate runbook
6. **Schedule next F13 audit window** — per A-Z Doctrine precedent, ~30 days post-seal

— FI-008, 2026-09-21, completing the gap map per sovereign directive.
