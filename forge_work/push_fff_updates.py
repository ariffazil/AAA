#!/usr/bin/env python3
"""
Push updated FFF files to Hugging Face dataset ariffazil/FFF.

Usage:
    export HF_TOKEN=hf_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    python push_fff_updates.py

Requires:
    pip install huggingface_hub
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

try:
    from huggingface_hub import HfApi, CommitOperationAdd
except ImportError:
    print("Install huggingface_hub: pip install huggingface_hub", file=sys.stderr)
    raise

REPO_ID = "ariffazil/FFF"
COMMIT_MESSAGE = (
    "SEAL(FFF): ILMU demotion verdict v1.1.0 — kernel containment, "
    "linguistic sovereignty failure, architecture honesty collapse | DITEMPA BUKAN DIBERI"
)

FILES_TO_PUSH = {
    "README.md": "FFF-README.md",
    "ilmu_demotion_verdict.json": "FFF-ilmu_demotion_verdict.json",
    "model_status.json": "FFF-model_status.json",
}


def main() -> int:
    token = os.environ.get("HF_TOKEN", "").strip()
    if not token:
        print("Error: HF_TOKEN not set.", file=sys.stderr)
        print("Get a write token from https://huggingface.co/settings/tokens", file=sys.stderr)
        return 1

    api = HfApi(token=token)
    user = api.whoami()
    print(f"Authenticated as: {user['name']}")

    operations = []
    for repo_path, local_path in FILES_TO_PUSH.items():
        local = Path(local_path)
        if not local.exists():
            print(f"Error: {local_path} not found.", file=sys.stderr)
            return 1
        content = local.read_bytes()
        operations.append(CommitOperationAdd(
            path_in_repo=repo_path,
            path_or_fileobj=content,
        ))
        print(f"  + {repo_path} ({len(content):,} bytes)")

    print(f"\nPushing {len(operations)} files to {REPO_ID}...")
    result = api.create_commit(
        repo_id=REPO_ID,
        repo_type="dataset",
        operations=operations,
        commit_message=COMMIT_MESSAGE,
    )
    print(f"\nSuccess: {result.commit_url}")
    print("\nΔ · Ω · Ψ — DITEMPA BUKAN DIBERI — Forged, Not Given.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
