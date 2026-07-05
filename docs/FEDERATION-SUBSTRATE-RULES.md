# Federation Substrate Partitioning Rules

> Ratified: pending F13 review
> Scope: all arifOS federation organs (arifOS, GEOX, WEALTH, WELL, A-FORGE, AAA)
> Principle: one engine, multiple contracts — not one big bucket.

---

## 1. Data Classification

Every piece of state in the federation falls into exactly one category:

| Class | Description | Storage | Example |
|---|---|---|---|
| **LIVE** | Current session state, heartbeats, agent presence | Redis (L1) | `aaa:federation:organs:pnc` |
| **FUZZY** | Semantic recall, capability matching, evidence search | Qdrant (L3) | `arifos_memory`, `arifos_session_memory` |
| **STRUCTURED** | Seals, sessions, tool calls, evidence index, plans | Postgres (L4) | `arifosmcp_vault_seals`, `evidence_index` |
| **RELATIONAL** | Entity graphs, knowledge links, sagas, episodes | FalkorDB/Graphiti (L5) | `arifos_federation`, `arif_l5_knowledge` |
| **IMMUTABLE** | SEAL chain, receipts, scars, capsules | VAULT999 (L6) | `seal_chain.jsonl`, `outcomes.jsonl` |
| **BLOB** | Raw domain data (SEGY, LAS, PDFs, models) | MinIO / filesystem | GEOX seismic volumes, LAS logs |
| **SCRATCH** | Ephemeral execution state, temp artifacts | A-FORGE CouchDB | Run outputs, build intermediates |

**Rule:** If data doesn't fit a class, it doesn't belong in the federation. No ad-hoc storage.

---

## 2. Canonical Write Paths (Registry Governance)

Each registry type has ONE write authority. All other copies are read-only mirrors or symlinks.

| Registry Type | Canonical Write Path | Read Mirrors |
|---|---|---|
| Agent Registry | `/root/.local/share/arifos/agent_registry/` | AAA `/a2a-server/agent-cards/`, OpenClaw copies |
| Tool / MCP Registry | `/root/AAA/docs/TOOLREGISTRY.json` | arifOS `TOOL_MANIFEST.json`, local `/tool_registry/` |
| Skill Registry | `/root/.arifos_skill_registry.yaml` | GEOX manifests, lifecycle registry |
| Schema Registry | `/root/AAA/registries/SCHEMA_REGISTRY.json` | arifOS `/schemas/`, organ-local schemas |

**Enforcement rules:**
1. **Write-through only.** Any API, UI, or script that modifies a registry MUST write to the canonical path.
2. **Mirrors are read-only.** Non-canonical paths must be symlinks or refreshed by sync script — never edited directly.
3. **Divergence = HOLD.** If a canonical path and its mirror disagree (hash mismatch), the mirror is stale. Reads from stale mirror trigger WARN log and fallback to canonical.
4. **No silent drift.** Daily cron scans all registry paths, compares SHA256, logs divergence to `/var/arifos/artifacts/logs/registry-drift.jsonl`.

---

## 3. Naming + ACL Contract

### Naming
- Postgres schemas: `{organ}_{purpose}` (e.g., `well_biometric`, `geox_survey`, `wealth_portfolio`)
- Qdrant collections: `{organ}_{domain}_{version}` (e.g., `arifos_memory_v2`, `geox_evidence_v1`)
- MinIO buckets: `{organ}-{datatype}` (e.g., `geox-seismic`, `geox-las`, `wealth-documents`)
- Redis keys: `{organ}:{subsystem}:{key}` (e.g., `aaa:agent:hermes-asi`, `geox:session:abc123`)

### ACL
- **Default deny.** Organ can only read/write its own namespace unless explicitly granted cross-organ access.
- **Cross-organ reads** require kernel ACL entry (logged to F11 audit trail).
- **Cross-organ writes** require SEAL + F13 approval (irreversible boundary crossing).
- **WELL namespace** (`well_*`) has row-level security enforced at kernel level — no organ, including arifOS runtime, can read WELL biometric data without explicit vitality check context.

