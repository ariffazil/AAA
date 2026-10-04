# arifFlow Blind-FQ Repair — Full Playbook (2026-08-11 P0)

## Incident context
Organs wrote 1434+ receipts **directly** to `/var/lib/arifflow/receipts.jsonl`
instead of `POST http://127.0.0.1:7073/ingest`. The daemon's in-memory FQ
accumulator never saw them → 3+ actors held on stale `FQ=0.00`.

## Diagnosis (read-only first)
```python
import json, http.client
c = http.client.HTTPConnection("127.0.0.1", 7073, timeout=5)
c.request("GET", "/health"); h = json.loads(c.getresponse().read()); c.close()
print(h["fq"], h["receipts"], h["invariants"]["restricted_actors"])
```
- `wc -l /var/lib/arifflow/receipts.jsonl` — expect far more lines than daemon `receipts` count.
- Held actors all at `FQ=0.00` = classic blindness signature.

## Replay implementation notes
Receives already carry the exact `/ingest` dialect (PascalCase variants), so
POST each parsed line almost as-is. Do NOT re-map.

### PITFALL — requests sends empty body
`requests.post(url, data=..., headers={'Content-Type':'application/json'})`
intermittently delivers an EMPTY body to the Rust server → `400`
`{"error":"EOF while parsing a value at line 1 column 0","status":"invalid"}`.
That error = **transport failure**, not chain-validation. This is the single most
impactful fix: switching to `http.client` moved success from ~25% to ~85%.

Use the native protocol (mirror `arifflow_client.py::ingest()`):
```python
conn = http.client.HTTPConnection("127.0.0.1", 7073, timeout=5)
conn.request("POST", "/ingest",
             body=json.dumps(receipt, default=str).encode(),
             headers={"Content-Type": "application/json"})
resp = conn.getresponse(); body = resp.read().decode(); conn.close()
```

### PITFALL — replay is a feedback loop
The daemon persists every ingested receipt back to the SAME
`/var/lib/arifflow/receipts.jsonl`. Re-reading the file re-ingests daemon-appended
copies → file grows unbounded (observed 1905 → 4335 lines) and actors double-counted.
- Backup first (`cp ... receipts.jsonl.bak-P0-<ts>`).
- Exactly **one pass**. Do not re-run the replay to "improve" numbers.

### Expected outcome
- Batch ~50; checkpoint every ~500.
- Expect ~70–85% success; rejects log + continue (orphan `previous_receipt_hash`
  chains return 400 too — that IS chain-validation, distinct from transport EOF).

## Enforcement-cycle behavior (why /release didn't stick)
- `POST /release {"actor_id":"..."}` → `200 {"status":"released"}`.
- Enforcement re-runs every ~10s and **re-holds any FQ < 0.5** (STUCK band).
- Observed: FI-DELTA-MIND @0.80 stayed CLEAR; 333-AGI @0.35 and OpenCode-FI-001
  @0.00 were released then re-held.
- Permanent unblock = inject Verify receipts to lift band ≥ 0.5, not just release.

## FQ correctness rules
- Always read `execute_count` + `verify_count` WITH quotient.
- `verify_count==0` → quotient may be `f64::MAX` (OPTIMAL) = degenerate, not healthy.
- Report live `:7073/health`, not `AAA/state/flow_state.json` cache (drift 0.3).

## Audit-log EROFS (A-FORGE)
Root cause chain: `a-forge.service` `ProtectHome=read-only` + `privilege-inversion.conf`
`User=forge`; `/root` is `drwx------ root:root` so forge lacks traversal; the
`ReadWritePaths=/root/.agent-workbench` carve-out does not materialize on OpenVZ
(limited mount-namespace support, commented in the unit) → EROFS on append.
Fix: `AF_FORGE_AUDIT_PATH` env override (read by
`A-FORGE/src/interfaces/mcp/telemetry.ts` constructor) to a path already in
`ReadWritePaths`, e.g. `/var/log/forge/mcp-audit.jsonl`. `/root/forge_work/meta`
works only if forge is granted ownership/traversal.