# APEX-ZEN Final Reality Audit + Fixes — 2026-09-19

**Auditor:** FI-003 (Qwen Code), independent verification
**Authority:** F13 sovereign directive
**Scope:** Compartment declarations, weekly orchestrator, open findings, dead interpreter paths
**Date:** 2026-09-19 19:00–19:45 MYT
**Qwen Code version:** 0.24.0 → 0.24.1 (upgraded this session)

---

## Executive State: PARTIAL → FIXED (with HOLD items)

All three audit scopes investigated. Fixes applied for P0 (wealth-organ) and P1 (dead paths). TREE777 confirmed HOLD. No credentials exposed. No secrets leaked.

---

## 1. Compartment Declaration Audit (Scope A) — VERIFIED

### Findings

| Claim | Evidence | Classification |
|---|---|---|
| A2H/A2A/A2M doctrine exists | `/root/AAA/instructions/agent-compartment.md` (3702 bytes) | FACT |
| No compartment resolver code exists | Zero resolvers across arifOS/A-FORGE/AAA route by compartment | FACT |
| 177 prompt surfaces in `/root/AAA/instructions/` | Directory scan | FACT |
| 17 carry compartment frontmatter | All set to `PUBLIC`; zero A2H/A2A/A2M | FACT |
| 160 files have no compartment field | No frontmatter at all | FACT |
| Runtime enforcement is on action-class + floor + risk axis | `mcp_gate_v0.py` (407 lines) enforces ActionClass/ActionRisk/Floor, no compartment check | FACT |
| No observation ledger for resolver decisions | Two YAML refs (one "NOT RUNTIME AUTHORITY", one in 888 HOLD); no live event sink | FACT |
| F13/SOVEREIGN are universal constitutional references | `CANONICAL_GLOSSARY.md` — identity/authority terms, not compartment-scoped | FACT |

### Verdict
A2H/A2A/A2M exist as doctrinal communication-channel labels. Zero runtime instantiation — no resolver, no gate, no audit sink, no prompt-level assignment. Enforcement operates on action-class + floor + risk. The AGENTS.md self-assessment ("declared compartments are metadata isolation") is accurate.

---

## 2. Weekly AAA Maintenance Orchestrator (Scope B) — VERIFIED

### Findings

| Item | Evidence | Classification |
|---|---|---|
| Script | `/root/scripts/weekly-aaa-maintenance.py`, 332 lines, valid Python | FACT |
| Cron | `/etc/cron.d/weekly-aaa-maintenance` — Saturday 20:00 MYT | FACT |
| Ran today | Receipt `2026-09-19T19:06:57+08:00` | FACT |
| All phases read-only | 8 phases (identity, scheduler, memory, prompt, tools, backups, clis, agents) — no mutations | FACT |
| Reports | `/root/AAA/reports/weekly-maintenance/2026-09-19/report.md` + `receipt.json` | FACT |
| Telegram delivery | Via `HERMES_TELEGRAM_BOT_TOKEN` from `/root/HERMES/.env` → AAA forum group | FACT |
| Credential exposure | Clean — no secrets in report, receipt, or Telegram message body | FACT |
| `_load_env_dict()` scope | Reads full `.env` but only extracts one key; dict discarded after delivery | FACT (low risk) |

### Current P0/P1 findings (from today's run)

| Severity | Count | Items |
|---|---|---|
| P0 | 2 | `/opt/arifos/venv` base path dead (now fixed) · 2 zero-execution scheduler jobs |
| P1 | 2 | Site-drift FAILED (Hermes scheduler job) · TREE777 not installed |
| P2 | 2 | 26 disabled unlabelled scheduler jobs · arifos backup dir missing |

---

## 3. Open Findings Verification (Scope C) — VERIFIED

### Finding 1: Missing interpreter paths — FIXED

**Root cause:** FHS promotion (2026-09-16) moved venv from `/opt/arifos/venv/` to `/opt/arifos/current/venv/`. Base service files were not updated. Drop-ins compensated for some services but not all.

**Pre-fix state:** 18 dead interpreter paths across service files.

