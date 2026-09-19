# Aggregate Receipt — FastMCP Upgrade + Middleware Reattach — 2026-09-19

> **Authority:** F13 sovereign directive *"Restart but can you please upgrade all MCP to latest fastMCP"* + OpenClaw operational plan
> **Actor:** Hermes ASI (venv upgrade + restart) + OpenClaw (repo pin + README + commit)
> **State:** ALL_SERVICES_HEALTHY

---

## Scope

Upgrade FastMCP across all organ venvs to latest stable, restart services, verify middleware attachment and health.

## Per-Organs Receipt

### 1. arifOS

| Field | Value |
|---|---|
| old_v | 4.0.4 |
| new_v | **4.0.5** |
| venv | `/opt/arifos/current/venv` |
| service | arifos (systemd, Restart=always) |
| PID | 1983292 (old: 1657536) |
| health | 200 OK, 13 floors active, vault999 healthy |
| middleware | IS_FASTMCP_3=True, IngressToleranceMiddleware IS real Middleware subclass; code path `if IS_FASTMCP_3:` enters real block |
| readme_commit | `36f69a46` |
| rollback | `kill -TERM <PID>` → systemd auto-restart with previous venv |

### 2. arifflow

| Field | Value |
|---|---|
| old_v | 3.4.4 |
| new_v | **4.0.5** |
| venv | `/opt/arifflow/venv` |
| service | arifflow (systemd, Restart=always) |
| PID | 1990181 (old: 1983298) |
| health | 200 OK, fq verdict OPTIMAL |
| readme_commit | `cc6d31e3` (AAA repo) |
| rollback | `kill -TERM <PID>` |

### 3. GEOX

| Field | Value |
|---|---|
| old_v | 3.4.7 |
| new_v | **3.4.7** (DOWNGRADED from 4.0.5) |
| venv | `/opt/geox/.venv` |
| service | geox-mcp (systemd, Restart=always) |
| PID | 1996573 (old: 1284839) |
| health | 200 OK, kernel_verdict=SEAL |
| **reason_for_downgrade** | GEOX uses `tasks` extension (`io.modelcontextprotocol/tasks`) which was removed in fastmcp 4.x. `pip install 'fastmcp[tasks]'` is a no-op in 4.x. |
| readme_commit | `835065e7` |
| rollback | `pip install fastmcp==3.4.7` |

### 4. WELL

| Field | Value |
|---|---|
| old_v | 3.4.4 |
| new_v | **3.4.7** (DOWNGRADED from 4.0.5) |
| venv | `/root/WELL/.venv` |
| service | well (systemd, Restart=always) |
| PID | 1996078 (old: 2844828) |
| health | 200 OK |
| **reason_for_downgrade** | Same as GEOX: uses tasks extension. WELL tools `well_999_vault`, `well_assess_sovereign_entropy`, `well_seal_vault` require it. |
| readme_commit | `962ee6a` (PASS_NO_OP — already at 4.0.5 in HEAD) |
| rollback | `pip install fastmcp==3.4.7` |

### 5. WEALTH

| Field | Value |
|---|---|
| old_v | 4.0.5 (old venv was DELETED during earlier upgrade attempt) |
| new_v | **4.0.5** |
| venv | `/root/WEALTH/.venv` (recreated from scratch) |
| service | NOT systemd — manual process (`server_federated.py`) |
| PID | 2000630 (old: 1638548) |
| health | 200 OK, tools_loaded=14 |
| extra | Had to install numpy, httpx, scipy, pandas after venv recreation |
| readme_commit | `81c2d74` |
| rollback | `kill -TERM <PID>` + re-run manual start |

## Summary

| Service | Port | fastmcp | Status | Middleware |
|---|---|---|---|---|
| arifos | :8088 | 4.0.5 | ✅ 200 | real Middleware subclass ✅ |
| arifflow | :7073 | 4.0.5 | ✅ 200 | no organ-specific middleware |
| geox-mcp | :8081 | 3.4.7 | ✅ 200 | tasks-based tools operational |
| well | :18083 | 3.4.7 | ✅ 200 | tasks-based tools operational |
| wealth | :18082 | 4.0.5 | ✅ 200 | no organ-specific middleware |

## Open Items

1. **GEOX and WELL cannot upgrade to fastmcp 4.x** until their `tasks` extension usage is migrated. The `io.modelcontextprotocol/tasks` extension does not exist in fastmcp 4.x. Any future upgrade requires code changes in both organs.
2. **WEALTH is not systemd-managed.** It runs as a manual process. If it dies, it does not auto-restart. Recommend converting to systemd unit.
3. **Middleware attachment verification for arifOS** — the COMPAT log lines do not appear in journald (logging configuration may suppress them), but the code path is verified: IS_FASTMCP_3=True, IngressToleranceMiddleware is a real Middleware subclass, and `mcp.add_middleware()` is called at server.py:2081.
4. **Individual repo receipts** at `/root/AAA/reports/mcp-upgrade-*-2026-09-19.md` (written by OpenClaw).

---

*Receipt written 2026-09-19 19:15 UTC+8 · Hermes ASI*
*DITEMPA BUKAN DIBERI*
