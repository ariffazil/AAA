---
name: kimi-rsi-apex-contrast
description: RSI APEX contrast for Kimi Code — before emitting the entropy-delta report, ask "Is this measurement reproducible? Could a different agent run the same tools and get the same numbers?"
license: Proprietary
version: 1.0.0
owner: F13 SOVEREIGN — Muhammad Arif bin Fazil
---

# RSI — APEX Contrast Skill (Kimi Code)

Before emitting the entropy-delta report, RSI MUST run a **measurement-reproducibility** check. If a different agent running the same tools gets different numbers, the measurement is theater, not science.

## The Pattern

Append to `A-FORGE/forge_work/YYYY-MM-DD/<session_id>/rsi-apex-check.md`:

```markdown
# RSI APEX Reproducibility Check

## Tools used
- [ ] `radon cc .` (Python cyclomatic complexity)
- [ ] `lizard .` (multi-lang)
- [ ] `jscpd .` (duplication)
- [ ] `knip` or `vulture` (dead code)
- [ ] `pyflakes` / `ts-prune` (unused imports)
- [ ] `wc -l` (file sprawl)
- [ ] Other: <list>

## Tool versions
<each tool's --version, snapshotted to ensure reproducibility>

## Tool reliability (omega_0)
For each tool:
- radon: omega_0 = 0.05 (mature, deterministic)
- lizard: omega_0 = 0.05 (mature, deterministic)
- jscpd: omega_0 = 0.10 (heuristic, false positives possible)
- knip: omega_0 = 0.10 (heuristic)
- vulture: omega_0 = 0.15 (heuristic, conservative)
- pyflakes: omega_0 = 0.03 (very mature, deterministic)
- wc -l: omega_0 = 0.01 (perfectly deterministic)

## Reproducibility test

Could a different RSI agent (different LLM, same tools, same commit SHA) produce:
- [ ] The same file count?  ___ Y / N
- [ ] The same cyclomatic_avg (within ±0.1)?  ___ Y / N
- [ ] The same duplication_pct (within ±0.5%)?  ___ Y / N
- [ ] The same dead_code count?  ___ Y / N

If any N → the measurement is heuristic, not deterministic. Mark with omega_0 in the report.

## Refactor-list reproducibility

For each refactor in `rsi-entropy-delta.md`:
- [ ] Could a different RSI agent identify the same top-3 refactors?  ___ Y / N
- [ ] Are the refactor targets (files, functions) unambiguous?  ___ Y / N
- [ ] Is the rationale reproducible (same code, same conclusion)?  ___ Y / N

If any N → the refactor list is opinionated. Mark as "RSI opinion" not "ground truth".

## F2 TRUTH — the measurement must be honest

If I cannot reproduce the measurement, I MUST say so in the report:

```markdown
# Honest entropy assessment

## Reproducible (omega_0 ≤ 0.05)
- file count: 142 (wc -l)
- cyclomatic_avg: 4.2 (radon)
- file sprawl delta: -4 (wc -l before/after)

## Heuristic (omega_0 = 0.10-0.15)
- duplication_pct: 5.1% (jscpd — heuristic, may vary ±1%)
- dead_code count: 41 lines (vulture — conservative, may miss 5-10%)

## Opinion (omega_0 = 0.30+)
- "top 3 refactors" — these are RSI judgement, not measurement
```

## Kimi-Specific Additions

- Use `mcp__aforge__forge_worktree` before RSI to establish git baseline.
- Attach entropy report to `A-FORGE/forge_work/YYYY-MM-DD/<session_id>/rsi-entropy-delta.md`.
- If entropy reduction cannot be measured, declare ΔS = UNKNOWN and escalate.

## Why this matters

- **F2 TRUTH**: Reproducible measurements are the only honest ones.
- **F7 HUMILITY**: Mark every measurement with its reliability (omega_0).
- **F11 AUDIT**: Reproducible measurements are auditable.

## Anti-patterns to avoid

- ❌ "Complexity is down 15%" without showing the tool + version + run command
- ❌ "Dead code reduced by 50%" without naming the specific lines
- ❌ "The codebase is cleaner now" (no metric = no claim)

---

**DITEMPA BUKAN DIBERI** — measure, then claim, never claim before measure.
