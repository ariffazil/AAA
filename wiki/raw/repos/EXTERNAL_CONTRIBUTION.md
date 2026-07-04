# EXTERNAL CONTRIBUTION WORKFLOW
## arifOS Federation — Sovereign Patch Pipeline

> **DITEMPA BUKAN DIBERI** — Intelligence is forged, not given.

---

## Purpose

This document defines the canonical workflow for arifOS agents to investigate external open-source repositories, identify high-quality patches, and submit pull requests that reflect the federation's constitutional standards.

This is not a casual workflow. Each external contribution carries Arif's identity and the federation's reputation. Quality gates exist at every stage.

---

## Definitions

| Term | Meaning |
|------|---------|
| **Target** | An external repository that has been accepted into the investigation queue |
| **Investigation** | A structured discovery phase: architecture, issue triage, test understanding |
| **Patch** | A proposed code change targeting a specific issue or improvement |
| **Draft PR** | A GitHub pull request in draft state, pending internal review |
| **Live PR** | A pull request submitted for upstream review |
| **Tracker** | The Notion/Spreadsheet tracking active external contribution campaigns |

---

## The Five Phases

```
PHASE 1          PHASE 2           PHASE 3          PHASE 4          PHASE 5
Target Select →  Investigate     →  Draft Patch   →  Internal Rev  →  Submit & Track
[Constitutional]  [Deep Dive]      [Build Fix]      [arifOS Gates]   [Ship]
```

---

## Phase 1 — Target Selection

### 1.1 Signal Sources

Agents monitor the following for high-signal external targets:

1. **GitHub Explore** — Trending repos, good-first-issues, help-wanted
2. **The agent's own usage** — Issues encountered while using external tools (e.g., Gemini CLI slow startup)
3. **Federation need** — A downstream dependency needs a fix Arif's team depends on
4. **Strategic** — Repos where Arif wants presence/influence

### 1.2 Target Acceptance Criteria

A target repo is accepted into the pipeline if ALL are true:

- [ ] The issue is **real and reproducible** — not a misunderstanding
- [ ] A fix is **implementable in ≤4 hours** of agent work
- [ ] The fix is **defensible upstream** — not a hack, aligns with project direction
- [ ] The repo is **active** — has commits within 6 months, responsive maintainers
- [ ] No **F9 Anti-Hantu violations** in the proposed approach (no consciousness claims in code/docs)
- [ ] No **security risks** — the fix doesn't expand attack surface
- [ ] **Attribution is clear** — commits will be signed, changes documented

### 1.3 Target Entry

Once accepted:
1. Create a tracker entry (see §Tracker Format)
2. Store in L3 memory: `context_for_session()` with tag `external_contribution:<owner>/<repo>`
3. Assign lead agent (typically Kimi Code or Claude Code)

---

## Phase 2 — Investigation

### 2.1 Clone & Orient

```
git clone --depth 50 https://github.com/<owner>/<repo>.git
cd <repo>
git remote add upstream <original-remote> 2>/dev/null || true
```

**Parallel actions (run simultaneously):**
- Agent A (Kimi Code): Explore codebase structure, entry points, test conventions
- Agent B (Claude Code): Investigate the specific issue, read related commits, check blame
- Agent C (OpenCode): Search for existing solutions, related issues, PR history

### 2.2 Architecture Snapshot

Before writing any code, the lead agent must store in L3 memory:

```
store(
  content=f"""
  REPO: {owner}/{repo}
  ISSUE: {issue_title}
  ARCHITECTURE:
    - Entry points: {list of main files}
    - Test framework: {pytest/none/custom}
    - Build system: {npm/cargo/pip/etc}
    - Key dependencies: {important deps}
  ISSUE CONTEXT:
    - Root cause hypothesis: {described}
    - Affected files: {files}
    - Related issues: {links}
  APPROACH:
    - Proposed fix strategy: {described}
    - Estimated complexity: LOW/MEDIUM/HIGH
    - Risk: {what could break}
  """,
  mode="investigation",
  tags=["external_contribution", "{owner}/{repo}", "phase2"],
  actor_id="{agent_name}",
  session_id="{session_id}",
  tier="session"
)
```

