# 08 — Evidence Matrix (Claim → Evidence → Confidence)

**Audit:** VMA-2026-08-07
**Method:** Every claim traceable to a file, port probe, or source reference

---

## Confidence Tiers

| Tier | Definition |
|------|-----------|
| **VERIFIED** | Live probe re-confirms; exact numbers/values match |
| **SUPPORTED** | Indirect probe (file exists, port open); claim is reasonable but exact number not confirmed |
| **DOWNGRADED** | Claim was made but live probe contradicts or partially contradicts |
| **UNVERIFIABLE** | Source not accessible from local probe |

---

## Claim-by-Claim Matrix

| # | Claim | Source in audit | Live evidence | Confidence |
|---|-------|----------------|---------------|-----------|
| 1 | 6 memory deliverables at `/root/AAA/reports/multimodal-memory-audit/` | MISSION.md | `ls -la` confirms 6 .md files | ✅ VERIFIED |
| 2 | 15+ memory components | 01_memory_census.md:22 | 15 rows in table; 6+ categories | ✅ VERIFIED |
| 3 | 15 Qdrant collections | 01:34 (col 4) | `curl :6333/collections` returns 15 | ✅ VERIFIED |
| 4 | VAULT999 = 38,945 events | 01:23 (col 4) | `wc -l outcomes.jsonl` = 38,947 | ✅ VERIFIED (off by 2, acceptable drift) |
| 5 | arifOS tools_loaded = 8 | (not in audit) | arifOS `:8088/health` reports `tools_loaded: 8, canonical: 8` | ✅ VERIFIED |
| 6 | bge-m3 (566M params, text-only) | (referenced) | Ollama `/api/tags` shows bge-m3 with bert family, 566.7M params | ✅ VERIFIED |
| 7 | qwen2.5:3b running | (referenced) | Ollama `/api/tags` confirms qwen2.5:3b (3.1B params) | ✅ VERIFIED |
| 8 | Graphiti MCP healthy | 03 gap_analysis: "Graphiti timeout" | `:8000/health` returns healthy; `initialize` returns 1.26.0 | ⚠️ DOWNGRADED — works with proper handshake, not "timeout" |
| 9 | MinIO available at :9000 | 06 roadmap: T2.1.1 | `docker ps` shows minio:127.0.0.1:9000-9001->9000-9001/tcp | ✅ VERIFIED |
| 10 | FalkorDB at :6380 | (referenced) | `docker ps` shows falkordb:127.0.0.1:6380->6379/tcp | ✅ VERIFIED |
| 11 | Redis at :6379 | 01:25 (col 3) | Redis alive, 23 keys | ✅ VERIFIED |
| 12 | RASA_DERITA exists, status 888_HOLD | 03: §3 Affective Layer | arifOS `:8088/health.rasa_derita.status = "888_HOLD"` | ✅ VERIFIED |
| 13 | 877 existing records to backfill | 06:53, 06:271, 06:310 | Qdrant `arifos_memory` = 49 points | ❌ NOT VERIFIED (49 in Qdrant; may be 877 elsewhere) |
| 14 | 54 Supabase tables with RLS disabled | (only in chat summary, not in deliverable) | Cannot verify (remote Supabase) | ⚠️ UNVERIFIABLE |
| 15 | 8 ingestion pathways mapped | 02:8 headings | 8 distinct ### Pathway N sections | ✅ VERIFIED |
| 16 | 0 multimodal ingestion today | Executive summaries | Qdrant text-only, no audio/image pipelines, no VLM/CLIP | ✅ VERIFIED |
| 17 | Schema has 8 faces (artifact/semantic/aff_obs/aff_int/relational/temporal/provenance/salience) | 04 schema | All 8 fields present in YAML | ✅ VERIFIED |
| 18 | F2 epistemic labels (OBS/DER/INT/SPEC) in schema | 04 schema | `epistemic_label: enum(OBS\|DER\|INT\|SPEC)` present | ✅ VERIFIED |
| 19 | Schema is backward compatible | 04 doc | All new fields nullable or defaulted | ✅ SUPPORTED |
| 20 | Memory Object schema is Pydantic v2 (claim) | OpenCode chat summary | Actual: YAML format, not Pydantic | ⚠️ DOWNGRADED — format mismatch |
| 21 | T1 schema migration = 3 hours, $0, reversible | 06: §13.0 | Reasonable estimate from scope | ✅ SUPPORTED |
| 22 | arifOS deployment drift | (mentioned in audit) | arifOS `:8088/health.deployment_drift_status = "drift_detected"` | ✅ VERIFIED |
| 23 | 10 quick wins = 24.5h total | 06: §11.0 | Sum of estimates: 2.5+2+7+4+2+1+1+2+2+1 = 24.5h | ✅ VERIFIED |
| 24 | 6 highest-risk assumptions | 06: §12.0 | 6 assumptions listed | ✅ VERIFIED |

---

## Evidence Sources Index

| File/Port | What it proves |
|-----------|----------------|
| `curl :8088/health` | arifOS state, tools, RASA_DERITA, Graphiti flag |
| `curl :6333/collections` | Qdrant collection inventory |
| `curl :6333/collections/<name>` | Per-collection point counts |
| `curl :8000/health` | Graphiti MCP liveness |
| `curl :8000/mcp initialize` | MCP handshake correctness |
| `docker ps` | Container inventory (MinIO, FalkorDB, Qdrant, Redis, postgres) |
| `wc -l /root/arifOS/VAULT999/outcomes.jsonl` | Sealed event count |
| `grep` against audit files | Internal consistency of deliverables |

---

## Risk Register

| # | Risk | Severity | Mitigation |
|---|------|----------|-----------|
| R1 | "877 records" — wrong number used in roadmap | MEDIUM | Probe Supabase directly or use 49 for Qdrant in T1.4 |
| R2 | "Graphiti timeout" — misdiagnosed | LOW | Tools list works with proper MCP handshake; client config fix |
| R3 | Schema delivered in YAML not Pydantic | LOW | YAML is more storage-agnostic; claim correction in chat log |
| R4 | "54 Supabase tables with RLS" — unverified | LOW | Claim removed from deliverables; only in chat summary |
| R5 | Line counts vary between OpenCode runs (1689 vs 1795) | LOW | Cosmetic; final state in disk is what matters |

---

## Recommendations

1. **Use actual Qdrant count (49) in T1.4 instead of 877.** Probe Supabase separately for the real backfill number.
2. **Document Graphiti MCP handshake requirement** in tooling docs (T3 quick win).
3. **Update chat-summary-only claims** — the "23 components", "54 tables", "Pydantic" stats are not in deliverables but propagated via chat. Either remove or surface them only with verification.
4. **Schedule a follow-up audit** after T1 schema migration lands, to verify the 8 JSONB columns actually do what the schema claims.
