# INIT_FORGE_RITUAL — Closed-Loop Constitutional Pipeline

> **Status:** BLUEPRINT v0 (sovereign 2026-10-02)
> **Doctrine:** forge-to-seal MUST be closed loop, not "enter root → mutate ad-hoc"
> **Authority during this session:** OBSERVE_ONLY. Not production-wired.

---

## 0. Closed-Loop Promise

```
ROOT_0
  → 000 INIT
  → CONTRACT
  → FORGE
  → VERIFY
  → 888 JUDGE
  → MUTATE (only on judge-SEAL)
  → 999 VAULT-SEAL
  → ROOT_1
```

One mission = one constitutional session spine. Every organ gets **same session_id / governed context**.

---

## 1. Canonical Flow (11 stages)

```
000 INIT        → arifOS / forge_session_init    [session_id, act_v1, lease]
111 SENSE       → AAA                            [bounded task]
222 OBSERVE     → organs                         [facts + unknowns]
333 COLLAPSE    → AAA_Q_COLLAPSE                 [NEXT_PATH]
401 DECLARE     → A-FORGE AUTH                   [task_id + acceptance criteria]
501 LEASE/LOCK  → arifOS + A-FORGE              [valid bounded execution scope]
777 FORGE       → A-FORGE                       [diff/artifact in workspace]
555 VERIFY      → independent verifier           [verified result]
888 JUDGE       → arifOS                        [SEAL/HOLD/SABAR/VOID]
777 ACT         → A-FORGE crosses boundary       [merge/deploy if JUDGE-SEAL]
999 WITNESS     → FRAME/CHRON/domain            [observed outcome]
999 VAULT-SEAL  → arifOS VAULT999               [seal ID/hash]
SESSION_CLOSE   → arifOS                        [closed session]
RETURN          → shell                         [root@forge:~#]
```

---

## 2. Two Distinct "Seal" Meanings (CONSTITUTIONAL)

| Type | What it means | When |
|---|---|---|
| **JUDGE-SEAL** (888) | "This proposed consequential action is constitutionally permitted." | Permission to act |
| **VAULT-SEAL** (999) | "This is what actually happened, witnessed and immutably recorded." | Historical truth |

```
JUDGE-SEAL = permission
FORGE      = consequence
VERIFY     = reality check
VAULT-SEAL = historical truth receipt
```

---

## 3. INIT Contract (must produce these fields)

```yaml
session_id: <SEAL-...>
kernel_origin: true | false
actor: arif
authority_band: OBSERVE_ONLY | LIMITED_MUTATE | FULL_MUTATE | SEAL
actor_verified: true | false
pre_minted_lease:
  lease_id: <LCL-...>
  scope: [forge_filesystem, forge_vault, forge_seal, ...]
  max_action_class: OBSERVE | MUTATE | DEPLOY | SEAL
  ttl_seconds: <1800 default>
  expires_at: <unix ms>
```

**One front door (sovereign 2026-10-02):** `ROOT → forge_session_init → kernel-born session`.

- If caller has governed arifOS session already → propagate authority context (parent_session_id + same ACT), do NOT mint independent.
- If starting directly from ROOT → use legal A-FORGE proxy path that proxies arifOS, returns kernel-born session + ACT + bounded lease.
- One mission = one constitutional session spine. No organ may invent its own session.

**Naming correction (sovereign 2026-10-02):**
- **BUILD/STAGE** = sandbox construction (before 888)
- **777 FORGE** = constitutionally authorized consequence (after 888)
- "777 before 888" = confusion; reserve 777 for actual authorized consequence.

---

## 4. Organs Provide Evidence, Not Votes

| Organ | Question | Authority they have |
|---|---|---|
| AAA | What deserves attention? | Display + Q-COLLAPSE proposal |
| HERMES | What does this mean? Contradictions? | Evidence only |
| CHRON | When? Temporal consequence? Calibration? | Evidence + carry-forward |
| WELL | Is substrate fit to act? | Evidence only |
| WEALTH | Resource / capital cost? | Evidence only |
| GEOX | Earth-domain reality constraint? | Evidence only |
| arifOS 888 | Is this constitutionally authorized? | **JUDGE** |
| A-FORGE | Execute the authorized consequence | **EXECUTE** |
| FRAME | Witness the actual consequence | **WITNESS** |
| VAULT999 | Immutable history | **RECORD** |

