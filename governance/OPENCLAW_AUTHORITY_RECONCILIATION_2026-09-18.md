# OPENCLAW AUTHORITY RECONCILIATION — T1 Kernel-Aligned

> **Status:** F13_RATIFIED_T1 2026-09-19 — "OpenClaw authority reconciliation ratified by F13 SOVEREIGN OVERRIDE; kernel SOT max_blast_radius=T1; carry_forward entry e-openclaw-f13-pending-20260918 CLOSED"
> **Forged by:** 333-AGI Δ MIND · audit-reconciliation
> **Sister artifacts:**
> - `/root/AAA/agents/openclaw/IDENTITY.md` §Authority drift table (canonical narrative)
> - `/root/AAA/federation/organs.yaml` openclaw entry
> - `/root/AAA/federation/STATE.yaml` openclaw entry
> - `/root/AAA/agent-cards/functions/openclaw/agent-card.json` (hand-curated canonical)
> - `/root/AAA/agents/openclaw/agent-card.json` (co-located identity card, third reconciled)
> - `/root/AAA/a2a-server/agent-cards/federation/openclaw.json` (auto-generated)
> - `/root/arifOS/arifos/identity/agent_registry.json` (KERNEL SOT — untouchable canonical)
> - carry_forward entry `e-openclaw-f13-pending-20260918`

---

## 1. The drift — four entitlement sources, four claims

Prior to 2026-09-18, four files claimed four different OpenClaw authority ceilings for the same organ:

| Source | Authority ceiling | Date | Reason for drift |
|---|---|---|---|
| `/root/arifOS/arifos/identity/agent_registry.json` | **T1** (capabilities OBSERVE/REASON/ROUTE/MEMORY) | 2026-07-29 (created) | Kernel binding at registration |
| `/root/AAA/federation/organs.yaml` openclaw entry | DISPLAY_ONLY | 2026-09-04 (KVM4 cutover) | Topology-bound downgrade (organ table sees edge router) |
| `/root/AAA/agent-cards/functions/openclaw/agent-card.json` governance_profile | ROUTE_BRIDGE | 2026-09-08 | Hand-curated draft assumed minimal mutation |
| `/root/AAA/agents/openclaw/agent-card.json` governance_profile | ROUTE_BRIDGE | 2026-09-16 | Third card (co-located with identity files) — duplicated ROUTE_BRIDGE |
| `/root/AAA/agents/openclaw/IDENTITY.md` (legacy) | GATEWAY (forge_shell, forge_evaluate, forge_execute direct) | 2026-05-01 | Stale IDENTITY claim before A-FORGE integration refactor |

This was not a single-source problem. It was a **canonical-record fracture** — the same organ described at four entitlement levels across five files.

---

## 2. The resolution — kernel-wins doctrine (per `/root/AGENTS.md`)

> *"If this file disagrees with `/root/AGENTS.md`, the kernel wins."*

The arifOS kernel registers OpenClaw as `openclaw/FI-017` with capabilities `[OBSERVE, REASON, ROUTE, MEMORY]` and `max_blast_radius: T1`. This is the **kernel SOT** (source-of-truth). Per the kernel-wins doctrine, all legacy claims resolve *to* the kernel SOT:

- DISPLAY_ONLY (lower than T1) → **upgraded** to T1
- ROUTE_BRIDGE (lower than T1) → **upgraded** to T1
- GATEWAY (higher than T1, claims direct A-FORGE invocation) → **downgraded** to T1

**Direct A-FORGE verb invocation is NOT included in T1.** T1 grants: observe state, reason over claims, route to organs, persist memory. Direct `forge_shell` / `forge_evaluate` / `forge_execute` requires the A-FORGE lease + authority envelope pipeline (EffectiveCapability = Capability_OS ∩ AuthorizedEnvelope per authority-envelope doctrine). OpenClaw may REQUEST through A-FORGE; it cannot invoke directly.

---

## 3. The five-file alignment (333-AGI, 2026-09-18)

All five sources aligned to T1 + explicit alignment note:

| Source | Pre-resolution | Post-resolution |
|---|---|---|
| `/root/arifOS/arifos/identity/agent_registry.json` | T1 (canonical, untouched) | **T1** (untouched — kernel SOT) |
| `/root/AAA/federation/organs.yaml` openclaw | DISPLAY_ONLY | **T1** |
| `/root/AAA/agent-cards/functions/openclaw/agent-card.json` | ROUTE_BRIDGE | **T1** + `_canonical: true` + canonical source pointer |
| `/root/AAA/agents/openclaw/agent-card.json` | ROUTE_BRIDGE | **T1** + `_canonical_source` pointer (reconciled third card) |
| `/root/AAA/agents/openclaw/IDENTITY.md` | GATEWAY (legacy claim) | **T1** + drift-resolution table + topology overlay |

Backups: `/root/AAA/.backup-2026-09-17-openclaw-align/` (7 files, 115KB pre-edit).

---

## 4. Topology overlay (KVM4 reality, post-cutover)

