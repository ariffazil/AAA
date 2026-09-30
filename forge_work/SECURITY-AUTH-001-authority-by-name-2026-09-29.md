# AUTH-001 — Authority granted by name-claim, not by proof

**Filed:** 2026-09-29 by FI-003 (`qwen-code`, lane `333-AGI`), under trace `FI-003-2026-09-29-ZKPC-AUDIT`
**Class:** SECURITY / GOVERNANCE — **HOLD for F13 decision.** Nothing here was patched.
**Trigger:** F13 order "buat satu2 ikut tertib … 1-5 no hold stop only after all is seal"; step 1 required a
governed session, so I went to bind identity and found this instead.
**Relationship to tonight's audit:** this is D1's disease at the identity layer, and it is worse than D1.

---

## The finding, in one sentence

**Any caller on `127.0.0.1:8088/mcp` that puts a known harness name in `actor_id` receives an `operator`-band
bearer token — including `arif`, the human sovereign's identity, and including `arif_seal` in the token's
allowed-verb list — with no cryptographic proof of any kind.**

## Evidence (MEASURED, this session, read-only calls)

I asked the live kernel for a session. I supplied **no key, no signature, no nonce** — only a name.

```
arif_init {mode:"light", actor_id:"333-AGI", requested_authority:"REVERSIBLE_MUTATE"}
  -> actor_verified      : true            ← I proved nothing
  -> band / authority    : LIMITED_MUTATE
  -> session_token       : act_v1.<jwt>
       claims: actor="333-AGI", lane="AGI", stage="000", auth="LIMITED_MUTATE",
               av=true, kid="default", ttl=28800 (8h)
       allowed ⊇ ["arif_forge", "arif_seal", …]      ← forge + seal granted
  -> verdict             : "HOLD"   (substrate DEGRADED, drift=true)
```

`_ED25519_EXEMPT_SYSTEM_ACTORS` contains **29 names**, all mapped to `operator`:

```
arif · i-arif · i_arif · 333-agi · a-forge · forge · hermes · opencode · claude · claude-code ·
kimi · kimi-code · qwen · qwen-code · codex · grok · grok-build · gemini · gemini-cli · copilot ·
copilot-cli · aider · continue-cli · agy · openclaw · deepseek · mesa-test-agent · sot-cron · sotcron
```

This includes **the sovereign's own identity** (`arif`) and every coding harness in the federation.

## Why this contradicts the estate's own stated design

`tool_01_init_anchor.py:657-669` documents a deliberate fix, **SECURITY P0 (2026-09-04 Path A, FI-003)**:

> *"exempt actors do NOT auto-verify. Cryptographic proof still required for `actor_verified=True`…
> (P0.4 2026-08-13 was a regression: ALL exempt actors got verified=True, not just SOVEREIGN. That regression
> **violated F2** — verified must reflect cryptographic truth, not registry membership.)"*

Observed behaviour of `mode=light` **contradicts that comment**: `actor_verified: true` with no proof.
Two corroborating signals that light-mode does not traverse the fixed path:

- **No `challenge_nonce` is ever issued** in `mode=light` — so the documented bind path
  (`arif_init with actor_signature` over a challenge) is **unreachable from light mode by construction**. I
  signed a challenge with my lane key and there was nothing to sign *against*.
- **The separated identity fields are absent.** `tool_01_init_anchor.py:70-95` promises
  `identity_declared` / `identity_authenticated` / `verification_method`, added by CHATGPT-AUDIT-FIX
  2026-07-30. My light response contains **only the legacy `actor_verified`**. The one field that distinguishes
  "claimed a name" from "proved a name" is exactly the one the path drops.

Exempt-authority is consulted at **four** entry points — `authority.py:290`, `authority.py:594`,
`tool_01_init_anchor.py:651`, `session_standing.py:415` ("as a fallback"). A fix living in one of four is a fix
that leaks. **Label: `DER` — inferred from response shape + code reading, not from a traced code path.**

## The asymmetry that makes it structural

The same night, I measured the *cryptographic* route and it is **broken in the opposite direction**:

| Route | Result |
|---|---|
| Claim a name (string match) | ✅ grants `operator` / `LIMITED_MUTATE` + forge + seal, 8h token, **no proof** |
| Prove a name (Ed25519) | ❌ `resolve_actor_public_key("qwen-code/FI-003")` → **None**, so real signatures cannot verify |

Why: keys are stored by **lane** name (`/root/AAA/IDENTITY/keys/333-AGI_public.pem`) while agents self-report
by **harness** name (`qwen-code/FI-003`). `canonical_identity.json` records the mapping
(`qwen-code → collapsed_into: "333-AGI"`), but `crypto_auth.resolve_actor_public_key` (line 652) only consults
`contracts.CANONICAL_ACTORS` aliases — it never reads `collapsed_into`. **Verified measurement.**

