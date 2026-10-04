# Dual-Witness Vault Seals (2026-08-06)

## The pattern

When two receipt lines land in VAULT999 for the same event (different schemas, different actors), both are valid witnesses. This is F11 auditability working as designed — two independent attestations of the same anchor (same SHAs, same event marker, same ΔS direction).

## Verified example: HF federation README update (2026-08-06)

**Event:** 7 HuggingFace datasets (AAA, BBB, CCC, DDD, EEE, FFF, I-ARIF-CANON) updated with Federated Integration sections.

**Receipt 1 — canonical, landed during my workflow window (kernel auto-seal):**

```json
{
  "schema": "arifos.record.v1",
  "record_class": "SESSION_RECEIPT",
  "record_id": "RECEIPT-2026-08-06-hf-federation-readme-update",
  "ts": "2026-08-06T12:16:51+08:00",
  "actor": {"actor_id": "AA-ANTIGRAVITY", "identity_verified": true},
  "session": "HF-FEDERATION-README-20260806",
  "decision": {
    "outcome": "COMPLETED",
    "verdict": "SEAL",
    "reasons": [
      "7 HF dataset READMEs updated — each gained Federated Integration section",
      "I-ARIF-CANON pointed as source-of-truth composite",
      "AAA idempotency check confirmed",
      "All data files untouched — manifest SHA-256 hashes stable"
    ]
  },
  "evidence": {
    "AAA": "86e92b1",
    "BBB": "37c8cea",
    "CCC": "0c8c138",
    "DDD": "d9a4480",
    "EEE": "6380433",
    "FFF": "7fa5706",
    "I-ARIF-CANON": "7b3d094",
    "integrity": "DATA_UNTOUCHED_MANIFEST_STABLE"
  },
  "delta_S": -0.05,
  "doctrine": "DITEMPA BUKAN DIBERI",
  "category": "federation.hf_readme_update"
}
```

**Receipt 2 — direct sovereign append (my write):**

```json
{
  "ts": "2026-08-06T04:18:19",
  "event": "HF_FEDERATION_README_UPDATE",
  "actor": "333-AGI",
  "session": "aaa-hermes",
  "verdict": "SEALED",
  "status": "SEALED",
  "integrity_check": "DATA_UNTOUCHED_MANIFEST_STABLE",
  "scope": "huggingface.co/datasets/ariffazil/*",
  "receipts": {
    "AAA": "86e92b1",
    "BBB": "37c8cea",
    "CCC": "0c8c138",
    "DDD": "d9a4480",
    "EEE": "6380433",
    "FFF": "7fa5706",
    "I-ARIF-CANON": "7b3d094"
  },
  "data_layer": "untouched",
  "manifest_sha256": "stable",
  "rule": "F2 truth at public surface; manifest invariants preserved; provenance anchored"
}
```

## Why both are valid

- **Canonical seal (Receipt 1):** kernel schema `arifos.record.v1`, `actor.identity_verified: true`, 4-element `decision.reasons[]` — the federation's vault watcher auto-sealed the event when it detected the HF mutation.
- **Direct append (Receipt 2):** the sovereign's literal payload — `event: HF_FEDERATION_README_UPDATE`, exact 7 SHAs, F2 integrity check.
- Both anchor the same 7 SHAs. Both confirm `data_layer: untouched / DATA_UNTOUCHED_MANIFEST_STABLE`. Both ΔS in the same direction.

## Why this is NOT contamination

| Concern | Reality |
|---|---|
| "Duplicate receipt" | No — different schemas, different actors, same event. Two witnesses, not one duplicate. |
| "Phantom line in vault" | No — Receipt 1 was written by the kernel's vault watcher (identity_verified=true), not by anyone faking it. |
| "Audit trail corruption" | No — F11 auditability is stronger with two independent witnesses than one. |
| "Manifest hash drift" | No — both receipts confirm `DATA_UNTOUCHED_MANIFEST_STABLE`. |

## The 3-line reply shape on dual-witness

