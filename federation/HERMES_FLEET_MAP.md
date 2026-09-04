# HERMES FLEET MAP — all Hermes agents across KVM2 / KVM4 / KVM8

> **Live-probed 2026-09-04 ~07:30 MYT by kimi-code/FI-008 from KVM8 (mesh SSH, BatchMode).**
> SOT family: `MACHINE_MAP.md` (machines) · `SERVICE_OWNERSHIP.yaml` (units) · `TELEGRAM_BOT_ROUTING_DOCTRINE.md` (bots/chats) — this file maps the HERMES LAYER and links them.
> Re-probe before acting. Fleet version at probe: **hermes-agent 0.20.1 on ALL three nodes** (consistent).

## 1. The fleet at a glance

| # | Instance | Machine (mesh IP) | Process / Unit | State | Serves | Model routing |
|---|---|---|---|---|---|---|
| H1 | **Hermes ASI 💃 (sovereign gateway)** | KVM4 kvm4-forge (100.64.0.5) | pid 519836 · `hermes-asi-gateway.service` **ACTIVE** | **LIVE — primary agent, all groups** | Arif (F13) | `i-arif` custom persona → FED `http://100.64.0.5:4000/v1` (litellm @ KVM4, 1M ctx), cfg `version: 35` |
| H2 | **Hermes Azwa (witness lane)** | KVM2 azwaos (100.64.0.4) | pid 275827 · `hermes-agent.service` **ACTIVE** | **LIVE — Azwa's own agent** | Azwa (SAF identity) | `agi-333` → provider `af-forge-fed` (→ KVM8 FED) + `qwencloud-free` fallback; regional: ILMU, SEA-LION, Xiaomi MiMo |
| H3 | **Hermes CLI seat (court)** | KVM8 af-forge (100.64.0.2) | on-demand `hermes` CLI (`/root/.local/bin/hermes`) | on-demand (interactive pts) | FI agents / Arif at terminal | seat config `~/.hermes` (identity docs) — one of the 12 FI coder seats |
| — | **OpenClaw 🦞AGI (edge twin)** | KVM8 af-forge (100.64.0.2) | pid 123327 · `openclaw-gateway.service` :18789 **ACTIVE** | LIVE — guest bot, AAA only | AAA governance guest | Node.js OpenClaw (NOT hermes-core — identity contract P3: never claims Hermes) |
| — | **FORGE 🔥 (opencode bot)** | KVM8 | `forge-gateway.service` DISABLED (dual-token risk — see doctrine) | dormant by design | DM tool interface | opencode bot.py |

KVM8 `hermes-asi-gateway.service` is **masked** — deliberate: the gateway was moved to KVM4 (workshop = EXECUTION SOT). Masked ≠ broken.

## 2. Linkage graph (who talks to whom)

```
                    ┌──────────── KVM8 af-forge (TRUTH/COURT) ────────────┐
                    │ kernel :8088 · FED HAProxy :4000 · organs :7071-:18085 │
                    │ A2A :3001 (aaa-a2a) · VAULT999 · NATS · FRAME         │
                    └───────▲──────────────▲──────────────▲────────────────┘
                            │ MCP (all organs)     │ FED hairpin      │ FED (via af-forge-fed)
              ┌─────────────┴───────┐   ┌────────┴────────┐  ┌───────┴──────────────┐
              │ H1 Hermes ASI 💃     │   │ FED litellm      │  │ H2 Hermes Azwa       │
              │ KVM4 ~/.hermes v35   │──▶│ KVM4 :4000       │  │ KVM2 ~/.hermes 0.20.1│
              │ + arifos-public MCP  │   │ (binds .5 only)  │  │ + arifosmcp FORK     │
              │                      │   └────────▲─────────┘  │   127.0.0.1:8080 (NOT │
              └──────────────────────┘            │            │   the judge) + hound  │
                          model i-arif ───────────┘            └──────────────────────┘
   H3 (KVM8 CLI seat) ──uses──▶ kernel :8088 + all organs directly (local MCP)
   OpenClaw 🦞AGI (KVM8 :18789) ──▶ federation edge (A2A bridge, audit, browser)
```

