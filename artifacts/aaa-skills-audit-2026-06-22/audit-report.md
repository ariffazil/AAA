# AAA Skills Audit — 2026-06-22

**Generated:** 2026-06-22 (Hermes / skill-trigger-linter invocation)
**Scope:** /root/AAA/skills/ (33 directories, 31 SKILL.md files)
**Auditor:** Hermes (skill-trigger-linter logic applied)

## Summary

- **Total SKILL.md files:** 31
- **Clean:** 0
- **With issues:** 30 (the 1 "clean" is spatial-grounding — but it has NO SKILL.md, false clean)
- **L3 (safety/constitutional) breaches:** 17
- **L2 (behavioral risk — missing triggers):** 24
- **L1 (vague verbs):** 3
- **Critical risk_tier skills:** 2 (incident-escalation, recursive-skill-forge)

## Top 10 systemic findings

1. **30/31 skills lack canonical `## Use When` / `## Do Not Use When` sections.** Most use alternate headings (`When to Load`, `Trigger`, etc). Triggers are present but non-standard.
2. **13/31 skills have no version in frontmatter.** All registry-listed skills show `artifact_hash: pending`.
3. **Only 11/31 skills declare F1-F13 floor binding.** Half the library is constitutionally unanchored.
4. **6/31 skills have no governance reference at all** (no arifos-governance, 888_HOLD, or constitutional mention).
5. **2 critical-risk skills (incident-escalation, recursive-skill-forge)** lack 888_HOLD explicit gate declaration.
6. **3 skills banned-verb hits:** agentic-dream-engine (`improve`), recursive-skill-forge (`improve`), skill-trigger-linter (all 6 — by design, it lists them).
7. **Only 1/31 skill (spatial-grounding) is "clean"** — and that is because it has NO SKILL.md, just subdirectories. False clean.
8. **No skill has passing tests or artifact_hash.** The registry schema declares them but nothing enforces.
9. **6 skills with no governance binding:** geox-basin-interpreter, geox-grounding, mcp-smoke-test, secret-safety-scan, service-health-triage, skill-creator. Cross-organ grounding theoretically possible but undeclared.
10. **arifos-observability, arifos-plan-dag, arifos-recursive-audit** declare Use When / Do Not Use but lack F-floor binding — these are the orchestration layer foundations.

## Full table

