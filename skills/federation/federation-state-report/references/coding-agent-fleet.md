# Coding-Agent Fleet — sources, probes, report shape

Companion to layer 5 of SKILL.md: how to answer "what coding agents do I have, and are they alive".
When a documentation file and a live probe disagree, the probe wins and the conflict gets REPORTED,
never silently resolved.

## Source map (read in this order)

| Source | Holds | Trust |
|---|---|---|
| `/run/arifos/mesh-health.json` | per-harness state, latency, doctrine `EXTERNAL != FAIL` | check `generated_at_utc` FIRST |
| `/root/AAA/scripts/mesh-health-probe.sh` | the marker probe that writes that SOT | re-run it when the SOT is stale |
| `/root/AAA/governance/GOTONG_ROYONG.md` | seat roster, lane, specialty, scheduled duty | lags; may carry stale seat numbers |
| `/root/AAA/registry/mcp-servers.yaml` | seat id ↔ harness ↔ MCP server list ↔ role | per-harness MCP truth |
| `/root/AAA/registry/canonical_agents.json` | canonical ids, aliases, authority bands | registration gate |
| `/root/AAA/a2a-server/agent-cards/harnesses/*.json` | per-harness cards | often lag reality |
| `/usr/local/bin/ccc-remote` | worker-host dispatch `case` list | ground truth for pool membership |
| each harness's own overlay doctrine file in its config home | model, MCP, hooks, autonomy tiers | harness-written, usually current |
| the scheduled-job table | which seats hold recurring duty | job comments usually name the seat |

Counts of skills per harness live under each config home; take them with `find -L`, never plain `find`.

## Worker host (the second box)

```bash
timeout 30 ssh -o ConnectTimeout=10 root@100.64.0.5 '\
  export NVM_DIR=/root/.nvm; . $NVM_DIR/nvm.sh >/dev/null 2>&1; \
  export PATH="$NVM_DIR/versions/node/v24.15.0/bin:$PATH"; \
  for c in codex opencode qwen; do echo "$c: $(command -v $c) $($c --version 2>/dev/null|head -1)"; done'
```

Without the nvm boot a non-login SSH cannot see the node CLIs, so they read as missing. Binary homes
there: node CLIs under `/root/.nvm/versions/node/<ver>/bin`, kimi/grok in `/usr/local/bin`, aider/agy in
`/root/.local/bin`. Batch every probe into ONE ssh call — per-command round-trips dominate the budget.

## Config facts per harness

Write a probe script to a file and execute it: an inline interpreter pipe is refused by the safety
scanner, and heredoc-to-python nesting mangles bracketed regexes. Print per harness: default model,
provider/route count, MCP server count, sub-agent count, permission mode, hooks count.

## Report shape (Arif)

- Lead with the live verdict line (PASS / EXTERNAL / FAIL counts) and say it was re-probed now, not read
  from the last SOT.
- One line per seat: `FI-00X Name — specialty · model/route · config · MCPs · skills`.
- Then harnesses that sit outside the marker probes — installed and configured, but name them as
  present-and-unprobed rather than dropping them.
- Then the worker host's pool with per-harness version drift.
- Close with the honest gaps as flags and ONE binary question. No raw matrices unless asked.

## Contradictions to surface

- One harness under two different seat numbers across docs (roster file vs MCP registry vs its own
  overlay) — report all of them.
- Role functions in the roster (clerk, pruner, on-demand helper) carried by an existing harness are
  roles, not extra seats.
- A worker-pool member whose config home is absent on that host is a half-migration — name the missing half.
