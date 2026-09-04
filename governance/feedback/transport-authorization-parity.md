# Transport Authorization Parity

> **Forged:** 2026-09-04 · From ARIF-Perplexity constitutional correction
> **Status:** ACTIVE
> **DITEMPA BUKAN DIBERI**

---

## Invariant

**Different transport may use different credentials. Different transport may not use weaker authorization.**

The in-process PEM-sign lane is a separately governed authority path for approved local operations — NOT a bypass.

## What this means

- The kernel (arifOS :8088) uses ACT/JWT tokens for authorization.
- The legacy federation_ritual.py uses HMAC bearer tokens.
- The in-process PEM-sign lane uses Ed25519 signatures.
- These are different transport mechanisms, not different governance levels.
- Each must meet or exceed the authorization strength of the canonical path.
- No transport may silently downgrade the authorization requirements.

## Failure modes

| Scenario | Correct behavior |
|---|---|
| Bearer token attempts to authorize SEAL | Reject — SEAL requires ACT/JWT |
| PEM-sign attempts to authorize vault append | Reject — vault append requires ACT/JWT + human approval |
| Expired capability on any transport | Reject — expiry is universal |
| Scope mismatch on any transport | Reject — scope is universal |

## Application

This invariant applies to:
- ACT/JWT tokens (canonical)
- HMAC bearer tokens (legacy)
- Ed25519 PEM signatures (in-process)
- Any future transport mechanism

Each transport is independently governed. None may bypass the others' requirements.
