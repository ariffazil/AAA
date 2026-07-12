#!/usr/bin/env python3
"""
sign_agent_card.py — Ed25519 sign A2A Agent Cards for the arifOS federation.

Reads a card JSON, canonicalises it, signs with the issuing organ's
Ed25519 private key from auth/keys/, and writes the card back with
a `signatures` array added.

Each signature follows the A2A v1.2 pattern:
  {
    "did": "did:arif:aaa",
    "proofValue": "<base64-signature>",
    "proofPurpose": "assertionMethod",
    "created": "<ISO-8601>",
    "type": "Ed25519Signature2020"
  }

Usage:
    python auth/sign_agent_card.py <card.json>              # sign one card
    python auth/sign_agent_card.py --all                    # sign all cards
    python auth/sign_agent_card.py --verify <card.json>     # verify card signatures
    python auth/sign_agent_card.py --verify-all             # verify all cards
"""

from __future__ import annotations

import argparse
import base64
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey, VerifyKey

ROOT = Path(__file__).parent.parent
KEYS_DIR = Path(__file__).parent / "keys"
REGISTRY_FILE = Path(__file__).parent / "did_registry.yaml"
CARDS_DIR = ROOT / "a2a-server" / "agent-cards"
SIGNING_DID = "did:arif:aaa"  # AAA gateway is the card issuer


def load_registry() -> dict[str, str]:
    """Load DID → public_key_hex mapping."""
    data = yaml.safe_load(REGISTRY_FILE.read_text())
    return {d["did"]: d["public_key_hex"] for d in data["dids"]}


def load_private_key(did: str) -> bytes:
    """Load the Ed25519 private key (32-byte seed) for a DID."""
    organ_map = {
        "did:arif:Ω": "omega",
        "did:arif:aaa": "aaa",
        "did:arif:a-forge": "a-forge",
        "did:arif:geox": "geox",
        "did:arif:wealth": "wealth",
        "did:arif:well": "well",
        "did:arif:hermes": "hermes",
        "did:arif:arifos": "arifos",
    }
    organ_id = organ_map.get(did)
    if not organ_id:
        raise ValueError(f"No organ mapping for DID {did}")

    key_file = KEYS_DIR / f"{organ_id}_private.key"
    if not key_file.exists():
        raise FileNotFoundError(f"Private key not found: {key_file}")

    hex_str = key_file.read_text().strip()
    return bytes.fromhex(hex_str)


def canonicalise(obj: dict) -> bytes:
    """Canonical JSON: sorted keys, no whitespace, UTF-8."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sign_card(card_path: Path, did: str = SIGNING_DID) -> dict:
    """Sign a card and return the updated card dict."""
    card = json.loads(card_path.read_text())

    # Remove existing signatures for re-signing
    if "signatures" in card:
        del card["signatures"]

    # Canonicalise the card (minus signatures)
    payload = canonicalise(card)

    # Sign
    seed = load_private_key(did)
    signing_key = SigningKey(seed)
    signed = signing_key.sign(payload)
    signature_bytes = signed.signature  # 64-byte Ed25519 signature
    proof_value = base64.b64encode(signature_bytes).decode("ascii")

    # Add signature
    card["signatures"] = [
        {
            "did": did,
            "proofValue": proof_value,
            "proofPurpose": "assertionMethod",
            "created": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "type": "Ed25519Signature2020",
        }
    ]

    return card


def verify_card(card_path: Path) -> tuple[bool, str]:
    """Verify all signatures on a card. Returns (valid, reason)."""
    card = json.loads(card_path.read_text())
    sigs = card.get("signatures", [])

    if not sigs:
        return False, "No signatures found"

    registry = load_registry()

    # Remove signatures for payload verification
    card_without_sigs = {k: v for k, v in card.items() if k != "signatures"}
    payload = canonicalise(card_without_sigs)

    for sig in sigs:
        did = sig.get("did", "")
        proof_value = sig.get("proofValue", "")
        pub_hex = registry.get(did)

        if not pub_hex:
            return False, f"Unknown DID: {did}"

        try:
            sig_bytes = base64.b64decode(proof_value)
            verify_key = VerifyKey(pub_hex, encoder=HexEncoder)
            verify_key.verify(payload, sig_bytes)
        except Exception as e:
            return False, f"Signature verification failed for {did}: {e}"

    return True, f"All {len(sigs)} signature(s) valid"


def find_all_cards() -> list[Path]:
    """Find all JSON cards in agent-cards/ (recursive)."""
    cards = []
    for p in CARDS_DIR.rglob("*.json"):
        cards.append(p)
    return sorted(cards)


def main():
    parser = argparse.ArgumentParser(description="Sign A2A Agent Cards with Ed25519")
    parser.add_argument("card", nargs="?", help="Card JSON file to sign")
    parser.add_argument("--all", action="store_true", help="Sign all cards in agent-cards/")
    parser.add_argument("--verify", metavar="CARD", help="Verify signatures on a card")
    parser.add_argument("--verify-all", action="store_true", help="Verify all cards")
    parser.add_argument("--did", default=SIGNING_DID, help=f"DID to sign with (default: {SIGNING_DID})")
    args = parser.parse_args()

    if args.verify:
        card_path = Path(args.verify)
        if not card_path.exists():
            print(f"Error: {card_path} not found")
            sys.exit(1)
        valid, reason = verify_card(card_path)
        if valid:
            print(f"✅ {card_path.name}: {reason}")
        else:
            print(f"❌ {card_path.name}: {reason}")
            sys.exit(1)
        return

    if args.verify_all:
        all_cards = find_all_cards()
        passed = 0
        failed = 0
        for card_path in all_cards:
            valid, reason = verify_card(card_path)
            if valid:
                print(f"✅ {card_path.name}: {reason}")
                passed += 1
            else:
                print(f"❌ {card_path.name}: {reason}")
                failed += 1
        print(f"\n{passed} passed, {failed} failed out of {len(all_cards)}")
        sys.exit(1 if failed > 0 else 0)
        return

    if args.all:
        all_cards = find_all_cards()
        print(f"Signing {len(all_cards)} cards with {args.did}...")
        for card_path in all_cards:
            try:
                signed = sign_card(card_path, args.did)
                card_path.write_text(json.dumps(signed, indent=2) + "\n")
                print(f"  ✅ {card_path.name}")
            except Exception as e:
                print(f"  ❌ {card_path.name}: {e}")
        print("Done.")
        return

    if args.card:
        card_path = Path(args.card)
        if not card_path.exists():
            print(f"Error: {card_path} not found")
            sys.exit(1)
        signed = sign_card(card_path, args.did)
        card_path.write_text(json.dumps(signed, indent=2) + "\n")
        print(f"✅ Signed {card_path.name} with {args.did}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
