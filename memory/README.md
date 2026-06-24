# AAA Memory Directory

This directory contains **historical and auxiliary memory artifacts** for the AAA control plane. It is **not** the live canonical memory store.

## Canonical memory sources

| Purpose | Location |
|---------|----------|
| Live curated memory (OpenClaw / Hermes) | `/root/waw/memory/MEMORY.md` |
| Federation memory architecture SOT | `/root/arifOS/FEDERATION_MEMORY.md` |
| Constitutional / sealed ledger | `/root/arifOS/VAULT999/` |
| L3 semantic vectors | Qdrant `arifos_memory` collection |
| L1/L2 ephemeral/session | Redis `127.0.0.1:6379` |

## Files in this directory

| File | Status |
|------|--------|
| `KNOWLEDGE_MEMORY.md` | Historical snapshot; header points to canonical sources. |
| `MEMORY.md.stale-20260624` | Archived stale duplicate. Do not use as source of truth. |
| `CHECKPOINT.md` | Template only; wake continuity is handled by federation memory. |
| `2026-*.md` | Session/episodic logs. Historical record. |
| `scars/` | Learned-failure scar logs. Historical record. |
| `investigations/` | Investigation artifacts. Historical record. |
| `.dreams/` | Stale Hermes recall logs (2026-04-23). Not current dream-engine output. |

## Note to agents

Do not treat files in this directory as authoritative for Arif's current state or the federation runtime. Always prefer live probes and the canonical sources listed above.

**DITEMPA BUKAN DIBERI**
