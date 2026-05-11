---
name: firejail-sandbox-arifos
description: Firejail sandbox setup for arifOS agent code execution — W_scar mitigation with penetration testing
tags: [firejail, sandbox, security, w-scar, f1-amanah]
last_updated: 2026-05-07
---

# Firejail Agent Sandbox for arifOS

## Purpose
Isolate agent code execution on arifOS VPS using Firejail. Mitigates W_scar risk — contained workspace, no host damage possible.

## Trigger
Use when agents need to run Python/Bash code that could be malicious or buggy.

## Prerequisites
- firejail installed: `apt-get install -y firejail`
- workspace created: `mkdir -p /workspace/agent-workspace && chmod 700 /workspace/agent-workspace`
- arif-agent user: `useradd -r -s /usr/sbin/nologin -M arif-agent` (optional, for extra safety)

## Profile: /etc/firejail/arif-agent.profile

```bash
# arifOS Agent Sandbox Profile
# F1 AMANAH — W_scar isolation
# Workspace: /workspace/agent-workspace (OUTSIDE /root to avoid blacklist conflict)

# Workspace only — whitelist mode ON
whitelist /workspace/agent-workspace

# Block all system paths
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

# Network: completely disabled
net none

# Capabilities: drop all (DOT syntax, not space)
caps.drop all

# Seccomp
seccomp
```

## Critical Syntax Rules (learned empirically)
- `caps.drop all` — DOT, not space. `caps drop all` is invalid.
- `nonewprivs` — compile-time disabled in Ubuntu 0.9.72 packages. Do not include.
- `noroot` — compile-time disabled in Ubuntu 0.9.72. Do not include.
- `readonly /` — NOT a valid top-level directive. Remove.
- `blacklist` paths must exist at runtime. Non-existent paths cause crashes.
- `/workspace/agent-workspace` MUST be outside `/root` — blacklist+whitelist conflict resolves /root as writable if both apply to same tree.

## Usage
```bash
# Basic sandbox execution
firejail --profile=/etc/firejail/arif-agent.profile python3 /workspace/agent-workspace/script.py

# With log output
firejail --profile=/etc/firejail/arif-agent.profile --output=/workspace/agent-workspace/sandbox.log python3 script.py
```

## Penetration Test
Save as `/workspace/agent-workspace/malicious.py` and run against the profile to verify F1:

```python
#!/usr/bin/env python3
import os, sys, socket

tests = []

# Test 1: Read /etc/shadow
try:
    open("/etc/shadow").read()
    tests.append(("FAIL", "Test 1: /etc/shadow readable — BREACH"))
except PermissionError as e:
    tests.append(("PASS", f"Test 1: /etc/shadow blocked — {e}"))

# Test 2: Network access
try:
    s = socket.socket()
    s.settimeout(2)
    s.connect(("8.8.8.8", 53))
    tests.append(("FAIL", "Test 2: Network reachable — BREACH"))
except OSError as e:
    tests.append(("PASS", f"Test 2: Network blocked — {e}"))

# Test 3: Write to /var/tmp
try:
    open("/var/tmp/test.txt", "w").write("x")
    os.remove("/var/tmp/test.txt")
    tests.append(("FAIL", "Test 3: /var/tmp writable — BREACH"))
except PermissionError as e:
    tests.append(("PASS", f"Test 3: /var/tmp blocked — {e}"))

# Test 4: Write to /root
try:
    open("/root/test.txt", "w").write("x")
    tests.append(("FAIL", "Test 4: /root writable — BREACH"))
except PermissionError as e:
    tests.append(("PASS", f"Test 4: /root blocked — {e}"))

# Test 5: Workspace is writable
try:
    open("/workspace/agent-workspace/.probe", "w").write("x")
    os.remove("/workspace/agent-workspace/.probe")
    tests.append(("PASS", "Test 5: Workspace correctly writable"))
except Exception as e:
    tests.append(("FAIL", f"Test 5: Workspace blocked — {e}"))

# Results
for status, msg in tests:
    print(f"  {'❌' if status == 'FAIL' else '✅'} {msg}")
all_passed = all(s == "PASS" for s, _ in tests)
print("\n🎯 SANDBOX VERIFIED — F1 HOLDING" if all_passed else "\n🚨 SANDBOX BREACH — F1 VIOLATION")
sys.exit(0 if all_passed else 1)
```

## Verification — Is Firejail ACTUALLY Running? (CRITICAL)

A common misconfiguration: firejail is installed, profiles exist on disk, but **zero processes are actually sandboxed**. Always verify before claiming W_scar is mitigated.

```bash
# VERIFICATION STEP — run this first
ps aux | grep firejail | grep -v grep

# Expected: list of firejail-wrapped processes
# ACTUAL on af-forge (2026-05-07): EMPTY — zero processes sandboxed despite profiles existing

# If empty, check:
firejail --version                    # Is binary installed?
ls -la /etc/firejail/arif-agent.profile  # Do profiles exist?
systemctl status arif-agent-worker  # Is the daemon active?
```

**Current af-forge state (2026-05-07):**
- Firejail 0.9.72 installed: ✅
- Profile at `/etc/firejail/arif-agent.profile`: ✅
- Workspace `/workspace/agent-workspace` (700): ✅
- Processes actually wrapped by firejail: ❌ **ZERO**
- **Verdict:** The cage is blueprints on disk, not a locked door. W_scar is NOT mitigated yet.

## What This Means
The profile being correct does not mean the sandbox is active. You must have a process running under `firejail --profile=...` for the isolation to be real. If `ps aux | grep firejail` returns empty, the agent code is running on bare metal with no cage.

## Known Limitations
- `noroot` / `nonewprivs` compile-time disabled in Ubuntu 0.9.72 — cannot use user namespaces. Sandbox runs as root SUID. Mitigated by `caps.drop all` + whitelist-only mode.
- For stronger isolation: consider Docker-based sandbox (rootless container) instead of or layered with Firejail.
- firejail cannot block `/proc` reads by root — only whitelist-based overlayfs effectively hides host files from root.
