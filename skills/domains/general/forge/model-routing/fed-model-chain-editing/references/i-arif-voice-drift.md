# i-arif Lane — Voice Drift from Fallback Swaps

## Symptom Arif reports

"Apsal hang cakap English ni. Hang pakai model apa ni" — the reply was technically in BM, but the cadence was stiff, telegraphic, headline-like ("Ini bukan X. Ini Y."): Malay that reads like it was translated from English. Arif hears voice drift and suspects a model swap. He is usually right.

## Lane shape (as of 2026-09)

`model.default: i-arif`, `provider: custom:fed-federation` → FED LiteLLM at :4000, config at `/root/A-FORGE/litellm-config.yaml` (mounted to `/app/config.yaml` in container `litellm-federation`).

`i-arif` is an alias with two layers:

1. **Ordered deployments inside the alias** — `order` in `litellm_params`:
   - P1 `openai/qwen3.8-max` (QWEN_INDIVIDUAL_API_KEY), order 1
   - P2 `openai/qwen3.7-plus` (Individual), order 2
   - P3 `openai/qwen3.8-max` (QWEN_HERMES_API_KEY), order 99
   - P4 `openai/qwen3.6-plus` (Hermes seat), order 99
2. **Router-level fallback list** — `router_settings.fallbacks` for `i-arif`. Here is the trap: the list is NOT Qwen-first. It reads deepseek-v4-flash-vision → MiniMax-M3 → mimo-v2.5 → glm-5.3-flash → qwen3.8-max → gemini-3.6-flash. So the moment the Qwen seats 429, the voice switches to a non-Qwen model while Hermes still logs `model=i-arif`.

## Why Hermes logs lie about this

`agent.log` prints `model=i-arif provider=custom` for every call, fallback or not. LiteLLM per-request attribution is unavailable here: the `litellm` DB exists in the `postgres` container but has **no `LiteLLM_SpendLogs` table** (DB spend logging off), so you cannot resolve the upstream model from the DB.

## Diagnosis recipe

1. Confirm the router was degraded at the exact minute of the reply:
   `docker logs --since 30m litellm-federation 2>&1 | grep -iE "429|RateLimit|fallback"`
   Container logs are UTC; Arif's clock is MYT (+08). 00:5x UTC == 08:5x MYT.
2. Cross-check `~/.hermes/logs/agent.log` for the turn: `Turn ended ... model=i-arif ... response_len=N`. Note the response length — over-long replies plus degraded router is the classic pair.
3. Read `router_settings.fallbacks` in `/root/A-FORGE/litellm-config.yaml` to see which voices can substitute.

## Fix

Keep the `i-arif` fallback list Qwen-first (or Qwen-only) so a Qwen 429 degrades to another Qwen seat rather than to a different model family. Requires a LiteLLM restart — treat as an architectural mutation: propose it, do not silently restart the federation gateway mid-conversation.

## Frame language is a second, independent cause

A first message written in English trains the reply's language even when the answering model is
healthy. The model reasons in the language of the incoming frame and translates back to BM — the
result reads as translated Malay, with none of the router symptoms above.

So a voice complaint has two candidate causes, and they are distinguishable:

| Cause | Signature | Resolves when |
|---|---|---|
| Degraded router | 429/cooldown in the FED log at that minute | the seats come back |
| English frame | no router event, reply still stiff | the user re-opens in BM |

Check both, and report which one you found. Do not dispute the user's language observation under
either cause.

## Length is part of the register

An over-long reply is itself a voice defect, and it co-occurs with the degraded router often enough
that the pair is diagnostic: a fallback model tends to answer an open analytical or emotional prompt
with a long structured essay where the primary lane would have been short. Budget before composing,
not after — a DM reply that overruns its natural length by 2–3× is the failure, and the user reads
the length as a change of voice.

## Rule

When Arif says your voice changed, do not defend the output. Check the router cooldowns first;
register drift is a routing event until proven otherwise.
