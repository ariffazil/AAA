# Code Semantic Alignment Audit (Phase C)
**Document:** `SEMANTIC_ALIGNMENT_AUDIT.md`  
**Standard:** QQQ Protocol · Names Must Match Behavior  
**Date:** 2026-09-14T09:50:30+08:00  
**Authority:** ARIF (F13 Sovereign Principal) · `ARIFOS::ENTROPY_REDUCTION::REALITY_GRAPH::v1`

---

## 1. Symbol & Behavior Integrity Matrix

| Symbol / Endpoint | Apparent Semantic | Actual Runtime Behavior | Semantic Classification | Risk & Impact |
|---|---|---|---|---|
| `forge_worktree` (`gatewayTools.ts`) | Implies worktree lifecycle actuator (`add`, `remove`, `branch`). | Executes read-only git status inspection (`git status`, `git branch`, stash, dirty count). | **MISLEADING_NAME** | Agents expecting to spawn worktrees fail; read-only physics sensor. |
| `flameClient.ts` (`flameClient.ts:40`) | Implies active client for FLAME network requests. | Returns instant string error `"FLAME decommissioned 2026-09-04"`; 0ms, zero network calls. | **FALSE_NAME / DEAD_CODE** | Dead import retained in `gatewayTools.ts:393` despite severed backend. |
| `agentgateway-shadow.service` | Implies a running gateway shadow daemon. | Process runs in memory from PID 3894767; underlying binary `/root/forge_work/agw/agentgateway-linux-amd64` was deleted. | **FALSE_NAME (GHOST)** | Invisible failure waiting for reboot. |
| `apa-*-bridge.service` (5 units) | Implies active Composio external tool bridges. | Running on stale RAM bytecode; Python virtualenv `/root/venvs/composio` was deleted. | **FALSE_NAME (GHOST)** | Will crash with `Failed to start` on next machine reboot. |
| `test_carry_forward_survives_seal` (pre-fix) | Implies regression test for carry-forward ledger persistence. | Asserted fixture reached live `/root/.local/share/arifos/carry_forward.json`, actively polluting production state. | **FALSE_NAME (POLLUTING)** | Fixed 2026-09-14 by FI-008 via sandbox mocks (`setUpModule`). |
| `now` / `now --json` | Implies instant unified MOTD/status pane. | In standard sandbox mode (no network), fails to connect to loopback ports and falsely reports all organs `DOWN`. | **PARTIAL_NAME** | Dependent on execution environment; accurate on host, blind in sandbox. |
| `forge_vps_ports` / `forge_vps_services` | Implies read-only observation (`OBSERVE`). | Fails execution with `status: ERROR` because it attempts write to `/root/.aforge/machine-constitution/` which is read-only in systemd. | **MISLEADING_NAME** | Pure observation tool fails due to hidden snapshot write requirement. |