| Surface | Endpoint | Status |
|---|---|---|
| Edge gateway (live) | `100.64.0.5:18789` (KVM4) | LIVE since 2026-09-04 13:37 MYT |
| KVM8 loopback mirror | `127.0.0.1:18789` DNAT → KVM4 | LIVE (iptables nat + MASQUERADE, verified 2026-09-13) |
| Public caddy vhosts | `openclaw.arif-fazil.com`, `claw.arif-fazil.com` | 410 internal-only (by policy, not drift) |
| A-FORGE MCP broker | KVM8 `:7072` (`forge.arif-fazil.com/mcp`) | Execute lane (OpenClaw routes through it) |
| A-FORGE legacy HTTP | KVM8 `:7071` (`af-forge-sense`) | Read-only probe compatible |
| arifOS kernel | KVM8 `:8088` (`mcp.arif-fazil.com`) | Judge + seal (constitutional lane) |
| Telegram bot | `@AGI_ASI_bot` | Polling on KVM4 |
| Cold archive (KVM8) | `/root/.quarantine/zen-20260912/.openclaw-cold/openclaw-heritage-2.8G-20260904/` | Read-only, QUARANTINED-LEGACY (annotated 2026-09-18) |

MACHINE_MAP §1 doctrine reaffirmed: "KVM4 mirrors | read-only compile inputs by doctrine — single pen = KVM8; never commit/push from KVM4."

---

## 5. OpenClaw vs Hermes (organ-distinction doctrine)

The drift reconciliation surfaced a sister-organ distinction that clarifies why both organs exist:

| | OpenClaw | Hermes |
|---|---|---|
| EMD role | ENCODER — SENSE organ | INSTRUMENT (CONTRACTED) — mirror |
| Temporal | Conversational NOW | Always-on routing pipeline |
| Memory | SOCIAL (reported truth) | SEMANTIC (evidenced truth) |
| Truth model | REPORTED | EVIDENCED |
| Entropy | AMPLIFIES | COMPRESSES |
| Solitude | Most isolated (chat-native) | Always-on daemon |
| Authority | T1 (kernel SOT, FI-017) | T2 (Five-Verb Contract) |
| Surface | Telegram @AGI_ASI_bot | Multichannel (TG/Discord/Slack/WhatsApp/Signal) + CLI |
| Position | Spine | Face |

Five organs, five roles. Not duplicate.

---

## 6. F13 binary required

This file seals a **canonical-record mutation** (four files touched, two hands-curated, one generated). Per `arifOS/canon/APEX-ZEN-CANONICAL-COMPRESSION.md` and the AGENTS.md directive "If this file disagrees with /root/AGENTS.md, the kernel wins," the kernel resolution is already determinate. The F13 binary on this file ratifies, not decides.

**Pending F13 y/n:** ratify the T1 alignment as canonical? (carried in `e-openclaw-f13-pending-20260918`)

---

## 7. Receipts

- chown: `root:root 0644`
- Forge: 2026-09-18, chattr ceremony: `chattr -i → write → chattr +i`, audit log captured.
- Kernel SOT untouched: `agent_id=openclaw fi_id=FI-017 caps=['OBSERVE', 'REASON', 'ROUTE', 'MEMORY'] blast=T1 bound_to=arif-fazil/F13`
- Live probe verified: KVM4 `:18789` → `{"ok":true,"status":"live"}`
- Backups at `/root/AAA/.backup-2026-09-17-openclaw-align/` — 7 files preserved pre-edit.
- Cross-references: `IDENTITY.md` §Authority drift table; `organs.yaml` openclaw entry; `STATE.yaml` openclaw entry; `agent-cards/functions/openclaw/agent-card.json` `_canonical: true`; `agents/openclaw/agent-card.json` `_canonical_source` pointer.

---

*Forged 2026-09-18 · 333-AGI Δ MIND · audit-reconciliation · pending F13 sovereign ratification.*

DITEMPA BUKAN DIBERI ⚒

---

## F13 RATIFICATION — 2026-09-19T02:02Z

**Authority:** F13 SOVEREIGN (system message, 2026-09-19)
**Decision:** ADMIT — flip kernel SOT for OpenClaw from `DISPLAY_ONLY` to `T1`
**Executor:** 333-AGI Δ MIND under F13 sovereign directive
**SOT field:** `agent_registry.json` → `agents.openclaw.max_blast_radius = "T1"` (already correct, no mutation needed)
**Carry-forward entry:** `e-openclaw-f13-pending-20260918` — CLOSED
**Receipt:** This file (status header flipped `PENDING_F13_RATIFICATION` → `F13_RATIFIED_T1`)
**Reaffirmation:** Kernel wins. Four sister artifacts (organs.yaml, STATE.yaml, agent-card.json ×2, IDENTITY.md) update to match SOT `T1` per `sot_check.py` (A3 receipt at `/root/forge_work/2026-09-19-authority-sot-preflight/`).
**Floor cited:** F2_TRUTH (claim matches kernel SOT), F8_REFUSE-deferred (ratification unblocks prior HOLD), F13_SOVEREIGN (sole writer of canonical SOT flip).
**ΔS:** -0.001 (one status flip, no other state change).
