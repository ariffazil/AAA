---
name: replicate-models
description: >
version: 1.0.0
---
## Docs

- Reference: <https://replicate.com/docs/llms.txt>
- OpenAPI schema: <https://api.replicate.com/openapi.json>
- MCP server: <https://mcp.replicate.com>
- Per-model docs: `https://replicate.com/{owner}/{model}/llms.txt`
- Set `Accept: text/markdown` when requesting docs pages.

## 1. Find models

- **Search**: `GET /v1/search?query=...` returns models, collections, and docs.
- **Collections**: `GET /v1/collections` for curated groups. The `official` collection is always warm with stable APIs.
- **Read schema**: `GET /v1/models/{owner}/{name}` → `model.latest_version.openapi_schema.components.schemas.Input.properties`. Always fetch before running — schemas change.

Prefer official models (warm, stable, predictable pricing). Prefer latest versions. Run count can be misleading — recency matters more.

## 2. Compare models

Build a shortlist, then compare on four axes:

| Axis | How to check |
|------|-------------|
| **Speed** | `metrics.predict_time` on completed predictions |
| **Cost** | Official = per-run. Community = GPU-seconds. Run a few and check `metrics` |
| **Quality** | Same prompt through each model. Match to your use case, not a leaderboard |
| **Capabilities** | Input schema: reference images, masks, aspect ratios, streaming, multi-image |

**Tradeoffs**: smaller = cheaper/slower; schnell/turbo = faster/pricier; pro/max = best/slowest; ControlNet = most control/most setup.

## 3. Run models

**Workflow**: choose → get schema → create prediction → poll → return output.

```bash
# Create
POST /v1/predictions

# Poll
GET /v1/predictions/{id}
```

**Output methods**:
1. Poll: store `id`, loop until `status == succeeded`
2. Sync: `Prefer: wait` header — blocking, max 60s, only for very fast models
3. Webhook: set `webhook` URL + `webhook_events_filter` (`start`, `output`, `logs`, `completed`). Validate with `Webhook-ID`, `Webhook-Timestamp`, `Webhook-Signature`

**Guidelines**:
- Use `POST /v1/predictions` for official and community models
- Validate inputs against schema constraints (`minimum`, `maximum`, `enum`)
- Don't set optional inputs without reason
- Use HTTPS URLs for file inputs
- Fire predictions concurrently
- Output URLs expire after 1 hour — back up immediately
- Set `lifetime` to auto-cancel (`30s`, `5m`, `1h`)

**Model identifiers**:
- Official: `owner/name` (routes to latest)
- Community: `owner/name:version_id` (must pin; can cold-boot)

## 4. Multi-model workflows

Chain models by passing output URLs as inputs to the next. Start independent predictions in parallel. Output URLs are valid for 1 hour.

## 5. Prompting guidance

- **Image**: see [replicate-prompting](../replicate-prompting/SKILL.md) §Image
- **Video**: see [replicate-prompting](../replicate-prompting/SKILL.md) §Video
