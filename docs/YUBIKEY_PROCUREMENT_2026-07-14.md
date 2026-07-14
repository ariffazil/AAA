# YUBIKEY_PROCUREMENT_2026-07-14.md — Sovereign Procurement Brief

> **Authority:** Sovereign ack (F13, 2026-07-14)
> **Status:** Procurement brief — ready to execute
> **Forge cycle:** FEDERATION-ALIGN-2026-07-14
> **Phase:** 6 of IDENTITY_BINDING_SPEC (deferred until keys in hand)

---

## 1. Why hardware-backed keys

Phase 1 of IDENTITY_BINDING_SPEC uses host-stored Ed25519 keys. That works for shadow mode. For **production sovereign authority** (SEAL_AUTHORITY_DOCTRINE §6: SOVEREIGN band), the private key must not live on the host filesystem. A YubiKey (or comparable FIDO2/PIV token) holds the key in secure element; signing happens on-device; key never leaves.

A stolen host = no compromise of sovereign authority.
A stolen YubiKey + PIN = still no compromise without physical possession + PIN.

## 2. Recommendation: YubiKey 5 NFC

| Spec | Detail |
|---|---|
| Model | YubiKey 5 NFC (or 5C if USB-C only) |
| FIDO2 / WebAuthn | Yes |
| PIV (smart card) | Yes — Ed25519 supported via PIV slot 9c (authentication) |
| OpenPGP | Yes — Ed25519 natively |
| Price | ~$50 USD each |
| Vendor | yubico.com (official) or authorised reseller |
| Lead time | Usually in stock; 2-3 day shipping |

**Why YubiKey over Ledger Nano S/X:** FIDO2/PIV integration with standard PKCS#11 is more mature. yubikey-agent + ssh-keygen works out of the box. Ledger requires more custom integration.

## 3. Quantity

Per IDENTITY_BINDING_SPEC §9 sovereign override + multi-agent:

| Key | Purpose | Quantity |
|---|---|---|
| Sovereign primary | F13 daily SEAL authority | 1 |
| Sovereign backup | F13 cold storage / emergency | 1 |
| Agent keys (one per active AAA warga) | kimi-code, antigravity-AAA, hermes, grok-build, opencode, etc. | 3-5 |
| Spare / decommissioned | Rotation buffer | 1-2 |

**Total: 6-8 YubiKeys. Budget: ~$400 USD.**

## 4. Procurement path (sovereign discretion)

**Option A — Yubico direct:**
- yubico.com → Shop → YubiKey 5 NFC → add 6-8 to cart
- Checkout with sovereign's preferred payment
- Ships from US/EU; 2-3 days to MY

**Option B — Local reseller (faster MY delivery):**
- Search "YubiKey Malaysia" on Lazada/Shopee
- Verify reseller authorisation (avoid counterfeits — buy direct if uncertain)
- Same-day or next-day delivery
- Higher price (~RM 250 each ≈ $55 USD)

**Option C — Enterprise bulk (if multi-org deployment):**
- Yubico enterprise sales: yubico.com/contact
- Volume discount possible for ≥10 units
- Slower procurement (procurement approval process)

## 5. Required dependencies (post-procurement)

Once YubiKeys are in hand, Phase 6 implementation requires:

```bash
# On each host where an actor signs:
apt-get install yubikey-manager                # ykman CLI
apt-get install libykcs11-dev pcscd            # PKCS#11 module for Ed25519
pip install python-yubikey-manager
# FIDO2 / WebAuthn libraries
pip install fido2 webauthn
```

## 6. Phase 6 (deferred) — Implementation outline

```python
# /root/arifOS/arifosmcp/runtime/hardware_binding.py (Phase 6)

from cryptography.hazmat.primitives.serialization import pkcs12
from ykman.device import list_all_devices
from yubikit.piv import PivSession

def sign_with_yubikey(payload: bytes, slot: str = "9c") -> bytes:
    """Sign payload using Ed25519 key stored in YubiKey PIV slot."""
    devices = list_all_devices()
    if not devices:
        raise HardwareBindingError("no YubiKey detected")
    device, info = devices[0]
    with device.open_connection() as conn:
        session = PivSession(conn)
        # Slot 9c = PIV Authentication (Ed25519 supported)
        return session.sign(slot, payload)
```

This replaces Phase 1's host-stored `actor_binding.sign()` with hardware-backed signing. **The actor_binding.py interface is unchanged** — only the implementation swaps.

## 7. Sovereign key ceremony (when keys arrive)

Once YubiKeys in hand:

1. **Init ceremony** (sovereign-only):
   - Generate Ed25519 keypair on each YubiKey PIV slot 9c
   - Export public keys only
   - Store public keys in `/root/.arifos/keys/sovereign/{key_id}.pub`
   - Backup BIP-39 mnemonic of any wallet-recovery keys (if applicable) to sealed envelope in sovereign safe

2. **Registration ceremony** (T3, sovereign-led):
   - Register each sovereign pub with arifOS kernel registry
   - SEAL the registration event to VAULT999 with witness: human=ARIF-F13, ai=kimi-code-FI-008, external=seal_chain_head
   - This is the F13 SOVEREIGN override path: any SEAL with `actor_source: sovereign_directive` is honored

3. **Operational ceremony** (daily):
   - YubiKey plugged in for sovereign SEALs
   - PIN entered each session
   - Key removed when not in use

## 8. Open questions

- **Sovereign PIN policy:** PIN complexity? Rotation cadence? Brute-force lockout?
- **Backup strategy:** BIP-39 mnemonic acceptable, or paper-only / metal plate (Cryptosteel)?
- **Geographic distribution:** Sovereign + 1 backup in same safe, or split (one at home, one at office)?
- **Agent YubiKeys:** same model (YubiKey 5 NFC) or smaller (YubiKey 5C Nano, $25) for daily-driver agents?

## 9. Procurement timeline (estimated)

| Day | Action |
|---|---|
| 0 | Sovereign orders 6-8 YubiKeys |
| 1-3 | Shipping to MY |
| 3-4 | Receipt + initial inspection |
| 4-5 | Init ceremony (generate keypairs, register pubs) |
| 5+ | Phase 6 implementation begins |

Cutover from Phase 1 (host-stored) to Phase 6 (hardware-backed) requires:
- 7-day parity after Phase 6 code ships
- Sovereign second ack
- Rollback plan tested (host-stored keys still valid as fallback)

---

## Provenance

- Phase 6 of IDENTITY_BINDING_SPEC.md
- Brief for sovereign execution
- Audit cycle: FEDERATION-ALIGN-2026-07-14
- Vault head: seq 9914, sha256:6517b1fb1171e9461c1d8af634119acdc031e61767fbe44e0547a7336544880b

DITEMPA, BUKAN DIBERI.