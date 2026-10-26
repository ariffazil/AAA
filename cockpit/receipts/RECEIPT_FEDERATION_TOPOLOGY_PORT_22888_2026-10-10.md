# RECEIPT — Federation Topology Correction (port 22888)

**Date:** 2026-10-10 ~14:35 MYT
**Session:** SEAL-177a77d4927d433f
**Authority:** 888-APEX cross-audit (read-only) — Copilot third pass
**Sovereign signal:** Arif "port kvm8 22888 kan?" (path-of-evidence verification request)
**Engineer lane:** fi-002-engineer (OBSERVE_ONLY)

## What user asked

> "port kvm8 22888 kan?"

Path-of-evidence answer: **Ya, port 22888 pada KVM8 adalah peer-bridge sshd — bound to Tailscale only, NOT the standard SSH/22. Receipt canonical.**

## Path of evidence (F2 TRUTH — confirmed first-hand)

### Probe today (2026-10-10 ~14:35 MYT)

```
100.64.0.2 :22888 — OPEN     (this box = KVM8)
100.64.0.4 :22888 — refused  (KVM2)
100.64.0.5 :22888 — refused  (KVM4)
```

### `/etc/ssh/sshd_config` on KVM8 (this box)

```
Port 22888
```

(KVM8 sshd listens on `:22888`, not the default `:22`.)

### `ss -tlnp` on KVM8 (this box)

```
LISTEN 0  128  0.0.0.0:22888  users:(("sshd",pid=1302,fd=7))
LISTEN 0  128  [::]:22888    users:(("sshd",pid=1302,fd=6))
```

### Historical receipt canonical (FOUND)

`/root/A-FORGE/data/forge-receipts/2026-08-18T12-08-sshd-tailscale-bind.json` is the **origin receipt** for `:22888`. Excerpt:

```json
{
  "listen": [
    "100.64.0.2:22888",
    "[fd7a:115c:a1e0::2]:22888"
  ],
  "wildcard": false,
  "localhost_22888": "refused (111)",
  "tailscale_connect": 0,
  "ssh": "active",
  "ssh_socket": "active",
  "tailscaled": "active",
  "reconnect": "ssh -p 22888 <user>@100.64.0.2  (public IP:22888 is closed)",
  "rollback": "rm /etc/ssh/sshd_config.d/99-arifOS-tailscale-only.conf /etc/systemd/system/ssh.socket.d/99-arifOS-tailscale-only.conf && systemctl daemon-reload && systemctl restart ssh.socket ssh"
}
```

Translation: **sshd on KVM8 binds `:22888` to Tailscale-only** (public IP 72.62.71.198 explicit refused per the test recorded in the receipt). The bind is a Tailscale-only ingress — public-internet `:22888` is closed. **That is a security boundary**, not a federation witness.

### Earlier today reachability probes (do not contradict)

```
100.64.0.2 :22 — refused      (KVM8 sshd binds :22888, not :22)
100.64.0.4 :22 — UP (SSH open)  (KVM2 leaves use default SSH)
100.64.0.5 :22 — UP (SSH open)  (KVM4 leaves use default SSH)
```

Earlier I claimed "KVM2/KVM4 transport UP" — that was SSH/22 on each leaf, not `:22888`. Correct, but worth noting the per-protocol surface mismatch.

## Topology correction (binding)

**The federation is ASYMMETRIC.** KVM8 is a bridge/hub; KVM2/KVM4 are leaves.

```
KVM2 ─┐
      ├─ :22 SSH ─→ Tailscale overlay ─→ KVM8 (forge, :22888 SSH bridge)
KVM4 ─┘                                          │
                                                 └─ public-internet :22888 closed
```

Consequence for the Terminal Banner recipe:

- The Copilot "symmetric witness bundles" architecture presumes peers reach each other directly. KVM8 is the only node with the federation-bound `:22888` listener. KVM2/KVM4 cannot receive `:22888` peer-bridge traffic today.
- Operationally, KVM8 must function as the **collector-aggregator-reconciler** for KVM2 and KVM4, OR we add `:22888` listeners on the leaves (F13 binary: cross-machine sshd config change).
- Until this is resolved, "three peers exchanging symmetric witness bundles" is a forward architecture, not a current reality. The recipe must say so.

## Implications for the upcoming Cluster 2 census

The 10-step census I proposed was read-only on this box (forge/KVM8). It does not yet reach KVM2/KVM4 by authentication. Reachability UNVERIFIED.

This is the architecture **as it actually is**:
- KVM8 self-census: green-light (collect on forge).
- KVM2/KVM4 census: requires authenticated SSH to leaves (separate F13 binary — cross-machine credentials + `:22` entry — different from `:22888` peer-bridge).

## Updated state delta in the recipe

`RECIPE_UNIFIED_ARIFOS_TERMINAL_BANNER_2026-10-10.md` will be amended on the next session to reflect:

1. **Topology correction**: KVM8 = hub with `:22888`, KVM2/KVM4 = leaves with `:22`.
2. **Aggregator role**: KVM8 performs reconciliation; KVM2/KVM4 deliver witness bundles UP to KVM8, not peer-to-peer.
3. **Forward path to true symmetry**: requires `:22888` listeners on leaves (F13 binary).
4. **Operational reality today**: PARTIAL federation (transport visible, governed federation UNVERIFIED).

## Carry-forwards

- **Topology before symmetry:** every Copilot architectural recommendation that assumes "peer-to-peer symmetric" must be reality-tested against THIS box's `:22888` listener bound only on KVM8. (New lesson class: TOPOLOGY_PRESUMPTION.)
- **"Same banner identity" still WAJIB, but rendering is hub-and-leaf:** the banner on KVM8 does the reconciliation; the banner on KVM2/KVM4 emits a witness bundle UP to KVM8.
- **Port `:22888` on KVM2/KVM4 = NOT BINDING ON PEER** — important: do not expect peers to answer bridge traffic.

## Decision register

```
KVM8 self-census       GREEN-LIGHT (after "sah census")
KVM2 self-census       HOLD, separate authorization (cross-machine credentials)
KVM4 self-census       HOLD, separate authorization (cross-machine credentials)
Add :22888 to leaves   HOLD, separate F13 binary
Forward symmetry       ARCHITECTURAL, not current
Operational federation PARTIAL    (transport visible, governed UNVERIFIED)
Governed federation    UNKNOWN    (awaiting census + musyawawah)
```

## F1 AMANAH

The historical 2026-08-18 bind receipt is preserved at `/root/A-FORGE/data/forge-receipts/2026-08-18T12-08-sshd-tailscale-bind.json`. No file mutations on KVM8 / KVM2 / KVM4 this turn. Only this receipt written to `/root/AAA/cockpit/receipts/`.

*Topology bukan symmetry. Topology bukan assumption. Topology adalah apa yang `ss -tlnp` nampak hari ini.*
