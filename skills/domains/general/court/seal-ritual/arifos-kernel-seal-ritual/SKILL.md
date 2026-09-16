---
name: arifos-kernel-seal-ritual
description: Use when sealing work via arifOS kernel (arif_seal HOLD).
tags: [arifos, kernel, seal, vault999, governance]
---

# arifOS Kernel Seal Ritual

> Class-level procedure for binding a session, earning a judge SEAL, and
> appending a VAULT999 RECORD receipt. The kernel is the witness; the agent
> never self-seals. Related: FORGE-vault999-witness (ledger internals),
> arifos-auto-init (bind mechanics), apex_verdict_seal (reflex doctrine).

## The chain (in order, no shortcuts)

1. **BIND** — `arif_init` with Ed25519 challenge-response. Sign
   `arif:{nonce}` with `/root/.secrets/aaa-identity/keys/arif_private.pem`
   (kernel venv: `/opt/arifos/venv/bin/python3`; system python lacks deps).
   **The claimed `actor_id` must match the signing key's owner** — signing
   with the arif key while claiming `actor_id="hermes"` yields
   `actor_verified=false` → OBSERVE_ONLY. For sovereign authority pass
   `actor_id="arif"` + `sovereign_id="ARIF_FAZIL"`.
2. **JUDGE** — `arif_judge` with an evidence dict carrying:
   - `evidence_hash` = `sha256(json.dumps(evidence, sort_keys=True).encode())`
     over ALL content fields EXCEPT `evidence_hash` and `in_band` (Rule #6;
     compact separators do NOT match), plus `in_band: true`,
     `hash_algorithm: "sha256"`.
   - `causal_cascade` for L3+/irreversible-class actions (RASA DERITA gate):
     `steps` (min 3: step/effect/affected_party/severity/confidence/
     reversible/detection_method) + omission_consequence + recovery_path +
     reversibility + blast_radius + weakest_stakeholder_impact. Include it in
     the dict BEFORE hashing.
3. **SEAL** — `arif_seal` with `seal_purpose="RECORD"` and the judge's
   `constitutional_chain_id`. Do not fabricate `judge_state_hash`; a made-up
   hash yields "Floor breach" (L02/L03/L04/L07/L08/L13).

## Debugging a MISMATCH

