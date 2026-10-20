---
name: third-party-tool-quarantine
version: 1.0.0
description: Use when adopting an untrusted third-party tool.
owner: HERMES
risk_tier: medium
autonomy_tier: T2
floor_scope: [F1, F2, F4, F9, F13]
tags: [quarantine, mcp, supply-chain, docker, tool-adoption, sandbox]
---

# Third-Party Tool Quarantine

> A tool you have not exercised is a **claim**, not a capability. The deliverable is a durable
> boundary plus measured invariants — not a report that the tool works.

## When to use

- The sovereign forwards a tool, repo, ad, or vendor pitch and asks whether to install it.
- You are about to add an MCP server or CLI to any agent's callable surface.
- A tool advertises N tools and you need to know what that does to context before exposing it.

## Core rules

1. **Quarantine first, expose never-until-proven.** Nothing enters a production MCP surface on the
   strength of a README. Install into a dedicated container, prove the boundary, and leave
   registration to the sovereign.
2. **Durable over throwaway.** A `docker run --rm` proves a moment; it leaves no state and cannot be
   re-inspected. Ship an image + a re-runnable script + a per-run output directory. If the proof
   disappears when the command ends, you have a demo, not a capability.
3. **State the state, not the intent.** `image built`, `container ran`, `tool installed`, `registered`,
   `exposed` are five different states. Name the one you actually reached.
4. **Measure the surface, do not estimate it.** Tool schemas are the real cost of adoption.

## Procedure

### 1. Verify the artifact before it runs

```bash
npm view <pkg> version dist.integrity dist.tarball   # pin exact version + record the hash
```

Pin an exact version. Never `npx -y <pkg>` (unpinned latest) in any lane you intend to keep. Record
`dist.integrity` in the receipt — an unpinned install is unreproducible by construction.

Run the tool's own doctor **inside** the target container, not on the host, so the answer describes
the runtime you will actually use:

```bash
docker run --rm node:<ver>-alpine sh -c "npm i -g <pkg>@<version> && <tool> doctor --json"
```

### 2. Build a durable quarantine image

Non-root user, pinned version baked in, no target data in the image:

```dockerfile
FROM node:<ver>-alpine
RUN npm install -g <pkg>@<version>
RUN addgroup -S q && adduser -S -G q q
USER q
WORKDIR /home/q
```

**Install needs network; execution must not.** Do the install in the build layer, then cut the network
for every run (`--network none`). A container that still reaches the internet after setup is not
quarantined.

### 3. Prove the three invariants in the same run that does the work

The invariants are only real if asserted *by the container itself* and written to a receipt:

| # | Invariant | Assertion |
|---|---|---|
| a | no egress | an outbound fetch inside the container fails |
| b | target read-only | a write into the mounted target fails |
| c | writes confined | output lands in the run dir; a write outside it fails |

Make the runner (`run.sh <run_id>`) do all three plus the real work, `tee` the result to
`<run_dir>/out/receipt.txt`, and keep the artifacts. A run that only prints `pass` proves nothing
six hours later.

Ownership gotcha: a non-root container user cannot write a root-owned bind mount. `chown` the output
directory to the container uid/gid before the run (`id -u` / `id -g` inside the image), or invariant
(c) fails for a permission reason and looks like a broken tool.

### 4. Measure what exposing the tool actually costs

Speak MCP to the server and measure the real `tools/list` payload — never estimate from a README:

```python
# initialize -> notifications/initialized -> tools/list, then:
# full_schema_chars = len(json.dumps({"tools": tools}))
# tokens_est        = chars / 4
# subset            = tools whose name+description match the lane you want, minus other families
```

Report **both** numbers: the full surface and the lane-scoped subset. A tool that advertises "50
capabilities" may enumerate 3x that, and the difference decides whether exposing it is even possible.

Before assuming a server supports a partial toolset, check for it: `tools/list` returning every tool
with no scope flag means **scoping must be done in the calling layer** (route key, wrapper proxy,
allowlist), not inside the tool. Say which layer will enforce it.

### 5. Report

One receipt: pinned version + hash, doctor output, the three invariants with the command that
asserted each, the measured token cost (full + scoped), what is still NOT done (registration,
exposure), and the single decision that remains with the sovereign.

## Pitfalls

- ❌ **Reporting "verified / PASS" for a proof you ran with `--rm`.** Throwaway runs leave no image,
  no output, no script and no container to re-inspect, so the next session cannot confirm the claim and
  the honest reading of your report is fabrication. Build the image, ship the runner, keep the run dir.
- ❌ **Proving a boundary, then extending the claim to "installed".** A tool inside a container is not a
  tool on PATH, not an MCP registration, and not a callable capability. Enumerate the states you did
  reach and stop at the last one you actually reached.
- ❌ **`--network none` on the install step.** The package will not download and you will misread it as
  a broken package. Install at build time; cut the network at run time.
- ❌ **Believing a vendor's capability claim for your host.** "Works for native apps" may be true only on
  a different OS. Run the tool's own doctor inside the container and publish the per-family table; declare
  the unsupported families explicitly instead of implying uniform coverage.
- ❌ **Adding a large MCP surface to an agent under a capability freeze.** Count the tools already
  registered and the ones you would add; a 170-tool server changes the arithmetic. Propose, do not register.
- ❌ **Treating a tool's own exit code as a pass/fail verdict for your invariant.** `doctor` exiting
  non-zero often means "environment not healthy", not "my write failed". Assert the invariant with the
  filesystem or network operation itself, and read the tool's exit code separately.
- ❌ **Skipping the "what it cannot do" section.** Most pitched tools analyse one layer (front end, binary,
  docs) and cannot reproduce a backend/auth/third-party API. State the ceiling in the same breath as the
  capability, or the sovereign plans work the tool cannot deliver.
