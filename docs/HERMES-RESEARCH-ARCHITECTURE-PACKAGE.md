# HERMES RESEARCH SUBSTRATE — Complete Architecture Package
> ARIFOS::HERMES_RESEARCH_SUBSTRATE::EXECUTION::v1
> All 12 phases designed. Ready for F13 ratification.
> Executed: 2026-09-20

---

## PHASE 1 — SOURCE REGISTRY

### Canonical Provider Set (9 providers, immutable)

| # | Provider | Authority Scope | License Scope | Rate Limits | Adapter Status | Replacement |
|---|---|---|---|---|---|---|
| 1 | OpenAlex | Global scholarly graph spine | Data: CC0. API: free (polite pool) | 100K credits/day (free key) | READY (no key needed) | Crossref + Semantic Scholar partial |
| 2 | Crossref | DOI registration + metadata | Metadata accessible | 5-10 req/s (polite pool) | READY (no key needed) | OpenAlex metadata partial |
| 3 | Semantic Scholar | Relevance + enrichment | ODC-BY (attribution) | 100 req/5min (unauth); 1 RPS (free key) | NEEDS FREE KEY | OpenAlex related works |
| 4 | CORE | OA aggregation + full text | Per-item provider license | 5 req/10s (unregistered) | NEEDS FREE KEY | Europe PMC + arXiv |
| 5 | arXiv | STEM preprints | arXiv terms | 1 req/3 sec | READY (no key needed) | OpenAlex (metadata only) |
| 6 | PubMed/Europe PMC | Biomedical discovery + OA text | Metadata accessible; OA subset licenses | 3/sec (unauth); 10/sec (key) | READY (no key needed) | Semantic Scholar biomedical |
| 7 | Open Library | Book metadata + availability | Open catalog; scan rights vary | 1-3 req/sec | READY (no key needed) | WorldCat + Google Books |
| 8 | Internet Archive | Book text + archived content | Item-level rights | ~60 calls/min | READY (no key needed) | HathiTrust |
| 9 | Gutenberg | Public domain full text | Public domain | No defined limit | READY (no key needed) | IA public domain |

### Optional Providers (not foundational)

| Provider | Authority | Access | Notes |
|---|---|---|---|
| Lens | Scholarly-patent bridge | Token required | Contractual access |
| Dimensions | Research intelligence | Subscription | High value but licensed |
| WorldCat | Library holdings | Usually subscription | Bibliographic utility |
| Google Books | Discovery + snippets | API key + quota | Not corpus authority |
| HathiTrust | Bibliographic + rights | Key/institutional | Not default full text |
| Zotero | Human-curated library | Web API | Personal bibliography |

### Provider Authority Map

```
Authority is NOT equal across providers:

OpenAlex  = graph spine (works, authors, institutions, citations)
Crossref  = DOI truth (registration, metadata, funder info)
S2        = relevance + influence (TLDR, embeddings, recommendations)
CORE      = OA full text (aggregated open access)
arXiv     = preprint truth (PDF + LaTeX source)
PubMed    = biomedical truth (MeSH, identifiers)
Europe PMC = biomedical OA text
Open Library = book catalog
IA        = book/archived text
Gutenberg = public domain text
```

**Rule:** Citation count ≠ truth. OpenAlex citation graph is attention, not evidence. S2 influence signals are derived, not primary.

---

## PHASE 2 — IDENTITY GRAPH

### Identity Hierarchy (priority order)

```
1. DOI          → registered scholarly works (Crossref = truth)
2. PMID/PMCID   → biomedical works (PubMed = truth)
3. arXiv ID     → arXiv versions (arXiv = truth)
4. OpenAlex ID  → cross-domain graph identity
5. S2 ID        → enrichment identity
6. ISBN         → books (Open Library = truth)
7. ORCID        → persons (where available)
8. ROR          → institutions (where available)
9. Internal UUID → every entity and evidence artifact
```

### Resolution Strategy

```
Provider IDs
     ↓
Canonical Identity
  (internal UUID + primary external ID)
     ↓
Witness Record
  (resolution method, confidence, competing candidates, timestamp)
```

**Never overwrite identity conflicts.** Store provider assertions separately. Create resolved internal identity with:
- resolver version
- matching method (exact / fuzzy / embedding similarity)
- confidence score (0.0–1.0)
- competing candidates
- timestamp
- human override status
- witness result

