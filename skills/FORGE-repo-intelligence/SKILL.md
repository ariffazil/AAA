---
id: repo-intelligence
name: FORGE-repo-intelligence
version: 1.0.0
description: 'SOLE controller skill for repository intelligence across the arifOS Federation. Exposes 12 modes (inventory, map, delta, pr_review, ci_diagnose, issue_triage, security, cross_repo_impact, release_audit, workflow_integrity, manifest_reconcile, ruleset_audit). Smaller GitHub skills (pr-review, ci-diagnose, issue-triage, github-ops) are consolidated as internal modules under this controller. No other repo-intelligence skill should be created — extend modes instead. Every mode outputs a minimum evidence envelope with repo, ref, commit_sha, working_tree, tag_delta, changed_files, critical_paths, tests, ci, security, contract_impacts, runtime_probe, risk_tier, proposed_action, rollback, evidence_class, and unknowns.'
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
- copilot-cli
dependencies:
  skills:
    - FORGE-pr-review
    - FORGE-pr-governance
    - FORGE-ci-diagnose
    - FORGE-issue-triage
    - FORGE-github-ops
    - aaa-agent-invariants
    - code-wiki
    - parallel-authority-detection
    - secret-safety-scan
  servers:
    - a-forge
    - github-official
  tools:
    - forge_worktree
    - forge_git_status
    - forge_git_diff
    - forge_git_log
    - forge_filesystem_read
    - forge_filesystem_grep
    - forge_github_search
    - forge_github_get_file
examples:
- Audit all 7 federation repos for tag-vs-main drift
- Cross-repo impact analysis for a contract change
- Full release audit: tag, commit, CI, artifact, runtime parity
- PR review with efficient diff pattern: metadata → filenames → critical files → patches
tests:
- inventory mode returns all 7 repos with branch, tag, commit, dirty state
- release_audit mode detects tag-vs-main divergence
- pr_review mode uses efficient diff pattern (filenames first, then critical patches)
- cross_repo_impact mode detects contract changes across organ boundaries
- security mode scans workflows for unpinned actions and missing permissions
version_lock:
  schema_version: '1'
  artifact_hash: pending
orthogonal_tags:
  trinitarian:
  - Ω
  - Ψ
  functional:
  - Meta
  - Ops
  - Audit
  layer: CODING/FI
  autonomy_tier: T1
floor_scope:
- F1
- F2
- F11
---

# FORGE-repo-intelligence — Controller Skill

> **One controller. Twelve modes. No duplicate logic.**
> This skill is the SOLE repository intelligence controller. Smaller GitHub skills are consolidated as internal modules.
> Every mode produces the minimum evidence envelope defined below.

## Operating Loop

```
OBSERVE → MAP → DIFF → VERIFY → REVIEW → (JUDGE) → (ACT) → RE-PROBE → RECEIPT
```

Parenthesized stages (JUDGE, ACT) require mutation authority and are gated.

## Minimum Evidence Envelope

Every mode output must include:

```yaml
repo:
ref:
commit_sha:
working_tree:
tag_delta:
changed_files:
critical_paths:
tests:
ci:
security:
contract_impacts:
runtime_probe:
risk_tier:
proposed_action:
rollback:
evidence_class:
unknowns:
```

Use `UNMEASURED` for any field where the probe failed — never substitute `0`, `clean`, or `healthy`.

---

## Modes

### `inventory` — Repository census

Orchestrates: `FORGE-github-ops`

```yaml
scope: all 7 federation repos
output:
  - repo name, remote, default branch
  - current branch, HEAD SHA, tag list
  - working tree dirty/clean
  - ahead/behind origin
  - collaborator permissions
```

Tool path: `forge_worktree` per repo → `forge_git_status` → `forge_git_log` → GitHub API for permissions.

### `map` — Architecture and critical paths

Orchestrates: `code-wiki`, `aaa-agent-invariants`

