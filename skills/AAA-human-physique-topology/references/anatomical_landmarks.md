# Canonical Anatomical & Physique Topography Reference

## 1. The 5-Stratum Topography Hierarchy

```
[Stratum 4: Photometric / Micro-relief]  ← SSS, specular highlights, micro-normals, pores, sweat sheen
[Stratum 3: Dense Surface UV Topology]   ← DensePose 24-patch coordinates, geodesic body continuity
[Stratum 2: Subcutaneous Adipose & Vasc] ← Somatotype, %BF, caliper pinch sites, venous highways
[Stratum 1: Musculoskeletal Contours]    ← Muscle origins, insertions, bellies, kinetic tension lines
[Stratum 0: Osteological Rigging]        ← Skeletal joints, proportional canon, biacromial/biiliac axes
```

---

## 2. Stratum 0: Osteological Landmarks & Anthropometry

### Proportional Canons
- **7.5 Heads (Natural Human Standard):**
  - Head 1: Cranium vertex to chin
  - Head 2: Chin to nipple line (4th intercostal space)
  - Head 3: Nipple line to navel (umbilicus)
  - Head 4: Navel to pubic symphysis / greater trochanter
  - Head 5: Pubic symphysis to mid-thigh
  - Head 6: Mid-thigh to bottom of patella
  - Head 7: Patella bottom to lower calf
  - Head 7.5: Lower calf to plantar foot base
- **8.0 Heads (Heroic / Athletic Standard):**
  - Used in classical sculpture and athletic physique modeling. Slightly elongated legs relative to torso.
  - Adonis Golden Ratio: $\frac{\text{Biacromial Shoulder Width}}{\text{Bi-iliac Waist Width}} \approx 1.618$.

### Key Skeletal Anchor Points (Keypoints)
1. **Acromion Process (R/L):** Outermost lateral boundary of the shoulder girdle.
2. **Suprasternal Notch:** Superior border of manubrium sterni, baseline for clavicles.
3. **Xiphoid Process:** Lower apex of sternum; junction of subcostal angle.
4. **Iliac Crest & ASIS (Anterior Superior Iliac Spine):** Bony pelvis landmarks anchoring obliques.
5. **Greater Trochanter:** Lateral femur pivot determining hip width and leg articulation.
6. **Patella (Kneecap):** Anterior knee junction anchoring quadriceps tendon and patellar ligament.
7. **Lateral & Medial Malleoli:** Ankle boundary points defining lower leg orientation.

---

## 3. Stratum 1: Myological Topography (Muscles & Kinetic Tension)

