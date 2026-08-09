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

## 3. Three things never mixed

```text
Communication  ≠  Authority  ≠  Proof
```

| Bucket | Layers | Trap if collapsed |
|--------|--------|-------------------|
| **Communication** | A2A · MCP · CALL_MAP | Protocol becomes policy → agent anarchy |
| **Authority** | DID · ACT · arifOS F1–F13 | “Works” mistaken for “allowed” |
| **Proof** | VAULT999 | Claims without evidence |

Good governance always knows **enforced** vs **assumed**.

---

## 4. Constitutional stack (pecahan kuasa)

### 4.1 Compression

```text
DID proves identity.
ACT grants authority.
arifOS decides legitimacy.
A2A carries intent.
MCP executes tools.
VAULT999 preserves evidence.
```

| Question | Layer |
|----------|--------|
| **WHO AM I?** | DID (`did:web` / `did:arif`) |
| **WHAT MAY I DO?** | ACT (`act_v1.*`) |
| **SHOULD I DO?** | arifOS F1–F13 |
| **HOW TO TALK?** | A2A |
| **HOW TO ACT?** | MCP |
| **CAN I PROVE?** | VAULT999 |

### 4.2 Spine

```text
STATE_READY → CALL_MAP → MCP → A2A → arifOS → ACT → DID → VAULT999
```

| Step | Precise role | Class |
|------|--------------|--------|
| STATE_READY | Institution standing? | Surface |
| CALL_MAP | Where do I send *here*? | Surface |
| **MCP** | **How is work executed?** (tooling) | Replaceable |
| **A2A** | **How participants communicate** (carries DID; does not prove it) | Replaceable |
| **arifOS** | **Should it be done?** | Immutable |
| **ACT** | **What may this office do?** | Immutable |
| **DID** | **Who is speaking?** (identity verified here) | Immutable |
| **VAULT999** | **Can we prove it?** | Immutable |

**Locked refinement:** A2A ≠ “who is talking?”. **DID** answers who. A2A is the **channel**. ACT is **office**. arifOS is **judgment**.

**Authority flow:** VAULT ← ACT+DID ← arifOS ← A2A ← MCP ← CALL_MAP ← STATE  
**Execution climbs the other way. Never reverse.**

| Class | Layers |
|-------|--------|
| **Immutable** | VAULT999 · ACT · DID · arifOS F1–F13 |
| **Replaceable** | A2A · MCP |
| **Disposable** | FastMCP · SDKs · frameworks · harness CLIs |

```
MCP/A2A = jalan raya (coordination)
AAA     = peta + pejabat kawalan (surface — NOT a protocol)
888     = hakim (arifOS)
VAULT   = arkib
```

```
Protocol PASS + Authority DENY = must not act
Protocol FAIL                  = no road
```

---

## 5. Authority layer — DID + ACT (403 is the proof)

DID and ACT are **not** communication. They are **authority**.

| | DID | ACT (`act_v1.*`) |
|--|-----|------------------|
| Question | Who are you? | What office / what may you? |
| Without | “trust me bro” | Identity → Action ungoverned |
| With | cryptographic actor | DID → capability → F1–F13 → action |

**Live:** `did:web:arif-fazil.com…` (public) · `did:arif:{organ}` (registry) + Ed25519. Map both.

**Offices:** 333 Propose · 555 Verify · 888 Judge · A-FORGE Execute · VAULT Witness.

### 5.1 The 403 proof (constitutional, not “security feature”)

```text
Hermes → AAA: "SEAL this action"

1 DID   Who?            → did:…:hermes     ✅
2 ACT   Office rights?  → OBSERVE/RESEARCH ✅
3 Req  SEAL
4 ACT   SEAL capability? → NO             ❌

Result: 403 / HOLD — AUTHORITY DENIED
```

**A2A valid · MCP valid · JSON-RPC valid — still DENY.**  
Transport success is orthogonal to office rights.

```text
Without ACT:  Identity → Action
With ACT:     DID → Capability → arifOS → Action → VAULT
```

**Wire:** ART `actGate` (OBSERVE exempt; MUTATE needs `act_v1.*`; IRREVERSIBLE → F13). Envelope DENY ALL; DISPLAY_ONLY max PREPARE.

### 5.2 Enforced vs assumed (honest)

| Enforced (fail-closed) | Soft / assumed today |
|------------------------|----------------------|
| Missing A2A-Version → **400** | Every CLI mutate live-ACT on every tool edge |
| Anonymous low W³ → **403 EMD** | Multi-hop ACT chain |
| DISPLAY_ONLY ceiling | Hermes A2A agent-card |
| Holy 8 kernel tools | Full OTel |
| ACT format + IRREVERSIBLE HOLD | — |
| DID registry + organ keys | — |
| VAULT file + vault CONNECTED | — |

