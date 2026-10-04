# Governance Enforcement Audit — N7 FQ Gate + N9 Gödel Lock (2026-08-05)

Audit task: verify two structural enforcement claims from a self-report, then produce a gap-closure plan. No production mutation — investigation only.

## Live FQ probe (arifFlow :7073/health)

```json
{
  "fq": {
    "execute_count": 2,
    "quotient": null,
    "verdict": "CAUTION",
    "verify_count": 1
  },
  "status": "ok",
  "uptime_ms": 77092,
  "formula_version": "qg.v0.2",
  "formula_hash": "sha256:arifflow-fq-v2.1-2026-08-05"
}
```

`quotient: null` is not "healthy" — denominator too small to compute (only 2 exec / 1 verify in window). Per F1 doctrine this falls into HOLD band. arifFlow daemon is up; FQ math is degenerate because the system hasn't accumulated enough history yet.

## N7 — FQ Gate (FQ<0.5 HOLD)

### AAA control plane — ENFORCED

- `/root/AAA/a2a-server/fq_gate.js` (145 lines, forged 2026-08-05)
  - L28-31: `ARIFLOW_URL = 'http://127.0.0.1:7073/health'`, `FQ_HOLD_THRESHOLD = 0.50`, `PROBE_TIMEOUT_MS = 3000`, fallback to `/root/AAA/state/flow_state.json`
  - L98-143: `fqGate()` (async) + `fqGateSync()` for middleware context
- `/root/AAA/a2a-server/server.js`
  - L58: `require('./fq_gate')`
  - L77-105: Express middleware `app.use(...)` — runs FIRST in chain. Reads `envelope.action_class`; OBSERVE/ANALYZE pass; everything else returns **HTTP 423** with `{error:'FQ_HOLD', verdict:'HOLD', fq:..., gate:'FQ'}` when `!fq.pass`
- Gate chain (post-2026-08-05 hardening): **FQ → G2 Witness → G3 Predict → Route**
- Git: commit `bfb81b71 feat: FQ Gate — constitutional HOLD at FQ < 0.5 (non-advisory)` — 188 insertions

### A-FORGE execution plane — PARTIAL

- `/root/A-FORGE/src/domain/forge/check_verdict.ts`
  - L68: `FQ_GATE_THRESHOLD = 0.50`
  - L82-111: `probeFq()` with 15s cache, fail-closed (returns `quotient: 0.0, verdict: 'UNREACHABLE'` if arifFlow down → blocks MUTATE)
  - L130-162: `checkFqGate(actionClass)` — exempts OBSERVE/DERIVE, blocks MUTATE/ATOMIC at FQ<0.50 or on UNREACHABLE
  - L194-219: `checkVerdictPrecondition()` calls `checkFqGate` as Gate 1 in a 5-gate chain
- `/root/A-FORGE/src/interfaces/mcp/client.ts`
  - L23: imports `checkVerdictPrecondition`
  - L246-330: on `MUTATE`/`ATOMIC`, calls `checkVerdictPrecondition(actionClass, sessionState)` at L301, throws `VERDICT_PRECONDITION_FAILED` if not permitted
  - **BUT:** L247 `if (requiresVerdictCheck(0.5) && (actionClass === 'MUTATE' || actionClass === 'ATOMIC'))` — the FQ gate only fires when `simulationIndex > 0.5`. Normal execution paths with simulationIndex ≤ 0.5 skip the gate entirely
- `/root/A-FORGE/domain/orchestration/arifFlow_adapter.py` (Python bridge to Rust arifFlow)
  - L388-498: `_call_arif_judge` — returns HOLD on arifOS timeout but **does NOT probe `arifFlow:7073/health` directly**. All Rust→arifOS round-trips via Python are ungated at the FQ level
