# Federation Multi-Repo Git Operations

## When to Use
When executing git/GitHub operations (branch, commit, push, PR, issues) across multiple federation repos simultaneously.

## Trigger Conditions
- 3+ repos need coordinated git operations in one session
- Using `gh` CLI for GitHub issues/PRs
- Federation-wide operations (roadmaps, releases, audits)

## Critical Learnings (Trial-Error Hard-Won)

### 1. Stash Before Branching
```bash
# Stash dirty working trees BEFORE creating feature branches
for repo in arifOS A-FORGE geox WEALTH WELL; do
  cd /root/$repo && git stash push -m "roadmap-wip-$(date +%s)"
done
# Then branch and commit cleanly
```

### 2. GitHub Issue Creation — Use `--body-file` NOT inline body
Shell quoting breaks on special characters, backticks, code blocks, and curly braces in YAML/TypeScript.

```python
# WRONG — shell quoting breaks
subprocess.run(["gh", "issue", "create", "--repo", repo, "--title", title, "--body", body])

# RIGHT — write to temp file, use --body-file
with open("/tmp/body.txt", "w") as f:
    f.write(body)
subprocess.run(["gh", "issue", "create", "--repo", repo, "--title", title, "--body-file", "/tmp/body.txt"])
```

### 3. GitHub Labels — Create Before Adding to Issues
```bash
# Create labels first
for repo in ariffazil/repo; do
  for label in H1 H2 H3 critical governance; do
    gh label create "$label" --repo "$repo" 2>/dev/null || true
  done
done

# THEN add to issues (separate command)
gh issue edit org/repo --issue N --add-label H1,critical
```

### 4. PR Creation After Branch Push — Two-Step
When creating a feature branch and immediately pushing, do NOT use `$(cmd)` in `--head`:
```bash
# WRONG — branch name contains backtick cmd subst, breaks
git push -u origin h1-roadmap-${TS}
gh pr create --repo X --head h1-roadmap-${TS}  # TS already substituted in shell but gh sees wrong refspec

# RIGHT — two commands, two variables
BRANCH="h1-roadmap-$(date +%s)"
git checkout -b "$BRANCH" && git push -u origin "$BRANCH"
gh pr create --repo X --head "$BRANCH" --base main
```

### 5. `git add` + `git commit` = "nothing to commit"
Pre-commit hooks can auto-commit files during the `git add` step. `git commit` then finds nothing to commit. Always check `git log --oneline -1` after "failed" commit — it may have already succeeded.

```bash
git add ROADMAP.md && git commit -m "..." || true
git log --oneline -1  # Check if commit actually happened
git push -u origin h1-roadmap-XXXX  # Proceed regardless
```

### 6. AAA Repo Branch — Not `main`
```bash
# WRONG — AAA default branch is canon/hermes-memory-v1, not main
gh pr create --repo AAA --base main

# RIGHT — check current branch first
cd /root/AAA && git branch --show-current
# Use whatever branch you're on as --base
gh pr create --repo ariffazil/AAA --base $(git branch --show-current)
```

### 7. Repo Path Casing on Linux
```python
# WRONG — Python subprocess path expansion
cwd=f"/root/{repo.split('/')[1]}"  # "wealth" fails

# RIGHT — WEALTH is uppercase on filesystem
cwd=f"/root/{repo.split('/')[1].upper()}"  # for WEALTH
# Or use a path mapping
PATH_MAP = {"arifOS": "/root/arifOS", "WEALTH": "/root/WEALTH", ...}
```

### 8. Push Branch Before PR
GH API needs the branch to exist on remote before creating PR:
```bash
git push -u origin "$BRANCH"  # Must happen first
gh pr create --repo X --head "$BRANCH" --base main  # Then this works
```

## Sequencing Template
```
1. gh auth status  (verify logged in)
2. git stash (all repos, dirty trees)
3. for each repo:
   a. git checkout -b feature-branch
   b. git add TARGET_FILE
   c. git commit -m "..."
   d. git log --oneline -1  (verify commit succeeded)
   e. git push -u origin feature-branch
4. for each repo:
   a. gh pr create --repo X --head branch --base main
5. gh issue create (body-file approach)
6. gh issue edit --add-label (labels created separately)
```

## Verification Commands
```bash
# Check all PRs across repos
for repo in ariffazil/arifOS ariffazil/A-FORGE ariffazil/AAA ariffazil/geox ariffazil/wealth ariffazil/well; do
  gh pr list --repo "$repo" --state open --limit 3
done

# Check all issues
for repo in ...; do
  gh issue list --repo "$repo" --state open --search "H1" --limit 5
done
```

## Pitfalls
- Don't use `--body` with multi-line YAML/TypeScript — use `--body-file`
- Don't chain `$(date +%s)` in `git push --head` — use separate variable
- Don't assume `main` is the default branch — always check
- Don't use lowercase repo paths — Linux filesystem is case-sensitive
- Don't retry a "failed" commit without checking `git log` — pre-commit may have already committed
- Don't create issues with labels that don't exist yet — create labels first

## Related Skills
- `github-pr-workflow`: Bulk PR operations with `gh` CLI
- `git-pre-push-hook-stdin-bug`: Git 2.51.0 stdin issue with hooks
- `repo-secret-blocking-system`: Secrets scanning in CI/CD
