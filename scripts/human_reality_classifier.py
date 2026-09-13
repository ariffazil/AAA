#!/usr/bin/env python3
"""
Human Reality Classifier — REGISTRY-DRIVEN (CLOSURE-002)
Phase 1 & 2 of APEX::HUMAN_REALITY_GRAPH_ACTIVATION::2026-09-13.

AUTHORITY : ARIF (F13 Sovereign)
DOCTRINE  : /root/AAA/prompts/HUMAN_REALITY_GRAPH_ACTIVATION_20260913.md
SPEC      : /root/AAA/canon/REALITY_CONSEQUENCE_OBJECTS_SPEC_v1.md
GOVERNANCE: /root/AAA/state/reality_objects/governance/GRO-SANCTUARY-001.yaml
GATE      : /root/AAA/scripts/reality_preflight.py

WHY THIS WAS REWRITTEN (CLOSURE-002, 2026-09-13)
------------------------------------------------
The previous revision discovered entities by iterating `/root/memory/people/` with
`iterdir()`. That is a FILESYSTEM scan, and a filesystem is not a human registry:

  · It counted 3 DIRECTORIES as human entities — `SCRIPTS`, `SCAR-WITNESSES`, `FAMILY`.
  · It therefore reported 14 "entities" of which only 11 were people.
  · WORSE: because it could only find people who happen to have a directory, it
    MISSED 6 registered humans — including `Fattah` (category family_minor, a minor)
    and three siblings (Naazira/Jia, Azwa, Fahim). The classifier built to protect
    the Sanctuary Invariant was blind to 4 of the 7 family members it exists for.

PRIMARY LAW:
  A name is not a human reality object.
  A mention is not a commitment.
  A memory is not a consequence.
  A person enters governance only when reality and consequence exist.

CLASSIFICATION TAXONOMY (H0..H5):
  H0 = Reference Only / non-person archetype   H1 = Stakeholder / Family Sanctuary
  H2 = Decision Owner   H3 = Consequence Owner
  H4 = Strategic Actor  H5 = Sovereign Actor

Source of truth: /root/memory/people/people_registry.json
The filesystem is used ONLY to detect REGISTRY GAPS (things on disk but not in the
registry) — never as the source of identity.
"""
from __future__ import annotations

import argparse
import fcntl
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml  # noqa: F401  (kept for parity / downstream use)
except ImportError:
    print("FATAL: pyyaml required", file=sys.stderr)
    sys.exit(1)

PEOPLE_DIR = Path("/root/memory/people")
REGISTRY = PEOPLE_DIR / "people_registry.json"
OUT_DIR = Path("/root/AAA/state/reality_objects")
MANIFEST_PATH = OUT_DIR / "human_entity_manifest.json"

# Categories that are NOT human persons (archetypes / groupings / infrastructure)
NON_PERSON_CATEGORIES = {
    "institutional_archetype", "conceptual_archetype",
}
NON_PERSON_DIR_NAMES = {"SCRIPTS", "SCAR-WITNESSES", "FAMILY", "__PYCACHE__", "ARCHIVE"}

# Sanctuary = family life & personal sanctuary. These categories are protected by GRO-SANCTUARY-001.
SANCTUARY_CATEGORIES = {
    "family", "family_parents", "family_siblings", "family_extended",
    "family_minor", "personal_sanctuary",
}

# Category -> tier. Individual overrides applied separately.
CATEGORY_TIER = {
    "sovereign": "H5",
    "family": "H1", "family_parents": "H1", "family_siblings": "H1",
    "family_extended": "H1", "family_minor": "H1", "personal_sanctuary": "H1",
    "named_institutional_person": "H3",
    "professional_peer": "H1",
    "institutional_witness": "H1",
    "strategic_leadership": "H4",
    "telegram_network": "H1",
    "institutional_archetype": "H0", "conceptual_archetype": "H0",
}

