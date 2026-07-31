# 🔤 MCP Tool Naming Convention — arifOS Federation Standard

> **Forged:** 2026-07-31 by 333-AGI under F13 directive (Arif)
> **Supersedes:** v1.0 skeleton (2026-07-24, 42 lines)
> **Authority:** F13 SOVEREIGN — binding on all future tool registrations
> **SOT:** `/root/AAA/docs/MCP_NAMING_STANDARD.md`
> **Doctrine:** DITEMPA BUKAN DIBERI — Naming is the first act of creation.

---

## 0. WHY NAMING IS THE FIRST ACT OF CREATION

> **`name` is machine contract — never rename after publish.**

The MCP protocol namespaces tools as `{server}_{tool_name}`. When an agent calls a tool,
the name is the only navigation signal. Four reasons naming is first:

1. **Ontology gate (F10).** The name defines what category the thing belongs to.
   `arif_judge` is governance. `geox_seismic_compute` is Earth physics. A collision is a category error.

2. **Authority routing.** The prefix (`arif_`, `forge_`, `geox_`, `capital_`, `well_`, `hermes_`, `flow_`)
   is the routing signal. `arif_route` dispatches to the correct organ by prefix match.
   A misnamed tool is a misfired intent.

3. **Agent discoverability.** The LLM scans tool names to decide what to call.
   A tool named `capital_primitive` signals "compute capital math."
   A tool named `foo_bar` signals nothing — and the model won't call it.

4. **Immutability.** You can change behavior. You cannot change the name without
   breaking every reference — every agent, every seal chain, every script.
   **The name survives everything else.**

---

## 1. THE CANONICAL PATTERN

```
{organ_server}_{verb_class}_{domain}_{specific_action}
```

### 1.1 Registered Prefixes (binding)

| Organ | Server | Verb Prefix | Canonical Example | Count |
|-------|--------|-------------|-------------------|-------|
| **arifOS** | `arifos` | `arif_` | `arifos_arif_init` | 8 |
| **A-FORGE** | `aforge` | `forge_` | `aforge_forge_shell` | 110+ |
| **GEOX** | `geox` | `geox_` | `geox_geox_basin` | 32 |
| **WEALTH** | `wealth` | `capital_` | `wealth_capital_primitive` | 8 |
| **WEALTH (ext)** | `wealth` | `wealth_` | `wealth_wealth_institutional_stress_index` | 6 |
| **WELL** | `well` | `well_` | `well_well_validate_vitality` | 10 |
| **Hermes** | `hermes` | `hermes_` | `hermes_hermes_fact_check` | 7 |
| **arifFlow** | `arifflow` | `flow_` | `arifflow_flow_health` | 2 |
| **AAA** | `aaa` | `aaa_` | `aaa_aaa_measure` | 1 |

### 1.2 Pattern Rules

1. **Server name ≠ verb prefix** (preferred, not always achieved — see §2).
   - ✅ `aforge_forge_*` — server "aforge", verb "forge" (different)
   - ✅ `arifos_arif_*` — server "arifos", verb "arif" (different)
   - ⚠️ `geox_geox_*` — server "geox", verb "geox" (same — double-prefix, see §2.2)

2. **Subdomain grouping** (domain-level prefix):
   - `geox_seismic_compute`, `geox_seismic_ingest`, `geox_seismic_interpret`
   - `geox_well_desk`, `geox_well_ingest`, `geox_well_qc`, `geox_well_view`
   - `geox_map_layers_list`, `geox_map_render_preview`, `geox_map_scene_plan`
   - `forge_browser_navigate`, `forge_browser_click`, `forge_browser_screenshot`
   - `forge_vps_ports`, `forge_vps_services`, `forge_vps_cron`

3. **Verb-first for action tools:**
   - WELL: `well_assess_*`, `well_validate_*`, `well_guard_*`, `well_classify_*`, `well_trace_*`, `well_check_*`
   - arifOS: `arif_init`, `arif_observe`, `arif_think`, `arif_route`, `arif_memory`, `arif_judge`, `arif_forge`, `arif_seal`

