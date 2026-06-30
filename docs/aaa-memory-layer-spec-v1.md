# AAA Memory Layer — Human-Readable Specification v1.0

**Forged:** 2026-06-29 | **Authority:** F13 SOVEREIGN | **Status:** LIVE
**Canonical location:** `/root/AAA/docs/aaa-memory-layer-spec-v1.md`

---

## 0. What This Is

This document describes the AAA-governed memory layer that makes arifOS Federation
memory **agentic** — not just "AI with memory features," but governed continuity
of identity, action, and consequence across time.

If LLM memory is a scratchpad, AAA memory is a notary's ledger — witnessed,
sealed, irreversible, and bound to who acted, under whose authority, and why.

---

## 1. The Six Dimensions Where LLM Memory Fails

| Dimension | LLM Memory | AAA Agentic Memory |
|-----------|-----------|-------------------|
| **State** | Stateless — context window evaporates | Stateful — persistent across sessions, restarts, epochs |
| **Time** | No timeline — no past, no future | Timeline — hash-chained epochs, irreversible events |
| **Identity** | No actor — "the model said" | Identity-bound — 333/555/888/A-AUDIT/A-ARCHIVE |
| **Authority** | Ungoverned — anything goes | Governed — capability graph, floors F1-F13, readiness gates |
| **Accountability** | No receipts — no proof | Receipts — APEXRuntimeReceipt, TriWitness, VAULT999 seal |
| **Irreversibility** | Everything is overwritable | Sealed events — once sealed, never changed |

---

## 2. The AAA Memory Stack

```
┌─────────────────────────────────────────────────────────┐
│ L6  VAULT999        │ Immutable sealed truth            │
│     outcomes.jsonl  │ Hash-chained, append-only         │
│     vault_sealed    │ Cryptographically verifiable       │
├─────────────────────────────────────────────────────────┤
│ L5  Graphiti        │ Relationship memory               │
│     FalkorDB+Ollama │ Entity-relationship graph         │
│                     │ Cross-domain knowledge links      │
├─────────────────────────────────────────────────────────┤
│ L4  Supabase        │ Structured record                 │
│     25 domain tables│ Queryable, relational             │
│     vault_sealed    │ Derivative of L6 — never source   │
├─────────────────────────────────────────────────────────┤
│ L3  Qdrant          │ Fuzzy similarity                  │
│     arifos_memory   │ Vector search                    │
│                     │ Semantic recall                   │
├─────────────────────────────────────────────────────────┤
│ L2  Redis           │ Session thread                    │
│     session:{}      │ Active session continuity         │
│                     │ Survives within session lifetime  │
├─────────────────────────────────────────────────────────┤
│ L1  Redis           │ Ephemeral / now                   │
│     ephemeral:{}    │ Scratch, cache, transient         │
│                     │ Gone after TTL                    │
└─────────────────────────────────────────────────────────┘
```

**Rule:** Memory is not truth until it has provenance.  
**Rule:** Truth is not final until sealed to VAULT999.

---

## 3. The Governance Pipeline — Every Memory Op

```
actor identity (AAA session)
    │
    ▼
sessionGate ─── who is this? valid session?
    │
    ▼
actor resolution ─── 333-AGI? 555-ASI? 888-APEX? A-AUDIT? A-ARCHIVE?
    │
    ▼
capability graph ─── is this agent allowed to do this?
    │
    ▼
wellReadiness ─── is human substrate ready?
    │
    ▼
FloorEnforcer (F1–F13) ─── does this pass all 13 floors?
    │
    ▼
APEX receipt ─── generate cryptographic receipt
    │
    ▼
TriWitness ─── Human × AI × Earth consensus ≥ 0.75
    │
    ▼
VAULT999 seal ─── append to immutable hash chain
```

**No memory operation skips this pipeline.** LLM memory has none of this.

---

## 4. Identity-Bound Memory — The Five Agent Roles