Each organ answers ONE question. None of them may vote on each other.

---

## 5. DECLARE Before Mutation (AUTH contract)

```yaml
task:
  id: AAA_QC_REPLAY_V0
objective: prove Q-COLLAPSE executable contract
class: MUTATE
target: /root/AAA
reversible: true
acceptance:
  - deterministic case passes
  - uncertain case chooses information probe
  - sovereign case HOLDs correctly
  - production untouched
evidence:
  - diff
  - tests
  - logs
  - receipt
merge:
  require_888_seal: true
final_seal:
  required: true
```

---

## 6. FORGE Two Worlds

```
FORGE
   │
   ├── WORKSPACE / sandbox (bounded lease)
   │     mutation okay within lease
   │     produces diff/artifact
   │     ↓
   │     TEST
   │     ↓
   │     EVIDENCE
   │     ↓
   │     VERIFY
   │     ↓
   │     JUDGE ──SEAL────►  PRODUCTION / canonical
   │
   └── PRODUCTION / canonical (only post-judge-SEAL)
         merge / deploy / mutation
```

Boundary:
```
worktree/sandbox ──→ canonical/production  (Judge is the gate)
```

`SEAL(action_A)` ⊭ `Authority(action_B)`.

---

## 7. Forge Evidence Packet (before 888)

```yaml
task_id: AAA_QC_REPLAY_V0
prediction:
  expected_result: ...
  expected_delta: ...
change:
  diff_hash: ...
  artifact_hash: ...
verification:
  tests_passed: ...
  tests_failed: ...
  independent_verifier: ...
risk:
  reversible: true
  blast_radius: low
  unresolved_unknowns: [...]
runtime:
  source_commit: ...
  built_commit: ...
  deployed_commit: ...
witness:
  receipts: [...]
```

Then: EVIDENCE → 555 VERIFY → 888 JUDGE.

**Self-certification is not independent verification.** 555 must be independent.

---

## 8. JUDGE Decision Tree

```
888 arif_judge
  ├── HOLD    → stop; preserve workspace/evidence
  ├── SABAR   → wait/gather condition
  ├── VOID    → reject candidate
  └── SEAL    → exactly this action authorized
```

No SEAL means:
- NO MERGE
- NO DEPLOY
- NO IRREVERSIBLE CONSEQUENCE

---

## 9. After JUDGE-SEAL: A-FORGE Crosses Boundary

Then:
```
888 SEAL verdict
  ↓
A-FORGE
  ├── commit (within approved scope)
  ├── merge (if approved)
  ├── deploy (if approved)
  └── restart (if approved)
```

NOT arbitrary follow-on actions. Capability envelope binds:
- what
- where
- who
- how long
- blast radius
- approved action hash

---

## 10. Reality MUST Be Checked Again After Execution

```
A-FORGE executes
  ├── runtime verify
  ├── CHRON actual vs expected
  ├── WELL substrate consequence
  ├── domain organ verification
  └── FRAME / evidence witness
```

Only then: CLAIM = OBSERVED REALITY.

**git commit succeeded ≠ DONE.**

---

## 11. 999 VAULT-SEAL (Final)

```yaml
arif_seal(
  mode="seal",
  payload: <final evidence bundle>,
  session_id: <same SEAL-*>,
  constitutional_chain_id: <888 chain>,
  judge_state_hash: <888 state>,
  seal_purpose: "...",
  ack_irreversible: true
)
```

Must contain enough to reconstruct:
```
intent → state before → candidate → authority
       → change → verification → actual consequence
       → final state
```

---

## 12. SESSION_CLOSE (final)

```
999 VAULT-SEAL
  ↓
SESSION_CLOSE (arif_seal mode=session_close)
  ↓
lease ends / session terminal state
  ↓
agent client returns/exits
  ↓
root@forge:~#
```

**LOCK release before 999 (sovereign 2026-10-02):**