# Explicit tier/meaning overrides for named individuals (canon-grounded).
CANONICAL_PEOPLE: dict[str, dict] = {
    "ARIF": {"tier": "H5", "role": "Sovereign Principal & Architect",
             "has_active_consequence": True, "attention_cost": "HIGH",
             "consequence_class": "STRATEGIC"},
    "AHMAD FAISAL BAKAR": {"tier": "H3", "role": "Former VP Exploration (PETRONAS Carigali)",
                           "has_active_consequence": True, "attention_cost": "LOW",
                           "consequence_class": "REPUTATIONAL"},
    "TENGKU TAUFIK": {"tier": "H4", "role": "President & Group CEO, PETRONAS",
                      "has_active_consequence": True, "attention_cost": "MEDIUM",
                      "consequence_class": "STRATEGIC"},
    "TENGKU MUHAMMAD TAUFIK": {"tier": "H4", "role": "President & Group CEO, PETRONAS",
                               "has_active_consequence": True, "attention_cost": "MEDIUM",
                               "consequence_class": "STRATEGIC"},
    "LALETHA": {"tier": "H3", "role": "PETRONAS Supervisor / Line Manager",
                "has_active_consequence": True, "attention_cost": "MEDIUM",
                "consequence_class": "OPERATIONAL"},
    "SYED": {"tier": "H2", "role": "Collaborator / Technical Partner",
             "has_active_consequence": True, "attention_cost": "MEDIUM",
             "consequence_class": "OPERATIONAL"},
}

# Grounded aliases: people/ABBAH = P-002 Fazil bin Khamis; people/MAK = P-003 Faridah; JUKHRIS = P-025 Mohd Jukris.
DIR_ALIASES = {
    "ABBAH": "FAZIL BIN KHAMIS",
    "MAK": "FARIDAH BINTI OTHMAN",
    "JUKHRIS": "MOHD JUKRIS BIN ABDUL WAHAB",
}


def _alias(name_upper: str) -> str | None:
    if "(" in name_upper and ")" in name_upper:
        return name_upper[name_upper.index("(") + 1:name_upper.index(")")].strip()
    return None


def _override_for(name_upper: str) -> dict | None:
    flat = name_upper.replace("-", " ").replace("  ", " ")
    for key, meta in CANONICAL_PEOPLE.items():
        if key in flat:
            return {**meta, "_matched_key": key}
    return None


def load_registry() -> tuple[list[dict], str | None]:
    if not REGISTRY.exists():
        return [], f"registry absent at {REGISTRY}"
    try:
        data = json.loads(REGISTRY.read_text())
    except Exception as exc:  # noqa: BLE001
        return [], f"registry unreadable: {exc}"
    return data.get("people", []), None


def classify_from_registry(people: list[dict]) -> list[dict]:
    out: list[dict] = []
    for p in people:
        name = str(p.get("name", "")).strip()
        if not name:
            continue
        up = name.upper()
        cat = str(p.get("category", "unknown")).lower()
        alias = _alias(up)
        over = _override_for(up)
        is_non_person = cat in NON_PERSON_CATEGORIES
        is_sanctuary = (cat in SANCTUARY_CATEGORIES) or bool(p.get("sanctuary_protected"))
        tier = (over or {}).get("tier") or CATEGORY_TIER.get(cat, "H0")
        out.append({
            "name": up,
            "display_name": name,
            "aliases": [a for a in filter(None, [alias]) if a],
            "registry_category": cat,
            "registry_memory_authority": p.get("memory_authority"),
            "registry_relation": p.get("relation"),
            "registry_status": p.get("status"),
            "tier": tier,
            "category": ("FAMILY_SANCTUARY" if is_sanctuary
                         else "NON_PERSON_ARCHETYPE" if is_non_person
                         else "CANONICAL"),
            "sanctuary_protected": is_sanctuary,
            "is_person": not is_non_person,
            "role": (over or {}).get("role"),
            "attention_cost": (over or {}).get("attention_cost"),
            "consequence_class": (over or {}).get("consequence_class"),
            "is_hro_candidate": bool((over or {}).get("has_active_consequence", False)),
            "source": "registry",
        })
    return out


def _registry_tokens(entities: list[dict]) -> set[str]:
    """Every name-token from the canonical registry, so a directory named ARIF or
    FARIDAH or NABILAH is recognised as a person we already have — not a gap.
    (Bug found on first run of this rewrite, 2026-09-13: plain string equality
    reported 6 false gaps.)"""
    toks: set[str] = set()
    for e in entities:
        for src in [e["name"], *e.get("aliases", [])]:
            for part in str(src).split():
                t = part.strip("(),.")
                if len(t) > 2:
                    toks.add(t)
    return toks


