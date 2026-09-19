# HERMES DEEP RESEARCH — Knowledge Substrate Blueprint
> F13-integrated · 2026-09-19 · 3 parallel research streams verified (24 paper MCPs, 40+ book MCPs, 9 raw APIs audited)
> Updated with subagent findings: subagent task 0 (MCP catalog), task 1 (raw API audit), task 2 (book/library catalog)

---

## THE CORE PRINCIPLE

One capability. Many interchangeable adapters. Hermes talks to `knowledge.search()`. The adapter decides the source.

```
KNOWLEDGE_DISCOVERY (capability)
    │
    ├── PAPERS: paper-search-mcp (20+ sources, Python, 2.7k★)
    │          arxiv-mcp-server  (arXiv specialist, 3.2k★)
    │
    ├── BOOKS: libgen-mcp       (Go binary, LibGen + 10 OA sources)
    │          openlibrary-mcp   (40M book records)
    │          gutenberg-mcp     (75k free public-domain books, full text)
    │
    └── [future adapters — swap without touching Hermes]
```

OpenAlex dies → replace the adapter. Capability survives.
> "Govern capabilities, not implementations. Skills are replaceable. Capabilities survive."

---

## TIER 1: PRIORITY INSTALLS (verified 2026-09-19)

### 1. paper-search-mcp — THE research paper engine

```
Repo:   github.com/openags/paper-search-mcp
Stars:  2,700+ | Lang: Python | License: MIT | Commits: 50
Install: uvx paper-search-mcp  (or pip / Docker / Smithery)
```

**20+ sources with free-first strategy:**
arXiv · PubMed · PMC · Europe PMC · bioRxiv · medRxiv · Semantic Scholar · OpenAlex · Crossref · CORE · Google Scholar · IACR · dblp · OpenAIRE · CiteSeerX · DOAJ · BASE · Zenodo · HAL · SSRN · Unpaywall DOI lookup

**Tools:** search_papers(query, sources, limit) · download_paper(doi, source) · read_paper(path)
**Features:** concurrent multi-source search, dedup, PDF download with fallback chain, text extraction from PDFs, DOI backfilling, standardized Paper class output
**Auth:** No API keys needed for core sources. Optional keys for higher rate limits (Semantic Scholar, CORE)

**This ONE MCP replaces what Copilot described as five separate integrations.**

---

### 2. arxiv-mcp-server — Deep arXiv specialist

```
Repo:   github.com/blazickjp/arxiv-mcp-server
Stars:  3,200+ | Lang: Python | License: MIT
Install: uvx arxiv-mcp-server  (or pip / Docker / Smithery)
Config: ~/.arxiv-mcp-server/papers
```

**Why install alongside paper-search-mcp:**
- LaTeX section-by-section reading (not just PDF blobs)
- BibTeX generation from arXiv metadata
- Citation graph via Semantic Scholar integration
- Topic watches/alerts (track new papers in your field)
- Papers stored locally on disk for re-reading
- HTML/Markdown/LaTeX full text retrieval
- Listed on official MCP registry (v0.7.2)

**Use case:** Deep dive into specific arXiv papers. paper-search-mcp finds them; arxiv-mcp-server lets you READ them properly.

---

### 3. libgen-mcp — THE book + federated paper engine

```
Repo:   github.com/jmrplens/libgen-mcp
Lang:   Go (single static binary, zero dependencies)
Install: Download binary from GitHub releases
Auth:    None required
```

**4 focused tools:**
- `acquire_book` — LibGen search + download (books, papers, comics, magazines)
- `research_topic` — Federated OA discovery across 10+ sources
- `get_paper` — Article download from Unpaywall/Europe PMC/bioRxiv/CORE/OAPEN
- `download_troubleshoot` — MD5/ISBN/DOI resolution

**Open-access sources integrated:**
arXiv · Crossref · OpenLibrary · Gutenberg · dblp · PubMed · ERIC · Unpaywall · Europe PMC · bioRxiv · CORE · OAPEN

**Why this is critical:** Single binary. No auth. Covers BOTH books (LibGen) AND papers (OA sources). Go = fast, no Python dependency hell. Already on Smithery.

**Note:** LibGen's legal status varies by jurisdiction. The MCP itself is a neutral tool; use responsibly.

---

### 4. openlibrary-mcp-server (cyanheads) — Better than 8enSmith version

