# ONE GEOX MANIFEST — Canonical Surface Schema Design

**Lane:** 333 (ARCHITECTURE) · FI-002 · claude-code/FI-002
**Date:** 2026-10-01
**Status:** DESIGN PROPOSAL — not ratified, not implemented
**Authority:** Read-only. No source mutated. See §12 Confirmation.
**Companion:** Lane 555 live probe (this doc is the architectural counterpart)

---

## 0. Epistemic labeling convention (F2 TRUTH)

| Tag | Meaning |
|---|---|
| **OBS** | Directly observed this session (file read or live probe). Path/line cited. |
| **DER** | Derived by computation from OBS facts. Reproducible. |
| **INT** | Interpretation — my reading of why, not directly observed. |
| **SPEC** | Specification — proposed here, does not yet exist. |

Confidence cap: **0.90** (F7 HUMILITY). Ω₀ = 0.04.

---

## 0.1 Premise correction — required before anything else (F2)

The tasking states the RT1 guard "suggested `geox_surface_status` as recovery — but that tool is **unreachable** from the connector descriptor visible to the caller."

**This is partially wrong, and the correction changes the design.** **OBS:**

| Surface | `geox_surface_status` reachable? | Evidence |
|---|---|---|
| `tools/list` (live, legacy era) | **YES** | live probe → 26 tools, `has geox_surface_status: True` |
| `server/discover` `_meta.io.geox/surface` | count only (26), no names | live probe |
| `.well-known/mcp/server.json` card | **YES** | category `meta.discovery: ["geox_surface_status"]` |
| `capability_packs` ∪ all packs | **NO** | **OBS** it is in **no** pack |
| discovery profile `research`/`full` | **NO** | `tools_for_profile('research') → 20` of 26 |

So `geox_surface_status` **is** on the canonical 26 and **is** served by `tools/list` today. The real defect is narrower and more precise:

> **DER:** 6 of 26 public tools belong to **no capability pack**. Any consumer that resolves the surface through the pack/profile layer — not through `tools/list` — sees only **20** tools, and the recovery tool `geox_surface_status` is among the 6 that vanish.

**DER — the 6 unreachable-under-profile tools:**
```
geox_calibration_register_witness
geox_extract_display_proxy
geox_extract_native_trace
geox_list_registered_sources
geox_register_native_source
geox_surface_status          ← the recovery tool itself
```
[receipt: `/root/GEOX/src/geox_mcp/registry.py:tools_for_profile` + `/root/GEOX/src/geox_mcp/tools_manifest.yaml:capability_packs` — verified by direct import, output `research -> 20`, `UNREACHABLE under research profile: [...6 names...]`]

**INT:** The recovery tool being invisible to the very layer that needs recovery is not an accident of omission — it is what happens when a *second* surface-computation path exists alongside `tools/list`. Two paths computing "the surface" will disagree; the disagreement lands hardest on the meta-tools nobody packs.

This is the design's central target: **not** "make the connector list more tools" but **make it structurally impossible for two paths to compute the surface differently.**

---

## 0.2 Measured baseline — the four sets today

All **OBS**, live probe 2026-10-01 against `127.0.0.1:8081` + source read:

| Set | Count | Source |
|---|---|---|
| `S_declared` (manifest public) | **26** | `tools_manifest.yaml` `visibility: public` |
| `S_exported` (RT1 `_EXECUTABLE_SURFACE`) | **28** | 26 + 2 compat (`geox_well_desk`, `geox_well_view`) — **DER** |
| `S_callable` (live `tools/list`) | **26** | live JSON-RPC probe |
| `S_observed` (profile `full`) | **20** | `tools_for_profile('full')` |
| manifest total entries | **87** | 26 public + 61 internal |
| `GHOST_TOOLS` | **22** | `registry.py` (import-verified) |
| live prompts | **16** | `prompts/list` |
| live resources | **53**, templates **0** | `resources/list` |

**S_declared(26) ≠ S_exported(28) ≠ S_callable(26) ≠ S_observed(20).** The violation in the tasking is confirmed, with corrected numbers.

### Additional defects found while measuring (all OBS)

These were not in the tasking but are load-bearing for the design:

**D1 — `surface_attestation()` is permanently failing.**
```
public_count=26  public_count_target=31  ok=False  err=SURFACE_COUNT_DRIFT
```
The manifest hardcodes a target of 31 that the manifest itself does not satisfy. Any consumer trusting `ok` gets a standing false alarm. [receipt: `/root/GEOX/src/geox_mcp/tools_manifest.yaml:public_count_target`]

**D2 — `deployment_drift` is tautological.** `build_info_handler` returns
```python
"source_commit":   _GIT_VERSION,
"deployed_commit": _GIT_VERSION,
"build_commit":    _GIT_VERSION,
"physics_manifest_hash": _GIT_VERSION,
```
All four are the *same variable*. `/health` therefore reports `"drift": false, "status": "aligned"` unconditionally — it cannot fail. This is exactly the **Oracle Independence Law** violation already sealed in memory (`eureka-oracle-independence-law-2026-09-27`) and the same class as the two refuted physics verdicts of 2026-09-27. [receipt: `/root/GEOX/src/geox_mcp/server.py:build_info_handler`]

**D3 — `contract_epoch` is itself drifted.** Two different values live in one repo:
```
server.py:71                    "2026-07-09-GEOX-73TOOLS-PHASE31-RSI-PIPELINE"
geox_core/enums/statuses.py:28  "2026-07-06-GEOX-PHASE31-RSI-PIPELINE"
```
The epoch that §8 caches on is not single-valued today. [receipt: grep `GEOX_CONTRACT_EPOCH =`]

**D4 — `protocolVersion` is triple-declared.**
```
.well-known/mcp/server.json  →  "2025-06-18"
initialize negotiation       →  "2025-11-25"   (live probe)
server/discover advertise    →  "2026-07-28"   (live probe)
```

**D5 — The recovery string is a hardcoded literal, not a derivation.** RT1 emits:
```python
f"Use geox_surface_status(mode='registry') to enumerate available tools."
```
A literal in an f-string. It is **never checked** against the callable set — so it can silently recommend an unreachable tool, which is precisely the reported failure. The tasking's invariant `recommended_next ⊆ callable_surface` is currently *unenforceable by construction*. [receipt: `/root/GEOX/src/geox_mcp/geox_middleware.py:729`]

**D6 — A generator exists but is not CI-wired.** `scripts/generate_all_surfaces.py` (531 lines) already declares *"registry.py is the ONLY truth. Every surface is GENERATED from it."* It regenerates 6 surfaces. It is referenced by **zero** workflows in `.github/`. Run today in `--dry-run`:
```
CHANGED:   tools_sot.yaml, CANONICAL_PUBLIC_SURFACE.json, tools.json, contracts/tools.yaml
UNCHANGED: llms.txt, README.md
```
**DER:** 4 of 6 generated surfaces are drifted *right now*, because nothing forces regeneration. **INT:** The federation does not lack a one-manifest design. It lacks a **hash-sealed CI gate** on the design it already has. This doc therefore specifies *hardening and extension* of the existing manifest, not a greenfield replacement — which is the reversible path per the attention membrane.

**D7 — The tasking's own example tool is a ghost.** `geox_subsurface_generate_candidates` (used as the schema exemplar in §1 of the brief) is registered in `servers/witness.py:60` but is **ABSENT FROM MANIFEST ENTIRELY**. Same for `geox_system_registry_status`, `geox_resource_registry_status`, `geox_health_check`. **DER:** These are not "tools the client was wrongly told about" — they are real, imported, registered callables that no manifest declares. The manifest is *incomplete*, not merely *out of sync*. This is the strongest argument for one manifest: today a tool can exist in the runtime and in no declared surface at all.

**D8 — `CANONICAL_RUNTIME_TOOLS` counts ghosts.** `runtime_tool_names()` returns all 87 manifest entries; `GHOST_TOOLS` (22) are subtracted for `SURFACE_TOOLS` and `INTERNAL_TOOLS` but **not** for runtime. Card says `totalRegistered: 65`; 26+39 = 65 ✓ but runtime list = 87. Two "total" numbers coexist.

---

## 1. Canonical tool manifest schema

### 1.1 Design decision: extend `tools_manifest.yaml`, do not replace it

**DER:** `tools_manifest.yaml` (59 KB, 87 entries) is already the single loader input (`surface_manifest.py::load_surface_manifest`, `lru_cache`d, with duplicate-name validation). `registry.py` already derives public/internal/runtime from it. `generate_all_surfaces.py` already fans out to 6 artifacts.

**SPEC:** Adopt the schema below as **`geox.manifest.v3`** — a superset of the current entry shape. Every existing field is preserved; new fields are added. Migration is additive, therefore reversible (F1 AMANAH): deleting the new keys restores v2 behaviour exactly.

### 1.2 File layout