### Cross-Provider Resolution Rules

| ID Pair | Resolution Method | Confidence Threshold |
|---|---|---|
| DOI ↔ OpenAlex | Exact match (OpenAlex stores DOI) | 1.0 |
| DOI ↔ S2 | Exact match (S2 stores DOI) | 1.0 |
| PMID ↔ DOI | Crossref/OpenAlex bidirectional | 0.95 |
| arXiv ID ↔ DOI | OpenAlex (arXiv papers get DOI) | 0.9 |
| ISBN ↔ Open Library | Open Library exact match | 1.0 |
| Author name ↔ ORCID | Disambiguation (S2/OpenAlex) | 0.8 (human review if <0.9) |
| Institution name ↔ ROR | Fuzzy match + country | 0.7 (human review if <0.85) |

---

## PHASE 3 — RESEARCH MEMORY (M0–M6)

| Class | Contents | Write Authority | Retention | Trust State |
|---|---|---|---|---|
| M0 Cache | Provider responses, search results, parsed metadata | System | Expirable (7 days) | Untrusted/retrieved |
| M1 Evidence Vault | Source snapshots, files, spans, hashes, licenses | Ingestion pipeline | Durable under policy | Evidence-bearing |
| M2 Research Workspace | Questions, search protocols, screening, extraction, notes | Hermes with human visibility | Versioned | Pending |
| M3 Claim Graph | Structured claims and relationships | Research engine; human review for status changes | Durable | Pending/reviewed |
| M4 Synthesis Register | Literature reviews, briefings, decision packets | Human ratification | Durable, versioned | Ratified or superseded |
| M5 Constitutional Memory | Research policy, source registry, evidence standards | AAA + human sovereign only | Durable | Governed |
| M6 Witness Ledger | Hashes, validation results, approvals, provenance | `/999` append-only | Durable | Witnessed |

### Storage Mapping

| Memory Class | Storage Backend | Why |
|---|---|---|
| M0 Cache | Qdrant (ephemeral collection) | Fast vector retrieval; disposable |
| M1 Evidence Vault | MinIO (objects) + PostgreSQL (metadata) | Immutable files + structured metadata |
| M2 Research Workspace | PostgreSQL (versioned tables) | Transactional; queryable |
| M3 Claim Graph | FalkorDB (graph) + PostgreSQL (constraints) | Relationship traversal + integrity |
| M4 Synthesis Register | PostgreSQL + MinIO (export packets) | Structured + portable |
| M5 Constitutional Memory | PostgreSQL (governed tables) | Audit trail |
| M6 Witness Ledger | PostgreSQL (vault999_witness) + VAULT999 files | Append-only; dual write |

---

## PHASE 4 — EVIDENCE LEDGER SPEC

### Evidence Object Schema

```json
{
  "evidence_id": "uuid",
  "work_id": "uuid (FK → works)",
  "source_provider": "openalex|crossref|s2|core|arxiv|pubmed|europe_pmc|openlibrary|ia|gutenberg",
  "external_ids": {
    "doi": "10.xxxx/xxxxx",
    "pmid": "12345678",
    "pmcid": "PMC12345678",
    "openalex": "W12345678",
    "arxiv": "2401.12345",
    "s2": "S2PaperId"
  },
  "retrieved_at": "ISO-8601",
  "source_url": "https://...",
  "content_hash": "sha256:...",
  "license_status": "CC-BY|CC0|OA-unknown|restricted|public-domain|publisher-TOS",
  "version_status": "preprint|accepted-manuscript|version-of-record",
  "locator": {
    "page": null,
    "section": "Results",
    "paragraph": 3,
    "table": null,
    "figure": null
  },
  "verbatim_text": "exact quoted text from source",
  "normalized_claim_ids": ["claim-uuid-1", "claim-uuid-2"],
  "extractor": {
    "pipeline_version": "1.0.0",
    "model": "i-arif",
    "prompt_hash": "sha256:..."
  },
  "trust_state": "machine_extracted_pending_review"
}
```

### Trust State Machine

```
machine_extracted_pending_review
    ↓ human review
human_reviewed_accepted
    ↓ ratification
ratified_evidence
    ↓ supersession
superseded_evidence
    ↓ retraction
retracted_evidence
```

### Evidence Rules

