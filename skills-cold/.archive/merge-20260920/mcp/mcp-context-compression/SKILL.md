---
name: mcp-context-compression
description: "Use when MCP tool schemas are eating the context window, or when adding any new MCP server. Compress instead of dropping capability."
version: 1.0.0
owner: AAA
category: forge
tags: [mcp, context, tokens, harness, federation, compression]
floor_scope: [F2, F4, F7]
autonomy_tier: T1
capability_tier: fed-long-context
ecology_state: WARM
---

# MCP Context Compression — the ceiling that is not model IQ

## The measured problem (2026-09-16, this machine)

Tool *metadata* — not the agent's reasoning — is often the binding constraint on how
much real work fits in a session. Measured on our own servers:

| server | tools | schema tokens |
|---|---|---|
| aforge | 126 | **58,403** |
| geox | 31 | 12,721 |
| well | 31 | 5,356 |
| wealth | 11 | 4,034 |

With 24 servers wired, six figures of tokens are spent before the agent reads a single
user word. Fix this **before** buying a bigger model or installing another server.

## The fix: `mcp-compressor` (Atlassian Labs, open source)

Wraps an existing MCP server and collapses its toolset into a small
discover-then-invoke interface. Measured on aforge with our wrapper:

| level | tools exposed | schema tokens | reduction |
|---|---|---|---|
| raw | 126 | 58,403 | — |
| medium | 2 | 6,242 | **-89.3%** |
| high | 2 | 4,778 | -91.8% |
| max | 3 | 1,260 | **-97.8%** |

**Use `medium` by default.** It keeps tool descriptions, which is what tool-selection
accuracy depends on. `max` keeps names + params only — greatest saving, highest chance
of picking the wrong tool. Tighten only after measuring accuracy on real tasks.

## The federation wrapper (use this, not the raw binary)

```bash
# in ANY agent's MCP config, wrap a stdio server:
/root/scripts/mcp-compress.sh <name> -c medium -- <command> [args...]

# example (Hermes, live):
command: /root/scripts/mcp-compress.sh
args: [aforge, -c, medium, --, node, /root/A-FORGE/dist/src/interfaces/mcp/cli.js, serve, --transport, stdio]
```

For Hermes specifically, use the governed editor — it preserves the config's provenance
comments (a `yaml.safe_dump` round-trip silently deleted 10 comment lines; caught and reverted):

```bash
python3 /root/scripts/hermes_mcp_compress.py plan   <server> [level]   # dry run
python3 /root/scripts/hermes_mcp_compress.py apply  <server> [level]   # backup+write+verify
python3 /root/scripts/hermes_mcp_compress.py revert <server>
python3 /root/scripts/hermes_mcp_compress.py status
```

## The operating procedure after wrapping

1. **Discover, then invoke.** The wrapped server exposes `get_tool_schema` and
   `invoke_tool`. Call `get_tool_schema` for the tool you are about to use, then
   `invoke_tool`. That is one extra round-trip per *unfamiliar* tool — cheap against
   the ~52,000 tokens the wrap saves on every single request.
2. **Always prove one real call.** Listing tools is not evidence. Invoke a known-safe
   read tool end-to-end (e.g. `forge_health_check`) and read the payload before you
   report the wrap as working.
3. **Restart the consuming agent**, not just the MCP server: the config is read at
   session start.

## Limits — know these before promising compression everywhere

- **stdio only.** HTTP/URL backends fail: the compressor attempts an OAuth handshake
  and dies with `No *** support detected` (verified on geox/well). A URL server cannot
  be wrapped by this tool today — bridge it to stdio first if you need it.
- **Shell vs service difference.** A wrapper that works in your shell can fail under
  systemd: verify `HOME` and `PATH` are set in the unit, or yt-dlp-style config lookup
  silently degrades.
- **Not worth wrapping small servers.** Under ~15 tools the round-trip cost exceeds the
  saving.
- **`skills + CLI beats MCP`** for anything with a good local CLI — 17–32× cheaper on
  some benchmarks. Compress the MCPs you keep; don't add more to compress.

## Hard-won pitfalls

- An arg-parser that consumes the first non-flag token as "name" will swallow `-c` if
  flags come after it. Parse order-independently; see `mcp-compress.sh`.
- Never `yaml.safe_dump` a config that carries provenance comments. Edit text surgically.
- A wrapped server that *lists* tools can still fail on *invoke*. Test the invoke path.
- **An external HTTPS MCP URL breaks the federation wire script's preflight.**
  `hermes_mcp_wire.py` originally demanded an explicit `:port`, so every legitimate
  default-port server was rejected as `unparseable url`. Fixed to default 443/80 while
  keeping the fail-closed reachability probe. If the preflight refuses an external
  server, check the regex before suspecting the endpoint.
- **Load secrets in every entry point, not just `main()`.** The media-ingest MCP called
  the module's `ingest()` directly while `load_secrets()` lived only in the CLI path —
  so every keyed lane failed with an empty environment under the service while the same
  command worked in a shell. Same class as the missing-`HOME` systemd bug: the service
  is the real runtime, so prove the service path, not the shell path.

## Verifying a wrap is genuinely live (do all three)

1. **Process check** — the consuming agent must have spawned the wrapper:
   `MP=$(systemctl show <agent> -p MainPID --value); ps --ppid $MP -o cmd | grep mcp-compressor`
2. **Schema measurement** — wrapped vs unwrapped: tool count and `len(json.dumps(tools))//4`.
3. **Real invoke** — call one known-safe read tool through `invoke_tool` and read the
   payload. Listing tools is not evidence that the server works.

## Relationship to other skills

| This skill | Other skills |
|---|---|
| Keep context affordable | `FORGE-fastmcp` — build the servers |
| Federation-wide wiring | `hermes-mcp-drift-audit`, `federation-mcp-drift-audit` |
| Add a server correctly | `external-platform-mcp` |
