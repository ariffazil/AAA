# Hermes Nudge Injector — Wiring Examples

Event-driven integration patterns for AAA warga agents.

## Design Constraint

The injector is **transport-agnostic**. It reads JSON from stdin and writes JSON
to stdout. A caller MUST wrap it at three lifecycle points:

- `pre_llm` — before the LLM sees the prompt.
- `pre_tool` — before a tool call is executed.
- `post_llm` — before text reaches the human UI.

The injector never blocks execution. On fatal error it exits 0 and echoes the
original input unchanged (fail-closed passthrough).

## Pattern A — Shell wrapper for any CLI agent

```bash
#!/usr/bin/env bash
# /root/.arifos/agents/shared/hermes-nudge-wrap.sh
set -euo pipefail

ENGINE="/root/AAA/federation/protocols/hermes-nudge-injector.py"
EVENT="$1"           # pre_llm | pre_tool | post_llm
shift

# Read the payload that the CLI would have sent to the LLM/tool/UI.
PAYLOAD=$(cat)

# Pipe through the injector and forward the transformed payload.
echo "$PAYLOAD" | python3 "$ENGINE" --event "$EVENT" "$@"
```

Usage inside an agent launch script:

```bash
# pre_llm
USER_PROMPT_JSON=$(jq -n '{event:"pre_llm",messages:[{role:"user",content:$msg}]}' --arg msg "$*")
ENRICHED=$(echo "$USER_PROMPT_JSON" | /root/.arifos/agents/shared/hermes-nudge-wrap.sh pre_llm)
# Feed ENRICHED.messages to the LLM backend.
```

## Pattern B — OpenCode plugin sketch

OpenCode plugins receive lifecycle hooks. A minimal pre-LLM hook:

```typescript
// ~/.config/opencode/plugins/hermes-nudge-injector.ts
import { spawn } from "child_process";
import { Readable } from "stream";

const ENGINE = "/root/AAA/federation/protocols/hermes-nudge-injector.py";

async function inject(event: "pre_llm" | "pre_tool" | "post_llm", payload: any): Promise<any> {
  return new Promise((resolve, reject) => {
    const proc = spawn("python3", [ENGINE, "--event", event]);
    let stdout = "";
    let stderr = "";
    proc.stdout.on("data", (d) => (stdout += d));
    proc.stderr.on("data", (d) => (stderr += d));
    proc.on("close", (code) => {
      if (code !== 0) {
        // Fail-closed: return original payload on error.
        return resolve(payload);
      }
      try {
        resolve(JSON.parse(stdout));
      } catch {
        resolve(payload);
      }
    });
    Readable.from([JSON.stringify(payload)]).pipe(proc.stdin);
  });
}

export async function onPreLLM(messages: any[]) {
  const result = await inject("pre_llm", { event: "pre_llm", messages });
  return result.payload?.messages ?? messages;
}

export async function onPreTool(toolName: string, toolInput: any) {
  const result = await inject("pre_tool", { event: "pre_tool", tool_name: toolName, tool_input: toolInput });
  // The result contains `nudge_injection` which can be appended to the tool intent context.
  return result.payload ?? { tool_name: toolName, tool_input: toolInput };
}

export async function onPostLLM(text: string) {
  const result = await inject("post_llm", { event: "post_llm", text });
  return result.payload?.text ?? text;
}
```

## Pattern C — Hermes CLI middleware

If Hermes CLI supports a prompt preprocessor, configure it to pipe through the
injector before the LLM call. The exact integration depends on the CLI's
middleware contract; the shell wrapper above is the safest universal pattern.

## Fail-closed contract

| Scenario | Exit code | Output |
|---|---|---|
| Success | 0 | Transformed JSON payload |
| Invalid JSON input | 0 | Original raw input echoed |
| Unknown event | 0 | Original raw input echoed |
| Registry missing | 0 | Input echoed, 0 nudges loaded |
| Engine crash | 0 | Original raw input echoed |

DITEMPA BUKAN DIBERI.
