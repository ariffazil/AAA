---
id: secret-safety-scan
name: Secret Safety Scan
version: 1.0.1
description: Scan a repo or workspace for exposed secrets, tokens, keys, and credentials
  Produce a findings report with remediation steps.
owner: AAA
risk_tier: critical
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
  schema_version: '1'
  artifact_hash: pending
orthogonal_tags:
  trinitarian:
  - ΦΙ
  functional:
  - Governance
  - Audit
  layer: HEXAGON
  autonomy_tier: T3
floor_scope:
- F1
- F2
- F11
- F12
- F13
---

# Secret Safety Scan

## Overview

Secrets exposed in repos are irreversible once pushed. This skill scans for patterns that look like credentials and flags them before they leak.

## arifOS-ACT Embedding

Before using this skill on any mutating, irreversible, or high-blast-radius task:
1. **ART** — Attune (what is the real task?), Recognize (what class of power?), Test (fit · authority · evidence · blast · reversible).
2. **Kernel** — Route to arifOS for F1–F13 judgment if action class is Maker/Messenger/Mutator/Destroyer/Sovereign.
3. **ACT** — Apply narrow, Constrain scope, Trace witness, STOP before corruption.
4. **Receipt** — Leave evidence of what changed, why, and under whose authority.

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

## Secret Hygiene Policy

Treat secrets as radioactive material: know where every atom is at all times. They are not configuration, environment variables, or conversation material.

### When to Rotate

- Key was posted in conversation (exposed in logs)
- Key appears in git history (committed, even if later removed)
- Key is in a tracked file that should not contain secrets
- Key has been active longer than 90 days
- Suspicious activity detected on the associated service

### When NOT to Rotate

- Without Arif's explicit approval (F13)
- Without a replacement key ready to deploy
- Without understanding which services depend on the key
- During an active incident, unless the key is the attack vector

### Where Secrets Live

- `/root/.secrets/vault.env` — canonical secret vault (chmod 600)
- Docker secrets for compose services
- Environment variables sourced from `.env` via `.bashrc`
- NEVER in VAULT999, git repos, conversation logs, or code comments

### Signal Priority

1. Key in git history → critical (rotate + rewrite history)
2. Key in conversation → high (rotate)
3. Key in tracked file → high (extract + rotate)
4. Key older than 90 days → medium (schedule rotation)
5. Dead/expired key → cleanup only

### Cleanup Rituals

- Remove dead/expired keys from `vault.env` and `.env`
- Delete commented-out keys from source and configs
- Verify no dependent service before removing a live key
- Document rotation in the skill receipt, never the secret value

### Uncertainty Protocol

- If unsure whether a value is a secret, treat it as one.
- If unsure whether a key is live, check `vault.env` status.
- If unsure how to rotate, 888 HOLD — do not experiment.
- Never echo a secret back or put it in VAULT999.

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

*Skill version 1.0.1 — AAA Skill Library*