```
Repo:   github.com/cyanheads/openlibrary-mcp-server
Lang:   TypeScript | Install: npm/bun or Docker
Hosted: openlibrary.caseyjhand.com/mcp
```

**10 tools across 5 categories:**
- Search: full-text book search with Solr field prefixes
- Books: edition fetching, reading availability
- Authors: author details and works
- Subjects: subject browsing
- Covers: cover image resolution

**Filters:** title/author/subject/publisher/ISBN/language
**Sort by:** relevance/newest/oldest/rating/edition count
**Reading availability:** borrow/browse/read links from Internet Archive
**Transports:** STDIO and Streamable HTTP

**Why cyanheads over 8enSmith:** More tools (10 vs 4), Solr field prefixes for precise search, reading availability from IA, subject browsing, cover resolution.

---

### 5. gutenberg-mcp-server — Free full-text books

```
Repo:   github.com/cyanheads/gutenberg-mcp-server
Lang:   TypeScript | Install: npm/bun or Docker
```

**75,000+ public-domain books with FULL PLAIN TEXT.**
- Offset/limit chunking for large texts
- STDIO or Streamable HTTP transport
- No auth required

**Use cases:** Philosophy, classics, economics, literature, history, pre-1928 scientific works. The ONLY legal way to read actual book content at scale.

---

## TIER 2: SPECIALIZED / SUPPLEMENTARY

### If PETRONAS has institutional API keys:
```
academic-mcp (LinXueyuanStdio) — 41★, Python
github.com/LinXueyuanStdio/academic-mcp
```
19+ sources including **premium** (need API keys):
- IEEE Xplore · Scopus · Springer · ScienceDirect · Web of Science · ACM · JSTOR
- Plus all free sources (arXiv, PubMed, Semantic Scholar, CORE, Crossref, Google Scholar)

### For biomedical research specifically:
```
pubmed-search-mcp (u9401066) — 40 tools, multi-source
github.com/u9401066/pubmed-search-mcp
```
PubMed · Europe PMC · CORE · OpenAlex · Full-text access · PICO analysis · Tenant-safe deployment

### For Anna's Archive access (books + papers):
```
annas-mcp (iosifache)
github.com/iosifache/annas-mcp
```
Mirrors LibGen + Sci-Hub + Z-Library. Well-maintained, published on tech news.

### For local PDF intelligence (after downloading):
```
pdf-mcp (jztan)
github.com/jztan/pdf-mcp
```
Hybrid semantic + keyword search over local PDFs. OCR. Tables. Images. Multi-column/CJK.

### For semantic scholar deep dive:
```
semantic-scholar-fastmcp (zongmin-yu) — 165★
github.com/zongmin-yu/semantic-scholar-fastmcp-mcp-server
```
Paper search · Citation networks · Recommendations · Bulk datasets · Docker

---

## RAW APIs — What They Actually Give You

| API | Free | Full Text | Rate Limit | Auth | Best For |
|-----|------|-----------|------------|------|----------|
| OpenAlex | Yes ($0.10/day no key) | Metadata + OA links (PDFs paid add-on) | 100K credits/day free | None | 286M works, citation graph, broadest index |
| Semantic Scholar | Yes | No (links only) | 1000 req/s shared; 1 RPS with free key | Optional free key | 214M papers, TLDR, embeddings, recommendations |
| arXiv | Yes | YES (PDF + LaTeX source) | 1 req/3 sec | None | AI/ML/Physics/CS preprints, guaranteed full text |
| Open Library | Yes | Partial (IA links) | Polite (<1 req/sec) | None | 40M book records, ISBN lookup, editions |
| Internet Archive | Yes | YES (where available) | ~60 calls/min CDX | None | Largest free full-text book archive |
| Crossref | Yes | No (DOI metadata only) | 5-10 req/s | None | 180M DOI records, citation metadata |
| CORE | Yes | YES (57M full texts) | 5 req/10s unregistered | Free API key | Largest OA full-text aggregator |
| PubMed/PMC | Yes | PMC OA subset full text | 3/sec (10/sec w/key) | Optional free key | Biomedical gold standard |
| Unpaywall | Yes | Links to free copies | 100K/day | Email required | Find legal OA versions |
| Gutendex | Yes | YES (public domain) | No defined limit | None | 70K+ Project Gutenberg books |

**The sleeper hit:** CORE API — 57 million open access papers with machine-readable full text. Free API key. Nobody talks about it but it's the largest full-text OA collection.

