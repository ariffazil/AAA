# Cross-Node Remote Read Probe (READ-ONLY)

> **Scope:** When local filesystem appears empty for an artifact you suspect lives on another federation node (KVM2, KVM4, KVM8, or beyond), how to **read** it remotely without transferring or mutating. The companion skill `cross-node-artifact-transfer` owns MOVE/WRITE; this reference owns READ.
> **Lane:** OBSERVE — no state mutation, no transfer receipt needed.

## When to use

- The agent is running on node A and an artifact referenced by Arif (a folder, a person-card, a helix strand, a benchmark output) is reported to exist on node B.
- Local search returns zero or partial hits, and the user expects a complete read.
- The user is asking "kita pernah ada X" and X is data, not a stateful service.

## Procedure

### 1. Identify the lane to the peer node

Three viable lanes, in order of preference:

1. **A-FORGE MCP `forge_filesystem`** — the canonical federation read path. Works across nodes via MCP wiring; supports `list_directory`, `read_file`, `grep_search`. Auth via MCP server's bearer, scoped to OBSERVE.
2. **ssh + filesystem** — `ssh <peer> "ls -la <path>"` etc. Direct, but bypasses the federation's audit lane. Acceptable for read-only when MCP is unavailable.
3. **Shared mount / symlinked tree** — only if both nodes resolve the same path. Zero transport, but rare in arifOS topology.

Always state which lane you used and why.

### 2. Probe, don't trust the local cache

A local-filesystem miss is **evidence of local absence, not federation absence.** Before reporting "not found":

- Run a wide search locally first: `search_files` with content + filename modes, covering hidden dirs (`.hermes/`, `.qwen/`, `.git/objects/`), quarantine (`forge_work/_quarantine/`), and dated session exports.
- If empty, **probe the federation** via A-FORGE MCP before claiming VOID. Cross-node artifacts are normal: WawaBot on KVM2 (`azwaos`, 100.64.0.4) routinely reads person-cards and helix strands that live on KVM4/KVM8 forge nodes.

### 3. Read-only contract

Remote probe is strictly READ. Never:

- Write, append, or `mkdir` on the peer.
- Run state-changing scripts (`arif_seal`, registry updates, lane mutations).
- Persist probe results back into the peer's filesystem.

If the artifact needs editing, route through the proper write path (`cross-node-artifact-transfer` or musyawarah-gotong), not this probe.

### 4. Receipt shape (light)

Unlike a transfer, a remote read does not require a four-field attestation. The receipt is:

```
REMOTE_READ  <artifact path>  from  host=<peer-hostname>
             lane=<mcp|ssh|mount>  bytes=<n>  lines=<n>
             probe_ts=<ISO>  observer=<actor>
```

State the lane and the timestamp; the file content itself is the evidence.

## Pitfalls

- **A local miss is not a federation miss.** The single most common error is concluding "the file does not exist" after one local `search_files` returned zero. Federation probes routinely surface artifacts on KVM2, KVM4, or KVM8 that the running node cannot see directly. Run a wide local sweep + cross-node probe before declaring absence.
- **Do not invoke peer write paths to "check" the file.** A `read_file` that accidentally hits a write endpoint is the federation's most expensive mistake. Restrict to MCP `read_*` / `list_*` verbs, or to ssh with explicit `cat`/`head`/`ls` — never anything that mutates.
- **Do not bridge a remote probe result into the peer's filesystem as a "side effect".** If you need to persist the read result, write to your own node's scratch (`/root/.hermes/cache/scratch/`), not the peer's tree.
- **Probe result is a snapshot, not a subscription.** Federation state mutates. If the artifact matters over time, re-probe on each access; don't pin a once-read value as "the truth".
- **Authenticate the lane, not just the path.** MCP `forge_filesystem` reads require the federation's bearer; ssh requires the peer's key. An unauthenticated read that succeeds is a misconfiguration, not a feature — report it.
- **Don't use this lane for hot files that change faster than the probe.** Read-only probes are atomic snapshots; for stateful services use the proper health/witness lane (`frame_probe`, `well_*`).

## Worked shape

```
# Example: KVM2 (WawaBot) probing KVM4 (forge) for an Azwa-related artifact
lane:  A-FORGE MCP forge_filesystem (OBSERVE)
host:  forge (100.64.0.5)
path:  /root/memory/people/FAMILY/azwa-fazil.md
probe_ts: 2026-09-26T13:15:00+08:00
result: 122 lines, last update 2026-09-26
action:  read-only, no state mutation, no transfer receipt
```

DITEMPA BUKAN DIBERI ⚒️