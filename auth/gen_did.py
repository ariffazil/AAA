#!/usr/bin/env python3
"""
gen_did.py — One-time Ed25519 DID keypair generator for the arifOS federation.

Run ONCE per organ. Private keys are stored in auth/keys/ (gitignored).
Public keys are committed to auth/did_registry.yaml.

Usage:
    python auth/gen_did.py               # generate missing keys only
    python auth/gen_did.py --list        # show DID registry
    python auth/gen_did.py --force       # regenerate ALL (DANGER: breaks existing signatures)
    python auth/gen_did.py --sign <hex>  # sign hex data with did:arif:aaa (test)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey, VerifyKey

KEYS_DIR = Path(__file__).parent / "keys"
REGISTRY_FILE = Path(__file__).parent / "did_registry.yaml"

# Canonical organ DIDs — ordered by authority (Ω is root of trust)
ORGANS: list[tuple[str, str, str]] = [
    ("omega",   "did:arif:Ω",       "Sovereign root — F13-issuer, capability token signer"),
    ("aaa",     "did:arif:aaa",     "AAA control plane — signs ingress capsules, issues capability tokens"),
    ("a-forge", "did:arif:a-forge", "A-FORGE execution — signs skill step receipts"),
    ("geox",    "did:arif:geox",    "GEOX domain — signs petrophysics and subsurface outputs"),
    ("wealth",  "did:arif:wealth",  "WEALTH capital — signs economic verdicts and NPV claims"),
    ("well",    "did:arif:well",    "WELL vitality — signs substrate assessments"),
    ("hermes",  "did:arif:hermes",  "HERMES relay — signs A2A envelope routing"),
    ("arifos",  "did:arif:arifos",  "arifOS kernel — signs constitutional verdicts (SEAL/HOLD/VOID)"),
]


def _load_or_generate(organ_id: str, did: str, force: bool = False) -> tuple[SigningKey, dict]:
    priv_path = KEYS_DIR / f"{organ_id}_private.key"
    pub_path  = KEYS_DIR / f"{organ_id}_public.key"

    if priv_path.exists() and not force:
        sk = SigningKey(priv_path.read_text().strip(), encoder=HexEncoder)
        action = "EXISTS"
    else:
        action = "REGENERATED" if priv_path.exists() else "GENERATED"
        sk = SigningKey.generate()
        KEYS_DIR.mkdir(exist_ok=True)
        priv_path.write_text(sk.encode(encoder=HexEncoder).decode())
        pub_path.write_text(sk.verify_key.encode(encoder=HexEncoder).decode())

    vk = sk.verify_key
    print(f"  [{action:11s}] did:arif:{organ_id}")
    return sk, {
        "did": did,
        "organ_id": organ_id,
        "public_key_hex": vk.encode(encoder=HexEncoder).decode(),
        "algorithm": "Ed25519",
    }


def load_signing_key(organ_id: str) -> SigningKey:
    """Load an organ's private key for runtime signing."""
    priv_path = KEYS_DIR / f"{organ_id}_private.key"
    if not priv_path.exists():
        raise FileNotFoundError(
            f"Private key for '{organ_id}' not found at {priv_path}. "
            "Run: python auth/gen_did.py"
        )
    return SigningKey(priv_path.read_text().strip(), encoder=HexEncoder)


def load_verify_key(organ_id: str) -> VerifyKey:
    """Load an organ's public key for runtime verification."""
    registry = load_registry()
    for entry in registry.get("dids", []):
        if entry["organ_id"] == organ_id:
            return VerifyKey(entry["public_key_hex"], encoder=HexEncoder)
    raise KeyError(f"organ '{organ_id}' not found in did_registry.yaml")


def load_registry() -> dict:
    if not REGISTRY_FILE.exists():
        raise FileNotFoundError(
            f"DID registry not found at {REGISTRY_FILE}. Run: python auth/gen_did.py"
        )
    return yaml.safe_load(REGISTRY_FILE.read_text()) or {}


def sign(data: bytes, organ_id: str = "aaa") -> str:
    """Sign data with an organ's private key. Returns hex signature."""
    sk = load_signing_key(organ_id)
    signed = sk.sign(data)
    return signed.signature.hex()


def verify(data: bytes, signature_hex: str, organ_id: str) -> bool:
    """Verify an Ed25519 signature against an organ's public key."""
    try:
        vk = load_verify_key(organ_id)
        vk.verify(data, bytes.fromhex(signature_hex))
        return True
    except Exception:
        return False


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    parser = argparse.ArgumentParser(description="arifOS DID keypair generator")
    parser.add_argument("--force",  action="store_true",
                        help="Regenerate ALL keys (DANGER: invalidates existing signatures)")
    parser.add_argument("--list",   action="store_true", help="Show DID registry")
    parser.add_argument("--sign",   metavar="HEX_DATA",
                        help="Sign hex-encoded data with did:arif:aaa (smoke test)")
    args = parser.parse_args()

    if args.list:
        if not REGISTRY_FILE.exists():
            print("Registry not found. Run: python auth/gen_did.py")
            sys.exit(1)
        reg = load_registry()
        print(f"\nDID Registry v{reg.get('version', '?')} — {len(reg.get('dids', []))} organs\n")
        for entry in reg.get("dids", []):
            pub = entry['public_key_hex'][:16] + "…"
            print(f"  {entry['did']:30s}  {pub}  [{entry['algorithm']}]")
        return

    if args.sign:
        data = bytes.fromhex(args.sign)
        sig = sign(data, "aaa")
        ok  = verify(data, sig, "aaa")
        print(f"signature : {sig}")
        print(f"verified  : {ok}")
        return

    if args.force:
        print("WARNING: --force regenerates ALL keys. Existing capsule signatures become unverifiable.")
        confirm = input("Type 'yes' to continue: ").strip()
        if confirm != "yes":
            print("Aborted.")
            sys.exit(0)

    KEYS_DIR.mkdir(exist_ok=True)

    # Write .gitignore inside keys/ — belt and braces
    gi = KEYS_DIR / ".gitignore"
    if not gi.exists():
        gi.write_text("*_private.key\n")

    print("\nGenerating DID keypairs:")
    registry: dict = {
        "version": "1.0",
        "note": "Public keys only. Private keys in auth/keys/ (gitignored — never commit).",
        "dids": [],
    }

    for organ_id, did, description in ORGANS:
        _, entry = _load_or_generate(organ_id, did, force=args.force)
        entry["description"] = description
        registry["dids"].append(entry)

    REGISTRY_FILE.write_text(yaml.dump(registry, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"\nPublic registry  : auth/did_registry.yaml  (commit this)")
    print(f"Private keys     : auth/keys/               (gitignored — never commit)")
    print("\nSmoke test: python auth/gen_did.py --sign deadbeef")


if __name__ == "__main__":
    main()
