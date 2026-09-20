---
name: github-ops
id: github-ops
version: 2.0.0
description: "Use when doing GitHub work — auth, repos, issues, PRs, review, CI, merge. One flow routes to the exact reference."
owner: AAA
risk_tier: low
floor_scope: [F1, F2, F11]
autonomy_tier: T1
triggers:
  - authentication
  - automation
  - bug-tracking
  - ci
  - ci/cd
  - code-review
  - coding
  - configuration
  - forge-github-ops
  - gh-cli
  - git
  - github
  - github-auth
  - github-code-review
  - github-issue-to-pr
  - github-issues
  - github-pr-workflow
  - github-repo-management
  - issues
  - merge
  - ops
  - project-management
  - pull-requests
  - quality
  - releases
  - repositories
  - runbook
  - secrets
  - setup
  - ssh
  - triage
tags: [github, git, gh-cli, ops, runbook, authentication, repositories, issues, pull-requests, code-review]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# github-ops — ONE routing surface for every GitHub action in the federation

Seven former GitHub skills are folded into the seven reference files below. The bodies are
byte-identical to the archived originals. **This file routes; the reference holds the procedure.**
Do not work GitHub from memory — open the reference the flow points at.

## FLOW

### Step 0 — PREFLIGHT (always, before any branch)

```bash
gh --version 2>/dev/null || echo "gh: absent"
gh auth status 2>/dev/null; echo "gh-auth-exit=$?"
git config --global credential.helper 2>/dev/null || echo "no git credential helper"
git remote get-url origin 2>/dev/null || echo "no origin remote"
```

Then walk the table top-down. The **observable** is the thing you can actually see on the machine —
not your impression of the request.

| # | Observable (what you see) | Reference | What it produces |
|---|---|---|---|
| **1** | `gh-auth-exit!=0` **AND** `$GITHUB_TOKEN` empty **AND** `~/.git-credentials` shows no `github.com` -> no working credential | `references/github-auth.md` | A working `AUTH_METHOD` (`gh` or `curl` or `none`) + a credential store that survives the session. **Every other branch is blocked until this is `gh` or `curl`.** |
| **2** | Auth proven, and the object of work is a **repository**: clone / create / fork / remotes / settings / branch protection / Actions secrets / releases / gists | `references/github-repo-management.md` (+ `references/assets/github-repo-management/references/github-api-cheatsheet.md`) | The repo exists / is configured / has a release or secret, verified by a live `gh` or REST read-back |
| **3** | Auth proven, an **issue number exists**, and a **code change is requested** ("fix #123", "implement this issue", "take this bug to green CI") | `references/github-issue-to-pr.md` | An issue that is *delivered*: premise validated, regression test proven to bite, PR open with an honest live CI state. **This reference owns the discipline**; load `references/github-pr-workflow.md` for PR mechanics and `references/github-code-review.md` before requesting review |
| **4** | Auth proven, object of work is an **issue**, and **no code change** is requested (create / list / triage / label / assign / comment / close / search) | `references/github-issues.md` (+ `references/assets/github-issues/templates/*`) | Issue opened, triaged, labelled, assigned, or closed — verified by reading the issue back |
| **5** | Auth proven, work is on a **branch / commit / open PR / watch CI / merge**, with **no issue number in play** | `references/github-pr-workflow.md` (+ `references/assets/github-pr-workflow/references/ci-troubleshooting.md`, `.../conventional-commits.md`, `.../templates/*`) | Branch pushed, PR opened, CI read live, PR merged — each state read back, never assumed |
| **6** | Auth proven, a **PR number or URL exists** and the ask is **review / look at / verdict** with **no code change requested** | `references/github-code-review.md` (+ `references/assets/github-code-review/references/review-output-template.md`) | A structured verdict (Critical / Warnings / Suggestions / Looks Good) posted as a formal review with inline comments, or delivered locally pre-push |
| **7** | The work spans **more than one federation repo / an arifOS organ**, or the ask is a **push to main, force-push, rebase, remote-branch delete, or a multi-repo PR** | `references/forge-github-ops.md` | Registry-derived repo paths (`/root/AAA/federation/organs.yaml`) and the F13 confirmation gate honoured **before** the mutation |

### Disambiguation — the pairs that look alike

- **#3 vs #5.** Both end in a merged PR. Split on the observable: *does an issue number exist?* If yes
  it is #3 (`github-issue-to-pr` — premise validation, duplicate sweep, sabotage run, honest CI) and #5 is
  its mechanics subcontract. If no, it is #5 and #3's discipline does **not** apply.
- **#6 vs everything else.** #6 never changes code. If the ask implies a code change, it is #3 or #5,
  and #6 becomes a review step *inside* that flow — not a parallel branch.