def detect_registry_gaps(entities: list[dict]) -> list[dict]:
    """Filesystem entries NOT represented in the canonical registry. Reported,
    never silently promoted and never silently dropped."""
    tokens = _registry_tokens(entities)
    known_names = {e["name"] for e in entities}
    gaps: list[dict] = []
    if not PEOPLE_DIR.exists():
        return gaps
    for item in sorted(PEOPLE_DIR.iterdir()):
        if not item.is_dir() or item.name.startswith("."):
            continue
        nm = item.name.upper()
        if nm in NON_PERSON_DIR_NAMES:
            continue
        target = DIR_ALIASES.get(nm, nm).split()[0]
        if nm in known_names or nm in tokens or target in tokens:
            continue
        gaps.append({
            "dir": str(item),
            "name": nm,
            "note": "present on disk, ABSENT from people_registry.json — "
                    "add to the registry or archive; not a human reality object yet",
        })
    return gaps


def classify_unregistered_actors(entities: list[dict]) -> list[dict]:
    """Tier actors reachable only from canon (no registry entry). Reported explicitly
    so an empty tier is EXPLAINED rather than silent — the Reality Mismatch Arif
    asked us to probe: tier-definition vs tier-assignment."""
    tokens = _registry_tokens(entities)
    out: list[dict] = []
    for key, meta in CANONICAL_PEOPLE.items():
        parts = [t.strip("(),.") for t in key.split()]
        if parts and all(p in tokens for p in parts):
            continue  # already represented in the registry
        out.append({
            "name": key,
            "tier": meta["tier"],
            "category": "ABSENT_FROM_REGISTRY",
            "sanctuary_protected": False,
            "is_person": True,
            "role": meta.get("role"),
            "is_hro_candidate": bool(meta.get("has_active_consequence")),
            "source": "canonical_override",
            "note": "tier assigned from canon but entity is NOT in "
                    "people_registry.json — registry gap",
        })
    return out


