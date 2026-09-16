# Seal Surfaces — Canonical Map v2026-08-30

> Zen of the updated seal protocols, forged after TB7 discovery + FQ-unstick completion trail.
> Live-verified 2026-08-30 (traces trc-47c6544bae73, trc-9e19c88735f6).

## The five real seal surfaces

| Surface | Path | Works for | Receipt form |
|---|---|---|---|
| **Kernel arif_seal** | MCP `arif_seal` mode=`seal` | Sovereign chain: init → judge → seal with `constitutional_chain_id` | VAULT999 append |
| **Kernel audit/record** | `arif_seal seal_purpose="RECORD"` + judge chain id | Documentary seals (no production state change) | VAULT999 append |
| **git_to_vault.py** | `/root/HERMES/scripts/git_to_vault.py` | Repo HEAD sealing — **idempotent** (already-sealed heads skip) | `COMMIT-<ORGAN>-<sha>` |
| **arifFlow pulse** | `POST :7073/ingest` step_type=`Seal` | Evidence-layer metabolic receipt | receipt_id (uuid) |
| **Organ-local ledgers** | e.g. WEALTH `/root/VAULT999/wealth/receipts.jsonl` | Organ-side evidence | jsonl append |

## Kernel arif_seal modes (verified live — TB7 correction)

Supported: `seal` | `dry_run` | `list` | `chain` | `retrieve_audit` | `deepnshadow`

**`mode: "receipt"` DOES NOT EXIST.** Any consumer script calling it fails regardless of
kernel health (qwen/FI-003's original seal was doomed before the 06:46 restart window).

## Authority gates (in order, all fail-closed)

1. Actor verification — no DPOP device key → `actor_verified: false` → OBSERVE_ONLY → no seal
   (TB4 class: FI-003, and currently FI-008 — only `arif` + `gemini-cli` keys exist in
   `/root/.secrets/aaa-identity/keys/`)
2. Session policy clamp — irreversible rank vs session threshold (SESSION_POLICY_CLAMP)
3. Judge chain — `constitutional_chain_id` + `judge_state_hash` from `.meta.kernel_intercept`
4. Floor re-measure at seal layer — judge SEAL ≠ append guaranteed

## Honest terminal states

- `receipt_state: UNSEALED` + judge verdict + call_hash + trace_id = **durable kernel evidence**
- Local outcome JSON + arifFlow Seal pulse = evidence layer, NOT VAULT999
- Never: fabricate judge_state_hash ("Floor breach"), burn nonces cycling, seal another
  actor's work under your own identity

## Agent-reported seal claims (binding rule)

Before echoing any agent's "SEALED::chain X" — `grep <chain-id> /root/arifOS/VAULT999/outcomes.jsonl`.
The AAA local chain (`:3001/health` → chain.seq) is NOT the canonical vault.

## Open work orders (from 2026-08-30 audit)

- TB4: DPOP key provisioning for FI-003/FI-008 — unlocks verified-actor lane (T1.5, F13)
- TB7: normalize consumer scripts to real modes (T2)
- SESSION_POLICY_CLAMP: SE-stage advance via proof bundle, or ceremonial-append doctrine (F13)