```yaml
output:
  - entry points, build commands, test runners
  - contract files (schemas, registries, manifests)
  - ownership (CODEOWNERS, organ responsibility)
  - generated vs hand-maintained files
  - critical paths that gate deployment
```

### `delta` — Ref comparison

Orchestrates: `FORGE-github-ops`

```yaml
input: base_ref, head_ref (branches, tags, or commits)
output:
  - commit diff (count, authors, files changed)
  - tag-vs-main drift detection
  - deployed-vs-source comparison
  - surface/manifest parity (tools/list vs tool_registry.json)
```

Never equate "clean" with "correct." A clean tree proves only no local changes.

### `pr_review` — Efficient diff review

Orchestrates: `FORGE-pr-review`, `FORGE-pr-governance`, `secret-safety-scan`

**Efficient pattern (DO NOT load 20,000-line diffs first):**

```text
1. PR metadata (title, author, base/head, labels)
2. Changed filenames only → list_pr_changed_filenames
3. Identify critical files (contracts, schemas, registries, workflows, constitution)
4. Fetch only critical file patches → fetch_pr_file_patch
5. Inspect review threads → list_pull_request_review_threads
6. Inspect CI status → fetch_commit_workflow_runs
7. Produce risk verdict
```

Risk classification:
- `LOW`: docs, comments, non-critical config
- `MEDIUM`: source changes in single organ, no contract impact
- `HIGH`: contract/schema/registry changes, cross-repo impact
- `CRITICAL`: constitutional, deployment, or secret-adjacent

### `ci_diagnose` — Workflow analysis

Orchestrates: `FORGE-ci-diagnose`

```yaml
input: repo, commit SHA or PR number
output:
  - workflow runs for commit
  - job-level pass/fail breakdown
  - step-level failure extraction
  - log analysis for root cause
  - classification: flake | dependency | regression | config | security
```

**Truth gate:** Never label a diagnostic-survival job as "passed." If lint fails but `continue-on-error` keeps the workflow green, report the truth.

### `issue_triage` — Issue intelligence

Orchestrates: `FORGE-issue-triage`

```yaml
input: repo, query filters
output:
  - deduplicated issue list
  - severity classification
  - routing (which organ, which agent)
  - linked PRs and cross-references
```

### `security` — Supply-chain and secret audit

Orchestrates: `secret-safety-scan`, `parallel-authority-detection`

```yaml
checks:
  - unpinned actions (movable tags → require SHA pinning)
  - least-privilege permissions (permissions: {} declared)
  - concurrency cancellation
  - OIDC vs long-lived credentials
  - artifact attestations
  - CODEOWNERS coverage for constitutional/registry/schema/deployment files
  - secret patterns in source
```

### `cross_repo_impact` — Federation boundary detection

Orchestrates: `code-wiki`, `FORGE-pr-review`

```yaml
input: changed files or PR
output:
  - which organs are affected
  - contract/schema/registry changes
  - breaking vs additive changes
  - required witness count per blast radius
  - organ attestation impacts
```

### `release_audit` — Tag, commit, CI, artifact, runtime parity

Orchestrates: `federation-release-attestation`

```yaml
output (per repo):
  - tag → commit SHA
  - commit → CI run status
  - CI → artifact hash
  - artifact → deployed commit
  - deployed → runtime health probe
  - tools/list match against registry

federation manifest:
  release: "vYYYY.MM.DD-AAA"
  repos:
    arifOS:    { commit, ci, artifact, runtime }
    A-FORGE:   { commit, ci, artifact, runtime }
    AAA:       { commit, ci, artifact, runtime }
    GEOX:      { commit, ci, artifact, runtime }
    WEALTH:    { commit, ci, artifact, runtime }
    WELL:      { commit, ci, artifact, runtime }
    arif-sites:{ commit, ci, artifact, runtime }
```

**Tag discipline:** Never silently move a published federation tag. Treat tags as immutable receipts. If a tag is behind main, issue a new corrected tag rather than overwriting.

### `workflow_integrity` — YAML validation and structural audit

