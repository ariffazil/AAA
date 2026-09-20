---
id: repo-intelligence
name: forge-repo-intelligence
autonomy_tier: T1
version: 2.0.0
description: "Use when you must know a repository's real state before changing it. Read-only repo/CI/doc intelligence — census, diff, release audit, stub & debris detection, CI diagnosis."
owner: AAA
risk_tier: medium
floor_scope: [F1, F2, F4, F9, F11]
merged_from:
  - FORGE-repo-intelligence    # case-duplicate copy (frontmatter was the only delta)
  - forge-ci-diagnose          # AAA copy
  - FORGE-ci-diagnose          # .hermes copy — DIVERGENT escalation targets, kept (see CONTRADICTION)
  - forge-cross-repo-doc-zen   # absorbed 2026-09-20 (docs graph)
merged_at: "2026-09-20T14:44:58Z"
merged_by: skill-merge-wave1 / cluster github-repo-ci-pr
cluster_note: "Observation lane only. The MUTATION lane (branch/commit/PR/merge) is `github-ops`."
triggers:
  - repository intelligence
  - audit repo
  - find stubs
  - orphan detection
  - dead code audit
  - repo reality audit
  - corruption score
  - release audit
  - tag drift
  - cross-repo impact
  - workflow integrity
  - branch protection audit
  - manifest reconcile
  - repo census
  - ci failure
  - red CI
  - github actions log
  - ci diagnose
  - failure class
  - cross-repo documentation
  - doc graph
  - floor name drift
  - deprecated tool names
tags: [repo, intelligence, audit, ci, read-only, federation]
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---
<!-- wave1-merge:FLOW:BEGIN -->
# forge-repo-intelligence — repository intelligence controller (read-only lane)

> **One controller. Twelve modes. No duplicate logic.**
> This skill is the SOLE repository intelligence controller for the federation.
> It ANSWERS what a repo really is. It does not change one —
> the mutation lane (branch → commit → PR → CI → review → merge) is `github-ops`.

**Lane split (canonical):** `forge-repo-intelligence` = observation (read, probe, classify, report).
`github-ops` = mutation (auth, branch, commit, push, PR, merge). A finding here is a candidate;
changing the repo is the other skill's job, with its own authority gate.

## FLOW — pick the mode by observable, then read the mode below

| # | Observable | Mode / reference | What it produces |
|---|---|---|---|
| 1 | "what is in this repo / on this tag / is it dirty" | `inventory` | census: branch, HEAD, tag, dirty, ahead/behind |
| 2 | "how is it built, what are the contracts, who owns it" | `map` | entry points, build/test commands, contract files, CODEOWNERS |
| 3 | "what changed between A and B / tag vs main" | `delta` | commit diff, tag-vs-main drift, manifest parity |
| 4 | "review this PR" (no code change requested) | `pr_review` | risk verdict from metadata → filenames → critical patches |
| 5 | **red X / failing workflow / build-test-lint gate broke** | `ci_diagnose` → `references/forge-ci-diagnose.md` + `references/FORGE-ci-diagnose.md` | failure class + root cause + reversible fix proposal |
| 6 | "what issues are open, which organ do they belong to" | `issue_triage` | deduplicated, severity-classified, routed list |
| 7 | "audit workflows / supply chain / secrets" | `security` | unpinned actions, permissions, OIDC, secret patterns |
| 8 | "this change crosses organ boundaries" | `cross_repo_impact` | affected organs, breaking vs additive, blast radius |
| 9 | "is the release real — tag, artifact, runtime" | `release_audit` | tag→commit→CI→artifact→deployed→runtime parity |
| 10 | "is this workflow YAML actually sound" | `workflow_integrity` | parse result, duplicate job IDs, unsafe patterns |
| 11 | "does our documented tool count match runtime" | `manifest_reconcile` | README/FEDERATION/AGENTS vs live tools/list |
| 12 | "are we enforcing branch protection" | `ruleset_audit` | protection gaps + remediation |
| 13 | **"is this code real or theatre" (stubs, orphans, leaks)** | read-only peer `audit/audit-ops`: `references/audit-repo-reality.md` + `references/audit-repository-entropy.md` | stub tiers, corruption score, disposition ledger |
| 14 | **"do the docs across repos agree"** | `references/forge-cross-repo-doc-zen.md` | orphan docs, wrong floor names, deprecated tool refs, fixed or listed |

