# Deployment drift → ψ-plane contamination (worked example of K4 in practice)

> **Session:** 2026-08-07 — Arif's "agentic test on arifOS MCP tools / Opus 5 runtime geometry probe"
> **Lesson type:** Concrete reproduction of K4 (substrate honesty dictates agentic reality). NOT a new K-law.
> **Trigger:** When `/health` shows `deployment_drift_status: drift_detected` OR `runtime_drift: true` AND any downstream probe is being planned (agentic test, Opus 5 prompt, federation-wide verify).

## The case in one paragraph

arifOS kernel `:8088` was running at `deployed_commit: 8bbcb3695` while the source had moved to `4d2bedd0b` (3 unpushed commits ahead — INIT v5.0, preflight mode, WAJIB 3). The `/health` endpoint honestly reported this as `deployment_drift_status: drift_detected`, `runtime_drift: true`, `owner_summary.color: YELLOW`, `nine_signal.psi: SYUBHAH`. Every tool call returned a SEAL verdict on `arif_observe`/`arif_think`/`arif_route`, but the ψ-plane was contaminated — the kernel was lying about its own governance integrity. Frontier models (Opus 5) would have detected this and stalled or dropped to advisory bands.

**The fix was the standard deploy dance:**

```bash
cd /root/arifOS
git push origin main                     # T1 — push the 3 unpushed commits
make deploy-local                        # T2 — service restart on prod, must announce
```

After deploy:

| Field | Before | After |
|---|---|---|
| `status` | `degraded` | `healthy` |
| `deployment_drift_status` | `drift_detected` | `aligned` |
| `deployed_commit` | `8bbcb3695` | `4d2bedd0b` |
| `runtime_drift` | `true` | `false` |
| `owner_summary.color` | `YELLOW` | `GREEN` |
| `nine_signal.psi` | `SYUBHAH` | unclogged (next probe reads true state) |
| `arif_judge` evidence accepts dict | yes | yes |

**The probe was then re-run as `actor_id: "arif"` (the P0 hotfix exemption, 2026-08-06) and returned:** `actor_verified: true, authority_level: FULL, session_id: SEAL-15b9cb2d94c94151, effective_verdict: SEAL`. The full 8-tool loop exercised cleanly.

## K4 lesson applied

K4 says: *"Substrate honesty is a precondition for agentic scale, not an afterthought."* This case proved it — without fixing the drift first, every probe of the 8 canonical tools would have returned verdicts polluted by the ψ-plane lying about governance_integrity. The agent (frontier model or human) would be making decisions on a substrate that lied about its own integrity.

The 3-line pre-probe gate:

```bash
curl -sf http://127.0.0.1:8088/health | python3 -c "
import json, sys
d = json.load(sys.stdin)
print('status:', d.get('status'))
print('drift:', d.get('deployment_drift_status'))
print('runtime_drift:', d.get('runtime_drift'))
print('deployed:', d.get('software_release',{}).get('deployed_commit'))
print('source:', d.get('software_release',{}).get('source_commit'))
print('owner.color:', d.get('owner_summary',{}).get('color'))
"
```

If `deployed_commit ≠ source_commit` OR `runtime_drift: true` OR `owner_summary.color == YELLOW` → **fix the drift before probing for real work**. This is the operational translation of K4 into a one-liner gate.

## The `make deploy-local` exit-code trap

`make deploy-local` may exit code 1 even when the deploy succeeded, because the post-deploy **conformance spine** reports `CAUTION` on the pre-migration vault chain gap (60 historical gaps from May 2026, ruled `NON-ISSUE` 2026-06-05 by sovereign). That CAUTION is documented, sovereign-ruled, and **does not block the deploy**.

Verify the actual deploy independently:

```bash
test "$(cat /opt/arifos/app/.git_commit 2>/dev/null)" = "$(git -C /root/arifOS rev-parse HEAD)" \
  && systemctl is-active arifos.service | grep -q active \
  && curl -sf http://127.0.0.1:8088/health | python3 -c "import json,sys; sys.exit(0 if json.load(sys.stdin).get('status')=='healthy' else 1)" \
  && echo "DEPLOY OK (despite make exit 1)" || echo "DEPLOY FAILED"
```

