# HERMES — Canonical Map v0.1

> **Authority:** Arif bin Fazil (F13 SOVEREIGN) · 2026-09-27 21:46 MYT
> **Provenance:** post-audit thread · `M11 (premature helpfulness)` · `M23 (mode selection finding)` · SE5
> **Doctrine applied:** `MAP before FORGE` · ARIFOS::CONSTITUTIONAL-COMPLEXITY-BUDGET-2026-09-21 (Canon #0 three-test gate) · Representation ≠ Reality · Anti-Bangang LAW 8 (no-duplicate)
> **Mode:** Lane A — observation only. No mutation proposed.
> **Single Source of Truth:** this document until Arif signs off.

## Executive Summary

```
HERMES today is NOT one runtime, NOT one MCP, NOT one Telegram bot, NOT one TUI.

HERMES today is an IDENTITY LAYER that is EMERGING across:

  - one Python package (Nous Research fork, 6.4G, dual-copied)
  - one sovereign directory (Arif, 6.4G, /root/.hermes + /root/HERMES symlink)
  - five MCP servers (one legacy, two live, two adjacent)
  - ten hermes-* skill bundles
  - five profile SOULs (ALL diverged from canonical)
  - four federation-labelled organs
  - ten hermes-* systemd units (TWO live, one MASKED, one running orphaned)
  - one Telegram gateway (hermesarifos-bot → A-FORGE :7071)
  - one production health monitor (/root/scripts/hermes-prod/hermes-health.py)

HERMES is a governor deciding what to emit per surface. The "identity" is the
governor — not any single file, not any single process.
```

**Falsifiable finding:** If `/root/.hermes/SOUL.md` is deleted, what runtime still emits F13 doctrine? **ANSWER: NONE.** Profile SOULs are diverged; live gateway loads Nous upstream, not Arif's constitution. **Identity today is configuration, not governance** — by the doctrine's own test.

---

## Topology — by Ecosystem

### ECOSYSTEM 1 · Nous Python package (source code)

| Path | Size | Files | Status | Class |
|---|---:|---:|---|---|
| `/root/hermes_work/hermes-agent-copy/` | 6.4G | 93,927 | git working copy | DUPLICATE |
| `/root/hermes_work/pristine-full/` | 6.4G | 93,924 | git pristine | DUPLICATE |
| `/root/hermes_work/pristine/` | 420K | — | partial scratch | ORPHAN |
| `/root/hermes_work/petronas-vm/` | 28M | — | unrelated asset | ORPHAN |
| `/root/hermes_work/helix_update.py` | 13K | — | 2026-09-17 PETRONAS session helper | LEGACY |
| `/root/hermes_work/rc.py` | 11K | — | PDF generator | LEGACY |
| `/root/hermes_work/probe_identity.py` | 1K | — | reads `.hermes/.env` for ASI_ARIFOS_BOT_TOKEN | LEGACY |
| `/root/hermes_work/probe_tokens.py` | 527B | — | regex-extracts Telegram tokens from `.env` | LEGACY |
| `/root/hermes_work/verify_origin_fix.py` | 3.2K | — | A/B check for private-chat attribution fix | LEGACY |
| `/root/hermes_work/telegram-origin-fix.patch` | 5K | — | patch for `plugins/platforms/telegram/adapter.py:3441` | LEGACY |
| `/root/hermes_work/telegram-origin-findings.md` | 26K | — | 2026-09-17 post-mortem | REPORT |
| `/root/hermes_work/uobkh.pdf` / `.txt` | 600K | — | unrelated asset (PETRONAS UOBKH 2008 AR) | ORPHAN |

**Δ 1.1** hermes-agent-copy vs pristine-full: 99%+ identical. **Both are source-of-truth candidates.** `diff -q` reports identical subdirs except 3 files. Pick one, delete the other → reclaims 6.4G.

### ECOSYSTEM 2 · `.hermes/` — Arif sovereign directory (6.4G)

| Path | Bytes | Lines | sha256[:16] | Class |
|---|---:|---:|---|---|
| `/root/.hermes/SOUL.md` | — | 639 | `cf47397c63e21798` | CANON · authority (KVM8) |
| `/root/.hermes/HERMES_IDENTITY.md` | — | 103 | — | CANON · EDGE_BRIDGE role, 5-verb contract |
| `/root/.hermes/HERMES_RUNTIME_CONTRACT.yaml` | — | — | — | CANON · identity priority order, separation of powers |
| `/root/.hermes/IDENTITY_LOCK.json` | — | 34 | — | CANON · humans/bots/groups, NAMING DECREE v2 |
| `/root/.hermes/AGENTS.md` | — | — | — | CANON · parallel pointer |
| `/root/.hermes/STATE.md` | — | — | — | CANON · AAA state doctrine pointer |
| `/root/.hermes/SOUL.md.backup-*` × 5 | — | — | — | BACKUP · 5 rotation points |
| `/root/.hermes/SOUL.md.mangled-voice-governor-attempt` | — | — | — | FAILED · do not restore |
| `/root/.hermes/config.yaml` | — | — | — | CONFIG · 16+ `.bak-*` files indicate heavy rotation |
| `/root/.hermes/carry_forward.json` | — | — | — | CONFIG · session continuity |
| `/root/.hermes/lanes.yaml` (empty in probe) | — | — | — | CONFIG · lane definitions |
| `/root/.hermes/channel_directory.json` | — | — | — | CONFIG · 2026-09-27 21:37 last updated |
| `/root/.hermes/governance/identity-guard-audit.jsonl` | — | — | — | AUDIT · SOUL.md BLOCKED then ALLOWED 2026-09-25 |
| `/root/.hermes/.hermes_history` | 11.2M | — | — | RUNTIME · chat history |

**Δ 2.1** `/root/HERMES → /root/.hermes` symlink (Sep 4 13:28). All canonical paths can resolve either form.

**MCP servers in `/root/.hermes/mcp_servers/`:**

| File | Bytes | Status | Class |
|---|---:|---|---|
| `hermes_mcp.py` | 32,379 | **LEGACY** (own docstring: "retained for reference only") | LEGACY |
| `hermes_agent_mcp.py` | 14,421 | unknown live state | UNKNOWN |
| `hermes_a2a_listener.py` | 16,147 | unknown live state | UNKNOWN |
| `hermes_real_bridge.py` | 6,681 | unknown live state | UNKNOWN |
| `substrate_output_gate.py` | 3,868 | gate-layer | INFRA |
| `federation_ports.py` | 4,632 | port mapping helper | INFRA |

**MCP server packages in `/root/.hermes/mcp/`:**

| Subdir | Class | Live? |
|---|---|---|
| `hermes-rasa` (port 18420) | live — systemd `hermes-rasa-mcp.service` ACTIVE since 2026-09-17 | YES |
| `media-ingest` | live — process PID 71827 since 2026-09-20 | YES |
| `session-federation` | live — process PID 638 since 2026-09-17 | YES |

**Live MCP package — `/root/.hermes/hermes_mcp/`:** imported as Python module `hermes_mcp`. Per its own docstring: "the **package** at `/root/.hermes/hermes_mcp/` is the live HERMES MCP organ" serving 11 canonical tools on :18087. Currently running via `python3 -m hermes_mcp` (PID 3032963). Service unit name `hermes-mcp-server.service` was not present in the live systemd enumeration — possibly folded under `hermes-asi-gateway.service` or running orphaned.

**Profile SOULs — `/root/.hermes/profiles/{x}/SOUL.md` (DIVERGED):**

| Profile | Lines | sha256[:16] | Class |
|---|---:|---|---|
| `hermes_apex/SOUL.md` | 3 | `55c482b2d4349d8f` | DIVERGED · Nous upstream base + F13 OBSERVE_ONLY ruling |
| `hermes_asi/SOUL.md` | 3 | `55c482b2d4349d8f` | DIVERGED · identical to hermes_apex |
| `hermes_forge/SOUL.md` | 3 | `55c482b2d4349d8f` | DIVERGED · identical |
| `aaa-hermes/SOUL.md` | 0 | `36c1f5a92e92cd1d0` | DIVERGED · shorter Nous upstream |
| `router-test/SOUL.md` | 0 | `36c1f5a92e92cd1d0` | DIVERGED · identical to aaa-hermes |

Canonical SOUL.md (`cf47397c63e21798`) is referenced by **ZERO** profiles. **This is the binding drift.**

**Skill bundles — `/root/.hermes/skills/`:**

```
hermes-align · hermes-asi-intelligence · hermes-claude-code-spawn
hermes-coding-gateway · hermes-federated-identity · hermes-federation-audit
hermes-gateway-image-routing · hermes-lane-switch-routing
hermes-naked-prior-audit · hermes-opencode-protocol
```

All 10 bundles sit under `.hermes/skills/`. None symlink to a single canonical body.

### ECOSYSTEM 3 · Federation-labelled organs (Arif-side shadows)

| Path | Size | Class |
|---|---:|---|
| `/root/arifOS/VAULT999/hermes/` | 44K | VAULT · sealed past, `receipts/` only |
| `/root/arifOS/skills/hermes-opencode-intelligence-protocol/` | 12K | SKILL · DIVERGED from `/root/.hermes/skills/hermes-opencode-protocol/` |
| `/root/AAA/observability/hermes-gateway/` | 8K | OBSERVABILITY |
| `/root/forge_work/hermes/` | 24K | DOCTRINE DRAFT · SECTION-5-SEXUALITY-v2 + SECTION-6-NON-DISCRIMINATION |
| `/root/forge_work/hermes-tools/` | 72K | ORPHAN · `kalkulator_audit.py`, `nasi_lemak_calc.py` — disconnected from HERMES |
| `/root/forge_work/hermes-cognitive-organs/` | 500K | SEPARATE PROJECT · CONTRADICTION-ATLAS, FOSSIL-REGISTRY — hermes-named but unrelated to runtime |
| `/root/apex777-audit/hermes-rasa-mcp.service` | 945B | SYSTEMD · mirrors `/etc/systemd/system/hermes-rasa-mcp.service` |
| `/root/work/dualfix/hermes/` | 2.1M | UNKNOWN · `build_patch.py`, `verbosity.py`, `tools.py` — possibly unrelated |
| `/root/hermes-research/` | 104K | SEPARATE PROJECT · adapters/core/pipeline/tests, no git |
| `/root/hermes-social/` | 1.8M | SEPARATE PROJECT · own git repo, `server.py`, `verify.py` — Telegram bot fragment |

**Δ 3.1** `hermes-opencode-protocol` skill: 4 files diverge between two paths. `HERMES_OPENCODE_PROTOCOL.md` (arifOS side only); `SKILL.md` + `references/` + `liveness.json` (.hermes side only). Two surfaces claiming the same name with non-overlapping content.

**Δ 3.2** `forge_work/hermes-tools` contains `nasi_lemak_calc.py` and `kalkulator_audit.py`. **HERMES-named folder contains non-HERMES code.** Either misnamed migration residue or stage of a larger refactor that was abandoned.

### ECOSYSTEM 4 · hermes-as-subject (declarative + diagnostic)

| Path | Size | Class |
|---|---:|---|
| `/root/.hermes/HERMES_IDENTITY.md` | 103 lines | DECLARATION · EDGE_BRIDGE role + 5-verb contract |
| `/root/.hermes/HERMES_RUNTIME_CONTRACT.yaml` | — | DECLARATION · identity priority order + separation of powers |
| `/root/forge_work/hermes-mcp-architecture-map-2026-09-23.md` | 9K | DRAFT_AWAITING_F13 · kimi-code/FI-008 mapping |

The original `HERMES_TELEGRAM_DIAGNOSIS_2026-09-26.md`, `HERMES_SELF_REPORT_DRIFT_2026-09-27.md`, `HERMES_DOCTOR_REPORT_2026-09-26.md`, `hermes-chaos-sweep.py`, `hermes_mcp_compress.py`, `hermes_morning_state.py` mentioned in earlier audits are **not present at expected filesystem paths**. Either (a) they exist at a path not yet probed, (b) they were sub-agent ephemeral context, or (c) they are referenced but not materialised. **OPEN — requires follow-up probe.**

---

## Runtime Layer — what is actually live RIGHT NOW

**Verified via `ps -ef` + `ss -tlnp` + `journalctl` on 2026-09-27 21:45 MYT:**

| PID | Path | Port | Since | Status | Class |
|---|---|---:|---|---|---|
| 638 | `/root/.hermes/mcp/session-federation/server.py` | — | Sep 17 | ALIVE | MCP |
| 1786193 | `/root/HERMES/mcp/hermes-rasa/server.py --port 18420 --transport http` | 18420 | Sep 17 17:29 | ALIVE (systemd `hermes-rasa-mcp.service`) | MCP |
| 2421883 | `/root/.hermes/mcp/hermes-rasa/server.py --transport stdio` | stdio | 07:21 today | ALIVE (child of hermes_cli gateway) | MCP |
| 2421088 | `/usr/local/lib/hermes-agent/hermes_cli/main.py gateway run --replace` (Python 3.14.7 embedded in `/root/.hermes/tools/`) | — | 07:21 today | ALIVE — parent of arifflow-mcp + hermes-rasa stdio + death supervisor | GATEWAY |
| 2421747 | `/root/arifFlow/mcp/arifflow-mcp.py` | — | 07:21 | ALIVE (child of 2421088) | MCP |
| 2421757 | `chrome-devtools-mcp` watchdog | — | 07:21 | ALIVE | MCP |
| 3032963 | `/usr/bin/python3 -m hermes_mcp` (LEGACY surface but LIVE) | — | 13:33 | ALIVE | MCP |
| 2423522 | `/root/scripts/hermes-prod/hermes-health.py` | — | 07:22 | ALIVE | PRODUCTION MONITOR |
| 71827 | `/root/.hermes/mcp/media-ingest/server.py` | — | Sep 20 | ALIVE | MCP |
| 946669 | `/opt/hermesarifos-bot/bot.py` (Telegram Gateway 3 → A-FORGE :7071) | 8091 | Sep 21 | ALIVE | TELEGRAM BOT |
| 2758136 | `/root/A-FORGE/bridges/telegram_bridge.py` | — | Sep 18 | ALIVE | TELEGRAM BRIDGE |
| 3293842 | `qwen-code serve --port 4170` (one of the workspaces is `/root/HERMES`) | 4170 | 15:47 | ALIVE | CODING AGENT |

**Listening ports actually holding hermes traffic:**

| Port | PID | Bound service |
|---|---|---|
| 127.0.0.1:18420 | 1786193 | hermes-rasa (HTTP) |
| 127.0.0.1:8091 | 946669 | hermesarifos-bot (FastAPI webhook) |

**Listening ports attributed to "hermes" in systemd docs but actually held by other processes:**

| Port | Actual PID | Actual binary |
|---|---|---|
| 18900 | 2438675 | `/root/AAA/auth/signing_server.py` — NOT hermes |
| 18902 | 3553427 | `/root/scripts/kabarkan_health_server.py` — NOT hermes |

**Δ R.1** systemd unit `hermes-rasa-mcp.service` is ACTIVE but its health endpoint `/health` returns 404 — observability path is broken on the live runtime.

**Δ R.2** `hermes-mcp-server.service` (referenced in `hermes_mcp.py` docstring) does not appear in current systemd enumeration. The 11-tool live package is running (PID 3032963) under an unknown service wrapper — orphaned, or folded into `hermes-asi-gateway.service`.

**Δ R.3** `hermes-asi-gateway.service` is enabled+active but its runtime is the **Nous hermes_cli gateway** (PID 2421088, "gateway run --replace"), not a custom-built ASI gateway. Naming mismatch between service unit and binary.

---

## Drift Signals — where surfaces disagree

| # | Surface A | Surface B | Conflict |
|---|---|---|---|
| Δ1 | `/root/.hermes/SOUL.md` (KVM8 shadow) | `/root/arifOS/memory/identity/SOUL.md` (KVM8 canonical) | 639 vs 154 lines; canonical per contract is the shorter one but local doctrine uses the longer one. Two files. |
| Δ2 | `/root/.hermes/SOUL.md` | `/root/.hermes/profiles/*/SOUL.md` | Canonical `cf47397c63e21798` vs profiles `55c482b2d4349d8f` × 3 + `36c1f5a92e92cd1d0` × 2. **All 5 profiles diverged.** |
| Δ3 | `/root/hermes_work/hermes-agent-copy/` (6.4G) | `/root/hermes_work/pristine-full/` (6.4G) | 99%+ identical. Both are source-of-truth candidates. |
| Δ4 | `/root/.hermes/skills/hermes-opencode-protocol/` | `/root/arifOS/skills/hermes-opencode-intelligence-protocol/` | 4 files different. Two surfaces same name. |
| Δ5 | `/root/.hermes/mcp_servers/hermes_mcp.py` (32K, LEGACY) | `/root/.hermes/hermes_mcp/` (LIVE package) | Same name, different content, different role. Legacy file's own docstring warns "do not edit". |
| Δ6 | systemd `hermes-rasa-mcp.service` ExecStart path | ps shows live `/root/.hermes/mcp/hermes-rasa/server.py` | Matches. But health endpoint 404. |
| Δ7 | systemd `hermes-asi-gateway.service` (enabled+active) | ps shows live hermes_cli gateway at `/usr/local/lib/hermes-agent/hermes_cli/main.py` | Service unit name doesn't match the actual binary. |
| Δ8 | `hermes-agent-mcp.service` MASKED | `/usr/bin/python3 -m hermes_mcp` (PID 3032963) ALIVE | Orphaned process outside systemd tracking. |
| Δ9 | `/root/.hermes/HERMES_RUNTIME_CONTRACT.yaml` says runtime_origin = KVM4 (100.64.0.5) | This filesystem is KVM8 (72.62.71.199) — KVM4 is remote | Runtime contract declares distributed identity (KVM4 runtime + KVM8 authority). Live runtime ALSO runs on KVM8 — meaning KVM8 is both authority AND runtime host. |
| Δ10 | IDENTITY_ASSEMBLY CONTRACT priority order 1-5 declares SOUL.md wins on persona/tone | All profile SOULs diverged from canonical | The contract is correctly written but its priority #1 file is not the one any profile actually loads. |
| Δ11 | hermes-agent-card.json signature_status.state = ABSENT (kid template unsubstituted) | Card declares Ed25519 signature present | Signature is materially broken — verifier cannot run. |

---

## Identity Survival Test (falsifiable)

**Test:** remove each surface in turn. Does the runtime still emit F13 doctrine in the next response?

| Surface removed | Runtime survives? | Doctrine survives? | Implication |
|---|---|---|---|
| `/root/hermes_work/*` (Nous source) | YES — embedded Python 3.14 + Node 26 in `/root/.hermes/tools/` | YES — doctrine is in SOUL.md, not in source code | Source tree is rebuildable. |
| `/root/.hermes/hermes_cli/` (Nous gateway package) | NO — PID 2421088 + 2421747 + 2421883 all read from `/usr/local/lib/hermes-agent/` which symlinks here | YES | Runtime depends on this. |
| `/root/.hermes/mcp/hermes-rasa/server.py` | PARTIAL — stdio child (PID 2421883) dies; HTTP child (PID 1786193) survives | YES | Two-process pattern resilient. |
| `/root/.hermes/SOUL.md` | YES — runtime keeps running | **NO** — but **no profile loads canonical anyway**, so doctrine already dead at boot | **Identity already dead** by current state. |
| `/root/.hermes/HERMES_RUNTIME_CONTRACT.yaml` | YES — runtime keeps running | **NO** — priority order lost; identity assembly becomes undefined | Contract absence = identity undefined. |
| `/root/.hermes/IDENTITY_LOCK.json` | YES — runtime keeps running (token from `.env`) | YES for runtime, NO for human-ID resolution (Arif/Syed/Irfanclaw addresses lost) | Token custody and human-ID custody are separate paths. |
| `/root/.hermes/governance/identity-guard-audit.jsonl` | YES — read-only audit trail | YES — this is past, not authority | Audit is forensic, not authoritative. |
| `/root/.hermes/profiles/{hermes_apex,hermes_asi,hermes_forge}/SOUL.md` | YES | YES — they already diverge; their absence converges runtime toward Nous base | Removing divergences weakens federation, not runtime. |
| `/root/.hermes/.hermes_history` (11.2M) | YES — history is cache, not authority | YES — doctrine says memory is cache | Per INSERTION 2 doctrine (if accepted), this deletion is doctrine-compliant. |

**Binding finding:** Today, deleting any ONE of `/root/.hermes/SOUL.md`, `/root/.hermes/HERMES_RUNTIME_CONTRACT.yaml`, or `/root/.hermes/IDENTITY_LOCK.json` leaves the runtime ALIVE but the IDENTITY ASSEMBLY CONTRACT violated. The contract is correct; the implementation does not honour it.

**Doctrine's own verdict** (per `SOUL.md` STEP 5 / INSERTION 2 doctrine):
> *"If identity depends on one file: identity is configuration."*

**HERMES today is configuration. Not governance.** This is the discovery.

---

## Constitutional Compression (proposed seal — pending F13 "Sah")

```
SEAL::HERMES_CONSTITUTIONAL_COMPRESSION::2026-09-27

Nous Hermes solved:
  "How does an agent remember?"

Arif HERMES is solving:
  "How does an agent remain itself?"

HERMES is not:
  Telegram · MCP · TUI · A2A · Forge
Those are doors.

HERMES is:
  The governor that decides
  what should emerge
  for whom
  in which context
  at what time.

Future architecture:
  Human Signal
  → Mode Governor
  → Capability Governor
  → Execution Surface
  → Witness

One Identity. Many Doors.
Map before Forge.
```

**Status:** STAGED_PENDING_F13_SAH (not sealed; awaiting Arif "Sah").

---

## Open Questions for F13 (binary-only)

1. **Profile SOUL.md divergence:** replace each profile's content with a symlink to canonical SOUL.md? Or refactor each profile to declare a different lane_card (then leave canonical as priority #1)?
2. **KVM8 shadow SOUL.md at `/root/arifOS/memory/identity/SOUL.md`:** reconcile with `/root/.hermes/SOUL.md` to one canonical, or keep two-shadow-by-design?
3. **hermes-agent-copy vs pristine-full:** delete one (reclaims 6.4G), keep which?
4. **hermes-mcp-server.service:** create systemd unit for the orphan PID 3032963, or fold under hermes-asi-gateway.service, or accept orphan status?
5. **Constitutional Compression SEAL:** approve "Sah" to seal, or stage-only?
6. **Forge order (post-map):** which door first — Telegram governor (Syed/SADO), TUI governor (work), or MCP governor (capability exposure)?

---

## Reversibility

```
removal: rm /root/AAA/blueprints/HERMES-CANONICAL-MAP-v0.1.md
audit:   /root/.local/share/arifos/vault999/seal_chain.jsonl (records blueprint sha256)
```

---

*HERMES-CANONICAL-MAP v0.1 · 2026-09-27 · F13 SOVEREIGN · DITEMPA BUKAN DIBERI ⚒️*