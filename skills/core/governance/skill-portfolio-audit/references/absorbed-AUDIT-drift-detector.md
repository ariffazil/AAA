# Absorbed: AUDIT-drift-detector

> **Provenance.** Pre-merge body of the `AUDIT-drift-detector` skill, tombstoned 2026-09-16T22:42:00Z by Wave 2 (`moved_to: core/governance/skill-portfolio-audit/SKILL.md`).
> Recovered verbatim from `/root/.hermes@entropy-wave2-pre-act-20260916T144144Z:skills/AUDIT-drift-detector/SKILL.md` — content was never carried into the target by the
> original consolidation; recovered 2026-09-17 to complete the recorded merge.
> Original sha256 (tombstone `sha256_before`): `4481e8d529de4aaf66b391650ce6cc4132d7b98895d967c6707d1a6df74ca308`
> Recovery sha256: `4481e8d529de4aaf66b391650ce6cc4132d7b98895d967c6707d1a6df74ca308`
> The `AUDIT-drift-detector` routing name stays retired — this file is a reference, not a skill.

---

# AUDIT-drift-detector

## Purpose
The federation has multiple registries (tool_registry.json, agent cards, SKILL_ALIAS_TABLE, affordances.yaml). Drift between them causes routing failures, orphaned skills, and silent capability loss.

## Drift Dimensions
1. **Build vs Runtime Manifest Drift** — Canonical drift check via `arifOS/runtime/manifest.py` (`build_manifest` vs `runtime_manifest`). This is the primary drift detection mechanism post-KSR Epoch 1+2.
2. **Tool Manifest Drift** — Live MCP tools vs registered tools vs agent card references
3. **Skill Registry Drift** — SKILL_ALIAS_TABLE vs actual directories vs agent card skill IDs
4. **Agent Card Drift** — Card skill IDs vs existing skill directories
5. **Schema Drift** — Tool input schemas vs documented schemas
6. **Floor Drift** — Declared floor_scope vs actual floor enforcement
7. **Verdict Taxonomy Drift** — Verdict emissions vs closed 6-value set (OBSERVE_ONLY|SEAL|SABAR|VOID|HOLD|888_HOLD)

## Detection Pipeline
1. **Snapshot** — Capture current state of all registries
2. **Compare** — Diff against saved baseline (or last-known-good)
3. **Classify** — Each mismatch: CRITICAL (breaks routing), WARNING (orphan), INFO (cosmetic)
4. **Report** — Structured drift report with fix recommendations
5. **Escalate** — CRITICAL drift → 888_HOLD before any SEAL operation

## ⚠️ Runtime-Injected Files (2026-07-19)

Some organ services modify files at runtime. Known patterns:
- **WELL `index.html`**: WebMCP adapter injected on service start → dirty after commit
- **arifOS session-state**: Runtime state files that change during operation

When dirty after clean commit: check if injected content was already committed → if yes, re-commit; if no, actual drift.

## Baselines
- **Canonical drift check**: `arifOS/runtime/manifest.py` — `build_manifest` vs `runtime_manifest` (post-KSR Epoch 1+2)
- Tool registry: `/root/arifOS/tool_registry.json`
- Agent cards: `/root/AAA/a2a-server/agent-cards/`
- Skill alias: `/root/AAA/skills/SKILL_ALIAS_TABLE.json`
- MCP surface: Live `tools/list` from each organ
- Verdict taxonomy: `arifOS/runtime/verdict.py` — closed 6-value set

## Floors
- F2 TRUTH: Report only what is actually observed. No inference without evidence.
- F4 CLARITY: Drift report must be actionable, not noise.
- F11 AUDITABILITY: Every drift check logged with timestamp and findings.
