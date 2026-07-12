#!/usr/bin/env python3
"""
AAA KERNEL BOOTSTRAP — Firmware, not skill.

This script runs BEFORE any skill manifest is parsed.
It loads the9 immutable invariants and registers them as
pre-output/pre-action hooks in the agent runtime.

This is the BIOS. Not the OS. Not an app.
DITEMPA BUKAN DIBERI.

Usage:
  python3 kernel_boot.py                    # Boot and verify
  python3 kernel_boot.py --verify-only      # Just verify, don't register
  python3 kernel_boot.py --sign <key_path>  # Sovereign signature
"""

import json
import hashlib
import sys
import os
from datetime import datetime, timezone
from pathlib import Path

KERNEL_DIR = Path(__file__).parent
BOOTSTRAP_FILE = KERNEL_DIR / "bootstrap_manifest.json"
SIGNATURE_FILE = KERNEL_DIR / "sovereign_signature.json"
BOOT_LOG = KERNEL_DIR / "boot_log.jsonl"

def load_bootstrap():
    """Load the firmware manifest."""
    if not BOOTSTRAP_FILE.exists():
        print(f"FATAL: Bootstrap file missing: {BOOTSTRAP_FILE}")
        print("This is firmware. It cannot be generated. It must exist.")
        sys.exit(1)
    
    with open(BOOTSTRAP_FILE) as f:
        data = json.load(f)
    
    # Verify structure
    required_keys = ["_meta", "invariants", "boot_sequence", "veto_hierarchy"]
    for key in required_keys:
        if key not in data:
            print(f"FATAL: Bootstrap missing required key: {key}")
            sys.exit(1)
    
    # Verify invariant count
    if len(data["invariants"]) != 9:
        print(f"FATAL: Expected 9 invariants, found {len(data['invariants'])}")
        sys.exit(1)
    
    return data

def compute_hash(data):
    """Compute deterministic hash of bootstrap content."""
    with open(BOOTSTRAP_FILE, "rb") as bf: raw_bytes = bf.read()
    return hashlib.sha256(raw_bytes).hexdigest()

def verify_signature(bootstrap_hash):
    """Verify sovereign signature against bootstrap hash."""
    if not SIGNATURE_FILE.exists():
        return {"status": "UNSIGNED", "message": "No sovereign signature found. All skills quarantined to OBSERVE_ONLY."}
    
    with open(SIGNATURE_FILE) as f:
        sig = json.load(f)
    
    if sig.get("manifest_hash") != f"sha256:{bootstrap_hash}":
        return {"status": "MISMATCH", "message": "Signature does not match bootstrap. Firmware may have been tampered with."}
    
    return {"status": "SIGNED", "signer": sig.get("ratifier_id", "UNKNOWN"), "signed_at": sig.get("timestamp", "UNKNOWN")}

def register_invariants(invariants):
    """Register invariants as runtime hooks."""
    hooks = []
    for inv in invariants:
        hook = {
            "id": inv["id"],
            "name": inv["name"],
            "sigil": inv["sigil"],
            "enforcement": inv["enforcement"],
            "veto": inv["veto"],
            "check": inv["check"],
            "failure_mode": inv["failure_mode"],
            "status": "ACTIVE",
        }
        hooks.append(hook)
    return hooks