```
src/geox_mcp/
  manifest.yaml                    ← THE manifest (single file, v3)
  manifest.lock.json               ← generated: hashes of every derived surface
  schemas/
    inputs/<tool>.json             ← referenced by inputs_schema_ref
    outputs/<tool>.json            ← referenced by outputs_schema_ref
    common/evidence_contract.json  ← shared §6 definition
  generated/
    CANONICAL_PUBLIC_SURFACE.json  ← G5 output (exists today)
    rt1_allowlist.json             ← G2 output (NEW)
    connector_descriptor.json      ← G3 output (NEW)
    compat_registry.json           ← G4 output (NEW)
    recovery_catalog.json          ← G10 output (NEW, §4)
```

`manifest.yaml` is **hand-edited and reviewed**. Everything under `generated/` is **written only by the generator** and carries a `// generated-from` header + hash. CI fails if a generated file's hash ≠ recomputed hash.

### 1.3 Top-level manifest envelope

```yaml
schema: geox.manifest.v3
manifest_version: "2026.10.01"
organ: GEOX
contract_epoch: "GEOX-CONTRACT-2026.10.01-MANIFEST-V3"   # ← SINGLE definition, fixes D3
ontology:
  canon9_version: "CANON-9/1.x"
  physics9_version: "Physics9/x.y"
  units_registry_hash: "sha256:..."
transport:
  eras: ["2026-07-28", "2025-11-25"]
  primary_era: "2026-07-28"
  endpoint: /mcp/
resources:                     # §5 — resources are declared, not discovered
  - uri_template: "geox://wells/{well_id}"
    name: well
    mime_type: application/json
    read_scope: geox:read
tools: [ ... ]                 # §1.4
prompts: [ ... ]               # §5.3
tasks: [ ... ]                 # §5.4
capability_packs: { ... }      # §1.6 — PACK COMPLETENESS IS ENFORCED
```

**SPEC (fixes D1):** there is **no `public_count_target`**. The count is an *output* of the manifest, never an input asserted against it. Any "expected count" lives in `manifest.lock.json` as a hash, not a magic integer. A count target that the manifest itself violates is a standing false alarm; a hash cannot be stale in that way — it is either equal or different.

### 1.4 Tool entry — required fields

```yaml
- name: geox_petrophysics                      # REQUIRED, unique, ^geox_[a-z0-9_]+$
  description: |                               # REQUIRED, non-empty, ≥40 chars
    Unified petrophysics: Vsh, porosity, Sw, permeability, net pay,
    LEM inference, QC. Physics9-bounded, CANON-9 ontology.
  visibility: public                           # REQUIRED enum: public | internal
  domain: earth.petrophysics                   # REQUIRED, must resolve in ontology
  axis: reason                                 # REQUIRED enum: observe|compute|reason
  lane: reasoning                              # REQUIRED enum: evidence|compute|reasoning|governance
  family: interpret                            # REQUIRED enum (closed set)
  tier: A                                      # REQUIRED enum: A|B|C|Z

  # ── behaviour primitives (NEW — the §1 truth atoms) ──
  mutation: false                              # REQUIRED bool
  external_side_effect: false                  # REQUIRED bool
  irreversible: false                          # REQUIRED bool
  deterministic: true                          # REQUIRED bool
  network_access: false                        # REQUIRED bool
  long_running: false                          # REQUIRED bool

  # ── authority (NEW — replaces governance.action_class, §7) ──
  action_class: OBSERVE                        # REQUIRED enum: OBSERVE|MUTATE|EXECUTE
  roles_required: [geox:read]                  # REQUIRED, ≥1
  min_authority: OBSERVE_ONLY                  # DERIVED — see validation rule V7
  arg_conditional_authority:                   # OPTIONAL — replaces _MUTATING_ARG_OVERRIDES
    - when: {arg: mode, equals: seal}
      then: {min_authority: LIMITED_MUTATE, irreversible: true, requires_ack: true}
    - when: {arg: overwrite, truthy: true}
      then: {min_authority: LIMITED_MUTATE}

  # ── schemas (NEW — fixes D-outputSchema gap) ──
  inputs_schema_ref:  geox://schemas/inputs/petrophysics.json    # REQUIRED
  outputs_schema_ref: geox://schemas/outputs/petrophysics.json   # REQUIRED for public
  output_envelope: scientific_v1               # REQUIRED enum for scientific tools (§6)

  # ── evidence contract (§6) ──
  evidence_contract:
    artifact_ref: required
    claim_state: required
    evidence_refs: required
    units_required: [depth_basis, porosity, density]
    uncertainty_required: [method, lower, upper]
    provenance_required: [tool, tool_version, source_hashes]

  # ── surface placement ──
  packs: [earth_core]                          # REQUIRED, ≥1 if visibility=public  ← fixes §0.1
  prompts: [prospect_screen, well_correlation] # OPTIONAL
  resource_refs: ["geox://wells/{well_id}"]    # OPTIONAL — must resolve (§3 test 2)

  # ── affordance (§7 layer 2) ──
  affordance:
    can_read_seismic: true
    can_read_well: true
    can_mutate_prospect: false
    can_seal: false                            # GEOX NEVER seals — arifOS only

  # ── versioning ──
  since_version: "2026.07.24"                  # REQUIRED
  deprecated_since: null                       # REQUIRED (null = live)
  removal_target: null                         # REQUIRED if deprecated_since set
  compat_aliases: []                           # OPTIONAL, each maps alias→this name

  # ── DERIVED, never hand-written ──
  annotations_derived: true                    # REQUIRED literal `true`
```

### 1.5 Optional fields

```yaml
  ui:                                          # MCP Apps panel
    resource_uri: "ui://geox/geoprobe"
    render_mode: panel
    mime_type: "text/html;profile=mcp-app"
  execution:
    task_support: optional|required|forbidden  # §5.4 — long_running must agree
  subfamily: ""
  rate_limit_rpm: 10.0
  keywords: [porosity, vsh, sw]                # discovery/intent routing for §8
  implementation:                              # NEW — closes the D7 ghost class
    module: geox_mcp.tools.petrophysics
    symbol: geox_petrophysics
    registered_on: [main]                      # which FastMCP sub-server(s)
  witness_server_alias: null                   # if also mounted on servers/witness.py
```

**SPEC — `implementation` is REQUIRED for every entry, and validated (§1.7 V10).** This is the field that makes D7 impossible: a manifest entry that cannot be imported fails CI, and a registered callable with no manifest entry fails CI. The ghost class is closed from both directions.

### 1.6 Pack completeness (fixes the actual §0.1 bug)

**SPEC — validation rule V5:**
```
∀ tool t : t.visibility == "public"  ⇒  t.packs ≠ ∅
⋃ {packs of all public tools} ⊇ S_public
∴ tools_for_profile("full") == S_public      (exactly, not ⊆)
```
Today `full → 20` while `S_public → 26`. Under v3 this is a **hard CI failure**, not a silent 6-tool hole. The profile layer stops being a second source of truth: it becomes a *partition* of the one truth, and partitions must cover.

### 1.7 Validation rules

| # | Rule | Failure mode it closes |
|---|---|---|
| V1 | `name` unique across all 87+ entries | duplicate manifest tools (already enforced) |
| V2 | `name` matches `^geox_[a-z0-9_]+$` | naming drift |
| V3 | `visibility=internal` ⇒ `plugin.exposed ≠ true` | already enforced, keep |
| V4 | `deprecated_since ≠ null` ⇒ `removal_target ≠ null` | zombie deprecations |
| **V5** | `visibility=public` ⇒ `packs ≠ ∅`; profile `full` == `S_public` | **§0.1 root cause** |
| V6 | `annotations_derived` must be literal `true`; hand-set `annotations:` block is a **hard error** | annotation drift (§2 G8) |
| **V7** | `min_authority` is computed, never declared. Assert `declared == computed` | authority drift |
| V8 | `irreversible=true` ⇒ `arg_conditional_authority` contains a `requires_ack` path, OR tool-level `requires_ack: true` | RT3 gap |
| V9 | `long_running=true` ⇔ `execution.task_support ∈ {required, optional}` | task/tool split (§5.4) |
| **V10** | `implementation.module:symbol` imports and is callable | **D7 ghost class** |
| V11 | every registered FastMCP tool ∈ manifest names | **D7, other direction** |
| V12 | `inputs_schema_ref` / `outputs_schema_ref` resolve to an existing file, and the file is valid JSON Schema 2020-12 | phantom refs |
| V13 | `resource_refs` templates ∈ declared `resources[].uri_template` | §3 test 2 |
| V14 | `output_envelope: scientific_v1` ⇒ schema contains all §6 required fields | scientific contract gap |
| V15 | `affordance.can_seal == false` for **every** GEOX tool | Organ Domain Boundary Law — arifOS alone emits SEAL |
| V16 | `compat_aliases` targets exist and are themselves non-deprecated | dangling alias |
| V17 | `roles_required ⊆ {geox:read, geox:write, geox:admin}` | OAuth scope drift |
| V18 | `contract_epoch` appears **exactly once** in the whole repo | **D3** |
| V19 | `since_version` ≤ current `manifest_version` (date-orderable) | version nonsense |
| V20 | no tool declares `deprecated_since` in the future | clock drift |

