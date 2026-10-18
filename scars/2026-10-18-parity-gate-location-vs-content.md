# SCAR-2026-10-18-005 — Parity Gate: Location vs Content

**Filed:** 2026-10-18 by AGY CLI (Deploy Closeout)
**Weight:** w_scar = 0.7
**Class:** GATE_OVERCONSTRAINT + FAIL_CLOSED_SAFETY
**Commit:** arifOS `09ad880fb`

## What happened

The initial version of the runtime parity gate enforced an identity constraint on path location:
```bash
assert realpath(LIVE_PKG) == realpath(/opt/arifos/app/arifosmcp)
```
However, in this environment, `/opt/arifos/app/arifosmcp` (the repo tree) and `/opt/arifos/venv/lib/python3.13/site-packages/arifosmcp` (the virtualenv site-packages tree) are two distinct physical directories by design.

As a result, the gate falsely triggered on a completely valid deployment:
`"ERROR: live import path /opt/arifos/venv/lib/python3.13/site-packages/arifosmcp is not a synced tree — refusing to restart"`

## Why this was the safe failure mode

Even though the location-assert was over-constrained and falsely rejected a valid sync, it failed **CLOSED**:
- Both destination trees were already synced.
- The service was prevented from restarting under an unproven state.
- The existing running process was left untouched and operating normally.
- Zero downtime and zero half-applied runtime mutations occurred. Fail-closed discipline successfully prevented corruption.

## Lesson & Fix landed

The invariant is **content parity, not location parity**. What matters for runtime correctness is that the active import directory contains exact byte-for-byte matching files, not that it shares an identical inode or path with the staging tree.

The gate was updated in commit `09ad880fb`:
- Checks both directories (`/opt/arifos/app/arifosmcp` and `$LIVE_PKG`) with `diff -rq` against source `$SRC/arifosmcp`.
- Replaces path-equality assertion with recursive content-equality and SHA verification.

## Binding rule (this scar)

- Gates must enforce invariant truth (content, cryptographic hash, semantic behavior), not incidental structural coincidences (path equality, symlink layout).
- A false alarm that fails closed is always preferable to a silent pass that fails open.
