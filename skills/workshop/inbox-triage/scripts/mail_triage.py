#!/usr/bin/env python3
"""Batch header pulls through the governed mailread broker path.

Usage:
  mail_triage.py triage 60 [out.jsonl]                 # latest N message headers
  mail_triage.py search "in:inbox is:unread newer_than:7d" 25 [out.jsonl]

Prints compact one-line summaries to stdout and writes JSONL rows
{id, from, subj, date, ts, labels, snippet} to out.jsonl (default /tmp/heads.jsonl)
for aggregation in code. Sort by ts, filter bot mail, read bodies only for candidates.
"""

import json
import os
import subprocess
import sys

USAGE = __doc__


def mr(args):
    """Run mailread, returning parsed JSON.

    The `Using keyring backend: keyring` banner is on the wrapper's stderr. Never line-strip
    stdout to remove it: with stderr suppressed, line 1 *is* the opening brace and stripping it
    breaks the parse with `Extra data: line 1 column 14`.
    """
    env = dict(
        os.environ,
        MAILREAD_ACTOR=os.environ.get("MAILREAD_ACTOR", "hermes"),
        MAILREAD_PURPOSE=os.environ.get(
            "MAILREAD_PURPOSE", "inbox triage: sovereign asked whether anything needs attention"
        ),
    )
    p = subprocess.run(["mailread"] + args, capture_output=True, text=True, env=env, timeout=120)
    out = p.stdout.strip()
    i = out.find("{")
    if i < 0:
        sys.exit(f"mailread {' '.join(args)} produced no JSON: {(p.stderr or out)[:300]}")
    try:
        return json.loads(out[i:])
    except json.JSONDecodeError as e:
        sys.exit(f"mailread {' '.join(args)}: parse failed ({e}); raw head: {out[i:i + 200]}")


def headers(d):
    return {x["name"].lower(): x["value"] for x in d.get("payload", {}).get("headers", [])}


def collect(ids, out_path):
    rows = []
    for mid in ids:
        d = mr(["meta", mid])
        h = headers(d)
        rows.append(
            {
                "id": mid,
                "from": (h.get("from") or "")[:120],
                "subj": (h.get("subject") or "")[:160],
                "date": (h.get("date") or "")[:40],
                "ts": int(d.get("internalDate", 0)) // 1000,
                "labels": d.get("labelIds", []),
                "snippet": (d.get("snippet") or "")[:200],
            }
        )
        r = rows[-1]
        unread = "U" if "UNREAD" in r["labels"] else " "
        print(f"{unread} {r['ts']} | {r['from'][:45]} | {r['subj'][:90]}", flush=True)
    with open(out_path, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    print(f"-- {len(rows)} rows -> {out_path}", flush=True)


def main():
    if len(sys.argv) < 2:
        sys.exit(USAGE)
    mode = sys.argv[1]
    if mode == "triage":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 20
        out = sys.argv[3] if len(sys.argv) > 3 else "/tmp/heads.jsonl"
        listing = mr(["list", str(n)])
    elif mode == "search":
        if len(sys.argv) < 3:
            sys.exit(USAGE)
        query = sys.argv[2]
        n = int(sys.argv[3]) if len(sys.argv) > 3 else 20
        out = sys.argv[4] if len(sys.argv) > 4 else "/tmp/heads.jsonl"
        listing = mr(["search", query, str(n)])
    else:
        sys.exit(USAGE)
    collect([m["id"] for m in listing.get("messages", [])], out)


main()
