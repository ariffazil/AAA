# SEAL_AUTHORITY_DOCTRINE.md — Constitutional Doctrine for SEAL Authority

> **Authority:** arifOS constitutional canon (F13 ratified, 2026-07-14)
> **Status:** v1.0 — EFFECTIVE on ratification
> **Witnessed by:** sovereign ack (F13), arif_judge (888), seal_chain (VAULT999)
> **Forge cycle:** FEDERATION-ALIGN-2026-07-14

---

## 1. Definition

**SEAL** is the constitutional mark of irreversible commitment. Once sealed:
- The artifact enters VAULT999 append-only ledger
- The hash binds the moment to the chain (arrow of time)
- All three witness channels must have been present at seal time
- Reversal requires a new SEAL of equal or higher authority (HOLD or VOID)

A SEAL without authority is **a forgery**. A SEAL without witness is **a hallucination**. A SEAL without audit is **a crime**.

## 2. Authority Bands (F1 AMANAH × F13 SOVEREIGN)

| Band | Issuer | Can SEAL | Cannot SEAL |
|---|---|---|---|
| **SOVEREIGN** | F13 (Arif) | Anything, including override of existing SEALs, identity binding, rotation | — |
| **FULL** | arif_judge with cryptographic actor binding | Constitution-compliant SEALs (governance, geometry, identity binding) | Sovereign-only acts (rotation, override, T3 irreversible) |
| **LIMITED_MUTATE** | arif_judge with session-scoped lease | Reversible session-level SEALs, tool registrations, salience audits | Constitutional changes, identity binding, irreversible ops |
| **OBSERVE_ONLY** | Anonymous / claimed actor | NEVER SEAL — return HOLD/VOID instead | SEAL authority |
| **ANONYMOUS** | Unverified identity | NEVER SEAL | SEAL authority |

**Default:** SEAL requires SOVEREIGN or FULL band. LIMITED_MUTATE may seal in narrow session scope. OBSERVE_ONLY and ANONYMOUS cannot seal.

## 3. Witness Requirement (F3 WITNESS — Nash 1950)

For a SEAL to be valid, all three witness channels must be present at seal time:

```
W³ = ∛(Human × AI × External) ≥ 0.70
```

| Channel | Who | Example |
|---|---|---|
| **Human** | F13 sovereign, OR named operator with F13 attestation | `human: "ARIF-F13"` |
| **AI** | Agent doing the work + a peer witness | `ai: ["kimi-code-FI-008", "antigravity-AAA"]` |
| **External** | Independent reality measurement | `external: "seal_chain_head+geo_observation"` |

**Zero in any channel → SEAL voided → HOLD.**

This is the floor for BIJAKSANA (G = A·P·E·X·Φ at threshold).

## 4. SEAL Authority Lifecycle

```
┌──────────────────────────────────────────────────────────┐
│  Phase 0: Pre-condition                                   │
│  - Actor identity cryptographically verified (sct_v1)   │
│  - Witness channels all present (W³ ≥ 0.70)             │
│  - Authority band ≥ LIMITED_MUTATE for reversible SEAL  │
│  - Authority band = SOVEREIGN for constitutional SEAL    │
└──────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│  Phase 1: SEAL request                                   │
│  - Tool emits SEAL request with:                         │
│    * action_class (OBSERVE | MUTATE | REVERSIBLE |       │
│      IRREVERSIBLE | CONSTITUTIONAL)                      │
│    * evidence (artifacts, hashes, witness tuple)         │
│    * scope (what gets sealed)                            │
│    * ttl (if applicable)                                 │
│  - arif_judge evaluates                                  │
└──────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│  Phase 2: arif_judge verdict                             │
│  - G = A·P·E·X·Φ computed                                │
│  - C_dark = A·(1-P)·(1-X) computed                       │
│  - If G ≥ 0.80 AND C_dark < 0.30 AND W³ ≥ 0.70 → SEAL   │
│  - Else HOLD or VOID                                     │
└──────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│  Phase 3: VAULT999 append                                │
│  - seal_chain.js writes enriched entry (v2)             │
│  - Includes: seq, prev_hash, this_hash, merkle_root,    │
│    witness, payload, signature                           │
│  - Head updated, chain head hash broadcast to organs    │
└──────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│  Phase 4: Cooling (post-seal)                            │
│  - 24-hour cooling period for constitutional SEALs       │
│  - forge_cool_drift / forge_cool_pattern observations    │
│  - If drift detected within cooling → reseal with delta  │
└──────────────────────────────────────────────────────────┘
```

