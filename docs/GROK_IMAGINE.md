# Grok Imagine — telephone for every AAA agent

> **Forged:** 2026-08-25 · FI-007 Grok Build
> **Doctrine:** Imagine tools are harness-native. Spawn Grok. Do not pretend Hermes has `image_gen`.

## Why this exists

Grok Build owns `image_gen`, `image_edit`, `image_to_video`, `reference_to_video`.
Those are **not** MCP tools and **not** on FED (no static xAI key).
Hermes / OpenCode / Claude / Kimi / Codex / OpenClaw / Copilot **spawn Grok**.

## Dial

```bash
grok-multimodal.sh image "prompt" [--ratio 9:16]
grok-multimodal.sh edit  /abs/path.jpg "prompt"
grok-multimodal.sh video /abs/path.jpg "prompt" [--seconds 6]
```

Wrapper: `/root/.grok/bin/grok-multimodal.sh` (PATH: `grok-multimodal`)
Outbox: `/root/forge_work/grok-mm/`
Equivalent: `grok -p --always-approve --output-format json "Use image_gen. …"`

## Floors

- Named person → `image_edit` + real reference.
- No sexual/romantic fabrication of a named third party.
- OIDC on this VPS. Do not add `model_name: grok` to LiteLLM.

## Router

Skill `forge-multimodal-router` → harness-native Imagine rows.
Parent telephone: [`CALL_MAP.md`](./CALL_MAP.md).

DITEMPA BUKAN DIBERI