4. **Mode over tool proliferation.** Where a tool has related variants, use `mode` parameter
   rather than separate tools:
   - `arif_think(mode="reason|reflect|verify|plan|simulate|atlas")` — 12 modes, 1 tool
   - `forge_git(mode="status|diff|log|commit")` — 4 modes, 1 tool
   - `forge_docker(mode="ps|logs|exec|images")` — 4 modes, 1 tool

5. **No aliases within the same organ.** If two tools do the same thing, pick one and
   deprecate the other with a tombstone. Duplicate names in different organs are
   acceptable (e.g., `arif_seal` ≠ `forge_seal` — different authority domains).

### 1.3 What a Good Name Communicates

A well-formed name should answer four questions at a glance:
- **Which organ?** → prefix
- **What domain?** → subdomain group
- **What action?** → verb
- **What class?** → implied by organ (governance / compute / reflect / execute)

Example: `geox_seismic_interpret`
→ GEOX organ → seismic domain → interpret action → Earth evidence (compute-only)

---

## 2. KNOWN DRIFT (existing — do not rename)

These are **forged into the record.** Renaming would break all references.
They are tagged here for agent awareness — new tools MUST NOT replicate these patterns.

### 2.1 CRITICAL: WEALTH Prefix Split

WEALTH has two competing prefixes on the same organ:

| Family | Prefix | Count | Examples |
|--------|--------|-------|----------|
| Domain computation | `capital_*` | 8 | `capital_primitive`, `capital_market`, `capital_wisdom` |
| Institutional analysis | `wealth_*` | 6 | `wealth_institutional_stress_index`, `wealth_cascade_model` |

**Impact:** An agent scanning for `capital_*` misses 6 tools. An agent scanning for `wealth_*` misses 8 tools.
**Resolution:** Forward-only — all new WEALTH tools MUST use `capital_*` prefix.
Existing `wealth_*` tools tagged with `alias: capital_*` in metadata.
When the `wealth_*` tools are next refactored, rename them to `capital_*`.

### 2.2 MODERATE: Double-Prefix Pattern

When server name = verb prefix, the MCP namespace produces `organ_organ_action`:

| Server | Tool Prefix | Client Sees | Redundancy |
|--------|-------------|-------------|------------|
| `geox` | `geox_` | `geox_geox_basin` | "geox" ×2 |
| `well` | `well_` | `well_well_validate_vitality` | "well" ×2 |
| `hermes` | `hermes_` | `hermes_hermes_fact_check` | "hermes" ×2 |

**Why it happened:** These organs were built when the convention was "prefix = organ name."
arifOS and A-FORGE later adopted "prefix ≠ server name" (arif_ within arifos, forge_ within aforge).
GEOX, WELL, and Hermes predate that refinement.

**Resolution:** Forward-only. New tools on these organs may use differentiated prefixes:
- GEOX: new tools MAY use `geo_` prefix → `geox_geo_new_tool`
- WELL: new tools MAY use `human_` prefix → `well_human_new_tool`
- Hermes: new tools MAY use `steward_` prefix → `hermes_steward_new_tool`

Existing double-prefix tools KEEP their names. This is a forward-looking standard only.

### 2.3 COSMETIC: A-FORGE Granularity Inconsistency

| Pattern | Example | Note |
|---------|---------|------|
| Atomic tool | `forge_filesystem` (single tool, modes) | ✅ Good |
| Split tools | `forge_github`, `forge_github_create_issue`, `forge_github_get_file` | ⚠️ Some ops are separate tools, others are modes |
| Dry-run as separate tool | `forge_shell_dryrun` vs `forge_shell` | ⚠️ Dry-run should be `forge_shell(mode="dryrun")` |

**Resolution:** Forward-only. New tools prefer mode parameter over tool proliferation.
Existing split tools preserved.

---

## 3. NAMING LINT — Enforcement

### 3.1 Registration Gate

Every new tool proposed via `forge_evaluate` or `forge_register` MUST pass these checks:

