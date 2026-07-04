---
title: "Skill: SOT Parity Enforcement"
created: 2026-05-17
updated: 2026-05-17
version: 1.0.0
type: skill
category: infrastructure
tags: [env, sot, synchronization, law, manifest]
confidence: high
contested: false
floors: [F1, F11]
risk_band: HIGH
---

# Skill: SOT Parity Enforcement (Ψ Law)

> **Mandate:** The file `/root/.env.sot` is the ONLY Source of Truth. The live `.env` must be a perfect mirror.

## 1. THE SCAR (RECOGNIZED)
"Environment Drift" occurs when agents update `.env` but forget the Master Manifest. This leads to secret loss and deployment chaos.

## 2. THE PROCEDURE (STEEL)

### 2.1 The "Atomic Mirror" Rule
1. **Change:** Always modify `.env.sot` FIRST.
2. **Mirror:** Execute `cp /root/.env.sot /root/.env` immediately after.
3. **Verify:** Run `diff /root/.env /root/.env.sot`. Zero output is the only success state.

### 2.2 Automated Guard
Every `make status` or `make forge` command MUST include a parity check step.

## 3. ENFORCEMENT
Drift > 0 lines triggers a **777 METABOLIC ALERT**. No `999 SEAL` can be issued while the SOT is drifted.

***
*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE*
