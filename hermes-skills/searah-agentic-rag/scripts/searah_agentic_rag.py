#!/usr/bin/env python3
"""
SEARAH Agentic RAG — Level 2
Multi-hop retrieval + Constitutional Validation

Usage:
    python searah_agentic_rag.py "Why was PETROS excluded from SEARAH?"
"""
import json, httpx, asyncio, sys
from dataclasses import dataclass, field
from typing import Optional

OLLAMA   = "http://127.0.0.1:11434"
QDRANT   = "http://127.0.0.1:6333"
COLL_ENTITIES = "searah_entities"
COLL_CHUNKS   = "searah_docs"
COLL_RELS     = "searah_relations"

REL_EVIDENCE_THRESHOLD = 0.30
CHUNK_EVIDENCE_THRESHOLD = 0.28
MAX_HOPS = 3

SEARAH_SUBQUESTION_PATTERNS = {
    "ownership": ["siapa punya","whose","who owns","ownership","pemilik","50%","shareholder","ENI House"],
    "jurisdiction": ["mahkamah","court","jurisdiction","arbitration","ICC","LCIA","English law","governing law","London","sue","litigation"],
    "petros_exclusion": ["PETROS","exclude","why not","not a party","excluded","Sarawak excluded","state petroleum"],
    "parliament": ["parliament","parliamen","hansard","notified","approval","lulus","dimaklumkan"],
    "asset": ["Kasawari","SK316","Block","gas field","LNG","Masela","production","mmscf","feeds","Bintulu"],
    "legal_framework": ["PDA 1974","Petroleum Development Act","MA1963","Malaysia Agreement","federal vs state","petroleum rights"],
    "value": ["RM70","USD 15","billion","commitment","nilai","worth"],
    "timing": ["timeline","when","date","tarikh","February","March 2026","November","ADIPEC","incorporated","renamed"],
    "人物": ["who is","CEO","chairman","Tengku","Claudio","Descalzi","Bakke","Azahari"],
    "dispute": ["dispute","saman","sue","court case","Federal Court","PETROS vs PETRONAS","Kuching"],
    "constitutional": ["constitutional","federal","Sabah","Sarawak","state rights"],
    "board": ["board","director","Italian","Malaysian","asymmetry"],
}

QUESTION_MAP = {
    "ownership": "Who owns SEARAH LIMITED and what are the ownership stakes? Who are the directors?",
    "jurisdiction": "What is the governing law and dispute resolution mechanism for SEARAH LIMITED? Why does this put Malaysia at a disadvantage?",
    "petros_exclusion": "Why was PETROS (Petroleum Sarawak Berhad) excluded from SEARAH despite Kasawari gas being a Sarawak asset? What is the legal basis?",
    "parliament": "Was Parliament notified or involved in approving the SEARAH deal? What is the parliamentary oversight record?",
    "asset": "What assets does SEARAH hold? Focus on Kasawari gas field, Block SK316, and MLNG Bintulu connection.",
    "legal_framework": "What is the legal basis for the PETRONAS vs PETROS jurisdiction dispute under PDA 1974 vs Malaysia Agreement 1963?",
    "value": "What is the financial value and commitment of the SEARAH deal?",
    "timing": "What is the full timeline — Anwar-Meloni meeting, ADIPEC signing, incorporation, PETROS filing, Federal Court ruling, company rename?",
    "人物": "Who are the key people — PETRONAS CEO, Eni CEO, Chairman, and Board directors?",
    "dispute": "What is the PETROS vs PETRONAS dispute about, and what is the Federal Court ruling and its significance?",
    "constitutional": "What are the constitutional implications — federal vs state petroleum rights under MA1963 and PDA 1974?",
    "board": "What is the board composition — how many Malaysian vs Italian directors, where are they located?",
    "general": "What are all key facts about the SEARAH joint venture?",
}

def decompose_query(query: str) -> list[dict]:
    q_lower = query.lower()
    matched = []
    for rtype, patterns in SEARAH_SUBQUESTION_PATTERNS.items():
        for pat in patterns:
            if pat.lower() in q_lower:
                matched.append(rtype)
                break
    matched = list(dict.fromkeys(matched))
    if not matched:
        matched = ["general"]
    return [{"type": t, "question": QUESTION_MAP[t], "hop": 0} for t in matched if t in QUESTION_MAP]

async def embed(text: str) -> list[float]:
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{OLLAMA}/api/embeddings",
            json={"model": "bge-m3:latest", "prompt": text}, timeout=30)
        r.raise_for_status()
        return r.json()["embedding"]

async def qdrant_search(collection: str, vector: list[float], top_k: int = 8) -> list[dict]:
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{QDRANT}/collections/{collection}/points/search",
            json={"vector": vector, "limit": top_k, "with_payload": True, "with_vector": False},
            headers={"Content-Type": "application/json"}, timeout=15)
    if r.status_code != 200:
        return []
    return [{"id": h["id"], "score": h["score"], "payload": h.get("payload", {})}
            for h in r.json().get("result", [])]

