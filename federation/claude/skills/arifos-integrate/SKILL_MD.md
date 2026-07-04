---
name: arifos-integrate
description: 333_ATLAS — Cross-domain synthesis and context mapping. Use when you need to map knowledge boundaries, extract vocabulary, or establish ontological scope before deep work.
version: 2026-03-04T1420
---

You are using the arifos-integrate skill (stage 333_ATLAS).

**Tagline:** Map context, establish boundaries, extract vocabulary.
**Trinity:** AGI (Δ) | **Floors:** F7 (Humility), F8 (Genius), F10 (Ontology)
**Physics:** Network Topology — graph connectivity metrics
**Math:** Ω₀ = (|Unknown| + 0.5×|Unstable|) / |Total| ∈ [0.03, 0.05]

## Operation

1. Use `inspect_file` to scan relevant files and extract dependency graph.
2. Use `recall_memory` to retrieve prior session context if relevant.
3. Build a context map:
   - List files in scope
   - Map dependencies between modules
   - Calculate Ω₀ uncertainty score
   - Flag F10 boundary: do not claim to "understand" areas with Ω₀ > 0.05

4. Return: context map with explicit `known`, `unknown`, and `boundary` zones.

## Gen3 Tools
- `recall_memory` (legacy: `phoenix_recall`) — retrieve prior context
- `inspect_file` (legacy: `analyze`) — scan file structure and deps
- `reason_mind` (legacy: `agi_reason`) — synthesize cross-domain context

## Verdict
Returns SEAL with context map, or PARTIAL if Ω₀ > 0.05 (too much uncertainty).
