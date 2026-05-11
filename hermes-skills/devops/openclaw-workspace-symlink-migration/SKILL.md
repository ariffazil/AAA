---
name: openclaw-workspace-symlink-migration
description: Replace /root/.openclaw symlink with a real directory — preserves workspace constitutional docs, agents, and exec-approvals config. Activate when OpenClaw exec fails with "Refusing to traverse symlink in exec approvals path" or when a workspace symlink needs conversion to a real directory for security/policy reasons.
tags: [openclaw, workspace, symlink, migration, exec-approvals, devops]
trigger: "Refusing to traverse symlink, /root/.openclaw is a symlink, exec approvals path error"
category: devops
sources:
  - af-forge VPS incident 2026-05-11 (/root/.openclaw symlink → real directory)
  - openclaw exec-approvals.json socket path resolution
---

# OpenClaw Workspace Symlink Migration

## Problem

OpenClaw's exec approvals system resolves the actual filesystem path of `~/.openclaw` before granting exec access. When `/root/.openclaw` is a **symlink** to `/root/AAA/.openclaw`, the resolved path contains a symlink component that OpenClaw refuses to traverse:

```
Refusing to traverse symlink in exec approvals path: /root/.openclaw
```

This blocks all `openclaw exec` operations.

## Root Cause

OpenClaw validates the exec approvals socket path (`/root/.openclaw/exec-approvals.sock`) by checking whether it can safely traverse the path. Symlinks in the path trigger a security check failure. The socket file itself may be fine — the problem is the symlink component in the path.

## Trigger Conditions

- `openclaw exec` fails with symlink traversal error
- `/root/.openclaw` shows as `lrwxrwxrwx` in `ls -la`
- `readlink /root/.openclaw` returns a target path

## Migration Strategy

### Smart Backup (~539MB vs full 5.3GB)

**Skip regeneratable directories:**
- `plugin-runtime-deps/` — 4.6GB, reinstalled by OpenClaw automatically
- `browser/` — 73MB, cache only
- `media/` — 31MB, cache only
- `openclaw.json.bak.*` and `openclaw.json.clobbered.*` — runtime noise

**Preserve critical content:**
- `workspace/` — contains SOUL.md, USER.md, AGENTS.md, MEMORY.md, IDENTITY.md, ROOT_CANON.yaml
- `agents/` — codex, kimi, main, opencode
- `credentials/`, `audit/`, `tasks/`, `cron/`
- `exec-approvals.json`, `openclaw.json`, `env.local`, `delta-log.jsonl`

### Migration Command Sequence

```bash
# PHASE 1: DETECT
echo "=== SYMLINK DETECTION ==="
ls -la /root/.openclaw
readlink /root/.openclaw
echo "---TARGET CONTENTS---"
ls /root/AAA/.openclaw/

# PHASE 2: SMART BACKUP (critical dirs + files only, ~539MB)
echo "=== CREATING TIMESTAMPED BACKUP ==="
BACKUP_DIR="/root/AAA/.openclaw.backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

for item in workspace agents credentials audit tasks cron; do
  if [ -d "/root/AAA/.openclaw/$item" ]; then
    echo "  backing up $item..."
    cp -a "/root/AAA/.openclaw/$item" "$BACKUP_DIR/$item"
  fi
done

for f in exec-approvals.json openclaw.json env.local delta-log.jsonl; do
  if [ -f "/root/AAA/.openclaw/$f" ]; then
    echo "  backing up $f..."
    cp -a "/root/AAA/.openclaw/$f" "$BACKUP_DIR/$f"
  fi
done

echo "Backup complete: $BACKUP_DIR"
du -sh "$BACKUP_DIR"

# PHASE 3: MIGRATE SYMLINK → REAL DIR
echo "=== MIGRATING SYMLINK TO REAL DIRECTORY ==="
rm /root/.openclaw
mkdir -p /root/.openclaw
cp -a /root/AAA/.openclaw/workspace /root/.openclaw/
cp -a /root/AAA/.openclaw/agents /root/.openclaw/
cp -a /root/AAA/.openclaw/credentials /root/.openclaw/
cp -a /root/AAA/.openclaw/audit /root/.openclaw/
cp -a /root/AAA/.openclaw/tasks /root/.openclaw/
cp -a /root/AAA/.openclaw/cron /root/.openclaw/
for f in exec-approvals.json openclaw.json env.local delta-log.jsonl; do
  cp -a /root/AAA/.openclaw/$f /root/.openclaw/$f
done

# PHASE 4: VERIFY CONSTITUTIONAL DOCS
echo "=== VERIFYING CONSTITUTIONAL DOCS ==="
for f in SOUL.md USER.md AGENTS.md MEMORY.md IDENTITY.md ROOT_CANON.yaml; do
  if [ -f "/root/.openclaw/workspace/$f" ]; then
    echo "✅ $f present"
  else
    echo "❌ $f MISSING"
  fi
done

# PHASE 5: FIX PERMISSIONS
echo "=== FIXING PERMISSIONS ==="
chmod 700 /root/.openclaw
chmod -R 700 /root/.openclaw/workspace
chmod 700 /root/.openclaw/agents
chmod 700 /root/.openclaw/credentials
chmod 600 /root/.openclaw/exec-approvals.json
chmod 600 /root/.openclaw/openclaw.json
chmod 600 /root/.openclaw/env.local

# PHASE 6: VERIFY SOCKET PATH RESOLUTION
echo "=== VERIFYING SOCKET PATH ==="
python3 -c "
import json
d = json.load(open('/root/.openclaw/exec-approvals.json'))
print('socket path:', d['socket']['path'])
"
# Expected: /root/.openclaw/exec-approvals.sock
# This resolves correctly under the real directory — no change needed to config

# PHASE 7: VERIFY STAT (confirm real dir not symlink)
echo "=== FINAL VERIFICATION ==="
stat /root/.openclaw | head -5
# Should show "Directory" not "symbolic link"
```

