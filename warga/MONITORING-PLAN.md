# Qwen Bridge — Tier-1 Monitoring Plan (7 days)

**Decision:** SAH (Arif F13 sovereign override, 2026-09-30)
**Window:** 2026-09-30 → 2026-10-07
**Goal:** observe real federation usage of the bridge before Tier-2 promotion decision

---

## What to watch

| Signal | Where to look | Healthy if |
|---|---|---|
| **Call volume per day** | `wc -l /root/VAULT999/warga/qwen-bridge/*.jsonl` (filtered by `kind=pre_call`) | rising then plateauing; no sudden 10× spike |
| **Scope distribution** | `grep '"kind":"pre_call"' *.jsonl \| jq -r .policy.bridgeFloor` | mostly OBSERVE_ONLY; ELEVATED only when justified |
| **F11 enforcement** | `grep '"kind":"post_call"' *.jsonl \| jq '.dropped_thought_chunks'` | >0 per call (Qwen always streams thoughts) |
| **Failure rate** | `grep '"returncode"' *.jsonl \| grep -v '":0"'` | < 5% non-zero |
| **Pre/Post hash chain** | `grep '"kind":"post_call"' *.jsonl \| jq 'select(.pre_hash == null)'` | zero broken chains |
| **External callers** | `ps -eo args \| grep qwen_bridge` | known agents (333-AGI / OpenCode) only; no unknown shells |

---

## Daily check (≤60 sec)

```bash
cd /root/AAA/warga && python3 -c "
import json, glob, collections
from pathlib import Path
today = Path('/root/VAULT999/warga/qwen-bridge')
files = sorted(today.glob('*.jsonl'))
for f in files[-7:]:
    kinds = collections.Counter()
    scopes = collections.Counter()
    drops = 0
    fails = 0
    for line in f.open():
        r = json.loads(line)
        kinds[r['kind']] += 1
        if r['kind'] == 'pre_call':
            scopes[r.get('policy', {}).get('bridgeFloor', '?')] += 1
        if r['kind'] == 'post_call':
            drops += r.get('dropped_thought_chunks', 0)
            if r.get('returncode', 0) != 0:
                fails += 1
    print(f'{f.name}: pre_call={kinds[\"pre_call\"]} post_call={kinds[\"post_call\"]} '
          f'scopes={dict(scopes)} drops={drops} fails={fails}')
"
```

---

## Tier-2 promotion criteria (gate for going from Tier-1 → Tier-2)

ALL of the following must be true before any Tier-2 work begins:

1. **7 days clean** — zero chain breaks, zero unknown external callers
2. **>50 calls served** — proves the bridge is in real use, not a toy
3. **<5% failure rate** — proves the wrapper is not breaking the agent
4. **No F11 leakage** — `dropped_thought_chunks` is monotonically increasing across the day (Qwen is always streaming thoughts; if drops = 0, the F11 gate is broken)
5. **arifFlow ingestion live** — the bridge's `_emit_ariflow()` call returns 2xx, not 400 (currently BROKEN — see §Known issues)

If any criterion fails → HOLD, diagnose, fix, restart the 7-day window.

---

## Known issues (open debt)

### 1. arifFlow `POST /ingest` returns 400

**Symptom:** bridge calls `_emit_ariflow()` after every pre_call + post_call. arifFlow responds 400 Bad Request.
**Impact:** not blocking, the JSONL log at `/root/VAULT999/warga/qwen-bridge/` is the source of truth. arifFlow was observability, never load-bearing.
**Tier-2 fix:** match arifFlow's MCP-tool field set (see `mcp__arifFlow__flow_ingest` schema: `actor_id, session_id, step_type, step_number, cost_ns, epistemic_label, floor_verdict, payload, previous_receipt_hash, witness_organs, harness_fingerprint`). Currently the bridge only sends 4 fields.

### 2. Unknown sibling test file

`/root/AAA/warga/qwen_bridge_test.py` (5.9 KB, NOT authored by FI-008) was written by an external OpenCode agent. It exercises the same public API with compatible test cases. Currently benign — a parallel test suite that the federation prefers. **Do not delete; instead, merge with `test_qwen_bridge.py` during Tier-2.** Note: this is a signal that the bridge's public API was already accepted as a federation contract.

---

## Rollback (reversible)

```bash
rm /root/AAA/warga/qwen_bridge.py \
   /root/AAA/warga/policy_schema.json \
   /root/AAA/warga/test_qwen_bridge.py
# Stop external liveness callers (they will fail gracefully on missing module)
```

No state outside `/root/AAA/warga/` and `/root/VAULT999/warga/qwen-bridge/` was mutated. The bridge is 100% reversible.

---

## Decision record

- **F13 sovereign:** Arif bin Fazil
- **Decision:** keep Tier-1, monitor 7 days
- **Issued:** 2026-09-30 12:12 MYT
- **FI-008 (Kimi Code) receiver:** session SEAL-031ea2c31cb04934, authority LIMITED_MUTATE
- **Bridge log start:** 2026-09-30T04:08:07Z
- **Window close:** 2026-10-07T04:08:07Z
- **Next action at window close:** Tier-2 promotion gate (this file §"Tier-2 promotion criteria")

---

*DITEMPA BUKAN DIBERI ⚒️ — Capability survives replacement.*