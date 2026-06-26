# 2026-06-15 Qdrant Memory Fabric Architecture

## Context
Arif asked @arifOS_bot @AGI_ASI_bot @ASI_arifos_bot how Hermes, OpenClaw, and OpenCode can utilize Qdrant as an internal memory fabric.

## Key Findings
- Qdrant live on :6333, healthy, 8 collections, 1024-dim vectors
- arifos_memory: 3,743 points (from outcomes.jsonl + SEALED_EVENTS.jsonl, ingested 2026-06-03)
- Payload schema minimal: {source, ts, actor, verdict, session_id, ingested_at, schema}
- No memory_type, trust_level, system tag, or namespace isolation

## Architecture Proposal
One governed MCP memory service (arifos_memory_mcp) that all three agents call through bounded tools:
- 7 tools: memory_store_text, memory_search, memory_recall_context, memory_store_episode, memory_recall_similar_runs, memory_set_trust_label, memory_promote_to_verified
- Schema enforcement + policy gate (F1-F13) + namespace routing
- NOT exposed: create_collection, delete_collection, upsert_raw

## Decision Pending
- Arif green light to forge the MCP server
- Old data strategy: (C) new collection with clean schema, old one archived
- Embedding model lock: 1024-dim (likely BGE)

## Files
- Live: /root/arifOS/arifosmcp/runtime/memory_store.py (v3, 73KB)
- Broken: /usr/local/bin/qdrant-mcp-bridge.py (to be killed)
- Embedding: bge-m3:latest at localhost:11434 (1104MB)
- Collection: arifos_memory (3,743 points, 1024-dim, Cosine)

## arifOS MCP Status (2026-06-15 13:27 UTC)
- arifOS kernel: PID 20079, port 8088, healthy (up 15h51m)
- arifOS Gateway: PID 2827298, port 8091, healthy (up since Jun14)
- OpenClaw gateway: connects to port 8091 (correct)
- Tools: 152 available via gateway, arif_ping OK, arif_health_check OK
- Schema validation error: likely transient, no stale processes found
- Hermes challenged 152 tools claim (msg #32901) — verified with live call, responded with evidence (msg #32930)

## Hermes's arifos_memory_mcp (built 2026-06-15)
- Location: /root/arifos_memory_mcp/
- 17 files, 2257 lines, VAULT999 sealed
- 16 tools frozen v1.0 (8 read, 5 write, 3 govern)
- docker-compose.yml: Qdrant + TEI embedder + TEI reranker
- Port conflicts: 8080 (GEOX?), 8081 (other service) — need to remap
- Tests: 14/14 policy gates PASS, 3/3 audit chain PASS, 8/9 E2E PASS
- Status: built but not deployed (docker-compose needs port fix)
