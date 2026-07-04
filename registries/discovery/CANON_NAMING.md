# AAA Canonical Naming — Hermes / APEX / ASI / MaxHermes

> **Forged:** 2026-06-22 by FORGE (000Ω)
> **Status:** CANONICAL — use these terms exclusively going forward
> **Supersedes:** All pre-2026-06-22 usage that conflated these terms

## Why this exists

Four different things have been called "Hermes" or "ASI" or "APEX" or "MaxHermes"
in AAA docs over the last 6 months. Per F2 TRUTH, this is a clarity violation (F4).
Per Arif's 2026-06-22 directive: **"when I said hermes, I always refer it to
hermes agent by nous research and my bot ASI in my telegram."**

This file fixes the naming. Going forward, every doc, code comment, agent
card, and conversation MUST distinguish these three.

## The three things

### 1. Hermes = Hermes-ASI = ASI (colloquial)

**This is what Arif means when he says "Hermes" in chat.**

The conversational Telegram bot / A2A gateway / Nous Research fork agent.

| Attribute | Value |
|---|---|
| Display name | **Hermes-ASI** (canonical) or **Hermes** (colloquial) |
| Source | Nous Research `hermes-agent` (binary: `/usr/local/bin/hermes`) |
| Fork HEAD | `2517917d` (per `agent-card.json`) |
| Telegram | `@ASI_arifos_bot` |
| A2A | `https://aaa.arif-fazil.com/a2a/hermes-asi` |
| Binary path | `/usr/local/lib/hermes-agent/` |
| Live config | `/root/.hermes/` (note: dot prefix — different from `/root/HERMES/`) |
| AAA agent entry | `/root/AAA/agents/hermes-asi/` |
| systemd services | `hermes-asi-gateway.service`, `hermes-a2a.service` |
| Ports | A2A: 18001 (bridge), 18789 (openclaw gateway), 5002 (memory broker) |
| The "ASI" suffix | Means **"Arif Sovereign Interface"** (per Hermes SOUL.md) — NOT "Artificial Super Intelligence" |
| Use case | Human-facing conversation, Telegram replies, A2A delegation |

### 2. APEX = 888_JUDGE = APEX Prime

**This is what F8 LAW / F13 SOVEREIGN calls the constitutional judge.**

The verdict authority for F1-F13 floors. Decommissioned as a standalone
repo/service; deliberation logic now lives in AAA a2a-server.

| Attribute | Value |
|---|---|
| Display name | **APEX** or **888_JUDGE** |
| Status | **DECOMMISSIONED 2026-06-14** (deliberation absorbed into AAA a2a-server) |
| Legacy repo | `/root/APEX/` (archived on GitHub, branch `apex`) |
| Legacy service | `apex-prime.service` on port 3002 — kept for legacy health probes ONLY |
| Deliberation (live) | `/root/AAA/src/gateway/deliberation.ts` (888-judgment module) |
| Constitutional citizen | `888-APEX` HEXAGON warga (`/root/AAA/agents/888-APEX/`) |
| Use case | Constitutional verdict issuance (SEAL/SABAR/VOID); F1-F13 floor enforcement |
| Distinguishing feature | NEVER a chatbot; NEVER replies on Telegram; only emits verdicts to arifOS kernel |

### 3. 555-ASI = HEXAGON warga

**Constitutional citizen, not a chatbot.**

Memory synthesis + ethical critique agent. Part of F1-F13 enforcement,
not part of the user-facing surface.

| Attribute | Value |
|---|---|
| Display name | **555-ASI** (HEXAGON warga) |
| Class | ASI (here meaning **Artificial Super Intelligence** — class name) |
| Role | Ω HEART — Memory synthesis + ethical critique |
| Skills | 3 (per AGENTS.md) |
| Path | `/root/AAA/agents/555-ASI/` |
| Use case | Constitutional memory + heart critique, invoked by arifOS kernel |
| Distinguishing feature | NOT the Hermes-ASI bot. Same "ASI" string, completely different meaning. |

## The four forbidden confusions

| ❌ Wrong | ✅ Right |
|---|---|
| "Hermes gave a verdict" (talking about APEX) | "APEX gave a SEAL verdict" (use APEX, not Hermes) |
| "Hermes is the judge" | "APEX is the constitutional judge; Hermes is the conversational agent" |
| "ASI means Artificial Super Intelligence" (in Hermes context) | "ASI means Arif Sovereign Interface" (Hermes); "ASI = HEXAGON class" (555-ASI) |
| "/root/HERMES/ is the live config" | "/root/.hermes/ is the live config (with dot); /root/HERMES/ is the DEAD pre-migration dir" |

