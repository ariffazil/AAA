#!/usr/bin/env python3
"""
YouTube transcript cache — persistent store keyed by video_id.

Locations (in priority order):
  1. $YT_CACHE_DIR                  (env override)
  2. /root/.cache/youtube-content/  (production default)
  3. ~/.cache/youtube-content/      (fallback)

Schema (one file per video):
  /cache/<video_id>.json
    {
      "video_id": "lpLReXGD2Kg",
      "url": "https://youtu.be/lpLReXGD2Kg",
      "fetched_at": "2026-08-08T...",
      "source": "supadata|cookies|whisper|paste|api",
      "transcript": {"full_text": "...", "timestamped_text": "...", "segments": [...]},
      "metadata": {...},
      "sha256": "..."
    }

  /cache/<video_id>.paste.txt       (raw pasted transcript, if user-provided)
"""

import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path
from datetime import datetime, timezone


def _cache_root() -> Path:
    env = os.getenv("YT_CACHE_DIR", "").strip()
    if env:
        return Path(env)
    for candidate in (Path("/root/.cache/youtube-content"), Path.home() / ".cache" / "youtube-content"):
        try:
            candidate.mkdir(parents=True, exist_ok=True)
            return candidate
        except OSError:
            continue
    return Path(tempfile.mkdtemp(prefix="ytcache_"))


CACHE_ROOT = _cache_root()


def video_path(video_id: str) -> Path:
    return CACHE_ROOT / f"{video_id}.json"


def paste_path(video_id: str) -> Path:
    return CACHE_ROOT / f"{video_id}.paste.txt"


def cache_get(video_id: str) -> dict | None:
    """Return cached digest if present, else None."""
    p = video_path(video_id)
    if not p.exists():
        return None
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def cache_put(video_id: str, payload: dict) -> dict:
    """Write digest to cache. Always computes sha256. Returns the stored record."""
    payload = dict(payload)
    payload.setdefault("video_id", video_id)
    payload.setdefault("url", f"https://youtu.be/{video_id}")
    payload["fetched_at"] = datetime.now(timezone.utc).isoformat()
    payload["sha256"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    p = video_path(video_id)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return payload


def cache_save_paste(video_id: str, raw_text: str) -> Path:
    """Save user-pasted raw transcript. Returns path written."""
    p = paste_path(video_id)
    with open(p, "w", encoding="utf-8") as f:
        f.write(raw_text)
    return p


def cache_list() -> list:
    """List all cached video_ids sorted by mtime descending."""
    if not CACHE_ROOT.exists():
        return []
    out = []
    for p in CACHE_ROOT.glob("*.json"):
        try:
            stat = p.stat()
            out.append({
                "video_id": p.stem,
                "path": str(p),
                "size_bytes": stat.st_size,
                "mtime": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
            })
        except OSError:
            continue
    return sorted(out, key=lambda x: x["mtime"], reverse=True)


def cache_clear(video_id: str | None = None) -> dict:
    """Delete one entry or all. Returns counts."""
    if not CACHE_ROOT.exists():
        return {"removed": 0, "cache_root": str(CACHE_ROOT)}
    removed = 0
    targets = [video_path(video_id)] if video_id else list(CACHE_ROOT.glob("*.json"))
    for p in targets:
        if p.exists():
            p.unlink()
            removed += 1
    return {"removed": removed, "cache_root": str(CACHE_ROOT)}


def main():
    import argparse
    parser = argparse.ArgumentParser(description="YouTube transcript cache CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list").add_argument("--limit", type=int, default=50)
    p_get = sub.add_parser("get")
    p_get.add_argument("video_id")
    p_put = sub.add_parser("put")
    p_put.add_argument("video_id")
    p_put.add_argument("json_file")
    p_clear = sub.add_parser("clear")
    p_clear.add_argument("--video-id", default="")
    args = parser.parse_args()

    if args.cmd == "list":
        rows = cache_list()[:args.limit]
        print(json.dumps({"cache_root": str(CACHE_ROOT), "count": len(rows), "entries": rows}, indent=2))
    elif args.cmd == "get":
        data = cache_get(args.video_id)
        print(json.dumps(data if data else {"error": "not_found", "video_id": args.video_id}, indent=2))
    elif args.cmd == "put":
        with open(args.json_file, encoding="utf-8") as f:
            payload = json.load(f)
        result = cache_put(args.video_id, payload)
        print(json.dumps({"cached": True, "sha256": result["sha256"], "path": str(video_path(args.video_id))}, indent=2))
    elif args.cmd == "clear":
        vid = args.video_id or None
        print(json.dumps(cache_clear(vid), indent=2))


if __name__ == "__main__":
    main()