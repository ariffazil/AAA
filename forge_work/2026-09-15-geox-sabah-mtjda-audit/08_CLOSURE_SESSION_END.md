# CLOSURE — GEOX Sabah/MTJDA audit, session end state

**Date:** 2026-09-15 · **Node:** forge (KVM8, 100.64.0.2) · **Authority:** F13 ARIF
**Peer:** KVM4 (srv1946043, 100.64.0.5) — independent audit, cross-verified

---

## 1. Durable state

| Artifact | Status | Live? |
|---|---|---|
| `CLM-NWS-004..008` (Sabah deep crustal H1–H4 + KT-7 decision test) | Written | **NO — repo only** |
| `CLM-MTJ-001..007` (Malay Basin / MTJDA) | Written | **NO — repo only** |
| Peer's staged file `workspace/claims/kinabalu_h1_h4_staged_2026-09-15.md` (KVM4) | Staged, marked SUPERSEDED | NO |
| Sabah reconciliation patch (9 defects) | Written, apply-ready | **HELD — sealed ledger** |
| KT-7 claim correction | Written | advisory |
| Artifact ledger for both PDFs | Written | record |
| `10-13.7 Ma` orphan string fix | Ready, one line | **HELD** |

Mutation footprint this session: **two resource files**, additive only, git-tracked, reversible.

---

## 2. The four GEOX surfaces (the session's principal finding)

```
/root/GEOX        @ 6d55a682   repo (this node)      — authored here, NOT served
/opt/geox         @ 8c6c7f2d   deployed (this node)  — what geox-mcp.service serves
/opt/geox/app     @ 4a462244   nested clone (this node)
KVM4 /root/GEOX   @ cf32a885   stale clone (27 Aug)  — 52 commits / ~19.8k lines behind
```

`geox-mcp.service`: `WorkingDirectory=/opt/geox`, `RESOURCES_DIR = _REPO_ROOT/"resources"`.
Basin claims load from `/opt/geox/resources/basins/<name>/claims.json`.

**Consequence:** `CLM-NWS-004..008` are NOT served by the organ. Verified by read-back —
repo 8 claims vs deployed 3.

## 3. Kernel attestation defect

`arifosmcp/core/reality_anchors.py:38` → `_ORGAN_SRCS["geox"] = "/root/GEOX"`, then reads
`<path>/.git/HEAD`. So `organ_shas.geox = 6d55a68` attests the **dev repo**, not the deployment.

The live service self-reports `geox-8c6c7f2d`. Both numbers are honest; they answer different
questions. Any consumer treating `organ_shas` as a deployment receipt will be confidently wrong.

Peer's report (KVM4) and this node's report were both correct — different machines. A peer's
older checkout does not invalidate their file-level verification:
`git diff --quiet cf32a885 6d55a682 -- sabah_prospect_discriminator.py` → IDENTICAL. Their KT-7
and granite confirmations stand.

---

## 4. Corrections made this session (own errors, on the record)

| # | Claim I made | Correction |
|---|---|---|
| C1 | "SEG-Y commit may have made the no-seismic caveat stale" | Retracted — capability ≠ data; caveat stands |
| C2 | "Granite age contradicted three ways" | It is ONE orphan unsourced string (`discriminator:369`); dossier + ledger + literature + `thermal_history.py` all agree |
| C3 | "Claims registered in GEOX" | Registered in repo only; **not served** |
| C4 | "12–21 km" implied to be a federation-geometry dispute | The figure has **zero** occurrences in the federation — it is dossier-vs-federation, not internal |
| C5 | `CLM-NWS-004` asserted the Vp overlap occurs "at 12–21 km" — as fact | **Fixed.** The depth is the contested figure I had just flagged unsourced. Now reads "at comparable depths (depth CONTESTED …)" with both geometries named |

**Recorded, not papered over.** C3 and C5 are the important ones. C3: I reproduced the exact
defect class I was auditing (write to one surface, report as live) two hours after diagnosing it
in others. C5: I imported the dossier's contested number into my own claim record as fact, in the
same session I established it has zero federation support — the precise error I was criticizing.

Both were self-caught and corrected. The pattern is the same in both: **an artifact inherits its
author's unexamined assumption, not just their data.** Reading back the record is what caught it.

Verified after fix: no unattributed occurrence of "12–21 km" remains in either claim store.

---

## 5. Lesson captured

`deploy-drift-verification` skill updated with:
- Enumerate the WRITE side, not just the read side — a data/resource file registered to the repo
  is not served when `WorkingDirectory` points elsewhere. Read back from the resolved path.
- A kernel/monitor "deployed SHA" field may attest the dev checkout. Read the code that populates
  it before treating it as deployment evidence.
- Health endpoint and kernel attestation may honestly disagree — name all three objects
  (repo / deployed tree / running process).

---

## 6. Decisions pending F13 (unchanged, now substrate-first)

1. **Which surface is GEOX authority?** repo / deployed / node-designated. **Blocks items 2–4.**
2. Ratify the Sabah reconciliation patch (held: sealed ledger).
3. Make `CLM-NWS-004..008` live, or leave git-only?
4. Fix the `10-13.7 Ma` orphan string?
5. Resolve KT-7 geometry (needs Franke et al. 2008 full text — paywalled).
6. Correct the two citation metadata errors in the dossier, or attach errata?
7. Home + provenance tag for the two PDFs (`PROVENANCE_PARTIAL` / `ABSENT`)?

**Sequencing (forced by substrate, agreed with peer):** reconcile substrate → claims go live →
ledger artifacts last, so their caveats absorb everything above.

---

DITEMPA BUKAN DIBERI ⚒️
