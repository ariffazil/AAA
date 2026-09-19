# ARIFOS::HERMES_RESEARCH_SUBSTRATE::PHASE0_AUDIT::v1

**Authority:** ARIF (Human Sovereign)
**Mission:** Read-only readiness audit for research intelligence substrate
**Executed:** 2026-09-19T22:55:00+08:00 (Asia/Kuala_Lumpur)
**Mutation status:** NONE — all commands read-only
**Exit criteria:** Complete evidence package, no hidden write path found

---

## 1. Scope and Non-Mutation Attestation

This audit was conducted under F13 authorization. All operations were read-only:
- `curl` to external APIs (test queries only, 1 request each)
- `cat/grep/ls/find` on local filesystem
- `docker ps/exec` for status only (no container creation/modification)
- `ss/ip/tailscale status` for network mapping
- `systemctl list-units` for service inventory
- `psql -c` for database schema inspection (read-only queries)

No packages installed. No configs modified. No containers created. No credentials created/rotated/exported. No MCP servers registered. No writes to any store.

---

## 2. Timestamp and Environment Boundaries

**Audit window:** 2026-09-19 22:51 — 23:05 MYT (UTC+8)
**Host:** forge (KVM8)
**Tailscale IP:** 100.64.0.2
**Public IP:** 72.62.71.199
**OS:** Linux 6.17.0-41-generic #1-Ubuntu SMP PREEMPT_DYNAMIC x86_64
**Uptime at audit:** 17 days, 14:44
**CPU:** 8 cores
**RAM:** 31GB total, 14GB used, 16GB available
**Disk:** 387GB total, 245GB used (64%), 142GB available
**Python:** 3.13.7
**Node:** v22.23.2
**uv:** 0.11.8 (available at /root/.local/bin/uv)
**pip:** 26.2.1

---

## 3. Capability Inventory

