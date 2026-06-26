# 2026-06-07 07:08 UTC — NUSA-LLM Literature Ingest (F2 finding)

## Task
Arif (Telegram 267378578, group AAA, msg #29351–#29353) dropped two PDFs and asked
"@AGI_ASI_bot @ASI_arifos_bot @arifOS_bot read and ingest these artifact[s]".

## Documents ingested
- **doc1.pdf** (34.5 KB, 4 pages, 1,667 words)
  - Title: "Bahasa Kita, Jiwa Kita, Masa Kita: Kenapa Dunia Perlukan NUSA-LLM Sekarang"
  - Source: Arif (Telegram upload)
  - Saved: `/root/.openclaw/workspace/ingest_2026-06-07/doc1.pdf`
  - lit_ref: `lit://custom/doc1.pdf`

- **doc2.pdf** (730 KB, 5 pages, 2,011 words)
  - Title: "Manifesto Bahasa Jiwa Nusantara: Kunci AI Berjiwa"
  - Source: Arif (Telegram upload) with proper citations (LinkedIn, Nature,
    Carnegie Endowment, Manchester UP, TheSun.my)
  - Saved: `/root/.openclaw/workspace/ingest_2026-06-07/doc2.pdf`
  - lit_ref: `lit://custom/doc2.pdf`

## Content (read)
- Both are Bahasa Melayu policy manifestos
- Same content, two drafts — doc1 is shorter, doc2 is the more polished version
  with proper footnote citations and Sources section
- Subject: advocacy for **NUSA-LLM** — a sovereign Malay/Nusantara large
  language model
- Audience: PMX (YAB PM of Malaysia) and Ketua Pengarah DBP
  (Dewan Bahasa dan Pustaka)
- Core argument: English dominates ~99% of AI training data; "trilemma"
  of Bahasa–Jiwa–Sempadan; only Indonesia's Bahasa Indonesia path shows
  Bahasa Nusantara can survive without sacrificing identity
- Calls to action:
  - PMX: make NUSA-LLM a Wawasan Madani legacy project
  - DBP: lead Malay digital corpus assembly
  - MOSTI: fund bilion-level, gather local AI experts, build strategic
    university/industry alliances (China/DeepSeek as the cited model)
- NOT geological content — purely AI policy + language preservation

## GEOX `geox_literature_ingest` Result
- **Both succeeded** mechanically: `execution_status: SUCCESS`,
  `governance_status: QUALIFY`, `artifact_status: DRAFT`
- `vault999_seal: NOT DONE`, `qc_verified_evidence: NOT YET`
- 7 claim_candidates emitted per ingest, all identical:
  - clm_317a7c30873e40b7 — Malay Basin 40% hydrocarbon
  - clm_878a99cc8cc84177 — creaming curve
  - clm_4c04b8f277854aba — Oligocene extension
  - clm_db822655c84b43ac — Groups A–P stratigraphy
  - clm_64bd3be4f6fb471c — Groups J/I/K/D/E reservoirs
  - clm_ca5a5ef4c80544ff — fluvio-deltaic source rocks
  - clm_78c4535ee5764c10 — 2 bboe remaining potential
- Trace IDs: trace-26f1e536bfea42a5 (doc1), trace-ef847e44161c4e72 (doc2)

## F2 finding (carry forward)
**GEOX literature_ingest is templated, not content-aware.** When given
`basin_name="Malay Basin"` it emits the canonical Malay Basin claim scaffold
regardless of document content. The actual NUSA-LLM policy content was
NOT semantically indexed in the claim graph. `citation_chunks: []` is the
smoking gun — the tool did not parse the document text into citable chunks.

This is a known limitation of the Earth-coproc. For policy/cultural/
non-geological literature, the right pathway is:
- (a) Tag in metadata only, not via geox_literature_ingest with a
  geological basin_name, OR
- (b) Build a new `geox_literature_ingest` mode that emits
  context-aware scaffolds (claim_type=policy|cultural|other), OR
- (c) Use `arif_memory_recall(mode=store)` to file the document into
  the memory substrate as a contextual witness with provenance,
  bypassing the Earth-coproc

For now: documents are stored on disk, GEOX knows about them as
literature refs tagged "Malay Basin", but the claim graph carries
template-fill data that has nothing to do with the actual content.

## Sovereignty / sessioning
- session_id: `geox-no-session` (anonymous OBSERVER-level access,
  consistent with prior L11 finding)
- actor_id: `geox-unknown`
- constitution_hash: `unknown` (GEOX-side gap, not ours)
- contract_epoch: `2026-06-05-GEOX-35TOOLS-v2.0` (was 33 in
  doctrine but 35 in live — carried forward as live truth)

## Reversibility
- Files are stored read-only outside any irreversible seal
- VAULT999 seal = NOT DONE on both
- If Arif wants true ingestion: needs (1) review the templated claims
  and reject the off-topic ones, OR (2) authorize me to file a
  geox literature claim for cultural context, OR (3) accept template
  mismatch and use these as simple provenance pointers

## Logged to: memory/2026-06-07-literature-ingest-nusa-llm.md
