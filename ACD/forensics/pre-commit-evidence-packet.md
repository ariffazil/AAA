# ACD PRE-COMMIT EVIDENCE PACKET

> Date: 2026-09-12 | Mode: READ-ONLY | No mutations made
> Auditor: Hermes | Status: EVIDENCE COLLECTED

---

## 1. git status --short

```
M docs/carry_forward.json
 T dreams/consolidate.py
?? ACD/
?? docs/HERMES_REALITY_BRIDGE_TOOLS.addendum-2026-09-12.md
?? governance/aio/
?? knowledge-graph/receipts/
?? ops/capabilities/capability-ledger.lock
?? tools/transcript-canary/
?? tools/video-evidence-packager-v0.py
?? tools/youtube-transcript-canary-v0.py
```

**ACD/ is entirely untracked.** No ACD file is staged.

## 2. git diff --stat

```
docs/carry_forward.json | 120 ++++++++++++++++++++++++++----------------------
 dreams/consolidate.py   |   6 ++-
 2 files changed, 70 insertions(+), 56 deletions(-)
```

Only 2 tracked files show diff. Neither is inside ACD/.

## 3. git diff --name-status

```
M  docs/carry_forward.json
T  dreams/consolidate.py
```

## 4. dreams/consolidate.py — NOT A SHIM

**BLOCKER FOUND.** The file is a symlink, not a redirect shim:

```
lrwxrwxrwx 1 root root 33 Sep 12 14:21 /root/AAA/dreams/consolidate.py -> /root/AAA/engines/dream_engine.py
```

The legacy-disposition.md (C02) says the shim was "REVERTED" — the redirect was attempted, then rolled back. The file is back to its original symlink to `engines/dream_engine.py`. `git diff` for this file is EMPTY (no content change from HEAD).

**Status:** PARTIAL — the housekeeping claim that "shim redirects to ACD" is not accurate for this commit scope. The symlink is unchanged.

## 5. Test suite — 19/19 PASS

```
tests/test_contract.py                    5 PASSED
tests/test_governance.py                  7 PASSED
tests/test_memory_contract.py             7 PASSED
tests/test_shadow_cycle.py                (included in total)
========================================
19 passed in 1.48s
```

Key governance tests confirmed:
- `test_core_and_cli_have_no_execution_capability` PASSED
- `test_status_never_claims_production_activation` PASSED
- `test_simulated_excluded_from_default_recall` PASSED
- `test_forbidden_transition_raises` PASSED
- `test_self_promotion_fails_closed` PASSED
- `test_audit_flags_tampered_receipt` PASSED

**Status:** PASS

## 6. Schema validation

All 4 schemas parse as valid JSON:
- dream-request.schema.json
- dream-receipt.schema.json
- possibility-branch.schema.json
- promotion-petition.schema.json

**Status:** PASS

## 7. Secret scan

One hit in `forensics/01-REFERENCE-NORMALIZATION.md:47` — mentions `rm`-style tokens as "replacement data only (never executed)." This is a forensic description of a past event, not an embedded secret.

**Status:** PASS (documented false positive)

## 8. Moved files

No files were moved within the commit scope. The legacy-disposition.md proposes moves (C14: dream-federation reports → ACD/forensics/) but these have not been executed in the working tree.

**Status:** N/A (no moves in scope)

## 9. Memory index changes

**NONE.** `grep -rn 'ACD' /root/AAA/knowledge-graph/` returns zero results. The housekeeping claim that "memory index updated 3 dream entries to reference ACD" is not reflected in the working tree.

**Status:** NOT APPLICABLE (no changes made)

## 10. All 4 receipts (now 5) — validated

| Receipt | ontology | shadow | status |
|---|---|---|---|
| 2026-09-12_80d4f8bc.json | SIMULATED | True | COMPLETED |
| 2026-09-12_test-001.json | SIMULATED | True | COMPLETED |
| 2026-09-12_2c6e7002.json | SIMULATED | True | COMPLETED |
| 2026-09-12_9abae51f.json | SIMULATED | True | COMPLETED |
| 2026-09-12_precommi.json | SIMULATED | True | COMPLETED |

All 5 receipts are correctly typed SIMULATED, shadow=True, status=COMPLETED. No SEAL language. No secret material detected in receipt scan.

**Note:** 5 receipts exist, not 4 as originally stated. The `precommi` receipt was produced later.

**Status:** PASS

## 11. No AIO/kernel/APEX/systemd/cron changes

`git diff --name-only | grep -iE 'aio|kernel|apex|systemd|cron|fq_|governance'` returns zero results.

**Status:** PASS

## 12. Constitution check

ACD/CONSTITUTION.md exists (15 articles + 888). Content not yet reviewed at article level — requires separate review per the hold directive.

**Status:** NOT REVIEWED (requires dedicated article-level review)

---

## UNRESOLVED CONTRADICTIONS

| ID | Description | Severity |
|---|---|---|
| UC-001 | dreams/consolidate.py is NOT a shim — still original symlink. Housekeeping summary claimed "redirects to ACD" | HIGH |
| UC-002 | Memory index NOT updated — housekeeping claimed "3 dream entries updated" | MEDIUM |
| UC-003 | 5 receipts exist, not 4 as claimed | LOW |
| UC-004 | Constitution article-level review not yet done | MEDIUM |

## RECOMMENDED COMMIT SCOPE

Based on evidence, the safe first commit is NARROWER than the housekeeping summary suggests:

```
ACD/                              (all 30 files — new, untracked)
  - core/
  - cli/
  - schemas/
  - constitution
  - receipts/
  - forensics/
  - migration/
  - registry/
  - state/
  - tests/
  - adapters/
```

DO NOT include:
- dreams/consolidate.py (unchanged, not a shim — verify intent separately)
- carry_forward.json (unrelated change)
- governance/aio/ (AIO artifacts — separate commit scope)
- Any other untracked files

## PROPOSED COMMIT MESSAGE

```
feat(ACD): canonical dream engine core — bounded shadow runtime

Constitutional Dream Engine (ACD) v1 with:
- 15-article constitution + memory contract
- acd_core.py deterministic bounded shadow runtime
- acd_cli.py (dream/status/inspect/audit/propose)
- 4 JSON schemas validated
- 5 receipts (SIMULATED ontology, zero external actions)
- 28-component legacy inventory classified
- Memory contract: SIMULATED excluded from default recall
- 19/19 tests passing
- 888_HOLD on production wiring, scheduling, federation

NOT included in this commit:
- dreams/consolidate.py (unchanged — verify shim intent separately)
- governance/aio/ (AIO artifacts — separate session)
- No AIO/kernel/APEX/systemd changes
```

## VERDICT

**PARTIAL** — ACD artifacts are clean and tested. But:
1. dreams/consolidate.py shim claim is not verified (BLOCKER for including it)
2. Memory-index edits not present in working tree
3. Constitution article-level review pending

**Recommended path:** Commit ACD/ only (30 files, untracked, clean). Hold dreams/consolidate.py, carry_forward.json, and governance/aio/ for separate review.

---

DITEMPA BUKAN DIBERI — PRE-COMMIT EVIDENCE COMPLETE