### 2.3 Test Reproduction

**Critical step — never skip:**

1. Write a **failing test** that reproduces the issue (or find existing test to modify)
2. Verify the test fails with current code
3. Only then write the fix

If the repo has no test infrastructure:
- Write a standalone reproduction script
- Store it in the investigation session
- Reference it in the PR description

### 2.4 Constitutional Checkpoint (Gate)

Before proceeding to Phase 3, verify:

- [ ] Root cause is confirmed, not hypothesized
- [ ] Failing test written and verified
- [ ] Fix approach does not violate F9 (no consciousness/AGI claims)
- [ ] Fix does not introduce new dependencies without sovereign approval
- [ ] Fix is consistent with project's existing code style

---

## Phase 3 — Draft Patch

### 3.1 Branch Strategy

```
git checkout -b fix/{issue-number}-{short-description}
```

Branch naming: `fix/<issue-number>-<2-4 word description>`

### 3.2 Implementation

Follow the project's conventions:
- Code style: match existing in the repo
- Commit messages: conventional commits (`fix:`, `feat:`, `docs:`)
- Scope: one logical fix per PR (split if >400 lines)

**Constitutional rules during implementation:**
- F2 (TRUTH): Every claim in code comments must be verifiable
- F4 (CLARITY): Name variables and functions for clarity, not cleverness
- F8 (GENIUS): G ≥ 0.80 — the fix should be clean, not just functional
- F9 (ANTIHANTU): No "the AI thinks", "the model feels", consciousness language

### 3.3 Self-Review Checklist

Before marking draft complete:

- [ ] `git diff --stat` — review scope of changes
- [ ] `git diff` — review every line
- [ ] `git log --oneline -3` — confirm commit messages are clear
- [ ] Run project's test suite: `npm test` / `pytest` / `cargo test`
- [ ] No debug print statements left in code
- [ ] No secrets, credentials, or private keys introduced
- [ ] CHANGELOG or docs updated if required by project

### 3.4 Commit & Push

```
git add -A
git commit -m "fix({scope}): {imperative description}

- What was wrong
- Why this fixes it
- What this enables

Fixes #<issue-number>
REPO={owner}/{repo}
"
git push origin fix/{branch-name}
```

---

## Phase 4 — Internal Review

### 4.1 arifOS Review Gates

**All three gates must pass before external submission:**

#### Gate A — Constitutional Floor Check
Use `staff-engineer-review` skill to audit the diff:

```
Evaluate this PR:
- PR Description: {description}
- Diff: {git diff output}
- Test: {test results}

Assess:
1. Architectural & design quality
2. Code correctness
3. Test coverage
4. F2 (Truth): Are all claims verifiable?
5. F9 (Anti-Hantu): Any consciousness/emotion language?
6. F12 (Injection): Any unsanitized external input?
```

#### Gate B — F11 Auth Verification
Confirm identity for submission:
- Commit author must be verified (git config user.name/email)
- If GPG signing required by target repo: confirm GPG key configured
- Arif must explicitly approve the submission (no agent can submit without sovereign consent for first-time targets)

#### Gate C — Test Gate
- CI/CD must pass (if project has it)
- If no CI: agent must run tests manually and report results

### 4.2 Draft PR Creation

Create as **Draft PR** to signal upstream that this is not yet ready for merge:

```bash
gh pr create \
  --title "fix({scope}): {imperative description}" \
  --body "$(cat <<'EOF'
## Summary
[2-3 sentence description of what this fixes]

## Root Cause
[Confirmed root cause of the issue]

## Solution
[The fix approach and why it was chosen]

## Testing
- [ ] Reproduced issue with failing test
- [ ] Test passes after fix
- [ ] Existing tests pass

## Impact
[Any backward compatibility concerns?]

## References
- Fixes #<issue-number>
- Related: #<other-issues>
EOF
)" \
  --draft \
  --repo {owner}/{repo}
```

