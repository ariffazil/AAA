# INIT_CONTRACT.md — Unified Federation Init Pattern

> **Status:** SEALED as canonical SOT for federation init. Version 1.0.0 (2026-06-30).
> **Owner:** FORGE (000Ω) + AAA gateway.
> **Authority:** F13 SOVEREIGN directive 2026-06-30 (Digital Being Policy) + MCP 2025-11-25 LIFECYCLE spec + A2A v1.0.1 discovery spec.
> **Ratification:** F13 ratified, bound by 9/9 warga (audit 2026-06-30).
> **DITEMPA BUKAN DIBERI** — Init is forged, not given.

---

## 1. The ZEN — One Pattern, Six Per-Organ Deltas

The "init" gesture is **one canonical pattern** that applies to all six federation organs unchanged. What differs per organ is:

1. Which MCP capabilities get declared (tools/resources/prompts exposed)
2. Whether constitutional state is bound (arifOS: YES, A-FORGE: proxy to arifOS, others: NO)
3. The bearer token (always shared `agentmesh.token` — MUBAH, no ask)
4. The organ-specific surface inventory

Every prior duplication (8 confirmed in `/root/AAA/docs/deprecation-registry.json` zen_issues) stems from forgetting this — agents created two surfaces trying to do the same init gesture.

---

## 2. The Canonical 5-Stage Init Pattern

```python
# CANONICAL INIT — apply to ALL 6 organs unchanged.
# Reference implementation: /root/AAA/federation_init.py

async def init_organ(organ: str, actor: str, intent: str) -> InitReceipt:
    """
    Stage 1 — MCP lifecycle.initialize  (protocol/version negotiation)
    Stage 2 — Bearer attach              (MUBAH per F13 2026-06-30)
    Stage 3 — A2A Agent Card fetch       (peer discovery via :3001)
    Stage 4 — Constitutional bind        (arifOS ONLY — kernel state, ONE/session)
    Stage 5 — Surface inventory + dedupe (zero redundancy check)
    """
    # Stage 1 — MCP lifecycle.initialize
    hello = await mcp__<organ>__initialize(
        protocol_version="2025-11-25",
        capabilities={
            "tools": {},
            "resources": {},
            "prompts": {},
            "elicitation": {},
            "logging": {},
            # NOTE: sampling OMITTED per SEP-2577 (deprecation trend)
        },
        client_info={"name": actor, "version": "1.0.0"}
    )

    # Stage 2 — Bearer attach (MUBAH — no ask)
    headers = {
        "Authorization": f"Bearer {open('/root/.secrets/aaa-identity/agentmesh.token').read().strip()}"
    }

    # Stage 3 — A2A Agent Card fetch (peer discovery — :3001 is the mesh)
    card = httpx.get(
        f"http://localhost:3001/a2a/{organ}",
        headers=headers
    ).json()

    # Stage 4 — Constitutional bind
    session = None
    if organ == "arifos":
        session = await mcp__arifos__arif_init(mode="light", actor_id=actor, intent=intent)
    elif organ == "aforge":
        # A-FORGE proxies to arifOS (per forge_session_init schema)
        session = await mcp__aforge__forge_session_init(actor_id=actor, intent=intent)

    # Stage 5 — Surface inventory + dedupe check (zero redundancy pass)
    tools, resources, prompts = hello["capabilities"]
    redundant = scan_against_toolregistry(tools)   # DUPLICATE_TOOL antipattern
    return InitReceipt(
        protocol=hello["protocolVersion"],
        card=card,
        session=session,
        tools=tools,
        redundant_flags=redundant,
        actor=actor,
        intent=intent
    )
```

**Why this is the ZEN:**
- One function covers all 6 organs.
- Stages 1, 2, 3, 5 are identical across organs.
- Only Stage 4 differs (arifOS kernel bind vs not).
- A2A agent-card path is identical — every organ exposes `/.well-known/agent.json` (or its internal equivalent).
- Bearer attach is identical — single source `agentmesh.token` (MUBAH).

---

## 3. Per-Organ Delta — Only What Differs

