---
name: git-pre-push-hook-stdin-bug
description: Git 2.51.0 pre-push hook stdin issue — hook receives empty stdin over SSH. For routing validation, use CI + branch protection as primary enforcement.
category: devops
---

# git-pre-push-hook-stdin-bug

## The Problem

Git 2.51.0 (confirmed on this system) invokes the pre-push hook with stdin connected to `/dev/null` when the remote is an SSH transport (`git@github.com:...`). The hook's stdin is empty, so it cannot read the standard `<local ref> <local sha> <remote sha>` push data.

**Symptom:** Hook works perfectly when tested manually with `echo "<ref> <sha> <oldsha>" | bash .git/hooks/pre-push`, but fails when invoked by `git push` — the parsed fields are empty.

**Confirmed with strace:** `fd 0 (stdin) content bytes: 0` when invoked by git over SSH.

## Workaround

Do NOT rely on stdin in pre-push hooks for SSH-pushed repos. Two-layer enforcement:

### Layer 1 — Local: Branch name check only
Block direct push to main/master by checking `git branch` output or `GIT_REF` env var.

```bash
#!/bin/bash
set -euo pipefail
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$CURRENT_BRANCH" == "main" || "$CURRENT_BRANCH" == "master" ]]; then
  echo "🛑 Direct push to main blocked. Use feature branch + PR."
  exit 1
fi
echo "✅ Branch check passed: $CURRENT_BRANCH"
```

### Layer 2 — CI: REPO= trailer validation
This is the REAL enforcement for SSH repos.

```yaml
# .github/workflows/repo-routing.yml
name: Repo Routing Validation
on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  validate-routing:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Validate REPO trailer
        run: |
          TARGET_REPO="${{ github.event.pull_request.base.repo.name }}"
          COMMITS=$(git log --format='%H %B' origin/main..HEAD)
          echo "$COMMITS" | while IFS= read -r sha body; do
            DECLARED=$(echo "$body" | grep -i "^REPO=" | sed 's/^REPO=//i' | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]')
            if [ "$DECLARED" != "${TARGET_REPO,,}" ]; then
              echo "❌ $sha: REPO mismatch"
              exit 1
            fi
          done
```

### Layer 3 — GitHub Branch Protection (mechanical backstop)
Set via API:
```bash
curl -X PUT -H "Authorization: token $GH_TOKEN" \
  -H "Content-Type: application/json" \
  https://api.github.com/repos/ariffazil/{REPO}/branches/main/protection \
  -d '{
    "required_pull_request_reviews": {"required_approving_review_count": 1},
    "restrictions": null,
    "require_linear_history": true,
    "allow_force_pushes": false
  }'
```

## What DOESN'T Work

- `while read local_ref local_sha remote_sha; do ... done < /dev/stdin` — stdin is empty
- `stdin_data=$(cat)` — empty
- `read -t 1 line` — times out, no data
- **New branch pushes** (first push of a feature branch): `${OLD_REMOTE_SHA}..${LOCAL_SHA}` gives "fatal: Invalid revision range 0000000..abc..." because OLD_REMOTE_SHA is all zeros. Must handle as special case:
```bash
if [ "$OLD_REMOTE_SHA" = "0000000000000000000000000000000000000000" ]; then
    git log --format='%B' "$LOCAL_SHA" > "$BODY_FILE"
else
    git log "${OLD_REMOTE_SHA}..${LOCAL_SHA}" --format='%B' > "$BODY_FILE"
fi
```

## `set -euo pipefail` Gotcha

With `set -e`, an empty `read` (because stdin is /dev/null) causes the script to **exit immediately** at the `read` line. Workaround: always provide a fallback or use `|| true`:
```bash
while read local_ref local_sha remote_sha; do
    # work
done < /dev/stdin || true  # prevents set -e from killing the loop
```

## Key Debugging Technique

```bash
# Test with simulated push data
echo "refs/heads/feat/test abc123defsha456 0000000000000000000000000000000000000000" | \
  bash .git/hooks/pre-push

# Verify git passes data correctly
GIT_TRACE=1 git push -u origin feat/test 2>&1 | grep -A2 "pre-push"
```

## SSH vs HTTPS Transport — Critical Distinction

The stdin buffering bug is **SSH-specific**. Over HTTPS (`https://github.com/...`), stdin is passed correctly. Over SSH (`git@github.com:...`), stdin is empty.

To verify:
```bash
git remote -v | grep push
# If git@github.com → SSH → stdin bug applies
# If https://github.com → HTTPS → stdin works normally
```

## New Branch Push Special Case

When pushing a brand-new branch (first push), `OLD_REMOTE_SHA` is literally `0000000000000000000000000000000000000000`. This is valid — it means "no previous ref". Handle it explicitly:
```bash
if [ "$OLD_REMOTE_SHA" = "0000000000000000000000000000000000000000" ]; then
    # New branch — get ALL commits on this branch
    git log --format='%B' "$LOCAL_SHA" > "$BODY_FILE"
else
    # Updating existing branch
    git log "${OLD_REMOTE_SHA}..${LOCAL_SHA}" --format='%B' > "$BODY_FILE"
fi
```
Using `"${OLD_REMOTE_SHA}..${LOCAL_SHA}"` when OLD_REMOTE_SHA is all zeros gives: `fatal: Invalid revision range 0000000..abc123...`.

## Verified Fix Sequence (2026-05-02)

1. Branch name check (works over SSH) — blocks direct main push
2. CI REPO= trailer validation (HTTPS GitHub Actions) — real enforcement
3. GitHub branch protection (API) — mechanical backstop

All three layers together give complete coverage despite the SSH stdin bug.

## Key Debugging Technique

When stdin seems to work manually but not via git:
```bash
# Confirm stdin is /dev/null during git push
cat > .git/hooks/pre-push <<'HOOK'
#!/bin/bash
echo "fd 0 is TTY: $([ -t 0 ] && echo yes || echo no)"
echo "fd 0 byte count: $(dd if=/dev/stdin bs=1 count=1 2>/dev/null | wc -c)"
# If byte count = 0 and not TTY → git 2.51.0 stdin bug
HOOK
```

## GitHub Token for Branch Protection API

Get token: `gh auth token`
Store: `GH_TOKEN` env var or `gh config get github.token`

## Trigger Conditions

- Git push over SSH (`git@github.com:...`) fails silently
- Hook validated manually but blocks during actual push
- `GIT_TRACE=1` shows hook runs but stdin is empty
