# Federated Domain Structure · ZEN · v2026.07.15

> **Contrast three repo architectures · Zen one shared skeleton · Flow as federated intelligence**  
> **Repos:** GEOX (`/root/GEOX`) · WEALTH (`/root/WEALTH`) · WELL (`/root/WELL`)  
> **Sibling:** [`ARIFOS_MCP_ARCHITECTURE_v2026.07.15.md`](./ARIFOS_MCP_ARCHITECTURE_v2026.07.15.md)  
> **Truth:** Live tree + `tools/list` · **DITEMPA BUKAN DIBERI**

---

## 0. One picture — three bodies, one nervous system

```
                         ARIF (F13)  ·  consciousness / veto
                                   │
                         arifOS :8088  ·  LAW / route / SEAL
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
              ▼                    ▼                    ▼
     ┌────────────────┐  ┌────────────────┐  ┌────────────────┐
     │ GEOX  :8081    │  │ WEALTH :18082  │  │ WELL  :18083   │
     │ NATURAL_LAW    │  │ CAPITAL_LAW    │  │ SUBSTRATE_LAW  │
     │ EARTH body     │  │ CAPITAL body   │  │ VITALITY body  │
     │ 15 tools       │  │ 12 tools       │  │ 27 tools       │
     └───────┬────────┘  └───────┬────────┘  └───────┬────────┘
             │ artifact          │ advisory          │ readiness
             └───────────────────┼───────────────────┘
                                 │
                         A-FORGE :7071  ·  HANDS after SEAL
                                 │
                         VAULT999  ·  immutable memory
```

**Zen rule:** Same **skeleton** (MCP membrane). Different **organs** (domain core). Shared **spine** (arifOS). Never merge skeletons into one repo.

---

## 1. Structural contrast (what the trees actually are)

| Layer (zen name) | GEOX | WEALTH | WELL | Role |
|------------------|------|--------|------|------|
| **Mass** | Heaviest (~900 py · ~900 md · apps/gui) | Medium (~240 py · domains + monolith) | Lightest (~90 py · monoreflect) | Entropy pressure |
| **MCP package** | `src/geox_mcp/` | `wealth_mcp/` + `mcp/` + `internal/monolith.py` | `well_mcp/` + root `server.py` | Transport face |
| **Domain core** | `src/geox_core/` · `core/` · `geox/` | `wealth_core/` · `internal/` · `domains/` · `canon/` | `engines/` · `gate/` · `sensors/` | Law of truth compute |
| **Contracts** | `contracts/` (openapi, schemas, tools) | `contracts/` · `wealth_contracts/` | `contracts/` · `specs/` · `envelopes/` | Schema boundary |
| **Adapters / bridges** | `adapters/wealth_bridge.py` | `wealth_arifos_bridge/` · `wealth_compat/` | `adapters/` · `well_mcp/resources/bridge_*` | Federation edges |
| **Apps / UI** | `apps/` · `geox-gui/` · MCP Apps | `apps/` · capital judge | readiness panel (light) | Human surface |
| **Canon / GENESIS** | `GENESIS/` | `GENESIS/` · `canon/` | `GENESIS/` | Doctrine |
| **Boundary** | `BOUNDARY.md` | `BOUNDARY.md` | `BOUNDARY.md` | Owns / refuses |
| **Agent card** | `.well-known/` | `.well-known/agent.json` | `.well-known/` + `identity.toml` | A2A discovery |
| **Tests** | large suite | pytest + node | boundary + metabolic | Conformance |
| **Vault local** | `999_vault/` (side / organ) | via arifOS | via arifOS | Not constitutional head |

### Character of each tree

| Organ | Architectural character | Risk if ungoverned |
|-------|-------------------------|---------------------|
| **GEOX** | **World-model factory** — multi-surface (MCP + GUI + Apps + physics cores + vision). High fan-out. | Docs/apps outrun public ZEN-15; dual cores (`core/` vs `src/geox_core/`) |
| **WEALTH** | **Math kernel + federated domains** — primitives in `wealth_core`, surface via FastMCP, legacy `internal/monolith`. | Monolith vs package dual-path; tool count prose drift |
| **WELL** | **Mirror + gate** — sensors in, reflect engines, dignity gate, transport metabolize. Tightest MCP-shaped package (`well_mcp/{tools,resources,prompts,transport}`). | Stale state.json; score vs STALE contradiction |