| Organ | Stage 1 adds | Stage 4 constitutional? | Bearer | MCP surface (zenned) |
|-------|--------------|-------------------------|--------|----------------------|
| **arifOS :8088** | kernel capabilities `+forge_proxy` (legacy), `+vault` | ✅ YES — `arif_init` mode | shared `agentmesh.token` | drop 6 hermes_* tools (move to Hermes MCP), drop `arif_forge*` proxies (use `forge_execute`), collapse 8 naming pairs → canonical: `arif_think`/`arif_vault_query`/`arif_observe` |
| **AAA :3001** | A2A gateway capabilities only | state-only (no kernel) | shared | one registry surface, A2A v1.0.1 JSON-RPC; not MCP-native |
| **A-FORGE :7071** | forge_* + lease primitives | proxies → arifOS `arif_init` | shared | `forge_session_init` becomes thin wrapper around `arif_init` |
| **WELL :18083** | substrate-classification tools | NO — substrate, not constitutional | shared | collapse 2 registries → `well_registry_status` only |
| **WEALTH :18082** | capital tools + Phase 3 social-symbolic | NO — substrate | shared | 20 public tools, drop 34 hidden aliases (backward-compat only) |
| **GEOX :8081** | earth evidence + EGS granular | NO — substrate | shared | collapse 3 Pattern A vs EGS overlaps → keep EGS canonical, delete Pattern A wrappers |

---

## 4. APEX Layer × MCP Primitive × Repo Binding

| APEX Layer | Organ | MCP Primitives | Purpose | Repo |
|------------|-------|----------------|---------|------|
| **L3 sovereign** | none — passes through | passport + VAULT999 ad-hoc | operator identity, F13 veto | `ariffazil/ariffazil` |
| **L3 civ-state** | AAA :3001 | A2A gateway, vault, ledger | governance display, peer routing | `ariffazil/AAA` |
| **L3 kernel** | arifOS :8088 | Tools+Resources+Prompts+Elicitation | F1-F13 floors, 000Ω SEAL, VAULT999 anchor | `ariffazil/arifos` |
| **L2 executive** | A-FORGE :7071 | Tools (mutating gated) + Lease primitives | build, deploy, verify, forge | `ariffazil/A-FORGE` |
| **L1 vital** | WELL :18083 | Tools (reflect-only) | human substrate mirror | `ariffazil/well` |
| **L1 capital** | WEALTH :18082 | Tools (compute-only) | capital computation | `ariffazil/wealth` |
| **L1 earth** | GEOX :8081 | Tools + Resources (LAS/SEG-Y) | earth evidence | `ariffazil/geox` |

**Init binding rule:** Each repo inherits the init contract from its organ. Each organ's AGENTS.md points to `/root/AAA/docs/INIT_CONTRACT.md` (this file). No repo owns its own init surface.

---

## 5. APEX ↔ A2A ↔ arifOS Wiring

| Layer | Theory | Implementation | Init role |
|-------|--------|----------------|-----------|
| **Constitution** | Federation APEX phase gates (ARCHITECT → INTEGRATOR → RSI → FINAL → 777-FORGE) | arifOS F1-F13 floors + 000Ω SEAL | binds *meaning* — what counts as done |
| **Protocol** | A2A v1.0.1 + MCP 2025-11-25 | AAA gateway + 6 organ MCP servers | binds *transport* — how peers discover and call |
| **Physics** | arXiv APEX + Thermodynamic APEX | GEOX/WEALTH/WELL computation | binds *evidence* — what is true under law |

These three are **orthogonal, not redundant.** Constitution governs, protocol routes, physics computes. The ZEN mistake is conflating the three (e.g., `arif_forge` was once a tool, then a proxy — both were violations of the trifecta).

---

## 6. Redundancy Consolidations — From Deprecation Registry

