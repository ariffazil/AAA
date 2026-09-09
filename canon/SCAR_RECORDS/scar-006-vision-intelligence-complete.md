# SCAR-006: Vision Intelligence & Multimodal Operational Scar Compilation

**Date:** 2026-09-07  
**Status:** CANONICAL SELECTION & FEDERATION-WIDE RATIFIED  
**Owner:** AAA / HERMES / VISION_ORGAN  
**Floor Scope:** F01 (Amanah), F02 (Truth), F04 (Clarity), F09 (Anti-Hantu), F11 (Audit), F13 (Sovereign)  

---

## Executive Summary

Over multiple operational cycles (June – September 2026), the arifOS federation experienced critical multimodal failures across ingestion, routing, generation, and editing. These failures were not model deficiencies; they were **architectural leaks where ungrounded assumptions breached constitutional boundaries**.

This document compiles the **8 Canonical Vision Scars**, their empirical root causes, their falsifiable post-mortems, and the immutable laws that now bind **HERMES, FED, AAA, and all citizen harnesses**.

---

## The 8 Canonical Vision Scars

### 1. SCAR-VIS-001: The 413 Payload Collapse (Context Image Bloat)
* **Incident:** 2026-07-30 (ALPHA - ZEN group chat nasi lemak image blast).
* **Symptom:** Every fallback provider sequentially threw `HTTP 413 (Request Payload Too Large)`. The session crashed completely across 10+ models.
* **Root Cause:** In group chats with `protect_last_n: 20`, raw image payloads remained uncompressed in session context. When accumulated messages exceeded provider HTTP request limits (10–50MB), the gateway attempted fallback. Because the payload size was identical for every model, all fallbacks failed identically.
* **Immutable Law:**
  1. **Zero Raw Image Bytes in Reasoning Context:** Image processing terminates at the gateway via PRMT. Primary reasoning models must receive text transcripts only.
  2. **Aggressive Context Hygiene:** Set `threshold: 0.3`, `target_ratio: 0.10`, `protect_last_n: 10`, and `hygiene_hard_message_limit: 3000`.

---

### 2. SCAR-VIS-002: `model.supports_vision: true` Premature Poisoning
* **Incident:** 2026-07-30 / 2026-08-04.
* **Symptom:** Vision enrichment never triggered; cryptic "unknown variant `image_url`" errors or immediate 413 crashes on text models.
* **Root Cause:** Setting top-level `model.supports_vision: true` on text-only models (e.g. DeepSeek V4 Flash) short-circuited `_lookup_supports_vision`. The gateway assumed the model was vision-native and attached base64 image bytes to text-only API endpoints.
* **Immutable Law:**
  1. **Registry Claim $\ne$ Verified Reality:** `supports_vision: true` is an unverified assertion until tested with a live canary.
  2. **Hard Ban on Top-Level Overrides:** Top-level `model.supports_vision` on text models is banned. If a model is text-only, `image_input_mode` must be `text` (PRMT).

---

### 3. SCAR-VIS-003: Split Failure Domain & Auxiliary Billing Brick
* **Incident:** 2026-07-30 (OpenRouter $0 balance credit lock).
* **Symptom:** Chat worked fine, but all image queries crashed or dropped images silently.
* **Root Cause:** Chat used MuleRouter while auxiliary vision enrichment used OpenRouter. When OpenRouter hit $0 credit (HTTP 402), it marked the vision provider "unhealthy for 600s". Vision enrichment was skipped, raw image bytes slipped into the text primary model, and the agent bricked.
* **Immutable Law:**
  1. **Single Failure Domain:** Auxiliary vision and primary chat MUST share the same provider and key (`MULEROUTER_API_KEY` / KVM8 LiteLLM). If chat is alive, vision must be alive. No independent auxiliary billing collapse.

---

### 4. SCAR-VIS-004: Path B Model-Override Cascade (Dynamic Swapping Disaster)
* **Incident:** 2026-07-30.
* **Symptom:** Text-only fallback models crashed sequentially after an image turn failed.
* **Root Cause:** Dynamic model swapping (`_pending_vision_model_overrides`) tried to swap the primary model to a vision model (qwen-vl / minimax-m3) for image turns, then revert. When the vision model failed, image bytes remained in context, and subsequent text-only fallback models crashed.
* **Immutable Law:**
  1. **Permanent PRMT Architecture:** Never swap the primary model for an image. The gateway extracts a 4-part structured transcript (`SCENE`, `OCR`, `DATA`, `IDENTITY`) and passes pure text to the primary reasoner.