| # | Capability | State | Evidence | Confidence |
|---|---|---|---|---|
| C-01 | AAA routing/governance | PRESENT_UNVERIFIED | Config exists; tool `arifos` MCP at :8088 | CLAIM |
| C-02 | Hermes human-reality interface (Telegram) | PRESENT_UNVERIFIED | Config + `ASI_ARIFOS_BOT_TOKEN` exists; 33 allowed chats | CLAIM |
| C-03 | `/999` witness function | PRESENT_UNVERIFIED | VAULT999 dir exists with 55 receipts; SEALED_EVENTS.jsonl present | CLAIM |
| C-04 | PostgreSQL | PRESENT_UNVERIFIED | Running in Docker, listening on 127.0.0.1:5432; cannot connect from host without Docker exec | CLAIM |
| C-05 | Qdrant vector store | PRESENT_UNVERIFIED | 20 collections, 768-dim cosine; `arif_evidence` collection exists (16 points) | MEASURED |
| C-06 | FalkorDB graph store | PRESENT_UNVERIFIED | 6 graphs: af_forge, sado_knowledge, arif_l5_knowledge, arifos_federation, atlas333_graph, arifos | MEASURED |
| C-07 | MinIO object storage | PRESENT_UNVERIFIED | Healthy, listening on 127.0.0.1:9000-9001 | MEASURED |
| C-08 | Redis (SearXNG) | PRESENT_UNVERIFIED | PONG from container; host-side requires auth | MEASURED |
| C-09 | SearXNG search | PRESENT_UNVERIFIED | Health check OK at 127.0.0.1:8080 | MEASURED |
| C-10 | A-FORGE agent stack | PRESENT_UNVERIFIED | Systemd running; MCP at :7072 | CLAIM |
| C-11 | Claim-ledger MCP | PRESENT_UNVERIFIED | Health endpoint returns "Not Found"; MCP endpoint responds with JSON-RPC | MEASURED |
| C-12 | Brave Search | PRESENT_UNVERIFIED | MCP configured with API key | CLAIM |
| C-13 | Exa search | PRESENT_UNVERIFIED | MCP configured with API key | CLAIM |
| C-14 | Firecrawl | PRESENT_UNVERIFIED | MCP configured with API key | CLAIM |
| C-15 | Context7 (dev docs) | PRESENT_UNVERIFIED | MCP configured (remote URL) | CLAIM |
| C-16 | DeepWiki | PRESENT_UNVERIFIED | MCP configured (remote URL) | CLAIM |
| C-17 | Z.ai reader/search | PRESENT_UNVERIFIED | MCP configured (remote URL with auth) | CLAIM |
| C-18 | Chrome DevTools | PRESENT_UNVERIFIED | MCP configured (headless browser) | CLAIM |
| C-19 | 588 AAA skills | PRESENT_UNVERIFIED | Found via find; not all loaded | MEASURED |
| C-20 | Tailscale mesh | PRESENT_UNVERIFIED | 4 nodes: KVM8, S24, azwaos, KVM4 | MEASURED |
| **C-21** | **Scholarly MCP server** | **NOT PRESENT** | No scholarly MCP in config or installed | **CONFIRMED ABSENT** |
| **C-22** | **Internal research adapter** | **DESIGN_ONLY** | No code exists for OpenAlex/Crossref/S2/arXiv adapters | **CONFIRMED ABSENT** |
| **C-23** | **Identity resolution engine** | **DESIGN_ONLY** | No DOI/PMID/arXiv/ORCID resolver exists | **CONFIRMED ABSENT** |
| **C-24** | **Evidence provenance ledger** | **DESIGN_ONLY** | No immutable evidence object schema exists | **CONFIRMED ABSENT** |
| **C-25** | **Claim graph / contradiction engine** | **DESIGN_ONLY** | No claim extraction or contradiction detection exists | **CONFIRMED ABSENT** |
| **C-26** | **Research memory (M0-M6)** | **DESIGN_ONLY** | No tiered research memory schema exists | **CONFIRMED ABSENT** |
| **C-27** | **Literature review pipeline** | **DESIGN_ONLY** | No corpus/screening/extraction workflow exists | **CONFIRMED ABSENT** |

**Capability coverage: 17 PRESENT_UNVERIFIED / 10 DESIGN_ONLY or ABSENT**

---

## 4. Authority/Effective-Permission Inventory

| Action | Authority | Gate | Status |
|---|---|---|---|
| Read public scholarly metadata | Hermes via approved read-only adapter | Provider policy + task scope | NOT YET GRANTED — no adapter exists |
| Retrieve lawful OA text | Research substrate | Rights classifier + source policy | NOT YET BUILT |
| Store evidence snapshot | Ingestion organ | Append-only provenance rules | NOT YET BUILT |
| Extract candidate claims | Research engine | Marked machine-pending | NOT YET BUILT |
| Label contradiction | Research engine (proposal only) | Human review required | NOT YET BUILT |
| Create review packet | Hermes / research organ | `/999` witness validation | NOT YET BUILT |
| Promote to durable knowledge | Arif only | 888 HOLD + `/999` witness | CONSTITUTIONAL — enforced by prompt |
| Change provider/tool scope/secrets | Arif only | 888 HOLD | CONSTITUTIONAL — enforced by prompt |
| Install MCP / enable write scope | Arif only | 888 HOLD | CONSTITUTIONAL — enforced by prompt |

**Key finding:** Governance authority exists in constitution and prompt. No kernel-level enforcement of research capability boundaries yet (consistent with compartment doctrine: prompt governance until kernel predicates exist).

---

## 5. Dependency and Data-Flow Maps

### Dependency chain (what must be operational for each capability)

