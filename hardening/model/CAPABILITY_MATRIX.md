# LIVE Generative-Model Capability Matrix — arifOS Federation

**Probe date:** 2026-09-14 17:43–17:52 UTC (2026-09-15 01:43–01:52 MYT)
**Host:** KVM8 truth node (`/root`), `mmx 1.0.22`, `edge-tts 7.2.7`, `ffprobe 6.x`
**Artifacts:** `/root/AAA/hardening/model/artifacts/`
**Method:** one live call minimum per lane, every call passed `--base-url https://api.minimax.io`; all sizes/durations read back with `ffprobe`/`stat`; no value in this document is inferred.

**Environment preamble (run once, every shell):**
```bash
set -a && source /root/.secrets/kunci-root.env && set +a
```

---

## 1. VERDICT TABLE

| # | Lane | Verdict | Evidence |
|---|------|---------|----------|
| 1 | MiniMax image (`image-01`) | **WORKS** | 5 sizes generated; 3 confirmed artifacts at 1024x1792, 1152x2048, 1440x2048, 2048x1152 |
| 1b | MiniMax image @ 2048x2048 | **BLOCKED** (server rpc timeout, deterministic 2/2) | `rpc timeout: timeout=1m0s ... (HTTP 200)` |
| 1c | MiniMax image @ 1440x2560 | **BLOCKED** (CLI bound) | `--height must be between 512 and 2048, got 2560.` |
| 2 | MiniMax video `MiniMax-Hailuo-2.3` i2v | **WORKS** | 768x1364, 5.875 s, 445 728 B, 105 s wall |
| 2b | MiniMax video `MiniMax-H3` | **BLOCKED** (Token Plan entitlement) | exact string in §4 |
| 3 | MiniMax speech (`speech-2.8-hd`) | **WORKS** (332 voices, **0 Malay**) | 4.104 s / 67 380 B |
| 4 | `mmx quota show` | **WORKS** | all counters in §5 |
| 5 | MiMo models (`token-plan-sgp.xiaomimimo.com`) | **WORKS** | 6 model ids, HTTP 200 |
| 6 | Qwen Token Plan — image / video / speech | **BLOCKED (quota exhausted)** — auth VALID | `Throttling.AllocationQuota`, HTTP 429, all 3 lanes |
| 7 | edge-tts `ms-MY` fallback | **WORKS** | 2 voices, 2 real MP3s |

---

## 2. LANE 1 — MiniMax image (`mmx image generate`)

### Exact commands
```bash
mmx image generate --base-url https://api.minimax.io \
  --prompt 'A minimalist navy-blue geometric seal emblem, flat vector, centered on white' \
  --width <W> --height <H> \
  --out /root/AAA/hardening/model/artifacts/mm_img_<W>x<H>.jpg --quiet
```

### Results

| W×H | px | exit | wall | artifact | bytes | ffprobe dims |
|-----|----|------|------|----------|-------|--------------|
| 1024×1792 | 1 835 008 | 0 | 27 s | `mm_img_1024x1792.jpg` | 93 382 | 1024x1792 |
| 1152×2048 | 2 359 296 | 0 | 36 s | `mm_img_1152x2048.jpg` | 117 033 | 1152x2048 |
| 1440×2048 | 2 949 120 | 0 | 47 s | `mm_img_1440x2048.jpg` | 159 115 | 1440x2048 |
| 2048×1152 | 2 359 296 | 0 | 35 s | `mm_img_2048x1152.jpg` | 148 948 | 2048x1152 |
| 2048×2048 | 4 194 304 | 1 | 63 s | *(none)* | — | — |
| 2048×2048 (retry) | 4 194 304 | 1 | 65 s | *(none)* | — | — |
| 1440×2560 | 3 686 400 | 2 | 0 s | *(none)* | — | — |