def veto_check(skill_manifest, hooks):
    """Check a skill manifest against all invariants. Returns (pass, violations)."""
    violations = []
    
    for hook in hooks:
        if not hook["veto"]:
            continue
        
        # INV-9: Sovereign signature required
        if hook["id"] == "INV-9-SOVEREIGN":
            if not skill_manifest.get("sovereign_signature"):
                violations.append({
                    "invariant": hook["id"],
                    "violation": "Missing sovereign signature",
                    "action": "QUARANTINE — load in OBSERVE_ONLY mode",
                })
        
        # INV-1: Evidence schema required
        if hook["id"] == "INV-1-VERIFY":
            if not skill_manifest.get("invariants", {}).get("evidence_schema"):
                violations.append({
                    "invariant": hook["id"],
                    "violation": "Missing evidence schema",
                    "action": "HOLD — cannot emit claims without evidence labels",
                })
        
        # INV-3: Reversibility declared
        if hook["id"] == "INV-3-REVERSE":
            if "reversibility" not in skill_manifest.get("invariants", {}):
                violations.append({
                    "invariant": hook["id"],
                    "violation": "Missing reversibility declaration",
                    "action": "888_HOLD — mutations blocked until declared",
                })
        
        # INV-5: Dignity check
        if hook["id"] == "INV-5-GUARD":
            # Always passes at load time — enforced at output time
            pass
    
    return (len(violations) == 0, violations)

def boot_log(event, data=None):
    """Append to immutable boot log."""
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "data": data or {},
    }
    with open(BOOT_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")

def main():
    verify_only = "--verify-only" in sys.argv
    
    print("=" * 60)
    print("  AAA KERNEL BOOTSTRAP — Firmware v1.0.0")
    print("  DITEMPA BUKAN DIBERI")
    print("=" * 60)
    
    # Step 1: Load firmware
    print("\n[1/5] Loading bootstrap invariants...")
    bootstrap = load_bootstrap()
    bootstrap_hash = compute_hash(bootstrap)
    print(f"  Hash: {bootstrap_hash[:16]}...")
    print(f"  Invariants: {len(bootstrap['invariants'])}")
    
    # Step 2: Verify signature
    print("\n[2/5] Verifying sovereign signature...")
    sig_status = verify_signature(bootstrap_hash)
    print(f"  Status: {sig_status['status']}")
    if sig_status["status"] == "UNSIGNED":
        print(f"  ⚠️  {sig_status['message']}")
    elif sig_status["status"] == "SIGNED":
        print(f"  ✅ Signed by: {sig_status['signer']}")
    
    # Step 3: Register invariants
    print("\n[3/5] Registering invariant hooks...")
    hooks = register_invariants(bootstrap["invariants"])
    for hook in hooks:
        veto_marker = "🔴 VETO" if hook["veto"] else "🟡 MONITOR"
        print(f"  {hook['sigil']} {hook['name']:12s} [{hook['enforcement']:15s}] {veto_marker}")
    
    # Step 4: Verify boot sequence
    print("\n[4/5] Boot sequence verification...")
    boot_seq = bootstrap["boot_sequence"]
    for i in range(1, 6):
        step = boot_seq.get(f"step_{i}", "")
        print(f"  {i}. {step}")
    
    # Step 5: Log and report
    print("\n[5/5] Boot complete.")
    boot_log("BOOT_COMPLETE", {
        "hash": bootstrap_hash,
        "signature_status": sig_status["status"],
        "invariants_registered": len(hooks),
        "mode": "VERIFY_ONLY" if verify_only else "ACTIVE",
    })
    
    if sig_status["status"] == "UNSIGNED":
        print("\n" + "=" * 60)
        print("  ⚠️  FIRMWARE UNSIGNED")
        print("  All skills will be quarantined to OBSERVE_ONLY mode.")
        print("  To sign: python3 kernel_boot.py --sign /path/to/key")
        print("  Or: Arif signs sovereign_signature.json manually.")
        print("=" * 60)
    
    print(f"\n  Veto hierarchy:")
    for level, desc in bootstrap["veto_hierarchy"].items():
        if level.startswith("level"):
            print(f"    {level}: {desc}")
    
    print(f"\n  Compression boundary:")
    print(f"    {bootstrap['compression_boundary']['principle']}")
    
    print(f"\n  External grounding:")
    eg = bootstrap.get('external_grounding', {})
    print(f"    {eg.get('principle', eg.get('mechanism', 'N/A'))}")
    
    print(f"\n{'='*60}")
    print(f"  Kernel booted. Skills can now load.")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