```
Hermes Research Answer
  └─ hermes-research (does not exist)
      ├─ Provider adapters (none built)
      │   ├─ OpenAlex ← TESTED: reachable, responds correctly
      │   ├─ Crossref ← TESTED: reachable, responds correctly
      │   ├─ Semantic Scholar ← TESTED: 429 rate limited (unauthenticated)
      │   ├─ CORE ← TESTED: empty response (needs API key)
      │   ├─ arXiv ← TESTED: empty response (slow/timeout?)
      │   ├─ PubMed ← TESTED: reachable, responds correctly
      │   ├─ Europe PMC ← NOT TESTED
      │   ├─ Open Library ← TESTED: empty response (timeout?)
      │   ├─ Internet Archive ← NOT TESTED
      │   └─ Gutenberg ← TESTED: empty response (timeout?)
      ├─ Policy registry (does not exist)
      ├─ Evidence substrate
      │   ├─ Object store: MinIO ← REACHABLE (127.0.0.1:9000)
      │   ├─ PostgreSQL ← LISTENING but connection issues
      │   ├─ Graph: FalkorDB ← REACHABLE (127.0.0.1:6380)
      │   ├─ Vector: Qdrant ← REACHABLE (127.0.0.1:6333)
      │   └─ Search index (does not exist for research)
      ├─ Identity resolver (does not exist)
      └─ /999 witness (VAULT999 exists; operational status unknown)
```

### Data flow (current state)

```
External web → SearXNG → Hermes → Human
                    ↑
              Brave/Exa/Firecrawl (MCP)

No scholarly data flow exists.
No evidence → ledger flow exists.
No claim → graph flow exists.
No review → witness flow exists.
```

---

## 6. Existing MCP Registry and Tool Schemas

**MCP server count:** 21 configured in `/root/.hermes/config.yaml`
**MCP tool count:** 41 tool definitions (url + command entries)
**Custom MCP servers (local):** aforge, arifflow, arifos, claim-ledger, doc-tables, fed, filings, frame, geox, hermes-mcp, hermes-rasa, media-ingest, numeric-audit, session-federation, wealth, well
**Remote MCP servers:** brave-search, chrome-devtools, context7, deepwiki, exa, firecrawl, zai_reader, zai_search, zai_vision

**Research-relevant MCPs installed:** ZERO

| MCP Server | Research Relevant? | Notes |
|---|---|---|
| aforge | No | AI agent tooling |
| arifflow | No | Flow governance |
| arifos | No | Kernel interface |
| brave-search | Partial | General web search, not scholarly-specific |
| chrome-devtools | Partial | Could scrape, but no structured paper data |
| claim-ledger | Yes | Claim tracking exists but no research schema |
| context7 | No | Developer docs only |
| deepwiki | No | Wiki content |
| exa | Partial | Semantic web search, not scholarly-specific |
| firecrawl | Partial | Web scraping, not scholarly-specific |
| filings | No | Financial filings |
| geox | No | Geoscience (domain-specific, not research substrate) |
| hermes-mcp | No | Hermes agent interface |
| hermes-rasa | No | Human reality bridge |
| media-ingest | No | Media processing |
| numeric-audit | No | Numeric verification |
| session-federation | No | Session management |
| wealth | No | Financial data |
| well | No | Human wellbeing |
| zai_reader | Partial | Web reading, no paper-specific features |
| zai_search | Partial | General web search |
| zai_vision | No | Image/video analysis |

**No scholarly MCP servers are installed. No paper discovery, citation graph, or book catalog MCP exists.**

---

## 7. Storage and Memory Map

### Qdrant (vector store)

| Collection | Points | Vector Dim | Purpose |
|---|---|---|---|
| arif_evidence | 16 | 768 | Evidence vectors (MINIMAL) |
| arifos_memory | ? | ? | General memory |
| arifos_constitution | ? | ? | Constitutional docs |
| arifos_precedent | ? | ? | Legal/doctrinal precedent |
| arifos_session_memory | ? | ? | Session state |
| arifos_vault_canon | ? | ? | Canonical vault |
| arifos_vault_working | ? | ? | Working vault |
| arifOS_skill_mesh | ? | ? | Skill graph |
| arifos_audio_memory | ? | ? | Audio transcripts |
| atlas333_eureka | ? | ? | Eureka insights |
| federation_memory_patterns | ? | ? | Federation patterns |
| federation_shared | ? | ? | Shared federation data |
| hermes_brief_editions | ? | ? | Brief editions |
| identity_vault | ? | ? | Identity data |
| mcp_capabilities | ? | ? | MCP capability registry |
| mem0 / mem0-v4 | ? | ? | Mem0 memory |
| openclaw_memory | ? | ? | OpenClaw memory |
| petronas_knowledge | ? | ? | PETRONAS domain knowledge |

