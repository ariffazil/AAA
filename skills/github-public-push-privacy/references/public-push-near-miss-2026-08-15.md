# Public-Push Near-Miss — 2026-08-15

## The trigger

Arif: "Push la" after a big forge session (wawa fallback-chain fix, v0.20.1 carry rebase, ghost-skill cleanup). Two repos had uncommitted work: arifOS (clean — one code fix + manifest) and HERMES (218 files).

## What happened

1. arifOS pushed clean. LSP gate ran, secret scan clean.
2. HERMES was diverged ahead 1 / behind 1 with **identical trees** (same entropy fix committed twice — once locally as a re-worded duplicate of remote). Resolved with tree-hash check + `git reset --soft origin/main`. Zero force-push.
3. Bulk `git add -A` (with exclusions that **failed silently** — the pathspec-exclusion form didn't match, everything got staged) committed 218 files: 12.5k insertions.
4. Secret scan on the commit: one hit — `sk-Nat` — which turned out to be "Multitask-National Speech Corpus" research prose. **False positive. Scan declared clean.**
5. Push landed. Post-push file-class review found the real leak:
   - `media/abang_sado_shadow_HD*.png`, `media/arif_hd_edit.png`, `media/arif_muscular_v1.png`, `media/arif_silhouette_*.png` — private body-edit/shadow images
   - `profiles/aaa-hermes/memories/MEMORY-sin.md` — a third person's private memory file
   - `cron/executions.db`, `cron/notepad.db*` — runtime SQLite state
   - Repo is **public** (`gh repo view` → `isPrivate: false`)

## Why the secret scan passed

It scanned for key-shaped CONTENT. The leak was by FILE NAME/class. Privacy scanning needs a path-class scan first: `media/`, `memories/MEMORY-`, `*.db`, `*.png`, `cache/`.

## Why the files were staged at all

- The exclusion pathspec `':!media/'` form failed silently under the multi-pathspec `git add` — the `|| git add -A` fallback swallowed it and staged EVERYTHING. Lesson: **verify `git status -s` AFTER staging, BEFORE commit** — the status output did show `media/` and `.db` files staged, and it was skimmed, not read.
- Older `memories/*.md` files were already tracked in the repo (remote `origin/main` had `memories/MEMORY.md`, `USER.md`) — precedent created false comfort. Precedent ≠ permission for NEW third-person memory files.

## Remediation presented (sovereign decision)

1. Flip repo private (recommended — 1 command, keeps history)
2. History rewrite + force-push main (T3 HOLD)
3. Accept exposure

## Verified working techniques from this session

- Tree-hash identical-divergence resolution (see SKILL.md)
- `git update-ref` for rollback anchors when `tag.gpgsign=true` forces an editor
- `gh repo view --json visibility,isPrivate` as the pre-push visibility check
- 60-char context verification for secret-scan hits before declaring leak
