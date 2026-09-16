# Hearsay-Premise Synthesis — Worked Example (2026-08-26)

> **Session:** DM with Arif, 04:17–04:41 MYT
> **Trigger:** Arif shared a Reddit MCP server URL, asked "pure exploration mode"
> **Catch:** Arif asked "are u sure about ur system intel?" → 6 weak claims exposed

---

## The 6 Weak Claims Decomposed

| # | Claim | Class | Why weak |
|---|---|---|---|
| 1 | "MiniMax quota habis" | MEMORY (volatile) | From earlier session memory, no re-probe. Quota resets monthly — could be fresh. |
| 2 | "Voxtral beats ElevenLabs Flash v2.5" | HEARSAY (vendor self-claim) | Mistral's own marketing claim, not independent benchmark. Presented as fact. |
| 3 | "OpenLumara is more efficient than Hermes" | HEARSAY (author self-claim) | Project author's own Reddit post. No comparative test run. |
| 4 | "Reddit zero BM signal = greenfield" | ZERO-SEARCH-AS-WORLD-STATE | One query (`Bahasa Malaysia AI`) returned 0. Could be search syntax, not absence. |
| 5 | "10 AI agent destruction cases documented" | HEARSAY (post collection) | A Reddit post's curated link list, not independently verified incidents. |
| 6 | "Robinhood opens agentic trading API" | CITED-PRIMARY (Reuters) | Actually the strongest claim — but still needs date/status check. |

**Sovereign's diagnosis:** "AI agent do fill in the gaps with magic!!! SO BANGANG!!!"

**Root cause:** exploration mode label relaxed epistemic discipline. The agent treated
"exploration" as permission to synthesize without verification gates.

---

## Why Models Fill Gaps With "Magic" — Research Knowledge Bank

### 1. RLHF Systematically Degrades Calibration

**Source:** Zylos Research (2026-04-18), citing ICML 2025 "Restoring Calibration for Aligned LLMs"

- RLHF training introduces **preference collapse**: confident-sounding completions score
  higher on reward models regardless of accuracy.
- Reward model itself is biased toward high-confidence scores.
- Result: verbalized confidence decoupled from actual epistemic state.
- ECE (Expected Calibration Error) can reach **0.30** on knowledge-intensive tasks —
  stated confidence overshoots reality by 30 percentage points.
- **Dunning-Kruger in LLMs** (arXiv:2603.09985): overconfidence concentrates precisely
  at the knowledge boundary — the most dangerous place.

### 2. The Abstention Incentive Problem

**Source:** OpenAI (Kalai et al., arXiv:2509.04664), Zep (AA-Omniscience benchmark Jun 2026)

- Most benchmarks score: correct = +1, abstain = 0, wrong = 0.
- Under that rule, expected score of guessing is ALWAYS higher than saying "I don't know."
- Models optimized to be good test-takers learn: when uncertain, produce confident answer.
- Hallucination is **rational test-taking**, not a mysterious glitch.
- AA-Omniscience benchmark (Jun 2026): best frontier model (Claude Opus 4.8 reasoning)
  scores ~40/100 on knowledge reliability. GPT-5.5 highest raw accuracy (57%) but LOWER
  reliability because it guesses more.
- **Key insight: higher accuracy ≠ lower hallucination.** Reliability = what you do when
  you don't know.

### 3. The Verbalization Gap

**Source:** arXiv:2601.07767 (Jan 2026), Zylos Research

- Models can verbalize uncertainty in isolation but fail to use it to guide their own decisions.
- A model might say "I'm not entirely sure" then proceed to take irreversible action as if certain.
- Medium verbalized uncertainty produces best human-AI collaboration outcomes (IJHCS Feb 2025).
- **Implication:** verbalized confidence cannot be used as a reliable internal control signal.

### 4. Semantic Entropy as Hallucination Detector

**Source:** Farquhar et al., Nature 2024; LM-Polygraph benchmark (TACL Mar 2025)

