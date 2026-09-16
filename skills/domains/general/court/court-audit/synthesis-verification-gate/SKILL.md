---
name: synthesis-verification-gate
description: Run before synthesis outputs to classify every claim.
version: 1.0.0
author: hermes (F13 directive)
license: MIT
trigger:
  - synthesis output
  - research summary
  - multi-claim report
  - exploration mode
  - deep research
  - cross-domain analysis
metadata:
  hermes:
    tags: [governance, epistemic, hallucination, verification]
    related_skills: [verify-gate, observe-ground, claim-receipt-discipline]
---

# Synthesis Verification Gate

> **Forged:** 2026-08-26 by F13 directive ("deep research how to solve this")
> **Scar:** Reddit exploration — 65% of claims were HEARSAY presented as fact
> **Wires to:** F2 Truth, Falsification Engine, W_scar, OBS/DER/INT/SPEC
> **DITEMPA BUKAN DIBERI**

---

## When to Use

- Before ANY synthesis output (research summaries, exploration reports, multi-source analysis)
- Before ANY output that contains more than 2 factual claims
- When output will influence decisions (money, reputation, health, technical direction)
- When browsing unfamiliar domains ("exploration mode")
- When claims span multiple sources with different reliability levels
- NOT for: routine operational output, single-source factual retrieval, internal logging

---

## The Problem

AI agents fill knowledge gaps with plausible-sounding but unverified claims.
This is not a bug — it's a structural incentive: training rewards confident
guesses over calibrated uncertainty. The fix is mechanical enforcement, not
good intentions.

**Root cause (Kalai et al., OpenAI 2509.04664):** Hallucination is rational
test-taking. Abstention scores zero; guessing sometimes scores positive.
RLHF amplifies this by rewarding confident-sounding output regardless of
accuracy (ICML 2025, ECE up to 0.30 on knowledge-intensive tasks).

---

## The Gate — 3-Phase Pipeline

### Phase 1: CLAIM ENUMERATION (pre-output)

Before any synthesis reaches the human, enumerate every factual claim.

```
For each sentence in draft output:
  IF sentence contains a factual assertion (date, number, existence,
     attribution, comparison, causal claim):
    → Extract as atomic claim
    → Classify source
  IF sentence is pure reasoning/inference with no factual assertion:
    → Mark as INFERRED, no source required
```

### Phase 2: SOURCE CLASSIFICATION

Every extracted claim gets exactly one label:

| Label | Definition | Can be premise? | Action |
|-------|-----------|-----------------|--------|
| **PROBED** | Verified via live tool call in THIS session | YES | Include with evidence |
| **CITED** | From primary source (paper, official doc, API response) | YES | Include with citation |
| **HEARSAY** | From secondary source (news article, Reddit post, blog) | **NO** | Include ONLY as "X reports that..." — never as established fact |
| **MEMORY** | From stored memory/honcho | CONDITIONAL | If > 7 days old → re-probe or label stale. If < 7 days → include with timestamp |
| **INFERRED** | Agent's own reasoning from other claims | CONDITIONAL | Only valid if ALL premises are PROBED or CITED. If any premise is HEARSAY → inference is also HEARSAY |
| **UNKNOWN** | Cannot determine truth value | **NO** | Must abstain: "tak pasti" / "tak verified" |

### Phase 3: OUTPUT FILTER

Apply these rules BEFORE the synthesis reaches the human:

1. **HEARSAY-as-premise block:** If a conclusion depends on a HEARSAY claim
   as premise, the conclusion itself is downgraded to HEARSAY. Rewrite:
   - ❌ "Voxtral beats ElevenLabs" (HEARSAY premise → presented as fact)
   - ✅ "Mistral claims Voxtral outperforms ElevenLabs Flash v2.5 in
     their own tests. Independent verification not found."

2. **Stale memory re-probe:** If a MEMORY claim is > 7 days old AND the
   claim is consequential (affects decisions, recommendations, or
   characterizations of people/systems):
   - Re-probe with live tool call if possible
   - If re-probe fails → label: "status unknown, last confirmed [date]"

