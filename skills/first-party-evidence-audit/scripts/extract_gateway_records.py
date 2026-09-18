#!/usr/bin/env python3
"""Extract first-party records from the Hermes gateway/agent log corpus.

Read-only. Walks every rotated copy, emits one JSONL record per inbound message and per
conversation-turn line, sorted by timestamp, and prints a per-chat census.

Usage:
    python3 extract_gateway_records.py [--logs DIR] [--out FILE]

Why a file rather than an inline heredoc: inline heredocs and pipe-into-interpreter shapes are
refused by the pre-tool gate, and a file-based script can be re-run against a different window
without re-typing. See the `telegram-conversation-history-extraction` skill for source semantics.

Caveats to carry into any deliverable:
  * message bodies are truncated in the log (~200 chars) - a long body is a PREFIX, never quote as whole
  * `user=unknown` rows may still be attributable via an inline `[Display|<uid>]` tag in the body
  * the same message can appear in several files and under two chat ids - dedupe on (ts, chat, text)
  * rotation depth bounds the window; anything older is absent, which is not the same as silence
"""
import argparse
import json
import os
import re
from collections import Counter

DEFAULT_LOGS = "/root/.hermes/logs"
FILES = ["gateway.log.3", "gateway.log.2", "gateway.log.1", "gateway.log",
         "agent.log.3", "agent.log.2", "agent.log.1", "agent.log"]

RE_IN = re.compile(
    r"^(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\d+ \w+ gateway\.run: inbound message: "
    r"platform=(?P<plat>\S+) user=(?P<user>.*?) chat=(?P<chat>-?\d+) "
    r"msg=(?P<msg>.*?) reply_to_id=(?P<rid>\S*) reply_to_text='(?P<rtext>.*)'$")

RE_TURN = re.compile(
    r"^(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\d+ \w+ \[(?P<sid>[0-9a-z_]+)\] "
    r"agent\.turn_context: conversation turn: session=\S+ model=\S+ provider=\S+ "
    r"platform=(?P<plat>\S+) history=(?P<h>\d+) msg='(?P<msg>.*)'$")

TAG = re.compile(r"^\[(?P<name>[^|\]]*)\|(?P<uid>\d+)\]\s*(?P<body>.*)$", re.S)


def strip_quotes(s):
    s = s.strip()
    if len(s) >= 2 and s[0] == "'" and s[-1] == "'":
        return s[1:-1]
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--logs", default=DEFAULT_LOGS)
    ap.add_argument("--out", default="./records/dump.jsonl")
    args = ap.parse_args()

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    recs = []
    for fn in FILES:
        path = os.path.join(args.logs, fn)
        if not os.path.exists(path):
            continue
        with open(path, "r", errors="replace") as fh:
            for line in fh:
                line = line.rstrip("\n")
                m = RE_IN.match(line)
                if m:
                    d = m.groupdict()
                    body = strip_quotes(d["msg"])
                    tag = TAG.match(body)
                    recs.append({
                        "ts": d["ts"], "kind": "inbound", "chat": d["chat"],
                        "user": d["user"], "msg": body,
                        "uid": tag.group("uid") if tag else None,
                        "display": tag.group("name") if tag else None,
                        "body": tag.group("body").strip() if tag else body,
                        "reply_to_id": d["rid"], "reply_to_text": d["rtext"],
                        "src": fn})
                    continue
                m = RE_TURN.match(line)
                if m:
                    d = m.groupdict()
                    recs.append({"ts": d["ts"], "kind": "turn", "chat": None,
                                 "user": None, "sid": d["sid"], "plat": d["plat"],
                                 "history": int(d["h"]), "msg": strip_quotes(d["msg"]),
                                 "src": fn})

    recs.sort(key=lambda r: r["ts"])
    with open(args.out, "w") as fh:
        for r in recs:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    inbound = [r for r in recs if r["kind"] == "inbound"]
    print("records:", len(recs), "inbound:", len(inbound), "->", args.out)
    if recs:
        print("window:", recs[0]["ts"], "->", recs[-1]["ts"])
    print("by chat:", Counter(r["chat"] for r in inbound).most_common(15))
    print("attributed by uid:",
          Counter(r["uid"] for r in inbound if r["uid"]).most_common(12))
    print("unattributed:", sum(1 for r in inbound if not r["uid"]))
    print("\nNOTE: bodies are truncated in the log; report the unattributed count and the "
          "window start in any deliverable before drawing per-person conclusions.")


if __name__ == "__main__":
    main()
