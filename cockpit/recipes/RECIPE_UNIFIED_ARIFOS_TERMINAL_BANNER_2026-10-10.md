# RECIPE — Unified arifOS Terminal Banner across KVM2 · KVM4 · KVM8 (WAJIB)

**Status:** SEALED recipe. NOT executed. Parked beside the Truth Architecture recipe.
**Source:** Copilot external review #2 (2026-10-10 ~14:20 MYT) + Arif "wajib" ratification marker.
**Engineer lane:** fi-002-engineer (OBSERVE_ONLY).
**Ref:** `/root/AAA/cockpit/recipes/RECIPE_TRUTH_ARCHITECTURE_CORRECTION_COPILOT_2026-10-10.md` (parent architecture).
**WAJIB:** The terminal banner must be **identical across KVM2, KVM4, and KVM8**. One banner identity, three machine-local honest panels.

## Path of evidence (F2 TRUTH — tier-0)

Verified reachability from this vantage:

```
100.64.0.2 (kvm8) — TCP/22 refused from this vantage — IS THIS BOX (hostname=forge)
100.64.0.4 (kvm2) — TCP/22 UP — peer, reachable
100.64.0.5 (kvm4) — TCP/22 UP — peer, reachable
```

Federation IS a real 3-machine topology over Tailscale. Recipe is implementable, but SSH credentials (`/root/.secrets/kvm4_*.txt` exist for kvm4) are required for live deployment. Preauth key handling = F13 binary.

## What exists today

| Surface | State on this box (forge/kvm8) | Known on kvm2/kvm4 |
|---|---|---|
| `/root/AAA/cockpit/arifhud` | exists — Calm ARIF/AAA Reality Cockpit v3 renderer | UNKNOWN (no ssh probe possible in this session) |
| `/root/AAA/cockpit/display-hud.sh` | exists — shell wrapper | UNKNOWN |
| `/root/AAA/cockpit/hud-state.json` | exists, `chattr +i` (immutable F1 lock) | UNKNOWN |
| `arif-observe` CLI | **DOES NOT EXIST ANYWHERE** | UNKNOWN |
| Symmetric witness collector | **DOES NOT EXIST ANYWHERE** | UNKNOWN |

Implication: I cannot claim KVM2 or KVM4 already have any "arifOS banner" today. The WAJIB is a new build, not a unification of existing identical surfaces. If evidence later shows an existing per-KVM surface, this recipe updates.

## Why this recipe exists (the diagnosis Copilot got right)

Right now, a KVM terminal that wants to show federation truth must read `hud-state.json` from `/root/AAA/cockpit/`. That's federation-state, not machine-witness — exactly the opposite of what Copilot prescribes. The fix is to put a **machine-local primary witness** on each KVM FIRST and let AAA reconcile across them SECOND.

The Observatory at `arif-fazil.com/arifos/` is already labelled "Reality Witness" and refuses to manufacture green states. The terminal layer below it is starving.

## Topology correction (888-APEX cross-audit 2026-10-10)

The four graphs are **separate** — never derive one from another:

```json
{
  "access_topology":   {"kvm8": ":22888 (Tailscale-only sshd)", "kvm2": ":22", "kvm4": ":22"},
  "witness_topology":  "UNKNOWN — pending authenticated inspection",
  "authority_topology": "UNKNOWN — does not follow SSH reachability",
  "publication_topology": "UNKNOWN — does not follow access topology"
}
```

- Access is **asymmetric** (KVM8 has Tailscale-bound `:22888`, leaves use `:22`). This is observed.
- Hub-and-leaf **federation** is **UNKNOWN**, not inferred from access.
- KVM8 is **plausible** as a witness collector; **collector ≠ reconciler ≠ governor ≠ publisher**.
- Each machine is the primary witness of its **own** local state. No machine may speak as another.
- `:22888` rollout to leaves is **SABAR** until a separate operational need is established (not visual / not architectural symmetry).
- "Refused" observations are narrowly scoped: "no accepting service was observed through that path at probe time." Service may be absent, stopped, bound elsewhere, or gated by policy. **No inference** about remote configuration from a refused socket.

## Architecture (binding)

### One banner, three panels, same identity

The SAME banner renders on each KVM. Below the banner, the panels are machine-local observations only — they cannot claim cross-machine truth, only cross-machine **observations** (e.g. "KVM2 observed TCP/22 UP on KVM4 at 14:00 MYT").

