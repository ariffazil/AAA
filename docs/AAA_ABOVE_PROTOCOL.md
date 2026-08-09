# AAA above protocol — constitutional surface, not vendor lock-in

> **SEAL (doctrine):** 2026-08-09 · F13-aligned · DITEMPA BUKAN DIBERI  
> **One sentence:** Do not make AAA another protocol. Make AAA a **canonical federation state** that **any** protocol can project.  
> **Companion:** `STATE.md` · `AAA_STATE_PROTOCOL_AUDIT.md` · `IDENTITY_NAMING_REGISTRY.md`

---

## 0. The real question

Not: *"How does AAA follow MCP/A2A?"*  
But: *"How is AAA a constitutional reference point without becoming vendor lock-in?"*

```
                AAA STATE  (federation surface · directory · telephone · readiness)
                    |
     +--------------+--------------+
     |              |              |
    MCP            A2A          Future-X
     |              |              |
     +--------------+--------------+
                    |
                 Runtime
```

- **MCP** = tool/transport protocol (AI ↔ tools)  
- **A2A** = agent communication protocol (agent ↔ agent)  
- **AAA State** = federation control-plane state (who/where/how/ready)  
- **arifOS** = law + judge + seal (WHO DECIDES) — not replaced by AAA  

**AAA does not force the world to speak AAA.**  
AAA **exposes** itself through standard protocols.

---

## 1. Iron separation (never mix)

| Concern | Owner | Protocol role |
|---------|--------|---------------|
| Floors / verdict / seal | **arifOS** | MCP tools `arif_*` |
| Execution after gate | **A-FORGE** | MCP tools `forge_*` |
| Domain compute | GEOX / WEALTH / WELL | MCP |
| Federation catalog / A2A gateway / STATE_READY | **AAA** | A2A card + adapters |
| Immutable receipt | **VAULT999** | append-only |

**DISPLAY_ONLY** on `:3001` remains: AAA **projects** state and **routes** tasks; it does **not** adjudicate or seal.

```
Protocol PASS  ≠  Governance PASS
MCP can carry "drop table" perfectly and still be VOID under F1–F13.
```

```
MCP / A2A  =  jalan raya
AAA        =  peta + pejabat kawalan trafik (surface constitution of the federation)
888        =  hakim (arifOS)
VAULT      =  arkib
```

---

## 2. Four layers of AAA vNext (locked shape)

```
L1  Canonical State     federation surface truth (cards, CALL_MAP, STATE_READY, ceilings)
L2  Constitutional API  stable verbs/read models AAA owns (read-mostly)
L3  Protocol Adapters   MCP consumer · A2A server · REST · Future-X
L4  External Agents     peers that only know MCP or A2A or REST or nothing
```

### L1 — Canonical state (native)

AAA-native shapes (examples — not full schema):

```json
{
  "state": "STATE_READY",
  "ceiling": "DISPLAY_ONLY",
  "deployment_drift": false,
  "catalog": { "identity": 4, "harness": 14, "binding": 20 },
  "organs": { "8088": "up", "7072": "up" },
  "telephone": "CALL_MAP",
  "authority_note": "verdicts live in arifOS; AAA only displays and routes"
}
```

When a **judgment** is involved, canonical **verdict** fields remain arifOS-native:

```json
{
  "verdict": "HOLD",
  "authority": "888",
  "confidence": 0.42,
  "receipt": "…"
}
```

AAA may **mirror/display** them; arifOS remains **source for seal**.

### L2 — Constitutional API

Stable, versioned surfaces AAA owns:

| Surface | Purpose |
|---------|---------|
| `GET /health` | readiness + drift + vault link |
| Agent card registry | 3-layer directory |
| CALL_MAP | telephone |
| A2A task routing | mesh dispatch **without** self-seal |
| Session init/seal **proxy** | path to arifOS, not replacement |

### L3 — Protocol adapters (translate, don’t redefine)

