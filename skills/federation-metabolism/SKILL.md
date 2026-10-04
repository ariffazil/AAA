---
name: federation-metabolism
description: "Operate the arifFlow (:7073) metabolism plane — receipt ingestion, FQ state diagnosis, blind-FQ repair, actor unblock, invariant enforcement cycles, audit-log path drift. Trigger: actors held on stale FQ=0.00, POST /ingest failures, daemon blind/receipts.jsonl growing without FQ effect, /release not sticking."
---

# Federation Metabolism — Operating arifFlow (:7073)

The arifFlow metabolism plane transmits and counts execution evidence but does not judge. It owns FQ (Flow Quotient), invariant enforcement gates, and the receipt chain. For governance/arifOS/judging use `arifos-federation-ops`; this skill handles the **nerve** layer.

## 1. Anatomy of arifFlow

| Surface | Port | Role |
|---------|------|------|
| GET `/health` | :7073 | FQ quotient + verdict + restricted_actors + receipt window |
| POST `/ingest` | :7073 | Submit flow receipt; updates in-memory FQ per actor |
| POST `/check` | :7073 | Invariant gate — can actor execute? |
| POST `/release` | :7073 | Release HOLD on actor after verification |
| POST `/enforce` | :7073 | Trigger enforcement cycle manually |

Receipts must reach `/ingest`. Writing to disk (`receipts.jsonl`) is NOT ingestion — the daemon never sees them.

## 2. FQ diagnosis (blindness pattern)

```bash
curl -s http://127.0.0.1:7073/health | python3 -m json.tool
```

**Signs of blindness:**
- `restricted_actors` contains actors with `FQ=0.00` reason
- `receipts` field shows low count despite large `receipts.jsonl` file
- Multiple actors all at exactly `FQ=0.00` simultaneously

**Not blind:** single actor low FQ (genuine low verify). Check `execute_count` + `verify_count` with quotient. If `verify_count==0` but `execute_count>0`, quotient may show OPTIMAL but this is a degenerate artifact (`verify==0 → f64::MAX`). See also FQ pitfall in `arifos-federation-ops`.

## 3. Blind-FQ repair (replay bypassed receipts)

When organs wrote receipts to `receipts.jsonl` instead of POSTing:

### Step A — Backup
```bash
cp /var/lib/arifflow/receipts.jsonl /var/lib/arifflow/receipts.jsonl.bak-P0-$(date +%Y%m%dT%H%M%S)
```

### Step B — Replay with http.client (NOT requests)
Parse each line, `http.client.HTTPConnection('127.0.0.1',7073)`, `conn.request("POST","/ingest",body=json.dumps(line).encode(),headers={"Content-Type":"application/json"})`. Batch size ~50, checkpoint every ~500.

**Why http.client:** the `requests` library intermittently sends EMPTY bodies to the Rust server → `400 {"error":"EOF while parsing..."}`. This is the **transport signature**, NOT chain-validation failure. Match the native `arifflow_client.py::ingest()` protocol exactly.

**Payload keys match Rust PascalCase variants:**
- `epistemic_label`: `"Observation"` | `"Derivation"` | `"Interpretation"` | `"Specification"` | `"Seal"`
- `floor_verdict`: `"Pass"` | `"Caution"` | `"Hold"` | `"Void"`
- `cooling_decision`: `"None"` | `"Hold"` | `"Clamp"` | `"Bypass"`

### Step C — Single pass only
The daemon persists every ingested receipt back to the SAME JSONL file. Re-reading = re-ingesting = runaway growth. One pass, stop.

Expect ~70–85% success rate after the first few batches (chain-validation catches orphan chains). Log rejects, continue.

## 4. Actor unblock — release is transient

`POST /release {"actor_id":"333-AGI"}` returns `200 released` but the enforcement cycle (~10s) re-holds any actor with **FQ < 0.5** (STUCK band). So:
- Actors now at FQ ≥ 0.5 stay CLEAR after release.
- Actors still under FQ < 0.5 get re-held — the release worked but cannot stick. Permanent unblock needs Verify receipts lifting the band above 0.5.

Always check `restricted_actors` AFTER one enforcement cycle completes to see true state.

## 5. Audit-log EROFS (A-FORGE side-channel)

`a-forge.service` sets `ProtectHome=read-only` + runs `User=forge`; `/root` is `drwx------ root:root`. forge cannot traverse it, and `ReadWritePaths=/root/.agent-workbench` carve-out fails silently on OpenVZ (limited mount namespaces) → EROFS on append.

Fix: set `AF_FORGE_AUDIT_PATH` env var (natively read by telemetry.ts constructor) pointing to a non-/root path already in `ReadWritePaths` (e.g. `/var/log/forge/mcp-audit.jsonl`).

