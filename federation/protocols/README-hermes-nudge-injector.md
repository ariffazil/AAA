# hermes-nudge-injector.py

Event-driven context injection for AAA warga agents. Replaces fat static system
prompts with conditional nudges that only fire when their conditions match.

## Files

| File | Role |
|---|---|
| `hermes-nudge-injector.py` | Engine. Reads JSON from stdin, injects/transforms, writes JSON to stdout. |
| `hermes-nudges.yaml` | Default registry of nudges. Add rows; never edit the engine for new guidance. |
| `README-hermes-nudge-injector.md` | This file. |

## Hook points

- `pre_llm` — before the LLM sees the prompt. Appends a system nudge to messages.
- `pre_tool` — before a tool call. Appends a falsification reminder to the tool context.
- `post_llm` — before text reaches the human UI. Strips labels/receipts and collapses blank lines.

## Usage

```bash
# Pre-LLM intake gate
echo '{"event":"pre_llm","messages":[{"role":"user","content":"deploy the new api"}]}' | \
  python3 /root/AAA/federation/protocols/hermes-nudge-injector.py --event pre_llm

# Pre-tool falsification gate
echo '{"event":"pre_tool","tool_name":"forge_shell","tool_input":{"command":"rm -rf /root/foo"}}' | \
  python3 /root/AAA/federation/protocols/hermes-nudge-injector.py --event pre_tool

# Post-LLM collapse gate
echo '{"event":"post_llm","text":"[OBS] I saw X.\n\n[🦾ACT] Done."}' | \
  python3 /root/AAA/federation/protocols/hermes-nudge-injector.py --event post_llm
```

## Adding a nudge

Edit `hermes-nudges.yaml` and append a row under `nudges`:

```yaml
- id: my-nudge
  event: pre_llm
  priority: 20
  condition:
    any_keyword: ["kubernetes", "k8s"]
  inject_position: last
  text: |
    <NUDGE_K8S>
    Validate namespace and context before any kubectl mutation.
    </NUDGE_K8S>
```

A bad nudge cannot crash the engine: each nudge is evaluated in isolation and
errors are logged to `/root/.local/share/arifos/hermes_nudge_injector.jsonl`.

## Condition reference

Conditions are AND-combined (all must pass) except `any_of`, which is an OR of
sub-conditions.

| Key | Type | Match rule |
|---|---|---|
| `always` | bool | Always match if `true` |
| `any_keyword` | list | Any keyword appears in the haystack |
| `all_keywords` | list | All keywords appear in the haystack |
| `regex` | str | `re.search` against the haystack |
| `tool_name` | str \| list | Exact tool name match |
| `message_count_min` | int | Minimum number of messages |
| `message_count_max` | int | Maximum number of messages |
| `any_of` | list of conditions | OR-combinator of sub-conditions |

Example combining OR + AND:

```yaml
condition:
  any_of:
    - tool_name: ["forge_shell", "bash"]
    - any_keyword: ["rm", "delete", "drop"]
```

This matches any `forge_shell`/`bash` call OR any haystack containing `rm`,
`delete`, or `drop`.

## Design decisions

1. **Physical vs psychological separation** — The hard-stop gate lives in
   `arifos-hermes-gate-hook.py` (Exit Code 2). This injector is soft guidance
   only; it never blocks execution.
2. **Fail-closed** — Any fatal error returns the original input unchanged and
   exits 0 so the caller is never blocked.
3. **Token economy** — A nudge only costs tokens when its condition matches.
   A clear prompt pays near-zero nudge cost.

## Wiring into Hermes / OpenCode

The engine is transport-agnostic. To wire it:

- **OpenCode**: wrap `hermes-nudge-injector.py` in a plugin hook at the
  `pre-llm`, `pre-tool`, and `post-llm` lifecycle points.
- **Hermes CLI**: add a shell hook that pipes the prompt/context through the
  engine before handing it to the LLM backend.
- **arifOS kernel**: call it from the MCP transport layer as a
  `CanonicalEnvelope` preprocessor.

See [`hermes-nudge-wiring.md`](hermes-nudge-wiring.md) for concrete shell
wrapper and OpenCode plugin sketches.

DITEMPA BUKAN DIBERI.
