---
name: searah-agentic-rag
category: investigations
description: Level 2 Agentic RAG for SEARAH investigation documents. Decomposes multi-hop queries, traverses entity graph + chunk corpus, validates evidence, applies F2/F3 constitutional checks, and synthesizes grounded answers. Uses Qdrant (searah_entities + searah_docs + searah_relations) + Ollama bge-m3 embeddings.
---

# SEARAH Agentic RAG — Level 2

## Trigger
Any SEARAH-related query that requires multi-hop reasoning across the investigation corpus. Activate when the user asks "why," "how," "timeline," "who," or "what is the connection between" any combination of: PETROS, PETRONAS, SEARAH, Kasawari, Eni, Federal Court, arbitration, Malaysia Agreement 1963, PDA 1974.

## Architecture

```
User Query
    ↓
decompose_query()  →  typed sub-questions (ownership | jurisdiction | petros_exclusion | parliament | asset | legal_framework | value | timing | 人物 | dispute | constitutional | board | general)
    ↓
multi_hop_retrieve()  [3 hops]
    Hop 0: Direct entity + chunk search (bge-m3 cosine similarity)
    Hop 1: Relationship traversal (EXCLUDES, DISPUTES_WITH, OWNS_ASSET, LEGACY_BASIS, etc.)
    Hop 2: Cross-reference entities with chunk evidence
    ↓
self_correct()  →  validate relevance, flag contradictions, detect empty retrievals
    ↓
governance_verdict()  →  F2 TRUTH + F3 WITNESS constitutional check
    ↓
reflect()  →  COMPLETE / PARTIAL / WEAK / INCOMPLETE verdict
    ↓
synthesize()  →  structured answer with evidence provenance
```

## Collections

| Collection | Purpose | Points |
|------------|---------|--------|
| `searah_entities` | 27 verified entities (orgs, people, assets, legal frameworks, events) | 1024-dim bge-m3 |
| `searah_docs` | 185 chunks from 4 PDFs (searah_harakah, FORGED_V5, EXPOSE, makcik) | 1024-dim bge-m3 |
| `searah_relations` | 37 typed relationships between entities | payload-only |

## Entity Types
- `organization`: SEARAH-LIMITED, PETRONAS, PETRONAS-CARIGALI, ENI-LASMO, PETROS
- `asset`: KASAWARI, BLOCK-SK316, MASELE-ABADI, MLNG-BINTULU
- `institution`: MALAYSIA-GOVERNMENT, FEDERAL-COURT-MY
- `person`: TEKKU-MUHAMMAD-TAUFIK, MOHD-BAKKE-SALLEH, CLAUDIO-DESCALZI, GUIDO-BRUSCO, AZAKARI-MOHD-SHUID, MOHD-JUKRIS-ABDUL-WAHAB
- `legal_framework`: PETROLEUM-DEVELOPMENT-ACT-1974, MALAYSIA-AGREEMENT-1963, ICC-LCIA-ARBITRATION
- `event`: DEAL-SIGNING-ADIPEC, COMPANY-INCORPORATION, FEDERAL-COURT-RULING, COMPANY-RENAME, ANWAR-MELONI-MEETING, KASAWARI-PRODUCTION, PETROS-FILING

## Relationship Types
EXCLUDES, DISPUTES_WITH, OWNS_50, OWNS_ASSET, CLAIMS_JURISDICTION, LITIGATES_IN, LEGAL_BASIS, GOVERNED_BY, LOCATED_IN, FEEDS, PRECEDED_BY, RESULTED_IN, ENABLED, AUTHORIZED_BY, OWNS_VIA, CONTROLS, LEADS, CHAIRS

## Threshold Reference
- `REL_EVIDENCE_THRESHOLD = 0.30` (cosine similarity — domain-specific BGE-m3)
- `CHUNK_EVIDENCE_THRESHOLD = 0.28`
- `MAX_HOPS = 3`

## Constitutional Checks
- **F2 TRUTH**: All retrieved entities must be VERIFIED or INFERRED. No fabrication.
- **F3 WITNESS**: All entities must have at least 1 evidence source. Contradicted entities flagged.

## Output Grades
- `COMPLETE (conf ≥ 0.60)`: Ready to use
- `PARTIAL (conf 0.45–0.59)`: Use with caveats
- `WEAK (conf < 0.45)`: More evidence needed
- `INCOMPLETE`: Self-correction detected gaps requiring retry

## Key Verified Facts (Ground Truth)
- SEARAH LIMITED: Company No. 17027115, incorporated Feb 11 2026, renamed Mar 30 2026 (14 days after Federal Court ruling)
- 50/50 PETRONAS/Eni ownership — confirmed in Companies House PSC
- 19 assets total: 5 Malaysia (Block SK316/Kasawari) + 14 Indonesia (Masela/Abadi)
- Kasawari: 200 mmscf/d since Aug 2024, feeds MLNG Bintulu
- Deal signed Nov 3 2025 at ADIPEC Abu Dhabi — BEFORE incorporation and BEFORE Federal Court ruling
- Federal Court ruling Mar 16 2026: allows PETRONAS constitutional challenge
- No BIT protection: no Italy-Malaysia BIT, UK-Malaysia BIT lapsed
- ICC/LCIA London arbitration — Malaysian courts cannot order transfers
- No parliamentary record — no Hansard entry found for SEARAH deal

## Integration
For arifOS MCP: call `_arif_memory_recall(mode='searah', query=..., session_id=..., actor_id=...)`. The `query` parameter is the natural-language question. The tool returns the synthesized agentic RAG output.
