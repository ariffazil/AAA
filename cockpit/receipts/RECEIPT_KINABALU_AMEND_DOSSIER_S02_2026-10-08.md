# RECEIPT — Kinabalu Dossier §02 Amendment

**Date:** 2026-10-08 (UTC)
**Class:** T3 mutation (canonical record, public-facing surface)
**Branch:** `feat/kinabalu-xsection-models` @ `ariffazil/arif-fazil.com`
**F13 authority:** Arif's "go amend" word; 1 binary ask answered (DRU tarikh + rujukan); SRU range selected from menu.

## What changed

Two-line amendment to `sites/arif-fazil.com/public/earth/kinabalu-basin/index.html`,
section 02 (Tectonic Evolution), aligning the dossier narrative with the cross-section
and PDF dossier v3 (both already on the same branch):

- **Line 423:** Added DRU age ~15.5 Ma with Balaguru & Hall 2009 attribution.
  Was: "Mid-Miocene Unconformity (MMU = Deep Regional Unconformity (DRU))".
  Now: "Mid-Miocene Unconformity (MMU) = Deep Regional Unconformity (DRU, ~15.5 Ma, Balaguru & Hall 2009)".
- **Line 428:** SRU corrected from 8.6 Ma single point to ~8.5–9.5 Ma range, matching
  the cross-section discrimination matrix and the PDF figure caption.
  Was: "Shallow Regional Unconformity (SRU, 8.6 Ma)".
  Now: "Shallow Regional Unconformity (SRU, ~8.5–9.5 Ma)".

## Commit chain

```
be0d018 fix(earth/kinabalu): dossier §02 chronology — DRU ~15.5 Ma, SRU 8.5–9.5 Ma range   ← amendment (this work)
32b454a feat(earth/kinabalu): Dangerous Grounds -> East Sabah section with four working models  ← Arif's force-push from laptop
d589398 world/politics: rebuild section index as proper front room
```

- Local started at `d5a3952` (initial clone, same content as `32b454a`).
- Arif force-pushed `32b454a` from laptop between local clone and amendment push.
- `git rebase origin/feat/kinabalu-xsection-models` auto-detected duplicate
  `d5a3952` ↔ `32b454a` (cherry-skip), applied `15bde1c` (pre-rebase SHA of
  amendment) cleanly on top of `32b454a`. New SHA after rebase: `be0d018`.
- `git push --force-with-lease` advanced remote `32b454a..be0d018`.
- `--force-with-lease` chosen over `--force` to fail-safe if remote had moved
  between fetch and push.

## Scope discipline

- Diff vs remote HEAD: **+2 / −2 lines**, both inside section 02.
- No collateral changes to: cross-section, PDF, build script, surfaces catalog.
- Confidentiality sweep on amended file: clean (no Perkaka, Layang-2, internal
  well picks, keyline refs, or non-public markers). The string "confidential"
  appears once at line 665 but is a public-facing note authored by Arif for
  readers ("PSC block boundaries are confidential until the next data room");
  not an internal-name leak.

## What was NOT done (F13 held)

- No PR created (`gh` not available in this container; laptop has gh).
- No merge to `main` (F13 SOVEREIGN; Arif must decide merge from laptop or
  via UI with review).
- No deploy, no cloudflare invalidation, no Vercel hook.

## Membrane compliance

- F1 AMANAH: amendment is reversible (`git revert be0d018`).
- F2 TRUTH: cited public source (Balaguru & Hall 2009) for DRU date; SRU
  range matches in-page discrimination matrix and PDF caption.
- F9 ANTIHANTU: no AI-claimed authorship on public surface; commit
  message describes the change neutrally.
- F11 AUDITABILITY: this receipt.
- F13 SOVEREIGN: 1 binary ask resolved; "go amend" → execute. Merge held.