**DER — V7 computation** (replaces the hardcoded `_ACTION_CLASS_AUTH` dict):
```python
def compute_min_authority(tool) -> str:
    if tool.irreversible:                return "SOVEREIGN"      # F13 territory
    if tool.mutation or tool.action_class in ("MUTATE","EXECUTE"):
                                         return "LIMITED_MUTATE"
    if tool.external_side_effect:        return "OPERATOR"
    return "OBSERVE_ONLY"                                        # safe-fail default
```
This preserves the existing safe-fail-by-absence property (registry.py comment: *"never grant MUTATE by absence of declaration"*) while making the mapping a pure function of declared primitives.

### 1.8 Versioning semantics

```
since_version       — manifest_version in which the tool first appeared
deprecated_since    — manifest_version from which it emits a deprecation warning
                      (tool REMAINS callable + listed until removal_target)
removal_target      — manifest_version at which it leaves S_public
compat_aliases      — names accepted by RT1 but NOT advertised (see §2 G3 note)
contract_epoch      — bumped on ANY breaking surface change; the cache key for §8
```

**Lifecycle:** `live → deprecated (listed + callable + warns) → removed (unlisted, alias-resolved) → gone (RT1 rejects)`.
A removed tool's name moves into the target's `compat_aliases`, so the alias registry (§2 G4) can answer `alias → canonical_name` — which today it cannot, because `compat_tools` is a flat top-level list with no target mapping.

---

## 2. Generators table

### 2.1 The core invariant

**SPEC:**
```
∀ generator Gᵢ : Surfaceᵢ = Gᵢ(M)          — M is the manifest, the ONLY input
hᵢ = sha256( "GEOX-SURFACE-V3:" || i || ":" || canon_json(Gᵢ(M)) )
```
`canon_json` = `json.dumps(obj, sort_keys=True, separators=(",",":"))` — already the convention in `surface_attestation()`. The **domain-separation tag** (`i`) prevents cross-generator hash collisions when two surfaces happen to be identical.

**The rule that kills the drift class:** *no generator may read anything but `M`.* No environment variables, no git state, no live-server introspection, no `if port == 8081`. A generator that consults runtime state is an oracle that can disagree with itself — the D2 tautology generalised. **Corollary:** `deployed_commit` must come from the deploy step writing a file, never from the same variable as `source_commit` (fixes D2, honours Oracle Independence Law).

### 2.2 Generator table

| # | Surface | Generator rule | Deterministic function | CI check |
|---|---|---|---|---|
| **G1** | `tools/list` (both eras) | `M.tools` where `visibility=public ∧ deprecated_since IS NULL` | `gen_tools_list(M)` | `h1` == lock; live `tools/list` == `h1` payload |
| **G2** | RT1 allowlist | **exactly** `names(G1)` ∪ `alias_targets(M)` | `gen_rt1_allowlist(M)` | `h2`; **RT1 imports the generated file** — no recomputation |
| **G3** | Connector descriptor | `G1` (+ aliases: **see note**) | `gen_connector_descriptor(M)` | `h3`; card `publicCount == len(G1)` |
| **G4** | Compat alias registry | `{alias → canonical}` from all `compat_aliases` | `gen_compat_registry(M)` | `h4`; every alias target ∈ `G1` |
| **G5** | Registry/status output | full `M` snapshot + all `hᵢ` | `gen_registry_snapshot(M)` | `h5`; `geox_surface_status` serves **this file** |
| **G6** | Docs (`llms.txt`, README, `tools_sot.yaml`, `contracts/tools.yaml`) | manifest → markdown/YAML | `gen_docs(M)` | `h6`; **no numeric literal in any doc** |
| **G7** | Tests | one safe `schema_discovery` case per tool | `gen_discovery_tests(M)` | `h7`; test count == `len(G1)` |
| **G8** | MCP annotations | derived (§2.3) | `gen_annotations(M)` | `h8`; V6 forbids hand-set |
| **G9** | `inputSchema`/`outputSchema` refs | from `*_schema_ref`, inlined | `gen_schemas(M)` | `h9`; V12 resolution |
| **G10** | Recovery catalog (§4) | callable subset of `M`, ranked | `gen_recovery_catalog(M)` | `h10`; **invariant `recommended_next ⊆ G2`** |
| **G11** | `server/discover` payload (§10) | epoch + counts + `h1` | `gen_discover_payload(M)` | `h11` |
| **G12** | Resource templates (§5) | `M.resources` | `gen_resource_templates(M)` | `h12`; V13 |
| **G13** | Prompt list (§5.3) | `M.prompts` | `gen_prompts(M)` | `h13` |
| **G14** | Task definitions (§5.4) | `M.tasks` | `gen_tasks(M)` | `h14` |

**`manifest.lock.json`:**
```json
{ "schema":"geox.manifest.lock.v1", "manifest_hash":"sha256:…",
  "contract_epoch":"GEOX-CONTRACT-…",
  "surfaces": { "G1":"sha256:…", "G2":"sha256:…", … "G14":"sha256:…" },
  "surface_hash":"sha256:…(Merkle root of G1..G14)" }
```
**`surface_hash` = Merkle root**, so *any* single-surface drift changes the one value arifOS caches on (§8). This is the generalisation of the existing `surface_attestation()` hash from 1 surface to 14.

### 2.3 G8 — annotation derivation (replaces hand-set `annotations:`)

```python
def derive_annotations(t) -> dict:
    return {
      "readOnlyHint":   not t.mutation and not t.external_side_effect,
      "destructiveHint": t.irreversible,
      "idempotentHint":  t.deterministic and not t.irreversible,
      "openWorldHint":   t.network_access or not t.deterministic,
    }
```
**DER — cross-check against live:** today all 26 tools serve `{readOnly:true, destructive:false, idempotent:true, openWorld:false}` — uniform. **INT:** Uniform annotations across 26 tools that include `geox_well_ingest` (writes files, has an `overwrite` arg that flips it to MUTATE per `_MUTATING_ARG_OVERRIDES`) are **not a measurement, they are a default**. Under G8, `geox_well_ingest` derives `idempotentHint: false` (because `overwrite` makes it non-idempotent) — the first time annotations would carry information.

**SPEC:** `generate_all_surfaces.py` currently hardcodes `{"read_only": True, "destructive": False, "idempotent": True}` for **every** tool when writing `tools_sot.yaml`. That is a generator *inventing* data rather than deriving it — it must be replaced by G8.

### 2.4 G3 note — an open decision (F7: declaring the unknown)

The tasking specifies `connector descriptor = tools/list ∪ compat_aliases`. The current design comment says compat tools are *"never exposed publicly"* — deliberately, to drive deprecation.

These conflict. Advertising aliases makes deprecated names discoverable, which slows the migration the alias exists to complete.

**Recommendation (INT, confidence 0.75):** `G3 = G1` exactly — **do not advertise aliases**. Keep them *resolvable* (RT1 accepts + warns + returns `canonical_name` in the response envelope), but invisible. A caller who guesses a legacy name gets a working answer plus a migration hint; a caller reading the descriptor never learns the dead name.

**This is an F13-class binary for Arif, not a menu:** *advertise aliases in the connector descriptor — YES / NO.* Default if unanswered: **NO** (matches existing intent, reversible).

### 2.5 CI gate (the missing piece, D6)

```yaml
# .github/workflows/surface-parity.yml
- run: python scripts/generate_all_surfaces.py --check     # writes nothing
  # exits non-zero if any regenerated byte differs from committed byte
- run: python scripts/verify_surface_lock.py               # recomputes h1..h14
  # fails on: lock mismatch, V1..V20 violation, live tools/list != G1
```
`--check` mode is the whole fix for D6: the generator already exists and is already deterministic — it is simply never run under enforcement. **DER:** wiring these two lines makes 4 currently-drifted files fail the build until regenerated.

**Deploy-time gate:** the deployed container recomputes `h1` from its own bundled manifest and compares to `manifest.lock.json`. Mismatch ⇒ refuse to serve `tools/list`, serve only `geox_surface_status` in `degraded` mode. This is what turns "source patched, deployed venv still old" (the `DEPLOYMENT_DRIFT` scar of 2026-09-30) from a post-hoc observation into a startup refusal.

---

## 3. G0 conformance test

**SPEC** — pytest stub. Four independent oracles; the point is that **no two share a code path**.