---

## 2. Zen skeleton (canonical organ layout)

Every domain organ **should** map to this 9-layer membrane. Names may differ; **roles must not**.

```
<organ>/
├── BOUNDARY.md              # owns / refuses / imports / exports
├── AGENTS.md · README.md    # human + agent face
├── FEDERATION_CONTRACT.md   # peer edges (optional if BOUNDARY complete)
├── GENESIS/ or canon/       # doctrine (domain_law manifest)
├── .well-known/             # agent.json · mcp/server.json
│
├── <organ>_mcp/  OR  src/<organ>_mcp/     # MCP MEMBRANE (only public face)
│   ├── server.py | tools_wiring.py
│   ├── tools/               # tools/list surface
│   ├── resources/           # resources/list
│   ├── prompts/             # prompts/list
│   ├── transport/           # ingress · encode · egress · judge hook
│   └── contracts/           # tool schemas (optional colocated)
│
├── <domain_core>/           # DOMAIN LAW (no HTTP, no SEAL)
│   GEOX: geox_core / physics9 / 1d-4d
│   WEALTH: wealth_core / optimizers / capital math
│   WELL: engines / gate / sensors
│
├── contracts/               # ABI with federation + OpenAPI
├── adapters/                # bridges TO peers (never re-implement peer law)
├── apps/                    # optional human shells (MCP Apps / GUI)
├── tests/                   # public_surface · health · boundary · audit_link
├── data/                    # fixtures only (not prod SOT)
└── docs/                    # doctrine + runbooks (ΔS ≤ 0: archive bloat)
```

### Layer ownership (iron)

| Layer | May do | Must not do |
|-------|--------|-------------|
| **MCP membrane** | Expose tools/resources/prompts; bind session_id | Invent domain physics; SEAL law |
| **Domain core** | Pure compute under `domain_law` | Call arif_seal; move money; diagnose |
| **Contracts** | Types, envelopes, affordance | Runtime mutation |
| **Adapters** | Translate artifact_ref A → input B | Recompute peer domain as authority |
| **Apps** | Host UI via host proxy | Quiet geology/finance in browser |
| **GENESIS** | Doctrine | Runtime truth |

---

## 3. Map current trees → zen skeleton

### GEOX → zen

| Zen layer | Live path | Status |
|-----------|-----------|--------|
| Membrane | `src/geox_mcp/` (tools, resources, prompts, apps, routing, epistemic) | **Strong** — closest to full MCP package |
| Core | `src/geox_core/` + legacy `core/` + `geox/` | **Split** — zen target: one core package |
| Contracts | `contracts/` + `CANONICAL_PUBLIC_SURFACE.json` | Strong |
| Adapters | `adapters/wealth_bridge.py` | Present — public wealth tools deregistered; keep adapter-only |
| Apps | `apps/` + `geox-gui/` | Rich — must stay host-proxied |
| Surface SOT | registry · tools.json · surface_status | ZEN-15 public |

### WEALTH → zen

| Zen layer | Live path | Status |
|-----------|-----------|--------|
| Membrane | `wealth_mcp/` · `mcp/server.py` · FastMCP on :18082 | **Dual entry** — pick one canonical entry |
| Core | `wealth_core/` (capital, optimizers, game, institutional) | Strong modular intent |
| Monolith shadow | `internal/monolith.py` | **Entropy** — should shrink toward `wealth_core` + thin membrane |
| Contracts | `contracts/` · `wealth_contracts/` · `canon/` | Strong doctrine |
| Adapters | `wealth_arifos_bridge/` · `wealth_compat/` | Kernel bridge present |
| Domains | `domains/` · `internal/domains/` | Federated capital domains |

### WELL → zen

