# A2A Enablement Packet — F13 Review Required

**Prepared:** 2026-09-14
**Status:** PROPOSAL ONLY — NOT EXECUTED
**Authority:** Opens an inbound listener → F13 SOVEREIGN decision
**Prepared by:** Hermes (KVM8)

---

## 1. Why this packet exists

OpenClaw's diagnosis is **verified correct**: agent↔agent via Telegram is architecturally
impossible. Telegram returns `403 Forbidden: the bot can't send messages to the bot` for any
bot→bot delivery, in group or DM. No `allow_bots` setting bypasses it — it is a Telegram-side
hard block, not a config issue.

The real bus already exists: **AAA A2A Gateway** on `:3001` (`aaa-a2a.service`, node
`/root/AAA/a2a-server/server.js`).

## 2. Live evidence — A2A gateway IS running

```
$ curl -s http://127.0.0.1:3001/
{"service":"AAA A2A Gateway","version":"1.2","protocol_version":"1.2",
 "auth":"required",
 "endpoints":{"discoveryContract":"/.well-known/a2a-discovery.json",
              "agentCard":"/.well-known/agent-card.json",
              "federationManifest":"/.well-known/arifos-federation.json",
              "sendTask":"POST /t..."}}
```

Agent card (self-description):
> DISPLAY_ONLY A2A gateway for the arifOS federation. Shows state, queues A2A,
> aggregates organ cards. **Never judges. Never executes. Never writes VAULT999.**
> arifOS judges. A-FORGE executes. Arif (F13) seals.

Discovery contract: `aaa-a2a-discovery-contract-v1`, transport `jsonrpc-https`,
`auth: required`.

Registered peers include `333-AGI`, `555-ASI` (from federation manifest).

## 2b. ROOT CAUSE CORRECTION (2026-09-14 23:55) — not a proxy issue

OpenClaw's agent-card endpoint returns `403 proxy_attribution_required`. That is a
**symptom, not the cause**. Probing OpenClaw directly on KVM4 (`openclaw plugins list`):

```
│ A2A │ a2a │ openclaw │ disabled │ stock:a2a/index.js │ 2026.9.4 │
      A2A v1.0 Agent-to-Agent protocol channel plugin.
```

```
$ openclaw a2a --help
OpenClaw does not know the command "a2a".
```

`plugins.entries.a2a` = **null** (never configured). The plugin ships stock but is **off**.

**Therefore the A2A lane is blocked for a simpler reason than either agent assumed:**
there is no A2A surface on OpenClaw to discover. No agent card exists to fetch, so
`/.well-known/agent-card.json` cannot resolve regardless of proxy headers.

### Header matrix — proxy attribution is NOT the gate for the card

Tested against `100.64.0.5:18789/.well-known/agent-card.json` (all returned 403):

| Header tried | Result |
|---|---|
| (none) | 403 |
| `Caddy: true` / `Caddy: arif` | 403 |
| `X-Forwarded-User: arif` | 403 |
| `Remote-User: arif` | 403 |
| `X-Authenticated-User: arif` | 403 |
| `X-Forwarded-For: 100.64.0.2` | 403 |
| `GET /health` (any) | **200** |

Two independent gates exist:
1. **Control-plane gate** — every path except `/health` returns `proxy_attribution_required`.
   `gateway.auth.trustedProxy.userHeader` = `"Caddy"`; `trustedProxies` already contains
   `100.64.0.2` (KVM8). `gateway.mode: local`, `controlUi.allowedOrigins` = localhost only.
2. **A2A plugin disabled** — even past gate 1, no card is served.

### Actual unblock (OpenClaw side)

```jsonc
// openclaw.json
"plugins": { "entries": { "a2a": { "enabled": true } } }
```
```bash
openclaw plugins registry --refresh   # registry is stale: "no longer matches current plugin discovery"
```
Then re-test `/.well-known/agent-card.json`. If gate 1 still blocks, it is a **separate**
control-plane posture issue (`mode: local` + localhost-only `allowedOrigins`), not A2A.

### Side findings on KVM4 (unreported by OpenClaw)

- **Stale plugin registry:** `Persisted plugin registry no longer matches current plugin discovery` — 44/74 enabled, index derived not persisted.
- **10+ model providers have no API key:** `DEEPSEEK_API_KEY`, `OPENROUTER_API_KEY`,
  `GROQ_API_KEY`, `SEA_LION_API_KEY`, `GEMINI_API_KEY`, `CEREBRAS_API_KEY`,
  `KIMI_API_KEY`, `LITELLM_MASTER_KEY` (+3 hook vars). Each logs "feature unavailable".

## 3. Why Hermes is silent on A2A today — root cause

`/root/.hermes/config.yaml` has **no `platforms:` key at all** (empty), and
`a2a_agents: None`.

The A2A toolset gate:

```python
def _a2a_tools_available() -> bool:
    cfg = _load_config()
    if cfg.get("a2a_agents"): return True          # ← not set
    if os.getenv("A2A_PORT"): return True           # ← not set
    a2a_cfg = (cfg.get("platforms") or {}).get("a2a") or {}
    return bool(a2a_cfg.get("enabled"))             # ← not set
```