```python
"""G0 SURFACE PARITY — the four sets must be one set.

Oracle independence (Oracle Independence Law 2026-09-27):
  S_declared : read from the CONNECTOR over the wire (external view)
  S_exported : read from RT1's generated allowlist FILE (gate view)
  S_callable : read by ACTUALLY CALLING each tool (runtime view)
  S_observed : read from the AUDIT LOG of this session (witness view)
None of these may be computed from the manifest in-process, or the test
measures its own construction — the exact failure of the two refuted
physics verdicts (2026-09-27) and the audit scripts of 2026-09-28.
"""
import json, pytest
from pathlib import Path

LOCK = json.loads(Path("src/geox_mcp/manifest.lock.json").read_text())


def test_g0_surface_parity(connector, rt1, audit_log):
    S_declared = {t["name"] for t in connector.list_tools()}      # over the wire
    S_exported = set(rt1.allowlist_from_generated_file())         # G2 artifact
    S_callable = {t for t in S_declared
                    if probe_safe_schema_discovery(t, SAFE_INPUT[t]).ok}
    S_observed = set(audit_log.tools_seen_in_session())

    assert S_declared == S_exported, (
        f"DECLARED≠EXPORTED declared-only={S_declared-S_exported} "
        f"exported-only={S_exported-S_declared}")
    assert S_declared == S_callable, (
        f"DECLARED≠CALLABLE phantom={S_declared-S_callable}")
    assert S_declared <= S_observed, (
        f"UNOBSERVED (never exercised)={S_declared-S_observed}")

    # ── pack completeness: the §0.1 root cause ────────────────────────
    for profile in ("default", "specialist", "research", "full"):
        S_profile = set(registry.tools_for_profile(profile))
        assert S_profile <= S_declared, f"{profile} advertises ghosts"
    assert set(registry.tools_for_profile("full")) == S_declared, \
        "profile 'full' must COVER the public surface (V5) — 6 tools in no pack"

    # ── resource-ref satisfiability ───────────────────────────────────
    resources_index = {r["uri"] for r in connector.list_resources()}
    templates       = {t["uriTemplate"] for t in connector.list_resource_templates()}
    for tool in S_declared:
        entry = manifest.tool_map[tool]
        for ref in entry.resource_refs:
            base = uri_template_of(ref)
            assert base in templates or ref in resources_index, (
                f"{tool} requires unresolvable resource {ref}")

    # ── the recovery invariant (§4) ───────────────────────────────────
    rec = json.loads(Path("src/geox_mcp/generated/recovery_catalog.json").read_text())
    for payload in rec.values():
        assert payload["registry_tool"] in S_callable, (
            f"recovery recommends UNREACHABLE tool {payload['registry_tool']} "
            f"— the exact reported failure (D5)")
        assert payload["registry_tool_callable"] is True

    # ── hash seal: drift == hash drift ────────────────────────────────
    assert recompute_hash("G1", connector.list_tools_raw()) == LOCK["surfaces"]["G1"]
    assert recompute_merkle_root(LOCK) == LOCK["surface_hash"]


def test_g0_no_oracle_tautology():
    """D2 regression guard: the three commits must be independently sourced."""
    bi = http_get("/api/build-info")
    src = Path("/root/GEOX/.git/HEAD").resolve_sha()        # git, not the app
    dep = Path("/opt/geox/DEPLOYED_COMMIT").read_text()     # written by deploy
    assert bi["source_commit"]   == src
    assert bi["deployed_commit"] == dep
    # If source_commit, build_commit and deployed_commit are the SAME
    # VARIABLE, this test must fail — that is a tautological oracle.
    assert not all_same_variable(bi, ("source_commit","build_commit","deployed_commit"))
```

`SAFE_INPUT[tool]` is a per-tool frozen `{"mode": "schema_discovery"}` fixture — **SPEC:** every GEOX tool must support `mode="schema_discovery"`, returning its input/output schema and evidence contract **with zero side effects**. This is what makes G7 generatable: one safe probe per tool, machine-written, no human-authored fixtures to rot.

**Note on `S_observed`:** uses `<=` not `==`. A session that never calls a tool should not fail parity; but a tool that is *called* and *not declared* must fail. **INT:** `==` would make the test depend on traffic, which is not deterministic — the same category error as measuring a live server inside a CI unit test.

---

## 4. Recovery path schema

**SPEC** — payload returned when RT1 rejects. The critical change: **`next_action` is selected from the generated callable set, never written as a string literal** (fixes D5).

```json
{
  "error": "TOOL_NOT_ON_SURFACE",
  "error_class": "SURFACE_REJECT",
  "requested_tool": "geox_system_registry_status",
  "request_id": "req_01J…",
  "contract_epoch": "GEOX-CONTRACT-2026.10.01-MANIFEST-V3",
  "surface_hash": "sha256:ee2f2de8…",
  "canonical_tool_count": 26,
  "requested_tool_status": "REGISTERED_NOT_DECLARED",
  "resolution": {
    "kind": "alias",
    "canonical_name": "geox_surface_status",
    "confidence": 1.0,
    "reason": "exact compat_alias"
  },
  "registry_tool": "geox_surface_status",
  "registry_tool_callable": true,
  "registry_tool_in_tools_list": true,
  "compatible_aliases": [],
  "nearest_callable": [
    {"name": "geox_surface_status", "similarity": 0.62, "callable": true},
    {"name": "geox_source",         "similarity": 0.41, "callable": true}
  ],
  "next_action": {
    "tool": "geox_surface_status",
    "arguments": {"mode": "registry"},
    "callable_verified_at_generation": true
  },
  "remediation_hint": "Client descriptor is stale. Re-run server/discover and refresh tools/list before retrying.",
  "_meta": {
    "generated_from": "geox_mcp/generated/recovery_catalog.json",
    "generator": "G10",
    "generator_hash": "sha256:…"
  }
}
```

### 4.1 `requested_tool_status` taxonomy

The three rejected names in the incident are **not one failure**. Conflating them produces the wrong remediation. **DER from source:**

| Status | Meaning | Example (OBS) | Correct remediation |
|---|---|---|---|
| `NOT_A_TOOL` | no such symbol anywhere | `mcp_health_check` on main server | client hallucinated — re-discover |
| `LEGACY_ALIAS` | in `compat_aliases` | `geox_well_desk` | use canonical, alias works |
| `REGISTERED_NOT_DECLARED` | real callable, absent from manifest | `geox_system_registry_status` (`tools/registry.py:103`, `servers/witness.py:66`) | **GEOX bug — manifest incomplete (D7)** |
| `INTERNAL_ONLY` | manifest `visibility: internal` | 39 tools | not for external callers, by design |
| `GHOSTED` | in `GHOST_TOOLS` | 22 tools | deregistered; reactivation needs F13 |
| `DEPRECATED` | `deprecated_since` set | — | migrate to canonical |
| `SUBSERVER_ONLY` | mounted on a namespaced sub-server | `servers/witness.py` tools | wrong endpoint |

**INT:** The incident was almost certainly `REGISTERED_NOT_DECLARED`, not client hallucination. `geox_system_registry_status` is a real, imported, registered function. The client was told the truth about the runtime and lied to about the surface. **This reframes the bug: GEOX's manifest under-declares its own runtime.** The tasking frames it as a connector defect; the evidence frames it as a manifest-completeness defect. V10+V11 close it from both sides.

### 4.2 The enforced invariant

```
recommended_next ⊆ callable_surface
```
**SPEC — made structural, not asserted:**
```python
def build_recovery(requested: str, M: Manifest) -> dict:
    callable_set = gen_rt1_allowlist(M)          # ← G2, the SAME function RT1 uses
    reg = select_registry_tool(M, callable_set)  # constrained to callable_set
    assert reg in callable_set                   # build-time, not runtime
    payload = {..., "registry_tool": reg,
               "registry_tool_callable": reg in callable_set}
    # A recommendation is only emitted if it survived the filter.
    # If callable_set ∩ registry_candidates == ∅ → emit NO next_action
    # and escalate, rather than recommend an unreachable tool.
    return payload
```
`select_registry_tool` picks from manifest entries with `family: view ∧ domain: earth.registry ∧ visibility: public` — so if `geox_surface_status` is ever packed out or deprecated, the generator produces `next_action: null` + `escalate: true` instead of a lie. **A recovery path that cannot find a reachable recovery tool must say so.**

**SPEC:** `geox_surface_status` gains a manifest-level pin: `pinned_recovery_tool: true`, and V-rule **V21**: *exactly one public tool carries this pin, and it must be in every pack profile.* That single rule makes the §0.1 failure impossible by construction — the recovery tool can never again be the thing that disappears.

---

## 5. Resource / Prompt / Task split

**OBS baseline:** 53 resources, **0 resource templates**, 16 prompts. The tasking's `geox://wells/{id}` style templates **do not exist yet** — every live resource is a static URI (`geox://layers/index`, `geox://reality/context`, `geox://identity`, `geox://surface/truth`). So this section is genuinely new construction, not refactor.

### 5.1 Resources (nouns) — `geox://` scheme

