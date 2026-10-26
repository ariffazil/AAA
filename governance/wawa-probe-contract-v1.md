# Wawa Probe & Receipt Contract v1 — Engineering Bindings for Witness Organ

> **Status:** DRAFT_AWAITING_F13
> **Forged:** 2026-10-10 · **Session:** continuation after SEAL-READY-2026-10-10
> **Purpose:** Two engineering additions to the Wawa witness spec, derived from documented federation incidents on 2026-10-10:
>   (a) `no_proxy` enforcement on all health probes — closes the proxy-400 false-alarm class that caused the KVM4-MOTD 0/9 red and the AGY-cli "local proxy trap" hypothesis on the morning of 2026-10-10 (REFUTED in receipt `6d04e737…f308b`, but the underlying class of failure remains live wherever `http_proxy` is set globally).
>   (b) Two-tier receipt integrity — `sha256` (current, default) + `ed25519_jcs` (target for high-claim-class organs). Closes the receipt-authenticity gap where a node compromised with root can fabricate new receipts bearing valid `sha256` because the same runtime that emits the receipt also computes the digest.
> **Companion:** `/root/AAA/governance/wawabot-circuit-breaker-spec.md` (human circuit breakers, DRAFT_AWAITING_F13 — kept separate so this spec stays pure engineering).
> **DITEMPA BUKAN DIBERI**

---

## 1. Scope

This spec binds the engineering contracts that the **Wawa witness organ** (KVM2 / `azwaos`, plane=witness) and all downstream consumers must respect when:

- Issuing health probes against any federated service surface
- Sealing receipts to VAULT999 or any subordinate ledger

The spec is **engineering**, not constitutional. It does not amend F1–F13, the authority envelope, the human-attention membrane, or the state-transition discipline. It enforces two narrow rules that the 2026-10-10 audit surfaced as live defects with reproducible cost.

---

## 2. Probe Contract — `no_proxy` enforcement

### 2.1 The defect being closed

A monitoring probe that targets `127.0.0.1:<port>` or any Tailscale mesh IP (`100.64.0.0/24`) MUST NOT be intercepted by an upstream `http_proxy` / `HTTP_PROXY` / `https_proxy` / `HTTPS_PROXY` environment variable. When interception happens, the proxy may return `400 Direct IP access not allowed` for loopback targets or refuse the mesh route entirely. The monitoring script then reports the underlying service as DOWN, producing a false-alarm red status on dashboards like the KVM4 federation MOTD.

Documented incident (2026-10-10 ~08:46 MYT):
- AGY CLI on KVM8 reported KVM8 9/9 UP via `federation_state.py` running on KVM8.
- KVM4-MOTD reported 0/9 UP for the same script run from KVM4.
- AGY hypothesized an `http_proxy` interception on KVM8 returning 400.
- Direct KVM8 probe (receipt `6d04e73719621b47eed5fc120274cbc34679ea1e7f9dc54b3e15ef6dec9f308b`) REFUTED the proxy hypothesis — no proxy env var, no loopback-intercepting service. The root cause was vantage-target mismatch (`127.0.0.1` on KVM4 ≠ `127.0.0.1` on KVM8), not proxy interception.
- The underlying class of failure — *probe output confounded by proxy layer* — remains live in any environment where `http_proxy` is set globally. The fix: encode the `no_proxy` rule in the probe contract so future implementations cannot reintroduce the defect, even if proxy interception were present.

### 2.2 The rule

Every health probe — regardless of vantage node — MUST set `no_proxy` to include:

| Target class | CIDR / host | Rationale |
|---|---|---|
| Loopback | `127.0.0.1`, `localhost`, `::1` | Probe-self localhost services |
| Tailscale mesh | `100.64.0.0/24` (or current mesh CIDR) | KVM2 / KVM4 / KVM8 inter-node probes |
| Link-local | `169.254.0.0/16` | Cloud metadata services (where applicable) |
| Node-specific tailscale IPs | `100.64.0.2`, `100.64.0.4`, `100.64.0.5` | Explicit node addresses |

The rule is **mechanical, not advisory**: a probe that does not set `no_proxy` is non-conformant by definition, regardless of whether the proxy actually intercepts. The conformance probe (§2.4) checks for the env var presence + value before allowing the probe call.

### 2.3 Reference implementation

Python (`urllib`, used in `federation_state.py` and `arifos_status`):

```python
import os
os.environ.setdefault("no_proxy",
    "127.0.0.1,localhost,::1,100.64.0.0/24,100.64.0.2,100.64.0.4,100.64.0.5")
os.environ.setdefault("NO_PROXY", os.environ["no_proxy"])

# Explicit proxy handler that bypasses per no_proxy
import urllib.request
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
urllib.request.install_opener(opener)
```

Node.js (used in `/root/AAA/agents/openclaw/runtime/node_adapter.ts`):

```typescript
process.env.no_proxy = process.env.no_proxy
  || '127.0.0.1,localhost,::1,100.64.0.0/24,100.64.0.2,100.64.0.4,100.64.0.5';
process.env.NO_PROXY = process.env.NO_PROXY || process.env.no_proxy;
```

