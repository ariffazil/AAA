---
name: output-attestation
description: "Cryptographic attestation for real-world outputs (PDFs, emails, documents). Computes real SHA-256 hashes, records to ledger, provides verification. Solves the 'fake crypto signoff' problem where agents generate text that LOOKS like hashes but never computed them. USE WHEN: generating PDFs, emails, or any output that goes to real humans; verifying claimed hashes; auditing output authenticity."
tags: [attestation, cryptography, sha256, ledger, verification, F2, F11]
version: 1.0.0
author: Hermes Agent
related_skills: [forge-vault-seal-receipt, audit-and-validate-deliverables]
---

# Output Attestation — Real Cryptographic Verification for Real-World Outputs

## Problem This Solves

Agents generate output (PDFs, emails) and claim cryptographic verification:
- "SHA-256: abc123..." — but never computed it
- "VAULT999 SEALED" — but never called arif_seal
- "arifOS Kernel verified" — but never touched the kernel

This is the Gödel Loop at the output layer: agent self-certifies its own output.

## Solution Architecture

```
OUTPUT GENERATED
       ↓
post_tool_call HOOK (auto-detect)
       ↓
output-attest.py (compute SHA-256)
       ↓
attestation-ledger.jsonl (record)
       ↓
OUTPUT DELIVERY (with real hash)
```

Three layers:
1. **Compute** — `output-attest.py` (T0, autonomous)
2. **Enforce** — `post_tool_call` hook + cron auto-attest
3. **Verify** — `output-verify.py` (check hash against ledger)

## Files

| File | Path | Purpose |
|---|---|---|
| Attest script | `/root/HERMES/scripts/output-attest.py` | Compute SHA-256, record to ledger |
| Verify script | `/root/HERMES/scripts/output-verify.py` | Check hash against ledger |
| Hook script | `/root/HERMES/scripts/output-attest-hook.py` | Auto-attest on write_file/terminal |
| Cron script | `/root/.hermes/scripts/check-unattested-outputs.sh` | Scan for unattested files |
| Ledger | `/root/HERMES/attestation-ledger.jsonl` | Append-only hash records |

## Usage

### Attest a file
```bash
python3 /root/HERMES/scripts/output-attest.py <file.pdf> --label "description" --agent "hermes"
```
Returns: `{"sha256": "...", "ledger_recorded": true, "verbatim": true}`

### Verify a file
```bash
python3 /root/HERMES/scripts/output-verify.py <file.pdf> <claimed_hash>
```
Returns: `{"verdict": "VERIFIED"}` or `{"verdict": "FABRICATED"}`

### Auto-attest (cron)
Runs every 2h, scans for PDFs without attestation, auto-attests them.
Cron job: `4f47cde23bb8`

## The Rule

**Never generate a hash without computing it.** The hash in the output must come from `output-attest.py`, not from text generation. The ledger entry IS the attestation — not text embedded in the PDF.

## What This Does NOT Do

- Does NOT seal to VAULT999 (that requires SOVEREIGN via `forge_vault`)
- Does NOT judge constitutional compliance (that requires `arif_judge`)
- Does NOT replace the apex-judge system (that's for decision attestation)

This is FILE attestation only — proving a file hasn't been tampered with.

## Integration

### For PDF generation
After generating any PDF, call:
```python
from hermes_tools import terminal
terminal("python3 /root/HERMES/scripts/output-attest.py /path/to/file.pdf --label 'surat-v3'")
```

### For email sending
Before sending, attest the attachment:
```python
terminal("python3 /root/HERMES/scripts/output-attest.py /path/to/attachment.pdf --label 'email-attachment'")
```

## Pitfalls

- **Hash chicken-and-egg**: You can't embed the hash in the file before computing it. The attestation lives in the LEDGER, not in the file itself.
- **Binary files**: `output-attest.py` works on any file (PDF, PNG, MP4, etc.)
- **Text content**: For text, use `--text` flag or pipe content
- **Ledger is append-only**: Never delete entries. New entries only.
