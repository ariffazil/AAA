---
id: push-protocol
name: GitHub Push Protocol
version: 1.0.0
description: Push is publishing intent. Only reviewed branches. Never to main.
owner: AAA
risk_tier: low
glyph: "🜉"
position: 9 of 12 in the GitHub Canon
canonical_siblings:
  - pr-governance
  - ci-obedience
  - github-runbook
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
    - forge_git_status
    - forge_git_log
    - forge_github_create_pull_request
version_lock:
  schema_version: '1'
  artifact_hash: 23e13d175ca82ce4
floor_scope:
  - F1
  - F2
  - F4
  - F11
  - F13
autonomy_tier: T1
---

# 🜉 9. GitHub Push Protocol

> *"Push is publishing intent. Only reviewed branches. Never to main."*
> — AAA GitHub Canon, position 9 of 12

## Purpose

Publish your branch to remote only after local validation and review-readiness.

## When to Use

- After local tests + lint pass
- When ready for CI to run on the PR
- When sharing work-in-progress with reviewers (draft PR)

## When NOT to Use

- Do NOT use to push to main directly (F13 SOVEREIGN + branch protection)
- Do NOT use to push broken code (CI will fail, you waste compute and trust)
- Do NOT use to push secrets, .env files, or unredacted credentials

## Procedure

1. Pre-push: `git status` clean, `git log --oneline -5` reviewed, tests pass
2. Push: `git push origin <branch>` (first push: `git push -u origin <branch>`)
3. Open or update PR on the pushed branch
4. Watch CI: GitHub Actions tab, fix any failures via new commits
5. Never `git push --force` to a shared branch — use `git push --force-with-lease` only if absolutely necessary and never on main

## Allowed Tools

| Tool | Purpose |
|---|---|
| `forge_git_status` | push-protocol operation |
| `forge_git_log` | push-protocol operation |
| `forge_github_create_pull_request` | push-protocol operation |

## Forbidden Actions

- NEVER push to main directly (F13 SOVEREIGN)
- NEVER push secrets or credentials
- NEVER force-push during active PR review
- NEVER push with uncommitted changes (commit first or they don't go)
- NEVER push without local test pass

## Output

Remote branch URL + CI run started + PR link (if opened/updated)

## Sibling Skills

- `pr-governance`
- `ci-obedience`
- `github-runbook`

---

*Position 9 of 12 in the AAA GitHub Canon. Sovereign ruling 2026-06-24.*
*Consolidates and supersedes prior GitHub-related skills in the federation.*
*License: AGPL-3.0 · Sovereign: Arif bin Fazil*
*DITEMPA BUKAN DIBERI*
