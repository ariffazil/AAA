# Federation Orphan & Dormant Registry (Phase F)
**Document:** `ORPHAN_REGISTRY.md`  
**Standard:** QQQ Protocol · Classification Without Deletion  
**Date:** 2026-09-14T09:52:30+08:00  
**Authority:** ARIF (F13 Sovereign Principal) · `ARIFOS::ENTROPY_REDUCTION::REALITY_GRAPH::v1`

---

## 1. Subsystem Orphan Classification

| Component / Path | Type | Reason for Orphan Status | Current Classification | Action Required (Pending F13) |
|---|---|---|---|---|
| `agentgateway-shadow.service` | Systemd Unit | Binary `/root/forge_work/agw/agentgateway-linux-amd64` was deleted; process running from ghost RAM. | **ORPHAN** | `systemctl stop` and `systemctl disable` (Requires F13). |
| `apa-calendar-bridge.service` | Systemd Unit | Virtualenv `/root/venvs/composio` deleted; crashes on reboot. | **ORPHAN** | Formal disable or recreate virtualenv. |
| `apa-drive-bridge.service` | Systemd Unit | Virtualenv `/root/venvs/composio` deleted; crashes on reboot. | **ORPHAN** | Formal disable or recreate virtualenv. |
| `apa-gmail-bridge.service` | Systemd Unit | Virtualenv `/root/venvs/composio` deleted; crashes on reboot. | **ORPHAN** | Formal disable or recreate virtualenv. |
| `apa-gws-bridge.service` | Systemd Unit | Virtualenv `/root/venvs/composio` deleted; crashes on reboot. | **ORPHAN** | Formal disable or recreate virtualenv. |
| `apa-sheets-bridge.service` | Systemd Unit | Virtualenv `/root/venvs/composio` deleted; crashes on reboot. | **ORPHAN** | Formal disable or recreate virtualenv. |
| `/root/forge_work/worktrees/RG2-*` (4 dirs) | Git Worktrees | Legacy verification directories from 2026-09-12 sessions; not registered in active git worktree list. | **ORPHAN / DORMANT** | Safe directory cleanup after verifying git metadata. |
| `flame_*` rule IDs (24 entries in `federation-models.json`)| Routing Config | Daemon decommissioned 2026-09-04; rules linger in config. | **ORPHAN** | Purge rule IDs from JSON. |
| `mulerouter` & `tokenrouter` entries | Pricing / Models | Drained/deprecated upstream routers from earlier 2026 iterations. | **DORMANT** | Retain as historical archive in `federation-models.json.archive`. |
| `/root/.hermes/cache/delegation/*.txt` (144 logs) | Log Cache | World-readable logs generated from completed subagent tasks. | **ORPHAN** | `chmod 600` and rotate old logs > 7 days. |
