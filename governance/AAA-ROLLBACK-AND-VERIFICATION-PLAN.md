---
status: DRAFT_PROPOSAL (PATCH_READY; awaiting governed commit path)
date: 2026-09-14
parent_campaign: AAA Federation Housekeeping
---

# AAA Rollback and Verification Plan

> Status: DRAFT_PROPOSAL — rollback strategy for every housekeeping patch, plus verifier contract.
> No mutation.

---

## Rollback strategy (per patch class)

| Patch class | Rollback method |
|---|---|
| Documentation commit (T1) | revert commit hash or remove file |
| Agent card migration (T1) | revert; WARGA STATUS files retain originals via tombstone markers |
| Identity binding into kernel (T2) | revert; arifOS engineer can also revert registry entry |
| Alias tombstone (T2) | Remove tombstone marker file; original alias file remains unchanged |
| Alias final retire (T3, F13) | Reserved for sovereign explicit ack; rollback requires sovereign ack too |
| Capability grant (T3, F13) | A-FORGE lease revocation; APEX/888 review |

Universal rule: every patch is reversible until sovereign explicit ack converts to irreversible.

---

## Verification contract (per committed patch)

For any patch marked READY in the backlog, the verifier lane MUST:

1. Compute SHA-256 of every file in the diff
2. Verify Git working-tree status matches the declared diff exactly
3. Confirm no additional files are included (no scope drift)
4. Validate content safety:
   - no PII or intimate profiles
   - no unsupported SEAL or READY or COMPLETED claims
   - no hidden identity or capability mutation instructions
   - no unbounded alias deletion
5. Validate status terminology:
   - DRAFTED, PROPOSED, NOT_WIRED, PENDING, HOLD only
   - reject SEAL or READY or COMPLETED where inappropriate
6. Produce verification receipt:
   - hashes (SHA-256)
   - repository and branch
   - changed paths
   - content-safety result
   - independent-review verdict
   - recommended next state

---

## Allowed verdicts (verifier lane)

- READY_FOR_GOVERNED_COMMIT_REVIEW
- HOLD_CONTENT_CORRECTION_REQUIRED
- HOLD_SCOPE_DRIFT
- HOLD_ADDITIONAL_FILES_DETECTED
- HOLD_EVIDENCE_INCOMPLETE

No write performed. Verifier lane is read-only.

---

## Acceptance gate (before any commit)

A legitimate commit requires:

```
Valid Session
  AND
Correct Actor Binding
  AND
Scoped arifOS Judgment (if arifOS state changes)
  AND
Bounded A-FORGE Lease (if mutation)
  AND
Independent Review
  AND
Reversible Diff
```

Documentation-only commits may have a lower tier (T1) but still require the binding chain above.

---

## Specific rollback for THIS campaigns drafts

| File | Rollback |
|---|---|
| AAA-MODEL-INIT-v1.md | remove governance/AAA-MODEL-INIT-v1.md |
| AAA-DUPLICATION-AND-ALIAS-MATRIX.md | remove governance/AAA-DUPLICATION-AND-ALIAS-MATRIX.md |
| AAA-AGENT-ROLE-AND-AUTHORITY-MATRIX.md | remove governance/AAA-AGENT-ROLE-AND-AUTHORITY-MATRIX.md |
| AAA-FEDERATION-ENTROPY-INVENTORY.md | remove governance/AAA-FEDERATION-ENTROPY-INVENTORY.md |
| AAA-CONTEXT-AND-MEMORY-HYGIENE-MATRIX.md | remove governance/AAA-CONTEXT-AND-MEMORY-HYGIENE-MATRIX.md |
| AAA-NOISE-AND-ATTENTION-ECONOMY-AUDIT.md | remove governance/AAA-NOISE-AND-ATTENTION-ECONOMY-AUDIT.md |
| AAA-DEPRECATION-TOMBSTONE-PLAN.md | remove governance/AAA-DEPRECATION-TOMBSTONE-PLAN.md |
| AAA-PATCH-READY-BACKLOG.json | remove governance/AAA-PATCH-READY-BACKLOG.json |
| AAA-ROLLBACK-AND-VERIFICATION-PLAN.md | remove governance/AAA-ROLLBACK-AND-VERIFICATION-PLAN.md |

No runtime state was modified by these drafts. Removal is pure rollback.

---

## Post-commit verification

For each committed patch:

1. git log -1 — confirm commit message matches proposal
2. git show --stat HEAD — confirm diff matches proposal exactly
3. Independent verifier runs content-safety scan
4. APEX/888 review recorded
5. git status — clean working tree post-commit
6. Receipt emitted (arifFlow consequence)

---

Reversibility: FULL — every patch reversible until F13 explicit ack.
F13 surface: only on alias final retire + sovereign-witness band ratification.
DITEMPA BUKAN DIBERI ⚒️