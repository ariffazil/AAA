#!/usr/bin/env python3
"""Sync /root/arifOS/arifos/identity/agent_registry.json

Re-derives pubkey_hex from PEM files and recomputes blake3 fingerprints.
Verifies from disk (not in-memory) after write.
Exits non-zero on any verification failure.

Usage:
    python3 scripts/sync_agent_registry_fingerprints.py [--dry-run]
"""

import json, os, glob, sys
from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key, Encoding, PublicFormat
)
import blake3

REGISTRY_PATH = "/root/arifOS/arifos/identity/agent_registry.json"
KEYS_DIR = "/root/AAA/IDENTITY/keys"
DRY_RUN = "--dry-run" in sys.argv


def pubkey_hex_from_pem(pem_path):
    with open(pem_path, "rb") as f:
        key = load_pem_public_key(f.read())
    return key.public_bytes(encoding=Encoding.Raw, format=PublicFormat.Raw).hex()


def compute_fingerprint(agent_id, actor_id, pubkey_hex, bound_to):
    canonical = f"{agent_id}|{actor_id}|{pubkey_hex}|{bound_to}"
    return blake3.blake3(canonical.encode()).hexdigest()[:32]


def main():
    # 1. Load registry
    with open(REGISTRY_PATH) as f:
        registry = json.load(f)
    agents = registry["agents"]
    print(f"Registry: {len(agents)} agents")

    # 2. Map PEM files
    pem_files = {}
    for p in glob.glob(os.path.join(KEYS_DIR, "*_public.pem")):
        name = os.path.basename(p).replace("_public.pem", "")
        pem_files[name] = p
    print(f"PEM files: {len(pem_files)}")

    # 3. Fix each agent
    fixed = 0
    skipped = 0
    for name, agent in agents.items():
        pem_path = pem_files.get(name)
        if not pem_path:
            skipped += 1
            continue

        new_pk = pubkey_hex_from_pem(pem_path)
        new_fp = compute_fingerprint(
            agent["agent_id"], agent["actor_id"], new_pk, agent["bound_to"]
        )

        old_pk = agent.get("pubkey_hex", "")
        old_fp = agent.get("fingerprint", "")

        if new_pk == old_pk and new_fp == old_fp:
            continue

        print(f"FIX  {name}: pk {'UPDATED' if new_pk != old_pk else 'same'} | "
              f"fp {old_fp[:8]}.. -> {new_fp[:8]}..")
        agent["pubkey_hex"] = new_pk
        agent["fingerprint"] = new_fp
        agent["needs_keygen"] = False
        fixed += 1

    if fixed == 0:
        print("All fingerprints already correct.")
    elif DRY_RUN:
        print(f"\n[DRY RUN] Would fix {fixed} entries. No write performed.")
        return

    # 4. Write
    with open(REGISTRY_PATH, "w") as f:
        json.dump(registry, f, indent=2)
        f.write("\n")
    print(f"\nWrote {REGISTRY_PATH}")

    # 5. VERIFY FROM DISK - DO NOT trust in-memory
    with open(REGISTRY_PATH) as f:
        verify = json.load(f)

    errors = []
    pubkeys_seen = set()
    fps_seen = set()

    for name, agent in verify["agents"].items():
        expected = compute_fingerprint(
            agent["agent_id"], agent["actor_id"],
            agent["pubkey_hex"], agent["bound_to"]
        )
        if agent["fingerprint"] != expected:
            errors.append(f"FP_MISMATCH {name}: stored={agent['fingerprint'][:12]}.. "
                          f"expected={expected[:12]}..")

        pk = agent["pubkey_hex"]
        fp = agent["fingerprint"]
        if pk in pubkeys_seen:
            errors.append(f"PUBKEY_COLLISION {name} with {pubkeys_seen[pk]}")
        pubkeys_seen.add(pk)
        if fp in fps_seen:
            errors.append(f"FP_COLLISION {name} with {fps_seen[fp]}")
        fps_seen.add(fp)

    print(f"\nVerify from disk: {len(verify['agents'])} agents")
    if errors:
        for e in errors:
            print(f"  X {e}")
        sys.exit(1)
    else:
        print(f"  OK {len(pubkeys_seen)} unique pubkeys, "
              f"{len(fps_seen)} unique fingerprints, all match blake3")
        print("PASS")


if __name__ == "__main__":
    main()