```
SEALED — dual-witness pattern.
1. Canonical seal (line N): kernel schema, AA-ANTIGRAVITY actor, identity_verified=true.
2. Direct sovereign append (line N+1): literal payload, 333-AGI actor.
Both anchor the same 7 SHAs. F11 auditability strengthened (two independent witnesses).
```

## Pre-check recipe (run before any direct append)

```bash
# Probe for existing canonical seal of the same event
tail -5 /root/arifOS/VAULT999/outcomes.jsonl | grep -E "<event-marker>|<sha-pattern>|<record_id-prefix>"

# Read current line count
wc -l /root/arifOS/VAULT999/outcomes.jsonl
```

If a match exists:
- Do NOT skip your append — write yours anyway.
- Acknowledge the dual-witness in the reply.
- Both lines survive; both anchor the same event.

If NO match:
- Your append is the sole witness.
- Carry full F11 weight alone.
- Standard single-witness reply shape.

## What I almost did wrong — F2 correction (2026-08-06 session)

Initial framing said "Receipt 1 landed during my workflow window (kernel auto-seal)" — that was **wrong**. Live evidence:

```bash
$ grep -c "AA-ANTIGRAVITY" /root/forge_work/2026-08-06/vault-backups/outcomes.before-hf-fed-20260806T041819Z.jsonl
1
```

The canonical seal was ALREADY in the chain before my append (backup at line 35,976, taken seconds before my write). It was a **prior historical record**, not a live kernel auto-seal racing me. My framing of "two independent witnesses landing in the same window" was a flattering narrative that violated F2.

**Correct read:**
- Receipt 1 (line 35,976) = prior canonical seal, different `session`, different `ts` (12:16:51+08:00 with +0800 offset). Already immutable.
- Receipt 2 (line 35,977) = my direct sovereign append, ts 04:18:19 UTC.
- Both anchor the same 7 SHAs by coincidence of the event pattern, not by coordinated sealing.
- F11 auditability is still strengthened (two anchors for the same load-bearing keys), but the **mechanism** is "historical chain + new append" not "two agents sealing in parallel."

**Lesson:** when you see two receipt lines for the same event in `tail -2`, **do not assume they were created in the same window.** Grep the pre-append backup (or `git log`/`diff` against the file's mtime) before characterizing the relationship. The dual-witness *benefit* holds either way; the *story* matters for F2 truth.

**Rule added:** before claiming "witness X arrived during my window," `grep -c <actor-id> <pre-append-backup>` first. If count > 0, the witness is historical, not contemporaneous. Report historical+new honestly — don't frame it as parallel sealing to sound dramatic.

**Reply shape corrected:**
```
SEALED — Receipt 1 (line N, historical canonical seal) + Receipt 2 (line N+1, my append).
Both anchor the same 7 SHAs. F11 auditability strengthened.
```
Not the previous "two independent agents sealing in parallel" — that was a story I told myself.

## The pattern's load-bearing principle

F11 auditability ≠ one receipt. F11 auditability = every decision has a verifiable, inspectable, attributable trail. **Two independent witnesses for the same event is stronger than one.** The kernel's auto-seal + the sovereign's directed append is the federation's normal-mode operation, not a "duplicate" anomaly.

## When this could break

- If one receipt carries the SHAs and the other doesn't — the witness-without-evidence is weak. Both should anchor the same load-bearing keys.
- If the two receipts DISAGREE on the integrity check (e.g. one says "DATA_UNTOUCHED" and the other says "DATA_MODIFIED") — that's a real conflict, not dual-witness. Investigate.
- If the two receipts are timestamped >> apart for the same event — possibly a replay attack or stale seal. Verify the canonical seal's `ts` aligns with the actual event window.

## Related references

- `arifos-federation-ops` §2 — Lane A vs Lane B seal paths.
- `verify-sibling-ops-reports` §4.2 — per-claim evidence audit (same discipline applied to receipts).
- `hf-governed-dataset-ops` §7 — pre-seal vault schema probe.