- `/root/A-FORGE/src/infrastructure/receipts/flowReceiptStore.ts` is the Postgres truth for FQ (L204-218 computes `verifyCount/execCount`) but `computeFQ(sessionId)` (L242-305) is **not** called by `checkFqGate` — independent code paths

**What's missing for full A-FORGE enforcement:**
1. `forge_seal` (sealed as `IRREVERSIBLE` per `actionClassifier.ts:72`) — if `actionClassifier` misrecognizes the canonical name, it could skip the gate. Belt-and-braces: explicit `canonicalTool === 'forge_seal'` filter in `client.ts:247`
2. `arifFlow_adapter.py:_call_arif_judge` needs an FQ probe before the MCP call
3. `checkFqGate` should cross-check `arifFlow.quotient` against `flow_receipts.fq_verified` — divergence > 0.1 should HOLD

## N9 — Gödel Lock (Self-Judge/Self-Seal)

### Doctrine (CANON, well-defined)

- `/root/arifOS/arifosmcp/constitution/godel_lock.yaml` (196 lines, RATIFIED 2026-06-12, F13 SOVEREIGN):
  - **G3 External Witness Axiom** (L72-81): "Any permission to execute an irreversible or high-impact action must come from outside the agent's own frame." Enforcement spec: `arif_forge refuses all MUTATE actions without actor_signature != agent's own id AND judge_state_hash != null`. Failure: HOLD, cause `self_authorized_mutation`. Witness: F13 SOVEREIGN (cannot be delegated to LLM)
  - **G4 Non-Unity Axiom** (L83-94): single-witness SEAL on tier≥2 is auto-HOLD
- `/root/arifOS/GENESIS/058_THREE_CLOSURES.md` (407 lines, sealed 2026-08-02): Q9 boot-time check `witness_actor_id != actor_id`; §3.1 explicit `godel_lock_check(seal)` pseudocode (L166-186)

### arifOS kernel runtime — ENFORCED

- `/root/arifOS/arifosmcp/constitution/__init__.py` L20-25: imports `godel_lock.yaml`, exposes `GODEL_AXIOMS`, `GODEL_LOCK_RAW`
- `/root/arifOS/arifosmcp/constitution/runtime_hook.py` L30-89: `check_godel_lock()` — checks G1/G3/G4/G6/G7 against `actor_signature`, `has_judge_hash`, `has_plan_id`, `has_vaul999_connection`. Returns `{"ok": False, "verdict": "HOLD", ...}` on self-certification
- `/root/arifOS/arifosmcp/runtime/godel_lock_enforcement.py` L83: `if audit_result.get("seal_bound") and not audit_result.get("external_validated")` — explicit anti-self-seal check
- `/root/arifOS/arifosmcp/runtime/governance_pipeline.py`:
  - L164-172: imports `godel_lock_gate` lazily with availability flag
  - L964-995: **Gate 5.1 GÖDEL_CLOSURE** runs in pipeline; if `!gate.passed` and `enforcement_mode != "simulate"` → `result.verdict = PipelineVerdict.HOLD` and `next_safe_action = "GÖDEL_CLOSURE: provide outside witness (auditor_id) or F13 override."`
- `/root/arifOS/arifosmcp/server.py` L907-944: mid-judge `godel_lock` annotation; warns on SEAL-bound with no external witness

### AAA — PARTIAL

- `/root/AAA/a2a-server/membrane_middleware.js` L423-424: checks `envelope.witness.W3 === 0` → MEMBRANE_W3_ZERO
- `/root/AAA/a2a-server/witness_gate.js` L8-10, L130-205: G2 Witness Gate computes W1 (human), W2 (AI), W3 (earth)
- **Gap:** No AAA-side enforcement of `actor_signature != actor_id` for SEAL-bound self-actions. The membrane rejects zero-witness but not same-actor witness

### A-FORGE — ABSENT for `forge_seal` (with three divergent definitions — a red flag)

