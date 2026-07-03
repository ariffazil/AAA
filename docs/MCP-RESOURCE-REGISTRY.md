# MCP RESOURCE REGISTRY — Central Discovery

> **Single source of truth for ALL live MCP resource URIs across the arifOS federation.**
> Generated: 2026-07-03. Update when resources change.
> Companion: `MCP-RESOURCES-MAP.md` (architecture/placement rules).

## Summary

| Organ | Protocol | Resource Count | Structure |
|-------|----------|---------------|-----------|
| arifOS | `arifos://` | ~30 | Modular (33 .py files) |
| GEOX | `geox://` + `tree777://` | ~55 | Monolith (1 .py file) |
| WEALTH | `wealth://` | 14 | Inline (server.py) |
| WELL | `well://` | 18 | Modular (19 .py files) — **gold standard** |
| A-FORGE | `forge://` | 8 | TypeScript (resources.ts) |
| Skills | `skill://` | 98 (49 × 2) | FastMCP SkillsDirectoryProvider |
| **TOTAL** | — | **~223** | — |

---

## arifOS (Ω Constitutional Kernel — :8088)

| URI | Purpose | Module |
|-----|---------|--------|
| `arifos://identity` | Sovereign identity manifest | identity.py |
| `arifos://doctrine` | Constitutional floors F1-F13 | doctrine.py |
| `arifos://schema` | Canonical tool blueprint | schema.py |
| `arifos://trinity` | AAA Trinity lanes (ΔΩΨ) | trinity.py |
| `arifos://civilization` | 7 organs + 3 strata ontology | civilization.py |
| `arifos://bootstrap` | Full federation world model | bootstrap.py |
| `arifos://memory` | L1-L6 memory architecture | memory.py |
| `arifos://jurisdiction` | 5 autonomy bands + CapabilityGrant | jurisdiction.py |
| `arifos://vitals` | Constitutional vitals thresholds | vitals.py |
| `arifos://seal-readiness` | Vault integrity + seal gate | seal_readiness.py |
| `arifos://mcp-alignment` | MCP spec conformance matrix | mcp_alignment.py |
| `arifos://loop-engineering` | 7-stage reality loop | loop_engineering.py |
| `arifos://quickstart` | LLM client getting started | quickstart.py |
| `arifos://human/metabolized` | Sovereign context (compact) | human_context.py |
| `arifos://reality/state` | Multi-layer reality snapshot | reality_state.py |
| `arifos://forge` | Forge context | forge.py |
| `arifos://philosophy` | Philosophical anchors | philosophy.py |
| `arifos://aaa-language` | AAA language conventions | aaa_language.py |
| `arifos://agent_geometry` | Agent geometry model | agent_geometry.py |
| `arifos://session/{id}` | Session state | session.py |
| `arifos://vault/{vault_type}` | Vault999 template | vault999_template.py |
| `arifos://mcp/surface-map` | Agent surface map | surface_map.py |
| `arifos://doctrine/floors` | Floor definitions | surface_map.py |
| `arifos://registry/organs` | Organ registry | surface_map.py |
| `arifos://state/latest` | Latest state | surface_map.py |
| `arifos://receipts/latest` | Latest receipts | surface_map.py |
| `arifos://tools/self-model` | Tool self-model | embodied_resources.py |
| `arifos://tools/permissions` | Tool permissions | embodied_resources.py |
| `arifos://tools/composition-matrix` | Tool composition | embodied_resources.py |
| `arifos://boundaries/domain/{id}` | Domain boundaries | embodied_resources.py |
| `arifos://witness/log` | Witness log | embodied_resources.py |
| `arifos://witness/stats` | Witness statistics | embodied_resources.py |
| `arifos://resources/index` | Resource index | resources_index.py |
| `arifos://resources/audit` | Resource audit | resources_index.py |
| `arifos://skills-catalog` | Skills catalog | skills_catalog.py |

---

## GEOX (🌍 Earth Intelligence — :8081)

