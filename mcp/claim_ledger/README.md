# claim-ledger-mcp

**Append-only claim ledger for arifOS federation intelligence briefs.**
Closes the gap where the federation hashed *artifacts* but never *claims*: today a
forged brief carries a SHA256 of its PDF, but nothing binds the sentence
"Bank Muamalat's retail funding is 12%" to the page it came from, the quote that
backs it, the artifact it lives in, or a verification record.

**Authority: WITNESS_ONLY.** This organ records and verifies claims. It does not
judge them, does not seal VAULT999, and never writes outside its own ledger dir.

---

## Layout

| Path | What |
|---|---|
| `/root/AAA/mcp/claim_ledger/server.py` | FastMCP server (10 tools) |
| `/root/AAA/mcp/claim_ledger/client.py` | Thin async client + CLI |
| `/root/AAA/mcp/claim_ledger/smoke_test.py` | Real MCP-client smoke test (55 checks) |
| `/root/AAA/mcp/claim_ledger/smoke_test_output.txt` | Last full smoke-test output |
| `/root/AAA/claim_ledger/claims.db` | The ledger (SQLite, WAL) |
| `/root/AAA/claim_ledger/evidence_pass1_claims.db` | First-pass ledger copy, kept as evidence |

Interpreter is mandated: `/opt/arifos/venv/bin/python` (fastmcp 3.4.6 + mcp SDK).
No new dependencies — stdlib `sqlite3`.

## Run

```bash
# start
/opt/arifos/venv/bin/python /root/AAA/mcp/claim_ledger/server.py    # 127.0.0.1:8791

# smoke test (resets the ledger, then proves every tool over real MCP)
/opt/arifos/venv/bin/python /root/AAA/mcp/claim_ledger/smoke_test.py
#   add --append to run against the existing ledger instead of resetting

# CLI
/opt/arifos/venv/bin/python /root/AAA/mcp/claim_ledger/client.py stats
/opt/arifos/venv/bin/python /root/AAA/mcp/claim_ledger/client.py verify
/opt/arifos/venv/bin/python /root/AAA/mcp/claim_ledger/client.py trace <claim_id>
```

Endpoint: `http://127.0.0.1:8791/mcp` (streamable-http, loopback only).
No auth — LOCALHOST_IS_PASSWORD doctrine, UFW blocks the outside.

## Tools

| Tool | Does |
|---|---|
| `claim_ledger_init` | Create schema, report tables/counts/chain head, confirm 8 append-only triggers |
| `claim_artifact_register` | Hash a file on disk, match against a declared SHA256, append artifact |
| `claim_record` | Record a claim: text → type → quote → locator → source_ref → artifact + hash snapshot |
| `claim_verify` | Append a verification (CONFIRMED/PARTIAL/REFUTED/UNVERIFIED), re-hashing the artifact live |
| `claim_get` | One claim + artifact + full verification history + `superseded_by` |
| `claim_trace` | End-to-end provenance: chain position, quote, locator, recorded vs live hash, `traceable` + `trace_gaps` |
| `claim_list` | Filter by `brief_id` / `claim_type`, per-row verdict + `unverified` count |
| `claim_ledger_stats` | Census by type / brief / verdict, verified vs unverified |
| `claim_export_brief` | Auditable bundle of every claim for a brief + `bundle_sha256` |
| `claim_ledger_verify_chain` | Recompute chain links, rebuild every record's payload vs the chained payload, re-hash artifacts on disk. `db_path=` audits a copy |

## Invariants

1. **Append-only at the schema level.** Eight `BEFORE UPDATE/DELETE` triggers
   `RAISE(ABORT, 'APPEND_ONLY: ...')` on `claims`, `verifications`, `artifacts`,
   `ledger_chain`. Corrections are appended with `supersedes_claim_id` set.
2. **Hash-chained writes.** Every write also appends a `ledger_chain` row with
   `seq`, `prev_hash` and `row_hash = sha256(prev_hash|event_type|canonical_payload)`.
3. **Payload cross-check.** `claim_ledger_verify_chain` rebuilds each record's
   canonical payload from the record row and compares it to the chained payload —
   so an edit that bypassed the triggers is caught, not just a broken link.
4. **Live artifact re-hash.** Verification and chain checks re-read the artifact
   from disk. "Verified" means the source still exists and matches, not that
   someone typed a verdict.

## Claim types

Federation vocabulary as used inside the forged briefs:
`OBS` observed · `DER` derived · `INT` interpretation · `SPEC` speculative ·
`VOID` could-not-verify · `FIQH` referred to scholars.

## Attaching a brief to the ledger

```python
from client import LedgerClient

async with LedgerClient() as L:
    await L.register_artifact(
        path="/root/AAA/forge_work/<brief>/Brief.pdf",
        sha256="<declared hash>", title="...", pages=20)
    await L.record(
        brief_id="<brief-id>", claim_text="...", claim_type="OBS",
        source_quote="<verbatim quote from the PDF>",
        locator="p.2 Executive Read, finding 5",
        artifact_id="art-<hash[:16]>", source_ref="<citation>")
    print(await L.export_brief("<brief-id>"))   # bundle + bundle_sha256
```

## What this does NOT do

- Does not read or parse the PDF — the operator supplies the quote and locator.
  It proves the claim is *bound* and *traceable*, not that the quote is faithful
  to the page. A quote-fidelity checker is the natural next tool.
- Does not judge claim truth; verdicts are human/agent attestations, recorded.
- Does not write VAULT999 and does not federate (no A2A surface yet).

DITEMPA BUKAN DIBERI — Forged, Not Given.
