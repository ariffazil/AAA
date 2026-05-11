# MaxHermes Tool Manifest
# Exhaustive tool registry for the MaxHermes workspace

version: 1
owner: maxhermes
domain_plane: GEOX

tools:
  # GEOX MCP tools
  - id: geox_load_well_log
    server: geox-mcp
    epistemic_input: OBSERVED
    vault_required: true
    risk_tier: low
    approval_policy: none

  - id: geox_archie_sw
    server: geox-mcp
    epistemic_input: COMPUTED
    vault_required: true
    ac_risk_threshold: 0.25
    risk_tier: low
    approval_policy: on-demand

  - id: geox_kozeny_carman_phi
    server: geox-mcp
    epistemic_input: COMPUTED
    vault_required: true
    risk_tier: low
    approval_policy: on-demand

  - id: geox_seismic_attribute
    server: geox-mcp
    epistemic_input: COMPUTED
    vault_required: false
    risk_tier: medium
    approval_policy: on-demand

  - id: geox_horizon_pick
    server: geox-mcp
    epistemic_input: INTERPRETED
    vault_required: true
    hold_conditions:
      - low_signal_to_noise
      - fault_complex_zone
    risk_tier: medium
    approval_policy: hold

  - id: geox_structural_mapping
    server: geox-mcp
    epistemic_input: CLAIM
    vault_required: true
    risk_tier: high
    approval_policy: hold
    required_witnesses: [GEOX, ARIFOS]

  - id: geox_reservoir_quality
    server: geox-mcp
    epistemic_input: PLAUSIBLE
    vault_required: true
    hold_conditions:
      - no_core_data
      - uncertain_facies
    risk_tier: medium
    approval_policy: hold

  - id: geox_charge_analysis
    server: geox-mcp
    epistemic_input: HYPOTHESIS
    vault_required: false
    hold_conditions:
      - no_geochemical_data
    risk_tier: high
    approval_policy: hold

  - id: geox_monte_carlo_volume
    server: geox-mcp
    epistemic_input: ESTIMATE
    vault_required: true
    hold_conditions:
      - wide_porosity_range
    risk_tier: high
    approval_policy: hold

  - id: geox_physics_guard
    server: geox-mcp
    epistemic_input: MANDATORY_GATE
    vault_required: true
    risk_tier: low
    approval_policy: none
    note: Required gate on all geox outputs

  - id: geox_vault_read
    server: geox-mcp
    epistemic_input: OBSERVED
    vault_required: false
    risk_tier: low
    approval_policy: none

  - id: geox_1d_model
    server: geox-mcp
    epistemic_input: COMPUTED
    vault_required: true
    risk_tier: medium
    approval_policy: on-demand

  - id: geox_2d_section
    server: geox-mcp
    epistemic_input: COMPUTED
    vault_required: true
    risk_tier: medium
    approval_policy: on-demand

  - id: geox_well_correlation
    server: geox-mcp
    epistemic_input: INTERPRETED
    vault_required: true
    risk_tier: medium
    approval_policy: hold

  - id: geox_time_depth
    server: geox-mcp
    epistemic_input: COMPUTED
    vault_required: true
    risk_tier: medium
    approval_policy: on-demand

  # arifOS MCP tools
  - id: arifos_compute_risk
    server: arifos-mcp
    epistemic_input: MANDATORY_GATE
    vault_required: true
    risk_tier: low
    approval_policy: none
    note: AC_Risk adjudication — mandatory before any claim

  - id: arifos_judge
    server: arifos-mcp
    epistemic_input: CONSTITUTIONAL
    vault_required: true
    risk_tier: high
    approval_policy: human-required
    hold_conditions:
      - arifOS verdict is HOLD or VOID
    required_witnesses: [ARIFOS]

  - id: arifos_init
    server: arifos-mcp
    epistemic_input: MANDATORY_BOOT
    vault_required: false
    risk_tier: low
    approval_policy: none
    note: Mandatory session start — arifos.init

  - id: arifos_f9_hantu
    server: arifos-mcp
    epistemic_input: MANDATORY_GATE
    vault_required: true
    risk_tier: low
    approval_policy: none
    note: F9 Anti-Hantu check — mandatory before VOID

  # WELL MCP tools
  - id: well_readiness
    server: well-mcp
    epistemic_input: OBSERVED
    vault_required: false
    risk_tier: low
    approval_policy: on-demand

  # Internal tools
  - id: geox_vault_write
    internal: true
    epistemic_input: COMPUTED
    vault_required: true
    risk_tier: high
    approval_policy: human-required
    note: Writing vault receipts — track per-session budget

  - id: maxhermes_memory_log
    internal: true
    epistemic_input: OBSERVED
    vault_required: false
    risk_tier: low
    approval_policy: none

  - id: maxhermes_escalate
    internal: true
    epistemic_input: CONSTITUTIONAL
    vault_required: true
    risk_tier: high
    approval_policy: human-required
    note: HOLD escalation to Arif
