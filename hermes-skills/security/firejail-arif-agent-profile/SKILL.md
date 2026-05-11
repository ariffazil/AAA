---
name: firejail-arif-agent-profile
description: arifOS Firejail agent sandbox profile — debugged working config for W_scar mitigation on VPS (v0.9.72)
trigger: "When needing to sandbox agent code execution on VPS, or when firejail profile fails to load"
created: 2026-05-07
tags: [firejail, sandbox, w-scar, vps, security]
confidence: high
---

# arifOS Firejail Agent Sandbox Profile — DEBUGGED WORKING CONFIG

## Working Profile

Location: `/etc/firejail/arif-agent.profile`

```
include allow-python3.inc

whitelist /workspace/agent-workspace

blacklist /root
blacklist /home
blacklist /etc
blacklist /var
blacklist /var/tmp
blacklist /var/log
blacklist /var/run
blacklist /boot
blacklist /opt
blacklist /srv
blacklist /mnt
blacklist /media
blacklist /sys
blacklist /proc/sys
blacklist /proc/irq
blacklist /proc/bus
blacklist /proc/timer_list
blacklist /proc/kcore
blacklist /proc/kallsyms
blacklist /proc/1/attr

net none
caps.drop all
seccomp
```

Workspace: `/workspace/agent-workspace` (chmod 700)

## Usage
```bash
firejail --profile=/etc/firejail/arif-agent.profile python3 <script.py>
```

## Critical Gotchas (v0.9.72)

| Issue | Wrong | Correct |
|-------|-------|---------|
| Caps syntax | `caps drop all` | `caps.drop all` (dot) |
| Network block | `network none` | `net none` |
| Readonly root | `readonly /` | Not a valid directive — remove |
| noroot | silently ignored | compile-time disabled — warning only |
| nonewprivs | causes profile failure | compile-time disabled — remove entirely |

## Whitelist Path Conflict (CRITICAL)

If workspace is `/root/agent-workspace` and you `blacklist /root`, the workspace becomes inaccessible (PermissionError). 

**Fix:** Move workspace to `/workspace/agent-workspace` (outside /root hierarchy).

## Penetration Test (must be 5/5)
```python
# /workspace/agent-workspace/malicious.py
# Tests:
#  1. open /etc/shadow          → PermissionError ✅
#  2. socket to 8.8.8.8:53     → Network unreachable ✅
#  3. write /var/tmp/file      → PermissionError ✅
#  4. write /root/file          → PermissionError ✅
#  5. write /workspace/agent-workspace → succeeds ✅
```

## Key Limitation
- Runs as root SUID — `noroot` not available. `caps.drop all` + whitelist overlay mitigates.
- For stronger isolation: Docker-based sandboxing (gVisor/firecracker) recommended.

## Validation
Validated 2026-05-07 — 5/5 pen tests passed. F1 HOLDING.