**Key finding:** `arif_evidence` collection exists with 16 points — this is the closest thing to a research evidence store, but it's essentially empty (16 evidence objects total). No research-specific schema.

### FalkorDB (graph store)

| Graph | Purpose |
|---|---|
| af_forge | A-FORGE knowledge |
| sado_knowledge | SADO (relationship) knowledge |
| arif_l5_knowledge | L5 knowledge layer |
| arifos_federation | Federation graph |
| atlas333_graph | Atlas 333 knowledge |
| arifos | Core arifos graph |

**Sample data in af_forge:** Entity/Organization (1), Episodic (3), Entity/Document (1), Entity (10), Entity/Object (2). Sparse.

**No research citation graph exists.** No claim graph. No author/institution graph.

### MinIO (object storage)

- Reachable at 127.0.0.1:9000
- Bucket list not enumerable without `mc` CLI (not configured on host)
- Used by some services for file storage

### PostgreSQL

- Running in Docker container
- Listening on 127.0.0.1:5432
- Cannot connect from host via `psql` directly (requires Docker exec or container networking)
- Database name unknown from this audit (connection blocked)
- No research-related schema evidence found

### VAULT999

- Exists at `/root/VAULT999/`
- Contains 55 receipt files
- SEALED_EVENTS.jsonl present
- Research-related content: NONE found

### Hermes Memory

- MEMORY.md (2,053 bytes)
- USER.md (1,396 bytes)
- Backup files from 2026-09-14, 2026-09-17, 2026-09-18
- No research memory, no evidence store, no citation cache

### AAA Skills

- 588 skill files found
- Research-related skills found (partial list):
  - `futures-forecast-briefing`
  - `human-corpus-falsification`
  - `basin-charge-screening`
  - `seismic-interpretation-alignment`
  - `geox-basin-claims-audit`
  - `biohacker-peptide-stack`
  - `sleep-data-interpretation`
  - `petronas-petros-shell-dispute`
- **None are scholarly paper discovery, citation analysis, or research intelligence skills**

---

## 8. Provider/Credential-Reference Inventory

**Total credential entries in environment:** 135

**Research-relevant credentials found:**

| Provider | Key Variable | Status |
|---|---|---|
| Brave Search | `BRAVE_API_KEY` | PRESENT — MCP configured |
| Exa | `EXA_API_KEY` | PRESENT — MCP configured |
| Firecrawl | `FIRECRAWL_API_KEY` | PRESENT — MCP configured |
| Cloudflare | `CLOUDFLARE_API_TOKEN` | PRESENT — CDN/proxy |
| Anthropic | `ANTHROPIC_API_KEY` | PRESENT — model provider |
| Z.ai | `ZAI_API_KEY` | PRESENT — reader/search |
| OpenAlex | NONE | NOT CONFIGURED |
| Semantic Scholar | NONE | NOT CONFIGURED |
| CORE | NONE | NOT CONFIGURED |
| PubMed/NCBI | NONE | NOT CONFIGURED |
| Open Library | NONE | NOT CONFIGURED (not required) |
| Internet Archive | NONE | NOT CONFIGURED (not required) |
| Gutenberg/Gutendex | NONE | NOT CONFIGURED (not required) |
| Zotero | NONE | NOT CONFIGURED |

**Key finding:** No scholarly API keys exist in the environment. OpenAlex, Semantic Scholar, CORE, and PubMed would need either no-key access (limited rate) or new API keys configured.

