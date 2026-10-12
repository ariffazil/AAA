#!/usr/bin/env python3
"""
person_validate_v1_3.py — Validator for arifos.person.v1.3 (RELATIONSHIP first-class)

Per /root/.hermes/cache/scratch/PERSON-FILE-DESIGN-v1.3-AMENDMENTS.md (Amends 16-30).

Re-aligns /root/AAA/scripts/person_validate/person_validate.py (v1.1, HELD) to the v1.3
architecture. Does NOT overwrite the v1.1 file. This script is a sibling, not a
migration; it enforces the v1.3 amendments as additional, not replacement, checks
on the core v1.1 surface (the v1.1 block list is preserved as a baseline).

v1.3 amendments enforced (per task spec):
  16. RELATIONSHIP is a first-class object (block 30).
      Required fields: participants, perspectives, dynamics
        (recurrence, reciprocity, disclosure, responsiveness,
         practical_interdependence, resource_investment,
         physical_affection, co_regulation),
        irreducibility (4 always-true flags).
  17. loop_graph uses outbound_relationships (not edges). PERSON-PERSON direct
      edges are rejected.
  18. Five mechanism classes are encoded in dynamics.
  22. model_versions (block 32), if present, must carry:
        model_id, parent_evidence_refs, predictive_accuracy,
        competing_hypotheses. Reject if simulation_quality is conflated
        with identity_fidelity.
  23. memory_tier (block 34) must be one of working/core/archival/longmem.
  24. W3C PROV envelope: every claim has subject_ref, evidence_refs,
        valid_from, valid_to, recorded_at, reporter, epistemic_state.
  25. relationship object forbids love_score or any single-scalar
        relationship-quality field.
  26. evaluation_metrics (block 33), if present, must address the 8
        evaluation questions (Amend 21).
  27. irreducibility.model_complete: false, epsilon_qualia: ">0" required
        permanent flag (not optional).

Falsification conditions (5 of 6 from v1.1, deferred per task spec):
  F1 single-source-of-truth (yaml sha = seal.sha256_yaml)
  F2 floor binding (privacy_floor + relation.person_class valid)
  F3 source-class discipline (ARIF_ATTESTED w/o cross_check → downgrade)
  F4 void ledger integrity (≥1 V5_IRREDUCIBLE void)
  F6 paradox-active disclosure
  F5 attention gate is DEFERRED to the retrieval layer (per task spec).

Stdlib + PyYAML only. Fail-closed (any error → exit 1). No derived-file
generation; this is a pure validator. Idempotent: running twice yields the
same verdict.

Usage:
  python3 person_validate_v1_3.py <person.v1.3.yaml>
  python3 person_validate_v1_3.py <person.v1.3.yaml> --json

Output: non-zero exit code + per-error diagnostics on failure; OK summary on
success. JSON mode emits a structured report.
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    print("FATAL: PyYAML is required (install with `pip install pyyaml`).", file=sys.stderr)
    sys.exit(2)


SCHEMA_NAME_V1_3 = "arifos.person.v1.3"

# ---- v1.1 baseline enums (reused for floor binding, evidence class, etc.) ---- #

ALLOWED_FLOORS = {f"F{i}" for i in range(1, 14)}
ALLOWED_PERSON_CLASS = {
    "SOVEREIGN", "FAMILY", "BONDED", "FAMILY_OF_BOND",
    "KERJA", "SERVICE", "STRANGER",
}
ALLOWED_EVIDENCE_CLASS = {
    "PRIMARY_CORPUS", "ARIF_ATTESTED", "CROSS_REFERENCED",
    "INFERRED", "VOID",
}
ALLOWED_INVARIANT_STATES = {"WITNESSED", "INFERRED", "UNKNOWN", "NOT_APPLICABLE"}
ALLOWED_VOID_STATES = {
    "V0_PREPARED", "V1_OPEN", "V2_COLLAPSED", "V3_SEALED",
    "V4_DELIBERATELY_OPEN", "V5_IRREDUCIBLE",
}
ALLOWED_MEMORY_TIER = {"working", "core", "archival", "longmem"}
ALLOWED_EPISTEMIC_STATE = {"OBS", "DER", "INT", "SPEC"}  # W3C PROV hadRole
ALLOWED_REPORTER = {"subject", "other", "agent", "system"}  # W3C PROV Agent
ALLOWED_RELATIONSHIP_TYPE = {
    "UNKNOWN", "PARTNER", "FAMILY", "BONDED_FRIEND", "KIN",
    "ADVERSARY", "PROFESSIONAL", "STRANGER",
}
ALLOWED_EDGE_DIRECTION = {"symmetric", "asymmetric", "unknown"}
ALLOWED_LOOP_NODE_KINDS = {
    "PERSON", "ORGAN", "SCAR", "SESSION", "CHRON",
    "CONSTITUTION", "CONTRACT", "RELATIONSHIP",
}

# Required v1.1 top-level blocks (baseline; v1.3 adds blocks 30-34 as
# additional, not replacement).
REQUIRED_TOP_BLOCKS = {
    "schema", "status", "forged", "last_seal", "forge_authority",
    "supersedes", "privacy_floor", "person_handle", "base", "relation",
    "human_9", "actg", "zkpc_shadows", "dynamics", "loop_graph",
    "values_observed", "register", "memory_wiring", "costs",
    "open_questions", "history", "supersession", "seal", "scars",
    "eurekas", "wisdom_highlights", "voids", "paradoxes_active",
    "persona_compression", "contradictions", "source_window",
    "evidence_class_discipline",
}

# v1.3 block 30: relationships (first-class list of RELATIONSHIP objects)
# v1.3 block 31: relationship_perspectives (optional)
# v1.3 block 32: model_versions (optional)
# v1.3 block 33: evaluation_metrics (optional)
# v1.3 block 34: memory_tier (required — every v1.3 file declares its tier)

RELATIONSHIP_DYNAMICS_KEYS = {
    "recurrence", "reciprocity", "disclosure", "responsiveness",
    "practical_interdependence", "resource_investment",
    "physical_affection", "co_regulation",
}

# Forbidden single-scalar relationship-quality fields (Amend 16 anti-pattern).
FORBIDDEN_RELATIONSHIP_SCALARS = {
    "love_score", "intimacy_score", "closeness_score",
    "trust_score", "relationship_quality", "bond_strength",
}

# Required W3C PROV envelope fields on every claim (Amend 24).
PROV_REQUIRED = (
    "subject_ref", "evidence_refs", "valid_from", "valid_to",
    "recorded_at", "reporter", "epistemic_state",
)

# 8 evaluation questions (Amend 21). block 33 must address each if present.
EVALUATION_QUESTIONS = (
    "retrieve_right_fact",
    "bitemporal_old_vs_current",
    "preserve_contradiction",
    "know_it_does_not_know",
    "cite_source",
    "avoid_irrelevant_intimacy",
    "user_correction_propagates",
    "sensitive_content_inaccessible",
)

ISO_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:?\d{2})?)?$"
)


# ----------------------------- typed dataclasses ---------------------------- #

@dataclass
class ValidationError:
    code: str
    message: str
    block: str = ""
    path: str = ""

    def __str__(self) -> str:  # pragma: no cover
        loc = f"{self.block}/{self.path}" if self.block else self.path
        return f"[{self.code}] {loc}: {self.message}" if loc else f"[{self.code}] {self.message}"


@dataclass
class ValidationReport:
    schema_name: str = SCHEMA_NAME_V1_3
    block_results: Dict[str, str] = field(default_factory=dict)
    errors: List[ValidationError] = field(default_factory=list)
    sha_yaml: str = ""
    falsification_results: Dict[str, str] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not self.errors

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ok": self.ok,
            "schema": self.schema_name,
            "block_results": self.block_results,
            "errors": [
                {
                    "code": e.code, "block": e.block, "path": e.path,
                    "message": e.message,
                }
                for e in self.errors
            ],
            "sha_yaml": self.sha_yaml,
            "falsification_results": self.falsification_results,
        }


# ------------------------------- iso / helpers ----------------------------- #

def _is_iso(value: Any) -> bool:
    return isinstance(value, str) and bool(ISO_RE.match(value))


def _is_str(value: Any) -> bool:
    return isinstance(value, str)


def _is_list_of_str(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(x, str) for x in value)


def _is_list_of_dicts(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(x, dict) for x in value)


def _mapping(obj: Any) -> Dict[str, Any]:
    return obj if isinstance(obj, dict) else {}


def _sequence(obj: Any) -> List[Any]:
    return obj if isinstance(obj, list) else []


# ------------------------------- block validators --------------------------- #

def _check_schema(person: Dict[str, Any], errors: List[ValidationError]) -> None:
    if person.get("schema") != SCHEMA_NAME_V1_3:
        errors.append(ValidationError(
            "B-SCHEMA", f"person.schema must be {SCHEMA_NAME_V1_3!r}",
            "schema", "schema",
        ))


def _check_floor(person: Dict[str, Any], errors: List[ValidationError]) -> None:
    floor = person.get("privacy_floor")
    if floor not in ALLOWED_FLOORS:
        errors.append(ValidationError(
            "B-FLOOR", f"person.privacy_floor invalid: {floor!r}",
            "privacy_floor", "privacy_floor",
        ))
    rel = _mapping(person.get("relation"))
    pclass = rel.get("person_class")
    if pclass not in ALLOWED_PERSON_CLASS:
        errors.append(ValidationError(
            "B-REL", f"person.relation.person_class invalid: {pclass!r}",
            "relation", "person_class",
        ))


# ---- block 30: relationships (first-class RELATIONSHIP objects) ----------- #

def _check_relationships(
    person: Dict[str, Any], errors: List[ValidationError]
) -> None:
    """Amend 16 — RELATIONSHIP is a first-class object.

    Required fields on each relationship:
      - id (string, R-<sha256[0:8]>)
      - participants (list[str], min 2)
      - perspectives (mapping)
      - dynamics (mapping with the 8 required keys)
      - irreducibility (mapping with 4 always-true flags, including
        model_complete: false and epsilon_qualia: ">0")
    """
    rels = person.get("relationships")
    if rels is None:
        errors.append(ValidationError(
            "B30", "person.relationships (block 30) is required",
            "relationships", "",
        ))
        return
    if not _is_list_of_dicts(rels):
        errors.append(ValidationError(
            "B30", "person.relationships must be a list of mappings",
            "relationships", "",
        ))
        return

    for i, r in enumerate(rels):
        prefix = f"relationships[{i}]"

        # forbidden single-scalar anti-pattern
        for forbidden in FORBIDDEN_RELATIONSHIP_SCALARS:
            if forbidden in r:
                errors.append(ValidationError(
                    "B30-FORBID",
                    f"relationship forbids single-scalar field {forbidden!r} "
                    f"(quantitative compression of relationship quality is forbidden)",
                    "relationships", f"{prefix}.{forbidden}",
                ))

        # id
        rid = r.get("id")
        if not _is_str(rid) or not rid.startswith("R-"):
            errors.append(ValidationError(
                "B30-ID", f"{prefix}.id must be string starting with 'R-'",
                "relationships", f"{prefix}.id",
            ))

        # participants (min 2)
        parts = r.get("participants")
        if not isinstance(parts, list) or len(parts) < 2:
            errors.append(ValidationError(
                "B30-PARTS",
                f"{prefix}.participants must be list with ≥2 entries",
                "relationships", f"{prefix}.participants",
            ))
        elif not all(_is_str(p) and p.startswith("P-") for p in parts):
            errors.append(ValidationError(
                "B30-PARTS",
                f"{prefix}.participants must be list of P-<id> strings",
                "relationships", f"{prefix}.participants",
            ))

        # perspectives (mapping with at least one entry)
        persp = _mapping(r.get("perspectives"))
        if not persp:
            errors.append(ValidationError(
                "B30-PERSP",
                f"{prefix}.perspectives must be a non-empty mapping",
                "relationships", f"{prefix}.perspectives",
            ))

        # dynamics: the 8 required mechanism keys
        dyn = _mapping(r.get("dynamics"))
        missing_dyn = sorted(RELATIONSHIP_DYNAMICS_KEYS - set(dyn.keys()))
        if missing_dyn:
            errors.append(ValidationError(
                "B30-DYN",
                f"{prefix}.dynamics missing required keys: {missing_dyn}",
                "relationships", f"{prefix}.dynamics",
            ))
        else:
            for k in RELATIONSHIP_DYNAMICS_KEYS:
                v = dyn[k]
                if not _is_str(v) or not v:
                    errors.append(ValidationError(
                        "B30-DYN",
                        f"{prefix}.dynamics.{k} must be a non-empty claim_ref string",
                        "relationships", f"{prefix}.dynamics.{k}",
                    ))

        # irreducibility: 4 always-true flags
        irred = _mapping(r.get("irreducibility"))
        if not irred:
            errors.append(ValidationError(
                "B30-IRRED",
                f"{prefix}.irreducibility must be a mapping",
                "relationships", f"{prefix}.irreducibility",
            ))
        else:
            # 4 always-true flags
            for flag in (
                "participants_not_reducible_to_relationship",
                "relationship_not_reducible_to_evidence",
                "model_complete",
                "remainder_present",
            ):
                if flag not in irred:
                    errors.append(ValidationError(
                        "B30-IRRED",
                        f"{prefix}.irreducibility.{flag} required",
                        "relationships", f"{prefix}.irreducibility.{flag}",
                    ))

            # model_complete must be false (H9 — never collapsible to complete)
            if irred.get("model_complete") is not False:
                errors.append(ValidationError(
                    "B30-IRRED",
                    f"{prefix}.irreducibility.model_complete must be false (H9 permanent)",
                    "relationships", f"{prefix}.irreducibility.model_complete",
                ))

            # epsilon_qualia: ">0" required (not optional, not a number)
            eq = irred.get("epsilon_qualia")
            if not (isinstance(eq, str) and eq.strip(" \"") == ">0" and eq.startswith(">")):
                errors.append(ValidationError(
                    "B30-IRRED",
                    f"{prefix}.irreducibility.epsilon_qualia must be string '>0' "
                    f"(H9 permanent flag, not a numeric score)",
                    "relationships", f"{prefix}.irreducibility.epsilon_qualia",
                ))


# ---- Amend 17: loop_graph uses outbound_relationships; reject PERSON-PERSON direct edges ---- #

def _check_loop_graph(
    person: Dict[str, Any], errors: List[ValidationError]
) -> None:
    """Amend 17 — PERSON-PERSON direct edges are forbidden.

    loop_graph must NOT contain `edges:` with PERSON-PERSON from→to.
    Allowed: outbound_relationships (list of refs to relationship objects).
    """
    lg = _mapping(person.get("loop_graph"))
    if not lg:
        errors.append(ValidationError(
            "B15", "person.loop_graph must be a non-empty mapping",
            "loop_graph", "",
        ))
        return

    # If `edges` is present, check for PERSON-PERSON direct edges
    if "edges" in lg:
        edges = lg.get("edges") or []
        if not isinstance(edges, list):
            errors.append(ValidationError(
                "B17", "person.loop_graph.edges must be a list if present",
                "loop_graph", "edges",
            ))
        else:
            for i, e in enumerate(edges):
                if not isinstance(e, dict):
                    continue
                from_node = e.get("from") or e.get("from_node")
                to_node = e.get("to") or e.get("to_node")
                if (
                    _is_str(from_node) and from_node.startswith("P-")
                    and _is_str(to_node) and to_node.startswith("P-")
                ):
                    errors.append(ValidationError(
                        "B17-PP",
                        f"loop_graph.edges[{i}] is a PERSON-PERSON direct edge "
                        f"({from_node} -> {to_node}); v1.3 forbids this. Use "
                        f"outbound_relationships and reference a RELATIONSHIP object.",
                        "loop_graph", f"edges[{i}]",
                    ))

    # outbound_relationships recommended (v1.3 architecture)
    out_rels = lg.get("outbound_relationships")
    if out_rels is not None:
        if not isinstance(out_rels, list):
            errors.append(ValidationError(
                "B17", "person.loop_graph.outbound_relationships must be a list",
                "loop_graph", "outbound_relationships",
            ))
        else:
            for i, oref in enumerate(out_rels):
                if not isinstance(oref, dict):
                    continue
                if "relationship_id" not in oref:
                    errors.append(ValidationError(
                        "B17",
                        f"loop_graph.outbound_relationships[{i}].relationship_id required",
                        "loop_graph", f"outbound_relationships[{i}].relationship_id",
                    ))


# ---- block 32: model_versions (Amend 22) ------------------------------------ #

def _check_model_versions(
    person: Dict[str, Any], errors: List[ValidationError]
) -> None:
    """Amend 22 — model_versions, if present, must NOT conflate
    simulation_quality with identity_fidelity.
    """
    if "model_versions" not in person:
        return
    mv = person.get("model_versions")
    if not _is_list_of_dicts(mv):
        errors.append(ValidationError(
            "B32", "person.model_versions must be a list of mappings",
            "model_versions", "",
        ))
        return
    for i, m in enumerate(mv):
        prefix = f"model_versions[{i}]"
        for k in ("model_id", "parent_evidence_refs",
                  "predictive_accuracy", "competing_hypotheses"):
            if k not in m:
                errors.append(ValidationError(
                    "B32",
                    f"{prefix}.{k} required",
                    "model_versions", f"{prefix}.{k}",
                ))
        # No digital twin: simulation_quality may be present, but it must
        # NOT be a stand-in for identity_fidelity. If identity_fidelity is
        # present, it's a violation of Amend 22 ("no digital twin" rule).
        if "identity_fidelity" in m:
            errors.append(ValidationError(
                "B22-TWIN",
                f"{prefix}.identity_fidelity forbidden (Amend 22: no digital twin). "
                f"Use simulation_quality, but never as identity_fidelity.",
                "model_versions", f"{prefix}.identity_fidelity",
            ))
        # can_speak_for_person is forbidden
        if m.get("can_speak_for_person") is True:
            errors.append(ValidationError(
                "B22-TWIN",
                f"{prefix}.can_speak_for_person: true forbidden (Amend 22: "
                f"the model is a derived interpretation, never the person's voice).",
                "model_versions", f"{prefix}.can_speak_for_person",
            ))


# ---- block 33: evaluation_metrics (Amend 21) ------------------------------- #

def _check_evaluation_metrics(
    person: Dict[str, Any], errors: List[ValidationError]
) -> None:
    """Amend 21 — evaluation_metrics, if present, must address all 8
    evaluation questions.
    """
    if "evaluation_metrics" not in person:
        return
    em = _mapping(person.get("evaluation_metrics"))
    if not em:
        errors.append(ValidationError(
            "B33", "person.evaluation_metrics must be a non-empty mapping",
            "evaluation_metrics", "",
        ))
        return
    missing = [q for q in EVALUATION_QUESTIONS if q not in em]
    if missing:
        errors.append(ValidationError(
            "B33",
            f"evaluation_metrics missing 8 evaluation questions (Amend 21): {missing}",
            "evaluation_metrics", "",
        ))


# ---- block 34: memory_tier (Amend 23) -------------------------------------- #

def _check_memory_tier(
    person: Dict[str, Any], errors: List[ValidationError]
) -> None:
    """Amend 23 — memory_tier must be one of working/core/archival/longmem."""
    tier = person.get("memory_tier")
    if tier not in ALLOWED_MEMORY_TIER:
        errors.append(ValidationError(
            "B34",
            f"person.memory_tier must be one of {sorted(ALLOWED_MEMORY_TIER)} "
            f"(got {tier!r})",
            "memory_tier", "memory_tier",
        ))


# ---- W3C PROV envelope on every claim (Amend 24) -------------------------- #

def _check_prov_envelope(
    person: Dict[str, Any], errors: List[ValidationError]
) -> None:
    """Amend 24 — every claim in `claims:` (if present) must carry the
    full W3C PROV envelope. We do not require `claims:` to exist on every
    file; but if it does, every claim must be PROV-complete.
    """
    claims = person.get("claims")
    if claims is None:
        return
    if not _is_list_of_dicts(claims):
        errors.append(ValidationError(
            "B24", "person.claims must be a list of mappings",
            "claims", "",
        ))
        return
    for i, c in enumerate(claims):
        prefix = f"claims[{i}]"
        for k in PROV_REQUIRED:
            if k not in c:
                errors.append(ValidationError(
                    "B24-MISS",
                    f"{prefix}.{k} required (W3C PROV envelope, Amend 24)",
                    "claims", f"{prefix}.{k}",
                ))

        # Type-check the typed fields
        subj = c.get("subject_ref")
        if subj is not None and not _is_str(subj):
            errors.append(ValidationError(
                "B24-TYPE", f"{prefix}.subject_ref must be string",
                "claims", f"{prefix}.subject_ref",
            ))
        ev = c.get("evidence_refs")
        if ev is not None and not isinstance(ev, list):
            errors.append(ValidationError(
                "B24-TYPE", f"{prefix}.evidence_refs must be list",
                "claims", f"{prefix}.evidence_refs",
            ))
        vf = c.get("valid_from")
        if vf is not None and not _is_iso(vf):
            errors.append(ValidationError(
                "B24-TYPE", f"{prefix}.valid_from must be ISO-8601",
                "claims", f"{prefix}.valid_from",
            ))
        vt = c.get("valid_to")
        if vt is not None and not _is_str(vt):
            errors.append(ValidationError(
                "B24-TYPE", f"{prefix}.valid_to must be string ('open' or ISO-8601)",
                "claims", f"{prefix}.valid_to",
            ))
        rec = c.get("recorded_at")
        if rec is not None and not _is_iso(rec):
            errors.append(ValidationError(
                "B24-TYPE", f"{prefix}.recorded_at must be ISO-8601",
                "claims", f"{prefix}.recorded_at",
            ))
        rep = c.get("reporter")
        if rep is not None and rep not in ALLOWED_REPORTER:
            errors.append(ValidationError(
                "B24-TYPE",
                f"{prefix}.reporter must be one of {sorted(ALLOWED_REPORTER)}",
                "claims", f"{prefix}.reporter",
            ))
        es = c.get("epistemic_state")
        if es is not None and es not in ALLOWED_EPISTEMIC_STATE:
            errors.append(ValidationError(
                "B24-TYPE",
                f"{prefix}.epistemic_state must be one of {sorted(ALLOWED_EPISTEMIC_STATE)}",
                "claims", f"{prefix}.epistemic_state",
            ))


# ---- Falsification (5 of 6 from v1.1; F5 deferred to retrieval layer) ----- #

def _enforce_falsification(
    person: Dict[str, Any],
    report: ValidationReport,
) -> None:
    """F1, F2, F3, F4, F6 from v1.1. F5 (attention gate) is DEFERRED to
    the retrieval layer per task spec.
    """
    # F2 floor binding
    floor = person.get("privacy_floor")
    rel = _mapping(person.get("relation"))
    pclass = rel.get("person_class")
    if floor in ALLOWED_FLOORS and pclass in ALLOWED_PERSON_CLASS:
        report.falsification_results["F2"] = (
            f"OK — floor={floor}, person_class={pclass}"
        )
    else:
        report.errors.append(ValidationError(
            "F2", "privacy_floor or person_class missing/invalid",
            "falsification", "F2",
        ))
        report.falsification_results["F2"] = "FAIL"

    # F3 source-class discipline — ARIF_ATTESTED w/o cross_check must
    # downgrade state to INFERRED.
    f3_failures: List[str] = []

    def _scan(obj: Any, path: str) -> None:
        if isinstance(obj, dict):
            ec = obj.get("evidence_class")
            if (
                ec == "ARIF_ATTESTED"
                and not obj.get("cross_check_required", False)
                and obj.get("state") in ("WITNESSED", "INFERRED")
                and obj.get("state") == "WITNESSED"
            ):
                f3_failures.append(path)
            for k, v in obj.items():
                _scan(v, f"{path}.{k}")
        elif isinstance(obj, list):
            for i, x in enumerate(obj):
                _scan(x, f"{path}[{i}]")

    _scan(person, "person")
    if f3_failures:
        for path in f3_failures:
            report.errors.append(ValidationError(
                "F3",
                f"ARIF_ATTESTED w/o cross_check_required at {path} — must "
                f"downgrade state to INFERRED",
                "falsification", path,
            ))
        report.falsification_results["F3"] = f"FAIL ({len(f3_failures)})"
    else:
        report.falsification_results["F3"] = "OK"

    # F4 void ledger integrity — at least one V5_IRREDUCIBLE void.
    voids = _sequence(person.get("voids"))
    has_v5 = any(
        isinstance(v, dict) and v.get("state") == "V5_IRREDUCIBLE"
        for v in voids
    )
    if not has_v5:
        report.errors.append(ValidationError(
            "F4",
            "voids must contain ≥1 V5_IRREDUCIBLE entry (H9 structurally irreducible)",
            "falsification", "F4",
        ))
        report.falsification_results["F4"] = "FAIL"
    else:
        report.falsification_results["F4"] = "OK"

    # F6 paradox-active disclosure — recorded for surface.
    paradoxes = _sequence(person.get("paradoxes_active"))
    report.falsification_results["F6"] = (
        f"OK — {len(paradoxes)} active paradox(es) recorded for surface"
    )

    # F1 single-source-of-truth — seal.sha256_yaml must equal computed sha.
    seal = _mapping(person.get("seal"))
    declared = seal.get("sha256_yaml")
    actual = report.sha_yaml
    if not declared:
        report.errors.append(ValidationError(
            "F1", "seal.sha256_yaml missing — no source-of-truth attested",
            "falsification", "F1",
        ))
        report.falsification_results["F1"] = "FAIL"
    elif declared != actual:
        report.errors.append(ValidationError(
            "F1",
            f"seal.sha256_yaml mismatch: declared={declared!r} actual={actual!r}",
            "falsification", "F1",
        ))
        report.falsification_results["F1"] = "FAIL"
    else:
        report.falsification_results["F1"] = "OK"

    # F5 attention gate — DEFERRED to retrieval layer (per task spec).
    report.falsification_results["F5"] = "DEFERRED (retrieval layer)"


# ----------------------------- sha + canonical ----------------------------- #

def _yaml_canonical_text(yaml_text: str) -> str:
    """Strip seal.sha256_yaml from the document before hashing (so the
    seal itself doesn't poison the hash)."""
    try:
        doc = yaml.safe_load(yaml_text)
    except yaml.YAMLError as e:
        raise ValidationError("F1", f"YAML parse error: {e}")
    if not isinstance(doc, dict) or "person" not in doc:
        raise ValidationError("F1", "top-level 'person:' mapping required")
    seal = _mapping(doc["person"].get("seal"))
    if seal and "sha256_yaml" in seal:
        seal_for_hash = dict(seal)
        seal_for_hash["sha256_yaml"] = "<sentinel-sha256-of-source-yaml>"
        doc["person"]["seal"] = seal_for_hash
    return yaml.safe_dump(doc, sort_keys=False, allow_unicode=True,
                          default_flow_style=False)


def _compute_yaml_sha(yaml_text: str) -> str:
    canonical = _yaml_canonical_text(yaml_text)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


# ----------------------------- public entry points ------------------------- #

def validate(person: Dict[str, Any]) -> ValidationReport:
    report = ValidationReport()
    if not isinstance(person, dict):
        report.errors.append(ValidationError(
            "TOP", "top-level YAML must be a mapping",
            "top", "",
        ))
        return report

    # baseline top-level presence (v1.1 block list)
    missing = [b for b in REQUIRED_TOP_BLOCKS if b not in person]
    if missing:
        report.errors.append(ValidationError(
            "TOP", f"missing top-level keys: {missing}",
            "top", "",
        ))

    # v1.3 schema name
    _check_schema(person, report.errors)
    report.block_results["schema"] = (
        "OK" if person.get("schema") == SCHEMA_NAME_V1_3 else "FAIL"
    )

    # floor + relation baseline
    _check_floor(person, report.errors)
    report.block_results["privacy_floor"] = (
        "OK" if person.get("privacy_floor") in ALLOWED_FLOORS else "FAIL"
    )

    # v1.3 block-level checks
    block_fns = {
        "relationships": _check_relationships,
        "loop_graph": _check_loop_graph,
        "model_versions": _check_model_versions,
        "evaluation_metrics": _check_evaluation_metrics,
        "memory_tier": _check_memory_tier,
        "claims": _check_prov_envelope,
    }
    for name, fn in block_fns.items():
        try:
            fn(person, report.errors)
            report.block_results[name] = (
                "OK" if not any(e.block == name for e in report.errors)
                else "FAIL"
            )
        except Exception as e:  # pragma: no cover
            report.errors.append(ValidationError(
                "B-EXC", f"{name} validator crashed: {e}",
                name, "",
            ))
            report.block_results[name] = "FAIL"

    return report


def run(yaml_path: str) -> ValidationReport:
    if not os.path.exists(yaml_path):
        r = ValidationReport()
        r.errors.append(ValidationError(
            "IO", f"YAML not found: {yaml_path}",
            "io", "",
        ))
        return r
    with open(yaml_path, "r", encoding="utf-8") as f:
        yaml_text = f.read()
    try:
        doc = yaml.safe_load(yaml_text)
    except yaml.YAMLError as e:
        r = ValidationReport()
        r.errors.append(ValidationError(
            "IO", f"YAML parse error: {e}",
            "io", "",
        ))
        return r
    if not isinstance(doc, dict) or "person" not in doc:
        r = ValidationReport()
        r.errors.append(ValidationError(
            "TOP", "top-level 'person:' mapping required",
            "top", "",
        ))
        return r
    person = doc["person"]

    # 1. structural validation
    report = validate(person)
    # 2. compute yaml sha
    report.sha_yaml = _compute_yaml_sha(yaml_text)
    # 3. falsification (uses sha)
    _enforce_falsification(person, report)
    return report


# ----------------------------- CLI ----------------------------------------- #

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="person_validate_v1_3",
        description="arifos.person.v1.3 validator (RELATIONSHIP first-class, W3C PROV)",
    )
    p.add_argument("yaml", help="Path to person.v1.3.yaml")
    p.add_argument("--json", action="store_true", help="Emit JSON report to stdout")
    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = _build_argparser().parse_args(argv)
    report = run(args.yaml)
    if args.json:
        print(json.dumps(report.to_dict(), indent=2, sort_keys=False))
    else:
        if report.ok:
            print(
                f"OK — schema={report.schema_name} "
                f"sha={report.sha_yaml[:12]}… "
                f"falsification={report.falsification_results}"
            )
        else:
            for e in report.errors:
                print(f"FAIL {e}", file=sys.stderr)
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
