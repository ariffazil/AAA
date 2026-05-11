---
name: git-rescue-contaminated
description: Rescue a git push when the local working directory is contaminated with hundreds of uncommitted files and won't fast-forward.
triggers:
  - "git push rejected"
  - "non-fast-forward"
  - "contaminated git"
  - "can't push"
  - "device or resource busy"
category: devops
---

# Git Rescue — Contaminated Working Directory

## Problem
Local git working directory has hundreds of uncommitted changes from prior sessions. Push fails:
```
! [rejected] main -> main (non-fast-forward)
error: failed to push some refs
hint: Updates were rejected because a pushed branch tip is behind its remote
```

Or `git reset --hard origin/main` fails:
```
error: unable to unlink old 'Caddyfile': Device or resource busy
fatal: Could not reset index file to revision 'origin/main'.
```

## Root Cause
A file is locked by an external process (e.g., bind-mounted Caddyfile locked by the Caddy Docker container). `git reset --hard` requires writing to every file in the working tree, so it fails on any locked file.

## Solution Sequence

### Step 1: `git reset --soft` (if contamination is moderate)
```bash
git reset --soft origin/main   # moves HEAD only, PRESERVES working tree
```
This never touches the filesystem — it only moves the index/HEAD. Locked files don't matter.

Then stage and commit only your intended change:
```bash
git add path/to/only-your-change.py
git commit -m "your message"
git push origin main
```

### Step 2: If `reset --soft` also fails (too many conflicting files)
Clone fresh to a temp directory, apply your patch there:
```bash
cd /tmp
rm -rf arifos-fresh
git clone --depth=1 https://github.com/ariffazil/arifos.git arifos-fresh
# apply your patch in /tmp/arifos-fresh/
cd arifos-fresh
git add <your-changed-files>
git commit -m "your message"
git push origin main
```
The fresh clone has zero contamination — push succeeds.

### Step 3: If you need to preserve a locked/bind-mounted file
```bash
# Copy it aside first
cp Caddyfile /tmp/Caddyfile.preserve
# Now git can reset
git reset --hard origin/main
# Restore the bind-mounted file
cp /tmp/Caddyfile.preserve Caddyfile
```

## Never Do These
- `git reset --hard` — requires unlinking every working tree file; fails on any locked file
- `git pull --no-rebase` — pulls ALL contaminated changes into history
- `git push --force` without fixing local state — just masks the problem
- `git checkout-index -f -a --` — same unlink problem as reset --hard
- `git update-index --assume-unchanged <file>` — git refuses to mark bind-mounted files

## Key Insight
`git reset --soft origin/main` is the safe path because it **only moves pointers** (HEAD, index). It never opens or modifies a single file in the working tree. The contaminated working tree stays exactly as-is until you explicitly stage a file.

## See Also
- `vps-architecture-audit` skill — for the broader context of VPS component auditing
