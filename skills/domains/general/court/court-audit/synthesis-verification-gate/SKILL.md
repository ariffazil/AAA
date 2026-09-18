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
| **CONTESTED** | Two named parties of standing contradict each other on the same status; a third body (registrar, court, commission) owns resolution | **NO** (until resolved) | Report both attributed claims, name the unresolved state, name the resolving owner. Never carry the louder claim as established fact |
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

6. **CONTESTED status may not be narrated as settled.** When two named officeholders or
   institutions of the same body contradict each other about a status change, the reportable
   finding is the disagreement plus who owns its resolution — not the claim that was stated
   loudest or latest. Collapsing it is a transition lie: `ANNOUNCED ≠ EFFECTIVE`, and
   `DISPUTED` is a state in its own right. Resolution is expected from a named owner, never
   inferred from who spoke last, from which wing is larger, or from what "will obviously"
   happen. Applies equally to institutions declaring their own compliance.

### Phase 2.5: INDEPENDENCE AND ORDER CHECKS (mechanical)

Two structural blindspots survive Phase 2 because both produce a *correct-looking* label set.

#### A · Source Independence Constraint (echo-chamber inflation)

Three URLs agreeing is not three witnesses. `CITED ×3` currently cannot distinguish three
independent origins from three reprints of one press release.

**Rule:** group every CITED claim's sources into **origin units** before counting weight.

| Same origin if… | Weight |
|---|---|
| all trace to one wire item (Bernama, Reuters, AFP), one press release, one speech, or one party statement | **W = 1** |
| independent outlets, each with its own reporting, same underlying event | W = number of outlets that did independent work |
| primary instrument plus any number of reports of it | W = 1 (the instrument), reports are transport |

- **A quote is one source however many times it is printed.** Restating a minister's line in five
  outlets is W = 1 attributable to *that minister*, never W = 5 for the proposition.
- **Data cannot be verified by its own echo.** If every source for a number routes back to one
  body's release, the number's status is *"self-reported by X"* — not "corroborated".
- Record the arithmetic: `SOURCES: 5 URLs → ORIGIN_UNITS: 1 (Bernama wire) → W = 1`.

#### B · Chronological Lock (temporal collapse)

Narrative order is not causal order, and prose arranged by theme silently re-dates events.

**Rule:** two events may be joined in a cause→effect sentence only if they carry absolute
timestamps and `t_A < t_B`. Where dates are ambiguous at day level, compare at month
resolution; where the order is genuinely unknown, the sentence becomes *"A and B (order
unestablished)"*.

- **Check the mechanism is even available at the earlier date.** An actor cannot have responded
  to a thing that had not yet happened. If the "response" predates the "trigger", the pairing is
  a narrative artefact — one of the two dates is wrong, or the two events are unrelated.
- **A policy stated in month M and reversed in month M+5 is a sequence of decisions, not a
  single "policy U-turn".** Collapsing them hides the reversal's trigger.
- Record it: `LOCK: A(YYYY-MM-DD) < B(YYYY-MM-DD) → ORDERED` or `→ UNESTABLISHED`.
- Narrow repo analogue: in codebase audit the same lock reads as commit/mtime ordering —
  `git log --format='%ct'` gives epoch order, and a "fix" whose hash predates the "bug" is not a fix.

**Both checks are mechanical and fail-closed on the draft:** an independence count that was not
computed, or an ordering that was not locked, is an edit — not a hedge.

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
