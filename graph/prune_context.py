#!/usr/bin/env python3
"""
prune_context.py — Reference implementation of FI-011 context prune.

Given a task description + candidate files, ask the code graph which files
actually matter, and return a pruned set with token-aware sizing.

This is a REFERENCE IMPL — not yet wired into delegation_envelope. Used by:
- /root/AAA/graph/FI-011-DESIGN.md
- I-ARIF (future) before answering codebase questions
- Forge_spawn (future) when bootstrapping sub-agent context

DITEMPA BUKAN DIBERI ⚒️ — graph says, we obey.
"""
from __future__ import annotations
import hashlib
import os
import re
import sys
import urllib.request
import urllib.error
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

BRIDGE_URL = os.environ.get("GRAPH_BRIDGE_URL", "http://127.0.0.1:18922")
DEFAULT_MAX_TOKENS = int(os.environ.get("PRUNE_MAX_TOKENS", "8000"))
AVG_FILE_TOKENS = int(os.environ.get("PRUNE_AVG_FILE_TOKENS", "350"))


# ─── tokenization ─ ────────────────────────────────────

# Match Python/JS/TS identifiers: snake_case + CamelCase + dotted paths
_ID_RE = re.compile(r"\b[a-zA-Z_][a-zA-Z0-9_]{2,}\b|\b[A-Z][a-zA-Z0-9]+(?:[A-Z][a-zA-Z0-9]+)+\b")

# Stop words that are too generic to search for
_STOPWORDS = {
    "the", "and", "for", "with", "this", "that", "from", "into", "have",
    "has", "you", "are", "your", "all", "any", "but", "not", "can",
    "use", "how", "what", "when", "where", "why", "which", "their",
    "code", "file", "files", "function", "functions", "module", "modules",
}


def tokenize_task(task: str) -> list[str]:
    """Extract candidate identifiers from a task description."""
    raw = _ID_RE.findall(task)
    seen = set()
    out = []
    for tok in raw:
        if tok.lower() in _STOPWORDS:
            continue
        if len(tok) < 3:
            continue
        if tok not in seen:
            seen.add(tok)
            out.append(tok)
    return out


# ─── bridge client ─────────────────────────────────────────────────────────────────


