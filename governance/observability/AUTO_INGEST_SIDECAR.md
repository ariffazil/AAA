# arifFlow Auto-Ingest Sidecar — v1.0 Spec

> **Forged:** 2026-08-10 by 333-AGI under 888-APEX audit directive
> **Target organ:** A-FORGE (:7071) — execution shell wrapper
> **Binding:** All AAA agents. Zero cognitive tax on LLM.

## The Disease

```
Agent reasons → Agent executes tool → Agent completes task → Agent forgets to ingest
                                                              ↑
                                                    SILENT TELEMETRY GAP
```

arifFlow ingestion currently requires the LLM to explicitly call `arifflow_flow_ingest`. This is a **cognitive tax** — the model prioritizes task completion over accounting. Research (AgentTrace 2026, Oracle Reasoning Provenance 2026) establishes: **LLMs should never be trusted to record their own telemetry.**

## The Cure: Sidecar Interception

Move ingestion OUT of the agent's tool list. Wrap the execution transport layer:

```
                    ┌─────────────────────┐
Agent calls tool ──→│  SIDECAR WRAPPER    │──→ Tool executes
                    │                     │
                    │ 1. Record pre-exec  │
                    │ 2. Execute tool     │
                    │ 3. Record post-exec │
                    │ 4. Return result    │
                    │ 5. ASYNC: ingest    │
                    │    arifFlow receipt │
                    └─────────────────────┘
```

## Implementation: Transport Proxy

For OpenCode (current primary harness), the sidecar lives at the tool execution boundary:

```python
# forge_tool_sidecar.py — intercepts every tool call
# Lives in A-FORGE, hooks into forge_shell / forge_filesystem / etc.

class ToolExecutionSidecar:
    """Wraps tool execution. Auto-ingests into arifFlow. Agent never knows."""
    
    def __init__(self, arifflow_url="http://127.0.0.1:7073"):
        self.arifflow = arifflow_url
        self.buffer = []  # Batch ingest every N calls
    
    async def wrap(self, tool_name, actor_id, session_id, tool_fn, *args, **kwargs):
        span_id = str(uuid.uuid4())
        start = time.monotonic_ns()
        
        result = None
        error = None
        try:
            result = await tool_fn(*args, **kwargs)
        except Exception as e:
            error = str(e)
            raise
        finally:
            latency_ns = time.monotonic_ns() - start
            
            # ASYNC ingest — never blocks tool execution
            asyncio.create_task(self._ingest(
                actor_id=actor_id,
                session_id=session_id,
                tool_name=tool_name,
                step_type="Verify" if "verify" in tool_name.lower() else "Execute",
                latency_ns=latency_ns,
                error=error,
                span_id=span_id,
            ))
        
        return result
    
    async def _ingest(self, **payload):
        """Fire-and-forget to arifFlow. Failure logged, never propagated."""
        try:
            async with aiohttp.ClientSession() as s:
                await s.post(f"{self.arifflow}/ingest", json=payload, timeout=2)
        except Exception:
            pass  # Telemetry failure must never break execution
```

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **ASYNC ingest** | Telemetry must never add latency to tool execution |
| **Fire-and-forget** | If arifFlow is down, execution continues. Gap is logged. |
| **No cognitive tax** | Agent never knows the sidecar exists |
| **Transport layer** | Intercept at gateway/socket, not in tool definitions |
| **Batch buffer** | Buffer N calls, flush on 10 or 30s timeout |

## arifFlow API Contract

The sidecar POSTs to `:7073/ingest`:

```json
{
  "actor_id": "333-AGI",
  "session_id": "SEAL-915ca247a8de4988",
  "tool_name": "qwen-image-2.0-pro", 
  "step_type": "Execute",
  "epistemic_label": "Derivation",
  "floor_verdict": "Pass",
  "latency_ns": 8500000000,
  "error": null,
  "span_id": "uuid",
  "trace_id": "uuid (from carry-forward or generated)",
  "parent_span_id": "uuid (from active span stack)"
}
```

## Migration Path

| Phase | What | When |
|-------|------|------|
| **Phase 1** | OpenCode bash wrapper — intercept `bash` tool calls | Now |
| **Phase 2** | A-FORGE MCP server middleware — all forge_* tools | Next |
| **Phase 3** | Hermes gateway proxy — Telegram → agent handoff | Next |
| **Phase 4** | Universal transport proxy — all MCP servers | Future |

## Phase 1: Immediate (Bash Tool Wrapper)

Simplest implementation — wrap the bash execution in a logging shim:

```bash
# /root/AAA/scripts/forge-tool-sidecar.sh
# Source this in agent environment. Wraps bash with auto-ingest.
# Usage: forge-tool-sidecar.sh "tool_name" "command"

TOOL_NAME="$1"
COMMAND="$2"
SESSION_ID="${ARIF_SESSION_ID:-unknown}"
ACTOR_ID="${ARIF_ACTOR_ID:-unknown}"
START_NS=$(date +%s%N)

# Execute
eval "$COMMAND"
EXIT_CODE=$?

END_NS=$(date +%s%N)
LATENCY_NS=$((END_NS - START_NS))

# Async ingest (fire and forget)
curl -s -X POST http://127.0.0.1:7073/ingest \
  -H "Content-Type: application/json" \
  -d "{
    \"actor_id\": \"$ACTOR_ID\",
    \"session_id\": \"$SESSION_ID\",
    \"step_type\": \"Execute\",
    \"tool_name\": \"$TOOL_NAME\",
    \"latency_ns\": $LATENCY_NS,
    \"error\": $([ $EXIT_CODE -eq 0 ] && echo 'null' || echo '\"exit_code_$EXIT_CODE\"')
  }" &>/dev/null &

return $EXIT_CODE
```

---

*DITEMPA BUKAN DIBERI — telemetry is forged in transport, not in prompt.*
