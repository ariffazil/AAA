# Session A — Operation + ReceiptOutbox

> **Status:** READY — execute when arifOS kernel is stable and PostgreSQL is up.
> **Authority:** F1 AMANAH (reversible) · F11 AUDIT · F13 SOVEREIGN for deployment.
> **Blast radius:** HIGH (changes execution path across all organs).
> **Pre-built:** OperationBus types + implementation in `AAA/src/gateway/`

---

## Pre-conditions (verify before starting)

```
✅ arifOS healthy:  curl -sf http://localhost:8088/health | jq .status
✅ PostgreSQL up:   docker ps | grep postgres
✅ No merge conflicts on arifOS
✅ OperationBus types compiled: cd /root/AAA && npx tsc --noEmit
```

---

## Step 1 — Deploy the durable bus (AAA side)

The bus is already built at `AAA/src/gateway/operation-bus.ts`. It writes to `/root/AAA/data/bus/operations.jsonl` and `receipts.jsonl`.

```bash
cd /root/AAA
mkdir -p data/bus
npx tsx -e "
import { getOperationBus } from './src/gateway/operation-bus.ts';
const bus = getOperationBus();
// Smoke test
const op = bus.emitOperationStart({
  actor_id: 'session-a-test',
  session_id: 'SEAL-TEST',
  trace_id: 'trc-test',
  organ: 'arifos',
  capability: 'arif_init',
  stage: '000_INIT',
});
bus.emitOperationComplete(op.op_id, true);
bus.emitReceipt({
  op_id: op.op_id,
  session_id: 'SEAL-TEST',
  trace_id: 'trc-test',
  organ: 'arifos',
  result_summary: 'Session A smoke test passed',
  vault_candidate: false,
});
console.log('Stats:', JSON.stringify(bus.stats(), null, 2));
"
```

## Step 2 — Wire emission points in arifOS

Add to arifOS tool handlers (one import, two lines per tool):

```python
# In each arif_* tool handler, add:
from arifosmcp.runtime.operation_bus import get_bus

bus = get_bus()
op = bus.emit_start(actor_id, session_id, trace_id, organ="arifos", capability="arif_init", stage="000_INIT")
# ... execute tool ...
bus.emit_complete(op.op_id, success=True)
bus.emit_receipt(op.op_id, session_id, trace_id, "arifos", f"arif_init completed")
```

### Priorities for wiring:
1. `arif_init` — session birth (stage 000)
2. `arif_judge` — constitutional verdict (stage 888)
3. `arif_seal` — VAULT999 append (stage 999)
4. `arif_forge` — execution (stage 010)
5. `arif_observe` — reality sensing (stage 111)

## Step 3 — Update observatory readers

Replace static 000–010 placeholders with bus stats:

```python
from arifosmcp.runtime.operation_bus import get_bus

bus = get_bus()
stats = bus.stats()
metabolism_pass = stats.by_stage  # real counts per stage
```

## Step 4 — Verify

```bash
# 1. Bus grows
wc -l /root/AAA/data/bus/operations.jsonl
wc -l /root/AAA/data/bus/receipts.jsonl

# 2. Edges show session/actor/trace/receipt
python3 -c "
import json
with open('/root/AAA/data/bus/operations.jsonl') as f:
    ops = [json.loads(l) for l in f if l.strip()]
print(f'Operations: {len(ops)}')
stages = {}
for o in ops:
    stages[o['stage']] = stages.get(o['stage'], 0) + 1
for s, c in sorted(stages.items()):
    print(f'  {s}: {c}')
"

# 3. Observatory snapshot shows non-zero metabolism
curl -s http://localhost:8088/api/observatory/v1/snapshot | jq '.metabolism_pass'
```

## Step 5 — Reversibility

All bus writes are append-only. No existing data is modified. Rollback:
```bash
# Truncate test data only
echo '' > /root/AAA/data/bus/operations.jsonl
echo '' > /root/AAA/data/bus/receipts.jsonl
```

---

## Output

- `SESSION_A_OPERATION_RECEIPTOUTBOX_REPORT.md` with:
  - Bus stats (operations, receipts, vault candidates)
  - Observatory snapshot (edges + metabolism comparison)
  - Wiring summary (which tools emit, which stages mapped)
  - Test evidence

---

## Change Control

```yaml
reversible: true
blast_radius: high
authority_required: F13_SOVEREIGN_FOR_DEPLOYMENT
judge_receipt_required: true
human_ack_required: true
rollback: truncate bus files, revert observatory readers to static placeholders
post_change_probe: verify bus stats > 0, observatory metabolism_pass > 0
```

---

*DITEMPA BUKAN DIBERI — Forged, Not Given.*
