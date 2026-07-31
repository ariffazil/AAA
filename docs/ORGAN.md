# arifOS Federation — Canonical System Map

> **Status:** CANONICAL SYSTEM MAP (stabilized 2026-07-30)  
> **Authority:** F13 SOVEREIGN — Muhammad Arif bin Fazil  
> **Machine twin:** `/root/AAA/federation/organs.yaml`  
> **Truth rule:** live `:port/health` beats this file. This file beats every other diagram.  
> **Doctrine:** DITEMPA BUKAN DIBERI  
> **Supersedes (topology claims only):** `FEDERATION_MAP.md`, `ARCHITECTURE_TRUTH.md`,  
> `docs/AGENTS-organs-v2026-07-28.md` organ tables, ad-hoc forge_work maps, I-ARIF merge diagrams.

---

## 0. Three-second answer

| Question | Answer |
|----------|--------|
| **Where am I?** | arifOS Federation on af-forge VPS — one sovereign, one kernel, many organs |
| **Why care?** | One map. No parallel SOTs. Probe before act. |
| **What next?** | Read §1 anatomy → §2 live spine → §6 authority chain → act only inside your organ’s ceiling |

**Dual SOT (do not invent a third):**

| Form | Path | Use |
|------|------|-----|
| Human | **this file** (`AAA/docs/ORGAN.md`) | Topology, boundaries, links |
| Machine | `AAA/federation/organs.yaml` | Ports, roles, ceilings, automation |

Everything else is a **pointer**, **contract**, **runbook**, or **draft** — not a competing map.

---

## 1. Anatomy (one organism)

```
                         ARIF (F13 SOVEREIGN)
                         purpose · irreversible consent
                                  │
                       ┌──────────▼──────────┐
                       │   arifOS KERNEL     │  :8088
                       │   admit · route ·   │
                       │   judge · memory law│
                       │   execution gate    │
                       └──────────┬──────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
       ┌──────▼──────┐     ┌──────▼──────┐     ┌──────▼──────┐
       │    GEOX     │     │   WEALTH    │     │    WELL     │
       │  Earth law  │     │ Capital law │     │ Vitality    │
       │    :8081    │     │   :18082    │     │   :18083    │
       └──────┬──────┘     └──────┬──────┘     └──────┬──────┘
              │                   │                   │
              └───────────────────┼───────────────────┘
                                  │ evidence only (never SEAL)
                       ┌──────────▼──────────┐
                       │  arifOS JUDGE 888   │
                       │ SEAL|HOLD|VOID|SABAR│
                       └──────────┬──────────┘
                                  │ only authorised mutation
                       ┌──────────▼──────────┐
                       │     A-FORGE         │  :7071 API · :7072 MCP
                       │ plan→dry-run→exec   │
                       │ verify→rollback     │
                       └──────────┬──────────┘
                                  │
                       ┌──────────▼──────────┐
                       │     VAULT999        │  append-only receipts
                       └─────────────────────┘

   COCKPIT          METABOLISM         EDGE (not organs)
   AAA :3001        arifFLOW :7073     Hermes · OpenCode · OpenClaw
   display/A2A      FQ · receipts      Claude · Grok · Kimi · Copilot
                    never judge/exec   → connect THROUGH kernel
```

**One-line zen:** Kernel is law. Organs are domain truth. A-FORGE is the only actuator. Models are replaceable workers. Arif is purpose.

---

## 2. Live constitutional spine (T₁ 2026-07-30)

| Class | Component | Port(s) | Unit | Live | Tools* | Owns | Never owns |
|-------|-----------|---------|------|------|--------|------|------------|
| **SOVEREIGN** | ARIF | — | human | — | — | purpose, irreversible yes | routine execution |
| **KERNEL** | arifOS | 8088 | `arifos.service` | healthy | 8 public | identity, admit, judge, memory law, seal gate | earth/capital compute, free execution |
| **EXECUTE** | A-FORGE | 7071 / 7072 | `a-forge` + `a-forge-mcp` | healthy | 124 API / 52 MCP stateless | plan, dry-run, apply, rollback | self-authorise, seal |
| **EARTH** | GEOX | 8081 | `geox-mcp.service` | healthy | 33 | earth evidence, physics claims | capital, judgment |
| **CAPITAL** | WEALTH | 18082 | `wealth-organ.service` | healthy | 14 public (9 canonical) | capital state, risk scenarios | allocation authority, earth truth |
| **VITALITY** | WELL | 18083 | `well.service` | **degraded** | 10 | readiness, dignity signal | medical diagnosis, final verdict |
| **COCKPIT** | AAA | 3001 | `aaa-a2a.service` | healthy | A2A | display, A2A route, registry home | judgment, execution |
| **METABOLISM** | arifFLOW | 7073 | `arifflow.service` | ok | — | FQ pulse, receipt metabolism | judge, execute |
| **TRUTH** | VAULT999 | path | filesystem | append-only | — | immutable receipts | reinterpretation |

