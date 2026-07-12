---
name: vault999-reader
description: >
  Bridge to arifOS VAULT999 append-only ledger. Read seal entries,
  verify chain integrity, list recent vault operations. USE WHEN:
  "check vault", "vault999 status", "read seals", "ledger integrity",
  "arifOS vault".
---

# Vault999 Reader

**Reads and verifies the arifOS constitutional ledger without writing.**

## What It Checks

- VAULT999 directory and file existence
- vault999.jsonl entry count and JSON validity
- arifOS MCP `arif_seal` and `arif_judge` tool availability
- Chain integrity (all entries valid JSON objects)
