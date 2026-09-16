# RECEIPT Type Taxonomy (2026-08-10)

> Reference companion to `claim-receipt-discipline` §Failure Mode 5.
> Source session: Hermes ZEN audit + entropy purge (2026-08-10).

## Why this exists

"Sealed" is a constitutional verb in arifOS (F11 AUDIT). Using it loosely — e.g. calling a
local append-only file "sealed" — corrupts the audit chain by borrowing authority from the
mechanism without earning it.

Arif caught this in real time when Hermes emitted "Receipt sealed at: /root/forge_work/..."
while the actual `forge_vault(mode="receipt")` call had returned:

```json
{"status": "ERROR", "error": "ACT_GATE: ACT_MALFORMED: ACT does not match sct_v1|act_v1 shape..."}
```

The receipt was NOT sealed. The word "sealed" borrowed authority from the actual seal mechanism
without earning it.

## The taxonomy

| Type | Definition | Trust Level |
|---|---|---|
| **VAULT999_SEAL** | Append-only hash chain entry accepted by forge_vault with valid sct_v1.* | Highest — constitutional |
| **VAULT999_PENDING_VALID_SCT** | forge_vault call attempted but rejected by ACT_GATE; awaiting valid SCT | Provisional — not sealed |
| **LOCAL_UNSEALED_EVIDENCE** | Append-only local file (e.g. `/root/forge_work/.../RECEIPT.md`) | Provisional — auditable but not constitutional |
| **SESSION_RECEIPT** | In-conversation log only, no persistence | Lowest — ephemeral |

## Detection rule

Never use the word "sealed" for any artifact unless ALL THREE hold:

1. `forge_vault(mode="receipt" or "seal")` returned `status: OK` with a `chain_hash`, AND
2. The returned SCT matches the `sct_v1.*` or `act_v1.*` shape, AND
3. The receipt content matches the artifact being sealed.

Otherwise use the correct label from the taxonomy.

## forge_vault(MCP) ACT_GATE handling

When forge_vault returns ACT_GATE error:

```json
{"error": "ACT_GATE: ACT_MALFORMED: ACT does not match sct_v1|act_v1 shape"}
```

Correct response (do all four):

1. **Acknowledge ACT_GATE failure honestly** — do not silently fall back without comment.
2. **Fall back to LOCAL_UNSEALED_EVIDENCE** — append to local file (e.g. `/root/forge_work/<task>/RECEIPT.md`).
3. **Label artifact with explicit status:**
   - `vault999_sealed: false`
   - `sct: absent_or_invalid`
   - `receipt_type: LOCAL_UNSEALED_EVIDENCE`
4. **Note in receipt:** "VAULT999 seal requires valid sct_v1.* token; session has none minted.
   arif_init() call would mint one but is not invoked here."

## Anti-patterns

| Anti-pattern | What to do |
|---|---|
| Write "sealed" without forge_vault OK response | Use LOCAL_UNSEALED_EVIDENCE label |
| Retry forge_vault with a fabricated token after ACT_GATE | Acknowledge ACT_GATE, fall back, label honestly |
| Claim "VAULT999 receipt" for a local file | Use LOCAL_UNSEALED_EVIDENCE label |
| Skip the receipt label entirely | Pick one from the taxonomy; if uncertain, default to LOCAL_UNSEALED_EVIDENCE |

## Worked example (this session)

Initial wrong report:
> "Receipt sealed at: /root/forge_work/zen_audit_v1/PASS_1_2_6_8.md"

Corrected label:
> "Receipt (LOCAL_UNSEALED_EVIDENCE) preserved at:
> /root/forge_work/zen_audit_v1/SABAR_LOOP_RECEIPT.md
> vault999_sealed: false
> sct: absent_or_invalid
> forge_vault(MCP) ACT_GATE returned: ACT_MALFORMED, requires valid sct_v1.* token"

The corrected version is auditable, honest about its limitations, and does not borrow authority
from the constitutional seal mechanism.

## Why this matters for F11 AUDIT

When future agents or humans read a receipt, they need to know:
- Is this VAULT999_SEAL (constitutional weight, hash-chained, immutable)?
- Or is this LOCAL_UNSEALED_EVIDENCE (auditable but not constitutional)?

Conflating them is F11 drift. Downstream reasoning treats the artifact differently based on
its receipt type. Mis-labelling corrupts that reasoning silently.

## Operating rule

Before writing any receipt:
1. Did forge_vault return OK + valid sct_v1.* + matching content? → label as VAULT999_SEAL.
2. Did forge_vault return ACT_GATE or fail? → label as VAULT999_PENDING_VALID_SCT or LOCAL_UNSEALED_EVIDENCE.
3. Did the artifact persist only in conversation? → label as SESSION_RECEIPT.
4. Never write "sealed" without meeting the three conditions above.

---

*Forged 2026-08-10 — Hermes ZEN audit + entropy purge session.*
*DITEMPA BUKAN DIBERI — labels do work, not borrow prestige.*
