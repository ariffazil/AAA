#!/usr/bin/env python3
"""
aforge_warga_view_generator.py

Generates the WARGA_AFORGE_VIEW from existing machine truths.

Reads:
  - /root/AAA/registries/AFORGE_VERB_SCHEMA.json       (cold verb schema)
  - /root/AAA/registries/CAPABILITY_INDEX.json          (live tools/list, 343 federation tools)
  - /root/A-FORGE/a_think/affordances.yaml              (semantic surface for aforge tools)

Writes:
  - /root/AAA/state/aforge/warga-capabilities.json      (projection output, regenerable)

The WARGA view is a projection, not a stored artifact. Re-run after:
  - AFORGE_VERB_SCHEMA.json changes
  - CAPABILITY_INDEX.json digest changes
  - affordances.yaml changes
  - per-session allowed capability set changes (out of scope for default projection)

Per A-FORGE ↔ AAA Competency Protocol v1 (2026-10-01):
  C_warga = C_live ∩ C_affordance ∩ C_kernel ∩ C_authority
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("error: PyYAML not installed. pip install pyyaml", file=sys.stderr)
    sys.exit(2)


VERB_SCHEMA_PATH = Path("/root/AAA/registries/AFORGE_VERB_SCHEMA.json")
CAPABILITY_INDEX_PATH = Path("/root/AAA/registries/CAPABILITY_INDEX.json")
AFFORDANCES_PATH = Path("/root/A-FORGE/a_think/affordances.yaml")
OUTPUT_PATH = Path("/root/AAA/state/aforge/warga-capabilities.json")


def sha256_file(path: Path) -> str:
    """SHA-256 of file bytes (used as fingerprint for cache invalidation)."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def load_verb_schema() -> dict[str, Any]:
    return json.loads(VERB_SCHEMA_PATH.read_text())


def load_capability_index() -> dict[str, Any]:
    return json.loads(CAPABILITY_INDEX_PATH.read_text())


def load_affordances() -> dict[str, Any]:
    return yaml.safe_load(AFFORDANCES_PATH.read_text())


def map_affordance_class_to_verb(affordance_class: str, capability_surface: str) -> str | None:
    """Heuristic: map affordance_class + capability_surface prefix to a verb."""
    # capability_surface pattern: aforge.<class>.<verb>  e.g. aforge.execute.abort
    if capability_surface.startswith("aforge."):
        parts = capability_surface.split(".")
        if len(parts) >= 2:
            cls = parts[1]
            sub = parts[2] if len(parts) > 2 else ""
            # ACTUATOR-style classes → change/run/control
            if cls in ("execute", "build", "deploy"):
                if sub in ("abort", "rollback", "status", "pause", "resume"):
                    return "forge_control"
                return "forge_run"
            if cls in ("patch", "commit", "fill"):
                return "forge_change"
            if cls in ("plan", "lease", "budget", "compile"):
                return "forge_plan"
            if cls in ("verify", "judge", "test", "lint", "witness"):
                return "forge_verify"
            if cls in ("extend", "ephemeral", "genesis", "sandbox"):
                return "forge_extend"
            if cls in ("read", "list", "search", "tree", "grep", "probe"):
                return "forge_inspect"
    if affordance_class in ("probe", "read", "registry"):
        return "forge_inspect"
    if affordance_class in ("build", "execute"):
        return "forge_run"
    if affordance_class in ("patch", "modify"):
        return "forge_change"
    if affordance_class in ("verify", "judge"):
        return "forge_verify"
    return None


