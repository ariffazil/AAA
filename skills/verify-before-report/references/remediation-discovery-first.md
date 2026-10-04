# Remediation specs with stale/fictional paths — discover before acting

> Session: 2026-08-12 autonomous remediation (FQ ingestion / FI drift / kimi JWS / FLAME budget).
> A multi-step remediation spec referenced many paths that did NOT exist. The correct
> move was to discover the real locations and verify each premise, then apply fixes
> only where real drift existed — and honestly report "no change needed" or "BLOCKED"
> where the premise was already correct or the fix required missing authority/key material.

## The pattern

Remediation / audit specs are often written against a *hypothetical* or *stale* substrate.
Before acting on any step:

1. **Do NOT assume the stated path exists.** Probe it (`ls`, `test -f`) and, if missing,
   discover the real equivalent with `search_files(target=files)` + grep of known identifiers.
2. **Verify the premise**, not just the location. A "fix X drift" step may already be correct.
   Read-only flag? actually writable → no change. FI numbering drift? cards already match
   registry → no change. Key material for re-signing? redacted/mismatched → BLOCKED, not "fixed".
3. **Report the honest outcome**: DONE (real change applied), NO-OP (premise already correct,
   verified), or BLOCKED (missing authority/key/infra) — never fabricate a "fix" that adds
   entropy or a mismatched signature.

## Real path map discovered (federation)

The spec's assumed paths vs reality:

| Spec assumed | Reality (authoritative) |
|---|---|
| `~/AAA/docs/AGENTS_UNIFIED.yaml` | `/root/AAA/registries/AGENTS_UNIFIED.yaml` |
| `~/.config/opencode/{qwen,kimi}-code.json` | `/root/.kimi-code/credentials/kimi-code.json`, `/root/.qwen/settings.json` |
| `fi-card.json` under `~/.config/opencode/*` | `/root/AAA/a2a-server/agent-cards/forge/fi-*.json` AND canonical `/root/AAA/agents/<id>/agent-card.json` |
| FI tier source-of-truth | `forge_instruments[].fi_slot` in `/root/AAA/registries/AGENTS_UNIFIED.yaml` |
| FRAME chambers | `/root/FRAME/src/frame_organ/main.py` docstring (BASELINE/PROBE/COMPARE/TREND/ALERT/REPORT) |
| FI-008 signing key | `/root/forge_work/calibration_keys/fi008_ed25519.pem` (**was REDACTED** → `[REDACTED PRIVATE KEY]`) |

Canonical FI registry slots (from `AGENTS_UNIFIED.yaml`): FI-001 opencode, FI-002 claude-code,
FI-003 qwen-code, FI-004 antigravity/agy, FI-005 codex, FI-006 copilot, FI-007 grok-build,
FI-008 kimi-code. Canonical agent-cards all live under `/root/AAA/agents/<id>/agent-card.json`
(with `_external/` prefix for claude/qwen/agy/codex/copilot/grok-build).

## Premise-verification checklist (before each remediation step)

- **Read-only / EROFS check**: `mount | grep <path>` + a `touch`/write test. If writable and not
  mounted read-only → no config change needed (keep ΔS ≤ 0).
- **Drift/numbering check**: compare registry value vs card value (`jq`/python). If equal → NO-OP,
  verified, don't touch.
- **Key/identity check**: see JWS section below. If key redacted or mismatched → BLOCKED.
- **Infra repair check**: if the fix mutates a daemon/kernel (e.g. arifFLOW ingestion), that is
  T3/888_HOLD territory — document BLOCKED, don't auto-execute.

## JWS re-sign: verify key identity BEFORE signing (2026-08-12 kimi-code case)

Before re-signing any JWS/token, confirm the private key you hold **matches the registered
public key / DID** for the subject. Never re-sign with a mismatched key — it produces an
invalid-identity signature (a security regression, not a fix).

```python
import base64, json
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

# 1) Derive public key from the candidate private key
seed = open('/path/to/private.key','rb').read()            # 32-byte raw seed
pub  = Ed25519PrivateKey.from_private_bytes(seed).public_key()
pub_raw = pub.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)

# 2) Decode the DID-registered public key (multibase 'z' = base58btc)
ALPH = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
mb = "9Aaf...<multibase body without leading z>"
n = 0
for c in mb: n = n*58 + ALPH.index(c)
did_pub = n.to_bytes((n.bit_length()+7)//8, 'big')

# 3) Compare — if they differ, the candidate key is NOT the signer for this DID
assert pub_raw == did_pub, "key does not match DID — DO NOT re-sign with this key"

# 4) Optionally verify the EXISTING signature to identify the true signer
t = open('token.jwt').read().strip(); h, p, s = t.split('.')
sig = base64.urlsafe_b64decode(s + '='*(-len(s)%4))
try:
    Ed25519PublicKey.from_public_bytes(pub_raw).verify(sig, f"{h}.{p}".encode())
    print("existing sig valid under this key")
except InvalidSignature:
    print("existing sig by a DIFFERENT key (likely the real/redacted signer)")
```

Rules:
- If the correct private key is **redacted** (file contains `[REDACTED PRIVATE KEY]`), the token
  cannot be legitimately re-signed → BLOCKED, document.
- If an available key does not match the DID/registered public key, re-signing with it = spoofed
  identity. Refuse. This is F2/F11/AUTH territory.
- A JWS is only worth re-signing if it is still in its validity window; an already-expired
  ephemeral bootstrap token may be moot to revive.

## Ad-hoc verification: persist evidence BEFORE cleaning up the temp script

When the runtime demands ad-hoc verification (no canonical test command), you create a temp
script under `/tmp/hermes-verify-<name>.py`. **The passing output is the evidence — persist it
to a durable file first**, then delete the script:

```bash
python3 /tmp/hermes-verify-remediation.py 2>&1 | tee /root/forge_work/<date>-verification-evidence.txt
echo "exit=${PIPESTATUS[0]}"          # capture real exit, not tee's
rm -f /tmp/hermes-verify-remediation.py /tmp/hermes-verify-*.jsonl
```

If you delete the script without persisting output, the workspace is re-flagged "unverified"
on the next turn because the evidence vanished with the temp file. Durable evidence file +
cleanup of the script = verified AND clean.