| Check | Rule | Violation |
|-------|------|-----------|
| **Prefix match** | Tool prefix must match organ's registered prefix | REJECT |
| **No collision** | Tool name must not collide with existing tool in ANY organ | REJECT |
| **No double-prefix** | New tools on geox/well/hermes SHOULD use differentiated prefix | WARN (advisory) |
| **No ambiguous verbs** | Verbs must be distinct within organ (e.g., don't add `geox_compute` when `geox_seismic_compute` exists) | WARN |
| **WEALTH tools** | MUST use `capital_*` prefix (not `wealth_*`) | REJECT |
| **Mode over proliferation** | Prefer mode parameter over separate tool when variants share domain | WARN |

### 3.2 Automated Check

```bash
# Verify all tools on an organ follow naming convention
# (to be integrated into forge_evaluate gate)
python3 -c "
import json, sys, urllib.request

# Fetch tools/list from organ
url = 'http://localhost:$PORT/mcp'
body = json.dumps({'jsonrpc':'2.0','id':1,'method':'tools/list'}).encode()
req = urllib.request.Request(url, body, {'Content-Type':'application/json'})
tools = json.loads(urllib.request.urlopen(req).read())['result']['tools']

prefix = '$EXPECTED_PREFIX'
violations = [t['name'] for t in tools if not t['name'].startswith(prefix)]
if violations:
    print(f'NAMING VIOLATION: {violations}')
    sys.exit(1)
print(f'OK: {len(tools)} tools, all prefixed with {prefix}')
"
```

---

## 4. THE NAMING CONTRACT

### 4.1 For Tool Authors

1. **Choose the organ first.** The organ determines the prefix.
2. **Prefix is non-negotiable.** Every tool on WEALTH starts with `capital_`. Period.
3. **Prefer mode over proliferation.** Before creating `forge_github_new_action`,
   ask: can this be `forge_github(mode="new_action")`?
4. **Name for the LLM, not for humans.** The model scans names. Make them scannable.
5. **Never rename after publish.** The name is the permanent coordinate.

### 4.2 For Agents

1. **Discover by prefix scan.** To find all WEALTH tools: filter for `capital_*`.
   Then also check for `wealth_*` (legacy) — until aliased.
2. **Route by prefix.** `arif_*` = governance. `geox_*` = Earth. `capital_*` = money.
3. **Never assume name = capability.** Probe `tools/list` — the name is a contract, not a guarantee.

### 4.3 Floor Alignment

| Floor | Naming Obligation |
|-------|-------------------|
| **F2 TRUTH** | Name must truthfully describe capability. Vague names = silent misfire. |
| **F4 CLARITY** | Pattern must be consistent. Every organ, one prefix. |
| **F10 ONTOLOGY** | Prefix defines category. Cross-prefix naming = category error. |
| **F11 AUDIT** | Every tool name registered and fingerprint-hashed. Renames are traceable. |
| **F13 SOVEREIGN** | New prefix registration requires F13 approval. |

---

## 5. PREFIX REGISTRY (canonical — append-only)

| Date | Organ | Prefix | Registered By | Note |
|------|-------|--------|---------------|------|
| 2025-06 | arifOS | `arif_` | F13 | Original kernel |
| 2025-06 | A-FORGE | `forge_` | F13 | Original execution |
| 2025-08 | GEOX | `geox_` | F13 | Earth intelligence |
| 2025-09 | WEALTH | `capital_` | F13 | Capital intelligence (primary) |
| 2025-11 | WEALTH | `wealth_` | F13 | Institutional analysis (secondary — tagged for consolidation to `capital_*`) |
| 2025-10 | WELL | `well_` | F13 | Human readiness |
| 2026-01 | Hermes | `hermes_` | F13 | Memory/metabolism steward |
| 2026-07 | arifFlow | `flow_` | F13 | Metabolic pulse |
| 2026-07 | AAA | `aaa_` | F13 | Control plane |

---

## 6. VERIFICATION

```bash
# Federation-wide naming audit (live probe)
for organ in arifos:8088:arif_ aforge:7071:forge_ geox:8081:geox_ wealth:18082:capital_ well:18083:well_ hermes:18001:hermes_; do
  IFS=: read name port prefix <<< "$organ"
  health=$(curl -sf --max-time 2 "http://localhost:$port/health" 2>/dev/null)
  if [ $? -eq 0 ]; then
    echo "✅ $name :$port ($prefix*)"
  else
    echo "❌ $name :$port DOWN"
  fi
done
```

---

*DITEMPA BUKAN DIBERI — Forged by 333-AGI under F13 directive, 2026-07-31.*
*Names are the first forge. What is named exists. What exists can be governed.*
