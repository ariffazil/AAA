LEDGER: /root/arifOS/VAULT999/SEALED_EVENTS.jsonl
physical records=1345  parse_failures=1

G1  json_parse_error                1   [4]
G2  schema_no_chain_fields          3   [3, 5, 1346]
G3  orphan_footer_no_chain          1   L1346
G4a genesis_subchain_starts       953
G4b prev_hash_empty_string          1
G4c consecutive_dup_prev            1   ['L588/L589']
      -> L588/L589: payload_identical=True chain_identical=True
G5  placeholder_records          1142   (84.9% of 1345)

CORRECTIONS TO THE 2026-10-06 CLASSIFICATION
  G4a and G5 OVERLAP: 951 of 953 GENESIS records (99.8%) are placeholders.
  -> They are ONE population counted twice, not two independent gaps.
  -> Claimed '1180 fixture records (88.3%)' vs actual 1142 (84.9%).

HEADLINE
  84.9% of this ledger is fixture data. Chain-integrity
  gap-counting is the wrong lens; the dominant fact is that the
  production ledger is mostly SESS-* test records.