- **Path-level Gödel Lock** `/root/A-FORGE/src/interfaces/mcp/shell/godelLock.ts`:
  - L25-54: `GODEL_LOCKED_PATHS` (constitution, arifJudge, arifSeal, FloorEnforcer, identities, etc.)
  - L196-228: `checkModificationIntent({type, target, tool})`
  - **Called from** `forgeShell.ts:30` and L835-836 — blocks shell exec into locked paths. ENFORCED at shell entry
  - **NOT called from** `forge_plan`/`forge_apply`/`forge_seal` in `forgeTools.ts`. The `forge_seal` tool definition (L1071-1136) does not invoke this lock
- **F7 Gödel Lock (uncertainty band)** `/root/A-FORGE/src/domain/governance/godelLock.ts` L88-143: caps confidence at 0.97, injects Ω₀ ∈ [0.03, 0.05]. Wired as `createGodelMiddleware()` (L164-197) but **not registered in any visible route**. `applyGodelLockToToolResponse` (L203-233) is also unused
- **Reality-loop Gödel Lock** `/root/A-FORGE/src/domain/reality-loop/types.ts` L30-62: third `GODEL_LOCKED_PATHS` array (overlapping but not identical to the shell one)
- **Gap:** No `actor_signature != actor_id` runtime check on `forge_seal` calls. Q9 self-seal rejection (GENESIS/058 §3.1) has no A-FORGE-side implementation

## Gap-closure plan

### Gap A — Wire FQ gate into forge_seal + Python adapter path

1. `/root/A-FORGE/src/interfaces/mcp/forgeTools.ts` L1071: at top of `forge_seal` handler, before L1080 actor_id check, add:
   ```ts
   import { checkFqGate } from "../../domain/forge/check_verdict.js";
   const fqCheck = await checkFqGate("ATOMIC");
   if (!fqCheck.permitted) {
     return { error: "FQ_HOLD", verdict: "HOLD", reason: fqCheck.reason, gate: "FQ" };
   }
   ```
2. `/root/A-FORGE/src/domain/forge/check_verdict.ts` L82-111: cross-check `arifFlow.quotient` against `flowReceiptStore.computeFQ(sessionId)`. If divergence > 0.1, HOLD with `reason: "FQ_CROSS_SOURCE_DIVERGENCE"`
3. `/root/A-FORGE/domain/orchestration/arifFlow_adapter.py` L388-498: before MCP call, `requests.get(f"{ARIFLOW_DAEMON_URL}/health", timeout=2)`. If `fq.quotient < 0.5 OR fq.verdict in {STUCK, BURNING, OVERHEAT}` → return `VerdictResult(verdict="HOLD", reason="FQ_BELOW_THRESHOLD")` BEFORE invoking 888-JUDGE
4. `/root/A-FORGE/src/interfaces/mcp/client.ts` L247: add `|| canonicalTool === 'forge_seal'` to the actionClass filter

### Gap B — Gödel Lock self-seal runtime enforcement (Q9a/b/c)

1. `/root/A-FORGE/src/domain/forge/seal_gate.ts` (NEW): port `godel_lock_check(seal)` from `058_THREE_CLOSURES.md` §3.1 L166-186 into TypeScript. Signature:
   ```ts
   export function godel_lock_check(seal: SealInput): GodelLockVerdict { ... }
   ```
   - Q9a `len(witness_ids) < 2` → VOID, "Single-witness seal. ≥2 witnesses required for SEAL."
   - Q9b `witness_ids.every(w => w === seal.actor_id)` → VOID, "Self-referential seal. All witnesses == actor_id."
   - Q9c `!seal.prediction_id` → HOLD, "Seal without falsifiable prediction (Reality Loop)."
