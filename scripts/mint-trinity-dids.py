#!/usr/bin/env python3
"""Mint the three Trinity principals — an F13 custody act, not CI.

Dry-run by default: generates ephemeral keys, prints the public identity, writes nothing.
--apply requires --i-have-custody and an --out directory OUTSIDE the repo; private keys
are written mode 0600 there and are never committed. The repo receives only the public
registry fragment printed by this tool.

Usage:
    python3 scripts/mint-trinity-dids.py
    python3 scripts/mint-trinity-dids.py --apply --i-have-custody --out /root/.secrets/trinity-dids

Why: did:arif:aaa currently covers 22 actor names including 333-AGI, 555-ASI and 888-APEX.
Three constitutional lanes (propose / verify / judge) share one principal, so a signature
proves "the AAA organ", not which lane signed. This tool exists so the split is a deliberate
custody ceremony, never a script run inside CI.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

LANES = {
    "333-AGI": "propose",
    "555-ASI": "verify",
    "888-APEX": "judge",
}


def main() -> int:
    ap = argparse.ArgumentParser(description="Mint Trinity principals (dry-run by default)")
    ap.add_argument("--out", help="directory OUTSIDE the repo for private keys")
    ap.add_argument("--i-have-custody", action="store_true")
    ap.add_argument("--apply", action="store_true", help="write keys (default: dry-run)")
    args = ap.parse_args()

    repo = Path(__file__).resolve().parent.parent
    out = None
    if args.apply:
        if not args.i_have_custody or not args.out:
            print("refusing: --apply requires --i-have-custody and --out", file=sys.stderr)
            return 2
        out = Path(args.out).resolve()
        if out == repo or repo in out.parents:
            print("refusing: --out must be outside the repo", file=sys.stderr)
            return 2
        out.mkdir(parents=True, exist_ok=True)
        os.chmod(out, 0o700)

    fragment = {
        "version": "1.0",
        "note": "Trinity principals — F13 custody. Public keys only; private keys stay outside the repo.",
        "dids": [],
    }

    for lane, role in LANES.items():
        key = Ed25519PrivateKey.generate()
        seed = key.private_bytes(
            serialization.Encoding.Raw,
            serialization.PrivateFormat.Raw,
            serialization.NoEncryption(),
        )
        pub = key.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
        did = f"did:arif:trinity:{lane.lower()}"
        fragment["dids"].append(
            {
                "did": did,
                "organ_id": lane,
                "public_key_hex": pub.hex(),
                "algorithm": "Ed25519",
                "description": f"Trinity {role} lane — {lane}",
                "actors": [lane],
            }
        )
        print(f"{lane:8} {role:7} pub={pub.hex()[:16]}… did={did}")
        if args.apply:
            p = out / f"{lane}.private.key"  # type: ignore[operator]
            p.write_text(seed.hex())
            os.chmod(p, 0o600)

    if args.apply:
        (out / "trinity-dids.registry.fragment.json").write_text(  # type: ignore[operator]
            json.dumps(fragment, indent=2) + "\n"
        )
        print(f"wrote 3 private keys + fragment to {out} (mode 0700/0600)")
    else:
        print("dry-run: nothing written. Re-run with --apply --i-have-custody --out <dir-outside-repo>.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