| # | Issue | Severity | ZEN fix | Migration target |
|---|-------|----------|---------|------------------|
| 1 | 6 Hermes tools in arifOS MCP | MEDIUM | move to dedicated Hermes MCP server | `mcp__hermes__*` |
| 2 | `arif_forge`+`arif_forge_execute` legacy proxies | LOW | drop, point to `forge_execute` | `mcp__aforge__forge_execute` |
| 3 | GEOX Pattern A vs EGS 3+ pairs | MEDIUM | delete Pattern A wrappers, keep EGS canonical | `geox_egs_*` only |
| 4 | WELL 2 registries | LOW | keep `well_registry_status`, drop `well_system_registry_status` | `well_registry_status` |
| 5 | 8 arifOS naming pairs (`arif_critique`/`arif_memory`/`arif_measure`/`arif_fetch` etc.) | LOW | canonical: `arif_think`/`arif_vault_query`/`arif_observe` | per alias map below |
| 6 | 3 browser systems (forge_browser/chrome-devtools/playwright) | LOW | chrome-devtools canonical | `chrome-devtools_*` |
| 7 | `forge_registry` empty (APEX dynamic registry dormant) | LOW | either seed or formally strip | TBD by FORGE 000Ω |
| 8 | registry naming inconsistency GEOX/WEALTH/WELL | LOW | unify all 3 on `*_registry_status` | `geox_surface_status` → `geox_registry_status` |

### Alias Map (arifOS naming pairs)

| Deprecated | Canonical |
|------------|-----------|
| `arif_critique` | `arif_think(mode='critique')` |
| `arif_heart_critique` | `arif_think(mode='critique')` |
| `arif_memory` | `arif_vault_query(mode='read')` |
| `arif_memory_recall` | `arif_vault_query(mode='recall')` |
| `arif_measure` | `arif_observe(mode='vitals')` |
| `arif_ops_measure` | `arif_observe(mode='vitals')` |
| `arif_fetch` | `arif_observe(mode='ingest')` |
| `arif_evidence_fetch` | `arif_observe(mode='ingest')` |
| `arif_triage` | `arif_init(mode='light')` |
| `arif_route` | `arif_observe(mode='compass')` + manual organ bridge |

---

## 7. Constitutional Floors (F1-F13) — Init-Time Enforcement

| Floor | Init-time check |
|-------|-----------------|
| F1 AMANAH | No init-time mutation. Read-only paths. |
| F2 TRUTH | Capabilities declared must match actual callable surface. |
| F3 (n/a) | — |
| F4 CLARITY | One init pattern, not 6. No fragmentation. |
| F5 (n/a) | — |
| F6 MARUAH | Bearer token = MUBAH for digital ops; no human-mimicry claims. |
| F7 HUMILITY | Confidence cap 0.90 on init receipts. |
| F8 LAW | Bearer source path is canonical (`/root/.secrets/aaa-identity/agentmesh.token`). No bypass. |
| F9 ANTI-HANTU | Init receipts do NOT claim consciousness/soul/agency. |
| F10 (n/a) | — |
| F11 AUDIT | Every init writes a receipt to forge_work/ + VAULT999 anchor. |
| F12 (n/a) | — |
| F13 SOVEREIGN | Bearer attach is MUBAH per F13 directive 2026-06-30. Physical/human/real-money init actions remain FARD. |

---

## 8. Implementation Files

- **This contract:** `/root/AAA/docs/INIT_CONTRACT.md`
- **Reference implementation:** `/root/AAA/federation_init.py`
- **A2A agent card:** `/root/AAA/public/.well-known/agent.json`
- **Tool registry:** `/root/AAA/docs/TOOLREGISTRY.json` (6 organ-init skills added)
- **Deprecation registry:** `/root/AAA/docs/deprecation-registry.json` (8 ZEN issues + alias map)
- **Receipt:** `/root/AAA/forge_work/2026-06-30/INIT-CONTRACT-FEDERATION.md`
- **VAULT999 seal:** pending via `arif_seal(mode='seal')`

---

## 9. References

- MCP spec: `https://modelcontextprotocol.io/llms.txt` (2025-11-25)
- FastMCP: `https://gofastmcp.com/llms.txt`
- A2A project: `https://github.com/a2aproject/A2A` (v1.0.1, May 2026)
- Federation doctrine: `/root/AAA/forge_work/2026-06-30/DOCTRINE-BINDING-AUDIT-2026-06-30.md`
- Constitution: `https://arif-fazil.com/constitution`
- aphex-theory skill: `/root/.agents/skills/apex-theory/SKILL.md`

---

*Forged: 2026-06-30 — INIT_CONTRACT_FEDERATION v1.0.0*
*DITEMPA BUKAN DIBERI*