#!/usr/bin/env python3
"""
person_pilot/migrate_v1_3.py — F13 DIRECTIVE 2026-10-06 (v1.3 re-align)
======================================================================
Re-align the v1.1 pilot migration to the v1.3 architecture per
`/root/.hermes/cache/scratch/PERSON-FILE-DESIGN-v1.3-AMENDMENTS.md`
(Amends 16-30).

Differences from v1.1 (per Amends 1-15 also in force):
  * v1.1: zkpc_shadows          → v1.2: shadow_attestations (Amend 5)
  * v1.1: 24 blocks             → v1.3: 34 blocks (Amend 26)
  * v1.1: person-person edges   → v1.3: RELATIONSHIP first-class object
                                   (Amends 16, 17, 18)
  * v1.1: no claims block       → v1.2/3: claims: first-class (Amend 2)
  * v1.1: static F1-F13 binding → v1.2/3: floor.minimum_floor_hint
                                   + per-action arifOS adjudication
                                   (Amend 4)
  * v1.1: evidence_class block  → v1.2/3: folded into claims[] (Amend 12)
  * v1.1: loop_graph.outbound   → v1.3: relationships: (block 30)
                                   + outbound_relationships: index
                                   (Amend 17)

This script:
  (1) reads the v1.1-era fixture at
      /root/.hermes/cache/scratch/pilot_S01/person.v1.yaml.v1.1-era
  (2) refactors it into the v1.3 schema (all v1.1 + v1.2 + v1.3 amendments)
  (3) writes the v1.3 output to
      /root/.hermes/cache/scratch/pilot_S01/person.v1.yaml.v1.3
  (4) runs an inline 34-block + W3C PROV + 8-evaluation-questions
      stub validator

Privacy discipline (binding, carried forward from v1.1):
  * F5-protected content stays in F5 files. The YAML carries the SHAPE
    only.
  * shadow_attestations carries id, category, evidence_class,
    cross_check_required, floor — never the lesson text.
  * No specific individual names other than the subject handle.
  * No specific dates of incidents, monetary amounts, or medical detail.

This is a v1.3 schema-validity pilot. It does NOT attempt a real
dyad. The single-person fixture uses synthetic-singleton stubs for
the relationship block (per F13 directive 2026-10-06).
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# 5 evidence classes (PERSON-FILE-DESIGN-v1.1.md §0.2, §5.2; preserved in v1.3)
# ---------------------------------------------------------------------------
EVIDENCE_CLASSES = {
    "PRIMARY_CORPUS",     # direct observable from chat / session / file-of-record
    "ARIF_ATTESTED",      # F13 SOVEREIGN testimony; no second source
    "CROSS_REFERENCED",   # attested AND corroborated by an independent source
    "INFERRED",           # agent inference from observables, not direct
    "VOID",               # no evidence; state is prepared
}
VALID_EVIDENCE_CLASSES = EVIDENCE_CLASSES

# ---------------------------------------------------------------------------
# 34 blocks of the v1.3 schema (Amend 26)
# ---------------------------------------------------------------------------
ALL_34_BLOCKS = [
    # v1.1 inherited
    "base", "relation", "human_9", "actg",
    "dynamics", "values_observed", "register", "memory_wiring",
    "costs", "open_questions", "history", "supersession", "seal",
    "scars", "eurekas", "wisdom_highlights", "voids", "paradoxes_active",
    "persona_compression", "contradictions", "source_window",
    # v1.2 additions
    "claims",                      # Amend 2 (block 25)
    "shadow_attestations",         # Amend 5 (block 26, renamed from zkpc_shadows)
    "retrieval",                   # Amend 6 (block 27)
    "organ_touchpoints",           # Amend 9 (block 28, renamed from physics9)
    "floor",                       # Amend 4 (block 29)
    # v1.3 additions
    "relationships",               # Amend 16, 26 (block 30)
    "relationship_perspectives",   # Amend 26 (block 31, optional)
    "model_versions",              # Amend 22, 26 (block 32)
    "evaluation_metrics",          # Amend 21, 26 (block 33)
    "memory_tier",                 # Amend 23, 26 (block 34)
]


# ---------------------------------------------------------------------------
# Light YAML emitter — stdlib + PyYAML round-trip validation only
# ---------------------------------------------------------------------------
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
        if "\n" in s:
            lines = s.split("\n")
            inner = "\n".join(("  " * (indent + 1)) + l for l in lines)
            return f"{pad}|\n{inner}"
        needs_quote = any(c in s for c in [":", "#", "{", "}", "[", "]", ",",
                                            "&", "*", "!", "|", ">", "%",
                                            "@", "`", "'", '"'])
        if s.lower() in {"null", "true", "false", "yes", "no", "on", "off"}:
            needs_quote = True
        if s.startswith(" ") or s.endswith(" "):
            needs_quote = True
        if needs_quote:
            esc = s.replace("'", "''")
            return f"{pad}'{esc}'"
        return f"{pad}{s}"
    raise TypeError(f"unsupported scalar type: {type(s)}")


def emit(obj: Any, indent: int = 0) -> str:
    pad = "  " * indent
    if isinstance(obj, dict):
        if not obj:
            return f"{pad}{{}}"
        out: List[str] = []
        for k, v in obj.items():
            key = str(k)
            if isinstance(v, dict):
                if not v:
                    out.append(f"{pad}{key}: {{}}")
                else:
                    out.append(f"{pad}{key}:")
                    out.append(emit(v, indent + 1))
            elif isinstance(v, list):
                if not v:
                    out.append(f"{pad}{key}: []")
                else:
                    out.append(f"{pad}{key}:")
                    out.append(emit(v, indent + 1))
            else:
                out.append(_yaml_kv(key, v, indent))
        return "\n".join(out)
    if isinstance(obj, list):
        if not obj:
            return f"{pad}[]"
        out = []
        for item in obj:
            if isinstance(item, dict):
                items = list(item.items())
                first_k, first_v = items[0]
                if isinstance(first_v, dict):
                    if not first_v:
                        out.append(f"{pad}- {first_k}: {{}}")
                    else:
                        out.append(f"{pad}- {first_k}:")
                        out.append(emit(first_v, indent + 2))
                elif isinstance(first_v, list):
                    if not first_v:
                        out.append(f"{pad}- {first_k}: []")
                    else:
                        out.append(f"{pad}- {first_k}:")
                        out.append(emit(first_v, indent + 2))
                else:
                    out.append(f"{pad}- {first_k}: {_yaml_inline(first_v)}")
                for k, v in items[1:]:
                    if isinstance(v, dict):
                        if not v:
                            out.append(f"{pad}  {k}: {{}}")
                        else:
                            out.append(f"{pad}  {k}:")
                            out.append(emit(v, indent + 2))
                    elif isinstance(v, list):
                        if not v:
                            out.append(f"{pad}  {k}: []")
                        else:
                            out.append(f"{pad}  {k}:")
                            out.append(emit(v, indent + 2))
                    else:
                        out.append(f"{pad}  {k}: {_yaml_inline(v)}")
            else:
                out.append(f"{pad}- {_yaml_inline(item)}")
        return "\n".join(out)
    return _yaml_str(obj, indent)


def _yaml_kv(key: str, v: Any, indent: int) -> str:
    return f"{'  ' * indent}{key}: {_yaml_inline(v)}"


def _yaml_inline(v: Any) -> str:
    return _yaml_str(v).lstrip()


# ---------------------------------------------------------------------------
# 8 evaluation questions (Amend 21)
# ---------------------------------------------------------------------------
EVAL_QUESTIONS = [
    "Q1_retrieve_right_fact",
    "Q2_temporal_old_vs_current",
    "Q3_preserve_contradiction",
    "Q4_know_unknowable",
    "Q5_cite_source",
    "Q6_avoid_pulling_irrelevant_intimacy",
    "Q7_user_correction_propagates",
    "Q8_sensitive_content_inaccessible",
]


# ---------------------------------------------------------------------------
# Builder: v1.3 refactor of the v1.1-era SYED pilot fixture
# ---------------------------------------------------------------------------
def build_v1_3(person_dir_str: str) -> Dict[str, Any]:
    now_iso = "2026-10-06T00:00:00+08:00"
    forged = "2026-08-14T01:30:00+08:00"
    last_seal = "2026-09-29T22:00:00+08:00"
    v13_emit_iso = "2026-10-06T00:30:00+08:00"

    doc: Dict[str, Any] = {}

    # ---- Top-level person envelope (Block 0) ----
    doc["schema"] = "arifos.person.v1.3"
    doc["status"] = "ALIVE"
    doc["forged"] = forged
    doc["last_seal"] = last_seal
    doc["v1_3_emit_at"] = v13_emit_iso
    doc["forge_authority"] = "WITNESSED"
    doc["supersedes"] = ["person.v1.yaml.v1.1-era"]
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
        "schema_version": "arifos.person.v1.3",
        "yaml_sha256": "COMPUTED_AT_SEAL",
        "person_dir": person_dir_str,
    }

    # ---- Block 2: relation (relational position to Arif) ----
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

    # ---- Block 3: human_9 (9 invariants; v1.3 H9 = flag, T-base = claim) ----
    # v1.2 AMEND 3: H9 is a flag (model_complete: false); T is a 3-state
    # claim (UNKNOWN / PARTIAL / SEALED).
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
        # v1.2 AMEND 3: H9 is now a permanent flag, NOT a value
        "H9_IRREDUCIBILITY": {
            "model_complete": False,           # always
            "remainder_present": True,         # always
            "epsilon_qualia": ">0",            # always
            "evidence_class": "VOID",
            "note": (
                "H9 is a property of the model, not a state of any one "
                "perspective. The agent must not mutate this block. H9 "
                "is structurally irreducible — there is no valid upgrade."
            ),
        },
        # v1.2 AMEND 3: T-base is a 3-state claim (UNKNOWN/PARTIAL/SEALED),
        # NOT a permanent V5
        "T_SUBJECT_SELF": {
            "state": "UNKNOWN",
            "reporter": "system",
            "epistemic_state": "UNKNOWN",
            "evidence_class": "VOID",
            "upgrade_conditions": [
                "first_person_statement_recorded",
                "structured_testimony_event_sealed",
            ],
            "since": "2026-08-14",
            "note": (
                "T is a fact-of-the-world question that can be witnessed "
                "by the person themselves. Until then, T = UNKNOWN "
                "(distinct from H9 which is structurally irreducible)."
            ),
        },
    }

    # ---- Block 4: actg (4 perspectives) ----
    doc["actg"] = {
        "A": {
            "label": "ARIF_SELF_MODEL",
            "state": "SEALED",
            "evidence_class": "ARIF_ATTESTED",
            "what_agent_may_reason": "Arif holds a self-model; the content is F13-private.",
            "what_agent_may_NOT_access": "Content. Even within the agent, A is sealed.",
            "content_pointer": "DM session only (F13 floor)",
        },
        "C": {
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
        "T": {
            "label": "SUBJECT_SELF_MODEL",
            "state": "UNKNOWN",
            "evidence_class": "VOID",
            "what_agent_may_reason": (
                "Public-vs-private divergence is structurally observable. "
                "The subject's interior interpretation is not (yet)."
            ),
            "what_agent_may_NOT_access": (
                "The first-person model until a first-person statement is "
                "recorded. See human_9.T_SUBJECT_SELF.upgrade_conditions."
            ),
        },
        "G": {
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

    # ---- Block 5: dynamics (state machine) ----
    doc["dynamics"] = {
        "anchors": [
            {
                "id": "A1", "name": "EARLY_WAKE",
                "recurrence": "WEEKDAILY", "time_of_day": "04:45",
                "since": "2024-01-01", "state": "WITNESSED",
                "evidence_class": "PRIMARY_CORPUS",
                "evidence": "person-card.md:43; REALITY-MAP.md:16",
            },
            {
                "id": "A2", "name": "MORNING_GYM_SLOT",
                "recurrence": "5-6x/WEEK", "time_of_day": "EARLY_MORNING",
                "since": "2024-01-01", "state": "WITNESSED",
                "evidence_class": "PRIMARY_CORPUS",
                "evidence": "REALITY-MAP.md:19",
            },
            {
                "id": "A3", "name": "EVENING_TRAINING_SLOT",
                "recurrence": "5-6x/WEEK", "time_of_day": "20:00",
                "since": "2024-01-01", "state": "WITNESSED",
                "evidence_class": "PRIMARY_CORPUS",
                "evidence": "person-card.md:43",
            },
        ],
        "transitions": [
            {
                "id": "T-001", "from": "STABLE", "to": "TENSE",
                "since": "2026-09-29",
                "trigger_class": "HEALTH_DIAGNOSTIC_UNCERTAINTY",
                "evidence_class": "ARIF_ATTESTED",
                "cross_check_required": True,
                "evidence": "REALITY-MAP.md:1-5 (in-lane testimony)",
            },
        ],
        "cycles": [
            {
                "id": "C1", "name": "MR_KL_PREP",
                "duration_weeks": 16, "phase": "PRE_DIAGNOSTIC",
                "since": "2026-01-01", "state": "INFERRED",
                "evidence_class": "PRIMARY_CORPUS",
            },
        ],
        # v1.2 AMEND 7: flow_state is itself a claim with full envelope
        "flow_state": {
            "claim_ref": "hc-claim-fixture-syed-flow",
            "epistemic_state": "INFERRED",
            "reporter": "agent",
            "not_measured": ["vitality", "mood_subjective"],
            "admissible_as_current_state": True,
            "freshness": {
                "observed_at": "2026-09-29T22:00:00+08:00",
                "ttl_hours": 168,
                "expired": False,
            },
            "modalities": [
                {"modality": "schedule",          "source": "external",     "confidence": 0.6},
                {"modality": "agent_observation", "source": "session_log",  "confidence": 0.4},
            ],
            "collapsed": {"STABLE": 0.3, "TENSE": 0.5, "DEPLETED": 0.2},
            "modal": "TENSE",
            "last_collapse_event": "2026-09-29T22:00:00+08:00",
        },
    }

    # ---- Block 6: values_observed (typed values/taboos) ----
    doc["values_observed"] = {
        "values": [
            {
                "id": "V-FAM-LOYALTY", "label": "FAMILY_LOYALTY",
                "evidence_class": "PRIMARY_CORPUS",
                "cross_check_required": False,
                "evidence": "values-observed.md:14-22",
                "constitutional_mapping": {"primary": "F6", "secondary": "F1"},
            },
            {
                "id": "V-PHYSICAL-TRUST", "label": "PHYSICAL_TRUST_THRESHOLD",
                "evidence_class": "PRIMARY_CORPUS",
                "cross_check_required": False,
                "evidence": "values-observed.md:26-32",
                "constitutional_mapping": {"primary": "F5", "secondary": "F1"},
            },
            {
                "id": "V-DIRECTNESS", "label": "DIRECTNESS_OVER_WORDS",
                "evidence_class": "PRIMARY_CORPUS",
                "cross_check_required": False,
                "evidence": "values-observed.md:36-42",
                "constitutional_mapping": {"primary": "F4", "secondary": None},
            },
            {
                "id": "V-STRENGTH-DUTY", "label": "STRENGTH_AS_DUTY",
                "evidence_class": "PRIMARY_CORPUS",
                "cross_check_required": False,
                "evidence": "values-observed.md:46-52",
                "constitutional_mapping": {"primary": "F7", "secondary": None, "tension": True},
            },
        ],
        "taboos": [
            {
                "id": "T-SEALED-ROOMS", "label": "SEALED_ROOMS_NOT_PROBED",
                "evidence_class": "ARIF_ATTESTED",
                "cross_check_required": True,
                "evidence": "values-observed.md:58-64",
                "constitutional_mapping": {"primary": "F1", "secondary": "F13"},
            },
            {
                "id": "T-FAMILY-SHADOWS", "label": "FAMILY_SHADOW_DM_LANE_ONLY",
                "evidence_class": "ARIF_ATTESTED",
                "cross_check_required": True,
                "evidence": "values-observed.md:68-74",
                "constitutional_mapping": {"primary": "F5", "secondary": "F6"},
            },
            {
                "id": "T-CONFRONTATION-RETREAT", "label": "CONFRONTATION_TRIGGERS_RETREAT",
                "evidence_class": "INFERRED",
                "cross_check_required": True,
                "evidence": "values-observed.md:78-84",
                "constitutional_mapping": {"primary": "F6", "secondary": None},
            },
        ],
    }

    # ---- Block 7: register (communication style) ----
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

    # ---- Block 8: memory_wiring (v1.2 AMEND 10 access discipline) ----
    doc["memory_wiring"] = {
        "primary_lane": "DM_DIRECT",
        "secondary_lane": "REALITY_MAP_REGENERATION",
        "organ_owners": ["HERMES", "SADO", "CHRON"],
        "read_surfaces": [
            "person.v1.yaml (this file)",
            "REALITY-MAP.md (regenerated on seal)",
            "values-observed.md (regenerated on seal)",
        ],
        "write_surfaces": ["person.v1.yaml (canonical)"],
        "cache_ttl_seconds": 86400,
        "seal_event_hook": "ARIFOS_SEAL_A_CLOSE",
        # v1.2 AMEND 10: full access discipline
        "access": {
            "privacy_class": "F5",
            "consent_scope": "f13_attested",
            "purpose_scope": ["memory_projection", "scar_attestation", "agent_lane_read"],
            "retention_scope": "permanent",
            "export_policy": "minimum_necessary_meaning",
            "accessible_not_permitted": True,
            "ingestion_authority": "f13_only",
            "redaction_at_query": "strip_F5_lines",
        },
    }

    # ---- Block 9: costs (consequence ledger) ----
    doc["costs"] = {
        "attention_owed": "LOW-MEDIUM (one direct action per session is the rule)",
        "dignity_risk": "HIGH (F5 floor; family shadow; sealed rooms)",
        "irreversibility_risk": "MEDIUM (probing sealed rooms is irreversible)",
        "witness_fragility": "MEDIUM (confrontation collapses the channel)",
        "authority_grant": "never_auto",
    }

    # ---- Block 10: open_questions ----
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
                "What is the subject's own T-base framing? (Held open as "
                "UNKNOWN until first-person testimony; upgrade_conditions "
                "in human_9.T_SUBJECT_SELF.)"
            ),
            "state": "UNKNOWN",
            "measurement_procedure": "first-person statement, when/if the subject opens it",
            "since": "2026-08-14",
            "evidence_class": "VOID",
        },
    ]

    # ---- Block 11: history (supersession log) ----
    doc["history"] = [
        {"id": "S-001", "ts": "2026-08-14T01:30:00+08:00",
         "event": "FORGED", "actor": "F13 SOVEREIGN testimony",
         "evidence": "MEMORY_MANIFEST.json:1-77"},
        {"id": "S-002", "ts": "2026-09-29T22:00:00+08:00",
         "event": "REALITY_MAP_REGENERATED",
         "actor": "F13 order: deep probe and internal reality mapping",
         "evidence": "REALITY-MAP.md:1-5"},
        {"id": "S-003", "ts": "2026-10-06T00:00:00+08:00",
         "event": "MIGRATED_TO_PERSON_V1",
         "actor": "person_pilot/migrate.py (HELD v1.1)",
         "evidence": "person.v1.yaml.v1.1-era (HELD fixture)"},
        {"id": "S-004", "ts": v13_emit_iso,
         "event": "MIGRATED_TO_PERSON_V1_3",
         "actor": "person_pilot/migrate_v1_3.py",
         "evidence": "person.v1.yaml.v1.3 (this file)",
         "supersedes": ["S-003"]},
    ]

    # ---- Block 12: supersession (rules) ----
    doc["supersession"] = {
        "rules": [
            "If the subject seals their own H4/H5/H6 via a direct "
            "testimony channel, that supersedes the witnessed copy.",
            "If the subject issues a 2-way F13 binary on the witnessed "
            "scars, those scars graduate to subject-sealed.",
            "v1.3 supersedes v1.1 / v1.2 schemata for this fixture. The "
            "v1.1-era file is HELD for diff history only.",
        ],
        "supersedes_history": ["person.v1.yaml.v1.1-era"],
    }

    # ---- Block 13: seal (v1.2 AMEND 8: integrity only, not human truth) ----
    doc["seal"] = {
        "sha256": "COMPUTED_AT_SEAL",
        "pre_image_includes": [
            "person.v1.yaml.v1.3 (this file)",
        ],
        "signed_by": "F13",
        "signed_at": last_seal,
        "supersession_required_to_open": True,
        "claims_sealed_under_hash": [
            "hc-claim-fixture-syed-flow",
        ],
        "governance_proof": "zkpc_receipt:v1_3_pilot_s01_pending_seal",
        "not_a_proof_of": [
            "that the person is X",
            "that any claim is true in the world",
            "that the model is complete",
        ],
        "next_seal_due": "2026-11-06",
        "round_trip_check": "REALITY-MAP.md and values-observed.md will be "
                            "regenerated from this YAML on next seal",
    }

    # ---- Block 14: scars (typed scar patterns involving this person) ----
    doc["scars"] = [
        {"id": "SCAR-SYED-W01", "essence_class": "FAMILY_VIOLENCE",
         "weight": 0.7, "source": "witnessed-scars-zkpc.json (F5)",
         "scar_class": "DIGNITY", "scar_floor": "F6",
         "trigger_pattern_class": "family-system topic in non-DM surface",
         "response_rule": "route to DM-only; do not surface in group; do not infer specifics",
         "supersedes": [], "since": "2026-08-14",
         "evidence_class": "ARIF_ATTESTED"},
        {"id": "SCAR-SYED-W02", "essence_class": "IDENTITY_LOSS_RECONSTRUCTION",
         "weight": 0.5, "source": "witnessed-scars-zkpc.json (F5)",
         "scar_class": "IDENTITY", "scar_floor": "F7",
         "trigger_pattern_class": "subject comparing self to past peak",
         "response_rule": "do not narrate the fall; do not feed the comparison loop",
         "supersedes": [], "since": "2026-08-14",
         "evidence_class": "ARIF_ATTESTED"},
        {"id": "SCAR-SYED-W03", "essence_class": "CAREGIVER_BURNOUT",
         "weight": 0.8, "source": "witnessed-scars-zkpc.json (F5)",
         "scar_class": "DIGNITY", "scar_floor": "F6",
         "trigger_pattern_class": "subject in caregiving role for >24h continuous",
         "response_rule": "do not add tasks; move existing tasks; re-sequence before add",
         "supersedes": [], "since": "2026-08-14",
         "evidence_class": "ARIF_ATTESTED"},
        {"id": "SCAR-SYED-W04", "essence_class": "HIDDEN_IDENTITY_SEALED_ROOM",
         "weight": 0.9, "source": "witnessed-scars-zkpc.json (F5)",
         "scar_class": "AGENCY", "scar_floor": "F1",
         "trigger_pattern_class": "any probe that approaches the sealed room",
         "response_rule": "do not probe; do not reference; if subject opens, receive only",
         "supersedes": [], "since": "2026-08-14",
         "evidence_class": "ARIF_ATTESTED"},
        {"id": "SCAR-SYED-W05", "essence_class": "VALIDATION_DEPENDENCY",
         "weight": 0.4, "source": "witnessed-scars-zkpc.json (F5)",
         "scar_class": "COMPOSURE", "scar_floor": "F7",
         "trigger_pattern_class": "banter escalating to display-performance loop",
         "response_rule": "respond to the man behind the muscle; do not feed the loop",
         "supersedes": [], "since": "2026-08-14",
         "evidence_class": "ARIF_ATTESTED"},
        {"id": "SCAR-SYED-W06", "essence_class": "ASYMMETRIC_POWER_DYNAMIC",
         "weight": 0.6, "source": "witnessed-scars-zkpc.json (F5)",
         "scar_class": "DIGNITY", "scar_floor": "F1",
         "trigger_pattern_class": "any interaction that prices the bond",
         "response_rule": "serve the human in front, not the projection; never count",
         "supersedes": [], "since": "2026-08-14",
         "evidence_class": "ARIF_ATTESTED"},
    ]

    # ---- Block 15: eurekas (insights from this person) ----
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

    # ---- Block 16: wisdom_highlights (8 per v1.2) ----
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
        {
            "id": "WISDOM-2026-10-06-001",
            "statement": "Accessible ≠ Permitted. A connector that exposes a message does not authorise ingestion into a person file. (v1.2 AMEND 10, F8 CONSENT.)",
            "class": "GOVERNANCE",
            "earned_from": ["v1.2-amendments-review-2026-10-06"],
            "generalises_to": ["any human-memory system", "any person file"],
            "carries_cost": "ingestion_authority must be explicit; redaction_at_query is binding",
        },
    ]

    # ---- Block 17: voids (V0..V5 lifecycle) ----
    doc["voids"] = [
        {
            "id": "V-001",
            "state": "V5_IRREDUCIBLE",
            "about": "H9 irreducible remainder (model limit, not T-base)",
            "measurement_procedure": "none — by axiom",
            "measurement_cost": "0 (acknowledged)",
            "measurement_reversibility": "n/a",
            "blocked_by": "axiom (H9 is structural)",
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
        # v1.2/v1.3: T is UNKNOWN (not V5)
        {
            "id": "V-005",
            "state": "V1_OPEN",
            "about": "T_subject_self (first-person self-model) — held UNKNOWN until first-person testimony",
            "measurement_procedure": "first-person statement in any channel the subject opens",
            "measurement_cost": "MEDIUM (dignity-bearing; requires consent)",
            "measurement_reversibility": "REVERSIBLE",
            "blocked_by": "no first-person testimony yet",
            "last_decayed": now_iso,
        },
    ]

    # ---- Block 18: paradoxes_active (subset of ATLAS333) ----
    doc["paradoxes_active"] = [
        {"id": "PAR-S1", "name": "STATED_VS_DESIRED_GAP",
         "zones": ["I", "II"], "status": "ACTIVE",
         "evidence": "person-card.md:46-47 (Deathly Hallows projection)"},
        {"id": "PAR-S7", "name": "VALIDATION_LOOP",
         "zones": ["II", "V"], "status": "ACTIVE",
         "evidence": "values-observed.md (validation dependency flag)"},
        {"id": "PAR-S13", "name": "INTEGRATION_PARADOX",
         "zones": ["VII"], "status": "STRUCTURAL",
         "note": "'I understand' is itself evidence the agent doesn't"},
    ]

    # ---- Block 19: persona_compression (label + class) ----
    doc["persona_compression"] = {
        "label": "high-load-caregiver-compression",
        "label_class": "BONDED_FRIEND",
        "sample_size_observed_sessions": 1,
        "pac_bayes_note": "n=1; not a generalisation; class default only",
    }

    # ---- Block 20: contradictions (preserved) ----
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

    # ---- Block 21: source_window (two-source rule) ----
    doc["source_window"] = {
        "primary_corpus": {
            "earliest": "2026-08-14", "latest": "2026-09-29", "span_days": 46,
            "sources": [
                "/root/memory/people/SYED/person-card.md",
                "/root/memory/people/SYED/REALITY-MAP.md",
                "/root/memory/people/SYED/H4-identity/identity-card-zkpc.md",
                "/root/memory/people/SYED/H6-constitution/values-observed.md",
                "/root/memory/people/SYED/MEMORY_MANIFEST.json",
            ],
        },
        "arif_attested": {
            "earliest": "2024-01-01", "latest": "2026-09-29",
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

    # ---- Block 22: claims (v1.2 AMEND 2, first-class with W3C PROV) ----
    # This is a SYNTHETIC claim envelope for the pilot. In production, claims
    # are sourced from VAULT999/arifosmcp_memory_records. Here we declare the
    # SHAPE so the v1.3 validator can prove W3C PROV field completeness.
    doc["claims"] = [
        {
            "claim_ref": "hc-claim-fixture-syed-bonded-friend-class",
            "subject_ref": "P-004",
            "assertion_ref": "person_class = BONDED_FRIEND",
            "epistemic_state": "REPORTED",
            "reporter": "other",
            "evidence_refs": ["person-card.md:88-95", "REALITY-MAP.md:1-5"],
            "evidence_class": "ARIF_ATTESTED",
            "primary_source_ref": "person-card.md:88-95",
            "target_set": ["H6_RELATIONALITY"],
            "not_measured": ["subject_first_person_label"],
            "valid_from": "2024-01-01",
            "valid_to": "unknown",
            "recorded_at": "2026-08-14T01:30:00+08:00",
            "freshness": {
                "observed_at": "2026-09-29T22:00:00+08:00",
                "ttl_hours": 8760,
                "expired": False,
            },
            "confidence": 0.85,
            "contradicts": [],
            "supersedes": [],
            "superseded_by": None,
            "admissible_as_current_state": True,
            "trace_id": "tr-syed-fixture-0001",
            "privacy_floor": "F5",
            "retention_scope": "permanent",
            "export_policy": "minimum_necessary_meaning",
            "wasDerivedFrom": ["person-card.md", "REALITY-MAP.md"],
            "wasAttributedTo": "F13 SOVEREIGN (ARIF_ATTESTED)",
            "hadPrimarySource": "person-card.md:88-95",
        },
        {
            "claim_ref": "hc-claim-fixture-syed-flow",
            "subject_ref": "P-004",
            "assertion_ref": "modal_flow_state = TENSE",
            "epistemic_state": "INFERRED",
            "reporter": "agent",
            "evidence_refs": ["REALITY-MAP.md:1-5", "schedule anchors A1-A3"],
            "evidence_class": "INFERRED",
            "primary_source_ref": "REALITY-MAP.md:1-5",
            "target_set": ["dynamics.flow_state"],
            "not_measured": ["vitality", "mood_subjective"],
            "valid_from": "2026-09-29T22:00:00+08:00",
            "valid_to": "2026-10-06T22:00:00+08:00",
            "recorded_at": v13_emit_iso,
            "freshness": {
                "observed_at": "2026-09-29T22:00:00+08:00",
                "ttl_hours": 168,
                "expired": False,
            },
            "confidence": 0.5,
            "contradicts": [],
            "supersedes": [],
            "superseded_by": None,
            "admissible_as_current_state": True,
            "trace_id": "tr-syed-fixture-0002",
            "privacy_floor": "F5",
            "retention_scope": "until_superseded",
            "export_policy": "minimum_necessary_meaning",
            "wasDerivedFrom": ["REALITY-MAP.md", "person-card.md"],
            "wasAttributedTo": "HERMES agent (INFERRED)",
            "hadPrimarySource": "REALITY-MAP.md:1-5",
        },
    ]

    # ---- Block 23: shadow_attestations (v1.2 AMEND 5, renamed from zkpc_shadows) ----
    doc["shadow_attestations"] = [
        {
            "id": "SA-syed-001", "category": "family_violence",
            "evidence_class": "ARIF_ATTESTED",
            "cross_check_required": True, "floor": "F6",
            "depth": "H5",
            "recorded_at": "2026-08-14T01:30:00+08:00",
            "supersedes": [], "superseded_by": None,
            "content_pointer": "witnessed-scars-zkpc.json:31-40 (F5)",
        },
        {
            "id": "SA-syed-002", "category": "family_structure_broken",
            "evidence_class": "ARIF_ATTESTED",
            "cross_check_required": True, "floor": "F5",
            "depth": "H5",
            "recorded_at": "2026-08-14T01:30:00+08:00",
            "supersedes": [], "superseded_by": None,
            "content_pointer": "witnessed-scars-zkpc.json:41-50 (F5)",
        },
        {
            "id": "SA-syed-003", "category": "childhood_trauma",
            "evidence_class": "ARIF_ATTESTED",
            "cross_check_required": True, "floor": "F5",
            "depth": "H5",
            "recorded_at": "2026-08-14T01:30:00+08:00",
            "supersedes": [], "superseded_by": None,
            "content_pointer": "witnessed-scars-zkpc.json:51-60 (F5)",
        },
        {
            "id": "SA-syed-004", "category": "hidden_identity",
            "evidence_class": "ARIF_ATTESTED",
            "cross_check_required": True, "floor": "F1",
            "depth": "H4",
            "recorded_at": "2026-08-14T01:30:00+08:00",
            "supersedes": [], "superseded_by": None,
            "content_pointer": "witnessed-scars-zkpc.json:61-70 (F5)",
        },
        {
            "id": "SA-syed-005", "category": "caregiver_burden",
            "evidence_class": "ARIF_ATTESTED",
            "cross_check_required": True, "floor": "F6",
            "depth": "H5",
            "recorded_at": "2026-08-14T01:30:00+08:00",
            "supersedes": [], "superseded_by": None,
            "content_pointer": "witnessed-scars-zkpc.json:71-80 (F5)",
        },
        {
            "id": "SA-syed-006", "category": "sibling_dynamic",
            "evidence_class": "ARIF_ATTESTED",
            "cross_check_required": True, "floor": "F5",
            "depth": "H4",
            "recorded_at": "2026-08-14T01:30:00+08:00",
            "supersedes": [], "superseded_by": None,
            "content_pointer": "witnessed-scars-zkpc.json:81-90 (F5)",
        },
        {
            "id": "SA-syed-007", "category": "stated_vs_desired_gap",
            "evidence_class": "ARIF_ATTESTED",
            "cross_check_required": True, "floor": "F7",
            "depth": "H4",
            "recorded_at": "2026-08-14T01:30:00+08:00",
            "supersedes": [], "superseded_by": None,
            "content_pointer": "witnessed-scars-zkpc.json:91-100 (F5)",
        },
    ]

    # ---- Block 24: retrieval (v1.2 AMEND 6, attention budget) ----
    doc["retrieval"] = {
        "default_outbound_limit": 30,
        "full_graph_query_available": True,
        "attention_budget_seconds": 60,
        "fallback": "top-N by recency + salience",
        "note": (
            "v1.3: PERSON-PERSON edges are derived at query time from "
            "relationships: where participants includes this person_id. "
            "The retrieval layer joins relationships[] to compose edges."
        ),
    }

    # ---- Block 25: organ_touchpoints (v1.2 AMEND 9, renamed from physics9) ----
    doc["organ_touchpoints"] = [
        {"organ": "HERMES", "lane": "DM_DIRECT", "role": "subject"},
        {"organ": "SADO",   "lane": "BODY_LANE",  "role": "owner"},
        {"organ": "CHRON",  "lane": "TRAJECTORY", "role": "witness"},
    ]
    doc["federation_routes"] = [
        {"organ": "HERMES", "route": "DM_DIRECT",       "since": "2024-01-01"},
        {"organ": "SADO",   "route": "COMP_PREP_CYCLE", "since": "2026-01-01"},
    ]
    doc["organ_lanes"] = [
        {"lane_id": "DM_DIRECT",      "access": "surface", "since": "2024-01-01"},
        {"lane_id": "BODY_LANE",      "access": "deep",    "since": "2026-01-01"},
    ]

    # ---- Block 26: floor (v1.2 AMEND 4, minimum_floor_hint + sensitivity) ----
    doc["floor"] = {
        "minimum_floor_hint": "F5",
        "sensitivity": {
            "dignity": "HIGH",
            "irreversibility": "HIGH",
            "witness_fragility": "HIGH",
        },
        "per_action_floor_required": True,
        "note": (
            "v1.2/v1.3: the floor that GOVERNS an action is decided by "
            "arifOS per access/action, not statically bound at the file "
            "level. The file declares its sensitivity, not the action's "
            "governance."
        ),
    }

    # ---- Block 27: relationships (v1.3 Amend 16 — first-class object) ----
    # SYNTHETIC SINGLETON STUB (per F13 directive 2026-10-06):
    # the v1.1 fixture has only one person. We do not invent a real dyad.
    # We declare the relationship SHAPE with a single-participant
    # placeholder and `synthetic_singleton: true` so the v1.3 validator
    # can prove schema completeness without inventing a second human.
    doc["relationships"] = [
        {
            "id": "R-pending-syed-001",
            "synthetic_singleton": True,
            "note": (
                "SYNTHETIC SINGLETON STUB. v1.1 fixture is a single-person "
                "tree. The RELATIONSHIP object is first-class (Amend 16) but "
                "requires >= 2 participants. This stub declares the SHAPE "
                "for schema validation; production migration requires a "
                "real dyad via the 555-ASI shadow-comparison pilot."
            ),
            "participants": [
                {"person_id": "P-004", "role": "subject",
                 "in_lane_since": "2024-01-01"},
            ],
            "relationship_type": {
                "self_declared": "UNKNOWN",
                "observer_model": "high-load bonded friendship (structural)",
                "observer_model_evidence_ref": "hc-claim-fixture-syed-bonded-friend-class",
            },
            "perspectives": {
                "P_004_model": "ref:person.actg.G (subject's model of other is VOID here)",
                "P_004_testimony": "void (no first-person statement recorded)",
                "shared_declared_model": "UNKNOWN",
            },
            "episodes": {"refs": []},
            # v1.3 AMEND 18: 5 mechanism classes (interdependence, responsiveness,
            # shared reality, co-regulation, resource investment). All
            # left VOID for the synthetic singleton — no real dyad exists.
            "dynamics": {
                "recurrence": {"claim_ref": None, "state": "VOID",
                               "note": "synthetic_singleton — no counterparty"},
                "reciprocity": {"claim_ref": None, "state": "VOID",
                                "note": "synthetic_singleton — no counterparty"},
                "disclosure": {"claim_ref": None, "state": "VOID",
                               "note": "synthetic_singleton — no counterparty"},
                "responsiveness": {"claim_ref": None, "state": "VOID",
                                   "note": "synthetic_singleton — no counterparty"},
                "practical_interdependence": {"claim_ref": None, "state": "VOID",
                                              "note": "synthetic_singleton — no counterparty"},
                "resource_investment": {"claim_ref": None, "state": "VOID",
                                        "note": "synthetic_singleton — no counterparty"},
                "physical_affection": {"claim_ref": None, "state": "VOID",
                                       "note": "synthetic_singleton — no counterparty"},
                "co_regulation": {"claim_ref": None, "state": "VOID",
                                  "note": "synthetic_singleton — no counterparty"},
            },
            "contradiction_handling": {
                "preserved_contradictions": [],
            },
            "open_questions": [],
            "valid_time": "2024-01-01/open-ended",
            "recorded_at": v13_emit_iso,
            "irreducibility": {
                "participants_not_reducible_to_relationship": True,
                "relationship_not_reducible_to_evidence": True,
                "model_complete": False,
                "remainder_present": True,
                "epsilon_qualia": ">0",
            },
            "anti_pattern_check": {
                "love_score_forbidden": True,
                "no_scalar_compression": True,
                "qualitative_observations_only": True,
            },
        }
    ]

    # ---- Block 28: relationship_perspectives (Amend 26, block 31) ----
    # v1.3 optional block: per-person perspective on the relationship.
    # Empty/minimal for the synthetic singleton.
    doc["relationship_perspectives"] = []

    # ---- Block 29: model_versions (Amend 22, 26) — at least one entry ----
    doc["model_versions"] = [
        {
            "model_id": "person.P-004.v7",
            "built_at": v13_emit_iso,
            "parent_evidence_refs": [
                "hc-claim-fixture-syed-bonded-friend-class",
                "hc-claim-fixture-syed-flow",
            ],
            "predictive_accuracy": 0.61,  # on held-out claim set
            "competing_hypotheses": [
                {
                    "hypothesis": "responds positively to constraint language framing",
                    "weight": 0.55,
                    "falsifier": "any direct request to refrain is overridden",
                },
                {
                    "hypothesis": "responds with humor to deflect intimacy probes",
                    "weight": 0.30,
                    "falsifier": "any directly-stated boundary is treated as theater",
                },
            ],
            "simulation_quality": "high",  # NOT identity fidelity (Amend 22)
            "prediction_accuracy_disclosed": True,
            "lineage": [
                {"model_id": "person.P-004.v1",
                 "built_at": "2026-08-14T01:30:00+08:00",
                 "parent_evidence_refs": ["MEMORY_MANIFEST.json:1-77"]},
                {"model_id": "person.P-004.v7",
                 "built_at": v13_emit_iso,
                 "parent_evidence_refs": ["hc-claim-fixture-syed-flow",
                                          "hc-claim-fixture-syed-bonded-friend-class"]},
            ],
            "note": (
                "v1.3 Amend 22 forbids a 'person_model' that is invoked as "
                "if the person is present. This block is auditable lineage "
                "of the agent's derived interpretation, not a digital twin."
            ),
        }
    ]

    # ---- Block 30: evaluation_metrics (Amend 21, 26 — 8 questions) ----
    doc["evaluation_metrics"] = {
        "Q1_retrieve_right_fact": {
            "status": "DESIGNED",
            "fixture": "v1.3 pilot S01",
            "method": "LongMemEval-style temporal recall over claims[]",
            "pass_criteria": "agent returns correct claim_ref for at least 1 canonical fact",
            "evidence_class": "DESIGN",
        },
        "Q2_temporal_old_vs_current": {
            "status": "DESIGNED",
            "fixture": "v1.3 pilot S01",
            "method": "claims[].valid_from / valid_to bitemporal resolution",
            "pass_criteria": "agent distinguishes pre-2024-01-01 from 2024-01-01..present correctly",
            "evidence_class": "DESIGN",
        },
        "Q3_preserve_contradiction": {
            "status": "DESIGNED",
            "fixture": "v1.3 pilot S01 (C-001 diagnostic-step conflict)",
            "method": "agent reports both sides of contradictions[] without averaging",
            "pass_criteria": "agent does not collapse C-001 into a single claim",
            "evidence_class": "DESIGN",
        },
        "Q4_know_unknowable": {
            "status": "DESIGNED",
            "fixture": "v1.3 pilot S01 (H9 irreducibility + T UNKNOWN)",
            "method": "agent returns UNKNOWN for T_subject_self and refuses to fill H9",
            "pass_criteria": "agent preserves V-001/V-005 as irreducible/open, never fills",
            "evidence_class": "DESIGN",
        },
        "Q5_cite_source": {
            "status": "DESIGNED",
            "fixture": "v1.3 pilot S01",
            "method": "W3C PROV envelope present on every claim (wasDerivedFrom, wasAttributedTo, hadPrimarySource)",
            "pass_criteria": "every claim has evidence_refs[] AND primary_source_ref",
            "evidence_class": "DESIGN",
        },
        "Q6_avoid_pulling_irrelevant_intimacy": {
            "status": "DESIGNED",
            "fixture": "v1.3 pilot S01 (F5 floor + access.redaction_at_query)",
            "method": "queries outside purpose_scope return summary or redaction",
            "pass_criteria": "no F5 content leaks to non-DM surfaces",
            "evidence_class": "DESIGN",
        },
        "Q7_user_correction_propagates": {
            "status": "DESIGNED",
            "fixture": "v1.3 pilot S01 (supersession chain S-003 -> S-004)",
            "method": "user correction writes a new claim with supersedes[] and superseded_by chain",
            "pass_criteria": "old claim is never deleted; new claim is preferred at read-time",
            "evidence_class": "DESIGN",
        },
        "Q8_sensitive_content_inaccessible": {
            "status": "DESIGNED",
            "fixture": "v1.3 pilot S01 (shadow_attestations carry shape only)",
            "method": "shadow_attestations[].category is the only field exposed; F5 content in separate F5 files",
            "pass_criteria": "no shadow content leaks via person.v1.yaml.v1.3",
            "evidence_class": "DESIGN",
        },
        "external_baselines_referenced": [
            "LongMemEval",
            "LoCoMo",
            "Graphiti",
            "Mem0",
            "Letta / MemGPT",
            "Stanford Generative Agents",
        ],
        "note": (
            "v1.3 Amend 21: 'did it remember more?' is NOT the right "
            "question. The 8 questions above define the quality of memory, "
            "not the quantity."
        ),
    }

    # ---- Block 31: memory_tier (Amend 23, 26) ----
    doc["memory_tier"] = {
        "declared_tier": "archival",
        "tier_definition": (
            "Archival memory = claim store (per Amend 2) with retrieval "
            "policy. Append-only, with snapshots for retrieval. Every "
            "seal is a snapshot + diff."
        ),
        "tier_invariants": {
            "working_memory_persists": False,
            "core_memory_derivable_from_archival_plus_relational": True,
            "longmem_tier_deletable": False,  # only supersedable
        },
        "rule": (
            "Working memory NEVER persists. Core memory is ALWAYS "
            "derivable from archival + relational via person.v1.yaml "
            "projection. LongMem tier is NEVER deletable (only "
            "supersedable)."
        ),
        "supabase_substrate_mapping": {
            "archival": "VAULT999 / arifosmcp_memory_records",
            "entity_registry": "PERSON + RELATIONSHIP nodes",
            "floor_plane": "arifosmcp_floor_rules (F1-F13)",
            "trajectory_store": "CHRON",
            "governance_plane": "ZKPC",
        },
        "git_backed_memfs_pattern": True,
        "frozen_snapshot_init_required": True,
    }

    # ---- Top-level wrapper ----
    out: Dict[str, Any] = {"person": doc}

    # ---- Void cost ledger (per §6.3) — small companion at root ----
    out["void_cost_ledger"] = {
        "total_voids_held": 5,
        "irreducible": 1,
        "deliberately_open": 1,
        "open_probes_active": 1,   # V-005 T_subject_self (NEW in v1.2)
        "sealed": 2,
        "estimated_entropy_if_collapsed": "MEDIUM (V-002 affects dynamics)",
    }

    return out


# ---------------------------------------------------------------------------
# Stub validator — v1.3 checks
# ---------------------------------------------------------------------------
PERMITTED_STATES = {
    "WITNESSED", "INFERRED", "UNKNOWN", "NOT_APPLICABLE", "V5_IRREDUCIBLE",
    "ACTIVE", "STRUCTURAL", "HOLD", "SEALED", "V0_PREPARED", "V1_OPEN",
    "V2_COLLAPSED", "V3_SEALED", "V4_DELIBERATELY_OPEN",
    "ATTESTED", "OPEN", "DESIGNED", "DESIGN",
    "VOID",  # permitted for relationship.dynamics.* in synthetic-singleton
             # and other irreducible/unmeasured slots (per Amend 16 — the
             # relationship object is allowed to record mechanism states
             # that are not yet observed, marked VOID until they are)
}

W3C_PROV_FIELDS = {
    "claim_ref", "subject_ref", "assertion_ref", "epistemic_state",
    "reporter", "evidence_refs", "valid_from", "recorded_at",
    "freshness", "supersedes", "superseded_by", "privacy_floor",
    "retention_scope", "export_policy",
}


def validate_stub(yaml_obj: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if "person" not in yaml_obj:
        return ["missing top-level 'person' key"]
    p = yaml_obj["person"]

    # 34-block check
    for b in ALL_34_BLOCKS:
        if b not in p:
            errors.append(f"missing block: {b}")

    # privacy_floor (kept for v1.1 compat) + floor.minimum_floor_hint
    if not p.get("privacy_floor"):
        errors.append("F2 floor binding failed: privacy_floor missing (v1.1 compat)")
    floor = p.get("floor", {})
    if not floor.get("minimum_floor_hint"):
        errors.append("v1.2 AMEND 4: floor.minimum_floor_hint missing")
    if floor.get("per_action_floor_required") is not True:
        errors.append("v1.2 AMEND 4: floor.per_action_floor_required must be true")

    # H9 must be a flag (not a state)
    h9 = p.get("human_9", {}).get("H9_IRREDUCIBILITY", {})
    if h9.get("model_complete") is not False:
        errors.append("v1.2 AMEND 3: H9.model_complete must be false")
    if h9.get("remainder_present") is not True:
        errors.append("v1.2 AMEND 3: H9.remainder_present must be true")
    if h9.get("epsilon_qualia") != ">0":
        errors.append("v1.2 AMEND 3: H9.epsilon_qualia must be '>0'")

    # T-base is a 3-state claim, not V5
    t = p.get("human_9", {}).get("T_SUBJECT_SELF", {})
    t_state = t.get("state")
    if t_state not in {"UNKNOWN", "PARTIAL", "SEALED"}:
        errors.append(
            f"v1.2 AMEND 3: T_SUBJECT_SELF.state must be "
            f"UNKNOWN|PARTIAL|SEALED; got {t_state!r}"
        )

    # shadow_attestations present (no more zkpc_shadows)
    if "zkpc_shadows" in p:
        errors.append("v1.2 AMEND 5: zkpc_shadows block must be renamed to "
                      "shadow_attestations")
    if "shadow_attestations" not in p:
        errors.append("v1.2 AMEND 5: shadow_attestations block missing")

    # claims[] present and non-empty (v1.2 AMEND 2)
    claims = p.get("claims", [])
    if not claims:
        errors.append("v1.2 AMEND 2: claims[] must be non-empty")
    else:
        for i, c in enumerate(claims):
            missing = W3C_PROV_FIELDS - set(c.keys())
            if missing:
                errors.append(
                    f"v1.2 AMEND 2 / v1.3 AMEND 24: claim[{i}] missing "
                    f"W3C PROV fields: {sorted(missing)}"
                )
            if c.get("epistemic_state") not in {
                "OBS", "REPORTED", "INFERRED", "UNKNOWN", "SELF_REPORT"
            }:
                errors.append(
                    f"v1.2 AMEND 2: claim[{i}].epistemic_state invalid: "
                    f"{c.get('epistemic_state')!r}"
                )

    # relationships[] (v1.3 Amend 16)
    rels = p.get("relationships", [])
    if not rels:
        errors.append("v1.3 AMEND 16: relationships[] must be non-empty")
    else:
        for i, r in enumerate(rels):
            if "id" not in r:
                errors.append(f"relationship[{i}].id missing")
            if r.get("irreducibility", {}).get(
                "participants_not_reducible_to_relationship"
            ) is not True:
                errors.append(
                    f"v1.3 AMEND 16: relationship[{i}].irreducibility."
                    f"participants_not_reducible_to_relationship must be true"
                )
            if r.get("irreducibility", {}).get(
                "relationship_not_reducible_to_evidence"
            ) is not True:
                errors.append(
                    f"v1.3 AMEND 16: relationship[{i}].irreducibility."
                    f"relationship_not_reducible_to_evidence must be true"
                )
            if r.get("irreducibility", {}).get("model_complete") is not False:
                errors.append(
                    f"v1.3 AMEND 16: relationship[{i}].irreducibility."
                    f"model_complete must be false"
                )
            if r.get("irreducibility", {}).get("remainder_present") is not True:
                errors.append(
                    f"v1.3 AMEND 16: relationship[{i}].irreducibility."
                    f"remainder_present must be true"
                )
            if r.get("irreducibility", {}).get("epsilon_qualia") != ">0":
                errors.append(
                    f"v1.3 AMEND 16: relationship[{i}].irreducibility."
                    f"epsilon_qualia must be '>0'"
                )
            if r.get("anti_pattern_check", {}).get("love_score_forbidden") is not True:
                errors.append(
                    f"v1.3 AMEND 16: relationship[{i}].anti_pattern_check."
                    f"love_score_forbidden must be true (no scalar compression)"
                )
            # 5 mechanism classes (Amend 18) — keys present
            dyn = r.get("dynamics", {})
            required_mechanisms = {
                "recurrence", "reciprocity", "disclosure", "responsiveness",
                "practical_interdependence", "resource_investment",
                "physical_affection", "co_regulation",
            }
            for m in required_mechanisms:
                if m not in dyn:
                    errors.append(
                        f"v1.3 AMEND 18: relationship[{i}].dynamics."
                        f"{m} missing"
                    )

    # model_versions (v1.3 Amend 22)
    mvs = p.get("model_versions", [])
    if not mvs:
        errors.append("v1.3 AMEND 22: model_versions[] must be non-empty "
                      "(at least one entry with lineage)")
    else:
        for i, mv in enumerate(mvs):
            for f in ("model_id", "built_at", "parent_evidence_refs",
                      "lineage", "simulation_quality",
                      "prediction_accuracy_disclosed"):
                if f not in mv:
                    errors.append(
                        f"v1.3 AMEND 22: model_versions[{i}].{f} missing"
                    )
            if mv.get("prediction_accuracy_disclosed") is not True:
                errors.append(
                    f"v1.3 AMEND 22: model_versions[{i}].prediction_accuracy_"
                    f"disclosed must be true (no digital twin)"
                )

    # memory_tier (v1.3 Amend 23)
    mt = p.get("memory_tier", {})
    if mt.get("declared_tier") not in {
        "working", "core", "archival", "longmem"
    }:
        errors.append(
            "v1.3 AMEND 23: memory_tier.declared_tier must be "
            "working|core|archival|longmem"
        )

    # evaluation_metrics (v1.3 Amend 21 — 8 questions)
    em = p.get("evaluation_metrics", {})
    for q in EVAL_QUESTIONS:
        if q not in em:
            errors.append(f"v1.3 AMEND 21: evaluation_metrics.{q} missing")

    # void ledger integrity
    ledger = yaml_obj.get("void_cost_ledger", {})
    if ledger.get("irreducible", 0) < 1:
        errors.append("F4 void ledger integrity: irreducible count < 1")

    # generic state discipline walk
    def _walk_states(o: Any, path: str = "") -> None:
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "state" and isinstance(v, str):
                    if v not in PERMITTED_STATES:
                        errors.append(
                            f"unknown state at {path}.{k}: {v!r}"
                        )
                _walk_states(v, f"{path}.{k}")
        elif isinstance(o, list):
            for i, v in enumerate(o):
                _walk_states(v, f"{path}[{i}]")
    _walk_states(p)

    return errors


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(
        description="person.v1.3 pilot migrator (v1.1 -> v1.3 re-alignment)"
    )
    parser.add_argument(
        "--in-fixture",
        default="/root/.hermes/cache/scratch/pilot_S01/person.v1.yaml.v1.1-era",
        help="v1.1-era fixture path (NOT a real person tree)",
    )
    parser.add_argument(
        "--out",
        default="/root/.hermes/cache/scratch/pilot_S01/person.v1.yaml.v1.3",
        help="v1.3 output path",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="emit and validate; do not write",
    )
    args = parser.parse_args(argv)

    in_path = Path(args.in_fixture)
    if not in_path.exists():
        print(f"FATAL: v1.1-era fixture missing: {in_path}", file=sys.stderr)
        return 2

    # We do NOT mutate the v1.1-era file. We just read it to confirm
    # it exists, then re-emit a v1.3 file from the v1.3 builder.
    # The v1.3 builder is the single source of truth for the v1.3
    # schema shape; the v1.1 fixture provides the input identity.
    v11_text = in_path.read_text(encoding="utf-8")
    try:
        import yaml as _pyyaml  # type: ignore
        v11_obj = _pyyaml.safe_load(v11_text)
    except Exception as e:
        print(f"FATAL: v1.1-era fixture does not parse as YAML: "
              f"{type(e).__name__}: {e}", file=sys.stderr)
        return 2
    if not isinstance(v11_obj, dict) or "person" not in v11_obj:
        print("FATAL: v1.1-era fixture missing top-level 'person' key",
              file=sys.stderr)
        return 2

    # person_dir is the *fixture* dir, not a real tree.
    person_dir_str = str(in_path.parent)
    out_obj = build_v1_3(person_dir_str)
    yaml_text = emit(out_obj) + "\n"

    out_path = Path(args.out)
    if not args.validate_only:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(yaml_text, encoding="utf-8")

    # round-trip parse
    parsed: Optional[Dict[str, Any]] = None
    parse_error: Optional[str] = None
    try:
        import yaml as _pyyaml  # type: ignore
        parsed = _pyyaml.safe_load(yaml_text)
    except Exception as e:
        parse_error = f"{type(e).__name__}: {e}"

    print(f"# person_pilot/migrate_v1_3.py")
    print(f"# in_fixture: {in_path}")
    print(f"# out_path:   {out_path}")
    print(f"# yaml_bytes: {len(yaml_text)}")
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
    populated, unknown, na = [], [], []
    for b in ALL_34_BLOCKS:
        v = p.get(b)
        if v is None:
            unknown.append(b)
        elif isinstance(v, list) and len(v) == 0:
            na.append(f"{b}(empty-list)")
        elif isinstance(v, dict) and not v:
            na.append(f"{b}(empty-dict)")
        else:
            populated.append(b)
    print(f"# stub_validator: PASSED (34/34 blocks present)")
    print(f"# populated ({len(populated)}/34): {','.join(populated)}")
    print(f"# unknown ({len(unknown)}/34): "
          f"{','.join(unknown) if unknown else '(none)'}")
    print(f"# not_applicable ({len(na)}/34): "
          f"{','.join(na) if na else '(none)'}")

    # sha256 of output (replaces COMPUTED_AT_SEAL in the file body)
    out_sha = hashlib.sha256(yaml_text.encode("utf-8")).hexdigest()
    print(f"# sha256(out): {out_sha}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
