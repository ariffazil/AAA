# Post-Commit Repository Audit Pattern (Node Organs)

> Session: 2026-08-14, A-FORGE apex scalar replication audit (commit b2a0dd7a)
> Applies to: any Node organ (A-FORGE, AAA, APEX) after a feature commit

## The 4-check parallelized audit

Run these in parallel (batch independent reads into one turn):

### 1. Git status — what's uncommitted?
```bash
cd /root/<organ> && git status              # working tree state
cd /root/<organ> && git log --oneline -5    # recent commits
cd /root/<organ> && git show <SHA> --stat   # what the commit touched
```

**Race condition pitfall:** If `git status` shows dirty files but `git status --porcelain`
returns empty moments later, a follow-up housekeeping commit (`chore:`) landed
between the two calls. Check `git reflog -5` to confirm. The working tree state
can change mid-audit when sibling agents are active.

### 2. npm test — any regressions?
```bash
npm test                                    # tsc + node --test dist/test/*
npm test 2>&1 | grep '^not ok'              # list failing suites
npm test 2>&1 | grep -E 'tests |pass |fail '  # summary line
```

**Pre-existing vs regression triage discipline:**
1. Check the commit message itself — does it document known failures?
   (e.g. "5 fail pre-existing EphemeralGenesisRunner")
2. Are the failing test suites the NEW feature's tests? If no → pre-existing.
3. Are the failing test suites infrastructure-dependent (Docker socket, sandbox)?
   If yes → pre-existing environment issue, not a code regression.
4. When in doubt, compare against the parent commit: `git stash && npm test && git stash pop`

### 3. ESM hygiene — .js import suffixes
For Node ESM projects (tsconfig with `moduleResolution: "node16"` or `"bundler"`),
all relative imports in `.ts` source files MUST use `.js` extensions:

```bash
# Check for bare relative imports without .js suffix (should return nothing)
grep -rn 'from "\.\./' src/ | grep -v '\.js"'
```

**Edge case:** If a file like `GovernanceBridge.ts` has zero `import` statements
(self-contained, uses only global `fetch`/`AbortController`), there is no ESM issue
to check — state that explicitly rather than flagging it as a problem.

### 4. TypeScript — zero errors
```bash
npx tsc --noEmit                            # should exit 0 with no output
```

Note: `npm test` already runs `tsc -p tsconfig.json` as its first step. If the full
test suite ran at all, tsc already passed. Use `--noEmit` for a quick standalone check.

## Structured output format

Report results as a summary table with two explicit buckets at the end:

```
| Check              | Status | Detail                                    |
| Git working tree   | ✅     | Clean / dirty (list files)                |
| npm test           | ✅/⚠️  | N/M pass; K fail (pre-existing or new)   |
| ESM .js suffixes   | ✅     | All imports use .js / list violations     |
| TypeScript errors  | ✅     | tsc --noEmit passes with zero errors      |
```

Close with:
- **Needs committing:** (files or "nothing")
- **Needs fixing:** (issues or "nothing urgent")

## Known pre-existing test failures (A-FORGE, as of 2026-08-14)

- `EphemeralGenesisRunner` — 3 suite-level failures (E2E GREEN Flow, Adversarial
  Escape, Failure & Cleanup). These are infrastructure-dependent (Docker socket /
  sandbox availability) and predate the apex scalar replication work. Do NOT count
  these as regressions unless the new feature's test file is among the failures.
- Baseline: 205/210 pass, 5 fail.
