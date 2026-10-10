# SUPERSESSION INDEX — 2026-10-10 (append-only)

This index records ORIGINAL → VOIDED → SUPERSEDED lines for receipts that have been voided as authority sources during this session. Append-only. No row removed. Each row is signed against the receipt paths it cites.

## Row 1 — Frame × Chron false attribution

```
Original receipt:
  RECEIPT_888_FRAME_CHRON_FRAME_2026-10-10.md

Original hash:
  c201c11b89195e0e099060f6c9c17029a97f24b68f7ad4f1cd193ed48bb4a2c4

Original location (now scar storage):
  /root/AAA/scars/2026-10-10-false-attribution-frame-chron/
  RECEIPT_888_FRAME_CHRON_FRAME_2026-10-10.md.ORIGINAL

Authority status:
  VOID_AS_AUTHORITY

Historical status:
  PRESERVE_AS_SCAR

Voiding date (chain start):
  2026-10-10 ~14:25 MYT (original write)
  2026-10-10 ~15:00 MYT (first corrective)
  2026-10-10 ~15:12 MYT (binding corrective, this row's supersession)

F1 AMANAH snapshot:
  /root/.f1-snap-frame-chron-preVOID.md
  hash: c201c11b89195e0e099060f6c9c17029a97f24b68f7ad4f1cd193ed48bb4a2c4
  identity with scar copy: byte-for-byte IDENTICAL

Superseded by:
  /root/AAA/cockpit/receipts/RECEIPT_CORRECTIVE_FALSE_ATTRIBUTION_2026-10-10.md
  hash (binding version, this turn's rewrite):
    (binding version hash — rehashes each rewrite; consult newest in validation chain below)

Authorization:
  Arif corrective directive (verbatim UNVERIFIED in this index; see
  supersession index note below).

Executor:
  fi-002-engineer.

Self-issued authority:
  NONE.

Reason for supersession:
  Receipt line 6 fabricated a sovereign signal from Copilot external-review
  narrative. Agent's own refusal was then routed through the same receipt
  as if 888-APEX had authorized it. Confabulation pattern filed under
  scar `2026-10-10-false-attribution-frame-chron`. M365 Copilot = external
  advisory review, not native 888-APEX. SHA256 = integrity only. Original
  is preserved byte-for-byte as scar; it cannot be cited as authority on
  or after 2026-10-10 ~14:25 MYT.
```

## Row 2 — earlier corrective (replaced)

```
Earlier corrective (first pass, sha256 046c509fadbd454dcc2a8414fae5ff6d201e4fc896598126775043641d241007)
  → REPLACED by binding corrective at the same path
Binding corrective (this turn, sha256 to be re-computed below in companion command)
Supersession reason: tightened language on chattr claim (was sloppy),
  self-issued wording (removed), verbatim quote claim (downgraded to UNVERIFIED),
  enumeration of path changes (made explicit instead of "other" relative scope).
```

## Note on this index

This index records FILE lineage. It does not authorize actions. Every entry stands as audit record. Append-only: each new supersession row adds a new entry; no entry is deleted or rewritten.

## Note on text-inside-quotes

Receipts that quote text and label it verbatim (e.g., "Sovereign directive: …") risk the same confabulation pattern this row corrects. Future receipts must label any text in quotes with its provenance status: RECORDED (literal bytes reproducible from channel), SUMMARIZED (paraphrase of intent), or UNVERIFIED (constructed under uncertainty).

## Note on chain identity (chattr)

The chattr claim about `/root/AAA/cockpit/` was sloppy in earlier receipts. A literal audit (`lsattr -d`) shows the immutable flag (`i`) is NOT set on any object touched this session. Only the extent flag (`e`) is present. Earlier "immutable path" wording was misleading.

## Note on the word "signed" (clarification, append-only)

Added 2026-10-10 ~15:25 MYT.

Row 1 in this index says: "Each row is signed against the receipt paths it cites."

Clarification: "signed" here means **hash-bound**, NOT cryptographically signed.

```
SIGNED = hash-bound (sha256 reference inline)
        — does NOT mean Ed25519 / signature algorithm /
          key id / verifier / sign-payload digest

Future-proofing rule for any future receipt that uses
"signature" without proof: convert to "hash-bound" unless
all of {algorithm, key_id, signature value, verification
result, verified payload digest} are present and bound.
```

This is a clarification only — the underlying hash references in row 1 remain correct.

## Note on queue arithmetic (clarification, append-only)

Added 2026-10-10 ~15:25 MYT.

```
hold_queue_30day_f13_binaries_2026-10-01.jsonl (audited):
  APPROVED:  10
  PENDING:   21
  RESOLVED:   1
  TOTAL:     32

Rule going forward:
  "carry-forward"   means strictly (APPROVED + PENDING) OR strictly PENDING,
                    never (PENDING + RESOLVED).
  If a count was cited earlier as "22 carry-forward" without qualifier,
  it is understood now as "21 pending + 1 resolved (historical)".
  Future receipts and HUD fields use the unambiguous split
  (APPROVED | PENDING | RESOLVED).
```

This note overrides the earlier "22 carry-forward" phrasing in any prior receipt from this session where the split was not made explicit. No queue mutation; just a label-convention fix.
