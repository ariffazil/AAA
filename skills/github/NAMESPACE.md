# NAMESPACE: github

**owner:** AAA

> **Marker file.** This directory is a namespace, not a skill.

## Purpose
One canonical GitHub skill, one door, one lifecycle.

## Contained skills (1)
- `github-ops` — INIT → ORIENT → CLASSIFY → PLAN → BUILD → PUBLISH → VERIFY → REVIEW → MERGE → DEPLOY → SEAL

## Archived aliases (2026-10-19)
`github-auth`, `github-issues`, `github-pr-workflow`, `github-code-review`,
`github-issue-to-pr`, `github-repo-management`, `FORGE-github-ops` were symlinks to
`github-ops`. They appeared as seven separate skills in every picker. Archived to
`/root/AAA/archive/skills-frozen-20261019/2026-10-19-github-ops-single-door/` (outside the catalog — the harness scans `.frozen`).

`FORGE-github-workflow` remains on disk as a `do_not_select` pointer to the same owner.

## Conventions
- Add a new GitHub capability as a **stage or reference** inside `github-ops`, not as a sibling skill.
- Never restore an alias without a harness config that hard-codes the old name.
- To deprecate: `do_not_select: true` + `absorbed_into:` — do not delete.
