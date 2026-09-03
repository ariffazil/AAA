#!/usr/bin/env python3
"""
aaa-registry compile — Single canonical compiler for the arifOS model registry.

Reads catalog/*.yaml, validates against schema, generates:
  - compiled/FEDERATION_MODEL.json   (kernel routing view)
  - compiled/REGISTRY_INDEX.md       (human-readable index)
  - compiled/model-state.json        (runtime state)
  - compiled/manifest.json           (hashes + metadata)

One authored truth → one compiler → three generated views.

DITEMPA BUKAN DIBERI.
"""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import yaml

try:
    import jsonschema
except ImportError:
    jsonschema = None


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super().default(obj)


def dumps(obj: object, **kwargs: object) -> str:
    return json.dumps(obj, cls=DateEncoder, **kwargs)


REGISTRY = Path(__file__).parent
CATALOG_DIR = REGISTRY / "catalog"
COMPILED_DIR = REGISTRY / "compiled"
SCHEMA_PATH = REGISTRY / "schema" / "model.schema.json"


def load_schema() -> dict:
    if SCHEMA_PATH.exists():
        return json.loads(SCHEMA_PATH.read_text())
    return {}


def load_catalog() -> list[dict]:
    records = []
    if not CATALOG_DIR.exists():
        print(f"WARN: catalog/ not found at {CATALOG_DIR}")
        return records
    for path in sorted(CATALOG_DIR.glob("*.yaml")):
        try:
            with open(path) as f:
                data = yaml.safe_load(f)
            if data:
                data["_source_file"] = path.name
                records.append(data)
        except Exception as e:
            print(f"ERROR: Failed to load {path.name}: {e}")
    return records


def _to_str(val: object) -> str | None:
    if val is None:
        return None
    if isinstance(val, (date, datetime)):
        return val.isoformat()
    return str(val)


def validate_record(record: dict, schema: dict) -> list[str]:
    errors = []
    if jsonschema and schema:
        try:
            clean = {k: v for k, v in record.items() if not k.startswith("_")}
            jsonschema.validate(clean, schema)
        except jsonschema.ValidationError as e:
            errors.append(f"{e.json_path}: {e.message}")
        except Exception as e:
            errors.append(f"Schema error: {e}")
    else:
        required = ["schema_version", "identity", "capability", "hazards", "freshness"]
        for field in required:
            if field not in record:
                errors.append(f"Missing required field: {field}")
        ident = record.get("identity", {})
        if "id" not in ident:
            errors.append("identity.id missing")
        if "status" not in ident:
            errors.append("identity.status missing")
    return errors


def check_duplicates(records: list[dict]) -> list[str]:
    errors = []
    seen: dict[str, str] = {}
    for r in records:
        model_id = r.get("identity", {}).get("id", "unknown")
        if model_id in seen:
            errors.append(
                f"Duplicate model ID '{model_id}' in "
                f"{seen[model_id]} and {r.get('_source_file', '?')}"
            )
        seen[model_id] = r.get("_source_file", "?")
    return errors


def check_evidence_refs(records: list[dict]) -> list[str]:
    warnings = []
    for r in records:
        model_id = r.get("identity", {}).get("id", "unknown")
        refs = r.get("capability", {}).get("evidence_refs", [])
        for h in r.get("hazards", []):
            refs.extend(h.get("evidence_refs", []))
        for ref in refs:
            if ref.startswith("ev:"):
                parts = ref.split(":")
                if len(parts) < 3:
                    warnings.append(f"{model_id}: malformed evidence ref '{ref}'")
    return warnings


def check_freshness(records: list[dict]) -> list[str]:
    warnings = []
    today = date.today().isoformat()
    for r in records:
        model_id = r.get("identity", {}).get("id", "unknown")
        freshness = r.get("freshness", {})
        review_after = _to_str(freshness.get("review_after"))
        if review_after and review_after < today:
            stale_action = freshness.get("stale_action", "warn")
            warnings.append(
                f"{model_id}: stale (review_after={review_after}, "
                f"action={stale_action})"
            )
    return warnings


