#!/usr/bin/env python3
"""Compare declared and live capability/tool surfaces.

Input JSON:
{
  "canonical": ["arif_init"],
  "live": ["arif_init", "arif_session_init"],
  "aliases": {"arif_session_init": "arif_init"},
  "exported": ["arif_init"]
}
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read valid JSON from {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("input root must be a JSON object")
    return data


def string_set(data: dict[str, Any], key: str) -> set[str]:
    value = data.get(key, [])
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{key} must be a list of strings")
    return set(value)


def audit(data: dict[str, Any]) -> dict[str, Any]:
    canonical = string_set(data, "canonical")
    live = string_set(data, "live")
    exported = string_set(data, "exported")
    aliases_raw = data.get("aliases", {})
    if not isinstance(aliases_raw, dict) or not all(
        isinstance(k, str) and isinstance(v, str) for k, v in aliases_raw.items()
    ):
        raise ValueError("aliases must be an object mapping string alias to canonical string")

    aliases = dict(aliases_raw)
    visible_aliases = sorted(alias for alias in aliases if alias in live or alias in exported)
    broken_aliases = sorted(
        alias for alias, target in aliases.items() if target not in canonical
    )
    missing_live = sorted(canonical - live)
    phantom_live = sorted(live - canonical - set(aliases))
    missing_export = sorted(canonical - exported)
    export_only = sorted(exported - live)

    status = "PASS"
    if missing_live or phantom_live or broken_aliases:
        status = "DRIFT"
    elif missing_export or visible_aliases or export_only:
        status = "PARTIAL"

    return {
        "status": status,
        "counts": {
            "canonical": len(canonical),
            "live": len(live),
            "exported": len(exported),
            "aliases": len(aliases),
        },
        "missing_live": missing_live,
        "phantom_live": phantom_live,
        "missing_export": missing_export,
        "export_only": export_only,
        "visible_aliases": visible_aliases,
        "broken_aliases": broken_aliases,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON surface description")
    parser.add_argument("--output", type=Path, help="optional output JSON path")
    args = parser.parse_args()

    try:
        result = audit(load_json(args.input))
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