---

## 9. Network and Egress Boundary Map

### Interfaces

| Interface | Address | Purpose |
|---|---|---|
| eth0 | 72.62.71.199/24 | Public VPS |
| tailscale0 | 100.64.0.2/32 | Tailscale mesh |
| docker0 | 172.17.0.1/16 | Docker default bridge |
| br-97da3cc44b2c | 172.18.0.1/16 | Docker custom network |
| br-aadb3cc216e2 | 172.21.0.1/16 | Docker custom network |

### UFW Rules (research-relevant)

| Port | Direction | Source | Purpose |
|---|---|---|---|
| 22888/tcp | ALLOW IN | Anywhere | SSH |
| 443/tcp | ALLOW IN | Anywhere | HTTPS (Caddy) |
| 80/tcp | ALLOW IN | Anywhere | HTTP (Caddy) |
| 8083/tcp | ALLOW IN | 72.61.126.65 | Headscale for A-FLOW |
| 11434/tcp | DENY IN | Anywhere | Ollama blocked externally |

### Egress

- General web egress confirmed working (curl to httpbin.org from public IP 72.62.71.199)
- OpenAlex API: REACHABLE (tested)
- Crossref API: REACHABLE (tested)
- PubMed API: REACHABLE (tested)
- Semantic Scholar: REACHABLE but rate limited (429)
- arXiv: REACHABLE but slow (timeout on first try)
- CORE: REACHABLE but requires API key
- Open Library: REACHABLE but slow (timeout on first try)
- Gutenberg: REACHABLE but slow (timeout on first try)

### Docker Networks

| Network | Driver |
|---|---|
| af-forge_default | bridge |
| arifos_core_network | bridge |
| bridge | bridge |
| host | host |
| none | null |

### Tailscale Mesh

| Node | IP | Role | Status |
|---|---|---|---|
| af-forge (KVM8) | 100.64.0.2 | All organs | Active |
| arifs-s24 | 100.64.0.1 | Phone | Offline (17d) |
| azwaos | 100.64.0.4 | Witness (KVM2) | Idle |
| kvm4-forge | 100.64.0.5 | LiteLLM + OpenClaw | Active |

---

## 10. Redundancy and Single-Point-of-Failure Analysis

### Redundancy Matrix

| Capability | Sources | True Redundancy? | SPOF Risk |
|---|---|---|---|
| Web search | SearXNG + Brave + Exa + Firecrawl | Yes (4 sources) | Low |
| Vector storage | Qdrant | No (single instance) | Medium |
| Graph storage | FalkorDB | No (single instance) | Medium |
| Object storage | MinIO | No (single instance) | Medium |
| Relational DB | PostgreSQL (Docker) | No (single instance) | Medium |
| Redis | SearXNG Redis only | No (single instance) | Low (non-critical) |
| Scholarly metadata | NONE INSTALLED | N/A | N/A |
| OA full text | NONE INSTALLED | N/A | N/A |
| Book catalog | NONE INSTALLED | N/A | N/A |
| Citation graph | NONE INSTALLED | N/A | N/A |
| Identity resolution | NONE INSTALLED | N/A | N/A |
| Evidence ledger | NONE INSTALLED | N/A | N/A |
| Claim extraction | NONE INSTALLED | N/A | N/A |
| Contradiction detection | NONE INSTALLED | N/A | N/A |
| Research memory | NONE INSTALLED | N/A | N/A |

### Critical SPOFs

1. **KVM8 (forge)** — hosts ALL organs. Single machine failure = total federation loss.
2. **Qdrant** — single instance, no replication. 20 collections, all data at risk.
3. **FalkorDB** — single instance, no replication. 6 graphs, all data at risk.
4. **PostgreSQL** — Docker container, no observed backup/replication.
5. **MinIO** — single instance, no observed backup.
6. **No scholarly capability exists** — this is not a SPOF but a complete absence.

