# arif_think LLM Wiring — provider cascade + FED/FLAME gap (2026-08-08)

> Traced from `/root/arifOS/arifosmcp/runtime/llm_client.py` + systemd drop-ins +
> live probes. Context for the blue-team DoS finding (35s SEA-LION timeout blocks
> the kernel HTTP thread) and Arif's question: *"Why don't we use FLAME or FED?"*

## Kernel boot env (systemd drop-in)

```
/etc/systemd/system/arifos.service.d/11-model-key.conf
Environment="ARIFOS_MODEL_KEY=kimi-code/k3"
```

`ARIFOS_MODEL_KEY` drives alignment_profile + adversarial_profile loading at
init (sovereign sessions), NOT the `arif_think` reasoning call itself.

## arif_think provider cascade (llm_client.py)

```
arif_think (mode=reason|verify|reflect|...)
  → llm_client.py cascade (circuit-breaker monitored, _cb_* helpers):
      1. tokenrouter          (federation gateway, if key configured)
      2. mimo / minimax       (openai-compatible remote)
      3. _call_sea_lion       ← PRIMARY reasoning backend
           model:   aisingapore/Qwen-SEA-LION-v4-32B-IT
           base:    https://api.sea-lion.ai/v1  (SEA_LION_BASE_URL)
           timeout: 35s  ← observed hang source
      4. ollama (local)       (localhost:11434, CPU — slow under memory pressure)
      5. deterministic HOLD   (no fabrication when all backends fail)
```

Provider health: `sea_lion: unconfigured|reachable|http_NNN|unreachable`,
`active_provider` selection at llm_client.py:2520.

## The FED/FLAME gap (Arif's question, answered 2026-08-08)

| Organ | Port | What it offers | Wired into kernel cascade? |
|---|---|---|---|
| **FED** | 7074 | `fed_route`/`fed_status`/`fed_probe`/`fed_contrast`/`fed_health` — model route advisor ("where to call"), ADVISORY_ONLY, never judges | ❌ NO — kernel never calls fed_route |
| **FLAME** | 18901 | RM0-TOOLS-FREELOOP inference mesh — **free** Groq models (`qwen3.6-27b`, `llama-3.3-70b-versatile`, `gpt-oss-120b/20b`, `llama-3.1-8b-instant` via `/v1/models`) | ❌ NO — kernel never calls FLAME |
| A-FORGE litellm | 4000 | federation model gateway for harness agents (Hermes/OpenClaw), `hermes-asi`/`agi-333`/`asi-555`/`apex-888` model_names | ❌ NO — separate harness layer, not kernel reasoning |

**Consequences:** every `arif_think` pays SEA-LION even when FLAME is free; the
DoS vector exists because the paid remote is the only real primary; FED — the
organ built to answer exactly "where should this reasoning call go" — is
bypassed.

**FLAME probe facts:** `GET :18901/v1/models` works (OpenAI-compatible listing);
`POST :18901/mcp` → `{"error": "Unknown action: mcp", "authority": "ADVISORY"}`
— **REST-only, no MCP surface** (same class as SIGNAL/FRAME).

## DoS chain (observed live 2026-08-08)

```
anonymous arif_think (prompt-injection payload)
  → SEA-LION slow/unreachable
  → 35s reasoning timeout blocks ONE kernel HTTP worker
  → /health + ALL /mcp requests queue behind it (shared thread pool)
  → whole :8088 surface dead 60s+ (4+ consecutive client timeouts observed)
  → auto-drain after timeout → /health recovers (NO restart needed)
```

Enablers: (1) LLM-bound call executes in-process on the shared HTTP worker
(no worker isolation / backpressure), (2) host memory pressure (swap 98% full,
cgroup ceiling 2G, Ollama CPU inference crawling) widens the window.

## Fix candidates (not yet applied — T1/T2 pending Arif's call)

1. **FED-first routing**: `arif_think` → `fed_route(need=reasoning, prefer=free)` → FLAME free tier happy path, SEA-LION fallback.
2. **Fail-fast anonymous band**: cap anonymous LLM-bound calls at ~5s (SABAR/HOLD beyond).
3. **Worker isolation**: move LLM calls to a bounded queue/worker thread so a slow backend can't block /health.
4. **Host memory headroom**: 2G cgroup ceiling on a 32G host is the real bottleneck behind the 35s crawl.