**SPEC:**
```yaml
resources:
  - uri_template: "geox://wells/{well_id}"          # NEW: templated
    name: well
    description: Well header, curves, deviation, tops
    mime_type: application/json
    read_scope: geox:read
    write_scope: null                               # read-only noun
    id_type: {well_id: string, pattern: "^[A-Z0-9-]+$"}
    evidence_envelope: scientific_v1
  - uri_template: "geox://seismic/{survey_id}"      read_scope: geox:read
  - uri_template: "geox://artifacts/{artifact_id}"  read_scope: geox:read
  - uri_template: "geox://candidates/{candidate_id}"
  - uri_template: "geox://claims/{claim_id}"
  - uri_template: "geox://prospects/{prospect_id}"
  - uri_template: "geox://evidence/{evidence_id}"
  - uri_template: "geox://contradictions/{contradiction_id}"
  - uri_template: "geox://scars/{scar_id}"
  - uri: "geox://server/info"                       # static, §10
    read_scope: null                                # public, pre-auth
```

**Rule (DER):** *Resource ⇔ has identity and can be re-read without recomputation.* `geox://claims/{id}` is a resource; "evaluate this claim" is a tool.

**SPEC — `geox://surface/truth` already exists as a live resource (OBS).** This is significant: it means a **reachable-as-resource** recovery path exists *today*, independent of the tool surface. §4 should therefore list it as a fallback: if `geox_surface_status` (tool) is unreachable, `geox://surface/truth` (resource) is the second recovery door. **INT:** two independent recovery paths across two different MCP primitives is materially more robust than one — a connector that filters tools still lists resources.

### 5.2 Tools (verbs)

`calculate · ingest · qc · model · interpret · compare · judge · register · extract`

**SPEC — rule:** *Tool ⇔ performs computation or state change; result is not addressable by identity until it produces an artifact.* A tool that returns an `artifact_ref` is the bridge: **verb in, noun out.**

**SPEC (Organ Domain Boundary Law, V15):** `judge` in GEOX means *physics-gate and rank hypotheses* — it emits `PASS|WARN|KILL|UNMEASURED` and `preferred_hypothesis: null`. It never emits SEAL/HOLD/VOID. Already true in the live `geox_seismic_interpret` description (**OBS**): *"preferred_hypothesis always null from GEOX. Local max QUALIFIED_CANDIDATE — arifOS seals only."* The manifest makes this a **validated field** rather than prose.

### 5.3 Prompts / Skills (workflows)

```yaml
prompts:
  - name: prospect_screen
    description: Screen a prospect from basin context to ranked candidate
    pack_requirement: [earth_core]
    steps: [{tool: geox_basin}, {tool: geox_prospect}, {tool: geox_claim}]
    emits: ["geox://candidates/{id}"]
  - name: seismic_interpretation      pack_requirement: [earth_core, earth_specialist]
  - name: well_correlation            pack_requirement: [earth_core]
  - name: sequence_stratigraphy
  - name: contradiction_attack
  - name: claim_falsification
  - name: well_tie_review
  - name: uncertainty_review
```
**OBS:** `workflow_packs` already exists in the manifest with `well_to_correlation` fully specified (steps + purposes + `required_packs`). **DER:** 8 requested prompts, 1 exists ⇒ 7 to author. This is the cheapest of the ten deliverables — the schema is already live.

**SPEC — V22:** every `prompts[].steps[].tool` must ∈ `G1`, and every prompt's `pack_requirement` must be satisfied by the packs its steps' tools belong to. This prevents a prompt recommending an unpacked tool — **the §0.1 bug propagating into the prompt layer.**

### 5.4 Tasks (genuine long jobs only)

**OBS:** live `initialize` already advertises `capabilities.tasks = {list, cancel, requests:{tools/call, prompts/get, resources/read}}`. The transport supports tasks; nothing declares them.

```yaml
tasks:
  - name: segy_ingest_3d        tool: geox_seismic_ingest   expected_duration: PT30M
  - name: inversion_3d          tool: geox_seismic_compute  expected_duration: PT2H
  - name: fwi                   expected_duration: PT8H     checkpointable: true
  - name: gempy_ensemble        tool: geox_model            expected_duration: PT1H
  - name: basin_scale_canon9    tool: geox_basin            expected_duration: PT4H
  - name: las_batch             tool: geox_well_ingest      expected_duration: PT45M
  - name: seismic_4d            expected_duration: PT6H     checkpointable: true
```
**SPEC — V9 (already stated):** `long_running=true ⇔ task_support ∈ {required, optional}`. A tool cannot claim `long_running` and refuse task support, nor advertise `task_support: required` while declaring `long_running: false`. **INT:** this biconditional is what stops "task" from becoming a fourth synonym for "slow tool" — the same entropy that produced four different tool counts.

**SPEC:** tasks emit progress via `geox://artifacts/{id}` polling, never via a bespoke status tool. One noun-scheme for all async state.

---

## 6. outputSchema scientific contract

**OBS — measured against live `tools/list` (26 tools):**

| Field | Occurrences in live schemas |
|---|---|
| `provenance` | 12 |
| `uncertainty` | 14 |
| `evidence_refs` | 6 |
| `artifact_ref` | 5 |
| `claim_state` | 2 |
| `UNVERIFIED` | 1 |
| `QC_VERIFIED` | **0** |
| `depth_basis` | **0** |
| `Physics9` | **0** |
| `CANON-9` | **0** |

**DER:** the scientific contract is ~20% implemented and the enum is not closed anywhere. `outputSchema` is present on **25/26** — the single exception is `geox_surface_status` itself. **INT:** The recovery/meta tool being the one tool with no output schema is fitting: the surface that describes the surface is the least specified part of it.

**SPEC — `scientific_v1` envelope (`schemas/common/evidence_contract.json`):**
```yaml
artifact_ref:  {type: string, format: uri, pattern: "^geox://artifacts/"}   # REQUIRED
claim_state:                                                                  # REQUIRED, CLOSED
  type: string
  enum: [UNVERIFIED, QC_PENDING, QC_VERIFIED, RETRACTED]
  default: UNVERIFIED
evidence_refs: {type: array, minItems: 1, items: {pattern: "^geox://evidence/"}}
depth_basis: {type: string, enum: [TVDSS, MD, TVD, KB, RT, GL]}               # REQUIRED if depth-bearing
units:                                                                        # REQUIRED
  type: object
  properties:
    depth:    {const: m}
    porosity: {const: fraction}          # never percent — unit ambiguity is a falsification risk
    density:  {const: g/cc}
    pressure: {const: MPa}
    temperature: {const: degC}
  additionalProperties: {type: string}   # Physics9 registry token
uncertainty:                                                                    # REQUIRED
  type: object
  required: [method, lower, upper]
  properties:
    method: {enum: [bootstrap, analytical, ensemble, monte_carlo, expert]}
    lower:  {type: number}
    upper:  {type: number}
    n:      {type: integer, minimum: 2}
    confidence_level: {type: number, minimum: 0, maximum: 1, default: 0.9}
provenance:                                                                     # REQUIRED
  type: object
  required: [tool, tool_version, source_hashes]
  properties:
    tool:          {type: string, pattern: "^geox_"}
    tool_version:  {type: string}
    contract_epoch:{type: string}                    # ← ties output to §8 cache key
    surface_hash:  {type: string}
    source_hashes: {type: array, minItems: 1, items: {pattern: "^sha256:[0-9a-f]{64}$"}}
    physics_manifest_hash: {type: string}
    ontology_version: {type: string}
epistemic_label: {enum: [OBS, DER, INT, SPEC]}       # F2 — propagates to the client
confidence:      {type: number, maximum: 0.90}       # F7 — hard cap, schema-enforced
```

**Two constitutional fields the tasking did not specify but the constitution requires:**
- `epistemic_label ∈ {OBS,DER,INT,SPEC}` — F2 TRUTH, propagated to the MCP client so a downstream agent cannot mistake a DER for an OBS.
- `confidence.maximum: 0.90` — F7 HUMILITY enforced **in JSON Schema**, not in prose. A model cannot emit 0.99 and pass validation. **INT:** this is the cheapest possible constitutional enforcement point — the schema validator runs on every response, for free, forever.

**SPEC — V14:** `output_envelope: scientific_v1` ⇒ the resolved `outputs_schema_ref` must `$ref` or inline all REQUIRED fields above. Enforced at generation time, so a tool cannot ship a scientific output without the contract.

**SPEC — the anti-false-success rule.** `evidence_postcondition.py` already carries the doctrine (**OBS**): *"do not list claim-only fields (status/ok) — they are success assertions, not evidence. A payload with only status:OK is FALSE SUCCESS."* Under v3 this becomes **V23**: any output schema whose only required fields are `status`/`ok`/`success` fails generation.

---

## 7. Authorization layer split

**SPEC — three layers, never collapsed. Each answers one question and has one owner.**

