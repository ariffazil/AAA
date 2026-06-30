# MCP RESOURCES MAP — Zen Aligned (2026-06-30)

**SOT under AAA.** Extends AAA_ZEN_INIT.md + heptalogy. All agents/warga load this via reference + MCP resource read after AGENTS.md + AAA_ZEN_INIT.

**APEX THEORY framing (canonical from AAA/agents/888-APEX/APEX_THEORY_AND_FEDERATION.md + A-FORGE copy):**

Intelligence is three layers (no layer replaces the one above):

```
L3: CIVILIZATION INTELLIGENCE (ASI) — Meaning, direction, coordination, state, alignment
  Δ (human telos): ariffazil/ariffazil (profile + HUMAN/ memory + SKILL_INDEX)
  Ω (constitutional): arifos (kernel)
  L3 state foundation: AAA (A2A, agent registry/cards, cockpit, zen, mesh)

L2: GOVERNED EXECUTION (AGI) — How, under constraints, autonomous but leased
  Ψ: A-FORGE (reality_loop, leases, forge_*, receipts, viz)

L1: SUBSTRATE / DOMAIN INTELLIGENCE — Facts, evidence, compute, vitality
  GEOX (earth evidence), WEALTH (capital), WELL (vitality mirror)
```

**GitHub mirrors (exact organ reflections):**
- https://github.com/ariffazil/ariffazil — Δ human / profile / federation index
- https://github.com/ariffazil/arifos — Ω arifOS kernel (llms.txt, contracts/mcp_surface.yaml, arifosmcp)
- https://github.com/ariffazil/AAA — L3 state/A2A/ASI civ foundation + agents/AAA_ZEN_INIT
- https://github.com/ariffazil/A-FORGE — Ψ execution
- https://github.com/ariffazil/geox , /wealth , /well — L1 domains

Public static resources surface via: llms.txt, AGENTS.md, contracts/mcp_surface.yaml, static/agent-card.json, README, resources/ dirs.

Live: organ MCP endpoints (resources/list + resources/read).

---

## 1. Resource vs Tool vs Prompt vs Skill (MCP distinction)

- **Tools**: Actions / verbs (arif_*, geox_*, forge_*, wealth_*, well_*). Mutable side-effects. Governance gated.
- **Resources**: Stable, addressable, mostly read-only state/canon/artifacts (URI like `well://identity`, `arifos://kernel/floors`). FastMCP `@mcp.resource("scheme://path")`.
- **Prompts**: Init templates, instructions (MCP prompts provider; per-organ *_init).
- **Skills**: Packaged behavior (FastMCP skills provider / .agents/skills/ + AAA zen central).

Zen rule (post 000-init-intent-classify + AAA_ZEN_INIT): 
- Doctrine/tables in central (AGENTS.md + AAA_ZEN_INIT + this map + INVARIANTS/MEANING).
- Per-organ: only **own domain + bridges** as live MCP resources.
- Agents: reference + `resources/read` (MCP) or file pointers. No full copies.

Use registry_status / TOOLREGISTRY pattern + resource registry for no-dup.

---

## 2. Canonical URI Scheme & 14+ Families (extended)

Base from federation-p1/resources/canonical_resources.py (14 families) + organ extensions.

