---
name: git-history-hygiene
description: "Use when evicting blobs or rewriting a git history."
version: 1.0.0
risk_tier: medium
floor_scope: [F1, F2, F7, F13]
triggers:
  - "this repo is too big"
  - "there is a huge file in git history"
  - "strip a file from git history"
  - "filter-repo"
  - "git gc / prune"
  - ".git is hundreds of megabytes"
  - "remove a blob from history and push"
  - "which branch carries this big file"
---

# Git History Hygiene

Evicting content from a git **history** is a different act from deleting it from a working tree, and
from committing a change. It moves every ref, breaks every SHA anyone has quoted, and leaves every
clone divergent. Treat it as a governed mutation, not as cleanup.

> Companion: `concurrent-agent-writers` — a `.git` under concurrent writers (a rewrite running while
> another lane reads) is a shared-state hazard; that skill carries the freeze-and-pin discipline.

## Always-on rules

1. **Attribute before you scope.** A blob's *history-wide* reachability (`rev-list --objects --all`)
   and a ref's *tree* contents (`ls-tree -r <ref>`) are different questions. Answer both, then scope
   the fix to the smallest one that removes it.
2. **Prefer the branch-scoped fix.** If one branch carries the blob and main does not, delete the
   branch and `gc --prune=now` — main's hash is unchanged and no clone desyncs. A history-wide rewrite
   is the fallback for a blob that many refs or tags carry.
3. **A history-wide rewrite invalidates every prior claim about the repo.** `git filter-repo` rewrites
   heads, remotes, tags and stash; therefore "main is unchanged", "no force-push needed" and "tags are
   untouched" are all false the moment it runs. Describe what the rewrite did, not what was intended.
4. **The rewrite's own map is the only pre→post hash bridge.** `.git/filter-repo/commit-map` (plus
   `ref-map`) must be copied **outside `.git`** as part of the operation — a later `gc` or rerun
   discards it, and without it old tag, ledger and external-document SHAs are unmappable forever.
5. **Pin before anything can prune.** An unreferenced object is not protected by having been observed
   or listed. `git update-ref refs/keep/<name> <sha>` (or `git stash store <sha>`), then verify with
   `git cat-file -t <sha>`. Do this *before* the rewrite, not after you notice something is gone.
6. **Snapshot with proof, not with hope.** `git bundle create … --all` then `git bundle list-heads` —
   `--all` omits `refs/stash` and `worktrees/*/HEAD` unless they are listed. Prove the objects are
   actually inside by bare-cloning the bundle and running `git cat-file -t <sha>` in the clone.
   "The bundle exists" ≠ "the object is in it".
7. **Every figure carries its snapshot and its axis.** `rev-list --count main..HEAD` (ahead),
   `rev-list --count HEAD` (total depth) and `ls-tree -r | wc -l` (files) are all "the number of
   commits/files"; quote the command's axis beside the integer, and say whether the reading predates
   or postdates the rewrite.
8. **Push is not the auditor's call.** Local read-only analysis ends at a verdict. Force-pushing a
   rewritten history is an owner decision with a divergence cost for every clone — present it as one,
   never execute it as cleanup.
9. **Keep the artifact outside git when its generator is missing.** A big file labelled
   "regenerable" in a commit message is only regenerable if the generator exists; if the script is
   gone, move the artifact to a backup dir and keep it there until the generator is found.

## Procedure

1. **Read the object store.** `du -sh .git`, `git count-objects -vH`, `git reflog --date=iso | head`,
   `git worktree list`, `git stash list`. Check for `.git/filter-repo/` — an existing `already_ran`
   means a rewrite has already happened and the repo is in post-rewrite state.
2. **Enumerate the big blobs, both ways** (rule 1). Keep the top ~20 by size with their paths.
3. **Attribute each path to refs** — `git log --all --oneline -- <path>`, `git branch -a --contains
   <commit>`. A path can exist at HEAD while absent from history, or the reverse.
4. **Snapshot + pin** (rules 5, 6) into a dated backup dir with a `sha256sums` file and a written
   manifest: evicted / retained / verified-recoverable / UNRECOVERABLE.
5. **Declare the scope** — branch-scoped delete, or history-wide rewrite — with the commit count and
   the ref list in the same sentence.
6. **Execute (authority required), one writer at a time.** `filter-repo` removes the `origin` remote:
   re-add it and confirm with `git remote -v`.
7. **Verify the post-state**, not the intent: per evicted path, `git log --all --oneline -- <path>`
   must return **0 commits** (left history, not just the tree); re-read `.git` size, biggest surviving
   blob, ref heads and the restored remote.
8. **Report by disposition** — evicted · still present · backed up (sha256) · verified recoverable ·
   UNRECOVERABLE — and label any unverifiable overlap `possible loss`, never "lost work" and never
   "nothing was lost".

## Pitfalls

- **Rewriting history to fix a stale record.** A record correct when written and later superseded is
  `STALE`, not false. Supersede it in place; history is not the repair surface.
- **Assembling the backup after the rewrite.** Order is: snapshot → pin → verify the snapshot → act.
  Anything pruned between your probe and your backup command is unrecoverable, and the window is
  minutes, not days.
- **A bundle is not a mirror.** A `--all` bundle from one ref set does not carry another ref set's
  refs; check `list-heads` before assuming a given SHA is inside.
- **Auditing a live target.** If refs moved between your own two commands, you measured a moving
  object: re-probe, name the snapshot, and require the writer to declare `DONE` with a receipt first.
- **Trusting the count over the axis.** When challenged on a commit count, re-read which axis the
  command measured before retracting it — retracting a correct number is the same defect as asserting
  a wrong one.

Deep command recipe, worked end-to-end: `references/git-history-rewrite-audit.md`.