---

### 5. SCAR-VIS-005: `OPENAI_BASE_URL` & SOPS Ciphertext Poisoning
* **Incident:** 2026-07-30.
* **Symptom:** All vision tool calls crashed with `Invalid IPv6 URL`.
* **Root Cause:** Setting `OPENAI_BASE_URL` or passing encrypted SOPS variables into client configuration caused `urlparse` in `base_url_host_matches` to crash on unescaped ciphertext characters.
* **Immutable Law:**
  1. **5-R Secret Discipline:** Secrets must be decrypted before runtime consumption. Base URLs must be explicitly sanitized strings, never raw encrypted blobs.

---

### 6. SCAR-VIS-006: Identity Drift & "Dagu Hilang" (Loss of Anatomical Identity)
* **Incident:** 2026-08-12 (F13 directive: "Hang jangan ubah muka manusia").
* **Symptom:** Real photo edits warped faces, removed jawlines ("dagu hilang"), smoothed out skin pores, and altered body habitus. Multi-turn edits caused statistical averaging.
* **Root Cause:** Naive img2img and background cutouts (`rembg`) treated human bodies as statistical pixels rather than rigid anatomical and identity invariants.
* **Immutable Law:**
  1. **F13 Hard Rule:** "Hang jangan ubah muka manusia." Real photo edits MUST preserve face, body structure, and skin tone 100%.
  2. **The 6 Iron Rules of Nano-Banana / Gemini Editing:**
     - Part ordering: Image first, text second.
     - MIME type must match actual bytes.
     - Image size 1024–1568px on longest side.
     - Strip alpha channels (convert PNG to RGB).
     - Stateless iteration (never trust multi-turn chat history).
     - Strictly ONE change per turn; enforce `--semantic-mask`.

---

### 7. SCAR-VIS-007: Unverified Vision Capability in Composite Lanes
* **Incident:** 2026-06-09 (GEOX seismic vision / OpenClaw connector) & 2026-09-04.
* **Symptom:** Runtime `NotImplementedError` during live execution despite code appearing to exist.
* **Root Cause:** Running Python processes loaded stale bytecode; tool wrappers claimed vision support in registries without a live paired-fixture canary.
* **Immutable Law:**
  1. **Weakest Leg Rule:** A composite lane is only as live as its weakest verified leg.
  2. Every multimodal hop must have a paired-fixture canary. Without canary proof, state is marked `UNPROVEN`.

---

### 8. SCAR-VIS-008: The Dimensionality Deficit & Plastic Mannequin Hallucination
* **Incident:** 2026-08-27 (`forge-vision-densify`) & 2026-09-07.
* **Symptom:** AI-generated human physiques exhibited floating serratus anterior muscles, impossible 8-packs, dislocated clavicles, airbrushed plastic skin, and inverted lighting normals.
* **Root Cause:** The Dimensionality Deficit. A 20-word prompt provides <100 bits of constraint for 1,048,576 pixels. Diffusion models compulsively hallucinate the remaining 99% from unconstrained priors.
* **Immutable Law:**
  1. **5-Stratum Topography Grounding:** Prompts referencing human physique must be compiled via `AAA-human-physique-topology` across 5 physical strata:
     - Stratum 0: Osteology & Anthropometric Canon (8-head, Adonis V-taper 1.618:1).
     - Stratum 1: Musculoskeletal Contours & Kinetic Tension.
     - Stratum 2: Subcutaneous Adipose & Vascularity (Heath-Carter, %BF).
     - Stratum 3: DensePose UV Continuous Surface Manifold.
     - Stratum 4: Photometric & Optical Normal Relief (45° raking cross-light, SSS).
  2. **Hard Gate Interception:** Naive short prompts (<0.20 density) must be rejected before diffusion and forced through `compile_physique_prompt.py`.

---

