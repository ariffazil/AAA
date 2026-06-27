---
id: github-ci-diagnose
name: GitHub CI Diagnose
version: "1.0.0"
status: DEPRECATED
deprecated_by: github-operations
redirect_to: github-operations §3 (ci-diagnose mode)
owner: AAA
risk_tier: medium
knowledge_basis:
  physics: false
  math: false
  language: true
host_compatibility:
  - claude-code
  - codex
  - opencode
replaced_by:
  skill: github-operations
  section: "§3 CI DIAGNOSE"
  mode: ci-diagnose
  effective_date: "2026-06-26"
  reason: "Unified into single github-operations skill covering issue + PR + CI"
---

# ⚠️ DEPRECATED — Use `github-operations` §3 Instead

> **This skill is deprecated.** Load `github-operations` instead and specify `mode="ci-diagnose"`.
> This file is retained for reference only and will be removed in a future version.

**Old usage:**
```
skill_load(github-ci-diagnose, repo=..., workflow_name=..., run_id=...)
```

**New usage:**
```
skill_load(github-operations, mode="ci-diagnose", repo=..., workflow_name=..., run_id=...)
```

---

# GitHub CI Diagnose (DEPRECATED — see github-operations §3)

## Overview

CI failures are symptoms, not diseases. This skill treats the log as a patient:
listen to it, classify the symptom, name the disease, prescribe a fix — but do
not perform surgery without consent.

## When to Use

- Red X on any `ariffazil/*` repo CI
- Build failure, test failure, lint failure, secret scan failure
- Workflow that passed yesterday but fails today (potential flake or dependency drift)

## When NOT to Use

- Do NOT use if failure is in a fork or external repo — scope is federation only
- Do NOT use if failure is a deliberate security gate blocking a known-bad PR — that is the gate working correctly
- Do NOT use if you already know the fix and just want to apply it — this skill is for diagnosis, not patching

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| repo | yes | Owner/repo name (e.g., ariffazil/AAA) |
| workflow_name | yes | Name of failing workflow |
| run_id | yes | GitHub Actions run ID |
| branch | no | Branch the run executed on |

## Procedure

### Step 1: Fetch & Parse Log

Retrieve the full Actions log. Look for these structural markers:

- `Error:` or `FAILED` — explicit failure line
- `npm ERR!` / `pip FAILED` / `pytest FAILED` — dependency or test break
- `secrets found` / `detect-secrets` — secret scan gate
- `timeout` / `cancelled` — infrastructure or infinite loop
- `checksum mismatch` / `lockfile out of date` — dependency drift

### Step 2: Classify Failure Mode

Assign exactly one primary cause:

| Class | Pattern | Typical Fix |
|-------|---------|-------------|
| `code-regression` | Test fails after code change | Fix code, not CI |
| `dependency-drift` | Lockfile mismatch, version conflict | Update lockfile, pin versions |
| `infra-flake` | Timeout, network error, runner crash | Re-run (with approval) |
| `lint-format` | Ruff, eslint, prettier violation | Run formatter, fix style |
| `secret-gate` | detect-secrets, TruffleHog alert | Rotate secret, clean history |
| `config-error` | Invalid YAML, missing env var, wrong path | Fix workflow config |
| `cross-repo-break` | Dependent repo changed interface | Coordinate multi-repo fix |

### Step 3: Root Cause Analysis

Ask five whys:
1. What failed? (the symptom)
2. What command produced the failure? (the trigger)
3. What changed since the last green run? (the delta)
4. Is this reproducible or a flake? (the confidence)
5. What is the minimal fix? (the prescription)

Document the chain in the diagnostic report.

### Step 4: Propose Fix

Draft a fix proposal that is:
- **Reversible** (can be reverted with `git revert`)
- **Bounded** (touches only the failing component)
- **Tested** (includes how to verify the fix locally)

Do NOT:
- Edit `.github/workflows/*.yml` directly
- Re-run CI without Arif approval
- Dismiss a security scan failure
- Suggest `npm audit fix --force` or equivalent blind upgrades

### Step 5: Report & Escalation

Output a diagnostic report (see format below).

Escalation rules:
- `secret-gate` → escalate to `secret-safety-scan` skill + alert Arif
- `cross-repo-break` → escalate to `parallel-authority-detection` skill
- `config-error` touching constitutional workflow → escalate to 888_JUDGE
- All others → present fix proposal, await Arif ack

## Forbidden Actions

- **NEVER** re-run CI without Arif approval (masks flakes, wastes compute)
- **NEVER** edit `.github/workflows/` without 888_JUDGE
- **NEVER** dismiss a security scan failure as "false positive" without evidence
- **NEVER** propose `--force` upgrades or destructive dependency resolution
- **NEVER** commit directly to main to "fix CI quickly"

## Output Format

```markdown
## CI Diagnostic Report

- **Repo:** owner/repo
- **Workflow:** name
- **Run ID:** id
- **Branch:** branch
- **Failure Class:** <class>
- **Confidence:** <high | medium | low>
- **Root Cause:** <concise explanation>
- **Last Green Run:** <run-id or unknown>
- **Delta Since Green:** <what changed>
- **Proposed Fix:** <reversible, bounded fix>
- **Local Verification:** <command to reproduce/fix locally>
- **Escalation:** <none | secret-safety-scan | parallel-authority-detection | 888_JUDGE>
```
