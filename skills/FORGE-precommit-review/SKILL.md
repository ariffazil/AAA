---
name: FORGE-precommit-review
description: "Pre-commit gate for any organ repo. Runs lint, type-check, test, constitutional surface scan, and shows the diff to the user. Use before every git commit in any organ. Delegates F1-surface detection to SURFACE-GATE (the live kernel probe hook that verifies canonical tools are still exposed)."
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
3. F1 surface scan on diff → if hit, defer to `SURFACE-GATE` (888 HOLD)
4. Show diff summary + test result to user
5. Wait for explicit "commit" or "abort"

## Verification loop
- All checks pass + user OK → commit
- Any fail → abort, surface to user with first failing line
- F1 surface hit → 888 HOLD via `SURFACE-GATE`

## Failure modes
- Linter wrong version → use organ's pinned version from its `pyproject.toml` / `package.json`
- Test flaky → re-run once; if still flaky, flag and ask user
- Diff too large (>500 lines) → suggest breaking into smaller commits

## Reference
- Per-organ commands: each organ's `Makefile` or `package.json scripts`
- F1 surfaces: see `SURFACE-GATE` — the live kernel probe hook that verifies canonical tools are still exposed pre-commit

---

## Negative Conformance (WAJIB 1 — added 2026-07-19)

For every "must never happen" statement, there MUST be a test that *would* fail if the anti-pattern ever regressed. An absent test becomes forgotten; a strict xfail stays visible.

### The 18 must-never-happen tests (per ARIFOS-READINESS-2026-07-20)

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

For each WAJIB test that is **not yet implemented** (cannot be written yet because the substrate doesn't exist), mark it as a strict expected failure in `conformance/` directory. Do not skip — the absence is itself a violation of WAJIB 1's "absent test becomes forgotten" principle.

```ts
// Example: WAJIB 2 (independent verifier) — not yet implemented
test("WAJIB-2: forge_execute result cannot self-attest VERIFIED", () => {
  // TODO when WAJIB 2 lands: forge_execute returns receipt without verification lane → DENY
  assert.fail("xfail(strict): WAJIB 2 not implemented — see audit 2026-07-20");
});
```

### Conformance directory structure (per audit)

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

When committing to A-FORGE, PolicyGate, or any organ with security surface, run the conformance tests for that surface BEFORE the regular precommit checks.

### Authority scope

Negative conformance tests are **T1 AUTO-DO** — adding/upgrading them does not require F13. The decisions they ENFORCE were already ratified; the tests just verify them.

