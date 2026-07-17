---
id: pr-governance
name: GitHub PR Governance
version: 1.0.0
description: PRs are constitutional hearings. Intent becomes law.
owner: AAA
risk_tier: low
glyph: "🜅"
position: 5 of 12 in the GitHub Canon
canonical_siblings:
  - github-pr-review
  - pr-review-governance
  - github-ci-diagnose
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
    - forge_github_create_pull_request
    - forge_github_get_file
    - forge_git_diff
version_lock:
  schema_version: '1'
  artifact_hash: 63bef5e6565ad00c
floor_scope:
  - F1
  - F2
  - F4
  - F11
  - F13
autonomy_tier: T1
---

# 🜅 5. GitHub PR Governance

> *"PRs are constitutional hearings. Intent becomes law."*
> — AAA GitHub Canon, position 5 of 12

## Purpose

Open, review, and merge PRs that turn governed intent into canon.

## When to Use

- Any PR touching >1 file
- Any PR modifying contracts, schemas, registries
- Any PR marked high/critical risk
- Any PR from an external contributor

## When NOT to Use

- Do NOT use for docs-only typo fixes if low-risk and self-contained (commit to a docs branch, fast-track)
- Do NOT use to merge your own PR (F1 AMANAH — self-seal forbidden)
- Do NOT use to dismiss security findings (escalate to secret-safety-scan + 888_JUDGE)

## Procedure

1. Open PR: `Closes #<issue-n>`, body = what + why + risks + fallback + checklist
2. Run pre-merge gate: tests pass, lint clean, secrets clean, schema updated
3. Request reviewers per risk tier (peer / peer+architect / 2 peers+auditor / all+Arif)
4. Respond to review comments — request changes is remand, not veto
5. Squash and merge after green CI + required signers + 888_JUDGE seal (if high/critical)

## Allowed Tools

| Tool | Purpose |
|---|---|
| `forge_github_pr` | pr-governance operation |
| `forge_github_create_pull_request` | pr-governance operation |
| `forge_github_get_file` | pr-governance operation |
| `forge_git_diff` | pr-governance operation |

## Forbidden Actions

- NEVER self-approve your own PR
- NEVER merge to main without branch protection + required signers
- NEVER dismiss security findings
- NEVER force-push a PR branch after review has started
- NEVER create cross-repo PRs without architectural judgment

## Output

PR URL + linked issue + risk tier + required signers + CI status + verdict (approve/changes/block)

## Sibling Skills

- `github-pr-review`
- `pr-review-governance`
- `github-ci-diagnose`

---

*Position 5 of 12 in the AAA GitHub Canon. Sovereign ruling 2026-06-24.*
*Consolidates and supersedes prior GitHub-related skills in the federation.*
*License: AGPL-3.0 · Sovereign: Arif bin Fazil*
*DITEMPA BUKAN DIBERI*