def generate_federation_model(records: list[dict]) -> dict:
    models = []
    for r in records:
        ident = r.get("identity", {})
        cap = r.get("capability", {})
        hazards = r.get("hazards", [])
        freshness = r.get("freshness", {})

        hazard_ids = [h["id"] for h in hazards if "id" in h]
        max_severity = "low"
        severity_order = {"low": 0, "medium": 1, "high": 2, "critical": 3}
        for h in hazards:
            sev = h.get("severity", "low")
            if severity_order.get(sev, 0) > severity_order.get(max_severity, 0):
                max_severity = sev

        floor_deltas = {}
        for h in hazards:
            for floor, delta in h.get("floor_deltas", {}).items():
                if delta != "standard":
                    floor_deltas[floor] = delta

        models.append({
            "model_key": ident["id"],
            "provider": ident.get("provider", "unknown"),
            "family": ident.get("family", "unknown"),
            "variant": ident.get("variant"),
            "route": ident.get("route", "unknown"),
            "status": ident.get("status", "unknown"),
            "context_window": ident.get("context_window"),
            "modality": ident.get("modality", []),
            "jurisdiction": ident.get("jurisdiction", "UNKNOWN"),
            "capabilities": cap.get("allowed_tasks", []),
            "capability_confidence": cap.get("confidence", "untested"),
            "hazards": hazard_ids,
            "max_hazard_severity": max_severity,
            "floor_deltas": floor_deltas,
            "forbidden": r.get("forbidden", []),
            "requires_human_ack_for": r.get("requires_human_ack_for", []),
            "censorship": r.get("censorship"),
            "pricing": r.get("pricing"),
            "freshness": {
                "review_after": _to_str(freshness.get("review_after")),
                "stale_action": freshness.get("stale_action"),
                "last_verified": _to_str(freshness.get("last_verified")),
            },
        })

    return {
        "schema": "arifos-federation-model-registry-v2",
        "compiled_at": datetime.now(timezone.utc).isoformat(),
        "compiler": "aaa-registry compile",
        "record_count": len(models),
        "models": models,
        "default_for_unlisted": {
            "risk_tier": "guarded",
            "forbidden": ["self_authorize", "seal_without_judge", "irreversible_commit"],
            "requires_human_ack_for": ["all_irreversible"],
        },
    }


def generate_index(records: list[dict], errors: list[str], warnings: list[str]) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Model Registry Index",
        "",
        f"> **Compiled:** {now}",
        "> **Compiler:** aaa-registry compile",
        f"> **Records:** {len(records)}",
        "> **Authority:** F13 SOVEREIGN (Arif Fazil)",
        "",
        "---",
        "",
        "## Active models",
        "",
        "| ID | Provider | Status | Hazards | Confidence | Review After |",
        "|----|----------|--------|---------|------------|--------------|",
    ]

    for r in records:
        ident = r.get("identity", {})
        cap = r.get("capability", {})
        hazards = r.get("hazards", [])
        freshness = r.get("freshness", {})
        hazard_count = len(hazards)
        high_count = sum(1 for h in hazards if h.get("severity") in ("high", "critical"))
        hazard_str = f"{hazard_count} ({high_count} high+)" if hazard_count else "none"
        lines.append(
            f"| `{ident.get('id', '?')}` "
            f"| {ident.get('provider', '?')} "
            f"| {ident.get('status', '?')} "
            f"| {hazard_str} "
            f"| {cap.get('confidence', '?')} "
            f"| {_to_str(freshness.get('review_after')) or '?'} |"
        )

    if errors:
        lines.extend(["", "## Errors", ""])
        for e in errors:
            lines.append(f"- ❌ {e}")

    if warnings:
        lines.extend(["", "## Warnings", ""])
        for w in warnings:
            lines.append(f"- ⚠️ {w}")

    lines.extend([
        "",
        "---",
        "",
        "*Generated by aaa-registry compile. Do not hand-edit.*",
        "*DITEMPA BUKAN DIBERI*",
    ])

    return "\n".join(lines) + "\n"