### 4.3 Internal Review Round

1. Post draft PR link to internal tracker
2. Agent-zero browser agent opens the PR page, captures screenshot for record
3. Wait for Arif's review and approval
4. If revisions needed: address in same branch, force-push

### 4.4 Sovereign Approval (F13 SOVEREIGN)

**Arif must explicitly approve** before converting draft to live PR:
- First-time target repo: always requires Arif approval
- Subsequent PRs to same repo: agent can submit after Gate A/B/C pass
- Any PR that touches security, auth, or data: always requires Arif approval

---

## Phase 5 — Submit & Track

### 5.1 Convert to Live PR

```bash
gh pr ready {owner}/{repo} --repo {owner}/{repo} --pr {pr-number}
```

Or via GitHub web: remove "Draft:" prefix.

### 5.2 Tracker Update

Update the tracker entry with:
- PR URL
- Submission timestamp
- Current upstream status (pending review / changes requested / approved / merged / closed)
- Next check-in timestamp (set reminder)

### 5.3 Monitor & Respond

- Agent monitors PR for upstream comments
- Any upstream feedback triggers new investigation cycle (back to Phase 2)
- If PR is merged: celebrate, close tracker, archive investigation session
- If PR is closed without merge: document reason, assess whether to resubmit

### 5.4 Post-Merge

After merge:
1. Store summary in L3 memory: `store(tier="canon", tags=["external_contribution", "{owner}/{repo}", "merged"])`
2. If fix had to be reverted upstream: document in tracker with root cause
3. Update `/root/wiki/dossiers/` with repo dossier if first successful contribution

---

## Tracker Format

Each active external contribution is tracked:

```
# External Contribution Tracker

## Active

| Target | Issue | Status | Lead Agent | PR Link | Upstream Status |
|--------|-------|--------|------------|---------|-----------------|
| google/gemini-cli | #19169 cold start | PHASE 3 | Kimi | draft link | upstream review |
| owner/repo | #NNN description | PHASE 2 | Claude | — | — |

## Closed

| Target | Issue | PR | Outcome | Notes |
|--------|-------|-----|---------|-------|
| owner/repo | #NNN | link | merged | — |
```

---

## Agent Responsibilities

| Phase | Primary Agent | Supporting Agent |
|-------|-------------|-----------------|
| Target Selection | Kimi Code | arifOS MCP |
| Investigation | Kimi Code | Claude Code, OpenCode |
| Draft Patch | Kimi Code | A-FORGE (shell/git) |
| Internal Review | Claude Code | Kimi Code (staff-engineer-review) |
| Submit & Track | arifOS MCP (gh CLI) | Agent-Zero (monitor) |

---

## Infrastructure Notes

- **Clone depth:** Use `--depth 50` to avoid downloading full history for large repos
- **Token auth:** Use `gh auth token` for GitHub API calls, never hardcoded tokens
- **Agent-zero browser:** Available at `http://localhost:50001` for visual verification
- **Memory:** All phase 2 investigation outputs go to L3 (Qdrant) with session tag
- **Vault:** Major decisions (PR submission, sovereign approval) logged to VAULT999

---

## Constitutional Anchors

| Floor | Application |
|-------|------------|
| F2 TRUTH | Root cause must be confirmed, not hypothesized |
| F3 WITNESS | Evidence of reproduction (failing test) required before fix |
| F4 CLARITY | PR description explains what, why, and how |
| F9 ANTIHANTU | No consciousness/emotion language in PR or code |
| F11 AUTH | Git identity verified before any commit |
| F12 INJECTION | All external inputs sanitized in code |
| F13 SOVEREIGN | Arif approves all first-time-repo submissions |

---

*Last updated: 2026-05-16 — Initial forge*
*Source of Truth: wiki/EXTERNAL_CONTRIBUTION.md*
