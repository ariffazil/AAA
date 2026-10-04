# Entropy Reduction Sweep — Detailed Probe Recipes

> Compiled 2026-08-14. Source: A-Z protocol execution across 37 repos, 31 services, 7 containers.

## Full BATCH 0 probe sequence

### Secret exposure — deeper patterns

```bash
# Check for REAL keys (complete patterns, not fragments)
# Complete Google API key (39 chars after AIza)
git grep -P 'AIza[a-zA-Z0-9_-]{35}' -- '*.py' '*.json' '*.yaml' '*.toml'

# Tracked .env files (should be .example only)
git ls-files '*.env' '.env*' | grep -v '.env.example' | grep -v '.secrets.baseline'

# Broken symlinks
find /root -maxdepth 3 -type l ! -exec test -e {} \; -print 2>/dev/null
```

**Classification guide:**
- Test data: `sk-abc...7890`, patterns inside test functions, `\"API_KEY=sk-abc...\"` in test strings
- Real exposure: complete key in doc, tracked `.env` file with secrets, key in committed config
- The AAA memory file `2026-06-18-ffff.md` has a partially-redacted key (`AIzaSy...ClQg`) — pointer, not full key → LOW risk
- The test file `automatic_runtime_gate.py` uses `sk-abc...7890` → synthetic, not real

### Agent workspace clone analysis

```bash
# These accumulate under .openclaw/ as coding agents create workspaces
for d in /root/.openclaw/workspace-claude /root/.openclaw/workspace-opencode \
         /root/.openclaw/workspace-codex /root/.openclaw/workspace-kimi \
         /root/.openclaw/workspace; do
  if [ -d "$d/.git" ]; then
    branch=$(cd "$d" && git branch --show-current 2>/dev/null)
    remote=$(cd "$d" && git remote get-url origin 2>/dev/null || echo "NO-REMOTE")
    dirty=$(cd "$d" && git status --porcelain 2>/dev/null | wc -l)
    size=$(du -sh "$d" 2>/dev/null | cut -f1)
    echo "$d  branch=$branch  dirty=$dirty  size=$size  remote=$remote"
  fi
done
```

Key observation: `.openclaw/workspace` is a 101M clone of AAA on a stale feature branch (`forge-direct-route-2026-06-08`) with 18 dirty files. This is the largest agent workspace and the strongest candidate for investigation.

### Snapshot/backup accumulation mapping

```bash
# The "20G pattern" — three directories holding stale backups
echo "=== /root/snapshots ==="
du -sh /root/snapshots/*/ 2>/dev/null | sort -rh

echo "=== forge_work snapshots ==="
du -sh /root/forge_work/snapshots/*/ 2>/dev/null | sort -rh

echo "=== forge_work _archive ==="
du -sh /root/forge_work/_archive/*/ 2>/dev/null | sort -rh

echo "=== /root/backups ==="
ls -la /root/backups/ 2>/dev/null

echo "=== /root/_archive ==="
du -sh /root/_archive/*/ 2>/dev/null | sort -rh
```

From the 2026-08-14 sweep:
- `/root/snapshots/2026-08-10T0950-pre-rebuild/` = 6.8G (pre-rebuild, 4 days old)
- `/root/forge_work/2026-08-11-act-zen-sweep/snapshots/` = 8.2G (zen sweep)
- `/root/forge_work/snapshots/arifos-deploy-20260807T120757Z/` = 3.9G (deploy backup)
- `/root/forge_work/_archive/` = 5.2G (historical archive)
- `/root/_archive/2026-08-04/` = 1.7G

### Docker volume analysis

```bash
du -sh /root/volumes/*/ 2>/dev/null | sort -rh
# ollama (5.5G), qdrant (1.4G), postgres (424M) — all functional, not waste
```

### forge_work analysis (20G total)

```bash
du -sh /root/forge_work/*/ 2>/dev/null | sort -rh
# 2026-08-11-act-zen-sweep/ = 8.2G (snapshots inside)
# _archive/ = 5.2G
# snapshots/ = 3.9G
# 2026-08-11-act-zen-sweep + _archive + snapshots = 17.3G of the 20G total
```

### Quarantine lifecycle check

```bash
ls -d /root/_quarantine* 2>/dev/null
# Check age — 7-day grace period from creation
for d in /root/_quarantine*/; do
  created=$(stat -c %Y "$d" 2>/dev/null)
  now=$(date +%s)
  age_days=$(( (now - created) / 86400 ))
  echo "$d  age=${age_days}d"
done
```

### arifOS deployment drift detail

The arifOS `/health` endpoint provides rich drift data:
```bash
curl -sf http://localhost:8088/health | python3 -c "
import sys, json
d = json.load(sys.stdin)
for k, v in d.items():
    if any(x in k.lower() for x in ['drift', 'deploy', 'identity', 'version', 'tool_count']):
        print(f'{k}: {v}')
"
```

Key fields:
- `deployment_drift_status`: "drift_detected" or "no_drift"
- `software_release.drift`: true/false
- `software_release.deployed_commit`: the commit actually running
- `software_release.built_commit`: the commit that was pip-installed
- `tool_count_semantics`: explains the different tool count numbers

## T2 redeployment recipe (if drift detected)

```bash
cd /root/arifOS
pip install -e . --no-deps 2>&1 | tail -5
systemctl restart arifos arifosd
# Verify
sleep 3
curl -sf http://localhost:8088/health | python3 -c "import sys,json; print(json.load(sys.stdin).get('deployment_drift_status'))"
```

## Common post-sweep state

After a full BATCH 0+1 sweep, typical remaining dirty repos are:
- Third-party (`.nvm` — 2 deleted agent files that shouldn't be there)
- Agent workspace clones with unknown owner work (5-6 dirs, 9-18 dirty files each)
- Date-named scratch directories (T3 candidates)

The canonical federation repos should all be clean after T1 commits.
