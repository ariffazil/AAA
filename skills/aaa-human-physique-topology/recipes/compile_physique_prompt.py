#!/usr/bin/env python3
"""
compile_physique_prompt.py — Human Physique Topography Compiler
Compiles declarative 5-layer physique topography contracts into:
1. Highly densified anatomical prompts (bridging the dimensionality deficit)
2. Negative anatomical constraint tokens
3. ControlNet multi-modal conditioning parameters (OpenPose, DensePose, Depth, Normal)
4. Atomic VLM quality gate verification checklist
"""

from typing import Dict, Any, Tuple, List
import json


def compile_physique_prompt(contract: Dict[str, Any]) -> str:
    """
    Compile a 5-layer physique topography contract into a dense generation prompt.
    """
    demo = contract.get("subject_demographics", {})
    somato = contract.get("somatotype", {})
    skel = contract.get("skeletal_framework", {})
    musc = contract.get("muscular_topography", {})
    photo = contract.get("photometric_micro_topography", {})

    prompt_segments: List[str] = []

    # 1. Base Identity & Demographics
    sex = demo.get("biological_sex", "male")
    age = demo.get("apparent_age_range", "30-year-old")
    height = demo.get("height_cm", 180)
    weight = demo.get("weight_kg", 85)
    tone = demo.get("ethnicity_melanin_tone", "natural skin tone")
    prompt_segments.append(
        f"Masterpiece anatomical physique portrait of a {age} {sex}, {height}cm, {weight}kg, {tone}"
    )

    # 2. Somatotype & Adiposity (Stratum 2)
    bf = somato.get("estimated_body_fat_pct", 10.0)
    vasc = somato.get("vascularity_grade", 2)
    stri = somato.get("muscular_striation_grade", 2)

    somato_desc = f"{bf:.1f}% body fat physique, athletic mesomorphic frame"
    if bf < 9.0:
        somato_desc += ", razor-sharp muscular separation and minimal subcutaneous adipose"
    elif bf < 14.0:
        somato_desc += ", lean athletic definition with clear abdominal wall segmentation"
    else:
        somato_desc += ", powerful athletic build with solid muscular mass"
    prompt_segments.append(somato_desc)

    # Vascularity tokens
    vasc_map = {
        0: "smooth non-vascular skin surface",
        1: "subtle cephalic vein trace along distal forearms",
        2: "prominent cephalic and basilic veins on forearms and bicipital groove",
        3: "ropy branching vascular networks mapping across deltoids, biceps, and forearms",
        4: "high-definition vascular map crossing lower abdominal wall, iliac crest, and upper chest",
        5: "dense systemic vascularity mapping across all kinetic muscle groups"
    }
    prompt_segments.append(vasc_map.get(vasc, vasc_map[2]))

    # Striation tokens
    stri_map = {
        0: "smooth muscle bellies",
        1: "faint linear muscle fiber orientation visible on contraction",
        2: "distinct feathering and fiber striations across lateral deltoids and triceps",
        3: "deep cross-striations visible in pectoralis major, quadriceps, and trapezius",
        4: "competition-grade feathered striations etched deeply into every muscle compartment"
    }
    prompt_segments.append(stri_map.get(stri, stri_map[2]))

    # 3. Skeletal Framework & Ratios (Stratum 0 - Basement Tectonics)
    canon = skel.get("proportion_canon", "7.5_heads_natural")
    ratio = skel.get("biacromial_to_biiliac_ratio", 1.45)
    posture = skel.get("posture_alignment", "athletic_brace")

    canon_map = {
        "8.0_heads_heroic_athletic": "heroic 8.0-head classical canon",
        "7.5_heads_natural": "natural 7.5-head athletic canon",
        "7.0_heads_stocky": "dense stocky 7.0-head powerlifter canon",
        "8.5_heads_stylized_ideal": "stylized 8.5-head fashion canon",
        "observed_demographic": "demographically grounded natural proportions"
    }
    canon_str = canon_map.get(canon, "natural 7.5-head athletic canon")
    prompt_segments.append(
        f"{canon_str}, V-taper frame with {ratio:.2f}:1 shoulder-to-waist biacromial ratio, {posture.replace('_', ' ')}"
    )

    # 4. Muscular Topography Details (Stratum 1 - Structural Geology)
    ant = musc.get("torso_anterior", {})
    post = musc.get("torso_posterior", {})
    arms = musc.get("upper_extremities", {})
    legs = musc.get("lower_extremities", {})
    tension = musc.get("kinetic_tension_state", "isometric_peak_flex").replace("_", " ")

    musc_tokens: List[str] = [f"kinetic tension: {tension}"]
    if ant.get("pectoralis_major"):
        musc_tokens.append(f"pectoralis major {ant['pectoralis_major']} with distinct clavicular head shelf")
    if ant.get("rectus_abdominis_quadrants"):
        musc_tokens.append(f"{ant['rectus_abdominis_quadrants']}, deep linea alba furrow")
    if ant.get("serratus_anterior_visibility"):
        musc_tokens.append(f"serratus anterior {ant['serratus_anterior_visibility']} interdigitating with external obliques")
    if post.get("latissimus_dorsi_spread"):
        musc_tokens.append(f"latissimus dorsi {post['latissimus_dorsi_spread']} flaring to waist")
    if arms.get("deltoids_triad"):
        musc_tokens.append(f"3-head deltoid triad {arms['deltoids_triad']}")
    if arms.get("biceps_brachii_peak"):
        musc_tokens.append(f"biceps brachii {arms['biceps_brachii_peak']} with distinct bicipital aponeurosis")
    if legs.get("vastus_medialis_teardrop"):
        musc_tokens.append(f"vastus medialis teardrop muscle contoured above patella")

    prompt_segments.append(", ".join(musc_tokens))

    # 5. Stratum S: Somatic State Layer (Reservoir Dynamics & Dynamic Embodiment)
    somatic = contract.get("somatic_state") or contract.get("temporal_physiology", {})
    if somatic:
        s_tokens = []
        if somatic.get("respiration_phase"):
            s_tokens.append(f"respiration: {somatic['respiration_phase'].replace('_', ' ')}")
        if somatic.get("weight_distribution"):
            s_tokens.append(f"weight distribution: {somatic['weight_distribution'].replace('_', ' ')}")
        if somatic.get("kinetic_tension"):
            s_tokens.append(f"kinetic tension: {somatic['kinetic_tension'].replace('_', ' ')}")
        if somatic.get("fatigue_state"):
            s_tokens.append(f"metabolic state: {somatic['fatigue_state'].replace('_', ' ')}")
        if somatic.get("emotional_embodiment"):
            s_tokens.append(f"embodied posture: {somatic['emotional_embodiment'].replace('_', ' ')}")
        if somatic.get("muscle_pump_state"):
            s_tokens.append(f"muscle pump: {somatic['muscle_pump_state'].replace('_', ' ')}")
        if somatic.get("hydration_glycogen_fullness"):
            s_tokens.append(f"glycogen status: {somatic['hydration_glycogen_fullness'].replace('_', ' ')}")
        if somatic.get("gravitational_loading"):
            s_tokens.append(f"gravitational vector: {somatic['gravitational_loading'].replace('_', ' ')}")
        if s_tokens:
            prompt_segments.append(", ".join(s_tokens))

    # 6. Optical & Photometric Topography (Stratum 4 - Remote Sensing)
    angle = photo.get("lighting_topography_angle_deg", 45.0)
    sheen = photo.get("surface_hydration_sheen", "subtle_satin_glow").replace("_", " ")
    micro = photo.get("skin_micro_texture", "fine_anisotropic_pores").replace("_", " ")
    prompt_segments.append(
        f"directional raking cross-lighting at {angle:.0f} degrees sculpting muscular relief and intermuscular sulci, "
        f"realistic human skin with {micro}, organic subsurface scattering (SSS) along muscle borders, "
        f"{sheen}, 8k raw photo, photorealistic, Hasselblad H6D-100c medium format clarity"
    )

    return ". ".join(prompt_segments) + "."