---

## WHAT WE ALREADY HAVE (KVM8 live)

| Tool | Covers | Gap vs Research |
|------|--------|-----------------|
| context7 | Dev docs (React, Next.js etc.) | Zero academic coverage |
| exa | Semantic web search | No paper-specific metadata/citations |
| brave_search | General web search | No citation graphs |
| firecrawl | Web scraping | No structured paper data |
| zai_reader | Web page reading | No book/paper discovery |
| zai_search | Web search | No scholarly sources |
| deepwiki | Wiki content | No books/papers |
| doc-tables | PDF table extraction | No search/discovery |

**The gap is total.** No tool can discover, search, or catalog papers or books.

---

## RECOMMENDED ARCHITECTURE

```
                    HERMES (A2H bridge)
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    EXISTING STACK   PAPER LAYER     BOOK LAYER
         │               │               │
    ┌────┴────┐    ┌─────┴─────┐   ┌────┴────┐
    │exa      │    │paper-     │   │libgen-  │
    │brave    │    │search-mcp │   │mcp      │
    │context7 │    │           │   │         │
    │firecrawl│    │arxiv-     │   │openlib- │
    │zai_read │    │mcp-server │   │mcp      │
    └─────────┘    └───────────┘   │guten-   │
                                   │berg-mcp │
                                   └─────────┘
         │               │               │
         └──────── Evidence Graph ────────┘
                         │
                   ┌─────┼─────┐
                   │     │     │
                cite  claim  witness
                graph ledger VAULT999
```

---

## PHASED INSTALLATION

### Phase 1: Immediate (today)
```bash
# 1. Paper search engine (covers 20+ sources)
uvx paper-search-mcp  # test it first

# 2. Book engine (LibGen + federated OA)
# Download Go binary from github.com/jmrplens/libgen-mcp/releases

# 3. Open Library (40M book records)
npx openlibrary-mcp-server  # cyanheads version
```

Config addition to /root/.hermes/config.yaml:
```yaml
  paper-search:
    command: uvx
    args: [paper-search-mcp]
    enabled: true
    timeout: 60

  libgen:
    command: /usr/local/bin/libgen-mcp  # after binary install
    enabled: true
    timeout: 60

  open-library:
    command: npx
    args: [openlibrary-mcp-server]
    enabled: true
    timeout: 60
```

### Phase 2: Deep reading (this week)
```bash
# 4. arXiv deep reader (LaTeX section reads, citation graphs)
uvx arxiv-mcp-server

# 5. PDF intelligence (for downloaded papers)
# pip install or npx for pdf-mcp
```

### Phase 3: Premium sources (if institutional keys exist)
```bash
# 6. Academic MCP with Springer/Scopus/IEEE keys
pip install academic-mcp  # LinXueyuanStdio
```

---

## ARIFOS DOCTRINE ALIGNMENT

| Principle | How this blueprint follows it |
|-----------|------------------------------|
| Capability ≠ Authority | Knowledge access ≠ permission to publish |
| Govern capabilities, not implementations | One KNOWLEDGE_DISCOVERY, swappable adapters |
| Witness before mutation | Papers cited as evidence, not truth |
| Reality before narrative | Search → evidence graph → synthesis |
| Anti-collapse | "Found 50 papers" ≠ "research done" |
| State-transition | Found → Retrieved → Extracted → Synthesized → Cited |
| F13 sovereignty | Arif decides what gets researched |
| LOCALHOST_IS_PASSWORD | All local installs, no external auth gates |

---

## THE VERDICT

**Copilot was architecturally right:** one capability, many adapters.

**Where Copilot fell short:** didn't verify which MCP servers actually exist.

**What actually exists (verified 2026-09-19):**

1. `openags/paper-search-mcp` — 2,700★, 20+ paper sources, Python, free-first
2. `blazickjp/arxiv-mcp-server` — 3,200★, deep arXiv with LaTeX reads
3. `jmrplens/libgen-mcp` — Go binary, LibGen + 10 OA sources, no auth
4. `cyanheads/openlibrary-mcp-server` — 10 tools, Open Library full coverage
5. `cyanheads/gutenberg-mcp-server` — 75k free books, full plain text

**Three installs transforms Hermes from "web search agent" to "research intelligence engine."**

Not five MCPs. Not five new organs.
One capability. Many interchangeable adapters.
