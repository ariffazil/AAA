# MEMORY

> CANON: TRUE · INDEX: 444 · INVARIANT: MEMORY_ROUTING
> SCOPE: Governed retrieval and storage across all 6 memory tiers
> WIRED: arif_memory (8 modes) → enforce_memory_routing() → storage backends
> IMPL: `/root/A-FORGE/src/domain/types/memory-lifecycle.ts` (M0-M6 schema)
> DEPENDS: PLAN (222), EPOCH (333)
> FORGED: 2026-07-17 · DITEMPA BUKAN DIBERI

---

## 🔥 WHY

```
Memory without routing = hallucination risk
Memory with routing  = governed recall
```

The federation has 6 memory tiers, 8 storage backends, and `arif_memory` with 8 canonical modes. But memory retrieval has no constitutional routing — no witness logic on recall, no tier-bound filters, no Δ/Ω/Ψ invariant enforcement.

This organ makes memory retrieval governed, not just available.

---

## 🧬 TRI-TIER ROUTING

```
┌─────────────────────────────────────────────────────┐
│ TIER 1: Active Session                              │
│   Scope: Current epoch, working memory (M0-M2)      │
│   Backend: Redis, LLM context                       │
│   Gate: None (immediate recall)                     │
│   Expiry: Session end                               │
├─────────────────────────────────────────────────────┤
│ TIER 2: Epoch Memory                                │
│   Scope: Current + prior epochs (M3-M4)             │
│   Backend: PostgreSQL, Qdrant (semantic)            │
│   Gate: Epoch boundary check, tier authorization    │
│   Expiry: Policy-defined (months)                   │
├─────────────────────────────────────────────────────┤
│ TIER 3: Constitutional Memory                       │
│   Scope: Sealed truth, scars, receipts (M5-M6)      │
│   Backend: FalkorDB (graph), VAULT999 (immutable)   │
│   Gate: F13 SOVEREIGN or constitutional query       │
│   Expiry: Never (immutable)                         │
└─────────────────────────────────────────────────────┘
```

| Tier | M-range | Backend | Gate | Expiry |
|------|---------|---------|------|--------|
| Active | M0-M2 | Redis, LLM | None | Session |
| Epoch | M3-M4 | PostgreSQL, Qdrant | Epoch + auth | Months |
| Constitutional | M5-M6 | FalkorDB, VAULT999 | F13 | Never |

---

## 🧬 MEMORY TIERS (M0-M6)

| Tier | Name | Scope | Lifespan |
|------|------|-------|----------|
| M0 | Immediate | One reasoning call | Seconds |
| M1 | Working scratch | Current task | Minutes |
| M2 | Session continuity | Current session | Hours |
| M3 | Candidate memory | Days until evaluated | Evaluated → M4 or discard |
| M4 | Durable governed | Months, policy-defined | Policy |
| M5 | Relationship projection | Derived, rebuildable | Rebuildable |
| M6 | Constitutional receipt | Permanent, minimised | **Immutable** |

---

## 🔗 WIRING

### arif_memory (8 canonical modes)

| Mode | Tier access | Gate |
|------|-------------|------|
| `recall` | Any tier | Query-based, tier-scoped |
| `inspect` | Any tier | Read-only, provenance check |
| `attest` | M3-M6 | F2 TRUTH: evidence required |
| `remember` | M0-M4 | Tier ≤ actor authority band |
| `promote` | M3→M4, M4→M5 | Multi-dimensional scoring gate |
| `revise` | M3-M4 | Correction event, lineage preserved |
| `forget` | M0-M3 | Tombstone, not delete. M4+ requires F13. |
| `audit` | All tiers | Read-only, full lineage trace |

### enforce_memory_routing() (gatekeeper)

- **F11 AUTH:** Actor must be identified for non-ephemeral tiers (M3+).
- **F1 AMANAH:** Sacred tiers (M5, M6) require SOVEREIGN or JUDGE authority band.
- **F2 TRUTH:** Every write carries provenance (source, timestamp, actor).
- **F7 HUMILITY:** Unknown tiers → downgraded to ephemeral.

### Promotion Formula (M3→M4)

