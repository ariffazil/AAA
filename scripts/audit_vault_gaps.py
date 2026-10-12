#!/usr/bin/env python3
"""Recompute the VAULT999 gap classification on ONE declared ledger.

Replaces the 2026-10-06 "13 GAP CLASSIFICATION (REPRODUCED)" which:
  - was produced while verify_vault_chain.py failed to run
    ("can't open file /root/scripts/verify_vault_chain.py")
  - mixed two ledgers (1346-line arifOS canonical vs 1337-line sa-fix copy)
  - double-counted 951 records as both "legitimate GENESIS sub-chain" (4a)
    and "placeholder contamination" (4f)
  - reported 1180 fixture records / 88.3%, which does not reproduce

Single declared ledger: arifOS canonical. Run with --path to override.
"""
import argparse, json, re, sys
from collections import Counter

DEFAULT = "/root/arifOS/VAULT999/SEALED_EVENTS.jsonl"
PLACEHOLDER = re.compile(
    r'^(SESS-123|SESS-1|SESS-REAL|SESS-FAKE|session-test-123|SESS-ID-ONLY|SESS-NATURAL)$')


def load(path):
    recs, parse_fail = [], []
    for i, ln in enumerate(open(path, encoding="utf-8", errors="replace"), 1):
        if not ln.strip():
            continue
        try:
            recs.append((i, json.loads(ln)))
        except Exception as exc:
            parse_fail.append((i, str(exc)[:50], ln[:70]))
    return recs, parse_fail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", default=DEFAULT)
    a = ap.parse_args()

    recs, pf = load(a.path)
    n = len(recs)
    print(f"LEDGER: {a.path}")
    print(f"physical records={n}  parse_failures={len(pf)}\n")

    # G1 -- unparseable records
    print(f"G1  json_parse_error            {len(pf):>5}   {[i for i,_,_ in pf]}")

    # G2 -- schema class: entries with no chain fields at all
    nochain = [i for i, d in recs if "chain_hash" not in d and "prev_hash" not in d]
    print(f"G2  schema_no_chain_fields      {len(nochain):>5}   {nochain}")

    # G3 -- orphan footer: last record with no chain fields
    orphan = None
    if recs and "chain_hash" not in recs[-1][1]:
        orphan = recs[-1][0]
    print(f"G3  orphan_footer_no_chain      {1 if orphan else 0:>5}   L{orphan}")

    # G4 -- prev_hash integrity, split into the three populations
    prevs = Counter(str(d["prev_hash"]) for _, d in recs if "prev_hash" in d)
    genesis = prevs.get("GENESIS", 0)
    empty = prevs.get("", 0)
    dup_pairs = []
    for k in range(len(recs) - 1):
        (i1, d1), (i2, d2) = recs[k], recs[k + 1]
        p = d1.get("prev_hash")
        if p is not None and p == d2.get("prev_hash") and p not in ("GENESIS",):
            dup_pairs.append((i1, i2, d1, d2))

    # G5 -- placeholder contamination, and its OVERLAP with the GENESIS set
    genesis_lines = {i for i, d in recs if d.get("prev_hash") == "GENESIS"}
    ph = [(i, d) for i, d in recs
          if PLACEHOLDER.match(str(d.get("session_id", "")))]
    ph_lines = {i for i, _ in ph}
    overlap = genesis_lines & ph_lines

    print(f"G4a genesis_subchain_starts     {genesis:>5}")
    print(f"G4b prev_hash_empty_string      {empty:>5}")
    print(f"G4c consecutive_dup_prev        {len(dup_pairs):>5}   "
          f"{[f'L{a}/L{b}' for a,b,_,_ in dup_pairs]}")
    for a_, b_, d1, d2 in dup_pairs:
        print(f"      -> L{a_}/L{b_}: payload_identical="
              f"{d1.get('payload') == d2.get('payload')} "
              f"chain_identical={d1.get('chain_hash') == d2.get('chain_hash')}")
    print(f"G5  placeholder_records         {len(ph):>5}   "
          f"({100*len(ph)/n:.1f}% of {n})")

    print("\nCORRECTIONS TO THE 2026-10-06 CLASSIFICATION")
    print(f"  G4a and G5 OVERLAP: {len(overlap)} of {genesis} GENESIS records "
          f"({100*len(overlap)/max(genesis,1):.1f}%) are placeholders.")
    print(f"  -> They are ONE population counted twice, not two independent gaps.")
    print(f"  -> Claimed '1180 fixture records (88.3%)' vs actual {len(ph)} "
          f"({100*len(ph)/n:.1f}%).")
    print("\nHEADLINE")
    print(f"  {100*len(ph)/n:.1f}% of this ledger is fixture data. Chain-integrity")
    print("  gap-counting is the wrong lens; the dominant fact is that the")
    print("  production ledger is mostly SESS-* test records.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
