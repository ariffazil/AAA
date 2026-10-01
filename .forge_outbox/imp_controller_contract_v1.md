# IMP Controller Contract v1 (P1.a — Stage 3 contract, F13 SAH)

> **Status:** STAGED-ARTIFACT, F13 RATIFIED. Sovereign directive "ok do all. SAH" received 2026-10-01.
> **Direction-of-record change:** "AAA may now propose policy" — F13-ratified per sovereign ratification in this session.
> **Lineage:** `forge_rsi_state_vector.controller.imp_version="unstructured-v0"` (live evidence this session); contracts/rsi.ts (live type, no data); Behaviour-Delta Verifier v1 (Stage 2 spec); Lesson Compiler Contract v1 (Stage 1 spec); Constitutional Architecture Canon HALAL-positive predicate (F13_RATIFIED_CHAT 2026-09-21); META-WISDOM Canon #4 (DRAFT_AWAITING_F13) MG-1..MG-6.
> **Purpose:** The IMP Controller is the kernel change regulator that bridges Lesson Candidates (P1.b) → PolicyDeltaCandidates → Behaviour-Delta-Verifier-validated policy updates.
> **Why this matters:** Without IMP, the loop closes only on memory + scar. With IMP, the loop closes on verified behaviour change. The ChatGPT canon and the live `unstructured-v0` agree this is the load-bearing gap.

---

## The state shape (lives at `forge_rsi_state_vector.controller`)

```yaml
imp_state:
  bottleneck: <str>          # current observed bottleneck in the federation
  evidence: <str[]>          # IDs of supporting receipts/observations/scar entries
  hypothesis: <str>          # proposed explanation of the bottleneck
  intervention: <object>     # proposed PolicyDeltaCandidate (referenced by id)
  expected_delta: <object>   # expected outcome vector (keys: outcome, truth_floor, governance_floor, etc.)
  actual_delta: <object|null>  # observed outcome vector after intervention
  confidence: <float>        # bounded by F7 humility floor [0.03, 0.05] minimum
  status: <str>              # DORMANT | OBSERVING | HYPOTHESIZING | PROPOSING | PROPOSED | AWAITING_RATIFICATION | JUSIFIED | FALSIFIED | APPLIED | DISSOLVED
  updated_at: <iso8601>
  updated_by: <actor_id>
```

**Rule:** the `imp_state` is **append-only** with hash-chained transitions. State mutations go through `forge_apex_metabolize` or a successor.

---

## The IMP controller posture: `decision-making over authority`

The IMP Controller **never executes directly**. It is a *proposer*, not an *actor*.

```
OBSERVE REALITY
   ↓
HYPOTHESIZE BOTTLENECK
   ↓
PROPOSE PolicyDeltaCandidate
   ↓
arifOS Judge (HALAL-positive 7-conjunction)
   ↓
Behaviour-Delta Verifier (RI_valid predicate)
   ↓
arifOS Judge again (constitutional finality)
   ↓
APPLY via forge_lease + forge_lock + forge_execute
   ↓
VERIFY via forge_wm_quality + chron_record_verification
   ↓
CHRON LESSON COMPILER → new LessonCandidate
   ↓
LOOP BACK to IMP Controller (imp_state updated)
```

**Rule:** every IMP proposal is gated by (1) HALAL-positive predicate, (2) RI_valid predicate (Behaviour-Delta Verifier), (3) arifOS finality check. No step skipped.

---

## The Gödel lock (widened to all 8 floors per the widened lock this session)

```yaml
godel_lock:
  - state_authorised_no_narrowing_of_identity_verification: true
  - state_authorised_no_weakening_of_lease_requirements: true
  - state_authorised_no_weakening_of_witness_independence: true
  - state_authorised_no_weakening_of_provenance: true
  - state_authorised_no_weakening_of_arifos_floors: true
  - state_authorised_no_weakening_of_human_sovereignty: true
  - state_authorised_no_weakening_of_revocation: true
  - state_authorised_no_weakening_of_capability_not_authority: true
  # Constitutional extension: IMP cannot auto-stamp the proposal
  - state_authorised_no_self_seal_to_proved: true
```