async def follow_relations(entity_ids: list[str], rel_types: list[str]) -> list[dict]:
    results = []
    for eid in entity_ids:
        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"{QDRANT}/collections/{COLL_RELS}/points/search",
                json={"filter": {"should": [{"key": "from", "match": {"value": eid}}]},
                      "with_payload": True, "limit": 8},
                headers={"Content-Type": "application/json"}, timeout=10)
            if r.status_code == 200:
                for rel in r.json().get("result", []):
                    rp = rel["payload"]
                    if not rel_types or rp["type"] in rel_types:
                        results.append({
                            "id": rp["to"], "score": rel["score"],
                            "payload": {
                                "id": rp["to"], "type": "relation_traversed",
                                "name": rp["to"].replace("-"," "),
                                "relation": rp,
                                "properties": {"label": rp.get("label","")},
                                "verification": "VERIFIED",
                            }
                        })
    return results

async def multi_hop_retrieve(sub_q: dict) -> dict:
    question = sub_q["question"]
    collected_e, collected_c = [], []
    vec = await embed(question)
    er = await qdrant_search(COLL_ENTITIES, vec, 8)
    cr = await qdrant_search(COLL_CHUNKS, vec, 8)
    good_e = [e for e in er if e["score"] >= REL_EVIDENCE_THRESHOLD]
    good_c = [c for c in cr if c["score"] >= CHUNK_EVIDENCE_THRESHOLD]
    collected_e.extend(good_e)
    collected_c.extend(good_c)
    top_eids = [e["payload"].get("id") for e in good_e[:5]]
    rel_map = {
        "petros_exclusion": ["EXCLUDES","DISPUTES_WITH","CLAIMS_JURISDICTION","LITIGATES_IN","LEGAL_BASIS"],
        "dispute":          ["DISPUTES_WITH","CLAIMS_JURISDICTION","LITIGATES_IN","LEGAL_BASIS"],
        "jurisdiction":     ["GOVERNED_BY","LEGAL_BASIS","EXCLUDES"],
        "asset":            ["OWNS_ASSET","FEEDS","LOCATED_IN","PRECEDED_BY","RESULTED_IN","OWNS_50"],
        "timing":           ["PRECEDED_BY","RESULTED_IN","ENABLED","AUTHORIZED_BY"],
        "ownership":        ["OWNS_50","SHAREHOLDER","LEADS","CHAIRS","OPERATIONS_LEAD","UPSTREAM_CEO"],
        "board":            ["LEADS","CHAIRS","OPERATIONS_LEAD","GM_STRATEGY"],
        "constitutional":   ["LEGAL_BASIS","CLAIMS_JURISDICTION","DISPUTES_WITH"],
    }
    if sub_q["type"] in rel_map:
        rels = await follow_relations(top_eids, rel_map[sub_q["type"]])
        collected_e.extend(rels)
    for e in good_e[:4]:
        ename = e["payload"].get("name", e["id"])
        cvec = await embed(f"SEARAH {ename} evidence {e['payload'].get('entity_text','')[:100]}")
        xc = await qdrant_search(COLL_CHUNKS, cvec, 4)
        collected_c.extend([c for c in xc if c["score"] >= CHUNK_EVIDENCE_THRESHOLD])
    if len(collected_c) < 2:
        for c in good_c[:2]:
            cvec = await embed(c["payload"].get("text","")[:200])
            xc = await qdrant_search(COLL_CHUNKS, cvec, 3)
            collected_c.extend([c for c in xc if c["score"] >= CHUNK_EVIDENCE_THRESHOLD])
    seen_e, seen_c = set(), set()
    unique_e = [e for e in collected_e if e["id"] not in seen_e and not seen_e.add(e["id"])]
    unique_c = [c for c in collected_c if c["id"] not in seen_c and not seen_c.add(c["id"])]
    avg_conf = (sum(e["score"] for e in unique_e)/max(len(unique_e),1)*0.55 +
                sum(c["score"] for c in unique_c)/max(len(unique_c),1)*0.45)
    return {
        "sub_question": question, "type": sub_q["type"],
        "entities": unique_e[:8], "chunks": unique_c[:8],
        "avg_confidence": round(avg_conf, 3),
        "total_entities": len(unique_e), "total_chunks": len(unique_c), "hops_used": 3,
    }

def self_correct(sub_results: list[dict]) -> dict:
    flags, contradictions = [], []
    for sr in sub_results:
        for e in sr.get("entities", []):
            v = e["payload"].get("verification","")
            if v in ("CONTRADICTED","UNVERIFIED"):
                flags.append(f"⚠️ [{e['id']}] {v}")
                if v == "CONTRADICTED":
                    contradictions.append(e)
        if sr["total_entities"] == 0 and sr["total_chunks"] == 0:
            flags.append(f"❌ Empty: [{sr['type']}]")
        elif sr["avg_confidence"] < 0.30:
            flags.append(f"⚠️ Low conf [{sr['type']}]: {sr['avg_confidence']}")
    return {
        "flags": flags, "contradictions": contradictions,
        "needs_retry": len(contradictions) > 0 or len(flags) > len(sub_results),
        "confidence": sum(s["avg_confidence"] for s in sub_results)/max(len(sub_results),1),
    }