## 5. Reversal and Override

A SEAL can only be reversed by:

| Override type | Authority required | Witness | Audit trail |
|---|---|---|---|
| **HOLD** (suspend, not reverse) | FULL or SOVEREIGN | Human + AI | Full re-seal event |
| **VOID** (invalidate, not reverse) | SOVEREIGN only | Human + AI + External | Full re-seal event |
| **Override** (replace with new SEAL) | SOVEREIGN only | Human + AI + External | Old + new SEAL cross-linked |

**The original SEAL remains in the ledger.** Override does not erase. This is the arrow of time: a SEAL once written cannot be un-written. Only its effect can be suspended or replaced by a higher-authority event.

## 6. SEAL Authority for arifOS Federation (canonical mapping)

| Action | Min Authority | Witness | Seal Type |
|---|---|---|---|
| Session bind (arif_init) | OBSERVE_ONLY (provisional) → FULL (after attest) | AI (until sovereign ack) | session.seal |
| Session seal close | LIMITED_MUTATE | AI | session.seal |
| Tool registration | FULL | AI + External | tool.register |
| Constitutional change (F1-F13) | SOVEREIGN | Human + AI + External | constitutional.verdict |
| Identity binding | SOVEREIGN | Human + AI + External | identity.binding |
| Salience recalibration | FULL | AI + External | salience.recalibrate |
| Chain fork acknowledgment | SOVEREIGN | Human + AI + External | chain.fork_ack |
| Cycle seal (audit close) | FULL | Human + AI + External | audit.cycle.seal |
| Irreversible mutation | SOVEREIGN | Human + AI + External | irreversible.seal |

## 7. SEAL Authority vs JURISDICTION

A SEAL is not authority over the world. A SEAL is authority over the **ledger entry** that records what happened.

If `forge_execute` SEALs a deletion, the deletion happens; the SEAL records it. The deletion is reversible in the world only by another SEAL of higher authority. The first SEAL stays in the ledger forever.

This separation — SEAL over ledger vs authority over world — is F1 AMANAH + F11 AUDIT working together.

## 8. Failure Modes

| Failure | Symptom | Mitigation |
|---|---|---|
| SEAL without witness | W³ = 0 in one channel | Verifier rejects; HOLD returned |
| SEAL with wrong band | Anonymous tries to SEAL | PolicyGate denies; returns 401 |
| SEAL with hash drift | Payload tampered after seal | this_hash mismatch; chain break detected |
| SEAL during outage | VAULT999 unreachable | Buffer seal in local ledger; replay on recovery (with witness gap logged) |
| SEAL with stale chain | Head mismatch | Re-anchor from canonical head; reseal |

## 9. Cross-references

- **F1 AMANAH** — reversibility-coupled action_class
- **F2 TRUTH** — evidence labeled OBS/DER/INT/SPEC
- **F3 WITNESS** — Nash 1950 tri-witness geometric mean
- **F8 GENIUS** — `G ≥ 0.80` threshold
- **F11 AUDIT** — append-only ledger invariant
- **F13 SOVEREIGN** — final authority on override

## 10. Effective Date and Sovereign Override

This doctrine is **EFFECTIVE** upon:
- F13 sovereign ack (received 2026-07-14 via session SEAL-9efcb703825e4682)
- arif_judge SEAL pending (gated on Step 7 phase 1 live)
- Phase 1 cutover pending (7-day parity after shadow mode)

Sovereign retains authority to amend any clause of this doctrine via SEAL of equal or higher precedence.

---

## Provenance

- Drafted by: `kimi-code-FI-008` (session SEAL-9efcb703825e4682)
- Audit cycle: FEDERATION-ALIGN-2026-07-14
- Vault head at draft time: seq 9914, sha256:6517b1fb1171e9461c1d8af634119acdc031e61767fbe44e0547a7336544880b
- Cross-references: SALIENCE_FUNCTION.md §3, IDENTITY_BINDING_SPEC.md §9, forge_salience_recompute_SPEC.md §7

DITEMPA, BUKAN DIBERI.