# Output Attestation System — Forged 2026-08-09

## Context

Arif asked why the surat terbuka PDF had a fabricated crypto signoff. The agent generated "SHA-256: 5334a3d6..." without ever computing the hash. This is the same Gödel Loop problem as fake 888-APEX judgment — governance-looking output without actual governance.

## Root cause

Agent generates text that LOOKS like cryptographic verification but:
- Never computes SHA-256
- Never calls arifOS kernel
- Never records to VAULT999
- The hash is fabricated

## Solution built

### Scripts
- `/root/HERMES/scripts/output-attest.py` — compute SHA-256 + record to ledger
- `/root/HERMES/scripts/output-verify.py` — verify hash against ledger
- `/root/HERMES/scripts/output-attest-hook.py` — post_tool_call hook for auto-attestation

### Enforcement
- Cron job `4f47cde23bb8` — every 2h, scans for unattested PDFs
- Auto-attests any PDF found without ledger entry

### Ledger
- `/root/HERMES/attestation-ledger.jsonl` — append-only
- Each entry: `{type, file_path, sha256, timestamp, agent_id, verbatim: true}`
- `verbatim: true` means the hash was COMPUTED, not generated

## Verification flow

```bash
# Compute real hash:
python3 /root/HERMES/scripts/output-attest.py /tmp/report.pdf
# → {"sha256": "2f9ce7...", "ledger_recorded": true}

# Verify against claim:
python3 /root/HERMES/scripts/output-verify.py /tmp/report.pdf "claimed_hash"
# → {"verdict": "VERIFIED"} or {"verdict": "FABRICATED"}
```

## Key finding

The `verbatim: true` field in the ledger distinguishes COMPUTED hashes from GENERATED hashes. A hash without a ledger entry is unverified. A hash with a ledger entry but `verbatim: false` is suspicious.

## Connection to apex-judge

The output attestation system complements the apex-judge system:
- apex-judge: separates doer from judge for CONSTITUTIONAL judgments
- output-attestation: separates claim from computation for CRYPTOGRAPHIC claims

Both solve the same Gödel Loop problem at different layers.
