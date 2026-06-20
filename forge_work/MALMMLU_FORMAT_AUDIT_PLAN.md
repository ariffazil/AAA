<!-- MALMMLU_FORMAT_AUDIT_PLAN.md -->
<!-- SOT-MANIFEST
owner: Muhammad Arif bin Fazil
plan_id: MALMMLU-FORMAT-AUDIT-2026-06-20
authority: F13 SOVEREIGN
status: PLAN_APPROVED
epistemic_status: INVESTIGATION_PLAN
-->

# MalayMMLU Format-Fix Audit Plan

**Plan ID:** MALMMLU-FORMAT-AUDIT-2026-06-20  
**Authority:** F13 SOVEREIGN  
**Date:** 2026-06-20 UTC  
**Target:** `UMxYTLAILabs/MalayMMLU` dataset  
**Claim under test:** Faysal format-fix critique — GPT-4o scores ~0% on MalayMMLU in its native format and ~83–90% after reformatting answer choices.

---

## Why This Matters

If the claim is true, then:
1. MalayMMLU scores reported by YTL AI Labs and others are **format-inflated**, not capability-inflated.
2. The headline "ILMU outperforms global models on MalayMMLU" may be a measurement artifact.
3. No honest model comparison between Malaysian and global LLMs is possible using MalayMMLU in its current form.

This audit directly supports the **Gate 3 (Evidence)** and **Gate 2 (Truth)** findings in `SEAL-ILMU-FFF-2026-06-20.md`.

---

## Hypothesis

- **H0 (null):** MalayMMLU formatting does not materially depress global-model accuracy. Scores are valid.
- **H1 (Faysal):** MalayMMLU formatting depresses global-model accuracy to near-zero; reformatting recovers 80%+ accuracy.

---

## Methodology

### 1. Dataset acquisition
Load `UMxYTLAILabs/MalayMMLU` from Hugging Face (`datasets` library) or GitHub JSON/CSV.

### 2. Prompt construction
For each question, create **two conditions**:

#### Condition A — Native format (as published)
Use the exact question + choices layout from the dataset. No reformatting.

#### Condition B — Fixed format
Standardise layout:
- Clear `Question:` header
- Enumerated choices `A)`, `B)`, `C)`, `D)` on separate lines
- Explicit instruction: "Answer with only the letter A, B, C, or D."

### 3. Models under test
At minimum:
- `gpt-4o` (OpenAI)
- `claude-sonnet-4.5` (Anthropic) — if available
- `qwen2.5-72b-instruct` or `qwen-max` (Alibaba) — strong multilingual baseline
- `ilmu-nemo-nano` (YTL) — for contrast

Optional:
- `gemini-1.5-pro` (Google)
- `llama-3.1-70b-instruct` (Meta)

### 4. Sampling
Full dataset = 24,213 questions. For cost control:
- **Pilot:** 100 random questions across all subjects
- **Full audit:** 1,000 random questions (or full dataset if budget allows)
- Stratify by subject and difficulty if metadata available

### 5. Evaluation
- Extract predicted letter (A/B/C/D) from model output.
- Compare to ground-truth label.
- Report accuracy per condition, per model, per subject.
- Report confidence intervals (Wilson score).

### 6. Statistical test
- Paired comparison per question between Condition A and Condition B.
- McNemar's test for significant difference.

---

## Success Criteria

| Outcome | Interpretation |
|---------|----------------|
| GPT-4o native ≈ fixed (both reasonable) | H0 holds; MalayMMLU is valid |
| GPT-4o native ≈ 0%, fixed ≈ 80%+ | H1 holds; format inflation confirmed |
| Intermediate gap | Partial format artifact; quantify |
| ILMU native >> global native | Suggests ILMU may be overfit to MalayMMLU format |

---

## Deliverables

1. `malmmlu_format_audit.py` — reproducible script
2. `malmmlu_format_audit_results.json` — per-question predictions and scores
3. `MALMMLU_FORMAT_AUDIT_REPORT.md` — findings with charts
4. Update `SEAL-ILMU-FFF-2026-06-20.md` Gate 3 / Gate 2 with audit result

---

## Cost Estimate

- Pilot (100 questions × 4 models × 2 conditions): ~$2–5
- Full (1,000 questions × 4 models × 2 conditions): ~$20–50
- Full dataset (24k × 4 × 2): ~$500–1,000 — only if funded

---

## Risks

- **API key availability:** Need OpenAI + Anthropic + Qwen keys. If unavailable, run only models with existing keys.
- **Dataset license:** MalayMMLU is CC BY 4.0 per paper; audit outputs are fair-use research.
- **YTL API rate limits:** ILMU free tier may throttle large batches.

---

## Next Action

Run the pilot using `malmmlu_format_audit.py` with `N=100` and `gpt-4o` + `ilmu-nemo-nano` to confirm effect size before committing to full audit.

---

*DITEMPA BUKAN DIBERI — Forged, Not Given.*