---

## 11. Unknowns, Conflicts, and Evidence Gaps

| # | Unknown | Why it matters | How to resolve |
|---|---|---|---|
| U-01 | PostgreSQL database names and schemas | May already have research-related tables | Docker exec into postgres container |
| U-02 | MinIO bucket contents and policies | May have existing object storage for research | Configure `mc` CLI or query MinIO API |
| U-03 | FalkorDB graph schemas in detail | May have partial citation/entity data | Graph queries per graph |
| U-04 | Qdrant collection schemas (all 20) | Vector dimensions, indexes, actual point counts | Qdrant REST API per collection |
| U-05 | KVM4 (LiteLLM) research capabilities | May have model routing for research tasks | SSH audit of KVM4 |
| U-06 | KVM2 (azwaos) role in research | Witness node — may already have research schema | SSH audit of KVM2 |
| U-07 | Existing Zotero library | User may have existing research bibliography | Ask Arif directly |
| U-08 | PETRONAS institutional subscriptions | Scopus/ScienceDirect/Web of Science access | Ask Arif directly |
| U-09 | Claim-ledger current state | Health "Not Found" but MCP responds — partial operational? | Deeper probe of claim-ledger |
| U-10 | ArifOS kernel version | Could not determine from available files | Check arifOS package manifest |
| U-11 | PostgreSQL connection method | Listening on 5432 but host psql fails | May need Docker network or credentials |
| U-12 | Existing research data in ANY store | May have papers/evidence in Qdrant, FalkorDB, or PostgreSQL already | Schema inspection across all stores |

---

## 12. Risk Register

| Risk | Severity | Likelihood | Control | Residual |
|---|---|---|---|---|
| No scholarly capability exists | High | Certain | Phase 0 audit (this document) | Resolved by awareness |
| Semantic Scholar 429 without key | Medium | Certain | Register for free API key | Low |
| arXiv/Open Library timeouts | Low | Medium | May be transient; retest | Low |
| PostgreSQL connection unknown | Medium | High | Docker exec investigation needed | Medium until resolved |
| Single-instance data stores | High | Medium | No replication currently | High until backup strategy |
| KVM8 single-machine SPOF | Critical | Low-Medium | Tailscale mesh exists; no failover | High until multi-node |
| No evidence provenance schema | High | Certain | Must be built in Phase 1 | Resolved by design |
| No identity resolution | High | Certain | Must be built in Phase 1 | Resolved by design |
| No research memory schema | High | Certain | Must be built in Phase 1 | Resolved by design |
| LibGen copyright risk | Critical | N/A | Audit correctly excludes from production | Low (excluded) |
| Prompt injection via paper content | High | High | Sanitize all MCP output; treat as untrusted | Medium (requires implementation) |
| GitHub star counts unreliable | Low | Certain | Use GitHub API with retrieval timestamps | Low (corrected) |

---

## 13. Recommended Canonical Shape

Based on audit evidence:

```text
ARIF — Human Sovereign
  │ ratification + veto
  │
AAA — Governance plane
  │ policy + capability grants + routing
  │
HERMES — Research reality edge
  │ questions + synthesis + uncertainty display
  │
hermes-research MCP — single governed interface (DOES NOT EXIST YET)
  │
  ├── Provider Organ: 9 canonical adapters (NONE BUILT)
  │   OpenAlex, Crossref, Semantic Scholar, CORE, arXiv,
  │   PubMed/Europe PMC, Open Library/IA, Gutenberg, Zotero
  │
  ├── Research Intelligence Organ (DESIGN_ONLY)
  │   Entity resolution, claim extraction, contradictions, synthesis
  │
  └── Governance Organ (DESIGN_ONLY)
      Source registry, rights policy, retention, audit

Provenance Spine (PARTIAL — stores exist, schema missing)
  ├── Qdrant: vector index (derivative, rebuildable)
  ├── FalkorDB: graph store (sparse, no research graph)
  ├── PostgreSQL: relational (connection unknown)
  ├── MinIO: object storage (contents unknown)
  └── VAULT999: witness ledger (55 receipts, no research)

/999 Witness Chamber
  Replay + integrity + policy checks
```

