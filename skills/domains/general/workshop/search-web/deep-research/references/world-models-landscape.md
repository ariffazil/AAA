# World Models / Large World Model (LWM) Landscape — Verified Knowledge Bank

Verified sources from 2026-08-21 deep research session. All arXiv IDs confirmed via export API. Load for any world-model, LWM, video-generation-as-simulation, JEPA, or embodied-AI-simulator question.

## Core Definition

"LWM" is NOT one model — it's a class. A world model learns **environment dynamics**: given state + action → predict next state. Three branches exist, often conflated in media coverage.

## The Three Branches

### 1. Video Generation as World Simulation (pixel-space)
- **Sora** (OpenAI, 2024): text-to-video. Criticized: no action grounding, not interactive. Survey arXiv:2403.05131 ("Sora as a World Model?", 250+ studies, v3 Jan 2026) concludes: adept at world modeling but incomplete — diversity-consistency tradeoffs remain.
- **Veo 3** (Google DeepMind, 2025): video + native audio generation, cinematic.
- **Cosmos** (NVIDIA, Dec 2024): open-weight physical-world simulators for robotics/AV. "Physical AI" positioning.
- Key open question: do they model physics or just imitate pixel statistics?

### 2. Interactive World Models (action-controllable)
- **Genie 1** (DeepMind, arXiv:2402.15391, Feb 2024): 11B params. First generative interactive environment trained unsupervised from unlabelled internet video. Spatiotemporal tokenizer + autoregressive dynamics + latent action model. No ground-truth action labels needed.
- **Genie 2** (DeepMind, Dec 2024): generates 3D environments on-the-fly, explorable.
- **Genie 3** (DeepMind, 2026): current frontier — "A new frontier for world models" (deepmind.google/models/genie/). Try via Project Genie (labs.google/projectgenie). DeepMind nav categorizes under "World models & physical AI" alongside Gemini Robotics.
- **UniSim** (Google): universal action-conditioned video simulator.

### 3. RL World Models (learned latent simulators)
- **PlaNet → Dreamer family** (Hafner): latent-space imagination, SOTA sample efficiency. DreamerV3.
- **MuZero** (DeepMind): world model without knowing game rules (Go, chess, Atari).
- **DIAMOND** (arXiv:2405.12399, NeurIPS 2024 Spotlight): diffusion world model; Atari 100k mean human-normalized 1.46 — best fully-in-world-model agent; doubles as playable neural game engine (CS:GO).
- **TD-MPC-Opt** (arXiv:2507.01823): distills 317M world-model agent → 1M params for edge deployment.
- **Doe-1** (arXiv:2412.09627): closed-loop autonomous driving LWM.

## The JEPA Paradigm (LeCun's Bet)

Joint-Embedding Predictive Architecture: predict in **latent space**, not pixel space. Cheaper, more abstract, closer to cognitive science of human prediction.

Active 2026 research line (all verified):
- **UWM-JEPA** (arXiv:2605.25313): belief-space imagination for partially-observed environments.
- **Sub-JEPA** (arXiv:2605.09241): subspace Gaussian regularization for stability.
- **Contrastive inverse dynamics JEPA** (arXiv:2608.17542): anti-collapse without Gaussian assumptions.
- **JEPA generalization theory** (arXiv:2606.27014): first theoretical grounding.
- **Music-JEPA** (arXiv:2607.22000): world model of sound from action.
- **V-JEPA** (Meta): video JEPA, self-supervised, no reconstruction.

Philosophical counterpoint: arXiv:2407.10311 — "Sora and V-JEPA Have Not Learned The Complete Real World Model" (productive imagination theory).

## Key Surveys (entry points)

- **arXiv:2606.00133** (May 2026, 26 authors): THE comprehensive survey. Multi-axis taxonomy: architecture (state-space/recurrent, transformer, diffusion, physics-informed, language-augmented), reasoning (imagination planning, latent policy, counterfactual, uncertainty), applications (robotics, AV, video, RL, science, medical, finance). Traces PlaNet→Dreamer→MuZero→Sora→Cosmos→Genie. Names persistent challenges: compounding prediction error, sim-to-real transfer, fragmented evaluation.
- **arXiv:2606.20781** (Jun 2026): World Action Models (WAMs) survey — embodied predictive-action models; notes blurred boundary between world models and video generation.
- **arXiv:2605.00080** / **2606.00113** (2026): robot-learning and robotic-manipulation world model surveys.

## Frontier Papers (Aug 2026, week of session)

- arXiv:2608.19779: irreducible quantum advantage in aligning world models with reality.
- arXiv:2608.16829 (CaliBench): are video-world-model stochastic dynamics physically calibrated? (new eval axis)
- arXiv:2608.18234 (GigaBrain-WBC-0.5): behavior world model for humanoid whole-body control.
- arXiv:2608.15309: physiological world models — human state-transition prediction from wearables.
- arXiv:2608.17163: Q-learning with world models for VLA fine-tuning.
- arXiv:2608.19085 (DA-WAM): decision-aligned driving world models.

## Field-Wide Open Problems (from surveys, 2026)

1. **Compounding error** — long-horizon rollouts drift.
2. **Sim-to-real gap** — policies trained in imagination fail on hardware.
3. **Fragmented evaluation** — no unified benchmark (CaliBench is an early attempt).
4. **Diversity-consistency tradeoff** — stochastic futures vs coherent worlds.
5. **Memory/state persistence** — worlds forget; agents don't persist.

## Relevance Notes (arifOS mapping — INT, from session)

- JEPA's latent-prediction philosophy ≈ arifOS knowledge graphs as latent representations of reality — predict implications, not pixels.
- Action-conditioned world models ≈ decision simulators for F13 thinking space.
- Physiological world models (2608.15309) parallel WELL's body-state modeling.
