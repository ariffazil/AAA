---
name: multi-repo-dirty-state-cleanup
description: Cleans dirty git state after removing tracked files across arifOS federation repos. Use when git status shows deleted files as dirty but rm was already run.
tags: [git, cleanup, arifOS-federation]
version: 2026.05.01
---

# multi-repo-dirty-state-cleanup

Cleans dirty git state across arifOS federation repos after removing files that were tracked by git.

## Trigger

- `git status` shows files as "not staged" dirty but `rm -f <file>` was already run
- Files deleted from disk but still showing as tracked/modified in `git status`
- Large directories (hermes/, state/, briefings/) need removal from both disk AND git

## Symptom

```
$ rm -f .push_test
$ git status
Changes not staged for commit:
  deleted: .push_test          ← misleading dirty state
```

## Root Cause

`rm -f` removes the file from disk but git still tracks it. The deletion must be **staged** before git considers the working tree clean.

## Standard Cleanup Pattern

```bash
# 1. Stage the deletion (git needs to know the file is gone)
git add <file>           # staging deletion = telling git "this file was removed"
git add <directory>/     # for directories

# 2. Verify clean
git diff --quiet && echo "CLEAN" || echo "DIRTY: $(git diff --name-only)"

# 3. Commit + push
git commit -m "<type>: remove <description>"
git push
```

## Staged Deletion vs Unstaged Deletion

| Command | Effect on disk | Effect on git | Use when |
|---------|---------------|---------------|---------|
| `rm -f <file>` | Deleted | Still tracked → dirty | Never alone |
| `git rm <file>` | Deleted | Staged for commit | File should be gone entirely |
| `git rm --cached <file>` | Kept on disk | Staged (untracked) | File stays locally but removed from git |
| `git add <file>` (after rm) | Already gone | Staged deletion | File already deleted, just stage it |

## Real-World arifOS Cleanup (2026-05-01)

Removing large tracked directories that shouldn't be in git:

```bash
# Move sensitive content to VAULT999 first
cp -r briefings/ /root/VAULT999/briefings_backup/

# Remove from git tracking (keep disk copy initially for safety)
git rm -r --cached hermes/ hermes-backup/ state/ briefings/

# Now remove from disk
rm -rf hermes/ hermes-backup/ state/ briefings/

# Verify what's tracked
git ls-files | grep hermes

# Stage the disk deletions if not already
git add hermes/ hermes-backup/ state/ briefings/

# Commit + push
git commit -m "chore: remove tracked noise files"
git push
```

## Verification Checklist

After cleanup:
- [ ] `git diff --quiet` returns 0
- [ ] `git status` shows only clean or "nothing to commit"
- [ ] `git push` succeeds
- [ ] Downstream CI still works

## Key Experiential Finding

`.push_test` was tracked by git. After `rm -f .push_test`, git still showed it as "deleted" dirty. The fix: `git add .push_test` stages the deletion, making the working tree clean. This is NOT intuitive — `rm -f` should remove the file but git tracks content, not files. The deletion must be explicitly staged.