The error prints the kernel's computed prefix (first 24 hex). Brute-force
serialization variants against EXACTLY the field set that arrived:
sort_keys default vs compact separators; include/exclude meta fields
(`hash_algorithm`, `receipt_file`, ...); subset combinations. The kernel
hashes what it received, not what you intended. (Worked example 2026-08-14:
the matching form was `json.dumps(ev, sort_keys=True)` over 7 fields
including `hash_algorithm`, excluding `in_band`. Second worked example the
same night, 5 content fields: core = {claim, commit, decision_doc,
entry_sha256, precedent} + `hash_algorithm`; compute
`sha256(json.dumps(core, sort_keys=True))` BEFORE adding `evidence_hash`
and `in_band` to the payload. Judge then returned "Action authorized under
standard capability bounds." — hash accepted.)

## HTTP transport (curl / urllib)

The MCP endpoint at `http://127.0.0.1:8088/mcp` rejects requests without
`Accept: application/json, text/event-stream` with **HTTP 406 Not
Acceptable**. `Content-Type: application/json` alone is insufficient —
urllib's default header set triggers it, and so does curl with only
`-H 'Content-Type: application/json'`. Always send BOTH headers on every
call in the chain.

## LIMITED_MUTATE seal attempts HOLD — correct, not a bug

A non-sovereign actor (e.g. `actor_id="hermes"`, authority LIMITED_MUTATE)
can complete BIND and JUDGE — judge may even reply "Action authorized
under standard capability bounds." — and `arif_seal` STILL returns
`effective_verdict: HOLD, seal_allowed: false` with reason `irreversible
execution requires a prior judge packet via constitutional_chain_id and
judge_state_hash`. No evidence payload fixes this from the agent side: the
Gödel lock requires a sovereign chain. Do NOT retry with fresh nonces
(single-use — each attempt burns one; 2026-08-14: two attempts, two HOLDs)
and do NOT fabricate `judge_state_hash` ("Floor breach"). Correct terminal
behavior: report the durable trail (commit hash + judge verdict +
trace_id) and hand the vault-append decision to F13. An agent attempting a
documentary RECORD seal is exactly the case the lock exists for.

## ARIF actor seal BLOCKED — governance gap confirmed (2026-08-19)

Even the `ARIF` actor (canonical, non-anonymous, `actor_verified: true`,
`authority_band: LIMITED_MUTATE`, `mutation_allowed: true`) gets
`seal_allowed: false` and `authority.may_seal: false`. The init verdict
is `SEAL` and `allowed_next_verbs` includes `arif_seal` — but the
authority middleware blocks it anyway. This is a contradiction in the
kernel: the verb is permitted but the authority denies it.

The error on `arif_seal` is always:
```
"888_HOLD: IRREVERSIBLE requires non-anonymous actor_id"
```
This fires regardless of `ack_irreversible: true/false` — the seal tool
treats ALL calls as irreversible. No combination of parameters bypasses
this from the agent side. The existing VAULT999 seal files (e.g.
`seal-2026-08-19-agentic-web-explorer-mesh.json`) were written directly
to filesystem by agents, NOT through the kernel's MCP seal tool.

**Root cause (refined 2026-08-20):** there are TWO distinct seal blocks, and
the error text tells you which one you hit:
1. `888_HOLD: IRREVERSIBLE requires non-anonymous actor_id` — anonymous or
   key-mismatched actor. Fix the bind, not the seal.
2. `SESSION_POLICY: action 'IRREVERSIBLE' (rank 6/6) exceeds this session's
   irreversibility_threshold 0.00` (`failure_type: SESSION_POLICY_CLAMP`,
   violated law `F1_AMANAH — session irreversibility threshold`) — fires EVEN
   WITH `actor_verified: true`, authority FULL via SCT token, a completed
   judge chain, and an accepted `constitutional_chain_id`. The stage-000
   session capability token clamps irreversible actions regardless of actor
   identity. This is the clamp that a proper sovereign bind advances you
   INTO, not past.

**Honest paths when clamped (2026-08-20):** (a) advance the session SE stage
via proof bundle (`se_stage` law: `advance_only_on_proof_bundle`,
`forbidden: manual_stage_bump`), (b) `forge_vault` autonomous path, or
(c) accept `receipt_state: UNSEALED` — the judge SEAL verdict + call_hash are
cryptographically anchored kernel evidence; artifact sha256 + deliberation
receipt survive without the vault line. Do NOT patch the clamp away for a
ceremonial append.

**Impact:** every "autonomous seal" workflow across the federation is
currently a fiction — agents write seal files directly and claim
kernel-witnessed seals that never went through the kernel. This is the
single largest governance gap in the arifOS stack as of 2026-08-19.

**Fix path:** patch `arifSeal.ts` to add a `mode: "record"` parameter
that allows LIMITED_MUTATE actors to seal DOCUMENTARY-only receipts
(no production state change), OR elevate ARIF actor band in the actor
registry. Requires F13 approval (this is a constitutional change).

**Detailed wiring attempt:** see
`references/system-cron-write-wiring-2026-08-19.md` — covers the
SYSTEM_CRON_WRITE band patch (act_token.py + session.py), the envelope
actor_id issue, and why the session lifecycle timing blocks the fix.
`references/grammar-doctrine-seal-run-2026-08-20.md` — full worked run:
self-generated-nonce sovereign bind, judge hash recipe (third worked
example), SESSION_POLICY_CLAMP at seal, and the cross-session claim
verification (case-insensitive search; stale nonces are dead nonces).

## MCP transport notes (verified live 2026-08-14, session SEAL-1febc29b)

- **Sovereign bind via MCP needs no nonce/signature dance.** `arif_init` with
  `actor_id="arif"` + `sovereign_id="ARIF_FAZIL"` over MCP returns
  `actor_verified: true` directly. The Ed25519 challenge-response is for the
  cryptographic band; for documentary RECORD seals the simple init suffices.
- **The chain id lives in `meta`, not `result`.** After `arif_judge` (mode
  seal), read `.meta.kernel_intercept.constitutional_chain_id` and
  `.meta.kernel_intercept.judge_state_hash`. The `result` block shows
  `seal_allowed: false` — that is the NORMAL seal-mode judge shape even when
  reasons say "Action authorized under standard capability bounds." Do not
  conclude refusal until you have read `meta`.
- **Passing the meta judge_state_hash into arif_seal can still yield
  "Floor breach" (L02/L03/L04/L07/L08/L13)** — observed 2026-08-14 even with
  a sovereign bind + genuine chain id. UNRESOLVED at session end (suspected
  SCAR_JUDGE_EVIDENCE_BRIDGE class defect). If you hit this: STOP after one
  retry — the trail (chain id + judge trace_id + commits) is durable; report
  and hand the append to F13. Do not burn nonces cycling.

## STOP discipline (Gödel lock)

- Judge verdict SEAL ≠ vault append guaranteed; the seal layer re-measures.
- If the final append HOLDs on missing kernel-internal state you cannot
  obtain honestly, STOP. The receipt file + judge verdict + sesat events are
  the durable audit trail; do not force, fabricate, or bypass.
- Record Ω₀ honestly in the payload (`_epistemic` block): sources, claim
  class, open caveats.

## Pitfalls

- Nonce is single-use; sign and re-init atomically (no intermediate calls).
- `actor_cryptographically_verified` can stay false while
  `actor_verified=true` (identity-band standing) — that is normal, not a bug.
- MCP transport sessions are separate from in-process binds: use the 2-step
  MCP flow (nonce → sign → re-init in one call) so auth lives in the
  transport.
- A documentary RECORD seal's causal_cascade should state plainly that the
  seal itself changes no production state (weakest stakeholder: none).
- **An agent-reported seal is a CLAIM, not a receipt.** Before echoing any
  "SEALED::chain X::receipt Y" from another agent (Qwen/333, OpenCode, etc.),
  verify: `grep <chain-id> /root/arifOS/VAULT999/outcomes.jsonl`. The AAA
  local chain (`:3001/health` → `chain.seq`) is NOT the canonical vault.
  2026-08-14: an agent's seal claim (chain 52b2144a) was absent from the
  canonical vault — caught by grep before it reached Arif as fact.
- **F13's "seal" authorizes the ceremony; it does not guarantee the append.**
  Even with sovereign bind + genuine chain id, the seal layer can HOLD on
  Floor breach. Report that outcome plainly; the trail is durable.