def generate_model_state(records: list[dict]) -> dict:
    models = {}
    severity_rank = {"low": 0, "medium": 1, "high": 2, "critical": 3}
    today = date.today().isoformat()
    for r in records:
        ident = r.get("identity", {})
        model_id = ident.get("id", "unknown")
        freshness = r.get("freshness", {})
        review_str = _to_str(freshness.get("review_after"))
        is_stale = review_str is not None and review_str < today

        hazards = r.get("hazards", [])
        max_sev = "none"
        max_rank = -1
        for h in hazards:
            sev = h.get("severity", "low")
            rank = severity_rank.get(sev, 0)
            if rank > max_rank:
                max_rank = rank
                max_sev = sev

        models[model_id] = {
            "status": ident.get("status", "unknown"),
            "stale": is_stale,
            "stale_action": freshness.get("stale_action") if is_stale else None,
            "hazard_count": len(hazards),
            "max_severity": max_sev,
            "confidence": r.get("capability", {}).get("confidence", "untested"),
        }

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "models": models,
    }


def content_hash(data: str | dict) -> str:
    if isinstance(data, dict):
        data = dumps(data, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(data.encode()).hexdigest()


def main() -> int:
    print("=" * 60)
    print("aaa-registry compile")
    print("=" * 60)

    schema = load_schema()
    records = load_catalog()
    print(f"\nLoaded {len(records)} catalog records")

    if not records:
        print("ERROR: No records found in catalog/")
        return 1

    all_errors: list[str] = []
    all_warnings: list[str] = []

    for r in records:
        errs = validate_record(r, schema)
        if errs:
            fname = r.get("_source_file", "?")
            all_errors.extend(f"{fname}: {e}" for e in errs)

    all_errors.extend(check_duplicates(records))
    all_warnings.extend(check_evidence_refs(records))
    all_warnings.extend(check_freshness(records))

    print(f"Validation: {len(all_errors)} errors, {len(all_warnings)} warnings")

    if all_errors:
        for e in all_errors:
            print(f"  ❌ {e}")

    for w in all_warnings:
        print(f"  ⚠️ {w}")

    COMPILED_DIR.mkdir(parents=True, exist_ok=True)

    fed_model = generate_federation_model(records)
    fed_json = dumps(fed_model, indent=2, ensure_ascii=False)
    (COMPILED_DIR / "FEDERATION_MODEL.json").write_text(fed_json)
    print(f"\nGenerated FEDERATION_MODEL.json ({len(fed_json)} bytes)")

    index_md = generate_index(records, all_errors, all_warnings)
    (COMPILED_DIR / "REGISTRY_INDEX.md").write_text(index_md)
    print(f"Generated REGISTRY_INDEX.md ({len(index_md)} bytes)")

    model_state = generate_model_state(records)
    state_json = dumps(model_state, indent=2)
    (COMPILED_DIR / "model-state.json").write_text(state_json)
    print(f"Generated model-state.json ({len(state_json)} bytes)")

    manifest = {
        "compiled_at": datetime.now(timezone.utc).isoformat(),
        "compiler": "aaa-registry compile",
        "record_count": len(records),
        "errors": len(all_errors),
        "warnings": len(all_warnings),
        "hashes": {
            "FEDERATION_MODEL.json": content_hash(fed_json),
            "REGISTRY_INDEX.md": content_hash(index_md),
            "model-state.json": content_hash(state_json),
        },
    }
    manifest_json = dumps(manifest, indent=2)
    (COMPILED_DIR / "manifest.json").write_text(manifest_json)
    print(f"Generated manifest.json")
    print(f"\nManifest hash: {content_hash(manifest_json)[:16]}...")

    if all_errors:
        print(f"\n⚠️  {len(all_errors)} errors — review before deploying")
        return 1

    print("\n✅ Compile complete — no errors")
    return 0


if __name__ == "__main__":
    sys.exit(main())