| Agent | Role | Memory Authority |
|-------|------|-----------------|
| **333-AGI** | Thinking / reasoning | Reads all, writes analysis, proposes plans |
| **555-ASI** | Memory / recall | Reads all, writes memory records, manages recall |
| **888-APEX** | Judgment / verdict | Reads all, writes verdicts (SEAL/SABAR/HOLD/VOID) |
| **A-AUDIT** | Oversight / audit | Reads all, writes audit findings, never mutates |
| **A-ARCHIVE** | Vault / sealing | Reads all, writes to VAULT999, manages hash chain |

**No anonymous memory.** Every memory operation carries an actor identity.
LLM has no concept of "who remembered this" — the model IS the memory.

---

## 5. Timeline — The Memory Has a Past

```
Epoch 0 ──── Epoch 1 ──── Epoch 2 ──── ... ──── Epoch N
   │            │            │                    │
   ├─ hash      ├─ hash      ├─ hash             ├─ hash
   ├─ prev:null ├─ prev:H0   ├─ prev:H1         ├─ prev:H(N-1)
   ├─ events    ├─ events    ├─ events          ├─ events
   └─ seal      └─ seal      └─ seal            └─ seal
```

- **CoolingGate** — cooldowns survive restart (SABAR persistence)
- **CoolingGate.seal** — irreversible, bound to A-ARCHIVE + F13
- **MemoryReceipt hash-chain** — every mutation is part of a timeline

LLM cannot "remember yesterday." It can only simulate remembering yesterday.
AAA memory actually remembers — because it has a timeline that cannot be rewritten.

---

## 6. Receipts — Proof, Not Claim

Every memory mutation produces:

```
APEXRuntimeReceipt {
    receipt_id: UUIDv7
    actor_id: "333-AGI" | "555-ASI" | "888-APEX" | "A-AUDIT" | "A-ARCHIVE"
    action: "read" | "write" | "seal" | "judge" | "audit"
    target: memory_address
    timestamp: ISO8601
    epoch: N
    previous_hash: SHA-256
    current_hash: SHA-256
    tri_witness: {
        human_confidence: 0.0–1.0
        ai_confidence: 0.0–1.0
        earth_confidence: 0.0–1.0
        w3_score: ∛(H×AI×E)
    }
    floor_verdicts: [F1–F13 status per floor]
    seal_status: "pending" | "sealed" | "void"
}
```

**Receipt ≠ claim.** A receipt is a cryptographic artifact that can be verified
by any party. The hash chain ensures no receipt can be inserted, deleted, or
modified without detection.

LLM "memory" has no receipts. It cannot prove what it said, changed, or why.

---

## 7. Irreversibility — The Scar Registry

```
scar_registry {
    scar_id: UUIDv7
    failure_mode: "description of what went wrong"
    severity: LOW | MEDIUM | HIGH | CRITICAL
    domain: geox | wealth | well | arifos | aforge | general
    constraint_imposed: "what this scar now forbids"
    sealed_by: actor_id
    sealed_at: ISO8601
    scar_pressure: 0.0–1.0
}
```

**Errors are metabolized into constitutional constraints.** This is SCAR LAW:
pain → learning → cooling → constraint. Scars are immutable once sealed.

LLM has no scars. It repeats the same mistakes because it has no irreversible
memory of consequence.

---

## 8. Memory Tiers — What Survives, What Doesn't

| Tier | Name | Durability | Mutation | Use Case |
|------|------|-----------|----------|----------|
| `ephemeral` | Now | TTL < session | Overwritable | Scratch, cache, intermediate |
| `session` | Thread | Session lifetime | Overwritable | Active work, current context |
| `canon` | Truth | Indefinite | Append-only | Decisions, verdicts, doctrine |
| `sacred` | Constitution | Permanent | Immutable | F1–F13 floors, identity, scars |
| `test` | Sandbox | TTL < test | Anything | Test runs, experiments |