\*Tool counts = live health probe. Re-probe before any SEAL-grade claim.

**Public MCP doors (edge protocol — not substrate truth):**

| Organ | Public | Local |
|-------|--------|-------|
| arifOS | `https://arifos.arif-fazil.com/mcp` | `127.0.0.1:8088` |
| A-FORGE | `https://mcp.arif-fazil.com/mcp` (canonical public door) · forge host may proxy | `127.0.0.1:7072` |
| GEOX | `https://geox.arif-fazil.com/mcp` | `127.0.0.1:8081` |
| WEALTH | `https://wealth.arif-fazil.com/mcp` | `127.0.0.1:18082` |
| WELL | `https://well.arif-fazil.com/mcp` | `127.0.0.1:18083` |
| AAA | `https://aaa.arif-fazil.com` | `127.0.0.1:3001` |

**Kernel public verbs (Holy 8):**  
`arif_init` → `arif_observe` → `arif_think` → `arif_route` → `arif_memory` → `arif_judge` → `arif_forge` → `arif_seal`

---

## 3. Linked non-organ planes (keep separate — do not promote to organ)

These run live and must appear on the map, but they are **not** constitutional organs. Promoting them creates authority chaos.

| Plane | Port | Unit | Role | Ceiling |
|-------|------|------|------|---------|
| **FED** | 7074 | `fed-router.service` | Model/route *advisor* (where to call) | ADVISORY — never judges |
| **FLAME** | 18901 | `flame-api.service` | RM0 free-loop inference for tools | ADVISORY worker — never constitutional |
| **WELL Witness** | 18084 | `well-witness.service` | Independent substrate observer for WELL | OBSERVE — never adjudicates |
| **AAA Signing** | 18900 | `aaa-signing.service` | Ed25519 F13 challenge signing | crypto helper |
| **AAA Pre-Forge** | — | `aaa-preforge.service` | pre-forge constitutional gate helper | gate helper |
| **Surface Guard** | — | `surface-guard.service` | MCP surface drift watchdog | observe/alert |
| **Hermes ASI GW** | (Tg) | `hermes-asi-gateway.service` | Telegram MIND relay | relay — never seals |
| **OpenClaw bot** | — | `openclaw-bot.service` | Telegram HANDS (777) | edge agent |
| **OpenCode bot** | — | `opencode-bot.service` | Telegram forge hands | edge agent |
| **Hermes MCP** | 18086 | process | Hermes local MCP surface | bridge |
| **APA bridges** | — | `apa-{email,calendar,github,telegram}-bridge` | External actuators under A-FORGE | execute only after lease |
| **Mini App API** | — | `miniapp-api.service` | Telegram mini-app API | UI edge |
| **arifosd** | — | `arifosd.service` | control-plane daemon (kernel companion) | kernel support |
| **NATS heartbeat** | — | `arifOS-NATS-heartbeat.service` | pulse publisher | telemetry |

**FED vs FLAME (one sentence each):**  
- **FLAME** answers cheap tool inference (RM0).  
- **FED** ranks *where* an agent should route a model call.  
Neither is an organ. Neither seals.

---

## 4. Substrate services (data plane — Docker/local)

| Service | Port | Role | Auth doctrine |
|---------|------|------|---------------|
| PostgreSQL | 5432 | durable state / future task ledger | localhost = password |
| Redis | 6379 | ephemeral / session / locks | localhost |
| Qdrant | 6333 | vector similarity (not truth) | localhost |
| FalkorDB | 6380 | graph | localhost |
| Graphiti MCP | 8000 | knowledge graph MCP | localhost |
| MinIO | 9000–9001 | object storage | localhost |
| NATS | 4222 | bus / heartbeat | localhost |
| SearXNG | 8080 | search | localhost |
| MCPJam | 6274 / 6277 | inspector / smoke host | localhost + mesh |
| Headscale | 8083 | mesh coordination | mesh |
| Caddy | 80/443 | ingress membrane | public TLS |
| Cloudflared | — | tunnel | public door |

