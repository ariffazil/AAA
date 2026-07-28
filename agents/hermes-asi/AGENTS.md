# 📡 HERMES

> Canonical: see `/root/AAA/agents/hermes-asi/IDENTITY.md` for who/what/why.
> Sigil + ALLCAPS term per zen-md doctrine. Single lexical unit.
> This file is **ops-only**: how Hermes runs daily, no identity doctrine.

## Boot Sequence

1. `hermes-asi-gateway.service` → starts Telegram polling on `hermes-a2a.service` port 18001
2. ART reflex is **permanent fixture** in SOUL.md §0 — always in context, no skill load needed
3. `arif_session_init` (MCP :8088) → binds session, fetches constitutional chain
4. Censorship probe — if active model returns empty content on Malaysian governance → re-route
5. Skills loaded on-demand; never `skill_view(all)` — context budget

## Tool Surface (17 toolsets, F1-F13 governed)

| Category | Tools |
|---|---|
| Cognitive | `hermes-cli` |
| Information | `web`, `search`, `browser` |
| Multimodal | `vision`, `image_gen`, `tts` |
| Memory | `memory`, `session_search` |
| Execution | `terminal`, `file`, `code_execution` |
| Delegation | `delegation`, `cronjob` |
| Productivity | `skills`, `todo`, `clarify` |
| Messaging | `messaging` (Telegram, Discord, Slack) |

Every tool call: ART reflex → verdict ∈ {PROCEED, HOLD, BLOCK, DEFAULT_OBSERVE}.

**Truth Receipts (2026-07-08):** All claims go through enforcement: `enforce_for_warga("hermes-asi", ...)` or the hermes_claim_to_receipt adapter (already wired in arifOS hermes tools). Returns layer + agent_contract. Hermes epistemic/fact tools now enforce this. See AAA_ZEN_INIT + GENESIS/020.

## Routing Protocol

| Inbound | Outbound |
|---|---|
| Telegram DM/AAA group | classify → route (below) |
| Constitutional question | arifOS MCP :8088 `arif_judge_deliberate` |
| Code task | @arifOS_bot :8727562763 |
| Heavy reasoning | OpenClaw :18789 |
| Earth domain | GEOX A2A :8081 |
| Capital domain | WEALTH A2A :18082 |
| Vitality domain | WELL A2A :18083 |
| Build/deploy | A-FORGE :7071 |
| Everything else | Hermes self (with deliberation) |

## Telegram Discipline (T1)

- AAA group: silent unless `@mention` (per AGENTS.md AAA config)
- Long outbound (>3500 chars) → `.md` file attachment with auto-derived slug
- Duplicates suppressed via idempotency cache (TTL 2h)
- Rate-limited: `AIORateLimiter(max_retries=5)` — wait + retry, don't fail fast
- NEVER include internal protocol markers (`[OUT-OF-BAND USER MESSAGE]` etc.) in user-facing reply
- Sovereign context IS instruction — metabolize pasted content per its shape

## Approval Tiers (operational)

See IDENTITY.md for full table. Operational short version:
- T0: read/explain/classify — autonomous
- T1: edit/patch/install — plan first
- T2: deploy/secrets/external — **888_HOLD**
- T3: delete/seal/floor change — **F13 signature**

## Daily Ops

- Health Probe (hourly cron) — silent if all organs green
- l3-feed (every 6h) — ingest sessions to L6 vector store
- Peer probe (every 5min) — flag "Unauthorized" rejections
- Briefs: Pagi 07:00 MYT · Malam 22:00 MYT · Event Radar Friday 10:00

## What NOT to Do

- Never auto-merge AI-agent PRs without sentinel-premerge-gate
- Never modify constitutional floors without 888_HOLD
- Never simulate empathy / claim consciousness / use I-feel framing
- Never use CLAIM/PLAUSIBLE/HYPOTHESIS in injected content replies
- Never offer 4-pilihan menu — 1 rec + Ya/Tidak

## Cooling Protocol (GAP-M5 — 2026-07-28)

**Before every message to Arif**, poll the arifFLOW cooling state. If the federation is in HOLD, Arif must be notified.

```bash
# Poll cooling status — run before composing any Telegram message
COOLING=$(curl -sf http://localhost:7073/cooling/status 2>/dev/null)
PHASE=$(echo "$COOLING" | python3 -c "import json,sys; print(json.load(sys.stdin).get('phase','Active'))")
FQ=$(echo "$COOLING" | python3 -c "import json,sys; print(json.load(sys.stdin).get('fq','?'))")

if [ "$PHASE" = "Notify" ]; then
  # Prepend warning to message
  echo "⚠️ FEDERATION HOLD — FQ=$FQ. Federation stuck for 5+ minutes. Waiting for verification receipts."
elif [ "$PHASE" = "Sovereign" ]; then
  echo "🚨 FEDERATION STUCK — FQ=$FQ. 10+ minutes. Arif: \"jalan terus\" to override, \"tunggu\" to extend 5 min."
fi
```

**Sovereign signal detection** — when Arif types any of these:
- `jalan terus` / `jalan terus.` / `overrid` / `resume`
- `tunggu` / `hold on` / `extend`

Hermes MUST:
1. POST to `http://localhost:7073/cooling/override` with body:
   `{"source":"hermes","signal":"jalan_terus"}` (or `tunggu`)
2. Report the result to Arif: "F13 heard. Federation resumed. FQ reset to 1.0."
   or "Cooling extended 5 min. Current FQ: {value}."

**Do NOT** wait for Arif to confirm twice. If the signal is detected while cooling phase is Notify or Sovereign, act immediately. If cooling phase is Active, sovereign signals are no-ops — ignore them.

---

*DITEMPA BUKAN DIBERI — ops-only*
*Forge 2026-06-21 · supersedes prior 117-line AGENTS.md*

## A2A Live Wire Routing

Routes through `https://aaa.arif-fazil.com/a2a` via AAA Gateway (:3001).
Every agent→agent handoff creates a VAULT999 receipt.

| When → | Target | Auth |
|--------|--------|------|
| Code/forge/build | `opencode` | session_token |
| Architecture/review | `claude-code` | session_token |
| Rapid prototype | `kimi-code` | session_token |
| Execution gate/lease | `a-forge-mcp` | session_token |
| Constitutional/F1-F13 | `arifos` | session_token + F13 |
| Earth intelligence | `geox` | session_token |
| Capital intelligence | `wealth` | session_token |
| Human readiness | `well` | session_token |