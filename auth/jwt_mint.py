#!/usr/bin/env python3
"""
arifOS Federation JWT Minting Service
Mints JWT tokens for agentgateway CEL authorization.

Usage:
  python3 jwt_mint.py --agent 333-AGI --approval-id apr-001 --approval-status granted

Output: JWT token to stdout

Architecture:
  arif_judge returns SEAL → this script mints JWT with approval_id →
  agentgateway validates JWT against CEL rules → tool executes
"""

import json, time, argparse, sys, os
import jwt  # PyJWT

KEYS_DIR = "/root/AAA/auth/keys"
PRIVATE_KEY_PATH = os.path.join(KEYS_DIR, "arifos-federation-private.pem")
KID = "arifos-federation-2026-09-04"
ISSUER = "arifos.dev"
AUDIENCE = "federation.arif-fazil.com"


def mint_token(
    agent: str,
    approval_id: str = None,
    approval_status: str = "pending",
    approval_expires_in: int = 7200,
    g_score: float = None,
    w3_score: float = None,
    sovereign_ack: bool = False,
    epistemic_label: str = None,
    entropy_delta: float = None,
    ttl: int = 3600,
) -> str:
    """Mint a JWT for agentgateway authorization."""
    with open(PRIVATE_KEY_PATH, "rb") as f:
        private_key = f.read()

    now = int(time.time())
    payload = {
        "sub": agent,
        "agent": agent,
        "iss": ISSUER,
        "aud": AUDIENCE,
        "iat": now,
        "exp": now + ttl,
        "nbf": now,
        "sid": f"SEAL-{now}",
    }

    if approval_id:
        payload["approval_id"] = approval_id
        payload["approval_status"] = approval_status
        payload["approval_expires_at"] = now + approval_expires_in

    if g_score is not None:
        payload["g_score"] = g_score
    if w3_score is not None:
        payload["w3_score"] = w3_score
    if sovereign_ack:
        payload["sovereign_ack"] = True
    if epistemic_label:
        payload["epistemic_label"] = epistemic_label
    if entropy_delta is not None:
        payload["entropy_delta"] = entropy_delta

    token = jwt.encode(
        payload,
        private_key,
        algorithm="RS256",
        headers={"kid": KID},
    )
    return token


def main():
    parser = argparse.ArgumentParser(description="Mint arifOS federation JWT")
    parser.add_argument("--agent", help="Agent ID (e.g., 333-AGI)")
    parser.add_argument("--approval-id", help="Approval ID from arif_judge SEAL")
    parser.add_argument("--approval-status", default="pending", help="Approval status")
    parser.add_argument("--approval-expires-in", type=int, default=7200)
    parser.add_argument("--g-score", type=float, help="G score (F8 GENIUS)")
    parser.add_argument("--w3-score", type=float, help="W3 tri-witness score")
    parser.add_argument("--sovereign-ack", action="store_true", help="F13 sovereign acknowledgment")
    parser.add_argument("--epistemic-label", help="Epistemic label (OBS/DER/INT/SPEC)")
    parser.add_argument("--entropy-delta", type=float, help="Entropy delta (F4 CLARITY)")
    parser.add_argument("--ttl", type=int, default=3600, help="Token TTL in seconds")
    parser.add_argument("--verify", help="Verify a JWT token instead of minting")
    args = parser.parse_args()

    if args.verify:
        # Verify mode
        with open(os.path.join(KEYS_DIR, "jwks.json")) as f:
            jwks = json.load(f)
        from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
        from cryptography.hazmat.backends import default_backend
        import base64

        def b64url_decode(s):
            s += "=" * (4 - len(s) % 4)
            return base64.urlsafe_b64decode(s)

        key_data = jwks["keys"][0]
        n = int.from_bytes(b64url_decode(key_data["n"]), "big")
        e = int.from_bytes(b64url_decode(key_data["e"]), "big")
        pub_key = RSAPublicNumbers(e, n).public_key(default_backend())

        decoded = jwt.decode(
            args.verify,
            pub_key,
            algorithms=["RS256"],
            audience=AUDIENCE,
            issuer=ISSUER,
        )
        print(json.dumps(decoded, indent=2))
    else:
        # Mint mode
        token = mint_token(
            agent=args.agent,
            approval_id=args.approval_id,
            approval_status=args.approval_status,
            approval_expires_in=args.approval_expires_in,
            g_score=args.g_score,
            w3_score=args.w3_score,
            sovereign_ack=args.sovereign_ack,
            epistemic_label=args.epistemic_label,
            entropy_delta=args.entropy_delta,
            ttl=args.ttl,
        )
        print(token)


if __name__ == "__main__":
    main()