def build_manifest() -> dict:
    people, reg_err = load_registry()
    entities = classify_from_registry(people)
    unregistered = classify_unregistered_actors(entities)
    all_rows = entities + unregistered
    gaps = detect_registry_gaps(entities)

    # HRO objects exist for people who are NOT in the canonical registry (e.g.
    # Laletha, Syed Khairuddin). Registry-first classification would silently drop
    # them from the manifest — the same silent-loss class we just fixed for
    # directories. Detect and REPORT; never silently lose a governed human.
    hro_no_reg: list[dict] = []
    known_tokens = {e["name"] for e in entities} | _registry_tokens(entities)
    # SCHEMA GAP DISCOVERED 2026-09-13: arifos.hro.v1 declares `owner` and
    # `stakeholders` but NO `subject_person`. The human a HRO is about is therefore
    # only recoverable from the human-readable id/title. `owner` is ARIF for every
    # HRO (he owns the obligation), so scanning `owner` found nothing — the first
    # revision of this detector was a no-op. Parsing the id is a HEURISTIC, flagged
    # as such; the correct fix is a `subject_person` field on the ratified schema.
    NON_PERSON_TOKENS = {"HRO", "CRO", "WRO", "MRO", "GRO", "PETRONAS", "ARIFOS",
                         "AFFORGE", "GEOX", "WEALTH", "WELL", "AAA", "COPILOT",
                         "SERVICE", "ENERGY", "INDUSTRY", "LIFE", "SHEET",
                         "OPERATOR", "GOLD", "TRADING", "MEMORY", "VAULT"}
    obj_dir = Path("/root/AAA/state/reality_objects")
    if obj_dir.exists():
        for hro in sorted(obj_dir.glob("HRO-*.yaml")):
            try:
                d = yaml.safe_load(hro.read_text()) or {}
            except Exception:  # noqa: BLE001
                continue
            subj = str(d.get("subject_person", "")).strip().upper()
            hid = str(d.get("id", hro.stem)).upper()
            cands = [subj] if subj else [t for t in hid.split("-")
                     if t.isalpha() and t not in NON_PERSON_TOKENS]
            unresolved = [t for t in cands if t not in known_tokens]
            if cands and unresolved:
                hro_no_reg.append({
                    "hro": hro.name,
                    "subject_candidates": cands,
                    "unresolved_in_registry": unresolved,
                    "schema_gap": ("none (subject_person present)" if subj
                                  else "arifos.hro.v1 has no subject_person field; subject recovered heuristically from id"),
                    "note": "an HRO exists for a subject absent from "
                            "people_registry.json — register the person, or archive the "
                            "object; today it exists in governance but not in memory",
                })

    tiers = {f"H{i}": [] for i in range(6)}
    for e in all_rows:
        tiers.setdefault(e["tier"], []).append(e["name"])

    persons = [e for e in all_rows if e.get("is_person")]
    sanctuary = [e for e in all_rows if e.get("sanctuary_protected")]

    return {
        "schema": "arifos.human_manifest.v2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_of_truth": str(REGISTRY),
        "registry_error": reg_err,
        "total_registry_entries": len(people),
        "total_classified": len(all_rows),
        "total_persons": len(persons),
        "total_non_person_rows": len(all_rows) - len(persons),
        "tiers": {k: sorted(v) for k, v in tiers.items()},
        "tier_counts": {k: len(v) for k, v in tiers.items()},
        "empty_tiers": sorted([k for k, v in tiers.items() if not v]),
        "hro_candidates_count": len([e for e in all_rows if e.get("is_hro_candidate")]),
        "sanctuary_protected_count": len(sanctuary),
        "sanctuary_protected_ids": sorted(e["name"] for e in sanctuary),
        "sanctuary_categories": sorted(SANCTUARY_CATEGORIES),
        "registry_gaps_on_disk": gaps,
        "hro_without_registry": hro_no_reg,
        "unregistered_actors": unregistered,
        "entities": all_rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Human Reality Classifier (registry-driven)")
    parser.add_argument("--report", action="store_true")
    args = parser.parse_args()

    m = build_manifest()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    lock_file = MANIFEST_PATH.with_suffix(".lock")
    with open(lock_file, "w") as lock_fd:
        fcntl.flock(lock_fd.fileno(), fcntl.LOCK_EX)
        try:
            tmp = MANIFEST_PATH.with_suffix(".tmp")
            with open(tmp, "w") as f:
                json.dump(m, f, indent=2)
            os.replace(tmp, MANIFEST_PATH)
        finally:
            fcntl.flock(lock_fd.fileno(), fcntl.LOCK_UN)

    print(f"Human Reality Classifier — registry-driven ({m['source_of_truth']})")
    if m["registry_error"]:
        print(f"  !! registry_error: {m['registry_error']}")
    print(f"  registry entries          : {m['total_registry_entries']}")
    print(f"  classified rows           : {m['total_classified']} "
          f"({m['total_persons']} persons, {m['total_non_person_rows']} non-person)")
    for i in (5, 4, 3, 2, 1, 0):
        k = f"H{i}"
        names = m["tiers"].get(k, [])
        print(f"  {k:<2} ({len(names):>2}) {', '.join(names[:6])}"
              f"{' ...' if len(names) > 6 else ''}")
    if m["empty_tiers"]:
        print(f"  empty tiers               : {', '.join(m['empty_tiers'])}")
    print(f"\n  Sanctuary-protected       : {m['sanctuary_protected_count']} "
          f"→ {', '.join(m['sanctuary_protected_ids'])}")
    print(f"  HRO candidates            : {m['hro_candidates_count']}")
    if m["registry_gaps_on_disk"]:
        print(f"\n  REGISTRY GAPS (on disk, not in registry):")
        for g in m["registry_gaps_on_disk"]:
            print(f"    - {g['name']}")
    if m.get("hro_without_registry"):
        print(f"\n  HRO WITHOUT REGISTRY (governance exists, memory does not):")
        for h in m["hro_without_registry"]:
            print(f"    - {', '.join(h['unresolved_in_registry'])}  ({h['hro']}) "
                  f"[subject from id — schema gap]")
    if m["unregistered_actors"]:
        print(f"\n  UNREGISTERED TIER ACTORS (canon-only):")
        for u in m["unregistered_actors"]:
            print(f"    - {u['tier']} {u['name']} ({u['role']})")
    print(f"\nManifest written to: {MANIFEST_PATH}")
    print("Sanctuary enforcement: GRO-SANCTUARY-001 via scripts/reality_preflight.py "
          "(runtime block, not a printed sentence)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
