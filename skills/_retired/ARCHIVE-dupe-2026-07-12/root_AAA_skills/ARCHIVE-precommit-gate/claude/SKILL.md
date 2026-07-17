---
id: precommit-gate
name: Precommit Gate
version: 1.0.0
description: Pre-commit ritual running lint, type-check, tests, constitutional surface
  scan, and diff review.
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
  skills: []
  servers: []
  tools: []
examples:
- Before every `git commit` in any federation organ repo
- After a non-trivial feature lands, before opening a PR
- Before merging a branch that touched constitutional or CI files
tests:
- Python organ with lint failure aborts before tests run
- Node organ with type error aborts before test execution
- F1-surface hit in the diff routes to 888 HOLD via f1-gate
- Diff >500 lines suggests smaller commits
version_lock:
  schema_version: '1'
  artifact_hash: pending
orthogonal_tags:
  trinitarian:
  - ΦΙ
  functional:
  - Governance
  - Audit
  layer: CODING/FI
  autonomy_tier: T1
floor_scope:
- F1
- F2
- F9
- F10
- F11
- F12
---

# Precommit Gate

## Overview

The "always run this before commit" ritual for every federation organ repo. It mirrors the commitment to reversibility and verifiability by running lint, type-check, tests, a constitutional surface scan, and a diff review before any commit is finalized. Fail-fast ordering stops at the first problem so the user gets one clear reason, not a wall of noise.

## arifOS-ACT Embedding

Before using this skill on any mutating, irreversible, or high-blast-radius task:
1. **ART** — Attune (what is the real task?), Recognize (what class of power?), Test (fit · authority · evidence · blast · reversible).
2. **Kernel** — Route to arifOS for F1–F13 judgment if action class is Maker/Messenger/Mutator/Destroyer/Sovereign.
3. **ACT** — Apply narrow, Constrain scope, Trace witness, STOP before corruption.
4. **Receipt** — Leave evidence of what changed, why, and under whose authority.

## When to Use

- Before every `git commit` in any organ repo.
- Before opening a pull request.
- After a non-trivial feature lands, before it is declared done.
- When the changed files include CI, governance, or constitutional surface files.

## When NOT to Use

- **Do not use as a substitute for full pre-merge CI.** This is a local gate, not the federation merge pipeline.
- **Do not bypass the gate on "trivial" changes.** One-line changes can still break tests or leak secrets.
- **Do not auto-commit.** Always wait for explicit user approval after the review.
- If secrets, sovereignty-affecting files, or irreversible operations are present, escalate to arifOS 888_JUDGE before committing.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| organ repo path | yes | Absolute path to the organ repo, e.g. `/root/arifOS` |
| diff against HEAD | yes | Output of `git diff --stat HEAD` and the full diff |
| lint/type/test results | yes | Results from the per-organ check sequence |
| F1 surface scan result | yes | Whether the diff touched F1-relevant surfaces |
| user decision | yes | Explicit `commit` or `abort` |

## Procedure

### Step 1: Scope the Change

Run `git -C /root/<organ> diff --stat HEAD` to understand the blast radius. If the diff exceeds **500 lines**, suggest breaking it into smaller, coherent commits.

### Step 2: Run Per-Organ Checks

Run the checks in order for the organ type. Abort on the first failure and surface the first failing line.

**Python organs** (`arifOS`, `GEOX`, `WEALTH`, `WELL`):
1. `ruff check .`
2. `mypy <configured package>` (where the organ's config defines it)
3. `pytest -q`

**Node organs** (`A-FORGE`, `AAA`, `APEX`):
1. `npm run lint`
2. `npm test`
3. `tsc --noEmit` (for `A-FORGE` and `AAA` only)

Use the organ's pinned tool versions from `pyproject.toml` / `package.json`. Do not rely on globally installed tools that may differ.

### Step 3: F1 Surface Scan

Scan the diff for F1-relevant surfaces (secrets, credentials, trust boundaries, authorization code, VAULT999 lineage). If anything matches, **stop and route to `f1-gate` / arifOS 888_JUDGE** rather than proceeding.

### Step 4: Show Summary and Wait

Present the user with:
- Diff stat and line count
- Results of each check (pass / fail)
- Any F1-surface hits
- Recommendation: `commit` or `abort`

Wait for explicit user instruction. Do not commit automatically.

### Step 5: Commit or Abort

- **All checks pass + user says `commit`** → stage and commit.
- **Any check fails** → abort, fix, and re-run the gate.
- **F1 surface hit** → 888 HOLD; do not commit.

## Allowed Tools

| Tool | Purpose |
|------|---------|
| `Bash` | Run git, lint, type-check, and test commands |
| `Read` | Inspect diffs, tool configs, and failing output |
| `Grep` | Search the diff for F1-surface patterns |

## Forbidden Actions

- **NEVER** commit without explicit user approval.
- **NEVER** ignore a failing check and commit anyway.
- **NEVER** bypass the F1 surface scan.
- **NEVER** use tool versions that differ from the organ's pinned versions.
- **NEVER** auto-stage files the user did not explicitly include.
- Escalate to **arifOS 888_JUDGE** if secrets, sovereignty files, or irreversible actions are detected.

## Output Format

```
## Skill Result: precommit-gate

### Summary
One-paragraph summary of what was checked and whether the gate passed.

### Evidence
- Organ: <repo>
- Diff stat: <stat>
- Lint: <pass/fail + first failing line if fail>
- Type-check: <pass/fail + first failing line if fail>
- Tests: <pass/fail + first failing line if fail>
- F1 surface scan: <clean/hit + details>

### Recommendations
- commit / abort / fix then re-run

### Escalations
- None / <list>
```

## Escalation Path

| Condition | Escalate To | Method |
|-----------|-------------|--------|
| F1 surface hit | `f1-gate` + arifOS 888_JUDGE | A2A / MCP verdict_request |
| Secrets detected | security.agent + arifOS 888_JUDGE | A2A message |
| Constitutional files affected | arifOS 888_JUDGE | A2A verdict_request |
| Irreversible action needed | Arif (F13 SOVEREIGN) | 888 HOLD |

---

*Skill imported from `/root/.claude/skills/precommit-REVIEW_MD.md` — AAA Skill Library*
