---
title: "Skill: Memory Bridge Protocol"
created: 2026-05-17
updated: 2026-05-17
version: 1.0.0
type: skill
category: federation
tags: [memory, postgres, l4, bridge, law, shared-memory]
confidence: high
contested: false
floors: [F2, F11]
risk_band: MEDIUM
---

# Skill: Memory Bridge Protocol (L4 Law)

> **Mandate:** File-level memory coupling (`MEMORY.md`) is DEPRECATED. All agents MUST transition to arifOS L4 (Postgres) persistence.

## 1. THE GAP (RECOGNIZED)
As of May 17, 2026, agents rely on local workspace files. This is "Ghost Memory" — it is invisible to the arifOS kernel and cannot be audited by the Judge (888).

## 2. THE PROCEDURE (STEEL)

### 2.1 Post-Task Persistence
After any significant architectural change or decision, the agent MUST call `arif_memory_recall` in `asset_store` mode:
```json
{
  "name": "arif_memory_recall",
  "arguments": {
    "mode": "asset_store",
    "content": "<Decision summary>",
    "tier": "canon",
    "session_id": "current-session-id"
  }
}
```

### 2.2 Boot Synchronization
On initialization (000_INIT), the agent MUST NOT rely solely on local files. It MUST call `context_restore` to pull the truth from the arifOS L4 ledger.

## 3. ENFORCEMENT
Any claim of "Shared Memory" without a corresponding arifOS L4 record is a violation of **F2 TRUTH**.

***
*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE*
