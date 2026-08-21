---
description: Probe Z.AI GLM coding plan health — models list, anthropic + openai endpoints, credit reality
---

Verify the Z.AI GLM Coding Plan is alive and correctly wired. Key lives in env `ZAI_API_KEY` (vault: /root/.secrets/kunci-root.env; mode-600 configs only).

Probes (all live, F2 OBS):

1. Plan models: `GET https://api.z.ai/api/coding/paas/v4/models` (Bearer key) — expect glm-4.5 … glm-5.3 (9 models).
2. Anthropic-compat (Kimi path): `POST https://api.z.ai/api/anthropic/v1/messages` with `x-api-key` + `anthropic-version: 2023-06-01`, model glm-5.3 — expect HTTP 200.
3. OpenAI-compat (Qwen path): chat completion at `/api/coding/paas/v4/chat/completions`, model GLM-5.3 — expect 200.
4. Cross-check wired surfaces: Qwen settings.json `[Z.AI]` entries, Kimi config.toml `zai-coding-plan` provider (both config homes), OpenCode `zai-direct`, Claude `ZAI_DIRECT_*` env — all must reference the same endpoints.
5. FED SOT: `/root/.config/federation-models.json` → provider `zai-coding-plan` must carry `anthropic_endpoint_url` + live telemetry.

Gotchas: `glm-5.2` requests return model=glm-5.3 (silent redirect — plan fact, not a bug). Peak Mon–Fri 14:00–18:00 SGT burns credits at 2×; off-peak 50% off. If anthropic endpoint 401s from Kimi: kimi-code does NOT expand `${ENV}` in provider api_key — literal key required (mode 600).

Report: endpoint statuses, model count, any drift between the 5 wired surfaces.
