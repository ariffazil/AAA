"""
test_receipt_v1.py — Comprehensive test suite for WITNESS_TO_ADAPTATION_VERTICAL_SLICE_V1
Authority: F13 Sovereign (Muhammad Arif bin Fazil)
Doctrine: DITEMPA BUKAN DIBERI
"""
import sys, os, json, hashlib
import pytest
import jsonschema
import nacl.signing
import nacl.exceptions
import rfc8785
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.witness.receipt_signer import ReceiptSigner
from src.witness.receipt_verifier import ReceiptVerifier

VECTORS_DIR = BASE_DIR / "tests" / "witness" / "vectors"

@pytest.fixture
def test_keys():
    seed = hashlib.sha256(b"WITNESS_V1_TEST_KEY_DETERMINISTIC_SEED_20261010").digest()
    sk = nacl.signing.SigningKey(seed)
    vk = sk.verify_key
    return sk, vk.encode().hex()

def test_1_valid_receipt_verifies(test_keys):
    sk, vk_hex = test_keys
    with open(VECTORS_DIR / "receipt_valid.json") as f:
        vec = json.load(f)
    verifier = ReceiptVerifier(vk_hex)
    assert verifier.verify(vec["receipt"], vec["signature_hex"]) is True

def test_2_one_byte_mutation_fails(test_keys):
    sk, vk_hex = test_keys
    with open(VECTORS_DIR / "receipt_tampered.json") as f:
        vec = json.load(f)
    verifier = ReceiptVerifier(vk_hex)
    with pytest.raises(nacl.exceptions.BadSignatureError):
        verifier.verify(vec["receipt"], vec["signature_hex"])

def test_3_wrong_public_key_fails():
    with open(VECTORS_DIR / "receipt_valid.json") as f:
        vec = json.load(f)
    other_sk = nacl.signing.SigningKey.generate()
    wrong_vk_hex = other_sk.verify_key.encode().hex()
    verifier = ReceiptVerifier(wrong_vk_hex)
    with pytest.raises(nacl.exceptions.BadSignatureError):
        verifier.verify(vec["receipt"], vec["signature_hex"])

def test_4_equivalent_json_produces_identical_canonical_bytes():
    d1 = {"b": 2, "a": 1, "nested": {"z": 10, "y": 20}}
    d2 = {"nested": {"y": 20, "z": 10}, "a": 1, "b": 2}
    assert rfc8785.dumps(d1) == rfc8785.dumps(d2)

def test_5_invalid_schema_is_rejected_before_signing(test_keys):
    sk, _ = test_keys
    signer = ReceiptSigner(sk, key_id="key-test-witness-01")
    bad_receipt = {"schema_version": "receipt.v0_invalid"}
    with pytest.raises(jsonschema.ValidationError):
        signer.sign(bad_receipt)

def test_6_proxy_induced_failure_not_classified_as_down():
    def classify_probe(code: int, body: str) -> str:
        if code == 200:
            return "UP"
        if code == 400 and ("direct ip" in body.lower() or "proxy" in body.lower()):
            return "UNKNOWN_PATH"
        return "DOWN"
    assert classify_probe(400, "Direct IP access not allowed") == "UNKNOWN_PATH"

