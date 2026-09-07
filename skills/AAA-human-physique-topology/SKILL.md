---
name: AAA-human-physique-topology
id: AAA-human-physique-topology
risk_tier: low
description: "Operational doctrine and computational architecture for mapping human physique topography and anatomical topology for image generation. Eliminates anatomical hallucinations and bridges the dimensionality deficit via the 5-layer topography hierarchy (Osteological Rigging, Musculoskeletal Contours, Adipose/Vascularity, DensePose UV Surface Manifold, Photometric/Normal Micro-relief). Enforces multi-modal ControlNet conditioning, prompt densification, and closed-loop VLM tri-witness quality gating across HERMES, FED, and AAA."
version: 1.0.0
tags:
  - vision
  - physique-topography
  - human-topology
  - image-generation
  - anatomy
  - densepose
  - controlnet
  - prompt-densification
  - F2-truth
  - F9-anti-hantu
floor_scope:
  - F01
  - F02
  - F04
  - F07
  - F09
  - F11
  - F13
owner: AAA
autonomy_tier: T1
capability_tier: fed-vision-topography
forged: 2026-09-07
forged_by: 333-AGI on F13 directive
constitutional_floor: F2 TRUTH + F9 ANTI-HANTU + F13 SOVEREIGN
f13_directive: "AI agents must not generate human physique images from naive fuzzy adjectives. Human physique topography must be anchored in falsifiable biomechanical strata, continuous surface topology, and optical normal physics."
---

# AAA-human-physique-topology

## 1. Purpose & The Anatomical Dimensionality Deficit

When an AI agent or human operator requests an image of a human physique (e.g. "muscular athletic man in a gym", "shredded fitness model"), naive text-to-image (T2I) generation suffers from a catastrophic **Dimensionality Deficit**.

A 20-word text prompt provides fewer than 100 bits of anatomical constraint. Yet a $1024 \times 1024$ image contains **1,048,576 pixels**, each requiring precise RGB values that must simultaneously satisfy:
1. Rigid skeletal biomechanics and degrees of freedom (DOF).
2. True muscular origins, insertions, and kinetic tensions.
3. Subcutaneous adipose layer variation and vascular paths.
4. Continuous 2D surface skin topology without sliding or shearing.
5. Volumetric light scattering (SSS) and surface normal shading.

Without structural topography mapping, diffusion models hallucinate:
- **Anatomical drift:** Floating muscles (serratus anterior detached from ribs, latissimus inserting in void), impossible 8-packs with uneven linea transversae, melted hands, dislocated clavicles.
- **Mannequin plastic sheen:** Uncanny artificial airbrushing that strips away natural pores, Langer's tension lines, and micro-relief.
- **Lighting inversion:** Convex muscle bellies shaded as concave hollows due to naive ambient light assumptions.

**The Golden Law of Physique Topography:**
> **Topography is not an aesthetic adjective. It is a multi-stratum physical coordinate system.** An AI agent must compile human physique requests into stratified structural coordinates before dispatching to diffusion models.

---

## 2. The 5-Stratum Topography Model

An AI agent mapping human physique must reason across five distinct strata:

```
┌──────────────────────────────────────────────────────────────┐
│ Stratum 4: Photometric & Optical Micro-Topography            │
│ (Raking cross-light 45°, SSS subsurface scattering, pores)   │
├──────────────────────────────────────────────────────────────┤
│ Stratum 3: Dense Surface UV Topology (DensePose / SMPL-X)    │
│ (24-patch geodesic manifold, continuous skin coordinates)     │
├──────────────────────────────────────────────────────────────┤
│ Stratum 2: Subcutaneous Adipose & Vascularity (Somatotype)   │
│ (Heath-Carter triad, %BF, skinfold thickness, vein highways) │
├──────────────────────────────────────────────────────────────┤
│ Stratum 1: Musculoskeletal Contours & Kinetic Tension        │
│ (Origins, insertions, bellies, sulci, isometric flex states) │
├──────────────────────────────────────────────────────────────┤
│ Stratum 0: Osteological Rigging & Anthropometric Canon       │
│ (25-joint scaffold, 8-head canon, Adonis shoulder-waist V)   │
└──────────────────────────────────────────────────────────────┘
```

### Stratum 0: Osteological Rigging & Anthropometry
- **Proportional Canon:** Enforces the classical 8.0-head athletic canon (or 7.5-head natural canon).
- **Golden V-Taper:** Biacromial shoulder width to bi-iliac waist width ratio $\approx 1.618$.
- **Joint Bounds:** Enforces biomechanical angle limits at clavicular, glenohumeral, elbow, hip, knee, and ankle pivots.

### Stratum 1: Musculoskeletal Topography
- **Torso Anterior:** Pectoralis major (distinct clavicular shelf vs sternal head), Linea Alba central furrow, Linea Transversae (3 distinct abdominal rows), External Obliques, and Serratus Anterior (interdigitating with ribs 5–8).
- **Torso Posterior:** Latissimus dorsi (flared cobra-spread), Trapezius diamond, Rhomboid-Infraspinatus valleys, Erector spinae furrow.
- **Extremities:** Deltoid triad (anterior, lateral, posterior heads), Biceps brachii with bicipital aponeurosis, Triceps horseshoe, Quadriceps sweep with Vastus Medialis teardrop above patella, Gastrocnemius diamond split.
- **Kinetic Tension:** Specifies whether muscles are in **isometric peak flex**, **eccentric load**, or **anatomical relaxation**.

