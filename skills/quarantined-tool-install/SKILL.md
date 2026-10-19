---
name: quarantined-tool-install
id: quarantined-tool-install
version: 1.0.0
description: "Use when installing a third-party tool in quarantine."
owner: Hermes (arifOS federation)
risk_tier: medium
autonomy_tier: T2
floor_scope: [F1, F2, F4, F13]
tags: [supply-chain, quarantine, docker, mcp, sandbox, install, invariants]
---

# Quarantined Tool Install

> A tool that runs once in a throwaway container has been **demonstrated**, not **installed**.
> A tool that is installed is not yet a tool that is **exposed**. Three separate states — and
> collapsing them is how an unvetted binary ends up on the production surface.

## When to Use

- A third-party CLI, MCP server, or analysis tool must be evaluated before production use.
- A tool installs its own backends (decompilers, browser engines, drivers) — the install command
  is a supply-chain event, not a package fetch.
- You need to answer "what does this tool actually do on *this* host?", not on the vendor's
  supported-platform list.
- A new MCP server would add tools to a surface that already has a freeze or a size budget.
- Someone asks to "just install it and try" on a host that also runs production organs.

## When NOT to Use

- The tool is in a distro repo and you need it locally for one read-only query.
- The install is on a disposable machine with no production organ and no credentials present.
- The question is which model/provider to use — that is routing, not quarantine.

## The Three States

| State | Evidence required | Never say |
|---|---|---|
| `DEMONSTRATED` | one run happened, output seen | "installed" |
| `PERSISTED` | image on disk + runner script + receipt dir from a real run | "ready" |
| `EXPOSED` | a route key / registration grants it, surface cost measured | "live" |

Report which state you reached. A run with `--rm`, a one-shot `npx`, or a `/tmp` target leaves
nothing behind and **is not** `PERSISTED` — the most common over-claim in this class of work.

## Procedure

### 1. Resolve the real version before pinning

`latest` moves between the question and the answer. Query the registry, then pin:

```bash
npm view <pkg> version          # current latest
npm view <pkg> time --json      # publication date of the version you intend to pin
npm view <pkg> dist.integrity   # record this — it is the pin's identity
npm view <pkg> engines --json   # node/python floor
```

Pin the version you audited. **Never `npx -y <pkg>` / `pip install <pkg>` unpinned** in the
quarantine lane — an unpinned install re-resolves on every run and voids the hash you recorded.

### 2. Use the tool's own capability report, not its README

Most CLIs expose a self-check (`<tool> doctor`, `--version`, `--help`, a `capabilities` verb):

```bash
npx -y <pkg>@<pinned> <doctor-verb> --json
npx -y <pkg>@<pinned> --help          # the authoritative command list
```

**A README grep cannot prove a command does not exist.** Absence from the README means the
maintainer did not document it there. Run `--help` before declaring a verb missing — a whole
capability table has been written off on the strength of a grep.

Read the report for two things a platform table will not tell you:

- **which target families actually work on this host** — a tool strongest on one OS may be degraded
  on another. Declare unsupported families explicitly instead of letting silence imply parity.
- **which engine dependencies are missing**, and whether the tool would install them itself. An
  installer that fetches its own decompiler/backend is a second supply-chain event inside the first.

### 3. Build a non-root image with the pin baked in

```dockerfile
FROM node:<major>-alpine
RUN npm install -g <pkg>@<pinned-version> --silent
RUN addgroup -S app && adduser -S -G app app
USER app
WORKDIR /home/app
```

```bash
docker build -t <tool>-quarantine:<version> .
```

The install needs network. **Everything after it does not** — that is what makes `--network none`
meaningful instead of theatrical.

### 4. Prove the three containment invariants, every run

Write them into a runner script so each run re-proves them and writes the result to a receipt.
The proof must be produced *inside* the boundary, not asserted outside it.

