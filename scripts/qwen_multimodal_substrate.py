#!/usr/bin/env python3
"""
qwen_multimodal_substrate.py — Unified Multimodal Embedding & Rerank Substrate for arifOS Federation
===================================================================================================
Provides persistent multimodal vision embeddings, dense text embeddings, and neural cross-encoder
reranking with an on-disk SHA256 cache and Parquet/DuckDB storage.

Built to convert ephemeral cloud compute into permanent offline assets for future federation agents.

Usage:
  # Search geological visuals using natural language:
  python3 qwen_multimodal_substrate.py search-geox "seismic section fault reflectors"

  # Search canon/skills:
  python3 qwen_multimodal_substrate.py search-canon "human attention membrane"

  # Run full harvest/index:
  python3 qwen_multimodal_substrate.py index-all
"""

import os
import sys
import json
import base64
import hashlib
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
import numpy as np

# Try importing pyarrow / pandas / duckdb
try:
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq
    HAS_PYARROW = True
except ImportError:
    HAS_PYARROW = False

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# ── Paths ──────────────────────────────────────────────────────────
STATE_VECTORS_DIR = Path("/root/AAA/state/vectors")
CACHE_DIR = STATE_VECTORS_DIR / "cache"
GEOX_ATLAS_FILE = STATE_VECTORS_DIR / "geox_visual_atlas.parquet"
CANON_SKILLS_FILE = STATE_VECTORS_DIR / "canon_skills_index.parquet"
RERANK_BENCH_FILE = STATE_VECTORS_DIR / "rerank_golden_bench.parquet"

