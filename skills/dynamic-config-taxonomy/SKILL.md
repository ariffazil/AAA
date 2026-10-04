---
name: dynamic-config-taxonomy
description: "Class-level skill for the no-static-literals arifOS substrate doctrine. 6-domain hardcode taxonomy: Model IDs (D1), Agent Topology (D2), Tools/Endpoints (D3), Human Policy (D4), Math Thresholds (D5), World State (D6). Use when auditing config files for hardcoded dynamic values, designing dynamic registries, or extracting static literals to data-driven config."
tags: [dynamic-config, registry, hardcode-taxonomy, 6-domain, arifos-substrate, brittleness]
license: AAA
version: 1.1.0
floor_scope: [F1, F2, F4, F11, F13]
autonomy_tier: T2
---

# Dynamic Configuration Taxonomy

> Undang-undang kekal. Realiti cair.
> Hardcode elemen yang sifatnya dinamik = sistem kaku = geseran = ΔS > 0 = chaos.

## The 6-Domain Taxonomy

### D1 — Model & Intelligence Engines (HARAM to hardcode)
- Model IDs and versions (e.g. gemini-3.6-flash, claude-3-5)
- Context windows, token limits, throughput
- Pricing, cost weights, per-provider wire_api/headers/auth

### D2 — Agent Roster & Federation Topology (HARAM to hardcode)
- Agent roster, counts (333/555/777 ephemeral)
- Node addresses, port bindings, IP topology
- Active worker states

### D3 — Tools & Capabilities (HARAM to hardcode)
- MCP server registrations, endpoints, binary paths
- Network timeouts, latency thresholds
- External API status

### D4 — Human Sovereign (HARAM to hardcode)
- Attention bandwidth (W_scar)
- Preferred communication channels

### D5 — Math Thresholds & Learning Parameters (HARAM to hardcode)
- Decay and regression rates
- Risk weights, error budgets (Ω_0)
- Confidence thresholds (varies by task criticality)

### D6 — World, Environment & Time (HARAM to hardcode)
- Time, dates, timezones (NTP drift)
- File system paths and disk limits (ENOSPC)
- Geopolitical and operational context

## What IS Invariant (static literals are correct)
- Constitutional floors F1–F13
- Math laws (Nash product, cos²+sin²=1)
- Protocol invariants (SCT format, Ed25519)
- Architectural topology (6-layer stack, ECHO/SCAR/ATLAS)

## Audit Procedure
1. Load config — wc -l + print top-level keys
2. Classify every literal — [INV] invariant, [D1]-[D6] dynamic, [EXT] external
3. Build registry (dynamic-registry.yaml) with sections: models, network, mcp, human, thresholds, paths
4. Write builder (opencode-dynamic-builder.py) — reads registry, builds config, provides --diff/--apply/stdout
5. Verify — python3 builder.py --diff shows only structural changes, secrets use ${VAR}
6. Document in /root/memory/H1-capture/

## Pitfalls
- "It's just one value" — even one literal breaks on vendor update day
- Builder may silently drop per-provider per-model options (first pass 91KB to 30KB) — track per-provider config in registry from start, or add --merge-with-current
- Secrets must use ${VAR} references — plaintext = security incident
- Do NOT extract invariants — misclassification = unnecessary indirection
- **Nested `os.environ.get` corruption**: a previous botched env-first patch inserted `os.environ.get(...)` *inside* the default string of another `os.environ.get()`, producing valid-looking but unparseable Python. Always `py_compile` after automated edits; always `git show HEAD:file | grep -n "pattern"` when a value looks suspicious to distinguish corruption from intent.
- **Path mismatches in task specs**: file paths given in instructions may be stale or approximate. Always `search_files()` for the actual location before patching; a wrong path wastes a round-trip and can mask a silent write to the wrong file.
- **`os.environ.get()` returns `str`**: numeric consumers (`timeout`, `port`) require an explicit `float()` or `int()` cast. Omitting it produces a `TypeError` at runtime, not at patch time.

## Worked Example 1: OpenCode (2026-08-12)
- Input: opencode.json (91KB, 178 model IDs, 12 ports, 26 MCP servers)
- Output: dynamic-registry.yaml (15KB) + opencode-dynamic-builder.py (7KB)
- Result: Future vendor updates = edit registry + run --apply

## Worked Example 2: Hermes Federation (2026-08-12)
Full execution across 6 domains on Hermes (FI-008). F13 SOVEREIGN self-executed.
- D1: 12 agent .md `model:` frontmatter deferred to opencode.json registry
- D2: 6 plugin .ts files refactored → `import { ARIFOS_MCP } from "./federation-ports"`; manifest compiler ports → `P("ARIFOS_PORT", 8088)` env-first; 3 profile configs marked INHERITED (DRY next iteration)
- D3: `/root/VAULT999` hardcoded ×3 → `os.environ.get('VAULT999_PATH', ...)`; `hermes_agent_mcp.py` 4 URLs + 3 timeouts env-first
- D4: N/A (clean)
- D5: `cognitive/config.py` 11 constants split: GRANITE (CONFIDENCE_CAP stays in Python) vs WATER (6 constants loaded from `cognitive-params.yaml` with `reload_params()` hot-reload + F7 floor enforcement via `max(0.03, ...)`)
- D6: 7 timeout magic numbers → env var with current value as fallback
- Anti-discovery: drift_monitor module itself had topology drift (ports diverged from organs.yaml)

See: references/hermes-execution-2026-08-12.md (full file list, 5 key patterns, verification scan)

## Key Pattern: Granite vs Water (D5)
Not all D5 constants are WATER. The decision is per-constant:
- **GRANITE** = constitutional floor (F1-F13 bound) → stays in Python source
- **WATER** = empirical, runtime-calibrated → moves to YAML registry
```python
# GRANITE: F7 floor, never changes without sovereign act
CONFIDENCE_CAP: float = 0.90

# WATER: loaded from YAML, clamped to F7 floor at runtime
OMEGA_0: float = max(0.03, _W.get("OMEGA_0", 0.03))
```

## Key Pattern: Env-first refactor with backward compat
Always preserve current behavior until env var is set:
```python
# BEFORE: timeout=60.0
# AFTER:
timeout=float(os.environ.get("HERMES_HEALTH_TIMEOUT", "60.0"))
```
The fallback value = the old hardcoded value. Zero risk of behavior change.

## References
- references/audit-recipe-2026-08-12.md — OpenCode scan procedure and session transcript
- references/hermes-execution-2026-08-12.md — Hermes federation batch 1: TS + D5 YAML + cognitive config + 5 patterns
- references/hermes-execution-batch2-2026-08-12.md — Hermes batch 2: 5 Python files, URL derivation, nested-env.get corruption fix, path verification
- scripts/verify-script-batch2.py — reusable ad-hoc verify template (compile + source scan + regex sweep + clean-subprocess defaults + override)
- templates/opencode-dynamic-builder.py — starter builder script
- Related: substrate/helix-memory-compress (same doctrine applied to memory)
- Related: devops/flame-stage-routing (concrete D5 dynamic thresholds)
- Related: devops/forge-port-architecture (concrete D2 dynamic topology)

---
*Forged 2026-08-12 from F13 SOVEREIGN directive. DITEMPA BUKAN DIBERI*