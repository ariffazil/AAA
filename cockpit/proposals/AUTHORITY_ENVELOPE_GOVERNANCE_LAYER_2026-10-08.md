<!-- DESIGN-ONLY · no mutation executed · status: PROPOSED awaiting F13_SAHH -->
<#authority-envelope-governance-layer>
<#diagnosis: capability > authority asymmetry (8 surface audit, 2026-10-08)>

# Authority Envelope Governance Layer — Constitutional-Class Mutation Hooks

**Status:** PROPOSED · 2026-10-08 · read-only design · awaiting F13_SAHH before any execution
**Author:** FI-003 (333-AGI, DECODEER lane) · **Soal:** asymmetry of Authority vs Capability on 8 surfaces
**One law:** `AuthorityMustBeScarcerThanCapability` [PROPOSED]
**Format rule:** headings + tables + ≤7-bullet lists (Miller) · provenance tag on every claim

---

## 0 · Diagnosis (from live audit, 2026-10-08) [OBSERVED]

8 capability surfaces identified; integrity rails exist (git, sha, audit footer, structured YAML). Authority flow = single-bottleneck (human-Arif approves all). Defect = authority scarcity collapse: agents can propose + verify + stage + execute in one sitting. Envelope remains unratified.

**F13 verbatim:** [PRESERVED ORIGINAL BM]
> *"…aku malas nak type seal acah2 everytime. Hang pandai2 la seal. Seal tu kerja hang. Manusia akan kata sah jaaaaa."*
> — auto-seal directive, 2026-09-24

> *"Jika HOLD dibuang, kau hilang brake. Jika HOLD kekal murah, kau hilang progress."*
> — AAA::SCAR_BINDING_DOCTRINE::v1, 2026-10-06

---

## 1 · Four-Layer Split (operational chain)

| Layer | Who has authority | Required output schema | Fail mode | Bypass? · Audit trail |
|---|---|---|---|---|
| **PROPOSE** | 333-AGI (any lane proposing mutation) | `{intent, target_path, falsifier, blast_radius, reversal_path, evidence_handle, proposed_by, ts}` | **fail-open** with HOLD-tagged receipt | none — proposal is always admissible |
| **VERIFY** | 555-ASI witness (NOT the proposer) | `{proposal_id, observation_source, observed_state, expected_postcondition, ⊨?, observer_identity, by_diff_ms, ts}` | **fail-closed** — missing `⊨` = block | bypass only on `traced_check=NO_PROPOSAL`; audit trail = `verify_skip.jsonl` |
| **APPROVE** | F13 sovereign OR quorum(≥3 of {F13, jitu.py status, chron_calibration_state}) | `{proposal_id, approved_by[], quorum_proof, time_lock_until, sah_checklist[], ts}` | **fail-closed** — missing quorum = HOLD | emergency bypass ONLY if `jitu_actuator.sh apply` cuts lane (see §4) · trail = `override.jsonl` |
| **EXECUTE** | A-FORGE lane (777_EXECUTE) | `{envelope_id, target_hash_pre, execution_hash_post, receipt_vaul999, ts}` | **fail-closed** — TOCTOU mismatch = re-VERIFY | none — zero bypass; revert on receipt anomaly |

**Authority tuple (12 fields, derived from authority-envelope.md):** `⟨ EnvelopeID, Proposer, Verifier, Approver[], Objective, Operation, Scope, Target, Issuer, Expiry, ExpectedPostcondition, Budget, RevocationRef ⟩`. Self-issuance = `VOID`.

---

## 2 · Constitutional-Class Mutations

Targets: `SOUL.md`, `lanes/people.yaml`, `carry_forward.json`, `profiles/*/config.yaml`.

### 2.1 Time-lock & budget [PROPOSED, derived from AAA::NO-HOLD_FLOW_DIRECTIVE_v2]

| Target | Time-lock | Line budget | Side-by-side required |
|---|---|---|---|
| `SOUL.md` | 24h | ≤80 lines / ratification | YES · prior+current, NO auto-diff |
| `lanes/people.yaml` | 12h | ≤40 lines | YES |
| `carry_forward.json` | 6h | ≤25 entries | YES (entry-level diff) |
| `profiles/*/config.yaml` | 6h | ≤60 lines | YES |

Expiry of time-lock requires re-staging from scratch; partial expiry = full re-stage.

### 2.2 Witness triangulation — minimum 3 independent sources [PROPOSED]

All three must return `CONSISTENT=true`. Any dissent = `scar_bind_fail` → HOLD → escalate.

| # | Source | MCP tool | What it attests |
|---|---|---|---|
| 1 | JITU breaker state | `mcp__jitu__status` (fallback: `/root/AAA/federation/kernel/jitu.py status`) | no active trip covering scope |
| 3 | Registry witness | `mcp__hermes_mcp__hermes_registry_status` | target is on organs/soul allow-list |
| 2 | Calibration drift | `mcp__chron__chron_calibration_state` | proposer prediction vs CHRON baseline within tolerance |
| (bonus) | Frame trend | `mcp__frame__frame_trend` | invariant trend over last 24h |

Independence law — `ρ̄→1 ⇒ 3 witnesses = 1 voice`. Witness sources MUST live in separate MCP servers / separate processes.