- **#7 is an overlay, not an alternative.** It can apply on top of #2 / #4 / #5 the moment the blast radius
  crosses one repo or touches `main`. Check it before any `git push`.

## CORE RULES

Applies to every branch. Duplicates across members are merged; disagreements are **kept and flagged**.

1. **No auth, no work.** Run Step 0 first. `gh` is preferred; `git` + `curl` with `$GITHUB_TOKEN` is the
   fallback. Never invent a credential — ask the human (`github-auth.md`, methods 1-2).
2. **Derive `OWNER`/`REPO` from the remote, never hardcode them.**
   `REMOTE_URL=$(git remote get-url origin)`, then strip `github.com[:/]` and `.git`.
   `forge-github-ops` is explicit: any `/root/<repo>` literal in the docs is an **EXAMPLE**; the live
   value comes from `/root/AAA/federation/organs.yaml`, and the registry wins on conflict.
3. **Every claim about remote state needs a fresh read.** Never say "CI is green", "merged", "released",
   or "issue closed" without a live `gh pr checks` / `state,mergedAt` / `gh issue view` in this session.
   Memory is not evidence (`github-issue-to-pr`, step 8).
4. **Read the thread, not the title.** `gh issue view N --comments` / `gh pr view N --comments`. The body
   is a filing-time snapshot; decisions live in the comments.
5. **Sweep before you create.** `gh pr list --search "#<N>" --state all` plus at least two keyword/synonym
   variants, and `git log --oneline -20 -- <files>`, before opening a PR or an issue.
6. **The REST `/issues` endpoint returns pull requests too.** Filter with `if 'pull_request' not in i` on
   every issue listing (`github-issues.md`).
7. **Never `rm`.** Members and their assets are archived, never deleted. Archive:
   `/root/AAA/skills/.archive/merge-20260920/github/`.
8. **Member support files live under `references/assets/<member>/`**, preserving each member's own relative
   layout (its `references/`, `templates/`, `scripts/`). The scripts the auth flow actually executes sit at
   the umbrella root in `scripts/` (`gh-env.sh`, `git-credential-token.py`).

### CONTRADICTION — push authority (KEEP BOTH, do not average)

- `forge-github-ops`, in its commit workflow, says inline:
  **`# NEVER: git push without ARIF confirmation (F13 SOVEREIGN)`** — every push is sovereign-gated.
- The same file's "Sensitive Actions" list narrows that to: push to `main`/`master`, `--force`, `rebase`,
  remote-branch delete, and PRs affecting greater than one repo.
- `github-issue-to-pr`, step 7, states the opposite tempo: *"push and open the PR **right away** — the PR is
  what dispatches CI ... do not sit on finished work."*

These cannot all be the rule for a feature-branch push. **Resolution is F13's, not an agent's.** Until F13
rules: treat the *narrower* list as the standing gate, and surface the conflict rather than silently
choosing the convenient reading.

## PITFALLS

Union of every member's scars, with the specificity that makes them useful. This is the part a summariser
destroys — read it before running the branch.

**Auth (`github-auth.md`)**
- **`gh auth login --with-token` hangs forever** on keyring-less/headless boxes (VPS, container, no dbus
  session) — even with `--insecure-storage`, and with no output. Guard it: `timeout 20 gh auth login
  --with-token`. On exit 124, skip gh's login machinery and write `~/.config/gh/hosts.yml` directly (the
  exact `printf` block is in the reference), `chmod 600`, then `gh auth status` + `gh auth setup-git` —
  those read the file store without touching the keyring. Proven on a headless x86_64 VPS, gh 2.97.0.
- **Windows PTY:** driving `gh auth login` through a pty, answer prompts with `process(submit)`, never
  `process(write)` with a bare newline. On ConPTY a lone line-feed is not a line terminator, so gh's
  blocking "Press Enter to open the browser" read never returns and the login hangs silently.
- Device-flow polling: respect `interval`; add 5s on `slow_down`; `expired_token` -> restart the flow;
  `access_denied` -> stop. Never echo the token.
- Windows winget installs gh at `/c/Program Files/GitHub CLI` — add it to `PATH` in the same shell.
- SSH `port 22: Connection refused` -> `~/.ssh/config` with `Hostname ssh.github.com` and `Port 443`.
- `git push` asking for a password is expected: GitHub disabled password auth. Token or SSH only.
- Multiple accounts -> per-host aliases in `~/.ssh/config`, or per-repo credential URLs.

**Repo management (`github-repo-management.md`)**
- `gh secret set` is dramatically simpler than the REST path — REST secrets require `PyNaCl` sealed-box
  encryption against the repo public key. If secrets are needed and `gh` is absent, install `gh` for that.