1. No evidence may exist without provenance
2. No evidence may be promoted without human review
3. All evidence carries a content hash (SHA-256)
4. Evidence is append-only (no mutation; supersede instead)
5. Full text stored only when license permits; otherwise store excerpts + hashes + links
6. RO-Crate export format for portability

---

## PHASE 5 — RESEARCH GRAPH MODEL

### Entity Types

```
Paper
Book
Author
Institution
Funder
Journal
Dataset
Claim
Evidence
```

### Relationship Types

```
CITES           (Paper → Paper, with context)
AUTHORED_BY     (Paper → Author)
AFFILIATED_WITH (Author → Institution)
FUNDED_BY       (Paper → Funder)
PUBLISHED_IN    (Paper → Journal)
SUPPORTS        (Claim → Claim, with evidence)
CONTRADICTS     (Claim → Claim, with evidence)
QUALIFIES       (Claim → Claim, with scope)
SUPERSEDES      (Work → Work, with version)
EXTRACTED_FROM  (Evidence → Work)
```

### Graph Storage: FalkorDB

```
Research Graph (NEW)
├── Paper nodes: {uuid, doi, title, year, source}
├── Author nodes: {uuid, orcid, name, h_index}
├── Institution nodes: {uuid, ror, name, country}
├── Claim nodes: {uuid, subject, predicate, object, polarity, confidence}
├── Evidence nodes: {uuid, content_hash, trust_state, locator}
├── CITES edges: {context, source_provider, retrieved_at}
├── SUPPORTS/CONTRADICTS edges: {relation_type, confidence, evidence_ids}
└── AUTHORED_BY edges: {position, corresponding}
```

### Graph Size Projections

| Graph | Nodes (initial) | Edges (initial) | Growth Rate |
|---|---|---|---|
| Citation | 1,000 | 5,000 | Per research question |
| Claim | 0 | 0 | Per evidence extraction |
| Author | 500 | 2,000 | Slow |
| Institution | 100 | 500 | Slow |

---

## PHASE 6 — CONTRADICTION ENGINE

### Typed Contradiction Relations

| Relation | Meaning | Example |
|---|---|---|
| CONTRADICTS | Direct empirical contradiction | "X increases Y" vs "X decreases Y" |
| QUALIFIES | Narrows scope or condition | "X increases Y in adults" vs "X has no effect in children" |
| SCOPE_DIVERGES | Different populations/settings | Different basins, different stratigraphy |
| METHOD_DIVERGES | Different measurement approaches | Different analytical methods yield different results |
| TEMPORALLY_SUPERSEDED | Newer evidence updates older | Preprint corrected by peer-reviewed version |
| INCOMPARABLE | Cannot be meaningfully compared | Different scales, different properties |
| INSUFFICIENT_EVIDENCE | Not enough data to judge | Single study vs established consensus |

### Contradiction Detection Pipeline

```
1. Extract claims from evidence
   → subject + predicate + outcome + polarity + scope + method + time

2. Link each claim to exact source spans
   → paper/version + section + page/paragraph + content hash

3. Cluster claims by comparable question
   → same target, outcome, scale, context

4. Detect candidate disagreement
   → opposite polarity, incompatible ranges, incompatible causal assertions

5. Test comparability
   → sample, geography, age, method, resolution, confounders, statistical design

6. Assign relation
   → CONTRADICTS / QUALIFIES / SCOPE_DIVERGES / METHOD_DIVERGES /
     TEMPORALLY_SUPERSEDED / INCOMPARABLE / INSUFFICIENT_EVIDENCE

7. Produce review queue
   → NO contradiction is elevated without human review
```

### Geological Adaptation

