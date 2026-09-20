# Recovery verification recipes

Read-only probes for the rewrite discipline in SKILL.md Step 3.5. The only write here is the
`refs/keep/*` creation, which exists to make an object unprunable.

## 1. What is at risk right now

```bash
# unreferenced commits (a report, not a lock — the next gc still deletes them)
git fsck --no-progress --dangling | awk '/dangling commit/{print $3}' \
  | while read -r s; do git log -1 --format='%ad %h %s' --date=short "$s"; done | sort

# is anything protecting them?  hits=0 means an unreachable object = prunable
git reflog show --all 2>/dev/null | grep -c "$sha"

# stash stack + worktrees (forgotten when bundling)
git stash list; git worktree list
```

## 2. Pin, then prove the pin

```bash
git update-ref refs/keep/<label> <sha>
git for-each-ref refs/keep                        # read the ref back
git rev-list --objects refs/keep/<label> | wc -l  # reachable ⇒ gc-safe

git bundle create <dir>/<label>.bundle refs/keep/<label>
git bundle verify <dir>/<label>.bundle      # pass line: "records a complete history"
git bundle list-heads <dir>/<label>.bundle  # coverage — the refs you actually need
git tag -f -m "<why>" KEEP-<label> <sha>    # -m is mandatory; without it git opens an editor and hangs
```

## 2b. Bundle coverage for a whole repo

```bash
git bundle create <f>.bundle --all
git bundle list-heads <f>.bundle | grep -E 'stash|worktrees|refs/heads/(main|<branch>)'
```

A ref absent from `list-heads` is absent from the backup — add it to the bundle command, or create a
`refs/keep/*` ref for it first. `--all` never includes dangling objects.

## 3. Prove recoverability (assert nothing)

```bash
git clone --bare --quiet <bundle> /tmp/probe.git && cd /tmp/probe.git
for c in <sha1> <sha2>; do printf '%s -> ' "$c"; git cat-file -t "$c"; done
```

`commit` / `blob` is the proof. `fatal: could not get object info` means the bundle does not carry it —
re-check `list-heads` before blaming the bundle format.

## 4. Was it lost, or did it land?

Given a lost object whose stat you recorded (`git diff --stat <base> <lost>`) and the paths it touched:

```bash
for f in <paths>; do
  printf '%-60s ' "$(basename $(dirname $f))"
  git log --since='<when the object was made>' --format='%h %ad' --date=format:'%m-%d %H:%M' -- "$f" | head -3
  git show <latest-touching-commit> --numstat --format= -- "$f"
done

# or compare sizes per path: object's base commit vs HEAD
git show <base>:"$f" | wc -l ; git show HEAD:"$f" | wc -l
```

A popped stash reappears as a near-exact `+N` match in the later commit. A path reading 0 lines has
usually moved namespace — locate it (`find <root> -name SKILL.md -path '*<name>*'`) before calling it
absent.

## 5. Is this node actually a mirror?

```bash
ls .git/shallow 2>/dev/null                        # present ⇒ truncated history
git config --get remote.origin.partialclonefilter   # blob:none ⇒ blobless clone
ssh <node> "git -C <repo> rev-list --count HEAD; git -C <repo> log -1 --format='%h %ad %s'"
```

A node whose `HEAD` is not an object in your repo, or which reports a small commit count behind a
partial filter, is a **consumer**, not a backup.

## 6. Post-rewrite state capture (before anything else touches `.git`)

```bash
cp -n .git/filter-repo/{commit-map,ref-map,changed-refs,first-changed-commits} <backup-dir>/filter-repo-maps/
grep -E 'refs/heads/main|refs/stash' <backup-dir>/filter-repo-maps/ref-map   # which refs actually moved
git remote -v                                    # filter-repo strips origin — re-add before any push
git count-objects -vH | grep -E 'in-pack|size-pack'
```

`commit-map` (one old→new pair per line) is the bridge that lets a seal, tag citation or ledger entry
quoting an old hash be re-pointed.
