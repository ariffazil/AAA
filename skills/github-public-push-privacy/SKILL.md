---
name: github-public-push-privacy
version: 1.0.1
author: Hermes Agent
license: MIT
description: "Use before any git push to a public GitHub repo."
metadata:
  hermes:
    tags: [github, git, privacy, secrets, push, public-repo, opsec]
    related_skills: [github-pr-workflow, FORGE-secret-hygiene]
---

# GitHub Public-Push Privacy Gate

## When to Use

- Before ANY `git push` to a public GitHub remote (federation repos on github.com/ariffazil/* are public) — including direct "push" orders from the operator.
- When a worktree mixes code with private media, per-person memory files, or runtime SQLite state.
- When local/remote are diverged and you suspect identical content.

Federation repos (github.com/ariffazil/*) are PUBLIC. The worktrees they live in also hold private material: generated media (body-edit/shadow images), per-person memory files (`MEMORY-<name>.md`, `USER-*.md`), lane configs with TTS/persona detail, and runtime SQLite state. A broad `git add -A` + a secret-pattern scan is NOT sufficient protection — privacy leaks leak by FILE NAME/class, not by key shape.

**Forged from a real near-miss (2026-08-15):** one 218-file commit carried shadow body-edit images, a third person's memory file, and runtime DBs to a public repo. The secret scan passed — the leak was by filename. Caught only AFTER push; remediation then required a sovereign decision (history rewrite vs private flip vs accept).

## When this gate runs

Before ANY `git push` to a public remote — including "push la" direct orders. The gate takes seconds; it is not optional when the remote is public. Check visibility first if unknown:

```bash
gh repo view <owner>/<repo> --json visibility,isPrivate
```

## Step 1 — Stage explicitly, never blind `-A`

Scope `git add` to explicit paths. If bulk-adding is unavoidable, unstage excluded classes BEFORE commit:

```bash
git restore --staged '*.db' '*.db-wal' '*.db-shm' media/ '*.lock' '*/memories/*' 'cache/'
```

Never-commit classes (runtime state, not source): `*.db`, `*.db-wal`, `*.db-shm`, `.backup.lock`, `catch_up_occurrences`, anything under `media/`, `cache/`, session/request dumps.

Third-person memory files (`MEMORY-<name>.md`, `USER-<name>.md` for anyone other than the operator) are never pushable without explicit sovereign direction — regardless of whether older files of that class are already tracked (precedent ≠ permission).

## Step 2 — Scan the EXACT commit (not the working diff)

```bash
# 1. Sensitive path classes — the scan that actually catches privacy leaks:
git show <SHA> --name-only | grep -E 'media/|memories/MEMORY-|\.db(-wal|-shm)?$|\.ogg|\.png|cache/'
# 2. Secret patterns (content):
git show <SHA> | grep -oE '(sk-[a-zA-Z0-9_-]{20,}|ghp_[a-zA-Z0-9]{20,}|[0-9]{8,10}:AA[a-zA-Z0-9_-]{30,}|xoxb-[0-9A-Za-z-]{10,})'
# 3. Key-shaped config lines:
git show <SHA> | grep -iE "api[_-]?key\s*[:=]\s*['\"]?[a-zA-Z0-9]"
```

Verify any hit's 60-char context before declaring a leak — false positives are real: `sk-Nat` once matched "Multitask-National Speech Corpus" research prose.

```bash
git show <SHA> | grep -oE '.{60}<match>.{60}'
```

## Step 3 — If sensitive content ALREADY landed

A "remove it" follow-up commit is insufficient — the remote keeps history. Three options, presented WITH a recommendation, sovereign decides:

1. **Flip repo to private** (recommended default when history has value): one command, keeps all history, breaks nothing.
2. **History rewrite + force-push main** (`git filter-repo` + force) — destroys the public history; irreversible for collaborators; normally a T3 HOLD requiring full diagnostic.
3. **Accept exposure** — sovereign call only.

## Diverged but identical trees (zero-force-push resolution)

Local/remote ahead 1 / behind 1 with identical content (same fix committed twice under different hashes — happens after updates or dual-machine work):

```bash
L=$(git rev-parse HEAD^{tree}); R=$(git rev-parse origin/main^{tree})
[ "$L" = "$R" ] && git reset --soft origin/main   # repoint pointer, keep index/worktree
```

Tree-hash equality proves zero content difference; `reset --soft` restores fast-forward. NEVER force-push a same-tree divergence. (Git config note: `tag.gpgsign=true` forces an editor on annotated tags — use `git update-ref` for lightweight rollback anchors instead.)

## Overlap note

This gate overlaps territory owned by protected skills (FORGE-github-ops, FORGE-precommit-review, FORGE-secret-hygiene, FORGE-github-workflow, github-pr-workflow). Those cover general git ops and secret audits; THIS skill is the narrow public-push privacy gate. If a curator adopts the material into an AAA-class skill, this one should be absorbed.

## Support files

- `references/public-push-near-miss-2026-08-15.md` — the incident this was forged from: what leaked, why the secret scan passed, how it was caught post-push, remediation presented.
