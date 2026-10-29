# Probe Contract

## The mandatory four fields

Every probe receipt carries, at minimum:

```
requested_model   # what we asked for
resolved_model    # what answered (response model / system_fingerprint), null if not echoed
http_status       # transport verdict only
output_validity:  # non_empty / schema_valid / finish_state_valid / expected_marker_present
```

## Receipts are append-only

One file per probe under `probes/`, named `probe-YYYYMMDDtHHMMSSz-route-model.yaml`.
Never overwrite, never delete. `receipt_hash` = sha256 over the canonical JSON of the
record (sorted keys, compact separators) EXCLUDING the hash field — any observer can
recompute it; tests do (`test_probe_receipt_hash_is_verifiable`).

Migrated records (`evidence_status: migrated_from_sot`) hash THIS record; their
`evidence_refs` point at the SOT patch notes that witness the observation.

## Verdict grammar (policies/probe-verdict-grammar-v1)

| Verdict | Exactly when |
|---|---|
| PASS | 200 + core validity (non_empty, schema_valid, finish_state_valid) + resolved == requested (+ marker, when declared) |
| WARN | exact match to a `known_remaps` entry on that route — nothing else |
| HOLD | any undocumented resolution mismatch; unresolved identity on a floating alias |
| FAIL | non-200; or 200 with empty/invalid output — **empty success is FAIL, never PASS** |

`expected_marker_present` participates in PASS/FAIL only when `expected_marker` is
declared for the probe; the three core validity dimensions are always binding.

## Known traps this grammar exists for

- **Empty success** (SOT patch 2026-10-18): DeepSeek thinking-ON with a small
  max_tokens returns HTTP 200 with EMPTY content and `finish_reason=length` → FAIL.
- **200 ≠ identity** (INC-001): glm-5.2 request returns 200 + `model: glm-5.3` → WARN
  only because the exact remap is witnessed; any other mismatch → HOLD.
- **Catalog presence ≠ resolution** (INC-002): `deepseek-v3.2` sits in the token-plan
  catalog; its resolution is UNKNOWN → HOLD until a live probe classifies it.
- **/models 200** proves AUTH_VALID / CATALOG_REACHABLE at most — never inference
  ALIVE (INC-005: a whole seat family sat "quota_exhausted" for days on a stale read).

## Regression suite

`tests/registry_supply_chain/test_supply_chain.py` encodes cases A–E from the
sovereign brief; the pure function `verdict_for()` in `registry/update.py` is the
single implementation both the prober and the tests use.