### Stratum 2: Subcutaneous Adipose & Vascularity
- **Heath-Carter Somatotype:** Endomorphy (adiposity), Mesomorphy (musculoskeletal robustness), Ectomorphy (linearity/slenderness).
- **Body Fat Percentage (%BF):**
  - `<9%`: Competition shredded, deep striations, minimal subcutaneous water, prominent vascularity.
  - `9–12%`: Athletic definition, clear 6-pack quadrants, visible serratus, distinct forearm/bicep veins.
  - `13–16%`: Athletic fitness, smooth muscle borders, lower belly definition soft.
  - `>17%`: Solid bulk, smooth subcutaneous layer covering striations.
- **Venous Mapping:** Traces cephalic and basilic veins on upper limbs, superficial epigastric veins on lower abdomen.

### Stratum 3: Dense Surface UV Topology
- **DensePose 24-Patch Manifold:** Maps the human body surface to 24 continuous UV patches.
- Guarantees that skin textures, muscle striations, hair, and clothing maintain continuous geodesic coordinates without stretching, seam tearing, or hallucinated extra limbs.

### Stratum 4: Photometric & Surface Normal Relief
- **Raking Cross-Light (35°–50°):** Casts micro-shadows into intermuscular sulci, creating three-dimensional tactile depth.
- **Subsurface Scattering (SSS):** Simulates epidermal light absorption (red-wavelength penetration at shadow terminators) to eliminate wax/plastic artifacts.
- **Micro-Dermal Relief:** Anisotropic pores, natural tension lines, and satin hydration sheen (perspiration).

---

## 3. Operational Pipeline for AI Agents

When an AI agent (in Hermes, FED, or AAA) receives a human physique image generation request, it follows this 4-step reflex arc:

```
[User Request] 
      ↓
(1) Intake & Topography Parameterization
      → Formulate Physique Topography Contract (JSON)
      ↓
(2) Multi-Modal Conditioning Synthesis
      → OpenPose (Skeleton) + DensePose (UV) + Depth/Normal (Volumetric Relief)
      ↓
(3) Prompt Densification
      → Compile Anatomical Directives + Negative Constraints via compile_physique_prompt.py
      ↓
(4) Multi-Adapter Generation & VLM Quality Gate
      → Dispatch via MiniMax / SDXL / FLUX
      → Post-generation audit against 4 atomic checks
```

### Step 1: Parameterize into Scene Contract
The agent maps user intent into a formal contract using `schemas/physique_topography.schema.json`.

### Step 2: Multi-Modal Conditioning Manifest
For models supporting ControlNet/T2I-Adapters (e.g. FLUX ControlNet, SDXL), the agent generates the multi-control stack:
- **DWPose / OpenPose:** Weight 1.0 (Pose scaffold)
- **DensePose IUV:** Weight 0.85 (Surface skin manifold)
- **ZoeDepth / Marigold Depth:** Weight 0.75 (Volumetric relief)
- **DSINE / NormalBae:** Weight 0.80 (Surface normals for lighting)

### Step 3: Prompt Densification
For API-based diffusion models (such as MiniMax `image-01`, Qwen Token Plan Image, or DALL-E) that accept text only without direct ControlNet tensors, **the agent relies on prompt densification**:
- It runs `recipes/compile_physique_prompt.py`.
- It injects explicit anatomical nouns, skeletal proportions, raking lighting angles, and optical SSS descriptors.
- It applies the negative anatomical ensemble to structurally block mannequin airbrushing and anatomical glitches.

### Step 4: Closed-Loop VLM Quality Gating
The generated candidate is audited against 4 atomic gates:
1. `ANATOMY_SKELETAL_INTEGRITY` (Pass/Fail)
2. `ANATOMY_MUSCLE_ORIGIN_INSERTION` (Pass/Fail)
3. `SURFACE_TOPOGRAPHY_CONTINUITY` (Pass/Fail)
4. `OPTICAL_LIGHTING_CONGRUENCE` (Pass/Fail)

If any gate fails, the agent flags `ANATOMY_FAIL` and triggers an automated re-densification or returns honest disclosure under F4 CLARITY.

---

## 4. Federation Integration (HERMES, FED, AAA)

| Node | Role in Physique Topography |
|---|---|
| **HERMES** (`~/.hermes/skills/`) | Gateway interface: Parses human chat intent, applies `AAA-human-physique-topology`, compiles dense prompts for MiniMax `image-01` and downstream actuators. |
| **FED / VISION_ORGAN** (`/root/arifOS/VISION_ORGAN/`) | Perception & evaluation organ: Houses `physique-topography.schema.json`, `compile_contract.py`, and validates candidate images via Qwen vision quality gates. |
| **AAA** (`/root/AAA/skills/`) | Canonical knowledge base & governance: Holds the master skill, landmark references, and binds with `forge-vision-densify` to prevent high-$\Delta S$ ungrounded image dispatch. |

---

## 5. Verification & Testing

To verify the pipeline:
```bash
python3 /root/AAA/skills/AAA-human-physique-topology/recipes/compile_physique_prompt.py
```
Expected output:
- Fully densified anatomical prompt exceeding 0.75 prompt density score.
- Standard negative anatomical token ensemble.
- 4-unit ControlNet conditioning manifest.

---

## 6. Sealing Note

> **DITEMPA BUKAN DIBERI — Human Physique Topography Architecture**
>
> Ratified 2026-09-07 under F13 Sovereign Directive.
> Eliminates subjective AI body distortion by grounding image synthesis in biomechanical osteology, myological contouring, DensePose UV manifolds, and optical surface normal physics.
