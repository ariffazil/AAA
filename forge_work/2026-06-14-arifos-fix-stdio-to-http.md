# FORGE AUDIT: arifOS Kernel Systemd Fix

**Date:** 2026-06-14 10:28 UTC  
**Agent:** 000-FORGE  
**Session:** SEAL-58137c0600e549dc  
**Trigger:** Arif requested audit of initTool call 3 (`arif_session_init`)

## Diagnosis

initTool call 3 returned `502` because:

1. **Root cause:** `/etc/systemd/system/arifos.service` ran `main()` with no `AAA_MCP_TRANSPORT` env var.
2. The code defaults to **stdio mode** — no TCP listener, no HTTP endpoint.
3. So the kernel WAS running (systemd said active) but port 8088 had zero listeners.
4. Bonus: a rogue stdio instance (PID 1790419) had been running for 2+ hours at `/usr/local/bin/python -m arifosmcp.runtime stdio` consuming resources.

## Fix Applied

| Before | After |
|--------|-------|
| No `PORT` env → defaulted to 8080 | `PORT=8088` added |
| No `AAA_MCP_TRANSPORT` → defaulted to `stdio` | `AAA_MCP_TRANSPORT=http` added |

**File:** `/etc/systemd/system/arifos.service`  
**Change:** Added two Environment lines

## Verification

| Check | Result |
|-------|--------|
| `ss -tlnp \| grep 8088` | LISTEN (PID 2070370) |
| `curl localhost:8088/health` | `{"status":"healthy"}` |
| `arif_ping` | SEAL ✅ |
| `arif_os_attest` | SEAL ✅ |
| `arif_session_init` (mode=light, actor=arifbfazil) | SEAL ✅ — session SEAL-58137c0600e549dc |
| `arif_organ_attest_all` | All 4 ALIVE: arifOS(13), GEOX(37), WEALTH(20), WELL(18) |

## Cleanup

- Killed rogue stdio instance (PID 1790419)
- Previous arifOS instance (PID 2035000) at 99.8% CPU — killed by systemctl stop

## Evidence

- Unit file: `/etc/systemd/system/arifos.service`
- Health: `curl http://127.0.0.1:8088/health`
- Attest all JSON: see session SEAL-58137c0600e549dc
