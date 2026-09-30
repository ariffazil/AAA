"""
test_human_state_claim_schema.py
================================

Regression fixture for the PROPOSED human-state admissibility contract.

  schema : /root/AAA/specs/human_state_claim.schema.json
  doctrine: /root/AAA/instructions/human-substrate-exclusions-PROPOSAL.md
  trace_id: trc-20260929-fi003-human9-ratification

Status: PROPOSED_AWAITING_F13. Nothing here is ratified. The point of the fixture is
that the lesson of GEOX PHYSICS.9 — "an excluded variable does not vanish, it returns
as an un-auditable default" — now has a test that fails when the lock is missing,
instead of a prose paragraph asserting one exists.

Rules enforced:
  - A conforming claim validates (golden path).
  - A bare scalar about a person is NOT a claim.
  - A claim with no declared target set is inadmissible (unnamed target == "whole person").
  - Response quantities (mood, energy_level, productivity, engagement, commitment,
    well_score, clarity ...) may not be asserted as state.
  - A hardcoded default must carry origin + error_bar (the cp=850.0 / energy_level=5 class).
  - Irreducible opacity cannot be switched off (H9 as structure, not sentiment).
  - Self-report by the subject is NOT excluded — guard against the contract silencing
    the person about their own body.
  - Stale readings must declare exclusion handling; there is no FLOORED option.
  - The schema is closed (additionalProperties: false) — WELL's human-state schema lacks this.

Run:
  cd /root/AAA && python3 -m pytest tests/test_human_state_claim_schema.py -q
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = PROJECT_ROOT / "specs" / "human_state_claim.schema.json"

# Quantities named by H1/H3/H4 + the WELL charter as *responses*, forbidden as asserted
# state. Mirrors target_set.items.not.enum in the schema; kept as an independent literal
# here on purpose: if someone loosens the schema enum, this list makes the diff fail.
RESPONSE_QUANTITIES = [
    "well_score",
    "energy_level",
    "energy_estimate",
    "mood",
    "willpower",
    "productivity",
    "engagement",
    "deep_engagement",
    "commitment",
    "focus",
    "clarity",
    "decision_fatigue",
    "capacity",
    "happiness",
    "obedience",
    "moral_worth",
]


def load_schema() -> dict[str, Any]:
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def schema() -> dict[str, Any]:
    return load_schema()


def golden_claim() -> dict[str, Any]:
    """A claim that satisfies every clause K1-K6 of the proposal."""
    return {
        "claim_id": "hsc-20260929-demo-001",
        "subject_ref": "arif-f13",
        "assertion": (
            "Over the 2026-09-29 session Arif self-reported sustained focus on the "
            "HUMAN-9 restoration lane; Governance axis inferred low from three open "
            "F13 HOLDs. This is an estimate of coordinates, not a statement about him."
        ),
        "evidence_class": "INFERRED",
        "target_set": ["Energy", "Attention", "Optionality", "Governance", "Meaning", "Witness"],
        "target_set_source": "AAA/skills/human-state-estimation/SKILL.md#state-axes-6",
        "not_measured": [
            "sleep architecture — no biometric read since 2026-09-15T15:30Z",
            "pain, hunger, hormonal state — never asked, never measured",
            "what this means to him (H3 valence) — unasked",
            "relational load R_t — single-perspective session evidence only",
        ],
        "coverage": 0.35,
        "freshness": {
            "observed_at": "2026-09-29T09:00:00Z",
            "age_hours": 0.5,
            "ttl_hours": 72,
            "expired": False,
        },
        "irreducible_opacity": {
            "remainder_present": True,
            "statement": (
                "The person is larger than this estimate; his future choices and lived "
                "qualia are not recorded here and cannot be."
            ),
            "unmodelled_influences_U_t": "unknown work-side pressures outside the session",
        },
        "confidence": 0.55,
        "trace_id": "trc-20260929-fi003-human9-ratification",
    }


# --------------------------------------------------------------------------
# 1. golden path — the contract must be satisfiable, or it is a veto not a gate
# --------------------------------------------------------------------------

def test_schema_is_a_valid_draft_2020_12_schema(schema):
    jsonschema.Draft202012Validator.check_schema(schema)


def test_conforming_claim_is_admissible(schema):
    jsonschema.validate(golden_claim(), schema)


# --------------------------------------------------------------------------
# 2. bare scalar — the human cp=850.0
# --------------------------------------------------------------------------

@pytest.mark.parametrize("bare", [88.4, 5.0, 85, "88.4"])
def test_bare_scalar_is_rejected(schema, bare):
    """`well_score: 88.4` as a claim about a person is not a claim, it is a default."""
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(bare, schema)


def test_well_shaped_object_is_rejected(schema):
    """The actual shape emitted by /var/lib/well/state.json fails this contract."""
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate({"well_score": 88.39999999999999}, schema)


def test_scalar_dumped_into_assertion_is_rejected(schema):
    """A person reduced to a numeral in the assertion field is too short to be a proposition."""
    claim = golden_claim()
    claim["assertion"] = "88.4"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(claim, schema)


# --------------------------------------------------------------------------
# 3. no target set — unnamed target silently becomes "the whole person"
# --------------------------------------------------------------------------

def test_claim_with_no_target_set_is_rejected(schema):
    claim = golden_claim()
    del claim["target_set"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(claim, schema)


def test_claim_with_empty_target_set_is_rejected(schema):
    claim = golden_claim()
    claim["target_set"] = []
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(claim, schema)


def test_target_set_without_a_named_owner_layer_is_rejected(schema):
    """K1 requires the owning layer, so no claim may invent a 4th coordinate system."""
    claim = golden_claim()
    claim["target_set_source"] = "my_own_new_set_of_nine"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(claim, schema)


def test_missing_not_measured_is_rejected(schema):
    """K4: the clause all nine inventoried layers lack — absence must be written down."""
    claim = golden_claim()
    del claim["not_measured"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(claim, schema)


def test_empty_not_measured_is_rejected(schema):
    """'We measured everything' is not an admissible statement about a human (H9)."""
    claim = golden_claim()
    claim["not_measured"] = []
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(claim, schema)


# --------------------------------------------------------------------------
# 4. response quantity asserted as state
# --------------------------------------------------------------------------

@pytest.mark.parametrize("quantity", RESPONSE_QUANTITIES)
def test_response_quantity_asserted_as_state_is_rejected(schema, quantity):
    claim = golden_claim()
    claim["target_set"] = [quantity]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(claim, schema)


@pytest.mark.parametrize("quantity", ["energy_level", "well_score", "deep_engagement"])
def test_response_quantity_hidden_inside_a_larger_set_is_rejected(schema, quantity):
    """The GEOX failure mode is re-entry, so one banned member must poison the set."""
    claim = golden_claim()
    claim["target_set"] = ["Energy", "Attention", quantity, "Witness"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(claim, schema)


def test_response_quantity_is_still_admissible_as_evidence(schema):
    """The ban is on conclusions, not measurements: cp=850.0 is legal as a measured input."""
    claim = golden_claim()
    claim["evidence_class"] = "OBS"
    claim["evidence_refs"] = [
        "/var/lib/well/state.json#metrics.cognitive.clarity=8.5",
        "/root/.hermes/carry_forward.json#human_state.energy_estimate=focused",
    ]
    jsonschema.validate(claim, schema)


@pytest.mark.xfail(
    strict=False,
    reason=(
        "KNOWN RESIDUAL, on the record: the derived exclusion list matches literal field "
        "names. A surface can dodge it by renaming energy_level -> energyLevel or 'vital charge'. "
        "Fix is a normalisation step in the write-point gate (proposal section 8.1), not a longer enum."
    ),
)
def test_renamed_response_quantity_still_dodges_the_list(schema):
    claim = golden_claim()
    claim["target_set"] = ["energyLevel"]
    jsonschema.validate(claim, schema)  # passes today => documented weakness


# --------------------------------------------------------------------------
# 5. hardcoded defaults must confess
# --------------------------------------------------------------------------

def test_hardcoded_default_without_provenance_is_rejected(schema):
    """The exact class of WELL server.py:9231-9236 and GEOX parameters.py:65."""
    claim = golden_claim()
    claim["value_source"] = "hardcoded_default"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(claim, schema)


def test_hardcoded_default_without_error_bar_is_rejected(schema):
    """cp=850.0 DID carry a provenance sentence and still had no bound — origin alone is a story."""
    claim = golden_claim()
    claim["value_source"] = "hardcoded_default"
    claim["default_provenance"] = {"origin": "WELL/server.py:9236 default quality_score=5"}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(claim, schema)


def test_hardcoded_default_declared_honestly_is_admissible(schema):
    """"unknown" is a valid answer; silence is not. Declaring a default keeps it auditable."""
    claim = golden_claim()
    claim["value_source"] = "hardcoded_default"
    claim["default_provenance"] = {
        "origin": "WELL/server.py:9236 sleep.get('quality_score', 5) — sensor never read",
        "error_bar": "unknown — not measured on this subject",
    }
    jsonschema.validate(claim, schema)


# --------------------------------------------------------------------------
# 6. H9 as structure
# --------------------------------------------------------------------------

def test_opacity_cannot_be_turned_off(schema):
    """No model may certify that nothing of the person remains unmodelled."""
    claim = golden_claim()
    claim["irreducible_opacity"]["remainder_present"] = False
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(claim, schema)


def test_opacity_without_a_statement_is_rejected(schema):
    claim = golden_claim()
    del claim["irreducible_opacity"]["statement"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(claim, schema)


# --------------------------------------------------------------------------
# 7. anti-overreach guard — the contract must not silence the person
# --------------------------------------------------------------------------

def test_self_report_of_a_banned_domain_is_admissible(schema):
    """'aku penat' is REPORTED/subject about the person's own body — Commandment #5 wins.

    Without this guard the exclusion list would become a machine that forbids a human
    from speaking about his own fatigue, which is the opposite of H3/H9.
    """
    claim = {
        "claim_id": "hsc-20260929-self-002",
        "subject_ref": "arif-f13",
        "assertion": "Arif said, in his own words: 'penat sikit tapi masih fokus'.",
        "evidence_class": "REPORTED",
        "reporter": "subject",
        "target_set": ["Energy"],
        "target_set_source": "subject_named_in_own_words",
        "not_measured": ["sleep quantity", "time of last meal", "pain"],
        "freshness": {
            "observed_at": "2026-09-29T09:10:00Z",
            "age_hours": 0.3,
            "ttl_hours": 72,
            "expired": False,
        },
        "irreducible_opacity": {
            "remainder_present": True,
            "statement": "His word 'penat' carries a texture we did not ask about.",
        },
        "trace_id": "trc-20260929-fi003-human9-ratification",
    }
    jsonschema.validate(claim, schema)


def test_reported_without_saying_who_reported_is_rejected(schema):
    """S (self) vs R (other) must not collapse — rasa-provenance keeps them separate."""
    claim = golden_claim()
    claim["evidence_class"] = "REPORTED"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(claim, schema)


def test_obs_without_evidence_refs_is_rejected(schema):
    claim = golden_claim()
    claim["evidence_class"] = "OBS"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(claim, schema)


# --------------------------------------------------------------------------
# 8. staleness — exclusion, never flooring
# --------------------------------------------------------------------------

def test_expired_reading_must_declare_handling(schema):
    """Reproduces the live defect: state.json well_score=88.4, freshness=EXPIRED, 14 days old."""
    claim = golden_claim()
    claim["freshness"] = {
        "observed_at": "2026-09-15T15:30:01Z",
        "age_hours": 330.0,
        "ttl_hours": 72,
        "expired": True,
    }
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(claim, schema)


def test_expired_reading_excluded_not_floored_is_admissible(schema):
    claim = golden_claim()
    claim["freshness"] = {
        "observed_at": "2026-09-15T15:30:01Z",
        "age_hours": 330.0,
        "ttl_hours": 72,
        "expired": True,
    }
    claim["expired_handling"] = "EXCLUDED_FROM_MIN"
    claim["admissible_as_current_state"] = False
    claim["coverage"] = 0.1
    jsonschema.validate(claim, schema)


@pytest.mark.parametrize("floored", ["FLOORED", "FLOOR_TO_ZERO", "KEPT_IN_MIN"])
def test_there_is_no_floor_option(schema, floored):
    """test_triad_phase4_exclusion: flooring makes the veto permanent. Not admissible vocab."""
    claim = golden_claim()
    claim["freshness"]["expired"] = True
    claim["expired_handling"] = floored
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(claim, schema)


# --------------------------------------------------------------------------
# 9. the lock itself — this is what GEOX's "CONSTITUTIONAL LOCK" never had
# --------------------------------------------------------------------------

def test_schema_declares_additional_properties_false():
    s = load_schema()
    assert s.get("additionalProperties") is False, (
        "open schema = unenforced lock (WELL human-state has additionalProperties ABSENT)"
    )
    hs = s["properties"]["irreducible_opacity"]
    assert hs.get("additionalProperties") is False
    assert s["properties"]["freshness"].get("additionalProperties") is False
    assert s["properties"]["default_provenance"].get("additionalProperties") is False


def test_unknown_extra_field_is_rejected(schema):
    """The day someone adds `constitutive_response: 850.0`, this test fires."""
    claim = golden_claim()
    claim["constitutive_response"] = 850.0
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(claim, schema)


def test_required_fields_are_the_named_contract(schema):
    s = load_schema()
    assert set(s["required"]) == {
        "claim_id",
        "subject_ref",
        "assertion",
        "evidence_class",
        "target_set",
        "target_set_source",
        "not_measured",
        "freshness",
        "irreducible_opacity",
        "trace_id",
    }, "required set IS the measurement contract K1-K6; changing it changes doctrine"


def test_trace_id_pattern_enforced(schema):
    """No trace_id => event-pile entry, not a causal-ledger entry (the 30/43 null defect)."""
    claim = golden_claim()
    claim["trace_id"] = "no-prefix-20260929"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(claim, schema)


def test_confidence_cap_is_inherited_not_invented(schema):
    """0.9 cap comes from SKILL.md Non-negotiable 1 + rasa-claim-envelope."""
    claim = golden_claim()
    claim["confidence"] = 0.95
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(claim, schema)


def test_doctrine_files_were_not_mutated_by_this_proposal():
    """Falsifier for the read-only promise: sealed canon must still be byte-identical to HEAD."""
    import subprocess

    for rel in (
        "instructions/human-substrate.md",
        "instructions/human-substrate.yaml",
        "instructions/human-reality-invariants.md",
    ):
        dirty = subprocess.run(
            ["git", "diff", "--name-only", "--", rel],
            cwd=PROJECT_ROOT, capture_output=True, text=True,
        ).stdout.strip()
        assert dirty == "", f"{rel} was modified — proposal must not touch sealed doctrine"

    canon = subprocess.run(
        ["git", "diff", "--name-only", "--", "canon/"],
        cwd=PROJECT_ROOT, capture_output=True, text=True,
    ).stdout.strip()
    assert canon == "", "canon/ was modified"


def test_status_header_is_not_ratified_class():
    s = load_schema()
    assert s["status"] == "PROPOSED_AWAITING_F13"
    proposal = (PROJECT_ROOT / "instructions" / "human-substrate-exclusions-PROPOSAL.md").read_text()
    lines = proposal.split("\n")

    # (1) this document's own classification line must be PROPOSED, never ratified
    cls = [ln for ln in lines if "**Classification:**" in ln]
    assert cls, "proposal lost its Classification header"
    assert "PROPOSED_AWAITING_F13" in cls[0]
    assert "F13_RATIFIED" not in cls[0]

    # (2) ratified-class wording is allowed ONLY as a citation of the PARENT doctrine.
    #     A line that says F13_RATIFIED without naming the parent it quotes is this
    #     proposal self-certifying — the exact failure mode the whole task forbids.
    parent_markers = ("human-substrate.md", "efdcaa8e", "rcpt-afa7207241b746e2", "Parent doctrine")
    offenders = [
        (i + 1, ln)
        for i, ln in enumerate(lines)
        if "F13_RATIFIED" in ln and not any(m in ln for m in parent_markers)
    ]
    assert offenders == [], f"unattributed ratified wording: {offenders}"

    # (3) the delivery-posture block must keep saying it is not sealed
    assert "RATIFIED = TIDAK" in proposal.replace("   ", " ")

