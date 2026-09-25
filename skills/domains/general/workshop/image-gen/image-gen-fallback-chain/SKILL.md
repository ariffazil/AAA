---
name: image-gen-fallback-chain
description: "Image generation under provider outage. Fallback ladder."
version: 1.1.0-2026.08.28
author: hermes
license: MIT
tags: [image-generation, fallback-chain, provider-outage, pollinations, sana, multi-subject, qwen-payg, identity-swap]
metadata:
  hermes:
    category: creative
    requires: [mmx-cli]
    related: [minimax-cli, photorealistic-human-image-gen, mulerouter-media, token-plan-image]
capability_tier: fed-multimodal-vision
ecology_state: WARM
---

# Image Generation Fallback Chain (under multi-provider outage)

> v1.1.0 (2026-08-28): Added Qwen PAYG env-override recipe (`QWEN_PROVIDER=dashscope` + `DASHSCOPE_PAYG_API_KEY`), identity-swap honest verdict (F9: ~75% likeness, not pixel-perfect), and key-prefix cheatsheet. See `references/qwen-payg-image-recipe-2026-08-28.md`.
>
> v1.2.0 (2026-09-25): Added scientific-diagram text-label fallback rule (matplotlib programmatic rendering, not AI image generation). See `references/scientific-diagram-text-labels-2026-09-25.md`.

## When to Use

Use when an image-generation request hits a provider error (404, 402, quota, unknown) and you must decide whether to retry, reshape the prompt, or fall through to the next lane — especially when the only live lane is free-tier Pollinations/SANA and the scene has more than one subject.

When the paid image stack returns errors, do NOT keep throwing prompts at the same lane. Read the error signature, classify it, and fall through the ladder. Retrying a dead lane wastes quota and time.