**Rule:** Do not containerize core organs. Data plane may stay Docker.

---

## 5. Source repos ↔ runtime

| Organ | Source | Runtime | Notes |
|-------|--------|---------|-------|
| arifOS | `/root/arifOS` | `/opt/arifos/app` | deploy must keep source=built=deployed |
| A-FORGE | `/root/A-FORGE` | `/opt/a-forge/app` (when used) | API + MCP units |
| AAA | `/root/AAA` | `/opt/aaa/app` (when used) | A2A + registry home |
| GEOX | `/root/GEOX` (`/root/geox` alias) | process from source common | 33 tools |
| WEALTH | `/root/WEALTH` | process from source | compute only |
| WELL | `/root/WELL` | process from source | REFLECT_ONLY |
| HERMES | `/root/HERMES` | gateway + MCP | edge bridge |
| VAULT999 | `/root/arifOS/VAULT999` | `/root/VAULT999` → share path | never rewrite |

---

## 6. Authority chain (do not skip)

```
human intent
  → arif_init     (000 session / identity)
  → arif_observe  (111 sense)
  → arif_think    (333 reason)
  → arif_route    (444/555 domain)
  → domain organ  (GEOX | WEALTH | WELL evidence)
  → arif_judge    (888 SEAL|HOLD|VOID|SABAR)
  → arif_forge    (777 lease to A-FORGE)     [only if SEAL]
  → A-FORGE exec  (plan · dry-run · apply · verify · rollback)
  → arif_seal     (999 VAULT999 receipt)
```

**Hard boundaries:**

| Component | May | Must not |
|-----------|-----|----------|
| arifOS | judge, route, require receipts | mutate production state as engineer |
| A-FORGE | mutate after valid SEAL + lease | self-authorise, legislate floors |
| GEOX / WEALTH / WELL | emit evidence + uncertainty | seal, allocate capital, diagnose medically |
| AAA | display, A2A route | judge or execute |
| arifFLOW | metabolise FQ / receipts | judge or execute |
| VAULT999 | append | edit history |
| Agents / models | propose | grant self authority or seal |

---

## 7. Six planes (EUREKA — conceptual, not extra services)

| Plane | Owner | Role |
|-------|-------|------|
| Sovereign | ARIF | purpose, veto |
| Governance | arifOS | floors, admit, judge |
| Intelligence | GEOX · WEALTH · WELL · agents | evidence / reasoning |
| Execution | A-FORGE | controlled mutation |
| Continuity | Postgres · Redis · Qdrant · organ stores | revisable state |
| Truth | VAULT999 · OTel · metrics | immutable consequence |

Detail: `AAA/docs/EUREKA_SIX_PLANE_EXECUTION_LOOP.md` (architecture essay — not a second topology SOT).

---

## 8. What is deliberately NOT an organ / not SOT

| Name | What it is | Map status |
|------|------------|------------|
| **I-ARIF** | Product brand + optional SFT/DPO corpus (`forge_work/i-arif-prep/`) | **Not runtime.** Do not merge units into “I-ARIF Kernel.” |
| **EUREKA ZEN AGI Substrate v1** | Draft architecture (`arifOS/docs/canon/…`, DRAFT_ONLY) | Future ABI/ledger design — **not** live topology |
| **FED-ZEN blueprint** | Model router design notes | Describes FED plane only |
| **OpenClaw / OpenCode / Claude / Grok / Kimi** | Edge agents (MCP clients) | Instruments — connect through kernel |
| **APEX as separate organ** | Judgment absorbed into arifOS/AAA path | Do not re-split without F13 |
| **CONTEXT.md** | deprecated live-state file | Prefer `carry_forward.json` + live health |

---

## 9. Document authority (anti-chaos)