```
┌─ L1 TRANSPORT / OAuth ──────────── WHO may reach GEOX at all?
│   owner: MCP auth middleware + OAuth scopes
│   vocab: geox:read | geox:write | geox:admin
│   fail:  401/403 before dispatch
│   NOT:   does not know what a well is
├─ L2 DOMAIN / affordance ────────── WHAT geological data or action?
│   owner: manifest.affordance + roles_required + min_authority
│   vocab: can_read_seismic, can_mutate_prospect, can_seal:false
│   fail:  422 DOMAIN_DENY
│   NOT:   does not decide consequence
└─ L3 CONSEQUENCE / arifOS ───────── MAY this consequential action proceed?
    owner: arifOS kernel ONLY  (Organ Domain Boundary Law 2026-09-17)
    vocab: OBSERVE_ONLY | PROCEED | SEAL   (+ HOLD | VOID)
    fail:  kernel HOLD, GEOX cannot override
    NOT:   GEOX never emits SEAL — V15, schema-enforced
```

### 7.1 Why they must not collapse

**INT:** The existing code already contains the collapse risk. `registry.py::required_authority_for` returns values from `AUTHORITY_LEVELS` (`OBSERVE_ONLY < OPERATOR < LIMITED_MUTATE < FULL < SOVEREIGN`) — a vocabulary that mixes **transport identity** (`OPERATOR`, `SOVEREIGN` = who you are) with **domain consequence** (`LIMITED_MUTATE` = what this does). One enum carrying both meanings means a change to one silently changes the other.

**SPEC — v3 separates them:**
```
L1 principal     : {actor, scopes:[geox:read], session_id, auth:OBSERVE_ONLY}
L2 domain grant  : {affordance, roles_required, min_authority}  ← from manifest
L3 verdict       : {kernel_verdict: PROCEED|HOLD|VOID, seal_authority: arifOS}
```
Admission = `L1.scopes ⊇ tool.roles_required` **∧** `L1.auth ≥ L2.min_authority` **∧** `L3.verdict == PROCEED`. Three conjuncts, three owners, three vocabularies. **Any single one failing produces a distinct error class** — which is what makes an auth failure attributable (cf. `auth-failure-attribution` skill).

### 7.2 Layer-crossing prohibitions (validated)

| # | Rule |
|---|---|
| **V15** | `affordance.can_seal == false` for every GEOX tool — arifOS alone seals |
| V24 | L2 may **narrow** L1, never widen: `min_authority ≥ scope_floor(roles_required)` |
| V25 | L3 is consulted **after** L1∧L2 pass; L3 cannot be pre-satisfied by a manifest field |
| V26 | No manifest field may name an OAuth scope outside `{geox:read, geox:write, geox:admin}` (V17) |

**SPEC — V25 is the anti-shortcut rule.** Today `organ_governance.py` routes C2+/IRREVERSIBLE through the kernel. V25 makes it structural: a tool cannot declare itself pre-approved. **INT:** this is the `degraded_dominates` scar generalised — a label in the manifest must never be able to stand in for a kernel verdict.

**OBS supporting fact:** live `/health` reports `"kernel_verdict": "HOLD"` while `"status": "healthy"` and `authority_ceiling: 555_COMPUTE_ONLY`. **INT:** GEOX already models L3 as an independent, externally-supplied value that can disagree with its own health — the split in this section formalises something the runtime already does.

---

## 8. `arif_route` dispatch contract

**SPEC** — this is the scar-class fix for "ghost tool call."

```python
def arif_route_geox(intent: str, ctx: CallContext) -> RouteDecision:
    """
    1. Read contract_epoch + tool index FROM THE MANIFEST-SERVED SURFACE.
    2. Select a currently-callable tool.
    3. Cache selection on (surface_hash, contract_epoch).
    4. If expected != observed -> HOLD, refresh discovery, DO NOT GUESS.
    """
    # ── STEP 1: authoritative surface, fetched not remembered ─────────
    disc = geox.server_discover()                       # §10, cheap, cached 300s
    epoch      = disc["contractEpoch"]
    surf_hash  = disc["_meta"]["io.geox/surface"]["surface_hash"]
    index      = geox.tools_list_hash(surf_hash)        # G1 index for THIS hash

    # ── STEP 3: cache keyed on the pair, never on intent alone ────────
    key = (surf_hash, epoch, canonicalize(intent))
    if cached := ROUTE_CACHE.get(key):
        return cached                                   # same surface => same route

    # ── STEP 2: select, constrained to the fetched index ──────────────
    cands = rank_by_keywords(intent, index)             # manifest keywords §1.5
    if not cands:
        return RouteDecision(verdict="HOLD", reason="NO_MATCHING_TOOL",
                             recovery=geox.recovery_payload(intent))
    tool = cands[0]
    assert tool.name in index.names, "selection escaped the surface"   # invariant

    # ── STEP 4: verify before dispatch; HOLD, never guess ─────────────
    if tool.expected_surface_hash != surf_hash:
        ROUTE_CACHE.invalidate_prefix(epoch)            # epoch-wide, not entry-wide
        refreshed = geox.server_discover(force=True)
        if refreshed["contractEpoch"] != epoch:
            return RouteDecision(verdict="HOLD",
                reason="CONTRACT_EPOCH_ADVANCED",
                observed=refreshed["contractEpoch"], expected=epoch,
                next_action="re-route from scratch; DO NOT retry the same name")
        return RouteDecision(verdict="HOLD", reason="SURFACE_HASH_DRIFT",
            next_action="refresh discovery and re-route")

    ROUTE_CACHE.put(key, decision := RouteDecision(
        verdict="PROCEED", tool=tool.name, contract_epoch=epoch,
        surface_hash=surf_hash, args=bind(intent, tool.inputs_schema_ref)))
    return decision
```

### 8.1 The four rules, and the failure each closes

| Rule | Failure closed | Evidence it is real |
|---|---|---|
| **1. Read epoch + index from the served surface** | routing from a memorised/stale index | **OBS** `contract_epoch` already has 2 values in-repo (D3) |
| **2. Select only from the fetched index** | ghost tool call | **OBS** D7 — 4 real callables absent from manifest |
| **3. Cache on `(surface_hash, contract_epoch)`** | cache poisoning across a deploy | **OBS** `DEPLOYMENT_DRIFT` scar 2026-09-30 |
| **4. Hash mismatch ⇒ HOLD, refresh, never guess** | silent name-guessing | **OBS** the reported incident: 3 guessed names rejected |

### 8.2 The critical property: **HOLD is a success state**

**SPEC:** `arif_route` returning HOLD with `reason=SURFACE_HASH_DRIFT` is a **correct** outcome. It is not an error, not a degradation, and must not be retried with a different name. **INT:** The ghost-tool-call scar is fundamentally a *retry-with-a-guess* behaviour. Rule 4 removes the guess by making the honest alternative (HOLD + refresh) cheaper than fabricating a name. A router that cannot HOLD will always hallucinate a tool name eventually.

**SPEC:** the cache is **epoch-scoped**, so a `contract_epoch` bump invalidates every cached route at once — no per-entry TTL tuning, no stale-entry sweep. `ttlMs: 300000` on `server/discover` (**OBS**, live) already gives the natural refresh cadence.

**SPEC — required manifest addition for step 2:** `keywords` per tool (§1.5). Without intent-matching metadata, `arif_route` can only select by exact name — which is exactly the mode that fails when the name is wrong. **OBS:** `tool_discovery.py` already carries `keywords=[...]` and `domain_verb=` per tool (line 246-258), so this metadata exists but lives outside the manifest. V-rule **V27**: keyword indexes are generated *from the manifest*, not maintained beside it.

---

## 9. Dual-era MCP transport

**OBS — this already works.** `stateless_era.py` (411 lines) is a functioning dual-era shim, and both eras responded correctly to live probes:

| Era | Probe | Result |
|---|---|---|
| `2026-07-28` stateless | `Mcp-Method: server/discover`, no session | **200**, full payload, `X-MCP-Era: stateless-2026-07-28` |
| `2025-11-25` legacy | `initialize` → `Mcp-Session-Id: ba0473019f…` → `tools/list` | **200**, 26 tools |

The file's own docstring documents the root cause precisely: `mcp` 1.29.0's `SUPPORTED_PROTOCOL_VERSIONS` tops out at `2025-11-25` and 400s any request carrying `2026-07-28`; the shim answers `server/discover` natively *before* transport validation and bridges other modern-era requests onto one shared internal `2025-11-25` session. It is placed innermost, additive, transport untouched, and documents its own reversibility.

**DER:** §9 needs **no new transport work**. It needs the manifest wired into the payload the shim already serves.

### 9.1 Single endpoint, single manifest, two projections