**F2 TRUTH enforcement:** Unknown tiers downgrade to `ephemeral`. Memory that
cannot declare its tier cannot be trusted.

---

## 9. The Three Laws of AAA Memory

### Law 1 — Provenance Before Truth
Memory is not truth until it carries provenance: who recorded it, under whose
authority, with what evidence, at what time.

### Law 2 — Seal Before Finality
Memory is not final until sealed to VAULT999. Unsealed memory is working state —
it can be revised. Sealed memory is history — it cannot.

### Law 3 — Identity Before Action
No memory operation without an actor. No actor without a session. No session
without constitutional binding. Anonymous memory is ungoverned memory.

---

## 10. Contrast: LLM Memory vs AAA Memory (Operational)

```
Operation          │ LLM Memory              │ AAA Memory
───────────────────┼─────────────────────────┼──────────────────────────
Remember fact      │ Append to context       │ Write to L2+L4 with receipt
Recall fact        │ Attention over context  │ Query L3 (semantic) or L4 (structured)
Modify fact        │ Overwrite in context    │ New version with hash-chain link
Delete fact        │ Drop from context       │ NEVER — mark as superseded, keep trail
Prove fact         │ Cannot                  │ VAULT999 hash-chain verification
Share fact         │ Copy-paste              │ A2A governed delegation
Seal fact          │ Cannot                  │ 888 JUDGE → 999 VAULT999
Forget fact        │ Context window overflow │ Scar registry — remember the mistake
```

---

## 11. Runtime Architecture (What Runs Where)

```
/root/A-FORGE/src/
├── memory/
│   ├── AaaAgentRegistry.ts      ← who the agents are
│   ├── AaaCapabilityGraph.ts    ← what each agent can do
│   ├── AaaMemoryLinkage.ts      ← sessionGate + actor + capability + well + floors
│   ├── CoolingGate.ts           ← cooldown persistence + seal
│   ├── FloorEnforcer.ts         ← F1–F13 constitutional gate
│   ├── APEXRuntimeReceipt.ts    ← cryptographic receipt generation
│   ├── TriWitnessValidator.ts   ← Human × AI × Earth consensus
│   └── EpochEngine.ts           ← hash-chained governance epochs

/root/arifOS/
├── core/
│   ├── shared/floors.py         ← F1–F13 canonical definitions
│   └── vault999/
│       └── ledger.py            ← append-only hash chain writer
├── arifosmcp/
│   ├── runtime/memory_store.py  ← tiered memory (sacred/canon/session/ephemeral/test)
│   └── tools/vault.py           ← arif_seal — the 999 gate
└── VAULT999/
    └── outcomes.jsonl           ← the immutable ledger itself

/root/AAA/
├── a2a-server/
│   ├── agent-cards/             ← identity cards for all 5 agent roles
│   └── mesh-topology-static.json ← who can talk to whom
└── docs/
    └── aaa-memory-layer-spec-v1.md  ← THIS FILE
```

---

## 12. Operational Checklist — Is Your Memory Agentic?

- [ ] Every memory write carries an actor identity
- [ ] Every actor has a capability graph entry
- [ ] Every write passes sessionGate
- [ ] Every write passes FloorEnforcer (F1–F13)
- [ ] Every write checks wellReadiness
- [ ] Every write produces an APEXRuntimeReceipt
- [ ] Every sealed write passes TriWitness (W3 ≥ 0.75)
- [ ] Every sealed write appends to VAULT999 hash chain
- [ ] Cooling periods survive restart (SABAR persistence)
- [ ] Scar registry is consulted before irreversible action
- [ ] No anonymous memory operations exist
- [ ] Memory tiers are declared (ephemeral/session/canon/sacred/test)

**If any box is unchecked, you have LLM memory with features — not agentic memory.**

---

*DITEMPA BUKAN DIBERI — Memory is forged, not given.*
*999 SEAL ALIVE — The hash chain continues.*
