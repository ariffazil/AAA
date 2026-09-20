# Deep recipe — attribute, snapshot, verify

Read-only through Step 1. Step 2+ are mutations that need authority and one writer.

## 1. Attribute a blob to refs

```bash
cd <repo>

# history-wide: every blob reachable from ANY ref
git rev-list --objects --all \
 | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' \
 | awk '$1=="blob" && $3>2000000 {printf "%.1fMB %s %s\n",$3/1048576,$2,$4}' | sort -rn | head -40

# per-checkout: what one ref actually contains
git ls-tree -r --long <ref> | awk '$4>2000000 {printf "%.1fMB %s\n",$4/1048576,$5}' | sort -rn

# which commits introduced a path, which refs carry them
git log --all --oneline -- <path>
git branch -a --contains <commit>
```

Branch-scoped case → `git branch -D <branch>` then `git gc --prune=now`; verify with
`git ls-tree -r --long <surviving-ref> | awk '$4>50000000'` (should be empty) and an unchanged
`git rev-list --count <surviving-ref>`.

## 2. What filter-repo leaves behind

```bash
ls .git/filter-repo/   # commit-map, ref-map, changed-refs, first-changed-commits, already_ran
head -3 .git/filter-repo/commit-map ; wc -l .git/filter-repo/commit-map
grep -E "refs/heads/main|refs/stash" .git/filter-repo/ref-map
git remote -v          # filter-repo removes origin — re-add it
```

`ref-map` is how you prove which refs moved (main included) and to what: old-SHA → new-SHA, one line
per ref. Copy all of it out of `.git` into the backup dir; it is the only bridge from an old SHA (a
tag, a VAULT entry, an external citation) to the object that now exists.

## 3. Pin

```bash
git fsck --no-progress --dangling > /tmp/dangling.txt   # lists, does not protect
for s in $(awk '/dangling commit/{print $3}' /tmp/dangling.txt); do
  git log -1 --format='%ad %h %s' --date=short "$s"    # what would be lost
  git reflog show --all | grep -c "$s"                   # 0 = reflog will not save it
done
git update-ref refs/keep/<name> <sha>                   # pin it
git cat-file -t <sha>                                   # confirm it is still there NOW
```

A dangling commit with no reflog entry — a dropped stash, a removed worktree head — is one
`gc --prune=now` from being unrecoverable, and a `filter-repo` run does exactly that prune. Pin the
moment you see it, not after you finish reading.

## 4. Snapshot with proof

```bash
D=/root/backups/<repo>-pre-rewrite-$(date +%Y%m%d) ; mkdir -p "$D" ; cd <repo>
git bundle create "$D/<repo>-ALL-REFS.bundle" --all
git bundle list-heads "$D/"*.bundle | head -40   # --all omits refs/stash and worktrees/*/HEAD
git bundle verify "$D/"*.bundle | tail -2        # expect "records a complete history"
sha256sum "$D/"* > "$D/SHA256SUMS.txt"

# prove recovery, do not assume it
git clone --bare --quiet "$D/"*.bundle /root/backups/<repo>-probe.git
cd /root/backups/<repo>-probe.git && git cat-file -t <sha>
```

Manifest in the backup dir: what was evicted and why, sha256 of every surviving copy, which objects
are *verified recoverable* (proved by the clone above), which are *unrecoverable*, and which backup is
the **sole** carrier of a ref nothing else holds.

## 5. Verify the post-state

```bash
du -sh .git ; git count-objects -vH
for p in <evicted paths>; do printf '%s -> %s commits\n' "$p" "$(git log --all --oneline -- "$p" | wc -l)"; done
git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectsize) %(rest)' \
 | awk '$1=="blob" && $2>1500000' | sort -rn | head
git remote -v ; git for-each-ref | wc -l ; git status -s | wc -l
```

Evicted path → **0 commits across all refs** is the receipt that it left history rather than the tree.

## 6. Reporting template

```
scope      : <N> commits on <branch>  |  history-wide rewrite over <N> refs
axis       : git rev-list --count <A>..<B> (ahead) / HEAD (depth) / ls-tree (files)
evicted    : <paths> (<sizes>)
retained   : <paths> (<sizes>) — still tracked, needs a decision, not a rewrite
backed up  : <dir> sha256=<…> per artefact
recoverable: <objects> — proved by bare-clone of <bundle>
UNRECOVERABLE: <objects> — absent from live repo, scratch clones and the operator mirror
snapshot   : every figure above was read <before|after> the rewrite at <time>
authority  : push decision pending owner; local audit ends at this verdict
```
