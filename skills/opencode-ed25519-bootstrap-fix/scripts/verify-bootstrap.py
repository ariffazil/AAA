#!/usr/bin/env python3
"""End-to-end Ed25519 bootstrap verification for a federation agent.

Tests the FULL chain (10 checks). Refuses partial success.

  1. Key files exist (seed + PEM + identity.json)
  2. pubkey consistent across PEM + keypair derivation
  3. NO stale lowercase PEM variant exists (Pitfall 9 trap)
  4. identity.key mode is 600
  5. kernel.resolve_actor_public_key() returns matching pubkey
  6. kernel.is_registered_actor() returns True
  7. arif_init(challenge) returns nonce
  8. arif_init(init, signed) returns session_token
  9. mutation_allowed=True + authority_band=LIMITED_MUTATE
 10. arif_judge does NOT return HTTP 406

Usage:
  python3 scripts/verify-bootstrap.py                    # default actor_id="333-AGI", seed at /root/AAA/agents/opencode
  python3 scripts/verify-bootstrap.py --actor <id> --agent-dir <path>

Exit 0 = fully bound, MUTATE-capable. Exit 1 = bootstrap broken at a specific step.
"""
import argparse
import base64
import json
import re
import subprocess
import sys
import time
from pathlib import Path

import requests
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PublicFormat,
    load_pem_public_key,
)