---

## 4. Special Cases

### WELL — Human Signal Isolation
- Dedicated Postgres schema: `well_biometric` with RLS (Row-Level Security)
- No cross-organ reads without `well:readiness` or `well:vitality` context
- Biometric raw data never enters Qdrant (vector similarity ≠ medical truth)
- WELL evidence that feeds SEAL is aggregated/anonymized before entering shared layers
- F6 MARUAH: human dignity preserved by data minimization, not just access control

### GEOX — Blob Storage
- Raw seismic (SEGY), well logs (LAS), survey data → MinIO buckets or structured `/GEOX/data/` dirs
- Metadata (survey params, well headers, interpretation results) → Postgres `geox_*` schemas
- No blob data in Postgres, Qdrant, or Redis (storage isolation)
- GEOX can grow independently without starving other organs' storage

### A-FORGE — Scratch Space
- CouchDB remains dedicated for execution lifecycle
- Ephemeral artifacts auto-purge after 72h unless promoted to VAULT999 (SEAL)
- Scratch ≠ memory. CouchDB data has no durability guarantee.

---

## 5. Enforcement Mechanism

1. **Drift scanner** (daily cron): compares canonical vs mirror registries, logs to `registry-drift.jsonl`
2. **Schema guard**: organ startup validates its schema/collection/bucket names against naming contract
3. **ACL audit** (weekly): cross-organ access review — who read what, when, why
4. **Write-path lint**: CI/lint check on any script or API that touches registries — must target canonical path

---

## 6. What This Solves

| Before | After |
|---|---|
| "Mana yang betul?" — 3 registries, 3 answers | Canonical read path. Drift = WARN. |
| New organ = setup DB + Qdrant + registry + sync | Declare organ → kernel allocates namespace → run |
| Manual trace: "data ni dari mana?" | Provenance chain: who wrote, where, which layer agrees |
| WELL data mixed with tool logs | RLS + minimization + aggregation boundary |
| GEOX blobs compete with Postgres disk | Separate storage tier. Metadata still in Postgres. |

---

## 7. Migration Path

Not a rewrite. A convergence:

1. Declare canonical write path for each registry (Section 2)
2. Convert non-canonical copies to symlinks or read-only mirrors
3. Add drift scanner cron
4. Create WELL RLS schema, migrate existing well data
5. Move GEOX blobs to MinIO (or formalize `/GEOX/data/` as blob tier)
6. Enforce naming convention on new schemas/collections/buckets

**Phase 1 (immediate):** Sections 2 + 5 (canonical paths + drift scanner)
**Phase 2 (short):** Section 4 (WELL RLS + GEOX blob formalization)
**Phase 3 (ongoing):** Section 3 (ACL enforcement + naming guard)

---

## 8. Memory Governance Contract

**Memory is not storage. Memory is delegated authority.**

The federation already has L1–L6 substrate (see FEDERATION_MEMORY_CONTRACT.md). This section adds the **constitutional layer** on top: rules for *what* may be remembered, *how* it is classified, *who* may act on it, *when* it expires, and *how* it may be overridden.

### 8.1 The Six Memory Systems (why one word creates bugs)

| Memory System       | What it is                              | Storage Layer | Risk if ungoverned                  |
|---------------------|-----------------------------------------|---------------|-------------------------------------|
| Model memory        | LLM weights / patterns from training    | LLM weights   | Outdated, uninspectable bias        |
| Context / Working   | Current turn state, in-flight variables | L1 Redis      | Ephemeral only, lost on crash       |
| Retrieval           | Semantic "feels similar" recall         | L3 Qdrant     | Stale vectors treated as truth      |
| Structured / Evidence | Exact records, decisions, sources     | L4 Postgres   | Inferred facts stored as observed   |
| Relational / Project| Entities, connections, sagas            | L5 Graphiti   | Orphan relations, stale context     |
| Constitutional / Immutable | Rules about memory itself + final truth | L6 VAULT999 | No meta-rules → authority creep     |