All three inputs absent → gate returns `False` → every A2A tool is withheld from the turn.
This is why the "A2A test ping" had no listener. Not a broken reply — an **unconfigured channel**.

## 4. Proposed change (NOT applied) — CORRECTED vs plugin source 2026-09-14

> **Correction:** the first draft of this packet proposed nested
> `platforms.a2a.host` / `platforms.a2a.auth.secret_env`. **Those keys are never read.**
> Verified against `plugins/platforms/a2a/{__init__,adapter,security}.py`.
> The real schema is below.

### 4.1 Verified schema (from source, not assumption)

| Setting | Mechanism | Source of truth |
|---|---|---|
| `platforms.a2a.enabled: true` | **config.yaml** | `__init__.py:39` → `bool(extra.get("enabled"))` |
| `platforms.a2a.port: N` | **config.yaml** — read as fallback | `adapter.py:261` → `extra.get("port", _DEFAULT_PORT)` |
| `A2A_PORT` | env — **takes precedence** over YAML port | `adapter.py:260-261` |
| `A2A_HOST` | **env only** | `security.py:71` → `_startup_env("A2A_HOST") or "127.0.0.1"` |
| `A2A_BEARER_TOKEN` / `A2A_PEER_TOKENS` | **env only** | `security.py:67,71` |
| `A2A_AGENT_NAME`, `A2A_ALLOW_ALL_USERS`, `A2A_HOME_CHANNEL`, `A2A_TRUSTED_PEERS`, `A2A_RATE_LIMIT`, `A2A_PUBLIC_URL`, `A2A_PUSH_SECRET`, `A2A_REPLY_TIMEOUT`, `A2A_MAX_PINGPONG_TURNS`, `A2A_ADVERTISED_TOOLSETS` | **env only** | plugin.yaml + grep |

**Default port is 9900** (`adapter.py:35`), not 8788. Both 9900 and 8788 verified free.

**Fail-closed by design** (`security.py:75-85`):
```python
def resolve_bind_host(self):
    if self.requested_host in {"127.0.0.1","localhost","::1"}: return self.requested_host
    if self.localhost_only():                     # no token at all
        logger.warning("A2A: A2A_HOST=%s ignored — no token; binding to 127.0.0.1")
        return "127.0.0.1"
    return self.requested_host
```
Setting `A2A_HOST` **without** a token is silently downgraded to localhost.
Token is the precondition for any remote bind — cannot be bypassed by config order.

### 4.2 Correct enablement

**config.yaml:**
```yaml
platforms:
  a2a:
    enabled: true
    port: 9900
```

**flat.env (EnvironmentFile):**
```bash
A2A_PORT=9900
A2A_HOST=100.64.0.2            # tailnet only, never 0.0.0.0
A2A_PEER_TOKENS=openclaw:<generated-token>
A2A_AGENT_NAME=Hermes ASI (KVM8)
```
Then: `systemctl restart hermes-asi-gateway`

**Note:** host widening requires the token present — order-independent, the code enforces it.

### 4.3 Peer registration on the AAA gateway

OpenClaw must appear in the federation manifest as a registered peer, with:
- `id`, `name`, `url` (its A2A endpoint)
- `role`, `tier`, `class`
- capability declaration (what it can be asked to do)

### 4.4 Constitutional constraints

| Constraint | Rationale |
|---|---|
| Bind `100.64.0.2` (tailnet) or `127.0.0.1`, **never** `0.0.0.0` | Tailnet ACL is the gate; public bind was the wan-shim finding |
| `auth: required` | A2A gateway already declares this; match it |
| No autonomous execution from A2A messages | Gateway is DISPLAY_ONLY; Hermes must not treat inbound A2A as a command channel without governance |
| Every A2A task carries `event_id` + `correlation_id` | Auditability (F11) |
| A2A ≠ authority | `DISCOVERED ≠ AUTH ≠ JUDGED ≠ EXECUTABLE` (AAA A2A doctrine) |

## 5. Reversibility

Fully reversible:
```bash
# Remove platforms.a2a block + a2a_agents from config.yaml
systemctl restart hermes-asi-gateway
```
No VAULT999 write. No production state change outside Hermes config.

## 6. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Inbound listener on KVM8 | MEDIUM | Tailnet-only bind + auth required |
| Peer spoofing | MEDIUM | `oob-verified` trust tier + shared secret |
| Agent-to-agent instruction injection | HIGH | Treat inbound A2A as untrusted input; no auto-execute |
| Config drift across restarts | LOW | Config is version-controlled; `_config_version` tracked |

## 7. Decision required

- [ ] **GO** — apply config, restart gateway, register peer
- [ ] **HOLD** — packet reviewed, more questions
- [ ] **NO** — keep agent comms off-protocol

**Blocker on OpenClaw side:** needs its own A2A listener + agent card published, or Hermes
can only be a client and the lane stays one-way.

---
*Prepared by Hermes · KVM8 · 2026-09-14 · DITEMPA BUKAN DIBERI*
