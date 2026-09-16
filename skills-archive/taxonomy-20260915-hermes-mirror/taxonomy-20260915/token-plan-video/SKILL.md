---
name: "token-plan-video"
id: "token-plan-video"
version: 1.0.0
owner: AAA
risk_tier: medium
floor_scope: [F1, F2, F4, F7]
description: "Call Qwen Token Plan video models on the Personal allowlist (happyhorse-1.1-t2v / i2v / r2v). Activate for text-to-video, image-to-video, or reference-to-video on Token Plan."
autonomy_tier: T1
capability_tier: fed-multimodal-vision
ecology_state: WARM
---

Generate video on **Qwen Token Plan** only. Capability SOT: `CAPABILITIES.json` (`video_out`).

User request: $ARGUMENTS

## Allowlist (exact IDs)

| Model | Job | Limits |
|---|---|---|
| `happyhorse-1.1-t2v` | **Default** text-to-video | 3–15s, 720/1080P, audio |
| `happyhorse-1.1-i2v` | Image-to-video (first frame) | 3–15s |
| `happyhorse-1.1-r2v` | Reference-to-video | 1–9 refs, 3–15s |

Not on Token Plan Personal: `wan3.0-video` (invite-only), `wan2.7-t2v`, `wan2.6-*`. Do not call them on this key.

## Steps

1. Short first: 5s, 720P. Video burns Credits fast; settle is async after complete.
2. Create task (Token Plan host, same video-synthesis path as QwenCloud docs):

```bash
source /root/.secrets/kunci-root.env
curl -s -X POST "https://token-plan.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis" \
  -H "Authorization: Bearer $QWEN_API_KEY" \
  -H "X-DashScope-Async: enable" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "happyhorse-1.1-t2v",
    "input": {"prompt": "<PROMPT>"},
    "parameters": {"resolution": "720P", "duration": 5}
  }'
```

3. Poll `GET .../api/v1/tasks/<task_id>` until SUCCEEDED. Download `video_url` immediately (24h expiry).
4. If 404/model-not-exist: fail loudly. Do not silently switch to DashScope pay-as-you-go.

## Notes

- Key is `QWEN_API_KEY` on Token Plan Singapore. `DASHSCOPE_API_KEY` on dashscope-intl is a different ledger.
- MiniMax `generate_video` is a different hand (`minimax-media`).
- Docs: https://docs.qwencloud.com/developer-guides/getting-started/video-models
  Allowlist: https://docs.qwencloud.com/token-plan/personal/token-plan-personal-overview
