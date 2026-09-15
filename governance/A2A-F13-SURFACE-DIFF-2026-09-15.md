# A2A F13 SURFACE DIFF — Decision Artifact for ARIF
> Status: DRAFT_2026-09-15 — lane work, awaiting F13 review (housekeeping consolidation)

**Prepared:** 2026-09-15 · **Status:** LIVE ON KVM4, PENDING F13 RULING
**Verified by:** Hermes (KVM8), read-only probes from both nodes
**Author of change:** sibling Hermes session `20260914_234522_46d3d6`
**NOT authored by:** this session, OpenClaw

---

## 1. What is live right now on KVM4

```jsonc
// /root/.openclaw/openclaw.json
"plugins": { "entries": { "a2a": { "enabled": true } } },
"channels": {
  "a2a": {
    "enabled": true,
    "advertisedUrl": "http://100.64.0.5:18789",
    "exposeAgents": ["main"],
    "rateLimitPerMinute": 30,
    "replyTimeoutMs": 120000,
    "configWrites": false,
    "peers": { "hermes": { "token": "<48-char, plaintext>", "url": "<TBD>" } }
  }
}
```

Verified live:
```
GET http://100.64.0.5:18789/.well-known/agent-card.json  → 200  (was 403)
GET http://100.64.0.5:18789/health                       → 200
JSON-RPC endpoint: http://100.64.0.5:18789/a2a/v1
```

Card self-describes as `OpenClaw`, `protocolVersion 1.0`, `capabilities: {streaming:false, pushNotifications:false}`.

## 2. KVM8 side — enabled but deliberately unreachable

```yaml
platforms: { a2a: { enabled: true, extra: { port: 9900 } } }
A2A_HOST: <unset>
A2A_PEER_TOKENS: <unset>
```
```
LISTEN 127.0.0.1:9900  (hermes)   ← localhost ONLY
```

The plugin's `resolve_bind_host()` fail-closed path is holding: no token ⇒ no remote bind.
**KVM4 cannot reach Hermes. The channel is one-way and inert.**

## 3. What is actually exposed (risk surface)

| Surface | Exposure | Reachable from |
|---|---|---|
| Agent card (read) | Public within tailnet | any tailnet node |
| `/a2a/v1` JSON-RPC | **Auth-required** (peer token) | tailnet + valid token |
| Streaming / push | **Disabled** in card | — |
| `exposeAgents` | `["main"]` only | one agent |
| `configWrites` | **false** | peers cannot mutate config |
| Rate limit | 30/min | abuse-bounded |

**Assessment: the configuration is conservative.** Not the blind exposure feared — narrower than my own packet proposed (`["default"]` was invalid; sibling correctly used `["main"]`).

## 4. Rollback target — and a filename trap

```
/root/.openclaw/openclaw.json.bak-a2a-inert-20260914-162917
  size 48223 · valid JSON · 20 top-level keys · occurrences of "a2a": 0
```

**The file named "…a2a-inert…" contains NO a2a config at all.** It is a **pre-A2A** backup, not an inert-A2A backup. The name is misleading.

Rollback to dormant is therefore clean: restore this file + restart, or simply set `enabled: false` on both the plugin entry and the channel.

## 5. Constraints respected

| Constraint | Status |
|---|---|
| No new inbound port | ✅ rides :18789 |
| Tailnet-bound, not public | ✅ `100.64.0.5`, Caddy public path returns 410 |
| `configWrites: false` | ✅ |
| Narrow `exposeAgents` | ✅ `["main"]` |
| Reversible | ✅ backup + `enabled:false` |

## 6. Open items

- **Token in plaintext in two places** on KVM4 (`openclaw.json` + `a2a-peer-token-hermes.txt`), and leaked into KVM8 `state.db` by this session. **Rotation required before Hermes-side wiring.**
- `peers.hermes.url` unset — the peer entry is incomplete; outbound direction not yet configured.
- Round-trip untested (requires Hermes-side wiring, which requires this ruling).

## 7. Decision

**ACCEPT** — keep it live; Hermes side then wires with a *fresh* token (never the leaked one), and Arif picks the restart window (all gateway sessions drop briefly).
**REVERT** — `enabled: false` on plugin entry + channel, restart, back to dormant. Clean and immediate.

---
*Read-only verification. No mutation performed by this session.*
*DITEMPA BUKAN DIBERI*
