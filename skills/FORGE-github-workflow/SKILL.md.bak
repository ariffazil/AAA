---
id: FORGE-github-workflow
name: FORGE-github-workflow
version: 2.0.0
description: >
  Class-level umbrella for GitHub operations — auth, repo management, PR lifecycle,
  issues, code review. Each op is a labeled section; load the relevant one.
  BIJAKSANA: XML-tagged for Claude, numbered steps for Codex, imperative for Hermes.
floor_scope: [F01, F11]
cognitive_hints:
  claude: "Use <workflow>, <pr-lifecycle>, <issue-lifecycle> tags. Extended context for PR review chains."
  codex: "GitHub API schema adherence required. Each operation: authenticate → execute → verify → log."
  hermes: "GitHub op? Auth. Execute. Verify. Log. Next."
---

# FORGE-github-workflow

<cognitive-note model="claude">XML-tagged workflow sections. Use extended context for multi-PR review state tracking.</cognitive-note>
<cognitive-note model="codex">GitHub API schemas strictly followed. Each op: auth → execute → verify response → log.</cognitive-note>
<cognitive-note model="hermes">Auth. Do. Verify. Log. Move on.</cognitive-note>

## Workflows

<workflow id="pr-lifecycle">
### PR Lifecycle
1. Create branch from main
2. Make changes, commit with conventional commits
3. Push branch, create PR via `gh pr create`
4. Run CI checks
5. Request review if needed
6. Address review comments
7. Merge when green + approved
8. Delete branch
</workflow>

<workflow id="issue-lifecycle">
### Issue Lifecycle
1. Create issue via `gh issue create`
2. Assign labels and milestone
3. Link to PR if applicable
4. Close when resolved
</workflow>

<workflow id="code-review">
### Code Review
1. Fetch PR diff via `gh pr diff`
2. Analyze changes for correctness, security, style
3. Check test coverage
4. Submit review via `gh pr review`
5. Request changes or approve
</workflow>

## Floors
- F1 AMANAH: All GitHub operations are reversible (branch-based).
- F11 AUDITABILITY: Every commit, PR, and review logged.