**Rule:** Every memory write MUST declare its system + evidence tier (OBS / DER / INT / HYP) at the point of creation.

### 8.2 Memory Bands + Authority Rules

Not all memory has the same power to influence action.

| Band                  | Examples                              | Evidence Tier Required | Expiry Default | Action Boundary                  | Override Path          |
|-----------------------|---------------------------------------|------------------------|----------------|----------------------------------|------------------------|
| **Preference**        | "Arif prefers direct answers"         | INT (user stated)      | 90d            | Style adaptation only            | User or F13            |
| **Project / Relational** | Task state, entity links            | DER                    | 90d            | Continuity within project        | Kernel review          |
| **Evidence / Decision** | Tool results, verdicts, receipts    | OBS or DER + source    | Canon 90d      | Input to SEAL only               | 888 + tri-witness      |
| **Identity**          | Biometric, human signals (WELL)       | OBS + minimization     | Per F6         | Never direct action              | F6 + explicit consent  |
| **Agent State**       | Workflow checkpoint, last tool call   | OBS + session          | 24h / ephemeral| Execution only                   | Rollback via L6        |
| **Constitutional**    | "This type of memory may never be used for X" | Sacred (L6)       | ∞              | Defines all other boundaries     | F13 only               |

### 8.3 Evidence Tier Enforcement (F2)

- **OBS (Observed)**: Direct from organ or human. Highest trust. Must carry source_id.
- **DER (Derived)**: Computed or summarized. Must carry derivation rule + confidence ≤ 0.85.
- **INT (Interpreted)**: Inferred by LLM. Must carry `inferred_by` + low confidence cap. Never feeds irreversible decisions without human witness.
- **HYP (Hypothesis)**: Speculative. Only for exploration. Auto-pruned.

Any recall feeding 888 JUDGE or SEAL must be `context="high_stakes"` and surface the tier + provenance.

### 8.4 The Observer Effect (Memory changes the future)

Once memory is loaded into context, it bends the next generation.

**Mitigations:**
- Tiered loading: high_stakes recalls are injected with explicit "This is Lx memory, tier Y" wrapper.
- Preference memory is soft-loaded only for style; never for content decisions.
- Agent state memory is isolated to the executing workflow; not mixed into general recall.
- Constitutional memory (L6) is always consulted first for "is this allowed to influence?"

### 8.5 Constitutional Memory (the missing layer)

Constitutional memory stores the *rules about memory*:

- Which bands may cross into which organs
- Expiry + prune policies (see tier discipline in FEDERATION_MEMORY_CONTRACT)
- What may never be remembered (e.g., raw WELL biometrics never vectorized)
- Override authority (user > kernel > organ)
- Drift detection between memory layers

This lives in L6 VAULT999 as sealed capsules + in the kernel as executable policy.

**Single write surface for constitutional memory:** only through arifOS 888 paths or F13 direct. No organ may self-authorize changes to "what is allowed to be remembered."

### 8.6 Integration with Substrate

- All memory writes still go through the single `arif_memory_recall` surface (or equivalent kernel gate).
- Canonical write paths apply to memory bands too (no organ writes preference memory directly into its own Redis without kernel mediation).
- Special isolation (WELL, GEOX blobs) already defined in Section 4 remains.
- Drift between L3 recall and L4 record triggers automatic HOLD for high-stakes actions.

This turns "memory" from a convenience into governed substrate.

---

**End of document.**

---

## 8. Memory Governance Contract

**Memory is not storage. Memory is delegated authority.**

The federation already has L1–L6 substrate (see FEDERATION_MEMORY_CONTRACT.md). This section adds the **constitutional layer** on top: rules for *what* may be remembered, *how* it is classified, *who* may act on it, *when* it expires, and *how* it may be overridden.

### 8.1 The Six Memory Systems (why one word creates bugs)

