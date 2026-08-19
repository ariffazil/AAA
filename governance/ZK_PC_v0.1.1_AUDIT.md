# ZK-PC v0.1.1 — Audit Log
## Changes from v0.1 → v0.1.1

> **Forged:** 2026-08-12 by Hermes ASI
> **Status:** CHANGE LOG

---

## 1. What Was Right in v0.1 (No Changes)

These sections remain as drafted:
- **§1 Objective** — sound framing
- **§3 Core Entities** — clean A/B/C structure
- **§4 Commitment Generation** — canonical encoding correct
- **§5 Governance Root** — Merkle construction correct
- **§9 ZK Statement** — formal statement correct
- **§10-11 Inputs** — public/private separation correct
- **§12 Verification** — boolean output correct
- **§13 Predicate** — GovernancePredicate logic correct
- **§14 Revocation** — ROOT recomputation correct
- **§15 Security Model** — limits acknowledged honestly

## 2. What Needed Clarification

| Section | Issue | Fix in v0.1.1 |
|---------|-------|---------------|
| **§6** | Visual shares confused with ZK core | Marked as **optional, human-facing only** |
| **§7** | Reconstruction implied verifier-side | Clarified as **prover-side only** |
| **§8** | EXEC_KEY could be duplicated | Added `proof_id` binding |
| **§9** | No freshness constraint | Added `timestamp within Δ` |

## 3. What Was Missing (Critical Gaps Filled)

| # | New Section | Why Critical |
|---|-------------|-------------|
| **§16** | Cryptographic Primitives | Without hash/sig/curve choice, spec is unbuildable |
| **§17** | Circuit Description (Circom) | Without circuit, no proof system to deploy |
| **§18** | Setup Ceremony | Trusted setup needs public record |
| **§19** | Attestation Schema | Standardized signing format |
| **§20** | Threat Model | Adversary classes, security assumptions |
| **§21** | Implementation Path | Real tooling, file layout, deployment phases |

## 4. Open Questions (Pending F13 Resolution)

| # | Question | Default Assumption | Alternative |
|---|----------|-------------------|-------------|
| 1 | Hash function: SHA3-256 vs SHA-256? | SHA3-256 (PQ-ready) | SHA-256 (Ethereum compat) |
| 2 | Proof system: Groth16 vs PLONK? | Groth16 (compact) | PLONK (universal setup) |
| 3 | Curve: BN254 vs BLS12-381? | BN254 (mature) | BLS12-381 (ETH2.0) |
| 4 | Setup: Trusted vs Transparent? | Trusted (smaller proofs) | Transparent (Halo2/STARK) |
| 5 | Witness freshness window? | 60 seconds | 5-300 seconds |

## 5. What v0.1.1 Does NOT Do (Deferred)

- **Post-quantum security** — deferred to v0.2 (STARK migration)
- **MPC for sovereign key** — deferred to v0.3 (F13 hardening)
- **Formal circuit verification** — pre-mainnet audit (T+2 weeks)
- **Cross-chain deployment** — Base/Optimism in Phase 4 only
- **Recursive proofs** — aggregation layer for v0.4

## 6. Verdict Trail

| Version | Verdict | Source |
|---------|---------|--------|
| ZK-PC v0.1 | PARTIAL-SEAL | Initial spec draft |
| ZK-PC v0.1.1 | READY FOR F13 | This revision |
| ZK-PC v0.2 | TBD | After v0.1.1 ratification + implementation |

---

*Forged: 2026-08-12. Audit closed. Awaiting F13 ratification.*