---

## 6. AAA above protocol (anti lock-in)

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

## 7. Identity naming (locked)

| Domain | Canonical |
|--------|-----------|
| Capability token | **ACT** `act_v1.*` (retire SCT in new prose) |
| Agent id | **agentId** + did (not SPIFFE primary) |
| Citizen later | **warga_status / passport** (not VC brand) |
| Multi-hop | **ACT chain** deferred (no HDP brand) |
| Workload stack | Map to arif_init + ACT + organ keys (no SPIRE organ) |

External standards **map**. They never rename the institution.

---

## 8. Operators (no passport required yet)

| Surface | agentId / FI | Role | Model socket (WHICH) |
|---------|--------------|------|----------------------|
| OpenCode | FI-001 | Primary forge | FED `opencode` |
| Hermes ASI | FI-000 | Human bridge | FED `hermes-asi` |
| OpenClaw | *(binding, no FI)* | Gateway metabolizer | FED `openclaw` |
| AGY | FI-009 | Forge instrument | Gemini-native `gemini-3.6-flash` |
| Organs | ministries | Law/hands/earth/capital/vitality | MCP ports |

Operating ≠ passport. **State first.**

---

## 9. Probes (enforcement)

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

## 10. Boot law (every agent)

```
1. state-probe.sh  (or this file + ports)
2. CALL_MAP.md
3. ORGAN.md
4. arif_init when mutation needs law
5. Work — then seal/receipt as required
```

---

## 11. Next (after boring green)

| Order | Work | Not |
|-------|------|-----|
| P0 | Keep STATE_READY + PROTOCOL_ENFORCED | New organs |
| P1 | External CALL_MAP draft (docs only) | Live public bridge without 888 |
| P2 | Citizen stamps (Hermes → OpenClaw → OpenCode) | While degraded |
| P3 | Optional external door | Economy/DAO/SPIRE/HDP |

**Phase E parked:** x402, IBCT, PEER, Labuan — after telephone is **used**.

---

## 12. Survival tests

| Remove | Survive? |
|--------|----------|
| MCP | ✅ CLI remains |
| A2A | ✅ CLI remains |
| FastMCP | ✅ |
| F1–F13 / arifOS | ❌ institution dies |
| ACT+DID | ❌ no trustworthy agency |
| VAULT999 | ❌ no proof |

---

## 13. Explicitly deferred

Warga stamps · multi-hop ACT · AIMS/SPIRE rename · economy rails · force-push/main deploy without T3.

---

## 14. Ops (one block)

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

## 15. Pointer index (satellites → this file)

| Former / related doc | Status |
|----------------------|--------|
| CONSTITUTIONAL_SEPARATION_AXIOM | **→ this file §3–12** |
| CONSTITUTIONAL_LAYER_SEPARATION | **→ this file** |
| AAA_ABOVE_PROTOCOL | **→ this file §7** |
| ACT_AUTHORITY_LAYER | **→ this file §5** |
| PROTOCOL_ENFORCEMENT_MATRIX | **→ this file §9** + `protocol-enforce.sh` |
| AAA_STATE_PROTOCOL_AUDIT | **→ this file §4,9** + script |
| IDENTITY_NAMING_REGISTRY | **→ this file §7** |
| AAA_NEXT_90D | **→ this file §11** |
| STATE_OPS | **→ this file §14** |

Machine twin: `federation/STATE.yaml`  
Telephone detail: `CALL_MAP.md`  
Territory detail: `ORGAN.md`

---

## 16. Docs entropy (4-tier — One truth · Many projections)

**Not:** less files = less entropy.  
**Yes:** 1 truth · N references · 0 contradictions.

| Tier | Role | Paths | Action |
|------|------|-------|--------|
| **A Constitution** | Institution | **This file** (~200–400L) | Edit here only for law |
| **B Canon** | Elaboration | `philosophy/` · `doctrine/` · `canon/` | Header: FEDERATED → STATE.md |
| **C Operational** | Procedure | `operations/` · `contracts/` · `transport/` · `geox/` | Header: Constitutional Context |
| **D Receipts** | Proof | `sessions/` · `audit-*` · `receipts/` | **Preserve.** Never merge. Proof > compression |
| **Legacy** | History | `architecture/` · `archive/` | Archive when dead; do not fold into STATE |

**Four tests (new MD):**

1. Institution changes if lost? → **STATE.md**  
2. Knowledge lost? → **canon/philosophy/doctrine**  
3. Only procedure lost? → **operations/contracts**  
4. Evidence lost? → **receipts** (preserve)

**Forbidden:** mega-STATE (entropy singularity).  
**Formula:** `STATE.md = Constitution, not Library.`

---

*Institution before passport. Protocol under governance. Ditempa, bukan diberi.*
