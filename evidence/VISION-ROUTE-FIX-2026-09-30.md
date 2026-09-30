# VISION ROUTE — FIX + WIRING · 2026-09-30

> Actor: HERMES (KVM8) · Mode: EXECUTION · Trigger: sovereign order *"Fix this as well"* + *"Guna minimax plan"*
> Outcome: vision LIVE (verified through the tool, in a gateway turn). Primary lane LIVE. litellm router de-staled.

## 1. VISION ROUTE WAS DEAD — ROOT CAUSE

Symptom seen by the agent: every `vision_analyze` call died with
`401 — LiteLLM Virtual Key expected. Received=${FE****KEY}` (LiteLLM masks as first 4 + last 4).

The credential sent on the wire was the **literal string** `${FED_ZEN_KEY}`, not a key.

Chain:

1. `config.yaml → custom_providers[0].api_key: ${FED_ZEN_KEY}`.
2. `gateway.multiplex_profiles: true` (confirmed in config.yaml:500) → the `${VAR}` resolver is
   `agent.secret_scope.get_secret()`, which reads the profile's `/root/.hermes/.env` **only**.
   `FED_ZEN_KEY` was absent from that file → `None`.
3. `hermes_cli.config._env_expand_match` (line ~1612) keeps the raw placeholder when the lookup misses.
   The bare `${VAR}` form logs nothing — only `${env:VAR}` warns — so the failure was silent.
4. The systemd `EnvironmentFile` did hold the name (in `kunci-mas.flat.env`), but that path is not the one the
   scoped resolver reads. This is why the variable looked present while the wire carried a template.

Class check: all 8 `${VAR}` refs in config.yaml cross-checked against `.env` → exactly one missing
(`FED_ZEN_KEY`); the other 7 resolved, which is why only this lane 401'd.

## 2. SECOND DEFECT — STALE ROUTER (found while verifying)

After `.env` was fixed, the seat key authenticated but `hermes-default` returned
`400 Invalid model name passed in model=hermes-default` — even though `/v1/models` listed it and the DB allowlist
contained it. Cause: `litellm-federation` booted **2026-09-29 05:52Z** while its config
`/root/A-FORGE/litellm-config.yaml` was last written **2026-09-29 22:40 MYT**. LiteLLM loads its config at boot,
so the running router served a deployment map that predated the edit. All `/v1/models` entries for a restricted
key echo the key's allowlist, so the model appeared available while the router had no deployment for it.

Effect on reality: the primary lane 400'd on every call and Hermes silently ran on `fallback_providers[0]`
(DeepSeek direct) — the Sep-29 finding repeating: work continues, witness is lost.

Fix: `docker restart litellm-federation` (plain docker restart — deliberately NOT compose, to avoid the
SEARXNG_ORPHAN_NUKE `--remove-orphans` failure class). Health restored in ~21 s; all 21 `os.environ/…` refs in
the config confirmed present in the container before the restart; YAML parsed; 129 deployments; 8 `hermes-default`
rungs. Verified after: `hermes-default → 200`, served `MiniMax-M3`.

## 3. WHAT CHANGED

| # | Change | Reversible by |
|---|---|---|
| 1 | `export FED_ZEN_KEY=…` appended to `/root/.hermes/.env` (mode 0600; backup `.env.bak-fedzen-20260930T093957`) | restore backup |
| 2 | `auxiliary.vision` set: `provider=custom`, `base_url=https://api.minimax.io/v1`, `model=MiniMax-M3`, `key_env=MINIMAX_API_KEY`, `api_key=${MINIMAX_API_KEY}`, `api_mode=chat_completions`, `timeout=120` | `config.yaml.bak-vision-20260930T094*` |
| 3 | `docker restart litellm-federation` | restart again |

`provider: custom` + explicit base_url is deliberate: it short-circuits provider-name resolution, which matters
because the registry's `minimax` overlay is `anthropic_messages` transport while the working path is
OpenAI-compatible `chat_completions`.

## 4. EVIDENCE

- `mmx vision describe` on a synthetic test image → verbatim OCR of all 3 lines + correct colours (MiniMax plan).
- `POST https://api.minimax.io/v1/chat/completions` with `MiniMax-M3` + data-URI `image_url` → 200, served
  `MiniMax-M3`. (`MiniMax-VL-01` → 400 `unknown model`: retired.)
- `vision_analyze` through the gateway tool, in a real turn → read all three lines verbatim and reported the
  colours correctly. **This is the end-to-end proof that the route is live.**
- Seat-key probe on `:4012` before/after: `hermes-default` 400 → 200; no `AuthenticationError` in the gateway
  journal in the 5 minutes after the fix (previously ~every turn).
- Gateways/lanes: `:4013` `health/liveliness` 200; `:4012` 200 after haproxy `rise 2` re-admitted the backend.

## 5. OPEN ITEMS (NOT done — recorded, not hidden)

- `i-arif` now returns `400 Invalid model name` on `:4012` while the seat key's allowlist still lists it — the
  new router config has no `i-arif` deployment. Affects the incident doc's reframing (`model.default: i-arif`).
- The seat key's allowlist still names `i-arif` and `hermes-default`; harmless, but the allowlist and the router
  deployment map are two sources that can disagree silently.
- No scheduled probe yet for: (a) any `${VAR}` in config.yaml that fails to resolve, (b) router-vs-config mtime
  skew, (c) seat-key auth failures. The Sep-29 incident report already carries this as P0; it remains unwired.
- The block-level lesson could not be written into the `hermes-gateway-image-routing` skill — the skill writer's
  security scan classifies any mention of credential file paths as exfiltration and the write was refused. The
  lesson lives here instead, and `kvm8-media-lane-fallbacks` points to this file.

DITEMPA BUKAN DIBERI ⚒️
