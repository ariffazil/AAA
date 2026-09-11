#!/usr/bin/env python3
"""
refresh_s3.py — REFRESH stage of reality_alignment (F13 authorized 2026-09-12).

Backs up `petronas_knowledge` Qdrant collection, re-embeds canonical PETRONAS
content via bge-m3 (Ollama), replaces stale vectors. Reversible via backup.

Canonical sources: ATLAS.md + KNOWLEDGE_GRAPH.json + WEALTH engine anchors.
Target: Qdrant `petronas_knowledge` (1024-dim cosine). NO SEAL — F13 only.
"""
import json, os, sys, urllib.request, datetime, re

ROOT = "/root"
ATLAS = f"{ROOT}/AAA/canon/PETRONAS/ATLAS.md"
KG = f"{ROOT}/AAA/canon/PETRONAS/KNOWLEDGE_GRAPH.json"
QDRANT = "http://localhost:6333"
OLLAMA = "http://localhost:11434"
COLLECTION = "petronas_knowledge"
TS = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
BACKUP = f"{ROOT}/AAA/canon/PETRONAS/qdrant_backup_{TS}.json"

def http_json(url, method="GET", payload=None, timeout=120):
    req = urllib.request.Request(url, method=method,
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=timeout))

def embed(text):
    r = http_json(f"{OLLAMA}/api/embed", "POST", {"model": "bge-m3", "input": text})
    return r["embeddings"][0]

def scroll_all(limit=500):
    pts, offset = [], None
    while True:
        payload = {"limit": limit, "with_payload": True, "with_vector": True}
        if offset is not None:
            payload["offset"] = offset
        r = http_json(f"{QDRANT}/collections/{COLLECTION}/points/scroll", "POST", payload)
        res = r.get("result", {})
        batch = res.get("points", [])
        if not batch:
            break
        pts.extend(batch)
        nxt = res.get("next_page_offset")
        if nxt is None:
            break
        offset = nxt
    return pts

def canonical_chunks():
    chunks = []
    # 1. ATLAS.md sections
    for s in re.split(r"\n(?=#{1,3} )", open(ATLAS).read()):
        s = s.strip()
        if len(s) > 40:
            chunks.append({"text": s[:3000], "category": "atlas", "source": "ATLAS.md"})
    # 2. KNOWLEDGE_GRAPH.json nodes
    for n in json.load(open(KG))["nodes"]:
        chunks.append({"text":
            f"{n['id']}: {n['summary']} (organ={n['organ']}, pillar={n['pillar']}, status={n['status']}, path={n['path']})",
            "category": "graph", "source": "KNOWLEDGE_GRAPH.json"})
    # 3. Engine anchors (source of truth for financials)
    sys.path.insert(0, f"{ROOT}/WEALTH/wealth_core")
    import petronas_vitals as pv
    eng = {b: (round(pv.compute_brent_sensitivity(b)["projected_full_year_pat_usd_b"], 1),
               pv.compute_brent_sensitivity(b)["projected_extraction_ratio"])
           for b in (100.60, 84.10, 67.34, 50.00)}
    eng_line = (
        "PETRONAS Brent sensitivity (WEALTH compute_brent_sensitivity, engine-calibrated): "
        f"$100.60 → PAT RM{eng[100.60][0]}B, extraction {eng[100.60][1]}%; "
        f"$84.10 → RM{eng[84.10][0]}B, {eng[84.10][1]}%; "
        f"$67.34 → RM{eng[67.34][0]}B, {eng[67.34][1]}% (exit threshold); "
        f"$50.00 → RM{eng[50.00][0]}B, {eng[50.00][1]}%. "
        "FY2025 audited: Revenue RM266.1B (down 16.8%), PAT RM45.4B, dividend RM32B, "
        "FY2026 dividend RM20B (38% cut), extraction 70.5%, CFFO RM85.2B, gearing 20.7%."
    )
    chunks.append({"text": eng_line, "category": "financials", "source": "WEALTH engine"})
    return chunks

def main():
    # 1. Backup
    pts = scroll_all()
    with open(BACKUP, "w") as f:
        json.dump({"collection": COLLECTION, "count": len(pts), "points": pts}, f)
    print(f"[backup] {len(pts)} points → {BACKUP}")

    # 2. Canonical content
    chunks = canonical_chunks()
    print(f"[canonical] {len(chunks)} chunks")

    # 3. Embed
    new_points = []
    for i, c in enumerate(chunks):
        new_points.append({"id": i + 1, "vector": embed(c["text"]),
            "payload": {"text": c["text"], "chunk_id": i + 1,
                        "category": c["category"], "source": c["source"]}})
    print(f"[embed] {len(new_points)} vectors via bge-m3")

    # 4. Replace collection (delete + recreate + upsert)
    http_json(f"{QDRANT}/collections/{COLLECTION}", "DELETE")
    http_json(f"{QDRANT}/collections/{COLLECTION}", "PUT",
              {"vectors": {"size": 1024, "distance": "Cosine"}})
    for i in range(0, len(new_points), 100):
        http_json(f"{QDRANT}/collections/{COLLECTION}/points", "PUT",
                  {"points": new_points[i:i+100]})
    print(f"[upsert] {len(new_points)} points into {COLLECTION}")

    # 5. Verify
    c = http_json(f"{QDRANT}/collections/{COLLECTION}/points/count", "POST", {"exact": True})
    print(f"[verify] final count = {c.get('result', {}).get('count')}")

if __name__ == "__main__":
    main()
