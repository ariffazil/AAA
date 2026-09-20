#!/usr/bin/env python3
"""mailbox-triage: pull inbox headers through the governed `mailread` path.

Usage:  python3 mail_triage.py [N] [search-query]

Emits one JSON row per message to stdout and writes the same rows to OUT_JSONL.
Headers only - never bodies. Tolerant of two `mailread` quirks that break naive
wrappers:
  * stdout is prefixed with a banner line, so we parse from the first '{'
  * a terse MAILREAD_PURPOSE is refused (8-char floor), so the default is a
    full sentence
"""
import json
import os
import subprocess
import sys

OUT_JSONL = os.environ.get("MAIL_TRIAGE_OUT", "/tmp/heads.jsonl")

ENV = dict(os.environ)
ENV.setdefault("MAILREAD_ACTOR", "hermes")
# 8-char minimum on the broker side - keep it a real sentence.
ENV.setdefault(
    "MAILREAD_PURPOSE",
    "sovereign asked: read inbox and flag anything urgent",
)


def mr(args, timeout=90):
    """Run mailread and parse the JSON payload out of its bannered stdout."""
    proc = subprocess.run(
        ["mailread", *args], capture_output=True, text=True, env=ENV, timeout=timeout
    )
    out = proc.stdout.strip()
    start = out.find("{")
    if start < 0:
        return {"_error": (proc.stderr or out or "empty output")[:300]}
    try:
        return json.loads(out[start:])
    except Exception as exc:  # banner, truncation, or a broker envelope
        return {"_error": f"parse: {exc}", "_raw": out[start : start + 300]}


def headers(msg_id):
    detail = mr(["meta", msg_id])
    head = {
        h.get("name", "").lower(): h.get("value", "")
        for h in detail.get("payload", {}).get("headers", [])
    }
    return {
        "id": msg_id,
        "from": (head.get("from") or "")[:120],
        "subj": (head.get("subject") or "")[:160],
        "date": (head.get("date") or "")[:40],
        "ts": int(detail.get("internalDate", 0)) // 1000,
        "labels": detail.get("labelIds", []),
        "snippet": (detail.get("snippet") or "")[:200],
    }


def main():
    count = 25
    query = None
    for arg in sys.argv[1:]:
        if arg.isdigit():
            count = int(arg)
        else:
            query = arg

    # NOTE: count is POSITIONAL - `mailread list --limit N` is rejected.
    listing = mr(["search", query, str(count)]) if query else mr(["list", str(count)])
    ids = [m["id"] for m in listing.get("messages", [])]
    if not ids:
        print(json.dumps(listing, indent=1)[:500], file=sys.stderr)
        print("no messages returned", file=sys.stderr)

    rows = []
    for msg_id in ids:
        row = headers(msg_id)
        rows.append(row)
        print(json.dumps(row), flush=True)  # print as we go - survive a timeout

    rows.sort(key=lambda r: r.get("ts", 0), reverse=True)
    with open(OUT_JSONL, "w") as fh:
        for row in rows:
            fh.write(json.dumps(row) + "\n")

    unread = sum(1 for r in rows if "UNREAD" in r.get("labels", []))
    print(f"\n{len(rows)} rows -> {OUT_JSONL}  ({unread} unread)", file=sys.stderr)


if __name__ == "__main__":
    main()