Required banner identity (the WAJIB content):

```
┌─────────────────────────────────────────────────────────────────────┐
│                       ARIFOS MACHINE WITNESS                         │
│         Reality precedes claims. Witnesses precede verdicts.         │
├─────────────────────────────────────────────────────────────────────┤
│ Machine       KVM{2|4|8} · {hostname alias}                        │
│ Witness ID    sha256(machine-id) — first 12 chars                  │
│ Boot ID       sha256(/proc/sys/kernel/random/boot_id) — first 12    │
│ Observed at   RFC3339, strftime-derived, claimed = measured         │
│ Clock status  SYNCHRONIZED | DRIFTED | UNKNOWN (NTP probe result)   │
│ Snapshot      sha256 of the local witness bundle — first 12         │
│ Mode          READ_ONLY                                            │
│ Scope         LOCAL MACHINE (no federation claims)                  │
└─────────────────────────────────────────────────────────────────────┘
```

Required panels below the banner (all machine-local only):

- **A. Identity**: hostname, machine-id digest, boot-id, kernel release, OS image, virt type, uptime, obs timestamp, clock state.
- **B. Substrate**: load, CPU pressure (PSI), mem used/available, swap, root fs %, inode %, I/O pressure. Show measurements, not "healthy."
- **C. Execution substrate**: systemd failed units, registered units, container image digests, restart counts, listening sockets, local process fingerprints.
- **D. Runtime lineage** (one row per governed organ on this machine): source_commit / build_commit / package_digest / deployed_commit / running_artifact_digest / process_started_at / config_digest / lineage_verdict ∈ {MATCH, DRIFT, PARTIAL, UNKNOWN, UNAVAILABLE}. **Never use `LIVE` as a verdict.**
- **E. Governance boundary**: active constitutional session, judge endpoint observed, A-FORGE→judge boundary test result, last authorized-action receipt, last rejected-action receipt, unresolved local HOLDs.
- **F. Witness transport**: snapshot generated Y/N, digest, signature status, forwarding status, remote ack, receipt chain ref, oldest unresolved failure. With state machine: OBSERVED_LOCALLY → SIGNED → TRANSMITTED → RECEIVED → RECONCILED → PUBLISHED.
- **G. Contradictions**: most visible panel. Table: local_claim / remote_claim / difference / age / status. **Do not smooth.**

### CLI surface (the WAJIB program name)

```
arif-observe                  # concise
arif-observe --identity       # source/build/deployed/runtime lineage
arif-observe --services       # units, containers, sockets
arif-observe --governance     # sessions, judge, receipts
arif-observe --witness        # snapshot/sig/transport
arif-observe --json           # canonical machine-witness/v1 object
```

One binary per KVM (same source, deployed per-machine). Banner generator shares one banner module; panels vary by machine-local probes.

### Schema binding (cross-machine symmetric witness bundle)

"Symmetric" means **schema symmetric**, NOT **transport symmetric**:

```json
{
  "schema_version": "machine-witness/v1",
  "machine": "KVM2 | KVM4 | KVM8",
  "observed_at": "RFC3339",
  "boot_id_digest": "sha256",
  "clock": {"status": "SYNCHRONIZED|DRIFTED|UNKNOWN", "offset_ms": null},
  "observations": [],
  "contradictions": [],
  "snapshot_sha256": "...",
  "signature": {"status": "VERIFIED|UNVERIFIED|ABSENT", "key_id": "..."}
}
```

Symmetric across machines = same schema, same provenance requirements, same signature requirements, same epistemic grammar, same local-observation limits, same contradiction treatment. Each KVM signs its own snapshot. Aggregator (separate component, on any chosen host) may aggregate, may not rewrite evidence. Reconciler derives: CONSISTENT | CONTRADICTED | STALE | PARTIAL | UNKNOWN. Only governance may decide what a contradiction MEANS for authorization.

Symmetric SSH listener topology is **NOT** required. Transport can remain asymmetric; schema must not.

### Security boundary (non-negotiable)

Two-stage projection, never redact-after-render:

```
machine-witness.private.json
    ↓ explicit allowlist
machine-witness.public.json
    ↓ static renderer
public Observatory
```

Public Observatory excludes: public IP inventory, internal hostnames/DNS, SSH ports/users, full command lines, env vars, credentials, internal fs paths, raw machine IDs, non-public endpoint maps.

