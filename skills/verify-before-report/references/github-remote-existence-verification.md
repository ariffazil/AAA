---
title: GitHub Remote Existence Verification Pattern
category: verify-before-report
date: 2026-08-11
author: verified by human correction
tags: [git, github, remote-existence, verification-pattern]
---

# GitHub Remote Existence Verification — Session Record (2026-08-11)

**Context:** OpenCode session audit claimed "✅ pushed to github.com/ariffazil/FED/FLAME/FRAME" but NONE of these repos existed on GitHub at time of report.

**Root cause:** Agent checked `git config --get remote.origin.url` and saw configured URL, then assumed "remote exists" without verifying the REMOTE IS ACTUAL EXISTENT GITHUB REPO.

**Lesson:** Local git remote configuration ≠ actual GitHub repository existence. Always probe live GitHub before claiming "pushed."

---

## The Failure Pattern (WHAT HAPPENED)

| Step | What agent did | What was wrong |
|------|----------------|----------------|
| 1. Check local state | `git status --short` → clean | ✅ Correct |
| 2. Check remote URL | `git config --get remote.origin.url` → shows `git@github.com:ariffazil/XXX.git` | ✅ Shows URL |
| 3. CLAIM | "✅ pushed to github.com/ariffazil/XXX" | ❌ **REMOTE NOT VERIFIED** |
| 4. Human asks | "Why GitHub FRAME not found?" | ❓ Exposes failure |

**The gap:** Step 2 only proves the *URL* is configured. It does NOT prove the *repository exists* on GitHub. A missing repo returns 404; a private repo you lack access to also returns error but agent never probed.

---

## The Correction Pattern (HOW TO FIX)

```bash
# After configuring or pushing to remote, ALWAYS verify the repo exists:

ORG="ariffazil"
REPO="FRAME"

# METHOD 1: curl health check (quick, works for public repos)
curl -sfI "https://github.com/$ORG/$REPO" >/dev/null && echo "$ORG/$REPO EXISTS ✅" || echo "$ORG/$REPO NOT FOUND ❌"

# METHOD 2: git ls-remote (works even if private, requires auth)
git ls-remote "https://github.com/$ORG/$REPO.git" HEAD >/dev/null 2>&1 && echo "$ORG/$REPO ACCESSIBLE ✅" || echo "$ORG/$REPO UNACCESSIBLE ❌"

# METHOD 3: GitHub API (official, rate-limited but reliable)
curl -sf "https://api.github.com/repos/$ORG/$REPO" -H "Accept: application/vnd.github.v3+json" | jq '.exists' 2>/dev/null || echo "API RESPONSE FAILED"
```

**Mandatory verification sequence for ANY repo claim:**
1. `git log --oneline -1` → local commit exists
2. `git remote -v` → remote configured
3. `curl -sfI https://github.com/<org>/<repo>` → repo exists (or `ls-remote` if private)
4. ONLY THEN claim: "Pushed to X" / "Repo ready"

---

## Multi-Repo Audit Recipe (for batch operations like FED+FLAME+FRAME)

When auditing multiple repositories in one pass:

```bash
# Define target list
REPOS=("FED" "FLAME" "FRAME")
ORG="ariffazil"

echo "=== MULTI-REPO VERIFICATION ==="
for repo in "${REPOS[@]}"; do
  echo "--- $repo ---"
  
  # 1. Local git state
  cd "/root/$repo" && git log --oneline -1 2>/dev/null | head -1 || echo "NO LOCAL COMMITS"
  
  # 2. Remote configured?
  remote=$(git config --get remote.origin.url 2>/dev/null)
  test -n "$remote" && echo "Remote: $remote" || echo "NO REMOTE CONFIGURED"
  
  # 3. Does GitHub repo exist?
  if curl -sfI "https://github.com/$ORG/$repo" >/dev/null 2>&1; then
    echo "✓ EXISTS ON GITHUB ✅"
  else
    echo "✗ NOT FOUND ON GITHUB ❌"
  fi
  
  echo
done
```

This is the pattern the failed session should have run before reporting.

---

## Prevention: Never Trust Git Config Alone

Git config stores URLs locally. They can be:
- Pointing to nonexistent repos
- Pointing to repos you don't have write access to
- Pointing to stale/cached remotes after manual changes

Always probe GitHub as final authority. Git config = client state; GitHub API = server truth.

---

## Session ID for Reference
- opencode session: `ses_00fe18e70ffee4OynFRyIBeyXV`
- Timestamp: 2026-08-11T18:33 MYT
- Report author: verified via human correction ("Why GitHub FRAME not found?")

DITEMPA BUKAN DIBERI.
