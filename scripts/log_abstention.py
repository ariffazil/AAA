#!/usr/bin/env python3
"""Abstention logger — P4, F13-greenlit 2026-08-25.

Logs abstention events (claim drafted → withheld) as structured JSONL.
This is the i-ARIF failure-grammar corpus. Schema:
  {ts, context, draft_claim, source_class, withheld_because}
Usage:
  log_abstention.py --context "..." --draft-claim "..." \
      --source-class INFERENCE --because "no source this session"
Atomic append (O_APPEND), never overwrites, never deletes.
"""
import argparse, json, os, datetime

CORPUS = "/root/AAA/abstention_corpus.jsonl"

p = argparse.ArgumentParser()
p.add_argument("--context", required=True)
p.add_argument("--draft-claim", required=True)
p.add_argument("--source-class", required=True,
               choices=["RECEIVED", "MEMORY", "INFERENCE"])
p.add_argument("--because", required=True)
p.add_argument("--actor", default="hermes")
a = p.parse_args()

rec = {
    "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "actor": a.actor,
    "context": a.context,
    "draft_claim": a.draft_claim,
    "source_class": a.source_class,
    "withheld_because": a.because,
}
os.makedirs(os.path.dirname(CORPUS), exist_ok=True)
with open(CORPUS, "a") as f:  # append-only
    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
print(json.dumps({"logged": True, "corpus": CORPUS}))
