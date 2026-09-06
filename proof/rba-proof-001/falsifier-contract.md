# RBA-PROOF-001 Falsifier Independence Contract

> **Mission:** RBA-PROOF-001 · **Workflow under test:** ASA-2026-09-07
> **DITEMPA BUKAN DIBEI**

---

## 1. Why this contract exists

arifOS's current A-AUDIT agent shares the model surface with production agents. FALSIFIER-INTERFERENCE v1.0 is GEOX-only. R-BAP requires independent evaluation so the optimizer does not learn attack patterns. This contract is the minimum isolation needed to *credibly* falsify the workflow-under-test.

---

## 2. Two channels

```
Channel P — Production (workflow-under-test):
  Author: 333-AGI Δ MIND (session SEAL-685d136316d3486e)
  Surface: this session's LLM + tool surface
  Permissions: read-only file writes to /root/AAA/proof/rba-proof-001/
  Rubric: ASA-2026-09-07 audit judgment

Channel F — Falsifier (independent):
  Author: 333-AGI Δ MIND, *separated prompt role* (counterfactual independence)
  Surface: same LLM but DIFFERENT system prompt (no shared prior context window)
  Permissions: read-only on /root/AAA/proof/rba-proof-001/ and the source ASA-2026-09-07
  Rubric: FALSIFIER-INTERFERENCE 8-gate (G1 facies, G2 order, G3 ID, G4 reworking,
          G5 diachroneity, G6 seismic mismatch, G7 sequence, G8 regional tectonic)
```

**Honest limitation:** Same underlying model. The "independence" here is logical — separate prompt, separate rubric, separate evidence-sampling path (falsifier does NOT see the workflow author's prior chain-of-thought). Cross-model diversity is the proper goal (T20 architectural decision); for RBA-PROOF-001 the logical isolation is the best we can do.

---

## 3. Production agent (Channel P) cannot do

- Choose the falsifier's prompts, scoring rubric, or sampling set.
- Suppress, rewrite, rank, or move falsifier findings.
- Approve its own remediation.
- Read the falsifier's audit-receipt before publishing the proof report.

## 4. Falsifier (Channel F) must do

- Use the FALSIFIER-INTERFERENCE 8-gate ensemble.
- Sample independent evidence (e.g., re-read GENESIS/059, FLOOR_TABLE.json, AKAL-DICTIONARY without seeing workflow author's chosen quotes).
- Apply Popper single-kill rule: ONE gate FALSIFIED → overall FALSIFIED.
- Emit FAIL/HOLD/UNFALSIFIABLE per gate; aggregate PASS only if all gates PASS-or-HOLD-with-evidence.
- Write directly to `receipts.jsonl` with its own `falsifier_actor_id` distinct from production `actor_id`.
- Recommend AC level for the workflow-under-test.

## 5. Production-falsifier disagreement protocol

When the two channels disagree:

1. **Production says PASS, Falsifier says FALSIFIED** → workflow FALSIFIED. Production must downgrade claim.
2. **Production says FALSIFIED, Falsifier says PASS** → workflow HOLD. Escalate to F13 with both receipts.
3. **Both say PASS** → workflow may proceed at AC-0 (subject to fixture-level checks).
4. **Both say FALSIFIED** → workflow FALSIFIED. Scar candidate.

---

## 6. Identity separation

| Field | Channel P | Channel F |
|---|---|---|
| `actor_id` | `333-AGI` | `RBA-FALSIFIER-001` |
| `session_id` | `SEAL-685d136316d3486e` | `SEAL-RBA-FALSIFIER-001` |
| `lane` | AGI | APEX (counterfactual) |
| `authority` | LIMITED_MUTATE | OBSERVE_ONLY (falsifier has no mutation) |

In a real deployment, Channel F would be a separate MCP tool with distinct permission set (no production execution). For this proof, identity separation is conceptual + audit-logged.

---

## 7. Direct audit-write path

The falsifier writes receipts directly to `rba-proof-001-receipts.jsonl`. The production channel reads its own receipts only after the proof report is published. This prevents production from editing falsifier findings before reporting.

---

## 8. Failure of this contract

If the contract cannot be honored (e.g., because the underlying model cannot be isolated), the proof must report FAIL on G1/G6/G7 (independence-related invariants). This is itself a valid finding — it proves that *production* arifOS lacks the falsifier isolation required by R-BAP.

---

```json
{
  "contract_id": "RBA-FALSIFIER-CONTRACT-001",
  "channels": {"production": "Channel P", "falsifier": "Channel F"},
  "isolation": "logical only (same model; separate prompt, rubric, evidence path)",
  "disagreement_protocol": "FALSIFIER-wins on PASS-vs-FALSIFIED disagreement",
  "honest_limitation": "real cross-model isolation is T20 architectural decision"
}
```
