---
name: hermes-vision-fix
description: Fix Hermes Agent cannot analyze images — vision_analyze fails for local files, correct pipe is mmx vision describe
triggers:
  - "vision tool fails"
  - "gambar tak boleh baca"
  - "vision_analyze error"
  - "Hermes image analysis broken"
---

# Hermes Vision Fix — SOUL.md + Config + Command Stack

## Trigger
- Hermes Agent tidak boleh analyze gambar yang Arif hantar
- `vision_analyze` tool gagal untuk local files
- Error patterns: "file valid (720x1280 JPEG) tapi sistem tak boleh baca"

## Root Causes Found

1. **Wrong vision tool** — Hermes default `vision_analyze` tool digunakan untuk local files, tapi tool itu expect URL/image external. Local JPEG dalam cache takleh baca.
2. **Wrong personality** — `config.yaml` ada `display.personality: ASI_Wellness` (wellness bot persona), bukan `hermes`
3. **Auto vision provider** — `auxiliary.vision.provider: auto` yang boleh pilih provider yang salah

## The Fix (3-part stack)

### Part 1: Config — `/root/.hermes/config.yaml`

```yaml
display:
  personality: hermes        # was: ASI_Wellness

auxiliary:
  vision:
    provider: minimax        # was: auto
    model: MiniMax-M2.7      # explicit
    timeout: 120
```

### Part 2: SOUL.md — `/root/.hermes/SOUL.md`

Hermes SOUL.md perlu ada VISION section yang bagitahu correct workflow:

```
## Vision — Primary Method

GAMBAR DARI ARIF = SIMPEL:

1. Terminal: mmx vision describe <file_path>
2. Return stdout as answer

mmx CLI ada di /usr/bin/mmx, pre-authenticated, sentiasa available.

Jangan guna vision_analyze untuk local files — ia akan gagal.
Jangan guna ImageMagick atau tesseract sebagai fallback primary.
```

### Part 3: Command Reference — `/srv/openclaw/workspace/commands/vision.md`

Write command reference untuk OpenClaw bot yang explain correct vision pipe.

## Correct Vision Workflow

```
1. Arif hantar gambar → saved ke /root/.hermes/cache/images/
2. RUN mmx vision describe /root/.hermes/cache/images/img_<hash>.jpg
3. Return stdout sebagai jawapan
```

## Telegram Image Cache (Key Discovery 2026-05-07)

When Arif sends an image in Telegram, it gets cached at:
```
/root/.hermes/cache/images/img_<sha_hash>.jpg
```

**Critical: `vision_analyze` tool FAILS on these local cached files.**
Always use `mmx vision describe` for cached Telegram images.

```bash
# Find most recent cached image
ls -lath /root/.hermes/cache/images/ | head -5

# Describe it (confirmed working 2026-05-07 with arifOS QR code card)
mmx vision describe /root/.hermes/cache/images/img_f1c754a97a74.jpg
# Output: Brand Name, arifOS, Slogan "DITEMPA BUKAN DICARI", QR code
```

## Additional Findings (2026-05-05)

- **WELL container debugging**: Inside Docker containers, `curl` often not available. Use Python instead:
  ```
  docker exec well python3 -c "import urllib.request,json; print(json.loads(urllib.request.urlopen('http://localhost:8083/health',timeout=5).read()))"
  ```
- **WELL GHCR push**: Image layers often already exist on GHCR — push is fast (streamable-v2 pushed in <5s). Verify with `docker manifest inspect ghcr.io/ariffazil/well:streamable-v2` or check digest in output.
- **Post-push verification**: After pulling new WELL image on VPS, must `docker stop well && docker rm well && docker run...` — image label change does NOT auto-restart running container.

## Verification

```bash
# mmx vision works — confirmed 2026-05-05
mmx vision describe /root/.hermes/cache/images/img_0bb5683c4e23.jpg
# ✅ Bill Gates memoir "Source Code: My Beginnings" — fully described
mmx vision describe /root/.hermes/cache/images/img_54a65e8506d0.jpg
# ✅ "The Art of Spending Money" by Morgan Housel — fully described

which mmx && mmx --version
# ✅ mmx 1.0.12 at /usr/bin/mmx
```

## Key Files Changed

| File | Change |
|------|--------|
| `/root/.hermes/config.yaml` | `personality: hermes`, `vision.provider: minimax` |
| `/root/.hermes/SOUL.md` | Added Vision section with mmx workflow |
| `/srv/openclaw/workspace/commands/vision.md` | Command reference for OpenClaw |

## Gotchas

- `mmx` pre-authenticated — tak perlu API key dalam command
- `vision_analyze` tool FAIL untuk local files — tool itu expect URL
- `ASI_Wellness` personality loaded instead of `hermes` — indicates previous config corruption or manual override
- After config change, Hermes needs restart: `kill <pid>` + `hermes gateway run`

## Related
- `hermes-personality-stack` skill — Hermes SOUL + personality overlay architecture