Modes 1–12 are the body below. Modes 13–14 are member bodies kept verbatim in `references/`.
Mode 5's procedure is the two `*-ci-diagnose` references, not the mode stub below.

## CORE RULES (this lane)

1. **UNMEASURED beats a plausible default.** Any field a probe failed to fill stays `UNMEASURED`.
   Never substitute `0`, `clean`, or `healthy` for "I did not look".
2. **A clean tree proves only no local changes.** Never equate clean with correct.
3. **Runtime beats README beats FEDERATION.md.** Reconcile by correcting the weaker source, never by averaging.
4. **Read-only by default.** No mutation, no unregister, no delete without an authority that is not this skill's.
5. **Never label a diagnostic-survival job "passed."** If lint fails but `continue-on-error` keeps the
   workflow green, report the truth.
6. **Tag discipline:** never silently move a published tag. A tag is an immutable receipt; if it is behind
   main, issue a corrected tag.
7. **No agent authors, approves, and merges the same consequential change.** (Crosses into `github-ops`.)
8. **Re-read `origin/main` immediately before you act, not only at the start.** Federation repos
   have concurrent writers; the fix you are about to write may already be merged. Before opening a
   PR, re-fetch and grep the target file's *current* content on `origin/main`. A merge base that
   predates your work means someone shipped it — report and withdraw, do not merge on top.
9. **Remove a false-positive source; never bless it into a baseline.** When a scanner is noisy,
   disable the detector that emits the noise and keep its sibling detectors live. Whitelisting the
   findings into a baseline hides that whole class permanently and is the harder change to reverse.
10. **Confirm which branch the working copy is on before claiming a push landed.** Run
    `git branch --show-current`. A checkout on a proposal branch is legitimately ahead of `main`,
    and `git push origin main` from it is not a delivery. Verify the remote ref itself
    (`gh api repos/<org>/<repo>/commits/<sha>`) rather than trusting the push output — it prints
    `Everything up-to-date` in states where nothing was pushed.

## CONTRADICTION — kept, not averaged

The two CI-diagnose copies name **different escalation successors** for the same failure class:

| failure class | `forge-ci-diagnose` (AAA, `references/forge-ci-diagnose.md`) | `FORGE-ci-diagnose` (.hermes, `references/FORGE-ci-diagnose.md`) |
|---|---|---|
| `secret-gate` | `secret-safety-scan` | `FORGE-secret-hygiene` |
| `cross-repo-break` | `parallel-authority-detection` | `live-probe-audit-pattern` |

`config-error` on a constitutional workflow → `888_JUDGE` in both. Both bodies are preserved verbatim;
F13 rules on which successor is canonical. Do not silently pick one.

## REFERENCES

| Reference | Source skill | Original path (archived) |
|---|---|---|
| `references/FORGE-repo-intelligence.md` | FORGE-repo-intelligence | `/root/AAA/skills/.archive/merge-20260920/repo-intelligence/FORGE-repo-intelligence/` |
| `references/forge-ci-diagnose.md` | forge-ci-diagnose | `/root/AAA/skills/.archive/merge-20260920/repo-intelligence/forge-ci-diagnose/` |
| `references/FORGE-ci-diagnose.md` | FORGE-ci-diagnose | `/root/AAA/skills/.archive/merge-20260920/repo-intelligence/FORGE-ci-diagnose/` |
| `references/forge-cross-repo-doc-zen.md` | forge-cross-repo-doc-zen | `/root/AAA/skills/.archive/merge-20260920/repo-intelligence/forge-cross-repo-doc-zen/` |

Read-only peers owned by another cluster (not absorbed here): `audit/audit-ops`
(`references/audit-repo-reality.md`, `references/audit-repository-entropy.md`).
Mutation lane: `github/github-ops`.

<!-- wave1-merge:FLOW:END -->
# FORGE-repo-intelligence — Controller Skill

> **One controller. Twelve modes. No duplicate logic.**
> This skill is the SOLE repository intelligence controller. Smaller GitHub skills are consolidated as internal modules.
> Every mode produces the minimum evidence envelope defined below.

## Operating Loop

```
OBSERVE → MAP → DIFF → VERIFY → REVIEW → (JUDGE) → (ACT) → RE-PROBE → RECEIPT
```

Parenthesized stages (JUDGE, ACT) require mutation authority and are gated.

## Minimum Evidence Envelope

Every mode output must include:

```yaml
repo:
ref:
commit_sha:
working_tree:
tag_delta:
changed_files:
critical_paths:
tests:
ci:
security:
contract_impacts:
runtime_probe:
risk_tier:
proposed_action:
rollback:
evidence_class:
unknowns:
```

Use `UNMEASURED` for any field where the probe failed — never substitute `0`, `clean`, or `healthy`.

---

## Modes

### `inventory` — Repository census

Orchestrates: `FORGE-github-ops`

```yaml
scope: all 7 federation repos
output:
  - repo name, remote, default branch
  - current branch, HEAD SHA, tag list
  - working tree dirty/clean
  - ahead/behind origin
  - collaborator permissions
```

Tool path: `forge_worktree` per repo → `forge_git_status` → `forge_git_log` → GitHub API for permissions.

### `map` — Architecture and critical paths

Orchestrates: `code-wiki`, `aaa-agent-invariants`

```yaml
output:
  - entry points, build commands, test runners
  - contract files (schemas, registries, manifests)
  - ownership (CODEOWNERS, organ responsibility)
  - generated vs hand-maintained files
  - critical paths that gate deployment
```

### `delta` — Ref comparison

Orchestrates: `FORGE-github-ops`

```yaml
input: base_ref, head_ref (branches, tags, or commits)
output:
  - commit diff (count, authors, files changed)
  - tag-vs-main drift detection
  - deployed-vs-source comparison
  - surface/manifest parity (tools/list vs tool_registry.json)
```

Never equate "clean" with "correct." A clean tree proves only no local changes.

### `pr_review` — Efficient diff review

Orchestrates: `FORGE-pr-review`, `FORGE-pr-governance`, `secret-safety-scan`

**Efficient pattern (DO NOT load 20,000-line diffs first):**

```text
1. PR metadata (title, author, base/head, labels)
2. Changed filenames only → list_pr_changed_filenames
3. Identify critical files (contracts, schemas, registries, workflows, constitution)
4. Fetch only critical file patches → fetch_pr_file_patch
5. Inspect review threads → list_pull_request_review_threads
6. Inspect CI status → fetch_commit_workflow_runs
7. Produce risk verdict
```

Risk classification:
- `LOW`: docs, comments, non-critical config
- `MEDIUM`: source changes in single organ, no contract impact
- `HIGH`: contract/schema/registry changes, cross-repo impact
- `CRITICAL`: constitutional, deployment, or secret-adjacent

### `ci_diagnose` — Workflow analysis

Orchestrates: `FORGE-ci-diagnose`

```yaml
input: repo, commit SHA or PR number
output:
  - workflow runs for commit
  - job-level pass/fail breakdown
  - step-level failure extraction
  - log analysis for root cause
  - classification: flake | dependency | regression | config | security
```

**Truth gate:** Never label a diagnostic-survival job as "passed." If lint fails but `continue-on-error` keeps the workflow green, report the truth.

### `issue_triage` — Issue intelligence

Orchestrates: `FORGE-issue-triage`

```yaml
input: repo, query filters
output:
  - deduplicated issue list
  - severity classification
  - routing (which organ, which agent)
  - linked PRs and cross-references
```

### `security` — Supply-chain and secret audit

Orchestrates: `secret-safety-scan`, `parallel-authority-detection`

```yaml
checks:
  - unpinned actions (movable tags → require SHA pinning)
  - least-privilege permissions (permissions: {} declared)
  - concurrency cancellation
  - OIDC vs long-lived credentials
  - artifact attestations
  - CODEOWNERS coverage for constitutional/registry/schema/deployment files
  - secret patterns in source
```

### `cross_repo_impact` — Federation boundary detection

Orchestrates: `code-wiki`, `FORGE-pr-review`

```yaml
input: changed files or PR
output:
  - which organs are affected
  - contract/schema/registry changes
  - breaking vs additive changes
  - required witness count per blast radius
  - organ attestation impacts
```

### `release_audit` — Tag, commit, CI, artifact, runtime parity

Orchestrates: `federation-release-attestation`

```yaml
output (per repo):
  - tag → commit SHA
  - commit → CI run status
  - CI → artifact hash
  - artifact → deployed commit
  - deployed → runtime health probe
  - tools/list match against registry

federation manifest:
  release: "vYYYY.MM.DD-AAA"
  repos:
    arifOS:    { commit, ci, artifact, runtime }
    A-FORGE:   { commit, ci, artifact, runtime }
    AAA:       { commit, ci, artifact, runtime }
    GEOX:      { commit, ci, artifact, runtime }
    WEALTH:    { commit, ci, artifact, runtime }
    WELL:      { commit, ci, artifact, runtime }
    arif-sites:{ commit, ci, artifact, runtime }
```