| Document | Authority | Allowed content |
|----------|-----------|-----------------|
| **`AAA/docs/ORGAN.md` (this)** | **Topology SOT** | Who, ports, ceilings, links |
| **`AAA/federation/organs.yaml`** | **Machine SOT** | Same facts for automation |
| `FEDERATION_CONTRACT.md` | Contract / web surface policy | Must **point** here for organ table |
| `AGENTS.md` | Agent operating doctrine | Thin organ table + pointer here |
| `MCP_FEDERATION_ZEN.md` | MCP affordance / drift ops | Tool naming, SEP notes — not organ invention |
| `AAA/docs/FEDERATION_MAP.md` | Repo-layer stack only | **No** live port SOT |
| `AAA/docs/ARCHITECTURE_TRUTH.md` | Historical A2A baseline | Superseded for topology counts |
| `RUNBOOK.md` | Restart / recovery | Ops only |
| forge_work/* maps | Receipts / drafts | Evidence, never SOT |

**Rule:** If two docs disagree on ports/roles, **ORGAN.md + live health** win. Then fix the other doc to a pointer — do not write a third map.

---

## 10. Stabilization checklist (how to keep this clean)

1. **New service?** Classify: CORE organ · METABOLISM · EDGE · SUPPORT · MEMORY. Update **yaml first**, then this file.  
2. **New diagram?** Must link here or be labeled DRAFT.  
3. **Tool count claims?** Always from live `/health` — never copy stale numbers across docs.  
4. **Do not** merge supporting planes into organs to “simplify names.”  
5. **Do not** call the system AGI; call it a **governed substrate**.  
6. **Probe script:**  
   `for p in 8088 7071 7072 7073 3001 8081 18082 18083; do curl -sf http://127.0.0.1:$p/health >/dev/null && echo OK $p || echo FAIL $p; done`

---

## 11. Known live debt (honest, not hidden)

| Item | State | Owner path |
|------|-------|------------|
| WELL status | degraded (92 days stale) | WELL + readiness |
| arifOS deploy source≠built marker | drift fields still fire | arifOS deploy discipline |
| WEALTH tool name/mode drift | intermittent smoke fails | WEALTH manifest |
| MCP Apps content-valid (GEOX) | RETAK (3 violations) | GEOX MCP Apps |
| FED :7074 | unit present; treat as advisory plane | FED only |
| Shared Federation ABI | not yet implemented | EUREKA ZEN draft — future |

### 11.1 Federation Edge Propagation (P0 resolved 2026-07-31)

Session/identity propagation debt partially resolved. Three forward edges
now carry SCT across organ boundaries:

| Edge | State | Method |
|------|-------|--------|
| arifOS→GEOX | **SESSION_LINKED** | Bridge probe (arif_route → geox_surface_status) |
| arifOS→WEALTH | **SESSION_LINKED** | Bridge probe (arif_route → capital_health) |
| arifOS→WELL | **SESSION_LINKED** | Bridge probe (arif_route → well_registry_status) |
| arifOS→A-FORGE | TRANSPORT_ONLY | Direct MCP tools/list (stateless transport — architectural constraint) |
| arifOS→AAA | TRANSPORT_ONLY | Direct /health (A2A control plane — no MCP surface) |
| All 6 return edges | TRANSPORT_ONLY | Not probed (F2 honesty — no cosmetic promotion) |

#### Architectural Constraints (by design, not defect)

**A-FORGE** — Stateless MCP transport. No session binding (explicit
`forge_agent` registration, no MCP session ID in response headers).
Direct probe verifies tool surface (131 tools) and server identity
(`A-FORGE-MCP v0.1.0`). Cannot achieve SESSION_LINKED without
adopting session-bound MCP or implementing SCT acceptance in the
forge agent registration flow.

**AAA** — A2A control plane on port 3001. No MCP endpoint. Direct
probe verifies `/health` + identity hash. Cannot achieve
SESSION_LINKED without exposing an MCP surface or implementing an
A2A-bridge probe that carries session context.

**Return edges** (organ→arifOS) — Transport verified (TCP + identity
match). No bridge probe configured. The forward path proves the
governance chain works; return edges are telemetry, not governance.
Per F2 (Truth): these edges are TRANSPORT_ONLY and will NOT be
cosmetically promoted. They stay honest until return-path probes
are engineered.

---

*Stabilized 2026-07-30 from live probes + SOT consolidation.  
Canonical path: `/root/AAA/docs/ORGAN.md` · Machine twin: `/root/AAA/federation/organs.yaml`*

**DITEMPA BUKAN DIBERI**