**LARGEST SIZE THAT ACTUALLY SUCCEEDS: 1440×2048 (2 949 120 px).**
Both axes cap at 2048. 2048×1152 also succeeds. 2048×2048 (the CLI's nominal maximum-square) fails deterministically — 2/2 attempts, not transient.

### Raw errors
`2048x2048` (both attempts, identical modulo remote IP):
```json
{"error":{"code":1,"message":"API error: rpc timeout: timeout=1m0s, to=amadeus-server-rpc.algeng-prod.svc.cluster.local:8888, method=Play, location=kitex.rpcTimeoutMW, remote=10.242.242.225:8888 (HTTP 200)"}}
```
`1440x2560` — client-side, exit 2, **zero API cost**:
```json
{"error":{"code":2,"message":"--height must be between 512 and 2048, got 2560."}}
```

### md5 (immutable identity)
```
edcb03fe433d844093350753b453746e  mm_img_1024x1792.jpg
b147e95b53a22e5ddc28d102288a9d98  mm_img_1152x2048.jpg
57aa538055a156956688aa01b8bc828a  mm_img_1440x2048.jpg
e685cb8aa94959803531f4a4fd2ea9af  mm_img_2048x1152.jpg
```

**VERDICT: WORKS** (ceiling 1440×2048; avoid 2048×2048).

---

## 3. LANE 2 — MiniMax video

### 2a. `MiniMax-Hailuo-2.3` image-to-video — **WORKS**
```bash
mmx video generate --base-url https://api.minimax.io \
  --model MiniMax-Hailuo-2.3 \
  --prompt 'Slow cinematic camera push-in, subtle light shift' \
  --image /root/AAA/hardening/model/artifacts/mm_img_1152x2048.jpg \
  --download /root/AAA/hardening/model/artifacts/mm_vid_hailuo23.mp4 --quiet
```
- exit 0, **wall 105 s** (blocking poll)
- stdout: `/root/AAA/hardening/model/artifacts/mm_vid_hailuo23.mp4`
- `stat`: **445 728 bytes**, md5 `276cd054abb5cb65c6fd1def9419b605`
- `ffprobe`: h264, **768×1364**, **5.875 s**, 141 frames
- Input ratio 1152:2048 = 0.5625 → output 768:1364 = 0.5630 (aspect preserved, dimensions server-chosen)

### 2b. `MiniMax-H3` — **BLOCKED**
```bash
mmx video generate --base-url https://api.minimax.io --model MiniMax-H3 \
  --prompt 'A small paper boat drifting on still water' \
  --download /root/AAA/hardening/model/artifacts/mm_vid_h3.mp4 --quiet
```
exit **1**, wall **1 s**, no file written. Raw return:
```json
{"error":{"code":1,"message":"API error: invalid params, TokenPlan or Credit does not currently support MiniMax-H3 series models (2013) (HTTP 400)"}}
```

### 2c. Output-parameter rejection matrix (Hailuo-2.3)
`--duration`, `--ratio`, `--reference-image`, `--reference-video`, `--reference-audio` are **H3-only**. All three probe flags returned the *same* CLI guard, exit **2**, wall 0 s, no quota consumed:

```json
{"error":{"code":2,"message":"--reference-image, --reference-video, --reference-audio, --duration, and --ratio require --model MiniMax-H3."}}
```

| Model | rejects | accepts |
|-------|---------|---------|
| `MiniMax-Hailuo-2.3` | `--duration`, `--ratio`, `--reference-image`, `--reference-video`, `--reference-audio` | `--image`, `--prompt`, `--download`, `--poll-interval` |
| `MiniMax-Hailuo-2.3-Fast` | same as above (requires `--image`) | `--image` |
| `MiniMax-H3` | *none of the above* — but **blocked by Token Plan entitlement** | *(never reached)* |

Per `mmx video generate --help`: `--last-frame` alone → auto-switch to `Hailuo-02` (SEF); `--subject-image` → auto-switch to `S2V-01`.

**VERDICT: WORKS for Hailuo-2.3 i2v (5.875 s sample verified). MiniMax-H3 = BLOCKED by Token Plan entitlement — deterministic, not retryable.**

---

## 4. KNOWN-CONSTRAINT CHECK — MiniMax-H3 rejection string

**Claim under test:** the current Token Plan rejects MiniMax-H3 with
`TokenPlan or Credit does not currently support MiniMax-H3 series models (2013)`.

**Result: CONFIRMED — verbatim, with wrapper.** Corrected full form (live capture, 2026-09-14 17:46 UTC):

```
API error: invalid params, TokenPlan or Credit does not currently support MiniMax-H3 series models (2013) (HTTP 400)
```

Delta from the claim as stated: the message is prefixed `API error: invalid params, ` and suffixed ` (HTTP 400)`; `mmx` wraps it as `{"error":{"code":1,"message":...}}` with process exit code **1**. The `(2013)` code is the MiniMax API error number. The claim's substring is exact.

**Operational consequence:** MiniMax-H3's entire capability surface — text-to-video V2, first/last-frame, `--reference-image/video/audio`, `--duration 4–15`, `--ratio adaptive|21:9|16:9|4:3|1:1|3:4|9:16`, 2K output — is unreachable on this seat regardless of correct parameters. Do not debug H3 failures as parameter errors.

---

## 5. LANE 3 — MiniMax speech

```bash
mmx speech voices --base-url https://api.minimax.io --quiet
mmx speech synthesize --base-url https://api.minimax.io \
  --text 'arifOS federation capability probe. Model lane live.' \
  --voice English_expressive_narrator \
  --out /root/AAA/hardening/model/artifacts/mm_speech_probe.mp3 --quiet
```
- `speech voices` → JSON array, **332 voice IDs** (raw: `artifacts/speech_voices_raw.txt`, 334 lines)
- synthesis → exit 0, **2 s** wall, **67 380 B**, md5 `7767ed8a2623500785360d6b5a905ce7`, ffprobe **mp3 4.104 s**

### ⚠ Malay coverage = ZERO (material finding)
Language distribution of the 332 system voices (prefix count):

```
Portuguese 73 · Korean 49 · Spanish 47 · English 45 · Chinese (Mandarin) 32
Japanese 15 · Indonesian 9 · Russian 8 · Cantonese 6 · French 6 · Thai 4
Polish 4 · Romanian 4 · Italian 4 · German 3 · czech 3 · finnish 3
hindi 3 · Arabic 2 · Dutch 2 · Turkish 2 · Ukrainian 2 · Greek 2+1
Vietnamese 1 · Arrogant 1 · Robot 1
```

**`[v for v in voices if 'malay' in v or v.startswith('ms')] → []`** — no `ms-MY`, no Melayu, no Malay voice ID exists in the MiniMax system catalog.

Two further probes, both failed (recorded so they are not retried):
| Attempt | exit | raw error |
|---------|------|-----------|
| `--voice Indonesian_Man` | 1 | `API error: voice id not exist (HTTP 200)` — correct ID is `Indonesian_ReservedYoungMan` |
| `--language ms` | 1 | `API error: invalid params, invalid params: language_boost (HTTP 200)` — `ms` is not a valid `language_boost` value |

**Working compromise (verified):** Malay text renders through the Indonesian voice with **no** language flag:
```bash
mmx speech synthesize --base-url https://api.minimax.io \
  --text 'Selamat pagi. Saya Hermes, ejen arifOS. Jalur suara Melayu sedang diuji.' \
  --voice Indonesian_ReservedYoungMan \
  --out /root/AAA/hardening/model/artifacts/mm_speech_bm_indonesian_voice.mp3 --quiet
```
exit 0, 2 s, **112 884 B**, mp3 **6.948 s**, md5 `10277d0c681f6ef6b82e9194d329690d`. Intelligibility judged by the human, not asserted here.

**VERDICT: MiniMax speech WORKS. Native Malay TTS = NOT AVAILABLE on MiniMax system voices.**

---

## 6. LANE 4 — `mmx quota show` (every counter)

```bash
mmx quota show --base-url https://api.minimax.io --output json
```
exit 0. Raw: `artifacts/quota_raw.txt`, `artifacts/quota_after.txt`, `artifacts/quota_final.txt`.
`base_resp`: `{"status_code": 0, "status_msg": "success"}`

| counter | value (final snapshot 17:52 UTC) | note |
|---------|-----------------------------------|------|
| `general.current_interval_remaining_percent` | **57** | was 61 pre-probe → 4 pts consumed by this matrix |
| `general.current_weekly_remaining_percent` | **87** | was 88 pre-probe |
| `general.current_interval_total_count` | 0 | not a count-based lane |
| `general.current_interval_usage_count` | 0 | |
| `general.current_weekly_total_count` | 0 | |
| `general.current_weekly_usage_count` | 0 | |
| `general.current_interval_status` | 1 | OK |
| `general.current_weekly_status` | 1 | OK |
| `general` interval window | 1789398000000 → 1789416000000 | ends **2026-09-14 20:00 UTC** |
| `video.current_interval_total_count` | **3** | daily cap = 3 videos |
| `video.current_interval_usage_count` | **3** | |
| `video.current_interval_remaining_percent` | **0** | |
| `video.current_interval_status` | **2** | exhausted flag |
| `video.current_weekly_total_count` | 21 | |
| `video.current_weekly_usage_count` | 3 | |
| `video.current_weekly_remaining_percent` | **85** | |
| `video.current_weekly_status` | 1 | OK |
| `video` interval window | 1789344000000 → 1789430400000 | ends **2026-09-15 00:00 UTC** |

### ⚠ Counter/gating discrepancy (recorded, unexplained)
The `video` interval counter read **3/3 used, 0 % remaining, status 2** both *before* and *after* the successful `MiniMax-Hailuo-2.3` call at 17:47 UTC — yet that call exited 0 and produced a real 445 728-byte MP4. Either the interval counter is stale/lagging or gating is on the **weekly** ledger (85 % remaining). Do not treat `video interval 0 %` alone as a hard stop; probe before declaring the lane blocked.

**VERDICT: WORKS. Daily video cap = 3; general lane is percent-based and non-zero-state.**

---

## 7. LANE 5 — MiMo models

```bash
curl -s -w "\nHTTP_CODE=%{http_code}\n" https://token-plan-sgp.xiaomimimo.com/v1/models \
  -H "Authorization: Bearer $MIMO_API_KEY"
```
**HTTP 200**, raw: `artifacts/mimo_models_raw.json`, `object: "list"`, `owned_by: "xiaomi"`.

| model id | class |
|----------|-------|
| `mimo-v2.5` | LLM |
| `mimo-v2.5-pro` | LLM |
| `mimo-v2.5-asr` | speech-to-text |
| `mimo-v2.5-tts` | text-to-speech |
| `mimo-v2.5-tts-voiceclone` | voice cloning |
| `mimo-v2.5-tts-voicedesign` | voice design |

**VERDICT: WORKS — 6 models enumerated. Exactly one inference call per model was NOT run (out of scope + cost discipline) → per-model inference status = NOT VERIFIED.**

---

## 8. LANE 6 — Qwen Token Plan routes

Skills read: `token-plan-image`, `token-plan-video`, `capabilities/media/token-plan-speech`.
Host: `https://token-plan.ap-southeast-1.maas.aliyuncs.com`. Key: `QWEN_API_KEY` (`sk-sp-H.…`).

| Lane | Model | Path | exit/HTTP | Result |
|------|-------|------|-----------|--------|
| image | `qwen-image-3.0-pro` | `POST /api/v1/services/aigc/multimodal-generation/generation` | **429** | blocked |
| video | `happyhorse-1.1-t2v` | `POST /api/v1/services/aigc/video-generation/video-synthesis` (`X-DashScope-Async: enable`) | **429** | blocked |
| speech | `qwen-audio-3.0-tts-plus` | `POST /api/v1/services/aigc/multimodal-generation/generation` | **429** | blocked |

Identical body from all three:
```json
{"code":"Throttling.AllocationQuota","message":"Your token-plan quota has been exhausted.","request_id":"<uuid>"}
```
request_ids: `334339ef-6727-4e18-935f-469528aa9ff4` (image), `be0b13dd-cfec-4f0e-a708-8d07d63284b9` (video), `52e45364-376b-4eec-b2c7-392b9c553a23` (speech).

### Auth-vs-quota discrimination (this is why the verdict is BLOCKED, not NOT CONFIGURED)
| Auth header sent | HTTP | body code |
|------------------|------|-----------|
| *(none)* | **401** | — |
| `Bearer sk-bogus-key` | **401** | `InvalidApiKey` |
| `Bearer $QWEN_API_KEY` | **429** | `Throttling.AllocationQuota` |
| `Bearer $QWEN_TEAM_OWNER_API_KEY` | **429** | `Throttling.AllocationQuota` |
| `Bearer $QWEN_ARIFOS_API_KEY` | **429** | `Throttling.AllocationQuota` |

Keys are **valid and accepted** (a bad/no key returns 401 at the same endpoint). All three seats are exhausted on the same `token-plan` ledger — this is a **billing/quota** block, not a configuration or routing fault. Nothing to fix in code; nothing was topped up and no payment was added, per cost discipline.

**VERDICT: BLOCKED — quota exhausted. Auth OK. All 3 lanes, all 3 keys.**

---

## 9. LANE 7 — edge-tts fallback (free lane)

```bash
edge-tts --list-voices | grep ms-MY
```
| voice ID | gender |
|----------|--------|
| `ms-MY-OsmanNeural` | Male |
| `ms-MY-YasminNeural` | Female |

Synthesis + artifact (both, exit 0):
```bash
edge-tts --voice ms-MY-YasminNeural --text 'arifOS federation, jalur suara Melayu hidup.' \
  --write-media /root/AAA/hardening/model/artifacts/edge_ms_my_yasmin.mp3
edge-tts --voice ms-MY-OsmanNeural --text 'arifOS federation, jalur suara Melayu hidup.' \
  --write-media /root/AAA/hardening/model/artifacts/edge_ms_my_osman.mp3
```
| voice | bytes | duration | md5 |
|-------|-------|----------|-----|
| Yasmin (F) | 26 208 | 4.368 s | `d782760d1da3cb4d76fe09321411c4d4` |
| Osman (M) | 25 056 | 4.176 s | `7851fe66a0b15d188936471bc5e7cfc2` |

**VERDICT: WORKS — and it is the ONLY lane on this host with a native Malay voice.** Cost: zero (no API key, Microsoft Edge read-aloud endpoint).

---

## 10. CLI PITFALL FACT — CORRECTION FROM LIVE EVIDENCE

**Briefed fact:** "the `mmx` CLI default base_url points at `https://api.minimax.io/anthropic`, so speech/image/video 404 unless you pass `--base-url https://api.minimax.io`."

**Live result: NOT REPRODUCIBLE.**
```bash
cat /root/.mmx/config.json
# {"api_key":"***","region":"global","base_url":"https://api.minimax.io"}
mmx config show
# {"region":"global","base_url":"https://api.minimax.io","output":"json","timeout":300,...}

mmx speech synthesize --text 'base url flag test' --voice English_expressive_narrator --out /tmp/nourl.mp3 --quiet
# exit 0 → /tmp/nourl.mp3
mmx image generate --prompt 'base url flag test square' --width 512 --height 512 --out /tmp/nourl_img.jpg --quiet
# exit 0 → /tmp/nourl_img.jpg, 172 657 bytes
```
`/root/.mmx/config.json` already holds `base_url: "https://api.minimax.io"` (no `/anthropic` path). Speech and image both succeed **without** the flag. The `/anthropic`-path defect appears to have been remediated in `mmx 1.0.22` config state.

**Retained discipline:** pass `--base-url https://api.minimax.io` on every call anyway — it is explicit, costless, and survives a config-file regression. `config.json` was read only, never edited, per constraint.

---

## 11. TOTAL ARTIFACT REGISTER

`/root/AAA/hardening/model/artifacts/` — all md5 + size produced by live `stat`/`ffprobe`:

| file | bytes | dims / duration | md5 |
|------|-------|-----------------|-----|
| `mm_img_1024x1792.jpg` | 93 382 | 1024x1792 | `edcb03fe433d844093350753b453746e` |
| `mm_img_1152x2048.jpg` | 117 033 | 1152x2048 | `b147e95b53a22e5ddc28d102288a9d98` |
| `mm_img_1440x2048.jpg` | 159 115 | 1440x2048 | `57aa538055a156956688aa01b8bc828a` |
| `mm_img_2048x1152.jpg` | 148 948 | 2048x1152 | `e685cb8aa94959803531f4a4fd2ea9af` |
| `mm_vid_hailuo23.mp4` | 445 728 | 768x1364, 5.875 s, 141f h264 | `276cd054abb5cb65c6fd1def9419b605` |
| `mm_speech_probe.mp3` | 67 380 | 4.104 s | `7767ed8a2623500785360d6b5a905ce7` |
| `mm_speech_bm_indonesian_voice.mp3` | 112 884 | 6.948 s | `10277d0c681f6ef6b82e9194d329690d` |
| `edge_ms_my_yasmin.mp3` | 26 208 | 4.368 s | `d782760d1da3cb4d76fe09321411c4d4` |
| `edge_ms_my_osman.mp3` | 25 056 | 4.176 s | `7851fe66a0b15d188936471bc5e7cfc2` |

Raw evidence files: `quota_raw.txt`, `quota_after.txt`, `quota_final.txt`, `speech_voices_raw.txt`, `mimo_models_raw.json`, `qwen_image_raw.json`, `qwen_video_create_raw.json`, `qwen_speech_raw.json`.

**Not written:** `mm_img_2048x2048.jpg` (2 failed attempts), `mm_img_1440x2560.jpg` (CLI rejected), `mm_vid_h3.mp4` (entitlement blocked), `mm_speech_bm_attempt.mp3` (bad voice id), `mm_speech_bm_indonesian_voice.mp3` with `--language ms` (invalid boost). No Qwen artifact — all three lanes 429.

---

## 12. NOT VERIFIED (honest gaps)

- **MiMo per-model inference** — only `/v1/models` was called. No chat/completion, ASR, TTS, voiceclone or voicedesign call was made. Each model's *serving* status is unproven.
- **MiniMax `MiniMax-Hailuo-2.3-Fast`**, **`Hailuo-02` SEF**, **`S2V-01`** — documented by `--help` only; not invoked.
- **MiniMax `speech-2.6` / `speech-02`** and the `--subtitles` SRT path — not invoked.
- **`mmx text chat`**, **`mmx vision describe`**, **`mmx search query`** — not probed (outside the 7 assigned lanes).
- **Malay intelligibility** of `mm_speech_bm_indonesian_voice.mp3` — audio was produced; correctness of pronunciation is a human judgement and was not asserted.
- **Video quota counter semantics** — the 3/3-vs-success discrepancy is observed but not root-caused.
- **Qwen lane route/param correctness** — 429 fires before model-route validation, so the Token Plan model IDs (`qwen-image-3.0-pro`, `happyhorse-1.1-t2v`, `qwen-audio-3.0-tts-plus`) are **not** confirmed as live on this seat. Re-probe after the quota window resets.
- **`QWEN_API_KEY` vs `DASHSCOPE_API_KEY` ledger separation** — asserted by skill docs, not independently tested.

---

## 13. ROUTING GUIDANCE (what to use, today)

| Need | Use | Because |
|------|-----|---------|
| Still image, any size to 1440×2048 | `mmx image generate --base-url https://api.minimax.io` | WORKS |
| Still image, square ≥2048×2048 | **avoid** — use 1440×2048 or 2048×1152 | deterministic rpc timeout |
| Short video from an image | `mmx video generate --model MiniMax-Hailuo-2.3 --image …` | WORKS, ~105 s/video, daily cap 3 |
| Video with duration/ratio/reference control | **no lane available** | H3 blocked by Token Plan (2013) |
| Malay voice note | `edge-tts --voice ms-MY-YasminNeural` | only native `ms-MY` lane on host |
| Any voice, expressive/narrator | `mmx speech synthesize` (332 voices) | WORKS; no Malay voice exists |
| Qwen Token Plan (image/video/speech) | **nothing** — wait for quota window | 429 on all 3 lanes, all 3 keys |
