# MATA — Unified Visual Intelligence Map (canonical)

> **MATA = mata (Malay: eye).** One truth surface for everything the federation can see and make seen: image generation, video generation, image/video understanding.
> **Rule zero (F13, 2026-09-10):** an agent may only claim a visual lane dead if `mata` (or `mata --gen`) said so **within 24h**. Stale prose is not evidence. "Models-list 200" ≠ "can generate" — only a generation canary is proof (Gemini scar, below).
> **Cure for:** Hermes's 2026-09-10 "zero video generation available" — falsified 40 minutes later by Hailuo 2.3 task `440098549555487` → `/root/forge_work/mata-canary/hailuo2.3-first-light.mp4` (89 KB).

## Live probe (the pane agents must run)

```bash
set -a; source /root/.secrets/kunci-root.env; set +a
/root/scripts/mata.sh          # pane (table)
/root/scripts/mata.sh --json   # machine snapshot → ~/.local/share/arifos/mata_last.json
/root/scripts/mata.sh --gen    # + real generation canaries (costs quota — use sparingly)
```

**First pane receipt — 2026-09-10T00:20Z (FI-003):**

| Lane | Verdict | Truth |
|---|---|---|
| gemini | auth-LIVE / **gen 429** | 55 models, 11 visual — but prepay credits DEPLETED. Models-list was a trap. |
| minimax-video | **LIVE** | `MiniMax-Hailuo-2.3`, durations 6s\|10s, **3 clips/day** in Monthly Max. Endpoint `POST /v1/video_generation`, poll `/v1/query/video_generation?task_id=`, fetch `/v1/files/retrieve?file_id=` |
| minimax-chat | **LIVE** | 8 models, M3 has native image+video input |
| mimo-tp | **LIVE** | 6 models; mimo-v2.5 omni (img+video+audio in). **LIST ONLY** — proves auth, not capability (SCAR #1). Renewal 2026-09-17 |
| mimo-tp-vision | **LIVE** | **REAL vision canary** — 1px PNG `image_url` data-URI → 200 with `image_tokens=9`. Added 2026-09-13 (FI-008) so the lane can no longer reach a LIVE verdict on a models-list alone. Lane id `mimo-tp` retained unchanged for `mata_last.json` consumers. |
| mimo-tp-video | **LIVE** | **PAIRED-fixture perception canary** — identical grey visuals, audio ASCENDING in fixture A vs DESCENDING in B; the model answered **RISE / FALL** → `PERCEPTION_VERIFIED`. Correct answers are *opposite*, so output bias is falsified. Run on demand: `mimo-vision vcanary` (NOT in the cheap pane — video tokens cost). Methodology per `FED_VIDEO_CANARY_LEDGER.yaml` (single-canary = bias). |
| mimo-tp-audio | **LIVE** | TTS (free window) + ASR + audio-understanding. Primitive: `mimo-audio` (`tts·design·clone·asr·understand`). Full contract: `audio-intelligence-map.md`. |
| kimi | **401** | key/endpoint mismatch on `api.moonshot.ai` — FED says kimi-moonshot LIVE 79% weekly. Investigate before claiming dead |
| dsq-free-vl | **403 ALL** | 13 SOT-"LIVE" VL models: free quota EXHAUSTED (was predicted Sep-29; came early). Key also in free-tier-only mode → PAYG image gen blocked behind payment-info wall |
| bailian-tp | **LIVE** | 12 models incl. `wan2.7-image`, `wan2.7-image-pro` — Hermes's "BAILIAN exhausted" falsified at auth level |
| qwen-indiv | models-OK | 12 models listed; **weekly gen quota was 429 until ~2026-09-11 04:01Z** — run `--gen` canary before claiming |
| comfyui :8188 | **DOWN** | local zero-cost pixel lane needs manual start (no systemd unit on KVM8) |
| fed :4000 | LIVE | HAProxy→KVM4 litellm |
| pollinations | LIVE | keyless T2I fallback |
| zai-vision | **LIVE** | `GLM-5.3-Flash` (1M ctx, 3x quota) + `@z_ai/mcp-server@latest` (8 visual tools: ui_to_artifact, extract_text, error diag, diagram/data viz, diff, video). 5h rolling credit bucket. |

## Routing recipes (what to use NOW)

- **Image generation:** `bailian-token-plan/wan2.7-image(-pro)` via `/compatible-mode/v1/chat/completions` (plain-text prompt → markdown image URL in content; capture FULL signed URL incl. query, GET within expiry). Fallback: pollinations (keyless). Tomorrow+: qwen-indiv resets. Local: start ComfyUI for zero-cost.
- **Video generation:** `MiniMax-Hailuo-2.3` (3/day, 6s or 10s) — schema in table above. Tomorrow: `happyhorse-1.1-t2v/i2v/r2v` on qwen-indiv. Veo 3.1 listed on gemini but gen-blocked by depleted prepay (needs top-up = F13 decision).
- **Image/video understanding:** `mimo-v2.5` (omni, img+video+audio). **Federation primitive:** `mimo-vision` (on PATH) — `see` for OpenAI **and** Anthropic wires, `tokens` for the vendor image-token formula, `doctor` for a real canary. Contract: JPEG/PNG/GIF/WebP/BMP, URL ≤50 MB or base64 ≤50 MB per image, multi-image ok, **no multipart upload**. Also available: `zai-vision` (GLM-5.3-Flash / @z_ai/mcp-server@latest, video ≤8MB), `MiniMax-M3` (native multimodal), `k3` (img+video) once the 401 is resolved, `gemini-*` family (video canary-verified ingestion — SEE `FED_VIDEO_CANARY_LEDGER.yaml`).
- **OCR:** `zai-vision` (`extract_text_from_screenshot` tool / GLM-5.3-Flash) / MiniMax-M3 / mimo-v2.5 (VL fleet is 403-dead).

## Scars that made MATA (do not repeat)

1. **Models-list trap** — 200 on `/models` proves auth, not quota. Gemini pane said "image fleet confirmed"; real canary 429'd. Generation claims need generation canaries.
2. **Console-redaction stub** — `MINIMAX_PLUGIN_API_KEY` held a 13-char `sk-cp-…UgO4` redaction artifact while the real 125-char key sat one variable over. Fixed in kunci-root.env + HERMES/.env (KVM8) + ~/.hermes/.env (KVM4) 2026-09-10; gateway restarted, key verified in process env.
3. **Wrong-path diagnosis** — "MiniMax video 404" came from probing wrong endpoints. The right one existed all along. Probe the documented path variants (empty-body POST: 400/200 = EXISTS, 404 = absent) before declaring a lane dead.
4. **SOT staleness class** — 6 lanes drifted between `/root/.config/federation-models.json` and live reality in one audit. SOT entries carry `last_verified`; anything older than 7 days is STALE by definition.
5. **Reasoning-budget blank-success (2026-09-13, FI-008)** — `mimo-v2.5` is a *reasoning* model: `max_tokens` is shared by the reasoning channel and the answer. A budget too small returns **HTTP 200 with EMPTY content** — a blank "success" that reads as a broken lane. `mimo-vision see` now detects it, retries at a wider budget, and stamps `retry_note`. General rule: on any reasoning model, **empty content with non-empty reasoning means budget exhaustion, not capability failure.**

## Lineage

- Supersedes: `visual-intelligence-map.md` (2026-08-26, stale), `video-intelligence-map.md` (2026-09-06, merged).
- Preserved as evidence: `FED_VIDEO_CANARY_LEDGER.yaml` (anti-bias canary methodology — paired fixtures, repeated trials).
- Audio stays separate: `audio-intelligence-map.md` (freshest, somatic doctrine).
- Skill: `/root/AAA/skills/mata/` · Probe: `/root/scripts/mata.sh` · Snapshot: `~/.local/share/arifos/mata_last.json`
- Musyawarah receipt: `/root/forge_work/qwen-sessions/musyawarah/2026-09-10T00-09-52Z.json` (4-role ran; kernel 888 verdict HOLD at L11 session gate — T1 build proceeded under direct F13 order)
