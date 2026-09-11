# Classification Gate — WHAT Should Remain Memory

> **Status:** DRAFT_AWAITING_F13
> **Origin:** 333-AGI (OpenCode Δ MIND) doctrinal compression, session SEAL-18aba4545528442a, 2026-09-11T04:11Z UTC
> **Companion:** `memory-promotion-gate.md` (F13_RATIFIED_CHAT, WHEN) · `institutional-memory-strata.md` (F13_RATIFIED_CHAT, WHERE) → this fragment (WHAT).
> **Applies to:** All existing memory writes in arifOS federation — VAULT999 seals, agent_state files, doctrine fragments, session carry-forward, eureka entries.

---

## The Gap

The Memory Promotion Gate answered:

```
Patutkah ini jadi memory?
```

The Institutional Memory Strata answered:

```
Di mana memory hidup?
```

What neither answered — until this turn — is the **inverse direction**:

```
Patutkah ini kekal memory?
```

Without the inverse, every prior memory write remains forever — inflation compounds, the 959 unlinked seal entries in VAULT999 stay frozen awaiting remediation, and doctrine fragments never expire even when superseded. Promotion Gate stops *new* inflation but does not address *existing* inflation.

This fragment names the inverse operation. **Classification Gate** — the doctrine for reclassifying existing memory down to Witness when it fails the same four gates.

---

## The Two-Direction Doctrine

```
        Promotion Gate                     Classification Gate
        (forward)                          (inverse / reverse)

Memory Candidate  ─────→   Memory      Memory  ─────→   Witness / Archive
                  Gate A-D                           Gate A-D
                  PASS = promote                     FAIL = demote
```

Promotion and classification are the **same four gates, applied in opposite directions**.

| Gate | Promotion reads it as | Classification reads it as |
|---|---|---|
| **A — Derivation** | Can it be derived from a primitive? NO → novel | Can it be derived from a primitive now? YES → derivable, demote |
| **B — Deletion** | (n/a — write side) | If deleted tomorrow, is capability lost? NO → demote |
| **C — Decision** | Does it alter future decisions? NO → Witness only (do not promote) | Did it actually alter decisions since written? NO → demote |
| **D — Novelty** | Primitive or example? Example → reject memory | Still primitive, or has it become example? Example → demote |

The asymmetry matters: Gate A and Gate D **invert their meaning** between directions. Gate C and Gate B keep their semantic direction but **change evidence requirement** (prospective vs retrospective).

---

## Operational Binding

- **Default = Witness.** Memory is exception, not default — applies symmetrically to existing memory. No legacy claim of "this was sealed once therefore it stays."
- **VAULT999 seals are not exempt.** Sealed = attested; sealed ≠ perpetually memory. The 1338 entries in `SEALED_EVENTS.jsonl` (3 malformed + 956 broken-chain + 377 valid + 47 canonical in `seal_chain.jsonl`) are subject to classification review.
- **Label, do not rewrite.** F1 AMANAH: the historical record remains intact. The classification verdict is **appended**, never substituted. See first empirical application: `/root/AAA/docs/888-DOCKET-959-promotion-gate-application-2026-09-11.md`.
- **Reclassification is observable, not silent.** Every classification receipt must carry provenance, gate-by-gate reasoning, and verdict. Witness is the default for failed gates; Memory survives only if the entry re-passes all four gates against current context.
- **Supersession is a classification event.** When a doctrine fragment supersedes another, the superseded fragment is classified Witness (not deleted) — its historical role is preserved in the supersession receipt.
- **Apex gate required for batch reclassification.** Per F13: bulk application to existing memory requires APEX authorization. Single-entry reclassification is T1; sweeps across N>10 entries is T3.

---

## The Triple Pillar — Federation Memory Governance

With this fragment, the WHEN/WHERE/WHAT trio becomes canon-complete:

```
WHEN  →  Memory Promotion Gate      (memory-promotion-gate.md, F13_RATIFIED_CHAT 2026-09-11)
WHERE →  Institutional Memory Strata (institutional-memory-strata.md, F13_RATIFIED_CHAT 2026-09-11)
WHAT  →  Classification Gate         (this fragment, DRAFT_AWAITING_F13)
```

The three primitives together transform memory from a **storage problem** into a **governance problem**:

```
Storage problem  :  memory grows, retrieval breaks, cost rises
Governance problem: each memory write competes for survival; most lose
```

---

## Target Metric