**Tag discipline:** Never silently move a published federation tag. Treat tags as immutable receipts. If a tag is behind main, issue a new corrected tag rather than overwriting.

### `workflow_integrity` — YAML validation and structural audit

Orchestrates: internal (no sub-skill — pure structural validation)

```yaml
input: repo path or PR number
checks:
  - Parse all YAML workflows (Python yaml.safe_load_all)
  - Reject duplicate job IDs
  - Reject malformed expressions (${{ }})
  - Reject reusable workflows referenced by moving branch names (@main, @v1)
  - Reject overly broad permissions (write-all)
  - Reject pull_request_target without explicit isolation
  - Actionlint validation
  - Unsafe pattern detection (shell injection, unpinned SHAs)
output:
  - Pass/fail per workflow file
  - Specific error locations (file:line)
  - Blocking vs advisory classification
```

**Truth gate:** A workflow that survives parsing with duplicate keys is silently corrupt. GitHub may keep only one. This mode catches that BEFORE merge.

### `manifest_reconcile` — Tool surface truth reconciliation

Orchestrates: internal + runtime probes

```yaml
input: organ name
output:
  - README declared count vs live tools/list count
  - FEDERATION.md declared count vs live
  - AGENTS.md declared count vs live
  - organ.yaml declared interfaces vs actual
  - Staleness score (days since last verification)
  - Recommendations: which source to update
  - Canonical manifest update (AAA/federation/repos.yaml)
rule: runtime beats README beats FEDERATION.md
```

**Truth gate:** If README says 8 tools and runtime says 12, the README is wrong. Update it. Do not "reconcile" by averaging.

### `ruleset_audit` — Branch protection and deployment policy

Orchestrates: GitHub API

```yaml
input: repo name or 'all'
output per repo:
  - Branch protection status (PR required, force push, linear history, deletions)
  - Required status checks configured
  - CODEOWNERS coverage for critical paths (contracts, schemas, registries, deploy)
  - Merge queue status
  - Tag protection status
  - Deployment environment protections
  - Gaps identified with specific remediation steps
```

**Remediation:** Can auto-apply ruleset via `gh api` (requires repo admin). Default policy:
- PRs required on main, force push blocked, deletions blocked
- Linear history, conversation resolution
- Signed commits for constitutional paths

---

## Tool Routing

| Intelligence Task | GitHub Tools | A-FORGE Tools |
|---|---|---|
| Repository inventory | `search_repositories`, `get_file_contents` | `forge_worktree`, `forge_git_status` |
| Code discovery | `search_code`, `get_file_contents` | `forge_filesystem_read`, `forge_filesystem_grep` |
| History comparison | `get_commit`, `list_commits` | `forge_git_log`, `forge_git_diff` |
| PR discovery | `search_pull_requests`, `pull_request_read` | `forge_github_search` |
| Efficient diff | `pull_request_read(method=get_files)` → patch | — |
| CI diagnosis | `list_commits` → workflow runs | `forge_log_tail` |
| Issue intelligence | `search_issues`, `issue_read` | — |
| Build evidence | `get_commit` → status/check runs | — |

**Mutation lane** (requires change control): `create_branch`, `create_or_update_file`, `create_pull_request`, `create_issue`, `pull_request_review_write`, `merge_pull_request`, tag creation.

**Default mutation pattern:**
```text
worktree → bounded branch → path-specific staging → tests → commit
→ draft PR → independent review → required checks
→ human/kernel authority → merge → post-merge verification
```

No agent should author, approve, and merge the same consequential change.

---

## Registry Repair Note

This skill replaces several overlapping GitHub micro-skills. The registry must:
1. Generate from active skill directories only — never resolve a retired path as active.
2. `github-runbook` (formerly in `_retired/ARCHIVE-github-runbook/`, now canonically `FORGE-github-workflow`) must be removed from active registry.
3. `FORGE-pr-governance` dependency on `github-runbook` must be updated to `FORGE-repo-intelligence`.
4. Version drift (ci-diagnose 1.0.0→1.1.0, issue-triage 1.0.0→1.1.0, pr-review 1.0.0→1.1.0) must be resolved in registry.

---

*DITEMPA BUKAN DIBERI — Forged, Not Given.*
