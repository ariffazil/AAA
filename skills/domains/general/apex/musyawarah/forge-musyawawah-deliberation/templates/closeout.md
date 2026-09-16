# CLOSEOUT — musyawawah-e2e-<YYYY-MM-DD>

## Directive received

<quote the directive that triggered this run, e.g., "test musyawawah", "let me think with another agent">

## Time window

<start MYT> — <end MYT>

## Files produced (F11 AUDIT)

<list all files with sizes>

## What was sealed (Lane A vs Lane B)

**Lane A (constitutional, F13 territory):**
- <list each Lane A seal or write "BLOCKED — <gate>">

**Lane B (autonomous, no kernel needed):**
- <list each Lane B seal with seq, hash, timestamp>

## What remains F13-gated (decision blocks)

1. <specific decision awaiting F13>
2. <specific decision awaiting F13>
3. <specific decision awaiting F13>
(NOT "further work" — name the decisions.)

## Constitutional compliance (F1-F13)

| Floor | Status | Evidence |
|-------|--------|----------|
| F1 AMANAH | ✅/⚠️/❌ | <evidence> |
| F2 TRUTH | ✅/⚠️/❌ | <evidence> |
| F3 TRI-WITNESS | ✅/⚠️/❌ | <evidence — usually ⚠️ since SOVEREIGN is deferred> |
| F4 CLARITY | ✅/⚠️/❌ | <evidence> |
| F5 PEACE² | ✅/⚠️/❌ | <evidence> |
| F6 EMPATHY ⇄ MARUAH | ✅/⚠️/❌ | <evidence> |
| F7 HUMILITY | ✅/⚠️/❌ | <evidence> |
| F8 GENIUS | N/A | <usually not a candidate action> |
| F9 ANTIHANTU | ✅/⚠️/❌ | <evidence — most important for honest F13 surfaces> |
| F10 ONTOLOGY | ✅/⚠️/❌ | <evidence> |
| F11 AUDITABILITY | ✅/⚠️/❌ | <evidence> |
| F12 RESILIENCE | ✅/⚠️/❌ | <evidence> |
| F13 SOVEREIGN | ✅/⚠️/❌ | <evidence — must be ✅ if no F13 substitution happened> |

## Chain integrity

- Lane B chain: <start seq> → <end seq>, all hashes linked ✅/❌
- Mirror in outcomes.jsonl: ✅/❌
- Pre-existing breaks: <none / describe>

## ΔS for the entire run

Net: <value> (<one-line justification>)

## Reversibility

Single command restores pre-test state:

```bash
rm -rf /root/forge_work/musyawawah-e2e-<YYYY-MM-DD>/
```

Lane B seals in VAULT999 are append-only by design and remain as audit
trail of what was done. They cannot be unsealed, even after the proposal
directory is removed.

## "Seal semua" — what was actually sealed vs what was not

✅ SEALED: <list>
❌ NOT SEALED: <list — be specific about gates>

This closeout makes the boundary explicit.

---

DITEMPA BUKAN DIBERI — Executed to the boundary. Honest about where the
boundary is. F13 to ratify what's left.

— <signing agent>
<timestamp MYT>