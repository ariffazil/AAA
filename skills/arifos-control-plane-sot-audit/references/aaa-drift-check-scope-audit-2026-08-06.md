# aaa-drift-check.py Scope Audit — 2026-08-06

> WARNING DRIFT 2026-10-14: local mirror /root/forge_work/i-arif-prep ABSENT (probed: dir + *.jsonl missing, depth-5 sweep /root). HF dataset ariffazil/I-ARIF-CANON = live SOT (card 2026-10-04, 1,699 rows, 7 subsets, redteam=100 probes, not 10). Local commands below fail until mirror restored (one-command T1 restore, only on F13 ask; license AGPL research-only, incorporation needs F13 approval).


**File:** `/root/AAA/scripts/aaa_drift_check.py` (~263 lines)
**Trigger:** `make aaa-drift-check` (Makefile line 142–146)
**Exit codes:**
- `0` = SEAL (no blocking drift)
- `1` = PARTIAL (non-blocking gaps documented)
- `2` = HOLD (contradiction blocks autonomous execution)
- `3` = VOID (invalid state)

---

## What the script DOES check (10 sections)

| # | Check | What it does |
|---|---|---|
| 1 | A2A agent cards | Iterates `AAA/a2a/registry/agents.yaml::agents`, verifies `card_path` resolves (skipping `external://` URLs). |
| 2 | AGENTS_UNIFIED.yaml invariants | (a) FI slot uniqueness, (b) identity lanes don't claim FI slots, (c) `canonical_card` paths resolve across 4 layers (`identity_lanes`, `forge_instruments`, `extensions`, `organs`), (d) collapsed agents don't own slots. |
| 3 | Skills registration (AAA-only scope) | Iterates `AAA/skills/*/SKILL.md` ↔ `registries/skills.yaml`. Bidirectional: SKILL.md must be registered; registered skills must have a file. |
| 4 | Registered skill files exist | Verifies `source_path` resolves for each entry in `skills.yaml`. |
| 5 | Tool authority hint presence | Fuzzy-matches "authority" / "gate" / "risk" substring on `registries/tools.yaml` entries. |
| 6 | Live agent card count | Counts `agent-card.json` files under `AAA/rglob`. |
| 7 | Canonical files exist | Checks `AGENTS_UNIFIED.yaml`, `CANONICAL_REGISTRY_POLICY.yaml`, `REGISTRY_CATALOG.generated.yaml`, `bindings.generated.yaml` exist. |
| 8 | Lane identity (333/555/888) | Checks `agent-cards/identity/<lane>/agent-card.json`. |
| 9 | Deprecated/tombstone files in active paths | Headers with `DEPRECATED` / `TOMBSTONE` outside `_archive/`. Threshold: ≤10 = PARTIAL, else ignore. |
| 10 | A2A alignment spec | Exist-checks for `a2a/A2A_ALIGNMENT_SPEC.md`, `a2a/taskstate_verdict_map.json`, `.well-known/agent-card.json`. |

## What the script MISSES (verified 2026-08-06)

### Cross-organ / federation-wide

- ❌ **No cross-organ port check.** Doesn't read `organs.yaml::port_observability` (28 unclassified live ports). Cannot detect SIGNAL/WELL-Witness `:18084` collision or HERMES port mismatch.
- ❌ **No `A-FORGE/contracts/mcp_surface.yaml` reconciliation.** Won't detect the 75/52/44/85/59 tool-count disagreement across A-FORGE SOTs.
- ❌ **No `arifOS/tools_sot.yaml` check.** Cannot catch arifOS SOT drift (currently CONSISTENT per `:8088/health`, but the script doesn't know that).
- ❌ **No authority-ceiling YAML cross-check.** Doesn't read `A-FORGE/a_think/organ_authority_ceilings.yaml` — cannot detect dual-vocabulary contradictions (DISPLAY_ONLY vs T3_888_HOLD etc.).
- ❌ **No FRAME/SIGNAL/arifFlow health probe.** Doesn't reach `:18085`/`:18084`/`:7073` — cannot detect SIGNAL chamber-3-vs-6 split or FRAME 6-vs-7 chamber count.
- ❌ **No RASA wiring state check.** Doesn't read `rasa_wiring_config.py` or `ml_floors` — cannot detect I-ARIF flip-point drift.

### Federation store / receipt integrity

- ❌ **No VAULT999 chain coverage probe.** Lives in `arifOS/Makefile::vault999-verify`, not in AAA's script. (Hash-chain coverage was 0.0297% in live probe — would have caught it.)
- ❌ **No I-ARIF corpus/manifest drift.** Doesn't reach `forge_work/i-arif-prep/manifest.json`.
- ❌ **No SOT `last_verified` date audit.** All SOTs dated >30 days pass silently.

### Coverage scope (skills/tools/lanes)

- ❌ **Scope: AAA skills only.** Per the script comment line 121: `# Only AAA skills/ directory — not .hermes/skills/, agents/_external/*/skills/, etc.`
- ❌ **No-outside-AAA agent cards.** Won't catch issues in `a2a-server/agent-cards/...` (per-agent directory cards).
- ❌ **No pyproject.toml or runtime config validation.** Doesn't read `AAA/pyproject.toml` or unit definitions.
- ❌ **Deprecated backup files not flagged.** `registries/AGENT_MODEL_MAP.json.bak-*` and `skills.yaml.backup.*` files exist alongside live registries; not flagged because they don't have `DEPRECATED/TOMBSTONE` headers.

### Specific gaps already exploited / signaled

- ❌ **No authority-band duplicate detection.** Doesn't traverse `AGENTS_UNIFIED.yaml::forge_instruments[*].id` to see if any ID claims two different authority bands.
- ❌ **No 3-schemas-for-1-organ reconciliation.** The A2A registry has 3 path conventions (`a2a/agent-cards/`, `a2a-server/agent-cards/`, `agents/_external/`) for the same agent — script treats them uniformly without normalization.

## Recommended extensions

If extending this script (NOT DRAFTED — just the shape):

```python
# 1. Cross-SOT tool-count check
def check_tool_sot_drift():
    counts = {
        "live": int(curl_aforgemcp_health().stateless_tools),
        "contracts": yaml_load("/root/A-FORGE/contracts/mcp_surface.yaml").registered_tools,
        "manifest": yaml_load("/root/AAA/federation/federation-manifest.yaml").organs.aforge.tools.mcp_reported,
    }
    if max(counts.values()) - min(counts.values()) > 5:
        finding("CONFLICT", "A-FORGE tool count", f"counts: {counts}", "HOLD")
```

```python
# 2. Authority-ceiling vocabulary dualism
def check_ceiling_vocab():
    for org in ["arifos", "a-forge", "aaa", "geox", "wealth"]:
        a = get_ceilings_yaml().organs[org].ceiling_band_equivalent
        b = get_organs_yaml().components[org].authority_ceiling
        if a and b and a != b and not band_equivalent(a, b):
            finding("CONFLICT", f"{org} ceiling", f"{a} vs {b}", "HOLD")
```

## Bottom line

Whenever asked "does the drift checker catch X?":
- **YES** for: AAA agent cards, AAA skills registration, FI slot collisions in AGENTS_UNIFIED, deprecated files in AAA active paths, A2A spec existence.
- **NO** for: cross-organ SOT reconciliation, organ-source/chamber-count drift, port assignments, authority vocabulary, FRAME/SIGNAL/arifFlow state, VAULT999 hash-chain, I-ARIF corpus drift.

The script is a **complement**, not a **substitute**, for federation-wide audit. Do NOT promise "drift check passed" for cross-organ claims.
