# WawaBot Probe & Capability Attestation Contract v1.0
**Authority:** F13 SOVEREIGN (Muhammad Arif bin Fazil)  
**Ratified Date:** 2026-10-10  
**Substrate Doctrine:** DITEMPA BUKAN DIBERI  
**Status:** CANONICAL_SPEC (ACTIVE)

---

## 1. Context & Motivation
Following the §2.1 & §3 operational audit from the distributed federation runtime:
1. **Network False Alarms:** Diagnostic and capability health checks querying loopback (`127.0.0.1`) or Mesh/Tailnet IPs (`100.64.0.0/10`) routinely trigger HTTP 400 (*Direct IP access not allowed*) or connection timeouts when intercepted by ambient HTTP proxies (`http_proxy`/`https_proxy`). This causes dashboards to falsely mark living organs as DOWN, causing severe human cognitive exhaustion and spurious escalations.
2. **Attestation Integrity vs Authenticity:** Hash-only receipts (`sha256`) guarantee payload integrity against bit-rot, but zero authenticity. A rogue or compromised node with root privileges can easily fabricate synthetic receipts with valid sha256 checksums. High-consequence claims require cryptographic non-repudiation.

---

## 2. Invariant A: Mandatory `no_proxy` Health Probes
Every automated probe script, monitoring daemon, and agent runner (including WawaBot and Kokpit probes) MUST enforce proxy bypass for internal federation communication:

```
NO_PROXY_DOMAINS = "127.0.0.1,localhost,100.64.0.0/10,local,.local"
```

### Implementation Rules:
- **Rule A.1 (Environment Stripping):** Direct Python probes utilizing `urllib.request` or `requests` must install a `ProxyHandler({})` or ensure environment variables `http_proxy`, `https_proxy`, `HTTP_PROXY`, and `HTTPS_PROXY` do not intercept traffic destined for internal subnetworks.
- **Rule A.2 (Subnet Exemption):** All Tailnet/Wireguard IP addresses (e.g., `100.64.0.2` af-forge, `100.64.0.5` kvm4-forge) and loopback addresses are strictly non-proxied.
- **Rule A.3 (Fault Classification):** A rejection returning HTTP 400 from a proxy gateway MUST NOT be classified as `service_down`. It is strictly classified as `E_PROXY_MISROUTE` (probe layer fault, not organ death).

---

## 3. Invariant B: Two-Tier Receipt Architecture for `CapabilityRecord`
Every capability assertion, health receipt, and organ state transition emitted into the federation ledger MUST declare its attestation tier:

```
CapabilityRecord:
  capability_id: string
  organ_id: string
  timestamp_utc: ISO8601
  status: UP | DOWN | DEGRADED
  tier: TIER_1_INTEGRITY | TIER_2_AUTHENTICITY
  attestation:
    receipt_sha256: string (Tier 1 & Tier 2)
    ed25519_signature: string (Tier 2 required)
    signer_public_key: string (32-byte Ed25519 hex/base64)
    canonicalization: "RFC_8785_JCS"
```

### Two-Tier Classification:
1. **Tier 1 (Fast Telemetry / Ephemeral Probes):**
   - **Mechanism:** Standard SHA-256 over raw JSON response.
   - **Scope:** High-frequency pulse checks (e.g., 5-second organ latency sweeps).
   - **Guarantee:** Transit integrity; minimal compute overhead.

2. **Tier 2 (High-Consequence Sovereign & Authority Claims):**
   - **Mechanism:** **Ed25519 (RFC 8032)** signature over canonical byte sequences normalized via **JSON Canonicalization Scheme (RFC 8785 - JCS)**.
   - **Scope:** State mutations, vault seals, capability grants, governance interventions, and F13-ratified records.
   - **Guarantee:** Cryptographic non-repudiation across multi-language nodes (Python, Node.js, Rust). Prevents key-order sorting discrepancies (Unicode code points vs UTF-16 code units).

---

## 4. Verification Gate
Any CapabilityRecord submitted to `VAULT999` or evaluated by `arif_judge` claiming high-consequence authority that lacks a valid Tier 2 RFC 8785 Ed25519 signature MUST fail-closed to `HOLD`.
