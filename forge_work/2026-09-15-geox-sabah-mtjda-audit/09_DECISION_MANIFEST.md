# DECISION MANIFEST — GEOX substrate + Sabah/MTJDA audit
**For:** F13 ARIF · **Compiled:** 2026-09-15 · **Nodes:** KVM8 (forge, 100.64.0.2) + KVM4 (srv1946043, 100.64.0.5)
**Status:** technical work complete · all remaining items are decisions

> Peer manifest received 16:10Z merged with this node's verification. **Two items corrected —
> see C1/C2.** Both corrections REDUCE the risk framing; ratifying the original numbers would
> have over-stated item 2 by ~50×.

---

## CORRECTIONS TO THE PEER MANIFEST
> **Status: peer CONFIRMED both corrections and formally amended item 2 (16:2xZ).**
> Amended item 2 reads: *"Push 6d55a682 to origin — SATU commit (429 lines, 2 files, dual-era
> transport), still not on origin after fresh fetch, so the data-loss flag STANDS — but
> one-command scale, not a catastrophe."* Items 1 and 3–9 unaffected.
> The correction is in the record on both sides; no residual wrong figure.

**C1 — Item 2's "52 commits / ~19,800 lines" is wrong. Measured on KVM8:**

```
origin/main : 5d543fee
local HEAD  : 6d55a682
commits ahead of origin/main : 1
6d55a682                    : 2 files changed, 429 insertions(+)
```

**One commit. Two files. 429 lines.** The 52-commit figure is the distance between KVM4's stale
clone and HEAD — and `git branch -r --contains` confirms **those 52 commits are on GitHub**.
They arrived from origin. KVM4's gap is a *fetch* problem, not a *push* problem.

**C2 — Item 2's gate is ANSWERED, not open.**

```
git merge-base 6d55a682 5d543fee  ->  5d543fee   (= origin/main itself)
git merge-base --is-ancestor 5d543fee 6d55a682  ->  TRUE
commits origin/main has that HEAD lacks : 0
```

`6d55a682` **contains** `origin/main`. It is one commit above main, zero divergence.
**Plain push. No merge. No rebase. No additional decision required.**

---

## THE FIVE GEOX STATES (one line, not a graph)

```
KVM4 /root/GEOX   cf32a885   27 Aug   stale clone (fetch gap)
origin/main       5d543fee   15 Sep   GitHub
KVM8 /root/GEOX   6d55a682   15 Sep   +1 commit unpushed (429 lines, 2 files)
/opt/geox         8c6c7f2d    9 Sep   SERVING (geox-mcp.service)
/opt/geox/app     4a462244            nested clone
```

---

## DECISIONS PENDING F13

| # | Decision | Gate / note |
|---|---|---|
| 1 | **Which surface is GEOX authority?** repo KVM8 / serving `/opt/geox` / declare node authority | **Blocks 4, 5** |
| 2 | **Push `6d55a682` to origin** — one commit, 429 lines, on one disk | **Gate CLEARED (C2).** `git push origin feat/mcp-dual-era-2026-07-28`. Data-loss risk is real but small |
| 3 | **Sync KVM4** — peer clone clean, fast-forward safe | Depends on #2 only. Two commands, no conflict |
| 4 | **`CLM-NWS-004..008` live on the organ, or git-only?** | Depends on #1. If live → one deploy from Hermes |
| 5 | **Ratify Sabah reconciliation patch** (9 defects + D11) | Held: Hermes wrote to a non-served surface. Ratify only after #1 |
| 6 | **Resolve KT-7 geometry** (6–8 vs 12–21 km) | Read-only, free, needs Franke 2008 full text (paywalled). Ready |
| 7 | **Orphan string `10-13.7 Ma`** → one line, one approval | Present on BOTH nodes at line 369 (verified) |
| 8 | **Ledger both dossiers with caveats** | Agreed last, after 1–7, so caveats don't stale |
| 9 | **Kernel attestation defect** — `organ_shas` reads `<path>/.git/HEAD` (dev checkout), not the running deployment | `reality_anchors.py:38` → `/root/GEOX`. Fix affects arifOS itself |

**Item 3's dependency is the only hard ordering constraint among 2–3.** Items 6, 7, 9 are
independent and can be authorised in any order.

---

## NOT YET A DECISION — H3 (gravity/mag reprocessing)

Engine exists (`geox_joint_inversion`, `multi_physics.py:71` — real invoker, takes
`ModalityObservation`s, fused to Physics13State under bounds). Uncertainty realizations exist
(`backstrip.py:310`). **What does not exist: cleaned public data, and an agreed resolution
threshold.**

Correction to peer's read: **`bwrap` appears nowhere in the GEOX codebase.** If a sandbox was
observed it comes from elsewhere, not GEOX source.

**Precondition before H3 starts:** state, in advance, the resolution at which H3 is considered
*killed*. Without that, the output is artwork, not a falsifier.

**Three capability-without-data strands this session** — SEG-Y lane (no volume), KT-7 filter
(no Vp), joint inversion (no cleaned data). Each can be sold as "runnable". None is.

---

## INVARIANT ADOPTED FROM THIS SESSION

**No sentence of the form "GEOX says X" without pinned node + path + commit.**
"GEOX" referred to four different artifacts today, each answering differently — the same
pathology as the three collision ages: one label, many referents, each stated confidently.

---

DITEMPA BUKAN DIBERI ⚒️
