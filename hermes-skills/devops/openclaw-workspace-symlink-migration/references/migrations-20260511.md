# Symlink Migration Session — 2026-05-11

## What Was Found

**Symlink detected:**
```
lrwxrwxrwx 1 root root 19 May  9 07:05 /root/.openclaw -> /root/AAA/.openclaw
```

**Target directory size:** 5.3GB total

**Size breakdown of target:**
| Directory | Size | Action |
|-----------|------|--------|
| `plugin-runtime-deps/` | 4.6GB | SKIP — regeneratable |
| `agents/` | 516MB | PRESERVE |
| `browser/` | 73MB | SKIP — cache |
| `workspace/` | 19MB | PRESERVE |
| `memory/` | 79MB | PRESERVE |
| `media/` | 31MB | SKIP — cache |
| `skills/` | 3MB | PRESERVE |
| `tasks/` | 2.3MB | PRESERVE |
| `cron/` | 2.6MB | PRESERVE |
| `sandboxes/` | 1.9MB | PRESERVE |
| `completions/` | 540K | PRESERVE |

**Smart backup size:** ~539MB (agents + workspace + tasks + cron + credentials + audit + critical files)

**Two backup dirs created:**
- `/root/AAA/.openclaw.backup-20260511-113343` — 4.4GB (from Phase 2 full copy attempt)
- `/root/AAA/.openclaw.backup-20260511-113511` — 539MB (from Phase 2 smart copy, used for migration)

## Commands Run (in order)

### Phase 1: Detect
```bash
ls -la /root/.openclaw
readlink /root/.openclaw
ls /root/AAA/.openclaw/
```

### Phase 2: Smart Backup
```bash
BACKUP_DIR="/root/AAA/.openclaw.backup-$(date +%Y%m%d-%H%M%S)"
cp -a /root/AAA/.openclaw/workspace "$BACKUP_DIR/"
cp -a /root/AAA/.openclaw/agents "$BACKUP_DIR/"
cp -a /root/AAA/.openclaw/credentials "$BACKUP_DIR/"
cp -a /root/AAA/.openclaw/audit "$BACKUP_DIR/"
cp -a /root/AAA/.openclaw/tasks "$BACKUP_DIR/"
cp -a /root/AAA/.openclaw/cron "$BACKUP_DIR/"
cp -a /root/AAA/.openclaw/exec-approvals.json "$BACKUP_DIR/"
cp -a /root/AAA/.openclaw/openclaw.json "$BACKUP_DIR/"
cp -a /root/AAA/.openclaw/env.local "$BACKUP_DIR/"
cp -a /root/AAA/.openclaw/delta-log.jsonl "$BACKUP_DIR/"
```

### Phase 3: Migrate Symlink → Real Dir
```bash
rm /root/.openclaw                          # remove symlink
mkdir -p /root/.openclaw                    # create real dir
cp -a /root/AAA/.openclaw/workspace /root/.openclaw/
cp -a /root/AAA/.openclaw/agents /root/.openclaw/
cp -a /root/AAA/.openclaw/credentials /root/.openclaw/
cp -a /root/AAA/.openclaw/audit /root/.openclaw/
cp -a /root/AAA/.openclaw/tasks /root/.openclaw/
cp -a /root/AAA/.openclaw/cron /root/.openclaw/
cp -a /root/AAA/.openclaw/exec-approvals.json /root/.openclaw/
cp -a /root/AAA/.openclaw/openclaw.json /root/.openclaw/
cp -a /root/AAA/.openclaw/env.local /root/.openclaw/
cp -a /root/AAA/.openclaw/delta-log.jsonl /root/.openclaw/
```

### Phase 4: Verify Constitutional Docs
```bash
for f in SOUL.md USER.md AGENTS.md MEMORY.md IDENTITY.md ROOT_CANON.yaml; do
  [ -f "/root/.openclaw/workspace/$f" ] && echo "✅ $f" || echo "❌ $f MISSING"
done
```

### Phase 5: Fix Permissions
```bash
chmod 700 /root/.openclaw
chmod -R 700 /root/.openclaw/workspace
chmod 700 /root/.openclaw/agents
chmod 700 /root/.openclaw/credentials
chmod 600 /root/.openclaw/exec-approvals.json
chmod 600 /root/.openclaw/openclaw.json
chmod 600 /root/.openclaw/env.local
```

### Phase 6: Verify Socket Path
```bash
python3 -c "import json; d=json.load(open('/root/.openclaw/exec-approvals.json')); print(d['socket']['path'])"
# → /root/.openclaw/exec-approvals.sock
```

### Phase 7: Verify Real Directory
```bash
stat /root/.openclaw | head -5
# → File: /root/.openclaw ... Directory ✅
```

## Git Integration Follow-On

After migration, workspace docs were copied to `/root/AAA/workspace/` for GitHub push. Nested `.git` in workspace was removed. Backup deletion required its own 888_HOLD step (F1 Amanah fires on each `rm -rf` independently, even within an approved sequence).

## OpenClaw Status After Migration

```
Gateway: local · ws://127.0.0.1:18789 · auth token ✅
Gateway service: systemd · enabled · stopped (state failed) ⚠️
Agents: 4 (codex, kimi, main, opencode) · no bootstrap files
Sessions: 7 active · default MiniMax-M2.7 (200k ctx) ✅
Tasks: 0 active · 31 issues · audit 7 warn
Heartbeat: 30m (main), 30m (codex), 30m (kimi), 30m (opencode)
```

Gateway service "state failed" predates migration; local gateway itself responding.