| Zen layer | Live path | Status |
|-----------|-----------|--------|
| Membrane | `well_mcp/{tools,resources,prompts,transport}` + root `server.py` | **Cleanest MCP shape** |
| Core | `engines/` · `gate/` · `sensors/` | Clear reflect path |
| Contracts | `contracts/` · `specs/` · `envelopes/` | Strong for small organ |
| Adapters | `adapters/` · `resources/bridge_{arifos,geox,wealth}.py` | Federation-aware |
| Apps | minimal | Correct for REFLECT_ONLY |

---

## 4. Federated intelligence flow (how structure connects)

### 4.1 Data / evidence flow (not authority flow)

```
 Earth sensors (LAS/SEGY) ──► GEOX core ──► epistemic envelope
                                              │
                                              │ artifact_ref / STOIP feed
                                              ▼
 Market / cashflow inputs ──► WEALTH core ──► advisory envelope
                                              │
 Human inject / biometrics ──► WELL sensors ──► readiness envelope
                                              │
                    all three ──► arifOS judge ──► SEAL? ──► A-FORGE ──► VAULT999
```

### 4.2 Directory-level handoff (code edges)

| Edge | GEOX path | WEALTH path | WELL path |
|------|-----------|-------------|-----------|
| GEOX → WEALTH | `adapters/wealth_bridge.py` · (deregistered MCP tools stay internal) | consume feed in `wealth_core` / capital primitive | — |
| WELL → WEALTH | — | personal finance / runway | `well_handoff_livelihood_to_wealth` · `bridge_wealth.py` |
| WELL → arifOS | — | — | `handoff_dignity_to_arifos` · `bridge_arifos_kernel.py` |
| WEALTH → arifOS | — | `wealth_arifos_bridge/` · judge handoff tools | — |
| GEOX → arifOS | judgment-lane tools via kernel bridge | — | — |
| Any → A-FORGE | never direct mutate | never | never |

### 4.3 Shared federation files (must stay aligned)

| File | Purpose | GEOX | WEALTH | WELL |
|------|---------|------|--------|------|
| `BOUNDARY.md` | Owns / refuses | ✓ | ✓ | ✓ |
| `AGENTS.md` | Agent boot | ✓ | ✓ | ✓ |
| `llms.txt` | LLM entry | ✓ | ✓ | ✓ |
| `.well-known/agent.json` | A2A card | partial | ✓ | ✓ |
| `FEDERATION_CONTRACT.md` | Peer edges | ✓ | ✓ | **add if missing** |
| `GENESIS/` + domain_law | Law anchor | ✓ | ✓ | ✓ |
| `tests/test_*boundary*` | Non-collapse | suite | suite | ✓ reflect_only |

---

## 5. Contrast matrix — structure as intelligence type

| Structural signature | GEOX | WEALTH | WELL |
|----------------------|------|--------|------|
| **Intelligence type** | Earth world-model | Capital deductive + abductive | Substrate mirror |
| **Dominant folder metaphor** | Lab + observatory + apps | Ledger + optimizers + domains | Clinic mirror + gate |
| **MCP maturity** | Full membrane + GUI | Multi-entry membrane | Cleanest 4-folder MCP |
| **Core purity** | Physics9 constrained | Golden-tested primitives | REFLECT_ONLY gate |
| **Fan-out risk** | Docs + apps explosion | Monolith + dual servers | Stale biometric SOT |
| **Bridge risk** | wealth_bridge re-implements capital | A-FORGE wealth proxy | handoff without session_id |
| **Zen pressure** | Collapse dual cores · archive docs | Thin monolith · one MCP entry | Score honesty on STALE |

---

## 6. Zen target — connected federated layout (target state)

Not a monorepo merge. **Three repos, isomorphic layers, typed edges.**

```
                    ┌────────── arifOS ──────────┐
                    │  session · route · judge    │
                    └────────────┬───────────────┘
           sct_v1 session_id shared across edges
                    │
     ┌──────────────┼──────────────┐
     ▼              ▼              ▼
  geox_mcp       wealth_mcp      well_mcp
  tools/         tools/          tools/
  resources/     resources/      resources/
  prompts/       prompts/        prompts/
     │              │              │
  geox_core      wealth_core     well engines/gate/sensors
  NATURAL_LAW    CAPITAL_LAW     SUBSTRATE_LAW
     │              │              │
     └── adapters ──┴── adapters ──┘
              artifact_ref + envelope only
```

