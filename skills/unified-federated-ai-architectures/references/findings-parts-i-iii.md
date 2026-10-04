# Research Findings — Parts I-III

> Compiled by SCOUT subagent (Reconnaissance) on 2026-08-12. Focus: Conceptual taxonomy, information theory/ensemble diversity, and epistemology/self-verification.

## Part I — Conceptual Taxonomy

*   **Claim:** The "federated" concept in ML is not monolithic.
*   **Evidence:** It decomposes into at least four distinct senses:
    *   **Mixture of Experts (MoE) routing:** e.g., Switch Transformer (Fedus et al., 2022).
    *   **Weight arithmetic:** e.g., Model Soups (Wortsman et al., 2022), Task Arithmetic (Ilharco et al., 2022).
    *   **Instance debate:** e.g., Multi-Agent Debate (Du et al., 2023), Self-Consistency (Wang et al., 2022).
    *   **Role orchestration:** e.g., MetaGPT (Hong et al., 2023), AutoGen (Wu et al., 2023).
*   **Implication:** The user's initial dichotomy ("Unified" vs. "Federated") *conflates* these distinct architectures. Any rigorous analysis must specify which sense of "federated" is meant.

## Part II — Information Theory / Ensemble Diversity

*   **Claim:** Ensemble benefit = variance reduction, NOT bias reduction.
*   **Source:** Krogh & Vedelsby (1995) — foundational work on ensemble learning theory.
*   **Claim:** No single diversity measure universally predicts accuracy.
*   **Source:** Kuncheva & Whitaker (2003) — survey on diversity measures in ensembles.
*   **Claim:** Diversity is necessary but not sufficient; federation of *identically-biased* models remains biased.
*   **Source:** Geman et al. (1992) — bias-variance decomposition in neural networks.
*   **Implication:** The "wisdom of the crowd" hypothesis is conditional. Correlation between ensemble members erodes the benefit. Naively federating multiple instances of the same model architecture trained on the same data yields little to no improvement.

## Part III — Epistemology / Self-Verification

*   **Claim:** LLM self-verification is empirically bounded.
*   **Evidence:**
    *   *TruthfulQA* (Lin et al., 2021): Scaling alone does not improve truthfulness; larger models can be *less* truthful.
    *   *CRITIC* (Gou et al., 2024): Self-correction requires *external tools* (e.g., internet search, calculators) to be effective.
    *   *Self-Refine* (Madaan et al., 2023): Iterative self-refinement shows mixed results; improvements are often marginal and domain-specific.
    *   *Latent Knowledge* (Burns et al., 2022): Models can internally represent that an answer is wrong while still outputting the wrong answer. Self-introspection is not reliably aligned with output.
*   **Claim:** Gödel's incompleteness theorem's domain is formal arithmetic.
*   **Source:** Gödel (1931).
*   **Implication:** Gödel's theorem does *not* apply directly to LLMs. The relevant epistemic constraint for LLMs is *information-theoretic* — the correlated self-observation problem (a model cannot fully escape its training distribution and prior to verify itself).
*   **Related Work:** Constitutional AI (Bai et al., 2022) and Weak-to-Strong Generalization (Burns et al., 2023) explore forms of verification, but both rely on *external* anchoring (human-written principles, stronger model supervision), not pure self-verification.

## Confidence & Limitations

*   **Overall Confidence:** 0.80 (Part I-III combined).
*   **Limitations Encountered:**
    *   Tavily search/extract APIs were completely unavailable (HTTP 432).
    *   Semantic Scholar rate-limited (HTTP 429).
    *   Two arXiv IDs cited in secondary literature were permanently reassigned; primary citations verified via venue records instead.
*   **Falsification:** The claims above would be falsified by:
    *   A single universally predictive diversity measure (falsifies Kuncheva & Whitaker).
    *   A formal proof of self-correction convergence in LLMs (falsifies CRITIC/Latent Knowledge).
    *   Empirical evidence that scale monotonically improves truthfulness across all domains (falsifies TruthfulQA).

---

*Forged: 2026-08-12 by Hermes ASI under F13 SOVEREIGN directive for continuous learning.*
*DITEMPA BUKAN DIBERI — Forge evidence, not just opinion.*
