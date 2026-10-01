# Trajectory Curator Blocker Route v1 (P2.b)

> **Status:** STAGED-ARTIFACT, FOR EXECUTION. F13 directive "ok i approve, sah, jalan and go" received 2026-10-01.
> **Lineage:** `forge_wm_quality` live evidence (this session): `phase2_ready=false, trajectories=22/100, eligible=21/50, tools=3/3, blockers=["GRPO implementation", "Harbor-style agent harness for forge_* tools", "Docker sandboxes for safe rollout execution", "Task-completion verifier (reward model)"]`; BIJAKSANA Appendix A T1/T2/T3 tiered items; Trilogy Gap §3.2 `mcpjam_unreachable`; META-WISDOM Canon #4 MG-1/MG-4 (counterfactual, anti-Goodhart).
> **Purpose:** Sequence the four live blockers into a T1/T2/T3 priority order with the correct constitutional gate at each step. The artifact says `Verifier → Curated trajectories → Replay sandbox → Counterfactual evaluation → only then learning algorithm` — we route that artifact's order against the existing T1/T2/T3 canon.
> **Why this matters:** `forge_wm_quality` has been at 22/100 trajectories since 2026-07-21 (chain `last_hash=d53ab81b...` updated then). Self-training cannot start until `phase2_ready=true`.

---

## The four live blockers (verbatim from `forge_wm_quality`)

1. `GRPO implementation needed`
2. `Harbor-style agent harness for forge_* tools`
3. `Docker sandboxes for safe rollout execution`
4. `Task-completion verifier (reward model)`

Plus two federation-state blockers from Trilogy Gap §3.2:
5. `mcpjam_unreachable` at 127.0.0.1:6274 — federation-OBSERVE inspector channel offline
6. `arifOS_kernel_arif_think_rejected_session_token` (L11 SCT mismatch) — this session's sovereign-chat ratification is the live evidence of this gap

---

## T1/T2/T3 priority order — the canonical routing

### T1 (already-implementable, just needs naming + execution)

| # | Blocker | WAJIB mapping | Path |
|---|---|---|---|
| **T1.a** | **Task-completion verifier (reward model)** | BIJAKSANA #16 Confidence/calibration + #53 Calibration loop (both MISSING) | **PATH GOES FIRST.** ChatGPT's own canonical order says `Verifier → Curated trajectories → Replay sandbox → Counterfactual evaluation → only then learning algorithm`. Without the verifier, all downstream labels are self-produced and noisy. Start here. The reward model is the lowest-leverage name; the *real* work is the predicate `outcome_observed ∧ outcome_expected → reward ∈ [-1, 1]`. |
| **T1.b** | **Harbor-style agent harness for forge_\* tools** | BIJAKSANA P12 governance observability (T1) | The harness is observability for the trajectory execution surface, not new agent infrastructure. The artifact calls it "safe rollout harness", which maps to the existing `forge_sandbox_run_image`, `forge_sandbox_pause/resume` — extend these with capability-set awareness. |

### T2 (needs design)

| # | Blocker | WAJIB mapping | Path |
|---|---|---|---|
| **T2.a** | **GRPO implementation** | BIJAKSANA P3 (VOI gate) + P4 (VOC gate) | **PATH GOES SECOND.** GRPO needs the verifier (T1.a) and the harness (T1.b) to be alive; otherwise it optimises against self-produced labels. Per the artifact, the correct order is *not* GRPO-first. |
| **T2.b** | **mcpjam_unreachable reconciliation** | (Trilogy Gap §3.2; no WAJIB mapping yet) | Two reconciliations: (i) probe the missing inspector channel from a different lane; (ii) if MCPJam is genuinely offline, declare it so rather than pretending. |

### T3 (significant engineering, post-MVP)

| # | Blocker | WAJIB mapping | Path |
|---|---|---|---|
| **T3.a** | **Docker sandboxes for safe rollout execution** | BIJAKSANA P7 (distribution-shift detector, T3) + #32-completeness (MISSING) | The sandbox is a runtime environment, not a policy gate. The Constitutional Architecture Canon's `ReversibleWithinBand` predicate already governs this; the sandbox is a stage, not a gate. Stage-2 arifOS-L13 build. |
| **T3.b** | **L11 SCT mismatch (this session)** | Constitutional Architecture Canon's HALAL-positive predicate `Authorized ∧ Provenanced` | Live: this session uses sovereign-chat ratification as fallback path (per A-Z Doctrine 2026-09-13 precedent). Drift-reconcile-unblock-test-2026-10-02 is the scheduled falsification event. |

---

## Why this order

The artifact's claim: `Verifier → Curated trajectories → Replay sandbox → Counterfactual evaluation → only then learning algorithm`. 

What this artifact adds (Canon #0 + Constitutional Architecture):

1. **T1.a (verifier) goes first** — without it, every other label is self-produced noise.
2. **T1.b (harness) goes second** — observability for the trajectory surface.
3. **T2.a (GRPO) is reserved for after T1 is alive** — the artifact explicitly says "do not start serious GRPO/self-training yet".
4. **T3.a (Docker sandbox) and T3.b (L11 SCT reconcile) are infrastructure concerns**, not learning-algorithm concerns. Stage 2 arifOS-L13 BUILD.

The artifact's "Counterfactual evaluation" stage is missing in the current `forge_wm_quality` blockers. META-WISDOM Canon #4 MG-1 (counterfactual) is the missing-piece. Add to T2: T2.c = `counterfactual evaluator`.

---

## Stage mapping (canonical)

| Blocker | Path | Stage | Owner |
|---|---|---|---|
| T1.a Task-completion verifier | Stage 1 autonomous (predicate spec) | 2026-10-02 target | Kimi/FI-008 |
| T1.b Harbor-style harness | Stage 1 autonomous (capability-set extension) | 2026-10-03 target | Kimi/FI-008 |
| T2.a GRPO | Stage 2 arifOS-L13 build (kernel predicate) | 2026-10-30 target | arifOS-L13 |
| T2.b mcpjam reconciliation | Stage 2 arifOS-L13 build (tool-finder probe) | 2026-10-15 target | arifOS-L13 |
| T2.c Counterfactual evaluator | Stage 2 arifOS-L13 build (MG-1 lineage) | 2026-11-01 target | arifOS-L13 |
| T3.a Docker sandboxes | Stage 3 (significant engineering, post-MVP) | 2027-Q1 target | arifOS-L13 |
| T3.b L11 SCT reconcile | Stage 0 + Stage 3 (drift-reconcile-unblock-test-2026-10-02) | 2026-10-02 falsification | arifOS-L13 |

---

## What this artifact is NOT

- Not a Stage 0 blocker (drift-reconcile-unblock-test-2026-10-02 is the Stage 0 gate).
- Not an authority grant.
- Not a kernel implementation; only the contract above is Stage 1 autonomous.

---

## Receipt chain

- `forge_experience_trace trace_id=exp-1790838115433-1790836981647` (audit trace)
- `forge_wm_quality` live evidence at the moment of write (22/100, 21/50, 3/3, 4 blockers)
- This contract artifact: `/root/AAA/.forge_outbox/trajectory_curator_blocker_route_2026-10-01.md`

DITEMPA BUKAN DIBERI ⚒️