### Convergence rules (ΔS ≤ 0)

1. **One public MCP entry per organ** (no dual server paths without deprecation date).  
2. **One domain core package** (GEOX: merge `core/` into `src/geox_core/`).  
3. **Adapters only at edges** — no capital math in GEOX public tools; no geology in WEALTH.  
4. **Shared envelope fields:** `domain_law`, `session_id`, `actor_id`, `trace_id`, `epistemic_tag`, `execution_authorized=false`, `human_final_authority=Arif`.  
5. **Session propagates** on all handoffs (fix WELL→WEALTH SESSION_REQUIRED crack).  
6. **Docs:** archive bloat under `docs/archive/`; README points to architecture seal.  
7. **Tests:** each organ ships `test_public_surface`, `test_health`, `test_boundary`, `test_audit_link` (FTC-1).

---

## 7. Flow recipe — agent walks the structure

```
000  arif_init → session_id
444  arif_route → organ plan [GEOX?, WEALTH?, WELL?]  # multi-organ preferred
     │
     ├─ GEOX:  geox_mcp tools → geox_core → OBS/DER/INT envelope
     ├─ WEALTH: wealth_mcp tools → wealth_core → advisory envelope
     └─ WELL:  well_mcp tools → gate/engines → readiness envelope
     │
888  arif_judge(compose envelopes) → SEAL|HOLD|VOID
777  arif_forge / A-FORGE only if SEAL
999  arif_seal → VAULT999
```

**Structural meaning of the recipe:**  
Membrane tools never skip core law. Core never skips kernel. Kernel never skips F13 on irreversible.

---

## 8. Entropy report (structure red team)

| Finding | Organ | Severity | Zen fix |
|---------|-------|----------|---------|
| Dual physics cores (`core/` vs `src/geox_core/`) | GEOX | P1 | Single import path |
| Dual MCP entries (mcp/ vs wealth_mcp vs monolith) | WEALTH | P1 | One `server` console entry |
| `internal/monolith.py` gravity well | WEALTH | P1 | Extract modes → wealth_core |
| Docs volume ≈ code volume | GEOX | P2 | archive + llms.txt index |
| Score 100 + STALE | WELL | P0 (runtime) | null score on expired |
| wealth_bridge inside GEOX | GEOX | P1 | adapter-only, no public capital verdict |
| Missing FEDERATION_CONTRACT on WELL | WELL | **DONE 2026-07-15** | `WELL/FEDERATION_CONTRACT.md` |
| WEALTH dual MCP entry | WEALTH | **DONE notice 2026-07-15** | `ENTRYPOINTS.md` · `server.py` redirects · package.json → federated |
| GEOX dual cores | GEOX | **MAPPED 2026-07-15** | `GEOX/CORE_IMPORT_MAP.md` — canonical `geox_core` |
| session_id not shared on handoff | ALL | P1 | envelope middleware (open) |

---

## 9. Minimal structural checklist (per organ PR)

- [ ] `BOUNDARY.md` matches live refuses  
- [ ] Public tools = `tools/list` only  
- [ ] MCP package has tools + resources + prompts  
- [ ] Domain core has zero HTTP  
- [ ] Adapters do not re-own peer law  
- [ ] `.well-known/agent.json` present  
- [ ] `domain_law` on /health  
- [ ] Handoff tests with session_id  
- [ ] No new top-level folder without zen mapping  

---

## 10. Seal

| Item | Value |
|------|--------|
| **Document** | Federated Domain Structure ZEN v2026.07.15 |
| **Claim** | Three repos are orthogonal **bodies** under one **law spine**; isomorphic MCP membranes enable federated flow |
| **Not claimed** | Trees already fully zen; dual-entry debt gone |
| **Next engineering** | P0 WELL score honesty · P1 session on handoffs · P1 one MCP entry WEALTH · P1 GEOX core unify |

**DITEMPA BUKAN DIBERI — structure is federation, not decoration.**

*Contrast by design. Flow by envelope. Connect by adapter. Govern by arifOS. Seal by 999.*