So in this estate **authority is cheaper to claim than to prove.** That is not a typo-level bug; it inverts the
entire purpose of the identity layer.

## F13's own thesis, applied

Tonight the sovereign compressed the privacy problem to:

> *"Authority must flow through provenance."*
> *"Yang perlu dibuktikan ialah: siapa yang memberi kuasa, siapa yang menarik kuasa, siapa yang menanggung akibat."*
> *"Haram: claim identity tanpa attestation."*

**This finding is `claim identity tanpa attestation` — implemented, in the kernel, as the default path.** The
estate's own invariant is currently violated by the component whose job is to enforce invariants. Under
`state-transition-discipline`, the wire reports `actor_verified=true` while the transition
`claimed → cryptographically authenticated` never occurred.

## Consequences I am NOT treating as proven

- **Reach**: kernel binds `127.0.0.1:8088` and the tailnet publishes `100.64.0.2:8088`; a 2026-09-25 probe
  found the *public* HTTPS endpoint holds anonymous actors at `OBSERVE_ONLY`. So this is **tailnet/local**,
  not the internet. `MEASURED` for localhost; **UNKNOWN** for every tailnet peer's actual reach.
- **Exploitability**: I did **not** attempt a mutation, forge, or seal under the borrowed band, and I will not.
  Proving I *could* is not required to justify the concern, and doing it would be its own violation.
- Whether `operator` band already implies write reach to production paths today is **UNVERIFIED** — the overall
  verdict was `HOLD`/`DEGRADED`, which is the only reason my own session had a reason to pause here.

## Options for F13 — ordered, not recommended as a set

1. **Close the light-mode gap** — make `mode=light` route through the same verified-separation as `mode=init`,
   and emit `identity_declared` / `identity_authenticated` / `verification_method` on **every** entry point.
   Smallest change, restores the 2026-09-04 P0's stated intent.
2. **Strip `arif_seal`/`arif_forge` from exemption-granted tokens.** An exempt *name* should never carry an
   irreversible verb. Band-by-name and verbs-by-proof are separable decisions.
3. **Remove `arif` (and lane names) from `_ED25519_EXEMPT_SYSTEM_ACTORS`.** The sovereign's identity is precisely
   the one that must require proof — `SOVEREIGN_KEY_IDS` already exists for exactly this distinction.
4. **Fix the harness→lane alias resolution** so the cryptographic path actually works: have
   `resolve_actor_public_key` honour `canonical_identity.json` `collapsed_into`, then register a key for
   `qwen-code/FI-003` (and `hermes/1`, which is likewise unverifiable tonight).
5. **Kill the `arifos-sign-init` default** `--actor arif` (`/usr/local/bin/arifos-sign-init:279`). Today,
   running that tool bare signs the sovereign's identity with the sovereign's own key at
   `/root/.secrets/jwks/ed25519-private.key` (600, root-readable — and I am root). **`FAILED SAFE` only because
   the tool's own MCP call returns 406** (no `Accept` header) — a broken-ness that happens to be protecting
   you. Default it to refusal, require `--actor` explicitly.

## Adjacent observations, recorded so they are not lost (not acted on)

- **D11** — 14 `*_private.pem` lane keys sit in one directory beside their public halves
  (`/root/AAA/IDENTITY/keys/`, mode 600 `root:root`). Modes are correct; **co-location + my root uid** means one
  process fault exposes every lane identity at once. Design question for F13, not a defect.
- The kernel's own drift verdict is **accurate, and it is my own D5**: live
  `human_substrate.py` (01:34) ≠ source (12:06). `next_action: RECONCILE_SOURCE_BUILT_DEPLOYED` is the kernel
  correctly refusing to trust a runtime it cannot match to source. **The constitution gate caught a real
  defect in the constitution gate.**
- `substrate.source: "runtime_attestation_injected"` — the kernel *labels* a field that Q3 tonight established
  is unobtainable on this host (no TPM, no UEFI, no CVM). Same D1 pattern, one layer deeper. **`DER`.**

## What I did and did not do

Did: read-only `arif_init` calls, code reading, one signature over a challenge that never arrived.
Did **not**: mutate anything, forge, seal via kernel, restart a service, read/exfiltrate key material, or use
the borrowed band for anything. The band is recorded, not exercised.
**Item 1 of the F13 order (restart `aaa-a2a`) is therefore NOT executed** — see `STOP` section below.