## Post-Migration Verification

```bash
# Confirm it's a real directory
stat /root/.openclaw | grep -E "File:|directory"
# → File: /root/.openclaw ... Directory ✅

# Confirm no symlink
ls -la /root/.openclaw | head -1
# → drwx------ ✅ (not lrwxrwxrwx)

# Verify constitutional docs
ls /root/.openclaw/workspace/*.md | wc -l
# → should be >= 5

# Test openclaw status (non-exec command)
openclaw status 2>&1 | head -15
# Should show clean overview, not errors

# Verify exec-approvals socket path resolves
python3 -c "import json; d=json.load(open('/root/.openclaw/exec-approvals.json')); print(d['socket']['path'])"
# → /root/.openclaw/exec-approvals.sock (no symlink in resolved path)
```

## Rollback

```bash
# If anything goes wrong:
rm -rf /root/.openclaw
cp -a /root/AAA/.openclaw.backup-YYYYMMDD-HHMMSS /root/AAA/.openclaw
ln -s /root/AAA/.openclaw /root/.openclaw
```

## exec-approvals.json Socket Path Note

The socket path in `exec-approvals.json` is `/root/.openclaw/exec-approvals.sock`. Under a symlink, the resolved path was `/root/AAA/.openclaw/exec-approvals.sock`. Under the real directory, the resolved path is `/root/.openclaw/exec-approvals.sock` — which is correct and requires no config change.

The config itself is fine; it's the filesystem path that needed fixing.

## After Migration: Git Integration (Pushing Workspace to GitHub)

`.openclaw/` is gitignored (protects agents/, credentials/, audit/). To push workspace constitutional docs to GitHub:

### Target architecture
```
/root/AAA/                    ← git-tracked ✅ → github.com/ariffazil/AAA
  workspace/                  ← constitutional docs (SOUL.md, USER.md, AGENTS.md...) ✅ PUSH
  skills/                     ← AAA skills ✅ PUSH
  contracts/                  ← workflow contracts ✅ PUSH

/root/.openclaw/              ← gitignored 🔒
  agents/                      ← codex, kimi, main, opencode (515MB) 🔒 PRIVATE
  credentials/                 ← API keys 🔒 PRIVATE
  audit/                       ← audit logs 🔒 PRIVATE
  workspace/                   ← staging only (source copy for AAA/workspace/)
```

### Git integration steps (after migration)

```bash
# STEP 1: Create AAA/workspace/ if it doesn't exist
mkdir -p /root/AAA/workspace

# STEP 2: Copy workspace docs to AAA root (not into .openclaw/)
cp -a /root/.openclaw/workspace/*.md /root/AAA/workspace/
cp -a /root/.openclaw/workspace/memory/ /root/AAA/workspace/
cp -a /root/.openclaw/workspace/skills/ /root/AAA/workspace/ 2>/dev/null || true

# STEP 3: Remove nested .git from workspace (nested .git blocks parent git add)
# 888_HOLD — confirm before running
rm -rf /root/.openclaw/workspace/.git

# STEP 4: Verify AAA gitignore allows workspace/ (should be unignored by default)
# If .openclaw/ is gitignored, workspace/ inside it is also ignored.
# The copy to /root/AAA/workspace/ sidesteps this entirely.

# STEP 5: git add, commit, push from AAA
cd /root/AAA
git add workspace/
git commit -m "chore: add workspace constitutional docs"
git push origin main
```

### After Migration: Next Steps

1. **Gateway service may show `state failed`** — this predates the migration and is unrelated. The local gateway (`ws://127.0.0.1:18789`) is responding fine.
2. **Optional cleanup** — prune old plugin-runtime-deps from the target after migration:
   ```bash
   # Only if you want to reclaim space in /root/AAA/.openclaw/
   # 888_HOLD REQUIRED — this fires F1 Amanah rm-rf gate
   ```
3. **Backup cleanup** — `rm -rf /root/AAA/.openclaw.backup-*` fires F1 Amanah gate even when part of an approved sequence. Must be a standalone 888_HOLD step, not embedded in a compound command block.

## Key Rules Discovered

1. **Always smart-backup** — skip regeneratable cache, copy only what matters
2. **Stat confirms real dir** — `stat` output shows "Directory" for real dirs, "symbolic link" for symlinks
3. **Socket path is self-correcting** — `exec-approvals.json` contains `/root/.openclaw/exec-approvals.sock`, which resolves correctly under the real directory with no config change needed
4. **Permissions must be fixed** — after copy, the inherited permissions may be wrong (e.g., 755 on dirs that should be 700)
5. **Plugin-runtime-deps is safe to skip** — OpenClaw reinstalls this automatically from npm on next gateway start
6. **888_HOLD fires on any `rm -rf` in a compound command block** — even when the block was approved as a sequence, F1 Amanah gate intercepts each `rm -rf` independently. Backup deletion must be its own explicit 888_HOLD step.
7. **Nested `.git` inside a directory blocks parent git add** — when copying workspace to AAA for git push, remove nested `.git` first: `rm -rf /root/.openclaw/workspace/.git`
8. **`.openclaw/` gitignore blocks all children** — copying workspace to `/root/AAA/workspace/` (outside `.openclaw/`) sidesteps this entirely and is the correct push target.

## Mantra

*Ditempa Bukan Diberi — reversibility before force*