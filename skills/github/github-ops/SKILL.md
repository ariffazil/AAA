---
id: github-ops
name: "GitHub Ops — Init to Deploy"
version: 3.0.0
description: "One GitHub door, init to deploy: auth, repo setup, issues, branches, PRs, CI, review, merge, release, deploy verification, receipt."
owner: AAA
risk_tier: medium
floor_scope: [F1, F2, F11]
autonomy_tier: T1
triggers:
  - github
  - gh cli
  - git remote
  - repository
  - repo setup
  - branch
  - commit
  - push
  - pull request
  - pr
  - ci
  - checks
  - merge
  - release
  - tag
  - deploy
  - issue
  - triage
  - code review
  - github auth
  - webhook
  - github actions
forged: 2026-09-20
forged_by: 333-AGI
upgraded: 2026-10-19
absorbed: [github-auth, github-issues, github-pr-workflow, github-code-review, github-issue-to-pr, github-repo-management, FORGE-github-workflow]
---

# GitHub Ops — the single door, INIT → DEPLOY

> **One door.** `github-issues`, `github-pr-workflow`, `github-code-review`, `github-repo-management`,
> `github-issue-to-pr`, `github-auth` and `FORGE-github-workflow` are **frozen aliases** of this skill.
> If a harness opened one of those names, you are already here. Do not maintain a second procedure.
>
> **This file owns the lifecycle. `references/` owns the detail.** Never work GitHub from memory:
> open the reference the stage points at.

**Authority:** T1 = read + branch + commit + push feature branch + open PR are auto.
`main` push, force-push, rebase, remote-branch delete, multi-repo PR, production deploy = **T2/F13 gate**.
Release/tag and deploy are T2. Destructive remote operations are T3.

---

## THE LIFECYCLE (walk in order; each stage has an exit gate)

| # | Stage | Observable that starts it | Do | Exit gate (must be true to move on) |
|---|-------|---------------------------|----|-------------------------------------|
| **0** | **INIT** | No auth, or a new repo/clone | `gh auth status`; `git remote -v`; derive `OWNER/REPO`; `gh repo create/clone`; branch protection; Actions secrets | `gh auth status` exit 0 **or** `$GITHUB_TOKEN` proven by a live API read. Remote resolves. → `github-auth.md`, `github-repo-management.md` |
| **1** | **ORIENT** | Any request about a repo/issue/PR | Read the real object: `gh issue view N --comments`, `gh pr view N --comments`, `git log`, `gh pr checks`. Fresh reads only | You can state object, state, owner/repo, and last human decision without guessing |
| **2** | **CLASSIFY** | Any GitHub ask | Pick exactly one object class from the table below | One branch chosen; no parallel flows |
| **3** | **PLAN** | Code change implied | Duplicate sweep (`gh pr list --search`, `git log -S`), scope, branch name, risk tier, F13 gate check | No duplicate PR/issue; scope fits one PR; tier known |
| **4** | **BUILD** | Implementation | Branch from current base, write code + test. For a bug fix: **sabotage check** — test must fail without the fix | Test fails before, passes after; no sibling call sites left with the same bug |
| **5** | **PUBLISH** | Work is green locally | Lane-signed commit; `git push -u origin HEAD`; `gh pr create` with **truthful** body (re-read `git status` + staged files first) | Commit signed; branch on remote; PR body matches the actual diff |
| **6** | **VERIFY** | PR exists | Poll BOTH `/commits/$SHA/status` **and** `/commits/$SHA/check-runs`. Read required checks from branch protection | Required checks green; every red non-required check classified as noise or patch-attributable |
| **7** | **REVIEW** | PR needs a verdict, or review feedback arrives | `git fetch origin pull/N/head:pr-N`, check out, read surrounding code, post inline comments (`side: LEFT` for deletions) | Every finding has file:line + severity; no verdict from diff-only reading |
| **8** | **MERGE** | Required checks green + approval | Confirm `mergeable`, `mergeStateStatus`, required contexts; merge per policy | Merge state read back live; branch cleaned; no force/rebase without F13 |
| **9** | **DEPLOY** | Merge landed and deploy is in scope | Tag/release (`gh release create`), run the organ's deploy command, then **live read-back** of the deployed surface | Public/live endpoint returns the new version or behavior; rollback path named before deploy |
| **10** | **SEAL** | Work is delivered | Write the receipt with the layer you reached: `repo` ≠ `receipt` ≠ `vault`. Hand-off for the next agent | Claim matches the layer: commit SHA, receipt path, or SEAL id — never "done" alone |

### Object → path (stage 2 in one table)

| Object / ask | Path | Reference |
|---|---|---|
| Auth, token, credential, headless login | 0 → 5 | `references/github-auth.md` |
| Create/clone/fork repo, settings, protection, secrets, topics, release | 0 → 9 | `references/github-repo-management.md` |
| Issue only: create, list, triage, label, assign, comment, close, search | 1 → 2 → 10 | `references/github-issues.md` |
| Issue **+ code change**: "fix #123", "take to green CI" | 1 → 4 → 5 → 6 → 8 → 10 | `references/github-issue-to-pr.md` |
| Branch/commit/open PR/watch CI/merge, no issue number | 1 → 5 → 6 → 8 → 10 | `references/github-pr-workflow.md` |
| Review a PR (no code change) | 1 → 7 → 10 | `references/github-code-review.md` |
| Release, tag, deploy, post-deploy verification | 8 → 9 → 10 | `references/github-pr-workflow.md` + organ runbook |
| Multi-repo / organ-level / push to main / force / rebase | any → **F13 gate first** | `references/forge-github-ops.md` |