- Auto-merge is GraphQL-only; REST has no endpoint for it.
- Topic updates need the `application/vnd.github.mercy-preview+json` Accept header.

**Issues (`github-issues.md`)**
- `GET /repos/{o}/{r}/issues` **includes pull requests**. Always filter `'pull_request' not in i`.
- `gh issue develop 42 --checkout` is the gh branch-from-issue shortcut; manual equivalent is
  `git checkout main && git pull origin main` then `git checkout -b fix/issue-42-<slug>`.

**PR workflow (`github-pr-workflow.md`)**
- Commit-status and check-runs are **two different endpoints** (`/commits/$SHA/status` and
  `/commits/$SHA/check-runs`). Checking only the first misses GitHub Actions failures.
- Auto-fix loop: **max 3 attempts, then ask the human.**
- Push the branch with `git push -u origin HEAD` before `gh pr create`, or the create fails for want of a
  tracking branch.

**Code review (`github-code-review.md`)**
- In inline review comments, `line` is the line number in the **new** version of the file; deleted lines
  need `"side": "LEFT"`.
- Reviewing a foreign PR without checking it out first is a mistake:
  `git fetch origin pull/N/head:pr-N && git checkout pr-N`. A diff alone misses issues that only the
  surrounding code reveals.
- Clean up afterwards: `git checkout main && git branch -D pr-N`.

**Issue to PR (`github-issue-to-pr.md`)**
- A regression test that passes **with and without** the fix proves nothing — run the sabotage check:
  restore the old behavior, confirm the test FAILS, restore the fix, confirm it passes.
- "Fixing" behavior that the original commit shows is intentional design. Check
  `git log -p -S "<symbol>"` before changing it.
- Fixing the symptom at one call site while sibling sites keep the same bug. `search_files` the bug shape
  and fix the class, or explicitly rule the siblings out.
- Claiming the issue is delivered because a PR exists. Delivery is the merged state, read live.

**Federation overlay (`forge-github-ops.md`)**
- Hardcoded `/root/<repo>` paths are EXAMPLES and drift. Read `source_path` from
  `/root/AAA/federation/organs.yaml`; the registry wins over any literal in a document.
- `gh issue` / `gh pr` run outside the repo need `-R "$ORG_REPO"`, with `ORG_REPO` derived from
  `git remote get-url origin` — not from memory.

## REFERENCES

| Reference | Source skill | Original path (now archived) |
|---|---|---|
| `references/forge-github-ops.md` | forge-github-ops | `/root/AAA/skills/forge-github-ops/SKILL.md` |
| `references/github-auth.md` | github-auth | `/root/AAA/skills/github/github-auth/SKILL.md` |
| `references/github-code-review.md` | github-code-review | `/root/AAA/skills/github/github-code-review/SKILL.md` |
| `references/github-issue-to-pr.md` | github-issue-to-pr | `/root/AAA/skills/github/github-issue-to-pr/SKILL.md` |
| `references/github-issues.md` | github-issues | `/root/AAA/skills/github/github-issues/SKILL.md` |
| `references/github-pr-workflow.md` | github-pr-workflow | `/root/AAA/skills/github/github-pr-workflow/SKILL.md` |
| `references/github-repo-management.md` | github-repo-management | `/root/AAA/skills/github/github-repo-management/SKILL.md` |

Each reference carries a 4-line provenance header; the body beneath it is byte-identical to the archived
original (sha256 verified at merge time — see the receipt at
`/root/forge_work/merge-2026-09-20/github-receipt.json`).

**Supporting assets** (`references/assets/<member>/...`, member-relative layout preserved):

- `github-code-review/references/review-output-template.md`
- `github-issues/templates/bug-report.md`, `github-issues/templates/feature-request.md`
- `github-pr-workflow/references/ci-troubleshooting.md`, `github-pr-workflow/references/conventional-commits.md`
- `github-pr-workflow/templates/pr-body-bugfix.md`, `github-pr-workflow/templates/pr-body-feature.md`
- `github-repo-management/references/github-api-cheatsheet.md`
- `forge-github-ops/liveness.json`

**Executable helpers** (`scripts/`, at the umbrella root): `gh-env.sh`, `git-credential-token.py`. The
member bodies point at `${HERMES_HOME}/skills/github/github-auth/scripts/...`, a path that does **not**
exist on this machine (the member directories held SKILL.md only). Use `scripts/` here instead — the fix
is recorded in the receipt.

## VERIFICATION

- The branch's own reference defines "done" for that branch.
- Cross-cutting, every branch: every claim about remote state (auth, CI, merge, release, issue state) is
  backed by a fresh read in this session, never by memory.
- Pre-merge archive: `/root/AAA/skills/.archive/merge-20260920/github/` — all seven member directories,
  untouched.