Once consequence verified or safely rolled back, release shared operational locks. Don't strand a lock just because historical sealing hasn't completed.

```
OUTCOME VERIFY (command success ≠ outcome success)
  │
  ├─ FAIL ─→ rollback/HOLD + evidence
  │
  ▼
RELEASE SHARED LOCK
  │
  ▼
999 VAULT-SEAL (records "lock released" state)
```

---

## 14. UX for Arif

```
root
  ↓
"I want X"
  ↓
agents carry the whole governed loop
  ↓
ONE human interruption only if sovereignty required
  ↓
sealed outcome + short receipt
  ↓
root
```

---

## 15. ROOT_RETURN_SURFACE (minimal)

```
ARIF / AAA ROOT
AUTH     VERIFIED · session closed
────────────────────────────────────────────

✓ SEALED
task      <one-line task name>
888       SEAL · cc_...
999       seq=<id> · hash=<hash>
outcome   <one-line observed outcome>
time      <MYT>

🔥 BURNING
<one named item, or "none">

⏳ WAITING
<oldest sovereign decision + age, or "none">

↔ SOURCE≠RUNTIME
<material divergences, or "none material">

◷ HUD
FRESH / WARM / STALE / TAMPER · <age>

────────────────────────────────────────────
SEALED · <N> sovereign decisions remain
```

OR (if nothing requires):

```
SEALED · no sovereign action required
```

Then stop.

---

## 16. One Critical Live Discovery (sovereign 2026-10-02, RETRACTED)

**Initial claim (sovereign's first observation):** A-FORGE forge_session_init with kernel_session passed from arifOS arif_init:
- ERR_ACT_SIGNATURE_INVALID
- HMAC-SHA256 signature mismatch

**Re-verification (live 2026-10-01 22:38 MYT):** forge_session_init standalone **PASS**:
- session_id: SEAL-a7e0c267f23c4b8e
- kernel_origin: true
- actor_verified: true
- authority: LIMITED_MUTATE
- pre_minted_lease: 1800s TTL, scope=[forge_filesystem...8 ops], max_action_class=MUTATE

**Sovereign retracted 2026-10-02:** "ACT signature failure NOT REPRODUCED on current path."

**Ingress asymmetry remains:** direct arif_init from outside A-FORGE may fall to OBSERVE_ONLY, but legal A-FORGE proxy path works. Audit later, not blocker.

**Next engineering target:** Make full root-to-root loop execute once on deliberately trivial reversible task and prove:

```
ROOT_0 → one governed consequence → 999 → ROOT_1
```

with no phantom transition, no second authority, no stale lock, no human option dump.

---

## 17. Architecture Summary

```
ROOT_0
  ↓
000 INIT → one constitutional session
  ↓
OBSERVE → domain evidence
  ↓
Q_COLLAPSE → one proposed next action
  ↓
AUTH DECLARE → bounded mutation contract
  ↓
LEASE + LOCK → execution scope
  ↓
777 FORGE → diff/artifact in workspace
  ↓
555 VERIFY → independent verification
  ↓
888 JUDGE → SEAL/HOLD/SABAR/VOID
  ↓
(if SEAL) A-FORGE crosses boundary → consequence
  ↓
REALITY VERIFY → witness actual outcome
  ↓
999 VAULT-SEAL → immutable record
  ↓
SESSION_CLOSE
  ↓
ROOT_1 (only this much)
```

---

## 18. Sovereign Promise (one line)

> Every completed cycle must leave Arif with less uncertainty and less attention debt than when it started — not merely another receipt.

---

## 19. Held for Production

- Wire to arifOS as constitutional organ
- Fix ACT_GATE HMAC signature handoff (real defect between arifOS + A-FORGE)
- A-FORGE mutation wiring
- /opt crossing
- AGENTS.md propagation
- 888 reservation OR F13 ratification

[reproduce: /root/AAA/cockpit/INIT_FORGE_RITUAL.md]
[reproduce: /root/AAA/cockpit/receipts/RECEIPT_Q_COLLAPSE_REPLAY_2026-10-02.md]
[reproduce: /root/arifOS/arifosmcp/runtime/verdict.py — CANONICAL_VERDICTS]