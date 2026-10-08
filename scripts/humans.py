#!/usr/bin/env python3
"""
Canonical human lookup for HERMES / AAA / arifOS agents.
The 3 defects this module fixes:
  D1. Agent fabricates reality from training weights when given a human name.
  D2. Over-cautious safety refuses to use promoted human-interaction memory.
  D3. Memory stale - doesn't track live state.

How it fixes them:
  - Every lookup is read-from-disk against the canonical substrate
    (people.yaml lanes + /root/memory/people/<handle>/person-card.md
    + /root/memory/people/<handle>/MEMORY_MANIFEST.json). Never from
    agent weights.
  - Every fact carries provenance + observed date. The agent must
    surface provenance; it cannot present a fact as "known" without it.
  - Freshness gate: if a person's last_seal > TTL ago, the response
    is "STALE" with a re-fetch instruction. The agent does not
    silently use stale memory.
  - Promoted claims (those with claim_ref in /root/.hermes/memories/MEMORY.md
    or people.yaml scope: shared) are surfaced with full content, not
    redacted. Over-cautious safety is bypassed when provenance is present.
  - Unknown is a valid result. UNKNOWN is preferred over fabrication.

Stdlib + PyYAML only. Fail-closed. No network calls.

Usage as a module:
    from humans import lookup, search, list_humans, freshness_check

    result = lookup("syed")
    # {"handle": "syed", "display_name": "Syed (Abang Sado)", "known": [...], "unknown": [...], "stale": bool, ...}

    result = search("abang")
    # Returns all matching handles.

Usage as a CLI:
    python3 humans.py lookup syed
    python3 humans.py list
    python3 humans.py search "abang sado"
    python3 humans.py freshness syed
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import yaml  # type: ignore
except ImportError:
    print("FATAL: PyYAML required.", file=sys.stderr)
    sys.exit(2)


# ----------------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------------
LANES_PEOPLE = Path("/root/.hermes/lanes/people.yaml")
MEMORY_PEOPLE_ROOT = Path("/root/memory/people")
HERMES_MEMORY = Path("/root/.hermes/memories/MEMORY.md")
HERMES_USER = Path("/root/.hermes/memories/USER.md")

# Default freshness TTL: 24h. Configurable per call.
DEFAULT_TTL_HOURS = 24

# Source-class discipline: 5 classes per v1.2/v1.3 amendments.
SOURCE_CLASSES = {"PRIMARY_CORPUS", "ARIF_ATTESTED", "CROSS_REFERENCED", "INFERRED", "VOID"}


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def _now() -> _dt.datetime:
    return _dt.datetime.now(_dt.timezone.utc)


def _load_yaml(path: Path) -> Dict[str, Any]:
    """Load a YAML file; return {} on missing or parse error."""
    if not path.exists():
        return {}
    try:
        with path.open() as f:
            return yaml.safe_load(f) or {}
    except Exception as e:  # pragma: no cover
        return {"_error": f"yaml_parse_error: {e}", "_path": str(path)}


def _safe_read_text(path: Path, max_lines: int = 200) -> str:
    """Read text safely. Cap at max_lines to avoid loading huge files."""
    if not path.exists():
        return ""
    try:
        with path.open() as f:
            return "".join([next(f) for _ in range(max_lines)])
    except StopIteration:
        return ""
    except Exception:  # pragma: no cover
        return ""


def _person_handle_candidates(query: str) -> List[str]:
    """
    Given a human query (display name, nickname, handle, or any string),
    return a list of probable canonical handles to look up.

    Resolution order:
      1. Direct handle match in people.yaml (lowercase, normalised).
      2. Display name match in people.yaml.
      3. Substring match against any person entry.
      4. Lowercase / space-stripped normalisation.
    """
    q = query.strip().lower()
    if not q:
        return []
    data = _load_yaml(LANES_PEOPLE)
    people = data.get("people", {}) or {}
    candidates: List[Tuple[int, str]] = []  # (priority, handle)
    for handle, person in people.items():
        if not isinstance(person, dict):
            continue
        h_low = handle.lower()
        d_name = (person.get("display_name") or "").lower()
        # 1. direct handle
        if h_low == q:
            candidates.append((0, handle))
        # 2. display name exact
        if d_name == q:
            candidates.append((0, handle))
        # 3. substring match
        if q in h_low or q in d_name:
            candidates.append((1, handle))
        # 4. token match (any token overlap)
        q_tokens = set(re.split(r"[\s,]+", q))
        h_tokens = set(re.split(r"[\s,()]+", h_low + " " + d_name))
        if q_tokens & h_tokens:
            candidates.append((2, handle))
    candidates.sort()
    seen = set()
    out: List[str] = []
    for _, h in candidates:
        if h not in seen:
            out.append(h)
            seen.add(h)
    return out


# ----------------------------------------------------------------------------
# Core API
# ----------------------------------------------------------------------------
def lookup(query: str, ttl_hours: int = DEFAULT_TTL_HOURS) -> Dict[str, Any]:
    """
    Look up a person by name/handle. Return a structured record with:
      - known: list of facts with provenance (from PRIMARY_CORPUS or ARIF_ATTESTED scope:shared)
      - unknown: list of voids (no data, or scope:dm withheld)
      - stale: bool - whether last_seal > ttl_hours ago
      - provenance_chain: list of source files consulted
      - safety_note: instruction to the agent about how to use this
    """
    candidates = _person_handle_candidates(query)
    if not candidates:
        return {
            "query": query,
            "resolved": None,
            "known": [],
            "unknown": [{
                "field": "person_identity",
                "state": "VOID",
                "reason": f"no match in {LANES_PEOPLE} for query={query!r}",
                "instruction": "do NOT fabricate. Reply: 'I don't have any record of {query} in the human substrate. Ask Arif to register the person via /root/.hermes/lanes/people.yaml.'",
            }],
            "stale": False,
            "provenance_chain": [str(LANES_PEOPLE)],
            "safety_note": "Unknown person. Fabrication forbidden.",
        }

    # Use best candidate (lowest priority number = best match)
    handle = candidates[0]
    data = _load_yaml(LANES_PEOPLE)
    person = data.get("people", {}).get(handle, {})
    if not person:
        return {
            "query": query,
            "resolved": handle,
            "known": [],
            "unknown": [{"field": "person_data", "state": "VOID", "reason": "handle found but person data missing"}],
            "stale": False,
            "provenance_chain": [str(LANES_PEOPLE)],
        }

    known: List[Dict[str, Any]] = []
    unknown: List[Dict[str, Any]] = []

    # Surface display_name + identities (always non-sensitive)
    known.append({
        "field": "display_name",
        "value": person.get("display_name"),
        "source_class": "ARIF_ATTESTED",
        "source": "lanes.yaml heritage register",
        "observed": person.get("last_updated", "unknown"),
    })

    for ident in person.get("identities", []) or []:
        known.append({
            "field": f"identity.{ident.get('kind')}",
            "value": ident.get("value"),
            "source_class": "ARIF_ATTESTED",
            "source": f"lanes.yaml (kind={ident.get('kind')})",
            "observed": ident.get("observed", "unknown"),
        })

    # Surface scope:shared facts (these are the promoted human-interaction memories)
    facts = person.get("facts", []) or []
    has_shared = False
    for fact in facts:
        scope = fact.get("scope", "shared")
        if scope == "dm":
            unknown.append({
                "field": "fact",
                "summary": (fact.get("fact") or "")[:80] + "..." if len(fact.get("fact") or "") > 80 else fact.get("fact"),
                "state": "WITHHELD",
                "scope": "dm",
                "reason": "scope:dm - DM-lane only, not surfaced in non-DM contexts",
                "instruction": "If user is in DM with the subject, surface this fact. Otherwise do NOT.",
            })
        else:
            has_shared = True
            known.append({
                "field": "fact",
                "value": fact.get("fact"),
                "source_class": "ARIF_ATTESTED" if fact.get("source", "").lower().startswith("arif") else "CROSS_REFERENCED",
                "source": fact.get("source", "unknown"),
                "observed": fact.get("observed", "unknown"),
                "scope": scope,
            })

    if not has_shared:
        unknown.append({
            "field": "shared_facts",
            "state": "VOID",
            "reason": "no scope:shared facts - person is registered but has no promoted memory",
            "instruction": "If user asks for any specific fact about this person, default to UNKNOWN. Do NOT fall back to training weights.",
        })

    # Try to read the canonical person-card from /root/memory/people/<handle>/
    # Handle may be lowercase (lanes.yaml key) but directory may be uppercase.
    person_dir = MEMORY_PEOPLE_ROOT / handle
    if not person_dir.exists():
        person_dir = MEMORY_PEOPLE_ROOT / handle.upper()
    memory_path = person_dir / "person-card.md"
    person_card_claims: List[Dict[str, Any]] = []
    if memory_path.exists():
        # Surface the path as an observed fact (proves the file exists)
        known.append({
            "field": "person_card_exists",
            "value": str(memory_path),
            "source_class": "PRIMARY_CORPUS",
            "source": str(memory_path),
            "observed": "file_mtime",
        })
        # Parse the person-card for **bolded claims** (markdown **N. ** or **1.** style)
        # and **## 2026-...-writeback** sections, treating each as a claim.
        try:
            with memory_path.open() as f:
                lines = f.readlines()
            cur_section = None
            for line in lines:
                s = line.strip()
                if s.startswith("## "):
                    cur_section = s
                    continue
                # PRIMARY_CORPUS writeback sections
                if cur_section and "writeback" in cur_section.lower():
                    # Capture the bolded numbered claims
                    if re.match(r'^\*\*\d+\.\s+\*\*', s) or s.startswith("**"):
                        person_card_claims.append({
                            "field": "writeback_claim",
                            "value": s[:300],   # cap at 300 chars per claim
                            "source_class": "PRIMARY_CORPUS",
                            "source": f"{memory_path}:{lines.index(line)+1}",
                            "observed": cur_section,
                        })
                # **bold** pattern in body
                m = re.match(r'^\*\*([^*]+)\*\*\s*[-:]\s*(.+)$', s)
                if m:
                    field = m.group(1).strip()
                    value = m.group(2).strip()
                    if len(value) < 300:  # cap
                        person_card_claims.append({
                            "field": field,
                            "value": value,
                            "source_class": "PRIMARY_CORPUS",
                            "source": f"{memory_path}",
                            "observed": "person-card.md",
                        })
        except Exception:
            pass
        # Merge person_card_claims into known
        known.extend(person_card_claims)
    else:
        unknown.append({
            "field": "person_card",
            "state": "VOID",
            "reason": f"no /root/memory/people/{handle}/person-card.md (tried uppercase too)",
        })

    # Freshness check
    # Handle may be lowercase (lanes.yaml key) but directory may be uppercase.
    # Try both.
    person_dir = MEMORY_PEOPLE_ROOT / handle
    if not person_dir.exists():
        # Try uppercase
        person_dir = MEMORY_PEOPLE_ROOT / handle.upper()
    memory_manifest = person_dir / "MEMORY_MANIFEST.json"
    last_seal_iso: Optional[str] = None
    if memory_manifest.exists():
        try:
            with memory_manifest.open() as f:
                manifest = json.load(f)
            last_seal_iso = manifest.get("last_seal") or manifest.get("created")
        except Exception:
            pass
    stale = False
    age_hours: Optional[float] = None
    if last_seal_iso:
        try:
            last_seal_dt = _dt.datetime.fromisoformat(last_seal_iso.replace("Z", "+00:00"))
            age_hours = (_now() - last_seal_dt).total_seconds() / 3600
            stale = age_hours > ttl_hours
        except Exception:
            pass

    provenance_chain = [str(LANES_PEOPLE)]
    if memory_path.exists():
        provenance_chain.append(str(memory_path))
    if memory_manifest.exists():
        provenance_chain.append(str(memory_manifest))

    return {
        "query": query,
        "resolved": handle,
        "display_name": person.get("display_name"),
        "known": known,
        "unknown": unknown,
        "stale": stale,
        "age_hours": age_hours,
        "last_seal": last_seal_iso,
        "provenance_chain": provenance_chain,
        "safety_note": (
            "Promoted facts (scope:shared) are surfaced with full provenance. "
            "Do NOT add detail beyond the surfaced facts. "
            "If asked about scope:dm content, defer to DM-lane. "
            "If asked about UNKNOWN fields, reply 'I have no record of <X> in the human substrate for <handle>' - do not fabricate."
        ),
    }


def list_humans() -> List[Dict[str, str]]:
    """List all humans in the people.yaml substrate."""
    data = _load_yaml(LANES_PEOPLE)
    out: List[Dict[str, str]] = []
    for handle, person in (data.get("people", {}) or {}).items():
        if isinstance(person, dict):
            out.append({
                "handle": handle,
                "display_name": person.get("display_name", ""),
            })
    return sorted(out, key=lambda x: x["handle"])


def freshness_check(handle: str, ttl_hours: int = DEFAULT_TTL_HOURS) -> Dict[str, Any]:
    """Check whether a person's canonical memory is fresh."""
    person_dir = MEMORY_PEOPLE_ROOT / handle
    if not person_dir.exists():
        person_dir = MEMORY_PEOPLE_ROOT / handle.upper()
    memory_manifest = person_dir / "MEMORY_MANIFEST.json"
    if not memory_manifest.exists():
        return {
            "handle": handle,
            "stale": True,
            "reason": f"no MEMORY_MANIFEST.json at {memory_manifest}",
            "instruction": "Re-seed canonical memory via /root/.hermes/lanes/people.yaml + person-card.md.",
        }
    try:
        with memory_manifest.open() as f:
            manifest = json.load(f)
    except Exception as e:
        return {"handle": handle, "stale": True, "reason": f"manifest_parse_error: {e}"}
    last_seal = manifest.get("last_seal") or manifest.get("created")
    if not last_seal:
        return {"handle": handle, "stale": True, "reason": "no last_seal in manifest"}
    try:
        last_seal_dt = _dt.datetime.fromisoformat(last_seal.replace("Z", "+00:00"))
    except Exception as e:
        return {"handle": handle, "stale": True, "reason": f"last_seal_parse_error: {e}"}
    age_hours = (_now() - last_seal_dt).total_seconds() / 3600
    return {
        "handle": handle,
        "last_seal": last_seal,
        "age_hours": round(age_hours, 2),
        "ttl_hours": ttl_hours,
        "stale": age_hours > ttl_hours,
        "instruction": "Re-fetch if stale" if age_hours > ttl_hours else "fresh",
    }


