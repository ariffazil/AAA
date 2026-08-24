---
id: fi-zai-probe
name: fi-zai-probe
version: 1.0.0
description: "Probe Z.AI GLM coding plan health — models list, anthropic + openai endpoints, credit reality, cross-check 5 wired surfaces. Use when Arif says 'zai probe', 'check Z.AI plan', 'is GLM alive', 'zai health', or when any zai-backed harness (Qwen/Kimi/OpenCode/Claude) behaves oddly."
owner: 333-AGI
risk_tier: low
floor_scope: [F2, F4]
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# Z.AI Plan Probe

Verify the Z.AI GLM Coding Plan is alive and correctly wired. Key lives in env `ZAI_API_KEY` (vault: /root/.secrets/kunci-root.env; mode-600 configs only — never paste keys into chat, receipts, or configs beyond mode-600).

## Probes (all live, F2 OBS)

1. Plan models: `GET https://api.z.ai/api/coding/paas/v4/models` (Bearer key) — expect glm-4.5 … glm-5.3 (9 models).
2. Anthropic-compat (Kimi path): `POST https://api.z.ai/api/anthropic/v1/messages` with `x-api-key` + `anthropic-version: 2023-06-01`, model glm-5.3 — expect HTTP 200.
3. OpenAI-compat (Qwen path): chat completion at `/api/coding/paas/v4/chat/completions`, model GLM-5.3 — expect 200.
4. Cross-check wired surfaces: Qwen settings.json `[Z.AI]` entries, Kimi config.toml `zai-coding-plan` provider, OpenCode `zai-direct`, Claude `ZAI_DIRECT_*` env — all must reference the same endpoints.
5. FED SOT: `/root/.config/federation-models.json` → provider `zai-coding-plan` must carry `anthropic_endpoint_url` + live telemetry.

## Gotchas (scars, not guesses)

- `glm-5.2` requests silently return model=glm-5.3 — plan fact, not a bug.
- Peak Mon–Fri 14:00–18:00 SGT burns credits at 2×; off-peak 50% off.
- If the anthropic endpoint 401s from Kimi: kimi-code does NOT expand `${ENV}` in provider `api_key` — literal key required in a mode-600 file.

## Output

Report: endpoint statuses, model count, any drift between the 5 wired surfaces.
