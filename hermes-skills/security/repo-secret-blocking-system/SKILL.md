---
name: repo-secret-blocking-system
description: Autonomous secret-blocking CI/CD system for arifOS federation repos — prevents secrets (Telegram tokens, API keys, GitHub tokens) from reaching GitHub. Uses detect-secrets baseline + git hook + GitHub Actions.
trigger: "Build secret scanning for a new repo, or fix a leaked secret in an existing repo"
version: 1.0.0
category: security
tags: [security, git, github-actions, detect-secrets, secrets-scanning]
---

# Repo Secret Blocking System

## What it does

Blocks commits containing secrets (Telegram bot tokens, API keys, GitHub tokens, AWS keys) from reaching GitHub via a 3-layer defense:

| Layer | Component | What it blocks |
|-------|-----------|---------------|
| Local pre-commit | `.git/hooks/pre-commit` | Secrets in staged files before commit |
| Tracked portable copy | `hooks/pre-commit-secret-scan` | Same hook, tracked in git for portability |
| GitHub CI | `.github/workflows/secrets-audit.yml` | Any secret push to any branch |

## Architecture

```
REPO/
├── .git/hooks/pre-commit           ← local hook (installed, not tracked)
├── hooks/pre-commit-secret-scan    ← tracked copy (portable)
├── .pre-commit-config.yaml         ← pre-commit framework (optional)
├── .secrets.baseline               ← snapshot of known secrets
└── .github/workflows/
    └── secrets-audit.yml           ← GitHub CI gate
```

## Setup Steps

### Step 1 — Install detect-secrets

```bash
pip install detect-secrets
```

### Step 2 — Create baseline

```bash
# WRONG: detect-secrets scan . --baseline .secrets.baseline
# CORRECT: pipe output to file
detect-secrets scan . > .secrets.baseline
```

### Step 3 — Create pre-commit hook

```bash
mkdir -p .git/hooks
# (write the hook script to .git/hooks/pre-commit — see reference below)
chmod +x .git/hooks/pre-commit
```

### Step 4 — Create tracked portable copy

```bash
mkdir -p hooks
cp .git/hooks/pre-commit hooks/pre-commit-secret-scan
chmod +x hooks/pre-commit-secret-scan
```

### Step 5 — Add to git

```bash
git add hooks/pre-commit-secret-scan .secrets.baseline .pre-commit-config.yaml
git add .github/workflows/secrets-audit.yml  # create this file first
```

### Step 6 — Commit with REPO= trailer

```bash
git commit -m "feat: WAJIB secrets audit system
REPO=<repo-name>"
```

## Hook Script Reference
### Hook Script Reference (AAA-v1 — deployed and working)