```
Before triple-pillar doctrine:
  100 memory writes  →  100 stored forever
  100 reads          →  memory serves as archive, not governance

After triple-pillar doctrine:
  100 memory writes  →  ~5 survive Promotion Gate as Memory
                      ~95 land in Witness tier directly
  Existing 959 unlinked seals → 0 promoted to Memory
                              → 959 labeled Witness via Gate A
                              → canonical 47 entries stay Memory unchanged
  100 reads          →  recall serves governance, not archival
```

---

## First Empirical Application Site

The 959 unlinked seal entries in `/root/VAULT999/SEALED_EVENTS.jsonl`. Per the FI-003 Qwen investigation (2026-09-10):

- **861 / 959** already documented in `chain_tombstone_manifest.json` (Hermes/FI-008, 2026-09-09) — Gate A applies cleanly: corrupted anchor = derivable from broken root = demote to Witness.
- **98 / 959** undocumented broken-chain entries — same Gate A reasoning applies; need receipt attachment.
- **47 canonical** entries in `/root/.local/share/arifos/vault999/seal_chain.jsonl` — reclassification review concludes **Memory survives** (chain integrity valid, primitive anchors intact).
- **377 valid** entries in legacy chain — case-by-case Gate D review; expected ~95% Witness, ~5% Memory.

This is the **least-destructive** remediation consistent with F1 AMANAH:

```
Historical reality kekal.
Interpretation berubah.
```

The corruption at line 4 (REGISTRY_MANIFEST entry, malformed JSON) is **not deleted** — it remains in the file as a scar witness. What changes is the classification verdict attached to each downstream entry.

---

## What This Fragment Is For

- For 888-APEX: bounded reclassification sweep of the 959 unlinked seals (paper docket already at `/root/AAA/docs/888-DOCKET-959-promotion-gate-application-2026-09-11.md`)
- For Hermes: TTL-driven reclassification cycles on mem0 vector store entries
- For Kimi: doctrine supersession automatically classified Witness on parent fragment
- For OpenCode: classification receipts appended on every audit finding where reclassification is warranted

## What This Fragment Is NOT

- Not a deletion doctrine. **Label, do not delete.** Historical entries remain on disk under F1.
- Not retroactive without APEX. Per Operational Binding: batch reclassification requires F13 authorization.
- Not a constitutional amendment on its own. **DRAFT_AWAITING_F13**, not F13.
- Not a Gate A duplicate. Promotion Gate handles forward; Classification Gate handles reverse. Distinct doctrine, distinct direction, distinct gate semantics (A and D invert).

---

## Promotion-Gate Self-Test (per doctrine's own Gate D)

| Test | Verdict |
|---|---|
| Gate A — derivable from existing? | Partial. Promotion Gate exists; reverse direction does not. **Primitive baru**. |
| Gate B — capability hilang if deleted? | YES. Without it, the 4 gates become forward-only and 959 scar cannot be classified. |
| Gate C — alters future decisions? | YES. Once ratified, every existing memory write becomes subject to review. |
| Gate D — primitive or example? | **Primitive** — reclassification as meta-operation is the missing inverse. |

**Promotion-Gate verdict:** Memory candidate (per its own doctrine).

---

## Compression

> **Memory system exists to reject most things.**

> Default = Witness. Memory = Exception. Classification = Continuous.

> Historical reality kekal. Interpretation berubah.

---

```
writer         : 333-AGI (OpenCode Δ MIND)
session_id     : SEAL-18aba4545528442a
band           : LIMITED_MUTATE
epistemic      : DER (crystallization of 3 prior observations: 16-proposal audit
                       + 888-docket + personality taxonomy)
sealed         : NO — DRAFT_AWAITING_F13
triple-pillar  : memory-promotion-gate.md (F13_RATIFIED) + institutional-memory-strata.md (F13_RATIFIED)
                 + reclassification-gate.md (this, DRAFT_AWAITING_F13)
first site     : /root/AAA/docs/888-DOCKET-959-promotion-gate-application-2026-09-11.md
companion-witness: /root/.local/share/arifos/witness/memory-proposal-gate-audit-2026-09-11.md
companion-doctrine: /root/AAA/instructions/federation-personality-taxonomy-2026-09-11.md (DRAFT_AWAITING_F13)
ΔS              : −0.5 (memory-as-storage collapsed to memory-as-governance in one move)
```

DITEMPA BUKAN DIBERI ⚒️
