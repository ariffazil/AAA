# HERMES Site Autoresearch Skill — Recursive Site Improvement via arifOS MCP
# Karpathy autoresearch pattern adapted for arifOS federation sites
# Traffic-light verdicts: 🔴 RED (VOID) → 🟡 YELLOW (SABAR) → 🔵 BLUE (SEAL)

skill_id: site-autoresearch
name: HERMES Site Autoresearch
version: 1.0.0
owner: AAA
domain_plane: ARIF_SITES
risk_tier: medium

description: >
  Autonomous recursive site improvement loop for arifOS federation surfaces.
  Adapts Karpathy's autoresearch pattern: modify → measure → judge → keep/discard.
  Uses arifOS MCP tools for constitutional judgment, vault sealing, and evidence preservation.
  Lower SCD (Site Coherence Defect) is better. 0.0 = perfect.

knowledge_basis:
  physics: false
  math: true
  language: true
  web: true

host_compatibility:
  - openclaw-maxhermes
  - hermes-agent
  - claude-code
  - codex
  - kimi-code

# ---------------------------------------------------------------------------
# Experiment Loop (The Core)
# ---------------------------------------------------------------------------

experiment_loop:
  invariant: >
    Each experiment modifies exactly ONE site file per iteration.
    The measurement harness (/root/sites/measure.py) is read-only.
    The agent NEVER stops once the loop begins.

  phases:
    1_observe:
      tool: arif_sense_observe(mode='ingest', url='https://{site}.arif-fazil.com')
      purpose: Capture current site state before mutation
      output: html_snapshot, headers, ttfb

    2_plan:
      tool: arif_mind_reason(mode='plan')
      purpose: Generate a concrete, minimal site improvement hypothesis
      constraints:
        - One file per experiment
        - Must be reversible (git branch per experiment)
        - Must reference a specific SCD category defect
      output: plan_receipt with plan_id

    3_mutate:
      tool: arif_forge_execute(mode='write')
      purpose: Apply the planned change to the site file
      constraints:
        - Write to /root/sites/{site}/ only
        - Do NOT modify Caddyfile or docker-compose.yml
        - Do NOT modify measure.py
      output: artifact_id

    4_measure:
      command: python3 /root/sites/measure.py --site {site} --format tsv
      purpose: Compute SCD before and after mutation
      output: scd_before, scd_after, delta_scd

    5_judge:
      tool: arif_judge_deliberate(mode='judge')
      purpose: Constitutional review of the change
      criteria:
        - F1 Amanah: Is the change reversible? (git branch exists)
        - F2 Truth: Does the measured improvement match the claim?
        - F8 Genius: Is the change elegant, not hacky?
        - F10 Ontology: Does the change preserve structural coherence?
      output: verdict ∈ {SEAL, SABAR, VOID, HOLD}

    6_verdict:
      mapping:
        BLUE:  "SEAL — scd improved, constitutional review passed → advance branch"
        YELLOW: "SABAR — scd unchanged or marginal, or constitutional concern → flag for human review"
        RED:    "VOID — scd regressed, or crash, or constitutional violation → git reset --hard"
      output: verdict_code + vault_receipt

    7_seal:
      tool: arif_vault_seal(mode='seal')
      purpose: Anchor the experiment outcome to VAULT999
      condition: Only for BLUE (SEAL) outcomes
      payload:
        - site
        - commit_hash
        - scd_before
        - scd_after
        - delta_scd
        - verdict
        - plan_id
        - artifact_id
      output: vault_entry_id

    8_repeat:
      purpose: Loop until human interruption
      strategy: >
        If stuck, recall prior experiments via arif_memory_recall.
        Combine near-misses. Try radical simplifications.
        Read the site's SKILL.md for domain-specific constraints.

# ---------------------------------------------------------------------------
# Traffic-Light Verdict System (RED / YELLOW / BLUE)
# ---------------------------------------------------------------------------