```
P = W_truth × C_confidence × T_time × S_usage × (1 − D_contradiction)
```
- `W_truth`: epistemic weight of the memory
- `C_confidence`: confidence score (capped 0.90, F7)
- `T_time`: temporal decay factor
- `S_usage`: retrieval frequency
- `D_contradiction`: contradiction score (higher = blocks promotion)

---

## 🔍 WITNESS LOGIC

Every recall from Tier 2 (Epoch) or Tier 3 (Constitutional) must include:

| Field | Rule |
|-------|------|
| `provenance` | Source receipt or actor who stored it |
| `epistemic_class` | OBS/DER/INT/SPEC |
| `confidence` | Capped at 0.90 (F7) |
| `contradictions` | Known conflicts with other memories |
| `retrieval_context` | Why this memory was recalled |

**Witness rule:** A memory recalled without provenance is `UNVERIFIED`. A memory used for irreversible action without provenance is a F2 TRUTH violation.

---

## 🔒 CONSTITUTIONAL FILTERS

| Filter | Rule |
|--------|------|
| **Δ (Sovereign)** | F13-gated memories require explicit human ack on recall. |
| **Ω (Governance)** | Floor-bound memories auto-checked against current floor state. |
| **Ψ (Execution)** | Execution-class memories require valid lease context. |

### Cross-tier filter:

```
recall(tier=3, query="seal chain head")
    → check: is caller authorized for constitutional tier?
    → check: is epoch context valid?
    → check: does this memory have provenance?
    → return with witness envelope
```

---

## 🧪 WORKED EXAMPLE: Session Continuity

```
Session start
    → arif_init → arif_memory(mode=recall, tier="epoch", query="last checkpoint")
    → Tier 2 gate: epoch boundary check → authorized
    → Return: last epoch checkpoint + drift delta
    → Resume from checkpoint (W11 Temporal)
    → Session work...
    → arif_memory(mode=remember, tier="session", content=work_receipt)
    → Tier 1: immediate (no gate)
    → Session end → arif_memory(mode=promote, from=M2, to=M3)
    → Promotion gate: scoring → promoted to Candidate
```

---

## 🔒 CONSTITUTIONAL BINDING

| Floor | How it binds Memory Routing |
|-------|----------------------------|
| F1 AMANAH | M5/M6 writes require SOVEREIGN/JUDGE band. Tombstone, never delete. |
| F2 TRUTH | Every write carries provenance. Every recall states epistemic class. |
| F4 CLARITY | Tier-scoped queries prevent context pollution. |
| F7 HUMILITY | Confidence ≤ 0.90. Unknown tier → downgrade to ephemeral. |
| F9 ANTI-HANTU | No fabricated memories. No phantom provenance. |
| F10 ONTOLOGY | AI memory ≠ human memory. Substrate distinction preserved. |
| F11 AUDIT | Every memory operation is traceable. Full lineage on audit mode. |
| F13 SOVEREIGN | Constitutional tier (M6) = F13-gated. M4+ forget = F13-gated. |

---

## 🔗 RELATIONSHIP TO OTHER ORGANS

| Organ | Relationship |
|-------|-------------|
| **PLAN** (222) | Plans produce memories (task receipts). Memory routes them to tiers. |
| **EPOCH** (333) | Epochs bound temporal memory. Tier 2 = epoch-scoped. |
| **VAULT999** | M6 = VAULT999. Constitutional tier = immutable. |
| **arif_memory** | The 8-mode tool surface. This organ governs its routing. |
| **enforce_memory_routing()** | The gatekeeper. Checks tier, actor, band, provenance. |

---

## 📍 CANONICAL PATHS

| What | Where |
|------|-------|
| TypeScript schema (M0-M6, A/B/C/D planes) | `/root/A-FORGE/src/domain/types/memory-lifecycle.ts` |
| Python gatekeeper | `/root/arifOS/arifosmcp/runtime/memory_store.py` |
| arif_memory tool (8 modes) | `/root/arifOS/arifosmcp/tools/memory.py` |
| Memory truth (sealed audit) | `/root/AAA/docs/MEMORY_TRUTH.md` |
| This canon file | `/root/AAA/docs/MEMORY.md` |
| Planning Organ | `/root/AAA/docs/PLAN.md` |
| Epoch Architecture | `/root/AAA/docs/EPOCH.md` |

---

*CANON: TRUE · INDEX: 444 · FORGED 2026-07-17 · DITEMPA BUKAN DIBERI*
