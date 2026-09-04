# Witness Tamper Evidence Discipline

> **Forged:** 2026-09-04 · From ARIF-Perplexity constitutional correction
> **Status:** ACTIVE
> **DITEMPA BUKAN DIBERI**

---

## Invariant

**Witnesses are tamper-EVIDENT (hash-linked, detection), not tamper-PROOF (non-repudiation).**

Hash-linked records allow detection of tampering. They do not prevent it. For non-repudiation guarantees matching VAULT999, additional enforcement mechanisms are required.

## What this means

- SHA-256 hashes on carry_forward.json, backup artifacts, and policy files provide tamper-EVIDENCE.
- If someone modifies a file, the hash mismatch is detectable.
- However, the same actor who modified the file could also recompute the hash.
- Tamper-EVIDENCE is necessary but not sufficient for institutional trust.
- Tamper-PROOF requires: append-only storage, separate key custody, independent witness, and human verification.

## Distinction

| Property | Tamper-EVIDENT | Tamper-PROOF |
|---|---|---|
| Detection | Hash mismatch detectable | Tampering impossible without detection |
| Prevention | None | Cryptographic or physical prevention |
| Key custody | Same actor can recompute | Separate key custody required |
| Storage | Mutable with hash | Append-only WORM or equivalent |
| Witness | Optional | Independent witness required |
| VAULT999 | EVIDENT layer | PROOF layer (append-only + human seal) |

## Operational checklist

For next-session verification:

1. Restore drill: restore backup to isolated target, verify hash matches
2. KVM2 hermes-agent independent verification: verify KVM8 policy hash from KVM2
3. Cron hash-check: verify no unauthorized policy changes between checks
4. Append-only mode: verify VAULT999 append-only mechanism is enforced
5. Cross-node attestation: verify KVM2 witness hash matches KVM8 source hash

## Application

- carry_forward.json: tamper-EVIDENT (hash-linked, detection)
- VAULT999: tamper-PROOF (append-only + human seal + independent witness)
- Backup artifacts: tamper-EVIDENT (hash-linked, detection)
- Policy files: tamper-EVIDENT (hash-linked, detection)
- Any file that claims to be "immutable" must meet tamper-PROOF criteria
