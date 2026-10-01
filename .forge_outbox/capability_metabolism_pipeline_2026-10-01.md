# Capability Metabolism Pipeline v1 (P3)

> **Status:** STAGED-ARTIFACT, FOR EXECUTION. F13 directive "ok i approve, sah, jalan and go" received 2026-10-01.
> **Lineage:** `forge_ephemeral` (live); `forge_skillstore_read/write` (live); HUMA bridge §5 row 2 ("HUMA bridge already-named in canon: progressive disclosure"); BIJAKSANA Appendix B rule (governance complexity is haram); META-WISDOM Canon #4 MG-4 (anti-Goodhart); Six-Graph Federation Model (F13_RATIFIED_CHAT 2026-09-16).
> **Purpose:** Darwinian pipeline for capabilities — gap → ephemeral capability → sandbox → mission → independent verification → reuse count → promotion OR dissolution. Permanent capability must be **earned by repeated usefulness**, not accumulated because an agent once needed it.
> **Why this matters:** A-FORGE has 122 unique tools. ChatGPT's canon notes "Intelligence ≠ Tool Count". Without metabolism, tool entropy grows faster than the agent's ability to reason over the surface.

---

## The seven stages

```
[1] capability_gap
   ↓
[2] ephemeral_tool
   ↓
[3] sandbox_invocation
   ↓
[4] mission_use
   ↓
[5] independent_verification
   ↓
[6] reuse_count_threshold
   ↓
[7] promotion_candidate OR dissolution
```

Append-only log; stages (visibility, duration, ability to reason over the surface).

---

## Stage 1 — capability_gap

**Trigger:** `forge_wm_gaps` flags a tool with severity ≥ CRITICAL or surprise ≥ 0.7 + experience_traces < 3.
**Output:**
```json
{
  "capability_gap_id": "cg-{hash8}",
  "tool": "forge_X",
  "severity": "CRITICAL",
  "surprise_score": 1.0,
  "experience_traces": 0,
  "feedback_coverage": 0,
  "detected_at": "2026-10-01T...",
  "detected_by": "forge_wm_gaps",
  "promotion_target": "ephemeral_tool"
}
```

**Rule:** every CRITICAL-flagged gap MUST produce one `capability_gap`. Insufficient → rejected at the gate.

**Why:** Constitutional Architecture Canon `Provenanced` conjunct. The capability_gap is the witness that a tool was missing.

---

## Stage 2 — ephemeral_tool

**Trigger:** capability_gap → spawn.
**Mechanism:** `forge_ephemeral mode=run(template_id=..., capability_need=..., tool_id=..., invoke_args=...)`.
**Output:**
```json
{
  "ephemeral_tool_id": "et-{hash8}",
  "source_capability_gap_id": "cg-...",
  "tool_id": "et-{hash8}",
  "template_id": "...",
  "capability_need": "...",
  "lifecycle": "ephemeral",
  "ttl_default": "default_expiry_per_mcp_type_max",
  "auto_dissolution": true,
  "registered_at": "2026-10-01T..."
}
```

**Rule:** ephemeral tool has **no upstream identity**; cannot affect the federation registry; cannot escalate authority. TTL is bounded by capability lifetime. Auto-dissolution on TTL expiry if no evidence of usefulness.

**Why:** `forge_ephemeral` is the substrate. The Darwinian pressure comes from the auto-dissolution gate.

---

## Stage 3 — sandbox_invocation

**Trigger:** ephemeral_tool + 1 mission call.
**Mechanism:** `forge_sandbox_run_image stage_id=etalon(image=..., test_suite=..., resource_limits=..., absolute_timeout_ms=...)`.
**Output:**
```json
{
  "sandbox_run_id": "sr-{hash8}",
  "source_ephemeral_tool_id": "et-...",
  "stage_id": "etalon",
  "image": "...",
  "test_suite": "...",
  "outcome": "PASS" | "FAIL" | "TIMEOUT" | "ERROR",
  "outcome_class": "OBSERVED",
  "run_at": "2026-10-01T..."
}
```

**Rule:** every ephemeral tool **must** complete at least one sandbox invocation before any production mission use. Sandbox pass ≠ production pass.

**Why:** HUMA bridge Law 5 — a refutation stage is a governance organ. The sandbox is the falsifier.

---

## Stage 4 — mission_use

**Trigger:** sandbox PASS.
**Mechanism:** tool is exposed at the registry under ephemeral_id; restricted to the original mission until reuse_count ≥ threshold.
**Output:**
```json
{
  "mission_use_id": "mu-{hash8}",
  "source_ephemeral_tool_id": "et-...",
  "mission_id": "...",
  "scope": "session",
  "use_count_this_mission": 1,
  "success_count_this_mission": 1,
  "first_used_at": "2026-10-01T..."
}
```

**Rule:** mission_use is bounded by `scope = session | memory_tier | grant_reasoning | budget | confidence_calibration | reversible_heuristic`. **No** kind is `META_CLAIM` or `IDENTITY` — those are policy-changing and go through `arifOS Judge` first.

