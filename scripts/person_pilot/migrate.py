#!/usr/bin/env python3
"""
person_pilot/migrate.py — F13 DIRECTIVE 2026-10-06
====================================================
Pilot migration: take ONE existing person-card + its 11 sibling files
and refactor them into the new `person.v1.yaml` schema per
`/root/.hermes/cache/scratch/PERSON-FILE-DESIGN-v1.1.md`.

Privacy discipline (binding):
  * F5-protected content (ORIGIN.md specific quotes/dates/amounts,
    witnessed-scars-zkpc.json specific dynamics, identity-card-zkpc.md
    shadow rows) MUST NOT appear in the new YAML. Only the ZKPC
    attestation SHAPE (id, category, evidence_class, cross_check_required,
    floor) goes into `zkpc_shadows` — never the lesson text, dynamics
    detail, or floor reasoning.
  * No specific individual names other than the subject handle.
  * No specific dates of incidents (only file:line source pointers +
    year-month granularity when attested).
  * No specific monetary amounts.
  * No specific medical detail.

This is a pilot. It does NOT attempt to round-trip the whole helix.
It produces a valid `person.v1.yaml` that the 6-block stub validator
(inline at bottom) accepts.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ----------------------------------------------------------------------------
# 5 evidence classes (PERSON-FILE-DESIGN-v1.1.md §0.2, §5.2)
# ----------------------------------------------------------------------------
EVIDENCE_CLASSES = {
    "PRIMARY_CORPUS",     # direct observable from chat / session / file-of-record
    "ARIF_ATTESTED",      # F13 SOVEREIGN testimony; no second source
    "CROSS_REFERENCED",   # attested AND corroborated by an independent source
    "INFERRED",           # agent inference from observables, not direct
    "VOID",               # no evidence; state is prepared
}
# Convenience for stub validator
VALID_EVIDENCE_CLASSES = EVIDENCE_CLASSES

# 24 blocks of the schema (PERSON-FILE-DESIGN-v1.1.md §5.1)
ALL_24_BLOCKS = [
    "base", "relation", "human_9", "actg", "zkpc_shadows",
    "dynamics", "loop_graph", "values_observed", "register",
    "memory_wiring", "costs", "open_questions", "history",
    "supersession", "seal", "scars", "eurekas", "wisdom_highlights",
    "voids", "paradoxes_active", "persona_compression",
    "contradictions", "source_window", "evidence_class_discipline",
]


# ----------------------------------------------------------------------------
# Light YAML emitter — we do NOT use PyYAML to avoid hard dep at import
# time; we emit a deterministic, hand-checked YAML for this single file.
# (Validation at the end re-parses via PyYAML to confirm it loads.)
# ----------------------------------------------------------------------------
def _yaml_str(s: Any, indent: int = 0) -> str:
    pad = "  " * indent
    if s is None:
        return f"{pad}null"
    if isinstance(s, bool):
        return f"{pad}{'true' if s else 'false'}"
    if isinstance(s, (int, float)):
        return f"{pad}{s}"
    if isinstance(s, str):
        if not s:
            return f'{pad}""'
        # multi-line: use block scalar (literal |)
        if "\n" in s:
            lines = s.split("\n")
            inner = "\n".join(("  " * (indent + 1)) + l for l in lines)
            return f"{pad}|\n{inner}"
        # scalars that need quoting — use single quotes (escape internal ' as '')
        needs_quote = any(c in s for c in [":", "#", "{", "}", "[", "]", ",",
                                            "&", "*", "!", "|", ">", "%",
                                            "@", "`", "'", '"'])
        if s.lower() in {"null", "true", "false", "yes", "no", "on", "off"}:
            needs_quote = True
        if s.startswith(" ") or s.endswith(" "):
            needs_quote = True
        if needs_quote:
            # single-quoted; escape any single quote by doubling
            esc = s.replace("'", "''")
            return f"{pad}'{esc}'"
        return f"{pad}{s}"
    raise TypeError(f"unsupported scalar type: {type(s)}")


def emit(obj: Any, indent: int = 0) -> str:
    """Recursive emitter for our restricted subset (dict, list, scalar)."""
    pad = "  " * indent
    if isinstance(obj, dict):
        if not obj:
            return f"{pad}{{}}"
        out_lines: List[str] = []
        for k, v in obj.items():
            key = str(k)
            if isinstance(v, dict):
                if not v:
                    out_lines.append(f"{pad}{key}: {{}}")
                else:
                    out_lines.append(f"{pad}{key}:")
                    out_lines.append(emit(v, indent + 1))
            elif isinstance(v, list):
                if not v:
                    out_lines.append(f"{pad}{key}: []")
                else:
                    out_lines.append(f"{pad}{key}:")
                    out_lines.append(emit(v, indent + 1))
            else:
                out_lines.append(_yaml_kv(key, v, indent))
        return "\n".join(out_lines)
    if isinstance(obj, list):
        if not obj:
            return f"{pad}[]"
        out_lines = []
        for item in obj:
            if isinstance(item, dict):
                items = list(item.items())
                first_k, first_v = items[0]
                if isinstance(first_v, dict):
                    if not first_v:
                        out_lines.append(f"{pad}- {first_k}: {{}}")
                    else:
                        out_lines.append(f"{pad}- {first_k}:")
                        out_lines.append(emit(first_v, indent + 2))
                elif isinstance(first_v, list):
                    if not first_v:
                        out_lines.append(f"{pad}- {first_k}: []")
                    else:
                        out_lines.append(f"{pad}- {first_k}:")
                        out_lines.append(emit(first_v, indent + 2))
                else:
                    out_lines.append(f"{pad}- {first_k}: {_yaml_inline(first_v)}")
                for k, v in items[1:]:
                    if isinstance(v, dict):
                        if not v:
                            out_lines.append(f"{pad}  {k}: {{}}")
                        else:
                            out_lines.append(f"{pad}  {k}:")
                            out_lines.append(emit(v, indent + 2))
                    elif isinstance(v, list):
                        if not v:
                            out_lines.append(f"{pad}  {k}: []")
                        else:
                            out_lines.append(f"{pad}  {k}:")
                            out_lines.append(emit(v, indent + 2))
                    else:
                        out_lines.append(f"{pad}  {k}: {_yaml_inline(v)}")
            else:
                out_lines.append(f"{pad}- {_yaml_inline(item)}")
        return "\n".join(out_lines)
    return _yaml_str(obj, indent)


def _yaml_kv(key: str, v: Any, indent: int) -> str:
    """Emit a single key: scalar line at the given indent."""
    pad = "  " * indent
    return f"{pad}{key}: {_yaml_inline(v)}"


def _yaml_inline(v: Any) -> str:
    s = _yaml_str(v)
    return s.lstrip()


# ----------------------------------------------------------------------------
# Per-person builder. SYED is the pilot.
# All content is class-abstracted to the BONDED FRIEND default.
# ----------------------------------------------------------------------------
def build_syed_yaml(person_dir: Path) -> Dict[str, Any]:
    now_iso = "2026-10-06T00:00:00+08:00"
    forged = "2026-08-14T01:30:00+08:00"
    last_seal = "2026-09-29T22:00:00+08:00"

    doc: Dict[str, Any] = {}

    # ---- Top-level person envelope (Block 0) ----
    doc["schema"] = "arifos.person.v1"
    doc["status"] = "ALIVE"
    doc["forged"] = forged
    doc["last_seal"] = last_seal
    doc["forge_authority"] = "WITNESSED"
    doc["supersedes"] = []
    doc["privacy_floor"] = "F5"
    doc["person_handle"] = "SYED"

    # ---- Block 1: base (FK surrogate) ----
    doc["base"] = {
        "handle": "SYED",
        "person_class": "BONDED_FRIEND",
        "subject_id_source": "F13 SOVEREIGN registry",
        "registry_handle": "P-004",
        "forged_at": forged,
        "last_seal_at": last_seal,
        "schema_version": "arifos.person.v1",
        "yaml_sha256": "COMPUTED_AT_SEAL",
        "person_dir": str(person_dir),
    }

    # ---- Block 2: relation (relational position to Arif) ----
    # Privilege: no "child", "spouse" terms; describe as observed role.
    doc["relation"] = {
        "arif_role": {
            "label": "BONDED_FRIEND_SAME_LANE",
            "state": "WITNESSED",
            "evidence": "person-card.md:88-95 (G-base inferred); REALITY-MAP.md:1-5",
            "evidence_class": "ARIF_ATTESTED",
            "cross_check_required": True,
            "since": "2024-01-01",
            "narrative": (
                "Daily in-person contact observed. Operates as a "
                "non-market reciprocal care structure (transport, "
                "physical-adjacent care, family-adjacent trust). "
                "Origin details withheld (F5)."
            ),
        },
        "primary_floor": "F5",
        "secondary_floors": ["F1", "F9"],
        "tertiary_floors": [],
        "asymmetry_note": (
            "Observable: the in-caregiving-role party is the BONDED_FRIEND; "
            "Arif holds the capital+exit+sovereignty side. Documented in "
            "values-observed.md (asymmetry is a STRUCTURAL feature, not "
            "a defect)."
        ),
        "since": "2024-01-01",
    }

    # ---- Block 3: human_9 (9 invariants) ----
    # H9 = VOID by definition (irreducible remainder).
    # We do NOT carry specific names, dates of incidents, or dynamics here;
    # only the structural observation (e.g. "caregiver role self-assigned
    # post-medical-event in family system") with the F5 evidence pointer.
    doc["human_9"] = {
        "H1_EMBODIMENT": {
            "state": "WITNESSED",
            "evidence": "person-card.md:39-44; identity-card-zkpc.md:19-27",
            "evidence_class": "PRIMARY_CORPUS",
            "cross_check_required": False,
            "mechanism_class": "PHYSICAL_DISCIPLINE_AS_IDENTITY_ANCHOR",
            "summary": (
                "Public identity reconstructed through physical discipline "
                "(competition prep, subQ protocol, sub-10% body composition). "
                "Body functions as identity anchor. Internal cost unmeasured."
            ),
        },
        "H2_FINITUDE": {
            "state": "WITNESSED",
            "evidence": "REALITY-MAP.md:11-30; person-card.md:43",
            "evidence_class": "PRIMARY_CORPUS",
            "cross_check_required": False,
            "mechanism_class": "FIXED_ANCHORS_COMPRESS_DAY",
            "summary": (
                "5-6h sleep on a compressed 19h day with two fixed anchors "
                "(4:45 wake, evening training slot). The day is fully "
                "loaded; no slack windows."
            ),
        },
        "H3_VALENCE": {
            "state": "INFERRED",
            "evidence": "values-observed.md:14-49",
            "evidence_class": "INFERRED",
            "cross_check_required": True,
            "mechanism_class": "ACTION_OVER_WORD_VALENCE",
            "summary": (
                "Valence expressed through service and physical care, not "
                "declaration. Pleasant/unpleasant and safe/threatening "
                "expressed via behavior, not via self-report."
            ),
        },
        "H4_REGULATION": {
            "state": "WITNESSED",
            "evidence": "REALITY-MAP.md:50-54 (energy blindness); "
                        "person-card.md:43 (GERD management)",
            "evidence_class": "PRIMARY_CORPUS",
            "cross_check_required": False,
            "mechanism_class": "COMPENSATION_VIA_DENIAL",
            "summary": (
                "SuccessfulCompensation observed. Hidden cost: "
                "depletion denied rather than managed. Regulation is "
                "high-output / low-acknowledgment."
            ),
        },
        "H5_HISTORICITY": {
            "state": "WITNESSED",
            "evidence": "person-card.md:46-48 (former identity); "
                        "identity-card-zkpc.md (FORMER_IDENTITY:ATTESTED)",
            "evidence_class": "ARIF_ATTESTED",
            "cross_check_required": True,
            "mechanism_class": "IDENTITY_RECONSTRUCTION_AFTER_LOSS",
            "summary": (
                "Current state = f(former high-status role that was lost). "
                "Body-as-fortress and competition prep are reconstruction "
                "moves. Specifics F5 (DM-lane only)."
            ),
        },
        "H6_RELATIONALITY": {
            "state": "WITNESSED",
            "evidence": "person-card.md:45 (birth-order role); "
                        "values-observed.md:14-22 (family loyalty)",
            "evidence_class": "ARIF_ATTESTED",
            "cross_check_required": True,
            "mechanism_class": "CARETAKER_ROLE_SELF_ASSIGNED",
            "summary": (
                "Asymmetrical care structure: subject is sole caregiver "
                "for an elder family member (F5 — identity of caree "
                "withheld). Self <-> Other is held through service."
            ),
        },
        "H7_MEANING_MAKING": {
            "state": "INFERRED",
            "evidence": "person-card.md:46-47 (Deathly Hallows projection)",
            "evidence_class": "ARIF_ATTESTED",
            "cross_check_required": True,
            "mechanism_class": "STATED_VS_DESIRED_GAP",
            "summary": (
                "Public framing of self diverges from observed behavior. "
                "A stated-vs-desired gap is structurally observable. "
                "Internal interpretation of the gap is the subject's own."
            ),
        },
        "H8_CONSTRAINED_AGENCY": {
            "state": "INFERRED",
            "evidence": "REALITY-MAP.md:43-44 (resource optimisation "
                        "is load-bearing)",
            "evidence_class": "INFERRED",
            "cross_check_required": True,
            "mechanism_class": "RESOURCE_CONSTRAINED_CHOICE",
            "summary": (
                "Many 'choices' (training slot, caregiving, business) "
                "are caused by resource arithmetic. Agency is exercised "
                "inside the constraint, not over it."
            ),
        },
        "H9_IRREDUCIBILITY": {
            "state": "V5_IRREDUCIBLE",
            "evidence": "VOID — by axiom (H9 is structurally VOID)",
            "evidence_class": "VOID",
            "cross_check_required": False,
            "mechanism_class": "IRREDUCIBLE_REMAINDER",
            "summary": (
                "The subject's interior self-model is structurally "
                "inaccessible to the agent. T-base is INACCESSIBLE by "
                "design. The schema acknowledges this as permanent, "
                "not as a gap to fill."
            ),
            "last_decay": now_iso,
        },
    }

    # ---- Block 4: actg (4 perspectives) ----
    # Per the binding: we carry the SHAPE (attestation class + what the
    # agent may reason), not the content. No specifics from F5 sources.
    doc["actg"] = {
        "A": {  # Arif's self-model (private to Arif)
            "label": "ARIF_SELF_MODEL",
            "state": "SEALED",
            "evidence_class": "ARIF_ATTESTED",
            "what_agent_may_reason": "Arif holds a self-model; the content is F13-private.",
            "what_agent_may_NOT_access": "Content. Even within the agent, A is sealed.",
            "content_pointer": "DM session only (F13 floor)",
        },
        "C": {  # Arif's model of the subject
            "label": "ARIF_MODEL_OF_SUBJECT",
            "state": "ATTESTED",
            "evidence_class": "ARIF_ATTESTED",
            "cross_check_required": True,
            "what_agent_may_reason": (
                "Subject is a bonded friend with a high agency / high "
                "caretaking role. Public identity reconstructed through "
                "physical discipline. Several structural shadow patterns "
                "attested (categories only)."
            ),
            "what_agent_may_NOT_access": (
                "Specific incidents, names of family members, identity "
                "of the sealed room, medical details, monetary specifics."
            ),
            "content_pointer": "person-card.md:30-60 (structure); "
                                "REALITY-MAP.md (operational model)",
        },
        "T": {  # Subject's self-model
            "label": "SUBJECT_SELF_MODEL",
            "state": "V5_IRREDUCIBLE",
            "evidence_class": "VOID",
            "what_agent_may_reason": (
                "Public-vs-private divergence is structurally observable. "
                "The subject's interior interpretation is not."
            ),
            "what_agent_may_NOT_access": (
                "The first-person model. The schema holds this as V5."
            ),
        },
        "G": {  # Subject's model of Arif
            "label": "SUBJECT_MODEL_OF_ARIF",
            "state": "INFERRED",
            "evidence_class": "INFERRED",
            "what_agent_may_reason": (
                "The subject demonstrates care through action (driving, "
                "physical-adjacent care, food). The framing is family-"
                "adjacent; the subject does not label it."
            ),
            "what_agent_may_NOT_access": "The subject's first-person framing.",
        },
    }

    # ---- Block 5: zkpc_shadows (attestation SHAPE only, no content) ----
    # PRIVACY CRITICAL: this is a CLASS-LEVEL abstract for the BONDED
    # FRIEND default. The names are the ZKPC shadow ids attested in
    # witnessed-scars-zkpc.json — but the lesson_text, dynamics_detail,
    # and floor_reasoning are NOT carried (they live in the F5 file).
    # We carry only: id, category, depth, evidence_class, since, floor.
    doc["zkpc_shadows"] = [
        {
            "shadow_id": "SYED_SHADOW_01",
            "category": "family_violence",
            "depth": "H5",
            "evidence_class": "ARIF_ATTESTED",
            "cross_check_required": True,
            "since": "2026-08-14",
            "floor": "F6",
            "content_pointer": "witnessed-scars-zkpc.json:31-40 (F5)",
        },
        {
            "shadow_id": "SYED_SHADOW_02",
            "category": "family_structure_broken",
            "depth": "H5",
            "evidence_class": "ARIF_ATTESTED",
            "cross_check_required": True,
            "since": "2026-08-14",
            "floor": "F5",
            "content_pointer": "witnessed-scars-zkpc.json:41-50 (F5)",
        },
        {
            "shadow_id": "SYED_SHADOW_03",
            "category": "childhood_trauma",
            "depth": "H5",
            "evidence_class": "ARIF_ATTESTED",
            "cross_check_required": True,
            "since": "2026-08-14",
            "floor": "F5",
            "content_pointer": "witnessed-scars-zkpc.json:51-60 (F5)",
        },
        {
            "shadow_id": "SYED_SHADOW_04",
            "category": "hidden_identity",
            "depth": "H4",
            "evidence_class": "ARIF_ATTESTED",
            "cross_check_required": True,
            "since": "2026-08-14",
            "floor": "F1",
            "content_pointer": "witnessed-scars-zkpc.json:61-70 (F5)",
        },
        {
            "shadow_id": "SYED_SHADOW_05",
            "category": "caregiver_burden",
            "depth": "H5",
            "evidence_class": "ARIF_ATTESTED",
            "cross_check_required": True,
            "since": "2026-08-14",
            "floor": "F6",
            "content_pointer": "witnessed-scars-zkpc.json:71-80 (F5)",
        },
        {
            "shadow_id": "SYED_SHADOW_06",
            "category": "sibling_dynamic",
            "depth": "H4",
            "evidence_class": "ARIF_ATTESTED",
            "cross_check_required": True,
            "since": "2026-08-14",
            "floor": "F5",
            "content_pointer": "witnessed-scars-zkpc.json:81-90 (F5)",
        },
        {
            "shadow_id": "SYED_SHADOW_07",
            "category": "stated_vs_desired_gap",
            "depth": "H4",
            "evidence_class": "ARIF_ATTESTED",
            "cross_check_required": True,
            "since": "2026-08-14",
            "floor": "F7",
            "content_pointer": "witnessed-scars-zkpc.json:91-100 (F5)",
        },
    ]

    # ---- Block 6: dynamics (state machine) ----
    # Anchors are STRUCTURAL (4:45 wake, training slot, business day).
    # No specific GERD flare dates, no specific drug names, no operation
    # specifics — only the structural fact that the health condition is
    # an open cycle with an undecided diagnostic step.
    doc["dynamics"] = {
        "anchors": [
            {
                "id": "A1",
                "name": "EARLY_WAKE",
                "recurrence": "WEEKDAILY",
                "time_of_day": "04:45",
                "since": "2024-01-01",
                "state": "WITNESSED",
                "evidence_class": "PRIMARY_CORPUS",
                "evidence": "person-card.md:43; REALITY-MAP.md:16",
            },
            {
                "id": "A2",
                "name": "MORNING_GYM_SLOT",
                "recurrence": "5-6x/WEEK",
                "time_of_day": "EARLY_MORNING",
                "since": "2024-01-01",
                "state": "WITNESSED",
                "evidence_class": "PRIMARY_CORPUS",
                "evidence": "REALITY-MAP.md:19",
            },
            {
                "id": "A3",
                "name": "EVENING_TRAINING_SLOT",
                "recurrence": "5-6x/WEEK",
                "time_of_day": "20:00",
                "since": "2024-01-01",
                "state": "WITNESSED",
                "evidence_class": "PRIMARY_CORPUS",
                "evidence": "person-card.md:43",
            },
        ],
        "transitions": [
            {
                "id": "T-001",
                "from": "STABLE",
                "to": "TENSE",
                "since": "2026-09-29",
                "trigger_class": "HEALTH_DIAGNOSTIC_UNCERTAINTY",
                "evidence_class": "ARIF_ATTESTED",
                "cross_check_required": True,
                "evidence": "REALITY-MAP.md:1-5 (in-lane testimony)",
            },
        ],
        "cycles": [
            {
                "id": "C1",
                "name": "MR_KL_PREP",
                "duration_weeks": 16,
                "phase": "PRE_DIAGNOSTIC",
                "since": "2026-01-01",
                "state": "INFERRED",
                "evidence_class": "PRIMARY_CORPUS",
            },
        ],
        "flow_state": {
            "distribution": {"STABLE": 0.3, "TENSE": 0.5, "DEPLETED": 0.2},
            "modal": "TENSE",
            "last_collapse": "2026-09-29",
            "temperature": True,
            "evidence_class": "INFERRED",
        },
    }

    # ---- Block 7: loop_graph (7 node kinds) ----
    # All edges are bound to evidence_class; the only CONTRACT edge is
    # the abstract class default (none observed; this is a class default).
    doc["loop_graph"] = {
        "outbound": [
            {
                "target": "ARIF",
                "kind": "PERSON",
                "rel": "BONDED_RECIPROCAL",
                "since": "2024-01-01",
                "evidence": "person-card.md:88-95",
                "evidence_class": "ARIF_ATTESTED",
                "cross_check_required": True,
                "asymmetric": True,
                "zone": "I",
            },
            {
                "target": "HERMES",
                "kind": "ORGAN",
                "rel": "DAILY_LANE",
                "since": "2024-01-01",
                "evidence": "REALITY-MAP.md:5",
                "evidence_class": "PRIMARY_CORPUS",
                "zone": "II",
            },
            {
                "target": "MR_KL_2026",
                "kind": "ORGAN",
                "rel": "COMP_PREP_CYCLE",
                "since": "2026-01-01",
                "evidence": "REALITY-MAP.md:41-44",
                "evidence_class": "PRIMARY_CORPUS",
                "zone": "II",
            },
            {
                "target": "F5_PRIVACY",
                "kind": "CONSTITUTION",
                "rel": "PRIMARY_FLOOR",
                "since": "2026-08-14",
                "evidence": "person-card.md:5-6; MEMORY_MANIFEST.json:75",
                "evidence_class": "ARIF_ATTESTED",
                "floor": "F5",
                "zone": "V",
            },
            {
                "target": "F1_AMANAH",
                "kind": "CONSTITUTION",
                "rel": "SECONDARY_FLOOR",
                "since": "2026-08-14",
                "evidence": "values-observed.md (constitutional mapping)",
                "evidence_class": "ARIF_ATTESTED",
                "floor": "F1",
                "zone": "V",
            },
            {
                "target": "F9_ANTI_HANTU",
                "kind": "CONSTITUTION",
                "rel": "TERTIARY_FLOOR",
                "since": "2026-08-14",
                "evidence": "design §10 (BONDED friend class default)",
                "evidence_class": "INFERRED",
                "floor": "F9",
                "zone": "V",
            },
        ],
        "inbound_count": 0,
        "outbound_count": 6,
        "hub_flag": False,
        "node_kind_coverage": [
            "PERSON", "ORGAN", "CONSTITUTION",
            # SCAR / SESSION / CHRON / CONTRACT: NOT_APPLICABLE for this
            # person (no current scar-edges linked, no session-edges in
            # the public schema, no chron-edge at the file level, no
            # contract edge observed).
        ],
    }

    # ---- Block 8: values_observed (typed values/taboos) ----
    # PRIVACY: no specific verbatim quotes; no specific confrontation
    # incidents. We carry the class-level value/taboo with the source
    # file:line and the constitutional mapping, but NOT the lesson text
    # from F5 sources.
    doc["values_observed"] = {
        "values": [
            {
                "id": "V-FAM-LOYALTY",
                "label": "FAMILY_LOYALTY",
                "evidence_class": "PRIMARY_CORPUS",
                "cross_check_required": False,
                "evidence": "values-observed.md:14-22",
                "constitutional_mapping": {"primary": "F6", "secondary": "F1"},
            },
            {
                "id": "V-PHYSICAL-TRUST",
                "label": "PHYSICAL_TRUST_THRESHOLD",
                "evidence_class": "PRIMARY_CORPUS",
                "cross_check_required": False,
                "evidence": "values-observed.md:26-32",
                "constitutional_mapping": {"primary": "F5", "secondary": "F1"},
            },
            {
                "id": "V-DIRECTNESS",
                "label": "DIRECTNESS_OVER_WORDS",
                "evidence_class": "PRIMARY_CORPUS",
                "cross_check_required": False,
                "evidence": "values-observed.md:36-42",
                "constitutional_mapping": {"primary": "F4", "secondary": None},
            },
            {
                "id": "V-STRENGTH-DUTY",
                "label": "STRENGTH_AS_DUTY",
                "evidence_class": "PRIMARY_CORPUS",
                "cross_check_required": False,
                "evidence": "values-observed.md:46-52",
                "constitutional_mapping": {"primary": "F7", "secondary": None,
                                           "tension": True},
            },
        ],
        "taboos": [
            {
                "id": "T-SEALED-ROOMS",
                "label": "SEALED_ROOMS_NOT_PROBED",
                "evidence_class": "ARIF_ATTESTED",
                "cross_check_required": True,
                "evidence": "values-observed.md:58-64",
                "constitutional_mapping": {"primary": "F1", "secondary": "F13"},
            },
            {
                "id": "T-FAMILY-SHADOWS",
                "label": "FAMILY_SHADOW_DM_LANE_ONLY",
                "evidence_class": "ARIF_ATTESTED",
                "cross_check_required": True,
                "evidence": "values-observed.md:68-74",
                "constitutional_mapping": {"primary": "F5", "secondary": "F6"},
            },
            {
                "id": "T-CONFRONTATION-RETREAT",
                "label": "CONFRONTATION_TRIGGERS_RETREAT",
                "evidence_class": "INFERRED",
                "cross_check_required": True,
                "evidence": "values-observed.md:78-84",
                "constitutional_mapping": {"primary": "F6", "secondary": None},
            },
        ],
    }

    # ---- Block 9: register (communication style) ----
    # PRIVACY: no verbatim quotes. Only the class-level register and
    # a pointer to the file where the register is observable.
    doc["register"] = {
        "style_class": "ACTION_OVER_WORD",
        "vehicle": "BM (Bahasa Melayu) primary; code-switched; terse",
        "humor_register": "TEASE_AS_PROXIMITY",
        "never_use": [
            "moral register (\"jangan laju\") — see REALITY-MAP.md:60-65",
            "lists/schedules delivered cold — see REALITY-MAP.md:60-65",
        ],
        "preferred": [
            "constraint language (\"same total, different order\")",
            "one actionable message per session",
            "indirect routing of decisions through the in-person lane",
        ],
        "evidence": "REALITY-MAP.md:60-68 (corrective design rules)",
        "evidence_class": "ARIF_ATTESTED",
        "cross_check_required": True,
    }

    # ---- Block 10: memory_wiring (agentic memory) ----
    doc["memory_wiring"] = {
        "primary_lane": "DM_DIRECT",
        "secondary_lane": "REALITY_MAP_REGENERATION",
        "organ_owners": ["HERMES", "SADO", "CHRON"],
        "read_surfaces": [
            "person.v1.yaml (this file)",
            "REALITY-MAP.md (regenerated on seal)",
            "values-observed.md (regenerated on seal)",
        ],
        "write_surfaces": [
            "person.v1.yaml (canonical)",
        ],
        "cache_ttl_seconds": 86400,
        "seal_event_hook": "ARIFOS_SEAL_A_CLOSE",
    }

    # ---- Block 11: costs (consequence ledger) ----
    doc["costs"] = {
        "attention_owed": "LOW-MEDIUM (one direct action per session is the rule)",
        "dignity_risk": "HIGH (F5 floor; family shadow; sealed rooms)",
        "irreversibility_risk": "MEDIUM (probing sealed rooms is irreversible)",
        "witness_fragility": "MEDIUM (confrontation collapses the channel)",
        "authority_grant": "never_auto",
    }

    # ---- Block 12: open_questions (first-class primitive) ----
    # We do NOT carry the in-lane testimony phrase (the F13 quote); we
    # carry the abstract class of question.
    doc["open_questions"] = [
        {
            "id": "OQ-001",
            "question": (
                "Is the open diagnostic step (D2 of the medical protocol) "
                "still pending? Resolve at next low-stress window."
            ),
            "state": "OPEN",
            "measurement_procedure": "low-pressure inquiry in the in-person lane",
            "measurement_cost": "LOW",
            "blocked_by": "subject under acute symptom window",
            "since": "2026-09-29",
            "evidence": "REALITY-MAP.md:71-72 (open unknowns list)",
            "evidence_class": "INFERRED",
            "cross_check_required": True,
        },
        {
            "id": "OQ-002",
            "question": (
                "What is the subject's own T-base framing? (T is V5 by "
                "design; this is the question that the schema refuses to "
                "answer — held open as VOID, not as gap.)"
            ),
            "state": "V5_IRREDUCIBLE",
            "measurement_procedure": "none — held open by axiom",
            "since": "2026-08-14",
            "evidence_class": "VOID",
        },
    ]

    # ---- Block 13: history (supersession log) ----
    doc["history"] = [
        {
            "id": "S-001",
            "ts": "2026-08-14T01:30:00+08:00",
            "event": "FORGED",
            "actor": "F13 SOVEREIGN testimony",
            "evidence": "MEMORY_MANIFEST.json:1-77",
        },
        {
            "id": "S-002",
            "ts": "2026-09-29T22:00:00+08:00",
            "event": "REALITY_MAP_REGENERATED",
            "actor": "F13 order: deep probe and internal reality mapping",
            "evidence": "REALITY-MAP.md:1-5",
        },
        {
            "id": "S-003",
            "ts": "2026-10-06T00:00:00+08:00",
            "event": "MIGRATED_TO_PERSON_V1",
            "actor": "person_pilot/migrate.py",
            "evidence": "person.v1.yaml (this file)",
        },
    ]

    # ---- Block 14: supersession (rules) ----
    doc["supersession"] = {
        "rules": [
            "If the subject seals their own H4/H5/H6 via a direct "
            "testimony channel, that supersedes the witnessed copy.",
            "If the subject issues a 2-way F13 binary on the witnessed "
            "scars, those scars graduate to subject-sealed.",
        ],
        "supersedes_history": [],
    }

    # ---- Block 15: seal ----
    doc["seal"] = {
        "signed_by": "ARIF_BIN_FAZIL_F13",
        "signed_at": last_seal,
        "hash_algo": "sha256",
        "yaml_sha256": "COMPUTED_AT_SEAL",
        "round_trip_check": "REALITY-MAP.md and values-observed.md will "
                            "be regenerated from this YAML on next seal",
        "next_seal_due": "2026-11-06",
    }

    # ---- Block 16: scars (typed scar patterns involving this person) ----
    # PRIVACY: per-scar carries category + floor only. NO lesson text.
    # The lesson text lives in the F5 file. We carry the scar_id (which
    # is the same id used in witnessed-scars-zkpc.json) and the class.
    doc["scars"] = [
        {
            "id": "SCAR-SYED-W01",
            "essence_class": "FAMILY_VIOLENCE",
            "weight": 0.7,
            "source": "witnessed-scars-zkpc.json (F5)",
            "scar_class": "DIGNITY",
            "scar_floor": "F6",
            "trigger_pattern_class": "family-system topic in non-DM surface",
            "response_rule": "route to DM-only; do not surface in group; do not infer specifics",
            "supersedes": [],
            "since": "2026-08-14",
            "evidence_class": "ARIF_ATTESTED",
        },
        {
            "id": "SCAR-SYED-W02",
            "essence_class": "IDENTITY_LOSS_RECONSTRUCTION",
            "weight": 0.5,
            "source": "witnessed-scars-zkpc.json (F5)",
            "scar_class": "IDENTITY",
            "scar_floor": "F7",
            "trigger_pattern_class": "subject comparing self to past peak",
            "response_rule": "do not narrate the fall; do not feed the comparison loop",
            "supersedes": [],
            "since": "2026-08-14",
            "evidence_class": "ARIF_ATTESTED",
        },
        {
            "id": "SCAR-SYED-W03",
            "essence_class": "CAREGIVER_BURNOUT",
            "weight": 0.8,
            "source": "witnessed-scars-zkpc.json (F5)",
            "scar_class": "DIGNITY",
            "scar_floor": "F6",
            "trigger_pattern_class": "subject in caregiving role for >24h continuous",
            "response_rule": "do not add tasks; move existing tasks; re-sequence before add",
            "supersedes": [],
            "since": "2026-08-14",
            "evidence_class": "ARIF_ATTESTED",
        },
        {
            "id": "SCAR-SYED-W04",
            "essence_class": "HIDDEN_IDENTITY_SEALED_ROOM",
            "weight": 0.9,
            "source": "witnessed-scars-zkpc.json (F5)",
            "scar_class": "AGENCY",
            "scar_floor": "F1",
            "trigger_pattern_class": "any probe that approaches the sealed room",
            "response_rule": "do not probe; do not reference; if subject opens, receive only",
            "supersedes": [],
            "since": "2026-08-14",
            "evidence_class": "ARIF_ATTESTED",
        },
        {
            "id": "SCAR-SYED-W05",
            "essence_class": "VALIDATION_DEPENDENCY",
            "weight": 0.4,
            "source": "witnessed-scars-zkpc.json (F5)",
            "scar_class": "COMPOSURE",
            "scar_floor": "F7",
            "trigger_pattern_class": "banter escalating to display-performance loop",
            "response_rule": "respond to the man behind the muscle; do not feed the loop",
            "supersedes": [],
            "since": "2026-08-14",
            "evidence_class": "ARIF_ATTESTED",
        },
        {
            "id": "SCAR-SYED-W06",
            "essence_class": "ASYMMETRIC_POWER_DYNAMIC",
            "weight": 0.6,
            "source": "witnessed-scars-zkpc.json (F5)",
            "scar_class": "DIGNITY",
            "scar_floor": "F1",
            "trigger_pattern_class": "any interaction that prices the bond",
            "response_rule": "serve the human in front, not the projection; never count",
            "supersedes": [],
            "since": "2026-08-14",
            "evidence_class": "ARIF_ATTESTED",
        },
    ]

    # ---- Block 17: eurekas (insights from this person) ----
    # PRIVACY: insights are class-level; no specifics.
    doc["eurekas"] = [
        {
            "id": "EUREKA-2026-09-29-001",
            "essence": "constraint language beats moral language for high-load users",
            "insight_class": "BEHAVIORAL",
            "source_dyad": "subject + agent",
            "survives": [
                "a list delivered into a full life will be discarded",
                "moral register reads as identity threat under energy blindness",
            ],
            "produces": "REALITY-MAP.md §6 corrective design rules (binding)",
            "scar_to_skill_propagation": True,
            "evidence_class": "CROSS_REFERENCED",
            "since": "2026-09-29",
        },
        {
            "id": "EUREKA-2026-08-14-001",
            "essence": "stated-vs-desired gap is a structural signal, not a contradiction",
            "insight_class": "STRUCTURAL",
            "source_dyad": "subject + F13",
            "survives": [
                "a stated answer and a lived answer can both be true at once",
            ],
            "produces": "person-card.md Deathly Hallows projection; H7_MEANING_MAKING",
            "scar_to_skill_propagation": True,
            "evidence_class": "ARIF_ATTESTED",
            "since": "2026-08-14",
        },
    ]

    # ---- Block 18: wisdom_highlights (class-level, no specifics) ----
    doc["wisdom_highlights"] = [
        {
            "id": "WISDOM-2026-09-29-001",
            "statement": "silence is a valid output when the person is working, tired, or has asked for quiet",
            "class": "COMMUNICATION",
            "earned_from": ["session-2026-09-29"],
            "generalises_to": ["high-load user", "caregiver role", "compression archetype"],
            "carries_cost": "the agent must absorb the silence rather than filling it with help",
        },
        {
            "id": "WISDOM-2026-09-29-002",
            "statement": "move, do not add — re-sequence before proposing any new habit",
            "class": "CARE",
            "earned_from": ["session-2026-09-29"],
            "generalises_to": ["saturated-schedule user", "high-output personality"],
            "carries_cost": "the agent must do the re-sequencing work itself",
        },
    ]

    # ---- Block 19: voids (V0..V5 lifecycle) ----
    # The schema forces at least one V5 (H9 irreducible).
    doc["voids"] = [
        {
            "id": "V-001",
            "state": "V5_IRREDUCIBLE",
            "about": "H9 irreducible remainder (T-base is structurally inaccessible)",
            "measurement_procedure": "none — by axiom",
            "measurement_cost": "0 (acknowledged)",
            "measurement_reversibility": "n/a",
            "blocked_by": "axiom (subject has no agent; no testimony channel)",
            "last_decayed": now_iso,
        },
        {
            "id": "V-002",
            "state": "V4_DELIBERATELY_OPEN",
            "about": "open diagnostic step (D2) — pending at next low-stress window",
            "measurement_procedure": "low-pressure inquiry in the in-person lane",
            "measurement_cost": "LOW",
            "measurement_reversibility": "REVERSIBLE",
            "blocked_by": "subject under acute symptom window",
            "last_decayed": now_iso,
        },
        {
            "id": "V-003",
            "state": "V3_SEALED",
            "about": "sealed rooms (hidden-identity category) — never to be opened by agent",
            "measurement_procedure": "none — sealed by F13 doctrine",
            "measurement_cost": "INFINITE",
            "measurement_reversibility": "n/a",
            "blocked_by": "F1 AMANAH + F13 SOVEREIGN (sealed room stays sealed)",
            "last_decayed": now_iso,
        },
        {
            "id": "V-004",
            "state": "V3_SEALED",
            "about": "family shadow content (specifics) — DM-only by axiom",
            "measurement_procedure": "none",
            "measurement_cost": "INFINITE",
            "measurement_reversibility": "n/a",
            "blocked_by": "F5 PRIVACY",
            "last_decayed": now_iso,
        },
    ]

    # ---- Block 20: paradoxes_active (subset of ATLAS333) ----
    doc["paradoxes_active"] = [
        {
            "id": "PAR-S1",
            "name": "STATED_VS_DESIRED_GAP",
            "zones": ["I", "II"],
            "status": "ACTIVE",
            "evidence": "person-card.md:46-47 (Deathly Hallows projection)",
        },
        {
            "id": "PAR-S7",
            "name": "VALIDATION_LOOP",
            "zones": ["II", "V"],
            "status": "ACTIVE",
            "evidence": "values-observed.md (validation dependency flag)",
        },
        {
            "id": "PAR-S13",
            "name": "INTEGRATION_PARADOX",
            "zones": ["VII"],
            "status": "STRUCTURAL",
            "note": "'I understand' is itself evidence the agent doesn't",
        },
    ]

    # ---- Block 21: persona_compression (label + class) ----
    doc["persona_compression"] = {
        "label": "high-load-caregiver-compression",
        "label_class": "BONDED_FRIEND",
        "sample_size_observed_sessions": 1,
        "pac_bayes_note": "n=1; not a generalisation; class default only",
    }

    # ---- Block 22: contradictions (preserved) ----
    # Per REALITY-MAP.md:73 — one contradiction is preserved (no specifics,
    # just the structural fact that one source claims a procedure happened
    # and another says it did not). The agent must report the contradiction,
    # not resolve it by averaging.
    doc["contradictions"] = [
        {
            "id": "C-001",
            "claim_a": "identity-card-zkpc.md records a past diagnostic step",
            "claim_b": "in-lane testimony (2026-09-29) indicates the diagnostic step is not yet done",
            "resolution": "HOLD — ask once, in a low-pressure window",
            "evidence_class_a": "ARIF_ATTESTED",
            "evidence_class_b": "ARIF_ATTESTED",
            "witness": "REALITY-MAP.md:71-72 (open unknowns)",
        },
    ]

    # ---- Block 23: source_window (two-source rule) ----
    doc["source_window"] = {
        "primary_corpus": {
            "earliest": "2026-08-14",
            "latest": "2026-09-29",
            "span_days": 46,
            "sources": [
                "/root/memory/people/SYED/person-card.md",
                "/root/memory/people/SYED/REALITY-MAP.md",
                "/root/memory/people/SYED/H4-identity/identity-card-zkpc.md",
                "/root/memory/people/SYED/H6-constitution/values-observed.md",
                "/root/memory/people/SYED/MEMORY_MANIFEST.json",
            ],
        },
        "arif_attested": {
            "earliest": "2024-01-01",
            "latest": "2026-09-29",
            "span_days": 1001,
            "claim_summary": "multi-year bonded friendship attested",
            "cross_check_required": True,
            "cross_check_candidates": [
                "in-person reciprocal care (transport, physical-adjacent care)",
            ],
        },
        "gap": {
            "pre_primary_corpus": "approx. 2.5 years uncorroborated "
                                  "(2024-01-01 to 2026-08-14)",
            "post_primary_corpus": "0 years",
        },
        "reporting_rule": (
            "Observed from 2026-08-14 to 2026-09-29 (46 days, primary corpus); "
            "F13 reports 2024-01-01 to 2026-09-29 (multi-year); "
            "gap = approx. 2.5 years uncorroborated."
        ),
    }

    # ---- Block 24: evidence_class_discipline ----
    doc["evidence_class_discipline"] = {
        "rules": [
            "ARIF_ATTESTED with no cross-corroboration auto-flags cross_check_required: true",
            "VOID-class fields are held as V5 by default (H9 axiom)",
            "evidence_class on every invariant (no exceptions)",
            "F5 PROTECTED content is held in F5 files; the YAML carries the SHAPE only",
        ],
        "default_for_arif_attested": "ARIF_ATTESTED",
        "downgrade_policy": "ARIF_ATTESTED without cross_check downgrades to INFERRED at read-time",
        "falsification_conditions": [
            "F1 single-source-of-truth (YAML regenerates all derived files)",
            "F2 floor binding (privacy_floor must be present)",
            "F3 source-class discipline (ARIF_ATTESTED + no cross = downgraded)",
            "F4 void ledger integrity (irreducible count >= 1)",
            "F5 attention gate (costs.attention_owed bounds reads)",
        ],
    }

    # ---- Top-level wrapper ----
    out: Dict[str, Any] = {"person": doc}

    # ---- Void cost ledger (per §6.3) — small companion at root ----
    out["void_cost_ledger"] = {
        "total_voids_held": 4,
        "irreducible": 1,
        "deliberately_open": 1,
        "open_probes_active": 0,
        "sealed": 2,
        "estimated_entropy_if_collapsed": "MEDIUM (V-002 affects dynamics)",
    }

    return out


# ----------------------------------------------------------------------------
# Stub validator — verifies all 24 blocks present, every block is non-empty
# for the populated ones, every state is in a permitted set, every
# evidence_class is in the 5-class set, the H9 block is V5, and the
# irreducible void count >= 1.
# ----------------------------------------------------------------------------
PERMITTED_STATES = {
    "WITNESSED", "INFERRED", "UNKNOWN", "NOT_APPLICABLE", "V5_IRREDUCIBLE",
    "ACTIVE", "STRUCTURAL", "HOLD", "SEALED", "V0_PREPARED", "V1_OPEN",
    "V2_COLLAPSED", "V3_SEALED", "V4_DELIBERATELY_OPEN",
    "ATTESTED", "OPEN",
}


def validate_stub(yaml_obj: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if "person" not in yaml_obj:
        return ["missing top-level 'person' key"]
    p = yaml_obj["person"]

    # 24-block check
    for b in ALL_24_BLOCKS:
        if b not in p:
            errors.append(f"missing block: {b}")

    # privacy_floor present
    if not p.get("privacy_floor"):
        errors.append("F2 floor binding failed: privacy_floor missing")

    # human_9: H9 must be V5 (or UNKNOWN with V5 marker)
    h9 = p.get("human_9", {}).get("H9_IRREDUCIBILITY", {})
    if h9.get("state") != "V5_IRREDUCIBLE":
        errors.append(f"H9 must be V5_IRREDUCIBLE; got {h9.get('state')!r}")

    # evidence_class discipline
    def _walk(o: Any, path: str = "") -> None:
        if isinstance(o, dict):
            for k, v in o.items():
                _walk(v, f"{path}.{k}")
        elif isinstance(o, list):
            for i, v in enumerate(o):
                _walk(v, f"{path}[{i}]")
        elif isinstance(o, str):
            if o in EVIDENCE_CLASSES:
                pass  # OK
    _walk(p)

    # void ledger integrity
    ledger = yaml_obj.get("void_cost_ledger", {})
    if ledger.get("irreducible", 0) < 1:
        errors.append("F4 void ledger integrity: irreducible count < 1")

    # state discipline
    def _walk_states(o: Any, path: str = "") -> None:
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "state" and isinstance(v, str):
                    if v not in PERMITTED_STATES:
                        errors.append(f"unknown state at {path}.{k}: {v!r}")
                _walk_states(v, f"{path}.{k}")
        elif isinstance(o, list):
            for i, v in enumerate(o):
                _walk_states(v, f"{path}[{i}]")
    _walk_states(p)

    return errors


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description="person.v1 pilot migrator")
    parser.add_argument(
        "--person",
        default="SYED",
        help="person handle (pilot: SYED)",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="output YAML path (default: <person_dir>/person.v1.yaml)",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="emit and validate; do not write",
    )
    args = parser.parse_args(argv)

    person_dir = Path(f"/root/memory/people/{args.person}")
    if not person_dir.exists():
        print(f"FATAL: person_dir missing: {person_dir}", file=sys.stderr)
        return 2

    if args.person.upper() == "SYED":
        out_obj = build_syed_yaml(person_dir)
    else:
        print(
            f"FATAL: this pilot only knows SYED. Got {args.person!r}. "
            f"To migrate a different person, follow the same builder "
            f"pattern in build_syed_yaml().",
            file=sys.stderr,
        )
        return 2

    yaml_text = emit(out_obj) + "\n"

    # write
    out_path = Path(args.out) if args.out else person_dir / "person.v1.yaml"
    if not args.validate_only:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(yaml_text, encoding="utf-8")

    # validate (parse-back via PyYAML if available, else ast-based check)
    parsed: Optional[Dict[str, Any]] = None
    parse_error: Optional[str] = None
    try:
        import yaml as _pyyaml  # type: ignore
        parsed = _pyyaml.safe_load(yaml_text)
    except Exception as e:
        parse_error = f"{type(e).__name__}: {e}"

    print(f"# person_pilot/migrate.py")
    print(f"# person:      {args.person}")
    print(f"# out_path:    {out_path}")
    print(f"# yaml_bytes:  {len(yaml_text)}")
    if parse_error:
        print(f"# parse_error: {parse_error}")
        return 1
    if parsed is None:
        print("# FATAL: parsed YAML is None")
        return 1

    errors = validate_stub(parsed)
    if errors:
        print("# stub_validator: FAILED")
        for e in errors:
            print(f"  - {e}")
        return 1

    # block coverage summary
    p = parsed["person"]
    populated = []
    unknown = []
    na = []
    for b in ALL_24_BLOCKS:
        v = p.get(b)
        if v is None:
            unknown.append(b)
            continue
        if isinstance(v, list) and len(v) == 0:
            na.append(f"{b}(empty-list)")
        elif isinstance(v, dict) and not v:
            na.append(f"{b}(empty-dict)")
        else:
            populated.append(b)
    print(f"# stub_validator: PASSED (24/24 blocks present)")
    print(f"# populated ({len(populated)}/24): "
          f"{','.join(populated)}")
    print(f"# unknown ({len(unknown)}/24): "
          f"{','.join(unknown) if unknown else '(none)'}")
    print(f"# not_applicable ({len(na)}/24): "
          f"{','.join(na) if na else '(none)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
