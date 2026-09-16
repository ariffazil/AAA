---
name: live-pipeline-trace-audit
description: "Trace a live pipeline hop-by-hop with measured receipts."
version: 1.0.0
owner: Hermes ASI (persona-system)
risk_tier: low
floor_scope: [F2, F3, F4, F7, F11]
autonomy_tier: T1
triggers:
  - "trace the pipeline"
  - "audit the request path"
  - "hop-by-hop"
  - "execution trace / receipt"
  - "latency breakdown / TTFT"
  - "subsurface systems audit"
  - "profile the running system"
---

# Live Pipeline Trace Audit

Repeatable method for tracing a live execution pipeline end-to-end (ingress→context→routing→execution→safety→egress) and producing a measured, evidence-backed audit report. Grounded in live probes and receipts — never in invented diagrams or guessed timestamps.

## The Iron Rule (F2 / F3)
```
Never issue a receipt for a hop you did not measure.
If a hop cannot be measured directly, label it [UNMEASURED] — never invent a timestamp.
```
An auditor that fabricates a timestamp is a fraud architect, not a systems auditor. A WARN/HOLD verdict on real findings beats a fabricated PASS every time.

## The Hop Taxonomy (adapted to the actual system)
| Hop | Stage | Measure |
|-----|-------|---------|
| 0 | Ingress (client→gateway/reverse-proxy) | process table + systemd unit; often [UNMEASURED] out-of-process |
| 1 | Context ingestion (file reads / memory) | `wc -c` / `wc -l` on pre-fill artifacts |
| 2 | Routing & model/product selection | `curl /v1/models` — cross-check declared model |
| 3 | Execution (inference / tool loop) | **streaming TTFT (first chunk)** + total, chunk count |
| 4 | Safety / verification floor | schema.json of the verdict/artifact type; existence check |
| 5 | Egress (stream response / DB write / seal) | `ss` for target port; registry listing |

## Procedure
1. **Map the surface first.** `systemctl cat <gateway>` reads the actual unit; read the wrapper script it ExecStarts. Real routing env vars live there (e.g. `OPENAI_BASE_URL=http://127.0.0.1:4000/v1`). Never assume from a diagram.
2. **Probe every hop the mandate names**, time-boxed so nothing hangs (see Pitfalls).
3. **Execute a real synthetic probe** through the live router for Hop 2/3. Measure TTFT via streaming (first `data:` chunk); non-stream `time_starttransfer` is a lower bound, not true TTFT.
4. **Verify every referenced artifact exists before certifying it.** If the audit names a scar/record/handle, grep the actual registry and confirm the ID conforms to the schema.
5. **Report** with: sequence diagram (ASCII), latency+token table per hop, bottlenecks/leak points, final seal status.

## Output Contract
```
Verdict headline: SEAL_STATUS: PASS | WARN | SEAL_FAIL (+ one-line why)
1. Sequence diagram
2. Latency & token budget table (per hop, measured)
3. Identified bottlenecks / extractive leak points (severity + evidence)
4. Final seal status gate table
5. Open questions to the user (so WARN doesn't dangle)
```

## Pitfalls (learned the hard way)
- **Recursive grep/find over `/root` hangs the probe.** `grep -rl <needle> /root` and `find /root -iname <pattern>` on a deep tree can exceed 300s and time out. Fix: scope to the specific state dir, and ALWAYS wrap in `timeout 10-15 grep ...` so the command returns instead of hanging the whole audit.
- **Model alias drift is common.** Config often declares a PRIMARY model alias the router's `/v1/models` does not expose (e.g. config says `-vision-exp`, router has only `-flash`). Surfaces as HTTP 400 `Invalid model name`. Cross-check the declared alias against `/v1/models` and report the mismatch — a genuine F4 finding (stated intent ≠ reality), not a transient error.
- **A 403 with a fallback chain is data, not an error.** Read the error body: LiteLLM logs the model-group fallback list (`i-arif→apex-888→agi-333→forge-777→asi-555`) inside the message. That reveals routing permissions and the group topology.
- **Never certify a phantom artifact.** If the audit says "prove enforcement of `scar_foo_bar`" and that handle does not exist (and fails the schema pattern), say so plainly and list what DOES exist. F2 forbids fabricating enforcement of a record that isn't there.
- **TTFT measurement:** streaming gives true first-token latency; non-stream `time_starttransfer` includes router/schema round-trip and is looser. Use a small `subprocess.Popen` + parse `data:` chunks (see `scripts/ttft_probe.py`).

## Support
- `scripts/ttft_probe.py` — streaming TTFT + total + chunk-count prober against any OpenAI-compatible `/v1/chat/completions`. Run, don't hand-type.
