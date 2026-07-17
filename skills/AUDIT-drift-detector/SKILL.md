---
name: AUDIT-drift-detector
description: >
  Real-time drift detection across tool manifests, agent cards, and skill registries.
  Compares live state against saved baselines and reports mismatches. Runs as a
  periodic audit or on-demand before SEAL operations. USE WHEN: "check drift",
  "verify registry", "detect manifest drift", "tool surface audit".
version: 1.0.0
tags: [drift, audit, registry, manifest, F2, F11]
floor_scope: [F02, F04, F11]
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
