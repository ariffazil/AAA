---
name: emem-shared-memory
description: Verifiable shared memory layer for multi-agent systems and Earth observation (emem.dev). Enables citing signed facts (emem:fact: tokens), offline receipt verification, and cross-agent A2A collaboration without vendor lock-in.
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# `emem` Verifiable Shared Memory Skill

`emem` is a universal shared memory layer for multi-agent systems (`https://emem.dev/mcp`). It allows independent AI agents across different vendors, models, and sessions to cite signed facts using permanent content-addressed tokens (`emem:fact:...`) and verify them offline with zero-trust Ed25519 receipts.

## Key Capabilities & Workflows

### 1. Zero-Key Reads & Fact Grounding

- **`emem_locate`**: Maps location names or coordinates to cell64 spatial addresses.
- **`emem_recall`**: Retrieves signed measurements, elevation, NDVI, weather, or foundation-model embeddings at a cell address.
- **`emem_memory_token`**: Mints permanent 84-character tokens (`emem:fact:cell:cid`) that survive context window compaction.
- **`emem_memory_token_resolve`**: Resolves `emem:fact:` or `emem:bundle:` tokens back to byte-identical signed facts across any model or session.
- **`emem_verify_receipt`**: Verifies Ed25519 cryptographic receipts and Merkle proofs offline without contacting a central server.

### 2. Multi-Fact Aggregation & Guarding

- **`emem_memory_bundle`**: Bundles up to 256 facts into a single 38-character `emem:bundle:` token.
- **`emem_query_region`** / **`emem_recall_polygon`**: Server-side exact value filtering, ranking, and spatial polygon queries over signed observations.
- **`emem_guard_verdict`**: Evaluates transcripts and assertions for signature validity (`PROV_SIG`), byte fidelity (`PROV_BYTES`), and drift thresholds (`PROV_DRIFT`).

---

## Token Grammar Reference

| Token Shape | Purpose |
| --- | --- |
| `emem:fact:` | Single signed observation at a location/entity |
| `emem:bundle:` | Compact handle for multiple facts (up to 256) |
| `emem:entity:` | Universal canonical identity for an object |
| `emem:raster:` | Native-resolution spatial grid / embedding array |
| `emem:trace:` | Verified OS execution trace from an enrolled device |

---

## Best Practices for Agents

1. **Context Compaction Resilience**: When context is about to be compacted or passed to another agent, retain the `emem:fact:` or `emem:bundle:` token string rather than paraphrasing numeric values.
2. **Offline Verification**: Always call `emem_verify_receipt` or verify Ed25519 receipts locally on critical decision handoffs.
3. Reads require **no API key, no account, and no signup**.