CHECKS = []
def check(name: str, ok: bool, detail: str = ""):
    icon = "✅" if ok else "❌"
    print(f"  {icon} {name}" + (f" — {detail}" if detail else ""))
    CHECKS.append((name, ok))
    return ok


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--actor", default="333-AGI")
    p.add_argument("--agent-dir", default="/root/AAA/agents/opencode")
    p.add_argument("--mcp", default="http://127.0.0.1:8088/mcp")
    p.add_argument("--kernel-path", default="/opt/arifos/app",
                   help="Path where the LIVE arifOS kernel is loaded from")
    args = p.parse_args()

    actor = args.actor
    seed_path = Path(args.agent_dir) / "identity.key"
    pem_canonical = Path("/root/AAA/IDENTITY/keys") / f"{actor}_public.pem"
    pem_lower = Path("/root/AAA/IDENTITY/keys") / f"{actor.lower()}_public.pem"

    print(f"\n=== Bootstrap verification: actor_id={actor} ===\n")

    # 1. Files exist
    check("identity.key exists", seed_path.exists(), str(seed_path))
    check("canonical PEM exists", pem_canonical.exists(), str(pem_canonical))
    if not (seed_path.exists() and pem_canonical.exists()):
        return fail_summary()

    # 2. pubkey consistent
    seed = seed_path.read_bytes()
    priv = ed25519.Ed25519PrivateKey.from_private_bytes(seed)
    derived_pub = priv.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw).hex()
    pem_pub = load_pem_public_key(pem_canonical.read_bytes()).public_bytes(
        Encoding.Raw, PublicFormat.Raw
    ).hex()
    check("derived pubkey matches canonical PEM",
          derived_pub == pem_pub,
          f"derived={derived_pub[:16]} vs pem={pem_pub[:16]}")

    # 3. NO stale lowercase variant (Pitfall 9)
    if pem_lower.exists():
        lower_pub = load_pem_public_key(pem_lower.read_bytes()).public_bytes(
            Encoding.Raw, PublicFormat.Raw
        ).hex()
        stale = (lower_pub != derived_pub)
        check("lowercase PEM is not stale", not stale,
              f"lowercase contains stale key — overwrite or delete")
        if stale:
            return fail_summary()
    else:
        check("no lowercase PEM variant", True, "skip (no lowercase file)")

    # 4. identity.key mode 600
    import stat
    mode = seed_path.stat().st_mode & 0o777
    check("identity.key mode is 600", mode == 0o600, f"actual={oct(mode)}")

    # 5. Kernel resolves actor + 6. is_registered_actor
    resolve_script = f"""
import sys
sys.path.insert(0, '{args.kernel_path}')
from arifosmcp.runtime.crypto_auth import resolve_actor_public_key, is_registered_actor
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
key = resolve_actor_public_key('{actor}')
if key:
    raw = key.public_bytes(Encoding.Raw, PublicFormat.Raw).hex()
    print('PUB:' + raw)
print('REG:' + ('1' if is_registered_actor('{actor}') else '0'))
"""
    r = subprocess.run(["python3", "-c", resolve_script],
                       capture_output=True, text=True, timeout=15)
    out = r.stdout
    pub_match = re.search(r"PUB:([a-f0-9]+)", out)
    reg_match = re.search(r"REG:([01])", out)

    kernel_pub = pub_match.group(1) if pub_match else ""
    is_reg = reg_match.group(1) == "1" if reg_match else False
    check("kernel resolves actor to derived pubkey", kernel_pub == derived_pub,
          f"kernel={kernel_pub[:16] or 'NONE'} vs derived={derived_pub[:16]}")
    check("kernel.is_registered_actor() returns True", is_reg)

    if not (kernel_pub == derived_pub and is_reg):
        return fail_summary()

    # 7-9. MCP challenge → sign → init
    def mcp(method: str, args_dict: dict) -> dict:
        body = {"jsonrpc": "2.0", "id": str(time.time()),
                "method": "tools/call",
                "params": {"name": method, "arguments": args_dict}}
        rr = requests.post(args.mcp, json=body,
                           headers={"Accept": "application/json, text/event-stream"},
                           timeout=15)
        j = rr.json()
        result = j.get("result", {})
        content = result.get("content", [])
        if isinstance(content, list) and content:
            text = content[0].get("text", "")
            if isinstance(text, str):
                try:
                    return json.loads(text)
                except Exception:
                    return text
        return result

    c = mcp("arif_init", {"mode": "challenge", "actor_id": actor})
    nonce = c.get("result", {}).get("nonce") if isinstance(c, dict) else None
    check("arif_init(challenge) returns nonce", bool(nonce),
          f"nonce={nonce[:24] if nonce else 'NONE'}...")

    if not nonce:
        return fail_summary()

    sig = priv.sign(f"{actor}:{nonce}".encode())
    sig_b64 = base64.b64encode(sig).decode()

    r = mcp("arif_init", {
        "mode": "light",
        "actor_id": actor,
        "actor_signature": sig_b64,
        "nonce": nonce,
        "requested_authority": "FULL",
        "verbosity": "minimal",
    })
    res = r.get("result", {}) if isinstance(r, dict) else {}

    st = res.get("session_token")
    ma = res.get("mutation_allowed")
    band = res.get("authority_band")

    check("arif_init(init, signed) returns session_token", bool(st),
          f"prefix={str(st)[:16] if st else 'NONE'}")
    check("mutation_allowed is True", ma is True, f"value={ma}")
    check("authority_band is LIMITED_MUTATE", band == "LIMITED_MUTATE", f"value={band}")

    if not (bool(st) and ma is True and band == "LIMITED_MUTATE"):
        return fail_summary()

    # 10. arif_judge does NOT 406
    jr = requests.post(args.mcp, json={
        "jsonrpc": "2.0", "id": "judge", "method": "tools/call",
        "params": {"name": "arif_judge",
                   "arguments": {"tool": "forge_shell", "actor_id": actor}},
    }, headers={"Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"}, timeout=10)
    check("arif_judge does not return HTTP 406",
          jr.status_code != 406, f"actual HTTP {jr.status_code}")

    return fail_summary()


def fail_summary() -> int:
    passed = sum(1 for _, ok in CHECKS if ok)
    total = len(CHECKS)
    print(f"\n{'🎉 FULLY BOUND' if passed == total else '⚠️  BROKEN'} — {passed}/{total} checks passed")
    if passed != total:
        print("\nFailing checks:")
        for name, ok in CHECKS:
            if not ok:
                print(f"  ❌ {name}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