**Why:** Constitutional Architecture Canon's `godel_lock_checked` pattern. Mission_use is reversible_heuristic-or-similar, never identity-changing.

---

## Stage 5 — independent_verification

**Trigger:** reuse_count ≥ 3 across ≥ 2 distinct missions.
**Mechanism:** a tool with a different attestation chain reviews the ephemeral tool's evidence. Per HUMA bridge Law 5: the verifier cannot be the same actor that proposed the capability_gap.
**Output:**
```json
{
  "independent_verification_id": "iv-{hash8}",
  "source_ephemeral_tool_id": "et-...",
  "verifier_actor_id": "...",
  "verifier_organ": "public_api",
  "verification_class": "REPLAY" | "PROBE" | "DOCUMENT",
  "verdict": "PASS" | "FAIL" | "INSUFFICIENT",
  "verdict_at": "2026-10-01T..."
}
```

**Rule:** the verifier MUST be a different actor and a different attestation chain than the proposer. Self-verification is rejected at the gate.

**Why:** HUMA bridge Law 5 + Constitutional Architecture Canon's `Independence` predicate. Witness independence is constitutional.

---

## Stage 6 — reuse_count_threshold

**Trigger:** independent_verification = PASS.
**Mechanism:** Count mission_use records ≥ 5 across different organ IDs, each successful, over ≥ 7 days.
**Output:**
```json
{
  "reuse_threshold_id": "rt-{hash8}",
  "source_ephemeral_tool_id": "et-...",
  "reuse_count": 5,
  "distinct_organs": ["forge_shell", "forge_git", "well_observe"],
  "distinct_days": 9,
  "success_rate": 0.85,
  "threshold_met": true,
  "computed_at": "2026-10-01T..."
}
```

**Rule:** threshold is **5 reuses, 3 distinct organs, 7 days, 0.7 success rate**. Below threshold → no promotion candidate.

**Why:** survival-of-evidence. ChatGPT's "must earn by repeated usefulness, not accumulated because an agent once needed it" maps to this threshold.

---

## Stage 7 — promotion_candidate OR dissolution

**Two outcomes:**

#### A. Promotion candidate (threshold met + independent_verification = PASS)

**Mechanism:** `forge_skillstore_write operation=PROMOTE artifact_id=... tags=[...]`.
**Output:**
```json
{
  "promotion_candidate_id": "pc-{hash8}",
  "source_ephemeral_tool_id": "et-...",
  "artifact_id": "...",
  "tags": ["promoted", "verified_useful"],
  "promotion_route": "PUBLIC_SKILLSTORE",
  "promotion_at": "2026-10-01T..."
}
```

**Rule:** promotion candidate **must** carry `tags=[promoted, verified_useful]` AND `promotion_route ∈ {PUBLIC_SKILLSTORE, ORGAN_SKILLSTORE, FEDERATION_SKILLSTORE}`. **Route ≠ anonymous → rejected.**

#### B. Dissolution (TTL expired OR reuse below threshold)

**Mechanism:** `forge_ephemeral mode=dissolve(...)`.
**Output:**
```json
{
  "dissolution_id": "dis-{hash8}",
  "source_ephemeral_tool_id": "et-...",
  "reason": "ttl_expired | reuse_below_threshold | avoid_tool_entropy",
  "disposed_at": "2026-10-01T..."
}
```

**Rule:** every ephemeral tool gets a dissolution event. No silent disappearance.

**Why:** BIJAKSANA Appendix B — governance complexity is haram. Silent accumulation is haram.

---

## Promotion to canonical (above Stage 7)

A promotion candidate from Stage 7 becomes canonical only after `forge_skillstore_write operation=PROMOTE` + sovereign ratification. **No** auto-promotion. (Immutable in Constitutional Architecture Canon HALAL-positive predicate `Authorized`.)

---

## Anti-patterns (BIJAKSANA Appendix B extension)

| Anti-pattern | Defect |
|---|---|
| Tool accumulation without dissolution | Tool entropy |
| Promotion without independent_verification | Single-actor witness collapse |
| Promotion without reuse_count_threshold | Survival-of-vocabulary amplification |
| Ephemeral tool granted authority beyond AUTO | Capability-like vs authority non-equivalence |
| Message that says "this is the future of federation" without a promotion_id | Ghost capability |

---

## Live substrate snapshot (this session)

- `forge_ephemeral`: present (mode=run / inverse / mcmc)
- `forge_sandbox_run_image`: present (stage_id required)
- `forge_skillstore_read/write`: present (operation=READ required query ≥3 chars; operation=WRITE required)
- `forge_wm_gaps`: present (severity filter, limit, with experience cross-ref)
- `forge_wm_quality`: present (phase2_ready false, 22/100 trajectories, 4 named blockers)

**Promotion gate: live in substrate. Promotion-to-canonical gate: requires sovereign ratification.**

---

## Receipt chain

- `forge_experience_trace trace_id=exp-1790838115433-1790836981647` (audit trace)
- This contract artifact: `/root/AAA/.forge_outbox/capability_metabolism_pipeline_2026-10-01.md`

DITEMPA BUKAN DIBERI ⚒️