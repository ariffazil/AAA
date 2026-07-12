#!/usr/bin/env python3
"""
SOVEREIGN SIGNATURE VERIFIER
Run by the kernel at boot time to verify the bootstrap manifest signature.
This is the other half of sovereign_sign.sh — the verification side.

Usage:
  python3 sovereign_verify.py                          # Verify bootstrap manifest
  python3 sovereign_verify.py --manifest <path>        # Verify specific manifest
  python3 sovereign_verify.py --key <pub_key_path>     # Use specific public key
"""

import json
import hashlib
import subprocess
import sys
import os
from pathlib import Path

KERNEL_DIR = Path(__file__).parent
MANIFEST_PATH = KERNEL_DIR / "bootstrap_manifest.json"
SIGNATURE_PATH = KERNEL_DIR / "sovereign_signature.json"
PUBLIC_KEY_PATH = Path("/root/.secrets/sovereign/root-arif-888.pub")
BOOT_LOG = KERNEL_DIR / "boot_log.jsonl"

def compute_manifest_hash(manifest_path):
    """Compute canonical SHA-256 hash of manifest."""
    with open(manifest_path, "rb") as f:
        content = f.read()
    return hashlib.sha256(content).hexdigest()

def load_signature(sig_path):
    """Load ratification object."""
    with open(sig_path) as f:
        return json.load(f)

def verify_signature(manifest_hash, signature_data, public_key_path):
    """Verify Ed25519 signature against manifest hash."""
    expected_hash = signature_data.get("manifest_hash", "")
    if expected_hash != f"sha256:{manifest_hash}":
        return {
            "status": "MISMATCH",
            "message": f"Manifest hash mismatch. Expected {expected_hash[:32]}..., got sha256:{manifest_hash[:32]}...",
        }
    
    # Try ssh-keygen verification
    sign_input = "/tmp/sovereign_verify_input"
    sig_file = "/tmp/sovereign_verify_sig"
    
    with open(sign_input, "w") as f:
        f.write(f"sha256:{manifest_hash}")
    with open(sig_file, "w") as f:
        f.write(signature_data.get("signature", ""))
    
    try:
        result = subprocess.run(
            [
                "ssh-keygen", "-Y", "verify",
                "-f", str(public_key_path),
                "-n", "manifest",
                "-s", sig_file,
                sign_input,
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        
        if result.returncode == 0:
            return {"status": "VERIFIED", "message": "Signature is valid."}
        else:
            return {"status": "INVALID", "message": f"Verification failed: {result.stderr.strip()}"}
    except FileNotFoundError:
        return {"status": "ERROR", "message": "ssh-keygen not found. Install OpenSSH."}
    except subprocess.TimeoutExpired:
        return {"status": "ERROR", "message": "Verification timed out."}
    finally:
        for f in [sign_input, sig_file]:
            if os.path.exists(f):
                os.remove(f)

def verify_metadata(signature_data):
    """Verify ratification object metadata."""
    issues = []
    
    if not signature_data.get("ratifier_id"):
        issues.append("Missing ratifier_id")
    if not signature_data.get("timestamp"):
        issues.append("Missing timestamp")
    if not signature_data.get("public_key_fingerprint"):
        issues.append("Missing public_key_fingerprint")
    if signature_data.get("algorithm") != "ed25519":
        issues.append(f"Unexpected algorithm: {signature_data.get('algorithm')}")
    
    return issues

def main():
    manifest_path = MANIFEST_PATH
    key_path = PUBLIC_KEY_PATH
    
    if "--manifest" in sys.argv:
        idx = sys.argv.index("--manifest")
        manifest_path = Path(sys.argv[idx + 1])
    if "--key" in sys.argv:
        idx = sys.argv.index("--key")
        key_path = Path(sys.argv[idx + 1])
    
    print("=" * 60)
    print("  SOVEREIGN SIGNATURE VERIFIER")
    print("=" * 60)
    
    # Check files exist
    if not manifest_path.exists():
        print(f"\n  ❌ Manifest not found: {manifest_path}")
        sys.exit(1)
    if not SIGNATURE_PATH.exists():
        print(f"\n  ❌ Signature not found: {SIGNATURE_PATH}")
        print("  Run sovereign_sign.sh on air-gapped machine first.")
        sys.exit(1)
    if not key_path.exists():
        print(f"\n  ❌ Public key not found: {key_path}")
        print("  Copy public key from air-gapped machine.")
        sys.exit(1)
    
    # Load
    manifest_hash = compute_manifest_hash(manifest_path)
    signature_data = load_signature(SIGNATURE_PATH)
    
    print(f"\n  Manifest: {manifest_path}")
    print(f"  Hash:     sha256:{manifest_hash[:32]}...")
    print(f"  Key:      {key_path}")
    print(f"  Signer:   {signature_data.get('ratifier_id', 'UNKNOWN')}")
    print(f"  Signed:   {signature_data.get('timestamp', 'UNKNOWN')}")
    
    # Verify metadata
    print(f"\n  [1/3] Checking metadata...")
    meta_issues = verify_metadata(signature_data)
    if meta_issues:
        for issue in meta_issues:
            print(f"    ⚠️  {issue}")
    else:
        print(f"    ✅ Metadata complete")
    
    # Verify hash match
    print(f"\n  [2/3] Checking hash match...")
    expected = signature_data.get("manifest_hash", "")
    actual = f"sha256:{manifest_hash}"
    if expected == actual:
        print(f"    ✅ Hash matches")
    else:
        print(f"    ❌ Hash mismatch!")
        print(f"       Expected: {expected[:48]}...")
        print(f"       Actual:   {actual[:48]}...")
        sys.exit(1)
    
    # Verify cryptographic signature
    print(f"\n  [3/3] Verifying cryptographic signature...")
    result = verify_signature(manifest_hash, signature_data, key_path)
    
    if result["status"] == "VERIFIED":
        print(f"    ✅ {result['message']}")
        print(f"\n{'='*60}")
        print(f"  ✅ SOVEREIGN SIGNATURE VERIFIED")
        print(f"  Bootstrap manifest is authentic.")
        print(f"  Skills can now load with full authority.")
        print(f"{'='*60}")
    else:
        print(f"    ❌ {result['message']}")
        print(f"\n{'='*60}")
        print(f"  ❌ VERIFICATION FAILED")
        print(f"  Bootstrap manifest is NOT authenticated.")
        print(f"  Skills will be quarantined to OBSERVE_ONLY.")
        print(f"{'='*60}")
        sys.exit(1)

if __name__ == "__main__":
    main()
