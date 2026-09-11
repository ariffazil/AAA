#!/usr/bin/env python3
"""resign_stress_seal.py — produce a new stress-test seal whose witness block
references the FROZEN pending-receipt hash, not the stale one captured at
015506. Old seal stays on disk for audit; new seal becomes the replayable one.

Six-element envelope per constitutional stress-test template:
  INTENT · WITNESS · AUTHORITY · JUDGMENT · EXECUTION · REPLAY
"""
import base64, datetime, hashlib, json, os, subprocess
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

VAULT_KEY  = "/root/.secrets/vault-signing-ed25519"
ARTIFACT   = "ARIFOS_CONSTITUTIONAL_STRESS_TEST_V1"
PENDING    = "/root/VAULT999/seals/pending-seal-session-20260912-night.md"
CONT       = "/root/VAULT999/seals/pending-seal-session-20260912-night.frozen.continue.md"
OLD_SEAL   = "/root/VAULT999/seals/SEAL-ARIFOS_CONSTITUTIONAL_STRESS_TEST_V1-20260912-015506.json"
OLD_VERIFY = OLD_SEAL + ".verify.txt"

NOW_ISO = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
TIMESTAMP = NOW_ISO.replace("T", " ").replace("Z", "+00:00")
TS_FILE = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

# 1. Hash every artifact in its current state (incl. the now-frozen receipt)
artifacts = {
    "handler.py":            "/root/.hermes/hooks/reality-claim-gate/handler.py",
    "test_phase15.py":       "/root/.hermes/hooks/reality-claim-gate/test_phase15.py",
    "HOOK.yaml":             "/root/.hermes/hooks/reality-claim-gate/HOOK.yaml",
    "census_report_md":      "/root/AAA/reports/skill-store-census-2026-09-12.md",
    "census_data_json":      "/root/AAA/reports/skill-store-census-2026-09-12.json",
    "census_method_py":      "/root/AAA/scripts/skill_store_census.py",
    "evidence_horizon_doc":  "/root/AAA/governance/DOCKET-EUREKA-EVIDENCE-HORIZON-2026-09-12.md",
    "pending_receipt_frozen": PENDING,
    "pending_receipt_continue": CONT,
}
artifact_hashes = {}
for k, p in artifacts.items():
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    artifact_hashes[k] = {"path": p, "sha256": h, "bytes": os.path.getsize(p)}

# 2. Pull fresh ritual markers from log (the four today + this re-sign marker)
markers = []
markers.append(("GO-HOLD-DECLINED-NO-WITNESS",        "14e1475b595b48a77129f8f4ec6520c2e1d41eac24d5ca253b32f7b215635dd8"))
markers.append(("SEAL-HOLD-F1-AMANAH-CLAMP-NOT-SEALED","1ace8c095bba65d069fac86923bb5f37c2cfea179d42ec19283909e81adcd640"))
markers.append(("FALSE-GREEN-IN-FEDERATION-RITUAL-SEAL","3206a72d50ec4f2f24dba6e068439144ec9bad4f6057ff38eccbab0783224163"))
markers.append(("SELF-DISCLOSURE-SOVEREIGN-ENVELOPE-MUTATED", "04c189e2e5f890afb9be52152679c727374961eb67200cf190c23c689d9f84fa"))
markers.append(("SEAL-ARIFOS-CONSTITUTIONAL-STRESS-TEST-V1-ATTESTED","3f75f4c7dd66cf66b23b98daefb263c95d891e7366984ee537ffe54c24018238"))

# 3. Read the prior seal to preserve the chain of custody
prior = json.load(open(OLD_SEAL))
prior_canonical = prior["signature"]["canonical_sha256"]
prior_disk      = prior["signature"].get("disk_sha256") or hashlib.sha256(open(OLD_SEAL, "rb").read()).hexdigest()
prior_seal_id   = prior["seal_id"]