---

## HARD RULES (apply at every stage)

1. **No auth, no work.** `gh` preferred; `git`+`curl` with `$GITHUB_TOKEN` is the fallback. Never invent a credential.
2. **Derive `OWNER/REPO` from the remote**, never from memory: `git remote get-url origin` → strip `github.com[:/]` and `.git`. Registry (`/root/AAA/federation/organs.yaml`) wins over any literal in a doc.
3. **Every remote claim needs a fresh read in this session.** "CI green", "merged", "released", "closed" without a live probe = an unsealed claim.
4. **Read the thread, not the title.** Bodies are filing-time snapshots; decisions live in comments.
5. **Sweep before create.** `gh pr list --search "#N" --state all` + two synonym variants + `git log --oneline -20 -- <files>`.
6. **`/issues` returns PRs too.** Filter `if 'pull_request' not in i`.
7. **Never `rm`.** Archive, never delete. Aliases and old procedures go to `/root/AAA/skills/.frozen/`.
8. **The PR body must match reality, not the plan.** Hooks can add files between `git add` and commit — re-read the staged diff before writing the description.
9. **Deploy is not done until the live surface is read back.** A green deploy command is a claim; the endpoint is the evidence.

### CONTRADICTION — push authority (KEEP BOTH, do not average)

- `references/forge-github-ops.md`: **never `git push` without F13 confirmation** (every push gated).
- The same file's sensitive list narrows it to: `main`/`master`, `--force`, `rebase`, remote-branch delete, multi-repo PRs.
- `references/github-issue-to-pr.md` says push immediately — the PR is what dispatches CI.

**Standing resolution until F13 rules:** feature-branch push + PR = T1 (do it, don't sit on green work).
The narrower sensitive list is the real gate. Surface the conflict; never silently choose the convenient reading.

---

## FAILURE MODES THAT BITE (specific, from live scars)

- **`gh auth login --with-token` hangs headless.** Guard with `timeout 20`; on 124 write `~/.config/gh/hosts.yml` directly, `chmod 600`, then `gh auth setup-git`.
- **Commit status ≠ check-runs.** Poll both; Actions failures live in check-runs.
- **Required vs noise.** Read branch protection contexts. If the required check is green and `enforce_admins:false`, the other red checks are not the gate.
- **Shallow-clone SOT gates + Mergify.** `fetch-depth: 2` sees only the top commits; a Mergify auto-commit hides yours. Fix structurally (squash/reopen or `no-merge` label), don't re-stamp in a loop.
- **Auto-fix loop max 3 attempts**, then escalate.
- **Review without checkout is blind.** `git fetch origin pull/N/head:pr-N` first; delete the local branch after.
- **A regression test that passes with and without the fix proves nothing.** Run the sabotage check.
- **Symptom-only fix.** `search_files` the bug shape; fix the class or rule siblings out explicitly.
- **"PR exists" ≠ delivered.** Delivery is merged, read live.
- **Token leakage.** Never echo tokens; never commit `.env`, `*.pem`, `vault.flat.env`, credentials.
- **Deploy without rollback.** Name the restore path before you deploy. Archive the previous tree.

---

## REFERENCE MAP (byte-identical bodies, provenance headers intact)

| Reference | Owns |
|---|---|
| `references/github-auth.md` | credential methods, headless gh, device flow, SSH-over-443 |
| `references/github-repo-management.md` | repo create/clone/fork, settings, protection, secrets, releases, topics |
| `references/github-issues.md` | issue lifecycle, triage, labels, templates |
| `references/github-issue-to-pr.md` | premise validation, duplicate sweep, sabotage test, delivery definition |
| `references/github-pr-workflow.md` | branch/commit/push/PR/CI/merge mechanics, conventional commits, CI triage |
| `references/github-code-review.md` | review procedure, inline comment shape, output template |
| `references/forge-github-ops.md` | federation overlay, organ registry, F13 confirmation gate |
| `scripts/gh-env.sh`, `scripts/git-credential-token.py`, `scripts/verify-canonical.sh` | executable helpers |

---

## VERIFICATION (before claiming this skill or a GitHub job is done)

- [ ] `gh auth status` exit 0 (or token proven by a live read)
- [ ] `OWNER/REPO` derived from remote, not memory
- [ ] Object state read live this session (issue/PR/CI/merge)
- [ ] Branch pushed with `-u`; PR body matches `git diff --stat`
- [ ] Required checks green; non-required failures classified
- [ ] Merge state read back; deploy surface read back
- [ ] Receipt names the layer reached: `repo=<sha>` · `receipt=<path>` · `vault=<id or PENDING>`

**The Zen:** one door, eleven stages, every gate opened by evidence — not by memory, not by a sibling's summary.
DITEMPA BUKAN DIBERI.