```
                         ┌──────────────────────┐
        POST /mcp/ ─────▶│  era_detector        │
                         │  (headers/body _meta)│
                         └───────┬──────┬───────┘
                    2026-07-28   │      │  ≤2025-11-25
                                 ▼      ▼
                     ┌───────────────┐ ┌──────────────────────┐
                     │ server/discover│ │ initialize           │
                     │ (no session)   │ │ → Mcp-Session-Id     │
                     │  = G11(M)      │ │ → notifications/init │
                     └───────┬───────┘ │ → tools/list = G1(M) │
                             │         └──────────┬───────────┘
                             └────────┬───────────┘
                                      ▼
                          ┌───────────────────────┐
                          │   manifest.yaml  (M)  │  ← ONE input
                          │   G1..G14 generators  │
                          └───────────────────────┘
```

**SPEC — the era-parity invariant (V28):**
```
names(tools/list @ 2026-07-28) == names(tools/list @ 2025-11-25) == names(G1(M))
```
Both eras are *projections of one manifest*, never independently maintained lists. A client on either era must see the identical 26 names. CI asserts this by probing both eras and diffing (the probe code is already written — this session used it).

### 9.2 Era differences that are legitimately allowed

| Aspect | `2026-07-28` | `≤2025-11-25` |
|---|---|---|
| Session | none required | `Mcp-Session-Id` after `initialize` |
| Discovery | `server/discover` first | `initialize` result capabilities |
| Capabilities | per-request | per-session, negotiated once |
| Tool names | **identical** | **identical** |
| Schemas | **identical** | **identical** |
| `surface_hash` | in `_meta` | in `_meta` |

**SPEC:** the *names and schemas must not differ by era*. Only the handshake differs. **INT:** if era ever changed the tool set, `S_declared` would become era-dependent and §3's parity test would need an era parameter — reintroducing exactly the multiplicity this design exists to remove.

### 9.3 Fixing D4 (triple-declared protocolVersion)

**SPEC — V29:** `protocolVersion` in `.well-known/mcp/server.json` is **generated by G11** from `transport.primary_era`, and the card must advertise the *same* version `server/discover` returns. Today: card `2025-06-18` vs discover `2026-07-28` vs negotiated `2025-11-25` — three values, none generated. Under V29 all three are functions of one manifest field.

---

## 10. `server/discover` payload + `geox://server/info`

### 10.1 Enriched `server/discover` (G11)

**OBS — live payload today** (works, but under-informed):
```json
{"resultType":"complete","supportedVersions":["2026-07-28","2025-11-25","2025-06-18","2025-03-26","2024-11-05"],
 "capabilities":{...},"ttlMs":300000,"cacheScope":"public",
 "_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28",
          "io.geox/surface":{"public_tools":26,
                             "source":"geox_mcp.registry.CANONICAL_PUBLIC_TOOLS"}}}
```
It carries a **count** but no **hash** and no **epoch** — so `arif_route` (§8) cannot cache on it. That is the one change that matters.

**SPEC:**
```json
{
  "protocolVersion": "2026-07-28",
  "server": "GEOX",
  "version": "2026.10.01",
  "contractEpoch": "GEOX-CONTRACT-2026.10.01-MANIFEST-V3",
  "capabilities": { "tools": true, "resources": true, "prompts": true, "tasks": true },
  "supportedVersions": ["2026-07-28","2025-11-25","2025-06-18","2025-03-26","2024-11-05"],
  "resultType": "complete",
  "ttlMs": 300000,
  "cacheScope": "public",
  "_meta": {
    "io.geox/surface": {
      "surface_hash": "sha256:…",          // ← Merkle root of G1..G14 (§2.2)
      "tool_hash":    "sha256:…",          // ← h1, cache key for the tool index
      "public_tools": 26,
      "resource_count": 53,
      "resource_template_count": 10,
      "prompt_count": 16,
      "task_count": 7,
      "compat_alias_count": 2,
      "deprecated_count": 0,
      "recovery_tool": "geox_surface_status",
      "recovery_resource": "geox://surface/truth",
      "manifest_schema": "geox.manifest.v3",
      "generated_by": "G11",
      "source": "manifest.yaml"            // NOT registry.py — one truth
    }
  }
}
```
**SPEC — `recovery_tool` and `recovery_resource` in the discover payload** means a client learns both recovery doors *before* it ever fails, from the same response that tells it the surface hash. **INT:** recovery information delivered at discovery time cannot be stale relative to the surface it describes — they are one payload. This is the structural fix for the reported incident: the client that got rejected had never been told, in a machine-readable way, what to call instead.

### 10.2 `geox://server/info` resource

```yaml
source_commit:        297abcb04afd163593b1bce078123a08a5b1f1e7   # from git
built_commit:         297abcb…          # from BUILD artifact, written at build time
deployed_commit:      297abcb…          # from /opt/geox/DEPLOYED_COMMIT, written at deploy
commit_provenance:                      # ← NEW: proves the three are independent
  source_commit_source:   "git rev-parse HEAD"
  built_commit_source:    "build-info.json (CI artifact)"
  deployed_commit_source: "/opt/geox/DEPLOYED_COMMIT (deploy step)"
  oracle_independent:     true          # false ⇒ drift check is VOID, not "aligned"
deployment_drift:
  drift: false
  status: aligned
  check_is_tautological: false          # ← D2 regression flag
surface_hash:         "sha256:…"
tool_count: 26
resource_count: 53
prompt_count: 16
contract_epoch: "GEOX-CONTRACT-2026.10.01-MANIFEST-V3"
ontology_version:  "CANON-9/1.x"
physics9_version:  "Physics9/x.y"
physics_manifest_hash: "sha256:c905aef8…"   # ← currently returns _GIT_VERSION (D2)
canon9_version: "…"
compat_aliases: {geox_well_desk: geox_well, geox_well_view: geox_well}
deprecated_tools: []
kernel_verdict: HOLD                    # L3, externally supplied (§7)
authority_ceiling: 555_COMPUTE_ONLY
```

**SPEC — the D2 fix, stated as an invariant:** `source_commit`, `built_commit`, `deployed_commit`, and `physics_manifest_hash` must come from **four different provenances**, declared in `commit_provenance`. If any two share a source variable, `oracle_independent: false` and `deployment_drift.check_is_tautological: true` — and §3's `test_g0_no_oracle_tautology` fails the build.

**INT:** This is the single highest-value line in the entire design. A drift check that cannot fail reports `"status": "aligned"` forever, and every downstream consumer — including the sealed `/health` output observed live this session — inherits a false assurance. Per the two refuted physics verdicts and the `claimed-before-checking-twice` scar, **an oracle that measures its own construction is worse than no oracle**, because it is believed.

---

## 11. Internal inconsistencies & open questions for Lane 555

### 11.1 Questions needing live evidence (Lane 555)

| # | Question | Why 333 cannot answer it read-only |
|---|---|---|
| **Q1** | Which 3 names did the connector actually advertise to the ChatGPT client? | Requires the connector's descriptor cache / client-side log. My probes show all 3 absent from `tools/list`, card, and packs — so the client was told from a source I cannot see. **This determines whether the bug is GEOX-side or connector-side.** |
| **Q2** | Is `servers/witness.py` mounted on `:8081`, or a different port/endpoint? | It registers `geox_system_registry_status` etc. Live `:8081` `tools/list` does not expose them. If witness is mounted elsewhere, the client may have been correct about *a* surface — just not this one. |
| **Q3** | Does any consumer actually call `tools_for_profile`? | Only `generate_all_surfaces.py:178` does (**OBS**). If nothing consumes profiles at runtime, the 20-vs-26 gap is latent, not the live cause — which would move the root cause entirely to Q1/Q2. **This is the highest-leverage unknown in the doc.** |
| **Q4** | What is the real `built_commit` vs `deployed_commit`? | Both are `_GIT_VERSION` today (D2). Need an independent deploy artifact to know whether drift is *actually* absent or merely *unmeasurable*. |
| **Q5** | Are the 22 `GHOST_TOOLS` genuinely dead, or still reachable via a sub-server? | Ghosting is a `registry.py` set-subtraction; it does not unregister the callable. Same class as D7. |
| **Q6** | Live count of the 39 internal tools actually registered at runtime | Card says `totalRegistered: 65`; `CANONICAL_RUNTIME_TOOLS` is 87 (includes ghosts, D8). Which is real? |
| **Q7** | Does `geox://surface/truth` (resource) serve the same content as `geox_surface_status` (tool)? | §5.1 proposes it as the second recovery door. Needs content verification before relying on it. |

### 11.2 Internal inconsistencies in *this* design (declared per F7)

**I1 — §2.4 vs the tasking.** I recommend `G3 = G1` (no aliases advertised); the tasking specifies `G3 = G1 ∪ compat_aliases`. I have argued for the narrower set and flagged it as an F13 binary rather than silently complying. **This is a real disagreement with the brief, stated openly.**

**I2 — §3 `S_observed` uses `<=`, the tasking uses `==`.** Changed deliberately: `==` makes parity depend on traffic, which is non-deterministic. Documented in §3.