| Muscle Group | Origin & Insertion Anchors | Topographical Feature in Surface Render |
|---|---|---|
| **Pectoralis Major** | Clavicular head (medial clavicle), sternocostal head (sternum/ribs 1-6) → inserts at lateral lip of bicipital groove of humerus | Horizontal shelf on upper chest; sharp lower cleave above ribcage. Must never float disconnected from clavicle or sternum. |
| **Rectus Abdominis** | Pubic crest → inserts at xiphoid process and costal cartilages 5-7 | Paired vertical column divided by **Linea Alba** (central groove) and separated horizontally by 3–4 **Linea Transversae** (tendinous intersections). Asymmetry is natural; perfectly grid-aligned 8-packs look synthetic. |
| **External Obliques** | External surfaces of ribs 5-12 → inserts into iliac crest and aponeurosis | Lateral flank wrapping down into the inguinal ligament, forming the classic "V-line" (Apollo's Belt). |
| **Serratus Anterior** | Lateral surfaces of ribs 1-8 → inserts into costal surface of scapula | "Finger-like" slips or serrations visible along the lateral ribs under the armpit, interdigitating directly with external oblique slips. |
| **Latissimus Dorsi** | Spinous processes T7-L5, thoracolumbar fascia, iliac crest → inserts at intertubercular groove of humerus | Broad winged triangle ("cobra spread") creating the upper V-taper. |
| **Deltoids (Triad)** | Clavicular (anterior), Acromial (lateral), Spinate (posterior) → inserts into deltoid tuberosity of humerus | 3-dimensional "cannonball" wrapping the glenohumeral joint. Directional light creates distinct shadows between anterior and lateral heads. |
| **Biceps Brachii** | Coracoid process (short head), supraglenoid tubercle (long head) → inserts into radial tuberosity | High peak (short head) vs elongated belly (long head), bordered distally by bicipital aponeurosis. |
| **Triceps Brachii** | Infraglenoid tubercle (long), posterior humerus (lateral & medial) → inserts into olecranon of ulna | Distinct "horseshoe" shape formed by lateral head, long head, and central common tendon. |
| **Quadriceps Femoris** | AIIS (rectus femoris), greater trochanter/linea aspera (vastus lateralis), intertrochanteric line (vastus medialis) → patellar tendon | Flared lateral sweep + **Vastus Medialis** ("teardrop" muscle directly above the medial patella). |
| **Gastrocnemius** | Medial and lateral condyles of femur → inserts into calcaneus via Achilles tendon | High diamond split on the posterior/lateral lower leg. |

---

## 4. Stratum 2: Adipose Topography & Vascularity Mapping

### Heath-Carter Somatotype Matrix
- **Ectomorph (1-2-7):** Long linear bone structure, narrow clavicles, minimal subcutaneous adipose, thin muscle bellies.
- **Mesomorph (1-7-1 to 2-6-2):** Broad clavicular frame, narrow pelvic girdle, dense muscle bellies, low to moderate body fat.
- **Endomorph (7-2-1):** Wide bone structure, wider pelvic waist, thicker subcutaneous adipose padding, rounded muscular contours.

### Body Fat Percentage (%BF) Topography Markers
- **Sub-8% (Extreme Competition Leanness):**
  - Skinfold thickness < 4mm at abdominal and subscapular sites.
  - Striations visible across gluteus maximus, lateral triceps, and chest fibers.
  - Prominent venous highways (cephalic, basilic, saphenous, inferior epigastric).
- **9–12% (Peak Athletic Definition):**
  - All 6 abdominal quadrants distinct; linea alba and linea semilunaris clearly engraved.
  - Serratus anterior visible; lower back "Christmas tree" furrow apparent.
  - Forearm and bicep vascularity clear.
- **13–16% (Fit / Athletic Everyday):**
  - Abdominal outline visible, soft lower belly separation.
  - Deltoid roundness maintained, vascularity mostly confined to forearms.
- **17–22% (Solid Bulk / Power):**
  - Full muscle thickness without striation; adipose layer smooths intermuscular valleys.

---

## 5. Stratum 3: DensePose 24-Patch Topological Manifold

DensePose maps 2D image coordinates to 24 continuous UV patches on the SMPL body model:
1. `P1, P2`: Torso Front (P1) & Torso Back (P2)
2. `P3, P4`: Right Upper Arm (Inner/Outer)
3. `P5, P6`: Left Upper Arm (Inner/Outer)
4. `P7, P8`: Right Forearm (Inner/Outer)
5. `P9, P10`: Left Forearm (Inner/Outer)
6. `P11, P12`: Right Hand / Left Hand
7. `P13, P14`: Right Thigh (Front/Back)
8. `P15, P16`: Left Thigh (Front/Back)
9. `P17, P18`: Right Shank/Calf (Front/Back)
10. `P19, P20`: Left Shank/Calf (Front/Back)
11. `P21, P22`: Right Foot / Left Foot
12. `P23, P24`: Head Front (Face) & Head Back

**Agentic Rule:** By specifying active DensePose UV coordinates, the diffusion process is topologically constrained to prevent "sliding textures", anatomically disconnected limbs, or inverted joints.

---

## 6. Stratum 4: Photometric & Surface Normal Principles

### The Raking Light Principle
- Direct frontal flash flattens musculature (washes out intermuscular sulci).
- **Raking Light (Key light at 35°–50° from the side/above):**
  - Light hits the peak of the muscle belly (specular highlight).
  - The terminator line falls sharply into the anatomical groove (e.g. Linea Alba, Infraglenoid fossa).
  - Ambient Occlusion (AO) creates realistic micro-shadows at muscle insertion depths.

### Biological Material Physics
- **Subsurface Scattering (SSS):** Human skin is semi-translucent. Red light penetrates deeper into tissue than green and blue, causing a warm reddish/amber glow along shadow terminator borders. Without SSS, muscles appear like painted plastic or grey stone.
- **Micro-Dermal Relief:** Human skin has anisotropic pores aligned along **Langer's lines** of tissue tension. Perspiration (micro-droplets) adds high-frequency specular glints along the convex apex of muscle bellies.
