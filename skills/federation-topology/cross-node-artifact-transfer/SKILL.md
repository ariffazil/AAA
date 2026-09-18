---
name: cross-node-artifact-transfer
description: "Use when moving a file between federation nodes."
version: 1.0.0
owner: AAA
risk_tier: medium
autonomy_tier: T1
floor_scope: [F1, F2, F11]
tags: [federation, transfer, verification, multi-machine, provenance, anti-fabrication]
triggers:
  - "store this file so <node> can retrieve it"
  - "move this to KVM4"
  - "push this to the other machine"
  - "the file isn't here"
  - "already on disk"
---

# Cross-Node Artifact Transfer

Moving bytes between federation hosts and proving they arrived. The failure mode is not a dropped
packet — it is a **successful write to the wrong machine**, followed by sender-side checks that agree
with you. See `federation-machine-verification` for node identity and the machine table; this skill
owns the *transfer* and its attestation.

## The invariant

```
exit 0  ≠  delivered
```

A successful `scp`, `ssh`, or `git push` attests that **whatever the target resolved to** accepted the
bytes. It says nothing about which node you named, and nothing about the receiving filesystem.

## Procedure

1. **Resolve the destination's identity before writing.** Run
   `scripts/verify-node.sh <ssh-target> [expected-hostname]` and compare against the node you intend.
   If it does not match, **stop** — fix the route (`~/.ssh/config`, `/etc/hosts`, MagicDNS) before
   transferring. A name you believe maps to node A can resolve to node B while staying perfectly
   reachable, so nothing errors and nothing warns.
2. **Pick the most-witnessed lane available.** In order:
   - **git** — commit on the sender, push to a shared remote, peer fetches. Gives the transfer a
     third-party witness and an immutable record of what moved. Preferred whenever both nodes share
     the remote.
   - **shared mount / symlinked tree** — no transport at all; confirm both nodes resolve the same path.
   - **`scp` / `rsync`** — works, but no third-party witness. Use only when the above are unavailable.
   - **chat paste** — never (see Pitfalls).
3. **Write.** Create the destination directory explicitly; do not assume the peer's tree matches yours.
4. **Request receiver attestation — the peer, not you, confirms.** Have the receiving node run
   `scripts/attest-transfer.sh <path>` and report back `host=… path=… sha256=… bytes=…`. The transfer
   is complete when the *receiver* reports the artifact, never when the sender reports success.
5. **Record the claim with all four fields.** `host + path + sha256 + bytes`. A hash quoted from the
   sender's own copy does not attest the receiver's, and "already on disk" without naming *which* disk
   is not a receipt. Where the artifact is consequential, add `lines=` and a timestamp.

## Reporting shape

```
TRANSFER  <artifact>  →  host=<receiver-hostname>  path=<absolute>
          sha256=<hash>  bytes=<n>  lane=<git|scp|mount>  attested_by=<receiver>
```

State the lane. "Sent" and "pulled" are different provenance claims, and a reviewer cannot tell them
apart from a hash alone.

## Pitfalls

- **Sender-side verification cannot detect a misroute — structurally, not merely in practice.**
  Checking the file from the sending seat re-reads the same wrong destination and confirms it. The only
  valid confirmation is the receiver probing its own filesystem; if you "verified" a delivery and the
  peer still reports absence, suspect your own routing before doubting their probe.
- **Never move artifacts by pasting them into a chat.** Platform message limits drop or split long
  payloads **silently** — the sender sees no error, and an apparently successful paste can deliver
  nothing at all. Paste only for human review; move bytes over git, a mount, or a hash-verified
  transfer. A chat relay also leaves no third party able to arbitrate who is right.
- **A directory's `mtime` is the cheapest falsifier of a claimed write.** `stat -c '%y %n' <dest-dir>`
  — if it predates your claimed landing time, the write did not arrive there. Stop re-asserting and
  re-derive the route; repeated re-sends to the same wrong target are indistinguishable from
  fabrication to everyone else.
- **Do not name the receiver's host from memory, an alias, or prior-turn prose.** Re-probe it. Aliases
  drift, and the label in a document is not the `hostname` on the box.
- **A directory that does not exist on the peer is not something to paper over with `mkdir -p` and then
  call it delivered** — confirm the peer's tree layout first. Nodes can carry different layouts for the
  same logical content, so the path that is correct on the sender may be wrong on the receiver, and a
  second copy scattered beside the real one is worse than the missing file.
- **Do not close a transfer on "the other side said it worked".** Self-reported success is a claim; the
  receiver's own hash output is the evidence. Where the two disagree, the filesystem wins.

## Related

- `federation-machine-verification` — node identity table, which host runs what (read it first).
- `agent-to-agent-enablement` — A2A *protocol* transport; that skill owns wire-level peer messaging,
  this one owns moving an artifact between node filesystems.
- `handoff-contract` — what may be asked of another agent, and the return contract.
- Transition law `PRODUCED ≠ SENT ≠ DELIVERED ≠ OBSERVED ≠ ACKNOWLEDGED` —
  `/root/AAA/instructions/state-transition-discipline.md`.

DITEMPA BUKAN DIBERI ⚒️
