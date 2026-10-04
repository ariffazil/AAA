# OpenClaw "memory_search broken" → real cause: gateway heap pressure (2026-08-09)

## Scenario
Sibling agent (OpenClaw itself, or another lane) reports: "hermes-agent is
INACTIVE", "memory_search embeddings broken — timed out 15s", "DeepSeek dead".
All three were WRONG or stale when probed. The verifiable root cause behind the
"broken memory_search" claim was OpenClaw's own gateway heap pressure.

## Live evidence chain (what to probe, in order)
1. Port truth beats claims:
   `curl -sf http://localhost:18789/health` → `{"ok":true,"status":"live"}`
   (OpenClaw) and `curl -sf http://localhost:18089/health` (Hermes edge) —
   a sibling claiming "hermes INACTIVE" while :18089 answers = stale/wrong probe.
2. Memory pressure signature in journald:
   `journalctl -u openclaw-gateway -n 200 | grep -i "memory pressure"` →
   `[diagnostics/memory] memory pressure: level=warning reason=heap_threshold
   rss=1.25 GiB heap=1.04 GiB threshold=1 GiB thresholdRatio=103.5%
   nextStep=run openclaw gateway status --deep ... restart gateway if pressure persists`
3. Restart history:
   `systemctl show openclaw-gateway -p MainPID -p NRestarts`
   Compare MainPID against `ps aux | grep openclaw-gateway`. PID changed since
   last session = auto-restart happened (Restart=always, RestartSec=15).
   NRestarts>0 or pressure recurring ~4h after a restart = leak or threshold
   set too low — NOT transient.
4. Correlate: internal searches (memory_search) timing out at 15s while the
   gateway is at 103.5% heap = thrash, not a broken embedding service.
   Qdrant :6333 healthz and ollama :11434 both healthy = embeddings substrate
   fine; the gateway's OWN heap is the bottleneck.

## Verdict pattern
- Report the real cause, not the sibling's label: "memory_search didn't break —
  the gateway is heap-thrashing at 103.5% of threshold."
- Restart is T1-class (single service) but drops in-flight sessions — report
  first, restart when nothing is mid-task. `systemctl restart openclaw-gateway`.
- Persistent recurrence → raise the heap threshold or hunt the leak; do not
  keep restarting.

## Meta-rule (already in this skill's doctrine, reinforced)
Every sibling claim is a hypothesis with a timestamp. T₀ evidence is only
valid at T₀ (Dynamic-State). Re-probe at decision time — same day flipped
"DeepSeek dead" (-$0.07 morning) → "DeepSeek alive" ($16.66 evening).