def _call_bridge(verb: str, params: dict, timeout: int = 5) -> dict:
    """Call graph_bridge :18922 verb. Returns result dict, or {} on error."""
    try:
        req = urllib.request.Request(
            f"{BRIDGE_URL}/{verb}",
            data=json.dumps({"verb": verb, "params": params}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except (urllib.error.URLError, ConnectionError, TimeoutError, OSError):
        return {}


# ─── pruning ───────────────────────────────────────────────────────────


def prune_for_task(
    task: str,
    candidate_files: list[str],
    *,
    bridge_url: str = BRIDGE_URL,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    depth: int = 1,
) -> dict:
    """Prune candidate_files to what graph says matters for this task.

    Inputs:
      task: free-text task description
      candidate_files: list of "repo/path" strings (relative to repo)
      bridge_url: graph_bridge HTTP base (default 127.0.0.1:18922)
      max_tokens: target context token budget
      depth: blast_radius depth (1 = direct only, 2 = 1 hop transitively)

    Returns dict with kept_files, dropped_files, receipt.
    On bridge unreachable: returns {graceful: True, kept: candidate_files, dropped: []}
    """
    global BRIDGE_URL
    BRIDGE_URL = bridge_url  # honour caller override

    receipt = {
        "receipt_id": f"pr-{uuid.uuid4().hex[:12]}",
        "task_hash": hashlib.sha256(task.encode()).hexdigest()[:16],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "input_files": list(candidate_files),
        "graph_queries": [],
    }

    if not candidate_files:
        receipt["kept"] = []
        receipt["dropped"] = []
        receipt["estimated_tokens_saved"] = 0
        receipt["graceful"] = True
        return receipt

    tokens = tokenize_task(task)
    receipt["extracted_tokens"] = tokens[:30]  # diagnostic cap

    # Step 1: lookup each token in graph
    relevant_files: set[str] = set()
    bridge_ok = False

    for tok in tokens[:15]:  # cap to avoid token-cost explosion
        s = _call_bridge("search", {"name": tok, "limit": 8})
        if not s.get("ok"):
            continue
        bridge_ok = True
        results = (s.get("result") or [])
        # Take top-3 by frequency of match
        for r in results[:3]:
            file_path = r.get("rel_path")
            repo = r.get("repo_name")
            if file_path and repo:
                relevant_files.add(f"{repo}/{file_path}")
                receipt["graph_queries"].append({
                    "verb": "search", "name": tok,
                    "match": f"{repo}/{file_path}::{r.get('qualified_name')}",
                })
                # Pull blast radius on this qualified name (depth=1)
                sym = r.get("qualified_name")
                if sym:
                    br = _call_bridge("blast", {"symbol": sym, "depth": depth})
                    if br.get("ok"):
                        for entry in (br.get("result") or {}).get("affected_files", []):
                            # affected_files is list[str]; match candidate
                            # by suffix equality
                            if isinstance(entry, str):
                                for cand in candidate_files:
                                    if entry == cand.split("/", 1)[-1] or cand.endswith("/" + entry):
                                        relevant_files.add(cand)
                        receipt["graph_queries"].append({
                            "verb": "blast", "symbol": sym,
                            "depth": depth,
                            "affected_count": len((br.get("result") or {}).get("affected_files", [])),
                        })

    if not bridge_ok:
        # Bridge unreachable — graceful fallback: keep all
        receipt["graceful"] = True
        receipt["bridge_ok"] = False
        receipt["kept"] = list(candidate_files)
        receipt["dropped"] = []
        receipt["estimated_tokens_saved"] = 0
        receipt["warning"] = "graph_bridge unreachable; full context passed"
        return receipt

    # Step 2: directly-mentioned files (filename/path match in task text)
    for cand in candidate_files:
        path_part = cand.split("/", 1)[-1] if "/" in cand else cand
        if any(tok in path_part for tok in tokens if len(tok) >= 5):
            relevant_files.add(cand)

    # Step 3: apply token budget
    candidate_set = set(candidate_files)
    relevant_in_candidates = candidate_set & relevant_files
    unreferenced_in_candidates = candidate_set - relevant_in_candidates

    # If relevant alone exceeds budget, keep all (don't shrink what graph said matters)
    if len(relevant_in_candidates) * AVG_FILE_TOKENS > max_tokens:
        kept = sorted(relevant_in_candidates)
        dropped = sorted(unreferenced_in_candidates)
    else:
        kept = sorted(relevant_in_candidates)
        dropped = sorted(unreferenced_in_candidates)

    # Safety: if we dropped >90% of files, keep at least the first 3 (some
    # agent needs at least context to start)
    if len(candidate_files) > 5 and len(kept) < max(3, int(len(candidate_files) * 0.1)):
        kept = sorted((relevant_in_candidates | set(candidate_files[:3])))
        dropped = sorted(candidate_set - set(kept))
        receipt["safety_override"] = True

    receipt["kept"] = kept
    receipt["dropped"] = dropped
    receipt["estimated_tokens_saved"] = len(dropped) * AVG_FILE_TOKENS
    receipt["graceful"] = True
    receipt["bridge_ok"] = True
    return receipt


# ─── CLI ──────────────────────────────────────────────────────────────


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("usage: prune_context.py '<task>' <file1> [<file2> ...]\n"
              "  example: prune_context.py 'audit arif_judge' arifOS/arifosd.py "
              "arifOS/judge.py arifOS/server.py")
        sys.exit(0)

    task = sys.argv[1]
    files = sys.argv[2:]
    r = prune_for_task(task, files)
    print(json.dumps(r, indent=2))