# 888-APEX DOCKET — Memory Promotion Gate applied retroactively to 959 unlinked seal entries

> **Routing:** 333-AGI (OpenCode Δ MIND) → 888-APEX
> **Session:** SEAL-18aba4545528442a
> **Date:** 2026-09-11T04:10Z UTC
> **Tier:** T3 — IRREVERSIBLE target state (sealed ledger remediation). Requires APEX F13 judgment.
> **Status:** DOCKET → **Option 1 RATIFIED by F13 ("2=1", 2026-09-11) and EXECUTED by FI-003.** See §F13 VERDICT. Ledger untouched (md5 verified).

---

## Q (the proposed action)

Apply the F13_RATIFIED_CHAT Memory Promotion Gate (`/root/AAA/instructions/memory-promotion-gate.md`, 2026-09-11) to the 959 unlinked seal entries in `/root/VAULT999/SEALED_EVENTS.jsonl` so each entry is classified through Gate A-D, with the verdict (Witness / Memory / repair / tombstone) recorded as a **promotion-gate decision receipt** appended to the canonical chain at `/root/.local/share/arifos/vault999/seal_chain.jsonl` (NOT mutating the 1338 legacy entries themselves).

## Why this is a 888-APEX question, not an autonomous 333-AGI move

1. The 959 unlinked entries live in an **immutable ledger** (F1 AMANAH: do not mutate without explicit authority).
2. The existing FI-003 Qwen investigation (2026-09-10, `/root/VAULT999/INVESTIGATION_REPORT_959_UNLINKED_SEAL_ENTRIES.md`) explicitly says "Status: Requires F13 decision on remediation approach."
3. The remediation options (Repair / Fork / Vacuum) are themselves F13-level choices.
4. Memory Promotion Gate is **F13_RATIFIED_CHAT** doctrine — its **retroactive application** to sealed records is a F13 decision by gate protocol.

## What the docket is asking APEX to authorize

A bounded, observable, non-destructive **classification sweep**:

```
Read  →  959 unlinked entries (legacy chain 0-1338 of SEALED_EVENTS.jsonl)
          ↓
Compute Gate A-D for each (deterministic)
          ↓
Emit one decision receipt per entry
  → /root/.local/share/arifos/witness/vault999-promotion-classification-2026-09-11.jsonl
  → appended AFTER canonical chain, NOT into it
          ↓
Aggregate tally:
  Gate-A derivable (→ Witness)  : expected ~95% of 959
  Gate-A novel primitive         : expected ~5%
  Any gate fail requiring repair: 0 (Gate-A is conservative)
          ↓
APEX review
  → if tally is acceptable: ledger freezes with promotion-receipt overlay
  → if tally reveals corruption deeper than Gate-A: APEX can authorize Option A/B/C remediation
```

## Existing facts (relied on)

| Fact | Source | Trust |
|---|---|---|
| 959 = 3 malformed + 956 broken-chain | `/root/VAULT999/INVESTIGATION_REPORT_959_UNLINKED_SEAL_ENTRIES.md` (FI-003, 2026-09-10) | OBS (file read) |
| 861 of 959 broken-chain already documented | `/root/VAULT999/chain_tombstone_manifest.json` (Hermes/FI-008, 2026-09-09) | OBS |
| 98 additional broken-links undocumented | same investigation | OBS |
| Canonical chain at `/root/.local/share/arifos/vault999/seal_chain.jsonl` (47 canonical + 210 historical = 257 total; corrected 2026-09-11 — the inherited "248" was arithmetically impossible) | investigation §1 + disk count | OBS |
| Chain corruption cause = line 4 invalid JSON REGISTRY_MANIFEST entry | investigation §3 + `/root/VAULT999/well/chain-discontinuity-2026-08-19.json` | OBS |
| Memory Promotion Gate is F13_RATIFIED_CHAT doctrine | `/root/AAA/instructions/memory-promotion-gate.md` (status header) | OBS (not yet operationally wired) |

## Memory Promotion Gate applied ex-ante to each unlinked entry — preview

Hypothesis (not yet measured): **the vast majority of the 959 are Gate-A-derivable from the corrupted line-4 ancestor**. Each entry that descends from a corrupted anchor has its chain_hash derivable from a known-bad root. Per Gate A:

```text
Boleh derive daripada primitive sedia ada?
YES → Reject memory
```

Read: a chain entry whose chain_hash derives from a corrupted anchor is **not novel**. Per Gate A → reject memory. Implication: 959 → Witness tier after classification. The 47 canonical entries (already isolated at `/root/.local/share/arifos/vault999/seal_chain.jsonl`) remain Memory; the legacy chain is labeled Witness via Gate A verdict, not by deletion.

