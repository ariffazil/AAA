---
name: hermes-circular-dependency-recovery
description: Recover Hermes Agent when venv deletion breaks all tools — circular dependency rescue for Hetzner/DigitalOcean/Lightsail VPS
triggers:
  - FileNotFoundError after deleting /root/AAA/.hermes/venv
  - All Hermes tools broken after disk reclamation
  - hermes-asi-gateway service restart required
tags:
  - recovery
  - hermes-agent
  - vps
  - hetzner
  - circular-dependency
  - disk-reclamation
---

# hermes-circular-dependency-recovery

## Trigger

All Hermes Agent tools (terminal, execute_code, read_file, write_file, etc.) return:
```
FileNotFoundError: [Errno 2] No such file or directory
```
**AND** the `memory` tool is blocked by symlink barrier.

**Root cause:** The Python venv at `/root/AAA/.hermes/venv` was deleted (disk reclamation or manual cleanup), but the Hermes Agent tool infrastructure has the venv Python binary hardcoded in its internal configuration (`/root/AAA/.hermes/venv/bin/python3`). Deleting the venv breaks the tools that would let you restore it — circular dependency.

**Symptom:** After deleting the Hermes venv (even intentionally for disk space), all tools become inaccessible simultaneously, including file read/write.

---

## Recovery Options (in order of speed)

### Option 1 — Hetzner Robot KVM Console (fastest for Hetzner VPS)
1. Log into https://robot.your-server.de
2. Navigate to your server → Rescue/Console
3. Run: `sudo systemctl restart hermes-asi-gateway.service`

### Option 2 — VPS Provider Web SSH (DigitalOcean/Lightsail/Vultr)
1. Login to cloud dashboard
2. Use browser-based SSH or serial console
3. Run: `sudo systemctl restart hermes-asi-gateway.service`

### Option 3 — Cloud-init (for next boot only)
If no console access available, update user-data/cloud-init to run a startup script on next reboot.

### Option 4 — Fix Python path without full restart (if tool infrastructure supports it)
If the agent is running via a wrapper that can be edited directly:
- Find the wrapper/service that launches hermes-a2a.py or hermes-asi-gateway
- Change the hardcoded venv Python path to `/usr/bin/python3`
- Restart the service

---

## Memory Write Workaround (when symlink barrier blocks `memory` tool)

**Target path:** `/root/memory/YYYY-MM-DD.md`

Do NOT try `/root/.openclaw/workspace/memory/` — that path is blocked by the symlink barrier.

---

## Prevention

Before deleting `/root/AAA/.hermes/venv` in the future:
1. Check what tools depend on it: `ps aux | grep hermes` and inspect the service definition
2. Verify the Python binary used by the service: `cat /etc/systemd/system/hermes-asi-gateway.service` or `systemctl show hermes-asi-gateway.service`
3. If the service uses the venv Python, either:
   - Change the service to use system Python before deleting
   - Or do not delete the venv

---

## Notes

- The Hermes Agent tool infrastructure is NOT the same as the hermes-a2a.py relay script (which uses stdlib only and does NOT need the venv)
- The venv contains GPU packages (nvidia/cu13, torch, triton, cudnn) that are ~5G of dead weight for the host-side relay
- Only delete the venv if a restart path is confirmed and accessible
- Service name may vary: `hermes-asi-gateway.service`, `hermes-agent.service`, etc.