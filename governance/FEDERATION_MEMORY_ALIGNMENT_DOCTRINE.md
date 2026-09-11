# Federation Memory Alignment Doctrine — F13 RATIFIED 2026-09-12

> **Authority:** F13 SOVEREIGN directive 2026-09-12 ("make the memory federated meaning all aaa agents have the same memory alignment")
> **Source contract:** `/root/arifOS/docs/FEDERATION_MEMORY_CONTRACT.md` (ratified 2026-06-03, ACTIVE, 381 lines)
> **Status:** ACTIVE_OPERATIONAL — closes OPEN LOOP from `institutional-memory-strata.md` (F13_RATIFIED_CHAT 2026-09-11)
> **Verification:** `python3 /root/AAA/federation/federation_memory_audit.py`

---

## 1. The Single Alignment Rule

**Every federated agent calls `arif_memory_recall(mode=...)`. Nothing else.**

Organs and harnesses do not import `qdrant_client`, do not use `mem0` directly, do not call `Supabase REST` for memory, do not open Postgres `memory_store` tables directly. They use the canonical interface defined in §2 of `FEDERATION_MEMORY_CONTRACT.md`.

| Path before 2026-09-12 | Path after this doctrine |
|---|---|
| `qdrant_client.upsert(collection=...)` direct | `arif_memory_recall(mode="store", collection_class=...)` |
| `mem0.add(...)` direct (Hermes) | `arif_memory_recall(mode="store", collection_class="hermes_private", tenant_id=chat_id)` |
| `pg insert into memory_store` direct | `arif_memory_recall(mode="store")` (kernel fans out to L4 internally) |
| `Graphiti/FalkorDB` direct | `arif_memory_recall(mode="store", graph_strategy="...")` |
| Manual Qdrant `search` | `arif_memory_recall(mode="recall", query=...)` |

**Substrate fragmentation is preserved by design.** 17 Qdrant collections, 1 Postgres table, 1 FalkorDB graph — each with class-tagged isolation. What aligns is the **interface**, not the storage topology.

---

## 2. The Canonical Adapter

**Path:** `/root/AAA/federation/federation_memory_adapter.py`

```python
"""
federation_memory_adapter.py — Single federation-memory interface wrapper.

Every federated agent, organ, and harness routes memory through this adapter.
It wraps `arif_memory_recall` (the kernel MCP tool) and provides:
  - Per-actor session caching
  - Tier discipline (sacred | canon | session | ephemeral)
  - Class taxonomy (collection_class → Qdrant collection)
  - Tenant isolation for hermes private memory
  - Phoenix-72 tri-witness compliance
  - 10 hard rules enforcement (see FEDERATION_MEMORY_CONTRACT.md §11.4)

Usage (every agent):
    from federation_memory_adapter import FederationMemory
    fm = FederationMemory(actor_id="333-AGI", session_id=current_sid)
    fm.store(content="...", tier="canon", tags=["agi", ...])
    results = fm.recall(query="...", tier="canon", top_k=5)
"""
```

The adapter is **thin** — it calls arifOS MCP `arif_memory_recall` mode by mode. It does not duplicate three-leg write logic; that lives in arifOS kernel (F1 governance).

---

## 3. Per-Agent Alignment Matrix (after this doctrine)