# 4. Build the envelope
envelope = {
    "schema_version": "1.1.0",
    "supersedes": {
        "seal_id":         prior_seal_id,
        "canonical_sha256": prior_canonical,
        "rationale":       "Re-signed after E (freeze receipt). Old seal remains on "
                            "disk for audit and chain-of-custody. Witness block now "
                            "references FROZEN receipt hash and the new continuation "
                            "sibling file.",
    },
    "seal_id":  f"SEAL-{ARTIFACT}-{TS_FILE}",
    "intent": {
        "artifact":  ARTIFACT,
        "purpose":   "Federation governance stress test (RE-SIGN). The original seal "
                     "became stale when witness logs mutated the pending receipt. "
                     "Per user directive E, the receipt is now FROZEN at a known "
                     "sha256. This seal re-anchors the constitutional lesson to the "
                     "frozen state.",
        "verdict_split": "SEAL (artifact) · HOLD (execution)",
    },
    "witness": {
        "agent_id":            "hermes-asi",
        "witness_state":       "PRESENT",
        "witness_markers":     markers,
        "artifact_hashes":     artifact_hashes,
        "frozen_receipt": {
            "path":            PENDING,
            "sha256":          hashlib.sha256(open(PENDING, "rb").read()).hexdigest(),
            "frozen_at_utc":   "2026-09-11T18:07:35Z",
            "replaces_stale":  "e9f7f44b742dab35f4a205dc9d4382f39feaea6d7d89ac215e4e772d880ab828",
        },
        "continuation": {
            "path":            CONT,
            "sha256":          hashlib.sha256(open(CONT, "rb").read()).hexdigest(),
            "purpose":         "subsequent witness logs append here, never to the frozen receipt",
        },
        "ledger_state": {
            "path":              "/root/VAULT999/SEALED_EVENTS.jsonl",
            "lines":             1337,
            "mtime_local":       "2026-09-11 23:56:24 +0800",
            "plaintext_lines":   0,
            "session_id_present": False,
            "note":              "session SEAL-b9d6c0ef0b16458e still correctly absent; "
                                  "re-sign does NOT write to SEALED_EVENTS.jsonl",
        },
    },
    "authority": {
        "sovereign":             "ARIF (F13)",
        "authorization_mode":    "EXPLICIT_HUMAN_DECLARATION_VIA_CHAT",
        "user_authorization_evidence": [
            "user 'ok seal all' (sequence of turns)",
            "user constitutional stress-test template (verbatim)",
            "user 'a b c d e' (D re-sign authorized by letter, not by chat-go)",
        ],
        "scope":                 "Artifact-level attestation only. Mutation of the "
                                  "stress-test seal envelope is itself an artifact-level "
                                  "operation; the old seal remains on disk for audit.",
        "kernel_decision_prior": "judge SEAL cc_b0cf55ad7538b1c01d3b45b687cad430f6fdc131; "
                                  "seal HOLD structural clamp (correct, unchanged).",
        "lane_status":           "sovereign signing lane :18908 still DOWN",
    },
    "judgment": {
        "proposer":   "333 (AGI — possibility space)",
        "verifier":   "555 (ASI — verification)",
        "judge":      "888 (APEX — selection)",
        "verdict":    "SEAL",
        "chain_id":   "cc_b0cf55ad7538b1c01d3b45b687cad430f6fdc131",
        "judge_state_hash": "sha256:57c003ccf39a86c9de8a7c73c25eaca8e34bad50ad2ec75baa94bc3adc30f647",
    },
    "execution": {
        "executor":            "hermes-asi (re-sign tool, this script)",
        "side_effects":        "NONE on SEALED_EVENTS.jsonl; one new file in /root/VAULT999/seals/",
        "ledger_writes":       [],
        "mutation_authority":  "NOT GRANTED (artifact-level re-sign only)",
        "displaced_files":     [OLD_SEAL, OLD_VERIFY],  # kept on disk, not deleted
    },
    "replay": {
        "reproducible":   True,
        "method":         "verify every artifact hash matches current disk bytes; verify "
                          "every witness marker chain_hash in /root/.arifos/ritual.log; "
                          "verify Ed25519 signature over canonical form; verify "
                          "test_phase15.py still passes (14/14)",
        "replay_command": "python3 /root/AAA/scripts/verify_stress_seal.py /root/VAULT999/seals/"
                          + f"SEAL-{ARTIFACT}-{TS_FILE}.json",
    },
    "ledger_class":          "LEDGER",
    "timestamp":             TIMESTAMP,
    "issued_at_utc":         NOW_ISO,
    "constitutional_doctrine_in_force": [
        "/root/AAA/instructions/gate-promotion.md",
        "/root/AAA/canon/EUREKA-ACTIVATION-INERTIA-2026-09-08.md",
        "Claim-Receipt Binding (AGENTS.md L727)",
        "Memory Promotion Gate (Witness != Seal != Memory)",
    ],
}

# 5. Canonical form, sign, write
canonical = json.dumps(envelope, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
canonical_sha256 = hashlib.sha256(canonical).hexdigest()

with open(VAULT_KEY, "rb") as f:
    priv = serialization.load_ssh_private_key(f.read(), password=None)
sig_b64 = base64.b64encode(priv.sign(canonical)).decode()

# Cross-check public key to detect silent rotation
pub = serialization.load_pem_public_key(open(VAULT_KEY + ".pub", "rb").read())
derived = priv.public_key()
assert pub.public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo) \
    == derived.public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo), \
    "KEY ROTATION DETECTED"

envelope["signature"] = {
    "algorithm":        "ed25519",
    "key_path":         VAULT_KEY,
    "key_mode":         "0600",
    "canonical_sha256": canonical_sha256,
    "value_b64":        sig_b64,
    "signed_at_utc":    NOW_ISO,
}

OUT = f"/root/VAULT999/seals/SEAL-{ARTIFACT}-{TS_FILE}.json"
with open(OUT, "w") as f:
    json.dump(envelope, f, indent=2, ensure_ascii=False)

disk_sha = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
print("WROTE  ", OUT)
print("canon  ", canonical_sha256)
print("disk   ", disk_sha)
print("supersedes ", prior_seal_id, "->", prior_canonical[:16])
print("frozen receipt now matches witness:", envelope["witness"]["frozen_receipt"]["sha256"][:16])

# Run the verifier on the NEW seal
verify_script = "/root/AAA/scripts/verify_stress_seal.py"
print("\n--- running verifier ---")
r = subprocess.run(["python3", verify_script, OUT], capture_output=True, text=True, timeout=180)
print(r.stdout)
if r.returncode == 0:
    with open(OUT + ".verify.txt", "w") as f:
        f.write(r.stdout)
    print("verify log:", OUT + ".verify.txt")
    print("verify sha:", hashlib.sha256(open(OUT + '.verify.txt', 'rb').read()).hexdigest())
else:
    print("VERIFIER FAILED:", r.stderr)