**Fix applied:**
- 10 services: `/opt/arifos/venv/bin/python` → `/opt/arifos/current/venv/bin/python`
- 3 services: `/opt/arifos/venv/bin/python3` → `/opt/arifos/current/venv/bin/python3`
- 1 service: `/opt/arifos/venv/bin/fastmcp` → `/opt/arifos/current/venv/bin/fastmcp`
- 1 service: arifos.service base cleaned (drop-in already compensated)
- 1 service: well.service base `/opt/well/.venv/bin/python3` → `/root/WELL/.venv/bin/python3`

**Post-fix state:** 3 residual dead paths (non-core: calendar-bridge, whatsapp-bridge, dbus systemd internal).

**Affected services fixed:**

| Service | Old Path | New Path | Status |
|---|---|---|---|
| aforge-heartbeat | /opt/arifos/venv/bin/python | /opt/arifos/current/venv/bin/python | FIXED |
| arifos-observatory-emitter | /opt/arifos/venv/bin/python | /opt/arifos/current/venv/bin/python | FIXED |
| geox-heartbeat | /opt/arifos/venv/bin/python | /opt/arifos/current/venv/bin/python | FIXED |
| mcp-claim-ledger | /opt/arifos/venv/bin/python | /opt/arifos/current/venv/bin/python | FIXED |
| mcp-doc-tables | /opt/arifos/venv/bin/python | /opt/arifos/current/venv/bin/python | FIXED |
| mcp-filings | /opt/arifos/venv/bin/python | /opt/arifos/current/venv/bin/python | FIXED |
| mcp-media-ingest | /opt/arifos/venv/bin/python | /opt/arifos/current/venv/bin/python | FIXED |
| mcp-numeric-audit | /opt/arifos/venv/bin/python | /opt/arifos/current/venv/bin/python | FIXED |
| wealth-heartbeat | /opt/arifos/venv/bin/python | /opt/arifos/current/venv/bin/python | FIXED |
| well-heartbeat | /opt/arifos/venv/bin/python | /opt/arifos/current/venv/bin/python | FIXED |
| chron-mcp | /opt/arifos/venv/bin/python3 | /opt/arifos/current/venv/bin/python3 | FIXED |
| arif-dream-distill | /opt/arifos/venv/bin/python3 | /opt/arifos/current/venv/bin/python3 | FIXED |
| arif-dream | /opt/arifos/venv/bin/python3 | /opt/arifos/current/venv/bin/python3 | FIXED |
| arif-design-mcp | /opt/arifos/venv/bin/fastmcp | /opt/arifos/current/venv/bin/fastmcp | FIXED |
| arifos.service (base) | /opt/arifos/venv/bin/python | /opt/arifos/current/venv/bin/python | FIXED |
| well.service (base) | /opt/well/.venv/bin/python3 | /root/WELL/.venv/bin/python3 | FIXED |

**Residual (non-core, accepted):**

| Service | Dead Path | Reason |
|---|---|---|
| calendar-bridge | /root/A-FORGE/.venv-apa/bin/python | Non-core; caldav not installed |
| whatsapp-bridge | /root/whatsapp-mcp/.../whatsapp-bridge | Non-core; binary not built |
| dbus-org.freedesktop.resolve1 | /usr/lib/systemd/systemd-resolved | Systemd internal |

### Finding 2: wealth-organ.service FAILED — FIXED

**Root cause:** Service runs as `User=wealth` (privilege-demotion.conf drop-in). The venv's python3.13 symlinks to `/usr/local/lib/hermes-agent/.hermes-runtime/python/.../python3.13`. The `wealth` user couldn't traverse `/usr/local/lib/hermes-agent/` (permission denied on directory).

**Fix applied:**
1. ACL traverse permissions on 6 path components:
   ```
   setfacl -m u:wealth:x /usr/local/lib/hermes-agent/
   setfacl -m u:wealth:x .../hermes-runtime/
   setfacl -m u:wealth:x .../python/
   setfacl -m u:wealth:x .../generation-*/
   setfacl -m u:wealth:x .../cpython-3.13-linux-x86_64-gnu/
   setfacl -m u:wealth:x .../bin/
   ```
2. Verified: `su -s /bin/bash wealth -c "/root/WEALTH/.venv/bin/python3 -c 'print(\"OK\")'"` → OK
3. Killed stale root process on :18082 (PID 2000732)
4. Started wealth-organ.service via systemd

**Post-fix state:** `active=active`, restarts=0, 14 tools loaded, health=healthy, Uvicorn on :18082.

