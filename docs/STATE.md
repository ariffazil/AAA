# AAA STATE — Constitutional institution (zen SOT)

> **Forged / unified:** 2026-08-09 · F13  
> **Doctrine:** DITEMPA BUKAN DIBERI  
> **This file is the single working SOT** for AAA state doctrine.  
> Satellites below are **pointers only** — do not fork doctrine.

```
Protocol = undang-undang koordinasi.
Governance = undang-undang kebenaran.
```

That is **separation of powers**, not a layer diagram.

---

## 0. One sentence

```
STATE = territory + law + organs + power + telephone + catalog + records + control plane
CITIZEN = passport inside that state (later)
AAA = federation surface state — NOT a protocol
```

**AAA is not a protocol. AAA is constitutional federation surface state.**  
MCP/A2A are replaceable adapters. arifOS decides. VAULT999 proves.

---

## 1. Seven pillars (must all stand)

| # | Pillar | SOT | Live proof |
|---|--------|-----|------------|
| 1 Territory | Who/where | `ORGAN.md` · `organs.yaml` | Port = health |
| 2 Law | F1–F13 | arifOS `:8088` · `FLOOR_TABLE.json` | kernel health |
| 3 Government | Core organs | arifOS · A-FORGE · GEOX · WEALTH · WELL · AAA · arifFLOW | `:port/health` |
| 4 Power | WHICH model | FED `:4000` | liveliness |
| 5 Telephone | How to dial | `CALL_MAP.md` · `call_map.yaml` | file + skill |
| 6 Catalog | Who exists | 3-layer cards · registry | identity/harness/binding |
| 7 Records | Proof | VAULT999 | `vault: CONNECTED` |

**Control plane:** AAA `:3001` = **DISPLAY_ONLY** — catalog, route A2A, never judge, never seal.

---

## 2. Three books (never mix)

| Book | Question | SOT |
|------|----------|-----|
| **Directory** | Who exists? | Agent cards · 3-layer |
| **Telephone** | How call? | **CALL_MAP** |
| **Power bill** | Which LLM? | FED + harness configs |

**Identity ≠ runtime.** WHO = agentId/FI · WHICH = model seat · never conflate.

---

## 3. Constitutional stack — two flows

### 3.1 Authority flow (who rules)

```
L6 VAULT999          Can it be proven?
L5 ACT + did:web     Who may act? / Who am I?
L4 arifOS F1–F13     Should it be done?
L3 A2A               Who is talking?     (replaceable)
L2 MCP               How is work done?   (replaceable)
L1 CALL_MAP / cards  Where do I send?    (surface)
L0 STATE_READY       Is institution up?  (surface)
```

### 3.2 Dependency flow (how we assemble)

```
STATE_READY → CALL_MAP → MCP → A2A → arifOS → ACT+DID → VAULT999
```

**Authority flows down. Execution climbs. Never reverse.**

| Class | Layers |
|-------|--------|
| **Immutable** | VAULT999 · ACT+DID · arifOS F1–F13 |
| **Replaceable** | A2A · MCP |
| **Disposable** | FastMCP · SDKs · frameworks · harness CLIs |

```
MCP/A2A = jalan raya
AAA     = peta + pejabat kawalan (surface)
888     = hakim (arifOS)
VAULT   = arkib
```

```
Protocol PASS + Governance VOID = must not act
Protocol FAIL                   = no road
```

---

## 4. L5 Authority — did + ACT (not communication)

| | did:web / did:arif | ACT (`act_v1.*`) |
|--|--------------------|------------------|
| Question | Who are you? | What office / what may you do? |
| Without | “trust me bro” | Identity → Action ungoverned |
| With | cryptographic actor | Identity → capability → action |

**Live forms:** public `did:web:arif-fazil.com…` · registry `did:arif:{organ}` + Ed25519. Map both; no third scheme.

**ACT enforces offices:**

| Actor | Office |
|-------|--------|
| 333 | Propose |
| 555 | Verify |
| 888 | Judge |
| A-FORGE | Execute |
| VAULT999 | Witness |

333 SEAL attempt → **ACT DENY** even if A2A/MCP/JSON-RPC valid.

**Chain:**

```
did → ACT → F1–F13 → execute → VAULT receipt
```

**Wire:** ART `actGate` (MUTATE needs `act_v1.*`; OBSERVE exempt; IRREVERSIBLE → F13). Envelope default-deny + DISPLAY_ONLY ceiling.

---

## 5. AAA above protocol (anti lock-in)

```
         AAA STATE (L0–L1 surface)
                │
    +-----------+-----------+
    MCP        A2A       Future-X   ← adapters only
    +-----------+-----------+
                │
             Runtime
```

- Do **not** invent “AAA Protocol” as world wire standard.  
- Do **not** store law inside A2A Task blobs.  
- MCP dies → CLI least-power survives. A2A dies → same. FastMCP dies → same.  
- **F1–F13 dies → institution dies.**  

