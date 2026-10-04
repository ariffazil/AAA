# Output Attestation System — 2026-08-09

## Problem

Agent generates outputs (PDFs, emails) with fabricated cryptographic signoffs — hash values that were never computed, VAULT999 seals that never happened.

## Solution: Three-layer attestation

### Layer 1: Compute (T0 — autonomous)

`/root/HERMES/scripts/output-attest.py` — computes real SHA-256 of any file, records to ledger.

```bash
python3 /root/HERMES/scripts/output-attest.py <file.pdf> --label "description" --agent "hermes"
# Returns: sha256, file_size, timestamp, ledger_recorded: true
```

### Layer 2: Enforce (cron auto-attest)

`/root/.hermes/scripts/check-unattested-outputs.sh` — scans for PDFs without attestation, auto-attests.

```bash
# Runs every 2h via cron job 4f47cde23bb8
# Finds unattested PDFs, computes SHA-256, records to ledger
```

### Layer 3: Verify (audit)

`/root/HERMES/scripts/output-verify.py` — checks file hash against claimed hash and ledger.

```bash
python3 /root/HERMES/scripts/output-verify.py <file.pdf> <claimed_hash>
# Returns: VERIFIED or FABRICATED
```

## Ledger

`/root/HERMES/attestation-ledger.jsonl` — append-only JSONL. Each entry:
```json
{
  "type": "output_attestation",
  "file_path": "/absolute/path",
  "sha256": "real_hash",
  "timestamp": "ISO8601",
  "agent_id": "hermes",
  "verbatim": true
}
```

## Key principle

The hash is COMPUTED from actual file content, not generated as text. The attestation lives in the LEDGER, not embedded in the PDF. A PDF with a hash inside it is not attested — the ledger entry is the attestation.

## Pitfall

The `post_tool_call` shell hook (`output-attest-hook.py`) is ready but requires config.yaml edit to register. Currently enforced only by cron (every 2h). For immediate attestation, call `output-attest.py` explicitly after generating any output.