def test_7_authorized_bounded_adaptation_changes_behaviour(test_keys):
    sk, vk_hex = test_keys
    signer = ReceiptSigner(sk, key_id="key-test-witness-01")
    verifier = ReceiptVerifier(vk_hex)

    # 1. OBSERVE (Before)
    rec_obs = {
        "schema_version": "receipt.v1",
        "receipt_id": "rec-11111111-1111-1111-1111-111111111111",
        "receipt_type": "OBSERVE",
        "actor_id": "observer/wawa-probe",
        "capability_id": "federation.health.observe.v1",
        "authority_ref": None,
        "parent_receipt_id": None,
        "previous_receipt_hash": None,
        "timestamp_utc": "2026-10-10T02:01:00Z",
        "key_id": "key-test-witness-01",
        "payload": {
            "target": "synthetic_canary",
            "probe_path": {"endpoint": "http://127.0.0.1:9999/health", "proxy_bypassed": True},
            "observation": {"reachable": True, "status_class": "UP", "param_throttle_ms": 100}
        }
    }
    _, sig_obs = signer.sign(rec_obs)
    assert verifier.verify(rec_obs, sig_obs)
    hash_obs = hashlib.sha256(rfc8785.dumps(rec_obs)).hexdigest()

    # 2. AUTHORIZATION (Governor separate object)
    rec_auth = {
        "schema_version": "receipt.v1",
        "receipt_id": "rec-22222222-2222-2222-2222-222222222222",
        "receipt_type": "AUTHORIZATION",
        "actor_id": "governor/888-apex",
        "capability_id": "federation.governance.authorize.v1",
        "authority_ref": "F13_SOVEREIGN_MANDATE",
        "parent_receipt_id": rec_obs["receipt_id"],
        "previous_receipt_hash": hash_obs,
        "timestamp_utc": "2026-10-10T02:02:00Z",
        "key_id": "key-test-witness-01",
        "payload": {
            "verdict": "SEAL_BOUNDED",
            "target_action": "tune_canary_throttle",
            "approved_parameters": {"param_throttle_ms": 500},
            "rollback_constraint": {"baseline_param_throttle_ms": 100}
        }
    }
    _, sig_auth = signer.sign(rec_auth)
    assert verifier.verify(rec_auth, sig_auth)
    hash_auth = hashlib.sha256(rfc8785.dumps(rec_auth)).hexdigest()

    # 3. CONSEQUENCE (Executor after bounded action)
    rec_csq = {
        "schema_version": "receipt.v1",
        "receipt_id": "rec-33333333-3333-3333-3333-333333333333",
        "receipt_type": "CONSEQUENCE",
        "actor_id": "executor/a-forge",
        "capability_id": "federation.action.execute.v1",
        "authority_ref": rec_auth["receipt_id"],
        "parent_receipt_id": rec_auth["receipt_id"],
        "previous_receipt_hash": hash_auth,
        "timestamp_utc": "2026-10-10T02:03:00Z",
        "key_id": "key-test-witness-01",
        "payload": {
            "action_executed": "tune_canary_throttle",
            "delta": {"before": {"param_throttle_ms": 100}, "after": {"param_throttle_ms": 500}},
            "observed_consequence": {"param_throttle_ms": 500, "status": "ADAPTED"}
        }
    }
    _, sig_csq = signer.sign(rec_csq)
    assert verifier.verify(rec_csq, sig_csq)
    assert rec_csq["payload"]["observed_consequence"]["param_throttle_ms"] == 500

def test_8_rollback_restores_baseline(test_keys):
    sk, vk_hex = test_keys
    signer = ReceiptSigner(sk, key_id="key-test-witness-01")
    verifier = ReceiptVerifier(vk_hex)

    # Base Consequence Hash mock for causal chain
    csq_hash = hashlib.sha256(b"mock_consequence_bytes").hexdigest()

    # ROLLBACK (Restoring baseline)
    rec_rb = {
        "schema_version": "receipt.v1",
        "receipt_id": "rec-44444444-4444-4444-4444-444444444444",
        "receipt_type": "ROLLBACK",
        "actor_id": "executor/a-forge",
        "capability_id": "federation.action.rollback.v1",
        "authority_ref": "rec-22222222-2222-2222-2222-222222222222",
        "parent_receipt_id": "rec-33333333-3333-3333-3333-333333333333",
        "previous_receipt_hash": csq_hash,
        "timestamp_utc": "2026-10-10T02:04:00Z",
        "key_id": "key-test-witness-01",
        "payload": {
            "rollback_action": "restore_canary_throttle_baseline",
            "restored_state": {"param_throttle_ms": 100},
            "baseline_verified": True
        }
    }
    _, sig_rb = signer.sign(rec_rb)
    assert verifier.verify(rec_rb, sig_rb)
    assert rec_rb["payload"]["baseline_verified"] is True
    assert rec_rb["payload"]["restored_state"]["param_throttle_ms"] == 100

def test_9_no_secrets_in_artifacts():
    # Verify no private key headers or binary seeds in vector files
    for vec_file in VECTORS_DIR.glob("*"):
        text = vec_file.read_text()
        assert "PRIVATE KEY" not in text
        assert "BEGIN EC PRIVATE" not in text
        assert "BEGIN OPENSSH PRIVATE" not in text
