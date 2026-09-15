# A2A Enablement — Handoff Packet for OpenClaw (KVM4) + Hermes (KVM8)
> Status: DRAFT_2026-09-15 — lane work, awaiting F13 review (housekeeping consolidation)

**Prepared:** 2026-09-15 · **Status:** DRY-RUN ONLY — NO MUTATION APPLIED
**Verified by:** Hermes (KVM8), read-only probes
**F13 gate:** YES — agent-addressable surface = authority question

---

## 0. Correction first — one "finding" on the stack is FALSE

**"10 missing API keys / most of brain unattached" — FALSE POSITIVE. Do not provision anything.**

The warning came from running `openclaw plugins list` **over SSH without the systemd env**.
The interactive CLI process had no env; the gateway service does.

Live proof — gateway PID 193766 environment:

| Key | Live gateway process |
|---|---|
| DEEPSEEK_API_KEY | SET |
| OPENROUTER_API_KEY | SET |
| GEMINI_API_KEY | SET |
| KIMI_API_KEY | SET |
| LITELLM_MASTER_KEY | SET |
| GROQ_API_KEY | SET |
| SEA_LION_API_KEY | SET |
| CEREBRAS_API_KEY | SET |
| OPENCLAW_HOOKS_TOKEN | SET |

Loaded from: `/etc/systemd/system/openclaw-gateway.service.d/10-keys.env`
(+ `vault.flat.env`, `tokens/openclaw-runtime.env`).

**Conclusion: no provisioning needed. Remove from stack. No F13 spend.**

Lesson: a warning emitted by a tool run in the *wrong environment context* is not a
finding. Verify against the **service's** env (`/proc/<gwpid>/environ`), not the CLI's.

---

## 1. Verified facts (read-only)

| Fact | Evidence |
|---|---|
| Module exists, bundled stock | `@openclaw/a2a` v2026.9.4, `dist/extensions/a2a/`, 76K |
| Ships dormant | manifest `"activation": {"onStartup": false}` |
| It is a **channel** plugin | `categories: ["channels"]`, `channels: ["a2a"]` |
| **No `port` field** | rides existing gateway :18789 — no new listener |
| Enable format (mirror proven entry) | `"a2a": {"enabled": true}` — same as `anthropic => {"enabled": true}` |
| Current state | `plugins.entries.a2a` = **null** (never configured) |
| Plugin registry | stale: "no longer matches current plugin discovery" (44/74) |

### Channel config schema (`channels.a2a`)

| Field | Type | Notes |
|---|---|---|
| `enabled` | boolean | master switch |
| `advertisedUrl` | URI (http/https) | card URL this node publishes |
| `peers` | object | per-peer `{token, url}` — outbound registry w/ per-peer auth |
| `exposeAgents` | string[] | which agents are reachable inbound |
| `rateLimitPerMinute` | integer | abuse control |
| `replyTimeoutMs` | 5000–600000 | turn budget |
| `configWrites` | boolean | allow peer config mutation — **keep false** |

---

## 2. Proposed change — KVM4 (OpenClaw)

**File:** `/root/.openclaw/openclaw.json`

```jsonc
{
  "plugins": {
    "entries": {
      "a2a": { "enabled": true }        // mirror proven format
    }
  },
  "channels": {
    "a2a": {
      "enabled": true,
      "advertisedUrl": "https://openclaw.arif-fazil.com",  // existing vhost, tailnet-gated
      "exposeAgents": ["default"],
      "rateLimitPerMinute": 30,
      "replyTimeoutMs": 120000,
      "configWrites": false,
      "peers": {
        "hermes": {
          "url": "https://<hermes-a2a-endpoint>",   // TBD after KVM8 side
          "token": "<generated-per-peer-token>"
        }
      }
    }
  }
}
```

Then:
```bash
openclaw plugins registry --refresh    # fixes the stale registry too
systemctl restart openclaw-gateway
```

**Verify after (read-only):**
```bash
curl -s -o /dev/null -w '%{http_code}\n' http://100.64.0.5:18789/.well-known/agent-card.json
ss -tlnp | grep 18789        # confirm still single listener, no new port
```

## 3. Proposed change — KVM8 (Hermes)

**File:** `/root/.hermes/config.yaml`
```yaml
platforms:
  a2a:
    enabled: true
    port: 9900
```
**File:** systemd env (flat.env)
```bash
A2A_PORT=9900
A2A_HOST=100.64.0.2
A2A_PEER_TOKENS=openclaw:<generated-token>
A2A_AGENT_NAME=Hermes ASI (KVM8)
```
Then `systemctl restart hermes-asi-gateway`.

**Fail-closed by design:** `resolve_bind_host()` (security.py:75-85) downgrades to
`127.0.0.1` if no token is present. A remote bind cannot happen without auth.

---

## 4. Constitutional constraints

| Constraint | Rationale |
|---|---|
| `configWrites: false` | peers must never mutate local config |
| `advertisedUrl` over tailnet-gated vhost | reuse existing control-plane gate |
| `exposeAgents` narrow | least authority |
| Per-peer tokens, not shared | identity in audit; revoke one peer without collateral |
| Inbound A2A ≠ command authority | `DISCOVERED ≠ AUTH ≠ JUDGED ≠ EXECUTABLE` |
| Rate limit on | abuse bound |

## 5. Reversibility

Both sides: set `enabled: false` + restart. No VAULT999 write. No data change.

## 6. UNKNOWN — not verified

- Card actually served on enable (not tested; would require mutation)
- Peer handshake end-to-end
- Whether enable needs plugin entry, channel config, or both
- `<hermes-a2a-endpoint>` value — depends on KVM8 enablement first

## 7. Sequencing

1. OpenClaw enables plugin **inert** (`enabled: true` + tight `exposeAgents`, no peers) → observe
2. Confirm card served + no new port
3. Then wire peers both sides with tokens
4. Then test one round-trip

Do NOT enable both sides simultaneously blind — one side at a time, observe between.

---
*No mutation applied. Dry-run only. DITEMPA BUKAN DIBERI*