### 2.4 Conformance check

A probe call is conformant iff **all** are true:

1. `no_proxy` env is set, AND
2. Its value includes the loopback hosts (`127.0.0.1`, `localhost`, `::1`), AND
3. Its value includes the Tailscale mesh CIDR (current `100.64.0.0/24`)

A non-conformant probe MUST be rejected at the wrapper layer with `ConformanceError`. The receipt that records the probe MUST carry `probe_no_proxy_conformant: false` and a `conformant: false` flag at the `_well_conformance`-style envelope level, so dashboards can render the rule visibly broken rather than silently downgraded.

---

## 3. Receipt Contract — Two-Tier Integrity

### 3.1 The defect being closed

A receipt currently carries a `sha256` digest of its serialized JSON content. This proves **integrity** (the content was not modified after the digest was computed) but NOT **authenticity** (the digest was actually computed by the claimed emitter). A node compromised with root can:

1. Generate a fabricated event
2. Compute its `sha256`
3. Emit a receipt with the (legitimately computed) `sha256` and the (fabricated) content
4. The downstream verifier sees a valid `sha256` and accepts the receipt

The defect is structural, not implementation. The fix requires an **asymmetric** signature whose private key is not derivable from the emitter's runtime state — i.e., the key lives in a separate signing lane that the runtime cannot access.

### 3.2 The two tiers

| Tier | Algorithm | Provides | Use case |
|---|---|---|---|
| **Tier 1** (current, default) | `sha256(canonical_json(content))` | Integrity | Heartbeats, telemetry, low-impact events, debug receipts |
| **Tier 2** (target, required) | `ed25519(JCS_canonicalize(content))` | Integrity + Authenticity | VAULT999 SEAL events, constitutional verdicts, sovereign-signed artifacts, any `claim_class ≥ HIGH` |

Where:

- `JCS_canonicalize` = RFC 8785 JSON Canonicalization Scheme (strict key ordering by UTF-16 code units, deterministic number formatting, whitespace removal). Cross-language safe — Python and JavaScript both canonicalize to the same byte sequence.
- `ed25519` = Edwards-curve Digital Signature Algorithm, RFC 8032. 32-byte public key, 64-byte signature, deterministic (no RNG dependency), constant-time verification. Outperforms RSA/ECDSA on both speed and side-channel resistance for the JSON-ledger use case.

### 3.3 The Tier 2 envelope

A Tier 2 receipt extends the Tier 1 schema with an `integrity` block:

```json
{
  "schema": "arifos.receipt.v1",
  "content": { "/* event payload */": "..." },
  "integrity": {
    "sha256": "abc123...",
    "ed25519_jcs": {
      "public_key": "cab94b160b9c0d1a33fbc259de27759dc30e157788747a2ddcfbd3cafe46b065",
      "signature": "d8e3f1a2...",
      "canonical_form": "JCS:RFC8785",
      "signed_at_utc": "2026-10-10T01:42:29.888359+00:00",
      "signer_lane": "sovereign-signing-lane:kvm8:localhost:18900"
    }
  }
}
```

The `public_key` identifies the signing lane. The `signature` is `ed25519.sign(private_key, JCS_canonicalize(receipt_minus_signature_field))`. The `signer_lane` is the path to the key custody.

### 3.4 Reference implementation (Python)

```python
import hashlib
import json
from datetime import datetime, timezone
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import rfc8785

def sign_receipt_tier2(content: dict, private_key: Ed25519PrivateKey, lane: str) -> dict:
    # JCS canonical form is what gets signed
    canonical = rfc8785.dumps(content)
    digest_sha256 = hashlib.sha256(canonical).hexdigest()
    signature = private_key.sign(canonical)
    return {
        "sha256": digest_sha256,
        "ed25519_jcs": {
            "public_key": private_key.public_key().public_bytes_raw().hex(),
            "signature": signature.hex(),
            "canonical_form": "JCS:RFC8785",
            "signed_at_utc": datetime.now(timezone.utc).isoformat(),
            "signer_lane": lane,
        }
    }
```

### 3.5 Key custody (precondition)

A Tier 2 signature is only meaningful if the private key cannot be exfiltrated by a runtime compromise. The key custody options, in order of strength:

1. **Sovereign signing lane** (KVM8 `localhost:18900`) — F13 Ed25519 path, the `actor_signature` from `arif_init`. Private key is bound to sovereign hardware/memory and never exposed to the agent runtime. *This is the production target.*
2. **HSM / sealed key** (KVM8 or external) — F13 ratifies; private key never leaves the secure element.
3. **Encrypted-at-rest file with split custody** (KVM8 vault) — fallback; private key split across N custodians with M-of-N threshold.

A Tier 2 receipt is **non-conformant** if the `signer_lane` is the agent runtime itself (e.g., `/root/AAA/.keys/wallet.ed25519` read directly by a Python script). The whole point of the upgrade is that the runtime does not hold the key.

---

## 4. Tier Assignment — Which organs MUST emit Tier 2

