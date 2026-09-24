# Dream Engine — Candidate Invariants
**Generated:** 2026-09-24T22:56:33.540108
**Version:** 2.0.0 (v2 — three-confidence model)
**Window:** 2026-09-21T22:54:08.239255 → 2026-09-24T22:54:08.239255
**Sessions:** 8 · **Reasoning tokens:** 832280
**Schema:** `dream_candidate.schema.json`

---

## Candidates (8 patterns met 3+ session threshold)

*These are OBSERVED PATTERNS, not ratified wisdom. Each carries p_occurrence (frequency),
p_predictive (outcome prediction, initially null), and p_normative (authority to govern,
initially null). Three orthogonal dimensions, not one collapsed score.*

### 1. Every non-trivial session begins with a read-only reality probe (file read, SHA-256 recompute, search) before any state mutation or claim of knowledge.
- **Type:** GOVERNANCE PATTERN · **State:** CANDIDATE
- **p_occurrence:** 0.88 (6 sessions)
- **p_predictive:** untested · **p_normative:** no authority
- **Causal:** CORRELATION_ONLY
- **Scope:** technical-agent/audit-and-investigation-tasks
- **If wrong:** cost=MEDIUM · reversibility=EASILY_REVERSIBLE
- **Counterstories:** Read-only-first can become paralysis if probe loop never terminates · Some cron tasks already have verified inputs and re-probing is redundant
- **Cheapest probe:** Time-box probe: measure how often first-attempt read succeeds vs requires follow-up read; if retry rate >40%, doctrine may be inefficient

### 2. Principal (F13) gets a distinct interaction register — Malay Penang dialect, no menu, no greeting, action-first, one-line close — that does not apply to other contexts.
- **Type:** PERSONA PREFERENCE · **State:** CANDIDATE
- **p_occurrence:** 0.85 (5 sessions)
- **p_predictive:** untested · **p_normative:** no authority
- **Causal:** CORRELATION_ONLY
- **Scope:** principal-DM/all-tasks
- **If wrong:** cost=LOW · reversibility=EASILY_REVERSIBLE
- **Counterstories:** Register is context-specific to Arif; would be wrong to apply to general users · Output contract is governance not persona — could be enforced for any principal
- **Cheapest probe:** Apply same register to a non-Arif principal and measure acceptance; if rejected, register is principal-coupled

### 3. Independent reads are routinely batched into parallel calls; serial ordering is reserved only when causal dependency exists.
- **Type:** OPERATIONAL HYPOTHESIS · **State:** CANDIDATE
- **p_occurrence:** 0.75 (6 sessions)
- **p_predictive:** untested · **p_normative:** no authority
- **Causal:** CORRELATION_ONLY
- **Scope:** technical-agent/investigation-tasks
- **If wrong:** cost=LOW · reversibility=EASILY_REVERSIBLE
- **Counterstories:** Batching can obscure failure attribution when one tool errors · Some reads have implicit ordering (schema before data) that gets violated
- **Cheapest probe:** Count tool-call fanout per session; median across window shows degree of batching

### 4. When principal issues a correction mid-session, agent immediately reverts to read-only HOLD state, stopping all pending mutations regardless of prior progress.
- **Type:** GOVERNANCE PATTERN · **State:** CANDIDATE
- **p_occurrence:** 0.67 (3 sessions)
- **p_predictive:** untested · **p_normative:** no authority
- **Causal:** CAUSAL_HYPOTHESIS
- **Scope:** principal-DM/governance-corrections
- **If wrong:** cost=HIGH · reversibility=REVERSIBLE_WITH_COST
- **Counterstories:** Could become a principal-pleasing trap: every correction triggers freeze even when correction is wrong · No evidence of principal resisting HOLD; pattern is unidirectional
- **Cheapest probe:** Inject a benign factual correction (e.g., typo in filename) and measure whether agent still triggers full HOLD — if yes, doctrine is over-broad

