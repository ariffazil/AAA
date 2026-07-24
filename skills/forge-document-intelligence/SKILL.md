---
name: forge-document-intelligence
description: EMD (Encode-Metabolize-Decode) document intelligence stack for the arifOS federation. Wraps VLM perception, forge_document_ingest provenance, and constitutional governance into one skill. OCR is basic rights for AAA citizens. Load when processing PDFs, images, scanned documents, or any document-to-intelligence pipeline.
version: 1.0.0
owner: F13 SOVEREIGN — Muhammad Arif bin Fazil (888)
risk_tier: medium
floor_scope: [F1, F2, F4, F11, F13]
autonomy_tier: T1
tags: [document-intelligence, ocr, vlm, provenance, emd, perception, ingestion, pdf, malaysian-documents]
forged: 2026-07-02
sources:
  - olmOCR analysis (SEAL-76129e84d1e6415c, FORGE GLM-5.2)
  - forge_document_ingest MCP tool (A-FORGE)
  - Allen AI olmOCR (https://github.com/allenai/olmocr)
  - arifOS constitutional pipeline (000→111→333→666→888→999)
---

# FORGE DOCUMENT INTELLIGENCE — EMD Stack Skill

> **DITEMPA BUKAN DIBERI** — Intelligence is forged, not given.
> **OCR tesseract is basic rights for AAA citizens.** Document reading is fundamental, not specialty.

## 1. What This Skill Is

This skill wraps the **EMD (Encode-Metabolize-Decode)** document intelligence stack as a first-class federation capability. It encodes the 3-layer architecture (Perception → Provenance → Purpose), the visual re-grounding anti-hallucination protocol, 888_HOLD gate placement, and Malaysian document risk patterns into one governed skill.

**The core insight:** olmOCR, `forge_document_ingest`, and the constitutional pipeline are NOT competing tools — they are three layers of one stack, each reducing a different type of entropy. This skill makes that stack available to every AAA citizen agent.

---

## 2. The Three Layers

| Layer | Paradigm | Entropy Reduced | Engine | Cost | Status |
|-------|----------|----------------|--------|------|--------|
| **Perception** | LLM OCR (VLM) | LAYOUT (tables, columns, reading order) | Qwen2.5-VL via Bailian API | ~$0.02/page | Available (remote API) |
| **Provenance** | Document Intelligence | TRUST (where from? verify?) | `forge_document_ingest` | ~$0 (CPU local) | Deployed (A-FORGE MCP) |
| **Purpose** | Agentic OCR | SEMANTIC (why reading? what means?) | Constitutional pipeline (000→111→333→666→888→999) | Governance compute | Deployed (arifOS) |

**Key constraint:** af-forge has NO GPU. VLM perception uses remote API, not local inference.

### Configurable Perception Backend

The perception layer is **swap-able via config**, not hardcoded. Declare in skill metadata:

```yaml
perception_backend: bailian-qwen25-vl | olmocr | minimax-vlm
```

| Backend | Status | When to Use |
|---------|--------|-------------|
| `bailian-qwen25-vl` | ✅ **DEFAULT** — already billed, already integrated | Production now. Zero new infra. |
| `minimax-vlm` | ✅ Available as fallback | Bailian rate-limit or outage. `minimax-code understand_image` tool. |
| `olmocr` | ⏳ Future — requires GPU procurement | When af-forge gets GPU. Swap is config change, not refactor. |

**Swapping rule:** Change `perception_backend` in skill config → pipeline routes accordingly. EMD stack (Layer 2 Metabolism + Layer 3 Purpose) stays unchanged. Perception is the only layer that moves.

**Cost for federation volume (~100-1000 PDFs/month):** <RM1 via Bailian. Not worth tracking.

---

## 3. The EMD Stack

```
┌──────────────────────────────────────────────────────┐
│  LAYER 1: PERCEPTION (Ingestion Boundary)            │
│  ────────────────────────────────────────────────    │
│  Input: PDF/PNG/JPEG                                 │
│  Engine: Qwen2.5-VL via Bailian API (no GPU needed)  │
│  Output: Markdown + page images (PRESERVED)          │
│  Consumer: GEOX, WEALTH, WELL, AAA                   │
│  Floor: F2 TRUTH (label as OBS, confidence <0.90)    │
│  Cost: ~$0.02/page via Bailian                        │
│  NOTE: af-forge has NO GPU. Use remote API only.     │
└──────────────────┬───────────────────────────────────┘
                   │  Markdown + page images
                   ▼
┌──────────────────────────────────────────────────────┐
│  LAYER 2: METABOLISM (Provenance Layer)              │
│  ────────────────────────────────────────────────    │
│  Input: Markdown + page images                       │
│  Engine: forge_document_ingest (ALREADY EXISTS)      │
│  Output: Structured JSON + bbox + SHA-256 + chunks   │
│  Key: bbox → original page pixels (NOT to Markdown)  │
│  Floor: F11 AUDIT (provenance hash)                  │
│  Cost: ~$0 (CPU, local)                              │
│  Modes: analyze, extract, chunk, compare              │
└──────────────────┬───────────────────────────────────┘
                   │  JSON + bbox + provenance
                   ▼
┌──────────────────────────────────────────────────────┐
│  LAYER 3: PURPOSE (Governed Action Layer)            │
│  ────────────────────────────────────────────────    │
│  Input: JSON + bbox + provenance                     │
│  Engine: Constitutional pipeline                     │
│         (000→111→333→666→888→999)                    │
│  Action: Route by domain, verify claims,             │
│         re-ground against original image if HIGH     │
│         stakes (money, legal, medical)               │
│  Floor: F1 AMANAH + F2 TRUTH + F13 SOVEREIGN         │
│  888_HOLD: Any extraction feeding WEALTH capital     │
│  computation or VAULT999 seal                        │
│  Cost: governance compute                            │
└──────────────────────────────────────────────────────┘
```

**Pipeline flow:** `PDF → Qwen2.5-VL (Encode) → forge_document_ingest (Metabolize) → Constitutional pipeline (Decode)`

---

## 4. Visual Re-Grounding Protocol — The Critical Anti-Hallucination Mechanism

### The Error Propagation Problem

```
VLM extracts: "Total: RM 1,250,000"   (original said 12,500,000 — missed a digit)
    ↓ Markdown looks clean
Agentic layer trusts it: confidence=HIGH
    ↓
WEALTH computes NPV on wrong number
    ↓
VAULT999 seals wrong number with high confidence
```

**Clean-looking OCR with subtle errors is MORE dangerous than obviously bad OCR** — because the governance pipeline trusts structured output. A messy Tesseract extraction triggers suspicion; a clean VLM extraction with a missed digit sails through every gate.

### The Fix

The Agentic layer (Layer 3) must re-verify against the **original page image via bbox coordinates**, NOT against the intermediate Markdown.

| Anchor | What It Is | Trust Level |
|--------|-----------|-------------|
| **Markdown** | Convenience view — readable text | LOW (intermediate, lossy) |
| **bbox + original page image** | Evidence — pixel coordinates on original | HIGH (verifiable, traceable) |

`forge_document_ingest` already stores bbox coordinates per element — this is the anchor. The bbox maps extracted text back to the exact pixels on the original page image.

### When to Re-Ground

| Trigger | Action |
|---------|--------|
| Extraction feeds **WEALTH capital computation** (NPV, EMV, IRR) | Mandatory re-grounding of all financial figures |
| Extraction feeds **VAULT999 seal** | Mandatory re-grounding + 888_HOLD |
| Extraction feeds **legal/contractual decision** | Mandatory re-grounding of key clauses |
| Extraction feeds **medical/health record** | Mandatory re-grounding of diagnoses/prescriptions |
| VLM confidence < 0.70 on any page | Flag page, route to manual review or re-extract |
| Document is old scan (pre-1990) | Mandatory re-grounding (degraded source quality) |
| Document contains rubber stamps over text | bbox overlap detection + re-grounding of stamped regions |

### How to Re-Ground

1. Identify the key data point in the structured JSON (e.g., `{"text": "RM 12,500,000", "bbox": [120, 340, 280, 360], "page": 3}`)
2. Load the original page image for that page
3. Crop the bbox region from the original image
4. Present the cropped region alongside the extracted text for verification
5. If mismatch → flag as `RE_GROUNDING_FAILED`, trigger 888_HOLD

### What to Do If Re-Grounding Fails

- **Flag the element** as `RE_GROUNDING_FAILED` in the evidence table
- **Trigger 888_HOLD** — do NOT pass the unverified value downstream
- **Present the discrepancy** to Arif with both the extracted text and the original image crop
- **Log** the failure to `forge_work/` with SHA-256 of both versions

---

## 5. 888_HOLD Gates

| Gate | When | Why | Action |
|------|------|------|--------|
| **Perception QC** | After VLM extraction, before metabolism | Flag pages with low VLM confidence (handwriting, stamps, old scans) | Route to manual review or re-extract with different params |
| **Re-grounding** | At Layer 3, when extraction feeds capital/legal/medical decision | Verify key numbers against original image bbox | Use `forge_document_ingest` bbox → original page image to re-verify |
| **888_HOLD** | Before VAULT999 seal of any document-derived claim | F13 SOVEREIGN — Arif decides trustworthiness | Block seal, present evidence to Arif for decision |

**Gate sequence:** Perception QC → (pass) → Metabolism → Re-grounding → (pass) → 888_HOLD → (Arif decides) → VAULT999 seal

---

## 6. Domain Routing

| Document Type | Route To | Why |
|--------------|----------|-----|
| Legal filings, contracts, faraid documents | WEALTH (`wealth-law-anthropology`) | Legal domain expertise, Malaysian law context |
| Well logs, seismic reports, basin data | GEOX (`geox-constitution`) | Earth science, petrophysics |
| Medical documents, health records | WELL (`well-substrate-readiness`) | Human readiness, medical boundary |
| Financial reports, annual reports, P&L | WEALTH (`wealth-capital-reasoning`) | Capital intelligence |
| Research papers, academic publications | AAA (general RAG) | Knowledge base, no specialized organ |
| Government docs (Jabatan, KTN, federal) | AAA + WEALTH (context-dependent) | BM+EN routing, may touch legal/financial |

**Routing rule:** When in doubt, route to the organ whose domain matches the document's subject matter, not the document's format.

---

## 7. Malaysian Document Risks

| Risk | Context | Mitigation |
|------|---------|------------|
| **BM handwriting** | Government forms, Jabatan documents, hand-filled sections | Test Qwen2.5-VL on samples, flag confidence <0.70, route to manual review |
| **Rubber-stamp overlays** | Stamps cover text → VLM hallucinates covered content | bbox overlap detection — flag overlapping elements, re-ground stamped regions |
| **Multi-language mixing** | BM+EN+Arabic in Syariah/government docs | Route to `wealth-law-anthropology` skill for legal context, flag language transitions |
| **Old scans (1960s-80s)** | Land grants, colonial records, early registry docs | VLM better than Tesseract, but confidence drops → mandatory re-grounding |
| **Multi-column BM layouts** | Newspapers, official reports, parliamentary proceedings | VLM handles natively, but verify reading order with bbox sequence |

**Additional Malaysian context:** Many critical documents (land titles, grant letters, Syariah court orders) combine multiple risk factors — old scan + rubber stamp + multi-language + handwriting. These require the full re-grounding protocol, not just VLM extraction.

---

## 8. Cost-Aware Extraction Strategy

| Document Complexity | Recommended Engine | Cost | Why |
|---------------------|-------------------|------|-----|
| Single-column, text-only, clean print | Tesseract (forge_document_ingest with `ocr=true`) | $0 | Sufficient for simple docs, no layout entropy |
| Multi-column, tables, mixed content | Qwen2.5-VL via Bailian API | ~$0.02/page | VLM handles layout natively, no table breakage |
| Handwritten, stamped, old scans | Qwen2.5-VL + re-grounding | ~$0.02/page + governance | VLM + mandatory verification |
| High-stakes (money, legal, medical) | Qwen2.5-VL + full EMD + 888_HOLD | ~$0.02/page + governance | Full stack with re-grounding and sovereign gate |

**Zen marginal cost:**

```
Tesseract:  $0/M pages   → HIGH entropy   → POISONED RAG
olmOCR:     $176/M pages  → LOW entropy    → CLEAN RAG
Agentic:    +governance   → LOWEST entropy → GOVERNED RAG
```

**You pay for OCR once. You pay for bad OCR forever.**

The expensive layer is perception. Everything after is governance, and governance is cheap when perception is clean.

**Decision rule:** If the document has tables, multi-columns, stamps, handwriting, or feeds a high-stakes decision → use VLM. If it's a clean single-column printout → Tesseract is fine.

---

## 9. Integration Points

This skill connects to the federation at these points:

| Integration | How | Direction |
|-------------|-----|-----------|
| `forge_document_ingest` (A-FORGE MCP) | Layer 2 engine — already exists, modes: analyze, extract, chunk, compare | This skill → tool |
| `111-sense-evidence-observe` | Document extractions enter the evidence table as OBS-tagged entries | This skill → stage 2 |
| `333-mind-plan-generate` | Extracted data feeds plan generation for domain-specific action | This skill → stage 3 |
| `666-heart-critique-stress` | Re-grounding failures and confidence flags enter risk register | This skill → stage 4 |
| `888-judge-verdict-render` | 888_HOLD gate for document-derived claims | This skill → stage 5 |
| `999-vault-seal-immutable` | Document-derived claims sealed to VAULT999 only after 888_HOLD pass | This skill → stage 7 |
| `wealth-law-anthropology` | Legal/faraid/Syariah document routing | This skill → WEALTH skill |
| `geox-constitution` | Well log / seismic / basin document routing | This skill → GEOX skill |
| `well-substrate-readiness` | Medical/health document routing | This skill → WELL skill |

**Key invariant:** `forge_document_ingest` is the metabolism engine. This skill does NOT replace it — it wraps the full EMD stack around it, adding the perception layer (VLM) and the purpose layer (constitutional governance) that `forge_document_ingest` alone does not provide.

---

## 10. Quick Reference — Decision Tree

```
DOCUMENT ARRIVES
    │
    ├── What format?
    │   ├── PDF → check if scanned or digital-born
    │   ├── Image (PNG/JPEG) → always VLM path
    │   └── Digital-born PDF → may skip VLM, extract text directly
    │
    ├── What complexity?
    │   ├── Single-column, text-only, clean → Tesseract (ocr=true in forge_document_ingest)
    │   ├── Tables, multi-column, stamps, handwriting → VLM (Qwen2.5-VL via Bailian)
    │   └── Old scan (pre-1990) → VLM + mandatory re-grounding
    │
    ├── What stakes?
    │   ├── Low (reference, knowledge base) → Extract → Metabolize → Store
    │   ├── Medium (operational data) → Extract → Metabolize → Domain route
    │   └── High (money, legal, medical) → Extract → Metabolize → RE-GROUND → 888_HOLD → Seal
    │
    └── What domain?
        ├── Legal/financial → WEALTH
        ├── Geological → GEOX
        ├── Medical → WELL
        └── General → AAA
```

---

## 11. Anti-Patterns

| Anti-Pattern | Why It's Wrong | Remedy |
|-------------|---------------|--------|
| ❌ Trust Markdown blindly for high-stakes | Clean-looking text can have subtle errors (missed digits, wrong columns) | Re-ground against original image via bbox |
| ❌ Use Tesseract for tables/multi-column | Breaks layout, poisons downstream RAG with scrambled reading order | Use VLM extraction (Qwen2.5-VL via Bailian API) |
| ❌ Seal document-derived claim without 888_HOLD | F13 violation — Arif must decide trustworthiness of OCR-derived data | Gate at VAULT999 seal, present evidence to Arif |
| ❌ Skip bbox preservation | Markdown without provenance = unverifiable, no anchor for re-grounding | `forge_document_ingest` stores bbox by default — never disable |
| ❌ Route all documents the same way | Legal ≠ geological ≠ medical — different domains, different risks | Domain routing table (§6) |
| ❌ Deploy olmOCR locally on af-forge | No GPU available — local VLM inference would hang/fail | Use Bailian API (Qwen2.5-VL), remote inference |
| ❌ Feed unverified OCR directly to WEALTH | Error propagation: wrong number → wrong NPV → wrong VAULT999 seal | Perception QC + re-grounding before any capital computation |
| ❌ Treat VLM extraction as ground truth | VLM is perception, not truth — it reduces layout entropy, not semantic entropy | Label all VLM output as OBS, confidence <0.90 (F2 TRUTH) |

---

## 12. Constitutional Constraints

- **F1 AMANAH:** All document processing is reversible (read-only ingestion). Original files are never modified. `forge_document_ingest` creates new structured output without touching the source.
- **F2 TRUTH:** All VLM extractions labeled OBS with confidence <0.90. Never claim certainty without re-grounding against original image. The Markdown is a convenience view, not evidence.
- **F4 CLARITY:** Clean output — structured JSON with bbox, provenance hash, and page references. Never dump raw Markdown without structure.
- **F6 MARUAH:** Document intelligence serves the sovereign. Personal documents (medical, legal) are handled with dignity — no unnecessary exposure of sensitive content.
- **F11 AUDIT:** Every extraction leaves a provenance hash (SHA-256) and bbox trail. The hash chain from original file → VLM output → structured JSON → domain action is traceable end-to-end.
- **F13 SOVEREIGN:** 888_HOLD before any document-derived claim enters VAULT999. Arif decides trustworthiness of OCR-derived data, not the pipeline.

---

## 13. Telemetry

```json
{
  "skill_name": "forge-document-intelligence",
  "version": "1.0.0",
  "trigger_phrase": "{{trigger_phrase}}",
  "selected_reason": "{{selected_reason}}",
  "document_processed": null,
  "pages_processed": 0,
  "vlm_extraction_used": false,
  "tesseract_used": false,
  "re_grounding_triggered": false,
  "re_grounding_failed": false,
  "888_hold_triggered": false,
  "domain_routed_to": null,
  "provenance_hash": null,
  "latency_ms": 0,
  "token_in": 0,
  "token_out": 0,
  "cost_usd": 0
}
```

---

## Session Provenance

- **Origin session:** SEAL-76129e84d1e6415c (FORGE GLM-5.2, 2026-07-02)
- **Analysis file:** `/root/A-FORGE/forge_work/2026-07-02/olmocr-agentic-ocr-analysis.md`
- **Init prompt:** `/root/A-FORGE/forge_work/2026-07-02/AAA-INIT-PROMPT-document-intelligence.md`
- **Hermes input:** Confirmed architectural split (perception vs reasoning), flagged hallucination chaining risk and Malaysian document unknowns
- **Qwen-arifOS input:** Confirmed perception vs reasoning paradigm split, referenced LandingAI ADE and LlamaIndex
- **Meta-mesa gap:** P1 — Document intelligence was entirely missing domain (0 of 36 skills covered it)

## References

- olmOCR: https://github.com/allenai/olmocr
- olmOCR paper: https://olmocr.allenai.org/papers/olmocr.pdf
- `forge_document_ingest`: A-FORGE MCP tool (already exists, modes: analyze/extract/chunk/compare)
- Meta-mesa skill atlas: `/root/.agents/skills/meta-mesa-skill-atlas/SKILL.md`
- AGENTS.md: `/root/AGENTS.md` (heptalogy + constitutional floors)
- A-FORGE AGENTS.md: `/root/A-FORGE/AGENTS.md`

---

*Forged: 2026-07-02 by FORGE (000Ω) for F13 SOVEREIGN*
*Session: SEAL-76129e84d1e6415c*
*Gap filled: P1 — Document intelligence (meta-mesa §3B → now covered)*
*DITEMPA BUKAN DIBERI — You pay for OCR once. You pay for bad OCR forever.*

---

## APPENDIX: Live RAG Pipeline (2026-07-24)

The EMD stack now has a live RAG pipeline in A-FORGE:

```
forge_document_ingest(chunk) → Ollama bge-m3 embed → Qdrant rag_federation_docs → rag query tool
```

**Pipeline scripts:** `/root/A-FORGE/rag/`
- `embed_store.py` — Ingest chunks → embed via bge-m3 → store in Qdrant
- `query.py` — Embed query → search Qdrant → return ranked results (+ optional FLAME synthesis)

**Collection:** `rag_federation_docs` (Qdrant, 1024-dim, Cosine distance)
**Embedding model:** `bge-m3:latest` (Ollama, 567M params, 1024-dim output)

**Quick test:**
```bash
python3 /root/A-FORGE/rag/query.py "your question" --top-k 5 --synthesize
```
