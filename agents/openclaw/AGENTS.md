# AGENTS.md — Pointer — OpenClaw — warga
> **EXECUTION-FIRST (anti-collapse, F13 2026-09-14):** Never collapse unfinished executable work back to the human. If info + authority + capability already exist, execute to completion / capability-exhaustion / authority-boundary / 888-HOLD. Plan ≤3 turns, then execute by default. Never ask Arif to do work you can do yourself. F1 / F13 / 888 remain binding. → `/root/AAA/instructions/anti-collapse-doctrine.md`

> **Canonical:** /root/AGENTS.md
> **ZEN:** /root/AAA/prompts/AAA-ZEN-ALIGNMENT.md
> **SOT:** 2026-09-18 | **seal_seq:** SEAL-8a8e064d1fe34443
> This file is a pointer, not a constitution. Load /root/AGENTS.md for full doctrine.

**IKAT 2026-09-20 F13:** OpenClaw = KVM4 `openclaw-gateway` + Telegram `@AGI_ASI_bot`. Kernel FI-017 T1. Not Hermes. Not 888. Not the encoder in front of Hermes.

OpenClaw runtime overlay.

- **Edge node:** KVM4 (workshop, 100.64.0.5) — gateway `:18789` (live since 2026-09-04 13:37 MYT per MACHINE_MAP §1)
- **KVM8 mirror:** loopback DNAT `127.0.0.1:18789 → 100.64.0.5:18789` (iptables NAT, verified 2026-09-13)
- **Public ingress:** caddy vhosts `openclaw.arif-fazil.com` + `claw.arif-fazil.com` → KVM4 `:18789` (410 internal-only by policy; tailnet-only access)
- **Telegram:** `@AGI_ASI_bot` polling on KVM4
- **A-FORGE MCP broker:** KVM8 `:7072` (forge.arif-fazil.com/mcp) — execute lanes route through A-FORGE, never direct
- **A-FORGE legacy HTTP:** KVM8 `:7071` (af-forge-sense) — read-only probe compatible
- **Kernel governance:** arifOS `:8088` (mcp.arif-fazil.com) — judge + seal via constitutional
- **Cold archive (KVM8):** **ABSENT** (measured 2026-09-20). Neither `/root/.openclaw-cold/` nor `/root/.quarantine/zen-20260912/.openclaw-cold/openclaw-heritage-2.8G-20260904/` exists. Do not plan on heritage files.
- **Agent identity (kernel):** `openclaw/FI-017` · capabilities: OBSERVE · REASON · ROUTE · MEMORY · max_blast_radius: T1 · bound_to: `arif-fazil/F13`
- **AAA agent card (canonical):** `/root/AAA/agent-cards/functions/openclaw/agent-card.json` (schemaVersion 2.3.0)
- **A2A federation card:** `/root/AAA/a2a-server/agent-cards/federation/openclaw.json` (protocolVersion 1.2)
- **Identity doc:** `/root/AAA/agents/openclaw/IDENTITY.md` — kernel-aligned T1 (capabilities OBSERVE · REASON · ROUTE · MEMORY, FI-017, bound_to arif-fazil/F13); drift resolution table embedded at §Authority. OpenClaw cannot directly invoke forge_shell/forge_evaluate/forge_execute — must route through A-FORGE :7072 with lease + authority envelope.
- **F13 ikat 2026-09-20:** sovereign "ok ikat la". Extra meanings (encoder, overseer, execution, HARNESS T2) are RETIRED as live authority. Kernel row FI-017 T1 is SOT.

If this file disagrees with `/root/AGENTS.md`, the kernel wins. Fix this file.

---

*ZEN-aligned 2026-08-01, re-aligned 2026-09-18 (KVM4 cutover doctrine update + drift reconciliation).*
