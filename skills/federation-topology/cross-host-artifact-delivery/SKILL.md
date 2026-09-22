---
name: cross-host-artifact-delivery
version: 1.0.0
description: "Use when moving a file between federation hosts."
owner: Hermes (arifOS federation)
risk_tier: low
autonomy_tier: T1
floor_scope: [F2, F4, F11]
tags: [federation, multi-host, transfer, verification, provenance, hash]
triggers:
  - "send this file to"
  - "put it on the other node"
  - "it should be on KVM"
  - "mirror this to"
  - "the peer says the file isn't there"
  - "sync these artifacts"
  - "cross-host"
  - "scp"
  - "rsync"
  - "already on disk"
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Cross-Host Artifact Delivery

Moving one artifact between two federation hosts, and proving it landed. The failure mode this skill
exists to prevent is not a failed transfer — it is a *successful* transfer to the wrong machine,
confirmed by the sender, reported as done.

Scope: the transfer and its verification. Machine identity, naming collisions, and the host table live
in `federation-machine-verification` (user-owned); read that first if you are unsure which host is
which.

## The Core Law

> **A transfer receipt proves a transfer happened. It does not prove where.**

`scp` exit 0, `rsync` exit 0, and a matching `sha256sum` are all *content* statements. None of them is
a *location* statement. The sender's SSH session is the only instrument you have for the transfer — so
when its target alias is wrong, the instrument and the object of verification are wrong together, and
every retry reproduces the same false confirmation.

## Procedure

### 1. Resolve the host from the identity table, not from memory

Look up the IP → hostname row before typing the IP. Adjacent rows of the form
`<hostA> | 100.64.0.4 | hostname flow-edge` and `<hostB> | 100.64.0.5 | hostname srv1946043` are
exactly the pair that gets swapped. If a peer names a host by hostname and you address it by IP,
reconcile the two before transferring.

### 1b. A local target makes every check agree — rule it out first

Before any deictic target ("the other node", "the far host"), resolve the alias to an address and
compare it against the machine you are standing on:

```bash
ssh -G <alias> | grep -iE '^hostname|^port'     # what the alias actually means
hostname; hostname -I; curl -s -m5 ifconfig.me   # what this machine actually is
```

If they match, the transfer is a copy to itself and **every instrument you have will confirm it
perfectly**: exit 0, matching `sha256sum`, `hostname` returns a real hostname, the directory mtime
advances. Step 2's three-field probe cannot catch this, because all three fields are true. This is the
one failure the core law does not cover — a *successful* transfer that never left the host.

Measured on this estate: `Host vps` resolves to the address of the machine the agent is running on, so
"put it on the VPS" from the VPS is a self-copy. Hostname aliases here were written for a human at a
terminal, not for an agent that may itself be on the target.

### 1c. `hostname` is the container's name when the peer runs it inside one

With 8+ containers on a host, `ssh <target> 'hostname'` can answer with a container id and still be a
true statement about the wrong machine. Ask for the **outside** identity in the same probe:

```bash
ssh <target> 'hostname; cat /etc/machine-id; ls -d /proc/1/root >/dev/null 2>&1 && echo BARE_METAL'
```

`/etc/machine-id` is per host, not per container, so it separates the two. If the copy lands inside a
container, the file is present by every local check and invisible to the next reader on the host.



```bash
ssh <target> 'hostname; sha256sum <path>; stat -c %y <dir>'
```

Three fields, one command:

| Field | What it settles |
|---|---|
| `hostname` | the transfer reached the machine you meant |
| `sha256sum` | the bytes are the bytes you sent |
| dir `mtime` | something actually wrote there, and when |

If `hostname` is not the intended host, stop — the matching hash is meaningless.

### 3. Only the receiving side is the witness

**The receiver must probe and report its own hash.** A cross-host claim verified only by the sender is
one-sided and unfalsifiable. State host + path + hash + timestamp together. A bare "it's on disk" names
no host and can be neither confirmed nor refuted by the other party.

### 4. Prefer a shared arbiter over repeated direct copies

A git remote both nodes can fetch from resolves to an identical blob on both sides *and* carries
provenance a direct copy cannot: commit sha, blob hash, branch name, author. Push to the remote; let
the peer pull and report the blob hash. This also survives the case where the two hosts cannot reach
each other directly.

### 5. Kill the loop at the second failure

Two rounds of "hash matches somewhere" claims cost more than the artifact is worth. After a second
failed probe:

- paste the content into the channel (**chunk it** — a multi-KB block can be silently dropped by the
  chat platform, leaving a message that mentions a document and contains none), **or**
- switch to the shared arbiter.

Do not run a third direct copy. A governance thread spent on one file transfer is the entropy the
transfer was supposed to avoid.

## Pitfalls

- **A target alias that resolves to this machine is never a transfer, however clean the receipt.**
  Resolve the alias and compare against `hostname -I` *before* copying (step 1b). Exit 0, a matching
  hash, a real hostname and an advanced mtime are all consistent with a self-copy.
- **A sender-side hash check cannot falsify its own transfer.** It reads the same wrong machine every
  time. Only a receiver-side probe, or the receiver's directory mtime, breaks the loop.
- **A directory mtime that did not advance at the claimed landing time means nothing was written
  there** — however confidently the sender reports success. Ask for the mtime, not the hash.
- **A multi-KB in-channel paste may not be transmitted at all.** Message-size limits can drop the body
  silently while a short accompanying note goes through. If the deliverable is a document, use git or
  filesystem transfer; if you must paste, chunk it and have the receiver confirm the byte count.
- **Never report a remote path as existing without printing the peer's hostname in the same probe.**
  "File absent on node B" and "file present on node A" can both be true — they are different trees.
- **Record the arbiter's provenance in the handoff**, not just the fact of transfer: commit sha, blob
  hash, and branch. That is what makes the artifact re-obtainable by a third party later.

## Constitutional Binding

- **F2 TRUTH** — location and content are separate claims; never merge them into one "delivered".
- **F4 CLARITY** — one probe, three fields, one sentence in the report.
- **F11 AUDITABILITY** — host + path + hash + timestamp is the minimum receipt for a cross-host artifact.

DITEMPA BUKAN DIBERI ⚒️