2. `/root/A-FORGE/src/interfaces/mcp/forgeTools.ts` L1130: in `forge_seal` handler, after actor_id parse at L1080:
   ```ts
   import { godel_lock_check } from "../../domain/forge/seal_gate.js";
   const witnessIds = (body.witness_ids ?? []) as string[];
   const lock = godel_lock_check({ actor_id, witness_ids: witnessIds, prediction_id: body.prediction_id as string | undefined });
   if (!lock.allowed) {
     return { error: "GODEL_LOCK", verdict: lock.verdict, reason: lock.reason, axiom: lock.axiom };
   }
   ```
3. `/root/AAA/a2a-server/witness_gate.js` L130-205: add `selfSealCheck(actor_id, witness_ids)` — reject if `witness_ids.length === 1 && witness_ids[0] === actor_id`. Expose via `module.exports`
4. `/root/AAA/a2a-server/membrane_middleware.js` L423: strengthen MEMBRANE_W3_ZERO to also reject `envelope.actor_id === envelope.witness?.human` and `envelope.actor_id === envelope.witness?.ai`
5. `/root/A-FORGE/src/interfaces/mcp/shell/godelLock.ts`: re-export `isGodelLocked` + `checkModificationIntent` as the **single source of truth** for path lock. F7 uncertainty and reality-loop versions become thin re-exports. New `seal_gate.ts` joins this consolidation under `/domain/governance/godel/`
6. Tests (`/root/A-FORGE/test/seal_gate.test.ts` NEW): mirror `/root/A-FORGE/test/godelLock.test.ts` structure. Cases:
   - `forge_seal({actor_id:'a', witness_ids:['a'], prediction_id:'p1'})` → VOID, Q9b
   - `forge_seal({actor_id:'a', witness_ids:[], prediction_id:'p1'})` → VOID, Q9a
   - `forge_seal({actor_id:'a', witness_ids:['b','c'], prediction_id:undefined})` → HOLD, Q9c
   - `forge_seal({actor_id:'a', witness_ids:['b','c'], prediction_id:'p1'})` → allowed

### Gap C — Boot-time attestation of closures (closes 058 §5)

1. `/root/AAA/a2a-server/server.js`: add `app.use(closuresAttestationMiddleware)` after the FQ gate middleware. Reads `058_THREE_CLOSURES.md`, runs `godel_lock_check`/`calhoun_lock_check`/`refusal_closure_check` (port §3.1-3.3), stamps `req._closures = {godel, calhoun, refusal}` on every request. Emit `closures=3/3` in boot log only when all three pass

## Lessons encoded

1. **Three definitions ≠ coverage.** When three Gödel-lock implementations exist in one codebase, none is complete — they each cover one axis (paths / uncertainty / self-seal). Consolidate under a single import boundary
2. **`export function` ≠ enforcement.** Grep for call sites, not just definitions. A fully exported gate with zero call sites is documentation
3. **Conditional gates are PARTIAL.** `if (requiresVerdictCheck(0.5))` before the FQ gate means it only fires under specific agent states. State explicitly which conditions gate the gate
4. **Middleware ≠ call-site coverage.** Express `app.use()` is global; `client.ts:301` is path-bounded. The middleware/call-site split determines whether "ENFORCED" survives scrutiny
5. **Python adapter paths often bypass JS gates.** When a JS-side gate is wired, the Python↔Rust↔kernel bridge is a separate attack surface. Always grep both languages

## Audit metadata

- Live FQ probed twice: first at uptime=7s (verdict=UNKNOWN, both counters 0); second at uptime=77s (verdict=CAUTION, 2 exec/1 verify, quotient=null due to small window). Formula hash changed from `v2.0-2026-08-04` to `v2.1-2026-08-05` between probes — same FQ code path, formula version increment
- Git context: `bfb81b71` (FQ gate), `2faeb526` (G2 witness), `ee561395` (G3 predict) — all forged 2026-08-05 by `kimi-code/FI-008`
- Author of gate code: `/root/AAA/a2a-server/fq_gate.js` header reads "Forged 2026-08-05. DITEMPA BUKAN DIBERI." — matches the bfb81b71 commit timestamp