| Memory System       | What it is                              | Storage Layer | Risk if ungoverned                  |
|---------------------|-----------------------------------------|---------------|-------------------------------------|
| Model memory        | LLM weights / patterns from training    | LLM weights   | Outdated, uninspectable bias        |
| Context / Working   | Current turn state, in-flight variables | L1 Redis      | Ephemeral only, lost on crash       |
| Retrieval           | Semantic "feels similar" recall         | L3 Qdrant     | Stale vectors treated as truth      |
| Structured / Evidence | Exact records, decisions, sources     | L4 Postgres   | Inferred facts stored as observed   |
| Relational / Project| Entities, connections, sagas            | L5 Graphiti   | Orphan relations, stale context     |
| Constitutional / Immutable | Rules about memory itself + final truth | L6 VAULT999 | No meta-rules → authority creep     |

**Rule:** Every memory write MUST declare its system + evidence tier (OBS / DER / INT / HYP) at the point of creation.

### 8.2 Memory Bands + Authority Rules

Not all memory has the same power to influence action.

| Band                  | Examples                              | Evidence Tier Required | Expiry Default | Action Boundary                  | Override Path          |
|-----------------------|---------------------------------------|------------------------|----------------|----------------------------------|------------------------|
| **Preference**        | "Arif prefers direct answers"         | INT (user stated)      | 90d            | Style adaptation only            | User or F13            |
| **Project / Relational** | Task state, entity links            | DER                    | 90d            | Continuity within project        | Kernel review          |
| **Evidence / Decision** | Tool results, verdicts, receipts    | OBS or DER + source    | Canon 90d      | Input to SEAL only               | 888 + tri-witness      |
| **Identity**          | Biometric, human signals (WELL)       | OBS + minimization     | Per F6         | Never direct action              | F6 + explicit consent  |
| **Agent State**       | Workflow checkpoint, last tool call   | OBS + session          | 24h / ephemeral| Execution only                   | Rollback via L6        |
| **Constitutional**    | "This type of memory may never be used for X" | Sacred (L6)       | ∞              | Defines all other boundaries     | F13 only               |

### 8.3 Evidence Tier Enforcement (F2)

- **OBS (Observed)**: Direct from organ or human. Highest trust. Must carry source_id.
- **DER (Derived)**: Computed or summarized. Must carry derivation rule + confidence ≤ 0.85.
- **INT (Interpreted)**: Inferred by LLM. Must carry `inferred_by` + low confidence cap. Never feeds irreversible decisions without human witness.
- **HYP (Hypothesis)**: Speculative. Only for exploration. Auto-pruned.

Any recall feeding 888 JUDGE or SEAL must be `context="high_stakes"` and surface the tier + provenance.

### 8.4 The Observer Effect (Memory changes the future)

Once memory is loaded into context, it bends the next generation.

**Mitigations:**
- Tiered loading: high_stakes recalls are injected with explicit "This is Lx memory, tier Y" wrapper.
- Preference memory is soft-loaded only for style; never for content decisions.
- Agent state memory is isolated to the executing workflow; not mixed into general recall.
- Constitutional memory (L6) is always consulted first for "is this allowed to influence?"

### 8.5 Constitutional Memory (the missing layer)

Constitutional memory stores the *rules about memory*:

- Which bands may cross into which organs
- Expiry + prune policies (see tier discipline in FEDERATION_MEMORY_CONTRACT)
- What may never be remembered (e.g., raw WELL biometrics never vectorized)
- Override authority (user > kernel > organ)
- Drift detection between memory layers

This lives in L6 VAULT999 as sealed capsules + in the kernel as executable policy.

**Single write surface for constitutional memory:** only through arifOS 888 paths or F13 direct. No organ may self-authorize changes to "what is allowed to be remembered."

### 8.6 Integration with Substrate

- All memory writes still go through the single `arif_memory_recall` surface (or equivalent kernel gate).
- Canonical write paths apply to memory bands too (no organ writes preference memory directly into its own Redis without kernel mediation).
- Special isolation (WELL, GEOX blobs) already defined in Section 4 remains.
- Drift between L3 recall and L4 record triggers automatic HOLD for high-stakes actions.

This turns "memory" from a convenience into governed substrate.

---

**End of document.**
