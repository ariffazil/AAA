---
name: hermes-research-substrate
description: Use when searching scholarly papers.
capability_tier: fed-long-context
ecology_state: WARM
---

# Hermes Research Substrate -- Agent Skill

This skill provides the RESEARCH METABOLISM to any AAA agent.

## The Pipeline

SENSE: Parse the research question. Identify domain, ontology, key terms.
RETRIEVE: Multi-provider search (OpenAlex, PubMed, Semantic Scholar). Dedup by DOI.
WITNESS: Store evidence objects with content hash, exact spans, provenance.
COMPARE: Build claim graph. Detect typed contradictions.
SYNTHESIZE: Evidence-weighted consensus with confidence levels.
REMEMBER: Store in research memory. Provenance lineage preserved.
RE-EXAMINE: When new evidence arrives, re-evaluate prior claims.
THINK: Produce human-facing synthesis with uncertainty disclosure.

## Provider Adapters

| Adapter | Status | Notes |
|---------|--------|-------|
| OpenAlex | LIVE TESTED | Graph spine. 327M+ works. No auth. |
| PubMed | LIVE TESTED | E-utilities. 37M+ citations. No auth. |
| Semantic Scholar | CODE READY | 214M papers. Free key recommended. |
| CORE | NEEDS KEY | 57M OA full texts. |
| arXiv | NEEDS ADAPTER | Preprints. |
| Open Library | NEEDS ADAPTER | Book catalog. |

## Database Schema

PostgreSQL research schema (19 tables).
Schema SQL: /root/AAA/docs/RESEARCH-SCHEMA.sql

## Current State

Forge 2.1: 5 relation types PROVEN (SUPPORTS, CONTRADICTS, QUALIFIES, SCOPE_DIVERGES, METHOD_DIVERGES) on vitamin D topic. Forge 3: Behaviour change test PROVEN — belief flipped from AGAINST (0/2) to SUPPORT (8/6) after injecting 5 papers. Evidence changes reasoning. Scientific metabolism first proof. Schema: 19 tables, 72 works, 28 evidence, 49 claims, 64 relations. Next: re-examination engine, survivor analysis, cross-agent integration.

## Cross-Agent Usage

GEOX: Geoscience papers, basin evolution, reservoir contradictions.
WEALTH: Financial research, company performance, analyst contradictions.
WELL: Health/biomedical papers, clinical contradictions.
All share the same evidence ledger and claim graph.

## Constitutional Rules

Evidence before declaration. Graph before mutation.
No agent self-ratifies truth. F13 ratification required for knowledge promotion.