Orchestrates: internal (no sub-skill — pure structural validation)

```yaml
input: repo path or PR number
checks:
  - Parse all YAML workflows (Python yaml.safe_load_all)
  - Reject duplicate job IDs
  - Reject malformed expressions (${{ }})
  - Reject reusable workflows referenced by moving branch names (@main, @v1)
  - Reject overly broad permissions (write-all)
  - Reject pull_request_target without explicit isolation
  - Actionlint validation
  - Unsafe pattern detection (shell injection, unpinned SHAs)
output:
  - Pass/fail per workflow file
  - Specific error locations (file:line)
  - Blocking vs advisory classification
```

**Truth gate:** A workflow that survives parsing with duplicate keys is silently corrupt. GitHub may keep only one. This mode catches that BEFORE merge.

### `manifest_reconcile` — Tool surface truth reconciliation

Orchestrates: internal + runtime probes

```yaml
input: organ name
output:
  - README declared count vs live tools/list count
  - FEDERATION.md declared count vs live
  - AGENTS.md declared count vs live
  - organ.yaml declared interfaces vs actual
  - Staleness score (days since last verification)
  - Recommendations: which source to update
  - Canonical manifest update (AAA/federation/repos.yaml)
rule: runtime beats README beats FEDERATION.md
```

**Truth gate:** If README says 8 tools and runtime says 12, the README is wrong. Update it. Do not "reconcile" by averaging.

### `ruleset_audit` — Branch protection and deployment policy

Orchestrates: GitHub API

```yaml
input: repo name or 'all'
output per repo:
  - Branch protection status (PR required, force push, linear history, deletions)
  - Required status checks configured
  - CODEOWNERS coverage for critical paths (contracts, schemas, registries, deploy)
  - Merge queue status
  - Tag protection status
  - Deployment environment protections
  - Gaps identified with specific remediation steps
```

**Remediation:** Can auto-apply ruleset via `gh api` (requires repo admin). Default policy:
- PRs required on main, force push blocked, deletions blocked
- Linear history, conversation resolution
- Signed commits for constitutional paths

---

## Tool Routing

| Intelligence Task | GitHub Tools | A-FORGE Tools |
|---|---|---|
| Repository inventory | `search_repositories`, `get_file_contents` | `forge_worktree`, `forge_git_status` |
| Code discovery | `search_code`, `get_file_contents` | `forge_filesystem_read`, `forge_filesystem_grep` |
| History comparison | `get_commit`, `list_commits` | `forge_git_log`, `forge_git_diff` |
| PR discovery | `search_pull_requests`, `pull_request_read` | `forge_github_search` |
| Efficient diff | `pull_request_read(method=get_files)` → patch | — |
| CI diagnosis | `list_commits` → workflow runs | `forge_log_tail` |
| Issue intelligence | `search_issues`, `issue_read` | — |
| Build evidence | `get_commit` → status/check runs | — |

**Mutation lane** (requires change control): `create_branch`, `create_or_update_file`, `create_pull_request`, `create_issue`, `pull_request_review_write`, `merge_pull_request`, tag creation.

**Default mutation pattern:**
```text
worktree → bounded branch → path-specific staging → tests → commit
→ draft PR → independent review → required checks
→ human/kernel authority → merge → post-merge verification
```

No agent should author, approve, and merge the same consequential change.

---

## Registry Repair Note

This skill replaces several overlapping GitHub micro-skills. The registry must:
1. Generate from active skill directories only — never resolve a retired path as active.
2. `github-runbook` (in `_retired/ARCHIVE-github-runbook/`) must be removed from active registry.
3. `FORGE-pr-governance` dependency on `github-runbook` must be updated to `FORGE-repo-intelligence`.
4. Version drift (ci-diagnose 1.0.0→1.1.0, issue-triage 1.0.0→1.1.0, pr-review 1.0.0→1.1.0) must be resolved in registry.

---

*DITEMPA BUKAN DIBERI — Forged, Not Given.*
