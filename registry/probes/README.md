# probes/ — append-only runtime observations

- Every file is one immutable receipt. NEVER overwrite or delete an old probe — append a new file.
- `receipt_hash` = sha256 over the canonical JSON of the record (sorted keys, compact separators) EXCLUDING the `receipt_hash` field itself. Any observer can recompute it.
- Migrated records (`evidence_status: migrated_from_sot`) carry content-hash receipts over THIS record; their `evidence_refs` point at the SOT patch notes that witness the observation.
- `expected_marker_present` participates in PASS only when `expected_marker` is declared; core validity (non_empty / schema_valid / finish_state_valid) is always binding — see policies/probe-verdict-grammar-v1.
- Verdict grammar: PASS / WARN (exact known_remap only) / HOLD (undocumented mismatch, unknown resolution on floating alias) / FAIL (empty-or-invalid success; non-200).
