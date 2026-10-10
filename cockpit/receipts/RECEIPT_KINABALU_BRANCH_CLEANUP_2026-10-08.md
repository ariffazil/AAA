# RECEIPT — Kinabalu branch cleanup

**Time:** 2026-10-08 09:55 UTC
**Trigger:** Arif's "Go: cleanup branches (with approval)" at 09:54 UTC.

## What was deleted

| Branch | Before | After |
|---|---|---|
| `origin/feat/kinabalu-xsection-models` | existed (`be0d018`) | deleted |
| `origin/feat/kinabalu-refine` | existed (`52b1d98`) | deleted |
| `origin/feat/kinabalu-refine-squashed` | existed (`bdfd825`) | deleted |
| `feat/kinabalu-xsection-models` (local) | existed (`be0d018`) | deleted |
| `feat/kinabalu-refine` (local) | existed (`52b1d98`) | deleted |
| `feat/kinabalu-refine-squashed` (local) | existed (`bdfd825`) | deleted |

The three branches were content-equivalent to commits already on
`origin/main` (`52b1d98` for the two refinement branches,
`be0d018` for the cross-section branch — `be0d018` is now an
ancestor of `52b1d98` via the merge). Deletion is lossless.

`origin` was pruned (`git remote prune origin`) to drop the
remote-tracking refs.

## Final state

```
local branches:   main only
remote branches:  origin/HEAD -> origin/main, plus unrelated
                  branches (audit-2026-08-06, chore/*, ci/*, dependabot/*)
origin/main:      52b1d98  (4 commits of refinement on top of be0d018)
local main:       52b1d98  (synced)
tags:             v2026.10.08 (auto), v2026.10.08-kinabalu (manual)
```

## Unreachable commits (held, NOT garbage-collected)

`git fsck --unreachable --no-reflogs` reports two unreachable commits
in the local repo:

- `d5a3952617c2e4c296c23979295e2f74ff9598fc` — the original
  `feat/kinabalu-xsection-models` tip that I cloned at the start
  of the session. Became unreachable when I rebased the amendment
  (`15bde1c`) onto Arif's force-pushed `32b454a`; `d5a3952`'s
  content is duplicated in `32b454a` (same diff, different SHA due
  to force-push metadata).
- `15bde1c02609fc30af674f38087e7bf4b38a1a06` — the pre-rebase
  amendment commit. Became unreachable when the rebase replayed it
  as `be0d018` onto `32b454a`.

Both are content-equivalent to commits already on `main`. They are
**not garbage-collected** in this receipt (no `git gc --prune=now`
run) because gc is irreversible and the session already carries
several F2/F13 scars; preserving them as orphans costs almost
nothing and lets future auditors trace the full session history if
needed.

Arif's call whether to gc them. The `git gc` command to run on his
laptop (one line, irreversible):

```bash
git reflog expire --expire=now --all && git gc --prune=now --aggressive
```

## What was NOT done (held)

- No `git gc` (irreversible; held for Arif's word).
- No re-tag of `v2026.10.08-kinabalu` onto `52b1d98` (held; tag
  still names a reachable commit so it is technically fine).
- No VPS deploy (Arif's laptop, agent has no SSH key).
- No further mutation.

## Membrane compliance

- F1 AMANAH: deletion is documented; remote branches can be
  restored within GitHub's 90-day window from trash if needed.
- F11 AUDITABILITY: this receipt + the 5 prior ones in
  `/root/AAA/cockpit/receipts/`.
- F13 SOVEREIGN: deletion executed under Arif's explicit
  "cleanup branches (with approval)" word.
