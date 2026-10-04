#!/usr/bin/env python3
"""
YouTube transcript fetch router — S0..S5 cascade with auto-cache.

Cascade order (each layer only runs if previous failed):

  S0  Cache hit              → /root/.cache/youtube-content/<vid>.json   (FREE)
  S1  youtube-transcript-api → direct library call                          (FREE, blocked on VPS)
  S2  yt-dlp subtitles       → yt-dlp --write-auto-sub --skip-download     (FREE, blocked on VPS)
  S3  audio + whisper        → download audio, transcribe locally           (compute cost)
  S4  cookies file           → yt-dlp/youtube-transcript-api with --cookies (FREE, account risk)
  S5  user-paste transcript  → reads /root/.cache/youtube-content/<vid>.paste.txt
  S6  Supadata hosted API     → 100 free credits/mo, then paid              (external)
  S7  Composio managed       → if COMPOSIO_API_KEY in env, list_captions   (external)

Output: structured JSON written to cache + stdout, with `source` field showing
which stage succeeded.

Usage:
  uv run python3 fetch_router.py "https://youtube.com/watch?v=VIDEO_ID"
  uv run python3 fetch_router.py VIDEO_ID --language en
  uv run python3 fetch_router.py VIDEO_ID --cookies /root/.secrets/yt-cookies.txt
  uv run python3 fetch_router.py VIDEO_ID --no-cache       # force re-fetch
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

# Local imports (cache module)
sys.path.insert(0, str(Path(__file__).parent))
from cache import cache_get, cache_put, cache_save_paste, CACHE_ROOT  # noqa: E402


VIDEO_ID_PATTERNS = [
    r'(?:v=|youtu\.be/|shorts/|embed/|live/)([a-zA-Z0-9_-]{11})',
    r'^([a-zA-Z0-9_-]{11})$',
]


def extract_video_id(url_or_id: str) -> str:
    s = url_or_id.strip()
    for p in VIDEO_ID_PATTERNS:
        m = re.search(p, s)
        if m:
            return m.group(1)
    return s


def format_timestamp(seconds: float) -> str:
    total = int(seconds)
    h, remainder = divmod(total, 3600)
    m, s = divmod(remainder, 60)
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


# ── S1: youtube-transcript-api ────────────────────────────────────────────────
def s1_transcript_api(video_id: str, language: str = "") -> dict:
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        return {"ok": False, "stage": "S1", "error": "youtube-transcript-api not installed"}
    try:
        api = YouTubeTranscriptApi()
        langs = [language] if language else None
        result = api.fetch(video_id, languages=langs) if langs else api.fetch(video_id)
        segs = [{"text": s.text, "start": s.start, "duration": s.duration} for s in result]
        if not segs:
            return {"ok": False, "stage": "S1", "error": "empty transcript"}
        return {
            "ok": True,
            "stage": "S1",
            "source": "youtube-transcript-api",
            "transcript": {
                "segment_count": len(segs),
                "duration": format_timestamp(segs[-1]["start"] + segs[-1]["duration"]),
                "full_text": " ".join(s["text"] for s in segs),
                "timestamped_text": "\n".join(f"{format_timestamp(s['start'])} {s['text']}" for s in segs),
                "segments": segs,
            },
        }
    except Exception as e:
        return {"ok": False, "stage": "S1", "error": f"{type(e).__name__}: {str(e)[:300]}"}


# ── S2: yt-dlp subtitles ─────────────────────────────────────────────────────
def s2_ytdlp_subs(video_id: str, cookies: str = "", language: str = "") -> dict:
    out_dir = tempfile.mkdtemp(prefix=f"ytsub_{video_id}_")
    cmd = [
        "yt-dlp", f"https://youtube.com/watch?v={video_id}",
        "--skip-download",
        "--write-auto-sub", "--write-sub",
        "--sub-format", "vtt",
        "--sub-langs", language or "en.*,en",
        "-o", os.path.join(out_dir, "%(id)s.%(ext)s"),
    ]
    if cookies:
        cmd += ["--cookies", cookies]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    except FileNotFoundError:
        return {"ok": False, "stage": "S2", "error": "yt-dlp not on PATH"}
    except subprocess.TimeoutExpired:
        return {"ok": False, "stage": "S2", "error": "yt-dlp timed out after 90s"}
    if result.returncode != 0:
        return {"ok": False, "stage": "S2", "error": (result.stderr or result.stdout).strip()[:400]}

    vtt_files = list(Path(out_dir).glob("*.vtt"))
    if not vtt_files:
        return {"ok": False, "stage": "S2", "error": "no .vtt files downloaded"}

    segs, full_lines = [], []
    for vtt_path in sorted(vtt_files):
        try:
            text = vtt_path.read_text(encoding="utf-8", errors="ignore")
        except OSError as e:
            continue
        # Parse VTT: skip WEBVTT header, capture cue text + start time
        for m in re.finditer(r"(\d{2}:)?(\d{2}):(\d{2})\.(\d{3})\s+-->.*?\n((?:.*?\n)+?)(?=\n\n|\Z)", text):
            h = int(m.group(1) or "0") if m.group(1) else 0
            mm = int(m.group(2))
            ss = int(m.group(3))
            start = h * 3600 + mm * 60 + ss
            cue = " ".join(line.strip() for line in m.group(5).split("\n") if line.strip())
            cue = re.sub(r"<[^>]+>", "", cue)
            if cue:
                segs.append({"text": cue, "start": float(start), "duration": 0.0})
                full_lines.append(f"{format_timestamp(start)} {cue}")

    if not segs:
        return {"ok": False, "stage": "S2", "error": "no cues parsed from VTT"}

    return {
        "ok": True,
        "stage": "S2",
        "source": "yt-dlp-subtitles",
        "transcript": {
            "segment_count": len(segs),
            "duration": format_timestamp(max(s["start"] for s in segs)),
            "full_text": " ".join(s["text"] for s in segs),
            "timestamped_text": "\n".join(full_lines),
            "segments": segs,
        },
    }


# ── S3: audio + whisper ──────────────────────────────────────────────────────
def s3_whisper(video_id: str, cookies: str = "", model: str = "base") -> dict:
    audio_dir = tempfile.mkdtemp(prefix=f"ytaudio_{video_id}_")
    audio_path = os.path.join(audio_dir, f"{video_id}.m4a")
    # Extract bestaudio
    cmd = [
        "yt-dlp", f"https://youtube.com/watch?v={video_id}",
        "-f", "bestaudio[ext=m4a]/bestaudio",
        "-o", audio_path,
    ]
    if cookies:
        cmd += ["--cookies", cookies]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    except subprocess.TimeoutExpired:
        return {"ok": False, "stage": "S3", "error": "yt-dlp audio extraction timed out"}
    if r.returncode != 0:
        return {"ok": False, "stage": "S3", "error": (r.stderr or r.stdout).strip()[:300]}
    if not Path(audio_path).exists():
        # yt-dlp may have used a different extension
        candidates = list(Path(audio_dir).glob(f"{video_id}.*"))
        if candidates:
            audio_path = str(candidates[0])
        else:
            return {"ok": False, "stage": "S3", "error": "audio file not produced"}

    # Run whisper
    try:
        w = subprocess.run(
            ["whisper", audio_path, "--model", model, "--output_format", "json", "--output_dir", audio_dir],
            capture_output=True, text=True, timeout=600,
        )
    except FileNotFoundError:
        return {"ok": False, "stage": "S3", "error": "whisper CLI not on PATH (install: pip install openai-whisper)"}
    except subprocess.TimeoutExpired:
        return {"ok": False, "stage": "S3", "error": "whisper timed out after 600s"}
    if w.returncode != 0:
        return {"ok": False, "stage": "S3", "error": (w.stderr or w.stdout).strip()[:400]}

    # whisper writes <basename>.json
    json_candidates = list(Path(audio_dir).glob(f"{Path(audio_path).stem}.json")) + list(Path(audio_dir).glob("*.json"))
    if not json_candidates:
        return {"ok": False, "stage": "S3", "error": "whisper produced no JSON output"}
    try:
        wjson = json.loads(json_candidates[0].read_text(encoding="utf-8"))
        segs = wjson.get("segments", [])
        if not segs:
            return {"ok": False, "stage": "S3", "error": "whisper returned 0 segments"}
        full = wjson.get("text", "").strip()
        return {
            "ok": True,
            "stage": "S3",
            "source": f"whisper-{model}",
            "transcript": {
                "segment_count": len(segs),
                "duration": format_timestamp(segs[-1].get("end", 0)),
                "full_text": full,
                "timestamped_text": "\n".join(
                    f"{format_timestamp(s.get('start', 0))} {s.get('text', '').strip()}" for s in segs
                ),
                "segments": [
                    {"text": s.get("text", "").strip(), "start": s.get("start", 0), "duration": s.get("end", 0) - s.get("start", 0)}
                    for s in segs
                ],
            },
        }
    except Exception as e:
        return {"ok": False, "stage": "S3", "error": f"whisper JSON parse: {e}"}


# ── S4: cookies file (delegates to S1/S2 with --cookies) ──────────────────────
def s4_cookies(video_id: str, cookies: str, language: str = "") -> dict:
    if not cookies or not Path(cookies).exists():
        return {"ok": False, "stage": "S4", "error": f"cookies file not found: {cookies}"}
    # Try transcript API first
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        # Note: youtube-transcript-api doesn't natively support cookies; pass via env
        # Most users pair cookies with yt-dlp; we go directly to S2 variant.
    except ImportError:
        pass
    # Fall through to yt-dlp with cookies
    res = s2_ytdlp_subs(video_id, cookies=cookies, language=language)
    if res.get("ok"):
        res["stage"] = "S4"
        res["source"] = f"yt-dlp-cookies({cookies})"
    return res


# ── S5: user-pasted transcript ────────────────────────────────────────────────
def s5_paste(video_id: str) -> dict:
    paste_p = CACHE_ROOT / f"{video_id}.paste.txt"
    if not paste_p.exists():
        return {"ok": False, "stage": "S5", "error": f"no paste file at {paste_p}"}
    try:
        raw = paste_p.read_text(encoding="utf-8")
    except OSError as e:
        return {"ok": False, "stage": "S5", "error": f"read failed: {e}"}
    if not raw.strip():
        return {"ok": False, "stage": "S5", "error": "paste file empty"}
    # Try to detect timestamped format [00:00] or [HH:MM:SS]
    segs = []
    full_lines = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        m = re.match(r"\[(?:(\d+):)?(\d{1,2}):(\d{2})\]\s*(.+)", line)
        if m:
            h = int(m.group(1) or 0)
            mm = int(m.group(2))
            ss = int(m.group(3))
            start = h * 3600 + mm * 60 + ss
            segs.append({"text": m.group(4).strip(), "start": float(start), "duration": 0.0})
            full_lines.append(line)
        else:
            full_lines.append(line)
    if not segs:
        # Treat as single blob
        return {
            "ok": True,
            "stage": "S5",
            "source": "user-paste-plain",
            "transcript": {
                "segment_count": 1,
                "duration": "0:00",
                "full_text": raw,
                "timestamped_text": raw,
                "segments": [{"text": raw, "start": 0.0, "duration": 0.0}],
            },
        }
    return {
        "ok": True,
        "stage": "S5",
        "source": "user-paste-timestamped",
        "transcript": {
            "segment_count": len(segs),
            "duration": format_timestamp(max(s["start"] for s in segs)),
            "full_text": " ".join(s["text"] for s in segs),
            "timestamped_text": "\n".join(full_lines),
            "segments": segs,
        },
    }


# ── S8: TranscriptAPI.com (hosted — proven to bypass VPS IP block) ───────────
def s8_transcriptapi(video_id: str, api_key: str = "", language: str = "") -> dict:
    """
    TranscriptAPI.com — 100 free credits/mo, no card required.
    Verified 2026-08-08: HTTP 200, 44.9 KB, 400 segments returned for lpLReXGD2Kg
    where S1/S2/S3 all failed. Uses YouTube's internal ASR + caption tracks.

    IMPORTANT: Must include User-Agent header (Cloudflare 1010 block otherwise).
    """
    key = api_key or os.getenv("TRANSCRIPT_API_KEY", "")
    if not key:
        return {"ok": False, "stage": "S8", "error": "TRANSCRIPT_API_KEY not set"}
    try:
        import urllib.request
        import urllib.error
        # ZeroPoint skill pattern: format=json + include_timestamp=true + send_metadata=true
        url = (
            f"https://transcriptapi.com/api/v2/youtube/transcript"
            f"?video_url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D{video_id}"
            f"&format=json&include_timestamp=true&send_metadata=true"
        )
        req = urllib.request.Request(url, headers={
            "Authorization": f"Bearer {key}",
            "User-Agent": "HermesAgent/0.11.0",
        })
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"ok": False, "stage": "S8", "error": f"HTTP {e.code}: {e.reason}"}
    except Exception as e:
        return {"ok": False, "stage": "S8", "error": f"{type(e).__name__}: {str(e)[:200]}"}

    if "transcript" not in data:
        return {"ok": False, "stage": "S8", "error": f"unexpected response: {str(data)[:200]}"}

    segs_raw = data["transcript"]
    if not segs_raw:
        return {"ok": False, "stage": "S8", "error": "empty transcript array"}

    # Normalize to router's segment shape
    segs, full = [], []
    for s in segs_raw:
        text = (s.get("text") or "").strip()
        start = float(s.get("start") or 0)
        dur = float(s.get("duration") or 0)
        if text:
            segs.append({"text": text, "start": start, "duration": dur})
            full.append(f"{format_timestamp(start)} {text}")

    if not segs:
        return {"ok": False, "stage": "S8", "error": "no usable segments after normalization"}

    meta = data.get("metadata", {})
    return {
        "ok": True,
        "stage": "S8",
        "source": "transcriptapi.com",
        "metadata": {
            "title": meta.get("title", ""),
            "channel": meta.get("author_name", ""),
            "channel_url": meta.get("author_url", ""),
            "thumbnail_url": meta.get("thumbnail_url", ""),
            "language": data.get("language", ""),
        },
        "transcript": {
            "segment_count": len(segs),
            "duration": format_timestamp(segs[-1]["start"] + segs[-1]["duration"]),
            "full_text": " ".join(s["text"] for s in segs),
            "timestamped_text": "\n".join(full),
            "segments": segs,
        },
    }


# ── S6: Supadata ─────────────────────────────────────────────────────────────
def s6_supadata(video_id: str, api_key: str = "", language: str = "en") -> dict:
    key = api_key or os.getenv("SUPADATA_API_KEY", "")
    if not key:
        return {"ok": False, "stage": "S6", "error": "SUPADATA_API_KEY not set"}
    try:
        import urllib.request
        url = (
            f"https://api.supadata.ai/v1/youtube/transcript"
            f"?videoId={video_id}&language={language}&text=false&timestamps=true"
        )
        req = urllib.request.Request(url, headers={"x-api-key": key})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"ok": False, "stage": "S6", "error": f"{type(e).__name__}: {str(e)[:200]}"}
    segs_raw = data.get("content") or data.get("segments") or []
    if not segs_raw:
        return {"ok": False, "stage": "S6", "error": f"empty response: {str(data)[:200]}"}
    segs = []
    full = []
    for s in segs_raw:
        text = s.get("text") or s.get("caption") or ""
        start = float(s.get("start") or s.get("offset") or 0)
        duration = float(s.get("duration") or 0)
        segs.append({"text": text, "start": start, "duration": duration})
        full.append(f"{format_timestamp(start)} {text}")
    if not segs:
        return {"ok": False, "stage": "S6", "error": "no segments parsed"}
    return {
        "ok": True,
        "stage": "S6",
        "source": "supadata",
        "transcript": {
            "segment_count": len(segs),
            "duration": format_timestamp(segs[-1]["start"] + segs[-1]["duration"]),
            "full_text": " ".join(s["text"] for s in segs),
            "timestamped_text": "\n".join(full),
            "segments": segs,
        },
    }


# ── S7: Composio ─────────────────────────────────────────────────────────────
def s7_composio(video_id: str, api_key: str = "") -> dict:
    key = api_key or os.getenv("COMPOSIO_API_KEY", "")
    if not key:
        return {"ok": False, "stage": "S7", "error": "COMPOSIO_API_KEY not set"}
    # Composio v3 endpoint — list_captions returns caption tracks for a video.
    # We use this as an existence probe. Caption text download typically requires
    # the user's YouTube OAuth via Composio's hosted flow, so we surface the
    # manifest + nudge to S5 (paste) for raw text.
    try:
        import urllib.request
        import urllib.error
        url = f"https://backend.composio.dev/api/v3/tools/execute/YOUTUBE_LIST_CAPTIONS"
        body = json.dumps({"input": {"id": video_id, "part": "snippet"}}).encode()
        req = urllib.request.Request(
            url, data=body,
            headers={"x-api-key": key, "Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"ok": False, "stage": "S7", "error": f"HTTP {e.code}: {e.reason}"}
    except Exception as e:
        return {"ok": False, "stage": "S7", "error": f"{type(e).__name__}: {str(e)[:200]}"}
    # v3 response shape: {"data": {...response...}, "error": null}
    response = data.get("data", data)
    items = response.get("items", []) if isinstance(response, dict) else []
    if not items:
        return {"ok": False, "stage": "S7", "error": f"no captions listed; response={str(data)[:200]}"}
    return {
        "ok": False,
        "stage": "S7",
        "source": "composio-manifest",
        "error": "manifest returned; captions require OAuth download via Composio hosted flow. Use S5 (paste) for raw text.",
        "manifest": [{"id": it.get("id"), "language": it.get("snippet", {}).get("language")} for it in items[:10]],
    }


# ── Cascade orchestrator ─────────────────────────────────────────────────────
STAGES = [
    ("S1", "youtube-transcript-api (direct)", s1_transcript_api),
    ("S2", "yt-dlp subtitles (direct)", None),  # dynamic — needs cookies arg
    ("S4", "yt-dlp with cookies", None),
    ("S5", "user-pasted transcript", s5_paste),
    ("S6", "Supadata hosted API", s6_supadata),
    ("S7", "Composio managed", s7_composio),
    ("S3", "audio + whisper (slow)", s3_whisper),
]


def run_cascade(video_id: str, *, language: str = "", cookies: str = "", no_cache: bool = False, whisper_model: str = "base") -> dict:
    """Run S0..S5 cascade; return first success or all failures."""
    # ── S0: cache ──
    if not no_cache:
        hit = cache_get(video_id)
        if hit and hit.get("transcript"):
            return {
                "ok": True,
                "stage": "S0",
                "source": f"cache:{hit.get('source', 'unknown')}",
                "cached_at": hit.get("fetched_at"),
                "transcript": hit["transcript"],
                "metadata": hit.get("metadata", {}),
                "sha256": hit.get("sha256"),
                "cached_path": str(CACHE_ROOT / f"{video_id}.json"),
            }

    attempts = []

    # ── S8: TranscriptAPI.com (free tier, external bypass) ──
    # Per Apex verdict 2026-08-08: tested proven against lpLReXGD2Kg, 200/44977 bytes / 400 segments
    # Placed BEFORE S1 because it actually works from VPS where S1/S2 fail.
    if os.getenv("TRANSCRIPT_API_KEY"):
        r = s8_transcriptapi(video_id, language=language)
        attempts.append({"stage": r["stage"], "ok": r["ok"], "error": r.get("error")})
        if r["ok"]:
            return _finalize(video_id, r, attempts)

    # S1
    r = s1_transcript_api(video_id, language=language)
    attempts.append({"stage": r["stage"], "ok": r["ok"], "error": r.get("error")})
    if r["ok"]:
        return _finalize(video_id, r, attempts)

    # S2 (no cookies)
    r = s2_ytdlp_subs(video_id, cookies="", language=language)
    attempts.append({"stage": r["stage"], "ok": r["ok"], "error": r.get("error")})
    if r["ok"]:
        return _finalize(video_id, r, attempts)

    # S4 (with cookies if provided)
    if cookies:
        r = s4_cookies(video_id, cookies, language=language)
        attempts.append({"stage": r["stage"], "ok": r["ok"], "error": r.get("error")})
        if r["ok"]:
            return _finalize(video_id, r, attempts)

    # S5
    r = s5_paste(video_id)
    attempts.append({"stage": r["stage"], "ok": r["ok"], "error": r.get("error")})
    if r["ok"]:
        return _finalize(video_id, r, attempts)

    # S6
    r = s6_supadata(video_id, language=language)
    attempts.append({"stage": r["stage"], "ok": r["ok"], "error": r.get("error")})
    if r["ok"]:
        return _finalize(video_id, r, attempts)

    # S7
    r = s7_composio(video_id)
    attempts.append({"stage": r["stage"], "ok": r["ok"], "error": r.get("error")})
    if r["ok"]:
        return _finalize(video_id, r, attempts)

    return {"ok": False, "video_id": video_id, "cascade": attempts}


def _finalize(video_id: str, result: dict, attempts: list) -> dict:
    """Cache successful result and return enriched response."""
    payload = {
        "video_id": video_id,
        "url": f"https://youtu.be/{video_id}",
        "source": result.get("source"),
        "stage": result.get("stage"),
        "transcript": result.get("transcript"),
        "metadata": result.get("metadata", {}),
        "cascade_history": attempts,
    }
    stored = cache_put(video_id, payload)
    payload["sha256"] = stored["sha256"]
    payload["cached_path"] = str(CACHE_ROOT / f"{video_id}.json")
    payload["ok"] = True
    return payload


# ── CLI ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="YouTube transcript fetch router — S0..S5 cascade")
    parser.add_argument("url", help="YouTube URL or video ID")
    parser.add_argument("--language", default="", help="Preferred language (e.g. en,ms)")
    parser.add_argument("--cookies", default="", help="Path to Netscape cookies.txt (S4)")
    parser.add_argument("--no-cache", action="store_true", help="Bypass cache, force re-fetch")
    parser.add_argument("--whisper-model", default="base", help="Whisper model size (S3): tiny|base|small|medium|large")
    parser.add_argument("--paste-save", help="Save user text as paste for video_id, then re-run cascade")
    args = parser.parse_args()

    video_id = extract_video_id(args.url)

    if args.paste_save:
        cache_save_paste(video_id, args.paste_save)
        print(json.dumps({"saved_paste": True, "video_id": video_id, "path": str(CACHE_ROOT / f'{video_id}.paste.txt')}))

    result = run_cascade(
        video_id,
        language=args.language,
        cookies=args.cookies,
        no_cache=args.no_cache,
        whisper_model=args.whisper_model,
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result.get("ok") else 1)


if __name__ == "__main__":
    main()