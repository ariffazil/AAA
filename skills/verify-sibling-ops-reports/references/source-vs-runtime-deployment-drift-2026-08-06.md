# Source vs Runtime Deployment Drift — false-positive "never deployed" claims (2026-08-06)

## Context

A sibling (3rd-party audit) pasted a WEALTH MCP ops report claiming:

> "4 WEALTH fixes committed to source (b60cdae, d6ba4a6, dce2670, a136245) but never deployed to runtime. Service needs restart to pick up the fix."
> "Ferrari is in the pit lane — one restart away."

On probe: **both claims wrong**. Service was already restarted 18 seconds before my probe. Source IS runtime via `PYTHONPATH`.

## The deployment-model matrix on this box

Sibling reports often assume one deployment model (source→/opt rsync + systemd restart). On this box, **different organs use different deployment models**:

| Organ | Runtime path | Deployment model | What "never deployed" means |
|---|---|---|---|
| arifOS | `/opt/arifos/app/` | `rsync source → /opt/arifos/app/`, `systemctl restart arifos` | Real — source commits ≠ runtime without deploy step |
| A-FORGE | `/opt/a-forge/app/` | `rsync source → /opt/a-forge/app/`, `systemctl restart a-forge` | Real — same as arifOS |
| WEALTH | `PYTHONPATH=/root/WEALTH` | Source IS runtime. No rsync. No deploy step. | **Source = runtime. Every commit is live.** |
| GEOX | `PYTHONPATH=/root/GEOX/src` | Source IS runtime. No rsync. No deploy step. | **Source = runtime. Every commit is live.** |
| AAA | process in `/root/AAA` | Source IS runtime (no separate /opt/AAA) | Source = runtime. |

The sibling treated WEALTH like arifOS — assumed a rsync+restart gap. There isn't one.

## Verification recipe — the 30-second deployment-drift probe

```bash
# 1. Find what the running process loads (PYTHONPATH or ExecStart)
PID=$(pgrep -f 'server_federated.py' | head -1)
cat /proc/$PID/environ 2>/dev/null | tr '\0' '\n' | grep -E 'PYTHONPATH|^HOME'

# 2. Compare source vs /opt/ mtimes
stat -c '%y %n' /root/WEALTH/wealth_contracts/envelope.py \
              /opt/wealth/app/wealth_contracts/envelope.py 2>/dev/null

# 3. Check systemd unit for ExecStart path
systemctl show wealth-organ.service -p ExecStart -p MainPID -p ActiveEnterTimestamp
```

**Interpretation:**

| Result | Verdict |
|---|---|
| `PYTHONPATH=/root/<organ>` (source dir) | **Source = runtime.** No deploy gap. Source mtime newer than /opt/ = irrelevant (process doesn't load /opt/). |
| `ExecStart=/root/<organ>/.venv/bin/python3 ...` | Same as above. |
| `ExecStart=/opt/<organ>/app/...` (arifOS / A-FORGE) | **Real deploy gap.** Source commits ≠ runtime without rsync+restart. |
| Source mtime > /opt/ mtime AND PYTHONPATH=/opt/... | Source has uncommitted edits; runtime is stale. Restart required. |

## Stale "needs restart" in same-turn reports

A sibling may restart a service, then paste a report claiming "needs restart to pick up the fix." The report reflects **pre-restart state**. Always cross-check:

```bash
# When did the service actually start?
systemctl show <unit> -p ActiveEnterTimestamp
# vs the report's timestamp (sent_at field, or git log time of the report file)
```

If `ActiveEnterTimestamp` is more recent than the report's claim-time, the restart already happened. Don't restart again.

## "Committed but never deployed" — the false-positive pattern

A sibling report will often say "fixes X, Y, Z committed but never deployed." Three possibilities:

1. **Source = runtime organ** (WEALTH, GEOX) → claim is FALSE. Commits are live.
2. **rsync+restart organ** (arifOS, A-FORGE) AND unit active with old `MainPID` → claim is TRUE.
3. **rsync+restart organ** AND unit was just restarted → claim was TRUE pre-restart, FALSE post-restart. Re-verify against the post-restart process.

**Always probe PYTHONPATH before accepting "never deployed" claims.**

## Migration-map fabrication pattern (related)

In the same session, the same sibling pasted a `/vitals → /propa` migration map with **5 fabricated file/line refs**:

| Ref claim | Live reality |
|---|---|
| `trinity-nav.js L109` emits `/vitals/` | **No such file.** Real nav lives in `src/data/navCanon.ts` L72-73 |
| `tokens.css L65-66` has `.fam-vitals-*` classes | **Zero matches in any CSS file** under `public/` or `src/` |
| `dist/vitals/` has "3 files + 1 .bak" | **2 files only** — `index.html` + `index.html.v1.1.bak` |

**Detection:** before trusting any migration map's auto-execute scope, run a 30-second grep on each cited file/line. If 1+ ref doesn't survive grep, the entire map was generated from prose intent, not filesystem reality. Re-scope or reject.

## The MCP tools/list false-negative trap (related pitfall)

When probing an MCP server's tool surface:

```bash
# WRONG — Streamable-HTTP transport needs an initialize handshake first
curl -s -X POST http://127.0.0.1:18082/mcp -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
# Returns session-id-required error or empty tools array
```

```bash
# RIGHT — initialize first, capture mcp-session-id, then tools/list
SESSION=$(curl -s -X POST http://127.0.0.1:18082/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"probe","version":"1"}}}' \
  -i | grep -i 'mcp-session-id' | tr -d '\r' | awk '{print $2}')

curl -s -X POST http://127.0.0.1:18082/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H "mcp-session-id: $SESSION" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
```

Without the session-id, every tool in the list appears "MISSING" — a false negative that has caused at least 3 sibling reports to misdiagnose healthy MCP servers as broken. Always probe with initialize-first when checking whether an MCP organ's tools are loaded.

## Reusable probe set

The 30-second "is the sibling report's failure-mode real?" kit:

```bash
# 1. Is the service alive?
systemctl is-active <unit>; curl -sf http://127.0.0.1:<port>/health

# 2. Is source = runtime?
cat /proc/<pid>/environ | tr '\0' '\n' | grep PYTHONPATH

# 3. Are the cited files real?
for f in <cited-file-paths>; do ls -la "$f" 2>&1; done

# 4. Are the cited line numbers real?
sed -n '<line>p' <file>  # should match the cited claim

# 5. Does the MCP server actually have the cited tools?
SESSION=$(curl -s -X POST .../mcp -d '{initialize}' -i | grep mcp-session-id | awk '{print $2}')
curl -s ... -H "mcp-session-id: $SESSION" -d '{tools/list}' | jq '.result.tools[].name'
```

5 commands. Each takes 1-3 seconds. Total: ~30 seconds. Catches every false positive in this reference.
