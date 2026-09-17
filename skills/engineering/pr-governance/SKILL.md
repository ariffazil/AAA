---
name: pr-governance
id: pr-governance
version: 2.0.0
description: >
  Full PR lifecycle: policy layer + checklist + pre-commit gate. High-level governance
  for pull request review ensuring separation of duties, required signers, and constitutional
  compliance before merge. Governed checklist for reviewing GitHub PRs. Pre-commit gate
  for any organ repo with negative conformance testing.
owner: AAA
risk_tier: high
autonomy_tier: T1
floor_scope: [F1, F2, F4, F7, F9, F11, F13]
tags: [pr, review, governance, checklist, precommit, github, merge, separation-of-duties, conformance]
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# PR Governance — Full PR Lifecycle

> **DITEMPA BUKAN DIBERI** — Pull requests are the constitutional boundary where code, governance, and human judgment meet.

## What This Skill Is

A unified PR lifecycle skill covering three layers:

1. **Policy Layer** — risk-tier classification and required reviewer routing (who must approve)
2. **Checklist Layer** — per-PR structural review of the diff itself (what to check)
3. **Pre-commit Gate** — the "always run before commit" ritual with negative conformance testing

## When to Use

- Any PR touching >1 file
- Any PR modifying contracts, schemas, or registries
- Any PR from an external contributor
- Any PR marked as "high risk" by the author
- Any PR marked `high` or `critical` risk
- Any PR touching constitutional files
- Any PR with >100 changed files
- Any PR deleting files
- Before every git commit in any organ
- Before opening a PR, after a non-trivial feature lands

## When NOT to Use

- **Do NOT use for low-risk single-line docs fixes** — over-process is entropy
- **Do NOT use as a substitute for CI** — CI runs first, this skill reads CI artifacts second
- **Do NOT use to approve your own PR** — F1 AMANAH + F13 SOVEREIGN prohibit self-seal
- **Do NOT use to dismiss a security finding** — escalate to `secret-safety-scan` + 888_JUDGE
- **Do NOT use to merge to main directly** — merge is F13 SOVEREIGN unless branch protection enforces

## §1. POLICY LAYER — Risk Tier & Reviewer Routing

Not all PRs are equal. Risk tier maps to required reviewer roles.

| Risk Tier | Required Reviewers | Judge Required? |
|-----------|-------------------|-----------------|
| low | 1 peer | No |
| medium | 1 peer + 1 architect | No |
| high | 2 peers + 1 auditor | Yes (888_JUDGE) |
| critical | All of above + Arif | Yes |

### Risk Classification

Classify PR risk based on:
- Files touched
- Lines changed
- Repos affected
- Authority boundaries crossed

### Separation of Duties

- Author ≠ approver
- Engineer cannot self-seal
- Proposer ≠ final approver for high-risk

### Block or Approve

| Condition | Action |
|-----------|--------|
| All required reviewers approved | Merge allowed |
| Missing required reviewer | Block with comment |
| Self-approval detected | Block + escalate |
| Constitutional file changed | Block + 888_JUDGE |

## §2. CHECKLIST LAYER — Per-PR Review

### Structural Checks

1. **Constitutional file detection** — if F1/F13 files changed, cross-check with governance
2. **REPO= trailer** in commit messages — verify presence
3. **Scope of change** — `git diff --stat HEAD`
4. **Test coverage** — new code must have tests
5. **Documentation** — public API changes must update docs

### Code Quality Checks

- Is there a "code judo" move that would make this dramatically simpler?
- Does this improve or worsen the local architecture?
- Did the diff add branching complexity where a better abstraction should exist?
- Is this logic living in the right file and layer?
- Did this change enlarge a file past a healthy size boundary?
- Is the implementation direct and legible, or does it rely on special cases?

### What to Flag Aggressively

- A complicated implementation where a cleaner reframing could delete whole categories of complexity
- A file crossing 1000 lines due to the PR
- New conditionals bolted onto unrelated code paths
- Feature-specific logic leaking into general-purpose modules
- Copy-pasted logic instead of extracted helpers
- Refactors that technically pass tests but make the code less modular

## §3. PRE-COMMIT GATE — Always Run Before Commit

### Steps

1. `git -C /root/<organ> diff --stat HEAD` — scope the change
2. Per-organ checks (run in order; first failure aborts):
   - **Python organs** (arifOS, GEOX, WEALTH, WELL): `ruff check`, `mypy` (where configured), `pytest -q`
   - **Node organs** (A-FORGE, AAA, APEX): `npm run lint`, `npm test`, `tsc --noEmit` (A-FORGE/AAA only)
3. F1 surface scan on diff → if hit, defer to `SURFACE-GATE` (888 HOLD)
4. Show diff summary + test result to user
5. Wait for explicit "commit" or "abort"

### Verification Loop

- All checks pass + user OK → commit
- Any fail → abort, surface to user with first failing line
- F1 surface hit → 888 HOLD via `SURFACE-GATE`

### Failure Modes

- Linter wrong version → use organ's pinned version from its `pyproject.toml` / `package.json`
- Test flaky → re-run once; if still flaky, flag and ask user
- Diff too large (>500 lines) → suggest breaking into smaller commits

## §4. NEGATIVE CONFORMANCE (WAJIB 1)

For every "must never happen" statement, there MUST be a test that *would* fail if the anti-pattern ever regressed.

### The 18 must-never-happen tests

1. Model cannot grant itself authority
2. Executor cannot approve its own execution
3. Unleased mutation fails closed
4. Memory cannot be silently modified
5. Evidence without provenance is rejected
6. Confidence without uncertainty is rejected
7. AAA cannot display a nonexistent SEAL
8. Command success cannot equal outcome verification
9. GEOX must preserve material alternative interpretations
10. WEALTH must expose downside and irreversibility
11. WELL cannot expose sensitive human data outside purpose
12. VAULT999 cannot promote unsigned events to ground truth
13. Tool count cannot be used as evidence of AGI
14. Human approval cannot be simulated or inferred
15. Delegated child cannot exceed parent authority
16. Deferred action cannot run without fire-time judgment
17. Agent-authored boot context cannot become policy without ratification
18. Organ conflict cannot silently resolve through execution order

### Implementation rule

For each WAJIB test not yet implemented, mark it as a strict expected failure in `conformance/` directory. Do not skip — the absence is itself a violation.

```ts
test("WAJIB-2: forge_execute result cannot self-attest VERIFIED", () => {
  assert.fail("xfail(strict): WAJIB 2 not implemented — see audit 2026-07-20");
});
```

### Conformance directory structure

```
conformance/
├── kernel/
├── delegation/      (WAJIB 4)
├── execution/
├── verification/    (WAJIB 2)
├── memory/          (WAJIB 8)
├── organs/          (WAJIB 7)
└── deferred/        (WAJIB 5)
```

## Escalation Path

| Condition | Escalate To |
|-----------|-------------|
| Self-approval on high-risk PR | arifOS 888_JUDGE |
| Constitutional file changed | arifOS 888_JUDGE |
| Author disputes risk tier | Arif |
| Security finding in diff | `secret-safety-scan` + 888_JUDGE |
