---
name: FORGE-precommit-review
description: "Pre-commit gate for any organ repo. Runs lint, type-check, test, constitutional surface scan, and shows the diff to the user. Use before every git commit in any organ. Delegates F1-surface detection to f1-gate."
when_to_use: "Before every git commit in any organ. Also: before opening a PR, after a non-trivial feature lands."
disable-model-invocation: false
allowed_tools: [Bash, Read, Grep]
---

# Precommit Review

The "always run this before commit" ritual. Mirrors the federation's commitment to reversibility and verifiability.

## Steps
1. `git -C /root/<organ> diff --stat HEAD` — scope the change
2. Per-organ checks (run in order; first failure aborts):
   - **Python organs** (arifOS, GEOX, WEALTH, WELL): `ruff check`, `mypy` (where configured), `pytest -q`
   - **Node organs** (A-FORGE, AAA, APEX): `npm run lint`, `npm test`, `tsc --noEmit` (A-FORGE/AAA only)
3. F1 surface scan on diff → if hit, defer to `f1-gate` (888 HOLD)
4. Show diff summary + test result to user
5. Wait for explicit "commit" or "abort"

## Verification loop
- All checks pass + user OK → commit
- Any fail → abort, surface to user with first failing line
- F1 surface hit → 888 HOLD via `f1-gate`

## Failure modes
- Linter wrong version → use organ's pinned version from its `pyproject.toml` / `package.json`
- Test flaky → re-run once; if still flaky, flag and ask user
- Diff too large (>500 lines) → suggest breaking into smaller commits

## Reference
- Per-organ commands: each organ's `Makefile` or `package.json scripts`
- F1 surfaces: see `f1-gate` skill
