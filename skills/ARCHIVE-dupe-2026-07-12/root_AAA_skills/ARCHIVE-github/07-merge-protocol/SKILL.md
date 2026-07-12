---
id: merge-protocol
name: GitHub Merge Protocol
version: 1.0.0
description: Merging is law update. Only after CI + review + signers.
owner: AAA
risk_tier: low
glyph: "🜇"
position: 7 of 12 in the GitHub Canon
canonical_siblings:
  - pr-governance
  - github-pr-review
  - ci-obedience
knowledge_basis:
  language: true
  math: false
  physics: false
host_compatibility:
  - claude-code
  - codex
  - opencode
  - kimi-code
  - grok-build
  - copilot-cli
dependencies:
  skills: []
  servers:
    - a-forge
  tools:
    - forge_github_pr
    - forge_git_log
    - forge_git_status
version_lock:
  schema_version: '1'
  artifact_hash: 973f8b127c3e0d3f
floor_scope:
  - F1
  - F2
  - F4
  - F11
  - F13
autonomy_tier: T1
---

# 🜇 7. GitHub Merge Protocol

> *"Merging is law update. Only after CI + review + signers."*
> — AAA GitHub Canon, position 7 of 12

## Purpose

Merge PRs cleanly. Avoid merge conflicts. Maintain linear history. Keep canon clean.

## When to Use

- PR has green CI + required reviewers signed + no unresolved conversations
- All required checks pass (security, tests, lint, schema)
- Risk-appropriate 888_JUDGE seal obtained (high/critical)

## When NOT to Use

- Do NOT use to merge a PR with unresolved review comments
- Do NOT use to merge if CI is red or required signers missing
- Do NOT use to merge constitutional file changes without Arif explicit ack

## Procedure

1. Verify: PR is green + reviews approved + branch up to date with main + no conflicts
2. Choose merge strategy: squash (default for feature branches) / merge commit (preserve history) / rebase (linear history, requires 888)
3. Squash message: aggregates all commits, references Issue + PR
4. Post-merge: delete branch (remote + local), verify deploy if applicable
5. Verify main: pull, check HEAD sha, verify deployment pipeline triggered

## Allowed Tools

| Tool | Purpose |
|---|---|
| `forge_github_pr` | merge-protocol operation |
| `forge_git_log` | merge-protocol operation |
| `forge_git_status` | merge-protocol operation |

## Forbidden Actions

- NEVER merge a PR with unresolved conversations
- NEVER merge your own PR to main (F13 SOVEREIGN)
- NEVER force-push to main under any circumstance
- NEVER delete main even after squash
- NEVER merge without verifying branch protection passed

## Output

Merge commit sha + merged-by + linked issue closed + branch deleted + deploy status

## Sibling Skills

- `pr-governance`
- `github-pr-review`
- `ci-obedience`

---

*Position 7 of 12 in the AAA GitHub Canon. Sovereign ruling 2026-06-24.*
*Consolidates and supersedes prior GitHub-related skills in the federation.*
*License: AGPL-3.0 · Sovereign: Arif bin Fazil*
*DITEMPA BUKAN DIBERI*
