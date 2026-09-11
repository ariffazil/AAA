#!/usr/bin/env python3
"""SEAL replay verifier for SEAL-ARIFOS_CONSTITUTIONAL_STRESS_TEST_V1-*.

Verifies, in order:
  1. Every artifact hash in witness.artifact_hashes matches the file on disk.
  2. Every ritual marker chain_hash in witness.witness_markers is present in
     /root/.arifos/ritual.log with the matching label.
  3. The Ed25519 signature over the canonical envelope verifies against the
     vault-signing-ed25519 public key.
  4. The test suite still passes.

Exit 0 = replayable. Non-zero = first failing step.

Usage:
  verify_stress_seal.py [path/to/SEAL-ARIFOS_CONSTITUTIONAL_STRESS_TEST_V1-*.json]
"""
import base64
import hashlib
import json
import os
import subprocess
import sys

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

PUB_KEY = "/root/.secrets/vault-signing-ed25519.pub"
RITUAL  = "/root/.arifos/ritual.log"


def step(label, fn):
    print(f"\n=== {label} ===")
    try:
        ok, detail = fn()
    except Exception as e:
        ok, detail = False, f"raised {type(e).__name__}: {e!r}"
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {detail}")
    return ok


def verify_artifacts(env):
    hashes = env["witness"]["artifact_hashes"]
    failed = []
    for name, h in hashes.items():
        path = h["path"]
        if not os.path.exists(path):
            failed.append(f"{name}: MISSING {path}")
            continue
        actual = hashlib.sha256(open(path, "rb").read()).hexdigest()
        if actual != h["sha256"]:
            failed.append(f"{name}: hash drift (expected {h['sha256']}, got {actual})")
    return (not failed), ("all %d artifacts match" % len(hashes)) if not failed else "; ".join(failed)


def verify_markers(env):
    expected = dict(env["witness"]["witness_markers"])
    found = {}
    for line in open(RITUAL):
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        label = d.get("label")
        ch = d.get("chain_hash")
        if label in expected and expected[label] == ch:
            found[label] = ch
    missing = [k for k in expected if k not in found]
    return (not missing), ("all %d markers found" % len(expected)) if not missing else f"missing: {missing}"


def _load_ed25519_pub(path):
    """The federation vault-signing-ed25519.pub is PEM PKCS#8 SPKI (BEGIN PUBLIC KEY),
    NOT OpenSSH format, despite `file(1)` reporting otherwise. Try both."""
    raw = open(path, "rb").read()
    try:
        k = serialization.load_pem_public_key(raw)
    except Exception:
        k = serialization.load_ssh_public_key(raw)
    return k


def verify_signature(env):
    sig_block = env["signature"]
    if sig_block.get("value_b64") is None:
        return False, f"signature missing: {sig_block.get('error')}"
    pub = _load_ed25519_pub(sig_block["key_path"] + ".pub")
    if not isinstance(pub, Ed25519PublicKey):
        return False, f"public key is {type(pub).__name__}, not Ed25519"
    # Cross-check by deriving pub from priv — catches silent key-rotation
    priv = serialization.load_ssh_private_key(open(sig_block["key_path"], "rb").read(), password=None)
    derived = priv.public_key()
    if derived.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ) != pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ):
        return False, "public key does NOT match the private key (key mismatch / rotation)"
    env_copy = {k: v for k, v in env.items() if k != "signature"}
    canonical = json.dumps(env_copy, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    actual_digest = hashlib.sha256(canonical).hexdigest()
    if actual_digest != sig_block["canonical_sha256"]:
        return False, f"canonical_sha256 drift (recomputed {actual_digest})"
    try:
        pub.verify(base64.b64decode(sig_block["value_b64"]), canonical)
    except InvalidSignature:
        return False, "Ed25519 signature INVALID"
    return True, f"Ed25519 signature valid over canonical_sha256={actual_digest[:16]}"


def verify_tests():
    r = subprocess.run(
        ["python3", "/root/.hermes/hooks/reality-claim-gate/test_phase15.py"],
        capture_output=True, text=True, timeout=120,
    )
    last = [l for l in r.stdout.splitlines() if "RESULT" in l]
    return (r.returncode == 0 and last and "ALL PASS" in last[0]), (
        f"exit={r.returncode} {last[0] if last else 'no RESULT line'}"
    )


def main():
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        candidates = sorted(
            [os.path.join("/root/VAULT999/seals", f) for f in os.listdir("/root/VAULT999/seals")
             if f.startswith("SEAL-ARIFOS_CONSTITUTIONAL_STRESS_TEST_V1-")],
            key=os.path.getmtime, reverse=True,
        )
        if not candidates:
            print("FATAL: no stress-test seal found", file=sys.stderr)
            sys.exit(2)
        path = candidates[0]
    print(f"verifying {path}")
    env = json.load(open(path))
    results = [
        step("ARTIFACT HASHES", lambda: verify_artifacts(env)),
        step("RITUAL MARKERS",  lambda: verify_markers(env)),
        step("ED25519 SIGNATURE", lambda: verify_signature(env)),
        step("TEST SUITE",       lambda: verify_tests()),
    ]
    print("\n" + ("REPLAY OK" if all(results) else "REPLAY FAILED"))
    sys.exit(0 if all(results) else 1)


if __name__ == "__main__":
    main()
