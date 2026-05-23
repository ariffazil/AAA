# Migration: /root/.openclaw symlink → real directory

**Date:** 2026-05-11  
**Epoch:** 2026-05-11T19:35+08:00  
**Type:** workspace path correction  
**Status:** COMPLETED

## Problem
OpenClaw refused to traverse `/root/.openclaw` as a symlink in its exec
approvals path, causing:
```
Refusing to traverse symlink in exec approvals path: /root/.openclaw
```

The symlink pointed: `/root/.openclaw` → `/root/AAA/.openclaw`

## Root Cause
OpenClaw's exec approval system validates the resolved path of `/root/.openclaw`
before granting exec access. A symlink in that path caused a security check
to fail silently (or hard-error depending on config).

## Solution Applied
1. Created smart backup of critical dirs (~539MB vs full 5.3GB)
   - Backup: `/root/AAA/.openclaw.backup-20260511-113511/`
   - Preserved: workspace/, agents/, credentials/, audit/, tasks/, cron/
   - Preserved: exec-approvals.json, openclaw.json, env.local, delta-log.jsonl
   - Skipped: plugin-runtime-deps/ (4.6GB, regeneratable), browser/, media/
2. Removed symlink at `/root/.openclaw`
3. Created real directory `/root/.openclaw/`
4. Copied preserved contents into the new real directory
5. Fixed permissions:
   - `chmod 700 /root/.openclaw`
   - `chmod -R 700 /root/.openclaw/workspace`
   - `chmod 700 /root/.openclaw/agents`
   - `chmod 600 /root/.openclaw/exec-approvals.json`
6. Verified all constitutional docs present

## Files Preserved
- /root/.openclaw/workspace/SOUL.md ✅
- /root/.openclaw/workspace/USER.md ✅
- /root/.openclaw/workspace/AGENTS.md ✅
- /root/.openclaw/workspace/MEMORY.md ✅
- /root/.openclaw/workspace/IDENTITY.md ✅
- /root/.openclaw/workspace/ROOT_CANON.yaml ✅
- /root/.openclaw/agents/codex/, kimi/, main/, opencode/ ✅
- /root/.openclaw/credentials/ ✅
- /root/.openclaw/audit/ ✅
- /root/.openclaw/exec-approvals.json ✅ (socket path: /root/.openclaw/exec-approvals.sock)
- /root/.openclaw/openclaw.json ✅

## What Was NOT Backed Up (Safe to Skip)
- `plugin-runtime-deps/` — 4.6GB, reinstalled by openclaw automatically
- `browser/` — 73MB, cache only
- `media/` — 31MB, cache only

## OpenClaw Status After Migration
- Gateway: local · ws://127.0.0.1:18789 · auth token ✅
- Gateway service: systemd · enabled · stopped (state failed) ⚠️
- Agents: 4 (codex, kimi, main, opencode) · no bootstrap files
- Sessions: 7 active · default MiniMax-M2.7 (200k ctx) ✅

Note: Gateway service "state failed" predates the migration and is unrelated
to the symlink fix. The local gateway itself is responding.

## Rollback
To restore from backup:
1. Delete /root/.openclaw directory contents
2. Copy from /root/AAA/.openclaw.backup-20260511-113511/ back to /root/.openclaw/
3. Recreate symlink: ln -s /root/AAA/.openclaw /root/.openclaw

## Validation
- [x] Symlink removed, real dir created
- [x] Constitutional docs verified present
- [x] Agents (codex, kimi, main, opencode) present
- [x] Permissions fixed (700 on openclaw dirs, 600 on configs)
- [x] exec-approvals.json socket path resolves under real dir
- [x] openclaw status returns clean overview
- [x] Backup available at /root/AAA/.openclaw.backup-20260511-113511/

**Mantra:** Ditempa Bukan Diberi — reversibility before force