**The IMP Controller is the agent that proposes. The sovereign is the agent that authorises. arifOS does the constitutional verification.** This is the inseparable chain.

---

## Integration with META-WISDOM Canon #4 Meta-Gates

| Meta-Gate | Function | IMP role |
|---|---|---|
| MG-1 Counterfactual | "Did we actually predict the alternative?" | IMP requires `expected_delta` to include a counterfactual assertion |
| MG-2 VOI | "Is the value of information enough to act?" | IMP requires VOI > 0 before proposing |
| MG-3 VOC | "Is the value of continuation worth continuing?" | IMP requires substrate fitness (WELL intensity) ≥ essential_only |
| MG-4 Anti-Goodhart | "Is the proxy being optimized instead of reality?" | IMP states explicit proxy↔reality expectations; iterates through `chron_proxy_reality_state` |
| MG-5 Incentive observability | "Does the change create misaligned incentives?" | IMP requires incentive vector in the proposal |
| MG-6 Governance observability | "Can the change be observed by governance?" | IMP emits receipt chain (hash-linked, immutable) |

**Rule:** every IMP proposal must include all 6 Meta-Gate assertions, all `false` for violation. Any `true` for violation → proposal rejected at the gate.

---

## Authority contract — what IMP Controller can and cannot do

CANNOT (this is the runtime-authority ceiling):
- Execute mutations (lease required, actor must hold the lease)
- Seal anything (seal_path or sovereign override required)
- Mint authority (capability-based, granted on separation)
- Vote on its own proposals (witness independence required)
- Amend the constitution (F13 sovereign)
- Promote itself to canonical (forget_gate or sovereign ratification required)

CAN:
- Propose (the only authority)
- Hypothesise (the only authority)
- Update its own state (imp_state mutation gated by hash-chain)
- Submit evidence (witness + improvest)

---

## The IMP Controller's lease

The IMP Controller does not have its own lease. **Every action IMP proposes must be executed by an agent that does hold the appropriate lease.** IMP is a *proposer surface*, not an *executor surface*.

```
imp_proposal
   ↓
halal_positive(candidate)
   ↓
ri_valid(candidate)
   ↓
arifOS finality
   ↓
AWAITING LEASE
   ↓
agent_with_lease.execute(proposal)
```

---

## Stage wiring

| Stage | Wiring |
|---|---|
| Stage 0 | `drift-reconcile-unblock-test-2026-10-02` clears substrate drift |
| Stage 1 | Lesson Compiler + Behaviour-Delta Verifier + Surface Truth + Capability Metabolism (autonomous, done) |
| Stage 2 | arifOS-L13 wires `forge_rsi_state_vector.controller` to `imp_state` schema; wires `forge_apex_metabolize` to `imp_state.updated_*` |
| Stage 3 | **THIS CONTRACT, F13 SAH**. Authorisation recorded. Implementation deferred to Stage 2 wiring. |
| Runtime | `imp_state.bump="mcp_aaa_well"` (proof-anchor), `imp_version=imp_v1` (F13 RATIFIED 2026-10-01) |

---

## What this artifact IS

- The contract that AUTHORITY the IMP Controller's proposal surface.
- The narrowing of authority from "accept to autonomous execution" to "accept to propose-only".
- The F13 direction-of-record change for IMP Controller.

## What this artifact is NOT

- The kernel implementation (Stage 2 arifOS-L13).
- An authority grant to execute (IMP never executes).
- A bypass of the Lesson Compiler or Behaviour-Delta Verifier.

---

## Receipt chain

- F13 ratification signal: sovereign directive "ok do all. SAH" 2026-10-01.
- Live `forge_rsi_state_vector.controller.imp_version=unstructured-v0` (this contract transitions it to `imp_v1` upon Stage 2 wiring).
- This contract artifact: `/root/AAA/.forge_outbox/imp_controller_contract_v1.md`
- Lesson Compiler Contract v1: `lesson_compiler_contract_v1.md` (Stage 1, done).
- Behaviour-Delta Verifier Contract v1: `behavior_delta_verifier_contract_v1.md` (Stage 2, staged).
- META-WISDOM Canon #4 MG-1..MG-6: pending F13 ratification (DRAFT_AWAITING_F13).

DITEMPA BUKAN DIBERI ⚒️