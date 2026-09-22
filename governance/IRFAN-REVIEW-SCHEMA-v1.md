# IRFAN-REVIEW-SCHEMA-v1 — Stewardship Review Contract (advisory, non-verdict)

**Status:** **F13_RATIFIED_CHAT — 2026-09-23** (sovereign in-band instrument,
quoted: *"LIFT THE HOLD. ratify seal all…"* + earlier *"RATIFY ARIF → SALAM →
IRFAN"*) — forged under those F13 directives.
**Author:** FI-003 (Qwen Code) · **Tree:** `AAA/governance` (canon-mutate cycle)
**Provenance map:** `canon/STAGE23-REVIEW-SCHEMA-AUDIT-2026-09-23.md`
(evidence: probes, collision findings, pairing matrix, adversarial tests).
**Class:** Layer-A/B narrative+contract only — **no runtime wiring** (a code
cycle with its own adversarial tests is required before any emission becomes
live; that cycle is NOT part of this directive).

---

## 1. Purpose (what this is)

A **second, advisory channel** that rides alongside the kernel verdict and
asks one family of questions the verdict does not: *does this proceed AND
deserve to proceed?* (the ratified pathway's recognition question, made
operational as review state).

It is **receipt-grade annotation**. The kernel verdict
(`SEAL / SABAR / HOLD / VOID / OBSERVE_ONLY / 888_HOLD`) remains the ONLY
authority-bearing output — unchanged, undiluted, always dominant.

## 2. The three laws (non-negotiable — evidence in the sealed map)

- **C1 · Namespace law.** Review state lives ONLY at
  `meta.stewardship_review = { state ∈ {CLEAR, CONCERN, ESCALATE}, reasons[], axis? }`.
  Never a `*verdict*`-suffixed key, never `decision` — the reconcile walker's
  bearing set is exactly `{verdict, effective_verdict, canonical_verdict,
  verdict_code, reasoning_verdict, decision, sufficiency_verdict}`; a bearing-set
  collision is the S4 manufactured-divergence defect (empirical cost: one full
  night, ~15 deploy cycles). Regression-test pins the7-key set.
- **C2 · Authority immutability.** Review NEVER writes `effective_verdict`,
  `can_mutate`, `seal_allowed`, `mutation_allowed`, any floor, or any L01–L13
  gate. Review ABSENT ⇒ every authority field byte-identical to review-PRESENT
  (advisory zero-cost property, adversarial test #4).
- **C3 · ESCALATE reuse-or-rename.** `ESCALATE` already has four live meanings
  (`verification_envelope.ESCALATE → Arif`, `topology_actuator.escalate → L13`,
  `narrative_tension`, `arif_judge mode=escalate`). The review state maps its
  `ESCALATE` **onto those existing lanes** (escalation target = the same
  Arif/L13/888_HOLD destinations). No fifth meaning, no new escalation queue.

## 3. Vocabulary (complete — three tokens, nothing else)

| State | Meaning | Pairing rule |
|---|---|---|
| `CLEAR` | no stewardship concern on record | pairs with any verdict |
| `CONCERN` | named stewardship concern on record (receipt-grade; proceed unchanged) | pairs with any verdict |
| `ESCALATE` | stewardship matter referred to existing escalation lane | pairs **only** with `HOLD/SABAR/VOID` — `SEAL+ESCALATE` is incoherent (proceeding ∧ undecided) and is rejected at composition |

## 4. Pairing matrix (normative)

```text
SEAL  + CLEAR      ✅   SEAL  + CONCERN   ✅   SEAL  + ESCALATE   ❌ (rejected)
HOLD  + CONCERN    ✅   HOLD  + ESCALATE  ✅   any   + <override>  ❌ VOID by C2
```

## 5. Failure modes (six — the contract exists to prevent these)

1. **Misnamed-key storm** (review enters bearing set → S4 divergence) → C1 + pin-test.
2. **ESCALATE laundering** (review cited as if it were a floor/block) → C2: it cannot touch authority fields; probe = mutate-behavior identical with/without ESCALATE.
3. **CLEAR used to override HOLD** (or any verdict) → C2 dominance.
4. **De-facto floor** (agents learn to stop on CONCERN → unratified F14) → doctrine line: CONCERN never blocks; blocking requires a real floor with F13 falsification.
5. **Parallel escalation queue** (fifth ESCALATE meaning → lost referrals) → C3 lane-mapping.
6. **Verdict-enum inflation** (CLEAR etc. added to `CANONICAL_VERDICTS`) → VOID by vocabulary scope; review tokens have their own closed set.

## 6. Rollout (DETECT-first — proven pattern: `reality-claim-gate`)

- **Phase 1:** emit `meta.stewardship_review` on responses only; zero effect on
  any gate (adversarial test: engine-level behavior unchanged).
- **Phase 2 (only after F13 review of live Phase-1 receipts):** advisory reads
  in prompts/lane-docs (agents may cite CONCERN in their reasoning, never as a stop).
- **Phase 3+:** any *behavioral* effect = new falsification cycle (Canon #0
  three-test), not part of this contract.

## 7. Ten essential tests (acceptance set before Phase-1 code)

1. bearing-key set pinned exactly to the7 keys (regression).
2. authority-field byte-equality: review present vs absent.
3. `SEAL+ESCALATE` composition rejected.
4. `ESCALATE` present ⇒ `can_mutate`/`seal_allowed`/floors unchanged (unit).
5. review tokens absent from `CANONICAL_VERDICTS` (unit).
6. escalate-lane mapping resolves to existing destinations (Arif/L13/888_HOLD) — no new handler.
7. Phase-1 emission does not alter any existing test outcome (suite diff = 0).
8. receipt format validates (state enum + reasons non-empty).
9. bearing-set collision attempt → walker unaffected (synthetic old-key probe still vetoes as today — vigilance preserved).
10. absent-review response hash-stable vs pre-deploy baseline sample.

## 8. Scope fence (what this contract does NOT do)

- No runtime emission tonight (code cycle separate, adversarial-tested first).
- No floor · no agent · no verdict-enum change · no escalation queue ·
  no authority-field access · **KEEP THE FLOORS untouched** (`e-b425e4fe`).
- The stewardship-LENS institutionalization remains VOIDED; this contract
  operationalizes *review annotation* under the ratified pathway, nothing more.
- Four-role separation preserved: whoever later emits review ≠ who judges ≠
  who executes ≠ who witnesses.

*Sealed as-tested: every claim above traces to the sealed audit map; hashes +
canon-mutate receipts in the accompanying carry_forward entry.*