### 9. SCAR-VIS-009: The Static Human Fallacy (Correct Anatomy, Lifeless Organism)
* **Incident:** 2026-09-07 (Somatic Intelligence Ratification under F13 Directive).
* **Symptom:** AI-generated human subjects exhibited mathematically correct proportions and surface textures, but appeared like dead mannequins, wax figures, or frozen statues. Center of gravity was ungrounded (balanced nowhere), breathing was absent (frozen ribcage), muscle contraction was uniform without kinetic load transfer, and emotional posture was biomechanically incoherent.
* **Root Cause:** The Static Human Fallacy. Modeling the body as pure geometry rather than an active, breathing organism. Just as geological structure alone does not describe a reservoir without pressure, fluid, and temperature dynamics ($Structure \ne State$), anatomy alone cannot describe a living human ($Skeleton \ne Human$).
* **Immutable Law:**
  1. **Stratum S (Somatic State Layer):** Orthogonal to Strata 0–4. Must define:
     - **Breathing State:** Full inspiration (costal expansion) vs. neutral tidal vs. forced expiration (abdominal vacuum).
     - **Weight Distribution & Center of Gravity:** Explicit load transfer (e.g. 60/40 unilateral drive, athletic stagger, grounded kinetics).
     - **Kinetic Tension:** Antagonist relaxation vs. agonist peak contraction (tendon tension, vascular turgor).
     - **Fatigue & Metabolic History:** Post-exertion flushing, sweat distribution, respiratory effort.
     - **Emotional Embodiment:** Thoracic elevation, neck/head alignment, shoulder depression/protraction.
  2. **The Reservoir Dynamics Invariant:** Topography answers *"What is this body?"*; Somatics answers *"What is this body doing?"* A render is invalid if it portrays a living human without somatic load coherence.

---

### 10. SCAR-VIS-010: Diffusion Prior Domination & The Operating Envelope (FI-008)
* **Incident:** 2026-09-07 (V1 Rejection & V2 Mandatory Disclosure under F13 Directive).
* **Symptom:** In human physique synthesis, text prompts declaring "natural lean 88kg athletic" still produced an oversized (>95kg) stage bodybuilder with residual spray-tan aesthetics.
* **Root Cause:** *"Prompt text kalah lawan diffusion prior."* Commercial diffusion models inherit a massive training prior where fitness imagery is dominated by contest bodybuilders. Adjectives cannot overcome a dataset prior; runtime inherits reality.
* **Immutable Law:**
  1. **Topological Anchoring Before Generation:** Realiti $\to$ Topografi $\to$ Render. Overcoming priors requires physical coordinate boundaries, not descriptive adjectives.
  2. **Negation Anchor Defense:** High-weight negative tokens must explicitly poison the prior (`non-stage, non-spray-tan, matte skin, no oil sheen, no competition tan, no bodybuilder stage lighting`).
  3. **Adherence Band Over Single Scalars (Rule 14):** Single scalar accuracy claims are banned. Every delivery must declare its empirical **Adherence Band** (e.g. `f2_adherence: [0.50, 0.60]`).
  4. **The V2 Invariant (Honesty Band):** `f2_adherence ~0.55` with full disclosure of flaws is a valid, honest delivery. Claiming `0.90` without disclosure is fraud. V2 stands as the first reference receipt of `rtc-loop`.

---

## Federation Routing & Invariant Matrix

| Modality / Action | Gateway Architecture | Conditioning / Prompting Layer | Verification Gate |
|---|---|---|---|
| **Incoming Image (Telegram/Chat)** | PRMT (Pre-Routing Modality Translation) | `qwen-vl-max` extracts 4-part transcript (`SCENE`, `OCR`, `DATA`, `IDENTITY`) | Primary reasoner sees text only; zero 413 risk |
| **Real Photo Edit (I2I)** | Nano-Banana / Gemini direct | 6 Iron Rules + `--semantic-mask` + identity preservation clause | F13 Hard Rule: Zero face/body drift; single change per turn |
| **Human Physique Generation (T2I)** | Hard Gate in `forge-vision-densify` | 5-Stratum Topography Compiler (`AAA-human-physique-topology`) | Closed-Loop VLM Quality Gate (`ANATOMY_FAIL`, `PROPORTION_FAIL`) |
| **SEAL-Grade Visuals (Charts/Maps)** | A-FORGE Actuators | Territory Komda Color Law (§04) | W³ Tri-Witness Consensus (W1 Vision, W2 DOM, W3 Sovereign) |