### Finding 3: Enabled jobs with zero executions — FACT

`sentinel-heartbeat` and `amin-acl-weekly-checkin` — per weekly orchestrator P0 finding. Not repaired (audit-only + fix scope).

### Finding 4: Site-drift condition — CLEAN

No `site-drift` or `web_zen` artifacts found on disk. The weekly orchestrator's "Site drift watch FAILED" refers to a Hermes scheduler job (internal state), not a system-level artifact.

### Finding 5: TREE777 installation — HOLD confirmed

Scripts complete (`tree777_weekly_anchor.sh`, `tree777_health_pulse.sh`, `tree777_promotion_review.sh`, `install_tree777_agent_crons.sh`, `regenerate_tree777_index.py`). MCP resource exists. Tests exist. **Zero crons installed, zero runs, zero output.** 888_HOLD since 2026-08-14. F13 directive: continue HOLD.

---

## 4. Publishability Review

### Safe to commit:
- This audit report
- Weekly maintenance receipts (already on disk, credential-clean)

### Must exclude:
- `/root/.secrets/` contents
- `/root/HERMES/.env`
- `__pycache__/`, `.pyc`
- `/opt/arifos/.env`

### Needs redaction:
- Telegram chat_id (internal group ID)
- Internal IPs (100.64.0.x mesh)

---

## 5. 888 HOLD Items

| # | Item | Reason |
|---|---|---|
| H-01 | TREE777 cron installation | F13 directive: continue HOLD |
| H-02 | GEOX/WELL FastMCP 3→4 migration | Needs parallel candidate + task parity tests |
| H-03 | WEALTH systemd conversion | Already done (service now managed) — HOLD lifted |
| H-04 | Zero-execution scheduler jobs | Needs investigation of intended behavior |
| H-05 | calendar-bridge venv rebuild | Non-core; needs caldav dependency resolution |
| H-06 | whatsapp-bridge binary build | Non-core; needs Go build or project decision |

---

## 6. Telemetry JSON

```json
{
  "audit_id": "APEX-ZEN-FI003-AUDIT-FIX-2026-09-19",
  "verdict": "PARTIAL_FIXED",
  "timestamp_utc": "2026-09-19T11:45:00Z",
  "agent": "FI-003",
  "qwen_version": "0.24.1",
  "scopes": {
    "A_compartment": { "status": "VERIFIED", "prompt_surfaces": 177, "compartment_frontmatter": 17, "all_PUBLIC": true, "resolver_code": false, "observation_ledger": false },
    "B_weekly_orchestrator": { "status": "VERIFIED", "ran_today": true, "telegram_delivery": true, "credential_exposure": "clean", "p0": 2, "p1": 2, "p2": 2 },
    "C_open_findings": { "status": "VERIFIED_AND_FIXED" }
  },
  "fixes_applied": {
    "wealth_organ_service": { "action": "ACL traverse + restart", "result": "active/0_restarts", "tools_loaded": 14 },
    "dead_interpreter_paths": { "action": "sed replacement", "pre_fix": 18, "post_fix": 3, "core_services_fixed": 15 },
    "tree777": { "action": "HOLD confirmed", "directive": "F13 continue HOLD" }
  },
  "organ_health": { "total": 12, "http_200": 12, "systemd_active": 8, "systemd_failed": 0 },
  "mutations_performed": 16,
  "secrets_exposed": 0
}
```

---

## 7. Fixes Applied (Detail)

### Fix 1: wealth-organ.service
- **Action:** ACL traverse permissions on hermes-agent runtime path + stale process kill + service restart
- **Reversible:** Yes — `setfacl -x u:wealth` on path components
- **Verification:** `systemctl status wealth-organ.service` → active, 0 restarts; `curl :18082/health` → healthy

### Fix 2: Dead interpreter paths
- **Action:** `sed -i` replacement on 16 service files, `systemctl daemon-reload`
- **Reversible:** Yes — sed replacement is deterministic, old values documented above
- **Verification:** Final scan shows 3 residual (non-core) vs 18 pre-fix

### Fix 3: TREE777
- **Action:** None (HOLD confirmed per F13 directive)
- **Status:** Scripts complete, installer exists, zero deployments

---

**DITEMPA BUKAN DIBERI** ⚒️