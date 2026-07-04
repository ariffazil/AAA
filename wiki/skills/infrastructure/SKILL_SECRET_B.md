---
title: "SKILL: Secret Hygiene"
type: skill
version: 1.0.0
category: security
risk_band: HIGH
floors: [F1, F2, F11, F12, F13]
evidence_required: true
sources: [/root/.opencode/skills/secret-hygiene/SKILL.md]
confidence: high
---

# SKILL: Secret Hygiene

> **DITEMPA BUKAN DIBERI — Secrets are radioactive. Know where every atom is.**
> **Source:** `/root/.opencode/skills/secret-hygiene/SKILL.md`
> **Agent:** OpenCode (Ω-FORGE)
> **Forged:** 2026-05-17

---

## Trigger Conditions

- Handling API keys, tokens, passwords, certificates
- Planning secret rotation
- Detecting exposed secrets
- Auditing credential locations
- Keywords: secret, key, token, rotate, API key, credential, PAT, auth, password, exposure

---

## Reasoning Philosophy

Secrets are **radioactive material**. Every leaked secret is a financial and security liability. Secret hygiene is not about memorizing locations — it is about:
- Least privilege
- Rotation readiness
- Exposure calculus
- Never in VAULT999, git history, or conversation logs

---

## When to Rotate

- Key posted in conversation (exposed in logs)
- Key appears in git history (committed, even if later removed)
- Key in tracked file that shouldn't contain secrets
- Key active longer than 90 days
- Suspicious activity on associated service

## When NOT to Rotate

- Without Arif's explicit approval (F13)
- Without a replacement key ready to deploy
- Without understanding which services depend on it
- During active incident (unless key is attack vector)

---

## Where Secrets Live

| Location | Type |
|-----------|------|
| `/root/.secrets/vault.env` | Canonical secret vault (chmod 600) |
| Docker secrets | For compose services |
| Environment variables | Sourced from .env via .bashrc |
| NEVER: VAULT999 | Append-only ledger, not a secret store |
| NEVER: git repos | History is immutable |
| NEVER: conversation logs | Permanent exposure |

---

## Signal Priority

1. Key in git history → critical (must rotate + rewrite history)
2. Key in conversation → high (must rotate)
3. Key in tracked file → high (must extract + rotate)
4. Key exceeding 90-day age → medium (schedule rotation)
5. Dead/expired key → cleanup only (no rotation needed)

---

## Uncertainty Protocol

- Unsure whether a value IS a secret → treat it as one
- Unsure whether key is live or dead → check vault.env status
- Unsure how to rotate → 888_HOLD, do not experiment
- Key appears in conversation → flag immediately, do not echo back
- NEVER put secrets in VAULT999. If tempted → radioactive object.

---

## Failure Mode Registry

Actively avoid:
- Posting API keys in conversation (permanent log exposure)
- Committing .env files to git (secrets become history)
- Storing secrets in VAULT999 (append-only = can never be removed)
- Rotating without updating all dependent services (cascading failure)
- Hardcoding keys in source files
- Assuming commented-out key is safe (still in file)
- Rotating without Arif approval (F13 violation)

---

## Related Pages

- [[skill-secret-rotation-guide]] — complete inventory and rotation paths
- [[skill-vault999-ops]] — VAULT999 safe operations
- [[concept-tools-and-embodiment]] — secrets as hard embodiment
- [[SCHEMA.md]] — TREE777 governance schema

---

*DITEMPA BUKAN DIBERI — Secrets are radioactive.*