## What lives where — quick ref

| Path | Status | Refers to |
|---|---|---|
| `/root/.hermes/` | ✅ LIVE | Hermes-ASI bot config (FLOOR: dot prefix) |
| `/usr/local/lib/hermes-agent/` | ✅ LIVE | Hermes-ASI binary |
| `/usr/local/bin/hermes` | ✅ LIVE | Hermes-ASI entry point |
| `/root/AAA/agents/hermes-asi/` | ✅ LIVE | AAA agent card + SOUL/AGENTS docs for Hermes-ASI |
| `/root/HERMES/` | ❌ DEAD | Pre-2026-05-19 dir; never migrated (per README.MIGRATED_TO_APEX.md) |
| `/root/APEX/` | ⚠️ LEGACY | APEX repo, archived; deliberation moved to AAA a2a-server |
| `/root/AAA/agents/888-APEX/` | ✅ LIVE | APEX constitutional warga (888) |
| `/root/AAA/agents/555-ASI/` | ✅ LIVE | 555-ASI HEXAGON warga (memory + ethical critique) |
| `/root/AAA/agents/apex/` | ⚠️ LEGACY | Old APEX agent entry; superseded by 888-APEX |
| `/root/AAA/src/gateway/deliberation.ts` | ✅ LIVE | Where APEX deliberation logic lives NOW |

## Migration status (per 2026-05-19 plan)

The "Migrate HERMES to APEX" plan (see `/root/HERMES/README.MIGRATED_TO_APEX.md`)
**never completed**. What actually happened:

| Step in plan | Reality |
|---|---|
| Rename `/root/HERMES/` → `/root/APEX/` | ✅ Done (May 2026) |
| Move Hermes runtime → `/root/AAA/agents/hermes-asi/runtime/` | ❌ NOT done — runtime stayed at `/root/.hermes/` |
| New Hermes-ASI agent card at AAA | ✅ Done — at `/root/AAA/agents/hermes-asi/agent-card.json` |

Net: APEX rename happened; Hermes-runtime migration did not. The
`/root/HERMES/` directory remains on disk as a leftover, marked STALE
in its own README. Future cleanup should remove it after confirming
no scripts reference it (currently appears unused).

## DITEMPA BUKAN DIBERI

This naming doc is the canonical reference. Any future doc that uses
"Hermes" without distinguishing these three MUST be updated or annotated.

## The fourth thing — MaxHermes (added 2026-06-22)

### 4. MaxHermes = external MiniMax cloud product

**This is NOT under AAA Federation control.** It runs on MiniMax's cloud
infrastructure at `agent.minimaxi.com/max-hermes`, powered by MiniMax M2.7.

| Attribute | Value |
|---|---|
| Display name | **MaxHermes** (external) |
| Source | MiniMax (HKEX: 00100), launched April 16, 2026 |
| URL | `https://agent.minimaxi.com/max-hermes` |
| Default model | MiniMax M2.7 (230B MoE, 10B active) |
| Hosted | MiniMax cloud (we don't control) |
| AAA agent entry | `external/maxhermes/` (documentation only) |
| Distinguishing feature | "Learning loop" — auto-extracts reusable skills from tasks |

### Historical context

Prior to 2026-06-22, AAA had a `agents/maxhermes/` directory with a
fictional "OpenClaw MaxHermes" agent entry describing a local instance
that never actually existed. It was archived to `_archive/maxhermes-2026-06-22/`.

Per Arif's clarification 2026-06-22:
> "MAX HERMES IS ACTUALLY EXTERNAL HERMES IN ANOTHER SERVER THAT I DONT
> HAVE ACCESS TO THE MACHINE"

### Naming distinctions

| Term | Means | Does NOT mean |
|---|---|---|
| **MaxHermes** | MiniMax cloud product (external) | ❌ NOT our agent; ❌ NOT a Hermes variant |
| **Hermes** | Hermes-ASI Telegram bot (our agent) | ❌ NOT MiniMax's product |
| **MiniMax M2.7** | LLM that powers MaxHermes | ❌ NOT the same as MiniMax-M3 (our kernel's primary model when available) |

### Integration (when desired)

If MaxHermes is to be called from AAA in the future:
1. Register MiniMax API key in `/root/.secrets/vault.env`
2. Add a **gateway route** in `aaa-gateway` (NOT a local agent entry)
3. F13 ack required (data flows to external vendor)
4. Witness every call via arifOS MCP

The archived `_archive/maxhermes-2026-06-22/` documents the previous (incorrect) integration attempt.

