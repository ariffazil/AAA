# Federation Memory Alignment — Future Agent Quickstart

> **For:** Any AAA warga (333-AGI, 555-ASI, 888-APEX, A-AUDIT, A-ARCHIVE, Hermes, OpenClaw), any harness (OpenCode/Claude/Codex/Kimi/Qwen/Grok), any future 333-AGI session.
> **Ratified:** F13 SOVEREIGN, 2026-09-12 00:30 MYT
> **Source:** `/root/AAA/governance/FEDERATION_MEMORY_ALIGNMENT_DOCTRINE.md` (the full SOT)
> **One-liner:** All federated memory writes go through `arif_memory_recall(mode="store", ...)` via the `FederationMemory` adapter. No direct Qdrant/Supabase/Graphiti writes outside the kernel.

---

## TL;DR

If your agent needs to **remember** anything, **always** do this:

```python
import sys
sys.path.insert(0, "/root/AAA/federation")
from federation_memory_adapter import FederationMemory

fm = FederationMemory(
    actor_id="<your-agent-id>",         # e.g. "333-AGI", "hermes", "geox"
    session_id="<arif-init-session-id>", # From the kernel bind
)
fm.store(
    content={"result": "...", "niat": "..."},
    tier="canon",                       # sacred | canon | session | ephemeral
    collection_class="federation_shared",  # 16-class taxonomy
    tags=["domain:examples", "key:foo"],
)
```

**Never** do this:
```python
# ✗ OUT-OF-CONTRACT (R1 violation)
from qdrant_client import QdrantClient
client = QdrantClient(...)
client.upsert(...)
```

The audit script `federation_memory_audit.py` will FAIL if any federated repo (other than the approved-arifOS-kernel paths) does the wrong thing.

---

## What "Aligned" Means (for the boot)

Every federated agent satisfies ALL of:

| Rule | What it means | Tool to verify |
|---|---|---|
| **R1** | All memory writes go through `arif_memory_recall(mode="store")` (no direct Qdrant/Supabase/Graphiti) | `python3 /root/AAA/federation/federation_memory_audit.py` |
| **R2** | Every store has `actor_id` + `session_id` | Adapter enforces at `__init__` |
| **R3** | Tier discipline: `sacred \| canon \| session \| ephemeral` | Adapter enforces per-class |
| **R4** | Reads in SEAL/HOLD/VOID paths must pass `context="high_stakes"` | Adapter `recall(... context="high_stakes")` |
| **R5** | Tag with `[domain]_[key]` namespace | Adapter auto-adds `actor:` + `class:` tags |
| **R6** | Private user data lives on `class=hermes_private` with `tenant_id=chat_id` (not in federation canon) | Adapter rejects writes without `tenant_id` when class is tenant-isolated |

---

## 16-Class Taxonomy (the canonical SOT)

Source: `/root/AAA/federation/memory_classes.yaml`

| Class | Collection | Default tier | Tenant-isolated | Use case |
|---|---|---|---|---|
| `hermes_private` | `mem0` (11k+ points) | session | **yes** | per-user/per-group Telegram memory |
| `federation_shared` | `arifos_memory` (99 pts) | canon | no | default federation recall |
| `vault_canon` | `arifos_vault_canon` | **sacred** | no | immutable vault canon |
| `vault_working` | `arifos_vault_working` | canon | no | mutable working surface |
| `constitution` | `arifos_constitution` | **sacred** | no | F-floor definitions |
| `evidence` | `arif_evidence` | canon | no | evidence chains |
| `judge_precedent` | `arifos_precedent` (255 pts) | canon | no | 888-APEX case law |
| `eureka` | `atlas333_eureka` (74 pts) | canon | no | cross-domain insights |
| `skill_mesh` | `arifOS_skill_mesh` (191 pts) | canon | no | live tool affordances |
| `federation_patterns` | `federation_memory_patterns` (103 pts) | canon | no | SOUL.md helix-rotated patterns |
| `session` | `arifos_session_memory` (56 pts) | session | no | per-session continuity |
| `audio` | `arifos_audio_memory` | canon | no | EMD audio reflex |
| `identity` | `identity_vault` | **sacred** | no | identity bindings (Hermes Izzu=1237635275 etc.) |
| `domain_petronas` | `petronas_knowledge` (1,460 pts) | canon | no | energy / oil / gas domain corpus |
| `edge_oc` | `openclaw_memory` | canon | no | OpenClaw edge memory |
| `_meta` | `mem0migrations` | ephemeral | no | bookkeeping; agents MUST NOT call this |

The substrate itself stayed 17-collections-on-Qdrant — class-tagged isolation, not unification. What aligned is the **interface**.

