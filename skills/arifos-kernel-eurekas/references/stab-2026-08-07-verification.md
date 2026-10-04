# STAB-2026-08-07 + 07b Verification — Opus 5 + Hermes + Kimi Chain

> **Sessions:** 2026-08-07 — Agentic test of arifOS MCP surface via Claude Opus 5 (Claude Desktop) + Gemini 2.5 Pro + Hermes ASI + Kimi Code FI-008
> **Commits:** `367b4c38` (STAB-2026-08-07, Kimi-Code FI-008), `05b6b433f` (STAB-2026-08-07b, Hermes)
> **Test invocations:** `PYTHONPATH=. /opt/arifos/venv/bin/python -m pytest tests/runtime/test_unmeasured.py tests/runtime/test_verdict.py -q -p no:logfire` → **48/48 pass**

## 8 invariants wired (Rules #1–#8)

| # | Invariant | Where | Status |
|---|---|---|---|
| 1 | Empty evidence = STOP | `judge.py:1078-1084` (EVIDENCE_EMPTY gate) | ✅ live |
| 2 | No fake math (0.65 → None → UNMEASURED → HOLD) | `tools.py:7944` (round(None) fix), `:7915` (UNMEASURED band → HOLD), `:5046` (failure-path 0.5→None) | ✅ live |
| 3 | One source per question (single constitutional_check) | `tools.py:4984-5043` (dual-truth derivation), `session_standing.py:809` (floor_passed from effective_verdict+failed_floors+canonical_verdict) | ✅ live (STAB-2026-08-07b) |
| 4 | Daily liveness (K8) | `scripts/daily_liveness.py` (cron-ready) | ✅ wired |
| 5 | Identity immutability | `session_standing.py:325` (preserves original_claimed_id) | ✅ |
| 6 | Evidence hash on judge (1373/1374 rule) | `judge.py:1078` (EVIDENCE_HASH_MISSING gate — Kimi added) | ✅ live |
| 7 | Execution Witness Protocol (probe-to-witness) | Documentation-level (needs `probed_receipt_id` gate in `core/governance_kernel.py:191`) | ❌ not wired |
| 8 | Never predict a probe result | Skill body (this file's Rule #8 section) | ✅ codified |

## STAB-2026-08-07b — The "Last Writer" Pattern

**The bug STAB-2026-08-07b fixed:** `cc.floor_passed=True` alongside `effective_verdict=HOLD` on judge path. Both Rule #3's enrichment (`tools.py:4984-5043`) and `_sync_authority_surfaces_from_standing_dict` ran *before* `attach_effective_verdict` wrote `effective_verdict`. Both correctly computed `floor_passed` from the same data — but that data was empty. Order beat logic.

**The fix:** `attach_effective_verdict` (`verdict.py:302+`) is now the **last writer** of `effective_verdict`. Immediately after writing `effective_verdict`, it re-derives `cc.floor_passed`, `cc.hold_required`, `cc.failed_floors`, and `cc.hold_reason`. `cc._derivation = "attach_effective_verdict:last_writer"`.

**Live verification (post-deploy, 2026-08-07T12:48Z):**
```python
import json, urllib.request
def probe(tool, args):
    body = json.dumps({"jsonrpc":"2.0","id":1,"method":"tools/call",
        "params":{"name":tool,"arguments":args}}).encode()
    req = urllib.request.Request("http://127.0.0.1:8088/mcp", data=body,
        headers={"Content-Type":"application/json","Accept":"application/json, text/event-stream"})
    return json.loads(json.loads(urllib.request.urlopen(req).read())["result"]["content"][0]["text"])

# judge with evidence dict → should be HOLD + floor_passed=False
r = probe("arif_judge", {"proposal":"jspace","evidence":{"source":"docs/1373.jpg"}})
assert r["effective_verdict"] == "HOLD", f"judge verdict: {r['effective_verdict']}"
assert r["constitutional_check"]["floor_passed"] is False, \
    f"judge cc.floor_passed: {r['constitutional_check']['floor_passed']}"
assert r["constitutional_check"]["_derivation"] == "attach_effective_verdict:last_writer"

# observe entropy_dS → also HOLD + floor_passed=False
r = probe("arif_observe", {"query":"vault both empty and full","mode":"entropy_dS"})
assert r["effective_verdict"] == "HOLD"
assert r["constitutional_check"]["floor_passed"] is False

print("STAB-2026-08-07b: PASS — single-source canonical floor_passed")
```

**Receipt (live, post `05b6b433f`):**
```
effective_verdict: HOLD
cc.floor_passed  : False
cc.hold_required : True
cc.hold_reason   : STAB-2026-08-07b canonical: effective_verdict=HOLD failed_floors=[]
cc.failed_floors : []
cc._derivation   : attach_effective_verdict:last_writer
```

## Rule #8 — Never Predict a Probe Result

**Defect pattern (2026-08-07, Gemini prediction):** Gemini generated a 3-paragraph script of what Opus 5's audit would say — before Opus 5 actually ran. 3/5 predictions were wrong. The prediction *replaced* the test, and the system had no receipt to falsify it.

**Why it's wrong:** A forecast dressed as a receipt is the highest-value lie in the system. It arrives sounding like exactly what you hope. If the forecast is wrong, the system learns nothing. If it's right, the system can't tell whether the forecast was lucky or the probe was real.

**Law (Rule #8):** Never predict a probe result. Run it, or report UNMEASURED. A prediction of a system state is not evidence of a system state.

**Operational consequence:** If you are about to write "Opus 5 will say X" — STOP. Write the curl command to probe the actual state. The time it takes to type a prediction is enough time to run the probe.

**Anti-pattern (live transcript, 2026-08-07):**
> Gemini: "Opus 5 will output something like this: 'The kernel works...'"
> Opus 5: "The kernel works. Score on the prediction: 2 right out of 5."

The prediction script is itself the violation. The corrective is: **don't write the script. Run the probe. Quote the probe.**

## AAA :3001 is A2A, not MCP (receipts)

| Probe | HTTP | Body |
|---|---|---|
| `POST /mcp` | 404 | `{"error":{"code":-32601,"message":"Endpoint /mcp not found"}}` |
| `GET /.well-known/agent.json` | 200 | `{"name":"AAA A2A Gateway","url":"https://aaa.arif-fazil.com","schema":"https://a2a-protocol.org/schemas/agent-card/v1.0"}` |
| `POST /tasks` | 400 | (endpoint exists, malformed body) |

## Session state files

- `/root/forge_work/sessions/2026-08-07-kernel-stabilize/` — snapshot, patches, reports
- `/tmp/fv_*.json` — final verification probe payloads
- `/tmp/stab7b_*.json` — STAB-2026-08-07b verification payloads

## Known residuals (NOT yet fixed)

1. **`delta_S` ghost on observe path** — inner result carries `None`, but top-level wrapper still emits `0.0`. Fix path: either build real Shannon-entropy-on-input or strip `delta_S` from active surface. **Sovereign decision pending (888).**
2. **Identity drift downstream of init** — arif_init locks `arif-fazil`, but arif_judge / arif_observe may still truncate to `arif`. Deferred: needs canonical_id cookie between init and downstream organs.
3. **Remaining 0.65/0.5 hardcodes** — `runtime/envelope.py:484`, `semantic_edge.py:180`, `quality_arqocf.py:30/140`, `memory_bridge.py:38/54/241`, `rasa_contract.py:361`. Unrelated to STAB; cosmetic unless surfaced as inner-result confidence.
4. **Execution Witness Protocol (Rule #7)** — `core/governance_kernel.py:191` accepts witness scores without `probed_receipt_id` gate. Doc-only.