```bash
#!/usr/bin/env bash
set -euo pipefail
IMAGE="<tool>-quarantine:<version>"
RUN_ID="${1:-$(date +%Y%m%d-%H%M%S)}"
TARGET="${2:-/path/to/read-only/target}"
RUN_DIR="/root/forge_work/<tool>/runs/${RUN_ID}"
OUT_DIR="${RUN_DIR}/out"
mkdir -p "${OUT_DIR}"
chown -R 100:101 "${OUT_DIR}"   # the container user's uid:gid — see pitfall below

docker run --rm --network none \
  -v "${TARGET}:/target:ro" \
  -v "${OUT_DIR}:/out" \
  "${IMAGE}" sh -c '
  {
    echo "=== (a) no egress ==="
    if timeout 6 wget -q -O- https://example.com 2>/dev/null; then echo "EGRESS_OK (FAIL)";
    else echo "EGRESS_BLOCKED (pass)"; fi

    echo "=== (b) read-only target ==="
    if echo x > /target/.write_probe 2>/dev/null; then echo "WRITE_OK (FAIL)";
    else echo "WRITE_BLOCKED (pass)"; fi

    echo "=== (c) writes confined ==="
    if echo x > /write_probe_root 2>/dev/null; then echo "ROOT_WRITE_OK (FAIL)";
    else echo "ROOT_WRITE_BLOCKED (pass)"; fi

    echo "=== real work, offline ==="
    <tool> <analysis-verb> /target --json > /out/analysis.json 2>&1
    echo "analysis.json bytes: $(wc -c < /out/analysis.json)"
  } 2>&1 | tee /out/receipt.txt
'
```

The last step is the point of the exercise: a containment proof with no real analysis in it proves
only that an empty container is isolated. Publish the artefact size and an evidence id so the claim
is falsifiable.

### 5. Measure the capability surface before proposing exposure

An MCP server's tool schema is context, not documentation. Count it in the unit you are budgeting:
speak MCP stdio directly — `initialize` → `notifications/initialized` → `tools/list` — then measure
the JSON you get back. Token estimate is `bytes / 4`; label it an estimate.

```javascript
// node measure-mcp-surface.mjs <command> [args...]
// spawn the server, send initialize(id=1), then tools/list(id=2);
// on the tools/list reply: print tools.length, JSON.stringify({tools}).length,
// and the same two numbers for a filtered subset you intend to expose.
```

Report full-surface vs subset **before** proposing a registration: a large server easily costs more
context than the task is worth, and hundreds of advertised tools routinely reduce to a dozen that
matter for one lane.

**A server that exposes everything and offers no partial mode must be scoped at your layer** — a
wrapper, a route key, or a proxy that publishes only the relevant names. Say plainly that the tool
has no native subset mode if it does not; do not imply one exists.

### 6. Stop at the gate

Prepare, do not execute, the production registration: the route key, the surface cost, the rollback
(stop container + remove key). Then stop and ask. Exposure is a different authority class from
inspection.

## Pitfalls

- ❌ **`docker run --rm` and calling it installed.** Nothing persists: no image check, no runner, no
  receipt dir. Re-runnable + artefacted is the bar.
- ❌ **A container writing to a host-mounted output dir as non-root.** The mount is owned by the host
  user; the container user (often uid 100) cannot write, and the run fails with `Permission denied`
  that reads like a tool defect. `chown -R <uid>:<gid>` the output dir first — read the container's
  real uid (`docker run --rm <image> id -u`), do not guess.
- ❌ **Reading `which <tool>` on the host as evidence about the container lane.** A quarantined tool is
  *supposed* to be absent from host `PATH`. That absence is correct, not a missing install — and its
  presence on the host is often the actual defect. State the namespace in every claim.
- ❌ **Concluding a CLI verb does not exist because the README omits it.** Run `--help`. The binary is
  the authority on its own command list.
- ❌ **Quoting a package entry count as a capability count.** One entry per deployment means a config
  of 146 entries can be 60 distinct names. Count distinct names, and count only the ones that resolve.
- ❌ **Folding the tool's backends into "one install".** A tool that fetches its own decompiler,
  browser engine, or JDK is a second supply-chain event. Decide it separately, and say which
  backends the lane is missing rather than letting a doctor report imply the whole capability is absent.
- ❌ **Asserting the host is unsupported from the container's distro.** An `alpine` base reports
  `unsupported_host` for tools that support the Debian/Ubuntu host fine. Probe the host's own
  `/etc/os-release` before writing a platform verdict.
- ❌ **Leaving an unpinned install in the runner.** `npx -y pkg` re-resolves every invocation and
  silently voids the pinned hash. The image bakes the pin; the runner only runs the image.
- ❌ **Testing a setting by reading it.** When a value clearly exists but the runtime ignores it, the
  key is usually defined twice and only one location is honoured — no parse error, no warning.
  Census the key everywhere it appears, then verify by **effect**: invoke the name and see if it
  resolves.

## Output Contract

One receipt, short. Per item: the pinned version + integrity hash, the host-platform verdict from the
**tool's own** doctor output, the three invariant results, the artefact size / evidence id from a real
run, the surface cost (tool count + token estimate), and the go/no-go with the authority class of the
next step. No narrative report, and no claim that the tool is "ready" unless all three states are
reached.
