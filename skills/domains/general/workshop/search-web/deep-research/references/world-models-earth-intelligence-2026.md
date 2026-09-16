# World Models & Earth Intelligence Landscape (verified 2026-08-21)

Verified knowledge bank from the LWM deep research session (2026-08-21) + GEOX/LEM strategy synthesis with Arif. Load for any "world model", "earth model", "foundation model for geoscience/seismic", or GEOX/LEM positioning question.

## Large World Models — three branches (OBS, arXiv-verified)

1. **Video generation as world simulation** — Sora (OpenAI), Veo3, NVIDIA Cosmos, Wan/HunyuanVideo. Survey "Sora as a World Model?" (arXiv:2403.05131, 250+ studies): text-to-video is adept at world modeling but lacks action grounding — not yet true world models.
2. **Interactive world models** — Genie 1 (arXiv:2402.15391, 11B, unsupervised from internet video, latent action model) → Genie 2 (3D env generation) → Genie 3 (2026, DeepMind frontier, "generate and explore interactive worlds"). Also UniSim.
3. **RL world models (learned simulators)** — PlaNet, Dreamer family (Hafner), MuZero, TD-MPC. Train agents in imagination, deploy to reality.

**JEPA paradigm (LeCun's bet):** predict in latent space, not pixels. V-JEPA. Counterpoint: arXiv:2407.10311 — video AIs have not learned a complete real-world model. 2026 surveys: arXiv:2606.00133 (comprehensive taxonomy: architecture/methodology/reasoning/applications), arXiv:2606.20781 (World Action Models). Persistent challenges: compounding prediction errors, sim-to-real transfer, fragmented evaluation.

## Large Earth Models — atmosphere/surface only (OBS)

- NVIDIA **Earth-2** (weather/climate digital twin), Microsoft **Aurora** (atmospheric FM; latent-regime interpretability studies 2026), Google **WeatherNext**, Pangu-Weather, FourCastNet, ClimaX.
- EO vision FMs: **Clay**, **Prithvi** (NASA/IBM), SatMAE, **TESSERA v2** (arXiv:2607.03949, pixel-wise scaling), EO-VGGT (3D multi-view recon), LoRetta (dense matching).
- **Nobody does subsurface.** No "Aurora for geology" exists. Subsurface = blind spot of the entire Earth FM ecosystem.

## Seismic foundation models — the frontier just opened (OBS, 2026)

- **NCS-Model** (arXiv:2603.23211): seismic FM pretrained on Norwegian Continental Shelf public seismic cubes (DISKOS), open weights. Proof the architecture works — but Norway-only data (disclosure is mandated there; Malaysia/PETRONAS regime is proprietary).
- SAM domain-guided prompting for seismic interpretation (arXiv:2606.15786), SeisDiff-intp (prompt-guided flow matching, arXiv:2604.12209), salt-dome federated segmentation.

## GEOX/LEM positioning (DER/INT — Arif's three-arah frame + sharpenings)

**Arif's frame:** (1) petroleum geoscience invented model-based RL decades before DeepMind — basin modelling/reservoir simulation, each exploratory well = training episode; imagination is cheap, reality expensive → imagination must carry uncertainty envelopes. (2) NVIDIA bets on Physical AI; nobody owns "governed world model for the subsurface"; trust problem (hallucination → $100M dry hole) is the exact F1-F13 use case; LEM is the only earth model in a constitutional governance loop = moat. (3) Upgrade path: now (loop + claim engine + AC) → mid (JEPA-style learned predictor over latent contrasts, physics as low-frequency prior) → end (Genie-3-class interactive basin world model, governed, every scenario carries provenance + P10/P50/P90).

**Sharpenings added (session-proven):**
- **Deterministic drift scar**: 40 years of basin modelling already paid the tuition generative WMs are about to pay — the P50 zombie. One beautiful generated subsurface scenario = beautiful lie; that's why simulators emit 50-100 realizations.
- **Feedback asymmetry is why governance matters here**: robots get reality-correction in milliseconds; subsurface gets it once per $100M with month-year lag. Governance is load-bearing precisely where correction is slow and expensive.
- **Physics-as-prior mechanism = delta-learning**: physics model carries the load, learned predictor learns the residual between physics prediction and well observation. Maps to epistemic layering: physics=DER, learned residual=INT, extrapolation=SPEC. JEPA predictor lives in DER-residual space, not raw seismic.
- **Training data answer**: physics simulators generate synthetic episodes (basin rollouts); real wells are the held-out validation set. Dreamer pattern: train in imagination, validate on reality.
- **Data honesty**: no internet-scale subsurface data exists (proprietary, locked). Realistic path = public-data pretraining + sovereign fine-tuning on national data trust. "We won't out-scale NVIDIA; we out-govern them."
- **Interactivity for subsurface ≠ video exploration**: it's **counterfactual drilling** — "drill here, what's the outcome distribution?" Output unit is a governed claim with provenance feeding WEALTH, not video.
- **Governance loop = data flywheel** (Arif's collapse): governed loop → corpus of provenance-carrying claims → better predictor → more decisions → bigger corpus. Trust generates data; competitors have data but no trust. Moat lives only if the loop runs on LIVE decisions — governance without live cases = documentation, not moat.
- **Perception → commodity; conscience → never** (Arif's axiom): seismic encoders will be downloadable like DINO; physics is textbook-open. The un-commoditizable asset = an institution that can swear on an uncertainty envelope and be audited — with consequence when the envelope breaks (888_HOLD delay is the cost that makes approval meaningful). Conscience > eyes. In this domain conscience is the only organ that can grow.

## Cross-references
- Research tool outage this session: see `references/research-tool-fallback-ladder.md` rungs 9b/10 (arXiv Atom API carried the whole synthesis).
- GEOX operational grounding: `geox-production-cockpit`, `geological-artifact-rigor`.
