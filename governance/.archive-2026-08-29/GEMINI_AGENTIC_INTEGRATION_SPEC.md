# AAA Gemini Agentic Integration & Dual-Provider Architecture

> **Document ID:** AAA-SPEC-GEMINI-2026-V1  
> **Status:** APPROVED (F13 SOVEREIGN)  
> **Forged:** 2026-08-10 by 333-AGI + F13 SOVEREIGN  
> **Location:** `/root/AAA/governance/GEMINI_AGENTIC_INTEGRATION_SPEC.md`  
> **Target Runtimes:** Hermes Agent, OpenCode, OpenClaw, A2A Proxy

---

## 1. Dual-Provider Routing Paradigm (FED Router)

Runtime AAA melarang persaingan terus pada satu endpoint. FED Routing Layer menguruskan dua provider secara serentak mengikut *Capability Signature*:

```
                     ┌────────────────────────────────────────┐
                     │          FED ROUTING LAYER (:7074)     │
                     └───────────────────┬────────────────────┘
                                         │
                   ┌─────────────────────┴─────────────────────┐
                   ▼                                           ▼
      [Capability: Deep Reasoning]              [Capability: Multimodal / Search]
         QWEN_API_KEY Provider                     GEMINI_API_KEY Provider
    • Base: Qwen Token Plan Gateway            • Base: https://generativelanguage.googleapis.com/v1beta/openai/
    • Models: deepseek-v4-pro, qwen3.7-max     • Models: gemini-3.1-pro, gemini-3.6-flash, gemini-3.5-flash-lite
    • Use: coding, analysis, reasoning         • Use: image/video gen, search, long-context, multimodal
```

**Capability Signature Routing Rules:**

| Task Type | Route To | Models | Why |
|---|---|---|---|
| Deep reasoning / coding | Qwen Token Plan | deepseek-v4-pro, qwen3.7-max | Strongest code/reasoning |
| Image generation | Gemini | gemini-3-pro-image, image-01 | Native multimodal |
| Video generation | Gemini | veo-3.1-generate-preview | Only video-capable |
| Web search + reasoning | Gemini | gemini-3.6-flash + googleSearch | Native search tool |
| Long context (>100K) | Gemini | gemini-3.1-pro (1M ctx) | Largest context window |
| Fast sub-agent tasks | Gemini | gemini-3.5-flash-lite | Cheapest, fastest |
| A2A handoffs | Both | Per capability | FED decides |

---

## 2. Runtime Integration Matrices

### P0: Hermes Agent (Dual-Route Toggle)

Add `HERMES_BACKEND` env toggle to launcher without breaking existing Qwen routing.

```bash
# Toggle Routing Protocol — add to Hermes launcher or systemd env
if [ "$HERMES_BACKEND" = "gemini" ]; then
    export OPENAI_API_KEY="$GEMINI_API_KEY"
    export OPENAI_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
    export DEFAULT_MODEL="gemini-3.6-flash"
else
    # Default: Qwen Token Plan
    export OPENAI_API_KEY="$QWEN_API_KEY"
    export OPENAI_BASE_URL="$QWEN_TOKEN_PLAN_BASE"
    export DEFAULT_MODEL="deepseek-v4-pro"
fi
```

### P1: OpenCode Provider Config (~/.opencode/config.json)

Two explicit providers — agent picks per task.

```json
{
  "providers": {
    "qwen_primary": {
      "type": "openai_compatible",
      "baseUrl": "${QWEN_TOKEN_PLAN_BASE}",
      "apiKey": "${QWEN_API_KEY}",
      "models": { "coder": "qwen3.7-max" }
    },
    "google_gemini": {
      "type": "openai_compatible",
      "baseUrl": "https://generativelanguage.googleapis.com/v1beta/openai/",
      "apiKey": "${GEMINI_API_KEY}",
      "models": {
        "coder": "gemini-3.1-pro",
        "fast_runner": "gemini-3.5-flash-lite"
      }
    }
  }
}
```

### P2: OpenClaw YAML Routing

```yaml
providers:
  gemini_agentic:
    api_key_env: GEMINI_API_KEY
    endpoint: "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
    parameters:
      extra_body:
        google:
          thinking_config:
            thinking_level: "high"
            include_thoughts: true
```

### P3: A2A Trace Propagation

- Header invariant: Every A2A message through Gemini includes `arif_trace_id` + `span_id` in payload metadata
- Schema enforcement: `response_format: {"type": "json_object"}` for deterministic handoffs

### P4: Context Caching

- OpenCode tasks >200K tokens use Gemini Context Caching API
- Register reusable codebases for multi-turn debugging

---

## 3. Advanced Gemini Features

| Feature | Gemini Param | OpenAI Gateway Field | Description |
|---|---|---|---|
| Thinking Mode | `thinking_config.thinking_level` | `reasoning_effort` | "low" / "medium" / "high" |
| Thought Summary | `include_thoughts: true` | `extra_body.google.thinking_config.include_thoughts` | Returns reasoning chain |
| Native Web Search | `tools: [{"googleSearch": {}}]` | `extra_body.tools` | Real-time web search |
| Code Execution | `tools: [{"codeExecution": {}}]` | `extra_body.tools` | Sandboxed Python runtime |
| Image Generation | `gemini-3-pro-image` | Direct API | Native multimodal |
| Video Generation | `veo-3.1-generate-preview` | `predictLongRunning` | 8s video + native audio |

---

## 4. Governance Invariants

1. **Self-Attestation Ban:** No agent may log own Gemini usage. Sidecar proxy intercepts all calls automatically. (See: `/root/AAA/governance/observability/SIGNAL_CHAIN_ART_ACT_AUTH.md`)
2. **Null-Root Provenance:** If Gemini response lacks thinking_config trace, sidecar injects UNKNOWN state into apex_block for FQ formula integrity.
3. **Fail-Closed Function Calling:** Gemini tool invocations executed by sidecar, verified, re-injected with trace headers.
4. **Cost Attribution:** Each Gemini call tagged with `arif_trace_id` for per-task cost tracking.

---

## 5. Implementation Checklist

- [ ] P0: Hermes `HERMES_BACKEND=gemini` toggle
- [ ] P1: OpenCode dual-provider config
- [ ] P2: OpenClaw YAML routing with thinking_config
- [ ] P3: A2A trace propagation (arif_trace_id + span_id)
- [ ] P4: Context caching for long repos
- [ ] P5: Sidecar integration for usage logging
- [ ] P6: FED routing rules for capability-based provider selection

---

*DITEMPA BUKAN DIBERI — Dual-provider architecture forged 2026-08-10. No single point of failure. FED routes by capability, not by default.*