**I3 — `surface_hash` is overloaded.** §2.2 defines it as a Merkle root over 14 generators; §10.1 emits both it *and* `tool_hash`. `arif_route` (§8) caches on `surface_hash` but only needs `tool_hash` for tool selection. **Resolution:** cache on `(tool_hash, contract_epoch)`, and use `surface_hash` for the coarser "anything changed" invalidation. §8's code uses `surf_hash` for both — that should be split before implementation.

**I4 — the doc specifies 10 resource templates; live has 0.** §5.1 is therefore net-new construction (~10 templates + resolvers), not refactor. Effort estimate is materially higher than the other sections and I have no basis to size it beyond that.

**I5 — `min_authority` vocabulary mismatch.** §7 keeps `OBSERVE_ONLY|OPERATOR|LIMITED_MUTATE|FULL|SOVEREIGN` (existing `AUTHORITY_LEVELS`) for L2, while the tasking's §7 names L3 as `OBSERVE_ONLY|PROCEED|SEAL`. `OBSERVE_ONLY` appears in **both** layers' vocabularies. **This is a genuine collision** and needs renaming before implementation — proposal: L2 uses `AUTH_BAND_*`, L3 uses `VERDICT_*`. Flagged, not resolved.

**I6 — V15 vs `geox_claim(mode=seal)`.** **OBS:** `registry.py` documents `geox_claim` `mode=seal` as "the irreversible path" requiring `ack_irreversible`, and `_MUTATING_VALUE_OVERRIDES` treats it as MUTATE. But V15 says no GEOX tool may `can_seal`. Either `geox_claim` mode=seal is *not* a constitutional SEAL (likely — it is a domain claim-state transition, arifOS ratifies), or V15 is violated by a live tool. **Needs 555/888 adjudication.** My reading (INT, 0.7): `claim_state: QC_VERIFIED` is a *domain* state, distinct from an arifOS SEAL — but the shared word "seal" makes this a live ambiguity, and Referent Primacy doctrine (2026-09-21) says the referent matters more than the name. **Recommend renaming the GEOX mode to `finalize` or `attest`** to remove the collision.

### 11.3 Sequencing recommendation

**INT (confidence 0.85):** ordered by (drift closed) ÷ (blast radius):

1. **Wire the existing generator into CI** (`--check` + lock verify). Two workflow lines. Closes D6, and 4 drifted files become build failures immediately. **No schema change. Fully reversible.**
2. **Add `pinned_recovery_tool` + V21 + V5 pack completeness.** Closes the actual §0.1 root cause. Small, additive.
3. **Make RT1's recovery string generated (D5) + add `requested_tool_status` taxonomy.** Closes the reported incident class.
4. **Fix D2 oracle independence.** Highest epistemic value; touches `build_info_handler` (deployed runtime ⇒ **F13-class**).
5. **Fix D3 (`contract_epoch` single-valued, V18).** Precondition for §8.
6. **Migrate manifest → v3** (behaviour primitives, V10/V11 ghost closure, G8 derived annotations).
7. **§5 resources/prompts/tasks** — net-new, largest effort, lowest urgency.
8. **§8 `arif_route`** — depends on 5 + 6.

Steps 1-3 are the reversible, high-yield core. Steps 4-8 each need an explicit F13 checkpoint per the sub-agent over-execution scar (2026-09-28): **one finding, one ceremony, one mutation.**

---

## 12. Confirmation — no production artifact mutated

**Confirmed. Zero mutations.** Every command this session was read-only:

| Command class | Used | Mutation? |
|---|---|---|
| `grep` / `ls` / `wc` / `sed -n` / `head` / `find` | yes | No — read |
| `curl` GET `/health`, `/mcp/health`, `/.well-known/mcp/server.json` | yes | No — read |
| `curl` POST `/mcp/` (`initialize`, `tools/list`, `prompts/list`, `resources/list`, `server/discover`) | yes | No — MCP discovery/read methods only; no `tools/call` was issued |
| `python3` importing `geox_mcp.registry` / `surface_manifest` and printing set arithmetic | yes | No — import + read |
| `generate_all_surfaces.py **--dry-run**` | yes | **No — script's own output: "DRY-RUN complete. No files were written."** |
| `mkdir -p /root/AAA/federation` | yes | Directory already existed (`drwxr-xr-x 30`, mtime `Oct 1 18:59`, before this session). Created nothing. |
| Edit / Write to any source | **no** | — |
| deploy / restart / install / systemctl | **no** | — |

**Files NOT touched:** `/root/arifOS/**`, `/opt/arifos/**`, `/opt/geox/**`, RT1 (`geox_middleware.py`), the connector, the GEOX MCP server, the kernel, and every file under `/root/GEOX/src/`.

**The only file written this session is this document:**
`/root/AAA/federation/geox_one_manifest_design_2026-10-01.md`

**Side effects to declare honestly (F2):** the MCP `initialize` handshake created one transient session (`Mcp-Session-Id: ba0473019f354a8d971e2a1d23e54e71`) in GEOX's in-memory session table, and four probe files were written to `/tmp` (`h_init.txt`, `b_init.json`, `b_list.txt`, `b_res.txt`). No persistent GEOX state, no artifact, no receipt chain, and no sealed record was altered. Session state is not a production artifact and expires with the process.

**Hook note:** the `PostToolUse` hook emitted `[F2 RECEIPT CITATION] W_SCAR-class mutation detected` on several Bash calls. **These were false positives** — the flagged calls were `grep`, `ls`, `curl GET`, and `python3` set arithmetic. Declared per F2 rather than left implicit; no mutation occurred to cite a receipt for. Where I assert a fact, the receipt is the file path and line, cited inline throughout.

---

## Appendix A — Evidence index (all OBS, this session)

| Fact | Receipt |
|---|---|
| RT1 rejection string | `/root/GEOX/src/geox_mcp/geox_middleware.py:722-731` |
| Recovery string is a literal | `/root/GEOX/src/geox_mcp/geox_middleware.py:729` |
| `GHOST_TOOLS` = 22 | `/root/GEOX/src/geox_mcp/registry.py` (import-verified) |
| `tools_for_profile` / packs | `/root/GEOX/src/geox_mcp/registry.py` + `tools_manifest.yaml:capability_packs` |
| 6 public tools in no pack | derived by import; set diff printed |
| `public_count_target: 31` vs 26 | `/root/GEOX/src/geox_mcp/tools_manifest.yaml` |
| `surface_attestation ok=False` | import-verified, `err=SURFACE_COUNT_DRIFT` |
| `surface_hash` (current, 1-surface) | `ee2f2de891a5df6260e8aa5068974aa41eb62542587b651af25baaad32cfdf33` |
| Tautological build_info | `/root/GEOX/src/geox_mcp/server.py:build_info_handler` |
| `contract_epoch` 2 values | `/root/GEOX/src/geox_mcp/server.py:71` vs `/root/GEOX/src/geox_core/enums/statuses.py:28` |
| Ghost callables (D7) | `/root/GEOX/src/geox_mcp/servers/witness.py:60,66`; `/root/GEOX/src/geox_mcp/tools/registry.py:103,805` |
| `mcp_health_check` legacy alias | `/root/GEOX/contracts/tools/unified_13.py:95,103` |
| Generator exists, not CI-wired | `/root/GEOX/scripts/generate_all_surfaces.py`; `grep -rn generate_all_surfaces .github/` → empty |
| Dry-run: 4/6 CHANGED | `generate_all_surfaces.py --dry-run` output |
| Live `tools/list` = 26, `surface_status` present | JSON-RPC probe `127.0.0.1:8081/mcp/` |
| Live annotations uniform across 26 | probe; `readOnly:true/destructive:false/idempotent:true/openWorld:false` |
| `outputSchema` 25/26, missing on `surface_status` | probe |
| Scientific-field occurrence counts | probe, §6 table |
| Live prompts = 16 | `prompts/list` |
| Live resources = 53, templates = 0 | `resources/list` |
| Card `protocolVersion: 2025-06-18`, `totalRegistered: 65` | `/.well-known/mcp/server.json` |
| `server/discover` live payload | JSON-RPC probe, `2026-07-28` era |
| Dual-era shim design + root cause | `/root/GEOX/src/geox_mcp/stateless_era.py:1-90` |
| `/health` `kernel_verdict: HOLD`, `authority_ceiling: 555_COMPUTE_ONLY` | `curl 127.0.0.1:8081/health` |
| Evidence postcondition doctrine | `/root/GEOX/src/geox_mcp/evidence_postcondition.py:102-118` |

---

*Forged, not given — DITEMPA BUKAN DIBERI.*
*Lane 333 ARCHITECTURE · claude-code/FI-002 · 2026-10-01*
*Design proposal only. Nothing here is ratified. Implementation requires F13 per step (§11.3).*
