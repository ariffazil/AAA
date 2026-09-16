# World Models Landscape (verified 2026-08-21)

Verified knowledge bank on Large World Models (LWM) / world foundation models — the "simulator dunia dalam kepala" class of AI. Sources fetched directly via Jina Reader (arxiv, DeepMind, OpenAI, NVIDIA) during SearXNG garbage-results outage. Load for any world-model, physical AI, video-generation-as-simulation, or embodied-agent research question.

## Lineage (oldest → newest)

1. **Ha & Schmidhuber "World Models" (arXiv:1803.10122, 2018)** — the origin paper. V (vision/compression) + M (memory/RNN) + C (controller). Agent trained entirely inside its own hallucinated dream, policy transferred back to real environment. Everything after this is scaling that idea.

2. **Sora / OpenAI (2024)** — thesis: "scaling video generation models is a promising path towards building general purpose simulators of the physical world." Diffusion transformer on spacetime patches (LLM tokens → visual patches analogy). Not action-controllable — pure generation.

3. **Genie 2 / Genie 3 (DeepMind, Dec 2024 / 2025)** — "large-scale foundation world model." Single prompt image → endless action-controllable, playable 3D environments (keyboard + mouse). Trained on large-scale video. Emergent capabilities at scale: object interactions, character animation, physics, modeling other agents' behavior. Purpose: limitless training curriculum for embodied agents (SIMA 2 plays in these worlds).

4. **NVIDIA Cosmos (arXiv:2501.03575, Jan 2025)** — open-source World Foundation Model Platform for Physical AI. Positioning: "Physical AI needs to be trained digitally first. It needs a digital twin of itself, the policy model, and a digital twin of the world, the world model." Platform = video curation pipeline + pre-trained WFM + post-training examples + video tokenizers. Open-weight, permissive license (github.com/NVIDIA/cosmos-predict1). Designed for fine-tuning into domain-specific world models (autonomous driving CosmosAlign, 4D-WAM etc. build on it).

5. **Meta V-JEPA (LeCun)** — the non-generative counterpoint. Joint Embedding Predictive Architecture: predict the *representation* of future states, not pixels. LeCun's objective-driven AI argument: generative decoding wastes compute on unpredictable detail; abstract representation capture is what matters for planning.

6. **2025-2026 follow-ons (arxiv, verified Aug 2026):** PIWM (arXiv:2509.12437 — lightweight physics-informed BEV world models; 400M param class, the size-vs-physics tradeoff for edge deployment), TD-MPC-Opt (arXiv:2507.01823 — distilling 317M multi-task world models into deployable sizes), 4D-WAM (arXiv:2608.10107 — 4D-consistent world+action models for driving, using geometric foundation models for training-time supervision), CosmosAlign (arXiv:2608.07693 — adapting Cosmos for traffic video forecasting).

## Two Schools (the architectural fork)

| | Generative (OpenAI, NVIDIA, DeepMind) | Latent-predictive (LeCun/Meta JEPA) |
|---|---|---|
| Predicts | pixels/patches/tokens | abstract representations |
| Strength | rich, usable output (video, playable worlds) | compute-efficient, immune to unpredictable detail |
| Weakness | compute-heavy, physical accuracy statistical not exact | no directly usable output — needs decoders for rendering |

## Defining properties of the class

1. **Visual tokenization** — patches (Sora) / video tokens (Cosmos) as the unifying representation
2. **Self-supervised training on internet-scale video** — predict next state, no labels
3. **Action-controllability** — the divider between video generator and world model (Genie line)
4. **Emergent physics** — gravity/collision/lighting appear from scale, but STATISTICAL (training data has many falling objects) not exact (model doesn't know F=ma). Honest gap: no LWM is physics-accurate for engineering simulation (reservoir flow, structural analysis) — generative realism ≠ physical correctness.

## Key URLs (Jina-Reader verified)

- https://arxiv.org/abs/1803.10122 (Ha & Schmidhuber)
- https://openai.com/index/video-generation-models-as-world-simulators/ (Sora technical report)
- https://deepmind.google/discover/blog/genie-2-a-large-scale-foundation-world-model/
- https://deepmind.google/models/genie/ (Genie 3 — listed under "World models & physical AI" alongside Gemini Robotics)
- https://arxiv.org/abs/2501.03575 (Cosmos) + github.com/NVIDIA/cosmos-predict1 (open weights)
- arxiv search pattern for the field: `arxiv.org/search/?query=%22world+model%22+video+generative+foundation&searchtype=all` → 126 results as of 2026-08, newest first gives the current frontier

## Relevance mapping (Arif/I-ARIF context)

- Cosmos is the open-source entry point — fine-tunable for domain world models if I-ARIF ever needs physical/spatial understanding
- Sora's scaling thesis matters strategically: world simulation emerges from scale, not from explicit physics encoding
- The physics-accuracy gap is the honest limiter — LWMs are for agent training environments and generation, NOT replacing numerical simulation (GEOX territory stays safe)
