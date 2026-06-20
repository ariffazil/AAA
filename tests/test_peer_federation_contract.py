"""
test_peer_federation_contract.py
==============================

Validate P2P Federation Contract v1 schema and spine instances.

Rules enforced:
  - Every instance matches the JSON Schema.
  - Only arifOS may hold authority_class == "judge".
  - Every contract MUST declare human_veto.f13_absolute == true.
  - Forbidden actions are non-empty.
  - Lease requirement aligns with authority_class (judge = false, others = true).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema
import pytest

PROJECT_ROOT = Path(__file__).parent.parent
SCHEMA_PATH = PROJECT_ROOT / "schemas" / "peer-federation-contract.schema.json"
CONTRACTS_DIR = PROJECT_ROOT / "a2a" / "peer-contracts"


def load_json(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _contract_params() -> list[tuple[str, dict[str, Any]]]:
    if not CONTRACTS_DIR.exists():
        return []
    out: list[tuple[str, dict[str, Any]]] = []
    for path in sorted(CONTRACTS_DIR.glob("*.json")):
        out.append((path.stem, load_json(path)))
    return out


@pytest.fixture(scope="module")
def schema() -> dict[str, Any]:
    if not SCHEMA_PATH.exists():
        pytest.skip(f"Schema not found: {SCHEMA_PATH}")
    return load_json(SCHEMA_PATH)


@pytest.fixture(scope="module")
def contracts() -> list[tuple[str, dict[str, Any]]]:
    return _contract_params()


class TestSchemaValidity:
    def test_schema_is_valid_json_schema(self, schema: dict[str, Any]) -> None:
        jsonschema.Draft202012Validator.check_schema(schema)

    @pytest.mark.parametrize("name,contract", _contract_params(), ids=[name for name, _ in _contract_params()])
    def test_contract_validates_against_schema(
        self, schema: dict[str, Any], name: str, contract: dict[str, Any]
    ) -> None:
        jsonschema.validate(contract, schema)


class TestConstitutionalConstraints:
    @pytest.mark.parametrize("name,contract", _contract_params(), ids=[name for name, _ in _contract_params()])
    def test_only_arifos_may_be_judge(
        self, name: str, contract: dict[str, Any]
    ) -> None:
        organ = contract["peer_id"]["organ"]
        authority_class = contract["authority_class"]
        if authority_class == "judge":
            assert organ == "arifOS", (
                f"[{name}] Only arifOS may hold authority_class='judge'. "
                f"Found organ='{organ}'."
            )

    @pytest.mark.parametrize("name,contract", _contract_params(), ids=[name for name, _ in _contract_params()])
    def test_f13_veto_is_absolute(
        self, name: str, contract: dict[str, Any]
    ) -> None:
        human_veto = contract.get("human_veto", {})
        assert human_veto.get("f13_absolute") is True, (
            f"[{name}] human_veto.f13_absolute must be true."
        )

    @pytest.mark.parametrize("name,contract", _contract_params(), ids=[name for name, _ in _contract_params()])
    def test_forbidden_actions_are_non_empty(
        self, name: str, contract: dict[str, Any]
    ) -> None:
        forbidden = contract.get("forbidden_actions", [])
        assert len(forbidden) >= 1, (
            f"[{name}] forbidden_actions must not be empty."
        )

    @pytest.mark.parametrize("name,contract", _contract_params(), ids=[name for name, _ in _contract_params()])
    def test_lease_requirement_matches_authority_class(
        self, name: str, contract: dict[str, Any]
    ) -> None:
        authority_class = contract["authority_class"]
        lease_required = contract["lease_required"]
        if authority_class == "judge":
            assert lease_required is False, (
                f"[{name}] judge class should not require a lease from itself."
            )
        else:
            assert lease_required is True, (
                f"[{name}] non-judge peers must require a lease."
            )

    @pytest.mark.parametrize("name,contract", _contract_params(), ids=[name for name, _ in _contract_params()])
    def test_attestation_signed_by_arifos_judge(
        self, name: str, contract: dict[str, Any]
    ) -> None:
        attestation = contract.get("signed_attestation", {})
        assert attestation.get("issuer") == "arifOS-888-JUDGE", (
            f"[{name}] signed_attestation.issuer must be 'arifOS-888-JUDGE'."
        )
        assert attestation.get("signature"), (
            f"[{name}] signed_attestation.signature must be present."
        )


class TestAuthorityClassUniqueness:
    def test_judge_class_unique_to_arifos(self) -> None:
        judges = [
            name for name, c in _contract_params()
            if c["authority_class"] == "judge"
        ]
        assert judges == ["arifos-kernel"], (
            f"Only arifos-kernel may be judge; found: {judges}"
        )