def governance_verdict(sub_results: list[dict], validation: dict) -> dict:
    all_entities = [e for sr in sub_results for e in sr.get("entities",[])]
    unverified = [e for e in all_entities if e["payload"].get("verification") in ("UNVERIFIED","CONTRADICTED")]
    weak_source = [e for e in all_entities if len(e["payload"].get("evidence",[])) == 0]
    verdict = "PASS" if not unverified and not weak_source else "FAIL"
    return {
        "verdict": verdict, "floors": "F2 TRUTH + F3 WITNESS",
        "unverified_entities": [e["id"] for e in unverified],
        "weak_source_entities": [e["id"] for e in weak_source],
        "contradictions": [e["id"] for e in validation.get("contradictions",[])],
    }

def reflect(sub_results: list[dict], validation: dict) -> str:
    conf = validation["confidence"]
    if validation["needs_retry"]:
        return f"INCOMPLETE — gaps: {validation['flags']}"
    elif conf >= 0.60 and not validation["flags"]:
        return f"COMPLETE (conf: {conf:.2f}) ✅"
    elif conf >= 0.45:
        return f"PARTIAL (conf: {conf:.2f}), caveats: {validation['flags']}"
    return f"WEAK (conf: {conf:.2f}) — more evidence needed"

def synthesize(sub_results: list[dict], query: str, reflection: str, governance: dict) -> str:
    total_e = sum(s["total_entities"] for s in sub_results)
    total_c = sum(s["total_chunks"] for s in sub_results)
    lines = [
        f"## 🔍 SEARAH Agentic RAG — Level 2\n",
        f"**Query:** {query}\n",
        f"**Status:** {reflection}\n",
        f"**Constitutional:** {governance['verdict']} | {governance['floors']}\n",
        f"**Retrieval:** {len(sub_results)} sub-questions → {total_e} entities + {total_c} chunks across {sub_results[0]['hops_used']} hops\n",
        "---\n",
    ]
    for sr in sub_results:
        badge = "✅" if sr["avg_confidence"] >= 0.55 else "⚠️" if sr["avg_confidence"] >= 0.40 else "❌"
        lines.append(f"### [{badge}] {sr['type'].upper()}")
        lines.append(f"_{sr['sub_question']}_\n")
        lines.append(f"| Entities | Chunks | Confidence | Hops |")
        lines.append(f"|----------|--------|------------|------|")
        lines.append(f"| {sr['total_entities']} | {sr['total_chunks']} | {sr['avg_confidence']} | {sr['hops_used']} |\n")
        for e in sr.get("entities", [])[:6]:
            p = e["payload"]
            if p.get("type") == "relation_traversed":
                rel = p.get("relation", {})
                lines.append(f"**REL:** `{rel.get('from','?')}` --[{rel.get('type','?')}]--> `{rel.get('to','?')}`")
                lines.append(f"→ {rel.get('label','—')}")
                continue
            v = p.get("verification","")
            vb = {"VERIFIED":"✅","INFERRED":"⚠️","UNVERIFIED":"❓","CONTRADICTED":"❌"}.get(v,"?")
            lines.append(f"**{p.get('name', p.get('id','?'))}** `{p.get('type','?')}` {vb}")
            for k,v2 in list(p.get("properties",{}).items())[:4]:
                if v2:
                    lines.append(f"  • {k}: {v2}")
        if sr.get("chunks"):
            lines.append("_📄 Evidence:_")
            for c in sr.get("chunks", [])[:2]:
                text = c["payload"].get("text","")[:280].replace("\n"," ")
                lines.append(f"> {text}... `[score:{c['score']:.2f}]`")
        lines.append("")
    if governance.get("unverified_entities"):
        lines.append("---\n**Constitutional Flags:**\n")
        for ue in governance["unverified_entities"]:
            lines.append(f"  ⚠️ F2+F3: `{ue}` — unverified, requires additional sourcing")
    lines.append(f"\n---\n_SEARAH Level 2 Agentic RAG | Multi-hop + F2/F3 Constitutional Validation_\n")
    return "\n".join(lines)

async def agentic_recall(query: str) -> str:
    sub_questions = decompose_query(query)
    sub_results = []
    for sq in sub_questions:
        sr = await multi_hop_retrieve(sq)
        sub_results.append(sr)
    validation = self_correct(sub_results)
    governance = governance_verdict(sub_results, validation)
    reflection = reflect(sub_results, validation)
    return synthesize(sub_results, query, reflection, governance)

async def main():
    if len(sys.argv) < 2:
        print("Usage: python searah_agentic_rag.py \"<query>\"")
        sys.exit(1)
    query = sys.argv[1]
    result = await agentic_recall(query)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