See full diagnostics: `references/ariflow-ingest-repair.md`.

## 6. FQ vector not operationalized (2026-08-14 audit)

`ActorFlowState` (invariants.rs:220) computes per-actor FQ in memory: quotient, verdict, execute_count, verify_count, held, throttled. The `InvariantEnforcer.actors` BTreeMap holds all actors.

**BUT `/health` does NOT expose this vector.** It only returns:
- Global scalar FQ (aggregate of all receipts)
- `restricted_actors()` — only actors currently held/throttled (not the full vector)

So FQ=47.0 OPTIMAL globally can hide 333-AGI at FQ=0.00 STUCK underneath. The vector is computed but invisible to consumers.

**Fix direction:** expose `actors` BTreeMap in `/health` payload (additive, like the health degraded_reasons fix).

## 7. FQ multi-language inconsistency (2026-08-14 audit)

FQ exists in FIVE places across three languages, with inconsistent thresholds and verdict bands:

| Version | Location | Key differences |
|---------|----------|----------------|
| Rust compute() | receipt.rs:307 | SOURCE OF TRUTH. 6 states: Unmeasured/Caution/Optimal/Flowing/Stuck/Burning. q≥1.0=Optimal, no high-FQ band. |
| Rust ActorFlowState | invariants.rs:300 | Same bands but uses deprecated `state.fq` alias in restricted_actors() despite comment saying "do NOT read fq" |
| Python φFQ | rest_routes.py:1028 | CONSUMER. Different thresholds: FQ∈[1,3]=1.0, FQ>3.0=3.0/FQ (damp). Rust has no >3 band. |
| Calhoun gate | calhoun_anti_sink_gate.py:56 | FQ_OVERHEAT_THRESHOLD=3.0, FQ_WINDOW=3. Hardcoded, not inherited from Rust. |
| TS mirror | fq.ts | Has DUAL UNMEASURED states (UNMEASURED + UNKNOWN) Rust doesn't have. Uses cost_ns>0 instead of StepType enum. |
| Kabarkan alerts | kabarkan_fq.rs | References FlowVerdict::Watching which compute() never assigns (dead enum). |

**Key bugs:**
1. Dead enum values: `Watching`, `Overheat`, `Balanced` exist in FlowVerdict but compute() never assigns them
2. `restricted_actors()` reads `state.fq` (deprecated) instead of `state.quotient`
3. FQ=47 verdict=OPTIMAL but φFQ=0.064 (3/47) — three opinions on one number
4. TS and Rust verdict bands diverge
5. No FQ frame metadata (window, sample_size, formula_version) on quotient values

See `references/fq-multi-language-inconsistency.md` for full audit with line numbers.

## 8. /health degraded_reasons[] + layer_health{} patch (2026-08-14, commit 5ad10f2f7)

The arifOS `/health` endpoint (rest_routes.py) now exposes:
- `degraded_reasons[]` — structured array with `{layer, field, value, severity, explanation}` per cause
- `layer_health{}` — 4 sub-objects: `constitutional`, `runtime`, `registry`, `infra`
- `_freshness_warning` on init tokens when built_commit is stale
- `_design_note` on tool_count_semantics (62/48/8 by design)
- Precedent surfacing in `judge.py` (advisory, non-blocking — `_precedent_advisory` was computed but never exposed)

This fix pattern (scalar → coordinate system) applies to FQ too: global FQ quotient → per-actor FQ vector with frame metadata.

## Pitfalls

- `requests` lib empties POST body → EOF parse error. Use `http.client` ALWAYS.
- Daemon appends to source JSONL during ingest → replay feedback loop. Backup first, one pass ONLY.
- `/release` is advisory — enforcement re-holds FQ < 0.5. Do not claim permanent unblock if FQ < 0.5.
- FQ "OPTIMAL" when `verify_count==0` is false — zero-verifies mean degeneracy, not health. Always report execute+verify counts alongside quotient.
- Global FQ quotients can be wildly misleading (FQ=47 OPTIMAL hiding per-actor FQ=0.00 STUCK). Always check restricted_actors AND probe per-actor state if diagnosis matters.
- Receipts MUST use Rust variant names (PascalCase), not Python Enum values.
- `session_token`, `topology_id`, `lane_id`, `merkle_root`, `merkle_inclusion_proof` are typically null in live organ receipts — do not fabricate values.
- Never trust a single language's FQ reading without cross-checking the other two. The same number means different things in Rust vs Python vs TS.

## Support files

- `references/ariflow-ingest-repair.md` — full blind-FQ repair playbook: step-by-step, transport-pitfalls, enforcement-cycle behavior, EROFS side-note.
