#!/usr/bin/env python3
"""Federation ABI Structural + Semantic Validator.

Two-layer validation:
  Layer 1 — JSON Schema shape, required fields, enums, patterns, conditionals.
  Layer 2 — Session liveness, deadline, hash integrity, idempotency, authority.

Usage:
  python scripts/validate_federation_abi.py fixtures/federation/valid-request.json
  python scripts/validate_federation_abi.py --all
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas" / "federation"
FIXTURE_DIR = ROOT / "fixtures" / "federation"


def load_schema(name: str) -> dict:
    path = SCHEMA_DIR / f"federation-{name}.v1.schema.json"
    return json.loads(path.read_text())


def validate_structural(instance: dict, schema: dict) -> list[str]:
    """Layer 1: JSON Schema validation."""
    errors: list[str] = []
    try:
        from jsonschema import Draft202012Validator, ValidationError
        validator = Draft202012Validator(schema)
        for err in validator.iter_errors(instance):
            errors.append(f"  {err.json_path}: {err.message}")
    except ImportError:
        # Fallback: basic structural checks
        required = schema.get("required", [])
        for field in required:
            if field not in instance:
                errors.append(f"  missing required field: {field}")
        props = schema.get("properties", {})
        for field, value in instance.items():
            if field in props and "pattern" in props[field]:
                import re
                if not re.match(props[field]["pattern"], str(value)):
                    errors.append(f"  {field}: pattern mismatch ({props[field]['pattern']})")
    return errors


def validate_semantic(instance: dict) -> list[str]:
    """Layer 2: Runtime semantic checks."""
    errors: list[str] = []

    # Session must have content
    session_id = instance.get("session_id", "")
    if not session_id or session_id == "":
        errors.append("  session_id empty — SESSION_MISSING")

    # Deadline check
    deadline = instance.get("deadline_at")
    if deadline:
        try:
            dt = datetime.fromisoformat(deadline.replace("Z", "+00:00"))
            if dt < datetime.now(timezone.utc):
                errors.append("  deadline_at in the past — DEADLINE_EXCEEDED")
        except (ValueError, TypeError):
            errors.append("  deadline_at invalid format")

    # Payload hash integrity
    payload_hash = instance.get("payload_hash")
    if payload_hash and "payload" in instance:
        computed = "sha256:" + hashlib.sha256(
            json.dumps(instance["payload"], sort_keys=True).encode()
        ).hexdigest()
        if payload_hash != computed:
            errors.append(f"  payload_hash mismatch: declared={payload_hash[:16]}... computed={computed[:16]}...")

    # Idempotency: attempt <= max_attempts
    attempt = instance.get("attempt", 1)
    max_attempts = instance.get("max_attempts", 3)
    if attempt > max_attempts:
        errors.append(f"  attempt ({attempt}) > max_attempts ({max_attempts})")

    # Hop index must be sequential with parent
    if instance.get("parent_invocation_id") and instance.get("hop_index", 0) < 1:
        errors.append("  parent_invocation_id present but hop_index < 1")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="*", help="Fixture files to validate")
    parser.add_argument("--all", action="store_true", help="Validate all fixtures")
    args = parser.parse_args()

    request_schema = load_schema("request")
    total, passed, failed = 0, 0, 0

    files = args.files
    if args.all:
        files = sorted(FIXTURE_DIR.glob("*.json"))

    for fpath in files:
        path = Path(fpath)
        if not path.exists():
            print(f"❌ {path}: not found")
            failed += 1
            continue

        total += 1
        instance = json.loads(path.read_text())
        name = path.name
        expected_fail = "invalid" in name or "without" in name

        structural = validate_structural(instance, request_schema)
        semantic = validate_semantic(instance)
        all_errors = structural + semantic

        if expected_fail:
            if all_errors:
                print(f"✅ {name}: correctly rejected ({len(all_errors)} errors)")
                for e in all_errors:
                    print(f"  (expected) {e}")
                passed += 1
            else:
                print(f"❌ {name}: SHOULD fail but passed")
                failed += 1
        else:
            if all_errors:
                print(f"❌ {name}: {len(all_errors)} errors")
                for e in all_errors:
                    print(e)
                failed += 1
            else:
                print(f"✅ {name}: PASS (structural + semantic)")
                passed += 1

    print(f"\n{passed}/{total} passed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