For geoscience work (Arif's domain), contradiction detection must carry scale explicitly:

- "Reservoir quality improves basinward" vs "reservoir quality degrades basinward" may BOTH be true if they refer to different stratigraphic intervals, depositional facies, burial histories, or property measures.
- Hermes must model qualifiers (basin, formation, facies, depth, property) rather than label premature contradictions.

---

## PHASE 7 — CONSENSUS ENGINE

### Consensus ≠ Majority Vote

```
Consensus is NOT: "70% of papers say X"
Consensus IS: "11 independent research groups, using 4 different methods, across
3 basins, converge on X — but 2 studies in a different tectonic setting disagree,
and their methodology is sound but their scope is narrower."
```

### Consensus Components

| Component | What it measures |
|---|---|
| Direction | Which way the evidence points |
| Conditional scope | Where the consensus applies |
| Evidence-weighted convergence | Weight by study quality, sample size, independence |
| Minority dissent | High-quality papers that disagree |
| Unresolved gaps | What the evidence doesn't cover |
| Temporal evolution | How consensus has changed over time |
| Confidence band | PLAUSIBLE / PROBABLE / ESTABLISHED / CONTESTED |

### Confidence Classification

| Level | Meaning | Requirement |
|---|---|---|
| INSUFFICIENT | Not enough evidence | <3 independent studies |
| PLAUSIBLE | Directionally supported | 3+ studies, same direction, some quality |
| PROBABLE | Strong convergence | 5+ independent groups, consistent methods |
| ESTABLISHED | Robust consensus | 10+ groups, multiple methods, no unresolved contradictions |
| CONTESTED | Active disagreement | Quality evidence on both sides |

---

## PHASE 8 — LITERATURE REVIEW ENGINE

### Review Pipeline

```
1. QUESTION
   → PICO/PECO format or domain equivalent
   → Target system, geography, method, outcome, date window, languages
   → Inclusion/exclusion criteria
   → Intended decision use

2. SEARCH PROTOCOL
   → Provider queries (OpenAlex, Crossref, S2, CORE, PubMed, arXiv)
   → Query hash for reproducibility
   → Timestamp per provider

3. CORPUS GENERATION
   → Multi-provider search
   → Deduplication (DOI-first, then title similarity)
   → Version tracking (preprint → published)
   → Corpus manifest with provider + query + timestamp

4. SCREENING
   → Title/abstract screening (automated + human)
   → Full-text screening (when needed)
   → Inclusion/exclusion decisions with reasons
   → Screening audit trail

5. EVIDENCE EXTRACTION
   → Exact spans from papers
   → Claims, methods, populations, outcomes, limitations
   → Extraction model + prompt version

6. CLAIM ANALYSIS
   → Normalize claims
   → Build claim graph
   → Detect contradictions
   → Assess evidence quality

7. SYNTHESIS
   → Evidence tables
   → Contradiction summary
   → Consensus assessment
   → Uncertainty disclosure
   → Blind spots identified

8. REVIEW PACKET
   → Question and scope
   → Search protocol + queries
   → Corpus manifest + dedup log
   → Screening decisions
   → Evidence tables
   → Claim graph
   → Contradictions
   → Synthesis
   → Citations
   → Known blind spots
   → Provenance hashes
   → Witness report

9. WITNESS VALIDATION
   → Source traceability
   → Hash integrity
   → Citation completeness
   → Claim provenance
   → Reproducibility check

10. HUMAN RATIFICATION
    → Arif reviews and approves/corrects
    → Review packet sealed to VAULT999
    → Published to M4 Synthesis Register
```

---

## PHASE 9 — HERMES RESEARCH MCP SPECIFICATION

### Single Canonical MCP: `hermes-research`

**NOT one MCP per provider.** One MCP with typed, read-only tools. The MCP is the outward-facing protocol adapter over a sovereign research substrate.

### Tool Contract

| Tool | Purpose | Mutation | Output |
|---|---|---|---|
| `search_works` | Multi-provider corpus search | No | Results with source, license, retrieval timestamp |
| `resolve_work` | DOI/PMID/arXiv/ISBN/OpenAlex ID resolution | No | Canonical IDs, confidence, source records |
| `get_work_graph` | Citations, references, related works | No | Edges with provider provenance |
| `get_entity_profile` | Author, institution, venue, funder profile | No | Entity IDs, disambiguation confidence |
| `locate_open_text` | Find lawful OA copies | No | URL, license, host, checksum |
| `retrieve_evidence` | Fetch/store evidence snapshot | Internal append-only | Content hash, source ID, rights status |
| `extract_claims` | Produce candidate claims with exact spans | No | Claim objects marked pending |
| `compare_claims` | Find support, contradiction, divergence | No | Typed relations + evidence links |
| `build_review_packet` | Create reproducible literature review | Internal append-only | Corpus manifest, methods, citations, uncertainty |
| `verify_review_packet` | `/999` witness validation | No | Pass/warn/fail + missing evidence |

### Anti-Tools (must NOT exist in initial MCP)

- No `browse_url` (unrestricted web access)
- No `execute_code` (arbitrary execution)
- No `download_any_pdf` (SSRF risk)
- No `write_zotero` (mutation without approval)
- No `promote_memory` (knowledge promotion without F13)
- No `install_mcp` (supply chain risk)

### MCP Server Architecture

```
hermes-research (Python/TypeScript)
  │
  ├── Provider Router
  │   ├── OpenAlex Adapter (REST, no auth)
  │   ├── Crossref Adapter (REST, polite pool)
  │   ├── S2 Adapter (REST, free key)
  │   ├── CORE Adapter (REST, free key)
  │   ├── arXiv Adapter (REST, rate-limited)
  │   ├── PubMed Adapter (E-utilities, no auth)
  │   ├── Europe PMC Adapter (REST, no auth)
  │   ├── Open Library Adapter (REST, no auth)
  │   └── Gutenberg Adapter (REST, no auth)
  │
  ├── Identity Resolver
  │   └── Cross-provider ID mapping
  │
  ├── Evidence Store
  │   └── PostgreSQL + MinIO integration
  │
  ├── Claim Engine
  │   └── Extraction + contradiction + consensus
  │
  └── Witness Interface
      └── Hash verification + provenance check
```

---

## PHASE 10 — AAA INTEGRATION

### Capability Registration

| Capability | Authority | Risk Level | Quota | Witness |
|---|---|---|---|---|
| KNOWLEDGE_DISCOVERY | Hermes (read-only) | Low | 10K queries/day | None (read-only) |
| EVIDENCE_EXTRACTION | Research substrate | Medium | 1K extractions/day | Hash verification |
| CLAIM_ANALYSIS | Research engine | Medium | 500 analyses/day | Human review queue |
| CONTRADICTION_ANALYSIS | Research engine | High | 100 analyses/day | Human review + `/999` |
| CONSENSUS_ANALYSIS | Research engine | High | 50 analyses/day | Human review + `/999` |
| REVIEW_GENERATION | Hermes + Research | High | 10 reviews/day | `/999` witness required |

### Authority Map

```
ARIF → approves capability activation, authorizes mutations, ratifies knowledge
AAA → issues bounded research contracts, grants tool scope, registers providers
HERMES → queries read-only capabilities, builds pending packets, presents uncertainty
RESEARCH SUBSTRATE → stores evidence, resolves claims, detects contradictions
/999 → verifies lineage, coverage, hashes, policy compliance
```

### Escalation Rules

| Event | Escalation |
|---|---|
| New provider added | AAA registration → Arif approval |
| Mutation to evidence | HOLD → Arif approval |
| Contradiction detected | Research engine proposes → Human review |
| Review packet ready | `/999` witness → Arif ratification |
| Knowledge promoted | 888 HOLD → Arif ratification |
| Provider outage | Automatic fallback → log + notify |
| Rate limit exceeded | Queue + backoff → log |

---

## PHASE 11 — WITNESS PROTOCOL

### /999 Verification Checklist

For every review packet before ratification:

| Check | Method | Pass Condition |
|---|---|---|
| Source traceability | Every claim → evidence → work → source | 100% traceable |
| Hash integrity | SHA-256 of evidence objects matches stored | All hashes match |
| Citation completeness | All cited works exist in works table | 0 orphans |
| Claim provenance | Every claim has evidence_id + locator | 100% linked |
| Reproducibility | Search protocol can replay | Queries return same corpus |
| Rights compliance | Evidence storage matches license | No violations |
| Contradiction disclosure | All detected contradictions listed | Nothing hidden |
| Uncertainty disclosure | Confidence levels stated for all claims | No false certainty |

### Witness Report Format

```json
{
  "review_packet_id": "uuid",
  "witness_timestamp": "ISO-8601",
  "checks": [
    {"check": "source_traceability", "status": "PASS|WARN|FAIL", "detail": "..."},
    {"check": "hash_integrity", "status": "PASS|WARN|FAIL", "detail": "..."},
    {"check": "citation_completeness", "status": "PASS|WARN|FAIL", "detail": "..."},
    {"check": "claim_provenance", "status": "PASS|WARN|FAIL", "detail": "..."},
    {"check": "reproducibility", "status": "PASS|WARN|FAIL", "detail": "..."},
    {"check": "rights_compliance", "status": "PASS|WARN|FAIL", "detail": "..."},
    {"check": "contradiction_disclosure", "status": "PASS|WARN|FAIL", "detail": "..."},
    {"check": "uncertainty_disclosure", "status": "PASS|WARN|FAIL", "detail": "..."}
  ],
  "overall_status": "PASS|WARN|FAIL",
  "missing_evidence": [],
  "warnings": [],
  "witness_hash": "sha256:..."
}
```

---

## PHASE 12 — EMERGENCE ANALYSIS

### Stage 0: Search (CURRENT STATE)

```
Capability: Find papers by keyword
Infrastructure: Web search (SearXNG, Brave, Exa)
Failure modes: No scholarly metadata, no citation awareness
Governance: None needed (read-only web search)
```

### Stage 1: Research Retrieval

```
New capability: Structured scholarly search with dedup, version tracking, rights
Infrastructure: 9 provider adapters + PostgreSQL works table + Qdrant vector index
Failure modes: Provider outage, rate limits, metadata conflicts, wrong dedup
Governance: Source registry, rate policy, read-only scope
Required for: Everything below
```

### Stage 2: Evidence Intelligence

```
New capability: Extract exact claims from papers with evidence spans
Infrastructure: Evidence objects, content hashing, locator model
Failure modes: Extraction error, hallucinated claims, wrong attribution
Governance: Machine-pending trust state, human review gate
```

### Stage 3: Citation Intelligence

```
New capability: Trace influence chains, find primary sources, map citation networks
Infrastructure: Citation edges in FalkorDB, citation graph queries
Failure modes: Incomplete citation coverage, wrong influence interpretation
Governance: Citation ≠ truth invariant
```

### Stage 4: Contradiction Intelligence

```
New capability: Discover WHY studies disagree (not just THAT they disagree)
Infrastructure: Claim graph, typed relations, comparability model
Failure modes: False contradictions, scope collapse, premature labeling
Governance: Human review queue for all contradictions
```

### Stage 5: Consensus Intelligence

```
New capability: Evidence-weighted consensus with uncertainty disclosure
Infrastructure: Consensus engine, confidence classification
Failure modes: False consensus, suppressed dissent, majority fallacy
Governance: Confidence levels require evidence justification
```

### Stage 6: Research Memory

```
New capability: Remember questions, corpuses, evidence, claims, reviews
Infrastructure: M0-M6 memory classes, provenance lineage
Failure modes: Memory corruption, stale evidence, provenance loss
Governance: Memory classes with retention policies
```

### Stage 7: Institutional Knowledge

```
New capability: Corporate research department + literature review team + citation analyst + knowledge graph
Infrastructure: All prior stages + AAA integration + production operation
Failure modes: Governance bypass, knowledge promotion without ratification
Governance: Full APEX-ZEN governance chain
```

### Stage 8: Collective Scientific Reasoning

```
New capability: Cross-domain synthesis, methodological meta-analysis, research frontier detection
Infrastructure: All prior stages + cross-domain graph queries + temporal evolution
Failure modes: Overreach, false synthesis, domain confusion
Governance: Maximum restraint; all output requires human review
```

**This stage is aspirational.** It requires all prior stages to be operational and validated.

---

## EMERGENCE VERDICT

```json
{
  "epoch": "ARIFOS::HERMES_RESEARCH_SUBSTRATE::EXECUTION::v1",
  "dS": "reduced: complete architecture designed, schemas specified, MCP contract defined",
  "peace2": 1.0,
  "kappa_r": "bounded by phased implementation with gates",
  "shadow": [
    "Implementation complexity underestimated",
    "Provider API changes may break adapters",
    "Extraction quality depends on model capability",
    "Contradiction detection requires domain expertise",
    "Full emergence (Stage 8) is multi-year aspiration"
  ],
  "confidence": 0.85,
  "psi_le": "Architecture complete; requires F13 ratification before Phase 1 implementation",
  "verdict": "PARTIAL",
  "witness": {
    "human": "ARIF — required for architecture ratification",
    "ai": "Hermes — designed architecture; no implementation executed",
    "earth": "Provider API documentation, existing infrastructure audit, PostgreSQL/Qdrant/FalkorDB state"
  },
  "qdf": "No installation. No mutation. No config changes. Architecture package for judgment."
}
```

DITEMPA BUKAN DIBERI ⚒️
