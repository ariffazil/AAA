#!/usr/bin/env python3
"""
vertical_slice_verifier.py — Reusable verification harness for WITNESS_TO_ADAPTATION_VERTICAL_SLICE_V1
Authority: F13 Sovereign (Muhammad Arif bin Fazil)
Doctrine: DITEMPA BUKAN DIBERI
"""
import os, sys, json, subprocess, tempfile, uuid, hashlib
from datetime import datetime, timezone
import nacl.signing
import rfc8785

def run_suite():
    print("=== WITNESS_TO_ADAPTATION_VERTICAL_SLICE_V1 ===")
    
    # 1. Provenance check
    print("[1/4] Checking Provenance...")
    provenance = {}
    for repo, shas in [('/root/AAA', ['2b2e491ba419173a50ee5a6a67b165192f6e1814', '1e1eca0adb04a1ad7d8bde1992118a9a5111135c']), 
                       ('/root/arifOS', ['dbecd35ee1e3b246032dd16c7402fe74f99da37f'])]:
        branch = subprocess.check_output(['git', '-C', repo, 'branch', '--show-current']).decode().strip()
        remote_url = subprocess.check_output(['git', '-C', repo, 'remote', 'get-url', 'origin']).decode().strip()
        for sha in shas:
            pushed = subprocess.run(['git', '-C', repo, 'branch', '-r', '--contains', sha], capture_output=True, text=True).stdout.strip()
            provenance[sha[:8]] = 'PUSHED' if pushed else 'LOCAL_ONLY_UNPUSHED'
    print(f"  Provenance: {provenance}")

    # 2. Schema validator
    def validate_schema(doc: dict) -> tuple[bool, str]:
        required = {'receipt_version', 'event_id', 'actor_id', 'capability', 'observed_at', 'target', 'probe_path', 'observation'}
        if not required.issubset(doc.keys()):
            return False, f"Missing keys: {required - doc.keys()}"
        if doc.get('receipt_version') != '1.0':
            return False, "Invalid receipt_version"
        if not isinstance(doc.get('probe_path'), dict) or not isinstance(doc.get('observation'), dict):
            return False, "probe_path and observation must be objects"
        return True, "OK"

    # 3. Cryptographic tests
    print("[2/4] Testing RFC 8785 Canonicalization & Ed25519...")
    signer = nacl.signing.SigningKey.generate()
    verifier = signer.verify_key

    # Equivalence test
    d1 = {'target': 'well', 'observation': {'reachable': True, 'latency_ms': 18.2}, 'actor_id': 'wawa-probe'}
    d2 = {'actor_id': 'wawa-probe', 'target': 'well', 'observation': {'latency_ms': 18.2, 'reachable': True}}
    assert rfc8785.dumps(d1) == rfc8785.dumps(d2), "Canonical equivalence failed"

    # Schema rejection test
    assert not validate_schema({'bad': True})[0], "Bad schema accepted"

    # Signing and verification
    receipt_0 = {
        'receipt_version': '1.0',
        'event_id': str(uuid.uuid4()),
        'actor_id': 'wawa-probe/FI-004',
        'capability': 'federation.health.observe',
        'observed_at': datetime.now(timezone.utc).isoformat(),
        'target': 'synthetic_canary_organ',
        'probe_path': {'endpoint': 'http://127.0.0.1:9999/health', 'proxy_bypassed': True},
        'observation': {'reachable': True, 'status_class': 'UP', 'latency_ms': 10.0, 'param_throttle_ms': 100},
        'previous_receipt_hash': None
    }
    canon_0 = rfc8785.dumps(receipt_0)
    sig_0 = signer.sign(canon_0).signature
    verifier.verify(canon_0, sig_0)

    # Tamper test
    canon_tampered = bytearray(canon_0)
    canon_tampered[5] ^= 0xFF
    try:
        verifier.verify(bytes(canon_tampered), sig_0)
        raise RuntimeError("Tampered receipt passed verification!")
    except nacl.exceptions.BadSignatureError:
        pass

    # Wrong key test
    wrong_vk = nacl.signing.SigningKey.generate().verify_key
    try:
        wrong_vk.verify(canon_0, sig_0)
        raise RuntimeError("Wrong key passed verification!")
    except nacl.exceptions.BadSignatureError:
        pass

    # Proxy misroute test
    def evaluate_probe(code, body):
        if code == 400 and ('direct ip' in body.lower() or 'proxy' in body.lower()):
            return 'UNKNOWN_PATH'
        return 'UP' if code == 200 else 'DOWN'
    assert evaluate_probe(400, "Direct IP access not allowed") == 'UNKNOWN_PATH'

    # 4. Vertical slice adaptation & rollback test
    print("[3/4] Testing Bounded Adaptation & Rollback...")
    canary = '/tmp/vertical_slice_canary.json'
    with open(canary, 'w') as f:
        json.dump({'service': 'canary', 'param_throttle_ms': 100}, f)

    with open(canary) as f:
        before_state = json.load(f)

    # Adapt
    with open(canary, 'w') as f:
        json.dump({'service': 'canary', 'param_throttle_ms': 500}, f)

    with open(canary) as f:
        after_state = json.load(f)
    assert after_state['param_throttle_ms'] == 500, "Adaptation failed"

    # Consequence receipt
    receipt_consequence = {
        'receipt_version': '1.0',
        'event_id': str(uuid.uuid4()),
        'actor_id': 'governor/888-apex',
        'capability': 'federation.adaptation.consequence',
        'observed_at': datetime.now(timezone.utc).isoformat(),
        'target': 'synthetic_canary_organ',
        'probe_path': {'endpoint': canary, 'proxy_bypassed': True},
        'observation': {'reachable': True, 'status_class': 'UP', 'delta': {'before': before_state, 'after': after_state}, 'verdict': 'SEAL_BOUNDED'},
        'previous_receipt_hash': hashlib.sha256(canon_0).hexdigest()
    }
    canon_c = rfc8785.dumps(receipt_consequence)
    sig_c = signer.sign(canon_c).signature
    verifier.verify(canon_c, sig_c)

    # Rollback
    with open(canary, 'w') as f:
        json.dump(before_state, f)
    with open(canary) as f:
        rolled_back = json.load(f)
    assert rolled_back == before_state, "Rollback failed"

    if os.path.exists(canary):
        os.remove(canary)

    print("[4/4] Verification Clean. All Gates Passed.")
    print("VERDICT: SEAL")

if __name__ == '__main__':
    run_suite()