# Ensure directories exist
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# ── Auth & Config ──────────────────────────────────────────────────
def load_api_key() -> str:
    """Safely extracts DashScope/Qwen API Key from environment or root secrets."""
    key = os.getenv("DASHSCOPE_API_KEY") or os.getenv("QWEN_PAYG_API_KEY")
    if key and not key.startswith("${"):
        return key

    secrets_path = Path("/root/.secrets/kunci-root.env")
    if secrets_path.exists():
        with open(secrets_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("export ") and "=" in line:
                    k, v = line[7:].split("=", 1)
                    v = v.strip("\"'")
                    if k in ("DASHSCOPE_API_KEY", "QWEN_PAYG_API_KEY") and not v.startswith("${"):
                        return v
    raise RuntimeError("No valid DASHSCOPE_API_KEY or QWEN_PAYG_API_KEY found.")

# ── Cache Utilities ────────────────────────────────────────────────
def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def get_cached_vector(cache_key: str) -> Optional[np.ndarray]:
    p = CACHE_DIR / f"{cache_key}.npy"
    if p.exists():
        try:
            return np.load(p)
        except Exception:
            return None
    return None

def save_cached_vector(cache_key: str, vector: np.ndarray):
    p = CACHE_DIR / f"{cache_key}.npy"
    np.save(p, vector)

# ── API Calls ──────────────────────────────────────────────────────
def get_http_headers() -> Dict[str, str]:
    import requests
    return {
        "Authorization": f"Bearer {load_api_key()}",
        "Content-Type": "application/json"
    }

def embed_text(texts: List[str], model: str = "qwen3.7-text-embedding") -> List[np.ndarray]:
    """Embeds texts using dense text embedding with disk caching."""
    import requests

    results = [None] * len(texts)
    uncached_indices = []
    uncached_texts = []

    for i, t in enumerate(texts):
        key = f"txt_{model}_{sha256_text(t)}"
        cached = get_cached_vector(key)
        if cached is not None:
            results[i] = cached
        else:
            uncached_indices.append(i)
            uncached_texts.append(t)

    if uncached_texts:
        url = "https://dashscope-intl.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding"
        # DashScope text embedding batch limit: max 25 texts per call
        batch_size = 20
        for b_start in range(0, len(uncached_texts), batch_size):
            b_texts = uncached_texts[b_start:b_start+batch_size]
            b_indices = uncached_indices[b_start:b_start+batch_size]
            
            resp = requests.post(url, headers=get_http_headers(), json={
                "model": model,
                "input": {"texts": b_texts}
            }, timeout=30)
            
            if resp.status_code != 200:
                raise RuntimeError(f"Text embed error {resp.status_code}: {resp.text}")
            
            embs = resp.json()["output"]["embeddings"]
            for idx, e in zip(b_indices, embs):
                vec = np.array(e["embedding"], dtype=np.float32)
                key = f"txt_{model}_{sha256_text(texts[idx])}"
                save_cached_vector(key, vec)
                results[idx] = vec

    return results

def embed_vision(items: List[Dict[str, Any]], model: str = "tongyi-embedding-vision-plus") -> List[np.ndarray]:
    """
    Embeds multimodal items (either {'text': '...'} or {'image': 'path_or_url'}).
    Uses disk caching to prevent duplicate token usage.
    """
    import requests

    results = [None] * len(items)
    uncached_indices = []
    contents_payload = []

    for i, item in enumerate(items):
        if "text" in item:
            cache_key = f"vis_{model}_txt_{sha256_text(item['text'])}"
            cached = get_cached_vector(cache_key)
            if cached is not None:
                results[i] = cached
            else:
                uncached_indices.append(i)
                contents_payload.append({"text": item["text"]})
        elif "image" in item:
            img_val = item["image"]
            if os.path.exists(img_val):
                with open(img_val, "rb") as f:
                    img_bytes = f.read()
                cache_key = f"vis_{model}_img_{sha256_bytes(img_bytes)}"
                cached = get_cached_vector(cache_key)
                if cached is not None:
                    results[i] = cached
                else:
                    # Optimize large images before base64 encode if > 4MB
                    if HAS_PIL and len(img_bytes) > 3 * 1024 * 1024:
                        from io import BytesIO
                        img = Image.open(BytesIO(img_bytes))
                        img.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
                        out_io = BytesIO()
                        img.save(out_io, format="JPEG", quality=85)
                        img_bytes = out_io.getvalue()
                    
                    b64_str = base64.b64encode(img_bytes).decode("utf-8")
                    data_uri = f"data:image/jpeg;base64,{b64_str}"
                    uncached_indices.append(i)
                    contents_payload.append({"image": data_uri})
            else:
                # Web URL
                cache_key = f"vis_{model}_url_{sha256_text(img_val)}"
                cached = get_cached_vector(cache_key)
                if cached is not None:
                    results[i] = cached
                else:
                    uncached_indices.append(i)
                    contents_payload.append({"image": img_val})

    if contents_payload:
        url = "https://dashscope-intl.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding"
        # Send in small chunks of 4 items
        chunk_size = 4
        for c_start in range(0, len(contents_payload), chunk_size):
            chunk_contents = contents_payload[c_start:c_start+chunk_size]
            chunk_indices = uncached_indices[c_start:c_start+chunk_size]
            
            resp = requests.post(url, headers=get_http_headers(), json={
                "model": model,
                "input": {"contents": chunk_contents}
            }, timeout=45)
            
            if resp.status_code != 200:
                raise RuntimeError(f"Vision embed error {resp.status_code}: {resp.text}")
            
            embs = resp.json()["output"]["embeddings"]
            for idx, e in zip(chunk_indices, embs):
                vec = np.array(e["embedding"], dtype=np.float32)
                item = items[idx]
                if "text" in item:
                    k = f"vis_{model}_txt_{sha256_text(item['text'])}"
                elif "image" in item:
                    img_val = item["image"]
                    if os.path.exists(img_val):
                        with open(img_val, "rb") as f:
                            k = f"vis_{model}_img_{sha256_bytes(f.read())}"
                    else:
                        k = f"vis_{model}_url_{sha256_text(img_val)}"
                save_cached_vector(k, vec)
                results[idx] = vec

    return results

def rerank(query: str, documents: List[str], model: str = "qwen3-rerank") -> List[Dict[str, Any]]:
    """Scores documents against query using neural cross-encoder."""
    import requests
    url = "https://dashscope-intl.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank"
    resp = requests.post(url, headers=get_http_headers(), json={
        "model": model,
        "input": {
            "query": query,
            "documents": documents
        }
    }, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(f"Rerank error {resp.status_code}: {resp.text}")
    return resp.json()["output"]["results"]

# ── Indexing Pipelines ─────────────────────────────────────────────
def index_geox_visuals():
    """Scans and embeds all geological and seismic visual assets in GEOX."""
    print(">>> [PIPELINE 1] Indexing GEOX Subsurface Visual Atlas...")
    valid_exts = {".png", ".jpg", ".jpeg"}
    image_paths = []

    # Priority directories
    priority_dirs = [
        Path("/root/GEOX/geox/seismic"),
        Path("/root/GEOX/artifacts"),
        Path("/root/GEOX/data"),
        Path("/root/GEOX/outputs"),
        Path("/root/GEOX/docs"),
        Path("/root/GEOX/forge_work")
    ]

    for p_dir in priority_dirs:
        if p_dir.exists():
            for p in p_dir.rglob("*"):
                if p.suffix.lower() in valid_exts and p.is_file():
                    sz = p.stat().st_size
                    # Filter out tiny logos/textures < 5KB
                    if sz > 5120 and "node_modules" not in str(p) and "cesium" not in str(p):
                        image_paths.append(p)

    # Root GEOX diagrams
    for p in Path("/root/GEOX").glob("*.png"):
        if p.is_file() and p.stat().st_size > 5120:
            image_paths.append(p)

    image_paths = sorted(list(set(image_paths)))
    print(f"  Found {len(image_paths)} primary geological visual assets.")

    records = []
    items_to_embed = []
    valid_paths = []

    for img_p in image_paths:
        name = img_p.name
        # Simple category inference from path/name
        cat = "general_geology"
        if "seismic" in str(img_p).lower():
            cat = "seismic_section"
        elif "well" in str(img_p).lower():
            cat = "well_log"
        elif "sunda" in str(img_p).lower() or "volcan" in str(img_p).lower():
            cat = "volcanology_tectonics"

        items_to_embed.append({"image": str(img_p)})
        valid_paths.append((img_p, cat))

    print(f"  Computing vision embeddings (tongyi-embedding-vision-plus)...")
    vectors = embed_vision(items_to_embed, model="tongyi-embedding-vision-plus")

    for (p, cat), vec in zip(valid_paths, vectors):
        records.append({
            "path": str(p),
            "filename": p.name,
            "category": cat,
            "size_bytes": p.stat().st_size,
            "dim": len(vec),
            "vector": vec.tolist()
        })

    # Save to Parquet
    df = pd.DataFrame(records)
    table = pa.Table.from_pandas(df)
    pq.write_table(table, GEOX_ATLAS_FILE)
    print(f"  [SUCCESS] Wrote {len(records)} visual embeddings to {GEOX_ATLAS_FILE}!")

def index_canon_and_skills():
    """Scans and dense-embeds canonical doctrine and federation skills."""
    print(">>> [PIPELINE 2] Indexing Federation Canon & Core Skills...")
    records = []
    texts_to_embed = []
    meta_list = []

    # 1. Canon docs
    canon_dir = Path("/root/AAA/canon")
    if canon_dir.exists():
        for p in sorted(canon_dir.glob("*.md")):
            try:
                content = p.read_text(encoding="utf-8")
                # Title and first 1000 chars for semantic anchor
                title = p.stem.replace("-", " ").replace("_", " ")
                preview = content[:1500].strip()
                embed_text_repr = f"Canon: {title}\nContent: {preview}"
                texts_to_embed.append(embed_text_repr)
                meta_list.append({
                    "id": p.name,
                    "type": "canon",
                    "path": str(p),
                    "title": title
                })
            except Exception:
                pass

    # 2. Key active skills
    skill_roots = [
        Path("/root/AAA/skills"),
        Path("/root/arifOS/skills"),
        Path("/root/HERMES/skills")
    ]
    seen_skills = set()
    for s_root in skill_roots:
        if s_root.exists():
            for p in s_root.rglob("SKILL.md"):
                skill_id = p.parent.name
                if skill_id in seen_skills:
                    continue
                seen_skills.add(skill_id)
                try:
                    c = p.read_text(encoding="utf-8")
                    preview = c[:1200].strip()
                    embed_repr = f"Skill: {skill_id}\n{preview}"
                    texts_to_embed.append(embed_repr)
                    meta_list.append({
                        "id": skill_id,
                        "type": "skill",
                        "path": str(p),
                        "title": skill_id
                    })
                    if len(meta_list) >= 150: # Cap to high-priority skills to conserve text quota
                        break
                except Exception:
                    pass
        if len(meta_list) >= 150:
            break

    print(f"  Embedding {len(texts_to_embed)} canon & skill documents (qwen3.7-text-embedding)...")
    vectors = embed_text(texts_to_embed, model="qwen3.7-text-embedding")

    for meta, vec in zip(meta_list, vectors):
        records.append({
            "id": meta["id"],
            "type": meta["type"],
            "path": meta["path"],
            "title": meta["title"],
            "dim": len(vec),
            "vector": vec.tolist()
        })

    df = pd.DataFrame(records)
    table = pa.Table.from_pandas(df)
    pq.write_table(table, CANON_SKILLS_FILE)
    print(f"  [SUCCESS] Wrote {len(records)} canon & skill embeddings to {CANON_SKILLS_FILE}!")

# ── Local Search Methods ───────────────────────────────────────────
def search_geox_visuals(query: str, top_k: int = 5):
    """Searches GEOX visual atlas via cross-modal cosine similarity in sub-10ms."""
    if not GEOX_ATLAS_FILE.exists():
        print("GEOX Atlas not found. Running index first...")
        index_geox_visuals()

    table = pq.read_table(GEOX_ATLAS_FILE)
    df = table.to_pandas()

    # Embed query text in vision space
    q_vec = embed_vision([{"text": query}], model="tongyi-embedding-vision-plus")[0]
    q_norm = np.linalg.norm(q_vec) + 1e-8

    scores = []
    for vec in df["vector"]:
        v = np.array(vec, dtype=np.float32)
        sim = float(np.dot(q_vec, v) / (q_norm * (np.linalg.norm(v) + 1e-8)))
        scores.append(sim)

    df["similarity"] = scores
    top_df = df.sort_values(by="similarity", ascending=False).head(top_k)

    print(f"\n=== Visual Search Results for: '{query}' ===")
    for idx, row in top_df.iterrows():
        print(f"  [{row['similarity']:.4f}] {row['filename']} ({row['category']})")
        print(f"         Path: {row['path']}")
    return top_df

def search_canon(query: str, top_k: int = 5):
    """Searches Canon & Skills via text cosine similarity + optional rerank."""
    if not CANON_SKILLS_FILE.exists():
        print("Canon/Skills Index not found. Running index first...")
        index_canon_and_skills()

    table = pq.read_table(CANON_SKILLS_FILE)
    df = table.to_pandas()

    q_vec = embed_text([query], model="qwen3.7-text-embedding")[0]
    q_norm = np.linalg.norm(q_vec) + 1e-8

    scores = []
    for vec in df["vector"]:
        v = np.array(vec, dtype=np.float32)
        sim = float(np.dot(q_vec, v) / (q_norm * (np.linalg.norm(v) + 1e-8)))
        scores.append(sim)

    df["similarity"] = scores
    top_df = df.sort_values(by="similarity", ascending=False).head(top_k * 2)

    # Cross-encoder Rerank top candidates for surgical precision
    cand_texts = [f"{r['title']}: {Path(r['path']).read_text(encoding='utf-8')[:300]}" for _, r in top_df.iterrows()]
    rr_res = rerank(query, cand_texts)

    ranked_indices = [item["index"] for item in rr_res]
    relevance_scores = [item["relevance_score"] for item in rr_res]

    print(f"\n=== Canon & Skill Search (2-Stage Vector + Qwen3 Rerank) for: '{query}' ===")
    top_candidates = top_df.iloc[ranked_indices].copy()
    top_candidates["rerank_score"] = relevance_scores

    for idx, row in top_candidates.head(top_k).iterrows():
        print(f"  [Rerank: {row['rerank_score']:.4f} | Cosine: {row['similarity']:.4f}] {row['id']} ({row['type']})")
        print(f"         Path: {row['path']}")

    return top_candidates.head(top_k)

# ── CLI Interface ──────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]
    if cmd == "index-all":
        index_geox_visuals()
        index_canon_and_skills()
    elif cmd == "index-geox":
        index_geox_visuals()
    elif cmd == "index-canon":
        index_canon_and_skills()
    elif cmd == "search-geox":
        q = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "seismic interpretation fault reflection"
        search_geox_visuals(q)
    elif cmd == "search-canon":
        q = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "sovereign human attention membrane"
        search_canon(q)
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