def build_verb_view(
    verb: str,
    verb_schema: dict[str, Any],
    tools: list[dict[str, Any]],
    affordances: dict[str, Any],
    affordance_by_name: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Build one verb's section of the projection output."""
    intent = verb_schema["verbs"][verb]["intent"]
    agent_visible_schema = verb_schema["verbs"][verb]["agent_visible_schema"]

    # Candidates: tools that resolve to this verb
    candidates: list[dict[str, Any]] = []
    for tool in tools:
        if tool.get("server") != "aforge":
            continue
        tool_name = tool.get("tool_name", "")
        affordance = affordance_by_name.get(tool_name)
        if affordance is None:
            # Tool exists in live tools/list but no affordance card — surface it as PENDING
            candidates.append({
                "tool_name": tool_name,
                "verb_mapping": verb,  # default mapping
                "status": "PENDING_AFFORDANCE",
                "risk_label": None,
                "mutation_class": None,
                "requires_human_approval": None,
                "description_short": (tool.get("description", "")[:120] + "...") if len(tool.get("description", "")) > 120 else tool.get("description", ""),
            })
            continue

        mapped_verb = map_affordance_class_to_verb(
            affordance.get("affordance_class", ""),
            affordance.get("capability_surface", ""),
        )
        if mapped_verb != verb:
            continue

        candidates.append({
            "tool_name": tool_name,
            "verb_mapping": verb,
            "status": "OK",
            "risk_label": affordance.get("risk_label"),
            "mutation_class": affordance.get("mutation_class"),
            "requires_human_approval": affordance.get("requires_human_approval"),
            "destructive": affordance.get("destructive"),
            "reversible": affordance.get("reversible"),
            "external_side_effect": affordance.get("external_side_effect"),
            "min_mode": affordance.get("min_mode"),
            "capability_surface": affordance.get("capability_surface"),
            "description_short": (affordance.get("purpose", "")[:120] + "...") if len(affordance.get("purpose", "")) > 120 else affordance.get("purpose", ""),
        })

    # Sort: OK first, then by risk_label (R0 first)
    risk_order = {f"R{i}": i for i in range(10)}
    candidates.sort(key=lambda c: (0 if c["status"] == "OK" else 1, risk_order.get(c.get("risk_label") or "R9", 9)))

    # Determine overall verb authority ceiling from candidates
    mutation_classes = {c.get("mutation_class") for c in candidates if c["status"] == "OK"}
    if "IRREVERSIBLE" in mutation_classes:
        ceiling = "MUTATE_IRREVERSIBLE"
    elif "MUTATE" in mutation_classes:
        ceiling = "MUTATE"
    elif "DRAFT" in mutation_classes:
        ceiling = "DRAFT"
    else:
        ceiling = "OBSERVE_ONLY"

    return {
        "intent": intent,
        "agent_visible_schema": agent_visible_schema,
        "authority_ceiling": ceiling,
        "candidate_count": len(candidates),
        "candidates": candidates,
    }


def build_warga_view(verb_schema: dict, capability_index: dict, affordances: dict) -> dict[str, Any]:
    """Build the full WARGA projection."""
    tools = capability_index.get("tools", [])
    affordance_tools = affordances.get("tools", []) if isinstance(affordances, dict) else []
    affordance_by_name = {a["name"]: a for a in affordance_tools if isinstance(a, dict) and "name" in a}

    verbs = verb_schema["verbs"]
    view = {
        "$schema": "arifOS/AAA/warga-aforge-view/v1",
        "version": "0.1.0-draft",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generated_by": "aforge_warga_view_generator.py",
        "doctrine_root": verb_schema.get("doctrine_root"),
        "rule": "C_warga = C_live ∩ C_affordance ∩ C_kernel ∩ C_authority (default projection excludes session filter)",
        "sources": {
            "verb_schema": {
                "path": str(VERB_SCHEMA_PATH),
                "fingerprint": sha256_file(VERB_SCHEMA_PATH),
                "version": verb_schema.get("version"),
            },
            "capability_index": {
                "path": str(CAPABILITY_INDEX_PATH),
                "fingerprint": sha256_file(CAPABILITY_INDEX_PATH),
                "digest": capability_index.get("digest"),
                "total_tools": capability_index.get("total_tools"),
            },
            "affordances": {
                "path": str(AFFORDANCES_PATH),
                "fingerprint": sha256_file(AFFORDANCES_PATH),
            },
        },
        "verbs": {},
        "summary": {
            "verb_count": 0,
            "candidate_count_total": 0,
            "pending_affordance_count": 0,
        },
    }

    for verb_name in verb_schema.get("verb_names_proposed", []):
        if verb_name not in verbs:
            continue
        verb_view = build_verb_view(verb_name, verb_schema, tools, affordances, affordance_by_name)
        view["verbs"][verb_name] = verb_view
        view["summary"]["verb_count"] += 1
        view["summary"]["candidate_count_total"] += verb_view["candidate_count"]
        view["summary"]["pending_affordance_count"] += sum(1 for c in verb_view["candidates"] if c["status"] == "PENDING_AFFORDANCE")

    return view


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0] if __doc__ else "Generate WARGA view")
    parser.add_argument("--check", action="store_true", help="Check fingerprints and exit 0 if up-to-date, 1 if stale")
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH, help=f"Output path (default: {OUTPUT_PATH})")
    args = parser.parse_args()

    verb_schema = load_verb_schema()
    capability_index = load_capability_index()
    affordances = load_affordances()

    if args.check:
        # Compare fingerprints against last output
        if not args.output.exists():
            print(f"missing: {args.output}", file=sys.stderr)
            sys.exit(1)
        try:
            old = json.loads(args.output.read_text())
        except json.JSONDecodeError as e:
            print(f"corrupt existing output: {e}", file=sys.stderr)
            sys.exit(1)
        old_sources = old.get("sources", {})
        staleness = []
        for k in ("verb_schema", "capability_index", "affordances"):
            new_fp = sha256_file({"verb_schema": VERB_SCHEMA_PATH, "capability_index": CAPABILITY_INDEX_PATH, "affordances": AFFORDANCES_PATH}[k])
            old_fp = old_sources.get(k, {}).get("fingerprint")
            if old_fp != new_fp:
                staleness.append(k)
        if staleness:
            print(f"stale: {staleness}")
            sys.exit(1)
        print("up-to-date")
        sys.exit(0)

    view = build_warga_view(verb_schema, capability_index, affordances)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(view, indent=2, ensure_ascii=False))
    print(f"wrote {args.output}")
    print(f"  verbs: {view['summary']['verb_count']}")
    print(f"  candidates: {view['summary']['candidate_count_total']}")
    print(f"  pending affordance: {view['summary']['pending_affordance_count']}")


if __name__ == "__main__":
    main()