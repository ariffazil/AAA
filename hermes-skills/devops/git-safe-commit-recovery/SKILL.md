---
name: git-safe-commit-recovery
description: Safe git workflow when pre-commit blocks commits in arifOS repos — avoids destroying uncommitted changes with git checkout -- .
category: devops
tags: [git, pre-commit, recovery, workflow]
---

# Git Safe Commit Recovery — arifOS Workflow

## The Failure Pattern

```
git add -A && git commit -m "..."
  → pre-commit blocks (ruff E501, black reformatted)
  → git checkout -- .
  → ALL working tree changes LOST
```

When pre-commit blocks, `git checkout -- .` restores every file to the last committed state — all uncommitted work is **permanently destroyed**.

## The Correct Sequence

### When pre-commit blocks — Unstage only, fix, recommit

```
# DON'T: git checkout -- .  ← destroys ALL uncommitted changes
# DON'T: git reset --hard  ← same destruction

# DO: git stash           ← preserves all uncommitted changes safely
git stash
# ... fix lint issues ...
git stash pop            # restore when ready to commit
```
git reset HEAD           # unstages everything, preserves working tree
ruff check --fix .       # fix lint errors automatically
ruff format <file1> <file2>  # fix line-length on specific files
git add <fixed-files>    # re-stage only what you want to commit
git commit -m "message"
```

### Fix specific files without restaging everything

```bash
# Fix lint on specific files only (doesn't touch other working tree files)
pre-commit run --files arifosmcp/runtime/public_registry.py arifosmcp/runtime/public_surface.py

# Or use ruff directly (faster):
ruff check --fix --select=E501,E402 arifosmcp/runtime/public_registry.py
ruff format arifosmcp/runtime/public_registry.py
git add arifosmcp/runtime/public_registry.py
git commit -m "fix: E501 long lines in public_registry"
```

### Surgical staging (avoid `git add -A`)

`git add -A` in arifOS stages legacy/archive dirs too, causing massive reformats. Stage only real changes:

```bash
git status --short | grep " M " | grep -v "legacy_materials\|00_legacy\|archive\|geox_local"
git add arifosmcp/runtime/public_registry.py arifosmcp/runtime/tools.py tests/...
```

## Scenario: You Already Ran `git checkout -- .`

**If changes were committed before checkout:**
1. `git reflog` — find the commit hash before checkout
2. `git show <hash>:<path>` — recover lost file content
3. Re-apply changes manually

**If changes were NEVER committed (lost):** Reflog won't help.
Use **contrast analysis** — audit current state vs canonical, then re-implement:

```bash
# 1. Audit what's now broken vs what should exist
python -m pytest tests/test_surface_lock.py tests/test_public_registry.py -q

# 2. Contrast canonical code against current state
# e.g. if canonical_map.py has 14 tools but should have 13:
#    diff CANONICAL_TOOLS against canonical13 list, identify extras

# 3. Re-implement lost hardening from scratch using:
#    - Canonical test suite as specification (tests define expected behavior)
#    - Canonical registries as source of truth
#    - Re-write from scratch rather than trying to recover dead git state
```

**Critical arifOS lesson from 2026-05-01 session:**
- `git checkout -- .` destroys ALL uncommitted changes — confirmed
- `git stash` preserves changes safely — use this instead when pre-commit blocks
- If `git checkout -- .` already ran on uncommitted work: do NOT waste time on reflog
- Instead: run canonical tests as specification, identify gaps, re-implement
- This session re-implemented 4 files of lost hardening in ~15 minutes via contrast analysis

## Scenario: Daily Backup Repo (Non-Development Reset)

For backup workflows (e.g., Hermes → AAA daily backup), the goal is *overwrite*, not *merge*. `git reset --hard origin/main` is correct here because the backup is a snapshot, not development history. This differs from normal safe-git advice.

```bash
# Daily backup workflow — NOT a development branch
cd /root/AAA
git fetch origin main
git reset --hard origin/main   # ✅ correct for backup — overwrites local history
git add -A
git commit -m "🪙 DAILY BACKUP $(date '+%Y-%m-%d %H:%M %Z')\n\nREPO=aaa"
git push origin main
```

The pre-push hook bug also affects this workflow: `REPO=` trailer parser strips whitespace but NOT semicolons, so `REPO=aaa; CONFIDENCE=0.98` extracts as `aaa;` which never matches `aaa`. Always use bare `REPO=aaa` with no trailing semicolons.

## Trigger Conditions

- Pre-commit blocks a commit in any arifOS federation repo
- About to run `git checkout`, `git reset --hard`, or `git clean -f`
- Used `git add -A` and hooks reformatted hundreds of files

## Verification

```bash
git status --short | grep -v "legacy\|archive" | head -20
```
