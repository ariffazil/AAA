---
name: safe-refactor
description: "Use when restructuring code that already works — change structure without changing behaviour, with a baseline, a rollback point, and named HOLD conditions."
version: 1.0.0
owner: AAA
risk_tier: medium
autonomy_tier: T1
floor_scope: [F1, F2, F4, F11]
tags: [refactor, restructure, behavior-preserving, baseline, rollback, blast-radius]
capability_tier: fed-agent
ecology_state: WARM
---

# Safe Refactor — structure changes, behaviour does not

A refactor is a claim that behaviour is unchanged. That claim is only admissible with a
baseline captured *before* the first edit and a comparison run *after* the last one.
Without both, what you have is a rewrite with nobody watching.

Covers: extract/split, rename, move, monolith split, dependency inversion, dead-code
removal. Does **not** cover: feature work, bug fixes, schema migrations, format sweeps.

## Procedure

1. **Capture the baseline.** Run the existing test suite and record `command → exit code →
   pass/fail counts`. If no suite exists, capture the observable behaviour instead (probe
   output, CLI transcript, HTTP responses) — an empty baseline means the refactor is
   unverifiable, which is a HOLD, not a green light.
2. **Resolve the live path first.** Duplicated code is the norm in this federation.
   `production-source-disambiguation` before any edit: confirm which file the running
   process actually loads (systemd `ExecStart`, `dist/` vs `src/`, symlink target).
   Editing a copy is the canonical wasted session.
3. **Inventory symbols and consumers.** Every renamed or moved symbol: `grep -rl` across
   organs, plus dynamic-dispatch check (string lookups, reflection, `importlib`, config
   keys, route tables). Unresolved consumers → HOLD.
4. **Declare the contract surface.** Public API, serialized payloads, DB columns, env var
   names, MCP tool signatures, file paths other repos read. Anything outside the declared
   surface is out of scope for this refactor.
5. **One intention per commit.** Separate: move-only, rename-only, logic-extraction,
   dead-code-deletion. A reviewer must be able to see one intention per diff.
6. **Re-run the baseline comparison.** Same commands, same inputs. Diff must be class-equal
   for behaviour (test counts, exit codes, output shape) — say explicitly which outputs
   were allowed to differ and why.
7. **Keep the rollback point explicit.** Name the commit/`git stash`/backup that restores
   the last known good state, and confirm the diff is revertible (no force-push, no
   history rewrite, no irreversible migration).

## HOLD conditions (stop, do not "proceed carefully")

- No baseline behaviour captured or capturable.
- Rename/move across unknown consumers, dynamic dispatch unresolved.
- Migration not reversible (data loss, dropped column, one-way format change).
- Generated and source files mixed in the same tree (edit the source, never the output).
- Locked canonical tree (`chattr +i`) mutated outside `canon-mutate`.
- Concurrent writer on the same files (`concurrent-agent-writers`) unacknowledged.
- Refactor bundled with a behaviour change, so the diff cannot be attributed.

## Federation specifics

- **Locked trees.** `/root/AAA/{skills,instructions,governance,canon,instructions}`,
  `/root/arifOS/GENESIS`, organ `.git` dirs are immutable. Use
  `ARIFOS_TRACE_ID=trc-… /root/scripts/canon-mutate run <tree> -- <cmd>`; never `chattr -i` by hand.
- **Symlinked skill trees.** `/root/.claude/skills`, `/root/.agents/skills`,
  `/root/.opencode/skills` point at `/root/AAA/skills`. Edit the source, not the link.
- **A-FORGE `dist/` trap.** `npm test` runs compiled `dist/`; source edits need
  `npm run build` before tests mean anything.
- **Bootstrap anchors.** A-FORGE `Bootstrap.ts`, `BootstrapRuntime.ts`, `godelLock.ts`,
  `EgressPolicy.ts`, `src/domain/forge/`, `arifOS mcp_server/server.py` tool signatures —
  refactoring these changes the constitution's blast radius; require 888 before touching.
- **Commits.** `git-lane <lane> -C /root/<repo> commit -m "refactor: …"` — plain
  `git commit` fails by design in governed repos.

## Anti-pattern

```
error/review → speculative multi-file edit → new error → more edits → accidental pass
```

Required: `baseline → inventory → contract → minimal intention → verification → receipt`.

## Output contract

```
SCOPE:      <files touched> / <files intentionally untouched>
BASELINE:   <command> → <exit code / counts> (captured before)
INVENTORY:  <symbols> → <consumers found / unresolved>
HOLD:       <condition> (if any fired — stop here)
VERIFY:     <command> → <after counts> → <behavioural delta: none | named>
ROLLBACK:   <commit / stash / backup>
STATE:      PRODUCED ≠ VERIFIED ≠ DEPLOYED — name which one you reached
```

*Forged 2026-10-27 (333-AGI) after external catalog audit found no federation owner for
behaviour-preserving restructuring. DITEMPA BUKAN DIBERI.*