**L1–L4 AAA vNext shape:** Canonical state → Constitutional API → Protocol adapters → External agents.

---

## 6. Identity naming (locked)

| Domain | Canonical |
|--------|-----------|
| Capability token | **ACT** `act_v1.*` (retire SCT in new prose) |
| Agent id | **agentId** + did (not SPIFFE primary) |
| Citizen later | **warga_status / passport** (not VC brand) |
| Multi-hop | **ACT chain** deferred (no HDP brand) |
| Workload stack | Map to arif_init + ACT + organ keys (no SPIRE organ) |

External standards **map**. They never rename the institution.

---

## 7. Operators (no passport required yet)

| Surface | agentId / FI | Role | Model socket (WHICH) |
|---------|--------------|------|----------------------|
| OpenCode | FI-001 | Primary forge | FED `opencode` |
| Hermes ASI | FI-000 | Human bridge | FED `hermes-asi` |
| OpenClaw | *(binding, no FI)* | Gateway metabolizer | FED `openclaw` |
| AGY | FI-009 | Forge instrument | Gemini-native `gemini-3.6-flash` |
| Organs | ministries | Law/hands/earth/capital/vitality | MCP ports |

Operating ≠ passport. **State first.**

---

## 8. Probes (enforcement)

```bash
/root/AAA/scripts/state-probe.sh        # STATE_READY · §7 light gates
/root/AAA/scripts/protocol-enforce.sh   # L0–L6 full matrix → PROTOCOL_ENFORCED
```

| Exit | Meaning |
|------|---------|
| state-probe 0 | STATE_READY |
| state-probe 1/2 | DEGRADED / DOWN |
| protocol-enforce 0 | PROTOCOL_ENFORCED |
| protocol-enforce 1/2 | PROTOCOL_GAP / CRITICAL |

**Live gates:** A2A-Version required · EMD blocks anonymous · DISPLAY_ONLY · Holy 8 · ACT format · DID registry · VAULT file.

**Least power:** same VPS T1 → `opencode run` / `agy -p` / `hermes` — do not force A2A theatre.

---

## 9. Boot law (every agent)

```
1. state-probe.sh  (or this file + ports)
2. CALL_MAP.md
3. ORGAN.md
4. arif_init when mutation needs law
5. Work — then seal/receipt as required
```

---

## 10. Next (after boring green)

| Order | Work | Not |
|-------|------|-----|
| P0 | Keep STATE_READY + PROTOCOL_ENFORCED | New organs |
| P1 | External CALL_MAP draft (docs only) | Live public bridge without 888 |
| P2 | Citizen stamps (Hermes → OpenClaw → OpenCode) | While degraded |
| P3 | Optional external door | Economy/DAO/SPIRE/HDP |

**Phase E parked:** x402, IBCT, PEER, Labuan — after telephone is **used**.

---

## 11. Survival tests

| Remove | Survive? |
|--------|----------|
| MCP | ✅ CLI remains |
| A2A | ✅ CLI remains |
| FastMCP | ✅ |
| F1–F13 / arifOS | ❌ institution dies |
| ACT+DID | ❌ no trustworthy agency |
| VAULT999 | ❌ no proof |

---

## 12. Explicitly deferred

Warga stamps · multi-hop ACT · AIMS/SPIRE rename · economy rails · force-push/main deploy without T3.

---

## 13. Ops (one block)

```bash
# Prove institution
/root/AAA/scripts/state-probe.sh
/root/AAA/scripts/protocol-enforce.sh

# After AAA commit
/root/AAA/scripts/sync-deploy-marker.sh
# post-commit hook also runs this

# Registry / a2a-server code change
systemctl restart aaa-a2a.service && sleep 3
/root/AAA/scripts/state-probe.sh
```

---

## 14. Pointer index (satellites → this file)

| Former / related doc | Status |
|----------------------|--------|
| CONSTITUTIONAL_SEPARATION_AXIOM | **→ this file §3–11** |
| CONSTITUTIONAL_LAYER_SEPARATION | **→ this file** |
| AAA_ABOVE_PROTOCOL | **→ this file §5** |
| ACT_AUTHORITY_LAYER | **→ this file §4** |
| PROTOCOL_ENFORCEMENT_MATRIX | **→ this file §8** + `protocol-enforce.sh` |
| AAA_STATE_PROTOCOL_AUDIT | **→ this file §3,8** + script |
| IDENTITY_NAMING_REGISTRY | **→ this file §6** |
| AAA_NEXT_90D | **→ this file §10** |
| STATE_OPS | **→ this file §13** |

Machine twin: `federation/STATE.yaml`  
Telephone detail: `CALL_MAP.md`  
Territory detail: `ORGAN.md`

---

*Institution before passport. Protocol under governance. Ditempa, bukan diberi.*