```bash
#!/bin/bash
# ============================================================
# PRE-COMMIT HOOK — arifOS AAA Secret Scanner
# WAJIB gate: F1 AMANAH enforcement
# Blocks commits containing untracked secrets.
# Skip: git commit --no-verify (emergency only — SABAR)
# ============================================================
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

echo "🔒 Running AAA Wajib Secret Gate..."

# ── 1. Pattern scan (fast regex — catches known secret formats) ──
echo "  [1/2] Pattern scan (Telegram/GitHub/API keys)..."

PATTERNS=(
    'bot[0-9]+:[A-Za-z0-9_\-]{20,}'
    'gh[pousr]_[A-Za-z0-9_]{35,}'
    'sk-[A-Za-z0-9_\-]{30,}'
    'AKIA[A-Z0-9]{16}'
)
EXCLUDE_DIRS="_archive memory secrets .git node_modules"

BLOCKED_FILES=$(git diff --cached --name-only)
FOUND_BAD=0

for file in $BLOCKED_FILES; do
    skip=0
    for ex in $EXCLUDE_DIRS; do
        [[ "$file" == $ex/* ]] && skip=1 && break
    done
    [[ $skip -eq 1 ]] && continue
    [[ -d "$file" ]] && continue

    CONTENT=$(git diff --cached "$file")
    for pat in "${PATTERNS[@]}"; do
        if echo "$CONTENT" | grep -qE "$pat"; then
            echo -e "  ${RED}🚫 $pat${NC} in staged file: $file"
            FOUND_BAD=1
        fi
    done
done

if [ $FOUND_BAD -eq 1 ]; then
    echo -e "\n${RED}🛑 BLOCKED — Known secret patterns in staged files${NC}"
    exit 1
fi
echo -e "  ${GREEN}✅ No known secret patterns detected${NC}"

# ── 2. detect-secrets baseline comparison ──────────────────────────────
echo "  [2/2] detect-secrets baseline comparison..."

if ! command -v detect-secrets &>/dev/null; then
    echo -e "  ${YELLOW}⚠️  detect-secrets not installed — pip install detect-secrets${NC}"
else
    SCAN_TMP=$(mktemp)
    detect-secrets scan . \
        --exclude-files '_archive/.*' \
        --exclude-files 'memory/.*' \
        --exclude-files 'secrets/.*' \
        --exclude-files 'skills/.*/_meta\.json' > "$SCAN_TMP" 2>/dev/null || true

    if [ -s "$SCAN_TMP" ] && [ -f ".secrets.baseline" ]; then
        NEW=$(python3 -c "
import json, sys
with open('$REPO_ROOT/.secrets.baseline') as f:
    baseline = json.load(f)
with open('$SCAN_TMP') as f:
    current = json.load(f)
baseline_map = {}
for fname, entries in baseline.get('results', {}).items():
    baseline_map[fname] = {e['hashed_secret'] for e in entries}
new_secrets = []
for fname, entries in current.get('results', {}).items():
    skip = any(fname.startswith(ex) for ex in ['_archive/','memory/','secrets/','skills/'])
    if skip: continue
    for entry in entries:
        h = entry['hashed_secret']
        if fname not in baseline_map or h not in baseline_map[fname]:
            new_secrets.append((entry['type'], fname, entry['line_number']))
if new_secrets:
    print('BLOCK')
    for t, f, l in new_secrets:
        print(f'  🚫 NEW: {t} in {f}:{l}')
else:
    print('OK')
" 2>/dev/null)

        if [ "${NEW:-OK}" = "BLOCK" ]; then
            echo -e "\n${RED}🛑 BLOCKED — New secrets not in .secrets.baseline${NC}"
            python3 -c "
import json
with open('$SCAN_TMP') as f: current = json.load(f)
with open('$REPO_ROOT/.secrets.baseline') as f: baseline = json.load(f)
baseline_map = {}
for fname, entries in baseline.get('results', {}).items():
    baseline_map[fname] = {e['hashed_secret'] for e in entries}
for fname, entries in current.get('results', {}).items():
    skip = any(fname.startswith(ex) for ex in ['_archive/','memory/','secrets/','skills/'])
    if skip: continue
    for entry in entries:
        h = entry['hashed_secret']
        if fname not in baseline_map or h not in baseline_map[fname]:
            print(f'  🚫 {entry[\"type\"]} in {fname}:{entry[\"line_number\"]}')
" 2>/dev/null
            echo ""
            echo "FIX: Remove secret or re-audit: detect-secrets scan . > .secrets.baseline"
            rm -f "$SCAN_TMP"
            exit 1
        fi
    fi
    rm -f "$SCAN_TMP"
fi

echo -e "\n${GREEN}✅ WAJIB gate PASSED — no new secrets detected${NC}"
exit 0
```

## GitHub Actions Workflow (AAA-v1 — deployed and working)

Full working workflow at `/root/AAA/.github/workflows/secrets-audit.yml`:
- `secrets-audit` job: detect-secrets scan + fast regex pattern scan
- `block-secrets` job: runs if secrets found on push/PR, blocks with explicit fix instructions
- Excludes `_archive/`, `memory/`, `secrets/`, `skills/_meta.json` from scan (historical secrets)
- Uses `python3 -c` inline scripts (no separate file needed)

      - name: Pattern scan
        run: |
          # Fast regex scan for known secret patterns
          grep -rE '(bot\d+:[A-Za-z0-9_\-]{20,}|gh[pousr]_[A-Za-z0-9_]{35,}|...)' \
              --exclude-dir=_archive --exclude-dir=memory --exclude-dir=secrets .
```

## Important Notes

### `.git/hooks/pre-commit` is NOT tracked by git
- `.git/hooks/` is in `.gitignore` by default
- Always ALSO store the hook script in `hooks/pre-commit-secret-scan` so it's tracked
- On clone: `cp hooks/pre-commit-secret-scan .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit`

### detect-secrets baseline creation syntax
- `--baseline` flag does NOT create a file — it's for a different workflow
- Correct: `detect-secrets scan . > .secrets.baseline`

### Excluding known-legacy dirs
- `_archive/`, `memory/`, `secrets/` should be excluded from the pre-commit gate
- These contain historical secrets that would fail every commit
- They ARE scanned by GitHub Actions (will warn but not block if in baseline)
- For full cleanup: use BFG Repo-Cleaner

### Selective staging
- Use `git add <specific_files>` to avoid committing unrelated WIP changes
- The pre-commit hook runs on whatever is staged, not the whole repo

## Applying to Multiple Repos

To apply to another repo (arifOS, A-FORGE, GEOX, WEALTH):

```bash
# For each repo:
cd /root/REPO_NAME
pip install detect-secrets
detect-secrets scan . > .secrets.baseline

# Copy hook and workflow
cp /root/AAA/hooks/pre-commit-secret-scan hooks/pre-commit-secret-scan
cp /root/AAA/.pre-commit-config.yaml .
mkdir -p .github/workflows
cp /root/AAA/.github/workflows/secrets-audit.yml .github/workflows/

# Update REPO_ROOT in the hook if needed (it auto-detects via git rev-parse)
chmod +x hooks/pre-commit-secret-scan
cp hooks/pre-commit-secret-scan .git/hooks/pre-commit

# Edit .secrets.baseline: scan the new repo
detect-secrets scan . > .secrets.baseline
```
