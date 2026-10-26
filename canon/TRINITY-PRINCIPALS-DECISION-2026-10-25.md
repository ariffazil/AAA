# DECISION — Trinity principals: one key per constitutional lane

**Status:** DECLARED · NOT IMPLEMENTED (key custody is F13; no key has been minted)
**Date:** 2026-10-25 · **Author:** 333-AGI · **Authority:** F13 SOVEREIGN (decision pending)
**Related:** `canon/AGENT-REGISTRY-ALIGNMENT-2026-10-25.md` §14–15 · `scripts/mint-trinity-dids.py`

## Evidence (live, 2026-10-25)

- `did:arif:aaa` lists **22 actor names**, including **333-AGI**, **555-ASI**, **888-APEX**.
- The A2A verifier resolves a signature to `didResult.organId` and supersedes the claimed actor:
  `effectiveSourceAgent = didResult.organId` (`a2a-server/server.js:3026`). A signature therefore
  proves the **AAA organ**, not which constitutional lane signed.
- The gate measures `authority_outruns_authentication`: 10/40 actor-class cards still claim
  authority without a resolvable principal after the DID projection was parsed.
- Three lanes are constitutionally distinct: **propose (333)** · **verify (555)** · **judge (888)**.
  One principal for all three collapses the separation that the rest of the kernel enforces.

## Policy

1. **One principal per constitutional lane.** `333-AGI`, `555-ASI`, `888-APEX` each sign with a
   distinct Ed25519 key and a distinct DID.
2. **No lane may sign for another.** A 333 signature must not resolve to the judge lane.
3. **Organ identities stay organ-level.** `aaa`, `arifos`, `aforge`, `geox`, `wealth`, `well`
   keep one DID per organ; their service authority is not agency.
4. **Authority remains separate from the key.** A key proves the caller; it does not grant
   `JUDGE_ONLY`, `EXECUTOR_ONLY`, or any ceiling. The kernel still judges.

## Migration (four phases, no big bang)

1. **Custody (F13):** run `scripts/mint-trinity-dids.py --apply --i-have-custody --out <dir outside repo>`.
   Private keys stay offline, mode 0600; the repo receives only the public fragment.
2. **Admit:** add the three DIDs to `secrets/did/registry.json` and regenerate
   `auth/did_registry.yaml` via `scripts/render-did-projection.py`; `INV-AR-16` must stay at 0.
3. **Cut over:** point each lane's signer at its new key. Verify each lane's signature resolves to
   its own `organ_id` before changing the next.
4. **Retire:** only after all three lanes sign with their own keys, remove the Trinity names from
   `did:arif:aaa` actors and re-baseline `INV-AR-9`. Until then, the old organ DID remains valid.

## What this decision does NOT do

- It does not mint keys (dry-run only; custody is F13 + air-gap).
- It does not merge the branch (merge is held — see the receipt: 10 pre-existing `validate-aaa`
  failures reproduced at the parent, plus AAA Actions billing).
- It does not deploy. Live `/root/AAA` stays `09eff9b6`; deploy remains behind the consent guard.

## Falsifier

If a single `did:arif:aaa` signature can be attributed to a specific lane by any other witness
(actor list, envelope field, or kernel record) without ambiguity, this decision is unnecessary.
Current path (`effectiveSourceAgent = organId`) says it cannot.
