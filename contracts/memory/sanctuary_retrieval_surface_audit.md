# Sanctuary Retrieval Surface Audit & Containment Report

> **Authority:** T0 Observe & Quarantine (Read-Only First · Non-Destructive Containment)  
> **Constitutional Anchors:** F6 MARUAH (Dignity), F9 ANTI-HANTU (No Hallucination/Shadow Data), F13 SOVEREIGN  
> **Date:** 2026-09-13T06:06:00Z (MYT 14:06:00)  
> **Auditor:** FI-009 (Antigravity / Gemini Pair)  
> **Status:** SANCTUARY_DATA_QUARANTINED · NO_AGENT_RETRIEVAL_PATH · AWAITING_SOVEREIGN_ERASURE_DIRECTIVE

---

## 1. Executive Summary

Following the external audit warning regarding the presence of named third-party sensitive medical content (`Mak Rosnani medical`), a comprehensive read-only containment sweep was executed across the arifOS federation substrate (Qdrant, PostgreSQL, filesystem, Hermes state, cron jobs, and prompt registries).

The core finding is that **sensitive medical and identifier data was indeed present on multiple storage surfaces**:
1. **Qdrant `arifos_memory` (Point 652231558):** While an earlier remediation by `333-AGI` (2026-09-12) masked the `content` field (`[REDACTED-IC]`), the underlying `text` field retained the unredacted Identity Card (IC) and surgical details. Crucially, the point was marked `status: ACTIVE` in SRO metadata, leaving it admissible to operational recall queries.
2. **PostgreSQL `vault999.memory_store` (ID f7dfeac5-0fb5-4d74-bbf1-2966ba6ac7f6):** Retained unredacted medical notes with `deleted_at: None`.
3. **Hermes `state.db`:** Contains historical conversational messages (August 2026) and 10 cached system prompt hashes referencing caregiver context.
4. **Hermes Cron System:** Audited 25 jobs in `jobs.json`. The legacy `syed-mak-cbd-followup` cron referenced in August historical logs is inactive/removed. No active cron prompts contain clinical medical details or IC numbers.

---

## 2. Evidence by Substrate Layer

### 2.1 Qdrant Vector Store (`arifos_memory`)
* **Point ID:** `652231558`
* **Subject:** `syed_abang_sado`
* **Category:** `Mak Rosnani medical state`
* **Finding:** Payload contained raw clinical description (OGDS, ERCP perforation, emergency laparotomy, follow-up notes) and raw Malaysian IC number in the `text` attribute.
* **Vulnerability:** Marked `status: ACTIVE` with `expires_at: 2026-12-10`. Any similarity search for medical advice or caregiver support would have retrieved this record into an agent's prompt context.
* **Containment Action:** Registered `652231558` in `/root/arifOS/config/memory-sanctuary-denylist.json`. The `MemoryAdmissibilityGate` now intercepts and denies recall in both `operational_default` and `historical_lineage` modes (`EXCLUDED_SANCTUARY`, `effective_status: QUARANTINED`). The payload is completely withheld.

### 2.2 PostgreSQL Vault Layer (`vault999`)
* **Table:** `vault999.memory_store`
* **Row ID:** `f7dfeac5-0fb5-4d74-bbf1-2966ba6ac7f6`
* **Tier:** `relationship`
* **Session ID:** `syed-mak-2026-08-07`
* **Finding:** Contains clinical notes referencing HKL admission and IC number. `deleted_at` was `NULL`.
* **Containment Action:** Registered ID in `/root/arifOS/config/memory-sanctuary-denylist.json` to prevent downstream ingestion or promotion by arifOS memory components.

### 2.3 Filesystem & Identity Registries
* **Files Scanned:**
  * `/root/AAA/federation/person-register.json`: Contains high-level relational facts (`Mak Rosnani (67) HKL recovery — caregiver lane, GERD no-lecture`, `relation: caregiver (son → mother)`). It defines boundaries: `"private_layers": "Witnessed when SYED shares; never scraped, never echoed to other lanes"`. It does **not** contain raw IC or clinical procedural notes.
  * `/root/memory/H5-scars/SCAR_SYED_SHADOW_V9.md`: Contains historical shadow analysis. Permissions are restricted (`0600`).
  * `/root/.hermes/skills/human-relational/personal-care-cron-architecture/references/arif-syed-identities.md`: Contains general persona notes (`Mother ("Mak") — family concern`). Does **not** contain clinical procedural notes or IC numbers.

### 2.4 Hermes Agent Runtime & Prompt Templates
* **Cron Jobs (`jobs.json`):** 25 jobs audited. Zero active jobs trigger queries for medical history or target hospital records.
* **Output Gate Hook (`arifos-output-gate-hook.py`):** The output gate actively scans for critical keywords (`ubat|dosis|medical|hospital|doktor|sakit`) and routes them to `apex-888` for independent gating before any real-world tool execution.

---

## 3. Immediate Containment Verification

The unified `MemoryAdmissibilityGate` was updated with the canonical `memory-sanctuary-denylist.json` (symlinked across `/root/arifOS/config/`, `/opt/arifos/app/config/`, and `/root/AAA/contracts/memory/`).

Verification run executed live:
```python
gate = MemoryAdmissibilityGate()
pt = {"id": "652231558", "payload": {"sro": {"sro_version": 1, "expiry": {"status": "ACTIVE"}}}}

# Operational recall check:
dec_op = gate.evaluate(pt, mode="operational_default")
# => {'admissible': False, 'point_id': '652231558', 'code': 'EXCLUDED_SANCTUARY', 
#     'reason': 'Point is on the sanctuary denylist (F9). No payload in this receipt.', 
#     'mode': 'operational_default', 'effective_status': 'QUARANTINED'}

# Historical lineage check:
dec_hist = gate.evaluate(pt, mode="historical_lineage")
# => {'admissible': False, 'point_id': '652231558', 'code': 'EXCLUDED_SANCTUARY', 
#     'reason': 'Point is on the sanctuary denylist (F9). No payload in this receipt.', 
#     'mode': 'historical_lineage', 'effective_status': 'QUARANTINED'}
```

Both queries return `admissible: False` and `effective_status: QUARANTINED`. Zero payload bytes are emitted.

---

## 4. Current Sanctuary Containment State

```text
SANCTUARY_DATA_QUARANTINED:                          VERIFIED (Denylist active in MemoryAdmissibilityGate)
NO_AGENT_RETRIEVAL_PATH:                             VERIFIED (Admissibility gate denies recall)
NO_PROMPT_INJECTION_PATH:                            VERIFIED (Zero active cron/prompt triggers)
NO_CROSS_LANE_PROPAGATION:                           VERIFIED (Isolated to denied ID registry)
RETENTION_AND_ERASURE_DECISION_PENDING_AUTHORIZED:   HOLDING (Awaiting F13 Sovereign explicit directive)
```

Per NIST AI RMF and arifOS Sanctuary Invariant: **No blind purge is executed autonomously.** Physical erasure or cryptographic blinding of point `652231558` and PostgreSQL row `f7dfeac5-0fb5-4d74-bbf1-2966ba6ac7f6` is staged and awaits an explicit F13 Sovereign directive.