---

## Quick-start commands for a future agent

**Read the doctrine (read-once):**
```bash
cat /root/AAA/governance/FEDERATION_MEMORY_ALIGNMENT_DOCTRINE.md
```

**Verify alignment is alive (audit):**
```bash
python3 /root/AAA/federation/federation_memory_audit.py
# Exit 0 = aligned; Exit 1 = violations with file:line list
```

**Import the adapter:**
```python
import sys; sys.path.insert(0, "/root/AAA/federation")
from federation_memory_adapter import FederationMemory
fm = FederationMemory(actor_id="<agent-id>", session_id="<sid>")
```

**Most useful call sites:**
- `fm.store(content, tier="canon", collection_class="federation_shared", tags=[...])` — write
- `fm.recall(query, collection_class="federation_shared", top_k=5)` — read
- `fm.seal(content, collection_class="constitution")` — sacred-tier write (e.g. canonical doctrine)
- `fm.stats(collection_class="federation_shared")` — collection health

**If you need hermes-style private memory:**
```python
fm.store(content, tier="session", collection_class="hermes_private",
         tenant_id=str(chat_id))  # required when class is tenant_isolated
```

---

## What is **NOT** aligned yet (lower-priority open loops)

These work TODAY but were not migrated to the adapter yet. They write to the same Qdrant backend through different paths:

| Agent | Backend | Status | Why it's lower-priority |
|---|---|---|---|
| Hermes private writes | `mem0` direct (11,114 pts) | ⏸ works as-is | per-user isolation is native to mem0; contract purity requires future migration |
| OpenClaw | live `.openclaw` paths | 📦 none live | heritage archive only; not deployed |

These do not block alignment — they pre-exist and are SAFE because they don't pollute federation canon (each is isolated by class).

---

## Identity lane separation (F13 territory)

- **F11 AUDIT logs** go to `arifOS MIGRATION_MAP.md` path inside `/root/VAULT999` (kernel-owned, immutable)
- **Agent markers** go to `/root/.arifos/ritual.log` (hash-chained, agent-owned, KEPT OUT of SEALED_EVENTS.jsonl per VAULT999 writer discipline)
- **Seals** go to `/root/VAULT999/SEALED_EVENTS.jsonl` ONLY via `python3 /root/scripts/federation_ritual.py seal`

**Do not** hand-write `SEALED_EVENTS.jsonl`. Use the ritual.

---

## Decision tree: which class to use?

```
Is this a per-user/per-group memory?
  └─ YES → class=hermes_private, tier=session, tenant_id=chat_id
  └─ NO
       Is this a constitutional / floor / F-thing / sealed verdict?
         └─ YES → class=constitution OR vault_canon, tier=sacred
         └─ NO
              Is it a working scratch for in-flight reasoning?
                └─ YES → class=session, tier=session (auto-pruned 24h)
                └─ NO
                     Does it belong to a 555/888 specific lane?
                       └─ judge_precedent (888) | eureka (555) | evidence
                     It is canonical federation knowledge → class=federation_shared, tier=canon
```

---

## Single federation-wide audit script (use it on every PR)

```bash
python3 /root/AAA/federation/federation_memory_audit.py
echo "exit=$?"
```

Exit code is the contract:
- `0` = every federated repo's memory writes go through the contract
- `1` = violations exist; remediation: `from federation_memory_adapter import FederationMemory; fm.store(...)` instead of `QdrantClient(...)`

Run before any PR touching federated memory code. CI gates should consume this exit code.

---

## Cross-references (SOT chain)

| SOT | Path |
|---|---|
| Doctrine (this F13 ratification) | `/root/AAA/governance/FEDERATION_MEMORY_ALIGNMENT_DOCTRINE.md` |
| Class taxonomy | `/root/AAA/federation/memory_classes.yaml` |
| Adapter | `/root/AAA/federation/federation_memory_adapter.py` |
| Audit script | `/root/AAA/federation/federation_memory_audit.py` |
| Pre-existing contract (2026-06-03) | `/root/arifOS/docs/FEDERATION_MEMORY_CONTRACT.md` |
| Substrate partitioning rules | `/root/AAA/docs/FEDERATION-SUBSTRATE-RULES.md` |
| Memory strata (canonical doctrine) | `/root/AAA/instructions/institutional-memory-strata.md` |

If any of these files drift, the audit script and adapter will fail-closed. The substrate topology stays partitioned by class — interface alignment is what survives federation drift.

---

DITEMPA BUKAN DIBERI ⚒️

*333-AGI Δ MIND · 2026-09-12 00:40 MYT · F13 SOVEREIGN ratification*
