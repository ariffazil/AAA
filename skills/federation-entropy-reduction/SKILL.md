---
name: federation-entropy-reduction
description: "Workspace hygiene sweep. Trigger: 'clean up', 'entropy'."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [entropy, hygiene, cleanup, federation, workspace]
    related: [arifos-federation-ops, verify-gate]
---

# Federation Entropy Reduction

Proactive workspace hygiene for the arifOS federation box. Catches and classifies accumulated chaos — scratch files, uncommitted work, stale snapshots, duplicate repos, orphan artifacts — before it causes failure.

**Not for:** single-organ debugging, security audits (`federation-constitutional-audit`), config validation (`agent-config-validation`), or kernel ops (`arifos-federation-ops`).

## When to use

- Arif says "fix this", "clean up", "sweep", "entropy reduction"
- Pre-session hygiene before major mutation
- Periodic federation health sweep (monthly)
- After a burst of agent activity
- Disk pressure (`df -h` >80%)

## BATCH 0: Read-only Discovery (T0)

Execute these probes in order. Record everything. Mutate nothing.

### 1. Git repo inventory + dirty state

```bash
find /root -maxdepth 3 -name '.git' -type d 2>/dev/null | while read g; do
  repo="${g%/.git}"
  name=$(basename "$repo")
  branch=$(cd "$repo" && git branch --show-current 2>/dev/null || echo "DETACHED")
  commit=$(cd "$repo" && git rev-parse --short HEAD 2>/dev/null || echo "NONE")
  dirty=$(cd "$repo" && git status --porcelain 2>/dev/null | wc -l)
  remote=$(cd "$repo" && git remote get-url origin 2>/dev/null || echo "NO-REMOTE")
  echo "REPO|$repo|$name|$branch|$commit|$dirty|$remote"
done
```

**Classify each:** canonical (has remote) vs agent workspace (no remote, dirty) vs date-named scratch vs quarantine vs third-party (NEVER TOUCH).

### 2. Runtime health probes

```bash
docker ps --format '{{.Names}}|{{.Status}}|{{.Ports}}'
systemctl list-units --type=service --state=running | grep -iE 'arif|aaa|forge|flame|fed|geox|wealth|well|caddy'
systemctl list-units --type=service --state=failed

for port in 3000 3001 7073 7074 8080 8088 9000 18082; do
  resp=$(curl -sf --max-time 2 "http://localhost:$port/health" 2>/dev/null | head -c 200)
  [ $? -eq 0 ] && echo "PORT $port: $resp" || echo "PORT $port: UNREACHABLE"
done
df -h / | tail -1
free -h | head -2
```

### 3. Deployment drift

```bash
cat /opt/arifos/app/.git_commit 2>/dev/null    # deployed
cd /root/arifOS && git rev-parse HEAD           # source HEAD
git log --oneline <deployed>..<HEAD>             # what changed
```

### 4. Scratch detection

```bash
find /root -maxdepth 1 -type f ! -name '.*' 2>/dev/null
```

### 5. Secret exposure scan (report location only, never values)

```bash
for repo in /root/AAA /root/arifOS /root/A-FORGE /root/HERMES /root/GEOX /root/WEALTH /root/WELL /root/FLAME /root/FED; do
  cd "$repo" 2>/dev/null || continue
  git grep -n -P 'AIza[a-zA-Z0-9_-]{35}|sk-[a-zA-Z0-9]{20,}' -- '*.py' '*.json' '*.yaml' 2>/dev/null | head -5
done
```

### 6. Storage waste

```bash
du -sh /root/*/ 2>/dev/null | sort -rh | head -20
```

Focus: `snapshots/`, `forge_work/snapshots/`, `_archive/`, `backups/`.

### 7. Duplicate/orphan + dirty repo deep-dive

Check for symlinked dirs, multiple clones of same remote, quarantine past 7-day grace, agent workspace clones with dirty state.

## BATCH 1: Safe T1 Reversible Hygiene

**Pre-condition:** ownership known, scope narrow, rollback immediate.

### T1 checklist
- [ ] PURPOSE declared
- [ ] FILES listed
- [ ] OWNER known
- [ ] ROLLBACK clear
- [ ] No protected dirty worktree

### T1 patterns

**Scratch removal:**
```bash
rm /root/zai_*.json /root/scout_parts*.yaml "/root/not a tty" /root/CLAUDE.md.bak*
```

**Preserve uncommitted work:**
```bash
cd <repo> && git add <files> && git commit -m "chore: preserve work — entropy reduction sweep"
# Rollback: git reset HEAD~1
```

**Gitignore runtime artifacts:**
```bash
echo ".megamemory/" >> .gitignore && git add .gitignore && git commit
```

## T2/T3 Boundary — STOP HERE

| Trigger | Tier |
|---|---|
| Service restart needed | T2 |
| Quarantine 7-day closure | T2 |
| Irreversible deletion | T3 |
| Unknown-ownership work | T3 |
| Credential changes | T3 |

Present T2/T3 as table with size/impact/reversibility. **Never execute T3 without Arif.**

## Entropy Register

```
E00X — <title> (<category>)
EVIDENCE: <observation>    IMPACT: <what degrades>
CONFIDENCE: 0.XX    OWNER: SOVEREIGN | UNKNOWN
REVERSIBILITY: high | low | irreversible
AUTONOMY TIER: T0 | T1 | T2 | T3
ACTION: <step>
```

Priority: SECURITY → AUTHORITY → TRUTH → RUNTIME → DUPLICATION → ORPHAN → NAMING → COSMETICS

## Zero-Chaos Verdicts

`UNKNOWN | SABAR | HOLD | PARTIAL | SEAL | VOID`

## Pitfalls

- **Don't touch third-party repos.** `.nvm`, `ComfyUI` — not ours.
- **Never overwrite unknown work.** T3 HOLD, not silent deletion.
- **The 20G pattern.** `snapshots/` + `forge_work/snapshots/` + `_archive/` = 15-20G stale.
- **Dirty ≠ broken.** Classify before acting.
- **Never claim ZERO DRIFT without measurement.** Report scope.