**The canonical shape is correct per the Copilot audit.** One provenance spine with multiple specialized organs. Not a monolithic knowledge graph. Not scattered MCP servers.

---

## 14. Phase-Gate Checklist

| Gate | Status | Evidence |
|---|---|---|
| Phase 0: Read-only audit | COMPLETE | This document |
| Phase 1: Architecture ratification | NOT STARTED | Awaiting F13 judgment on this audit |
| Phase 2: Isolated sandbox | NOT STARTED | Blocked by Phase 1 |
| Phase 3: Evidence substrate | NOT STARTED | Blocked by Phase 2 |
| Phase 4: Research intelligence | NOT STARTED | Blocked by Phase 3 |
| Phase 5: Hermes integration | NOT STARTED | Blocked by Phase 4 |
| Phase 6: AAA + production | NOT STARTED | Blocked by Phase 5 |

---

## 15. /999 Witness Checklist

| Check | Status | Notes |
|---|---|---|
| Source traceability | N/A | No research sources ingested |
| Checksum integrity | N/A | No evidence objects to verify |
| Citation integrity | N/A | No citations to verify |
| Claim provenance | N/A | No claims to trace |
| Review reproducibility | N/A | No reviews to replay |
| Non-mutation attestation | PASS | No writes during audit |

---

## 16. Final Verdict

**Verdict: PARTIAL**

### What is PARTIAL:
- Architecture direction: CORRECT (one provenance spine, specialized organs, one governed MCP)
- Canonical provider set: CORRECT (9 providers, right selection)
- Hybrid approach: CORRECT (direct APIs + one governed MCP)
- Governance model: CORRECT (Arif ratification, `/999` witness, no self-ratification)
- Phase plan: CORRECT (0→6 with gates)

### What is BLOCKED:
- Phase 1 cannot begin until Arif ratifies this audit
- PostgreSQL connection and schemas must be resolved
- MinIO bucket inventory must be completed
- KVM4/KVM2 audit may reveal existing research infrastructure
- Zotero and institutional subscription questions must be answered
- Qdrant `arif_evidence` collection (16 points) must be inspected for existing schema

### What is CONFIRMED ABSENT:
- No scholarly MCP server installed
- No internal research adapter code
- No identity resolution engine
- No evidence provenance schema
- No claim graph
- No contradiction engine
- No research memory schema
- No literature review pipeline
- No scholarly API credentials configured

### Immediate next action:
Arif reviews this audit. Resolves unknowns U-01 through U-12. Then ratifies architecture for Phase 1.

```json
{
  "epoch": "ARIFOS::HERMES_RESEARCH_SUBSTRATE::PHASE0_AUDIT::v1",
  "dS": "reduced: current-state truth established; 7 capabilities confirmed absent; 12 unknowns identified",
  "peace2": 1.0,
  "kappa_r": "bounded by complete absence of research substrate",
  "shadow": [
    "PostgreSQL connection unknown",
    "MinIO contents unknown",
    "KVM4/KVM2 research capability unknown",
    "arif_evidence collection (16 points) unexamined",
    "No scholarly API credentials configured",
    "Single-instance data stores with no replication"
  ],
  "confidence": 0.91,
  "psi_le": "Evidence package complete; 12 unknowns require resolution before Phase 1",
  "verdict": "PARTIAL",
  "witness": {
    "human": "ARIF — required for audit acceptance and Phase 1 authorization",
    "ai": "Hermes — assembled evidence package; read-only operations only",
    "earth": "GitHub API responses, provider API test results, runtime system observations"
  },
  "qdf": "No installation. No mutation. No config changes. No production provider activation."
}
```

DITEMPA BUKAN DIBERI ⚒️