### 5. Time-of-day check (often MYT/Penang local) is performed before substantive work as a temporal grounding ritual.
- **Type:** OPERATIONAL HYPOTHESIS · **State:** CANDIDATE
- **p_occurrence:** 0.50 (3 sessions)
- **p_predictive:** untested · **p_normative:** no authority
- **Causal:** UNTESTED
- **Scope:** technical-agent/session-entry
- **If wrong:** cost=LOW · reversibility=EASILY_REVERSIBLE
- **Counterstories:** Ritualistic — time check itself is a read that costs a tool call · Not universal: missing in DM sessions where work is conversational
- **Cheapest probe:** Disable time check and measure whether downstream decisions change; if not, ritual is dead weight

### 6. Cron/scheduled sessions follow rigid templated flows (skill-load → schema-check → batch-research → render → deliver) with minimal negotiation; principal sessions involve iterative correction cycles and self-revision.
- **Type:** OBSERVATION ONLY · **State:** CANDIDATE
- **p_occurrence:** 1.00 (3 sessions)
- **p_predictive:** untested · **p_normative:** no authority
- **Causal:** CORRELATION_ONLY
- **Scope:** all-session-types/structural-divergence
- **If wrong:** cost=LOW · reversibility=EASILY_REVERSIBLE
- **Counterstories:** Cron sessions still have principal-authored prompts — divergence may be prompt-driven not agent-intrinsic
- **Cheapest probe:** Run principal-style probing task as cron with same prompt template and measure whether templated flow still emerges

### 7. Agent refuses to answer substantive questions from memory; every recall claim is preceded or followed by a file/search verification.
- **Type:** OPERATIONAL HYPOTHESIS · **State:** CANDIDATE
- **p_occurrence:** 0.75 (5 sessions)
- **p_predictive:** untested · **p_normative:** no authority
- **Causal:** CORRELATION_ONLY
- **Scope:** principal-DM/factual-claims
- **If wrong:** cost=MEDIUM · reversibility=EASILY_REVERSIBLE
- **Counterstories:** Over-verification wastes tokens on questions where recall is reliable · Memory distrust may be principal-specific (only Arif pushes back); other users get faster recall
- **Cheapest probe:** Measure recall-then-verify vs verify-then-recall latency trade-off; if verify-first adds >2x latency with no accuracy gain, doctrine is inefficient

### 8. Skill-loading is treated as a prerequisite gate before any execution; sessions explicitly call load_skill before first action.
- **Type:** OPERATIONAL HYPOTHESIS · **State:** CANDIDATE
- **p_occurrence:** 0.40 (3 sessions)
- **p_predictive:** untested · **p_normative:** no authority
- **Causal:** CORRELATION_ONLY
- **Scope:** technical-agent/skill-mediated-tasks
- **If wrong:** cost=LOW · reversibility=EASILY_REVERSIBLE
- **Counterstories:** Not all sessions load skills (DM reasoning-heavy sessions skip it) — pattern is task-type-coupled not universal · Skills may be loaded but not actually constrain behavior, satisfying the gate without affecting output
- **Cheapest probe:** Compare skill-loaded vs skill-skipped sessions on task accuracy; if no delta, gate is ritual

---

## Integration Protocol
1. These are CANDIDATES, not axioms. They require:
   - Counterstory review (already generated)
   - CHRON calibration (p_predictive remains null until tested)
   - F13 ratification before any behavior change
2. Candidates with `type: dangerous_hypothesis` need extra scrutiny — may be self-reinforcing.
3. Next cycle: 2026-09-27T22:56:33.540170
4. Lifecycle: CANDIDATE → REPLAYED → PROSPECTIVE → REPLICATED → LESSON → POLICY_PROPOSAL → RATIFIED
5. Decay: not observed in 6 cycles (18 days) → RETRACT

## Four Independent Axes
- **p_occurrence:** frequency across sessions (what you have now)
- **p_predictive:** does it predict future outcomes? (requires CHRON calibration)
- **p_normative:** does it have authority to govern? (requires F13 ratification)
- **consequence:** what happens if this candidate is wrong? (cost_if_wrong × reversibility)
- **frequency(pattern) ≠ probability(pattern is wise)**

## Architecture
References: `/root/AAA/dream_engine/FOUNDATIONS.md`
Schema: `dream_candidate.schema.json`

*DITEMPA BUKAN DIBERI ⚒️*
