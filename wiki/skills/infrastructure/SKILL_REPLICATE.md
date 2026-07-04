---
title: "Skill: Replicate AI Media"
created: 2026-05-17
updated: 2026-05-17
version: 1.0.0
type: skill
category: infrastructure
tags: [replicate, ai-models, images, videos, predictions, webhooks, streaming, mcp]
confidence: high
contested: false
floors: [F7, F8]
risk_band: LOW
sources: [
  /root/.agents/skills/compare-models/SKILL.md,
  /root/.agents/skills/find-models/SKILL.md,
  /root/.agents/skills/run-models/SKILL.md,
  /root/.agents/skills/prompt-images/SKILL.md,
  /root/.agents/skills/prompt-videos/SKILL.md
]
---

# Skill: Replicate AI Media Suite

> **Sources:** 5 Replicate skills consolidated
> **Agent:** OpenCode / Kimi
> **Forged:** 2026-05-17

---

## Trigger Conditions

Load this skill when the task involves:
- Running AI models on Replicate (images, videos, LLMs)
- Comparing models by cost, speed, quality
- Writing prompts for image or video generation
- Setting up webhooks or streaming predictions
- Keywords: replicate, prediction, model, image-generation, video-generation

---

## Doctrine

Replicate is an API for open-source AI models. Treat it as a compute layer, not a creative partner.

---

## Sub-Skills

| Sub-Skill | Purpose | Trigger |
|-----------|---------|---------|
| **find-models** | Search Replicate model registry | "find a model for X" |
| **compare-models** | Cost/speed/quality comparison | "which model is best for X" |
| **run-models** | Execute predictions via API | "run this model" |
| **prompt-images** | Write image generation prompts | "create an image of..." |
| **prompt-videos** | Write video generation prompts | "create a video of..." |

---

## Key URLs

| Resource | URL |
|----------|-----|
| Docs | `https://replicate.com/docs/llms.txt` |
| OpenAPI | `https://api.replicate.com/openapi.json` |
| MCP Server | `https://mcp.replicate.com` |
| Per-model docs | `https://replicate.com/{owner}/{model}/llms.txt` |

---

## Related

- [[skill-cloudflare]] — If deploying Replicate output to Workers/Pages
- [[skill-frontend-design]] — If building UI around generated media

---

*DITEMPA BUKAN DIBERI — Models are tools, not muses.*