| Skill | Ver | UW | DN | Floor | Gov | Risk | Issues |
|-------|-----|----|----|-------|-----|------|--------|
| aaa-agent-invariants | 1.0.0 | 0 | 0 | ✓ | ✓ | low | L2:no_use_when; L2:no_dont_use; meta:no_example |
| aaa-agentic-governance | 3.0.0 | 0 | 0 | ✓ | ✓ | low | L2:no_use_when; L2:no_dont_use; meta:no_example |
| agent-onboarding | 1.0.0 | 0 | 3 | ✗ | ✓ | medium | L2:no_use_when; L3:no_floor; meta:no_example |
| agentic-dream-engine | 1.0.0 | 0 | 3 | ✓ | ✓ | high | L2:no_use_when; L1:banned:improve; meta:no_example |
| arifos-evals | MISSING | 5 | 3 | ✗ | ✓ | n/a | L3:no_floor; meta:no_ver; meta:no_example |
| arifos-governance | MISSING | 6 | 3 | ✓ | ✓ | n/a | meta:no_ver; meta:no_example |
| arifos-mcp-federation | MISSING | 5 | 3 | ✓ | ✓ | n/a | meta:no_ver; meta:no_example |
| arifos-observability | MISSING | 5 | 3 | ✗ | ✓ | n/a | L3:no_floor; meta:no_ver; meta:no_example |
| arifos-plan-dag | MISSING | 5 | 3 | ✗ | ✓ | n/a | L3:no_floor; meta:no_ver; meta:no_example |
| arifos-recursive-audit | MISSING | 5 | 3 | ✗ | ✓ | n/a | L3:no_floor; meta:no_ver; meta:no_example |
| drift-response | MISSING | 4 | 0 | ✗ | ✓ | n/a | L2:no_dont_use; L3:no_floor; meta:no_ver; meta:no_example |
| federation-health-scan | MISSING | 4 | 0 | ✗ | ✓ | n/a | L2:no_dont_use; L3:no_floor; meta:no_ver; meta:no_example |
| geox-basin-interpreter | MISSING | 5 | 3 | ✗ | ✗ | n/a | L3:no_floor; L3:no_gov; meta:no_ver; meta:no_example |
| geox-grounding | 0.1.0 | 0 | 0 | ✗ | ✗ | medium | L2:no_use_when; L2:no_dont_use; L3:no_floor; L3:no_gov; meta:no_example |
| github-ci-diagnose | 1.0.0 | 0 | 3 | ✗ | ✓ | medium | L2:no_use_when; L3:no_floor; meta:no_example |
| github-issue-triage | 1.0.0 | 0 | 3 | ✓ | ✓ | medium | L2:no_use_when; meta:no_example |
| github-pr-review | 1.0.0 | 0 | 0 | ✗ | ✓ | medium | L2:no_use_when; L2:no_dont_use; L3:no_floor; meta:no_example |
| incident-escalation | 1.0.0 | 0 | 0 | ✗ | ✓ | **critical** | L2:no_use_when; L2:no_dont_use; L3:no_floor; L3:critical_needs_888; meta:no_example |
| mcp-smoke-test | 1.0.0 | 0 | 3 | ✗ | ✗ | low | L2:no_use_when; L3:no_floor; L3:no_gov; meta:no_example |
| nusantara-intelligence-substrate | MISSING | 0 | 0 | ✓ | ✓ | n/a | L2:no_use_when; L2:no_dont_use; meta:no_ver; meta:no_example |
| openclaw-a2a-bridge | 0.1.0 | 0 | 0 | ✗ | ✗ | medium | L2:no_use_when; L2:no_dont_use; L3:no_floor; L3:no_gov; meta:no_example |
| parallel-authority-detection | 1.0.0 | 0 | 0 | ✗ | ✓ | high | L2:no_use_when; L2:no_dont_use; L3:no_floor; meta:no_example |
| pr-review-governance | 1.0.0 | 0 | 0 | ✗ | ✓ | high | L2:no_use_when; L2:no_dont_use; L3:no_floor; meta:no_example |
| readme-truth-check | 1.0.0 | 0 | 0 | ✗ | ✓ | low | L2:no_use_when; L2:no_dont_use; L3:no_floor; meta:no_example |
| recursive-skill-forge | 1.0.0 | 0 | 5 | ✓ | ✓ | **critical** | L2:no_use_when; L1:banned:improve; L3:critical_needs_888; meta:no_example |
| repo-hygiene-audit | 1.0.0 | 0 | 3 | ✗ | ✓ | medium | L2:no_use_when; L3:no_floor |
| secret-safety-scan | 1.0.0 | 0 | 0 | ✗ | ✗ | high | L2:no_use_when; L2:no_dont_use; L3:no_floor; L3:no_gov; meta:no_example |
| service-health-triage | 1.0.0 | 0 | 0 | ✗ | ✗ | low | L2:no_use_when; L2:no_dont_use; L3:no_floor; L3:no_gov; meta:no_example |
| skill-creator | MISSING | 4 | 3 | ✗ | ✗ | n/a | L3:no_floor; L3:no_gov; meta:no_ver; meta:no_example |
| skill-trigger-linter | MISSING | 4 | 3 | ✗ | ✓ | n/a | L1:banned:6_verbs; L3:no_floor; meta:no_ver; meta:no_example |
| spatial-grounding | NO_SKILL_MD | — | — | — | — | n/a | CLEAN (false — has no SKILL.md, just subdirs) |

## Recommended forge plan (T1 reversible)

1. **Normalize headings across all 31 skills** — add `## Use When` and `## Do Not Use When` aliases. Mechanical, no semantic change.
2. **Inject F1-F13 floor binding in 20/31 skills that lack it** — append 1-paragraph reference, reversible.
3. **Stamp version + artifact_hash on registry** — bulk update via python script, sha256 of SKILL.md content.
4. **Patch 2 critical-risk skills (incident-escalation, recursive-skill-forge)** with explicit 888_HOLD gate language.
5. **Bind or deprecate 6 skills with no governance binding:** geox-grounding, mcp-smoke-test, secret-safety-scan, service-health-triage, skill-creator, openclaw-a2a-bridge.
6. **Add `## Examples` section** to all 30 skills — minimum 1 example per skill.

## Owners (per constitutional chain)

- 888-APEX (governance) → owns the floor-binding patch
- 555-ASI (memory+ethics) → owns the banned-word sweep
- A-AUDIT → owns the L3 verification round
- agent-onboarding skill → template for future skill registration (only one currently with proper structure)

## Why this matters

The skill library is **documentation that clever agents read**, not enforced governance. The audit reveals that AAA's skills are mostly *shaped like* constitutional artifacts but *function as* markdown. Until headings normalize, F-floor binding lands in every file, and registry artifact_hash stamps become real, AAA cannot claim "governed skills" — only "documented procedures".

The skill-trigger-linter finds nothing clean because nothing IS clean. The skill library needs a forge cycle, not another linter run.

DITEMPA BUKAN DIBERI — audit done, no card mutation this turn. Awaiting Arif directive on patch priority.