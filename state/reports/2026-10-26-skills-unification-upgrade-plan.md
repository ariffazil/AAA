# AAA Skills Unification & Upgrade Plan — FI-008, 2026-10-26

> Status: F13 ratification requested. Executed during the unified-main session (main = cd665759).
> One problem, one owner, one path (Anti-Bangang LAW 8). Every number below is a live-probe count, not an estimate.

## What already landed this session (DONE, verified)

1. **Single canonical catalog**: `/root/AAA/skills` (786 top-level entries; 694 SKILL.md at depth-1 dirs; 1146 SKILL.md total incl. domains tree). All five harnesses consume it:
   - `.claude/skills` → direct symlink to AAA/skills (786 entries, 0 broken)
   - `.grok/skills` → direct symlink (786, 0 broken)
   - `.kimi-code/skills` (824), `.qwen/skills` (790), `.config/opencode/skills` (784) → per-skill symlinks, 0 broken after repair
2. **Wiring repair**: 54 dangling links removed, 39 organ-lane links re-pointed to their post-`23b0cdf3` homes (GEOX/WEALTH/WELL/skills + AAA domains). 5 names absorbed as references inside other skills (e.g. `web-ops/references/agi-web-optimization.md`) — deliberately not resurrected.
3. **Today's skill content unified into main**: F-9 frontmatter enrichment (PR #215, 194 skills), ratify-branch citizen skills (`FORGE-mcp-smoke-test`, `FORGE-verify-runtime`, `AAA-voice-suara-siti`), atlas_* frontmatter retained.
4. **A2A aligned**: `registry_alignment_check.mjs` → PASS (INV-REG-7, INV-AR-5, L4 port parity, INV-AR-6); gateway :3001 live on A2A v1.0 card+JSON-RPC (getCard/tasks/list exercised); `a2a/` + `federation/protocols/arifos-hermes-gate-hook.py` (reality-gated version) now on main.
5. **Frontmatter hygiene**: sampled first 400 canonical SKILL.md — 0 missing `name:`.

## Catalog reality (counts that drive the plan)

- AAA canon top-level entries: 786 — but only ~400 are live skills; the rest are pointer stubs (10 explicit "Alias →" headers found; the 2026-10-23/25 entropy merges planned 110 collapsed aliases — `skill-alias-map.md`), archives (`.archive*`), taxonomy meta-files (`*.json/*.md/*.yaml` at root ≈ 25).
- Kimi-local extras: 73 — most are registry/inventory JSON/MD (governance artifacts), plus ~12 real skill dirs that exist ONLY in kimi scope (never adopted to canon).
- Duplicates across roots: 0 by name after the domain-tree reorg (find-based dedupe confirmed the earlier "duplicate SKILL.md names" are the same file seen through symlinks).

## Upgrade phases (each independently ratifiable)

### P1 — Adopt-then-point (kimi-local citizens → canon)
Move the ~12 real skills living only in `.kimi-code/skills/` into `AAA/skills/` via `canon-mutate`, replace the locals with symlinks. Zero behavior change for kimi; every other warga gains the capability.
Exit test: `comm -13` between canon and each harness returns only harness-private registry files.

### P2 — Index regeneration from disk (kill stale-catalog class)
Regenerate `skills/SKILLS_INDEX.json` + `capabilities/skill-index.generated.json` from the live tree (script in `scripts/curator-*`), with a hash-of-manifest provenance field, so "catalog says X, disk says Y" cannot recur (the failure this session found twice: 54 dangling links, stale catalog entries for absorbed skills).
Exit test: index entries resolve 100% to on-disk SKILL.md (INV-AR-5 baseline 0).

### P3 — Pointer-stub retirement
The 10 "Alias →" stubs + `skill-alias-map` survivors: keep for one release cycle, then move to `archive/skills-frozen-20261019`-style storage. Discovery must go through one router (`zen-router` / `aaa-capability-compiler`), not through 110 aliases.
Exit test: harness listings show no skill whose entire body is a pointer.

### P4 — Trigger-collision sweep (one load per job)
Run `FORGE-skill-linter` across the canon: every skill needs non-overlapping trigger phrases; collisions resolved by collapsing to owner + alias stub (P3 pattern). Start with the known hot clusters: firecrawl-* (24 skills), apex*/APEX* (~12), persona-voice-* (~8), qwencloud-* (~11), geox-* (~12).
Exit test: linter reports 0 unresolved trigger collisions in the top-5 clusters.

### P5 — Activation equivalence test (REA the skills, don't trust the listing)
One fixture task per phase-critical cluster, dispatched identically on claude/kimi/qwen/opencode; assert the same canonical skill resolves on all four. This is the first *behavioral* (not inventory) proof of unification — per the FI-002 audit lesson: inventory evidence ≠ behavioral evidence.
Exit test: 4-harness resolution matrix stored in `state/reports/`.

## Explicit non-goals
- No new registries/dashboards (LAW 3).
- No mass deletion of the domains/ tree — archives stay frozen, untouched.
- No authority changes: skills are capability text; execution authority stays with the kernel/actuator gates exactly as wired today.

## Ratification request
P1+P2 are reversible and mechanical — ready to execute on "go".
P3–P5 need one decision each (retire date, collision owner map, fixture set).
