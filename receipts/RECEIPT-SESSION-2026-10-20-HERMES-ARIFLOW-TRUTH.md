# SESSION RECEIPT — 2026-10-20 MYT — HERMES

**Level: RECEIPT, not constitutional SEAL.** `arif_seal` is not in this session's allowed verbs
(`arif_init` → `authority=OBSERVE_ONLY`, `actor_verified=false`, `hold_scope=MUTATION`), and
A-FORGE `forge_vault` mode=receipt returned `URLElicitationRequiredError` — the write needs
your confirmation in the UI. So this file is the honest floor: evidence recorded, seal withheld
by the system, not by me.

## Removed, verified live

1. **`arifFlow /health → provenance.window_start_utc`** carried `start_time.elapsed().as_secs()`
   — process uptime in seconds, under a name promising a UTC timestamp (live value `941`;
   read as a time that is 1970-01-01T00:15:41Z). Now: RFC3339 UTC of process start +
   `window_age_s` + `window_basis: process_lifetime_since_start`.

2. **`restricted_actors()` reason string.** `"HELD: FQ={:.2}"` was formatted off the `state.fq`
   alias that maps `None → 0.0`, so "not measurable" and "measured zero" printed identically.
   Reasons now carry the measured counts and say `UNMEASURED` where a quotient is not
   computable. **No threshold moved. No actor released.**

   Commit `1c4339e` on `/root/arifFlow`, binary deployed to `/opt/arifflow/bin/arifflow`
   (backup `arifflow.bak-20261020T2245`), `cargo test --release` 246 passed / 2 ignored.

3. **`hermes_mcp` principal extraction** (earlier this session, verified on live :18087):
   ordinary capitalised words were emitted as `referenced_principals` and the claimant handle
   `assistant` was typed `PERSON`. Capitalisation now counts as name evidence only where it
   discriminates; model handles type as `AI_ORGAN`. 85 + 106 tests passed.

## What the new strings immediately exposed

```
codex | HELD: FQ=3.00 (execute=1 verify=3)
```

A held actor at six times the 0.50 gate. Under the old string it read `HELD: FQ=0.00` and the
contradiction was invisible. Holds are durable; the evidence window is the process lifetime.
A hold can therefore outlive the state that produced it — and until tonight the reporting made
that unreadable.

## Open, needs F13 (not deletions)

1. Does a hold survive a restart at all, or is it re-derived from the rehydrated window?
2. Which axis belongs on the FLOW PLANE of the dashboard — the deprecated flow band
   (`OPTIMAL`/`BALANCED`) or the vector constellation (`SIMULATION`/`PARTIAL_WIRING`)? Both are
   emitted; `observatory_routes.py:1773` silently prefers the deprecated one.
3. `HOLD` carries three meanings on one tool: input contract (`status`), authority scope
   (`verdict`), transport block. Constitutional vocabulary change, not a rename.

## Artifacts

- `/root/AAA/reports/arifflow-hold-audit-2026-10-20.md` — full audit, 10 sections, claim-by-claim
- `/root/AAA/instructions/hermes-meaning-fidelity.md` — 3 deltas only (DRAFT_AWAITING_F13)
- `/root/arifFlow` commit `1c4339e`
- carry_forward `e-80633bc4` (decision) and `e-6d652461` (lesson)

## Not touched, deliberately

The 6 holds (5 are the gate working), `/release` behind 888_JUDGE, the three genuine Verify
receipts written for real work, `explanation_gate`'s CM-1, `merkle_root`/`tri_witness_votes`
(protected by `compute_jcs_body_hash` over the whole struct), `WAITING_FOR_WITNESS` (documented
P4 substate, zero emitters — remove only with the lattice doc).
