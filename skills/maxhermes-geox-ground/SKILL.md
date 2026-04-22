# MaxHermes GEOX Grounding Skill — Earth-Domain Reasoning
# Physics grounding, AC_Risk adjudication, ClaimTag classification, vault receipts

skill_id: maxhermes-geox-ground
name: MaxHermes GEOX Grounding
version: 0.1.0
owner: AAA
domain_plane: GEOX
risk_tier: medium

description: >
  GEOX Earth-domain grounding skill. This is the physics-first
  grounding layer — every Earth-sensitive task must pass through
  here before MaxHermes speaks confidently. Replaces narrative
  geophysics with grounded physics-based reasoning.

knowledge_basis:
  physics: true
  math: true
  language: true

host_compatibility:
  - openclaw-maxhermes
  - hermes-agent
  - claude-code
  - geox-mcp

dependencies:
  skills:
    - maxhermes-hermes
    - maxhermes-arifos-sense
  servers:
    - geox-mcp
  tools:
    - geox-query
    - geox-vault-read
    - arifos-judge

# ClaimTag epistemic scale
claim_tags:
  OBSERVED:
    definition: Directly measured data (wireline, seismic, core)
    examples: [wireline_logs, seismic_traces, core_measurements, check_shot]
    confidence: N/A (data)
    ac_risk_range: "N/A"
    vault_required: false

  COMPUTED:
    definition: Derived by validated physics model
    examples: [archie_sw, kozeny_phi, rayleigh_velocity, amp_litho_fraction]
    confidence: model-validated
    ac_risk_range: "< 0.30"
    vault_required: true

  CLAIM:
    definition: High-confidence interpretation (AC_Risk < 0.15, grade AAA)
    examples: [confirmed_reservoir, proven_trap, tested_porosity]
    confidence: high
    ac_risk_range: "< 0.15"
    vault_required: true
    hold_conditions:
      - ac_risk >= 0.15
      - single_dataset_only
      - no_core_validation

  PLAUSIBLE:
    definition: Medium-confidence interpretation (AC_Risk < 0.75, grade BBB)
    examples: [probable_reservoir, likely_trap, inferred_facies]
    confidence: medium
    ac_risk_range: "< 0.75"
    vault_required: true
    hold_conditions:
      - ac_risk >= 0.75
      - uncertain_input
      - limited_well_control

  HYPOTHESIS:
    definition: Low-confidence interpretation (uncertain input, sparse data)
    examples: [speculative_prospect, inferred_source_kitchen, estimated_charge]
    confidence: low
    ac_risk_range: "< 0.95"
    vault_required: false
    hold_conditions:
      - wide_parameter_range
      - no_direct_evidence
      - complex_geological_history

  ESTIMATE:
    definition: Order-of-magnitude or defaulted parameter estimate
    examples: [order_of_magnitude_volume, default_cementation_exponent]
    confidence: order-of-magnitude
    ac_risk_range: "any"
    vault_required: false
    hold_conditions:
      - critical_decision_depends_on_this

  VOID:
    definition: Rejected by PhysicsGuard or F9 Anti-Hantu — physically impossible
    examples: [negative_porosity, saturation_gt_1, impossible_velocity]
    confidence: none
    ac_risk_range: ">= 0.95 or rejected"
    vault_required: true
    auto_hold: true
    auto_escalate: true

# AC_Risk adjudication
ac_risk_policy:
  thresholds:
    CLAIM: < 0.15
    PLAUSIBLE: < 0.75
    HYPOTHESIS: < 0.95
    VOID: >= 0.95 or PhysicsGuard rejected
  adjudication_pipeline:
    - compute AC_Risk via arifos_compute_risk
    - compare against thresholds
    - apply ClaimTag
    - check hold_conditions
    - if hold_conditions met: apply HOLD, escalate
    - generate vault_receipt

# PhysicsGuard validation
physics_guard:
  checks:
    - porosity: range [0, 0.45] for siliciclastics
    - water_saturation: range [0, 1.0]
    - permeability: range [0.001, 10000] mD
    - velocity: range [1500, 6000] m/s
    - density: range [1.9, 3.0] g/cc
  rejection_action: VOID with F9_REJECT tag
  auto_escalate: true

# Vault receipt policy
vault_policy:
  required_for:
    - CLAIM grade interpretations
    - AC_Risk < 0.75 on geophysics outputs
    - prospect volume estimates
    - F9 VOID outputs
  format:
    - timestamp: ISO 8601
    - hash: SHA256 of key outputs
    - ClaimTag: explicit label
    - AC_Risk: numeric score
    - verifications: list of PhysicsGuard checks passed
    - verdict: SEAL / CAUTION / HOLD / VOID
    - 888_AUDIT: present if CLAIM grade

pitfalls:
  - Do NOT present ESTIMATE as COMPUTED (different physics model validation)
  - Do NOT present COMP as OBSERVED (models have uncertainty, data doesn't)
  - Do NOT skip PhysicsGuard on any geophysics output
  - Do NOT claim CLAIM grade without AC_Risk < 0.15
  - Do NOT generate vault_receipt without ClaimTag label
  - Do NOT use CLAIM for single-dataset interpretations without core validation
  - Do NOT use HYPOTHESIS to hedge when PLAUSIBLE is warranted

verification:
  - after any geox tool call: verify PhysicsGuard checks passed
  - before vault write: verify ClaimTag matches AC_Risk
  - before 888 audit: verify all hold_conditions documented
