#!/usr/bin/env python3
"""Render the tracked DID projection from the runtime DID store.

One owner: `secrets/did/registry.json` (gitignored, public keys only in practice).
One projection: `auth/did_registry.yaml` (tracked, public keys only — never private).

The gate reads the projection; the A2A verifier reads the runtime store. This script
keeps them from drifting. It refuses to write if any private-key material is present.

Usage:
    python3 scripts/render-did-projection.py [--check]

--check exits 1 if the tracked projection differs from the runtime store.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
RUNTIME = Path(os.environ.get("DID_REGISTRY_PATH", "/root/AAA/secrets/did/registry.json"))
PROJECTION = ROOT / "auth" / "did_registry.yaml"

# Only public metadata may cross the boundary.
ALLOWED = ("did", "organ_id", "public_key_hex", "algorithm", "description", "actors")


def load_runtime() -> dict:
    data = json.loads(RUNTIME.read_text())
    dids = data.get("dids") or {}
    if not isinstance(dids, dict):
        raise SystemExit("runtime store: `dids` must be an object")
    for did, entry in dids.items():
        for key in entry:
            if "private" in key.lower() or "secret" in key.lower():
                raise SystemExit(f"refusing: private material in {did}.{key}")
    return data


def project(data: dict) -> dict:
    dids = []
    for did in sorted(data.get("dids") or {}):
        src = data["dids"][did]
        entry = {"did": did}
        for key in ALLOWED[1:]:
            if key in src and src[key] not in (None, ""):
                entry[key] = src[key]
        entry.setdefault("algorithm", "Ed25519")
        dids.append(entry)
    return {
        "version": "1.0",
        "note": (
            "Public keys only. Projection of secrets/did/registry.json — "
            "regenerate with scripts/render-did-projection.py. Never commit private keys."
        ),
        "generated_from": "secrets/did/registry.json",
        "dids": dids,
    }


def main() -> int:
    data = load_runtime()
    rendered = project(data)
    text = yaml.safe_dump(rendered, sort_keys=False, allow_unicode=True, width=100)
    if "--check" in sys.argv:
        current = PROJECTION.read_text() if PROJECTION.exists() else ""
        if current != text:
            print("DRIFT: tracked DID projection differs from runtime store", file=sys.stderr)
            return 1
        print("OK: tracked DID projection matches runtime store")
        return 0
    PROJECTION.write_text(text)
    print(f"wrote {PROJECTION} ({len(rendered['dids'])} DIDs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