### 2.3 Sovereign "SAH" template — checklist replaces single word [PROPOSED]

```
SAH = [ dibaca ] [ difahami ] [ tiada alternatif reversible ]
   ↑        ↑             ↑                        ↑
confirm   confirm       confirm                  confirm
read     understood    digest recorded         reversible path exists
```

Single-word "SAH" without all four `[]` ticked = `VOID_SAH`. Receipt MUST record which checkbox was ticked by which sovereign seat. F13 is the only seat authorised to wire mandates.

---

## 3 · Trust-Theater Detection (longitudinal runtime)

| Element | Spec |
|---|---|
| **Invariant** | `same_signature + same_selection_after_new_evidence → scar_bind_fail` |
| **Probing** | varied input prompts (semantic/parametric, NOT literal repeat) targeting same invariant; CHRON episodic memory depth re-runs the probe with disjoint vocabulary |
| **Cadence** | weekly, embedded in `mcp__chron__chron_active_events` schedule (Monday 04:00 MYT) |
| **Output** | regression table — `(invariant_id, baseline_verdict, current_verdict, drift_score)` |
| **Drift threshold** | `drift_score > 0.15` ⇒ escalate to F13 binary; `> 0.40` ⇒ auto-HOLD + scar register |

[DERIVED from apex-geometry-substrate "∂G/∂P binding constraint" + scar-binding-doctrine v1 L2]

---

## 4 · Failure Mode Taxonomy [PROPOSED + F13 verbatim]

| # | Mode | Detection | Defence |
|---|---|---|---|
| 1 | **Stage-then-persuade** (Arif-named risk #7) | staged-patch age < time-lock | time-lock floor (24h SOUL) · sealable only after expiry |
| 2 | **Capability inflation / authority scarcity collapse** | proposer signs own envelope | self-issuer = `VOID`; verifier ≠ proposer mandatory |
| 3 | **Witness corruption** (independent witnesses share state) | `ρ̄` between witnesses > 0.7 | MCP servers must live in separate processes; shared file = `witness_corrupt.jsonl` |
| 4 | **Legitimacy preserved, integrity broken** (the worst state) | receipts green; independence audit shows `UnauthorizedEscapeRate > 0` | weekly frame_drift probe + Qwen red-team law: regression fixture must pass for any mutation path |

> *"…kalau benda tu tambah kerja manusia, ia bukan improvement."* — ARIFOS::ANTI_BANGANG_ENGINEERING::v1, LAW 1

---

## 5 · Backward Compatibility

| Asset | Rule |
|---|---|
| Existing proposals in `/root/AAA/cockpit/proposals/` (18 files, OBS) | preserve · re-stamp with `legacy_unverified` tag; do NOT auto-adopt |
| `/root/AAA/.staged/agents-staging-2026-10-06/*.draft` (3 files, OBS) | require fresh witness pass under new schema before next ratification cycle |
| Existing `carry_forward.json` entries | preserve byte-for-byte; new entries only via APPROVE+EXECUTE |
| `SOUL.md` git history | preserve all refs/tags; constitutional-class mutation = signed tag only (no force-push) |

No silent migration. Legacy items get explicit `legacy_*` provenance and remain subject to current envelope gate.

---

## 6 · Rollout (three phases) [PROPOSED]

| Phase | Smallest executable thing (one sentence) |
|---|---|
| **Phase 1 · paper-only** | Render this doc, tag every existing proposal with `legacy_unverified`, hand-adopt the SAH-checklist when F13 signs anything this week. |
| **Phase 2 · hook layer** | Wire existing `arifOS` hook (`verdicts.py` pre-exec gate) to require `time_lock_until < now ∧ witness_count ≥ 3 ∧ sah_check[] complete` before any constitutional-path write — no new schema, no new MCP. |
| **Phase 3 · runtime** | Activate `mcp__chron__chron_active_events` weekly trust-theatre probe + `mcp__frame__frame_drift` baseline; activation requires explicit F13_SAHH + dry-run receipt for 2 consecutive weeks. |

---

## References (paths only, per request)

- /root/AAA/canon/APEX-REALITY-KERNEL.md
- /root/AAA/canon/APEX-GEOMETRY-SUBSTRATE-2026-10-06.md
- /root/AAA/canon/FAILURE-CLASS-SEPARATION-2026-10-06.md
- /root/AAA/canon/AAA-SCAR-BINDING-DOCTRINE-v1.md
- /root/AAA/canon/ASI-SUBSTRATE-INVARIANTS-2026-10-07.md
- /root/AAA/instructions/authority-envelope.md
- /root/AAA/instructions/capability-rich-authority-poor.md
- /root/AAA/instructions/aaa-scar-binding-doctrine.md
- /root/AAA/instructions/aaa-no-hold-flow-directive-v2.md
- /root/AAA/instructions/anti-bangang-engineering.md
- /root/AAA/instructions/auto-seal.md
- /root/AAA/instructions/sovereign-attention-preservation.md
- /root/AAA/instructions/human-attention-membrane.md
- /root/AAA/federation/kernel/jitu.py
- /root/AAA/canon/A-Z-APEX-ZEN-DOCTRINE.md
- /root/AAA/canon/LANGUAGE-GEOMETRY-GRADIENT-2026-10-06.md