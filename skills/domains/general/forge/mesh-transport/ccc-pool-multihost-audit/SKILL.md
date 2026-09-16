---
id: ccc-pool-multihost-audit
name: ccc-pool-multihost-audit
version: 1.0.0
description: "Use when auditing CCC coding-agent transfer across hosts."
owner: curator
risk_tier: T1
floor_scope: [F2, F4, F12]
---

# CCC Pool Multi-Host Audit — KVM8 ↔ KVM4

The federation runs coding workers on two hosts: KVM8 (af-forge, 72.62.71.199,
control plane) and KVM4-forge (srv1946043, 100.64.0.5, dedicated CCC worker
pool). KVM4 workers must route ALL inference through the sovereign FED gateway
`http://100.64.0.2:4000/v1` (haproxy auth injection — zero local secrets).

Use this skill when Arif asks "is the transfer complete?", "contrast KVM8 vs
KVM4", "any remaining agents or cards?", or before/after any pool migration
step. For how to dispatch work to KVM4, read `kvm4-ccc-dispatch` (user-owned,
read-only reference).

## The 6-axis audit (a harness is "transferred" only if ALL pass)

1. **Dispatch truth** — diff the `ccc-remote` case list on KVM8
   (`head /usr/local/bin/ccc-remote`) against binaries actually on KVM4
   (`ssh root@100.64.0.5 'PATH=... which opencode codex qwen kimi aider'`).
   Binary on disk with no dispatch entry = half-migrated. Dispatch entry with
   no config dir on KVM4 (e.g. `agy` without `~/.antigravity`) = also
   half-migrated.
2. **Pool card** — `kvm4-ccc-pool.json` harness list vs reality
   (`/root/AAA/a2a-server/agent-cards/harnesses/` on KVM8).
3. **Individual harness cards** — do opencode/codex/qwen/kimi-code/aider cards
   acknowledge KVM4 routing, or still describe KVM8 binaries only? A router
   reading individual cards will mis-route to stale hosts.
4. **AAA repo drift** — on BOTH boxes: `git -C /root/AAA rev-list --count
   HEAD..origin/main` + skills dir count (`ls /root/AAA/skills | wc -l`).
5. **Governance overlay coverage** — which harnesses have AGENTS.md/rules
   overlays on KVM4 (2026-09-02: only opencode had rules; codex/qwen rely on
   root AGENTS.md).
6. **Config routing** — every harness config must point at
   `http://100.64.0.2:4000` (grep `base_url` in opencode.json,
   .codex/config.toml, .kimi-code/config.toml, .qwen/settings.json).

## Audit pitfalls

- **Same-day version drift is normal.** KVM4 is the fresh box and its
  binaries run NEWER than KVM8 (2026-09-02: opencode 1.18.26 vs 1.18.11,
  codex 0.152.0 vs 0.149.1, kimi 0.39.1). Never quote one host's versions as
  "the federation version"; always record both, per harness.
- **Wrap `--version` in `timeout 30`** — node-based CLIs (kimi, aider) can
  hang indefinitely under load and eat the whole audit budget.
- **`which` ≠ complete.** Presence of a binary proves nothing about config,
  card registration, or dispatch. Probe marker output, not file existence.
- **KVM8-only lanes are by design** — claude / gemini / copilot /
  continue-cli / openclaw do not exist on KVM4. Absence there is not a defect.
- SSH to KVM4 is `root@100.64.0.5` ('kvm4' does not resolve); use
  `-o ConnectTimeout=10`. Batch probes into one SSH call — per-command SSH
  round-trips dominate audit time.
- The agent-card registry lives ONLY on KVM8; KVM4 has no a2a-server dir.
  Cards are a KVM8-side concern (KVM4 boxes don't serve them).

## Reporting shape (human bridge)

Collapse to: (a) what is fully transferred, (b) what is half-migrated — item
by item with the exact missing half, (c) what is KVM8-only by design,
(d) registry/overlay drift, then ONE closing offer to close the gaps in a
single pass. No raw matrices to Arif.

## Session evidence

- `references/kvm8-kvm4-transfer-audit-20260902.md` — full findings from the
  2026-09-02 contrast audit (grok/agy half-migrated, card staleness, repo
  drift, overlay gaps).

## Related (read-only, not editable by curator)

- `kvm4-ccc-dispatch` (user-owned) — dispatch commands, probe markers, M1
  opencode-server migration.
- `fi-mesh-check` (AAA external) — single-host FI probe matrix; extend
  mentally to both hosts when doing a full mesh check.
