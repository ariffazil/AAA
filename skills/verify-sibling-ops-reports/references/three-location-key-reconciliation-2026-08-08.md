# Three-Location Key Reconciliation Protocol

**Generated:** 2026-08-08 by Hermes (mandor) during OpenCode/Full-system audit.

When a sibling agent reports rotating a private key (credential rotation, identity reconciliation, DID key update), verify all three locations independently before accepting the claim.

## The Three Locations

| # | Location | Canonical form | What it stores |
|---|---|---|---|
| 1 | **Private key file** | `/root/AAA/auth/keys/<agent>_private.key` (32-byte Ed25519 seed) | Raw signing key |
| 2 | **DID registry (auth SOT)** | `/root/AAA/auth/did_registry.yaml` | Public key hex + DID + metadata |
| 3 | **Runtime registry** | `/root/.secrets/did/registry.json` (read by arifOS kernel at boot) | Public key hex + DID + metadata |

A correct rotation requires ALL THREE to agree on the same key material. Partial rotation (1 of 3) produces a silent signature verification failure at runtime.

## Verification Protocol

### Step 1: Read the actual private key bytes

```bash
xxd /root/AAA/auth/keys/<agent>_private.key | head -3
# Print first 16 bytes as hex
# Compare with what the sibling claims they wrote
```

### Step 2: Derive the Ed25519 public key from the on-disk private key

```python
from nacl.signing import SigningKey
key_bytes = open('/root/AAA/auth/keys/<agent>_private.key','rb').read()
sk = SigningKey(key_bytes)
pubkey = sk.verify_key.encode().hex()
print(f'Derived pubkey: {pubkey}')
```

If `nacl` is unavailable, use `openssl pkey -in <keyfile> -text -noout` or `ssh-keygen -y -f <keyfile>`.

### Step 3: Compare against DID registry YAML (auth SOT)

```bash
grep -A8 'did:arif:<agent>' /root/AAA/auth/did_registry.yaml
```

Check: `public_key_hex` must match the derived pubkey from Step 2.

### Step 4: Compare against runtime registry JSON

```bash
python3 -c "
import json
d = json.load(open('/root/.secrets/did/registry.json'))
oc = d.get('dids',{}).get('did:arif:<agent>')
print(f'runtime pubkey: {oc.get(\"public_key_hex\")}')
"
```

### Step 5: Check for YAML syntax errors

```bash
python3 -c "import yaml; yaml.safe_load(open('/root/AAA/auth/did_registry.yaml'))"
```

Common failure: unquoted colons in description strings (`OpenClaw AGI runtime — ... source: /root/...` → YAML parser error).

### Step 6: Check the deployed runtime permissions

```bash
stat -c '%a %U:%G %n' /root/.secrets/did/registry.json
sudo -u arifos test -r /root/.secrets/did/registry.json
```

## Common Inconsistencies Found (2026-08-08)

| Inconsistency | What happened | Detection |
|---|---|---|
| Sibling claims pubkey X, on-disk key derives to Y | Sibling wrote pubkey into registry but actual key file was rotated to different seed | Compare derived pubkey (Step 2) with YAML pubkey (Step 3) |
| YAML updated, runtime JSON not re-deployed | Source-of-truth changed but running service still reads old file | Compare YAML pubkey (Step 3) with runtime pubkey (Step 4) |
| YAML broken by unquoted colon | Sibling's edit introduced YAML syntax error | `yaml.safe_load()` throws ScannerError |
| Runtime JSON permissions changed during deploy | chmod/chown during deploy locks out arifos user | `sudo -u arifos test -r` fails |

## Severity Rules

| Pattern | Severity | Action |
|---|---|---|
| All 3 locations agree + permissions OK | PASS | No action |
| YAML ≠ runtime (deploy lag) | MODERATE | Re-deploy before next service restart |
| Key file ≠ YAML (key mismatch) | SEVERE | Reconcile or HOLD — kernel cannot verify signatures |
| YAML broken (syntax error) | MODERATE | Fix YAML syntax before next parse |
| Runtime permissions wrong | HIGH | chmod/own fix — blocks arifOS boot |
| Rotation without ACK_M7 receipt | PROCEDURE | Flag as T3 executed without sovereign approval |
