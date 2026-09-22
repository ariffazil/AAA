---
name: aforge-test-runner
id: aforge-test-runner
version: 1.0.0
description: "Run A-FORGE tests correctly."
owner: A-FORGE
risk_tier: low
floor_scope: [F1, F2, F11]
autonomy_tier: T0
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# A-FORGE Test Runner — Canonical Commands & Pitfalls

> **Use when:** Running tests in A-FORGE before committing, in audit loops, or when triaging a CI failure.

## The Wrong Way (DON'T)

```bash
cd /root/A-FORGE
npx jest test/apex_g_standardization.test.ts
```

**What happens:** SyntaxError on every `type` modifier in inline imports.

```
SyntaxError: /root/A-FORGE/test/apex_g_standardization.test.ts:
  Unexpected token, expected "," (22:7)
> 22 |   type FloorScores13,
     |        ^
```

`npx jest` (when invoked via `npx`) bundles an older Babel parser that does not support inline `type` modifiers in named imports. Three or four false failures usually look like real bugs but are tooling mismatches.

## The Right Way

```bash
cd /root/A-FORGE
npx tsc -p tsconfig.json          # compile TS → dist/
npm test                          # canonical runner — uses `node --test` on dist/
# OR directly:
node --test dist/test/apex_g_standardization.test.js \
       dist/test/apexEmpirical.test.js \
       dist/test/apex_falsification.test.js \
       dist/test/apexGoodhart.test.js
```

`npm test` is wired via `package.json` → `scripts.test` to invoke `node --test` on the compiled `.test.js` files. This is the canonical runner.

## Why this matters

A real test failure can hide behind a tooling mismatch. Correct sequence:

1. Try `npm test` first.
2. If a test fails, distinguish parse / compile / runtime failure.
3. **Do not edit the test source to "fix" parse errors** — the test file is correct.
4. If `npx jest` is the only tool available, you must transpile the test files first (e.g. via `tsc` then run jest on the `.js` output), or pre-process to strip `type` modifiers.

## Common test files in A-FORGE

```
test/apex_g_standardization.test.ts   ← V3 four-dial geometric mean across 3 modules
test/apexEmpirical.test.ts            ← truth ladder empirical checks
test/apex_falsification.test.ts       ← counterexample search
test/apexGoodhart.test.ts             ← Goodhart resistance
test/agentReadiness.test.ts           ← agent capability suite
test/gAuthority.test.ts               ← CANONICAL_G_SOURCE / CANONICAL_G_MODULE pins
```

All of these use `type` modifiers in imports. All require `tsc` + `node --test` (i.e. `npm test`).

## Real test failure pattern — distinguish from parse error

A real `node --test` failure looks like:

```
not ok 3 - taskJacobian: (0.8,0.8,0.8,0.8) in task entries → local estimate
  ---
  error: |-
    Local estimate should be 0.5888 (got 0.8229)
  code: 'ERR_ASSERTION'
```

This is a genuine assertion failure (test locked to V2 formula, code on V3). Distinguish from parse errors by:

- Parse error: `Unexpected token, expected ","` — tooling mismatch.
- Assertion error: `expected X, got Y` — real divergence.

## Floor notes

- **F2 TRUTH:** Don't claim a test fails because `npx jest` says so. Confirm with the canonical runner first.
- **F11 AUDITABILITY:** When recording test results in a receipt, note which runner was used.