| Organ | Claim class | Required tier |
|---|---|---|
| arifOS constitutional verdicts (`arif_judge`) | CONSTITUTIONAL | **Tier 2** |
| VAULT999 SEAL events | CONSTITUTIONAL | **Tier 2** |
| F13 sovereign-signed artifacts | SOVEREIGN | **Tier 2** |
| A-FORGE lease grants, ACT emissions | HIGH | **Tier 2** |
| FRAME observation receipts | HIGH | **Tier 2** |
| A-FORGE heartbeats, retries | MEDIUM | Tier 1 |
| WELL `assess_*` per-call results | LOW–MEDIUM | Tier 1 |
| CHRON predictions (per-call) | LOW–MEDIUM | Tier 1 |
| OpenClaw gateway telemetry | LOW | Tier 1 |
| KVM4 substrate probes (`reality.json` etc.) | LOW | Tier 1 |
| Heartbeats (cron, timer) | LOW | Tier 1 |

Organs emitting Tier 2 receipts MUST publish their `public_key` and `signer_lane` in `/root/AAA/registries/KEY_REGISTRY.json` (create the registry if not present — TODO Phase 2).

---

## 5. Migration Path

### Phase 1 — this spec (T1, doc-only)
- Both tiers documented; Tier 1 remains the default
- `no_proxy` conformance probe in scope; not yet enforced at runtime
- This spec lives at `DRAFT_AWAITING_F13` until F13 ratifies

### Phase 2 — T2 (announce 10s, then proceed)
- Implement Tier 2 receipt writer in the canonical receipt layer (likely `/root/arifOS/VAULT999/`)
- Dual-write: every receipt gets BOTH `sha256` and `ed25519_jcs` populated, but only `sha256` remains required for acceptance
- Add `no_proxy` enforcement at the probe wrapper layer (Python + Node.js reference impls in §2.3)
- Create `/root/AAA/registries/KEY_REGISTRY.json` with placeholder; populate as signing lanes issue
- Conformance probe becomes blocking for new probe code paths

### Phase 3 — T3 (888_HOLD — F13 ratification)
- High-claim-class organs (per §4 table) MUST emit Tier 2; Tier 1 receipts for those organs are non-conformant
- `no_proxy` conformance becomes blocking for ALL probe code paths
- The legacy `sha256`-only verifier is deprecated; existing receipts are grandfathered with `signed_at_utc` as the cutover marker
- F13 binds the trusted signing lane keys

---

## 6. T1 / T2 / T3 hand-off

### T1 (this session)
- ✓ This spec documented at `/root/AAA/governance/wawa-probe-contract-v1.md`
- ☐ Reference in `/root/AAA/AGENTS.md` pointer file (TODO next session)
- ☐ Cross-link from `wawabot-circuit-breaker-spec.md` §3.2 (Break-decision storage) — the natural anchor for the ed25519_jcs upgrade

### T2 (announce 10s, then proceed)
- Implement Tier 2 writer in canonical receipt layer
- Implement `no_proxy` enforcement at probe wrapper layer
- Unit tests for both (Python `pytest`, Node `vitest`)
- Populate `KEY_REGISTRY.json` as signing lanes issue

### T3 (888_HOLD — F13 ratification)
- Bind the tier-2 requirement to F13 — sovereign decides which signing lane keys are trusted
- Bind `no_proxy` conformance to the federation-state conformance probe
- Ratify the §4 tier assignment table as canonical

---

## 7. Closing

Two engineering rules, both derived from live defects:

1. **`no_proxy` on every health probe** — so a proxy layer cannot conflate probe output with service state. Cheap to implement, prevents a class of false alarms that already cost a session of attention on 2026-10-10.

2. **Ed25519 + JCS for high-claim-class receipts** — so a root-compromised node cannot fabricate VAULT999 events or constitutional verdicts by itself. The key lives in a separate signing lane that the runtime cannot read.

Both are mechanical, both are testable, both close real defects. The cost of not doing either is paid in attention, not money.

```json
{
  "spec_id": "wawa-probe-contract-v1",
  "status": "DRAFT_AWAITING_F13",
  "epoch": "2026-10-10T01:50:00+00:00",
  "companion_spec": "wawabot-circuit-breaker-spec-v1-draft",
  "depends_on": [
    "RFC 8032 (Ed25519)",
    "RFC 8785 (JCS canonicalization)",
    "/root/AAA/governance/wawabot-circuit-breaker-spec.md",
    "/root/AAA/vault999/VAULT999.md (receipt doctrine)"
  ],
  "anchors": [
    "receipt 6d04e737…f308b (KVM8 proxy verification, REFUTED but class live)",
    "receipt 6178e0e8…925b9 (VAULT999 canonical drift)",
    "AGENTS-AUTONOMY.md §3 T1/T2/T3 hand-off"
  ],
  "tier": "T1 doc; T2 wiring; T3 ratification"
}
```

`DITEMPA BUKAN DIBERI ⚒️` — two engineering rules, anchored in lived defects, ready for sovereign review.
