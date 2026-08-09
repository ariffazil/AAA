# SOT — Authority Trust Model (arifOS Kernel)

> **Stabilized:** 2026-08-09 after external vault7 probe  
> **Code:** arifOS `tools/session.py`, `runtime/act_token.py`, `runtime/tools.py`  
> **DITEMPA BUKAN DIBERI**

## One sentence

**Who may mutate is not “who said their name” — it is identity proof + authority band, and every envelope field must agree.**

## Authority bands (canonical)

| Band | mutation_allowed | seal_allowed | Who |
|------|------------------|--------------|-----|
| `OBSERVE_ONLY` | **false** | false | Unverified / guest / CLAUDE / HERMES / GROK without crypto |
| `LIMITED_MUTATE` | true | false | Verified harness operators (OPENCLAW, OPENCODE→333-AGI) via localhost Ed25519 auto-sign |
| `FULL` | true | true* | Verified sovereign principal path only |
| `VOID` | false | false | Explicit reject (e.g. sovereign spoof) |

\* Seal mode still F13-gated in `arif_seal`.

## Dual-truth iron rule

```
effective_verdict  ──►  effective_state.mutation_allowed
                   ──►  result.mutation_allowed
                   ──►  session_birth.mutation_allowed
```

**Forbidden:** `effective_verdict=OBSERVE_ONLY` with any nested `mutation_allowed=true`.

**status=completed** is execution only — never constitutional SEAL.

## Localhost auto-identity (OPENCLAW / OPENCODE)

**Intentional** on the VPS under `LOCALHOST_IS_PASSWORD`:

- Kernel process auto-signs challenges with on-disk Ed25519 keys for registered harnesses.
- Traffic reaches `:8088` via Caddy/CF but **terminates on localhost** — kernel sees local keys.
- Band after auto-sign: **LIMITED_MUTATE** (not FULL, not SOVEREIGN) for operators.
- **Not** a password; **is** host-bound key possession.

**Not intentional for:** claiming `F13` / `ARIF FAZIL SOVEREIGN` without signature → **VOID** + `SOVEREIGN_SPOOF_ATTEMPT`.

## Guest sessions

- Prefix: `GUEST-<hex>` (never `SEAL-guest-…`)
- No SCT, mutation_allowed=false

## External auditor expectations

External Claude without crypto:

| Claim | Kernel |
|-------|--------|
| actor=CLAUDE | OBSERVE_ONLY, mutation false everywhere |
| actor=OPENCLAW | LIMITED_MUTATE if auto-sign works (host keys) |
| actor=ARIF FAZIL F13… | VOID spoof |
| free-text SEAL in judge | HOLD |

## Fixes landed 2026-08-09

1. Removed KC8 test hardcode `authority_override=FULL`  
2. Envelope reconciliation after `_project_light`  
3. Auto-sign uses `classify_actor_band` (agents ≠ SOVEREIGN_PRINCIPAL)  
4. `identity_band_authority` → LIMITED_MUTATE for verified non-sovereign  
5. Guest prefix `GUEST-`  
6. Sovereign spoof → VOID  

## Operator policy (Arif)

If public MCP must never elevate OPENCLAW without network ACL:

- Keep Cloudflare Access / allowlist on mutation-capable clients, **or**  
- Disable auto-sign via future flag (not default until you decide).

Default 2026-08-09: **localhost key auto-sign = LIMITED_MUTATE for harness VIP names; envelope fields must not contradict.**
