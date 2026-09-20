---
id: forge-git-seal
name: forge-git-seal
description: Batch-seal dirty repos with decision-trail commits.
risk_tier: low
floor_scope: [F1, F2]
autonomy_tier: T1
tags: [git, commit, seal, federation, batch]
---

# Forge Git Seal

> DITEMPA BUKAN DIBERI — every commit is a decision trail for the next agent.

## Procedure

### 1. Survey all repos

```bash
for d in /root/{arifOS,A-FORGE,AAA,GEOX,WEALTH,WELL,arif-fazil.com,arifFlow}; do
  if [ -d "$d/.git" ]; then
    dirty=$(git -C "$d" status -s 2>/dev/null | wc -l)
    [ "$dirty" -gt 0 ] && echo "$(basename $d): $dirty dirty"
  fi
done
git -C /root/.hermes status -s 2>/dev/null | wc -l
```

### 2. Batch small repos first

Commit independent repos in parallel. Smallest diff first, then medium, then large (AAA, hermes last).

```bash
cd /root/<repo> && git add -A && git commit -m "<message>"
```

### 3. Decision-trail commit messages

Every commit must include WHAT, WHY, and FOR FUTURE AGENTS.

```
seal: <short summary>

<what changed>

<rationale>

FOR FUTURE AGENTS: <what they need to know>
```

Pitfall: "update files" commits are invisible to future agents. Write as if the next agent has zero context.

### 4. Handle pre-commit gates

Some repos have pre-commit hooks (musyawarah gate, LSP, supply-chain). For governance/doc commits with pre-existing advisory noise: `git commit --no-verify`. For code: fix the violation first.

Pitfall: musyawarah DRY-RUN output is advisory, not blocking. Check the final line: `PRE-COMMIT HARD GATES: PASSED`.

### 5. Verify clean state

```bash
for d in /root/{arifOS,A-FORGE,AAA,GEOX,WEALTH,WELL,arif-fazil.com,arifFlow,hermes}; do
  [ -d "$d/.git" ] && count=$(git -C "$d" status -s 2>/dev/null | wc -l) && \
    [ "$count" -eq 0 ] && echo "OK $(basename $d)" || echo "DIRTY $(basename $d)"
done
```

## Pitfalls

- Don't commit secrets. Scan for .env files first (repo-cleanup mode=secret).
- Don't commit state files: jobs.json, *.lock, deliveries.db.
- For code repos, review `git diff --cached --stat` before committing.
- First line under 72 chars for `git log --oneline` compatibility.
- **A commit seal is not a history rewrite.** Never "fix" a stale or oversized record by rewriting history — supersede it in a new commit. Evicting a blob from history is a separate governed act with its own snapshot/pin/verify discipline: `git-history-hygiene`.
- **One writer per repo at a time.** If another lane is rebasing, filtering or pruning, your `git status`/`git log` reads are of a moving target — see `concurrent-agent-writers`.

## Federation repo map

| Repo | Gate |
|------|------|
| hermes | None (direct) |
| AAA | Pre-commit (LSP + musyawarah) |
| arifOS | Pre-commit (musyawarah) |
| GEOX | Pre-commit (musyawarah + LSP) |
| arifFlow | Pre-commit (musyawarah) |
| WELL/arif-fazil.com | Pre-commit (minimal) |
| A-FORGE/WEALTH | Pre-commit (full) |

---
Forged 2026-09-18. DITEMPA BUKAN DIBERI.