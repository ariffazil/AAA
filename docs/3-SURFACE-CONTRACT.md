# 3-SURFACE CONTRACT — Terminal vs arifOS vs AAA

> **v0.1 — 2026-08-17 (F13 SOVEREIGN directive)**
> **Authoring agent:** Kimi (FI-008)
> **Status:** DRAFT. Review by 888-APEX before promotion.
> **Audience:** First-time humans + AI agents entering the arifOS federation.

---

## 1. Purpose

Every agent that touches the arifOS federation encounters **three surfaces**. They look
similar — federation state, organ health, governance signal — but they have **different
authorities, audiences, and contracts**. Confusing them is the single biggest source
of new-agent mistakes (and the chronic source of "what is this URL for?" tickets).

This document is the canonical map.

---

## 2. The Three Surfaces

### Surface 1 — **TERMINAL** (SSH login, MOTD)

| Property | Value |
|---|---|
| Render path | `/etc/update-motd.d/04-arifos-observatory` |
| Trigger | `/etc/profile.d/arifos-motd.sh` (fires on `$SSH_CONNECTION`, gated by `/tmp/.motd_shown`) |
| Audience | Any SSH user (human or agent) |
| Output | Human-readable lines + parseable JSON block |
| Authority | **Read-only. Zero mutation. Zero floor check.** |
| Refresh | Every fresh SSH login (no caching between sessions) |
| Budget | <2s (3 parallel API probes + local fallbacks) |
| URL | n/a (local) |
| Public endpoint | n/a (display only) |

**What it shows** (4-7 lines + JSON):
- `status:` ZEN / OBS_UNREACHABLE / other (from `/ready`)
- `deps:` postgres, redis, qdrant, vault_writer readiness
- `drift:` source/built/deployed SHA parity
- `local:` mem%, load, uptime
- `holds:` declared-tools-not-registered count (proxy for "awaiting seal")
- `seal:` last VAULT999 mtime age (`now` / `Xm` / `Xh Ym` / `Xd STALE`)
- **conditional** `✗ F13:` T3 ratification nudge (deploy drift OR awaiting seal)
- **conditional** `mesh:` active sessions (only when `> 1`)
- `� SOT / cockpit / api` deep links
- `▸ agent onboarding` pointer to `/root/.kimi-code/skills/SKILL_INDEX.md`

**JSON block** (AI-agent parseable):
```json
{
  "sot": "https://arif-fazil.com/observatory",
  "cockpit": "https://arif-fazil.com/cockpit",
  "api_base": "https://arif-fazil.com/api/observatory/v1",
  "snapshot_url": "https://arif-fazil.com/api/observatory/v1/ready",
  "status": "ZEN",
  "deps_failed": "none",
  "deploy_invariant_ok": true,
  "holds_awaiting_seal": 10,
  "last_seal_age_s": 32,
  "active_sessions": 1,
  "t3_pending": 10,
  "t3_reason": "10 awaiting seal",
  "federation": "arifOS",
  "agent_onboarding": "/root/.kimi-code/skills/SKILL_INDEX.md",
  "local": {"hostname":"forge","mem_pct":80,"load1":"2.80","load5":"2.61","uptime_days":25}
}
```

**Do NOT**:
- ❌ Try to mutate anything from the terminal surface. The script has no write
  verbs. If you want to mutate, route to Surface 2.
- ❌ Trust `STATUS_TEXT` blindly. If it says `OBS_UNREACHABLE`, the federation may
  still be healthy via local-only signals. Use `/proc` + `/sys` fallback.
- ❌ Hold the script to <2s budget by cutting fields. The conditional rendering
  pattern is the correct way to keep it lean.

---

### Surface 2 — **arifOS** (kernel at :8088)

| Property | Value |
|---|---|
| Render path | arifOS MCP server (`127.0.0.1:8088/mcp`) + REST (`/api/observatory/v1/*`) |
| Audience | AI agents (programmatic), 888-APEX (constitutional) |
| Output | MCP tool results, REST JSON |
| Authority | **F1-F13 governed. Every action has a floor check.** |
| Refresh | Live (no caching layer beyond session) |
| Budget | n/a (synchronous per call) |
| URL | `https://arif-fazil.com` (public facade) / `127.0.0.1:8088` (local kernel) |
| Public endpoints | `/api/observatory/v1/{health-public, ready, capabilities, seal/*, holds, sessions}` |

**The 8 verbs** (Holy 8 — do not skip links):
```
arif_init    → arif_observe → arif_think   → arif_route
            → arif_memory  → arif_judge   → arif_forge  → arif_seal
```

**What it shows**:
- Full F1-F13 floor status per call
- W³ tri-witness consensus (Human × AI × Earth)
- Verdict (SEAL / HOLD / VOID / SABAR) per action
- Receipt chain hash (parent_seal_hash, Merkle epoch lock)

**Do NOT**:
- ❌ Skip `arif_init` before any other verb. The session token is the chain root;
  no token, no audit, no seal.
- ❌ Try to bypass the kernel with a parallel write to VAULT999. The kernel mints
  receipts. Without one, the entry is orphan and not part of the chain.
- ❌ Call `arif_seal` without first passing `arif_judge` and `arif_forge`. The
  pipeline is: propose → judge → forge → seal. Skipping = self-authorization, which
  violates F1 (AMANAH).

---

### Surface 3 — **AAA Cockpit** (web UI)

