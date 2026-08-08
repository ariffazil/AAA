#!/usr/bin/env python3
"""Validate a JSON organ capability manifest against minimum federation rules."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

CAPABILITY_RE = re.compile(r"^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*){1,}$")
ALLOWED_ACTIONS = {"OBSERVE", "COMPUTE", "RECOMMEND", "MUTATE", "IRREVERSIBLE"}
ALLOWED_FAILURES = {"PASS", "WARN", "HOLD", "VOID", "ERROR"}


def load(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read valid JSON from {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("manifest root must be an object")
    return data


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    organ = data.get("organ")
    capabilities = data.get("capabilities")
    registry = data.get("registry")
    promotion = data.get("promotion")

    if not isinstance(organ, dict):
        errors.append("organ must be an object")
    else:
        for field in ("id", "version", "domain_law", "owner", "purpose", "does_not_own"):
            if field not in organ:
                errors.append(f"organ.{field} is required")
        if "does_not_own" in organ and not isinstance(organ["does_not_own"], list):
            errors.append("organ.does_not_own must be a list")

    if not isinstance(capabilities, list) or not capabilities:
        errors.append("capabilities must be a non-empty list")
    else:
        seen: set[str] = set()
        for index, capability in enumerate(capabilities):
            prefix = f"capabilities[{index}]"
            if not isinstance(capability, dict):
                errors.append(f"{prefix} must be an object")
                continue
            required = (
                "capability_id",
                "semantic_version",
                "implementation",
                "action_class",
                "mutation",
                "irreversible",
                "authority_required",
                "idempotency",
                "failure_mode",
                "receipt_policy",
            )
            for field in required:
                if field not in capability:
                    errors.append(f"{prefix}.{field} is required")
            cap_id = capability.get("capability_id")
            if not isinstance(cap_id, str) or not CAPABILITY_RE.fullmatch(cap_id):
                errors.append(f"{prefix}.capability_id must be dotted lowercase semantic ID")
            elif cap_id in seen:
                errors.append(f"duplicate capability_id: {cap_id}")
            else:
                seen.add(cap_id)
            action = capability.get("action_class")
            if action not in ALLOWED_ACTIONS:
                errors.append(f"{prefix}.action_class must be one of {sorted(ALLOWED_ACTIONS)}")
            failure = capability.get("failure_mode")
            if failure not in ALLOWED_FAILURES:
                errors.append(f"{prefix}.failure_mode must be one of {sorted(ALLOWED_FAILURES)}")
            mutation = capability.get("mutation")
            irreversible = capability.get("irreversible")
            if not isinstance(mutation, bool) or not isinstance(irreversible, bool):
                errors.append(f"{prefix}.mutation and irreversible must be booleans")
            if irreversible is True and mutation is not True:
                errors.append(f"{prefix}: irreversible capability must also declare mutation=true")
            if irreversible is True and not capability.get("human_ack_required", False):
                errors.append(f"{prefix}: irreversible capability requires human_ack_required=true")
            if mutation is True and not capability.get("rollback") and not capability.get("compensation"):
                errors.append(f"{prefix}: mutating capability requires rollback or compensation")
            implementation = capability.get("implementation")
            if not isinstance(implementation, dict) or not implementation.get("provider"):
                errors.append(f"{prefix}.implementation.provider is required")

    if not isinstance(registry, dict):
        errors.append("registry must be an object")
    else:
        for field in ("source_of_truth", "health_capability", "profiles"):
            if field not in registry:
                errors.append(f"registry.{field} is required")

    if not isinstance(promotion, dict):
        errors.append("promotion must be an object")
    elif promotion.get("sovereign_approval_required") is not True:
        errors.append("promotion.sovereign_approval_required must be true")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        errors = validate(load(args.manifest))
    except ValueError as exc:
        print(json.dumps({"status": "INVALID", "errors": [str(exc)]}, indent=2))
        return 2
    result = {"status": "VALID" if not errors else "INVALID", "errors": errors}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
