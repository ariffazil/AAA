---
id: arifos-recursive-audit
name: arifOS Recursive Audit
version: 1.0.0
description: Audit all installed skills for overlap, stale docs, prompt bloat, trigger
  ambiguity, and broken references. Load when reviewing the skill portfolio or after
  modifying or adding new skills.
owner: AAA
risk_tier: medium
knowledge_basis:
  language: true
  math: false
  physics: false
host_compatibility:
- claude-code
- codex
- opencode
- kimi
- kimi-code
dependencies:
  skills:
  - skill-trigger-linter
  servers: []
  tools: []
examples:
- Audit all installed skills for doc-rot and trigger-rot
- Flag a skill whose references to wrangler versions are stale
tests:
- Circular skill reference detected and logged
- Skill >30 days old without compatibility check flagged
version_lock:
  schema_version: '1'
  artifact_hash: pending
orthogonal_tags:
  trinitarian:
  - ΦΙ
  functional:
  - Governance
  layer: HEXAGON
  autonomy_tier: T2
floor_scope:
- F2
- F4
- F7
- F9
- F11
---

# arifos-recursive-audit (O_Ω Constitutional Layer)

## arifOS-ACT Embedding

Before using this skill on any mutating, irreversible, or high-blast-radius task:
1. **ART** — Attune (what is the real task?), Recognize (what class of power?), Test (fit · authority · evidence · blast · reversible).
2. **Kernel** — Route to arifOS for F1–F13 judgment if action class is Maker/Messenger/Mutator/Destroyer/Sovereign.
3. **ACT** — Apply narrow, Constrain scope, Trace witness, STOP before corruption.
4. **Receipt** — Leave evidence of what changed, why, and under whose authority.


## Purpose
Audit all installed skills for overlap, stale docs, prompt bloat, trigger ambiguity, and broken references.

## Use When
1. Reviewing the overall capabilities, naming conventions, and performance of the active skill portfolio.
2. A new skill is drafted or proposed for installation into any workspace or global directory.
3. An existing skill's `SKILL.md` is updated or modified.
4. Executing portfolio maintenance checks to clean up outdated APIs, dead links, or legacy documentation.
5. Tuning the triggering accuracy of skills when experiencing trigger drift.

## Do Not Use When
1. Creating a single new skill from scratch (use `skill-creator` for capture and bootstrapping instead).
2. Linting individual skill trigger statements (use `skill-trigger-linter` instead).
3. The task is a general system performance audit unrelated to L2 Skills.

## Inputs
*   **Skill Directories:** Path to `/root/.agents/skills/` or individual skill directories.
*   **Dependency Files:** package.json, pyproject.toml, wrangler.jsonc configurations.
*   **Audit Manifest:** List of currently configured tools and their execution limits.

## Operational Age Thresholds
*   **Freshness Threshold:** Any skill whose `SKILL.md` has not been modified for **>30 days** MUST be cross-checked against its dependent packages/APIs to verify compatibility.
*   **De-activation Candidate:** Any skill that has not been active in the last **90 days** must be classified as `unused-rot` and flagged for graceful de-activation or archive.

## Rot Classification Schema
Each checked skill must receive a specific Rot Rating in the audit report:
*   **`doc-rot`:** The skill references external URLs, guidelines, or paths that are no longer accessible or have been superseded.
*   **`api-rot`:** The SDK or CLI packages that the skill coordinates (e.g. Wrangler, Agents SDK) have moved past the compatibility versions listed in the skill.
*   **`trigger-rot`:** The skill's triggering criteria overlap semantically with other skills, leading to multiple activations or trigger failures.
*   **`unused-rot`:** The skill is structurally valid but has not registered a telemetry execution record within the threshold window.

## Procedure
1.  **Portfolio Scan:** Map all active `SKILL.md` files and resolve their frontmatter definitions.
2.  **Staleness Analysis:** Apply **Age Threshold** rules. Check all embedded documentation URLs and reference scripts against the latest system files and packages.
3.  **Prompt Bloat Check:** Calculate the token density of each skill. Flag files where instruction length exceeds 500 lines.
4.  **Collision Auditing:** Run semantic cross-checks on skill descriptions to flag potential trigger overlaps.
5.  **Rot Classification tagging:** Assign rot ratings (`doc-rot`, `api-rot`, `trigger-rot`, `unused-rot`) to flagged skills.
6.  **Report Generation:** Write a structured markdown analysis identifying critical flaws, warnings, and remediation paths.

## Postconditions
1.  All skills are checked for age thresholds and direct system dependency freshness.
2.  A complete rot matrix mapping overlap risk and prompt size is successfully outputted.
3.  Any identified broken file reference is cataloged in the telemetry report.

## Failure Modes & Escalation
*   **Infinite Loop Detect:** Circular references between skills (e.g. Skill A loads Skill B, which loads Skill A). *Action:* Immediately break recursion, output a warning block, and log the path loop.
*   **Workspace Access Error:** Missing permissions on global or shared folders. *Action:* Degrade gracefully and audit only local workspace skills, raising a warning flag in the report.

## Telemetry per Run
```json
{
  "skill_name": "arifos-recursive-audit",
  "version": "1.1.0",
  "trigger_phrase": "{{trigger_phrase}}",
  "selected_reason": "{{selected_reason}}",
  "latency_ms": 0,
  "token_in": 0,
  "token_out": 0,
  "commands_run": 0,
  "artifacts_written": 0,
  "postcondition_pass": false,
  "human_approval_required": false,
  "hold_code": "{{hold_code}}"
}
```

## Recursive Scorecard
*   **Activation Precision:** [0.0 - 1.0] (Target: >0.90)
*   **Task Completion Rate:** [0.0 - 1.0] (Target: >0.95)
*   **Rollback Safety:** [0.0 - 1.0] (Target: 1.00)
*   **Context Efficiency:** [0.0 - 1.0] (Target: >0.95)
*   **Doc Freshness:** [0.0 - 1.0] (Target: 1.00)
*   **Cross-Skill Collision Rate:** [0.0 - 1.0] (Target: 0.00)
*   **Human Trust Score:** [0.0 - 1.0] (Target: >0.95)