---
name: multi-repo-dirty-state-review
description: Inspect dirty git state across arifOS federation repos and classify changes against the 6-agent architecture model
triggers:
  - "git status"
  - "dirty"
  - "git repo status"
  - "inspect git"
---

# Multi-Repo Dirty State Review — arifOS Federation

## Workflow

### 1. Run parallel git status
```bash
echo "=== arifOS ===" && cd /root/arifOS && git status --short
echo "=== GEOX ===" && cd /root/geox && git status --short
echo "=== WEALTH ===" && cd /root/WEALTH && git status --short
echo "=== A-FORGE ===" && cd /root/A-FORGE && git status --short
```

### 2. Inspect each dirty file
```bash
git diff --stat
git diff <file>        # full diff
git diff --cached      # staged
```

### 3. Classify each change — 6-Agent model
| Agent | Role |
|-------|------|
| P-Agent | Perception — reads from WELL, GEOX, WEALTH, VAULT |
| T-Agent | Transformation — physics, math, monte_carlo |
| V-Agent | Valuation — NPV, EMV, DSCR, allocation |
| G-Agent | Governance — F1-F13 enforcement, input validation |
| E-Agent | Execution — forge, seal, memory recall |
| M-Agent | Meta — health checks, monitoring, coherence |

### 4. Three buckets
| Bucket | Action |
|--------|--------|
| ✅ Architecture-aligned | Commit |
| ⚠️ Needs-fix | Identify specific breakage |
| 🗑️ Contamination | `git rm --cached` (NOT `git rm`) |

## Known Dangerous Patterns

### Caddyfile reversions
Previous sessions reverted key routes. Watch for:
- `/000` and `/999` → `file_server` instead of `reverse_proxy arifosmcp:8080` — **breaks MCP**
- `/ops` losing `import sovereign_gate` — **opens to internet**
- `dozzle` target `127.0.0.1:8888` instead of `dozzle:8080` — **breaks container networking**

### Windows path contamination (WEALTH)
`C:/ariffazil/arifOS/...` in git index. Fix:
```bash
git rm --cached "C:/ariffazil/arifOS/arifosmcp/VAULT999/harness_breaches.jsonl"
```
**Do NOT delete the file** — real breach data.

### Submodule dirty state — `.git/` stored inside submodule
`geox` shows `M geox` in parent repo even after `git submodule update --init` succeeds and submodule HEAD matches. Root cause: submodule's `.git/` directory is inside the submodule folder (`geox/.git/`) instead of the proper location (`.git/modules/geox/`).

**Diagnosis:**
```bash
# Parent shows dirty but submodule is clean
git status  # →  M geox
cd geox && git status --short  # → nothing dirty
git rev-parse HEAD  # matches parent index commit

# Confirm the misplaced .git/
ls -d geox/.git  # exists as a directory (should be a file)
ls .git/modules/  # geox/ NOT here
```

**Fix:**
```bash
cd /root/arifOS
mkdir -p .git/modules/geox
mv geox/.git/* .git/modules/geox/
rmdir geox/.git
printf "gitdir: %s/.git/modules/geox\n" "$(pwd)" > geox/.git
git submodule update --init geox
git status  # should be clean
```

## Verify after git ops
```bash
curl -s http://localhost:8080/health | jq .status
curl -s http://localhost:8081/health | jq .status
curl -s http://localhost:8082/health | jq .status
curl -s http://localhost:8083/health | jq .status
```
