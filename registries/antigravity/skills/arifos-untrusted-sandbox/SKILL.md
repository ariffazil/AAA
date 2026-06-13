---
name: arifos-untrusted-sandbox
description: Mandatory bubblewrap (bwrap) supermax jail for executing any untrusted Python/JS synthesized by external AIs (Copilot, Mythos, third-party). Load when running, evaluating, or testing code from non-federation AI sources. Triggers on `exec(`, `eval(`, untrusted code review, jail requirement.
version: 1.0.0
author: arif
tags: arifos, sandbox, security, bwrap, jail, untrusted
---

# arifOS Untrusted Execution Sandbox

## Authority
- **Owner:** Sovereign Architect 888 (Arif)
- **Status:** ACTIVE
- **Deployed:** 2026-06-03

## Purpose
When an external AI (Copilot, Mythos, or any untrusted synthesizer) generates Python code for arifOS, that code MUST be executed inside a `bwrap` (Bubblewrap) Supermax jail before it touches any federation organ.

This skill defines both:
1. The **System Prompt** fed to untrusted AI engines
2. The **Runtime Harness** (`arifos-sandbox`) that enforces the jail

## When to Use
- Generating code from external LLMs (non-arifOS agents)
- Running user-submitted scripts
- Testing AI-generated automation
- Any scenario where code origin is not 100% trusted

## When NOT to Use
- Federation agents (arifOS, WEALTH, WELL, GEOX) — these run under systemd hardening, not bwrap
- Internal tool execution — use `arifosmcp.runtime.dispatcher`

## The System Prompt

See `/root/arifOS/prompts/untrusted_execution_synthesizer.txt`

Core constraints communicated to the AI:
- UID 65534 (nobody), cap-drop ALL
- Network namespace: loopback exists, zero external routes
- Filesystem: read-only binds, writable only in `/tmp` (64MB tmpfs)
- Hard limits: 5 seconds, 128MB RAM
- Python stdlib only, zero third-party imports
- Banned modules: subprocess, os.system, ctypes, socket, urllib, eval, exec, compile, __import__
- I/O: stdin only in, stdout only out

## The Runtime Harness

```bash
arifos-sandbox '<python_code>' [timeout] [memory_kb]
```

### Implementation
- `timeout(1)` enforces the seconds limit (SIGKILL)
- `ulimit -v` enforces the memory limit (OOM)
- `bwrap` provides namespace isolation, capability drop, and filesystem sandboxing
- Script is written to ephemeral temp file, destroyed after execution

### bwrap flags used
```
--ro-bind /usr /usr
--ro-bind /lib /lib
--ro-bind /lib64 /lib64
--proc /proc
--dev /dev
--size 67108864 --tmpfs /tmp
--unshare-all
--die-with-parent
--new-session
--cap-drop ALL
--setuid 65534
--setgid 65534
--dir /run/user
```

## F1–F13 Alignment

| Floor | Compliance |
|-------|------------|
| F1 | Capability drop + namespace isolation = no privilege escalation |
| F2 | Prompt accurately reflects runtime reality (loopback truth, timeout truth) |
| F4 | Single-threaded, stdlib-only = consistent execution environment |
| F7 | 5s/128MB bounds prevent resource exhaustion |

## DITEMPA BUKAN DIBERI