| URI | Purpose |
|-----|---------|
| `geox://identity` | GEOX organ identity |
| `geox://reality/context` | Earth reality context |
| `geox://registry/apps` | GEOX MCP apps |
| `geox://profile/status` | Profile status |
| `geox://capabilities` | Tool capabilities |
| `geox://surface/truth` | Surface truth class |
| `geox://resources/index` | Resource index |
| `geox://resources/ontology/index` | Ontology index |
| `geox://resources/playbooks/index` | Playbooks index |
| `geox://resources/prompts/index` | Prompts index |
| `geox://resources/schemas/index` | Schemas index |
| `geox://resources/{category}/{name}` | Category resource |
| `geox://artifacts/index` | Artifacts index |
| `geox://claims/index` | Claims index |
| `geox://claims/graph` | Claims graph |
| `geox://layers/index` | Map layers index |
| `geox://layers/{id}/package` | Layer package |
| `geox://literature/index` | Literature index |
| `geox://literature/{ref}` | Literature reference |
| **Basins** | |
| `geox://basins/index` | Basins index |
| `geox://basins/malay-basin/profile` | Malay Basin profile |
| `geox://basins/{name}/profile` | Basin profile |
| **Deep Time** | |
| `geox://deep_time/temperature` | Temperature record |
| `geox://deep_time/co2` | CO2 record |
| `geox://deep_time/o2` | O2 record |
| `geox://deep_time/d18o` | δ18O record |
| `geox://deep_time/sea_level` | Sea level record |
| **Stratigraphy** | |
| `geox://stratigraphy/macrostrat_timescale` | Macrostrat timescale |
| `geox://stratigraphy/macrostrat_units` | Macrostrat units |
| `geox://stratigraphy/onegeology` | OneGeology |
| **Geophysics** | |
| `geox://magnetics/emag2v3` | EMAG2v3 |
| `geox://magnetics/icgem_vrm` | ICGEM VRM |
| `geox://magnetics/wmm2025` | WMM2025 |
| `geox://heatflow/global` | Global heat flow |
| `geox://heatflow/ihfc` | IHFC heat flow |
| **Seismology** | |
| `geox://earthquake/usgs_summary` | USGS summary |
| `geox://earthquake/usgs_dyfi` | USGS DYFI |
| **Ocean/Atmosphere** | |
| `geox://ocean/copernicus_bathymetry` | Copernicus bathymetry |
| `geox://ocean/copernicus_sea_level` | Copernicus sea level |
| `geox://atmosphere/era5` | ERA5 |
| `geox://atmosphere/era5_pressure_levels` | ERA5 pressure levels |
| `geox://bathymetry/etopo1` | ETOPO1 |
| `geox://bathymetry/gebco2024` | GEBCO2024 |
| `geox://bathymetry/srtm15plus` | SRTM15+ |
| **Other** | |
| `geox://hydrology/usgs_nwis` | USGS NWIS |
| `geox://geochemistry/earthchem` | EarthChem |
| `geox://paleomag/magic` | MagIC |
| `geox://space/kp_index` | Kp index |
| `geox://space/solar_nso` | Solar NSO |
| `geox://tectonics/gplates_velocity` | GPlates velocity |
| `geox://tectonics/gplates_paleomask` | GPlates paleomask |
| **Render** | |
| `geox://render/surfaces/{id}` | Surface render |
| `geox://render/cubes/{id}/manifest` | Cube manifest |
| `geox://render/cubes/{id}/lod/{lod}/brick/{x}/{y}/{z}` | Cube brick |
| `geox://render/cubes/{vol}/{orientation}/{slice}` | Cube slice |
| `geox://render/payload-schema/{version}` | Payload schema |
| **Tree777 Wiki** | |
| `tree777://index` | Wiki full index |
| `tree777://skills/geox/{name}` | GEOX skill page |
| `tree777://geo/concepts/{name}` | Concept page |
| `tree777://geo/scars/{name}` | Scar page |

---

## WEALTH (💰 Capital Intelligence — :18082)

