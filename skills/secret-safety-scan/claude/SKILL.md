---
id: secret-safety-scan
name: Secret Safety Scan
version: "1.0.0"
description: Scan a repo or workspace for exposed secrets, tokens, keys, and credentials. Produce a findings report with remediation steps.
owner: AAA
risk_tier: high
knowledge_basis:
  physics: false
  math: false
  language: true
host_compatibility:
  - claude-code
  - codex
  - opencode
dependencies:
  skills: []
  servers: []
  tools:
    - grep
    - file-read
    - git-log
examples:
  - Pre-commit secret sweep on AAA repo
tests:
  - Detect fake AWS key in test fixture
  - Ignore secrets in `.env.example` templates
version_lock:
  schema_version: "1"
  artifact_hash: pending
---

# Secret Safety Scan

## Overview

Secrets exposed in repos are irreversible once pushed. This skill scans for patterns that look like credentials and flags them before they leak.

## When to Use

- Before any `git commit`
- Before any `git push`
- After importing external code
- Quarterly security sweep

## Patterns to Detect

- AWS: `AKIA[0-9A-Z]{16}`
- GitHub: `ghp_[a-zA-Z0-9]{36}`
- OpenAI: `sk-[a-zA-Z0-9]{48}`
- Generic: `password=`, `token=`, `secret=`, `api_key=`
- Private keys: `-----BEGIN <ALGO> PRIVATE KEY-----`
- `.env` files with real values (not `.env.example`)

## Procedure

### Step 1: File Scan

Search for patterns in all text files. Exclude:
- `node_modules/`, `__pycache__/`, `.git/`
- `.env.example`, `.env.template`
- Test fixtures with fake values (documented)

### Step 2: Git History Scan

Check `git log -p` for secrets in history. Even if removed from current HEAD, they may exist in history.

### Step 3: Evaluate Findings

- False positive → document why
- Real secret → immediate escalation
- Template/example → verify it's fake

## Forbidden Actions

- **NEVER** commit secrets to fix them — use `git filter-repo` or BFG
- **NEVER** post findings in public channels
- **NEVER** dismiss findings without verification

## Escalation Path

| Condition | Escalate To |
|-----------|-------------|
| Live secret found | Arif + security.agent — IMMEDIATE |
| Historical secret | ops.agent — rotation needed |
| False positive pattern | AAA agent — update scan rules |

---

*Skill version 1.0.0 — AAA Skill Library*
