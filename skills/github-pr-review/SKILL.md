---
id: github-pr-review
name: GitHub PR Governance Review
version: 1.1.0
description: Governed checklist for reviewing GitHub pull requests in the arifOS federation.
  Ensures PRs meet constitutional, structural, and safety standards before merge.
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
dependencies: {}
  servers:
  - a-forge
  tools:
  - forge_github_pr
  - forge_filesystem_read  # forge_github_get_file not in /mcp/aforge/
  - forge_github_search  # forge_github_search_code not in /mcp/aforge/ — use forge_github_search
  - forge_git_diff
  - forge_git_log
  - forge_git_status
examples:
- Review a cross-repo architectural PR before merge
- Pre-merge gate on PR touching constitutional files (F1/F13 cross-check)
tests:
- Detect constitutional file changes in non-arifOS repos
- Verify REPO= trailer in commit messages
- Refuse to auto-approve without required reviewer per pr-review-governance risk tier
version_lock:
  schema_version: '1'
  artifact_hash: 61fe928f10e8de80
orthogonal_tags:
  trinitarian:
  - ΦΙ
  functional:
  - Governance
  layer: CODING/FI
  autonomy_tier: T2
floor_scope:
- F1
- F2
- F4
- F9
- F11
- F13
canonical_siblings:
- pr-review-governance    # risk-tier + reviewer routing
- github-runbook          # local git/gh inspection
- github-ci-diagnose      # workflow failure analysis
- github-issue-triage     # pre-PR context
- github-issues           # OpenCode-scope: monitoring shell
---

# GitHub PR Governance Review

## Overview

Pull requests are the constitutional boundary of a federation repo. A PR is the
unit at which code, governance, and human judgment meet. This skill defines the
**per-PR checklist** an agent must run before recommending merge or approval.

Scope: structural review of the diff itself, not the high-level risk-tier and
reviewer-routing rules (those live in `pr-review-governance`). This skill is the
**checklist**, that skill is the **policy layer**.

Companion skills:
- `github-runbook` — local git/gh inspection (read-only first)
- `github-ci-diagnose` — if CI is red on the PR branch
- `github-issue-triage` — if the PR resolves an open issue
- `pr-review-governance` — risk tier + reviewer routing (delegate first if risk ≥ high)

## When to Use

- Any PR touching >1 file
- Any PR modifying contracts, schemas, or registries
- Any PR from an external contributor
- Any PR marked as "high risk" by the author

## When NOT to Use

- **Do NOT use on cross-repo PRs without first invoking `pr-review-governance`** to determine risk tier.
- **Do NOT use as a substitute for CI** — CI runs first, this skill reads CI artifacts second.
- **Do NOT use to approve your own PR** — F1 AMANAH + F13 SOVEREIGN prohibit self-seal.
- **Do NOT use to dismiss a security finding** — escalate to `secret-safety-scan` + 888_JUDGE.
- **Do NOT use to merge to main directly** — merge is F13 SOVEREIGN unless branch protection already enforces the policy.

## arifOS-ACT Embedding

Before using this skill on any mutating, irreversible, or high-blast-radius task:
1. **ART** — Attune (what is the real task?), Recognize (what class of power?), Test (fit · authority · evidence · blast · reversible).
2. **Kernel** — Route to arifOS for F1–F13 judgment if action class is Maker/Messenger/Mutator/Destroyer/Sovereign.
3. **ACT** — Apply narrow, Constrain scope, Trace witness, STOP before corruption.
4. **Receipt** — Leave evidence of what changed, why, and under whose authority.
