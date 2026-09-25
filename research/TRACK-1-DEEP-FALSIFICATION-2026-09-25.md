# Track #1 Deeper Falsification — Witness Findings (2026-09-25 07:38 MYT)

> **Status:** OBSERVATION (not classification). F12 says surface, don't swallow.
> **Method:** Sovereign ran independent verify on Track #1 L13; surfaced
> two follow-on findings. FI-005 cross-validated each by reading source.

---

## F1 — namespace collision: `outcome_class` ↔ `execution_outcome_class`

**Claim:** Same name in two organs, different enum body.

**Cross-validated evidence (file content, MEASURED):**

| File | Line | Reference | Enum body |
|---|---|---|---|
| `/root/arifFlow/src/lineage_query.rs` | 488 | `pub outcome_class: String,` | `recovery | regression | neutral` |
| `/root/arifFlow/src/lineage_query.rs` | 834 | `"outcome_class": "recovery"` | (test fixture) |
| `/root/A-FORGE/src/infrastructure/bridges/arifFlowBridge.ts` | 96 | `input.outcome_class === "UNKNOWN_OUTCOME"` | `SUCCESS | FAILURE | UNKNOWN_OUTCOME | RECOVERY | DENIED` |

**K1 fatwa analog:** Same exact class as the L14 nucleus collision that K1 fatwa closed (kernel SEAL vs linkgraph ABANDON). Same fix pattern: prefix coordinate systems.

**Hang's proposed fix:** A-FORGE bridge should put A-FORGE value under
`payload.execution_outcome_class`, and arifFlow should add a typed field.

**Severity:** MEDIUM. The collision has a known overlap (`RECOVERY`) but the
other 4 strings are disjoint. Risk is **semantic confusion in audit trails**
more than runtime break.

---

## F2 — silent drop in FlowReceipt deserialize

**Claim:** `FlowReceipt` has no `outcome_class` field AND no `deny_unknown_fields`.
A-FORGE bridge writes `outcome_class: "UNKNOWN_OUTCOME"` to wire → arifFlow
deserialize silently drops → ledger has no record of WHY `floor_verdict: Caution`.

**Cross-validated evidence (file content, MEASURED):**

| File | Line | Content |
|---|---|---|
| `/root/arifFlow/src/receipt.rs` | 472 | `#[derive(Debug, Clone, Serialize, Deserialize)]` |
| `/root/arifFlow/src/receipt.rs` | 472-560 | struct body — Identity, Actor, FlowStep, Cost, Epistemic, Governance, Witness, Merkle — **NO `outcome_class` field** |
| full file | — | grep `deny_unknown_fields` → 0 hits |
| `/root/A-FORGE/src/infrastructure/bridges/arifFlowBridge.ts` | 113 | `if (input.outcome_class !== undefined) receipt.outcome_class = input.outcome_class;` |
| `/root/A-FORGE/src/infrastructure/bridges/arifFlowBridge.ts` | ~119 | `JSON.stringify(receipt)` — sends `outcome_class` on wire |
| `/root/A-FORGE/src/infrastructure/bridges/arifFlowBridge.ts` | — | grep `jcs_body_hash` → 0 hits → no hash-mismatch risk |

**The round-trip:** A-FORGE constructs receipt → POST /ingest → arifFlow
deserialize → silently truncates → ledger stores receipt with
`floor_verdict: Caution` but no `outcome_class` field.

**Severity:** HIGH for state-transition-discipline compliance.
- `floor_verdict: Caution` survives (counts in FQ — §2.6 honored).
- `outcome_class: UNKNOWN_OUTCOME` does NOT survive.
- Result: VAULT999 can't tell "Caution because UNKNOWN" from "Caution because anything else."
- Witness chain has visible verdict with invisible reason.

---

## Cross-check on the `jcs_body_hash` hypothesis

Hang's falsification hypothesis: "If arifFlow recalculates jcs_body_hash from the wire, then having outcome_class in the wire would cause hash mismatch and rejection."

**fi005 verification:** Bridge does NOT set `jcs_body_hash`. Field not present in
arifFlow FlowReceipt struct either. No hash-mismatch pathway. So the failure
mode is silent acceptance, not rejection. Hang's note that the failure mode is
"kelas yang lebih halus" (more subtle class) is correct.

---

## Scanners applied to these findings

| Scanner | Verdict |
|---|---|
| 1 Registry coherence | F1 + F2 = REAL MEASURED defects |
| 2 Tool reachability | Bridge arifFlowBridge.ts → /ingest works (POST 200 likely); arifFlow deserializer does NOT roundtrip the field. PARTIAL. |
| 3 Metadata coherence | A-FORGE 5-state enum ≠ arifFlow 3-string enumeration ≠ FlowReceipt field set. 3 different shapes. DRIFT. |
| 4 Input transport | Wire layer transports the field correctly. Defect is downstream (deserialize). |
| 5 Contradiction semantics | Engine does not detect — silently accepts. SAME class as Hermes Defect-B. |
| 6 Machine-contract witness | Bridge holds the contract; arifFlow accepts contract breach as permitted. Silent-drift — VIOLATES witness doctrine. |

---

## F12 disposition

Per F12 contradiction-vs-dissent doctrine: do not collapse findings into the original verdict.

- L13 patch = MEASURED at OBSERVED — held.
- F2 silent-drop = MEASURED — separate real defect.
- F1 namespace collision = MEASURED — separate real defect.

Three verdicts. None eats the other. F12 explicitly forbids "PASS_TECHNICAL swallows deeper FALSIFICATION_FINDING."

---

## Scope boundary — what FI-005 does NOT do

1. ❌ **Does not patch arifFlow receipt.rs** — different organ, different commit hash lineage, would break Track #1's `8b44cd74`.
2. ❌ **Does not spawn Track #1.5** — sovereign disposition required.
3. ❌ **Does not classify Track #1** — sovereign.
4. ❌ **Does not push** — T3 territory.
5. ✓ **Records the witness anchor.** Carries the load forward. Preserves the contradiction.

DITEMPA BUKAN DIBERI ⚒️
