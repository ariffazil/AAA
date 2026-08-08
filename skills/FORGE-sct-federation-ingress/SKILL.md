---
name: FORGE-sct-federation-ingress
description: >
  Wire, verify, and operate federation Session Capability Tokens (SCT) across
  arifOS mint/validate and organ ingress gates (A-FORGE, GEOX, WEALTH, WELL, AAA).
  Use when: SCT gate, session_token, federation_sct, SCT_AMBIGUOUS, tool_authority,
  FORGE_SCT_REQUIRE_MUTATE, 65-case matrix, decision event. Now also covers
  ChatGPT App OAuth 2.1 resource-server alignment (RFC 9728 PRM, canonical
  resource identity, per-tool securitySchemes) as the EXTERNAL host ingress
  path alongside the INTERNAL SCT path.
version: 2026.07.20
floors: [F1, F2, F11, F12, F13]
---

# FORGE — SCT Federation Ingress

> **Canonical:** `/root/AAA/governance/federation_sct.py`  
> **Authority registry:** `/root/AAA/registries/tool_authority.py` (tools.yaml)  
> **A-FORGE:** `src/infrastructure/governance/sctIngress.ts`

## SEALED foundation (do not re-implement)

| PR | Law | Commit |
|----|-----|--------|
| **PR1** | Collect-all sources; identical→normalize; distinct→**SCT_AMBIGUOUS** | AAA `056a8c9` |
| **PR2** | action_class from **tools.yaml** only; no caller self-declare | AAA `57217da` |
| **A-FORGE** | Same AMBIGUOUS + production `FORGE_SCT_REQUIRE_MUTATE=0` → **exit(1)** | `1f1779b` |

## Law

```
SCT present     → verify fail-closed (claims required)
No SCT + OBSERVE → allow (registry-owned OBSERVE)
No SCT + MUTATE → SCT_REQUIRED
Conflicting tokens → SCT_AMBIGUOUS, execute nothing
Log fingerprint only (sha256) — never raw SCT
Production mutate bypass → startup FATAL
```

## Mint + gate

```python
import sys; sys.path.insert(0, "/root/AAA")
from governance.federation_sct import gate_tool_ingress
# gate_tool_ingress(tool, args, organ="geox")  # registry sets require_sct
```

## PARKED — next block (after T3a + R4)

| PR | Scope |
|----|--------|
| 3 | Decision-event schema formal seal (scaffold may exist) |
| 4 | `trace_id` across 5 organs |
| 5 | Cockpit filter by trace_id |
| 6 | **13×5 = 65** adversarial matrix, one shared trace_id |
| 7 | VAULT999 rollup receipt |

## ChatGPT App OAuth 2.1 resource-server alignment

> Blueprint contract: `/root/forge_work/2026-07-20/GEOX-CHATGPT-MCP-GUI-BLUEPRINT.md` §8 (auth), PR `pr/geox-auth-resource-alignment`. Exit criteria: auth matrix passes; wrong-audience fails closed.

ChatGPT is an EXTERNAL host. Its OAuth path is parallel to — never a replacement for — the SCT Law above.

### 1. RFC 9728 protected-resource metadata (PRM)

- Serve `/.well-known/oauth-protected-resource` on the GEOX public origin. The document MUST carry:
  - `resource` — the canonical resource URI (§2).
  - `authorization_servers` — at least one entry naming the AS that issues ChatGPT-bound tokens.
- On any `401`, respond with a `WWW-Authenticate` challenge pointing at the PRM URL:
  ```
  WWW-Authenticate: Bearer resource_metadata="https://geox.arif-fazil.com/.well-known/oauth-protected-resource"
  ```
- Without the challenge, ChatGPT cannot discover the AS; without `authorization_servers`, discovery dead-ends. Both are boot-blocking.

### 2. ONE canonical resource identity

Exactly one identity string is the resource. For GEOX v1 it is the HTTPS MCP endpoint:

```
https://geox.arif-fazil.com/mcp
```

All four positions MUST agree byte-for-byte:

| Position | Value |
|---|---|
| MCP endpoint URL | `https://geox.arif-fazil.com/mcp` |
| PRM `resource` field | same |
| OAuth `resource` parameter (auth + token requests) | same |
| Access-token audience validation on the server | same |

Never mix `geox.arif-fazil.com/mcp` with any other identity (no pathless origin, no `forge.*` alias, no localhost) across these positions. Any mismatch = wrong-audience = **fail closed**.

### 3. Per-tool `securitySchemes` + scope map

Every public tool declares `noauth` or `oauth2` + scopes explicitly (silence is not a policy). Blueprint scope table:

| Scope | Covers | v1 exposure |
|---|---|---|
| `geox.read` | read-only evidence tools (profile, status, view) | ChatGPT-allowed |
| `geox.compute` | compute-lane tools (petrophysics, seismic compute, basin math) | ChatGPT-allowed |
| `geox.ingest` | ingest tools (well/seismic ingest) | ChatGPT-allowed |
| `geox.export` | export / publish tools | ChatGPT-allowed |
| `geox.claim.write` | claim lifecycle writes | ChatGPT-allowed |
| `geox.seal` | claim sealing (irreversible) | **WITHHELD from ChatGPT v1 — sovereign-gated per F13** |

`geox.seal` never appears in any ChatGPT-facing scope set, metadata document, or consent screen. Requesting it from the external path is rejected, not deferred.

### 4. Token validation duties (resource server side)

Every bearer token presented to `/mcp` is validated fail-closed on all five:

1. **Signature** — valid against the AS key set.
2. **Issuer** — matches a declared `authorization_servers` entry.
3. **Audience / resource** — equals the canonical identity of §2 exactly.
4. **Expiry** — not expired (no grace window).
5. **Scopes** — token scopes ⊇ the called tool's declared scopes; absent scope = deny.

### 5. Two ingress paths, no weakening

| Path | Principal | Mechanism | Status |
|---|---|---|---|
| **INTERNAL federation** | organ → organ (A-FORGE, AAA, WEALTH, WELL) | SCT mint/validate per the Law above | unchanged, authoritative |
| **EXTERNAL host** | ChatGPT App | OAuth 2.1 + RFC 9728 + scopes | new, this section |

Threading rules:

- An external ChatGPT call authenticated by OAuth does NOT mint, imply, or bypass an SCT. If the requested action class would require SCT internally (`MUTATE`+), the OAuth scope set must independently authorize it — and `geox.seal`-class actions remain F13-gated regardless of token.
- An SCT does NOT satisfy OAuth audience checks; internal tokens are never accepted on the external ingress path.
- One request, one ingress path. Mixed credentials (SCT header + bearer token) are treated like conflicting tokens → reject, execute nothing (same posture as `SCT_AMBIGUOUS`).
- Both paths log fingerprint only (sha256) — never raw tokens.

## Do not

- First-token-wins  
- Trust caller `action_class`  
- Mock arifOS in production gates  
- Advance SE stage from this skill — T3a matrix first (`FORGE-t3a-binding-matrix`)  
- Mix canonical resource identities across endpoint / PRM / OAuth param / audience check  
- Expose `geox.seal` to ChatGPT v1 under any alias or wildcard scope  
- Accept SCT on the external path, or OAuth bearer on the internal path  
