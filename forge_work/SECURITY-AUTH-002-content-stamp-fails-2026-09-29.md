# AUTH-002 — The deployed kernel's content attestation does not verify

**Filed:** 2026-09-29 · FI-003 · trace `FI-003-2026-09-29-ZKPC-AUDIT`
**Class:** INTEGRITY — **report only, nothing repaired.** `MEASURED` (I ran the project's own documented recipe).
**Relationship to the session:** the kernel's `substrate.drift=true` verdict is **correct**, and its cause is
this. So AUTH-001's HOLD that stopped me was the constitution working — but for a reason nobody had written down.

---

## What I did

`scripts/deploy-release.sh:155-187` implements a **S5 "deploy-honesty" content stamp**: after install, it
hashes every `.py` in the installed package and writes the digest into `arifosmcp/__init__.py`, recording the
same value in `release-manifest.json`. It documents its own verify recipe verbatim:

> *"Verify recipe: strip the `__content_sha256__` line from the installed `__init__.py`, re-run the pipeline
> below, compare. (The stamp line cannot contain its own digest — self-reference is cryptographically
> infeasible — hence the documented exclusion rule.)"*

I replayed that recipe **exactly** on the live deployed tree (`/opt/arifos/current/venv/lib/python3.13/
site-packages/arifosmcp`), restoring the file afterwards (`cmp` → identical, no mutation left behind).

```
recomputed : fd60aee937bf70f9dfc71fdd175038351d855ada52c86b42e2698b2199cd752c
stamped    : cfe87cfe8fee2f75779f2e54fae398d55bcdc037853b6bb681735cea8495f960
RESULT     : DOES NOT VERIFY
```

## What that means

**The bytes on disk are not the bytes the deployed binary claims to be.** The package was stamped, then
changed, and nothing noticed — *except* the drift detector, which reported `drift=true` without ever naming
this as the cause.

Self-reference is handled correctly in their design (the exclusion rule is right, and I applied it). So this is
not a theoretical flaw in the scheme — it is the scheme working on a tree that was mutated after stamping.

## The likely cause is the drift I already found (D5, now 4 modules)

Deployed vs source differ in **four** `.py` modules, all carrying stale provenance pointing at
`scar-terrain-arif-fazil.md`, **a file that does not exist anywhere on disk**:

```
core/human_substrate.py           line 9, 63, 363   (source= string goes INTO sealed receipts)
schemas/human_properties.py       line 17
resources/human_context.py        line 12, 89
__init__.py                       (the injected __content_sha256__ line — expected by design)
```

Source was corrected at 12:06 today to `AAA/wiki/SCAR_TERRAIN.md` (which exists); the deployed copy is from
01:34. Whether the deployed tree was also hand-edited, or simply never rebuilt after the fix, I **cannot tell
from disk alone** — `UNKNOWN`, and it matters: a hand-edit of a deployed package is a different class of event
from a missed rebuild.

**Cross-check I could not complete:** the script says the digest is "also recorded in `release-manifest.json`".
I could not locate a release-manifest under `/opt/arifos/current`. If it is absent, there is **no second
witness** to compare against — the stamp in the binary is the only record, and it is unverifiable by definition
(see AUTH-001's `runtime_attestation_injected` label, which Q3 established cannot be real on this host).

## Why this is the session's theme, one layer down

Every finding tonight is the same shape — **a claim that outruns its evidence**:

| Layer | Claim | Reality |
|---|---|---|
| D1 | wire says `ZKPC_OBSERVATION` proof passed | host has no ZK circuitry |
| D5 | live kernel seals `source=…scar-terrain-arif-fazil.md` | that file does not exist |
| **AUTH-002** | binary attests `__content_sha256__=cfe87cfe…` | its own bytes hash to `fd60aee9…` |
| AUTH-001 | kernel reports `actor_verified: true` | no signature was ever provided |
| substrate | `source: "runtime_attestation_injected"` | no TPM/UEFI/CVM exists on this host (Q3) |

F13's compression tonight: *"Authority must flow through provenance."* The kernel's provenance stamp is the
one thing that was supposed to make that checkable — **and it is currently false-silent.** It did not fail loudly;
it produced `drift=true` and moved on.

## Options for F13 — not executed

1. **Rebuild + redeploy from source HEAD** (`ac054a582`, 12:13 today) so the stamp recomputes and the four
   stale provenance strings go away together. Fixes D5 and AUTH-002 in one action, and satisfies the kernel's
   own `next_action: RECONCILE_SOURCE_BUILT_DEPLOYED`.
2. **Make the stamp verifiable, not just present** — have the drift check recompute the digest and report a
   mismatch by name (today it reports a boolean; it never told anyone *which* of its own attestations failed).
3. **Emit `release-manifest.json` and keep it out-of-band** so a mutated tree can be compared against a second
   witness the mutator cannot also edit. Without that, the stamp is self-asserted — the same objection I raised
   against a self-installed swtpm in the Q3 addendum.
4. **Record whether the deployed tree was hand-edited** (investigate before rebuilding — rebuilding destroys
   the evidence of how it drifted). **I deliberately did not rebuild for exactly this reason.**

## What I did NOT do

Did not rebuild, redeploy, restart, restamp, or edit anything in `/opt/arifos`. The verify recipe requires a
temporary file swap; I restored it and confirmed byte-identical (`restored identical: YES`). Stopping was the
correct call: destroying the drifted tree destroys the only evidence of how it drifted.
