# GitHub Zen — Federation Repo Standard, Agent Duties, and Flows

> Forged 2026-09-06 by FI-003 under F13. Deep-probe evidence: 33 repos, 7 core, 16 local `.github` inventories, 4 canon skills, live CI/PR/release state. Full doctrine report: session SEAL-398d4a3ca1a14ce0. Execution artifacts: `/root/forge_work/2026-09-06-github-zen/`.

## The Law

The canon layer (governance-gate, sentinel, external-witness, bijaksana ΔS≤0, REPO-trailer routing, build-once→SBOM→attest) is ahead of industry. The failure mode it must never regress into: **automation that cannot say NO and monitors that scream into the void** (gate-promotion + witness doctrines). Every declared gate must be an enforced check; every red monitor must be fixed or disabled.

## Repo anatomy (tier SOT = `.github/repo-policy.yml`)

Every repo declares a tier; the tier dictates anatomy. Silence must be a decision (`tier: experimental`), not drift.

| Tier | Must have |
|---|---|
| core/organ | enforced required checks (Lane 1 CI, validate-routing, Constitutional Audit, secrets scan, Sentinel) + dependabot (grouped) + auto-tag-date + hygiene-weekly + CODEOWNERS (doc, not enforcement) |
| package | CI + lockfile invariant + dependabot + auto-tag |
| site | build/audit gate + deploy check + routing |
| experimental | repo-policy.yml saying so; nothing else |

Community layer lives centrally: `ariffazil/.github` repo (when created) — CONTRIBUTING, SECURITY.md, PR template, default issue forms inherited by all repos. Local templates only when deliberate (WEALTH Malay suite).

## Agent duties (trigger → owner → gate)

- **commit** → any FI agent → conventional commit + REPO trailer (FORGE-github-ops)
- **PR (dependabot)** → no human, ever → CI green + invariants → auto-merge squash, branch deleted. Auto-merge bit must be ON (F-2).
- **PR (agent proposal, F13-gated)** → author ≠ witness (Gödel Lock, external-witness). Witness check stays ADVISORY until witness automation exists — never a required check (would rot dependabot).
- **PR (any)** → sentinel PASS/BLOCK + required checks enforced (F-1)
- **issue** → FORGE-issue-triage: classify→route via organs.yaml→label→draft; never close/assign Arif silently
- **CI red** → FORGE-ci-diagnose fires on failure, not on human noticing; 7 failure classes; never rerun/edit-workflow/commit-to-main without authority
- **tag** → auto-tag-date (calver vYYYY.MM.DD); **tags immutable** — corrections get `-r2`, never `-f`
- **release** → tag → `gh release create` + attestation manifest (federation-release-attestation; repo-map read from organs.yaml, never hardcoded)
- **weekly** → hygiene drift-check; dependabot backlog ≤ 0; monitor red >7d without issue = auto-disable + issue

## Enforcement record (executed 2026-09-06)

- **F-1 EXECUTED**: required checks wired via classic branch protection (the mechanism repo-policy.yml declares) on arifOS(6) AAA(5) A-FORGE(6) GEOX(6) WEALTH(5) WELL(5) arif-fazil.com(4) — only contexts observed reporting on PR heads; all re-GET verified. Script: `/root/forge_work/2026-09-06-github-zen/wire_required_checks.py`. arifOS ruleset APEX-CORE-PROTECTION retained as deletion/non-fast-forward guard.
- **F-2 EXECUTED**: `allow_auto_merge=true` + `delete_branch_on_merge=true` on AAA, WEALTH, arifFLOW.
- Open (fix on touch): F-3 silence-or-fix red monitors · F-4 arifOS tag→release arrow (release stuck v2026.07.09, tags at v2026.09.04) · F-5 central `.github` repo (must be PUBLIC; LICENSE per-repo — never inheritable; prefer YAML issue forms over markdown) + AAA `PULL_REQUEST.md` misname · F-6 de-hardcode attestation repo-map, dedupe `workflows/core/` skills · F-7 machine identity (see Research deltas) + gh upgrade + Azure workflow decommission decision.
- Legacy: policy `check_name`s (2026-05-26) were workflow names, not job contexts — intent mapped to observed contexts at wiring time.

## Reject (zen list)

Org migration · Projects v2 · Renovate · Terraform/settings-app · semantic-release/changesets · merge queue (beyond existing Mergify) · CODEOWNERS-enforced review · more monitors.

## Interfaces

gh CLI = primary GitHub lane (MCP forge_github flaky 2026-09-06). Direct pushes to main remain allowed (no require-PR rule) — gates bind merges; F13 exempt (enforce_admins=false).

## Research deltas (2026-09-06 external, 15 sources)

- **Agent acting as repo owner defeats every protection** — the admin exemption IS the agent when agents push as the sovereign's token. Structural fix: machine-user + per-repo fine-grained PAT (GitHub Apps cannot create PRs on personal-account repos, Jul 2026). This makes F-7 load-bearing, not hygiene. Pairs: CODEOWNERS naming the human on irreversible paths only (workflows, release/ruleset scripts) + deploy/release jobs in a GitHub Environment with F13 as required reviewer — the mechanical "agent proposes, F13 disposes."
- **Classic branch protection is a deprecated surface** — GitHub shipped auto-migration to rulesets (Aug 2026). F-1 wiring is functional and policy-declared; migrate via the one-click path once the rulesets `required_status_checks` shape is confirmed against live API (our 422 scar, forge_work).
- **Dependabot auto-merge + grouped updates confirmed consensus** for small GitHub-only fleets; Renovate only for monorepos. Probot settings app REJECTED with sharper reason: `.github/settings.yml` = anyone with push gets admin — anti-doctrine when agents hold push.
- Hardening adopts on next CI touch: `concurrency: cancel-in-progress`, `paths:` filters, `permissions: contents: read` default, SHA-pinned third-party actions, CodeQL default setup + secret scanning + push protection (public repos).
