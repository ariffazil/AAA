# MaxHermes Hermes Skill — Tool Orchestration & Session Management
# "Grounded geophysics. Governed action. No fiction."

skill_id: maxhermes-hermes
name: MaxHermes Hermes
version: 0.1.0
owner: AAA
domain_plane: GEOX
risk_tier: medium

description: >
  Core orchestration skill for MaxHermes geophysics agent.
  Manages GEOX tool calls, session context, memory, and
  workflow coordination. The "conductor" skill — routes
  tasks to the right tools with correct epistemic labeling.

knowledge_basis:
  physics: true
  math: true
  language: true

host_compatibility:
  - openclaw-maxhermes
  - hermes-agent
  - claude-code
  - codex

dependencies:
  skills:
    - geox-grounding
    - maxhermes-arifos-sense
  servers:
    - geox-mcp
    - arifos-mcp
    - well-mcp
  tools:
    - geox-query
    - geox-vault-read
    - arifos-judge

epistemic_pipeline:
  # Every tool call must pass through this pipeline
  1_preflight:
    - check: arifos.init loaded?
      if_fail: load arifos.init before proceeding
    - check: task domain is GEOX or cross-domain?
      if_cross_domain: route through aaa-gateway
    - check: required witnesses available?
      if_missing: apply HOLD, escalate

  2_ground:
    - invoke: geox-grounding skill
    - extract: AC_Risk, ClaimTag, hold_conditions
    - validate: physics checks via PhysicsGuard

  3_verdict:
    - apply: SEAL / CAUTION / HOLD / VOID
    - if_void: reject immediately, log to void-log
    - if_hold: pause, escalate to aaa-gateway
    - if_caution: warn, proceed with uncertainty noted
    - if_seal: execute with vault receipt

  4_output:
    - generate: vault_receipt with timestamp, hash, verdict
    - apply: ClaimTag epistemic label
    - record: memory/ if significant decision
    - emit: audit event if 888 CLAIM-grade

workflows:
  - id: geox-well-log-full
    description: Full well-log analysis workflow
    steps:
      - geox_load_well_log
      - geox_compute_archie_sw
      - geox_compute_kozeny_phi
      - geox_adjudicate_ac_risk
      - arifos_judge
    epistemic_contract:
      min_claim: CLAIM
      vault_required: true
      hold_conditions:
        - ac_risk >= 0.75
        - missing_core_data
        - uncertain_porosity_model

  - id: geox-prospect-full
    description: Full prospect evaluation workflow
    steps:
      - geox_structural_mapping
      - geox_reservoir_quality
      - geox_charge_analysis
      - geox_monte_carlo_volume
      - geox_final_verdict
    epistemic_contract:
      min_claim: PLAUSIBLE
      vault_required: true
      required_witnesses: [GEOX, ARIFOS, HUMAN]
      hold_conditions:
        - any_component HYPOTHESIS
        - ac_risk >= 0.75

session_memory:
  path: agents/maxhermes/memory/
  daily_format: "memory/YYYY-MM-DD.md"
  carry_forward: true
  curate_on: session_end

examples:
  - "Analyze this wireline log for porosity and water saturation"
  - "Evaluate this prospect for exploration potential"
  - "What is the AC_Risk on this horizon pick?"

pitfalls:
  - Do NOT call geox tools without arifos.init loaded
  - Do NOT present ESTIMATE as COMPUTED or COMP as OBSERVED
  - Do NOT skip AC_Risk adjudication on interpretations
  - Do NOT self-seal — require arifos-kernel verdict
  - Do NOT write to vault without ClaimTag label