Families (read-only, versioned, sha'd):
schema | health | registry | canon | glossary | contract | intake | regime | uncertainty | contradiction | bandwidth | handoff | envelope | receipt

**Layered URIs (placement by organ/layer):**

### Kernel / AGI Substrate (arifOS — Ω, L3/ L2 governance)
- arifos://kernel/identity
- arifos://kernel/floors (F1-F13 manifest)
- arifos://kernel/session (init state)
- arifos://kernel/vault/liveness (or va ult999 pointer)
- arifos://kernel/heptalogy (or pointer to AGENTS + AAA_ZEN)
- arifos://kernel/doctrine
- arifos://kernel/reality_state
- arifos://kernel/trinity (ΔΩΨ)
- arifos://kernel/civilization
- arifos://kernel/philosophy
- runner://receipt/{run_id} (context engine, current)
- runner://policy/v1
- arifos://leases/* (governance side of leases)

**Owned per mcp_surface.yaml (arifOS):** governance_primitives, floor_checks, memory_governance, audit_and_vault, federation_brokering.

Files: /root/arifOS/arifosmcp/resources/ (~32 modules: identity.py, runner.py, doctrine.py, reality_state.py, vitals.py, session.py, vault999_template.py, trinity.py ... + resources_index.py support).

### State / ASI Civilization Foundation (AAA — L3)
- aaa://state/agent-registry (AAA_AGENTS_REGISTRY.json + live)
- aaa://state/a2a-cards (per-warga .well-known/agent-card-*.json + a2a-server/agent-cards/)
- aaa://state/zen-init (this + AAA_ZEN_INIT.md as resource)
- aaa://state/cockpit (mesh/state, hold queue)
- aaa://state/session-identity
- aaa://state/mesh-topology
- aaa://contracts/mcp_surface (and federation contracts)
- aaa://a2a/peer-contracts

**Owned per mcp_surface (AAA):** cockpit_workflows, a2a_gateway, session_identity, operator_visibility, agent_cards.

Files: /root/AAA/a2a-server/agent-cards/* , /root/AAA/agents/agent_cards/ , contracts/ , public/ static.

A2A makes these first-class addressable resources (machine + human readable).

### Execution / Governed Agentic (A-FORGE — Ψ, L2)
- aforge://execution/leases/status
- aforge://execution/reality/{loop,source,snapshot}
- aforge://execution/receipts/{id}
- aforge://execution/manifests (build/deploy)
- aforge://execution/chart-data (forge_chart outputs as resources)
- aforge://execution/forge_work (pointers to recent sealed)
- aforge://leases/* (runtime)

Current: Strong primitives in src/domain/forge/workflow/reality_source.ts , leaseKernel.test , receiptClient, data/*.jsonl , forge_work/ receipts. Explicit MCP @resource light — zen gap to fill.

**Owned:** deployment_substrate, build/execute (via contracts).

### L1 Domain Substrates

**GEOX (earth evidence):**
- geox://evidence/{well,seismic,prospect,claim}
- geox://basins/index
- geox://resources/artifacts , /render/* (geox://render/surfaces/... in tests)
- geox://claims/graph , /uncertainty
- ui://* (MCP apps in apps/ — ac_risk, seismic_vision etc.)
- Files heavy: /root/GEOX/resources/ (79), data/evidence , geox_panels , wells/*.las

Strong on artifact + render resources. Apps expose ui:// .

**WEALTH (capital intelligence):**
- wealth://schema , health , registry , canon , glossary
- wealth://capital/npv|emv|irr|risk|thresholds
- wealth://collapse/signatures
- wealth://flows , /personal , /market
- wealth://handoff/arifos
- Partial in wealth_mcp/resources/ (registry, sot, sources, policy, translation, examples)
- 14-family proposal exists. mcp_surface focuses tools; resources lighter.

**WELL (vitality — best current impl):**
- well://identity (five-well frame — H/M/G/C/U — sovereign canon)
- well://metabolic/flux
- well://decision/classes (C1–C5 human / M1–M5 machine)
- well://coupling , /chemistry/glue , /transport/loop
- well://bridge/{arifos-kernel,geox,wealth}
- well://signals/consent-integrity , /human_substrate , /machine_substrate
- well://registry , /doctrine , /physics_laws , /vitals/arif , /state/arif
- Explicit @mcp.resource in every well_mcp/resources/*.py (20+). Reflect-only.
- Perfect model for state resources + bridges.

---

## 3. Placement Rules (Zen + APEX)

1. **Kernel state only in arifOS** (Ω). No domain evidence.
2. **Civilization/agent state only in AAA** (L3). A2A cards + registry = resources.
3. **Execution state + receipts in A-FORGE** (Ψ). Leases/reality/receipts as resources. Tools mutate; resources observe.
4. **Domain evidence/compute/vitals in L1 organs**. Bridges (WELL style) for cross.
5. **Δ human in ariffazil/ariffazil profile + HUMAN/** — memory graphs, transcripts, identity. Not MCP resources primarily (personal).
6. **Shared canon** (doctrine, floors, heptalogy, INVARIANTS, APEX theory): central in AAA + arifOS; referenced by pointer or MCP resource read. No dups in warga.
7. **MCP-native**: Register as resources in FastMCP server (prompts/resources/skills). Use `resources/list` + `resources/read`. Expose in llms.txt / manifest.
8. **Discoverability**: organ registry_status + central resource map. Capability tags.
9. **Version + hash**: every resource has version + sha. Staleness policy fail_closed for canon.
10. **Blast + floors**: declare in meta (like WELL does). F2/F11/F13 heavy for kernel/state.

---

## 4. Current State (Audit 2026-06-30)

**Strengths:**
- WELL: full explicit resources + bridges. Model to copy.
- GEOX: rich artifact/resources/ + renders + evidence URIs.
- arifOS: 32+ supporting modules + runner/arifos://identity live. llms.txt + contracts good public.
- AAA: agent cards + A2A + zen + registry = excellent state resources. mcp_surface clear.
- APEX theory + GitHub mirrors aligned.
- federation-p1 canonical_resources.py + 14 families good seed.
- Health all organs live. Registry truth verified via A-FORGE.

**Gaps (zen work remaining):**
- Inconsistent explicit `@mcp.resource` decorators outside WELL.
- A-FORGE execution resources thin (primitives exist; expose forge://* via MCP resources).
- WEALTH lighter on resources vs tools (implement 14 families + capital-specific).
- GEOX resources/ mostly files; wire more geox:// + ui:// consistently with _meta.
- arifOS kernel resources modules exist but full exposure + URI consistency to complete (more arifos://kernel/*).
- No single central resource registry (extend TOOLREGISTRY or new in AAA).
- Some duplication risk in docs vs live resources (zen fix: pointers + MCP read).
- mcp_surface.yaml should list owned **resources** per organ (currently tool-heavy).

**No major misplacements** — domains stay in domains, kernel in kernel, state in AAA, execution in A-FORGE. Bridges good.

---

## 5. Zen Actions (post skills unification)

- All warga/agents: load AGENTS.md → AAA_ZEN_INIT.md → this MCP-RESOURCES-MAP.md (or MCP resource read of same).
- Organs:
  - arifOS: complete arifos://kernel/* + runner as first-class MCP resources. Owns kernel state.
  - AAA: expose aaa://state/* + agent cards as MCP resources. Register zen_init resource. A2A as resource surface.
  - A-FORGE: add forge://execution/* resources for reality/leases/receipts. Pair with forge_chart for viz resources.
  - GEOX/WEALTH/WELL: continue + align to 14 families + specific. Add handoff/bridge resources everywhere.
- Central: update heptalogy (add this map), AAA_ZEN_INIT "Resources" section, deprecation registry for old URIs.
- Registry: use aforge__forge_registry_status + organ surface_status; add resource mode.
- GitHub: keep raw contracts, llms.txt, agent-cards, resources/ in sync as public mirrors. No drift.
- MCP compliance: prompts for inits, resources for state/canon, skills for behavior, tools for action. Apps for viz (forge_chart).
- Mubah: digital alignment of resources (edit, expose, point) auto per F13 2026-06-30. Irreversible (e.g. floor changes) → 888.

**Load order (updated heptalogy reference):**
1. AGENTS.md (global)
2. CONTEXT.md (T1)
3. AAA_ZEN_INIT.md + this MCP-RESOURCES-MAP.md + agent-card
4. Organ AGENTS + mcp_surface contracts
5. MCP: <organ>_init prompt + resources/read for canon/state (arifos:// , aaa:// , well:// etc.)
6. apex-theory skill
7. Act (A-R-I-F). Seal via arifos.

---

## 6. Next Lawful (after classify)

- Observe: aforge__forge_registry_status + forge_probe + organ surface_status (resources mode).
- Read key resources via MCP where live (well://identity first).
- Forge: implement missing @mcp.resource in A-FORGE + arifOS kernel + WEALTH.
- AAA: wire aaa://state/* resources + update A2A to serve cards as resources.
- Seal map in VAULT999 after verification.
- Update per-organ mcp_surface.yaml to declare resources owned.

**Verification receipt template:**
- All 6 organs expose expected URIs.
- No dup content (pointers + hashes match central).
- Agents bootstrap references this map.
- GitHub mirrors match local SOT.

*DITEMPA BUKAN DIBERI — Resources are state, not action. Placed by layer. Zenned under AAA.*

---

**Related files (load these):**
- /root/AAA/agents/AAA_ZEN_INIT.md
- /root/AGENTS.md (heptalogy §0)
- /root/AAA/agents/888-APEX/APEX_THEORY_AND_FEDERATION.md
- federation-p1/resources/canonical_resources.py
- Per-organ: contracts/mcp_surface.yaml + *_mcp/resources/ + llms.txt
- GitHub public: raw llms.txt, contracts, agent cards, README (Δ)

## 7. Audit 2026-06-30 (Grok Build / arif-governed-autonomous-execution)

**Probe (T1):** aforge__forge_probe → all organs ALIVE (arifos:20ms, geox:17, wealth:3, well:3, aforge:2). forge_registry_status: SEAL + VERIFIED. forge_health: healthy.

**Static surfaces scanned:**
- llms.txt / llms.json + contracts/mcp_surface.yaml + static/agent-card.json + .well-known/ present across organs + AAA central cards (organs/ + warga incl. grok-build).
- resources/ dirs: WELL (18 py explicit @mcp.resource + bridges), arifOS/arifosmcp/resources (32+ py: identity, reality_state, resources_index, doctrine etc + add_resource), WEALTH/wealth_mcp/resources (14-family data + server _register), GEOX/resources (79 data + src/geox_mcp/resources register 17+ geox:// + tree777://), A-FORGE (TS server.resource in interfaces/mcp/).

**Code transport:**
- Decorators/registers wired: WELL exemplar full (well://identity etc), GEOX register_resources (geox:// + tree777), WEALTH _register_resources (wealth:// 14 SOT+dynamic with meta), arifOS (register_* + TextResource + arifos://* in modules + resources/index + reality/state), A-FORGE partial (forge://governance/* + vault + now extended execution/*).
- A2A/AAA: agent-cards + .well-known as state resources (L3).
- mcp_surface.yaml updated (this session): owned_resources declared per layer. Dates 2026-06-30.
- A-FORGE resources.ts extended with execution/leases, reality/snapshot, receipts, manifests, forge_work/pointers.

**Gaps closed this pass:** A-FORGE execution resources + all mcp_surface resources_owned. No major misplacements (kernel→arifOS, state→AAA, exec→A-FORGE, L1 domains). Bridges (WELL style) present.

**Remaining noted:** Central resource registry (future), full arifOS main server load audit (modules present), explicit some ui:// in GEOX. Git mirrors F11 Mubah.

**Live MCP transport:** resources/list + read via organ endpoints (arifos:// etc). Agents: post zen → resources/read key (well://identity, arifos://identity, aaa://state/*).

AAA state now includes haram_enforcement (aaa://state/haram_map equivalent via contracts/haram_enforcement_map.yaml + a2a-server/agent-state/haram_enforcement.json). All F9/F13/F5 etc. behaviors, actions, outputs mapped for enforcement.

**Verification:** Heptalogy + MAP + ZEN point here. Registry truth via aforge. All agentic canon/state (identity, floors, doctrine pointers, bridges, reality, receipts) addressable as MCP resources.

**SEAL receipt (2026-06-30):** reality_loop started+advanced (rl-f45249ad...) + metrics. Map + mcp_surfaces + A-FORGE resources updated. Agentic intelligence (identity, state, execution receipts, bridges, 14-family, kernel/*) now explicitly MCP-addressable + declared. F11 audit in map. All via direct fs + aforge probe. No irreversible. Git mirrors Mubah.

F13 SOVEREIGN DIRECTIVE 3 (this session): HARAMKAN "I don't have that tool" / "not my tool".

**"make sure my agents cannot say no without even trying" — ENFORCED:**
- arif-governed-autonomous-execution/SKILL.md: Mandatory DISCOVERY block + prefix rule before any negative. search_tool + fs scan REQUIRED. Forbidden to endpoint on gap without attempt.
- 000-init-intent-classify prompt + SKILL.md: discovery_performed + surfaces_scanned + attempted_calls now mandatory in return. Anti-pattern added.
- AAA_ZEN_INIT: F13 Capability Rights note added under Mubah.
- Demo (this turn): search_tool on aforge returned shell/fs/probe + prior browser tools. grok_com_github fs cache has 95 tools (create_file, PRs, search, actions, web_search etc). Agents now structurally cannot refuse without documented try.

Receipts: multiple skill edits + MAP. All agents under AAA now prevented from lazy "no". Jalan terus.

Forged 2026-06-30 under Mubah + RSI alignment. Jalan terus.