traffic_lights:
  RED:
    code: VOID
    color: "#8B3A3A"
    triggers:
      - scd_after > scd_before  (regression)
      - measure.py returns status: crash
      - arif_judge_deliberate returns VOID
      - F1 Amanah violated (no git branch, irreversible change)
      - F9 Anti-Hantu triggered (dark pattern, shadow behavior)
    action: "git reset --hard HEAD~1 → log crash in results.tsv → continue"
    human_notify: false  # autonomous recovery

  YELLOW:
    code: SABAR
    color: "#C4A35A"
    triggers:
      - abs(delta_scd) < 0.01  (marginal, within noise)
      - scd_after == scd_before
      - arif_judge_deliberate returns SABAR or HOLD
      - F7 Humility concern (uncertainty too high)
    action: "Keep commit but flag in results.tsv as 'sabar' → continue"
    human_notify: true   # queue for human review

  BLUE:
    code: SEAL
    color: "#4A7C8B"
    triggers:
      - scd_after < scd_before  (improvement)
      - arif_judge_deliberate returns SEAL
      - All F1-F13 floors pass
    action: "git commit --amend --no-edit → advance branch → vault seal → continue"
    human_notify: false  # autonomous advance

# ---------------------------------------------------------------------------
# Measurement Harness Contract
# ---------------------------------------------------------------------------

measurement_contract:
  path: /root/sites/measure.py
  read_only: true
  metric: SCD (Site Coherence Defect)
  direction: lower_is_better
  baseline_required: true
  categories:
    - performance   (weight 0.25)
    - structure     (weight 0.20)
    - seo           (weight 0.15)
    - accessibility (weight 0.15)
    - constitutional (weight 0.15)
    - federation    (weight 0.10)

# ---------------------------------------------------------------------------
# File Scope (What the agent CAN and CANNOT touch)
# ---------------------------------------------------------------------------

in_scope:
  - /root/sites/{site}/index.html
  - /root/sites/{site}/css/
  - /root/sites/{site}/js/
  - /root/sites/{site}/assets/
  - /root/sites/{site}/llms.txt
  - /root/sites/{site}/llms-full.txt
  - /root/sites/{site}/.well-known/agent.json
  - /root/sites/{site}/robots.txt
  - /root/sites/{site}/sitemap.xml

out_of_scope:
  - /root/sites/measure.py           (read-only harness)
  - /root/arifOS/Caddyfile           (infrastructure)
  - /root/compose/docker-compose.yml (infrastructure)
  - /root/arifOS/                    (kernel — read only)
  - Any file outside /root/sites/

# ---------------------------------------------------------------------------
# Git Discipline (F1 Amanah)
# ---------------------------------------------------------------------------

git_protocol:
  branch_prefix: autoresearch/
  branch_naming: "autoresearch/{site}-{YYYYMMDD}-{agent_id}"
  baseline_commit: Must be clean master before first experiment
  commit_message: "[site-autoresearch:{site}] {brief_description} | SCD {before}→{after}"
  never_commit:
    - results.tsv
    - run.log
    - __pycache__
    - .env
  rollback_command: "git reset --hard {baseline_commit}"

# ---------------------------------------------------------------------------
# Logging Format
# ---------------------------------------------------------------------------

results_tsv:
  path: results.tsv  # untracked, leave out of git
  columns:
    - commit        # short hash
    - site          # which site
    - scd_before    # float 6 decimals
    - scd_after     # float 6 decimals
    - delta_scd     # float 6 decimals
    - status        # keep | sabar | void | crash
    - verdict       # SEAL | SABAR | VOID | HOLD
    - description   # what was tried
    - vault_id      # VAULT999 entry id (if SEAL)

# ---------------------------------------------------------------------------
# Pitfalls
# ---------------------------------------------------------------------------

pitfalls:
  - Do NOT modify Caddyfile or Docker configs. That breaks F10 Ontology.
  - Do NOT install new packages. Only use existing stack (Python stdlib + requests).
  - Do NOT delete files irreversibly. Always git-tracked, always branch-per-experiment.
  - Do NOT present cosmetic changes as structural improvements. Be honest in description.
  - Do NOT ignore YELLOW (SABAR) flags. They are signal, not noise.
  - Do NOT bypass arif_judge_deliberate. Every experiment MUST pass judgment.
  - Do NOT seal without a plan_id from arif_mind_reason. H2 ratification required.
  - Do NOT flood the vault. Only SEAL outcomes get vault entries.

# ---------------------------------------------------------------------------
# arifOS Integration Contract
# ---------------------------------------------------------------------------

arifos_init_contract:
  path: arifos.init
  must_load: true
  godel_lock: true
  anti_drift: true
  required_tools_per_phase:
    observe:  [arif_sense_observe]
    plan:     [arif_mind_reason]
    mutate:   [arif_forge_execute]
    measure:  [arif_ops_measure]  # health/vitals check on mutation
    judge:    [arif_judge_deliberate]
    seal:     [arif_vault_seal]
    recall:   [arif_memory_recall]
