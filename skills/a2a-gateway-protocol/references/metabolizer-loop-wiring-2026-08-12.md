# Metabolizer Loop Wiring — Session Detail (2026-08-12)

## Files touched

| File | Change | Lines |
|---|---|---|
| `server.js:4508` | Added `decodeTasksToEnvelopes` to import | 1 |
| `server.js:4540` | Added `decomposeGoal(G)` call in decompose endpoint to register goal | 3 |
| `server.js:4598` | Fixed param extraction (`req.jsonrpc.params.goal_id` instead of `req.body.goal_id`) | 4 |
| `server.js:4580` | Changed `app.get('/a2a/goal/list')` → `app.post(...)` | 1 |
| `server.js:73` | Added `listActiveDecompositions` to metabolizer_loop require | 1 |
| `metabolizer_loop.js:54` | Destructured `{tasks, jacobian, receipts}` instead of `{tasks, meta}` | 1 |
| `metabolizer_loop.js:57` | Fixed decodeTasksToEnvelopes args: `(tasks, jacobian, goal)` | 1 |
| `metabolizer_loop.js:70` | Fixed return to build `meta` from destructured vars | 1 |
| `middleware/receipt_wrap.js:102-140` | Added composite G + C_dark computation | ~20 |
| `chat_agent.py:149,230` | Already ADVISORY (pre-existing, no change needed) | 0 |

**Total: ~31 lines changed across 4 files.**

## A2A-Version header requirement

ALL `/a2a/goal/*` endpoints go through `jsonRpcValidate` which requires:
- POST method (not GET)
- `A2A-Version: 1.0` header
- JSON-RPC 2.0 body with `method` field

Without `A2A-Version` header → `-32600 Invalid Request`. Without `method` in body → `-32600 method must be a string`.

## The "goals don't register" pattern

**Symptom:** decompose returns `goal_id` but `list` returns `count: 0` and metabolize returns "goal_id required".

**Root cause:** The decompose endpoint calls `encodeGoalToTasks(G)` which does NOT register the goal in `_activeDecompositions`. It only computes tasks + Jacobian locally. The registration only happens when `decomposeGoal(G)` is called — but the old decompose endpoint never called it.

**Fix:** Add `decomposeGoal(G)` call after encoding, inside the decompose endpoint, before the response.

**Key insight:** `encodeGoalToTasks()` ≠ `decomposeGoal()`. The former is a pure function (G → tasks). The latter is a stateful registrar (G → map entry). The metabolizer loop can only metabolize goals that were registered via `decomposeGoal()`.

## Composite G computation (Gap A — receipt_wrap.js)

```
G = (A × P × E × X)^0.25
A = authority: ARIF→1.0, loopback→0.5, anonymous→0.1
P = pass: status<400→1.0, else→0.0
E = efficiency: max(0.1, min(1.0, 1 - latency/30000))
X = completeness: valid result→1.0, void/fail→0.0
C_dark = A × (1−P) × (1−X)
```

G is emitted on EVERY MCP receipt. Currently blocked from flushing to outcomes.jsonl by `chattr +a` + root:root ownership — `arifos` user can't append. Requires F13 decision to add arifos to append-allowed list OR write to separate `receipts.jsonl`.

## Deployment

```bash
# After all edits:
systemctl restart aaa-a2a.service
sleep 3

# Verify health:
curl -sf http://127.0.0.1:3001/health

# Verify decompose:
curl -sf -X POST http://127.0.0.1:3001/a2a/goal/decompose \
  -H "Content-Type: application/json" -H "A2A-Version: 1.0" \
  -d '{"jsonrpc":"2.0","method":"goal.decompose","id":1,"params":{"goal":"test"}}'
# → goal_id=g-XXXXX, tasks=1

# Verify metabolize:
curl -sf -X POST http://127.0.0.1:3001/a2a/goal/metabolize \
  -H "Content-Type: application/json" -H "A2A-Version: 1.0" \
  -d '{"jsonrpc":"2.0","method":"goal.metabolize","id":2,"params":{"goal_id":"g-XXXXX","results":[]}}'
# → state=SEALED, cycles=1
```