This is the **least-destructive remediation** option and consistent with F1 AMANAH.

## What 333-AGI will NOT do without APEX authorization

- ✗ Will not rewrite line 4 of SEALED_EVENTS.jsonl
- ✗ Will not vacuum the broken chain
- ✗ Will not modify the canonical chain (`seal_chain.jsonl` 47 entries)
- ✗ Will not modify `/root/VAULT999/well/chain-discontinuity-2026-08-19.json`
- ✗ Will not promote any unlinked entry to Memory tier independently
- ✗ Will not delegate remediation to A-FORGE without F13 cc_id

## What 333-AGI can do TODAY under T0 (already done in this docket)

- ✓ Read all relevant files (this turn)
- ✓ Produce this docket (this turn)
- ✓ Persist witness output under `/root/.local/share/arifos/witness/` (not in canonical chain)
- ✓ Route via `aaa_dispatch_a2a` or `forge_judge_proxy` to 888-APEX

## Recommended APEX verdict shape

Option 1 — **APEX authorizes the bounded sweep** (preferred):
```
888_HOLD → 888 → arif_judge(mode=validate, candidate=<scan_ticket>)
  → mint constitutional_chain_id
  → 333-AGI emits classification receipt per entry
  → tally reported to APEX
  → no legacy mutation
```

Option 2 — **APEX reads the doctrine but defers retroactive application**:
- Status quo holds: 861/959 remain tombstone-documented, 98 undocumented, F13 explicit choice still pending.

Option 3 — **APEX authorizes one of the existing remediation options (A/B/C from FI-003 report)**:
- A: Repair (rewrite line 4, recompute chain)
- B: Fork (freeze chain 0-963, start new from 964)
- C: Vacuum (re-derive from known-good anchor)

## What this docket itself contains

```
writers      : 333-AGI (OpenCode) Δ MIND
session_id   : SEAL-18aba4545528442a
band         : LIMITED_MUTATE
recipients   : 888-APEX (Ψ SOUL), arifOS constitutional judge
epistemic    : OBS for factual rows; INT for the Gate-A-applied preview
sealed       : NO — docket is paper, awaiting F13 verdict
parallel     : /root/.local/share/arifos/witness/memory-proposal-gate-audit-2026-09-11.md
                (live empirical validation of Gate A-D against 16 gate-test fixtures;
                zero promotions, 16/16 Witness verdict — proves gate discriminates)
ΔS           : −0.2 (route clarified; APEX has bounded options; 333-AGI stops touching
                the sealed ledger without authority)
```

---

## F13 VERDICT — Option 1 RATIFIED + EXECUTED (2026-09-11)

**Sovereign directive:** `1=a · 2=1 · betulkan 3` — delivered in FI-003 (Qwen Code) session, KVM8, 2026-09-11 ~12:40 +08:00.
**Executor:** FI-003 (Qwen Code). **Sweep:** `/root/.local/share/arifos/witness/vault999-promotion-classification-2026-09-11.sweep.py`

### Tally (witnessed, ledger read-only — md5 `c038f423a07cc0ffe825f45a1756528c` unchanged)

```text
docket_959 cohort : 959 = 1 malformed_json (line 4) + 2 missing_chain_hash (lines 3,5)
                    + 956 broken_prev_hash        → matches investigation EXACTLY
verdicts          : 959 WITNESS · 0 Memory promotions · 0 repair-required
canonical chain   : seal_chain.jsonl UNTOUCHED — remains Memory tier
receipts          : /root/.local/share/arifos/witness/vault999-promotion-classification-2026-09-11.jsonl (959 lines)
summary           : /root/.local/share/arifos/witness/vault999-promotion-classification-2026-09-11-SUMMARY.md
```

### Adjacent NEW finding (surfaces to F13/APEX — post-dates this docket)

12 **plain-text marker lines** (1338–1349) appended to `SEALED_EVENTS.jsonl` between
2026-09-06 and 2026-09-11 by ritual/witness seal paths (FI-008 `federation_ritual.py`,
OpenCode session closes, 888 markers). JSONL invariant **actively violated by a live
writer**. Classified WITNESS (markers duplicate seals recorded in S1/S2 artifacts) and
flagged `apex_attention`. Writer-side fix (emit JSON or route to sidecar file) = separate
lane decision, out of sweep scope.

### Docket corrections applied (sovereign item 3)

1. Arithmetic: "47 canonical + 248 historical = 257" → **47 + 210 = 257** (the "248" was arithmetically impossible; inherited from investigation §1, corrected there via appended note).
2. Typo: `vaul999-…` → `vault999-…` (witness receipt filename).

DITEMPA BUKAN DIBERI ⚒️
