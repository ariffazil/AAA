# NOTE: Kimi 2.5 Model ID — Needs Confirmation

## Current setting in openclaw.json

```json
"model": {
  "primary": "moonshot/kimi-k2",
  "fallbacks": ["anthropic/claude-sonnet-4-6"]
}
```

## Uncertainty

The exact model ID string OpenClaw expects for Kimi 2.5 is not confirmed.
The value `moonshot/kimi-k2` is a best-effort guess based on Moonshot AI's API naming.

## How to confirm

1. Check the OpenClaw docs at https://docs.openclaw.ai for supported providers.
2. Or after restart, open the Control UI at https://claw.arifosmcp.arif-fazil.com
   and browse available models — the UI should list what the Kimi provider exposes.
3. Possible alternatives to try:
   - `moonshot/kimi-k1.5`
   - `moonshot/moonshot-v1-8k`
   - `kimi/kimi-k2`
   - `kimi/kimi-2.5`

## To change

Edit `/opt/arifos/data/openclaw/openclaw.json`, update `agents.defaults.model.primary`,
then restart the container:

```bash
docker compose -f /srv/arifOS/docker-compose.yml up -d openclaw_gateway
```

## After confirming

Delete this file and commit the removal.