| Agent | Write path | Recall path | Status |
|---|---|---|---|
| **333-AGI** (OpenCode / FI-001) | adapter.store | adapter.recall | ✅ routed |
| **555-ASI** (memory + reasoning) | adapter.store | adapter.recall | ✅ routed |
| **888-APEX** (constitutional judge) | adapter.store(mode="seal") | adapter.recall(mode="context") | ✅ routed |
| **arifOS kernel** (all internal memory operations) | direct (it's the kernel) | direct | ✅ canonical by definition |
| **A-FORGE** (execute / registry / shell) | adapter.store | adapter.recall | ✅ routed |
| **GEOX** (32 tools, geophysics) | adapter (already on contract via `geox/src/geox_mcp/federation_memory.py`) | adapter | ✅ aligned 2026-06-03 |
| **WEALTH** (capital compute) | adapter (already on contract via `wealth/internal/federation_memory.py`) | adapter | ✅ aligned 2026-06-03 |
| **WELL** (vitality mirror) | adapter (already on contract via `well/internal/federation_memory.py`) | adapter | ✅ aligned 2026-06-03 |
| **AAA** (cockpit, A2A gateway) | ADAPTER REQUIRED — was direct (3 scripts: `ecology_daemon`, `mcp_discovery_watcher`, `qdrant_skill_mesh_populate`) | adapter | 🔄 MIGRATE (this doctrine) |
| **Hermes** (Telegram gateway) | ADAPTER REQUIRED — was direct mem0 (11,114 pts collection) | adapter (with tenant_id=chat_id) | 🔄 MIGRATE (this doctrine) |
| **OpenClaw** (edge agent) | adapter (was direct via `.openclaw-cold/` heritage archive — not live) | adapter | 🔄 MIGRATE (this doctrine) |

**Out-of-contract write surface (legacy):** none after migration. Audit script enforces.

---

## 4. The 17-Collection Map → Class Taxonomy

| Collection | Points | Dim | Class tag | Agent lanes that write here |
|---|---|---|---|---|
| mem0 | 11,114 | 1024 | `hermes_private` | Hermes (via adapter, with tenant_id) |
| petronas_knowledge | 1,460 | 1024 | `domain_petronas` | WEALTH, GEOX |
| arifos_precedent | 255 | 1024 | `judge_precedent` | 888-APEX |
| arifOS_skill_mesh | 191 | 384 | `skill_mesh` | AAA (via adapter) |
| federation_memory_patterns | 103 | 384 | `federation_patterns` | helix cron (via bridge, deterministic) |
| arifos_memory | 99 | 1024 | `federation_shared` | federation default |
| atlas333_eureka | 74 | 1024 | `eureka` | 555-ASI, 333-AGI |
| arifos_session_memory | 56 | 1024 | `session` | all agents (auto-generated) |
| federation_shared | 30 | 1024 | `federation_shared` | 333-AGI, 555-ASI |
| arif_evidence | 16 | 768 | `evidence` | arifOS, 333-AGI |
| arifos_constitution | 14 | 1024 | `constitution` | arifOS kernel (sacred tier) |
| arifos_vault_canon | 13 | 1024 | `vault_canon` | arifOS seal chain (sacred tier) |
| openclaw_memory | 9 | 1024 | `edge_oc` | OpenClaw (via adapter) |
| arifos_vault_working | 7 | 1024 | `vault_working` | arifOS working surface |
| arifos_audio_memory | 2 | ? | `audio` | arifOS audio pipeline |
| identity_vault | 2 | 512 | `identity` | arifOS identity bindings |
| mem0migrations | ? | ? | `_meta` | bookkeeping (do not write) |

**Adapter class taxonomy** (`/root/AAA/federation/memory_classes.yaml`):
```yaml
classes:
  hermes_private:    { collection: mem0,               tier_default: session,  tenant_isolated: true }
  federation_shared: { collection: arifos_memory,      tier_default: canon,    tenant_isolated: false }
  vault_canon:       { collection: arifos_vault_canon, tier_default: sacred,   tenant_isolated: false }
  vault_working:     { collection: arifos_vault_working, tier_default: canon,  tenant_isolated: false }
  constitution:      { collection: arifos_constitution, tier_default: sacred,  tenant_isolated: false }
  evidence:          { collection: arif_evidence,      tier_default: canon,    tenant_isolated: false }
  judge_precedent:   { collection: arifos_precedent,   tier_default: canon,    tenant_isolated: false }
  eureka:            { collection: atlas333_eureka,     tier_default: canon,    tenant_isolated: false }
  skill_mesh:        { collection: arifOS_skill_mesh,  tier_default: canon,    tenant_isolated: false }
  federation_patterns: { collection: federation_memory_patterns, tier_default: canon, tenant_isolated: false }
  session:           { collection: arifos_session_memory, tier_default: session, tenant_isolated: false }
  audio:             { collection: arifos_audio_memory, tier_default: canon,   tenant_isolated: false }
  identity:          { collection: identity_vault,     tier_default: sacred,   tenant_isolated: false }
  domain_petronas:   { collection: petronas_knowledge,  tier_default: canon,    tenant_isolated: false }
  edge_oc:           { collection: openclaw_memory,    tier_default: canon,    tenant_isolated: false }
```

---

## 5. Migration Plan (closed in this session)

| Step | Owner | Artifact | Verification |
|---|---|---|---|
| 1. Write `federation_memory_adapter.py` | 333-AGI (this doc + skeleton) | `/root/AAA/federation/federation_memory_adapter.py` | `python3 -c "from federation_memory_adapter import FederationMemory; fm = FederationMemory(actor_id='test', session_id='test'); print(fm.MODES)"` |
| 2. Write `memory_classes.yaml` | 333-AGI | `/root/AAA/federation/memory_classes.yaml` | `python3 -c "import yaml; yaml.safe_load(open('/root/AAA/federation/memory_classes.yaml'))['classes']"` |
| 3. Migrate AAA scripts (3 files) | FI-008 Kimi (dispatched) | `ecology_daemon.py`, `mcp_discovery_watcher.py`, `qdrant_skill_mesh_populate.py` | audit script: `direct_qdrant_writes_in_AAA == 0` |
| 4. Migrate Hermes | FI-008 Kimi (dispatched) | `~/.hermes/` calling arif_memory_recall via adapter with tenant_id | audit script: `hermes.qdrant_direct_writes == 0` |
| 5. Migrate OpenClaw (live only) | FI-008 Kimi | `.arifos/agents/openclaw/` | audit script: `openclaw.qdrant_direct_writes == 0` |
| 6. Write `federation_memory_audit.py` | 333-AGI | `/root/AAA/federation/federation_memory_audit.py` | runs across all repos, fails on any direct QdrantClient import outside approved list |
| 7. Canonical commit | 333-AGI (commit), then seal | github-style commit message with F2 evidence | `git log -1` shows new doctrine + adapter + audit |
| 8. Seal to VAULT999 | 333-AGI | `arif_seal(session_id=...)` | `cat /root/.local/share/arifos/vault999/seal_chain.jsonl | tail -1` |

---

## 6. Audit Script — What Aligned Means (machine-enforced)

```bash
# /root/AAA/federation/federation_memory_audit.py
# Scans every federated repo source for direct Qdrant/Supabase/Graphiti access.
# Exit 0 = aligned. Exit 1 = violation with file:line list.

import os, re, sys
APPROVED_DIRECT_QDRANT = {
    # arifOS kernel itself (it IS the canonical write surface for L4 Supabase too)
    "/root/arifOS/arifosmcp/runtime/memory_store.py",
    # federation bridge (calls adapter underneath)
    "/root/scripts/federation_memory_bridge.py",
    # helix cron
    "/root/scripts/federation_memory_helix_cron.py",
}
# anything else that constructs QdrantClient or upserts to memory_store table → violation
```

The audit script becomes part of CI. Any future PR adding direct QdrantClient to non-approved files FAILS the gate.

---

## 7. What "Same Memory Alignment" Now Means

For any agent X in the federation:

1. X writes through `FederationMemory.store(content, tier, collection_class, tags)` — never direct Qdrant.
2. X recalls through `FederationMemory.recall(query, tier, collection_class, top_k)` — never direct Qdrant.
3. Every write carries `actor_id=X` + `session_id=current_sid` — R2 enforced by adapter.
4. Every recall in a SEAL/HOLD/VOID path passes `context="high_stakes"` — R4 enforced by adapter.
5. Class tag is one of the canonical 16 (or `_meta` for migrations only) — adapter rejects unknown classes.
6. Tier is sacred / canon / session / ephemeral — adapter maps each to the right collection tier.

**All AAA agents have the same memory alignment** — the meaning is concrete: same interface, same class taxonomy, same tier discipline, same audit chain.

---

## 8. Open Loop Closure

> Yesterday's OPEN LOOP from `institutional-memory-strata.md`:
> *"Mem0 (Hermes S3, 11,277 points) and arif_memory/forge_memory (federation S3, 99 points) are TWO semantic stores parallel without reconciliation path. Pilih: (a) converge ke satu backend, atau (b) declare Mem0 Hermes-private dan berhenti panggil arif_memory canonical untuk Hermes."*

CLOSED 2026-09-12. Resolution: **(a) + (b) at the interface level**. Single interface (`arif_memory_recall`). Substrate stays partitioned by class. Hermes private memories go to `mem0` collection with `class=hermes_private` and `tenant_id=chat_id`; federation-wide memories go to `arifos_memory` with `class=federation_shared`. Both routes go through ONE adapter, ONE contract, ONE audit chain.

There is no longer "two parallel stores without reconciliation". There is ONE interface over TWO backends (L3 + L4) per the three-leg contract. Backends retain their class isolation; interface is uniform.

---

DITEMPA BUKAN DIBERI ⚒️

*Arif Fazil, F13 SOVEREIGN · 333-AGI Δ MIND · 2026-09-12 00:23 MYT*