| URI | Purpose |
|-----|---------|
| `wealth://` | Root |
| `wealth://schema` | Canonical schema |
| `wealth://tools/registry` | Tool registry |
| `wealth://prompts/index` | Prompts index |
| `wealth://domains/index` | Domains index |
| `wealth://glossary` | Capital glossary |
| `wealth://canon/002-human-law` | Human law canon |
| `wealth://federation/contract` | Federation contract |
| `wealth://health` | Organ health |
| `wealth://reality/context` | Capital reality |
| `wealth://market/sources` | Market data sources |
| `wealth://risk/thresholds` | Risk thresholds |
| `wealth://affordance/contracts` | Affordance contracts |
| `wealth://handoff/arifos-schema` | arifOS handoff schema |
| `wealth://replay/receipt-schema` | Receipt replay schema |
| `wealth://runtime/policy` | Runtime policy |

---

## WELL (🫀 Human Readiness — :18083)

| URI | Purpose | Module |
|-----|---------|--------|
| `well://identity` | Five-well frame | identity.py |
| `well://doctrine` | REFLECT_ONLY + HARAM | doctrine.py |
| `well://bio/signals` | 4-tier × 13-signal map | bio_signals.py |
| `well://metabolic/flux` | Flux equation + thresholds | flux.py |
| `well://decision/classes` | C1-C5 × M1-M5 routing | decision_classes.py |
| `well://coupling` | H × M × G coupling | coupling.py |
| `well://human/substrate` | Human contract | human_substrate.py |
| `well://machine/substrate` | Machine contract | machine_substrate.py |
| `well://chemistry/glue` | Cross-organ glue | chemistry_glue.py |
| `well://transport/loop` | 5-stage reaction loop | transport_loop.py |
| `well://registry` | Surface registry | registry.py |
| `well://physics/laws` | Physics laws | physics_laws.py |
| `well://signals/consent-integrity` | Consent integrity | consent_integrity.py |
| `well://signals/information-asymmetry` | Info asymmetry | info_asymmetry.py |
| `well://substrate/interaction` | Interaction substrate | interaction_substrate.py |
| `well://bridge/arifos-kernel` | Bridge to arifOS | bridge_arifos_kernel.py |
| `well://bridge/geox` | Bridge to GEOX | bridge_geox.py |
| `well://bridge/wealth` | Bridge to WEALTH | bridge_wealth.py |

---

## A-FORGE (⚒️ Execution — :7071/:7072)

| URI | Purpose |
|-----|---------|
| `forge://governance/floors` | F1-F13 floor reference |
| `forge://approvals/pending` | Hold queue |
| `forge://memory/working` | Working memory |
| `forge://execution/leases/status` | Lease status |
| `forge://execution/reality/snapshot` | Reality snapshot |
| `forge://execution/receipts/recent` | Recent receipts |
| `forge://execution/manifests` | Build/deploy manifests |
| `forge://execution/forge_work/pointers` | Forge work pointers |
| `forge://vault/categories` | Vault categories |
| `forge://vault/records` | Vault records |
| `forge://well/state` | WELL state bridge |

---

## Skills (skill:// — arifOS MCP)

49 skills × 2 URIs each = 98 URIs.

| Pattern | Purpose |
|---------|---------|
| `skill://{name}/SKILL.md` | Skill instructions |
| `skill://{name}/_manifest` | File listing |

Full list: `ls /root/.agents/skills/`

---

## Placement Rules (from MCP-RESOURCES-MAP.md)

1. Kernel state → arifOS only
2. Agent/civilization state → AAA only
3. Execution/receipts → A-FORGE only
4. Domain evidence → L1 organs (GEOX/WEALTH/WELL)
5. Shared canon → central (AAA + arifOS), referenced by pointer
6. MCP-native: `@mcp.resource` decorator + `resources/list` + `resources/read`
7. Version + hash on every resource
8. Blast + floors declared in meta

---

*DITEMPA BUKAN DIBERI — Resources are state, not action. Placed by layer. Zenned under AAA.*