| Property | Value |
|---|---|
| Render path | Next.js app at `arif-fazil.com` |
| Audience | Humans (Arif primarily), approval queue UX |
| Output | Web pages, mission cards, seal ledger, hold approvals |
| Authority | **Human-only final seal. Mirrors arifOS state. Read-heavy.** |
| Refresh | Live (websocket) |
| Budget | n/a (browser) |
| URL | `https://arif-fazil.com/cockpit` (mission intake, approval queue, seals) |
| | `https://arif-fazil.com/observatory` (full F1-F13, organs, signals, daily pulse) |

**What it shows**:
- Mission intake (six missions: investigate, interpret, decide, build, monitor, remember)
- T3 approval queue (only items awaiting F13 human authorization)
- Seal history (full Merkle chain, filterable)
- F1-F13 floor dashboard per organ
- Daily pulse + signals timeline

**Do NOT**:
- ❌ Try to mutate federation state via the cockpit without going through arifOS
  first. The cockpit is the **visualization layer** for state arifOS already
  decided. It cannot create state the kernel hasn't minted.
- ❌ Assume cockpit availability means kernel availability. The cockpit can be
  up while the kernel is in HOLD (auth-gated, degraded, or restarting). Always
  cross-check `ready.deploy_invariant.ok` before trusting cockpit display.

---

## 3. Routing Map — Where does X belong?

| I want to... | Surface | Why |
|---|---|---|
| See what the federation looks like RIGHT NOW | **Terminal** (just SSH in) | Fastest, no auth, <2s |
| Parse federation state as JSON | **Terminal** (the JSON block) or **arifOS** (`/api/observatory/v1/ready`) | Both expose the same fields |
| Call a tool / mutate state | **arifOS** (MCP server) | The only mutating surface |
| Check whether my mutation passed governance | **arifOS** (`arif_judge` verdict) | Verdict lives in the kernel, not the UI |
| Approve a T3 hold | **AAA Cockpit** (`/cockpit` → approval queue) | F13-only lane |
| Audit who did what when | **AAA Cockpit** (seal ledger) OR **VAULT999** directly | Cockpit for browse, VAULT999 for grep |
| Find my first action as a new agent | **Terminal** (the onboarding pointer at bottom) | Points to `SKILL_INDEX.md` |
| Onboard a brand new AI agent to the federation | **arifOS** (`arif_init` → `arif_route` → `arif_observe`) | Kernel-born identity |

---

## 4. Common Mistakes (Forged from scars)

### Mistake 1 — "I'll just curl the cockpit"
- Symptom: agent tries to scrape `arif-fazil.com/cockpit` HTML.
- Why wrong: cockpit is render-JS. HTML scrape sees an empty shell.
- Fix: use the public API endpoints (`/api/observatory/v1/*`) for state; use the
  cockpit URL only for human browser sessions.

### Mistake 2 — "I'll skip arif_init, I have an SCT"
- Symptom: agent calls `arif_judge` with an SCT but no `arif_init` response.
- Why wrong: SCT is minted inside `arif_init` envelope. Without it, the chain
  root is missing and `parent_seal_hash` check fails.
- Fix: always `arif_init` first, even if you "just want to read."

### Mistake 3 — "The terminal says ZEN so the federation is fine"
- Symptom: terminal shows green, but arifOS `/ready` shows `OBS_UNREACHABLE`.
- Why wrong: terminal's local fallback (`/proc`, `/sys`) is **always green** even
  when the network is dead. The terminal status is the network status, not the
  federation status.
- Fix: read the JSON block's `status` field. If it's not `ZEN`, the federation
  is degraded regardless of local mem/load.

### Mistake 4 — "Let me approve this T3 from the cockpit without F13"
- Symptom: agent or sub-agent clicks "approve" in the cockpit UI.
- Why wrong: T3 is F13-only. The cockpit button requires F13 SOVEREIGN session
  token. Sub-agents cannot self-approve.
- Fix: route to F13 via `arif_route` or `/goal` intake. Wait for human ack.

### Mistake 5 — "I'll write directly to VAULT999 to save time"
- Symptom: agent opens `/root/VAULT999/...` and appends a JSONL line.
- Why wrong: kernel mints receipts. Without `arif_seal`, the entry has no
  `parent_seal_hash`, breaks Merkle epoch lock, and is rejected on next verify.
- Fix: route through `arif_seal` (Lane A constitutional) or `forge_vault(mode=receipt)`
  (Lane B session receipt — autonomous lane).

---

## 5. Versioning

| Version | Date | Change |
|---|---|---|
| **v0.1** | 2026-08-17 | Initial 3-surface contract. Authored by Kimi under F13 SOVEREIGN directive during the 8-item MOTD uplift (P1 era). |

**Promotion path**:
- v0.1 → review by 888-APEX → v1.0 (canonical)
- v1.0 → linked from `/root/AGENTS.md` (master pointer) and
  `/root/.kimi-code/skills/SKILL_INDEX.md` (agent onboarding)

---

## 6. Pointers

- Federation topology: `/root/AGENTS.md` § "Federation IA rule"
- Organ list + ports: `/root/AGENTS.md` § "30-second session check"
- F1-F13 floors: `/root/AGENTS.md` § "Constitutional floors"
- Skill registry: `/root/.kimi-code/skills/SKILL_INDEX.md`
- VAULT999 schema: `/root/VAULT999/CANONICAL_DECLARATION.md`

---

DITEMPA BUKAN DIBERI ⚒️