3. **Inference chain validation:** If claim A (HEARSAY) → inference B →
   inference C, then C is also HEARSAY. Inference chains cannot upgrade
   source quality. A chain is only as strong as its weakest premise.

4. **Abstention default:** When a claim cannot be classified as PROBED or
   CITED, the default output is NOT confident narrative. It is:
   - "Aku tak verify ni, tapi [source] reports..."
   - "Status tak pasti — last check [date]"
   - "Tak ada primary source untuk ni"

5. **Confidence ceiling on hearsay:** Maximum confidence for any claim
   sourced from HEARSAY = 0.7. Never present as "confirmed."

---

## SelfCheckGPT Pattern (Black-Box Verification)

For high-stakes synthesis (consequential decisions, people, money,
reputation), apply SelfCheckGPT post-verification:

```
1. Generate draft synthesis
2. For each atomic claim in draft:
   a. Reformulate as a yes/no question
   b. Sample the same model 3× with the question (temperature 0.7)
   c. If ≥2/3 samples disagree with the draft claim:
      → Tag claim as [UNVERIFIED-CONFLICT]
      → Rewrite as "tak pasti" or remove
3. Output only claims that survive sampling
```

**When to apply:** Not every output. Only when:
- Synthesis involves claims about people, organizations, or events
- Output will influence decisions (money, reputation, health)
- Claims span multiple sources with different reliability levels
- "Exploration mode" where agent is browsing unfamiliar domains

**When to skip:** Routine operational output, single-source factual
retrieval, internal logging.

---

## Sufficient Context Gate

Before generating synthesis, check if evidence package is adequate:

```
1. List all questions the synthesis must answer
2. For each question, check: do I have PROBED or CITED evidence?
3. If evidence coverage < 70% of required claims:
   → STOP. Do not synthesize.
   → Report: "Evidence insufficient for reliable synthesis.
     Missing: [list gaps]. Options: [re-probe / ask human / abstain]"
4. If coverage 70-90%:
   → Synthesize with explicit gaps marked
5. If coverage > 90%:
   → Proceed normally
```

---

## Integration Points

- **arif_think:** Apply Phase 1 (claim enumeration) + Phase 2 (classification)
- **arif_judge:** Apply Phase 3 (output filter) + Sufficient Context gate
- **arif_seal:** Claims that survive gate get sealed with source classification
- **Musyawarah:** Add "hallucination detection" as explicit role in deliberation
- **Falsification Engine:** HEARSAY-as-premise triggers FALSIFICATION_MEDIUM

---

## Scar Anchors

| Date | Incident | Lesson |
|------|----------|--------|
| 2026-08-26 | Reddit exploration: 65% claims were HEARSAY presented as fact | Gate required before synthesis output |
| 2026-08-26 | "MiniMax quota habis" from stale memory asserted as current | Memory > 7 days = re-probe required |
| 2026-08-26 | Meta-hallucination: diagnosis of hallucination contained unverified claims | Gate must apply to ALL outputs including self-analysis |

---

## What This Does NOT Do

- Does NOT require model internals (token probabilities, hidden states)
- Does NOT require fine-tuning
- Does NOT guarantee zero hallucination (no method does)
- Does NOT slow down routine operational output
- DOES add latency to synthesis/research outputs (acceptable trade-off)

---

## References (verified primary sources)

- Kalai et al., "Why Language Models Hallucinate," OpenAI, arXiv:2509.04664
- Farquhar et al., "Detecting hallucinations using semantic entropy," Nature 2024
- "I-CALM: Incentivizing Confidence-Aware Abstention," arXiv:2604.03904
- "ReDAct: Uncertainty-Aware Deferral for LLM Agents," arXiv:2604.07036
- Wang et al., "Restoring Calibration for Aligned LLMs," ICML 2025
- "The Dunning-Kruger Effect in LLMs," arXiv:2603.09985
- Arthur AI, "Agent Guardrails: Pre-LLM & Post-LLM Best Practices," Apr 2026
- Zep, "How to Reduce LLM Hallucinations," Jun 2026 (AA-Omniscience data)
