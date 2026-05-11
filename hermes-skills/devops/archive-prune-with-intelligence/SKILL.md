---
name: archive-prune-with-intelligence
description: Remove a large directory from git history permanently — distill intelligence first, rewrite history clean, update all live references. Prevents "zombie archive paths" haunting future agents.
tags:
  - git
  - history-rewrite
  - cleanup
  - arifOS
created: 2026-04-26
---

# archive-prune-with-intelligence

Remove a large directory from git history while preserving intelligence and updating all live references.

## When to Use
- A directory like `archive/` has grown to 100+ files with 155+ commits and you want it GONE from git history permanently
- You've already identified the directory has no ongoing value but may contain intelligence worth keeping
- Standard `git rm` + commit only removes files from current tree — history still contains them

## Core Principle
**DITEMPA BUKAN DIBERI** — Intelligence must be forged into live code BEFORE history is rewritten. Never delete first.

## Pre-Check: Extract Intelligence First

```bash
# 1. Find all .md files in the archive
find /path/to/archive -name "*.md" 2>/dev/null | head -50

# 2. Read critical documents (ones with real content, not session logs)
# Focus on: eureka files, engineering blueprints, protocol specs, audit docs
# Skip: Telegram metadata sessions, provider configs, working docs

# 3. For each meaningful doc:
#    a. Identify the eureka/insight
#    b. Find where in live code it should be forged
#    c. Patch the target file BEFORE history rewrite
```

## The 7-Step Forge

```
STEP 1 — Audit and distill
├── find /path/to/archive -name "*.md" | xargs wc -l
├── Read top 5-10 meaningful docs (not session logs)
├── Identify: P1 gaps, implementation patterns, physics grounding
└── Write distilled insights to wiki/pages/RECURSIVE_IMPROVEMENT_LOG.md

STEP 2 — Forge eureka into runtime code
├── Delta Bundle spec → tools/mind_reason.py
├── Quantum Sabar Protocol → tools/sense_observe.py
├── Extension hooks → tools_canonical.py header
└── P1 gaps → wiki/RECURSIVE_IMPROVEMENT_LOG.md

STEP 3 — Install git-filter-repo
python3 -m pip install --target /tmp/gitfi git-filter-repo
python3 /tmp/gitfi/git_filter_repo.py --version  # verify

STEP 4 — Rewrite history (remove directory from ALL commits/branches/tags)
cd /path/to/repo
git filter-repo --path archive/ --invert-paths --force

STEP 5 — Update ALL live references to the removed directory
# grep for remaining "archive/" in active (non-.git) files
grep -r "archive/" --include="*.md" --include="*.py" -l . | grep -v ".git"

# For each reference:
# - Code paths → update to new location (wiki/, etc.)
# - Documentation → remove stale references
# - Session anchors → add annotation: "⚠️ DELETED 2026-04-26 — no longer in git history"
# - CLAUDE.md / ruff excludes → remove stale patterns

STEP 6 — Push force (requires --force because history changed)
git push --force origin main
git push --force origin refs/tags/*:refs/tags/*  # tags were rewritten too
git push --force origin other-branch:other-branch  # if applicable

STEP 7 — Verify on GitHub
# Check no commits reference the directory
git log --all --oneline -- path/  # must return 0
# Verify GitHub SHA matches
curl https://api.github.com/repos/USER/REPO/commits?per_page=1
```

## Critical Gotchas

**Gotcha 1: Remote not configured**
```bash
# git-filter-repo needs a remote to exist — may need to add
git remote add origin https://github.com/USER/REPO.git
# or check: git remote -v
```

**Gotcha 2: Branch checked out blocks push to local remote**
```bash
# ERROR: remote rejected main -> main (branch is currently checked out)
# Fix: push to origin (GitHub) only, not to /root/arifOS/.git style local remotes
git push --force origin main
```

**Gotcha 3: Tags are rewritten too — need to push separately**
```bash
git push --force origin refs/tags/*:refs/tags/*
```
If you forget this, old tags still reference the old history.

**Gotcha 4: 155+ commits referencing archive/ but grep returns 0 after filter**
This is correct — filter-repo rewrote all commits. The history is gone.

**Gotcha 5: Active code references still exist after "deletion"**
This happens when files in the current tree still reference archive/ paths.
Must be fixed before commit+push — otherwise you're encoding stale references.

**Gotcha 6: "archive/" in session anchors is historical RECORD**
Files in `.claude/sessions/` that reference archive/ are accurate historical records.
Don't erase them — ANNOTATE them with the 2026-04-26 deletion note.
Agents reading session anchors need to know why an old reference is now broken.

## Verification Checklist
```
[ ] 0 commits in git history reference archive/
[ ] All live file references updated to point to new location
[ ] All session anchors annotated with deletion note
[ ] force push sent to origin main + all branches + all tags
[ ] GitHub SHA matches local HEAD
[ ] No active code paths reference the removed directory
```

## This session's results
- archive/ directory: 394 files, 78,981 lines, 155 commits — GONE from history
- 99 tags: all rewritten (tags reference commit content, not paths)
- 15 eureka items distilled into wiki + runtime code
- 4 files updated (wisdom_quotes.py, MEMORY_ROTATION_POLICY.md, 2 session anchors)
- SHA: 9174ade94 pushed to origin/main