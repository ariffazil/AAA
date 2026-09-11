# VAULT999 Writer Discipline — Kernel Owns the Ledger

> **Status:** F13_DIRECTED_FIX (2026-09-11, "betulkan writer plaintext tu")
> **Origin:** 888-DOCKET-959 §F13 VERDICT — 12 plaintext marker lines (1338–1349) violated SEALED_EVENTS.jsonl's JSONL invariant, written by live agent sessions 2026-09-06..11.
> **Applies to:** ALL agents in arifOS federation. Every VAULT999 write. No exception.

## The Rule

```text
SEALED_EVENTS.jsonl is KERNEL-OWNED.
Agents never append to it — not JSON, not plaintext, not "just a marker".
```

Session markers (SEAL::, SESSION_CLOSE, ratification notes) go through the canonical lane:

```bash
python3 /root/scripts/federation_ritual.py marker \
  --label LAYER0-ECONOMICS-WIRED \
  --text "one-line summary" \
  --actor fi008_kimi_code
```

This appends a **hash-chained JSON entry** to `/root/.arifos/ritual.log` — tamper-evident, greppable, and outside the kernel's seal ledger.

## Why

- Broken record = symptom. Broken writer = cause. Hand-rolled `echo "SEAL::..." >> SEALED_EVENTS.jsonl` corrupts the invariant every validator and sweep relies on (12 lines → whole-tail unparseable, `apex_attention` flags, classification noise).
- The sanctioned lane already existed (ritual.log, hash-chained since 2026-09); the fix connects arrows to it — no new component.
- Layer discipline: kernel writes seal events; agents write markers to their own chain; humans ratify in chat. Actor ≠ Authorizer ≠ Ledger.

## Enforcement shape

- Validators treat any non-`{` line in `SEALED_EVENTS.jsonl` as `plaintext_marker_line` (defect class, `apex_attention`) — see the 2026-09-11 sweep classifier.
- Repeat offenses after this fragment's render = F11 AUDITABILITY violation, not an accident.

DITEMPA BUKAN DIBERI ⚒️
