# Flow Gaps & Bypass Analysis (Phase D)
**Document:** `FLOW_GAPS.md`  
**Standard:** QQQ Protocol · Fail-Closed · No Shadow Paths  
**Date:** 2026-09-14T09:51:30+08:00  
**Authority:** ARIF (F13 Sovereign Principal) · `ARIFOS::ENTROPY_REDUCTION::REALITY_GRAPH::v1`

---

## 1. Identified Flow Gaps

| Flow Gap ID | Type | Description | Observed Reality | Risk Level |
|---|---|---|---|---|
| **GAP-FLOW-01** | **BYPASS / SHADOW** | Hermes Memory Storage Bypass | Hermes stores conversational memory directly in Qdrant collection `mem0` (14,399 points), completely bypassing `sroAdmissibility.ts` and the canonical `arifos_memory` collection (40 points). | **HIGH** |
| **GAP-FLOW-02** | **DEAD_END** | FLAME Low-Effort Dead End | Requests classified as `low` effort in `/root/.config/federation-models.json` resolve to `flame-free`, pointing to decommissioned FLAME daemon. | **MEDIUM** |
| **GAP-FLOW-03** | **DEAD_END** | Single-Disk Backup Dead End | `direct-backup.sh` dumps restic snapshots to `/root/backups/restic-repo` on `/dev/sda1`. If disk corrupts, live system and backups fail simultaneously. `/root/.hermes` has zero off-box path. | **HIGH** |
| **GAP-FLOW-04** | **BYPASS** | Direct Root Mutation Bypass | Before Path-5, agents mutated `/root/<REPO>` directly. Concurrent runs resulted in Git collisions (e.g. Kimi vs Antigravity file lock races). | **RESOLVED by Path-5** |
| **GAP-FLOW-05** | **LOOP / RETRY** | LiteLLM Exhausted Provider Fallback Loop | `litellm-config.yaml` traverses 4 dead rungs (Gemini 429, Mistral 402, Z.AI 429, Qwen 429) sequentially on every request before hitting working providers, burning seconds of latency. | **MEDIUM** |
| **GAP-FLOW-06** | **SHADOW EXPOSURE**| Hermes Subagent Log Permissions | 144 delegation task logs generated at mode `644` in `/root/.hermes/cache/delegation/`, exposing prompt context to any process on host. | **MEDIUM** |
