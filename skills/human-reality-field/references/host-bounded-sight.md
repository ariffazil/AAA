# Host-Bounded Sight — Federation is Distributed, Yours is Not

> **Use when:** the agent is about to declare a registry, file, path, or artefact as **missing** / **absent** / **uncanonical** / **ENOENT** / **untrusted**, OR when the sovereign references an artefact (SHA, filename, summary) that the agent cannot byte-verify from its current host.

---

## The Federation Architecture (one breath)

arifOS is a distributed federation. Each host has a distinct role and visibility:

| Host | Role | Typical tree roots |
|---|---|---|
| KVM8 (forge) | Authoritative substrate — kernel, AAA organs, ratified seals | `/root/AAA`, `/root/A-FORGE`, `/root/.hermes`, `/root/well` |
| KVM4 (workshop) | CCC coding workers, subagent working trees | `/root/.openclaw/`, `/root/.gemini/`, `/root/.kimi/` |
| KVM2 (witness) | Independent observation, FRAME | `/root/frame`, `/root/AAA/witness` |
| HERMES (legacy) | Pre-migration heritage tree | `/root/HERMES/` (quarantined or shadow-mirrored) |

What you see on your host is not what the federation sees. **You are bounded by your mount points.**

---

## The Probe Order (always do this before declaring absence)

Before answering "is X present?", "does Y exist?", "where is Z?":

1. **Check your host** — `ls`, `find`, `read_file`, `grep` on the path the sovereign or external agent named.
2. **Try alternates** — with extensions (`.yaml`, `.json`, `.md`), without, in archive trees, in shadow mirrors.
3. **Cross-check the registry** — if the sovereign cited a path, is it listed in any host-wide index (`FEDERATED_SKILLS_REGISTRY_V3.yaml`, `MACHINE_MAP.md`, `SUBSTRATE_GATE_POLICY.yaml`)?
4. **State the limit** — what you CAN see, what you CANNOT see, what requires the sovereign to lift cross-host access.
5. **Never declare ENOENT** without first saying "I checked <path> with extensions X, Y, Z, on host K, and did not find it. If the file lives on another host, I cannot witness it from here."

---

## Anti-Pattern: The Wrong-Address State Failure

The most common silent failure mode:

- Sovereign names `path/to/syed_khairuddin` (no extension).
- Agent probes `path/to/syed_khairuddin` → ENOENT.
- Agent reports: "Identity card missing."
- Reality: `path/to/syed_khairuddin.yaml` (7,146 bytes, sha256:03fdd601...) exists on the same host.

**The bug is in the probe, not the disk.** The agent silently misled, the audit assumed the disk, and the report went stale.

**Fix:** when probing for a named file, list **with extension first**, then **without**. State both attempts.

---

## Anti-Pattern: The Cross-Host SHA Trust

When the sovereign shares an artefact by SHA-256 and a one-line description:

- The artefact may have been forged on another host or in another agent's working tree.
- You CANNOT byte-verify it from your host unless you have read access to that tree.
- If you have read access, hash it yourself: `sha256sum <path>`.
- If you do not have read access, **state the limit**: "I see the SHA from your message; I cannot byte-confirm from this host. I will treat it as a reference, not a reading."

Trust by reference ≠ witness by reading.

---

## Anti-Pattern: The Federation-Topology Claim

Statements like:
- "There is no edge registry" — without probing all four host roles.
- "Identity card missing" — without listing with extensions.
- "registry-exists-but-unread" — without checking what actually reads it.

Each is a **claim about federation state**, not just local state. Local claims are easy. Federation claims require probe-everywhere-first.

---

## The Pattern

Before any negative claim about a distributed system:

```
1. Probe locally with extensions.
2. Probe alternate trees (archive, shadow, mirror).
3. Cross-check host-wide indexes.
4. State the verification limit.
6. If the claim survives, name it. If it doesn't, retract it honestly.
```

---

## Worked Example

**Sovereign says:** "I forged `FEDERATED-HUMAN-REALITY-MAP-2026-09-24.md` with SHA `138d4064...`."

**Agent response:**

> The SHA you cited is from Lane B's working tree (likely `/root/.gemini/antigravity-cli/brain/...`), not on my host (KVM8). I cannot byte-verify the SHA from here. I will treat the artefact as a reference. If you want me to read it, paste the content or grant access to the tree where it lives.

Do NOT say "got it, sealing per your SHA" without verification. Do NOT say "ENOENT, missing" without probing the alternate.

---

## Cross-Reference

- Pitfall #9 (Host-Bounded Sight Trap) and #10 (Cross-Host Artefact Trust Trap) in `SKILL.md`.
- `human-reality-bridge` — for cron runs that touch a human (delivery surface).
- `federation-alignment-probe` — for read-only federation audit posture.
- `wrong-address-state-fails-silently` doctrine — for the underlying mechanism.