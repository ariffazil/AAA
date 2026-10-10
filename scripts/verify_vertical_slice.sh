#!/bin/bash
set -euo pipefail

echo "================================================================="
echo " WITNESS_TO_ADAPTATION_VERTICAL_SLICE_V1 — VERIFICATION SCRIPT"
echo " Authority: F13 Sovereign (Muhammad Arif bin Fazil)"
echo " Doctrine: DITEMPA BUKAN DIBERI"
echo "================================================================="

# 2026-10-10 clean-room fix: bare `python3` resolves to an interpreter
# without pytest on some witnesses (hermes toolchain shim shadows PATH).
# Pin to PYTEST_PY (override), else /usr/bin/python3.13 (verified deps:
# pytest, nacl, rfc8785, jsonschema), else fall back to python3.
# Also: verify the CHECKED-OUT tree, not the author's working tree.
if [ -n "${PYTEST_PY:-}" ]; then PY="$PYTEST_PY"
elif /usr/bin/python3.13 -c "import pytest, nacl, rfc8785, jsonschema" 2>/dev/null; then PY=/usr/bin/python3.13
else PY=python3; fi

cd "$(dirname "$0")/.."
ROOT="$(pwd -P)"
export PYTHONPATH="$ROOT"

echo "[1/3] Executing 9 Mandatory Unit & Causal Chain Tests..."
"$PY" -m pytest -q tests/witness/test_receipt_v1.py

echo "[2/3] Verifying Persisted Receipt Chain & Independent Verification..."
"$PY" -c "
import sys, json, nacl.signing, rfc8785, hashlib
from src.witness.receipt_verifier import ReceiptVerifier

with open('tests/witness/vectors/public_key.hex') as f:
    pubkey = f.read().strip()
verifier = ReceiptVerifier(pubkey)

with open('evidence/vertical_slice_receipts.json') as f:
    chain = json.load(f)

assert len(chain) == 4, 'Chain must contain exactly 4 stages'
stages = ['OBSERVE', 'AUTHORIZATION', 'CONSEQUENCE', 'ROLLBACK']

prev_hash = None
for i, item in enumerate(chain):
    rec = item['receipt']
    sig = item['signature_hex']
    assert rec['receipt_type'] == stages[i], f'Stage mismatch at {i}: {rec[\"receipt_type\"]}'
    assert verifier.verify(rec, sig) is True, f'Signature verification failed at stage {stages[i]}'
    if prev_hash is not None:
        assert rec['previous_receipt_hash'] == prev_hash, f'Causal hash chain broken at stage {stages[i]}'
    prev_hash = hashlib.sha256(rfc8785.dumps(rec)).hexdigest()

print('  ✓ All 4 causal receipts mathematically verified against public key: ' + pubkey[:16] + '...')
"

echo "[3/3] Verifying Zero Secrets in Staged Artifacts..."
"$PY" -c "
from pathlib import Path
for p in list(Path('tests/witness/vectors').rglob('*')) + list(Path('evidence').rglob('*')):
    if p.is_file():
        t = p.read_bytes()
        assert b'PRIVATE KEY' not in t, f'Secret leak in {p}'
print('  ✓ Zero private keys serialized in vectors and evidence.')
"

echo "================================================================="
echo " ALL GATES PASSED CLEAN. VERDICT: SEAL"
echo "================================================================="
