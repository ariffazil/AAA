#!/usr/bin/env python3
"""ttft_probe.py — streaming TTFT + total + chunk-count prober.

Per live-pipeline-trace-audit SKILL.md: streaming gives true first-token
latency; non-stream `time_starttransfer` includes router/schema round-trip
and is looser. This prober issues a STREAMING request against any
OpenAI-compatible /v1/chat/completions and reports:

  TTFT   = wall time from request send to first parsed `data:` chunk
           carrying non-empty content
  TOTAL  = wall time to stream completion ([DONE])
  CHUNKS = number of content-bearing chunks received

Usage:
  python3 ttft_probe.py --base-url http://127.0.0.1:4011/v1 \
                        --model i-arif --prompt 'reply PONG'
  python3 ttft_probe.py                     # uses defaults below

Auth: reads $OPENAI_API_KEY (or --api-key) and sends it as a Bearer token.
No auth is required by the federation's localhost surfaces, in which case
omit --api-key.
"""
import argparse
import json
import time
import urllib.request
import urllib.error


def probe(base_url, model, prompt, api_key=None, timeout=120, max_tokens=64):
    url = base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "stream": True,
    }
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = "Bearer " + api_key

    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(), headers=headers, method="POST")

    t0 = time.perf_counter()
    ttft = None
    chunks = 0
    text = ""
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            for raw in resp:
                line = raw.decode("utf-8", "replace").strip()
                if not line.startswith("data:"):
                    continue
                data = line[5:].strip()
                if data == "[DONE]":
                    break
                try:
                    obj = json.loads(data)
                except json.JSONDecodeError:
                    continue
                delta = (obj.get("choices") or [{}])[0].get("delta", {})
                piece = delta.get("content") or ""
                if piece:
                    chunks += 1
                    text += piece
                    if ttft is None:
                        ttft = time.perf_counter() - t0
    except urllib.error.HTTPError as exc:
        return {"ok": False, "http_status": exc.code,
                "error": exc.read().decode("utf-8", "replace")[:800]}
    except Exception as exc:  # noqa: BLE001 - probe must never raise
        return {"ok": False, "error": f"{type(exc).__name__}: {exc}"}

    total = time.perf_counter() - t0
    return {"ok": True, "ttft_s": round(ttft, 4) if ttft else None,
            "total_s": round(total, 4), "chunks": chunks,
            "chars": len(text), "preview": text[:120]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default="http://127.0.0.1:4011/v1")
    ap.add_argument("--model", default="i-arif")
    ap.add_argument("--prompt", default="reply PONG")
    ap.add_argument("--api-key", default=None)
    ap.add_argument("--timeout", type=int, default=120)
    ap.add_argument("--runs", type=int, default=1)
    args = ap.parse_args()

    for i in range(args.runs):
        res = probe(args.base_url, args.model, args.prompt,
                    args.api_key, args.timeout)
        if res.get("ok"):
            print(f"run {i+1}: TTFT={res['ttft_s']}s total={res['total_s']}s "
                  f"chunks={res['chunks']} chars={res['chars']}")
            print(f"         preview={res['preview']!r}")
        else:
            print(f"run {i+1}: FAILED {res}")


if __name__ == "__main__":
    main()