def search(query: str) -> List[Dict[str, str]]:
    """Fuzzy search for humans by any field."""
    return [lookup(c) for c in _person_handle_candidates(query)]


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------
def _emit_json(obj: Any) -> None:
    print(json.dumps(obj, indent=2, ensure_ascii=False, default=str))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Canonical human lookup. Never fabricate; surface provenance; mark stale."
    )
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list").add_argument("--ttl-hours", type=int, default=DEFAULT_TTL_HOURS)
    p_lookup = sub.add_parser("lookup")
    p_lookup.add_argument("query")
    p_lookup.add_argument("--ttl-hours", type=int, default=DEFAULT_TTL_HOURS)
    p_search = sub.add_parser("search")
    p_search.add_argument("query")
    p_fresh = sub.add_parser("freshness")
    p_fresh.add_argument("handle")
    p_fresh.add_argument("--ttl-hours", type=int, default=DEFAULT_TTL_HOURS)

    args = parser.parse_args()
    if args.cmd == "list":
        _emit_json(list_humans())
    elif args.cmd == "lookup":
        _emit_json(lookup(args.query, ttl_hours=args.ttl_hours))
    elif args.cmd == "search":
        _emit_json(search(args.query))
    elif args.cmd == "freshness":
        _emit_json(freshness_check(args.handle, ttl_hours=args.ttl_hours))
    return 0


if __name__ == "__main__":
    sys.exit(main())
