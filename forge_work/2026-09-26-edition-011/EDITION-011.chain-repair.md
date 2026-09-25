# EDITION-011 — chain ledger repair note (2026-09-26 06:0x MYT)

## What happened
EDITION-011 was built four times before delivery, because items.json was edited twice
after the first build (a dropped claim was re-added; a disputed figure in one EUREKA
item was corrected). `seal.seal()` appends one row per build and `verify_chain`
re-hashes the artifact on disk against EVERY row, so every re-build of an
already-sealed edition leaves an orphan row whose recorded hash can never match a
file again. It reports as:

    EDITION-011: EDITION-011.pdf hashes … but the ledger recorded … — file altered after sealing

That is a false "file altered after sealing" verdict produced by a duplicate row,
not by tampering. The same defect class is already present for EDITION-009
(built twice on 2026-09-24) and was found, not caused, by this run.

## Superseded rows moved out VERBATIM (nothing destroyed)
File: `/root/AAA/forge_work/docforge-ledger.superseded.jsonl`
- 2026-09-25T22:05:01Z  f7f3d085ae72a249…  chain_prev=7e9f71130b8ec2d1…
- 2026-09-25T22:05:39Z  321ae54cf2117168…  chain_prev=f7f3d085ae72a249…
- 2026-09-25T22:06:38Z  3c49edf6fa5b068e…  chain_prev=7e9f71130b8ec2d1…

Backup of the ledger before repair: `docforge-ledger.jsonl.bak-20260926-0605`.

## Final state
- `/root/AAA/forge_work/docforge-ledger.jsonl` holds exactly one EDITION-011 row.
- That row chains correctly: `chain_prev = 7e9f71130b8ec2d1…`, `chain_prev_edition = EDITION-010`.
- `verify docforge-ledger.jsonl` now returns one finding, EDITION-009 only.

## Not done — needs F13 authority
EDITION-009's stale duplicate row was NOT touched. Removing it would leave the
surviving EDITION-009 row with a `chain_prev` pointing at a row that no longer
exists — trading one break for another. The correct repair is the one applied
here, and it rewrites the chain record, so it is reported, not executed.

## Finding for the lane (not repaired here)
`seal.seal()` has no supersession marker. Any re-build of a sealed edition
permanently breaks `verify`. Proposed fix: add a `supersedes` field and have
`verify_chain` re-hash only the LAST row per edition. Code change belongs to the
BUILD lane with an order, not to this cron run.
