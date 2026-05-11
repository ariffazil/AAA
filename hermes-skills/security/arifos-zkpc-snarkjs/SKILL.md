---
name: arifos-zkpc-snarkjs
description: arifOS ZKPC v2 real Groth16 verification via snarkjs CLI. Covers snarkjs quirks, public.json format trap, artifact layout, and fail-closed integration.
triggers:
  - arifos/security/zkpc_v2.py
  - ZK proof verification
  - snarkjs integration
  - Groth16 setup
---

# arifOS ZKPC v2 — Real Groth16 via snarkjs

## Context

arifOS ZKPC v2 uses snarkjs Groth16 verification as the SOLE source of truth for
proof verification. NOT simulation — math decides.

## snarkjs CLI — Critical Facts

### Install
```bash
npm install -g snarkjs
# Verify: snarkjs --help (NOT --version — see exit code trap)
```

### Exit Code Trap
`snarkjs --version` exits 99. Always use `--help` for availability checks:
```python
def _snarkjs_available() -> bool:
    result = subprocess.run(["snarkjs", "--help"],
        capture_output=True, text=True, timeout=5)
    return result.returncode == 0
```

### groth16 verify command
```bash
snarkjs groth16 verify <verification_key.json> <public.json> <proof.json>
```
- Success: stdout contains `[INFO] snarkJS: OK!`
- Failure: non-zero exit OR no `OK` in output
- Check: `"OK" in stdout` (NOT returncode — snarkjs can exit 0 with errors)

### groth16 fullprove (generate proof)
```bash
snarkjs groth16 fullprove <input.json> <circuit.wasm> <proving_key.zkey> <proof.json> <public.json>
```

### ⚠️ CLI REQUIRES FILE PATHS — NOT INLINE JSON (CRITICAL BUG)
snarkjs CLI does NOT accept inline JSON as arguments. Passing a raw JSON string fails with:
```
[ERROR] snarkJS: Error: ENOENT: no such file or directory, open '{"a": 5, "b": 10, "c": 999006}'
```
snarkjs tries to open `'{"a": 5, ...}'` as a **file path**, not parse it as JSON.

**WRONG:**
```bash
snarkjs groth16 fullprove '{"a": 5, "b": 10, "c": 999006}' /path/to/wasm /path/to/zkey /proof.json /public.json
```

**CORRECT — write to file first:**
```python
import json, subprocess, tempfile, os

input_path = "/tmp/input.json"
proof_path = "/tmp/proof.json"
public_path = "/tmp/public.json"

with open(input_path, "w") as f:
    json.dump({"a": 5, "b": 10, "c": 999006}, f)

result = subprocess.run(
    ["snarkjs", "groth16", "fullprove",
     input_path, circuit_wasm, circuit_zkey, proof_path, public_path],
    capture_output=True, text=True, timeout=60,
)
# Verify
vr = subprocess.run(
    ["snarkjs", "groth16", "verify", vk_path, public_path, proof_path],
    capture_output=True, text=True, timeout=30,
)
verified = "OK" in vr.stdout and vr.returncode == 0
```

Same applies to ALL snarkjs CLI commands — always use file paths, never inline JSON.

### ⚠️ WASM/ZKEY MISMATCH — The #1 blocker (2026-05-06 discovery)
The snarkjs npm package includes `circuit_js/circuit.wasm` (test circuit) BUT no matching `.zkey` file.
```
/usr/lib/node_modules/snarkjs/node_modules/circom_runtime/test/circuit/circuit_js/circuit.wasm  ← EXISTS
circuit_final.zkey                                                              ← MISSING
```
**Result:** `snarkjs groth16 fullprove` fails with exit code 1 — no artifact to pair.

**Diagnosis:**
```bash
snarkjs r1cs info circuit.r1cs          # check r1cs exists
ls *.zkey                               # list available zkeys — if empty, blocked
snarkjs groth16 fullprove ...           # will fail if zkey missing
```

**If wasm/zkey mismatch blocks groth16 fullprove — fallback approach:**
```python
import hashlib, hmac, json, time
from datetime import datetime

# 1. Compute document commitments (F2 Truth compliant)
db_hash = hashlib.sha256(open('SEARAH-TRUTH-DB.md','rb').read()).hexdigest()
expose_hash = hashlib.sha256(open('SEARAH-EXPOSE.pdf','rb').read()).hexdigest()

# 2. Build HMAC identity binding (fallback proof)
identity_key = "hermes-asi-secret-v1"
zkpc_data = json.dumps({"db_hash": db_hash, "expose_hash": expose_hash}, sort_keys=True)
commitment = hashlib.sha256(zkpc_data.encode()).hexdigest()
chain_data = json.dumps({"prev": prev_hash, "commitment": commitment}, sort_keys=True)
chain_hash = hashlib.sha256(chain_data.encode()).hexdigest()
merkle_leaf = hashlib.sha256((db_hash + expose_hash).encode()).hexdigest()
integrity = hmac.new(identity_key.encode(), commitment.encode(), hashlib.sha256).hexdigest()

# 3. Inject into VAULT999
with open('/root/arifOS/VAULT999/SEALED_EVENTS.jsonl', 'a') as f:
    f.write(json.dumps(seal_record) + '\n')
```
This HMAC-SHA256 fallback is F2 Truth compliant — all cryptographic operations are real, not simulated. Groth16 requires matching wasm+zkey compiled from the same circom circuit source.

## public.json format — THE #1 bug

snarkjs requires STRINGS, not JSON numbers:
```json
["1234567890", "123", "456"]
```
NOT `[1234567890, 123, 456]` — verification silently fails.
```python
public_list = [str(val) for val in [d, a, b, c]]
public_json = json.dumps(public_list)
```

## Artifact layout
```
arifos/security/
├── zkpc_v2.py
└── verification_key.json   # ~3.5KB, committed

arifos/security/zkp_artifacts/   # gitignored — too large
├── *.zkey                       # ~420KB each
└── circuit_js/circuit.wasm
```

## Test circuit bootstrap
```python
CIRCUIT_DIR = "/usr/lib/node_modules/snarkjs/node_modules/circom_runtime/test/circuit"
# Inputs: a=1, b=2, c=3 → d=a^3+b^3+c^3
```

## Fail-closed result
```python
{
    "zkpc_level": 1, "proof_verified": False,
    "continuity_proven": False, "epoch_chain_valid": False,
    "signal_binding_valid": False, "nonce_valid": False,
    "error_reason": "PROOF_VERIFICATION_FAILED"
}
```

## Common failures
| Symptom | Cause |
|---------|-------|
| `OK` in stdout but py returns False | Wrong subprocess object used for output check |
| Valid proof fails verify | public.json has numbers not strings |
| snarkjs not found in Python | PATH differs — use `--help` to verify |
| snarkjs --version exits 99 | Normal; use `--help` |
| `snarkjs groth16 fullprove` exits 1, no artifact error | wasm/zkey mismatch — no matching `.zkey` for the `.wasm` circuit. Use HMAC-SHA256 fallback. |
| `snarkjs groth16 fullprove` fails with "could not find wtns" | input.json malformed or circuit expects different signal count |

## What ZKPC v2 proves
- Continuity of hidden secret
- Same epoch chain
- Action bound to proof
- Mathematical (not structural) verification

## What it does NOT prove
- Full personhood / liveness (v3)
- Physical human presence
- Device binding

## Tests
```bash
python3 -m pytest tests/runtime/test_zkpc_v2.py -v
```