| Adapter | Direction | Example mapping |
|---------|-----------|-----------------|
| **MCP** | external ↔ organs via federation | Tool result `status` + `metadata.aaa_*` / membrane |
| **A2A** | peer agents ↔ AAA gateway | `taskState: input-required` ↔ HOLD / auth-required |
| **REST** | legacy / simple clients | `/health`, card JSON |
| **Future-X** | tomorrow’s protocol | new adapter only |

**Mapping rule:** Adapter fields are **lossy projections** of L1. L1 does not become MCP-shaped or A2A-shaped as its storage.

### L4 — External / wild agents

```
Random Agent  →  AAA Gateway (translator)  →  AAA State  →  organs / arifOS as needed
```

- Do **not** force random agents to become AAA-native.  
- Gateway translates. EMD / ACT / ceilings still apply.  
- No MCP, no A2A → still REST health + card; mutations require ACT path.

---

## 3. Adapter examples (illustrative)

### MCP projection

```json
{
  "content": [{ "type": "text", "text": "…" }],
  "isError": false,
  "metadata": {
    "aaa_state": "STATE_READY",
    "aaa_ceiling": "DISPLAY_ONLY",
    "arifos_verdict": "HOLD"
  }
}
```

### A2A projection

```json
{
  "taskState": "input-required",
  "metadata": {
    "authority": "888",
    "aaa_route": "arifos",
    "ceiling": "DISPLAY_ONLY"
  }
}
```

Governance may still **VOID** the action even when A2A taskState is valid.

---

## 4. Survival test (anti lock-in)

| Event | Result |
|-------|--------|
| MCP dies / is replaced | AAA state lives; write new MCP adapter |
| A2A replaced by XYZ | AAA state lives; write XYZ adapter |
| Vendor harness changes | FI cards + CALL_MAP update; state machine unchanged |
| Single VPS monolith | CLI least-power; adapters idle but state remains |

**AAA is source of truth for federation *surface state*.**  
**arifOS is source of truth for *constitutional verdicts and seals*.**  
**VAULT999 is source of truth for *immutable receipts*.**

Three books, three owners — not three competing protocols.

---

## 5. What AAA must never do

| Forbidden | Why |
|-----------|-----|
| Invent “AAA Protocol” as wire standard for the world | Vendor lock-in |
| Replace arifOS judge with gateway logic | Ceiling breach |
| Store federation truth only as A2A Task blobs | Protocol death = state death |
| Force external agents to implement F1–F13 natively | Use adapter + gates |
| Skip ACT/EMD because “we own everything” | Multi-process still needs contract |

---

## 6. Relation to prior docs

| Doc | Role after this SEAL |
|-----|----------------------|
| `STATE.md` | Seven pillars + institution before citizens |
| `AAA_STATE_PROTOCOL_AUDIT.md` | Live MCP/A2A compliance matrix |
| **This file** | Architecture: AAA **above** protocol |
| `IDENTITY_NAMING_REGISTRY.md` | Names (ACT, agentId) independent of SPIFFE/AIMS |
| `CALL_MAP.md` | Telephone — one adapter path among several |

---

## 7. Implementation posture (next, not now-all)

| Priority | Work | Tier |
|----------|------|------|
| Done | Doctrine SEAL (this doc) | T1 docs |
| Next | Keep L1 fields stable in `/health` + registry + STATE_READY | T1 |
| Next | Document adapter mapping table in CALL_MAP | T1 |
| Later | Explicit `adapters/` module (MCP/A2A/REST mappers) if code sprawl | T2 |
| Hold | New PEER protocol organ | T3 |

---

## 8. SEAL formula

> **Jangan jadikan AAA satu lagi protocol.**  
> **Jadikan AAA sumber kebenaran surface federasi yang boleh diterjemahkan kepada mana-mana protocol.**  
> **Protocol = jalan. AAA = peta kawalan. arifOS = undang-undang + hakim.**

```
Protocol PASS  +  Governance SEAL  =  may act
Protocol PASS  +  Governance VOID  =  must not act
Protocol FAIL  +  anything         =  no road
```

DITEMPA BUKAN DIBERI.