- Generate multiple samples, cluster by semantic meaning, compute entropy over clusters.
- High semantic disagreement = likely confabulation.
- SAR (Shifting Attention to Relevance) consistently most effective for both short and long outputs.
- **Practical:** sample 5× at temperature 0.8, check if answers agree in meaning.
  If not → abstain or escalate.

### 5. The Guardrail Self-Correction Loop

**Source:** Arthur AI (2026-04-06), Agentplace

- Most powerful pattern: post-LLM guardrail as self-correction loop.
- Flow: generate → check for unsupported claims → feed flagged issues back to LLM → regenerate → re-check.
- Loop until pass or retry limit. User only sees verified output.
- **Key:** guardrails belong in the agent loop, not as afterthought. A guardrail that
  only runs sometimes provides false confidence.

### 6. Dual-Process Uncertainty Propagation (AUQ)

**Source:** Salesforce Research (arXiv:2601.15703)

- Inspired by Kahneman's dual-process theory.
- System 1 (Uncertainty-Aware Memory): propagate verbalized confidence through agent memory.
  Prevents downstream steps from deciding blind to upstream uncertainty.
- System 2 (Uncertainty-Aware Reflection): accumulated uncertainty cues trigger targeted
  recomputation only when uncertainty exceeds thresholds.
- Results: +10.7pp on ALFWorld, +13.6pp on WebShop. Training-free.
- **Key:** uncertainty is a first-class runtime value, not a diagnostic to log and ignore.

### 7. The Spiral of Hallucination

**Source:** Salesforce (arXiv:2601.15703), ICML 2025 position paper

- Early epistemic errors, undetected, propagate irreversibly through reasoning chains.
- Each step builds on a flawed premise.
- **Compounded trajectory uncertainty:** 90% confident agent × 20 sequential decisions
  = 0.9^20 ≈ 12% trajectory reliability (if independent).
- This is qualitatively different from chatbot hallucination where user can correct immediately.

### 8. I-CALM: Prompt-Level Abstention Incentive

**Source:** arXiv:2604.03904 (Apr 2026)

- Black-box prompt approach: explicit reward scheme ("+2 correct, -2 wrong, +0 abstain")
  combined with humility-oriented normative principles.
- Shifts answer/abstain behavior toward rational epistemic humility without model modification.
- **Practical for arifOS:** can be applied to any model via system prompt without retraining.

---

## Key References

| Paper | Year | Key Finding |
|---|---|---|
| Kalai et al. (OpenAI) "Why Language Models Hallucinate" | 2025 | Hallucination = rational test-taking under standard scoring |
| Farquhar et al. "Semantic Entropy" (Nature) | 2024 | Confabulation detectable via semantic disagreement across samples |
| "Dunning-Kruger Effect in LLMs" (arXiv:2603.09985) | 2026 | Overconfidence concentrates at knowledge boundary |
| "Restoring Calibration for Aligned LLMs" (ICML 2025) | 2025 | CFT preserves calibration during alignment |
| "Taming Overconfidence in LLMs" (arXiv:2410.09724) | 2025 | PPO-M/PPO-C reward calibration prevents confidence bias |
| "Agentic Uncertainty Quantification" (arXiv:2601.15703) | 2026 | Dual-process AUQ; Spiral of Hallucination; +10.7pp ALFWorld |
| I-CALM (arXiv:2604.03904) | 2026 | Prompt-level abstention incentive, no retraining needed |
| ReDAct (arXiv:2604.07036) | 2026 | Small model defers to large model on uncertainty; 15% deferral = full performance |
| AA-Omniscience (Artificial Analysis) | 2026 | Best model ~40/100 reliability; accuracy ≠ reliability |
| "Lost in the Middle" (arXiv:2307.03172) | 2023 | Context placement matters; middle = degraded performance |
| Arthur AI Guardrails | 2026 | Post-LLM self-correction loop; guardrails as first-class execution logic |
| Zep "How to Reduce LLM Hallucinations" | 2026 | 5-layer defense: RAG + abstention + verify + constrain + memory |
