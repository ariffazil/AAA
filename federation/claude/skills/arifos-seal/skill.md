---
name: arifos-seal
description: 999_SEAL — Immutable ledger commitment. Use after apex_judge returns SEAL to finalize a decision and write it to VAULT999 with cryptographic proof.
version: 2026-03-04T1420
---

You are using the arifos-seal skill (stage 999_SEAL).

**Tagline:** Immutable ledger commitment.
**Trinity:** APEX (Ψ) | **Floors:** F1 (Amanah), F3 (Tri-Witness), F11 (Command Auth)
**Physics:** Noether's Theorem — conserved information
**Math:** H(parent) = H(H(left) + H(right)) — Merkle tree

## Operation

1. Verify prerequisites:
   - `apex_judge` returned SEAL verdict
   - `governance_token` is present (from `apex_judge` response)
   - F11 Command Auth is confirmed (human identity verified)

2. Call `seal_vault` with:
   - `event_type`: e.g. `decision`, `deployment`, `security_patch`
   - `payload`: JSON summary of what is being sealed
   - `verdict`: "SEAL"
   - `actor`: e.g. `arif-engineer`
   - `governance_token`: token from `apex_judge` — **required**, tamper-detects the chain

3. If `governance_token` missing or tampered → VOID. Do not proceed.

4. Verify the returned `merkle_root` matches the vault state.

5. Log the seal entry ID for the session record.

## Gen3 Tool
`seal_vault` (legacy: `vault_seal`)

## Critical Rules
- `seal_vault` is **token-locked** — pass `governance_token` from `apex_judge`. Missing = VOID.
- New entries must use `git add -f VAULT999/vault999.jsonl` to force-track.
- Sealing is **irreversible** — 888_HOLD applies if any doubt remains.

## Verdict
Returns immutable ledger entry with `entry_id` and `merkle_root`, or VOID if token invalid.
