# Federation Contradiction Ledger (Phase G)
**Document:** `CONTRADICTION_LEDGER.md`  
**Standard:** QQQ Protocol · F1 Truth · Reality Wins  
**Date:** 2026-09-14T09:53:00+08:00  
**Authority:** ARIF (F13 Sovereign Principal) · `ARIFOS::ENTROPY_REDUCTION::REALITY_GRAPH::v1`

---

## 1. Documented Contradictions

### Contradiction C-001: WELL Organ Telemetry
- **Claim:** WELL organ provides verified physiological and dignity telemetry for sovereign decision gating.
- **Observed Reality:** `/health` reports `has_verified_telemetry: false`, `source_type: OPERATOR_REPORTED`, `freshness_band: STALE` (>232h). Telemetry is 0% sensor-driven and 100% aged self-report.
- **Severity:** **MEDIUM** (Mitigated by honest banner requirement).
- **Action:** Retain degraded status; never fabricate biometric scores; await sovereign inject.

### Contradiction C-002: FLAME in Federation Routing
- **Claim:** `/root/.config/federation-models.json` routes `low` effort tasks to `"flame-free"`.
- **Observed Reality:** FLAME daemon was decommissioned on 2026-09-04; port 18901 is dead; `flameClient.ts` returns an instant string error.
- **Severity:** **HIGH** (Low-effort tasks hit dead-end routing).
- **Action:** Re-route `low` effort to `fed-flash-cascade` (Gemini Flash / Qwen Flash).

### Contradiction C-003: 6 Systemd Orphan Services
- **Claim:** `systemctl` reports `agentgateway-shadow` and 5 `apa-*-bridge` services as `active (running)` and `enabled`.
- **Observed Reality:** The executable binaries (`/root/forge_work/agw/agentgateway-linux-amd64` and `/root/venvs/composio/bin/python3`) have been deleted from disk. They run from RAM and will fail completely on system reboot.
- **Severity:** **HIGH** (Hidden failure domain).
- **Action:** Request F13 sovereign ratification to formally stop and disable the units.

### Contradiction C-004: A-FORGE VPS Observation Tools vs Systemd Sandbox
- **Claim:** `forge_vps_ports` and `forge_vps_services` are read-only `OBSERVE` tools that report system state.
- **Observed Reality:** The tools attempt to persist snapshots to `/root/.aforge/machine-constitution/`, but systemd `a-forge-mcp.service` has `ProtectHome=read-only` without `/root/.aforge` whitelisted, returning `status: ERROR` (EROFS).
- **Severity:** **HIGH** (Breaks constitutional port/service assertions).
- **Action:** Add `ReadWritePaths=/root/.aforge` to `/etc/systemd/system/a-forge-mcp.service.d/override-audit-path.conf`.

### Contradiction C-005: Model Plan Quota Status
- **Claim:** Notes in `fed_status` claimed Qwen Individual plan was topped up and live.
- **Observed Reality:** Live socket probe returned `HTTP 429: Your token-plan 1-week quota has been exhausted. Resets at 09-18 04:10:00 UTC`.
- **Severity:** **HIGH** (Traffic routed to 429 rungs incurs latency penalties).
- **Action:** Update `fed_status` and LiteLLM fallback order to favor live providers (DeepSeek $14.28 and MiniMax).
