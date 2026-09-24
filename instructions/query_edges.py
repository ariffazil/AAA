#!/usr/bin/env python3
"""
Edge Registry Query Tool
Per reality-graph-doctrine-20260912 + 5-layer doctrine §3 + small-world-helix-linkage-20260924
Read /var/lib/arifos/edge_assertions.jsonl (append-only Reality Graph receipts).

Usage:
  query_edges.py --layer relationship
  query_edges.py --subject human:arif
  query_edges.py --predicate employed_by
  query_edges.py --sensitivity F5_PROTECTED
  query_edges.py --confidence CONFIRMED
  query_edges.py --count-by-layer
  query_edges.py --trace PARENT <edge_id>  # walk parent_assertion_ids chain
"""
import json
import sys
import argparse
from pathlib import Path

EDGE_FILE = Path("/var/lib/arifos/edge_assertions.jsonl")


def load_edges(path=EDGE_FILE):
    if not path.exists():
        print(f"ERROR: edge file not found at {path}", file=sys.stderr)
        sys.exit(1)
    edges = []
    with path.open() as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                edges.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"WARN: line {line_num} parse error: {e}", file=sys.stderr)
    return edges


def filter_edges(edges, args):
    result = edges
    if args.layer:
        result = [e for e in result if e.get("layer") == args.layer]
    if args.subject:
        result = [e for e in result if e.get("subject", {}).get("canonical_id") == args.subject]
    if args.predicate:
        result = [e for e in result if e.get("predicate") == args.predicate]
    if args.sensitivity:
        result = [e for e in result if e.get("governance", {}).get("sensitivity") == args.sensitivity]
    if args.confidence:
        result = [e for e in result if e.get("confidence", {}).get("band") == args.confidence]
    return result


def print_edge(edge, verbose=False):
    sub = edge.get("subject", {}).get("canonical_id", "?")
    obj = edge.get("object", {}).get("canonical_id", "?")
    pred = edge.get("predicate", "?")
    layer = edge.get("layer", "?")
    conf = edge.get("confidence", {}).get("value", "?")
    band = edge.get("confidence", {}).get("band", "?")
    sens = edge.get("governance", {}).get("sensitivity", "?")
    eid = edge.get("edge_id", "?")
    print(f"  [{layer:12s}] {eid}")
    print(f"    {sub:35s} --{pred:18s}--> {obj}")
    print(f"    confidence: {conf} ({band}) | sensitivity: {sens}")
    if verbose:
        ts = edge.get("ts", "?")
        note = edge.get("note", "")
        parents = edge.get("parent_assertion_ids", [])
        print(f"    ts: {ts}")
        print(f"    parents: {parents}")
        if note:
            print(f"    note: {note}")


def count_by_layer(edges):
    from collections import Counter
    layers = Counter(e.get("layer") for e in edges)
    print("Edge counts by layer:")
    for layer, count in sorted(layers.items()):
        print(f"  {layer:15s}  {count}")


def trace_parents(edges, edge_id):
    """Walk parent_assertion_ids chain (simplified — just look in our edge set)."""
    matches = [e for e in edges if e.get("edge_id") == edge_id]
    if not matches:
        print(f"  Edge {edge_id} not found in current set")
        return
    edge = matches[0]
    print(f"Edge: {edge_id}")
    parents = edge.get("parent_assertion_ids", [])
    if not parents:
        print("  No parents in current edge set (parent may be in other substrate)")
        return
    for p in parents:
        print(f"  Parent: {p}")
        p_matches = [e for e in edges if e.get("edge_id") == p]
        if p_matches:
            print_edge(p_matches[0], verbose=True)
        else:
            print(f"    (parent {p} not in current edge set — cross-substrate lookup needed)")


def main():
    parser = argparse.ArgumentParser(description="Edge Registry Query Tool")
    parser.add_argument("--layer", help="Filter by layer (relationship, authority, consequence, reality)")
    parser.add_argument("--subject", help="Filter by subject canonical_id")
    parser.add_argument("--predicate", help="Filter by predicate type")
    parser.add_argument("--sensitivity", help="Filter by governance sensitivity")
    parser.add_argument("--confidence", help="Filter by confidence band (CONFIRMED, PLAUSIBLE, UNVERIFIED, WITHDRAWN)")
    parser.add_argument("--count-by-layer", action="store_true", help="Count edges by layer")
    parser.add_argument("--trace", metavar="EDGE_ID", help="Trace parent_assertion_ids chain for an edge")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--file", default=str(EDGE_FILE), help="Edge file path")
    args = parser.parse_args()

    edges = load_edges(Path(args.file))

    if args.count_by_layer:
        count_by_layer(edges)
        return

    if args.trace:
        trace_parents(edges, args.trace)
        return

    filtered = filter_edges(edges, args)
    print(f"\n=== {len(filtered)} edges (from {len(edges)} total) ===\n")
    for edge in filtered:
        print_edge(edge, verbose=args.verbose)
        print()


if __name__ == "__main__":
    main()
