---
id: ci-obedience
name: GitHub CI Obedience
version: 1.0.0
description: CI is doctrine enforcement. Never bypass.
owner: AAA
risk_tier: low
glyph: "🜆"
position: 6 of 12 in the GitHub Canon
canonical_siblings:
  - github-ci-diagnose
  - secret-safety-scan
  - parallel-authority-detection
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
    - forge_log_tail
    - forge_shell_dryrun
    - forge_github_get_file
version_lock:
  schema_version: '1'
  artifact_hash: 8d77773612b226bf
floor_scope:
  - F1
  - F2
  - F4
  - F11
  - F13
autonomy_tier: T1
---

# 🜆 6. GitHub CI Obedience

> *"CI is doctrine enforcement. Never bypass."*
> — AAA GitHub Canon, position 6 of 12

## Purpose

Write code that passes tests, lint, safety, and policy checks. Read CI failures. Fix violations.

## When to Use

- On every PR update — CI runs automatically
- When CI fails — diagnose (github-ci-diagnose) and fix
- When adding new tests or new CI gates

## When NOT to Use

- Do NOT use to re-run CI without approval (masks flakes, wastes compute)
- Do NOT use to edit .github/workflows/*.yml directly without 888_JUDGE
- Do NOT use to dismiss a security scan failure as false positive without evidence

## Procedure

1. On push: GitHub Actions runs the workflow YAML
2. Local mirror: `make test` (pytest) + `ruff check .` + `make security-audit`
3. On red: classify failure (code-regression | dependency-drift | infra-flake | lint-format | secret-gate | config-error | cross-repo-break)
4. Fix at the smallest possible blast radius — reversible, bounded, tested
5. Push fix as new commit on the PR branch — never force-push during review

## Allowed Tools

| Tool | Purpose |
|---|---|
| `forge_log_tail` | ci-obedience operation |
| `forge_shell_dryrun` | ci-obedience operation |
| `forge_github_get_file` | ci-obedience operation |

## Forbidden Actions

- NEVER commit directly to main to 'fix CI quickly'
- NEVER propose --force upgrades or destructive dependency resolution
- NEVER disable a security scan to make CI green
- NEVER edit .github/workflows/*.yml without 888_JUDGE

## Output

CI status (green/red) + failure class + root cause + minimal fix + local verification command

## Sibling Skills

- `github-ci-diagnose`
- `secret-safety-scan`
- `parallel-authority-detection`

---

*Position 6 of 12 in the AAA GitHub Canon. Sovereign ruling 2026-06-24.*
*Consolidates and supersedes prior GitHub-related skills in the federation.*
*License: AGPL-3.0 · Sovereign: Arif bin Fazil*
*DITEMPA BUKAN DIBERI*