- **H1 → organs**: MCP wired to `arifos` (kernel :8088 + public), `aforge`, `geox`, `wealth` (+ more in cfg) — full federation reach from the sovereign gateway.
- **H1 model path trap** (fixed 2026-09-03, cfg note): local `127.0.0.1:4000` retired → now `http://100.64.0.5:4000/v1`; but the CHAT path still hairpins KVM4→KVM8:4000→KVM4 litellm — **KVM8 is mesh SPOF for H1's brain** (MACHINE_MAP §2).
- **H2 isolation is deliberate**: KVM2's `arifOS` MCP = `127.0.0.1:8080` = the arifosmcp **FORK** (Azwa lane), NOT the KVM8 judge. H2 reaches KVM8 only through FED (model tokens) — no kernel authority. Witness-lane doctrine.
- **H2 Nusantara substrate**: ILMU AI + SEA-LION AI + Xiaomi MiMo (SG) — the only instance with regional-model grounding.

## 3. Identity chain

- **WHO Hermes is**: `~/.hermes/HERMES_IDENTITY.md` (KVM8 copy) — "agentic intelligence mirror of ARIF… reflects, does not decide"; boundaries: no judge, no self-authorize, no irreversible exec, no VAULT999 writes, no veto override. Repo doctrine: `~/.hermes/FEDERATION_ROLE.md` (AAA-registered, arifOS-governed, separate repo).
- **Bot identity contract (P3)**: ASI💃=@ASI_arifos_bot=Hermes · 🦞AGI=@AGI_ASI_bot=OpenClaw · 🔥FORGE=@arifOS_bot=opencode. One token = one process (P1). SSOT tokens: `kunci-mas.env`.
- **A2A cards**: `a2a-server/agent-cards/extensions/hermes-asi.json` (baseUrl `https://aaa.arif-fazil.com/a2a/hermes-asi`, identity_anchor `/root/HERMES/SOUL.md` ⚠ KVM8 heritage path), `hermesarifos-bot.json` (archive bot, Gateway 4).
- **Heritage on KVM8**: `/root/HERMES` (4.6G, reclaim-gated) + `/root/Hermes` (164K receipts-only shadow — case-twin trap, MACHINE_MAP §3).

## 4. Stale-metadata fix (this probe)

`reality.py` KNOWN said `openclaw-gateway` `expected_kvm: KVM2` — **wrong**, it runs on KVM8 (verified pid + unit). Fixed to KVM8 with evidence. This was a root cause of the (now-cleared) `duplicate-classify-hermes-openclaw` attention item: two telegram runtimes on one box is CORRECT per doctrine (different bots, different cores).

## 5. Open fleet gaps (honest)

1. **H3 seat ↔ H1 gateway memory split**: CLI sessions on KVM8 and gateway conversations on KVM4 do not share conversational memory (both lean on kernel L1–L6 for federation memory — conversation-local memory is per-home).
2. ~~H1 SOUL.md anchor~~ **RESOLVED 2026-09-04**: SOUL unified to KVM4 canonical (13257B, one inode across KVM8 twins; backup cron-migration-20260904/SOUL.kvm8-preUnify.md); a2a anchor → `/root/.hermes/SOUL.md` (same path both machines).
3. **KVM2→KVM4 :4000 TCP blocked** (ICMP OK) — H2 cannot use KVM4 litellm directly; forced through KVM8 FED. Mechanism UNKNOWN (docker iptables or ts ACL).
4. ~~Cron schedulers~~ **RESOLVED 2026-09-04 (F13 'go')**: 9 sovereign rituals migrated KVM8→KVM4 gateway book (validator adds[] extension, receipts 20260904-001536/001732); dream-dupe retired; scheduler live. `now` reads KVM4. REMAINS: 19 script-bound jobs orphaned on KVM8 — Phase-2 system-cron conversion decision. H2 (KVM2) cron: 1 job, disabled — witness lane, quiet by design.