If all three pass → deploy is good; the non-zero make exit is the conformance spine asserting itself honestly, not a real failure. Read the `unexplained_critical_evidence` array in the conformance output — if it's empty AND a sovereign ruling reference is present (`AGENTS.md VAULT999 known anomaly`, `ruling: NON-ISSUE`), the CAUTION is non-blocking.

## Agentic probe pattern (the 8 canonical verbs)

When asked to "test the kernel", "exercise arifOS MCP", or "agentic probe", use `curl` + JSON-RPC against `http://127.0.0.1:8088/mcp`. The 8 canonical verbs:

1. `arif_init` — session ignition, binds actor + floors + audit
2. `arif_observe` — multimodal sensing, evidence-gathering
3. `arif_think` — epistemically honest reasoning engine
4. `arif_route` — intent → organ routing
5. `arif_memory` — 6-layer federated memory (recall/remember/revise/forget/attest)
6. `arif_judge` — final constitutional arbitration (888)
7. `arif_forge` — controlled mutation (A-FORGE authority)
8. `arif_seal` — VAULT999 immutable seal

### Canonical probe envelope

```bash
curl -sf --max-time 30 -X POST http://127.0.0.1:8088/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": <n>,
    "method": "tools/call",
    "params": {
      "name": "<tool_name>",
      "arguments": { ... }
    }
  }' | python3 -c "<json extraction>"
```

### Why this works

- **No MCP client library needed** — FastMCP streamable-HTTP transport accepts plain JSON-RPC + the dual Accept header. curl + python3 is enough.
- **`session_id` is a free-form string** — the kernel doesn't reject arbitrary session IDs on `arif_observe`/`arif_think`/`arif_route`/`arif_memory`. Use a probe tag like `"agentic_probe_001"` so the trace_id chain is grep-able.
- **Anonymous actors are useful probes** — they hit OBSERVE_ONLY neutering on purpose, so you observe what the kernel does when the identity gate fails. `888_HOLD` on `arif_forge`/`arif_seal` for anonymous actors is correct behavior.
- **`arif` actor exemption (P0 hotfix 2026-08-06, wired through INIT v5.0)** — calling `arif_init` with `actor_id: "arif"` returns `actor_verified: true, authority_level: FULL, session_id: SEAL-<hex>, effective_verdict: SEAL`. This is the operator authority lane, not an arbitrary agent — use it to verify the gates are NOT silent failures, just deliberate neutering.

## Schema quirks discovered (2026-08-07)

- **`arif_judge.evidence` must be a `dict`, NOT a `list`.** Pydantic v2 will reject lists with `Input should be a valid dictionary [type=dict_type, input_value=[...]]`. Wrap list-shaped evidence in `{"probe_evidence": [...]}` or use a structured dict per claim.
- **`arif_think.question` is required** but the kernel can return `claim_state: UNSUPPORTED` when given an unsupported claim — that's the engine working, not failing.
- **`arif_observe.subject` and `arif_observe.frame` are natural inputs** for "do the MCP tools help with X?" style questions.
- **`arif_route.intent` is the routing key** — kernel returns resolved organ + mission + pipeline stages. Expect `organ: ARIFOS, mission_id: build` for keyword-classified intents.
- **`arif_seal.receipt` and `arif_seal.session_id` are required**; kernel rejects anonymous callers with `888_HOLD: IRREVERSIBLE requires non-anonymous actor_id`.

## K4 audit cadence (applied)

Before any agent-driven job consumes the `/health` payload, the K-Series bundle verification (K1/K2/K3 probes in the parent SKILL.md) MUST pass. If drift is detected via the pre-probe gate above, fix the drift FIRST — the bundle verification will catch the lie at the runtime-floor level, but drift must be resolved at the substrate level.

## Reference

- **Parent skill:** `arifos-kernel-eurekas` (K1-K6 substrate honesty laws)
- **Adjacent skill:** `arifos-federation-ops` (operational kernel/seal/topology layer — covers SCT renewal, Lane A/B seals, ATLAS333 ledger)
- **Source session:** 2026-08-07, Arif's "agentic test" request
- **Code paths verified:** `rest_routes.py:_build_governance_status_payload()`, `live_metrics.py` dual-vault reader
- **P0 hotfix reference:** 2026-08-06 'arif' actor exemption, commit `8bbcb3695`
- **INIT v5.0 reference:** commit `4d2bedd0b` — collapsed 4-step governed ignition