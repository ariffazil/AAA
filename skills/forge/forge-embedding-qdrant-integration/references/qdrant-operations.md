# Qdrant Operations Reference

## Collection Creation

```python
import json, urllib.request

def create_collection(qdrant_url, collection, dim=1024, recreate=False):
    if recreate:
        try:
            req = urllib.request.Request(f"{qdrant_url}/collections/{collection}", method="DELETE")
            urllib.request.urlopen(req, timeout=10)
        except: pass
    payload = json.dumps({
        "vectors": {"size": dim, "distance": "Cosine"},
        "optimizers_config": {"default_segment_number": 2}
    }).encode()
    req = urllib.request.Request(
        f"{qdrant_url}/collections/{collection}",
        data=payload, headers={"Content-Type": "application/json"}, method="PUT")
    urllib.request.urlopen(req, timeout=10)
    idx = json.dumps({"field_name": "doc_type", "field_schema": "keyword"}).encode()
    req = urllib.request.Request(
        f"{qdrant_url}/collections/{collection}/index",
        data=idx, headers={"Content-Type": "application/json"}, method="PUT")
    try: urllib.request.urlopen(req, timeout=10)
    except: pass
```

## Point ID Format

Qdrant requires UUIDs or unsigned integers. Arbitrary strings are SILENTLY rejected — HTTP says acknowledged but point never stored.

```python
import uuid
pid = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{source}:{chunk_idx}"))
```

## Upsert + Verify

```python
def upsert_and_verify(qdrant_url, collection, points, expected):
    for i in range(0, len(points), 100):
        payload = json.dumps({"points": points[i:i+100]}).encode()
        req = urllib.request.Request(
            f"{qdrant_url}/collections/{collection}/points",
            data=payload, headers={"Content-Type": "application/json"}, method="PUT")
        urllib.request.urlopen(req, timeout=30)
    import time; time.sleep(2)
    req = urllib.request.Request(f"{qdrant_url}/collections/{collection}")
    with urllib.request.urlopen(req, timeout=10) as r:
        actual = json.loads(r.read())["result"]["points_count"]
    if actual < expected:
        print(f"WARNING: {actual}/{expected} points stored — check ID format")
    return actual
```

## Filtered Search

```python
def search(qdrant_url, collection, vector, doc_type=None, limit=10):
    body = {"vector": vector, "limit": limit, "with_payload": True}
    if doc_type:
        body["filter"] = {"must": [{"key": "doc_type", "match": {"value": doc_type}}]}
    payload = json.dumps(body).encode()
    req = urllib.request.Request(
        f"{qdrant_url}/collections/{collection}/points/search",
        data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read()).get("result", [])
```

## Diagnosis Checklist

1. Check points_count after upsert — if much lower than expected, points were dropped
2. Most common: invalid point ID (must be UUID, not hex string)
3. Second: vector dimension mismatch (collection dim != actual vector length)
4. Third: payload serialization error (non-UTF8 in text)
5. Test with one manual upsert of a known-good point to isolate the issue
