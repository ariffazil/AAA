# 999_VAULT — MerkleV3 Ledger

> **CLAIM** | Source: `SovereigntyManifest.json` + workspace memory | **Confidence:** 0.92 | **Epoch:** 2026-04-23

## Summary

VAULT999 is arifOS's audit and sealing layer. Events that pass 888_JUDGE are sealed into a MerkleV3 ledger — append-only, cryptographically verifiable, non-repudiable.

**Motto:** DITEMPA BUKAN DIBERI — Forged, Not Given.

---

## Key Properties

| Property | Value |
|----------|-------|
| Hash algorithm | MerkleV3 |
| Append-only | Yes — no delete or edit |
| Event immutability | Cryptographically guaranteed |
| Tri-witness record | Human + AI + Earth timestamp |
| Audit trail | Queryable by epoch, agent, verdict |

---

## Sealed Event Structure

```json
{
  "epoch": "2026-04-23T12:04+08",
  "verdict": "SEAL",
  "dS": -0.04,
  "kappa_r": 0.07,
  "confidence": 0.72,
  "witness": {
    "human": "Arif Fazil",
    "ai": "ARIF-Perplexity",
    "earth": "github/b906c68"
  }
}
```

---

## APEX Holds (VAULT999 relevant)

- **APEX-HOLD-A:** VAULT999 schema changes blocked until snapshot+restore procedure in place
- **APEX-HOLD-B:** Supabase VAULT999 schema changes blocked until snapshot+restore procedure in place
- **APEX-HOLD-C:** Dockerfile.hardened promotion blocked until regression pass on all 21 containers

---

## Cross-References

- [[arifos/888_JUDGE]] — SEAL verdicts issued by 888_JUDGE
- [[arifos/FLOORS]] — F13 (Sovereign Scale) governs VAULT999 itself

---

## Status

**Stable** — MerkleV3 ledger structure is canonical. APEX-HOLD-B active until schema safeguard exists.

---

DITEMPA BUKAN DIBERI — 999 SEAL ALIVE