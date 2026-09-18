# MCP lane probe — tools missing while the organ looks healthy

Load when an agent has no tools from a configured MCP server, when a tool call returns
nothing, or when you must certify an MCP server as routable. The hiding place: an MCP
server is a **bridge** (stdio launcher or HTTP endpoint) in front of a **daemon**. A
healthy daemon proves nothing about the bridge, and a dead bridge surfaces to the agent as
silent absence — not as an error.

## 1. Census config, then the derived health file

Two artifacts that disagree more often than either is wrong:

| Artifact | What it is | Trap |
|---|---|---|
| `~/.hermes/config.yaml` → `mcp_servers` | DECLARED — the wiring | presence proves nothing about function |
| `~/.hermes/MCP_HEALTH.json` | derived census: `generated`, `counts`, per-server `status` / `routable` | it can lag config |

```bash
python3 -c "import yaml;c=yaml.safe_load(open('/root/.hermes/config.yaml'))['mcp_servers'];print(len(c),sorted(c))"
python3 -c "import json;d=json.load(open('/root/.hermes/MCP_HEALTH.json'));print(d['counts'],len(d['servers']))"
python3 -c "import yaml,json;c=yaml.safe_load(open('/root/.hermes/config.yaml'))['mcp_servers'];h=json.load(open('/root/.hermes/MCP_HEALTH.json'))['servers'];print('config-only:',sorted(set(c)-set(h)))"
```

- `status: stdio_present` = "the launcher exists", **not** "it works". Only `healthy` +
  `routable: true` is capability (C17: configured ≠ capable). Count the sets, never the rows.
- A server in config but absent from the census that handshakes fine on a manual probe =
  **monitor drift**. Probe it and report the drift; do not relay the census as the verdict.
- `enabled: false` is a decision, not a fault — report it separately from the dead ones.

## 2. stdio server: read the stderr log before touching anything

The gateway respawns a crashing stdio launcher continuously, so a one-line syntax error
becomes hundreds of identical failures a day and looks like "the tools just aren't there".

```bash
grep -c "starting MCP server '<name>'" ~/.hermes/logs/mcp-stderr.log   # large count = crash loop
tail -30 ~/.hermes/logs/mcp-stderr.log                                 # the real traceback
python3 -m py_compile <launcher.py> && echo COMPILE_OK                 # cheapest discriminator
grep -n '^<<<<<<< \|^=======$\|^>>>>>>> ' <launcher.py>                # conflict markers left in the tree
grep -rl '^<<<<<<< ' <repo> --include='*.py'                           # is it only this file?
```

A committed working tree can still hold conflict markers: `git show HEAD:<file> | grep -c '^<<<<<<<'`
returning 0 while the file on disk has them means the breakage is **uncommitted local state**,
which changes who may fix it (see §5). Note the file's mtime and `git log --oneline -3 -- <file>`
to tell a fresh break from one that has been failing for days.

## 3. Prove function with a real handshake, not a port check

`scripts/mcp_stdio_probe.py` does the JSON-RPC `initialize` → `tools/list` round trip against a
stdio launcher and prints the server name, version, and tool list:

```bash
python3 <skill>/scripts/mcp_stdio_probe.py -- python3 /path/to/server-mcp.py
python3 <skill>/scripts/mcp_stdio_probe.py --cmd '/opt/venv/bin/python' -- /path/to/server.py --transport stdio
```

Read the tool names, not just the count: a server that initializes and returns a shorter list
than the registry declares is partially wired. For HTTP servers, the equivalent is a POST
`initialize` with session-id capture — see the `mcp-testing` skill (Section 5: Era Mismatch) for the
version/session headers, since a 400 there is a protocol-era problem, not a dead lane.

## 4. Verify a fix by delta, not by "it compiles now"

A crash loop is a rate; prove the rate went to zero.

```bash
B=$(grep -c "starting MCP server '<name>'" ~/.hermes/logs/mcp-stderr.log); sleep 35
A=$(grep -c "starting MCP server '<name>'" ~/.hermes/logs/mcp-stderr.log); echo "delta=$((A-B))"
```

`delta=0` after the fix is the evidence. Also re-run §3's handshake and confirm the backing
daemon's own `/health` still answers — the bridge and the daemon are separate objects and both
need a verdict.

## 5. Repair authority: fix the tree, leave the commit

Repairing a broken launcher in the working tree is capability work — reversible, backed up,
and needed for the lane to exist at all. **Committing it is not yours** when the same file
carries another agent's uncommitted work or sibling sessions are live in the repo
(`ps aux | grep -E 'opencode|qwen|codex|claude'`, `git status -s`, `git diff --stat`).

Sequence: back up to `/tmp/<name>.bak-<stamp>` → make the minimal fix → show exactly what
changed (`diff <backup> <file>`, so the report can prove you deleted six marker lines and
nothing else) → verify with §3 and §4 → state in the report that the fix is uncommitted and
why.

Resolution rule for conflict markers: if one side is empty and the other is purely additive,
keep-both is safe and mechanical. If both sides carry logic, do not guess — that is a merge
decision belonging to whoever owns the branches.