def compile_physique_negatives() -> str:
    """
    Standard negative prompts eliminating common diffusion anatomical hallucinations.
    Includes SCAR-VIS-009 (Static Human Fallacy) anti-mannequin guards.
    """
    negatives = [
        "plastic smooth skin", "airbrushed mannequin", "cgi render", "fake 3D look",
        "floating serratus anterior", "misplaced ribs", "asymmetrical deformed pectorals",
        "fused limbs", "polydactyly", "extra fingers", "missing fingers",
        "inverted knee joint", "dislocated clavicle", "random abdominal segmentations",
        "impossible bone length", "unrealistic muscle insertions", "blurred skin pores",
        "oversaturated cartoon", "wax figure texture", "watermark", "signature",
        "statue posture", "mannequin stance", "unbalanced center of gravity",
        "frozen dead expression", "rigid lifeless limbs", "plastic wax figure texture"
    ]
    return ", ".join(negatives)


def compile_conditioning_manifest(contract: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate the ControlNet / conditioning map manifest.
    """
    adapters = contract.get("conditioning_adapters", {})
    return {
        "conditioning_units": [
            {
                "module": "dw_openpose_full",
                "model": "control_v11p_sd15_openpose / flux_controlnet_openpose",
                "weight": adapters.get("controlnet_openpose_weight", 1.0),
                "guidance_start": 0.0,
                "guidance_end": 1.0,
                "purpose": "Anchor 25-keypoint skeletal scaffold and head-to-body ratios"
            },
            {
                "module": "densepose_iuv",
                "model": "controlnet_densepose / densepose_flux",
                "weight": adapters.get("controlnet_densepose_weight", 0.85),
                "guidance_start": 0.0,
                "guidance_end": 0.90,
                "purpose": "Anchor continuous 24-patch geodesic body surface coordinates"
            },
            {
                "module": "depth_zoe / marigold_depth",
                "model": "control_v11f1p_sd15_depth / flux_controlnet_depth",
                "weight": adapters.get("controlnet_depth_weight", 0.75),
                "guidance_start": 0.0,
                "guidance_end": 0.80,
                "purpose": "Enforce volumetric muscular protrusions and depth relief"
            },
            {
                "module": "normal_dsine / normalbae",
                "model": "control_v11p_sd15_normalbae",
                "weight": adapters.get("controlnet_normal_weight", 0.80),
                "guidance_start": 0.0,
                "guidance_end": 0.85,
                "purpose": "Enforce surface normal vectors for accurate raking-light shadow fidelity"
            }
        ]
    }


def compile_vlm_audit_criteria(contract: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compile the atomic quality gate checklist for VLM inspection.
    """
    return {
        "checks": [
            {
                "check_id": "ANATOMY_SKELETAL_INTEGRITY",
                "target": "Stratum 0: Skeletal framework and joint articulation",
                "pass_condition": "Limbs are proportionally aligned (according to specified canon: 7.0/7.5/8.0 heads), joint angles biomechanically valid, clavicle/pelvic girdle stable."
            },
            {
                "check_id": "ANATOMY_BIOMECHANICAL_ATTACHMENT",
                "target": "Stratum 1: Musculoskeletal attachments (Structural Geology)",
                "pass_condition": "Pectoralis major inserts at humerus, latissimus connects spine to humeral sulcus, serratus anterior interdigitates with external obliques over ribs 5-8. NOTE: Topology PASS does NOT guarantee Anatomy PASS."
            },
            {
                "check_id": "TOPOLOGY_SURFACE_CONTINUITY",
                "target": "Stratum 3: DensePose UV continuous skin manifold (Human DEM)",
                "pass_condition": "Surface skin coordinates are continuous across all 24 patches, no texture sliding, seams, or duplicated extremities."
            },
            {
                "check_id": "TEMPORAL_PHYSIOLOGICAL_COHERENCE",
                "target": "Stratum T: Dynamic biomechanical state & metabolic fullness",
                "pass_condition": "Respiration phase (ribcage expansion/vacuum), muscle pump, and gravity drape are physically congruent — subject looks alive, not like a frozen mannequin."
            },
            {
                "check_id": "SOMATIC_EMBODIMENT_LOAD_INTEGRITY",
                "target": "Stratum S: Somatic State Layer & Reservoir Dynamics (SCAR-VIS-009 Anti-Mannequin Gate)",
                "pass_condition": "Center of gravity is grounded and balanced, kinetic tension is differentiated between active vs passive limbs, respiration is physically apparent in thoracic cage, and emotional posture is biomechanically authentic."
            },
            {
                "check_id": "OPTICAL_LIGHTING_CONGRUENCE",
                "target": "Stratum 4: Raking cross-light & dermal subsurface scattering",
                "pass_condition": "Directional light casts micro-shadows into intermuscular sulci (linea alba, serratus clefts), warm subsurface scattering present at shadow terminators without airbrushed plastic glaze."
            }
        ]
    }


if __name__ == "__main__":
    sample_contract = {
        "version": "1.0.0",
        "subject_demographics": {
            "biological_sex": "male",
            "apparent_age_range": "32-year-old",
            "height_cm": 182,
            "weight_kg": 88,
            "ethnicity_melanin_tone": "sun-kissed olive tone"
        },
        "somatotype": {
            "endomorphy": 2.0,
            "mesomorphy": 7.0,
            "ectomorphy": 2.0,
            "estimated_body_fat_pct": 9.5,
            "vascularity_grade": 3,
            "muscular_striation_grade": 3
        },
        "skeletal_framework": {
            "proportion_canon": "8.0_heads_heroic_athletic",
            "biacromial_to_biiliac_ratio": 1.68,
            "posture_alignment": "athletic_brace"
        },
        "muscular_topography": {
            "torso_anterior": {
                "pectoralis_major": "athletic_square",
                "rectus_abdominis_quadrants": "6_pack_distinct",
                "serratus_anterior_visibility": "razor_sharp_finger_slits"
            },
            "torso_posterior": {
                "latissimus_dorsi_spread": "winged_cobra_spread"
            },
            "upper_extremities": {
                "deltoids_triad": "capped_athletic",
                "biceps_brachii_peak": "high_peaked_short_belly"
            },
            "lower_extremities": {
                "vastus_medialis_teardrop": "sculpted_above_patella"
            },
            "kinetic_tension_state": "isometric_peak_flex"
        },
        "photometric_micro_topography": {
            "lighting_topography_angle_deg": 45.0,
            "surface_hydration_sheen": "light_perspiration_sheen",
            "skin_micro_texture": "fine_anisotropic_pores"
        },
        "somatic_state": {
            "respiration_phase": "deep_inhale_ribcage_flared",
            "weight_distribution": "unilateral_60_40_drive",
            "kinetic_tension": "agonist_peak_flexion",
            "fatigue_state": "mid_workout_vascular_warmth",
            "emotional_embodiment": "focused_kinetic_readiness",
            "muscle_pump_state": "hyperemic_full_gym_pump",
            "hydration_glycogen_fullness": "glycogen_loaded_dense",
            "gravitational_loading": "standing_axial_load"
        }
    }

    print("=== COMPILED PROMPT ===")
    print(compile_physique_prompt(sample_contract))
    print("\n=== NEGATIVE PROMPT ===")
    print(compile_physique_negatives())
    print("\n=== CONDITIONING MANIFEST ===")
    print(json.dumps(compile_conditioning_manifest(sample_contract), indent=2))