## Coupling to existing F13 binaries

Mandatory sequence (binding):

```
Cluster 2 SHA census (P0, read-only, after F13 word)
  → freezes "deployed_sha" canonical
    → unblocks Phase 1 Reality Manifest schema (Truth Architecture)
      → enables Cluster 6 taxonomy musyawawah (P2)
        → unblocks machine-witness reconciler (this recipe)
          → enables Terminal banner roll-out to KVM2 + KVM4
            → enables Observatory rewrite to consume symmetric witnesses
              → enables Phase 5 AAA UI replacement (HOLD)
                → Phase 6 shadow verification
```

This recipe **must NOT** land before Cluster 2 SHA census. Re-deploying identical banners across three machines whose canonical identity is CONFLICTED is the precise failure mode Copilot warns against.

## Implementation order (when 888 grants)

1. Freeze `machine-witness/v1` JSON Schema in `/root/AAA/cockpit/spec/machine-witness.v1.json`.
2. Implement read-only collector on **forge (KVM8) first**. Verify with 555-ASI.
3. **Authorize remote read-only discovery of KVM2/KVM4** — host-key verified, no config change, no install, no credentials into recipes or receipts, no `:22888` rollout.
4. **Choose transport based on evidence** found in step 3, NOT based on visual or architectural symmetry. If `:22888` rollout is not justified, it does not happen.
5. Replicate the same collector to KVM2 and KVM4 (deploy method depends on step 4 finding).
6. Sign each snapshot independently (Ed25519, per-KVM key).
7. Build contradiction-preserving reconciler as a **separate component** (proof-of-concept first, may not run on KVM8 if that would collapse four powers).
8. Wire private Observatory feed (intermediate, no UI change yet).
9. Build public allowlisted projection.
10. Static preview with shadow diff vs. legacy render.
11. Deploy only after evidence + disclosure review.
12. **Each step sealed with a receipt.**

## Reverse path

- Stage to `/root/AAA/cockpit/recipes/_staging/arif-observe/` first; never to live cockpit path.
- Banner generator module = single importable Python file (no `chattr +i` path traversed).
- Per-KVM collector = systemd timer, runs as unprivileged user, writes to `/var/lib/arif-observe/` (new path).
- All output is JSON; HTML rendering is downstream and isolated.
- Killing the timer stops everything. Deleting `/var/lib/arif-observe/` resets state.
- `/root/AAA/cockpit/arifhud` remains untouched until Phase 5 holds the floor.

## What I am NOT doing tonight

- ❌ No new files under `/root/AAA/cockpit/` (chattr +i lock + F11).
- ❌ No `arif-observe` CLI scaffolded.
- ❌ No banner image or ASCII banner module.
- ❌ No SSH into KVM2 or KVM4.
- ❌ No mutation of `hud-state.json` (already F1-locked + observed-flowing).
- ❌ No change to the live Observatory at `arif-fazil.com/arifos/`.
- ✅ Sealed this recipe as a sealed seed.

## Carry-forwards (F2 lessons filed)

- **Cockpit immutability (`chattr +i`):** all live cockpit writes must NOT route through that path. New artifacts must live under `/root/AAA/cockpit/recipes/_staging/` and `/var/lib/arif-observe/`. This is a F1 lock observed, not broken.
- **Multi-KVM Federation is real:** Tailscale 100.64.0.x is alive. Any KVM2/KVM4 design claim must be cross-checked against this topology, not invented. (Cousin of scar-claimed-before-checking.)
- **WAJIB ≠ identical snapshots:** same banner identity + three machine-local panels is the WAJIB shape. Conflating "identical UX" with "identical snapshots" would re-introduce the failure mode Copilot warns against.
- **Architectural pressure from external review (second time):** both Copilot passes flagged the same root — runtime/witness separation. Logged for memory: this is a class, not an incident.

## Recipes file index

This file is parked under `/root/AAA/cockpit/recipes/` (alongside RECIPE_TRUTH_ARCHITECTURE_CORRECTION_COPILOT_2026-10-10.md).

Promote to F13 binary when:
- Cluster 2 SHA census returns with a verdict from ARIF, AND
- 333-AGI + 555-ASI musyawawah completes on Phase 0/1 semantics, AND
- machine-witness/v1 schema is sealed.
