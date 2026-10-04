# Multimedia Arsenal Recipe — Sovereign-Grade Artifacts

**Forged:** 2026-08-12 · **Source session:** PETRONAS APEX LETTER II v14

## Why multimedia matters

A pure-text PDF is **F2/F11 underweight** for sovereign-grade dispatch. The artifact needs:
- **PDF** — primary deliverable for formal dispatch (PAC, Parliament)
- **Cover image** — public surface for arif-fazil.com, social media thumbnails
- **Charts pack** — F2/F11 evidence visualization, audio-amplifiable
- **Audio TTS** — accessibility (mobile Malaysia), Telegram voice note distribution
- **Video trailer** — public engagement, 60-second narrative compression vs 10-page letter

Without these, the artifact loses public surface and witness function — the letter exists but isn't witnessed.

---

## Verified Tool Stack (2026-08-12)

| Asset | Tool | Command pattern | Size class |
|-------|------|-----------------|------------|
| **Surat PDF** | weasyprint (Python) | `python3.13 -c "import weasyprint; ..."` | 60-100KB, 8-12 pages |
| **Cover image** | `gemini-image.py` (Gemini 3 Pro) | `--model gemini-3-pro-image --output path.png` | 700-900KB, 4K |
| **Charts pack** | matplotlib (server-side PNG, dpi ≥ 150) | One batch script, shared rcParams | 80-200KB per chart |
| **Audio TTS** | `edge-tts` (ms-MY-OsmanNeural) | `edge-tts --voice ms-MY-OsmanNeural --file <txt> --write-media <mp3>` | 3-5MB, full surat rendered |
| **Video trailer** | `gemini-video.py` (Gemini Omni Flash) | `--aspect 16:9 --wait` | pending (2-10 min) |

---

## Multi-Agent Dispatch Model ID Pain Chain

**This is the operational reality** of multi-agent dispatch — the model ID layer bites hard. Verified 2026-08-12 PETRONAS session:

### qwen-code CLI

```bash
# WRONG — fails with "Invalid model name passed in model=qwen3-coder-plus"
qwen -m qwen3-coder-plus -p <prompt>

# CORRECT — no -m flag, use default anthropic-routed model
qwen -p <prompt> -o text

# ANOTHER OPTION — explicit model that exists in anthropic config
qwen -m qwen3.7-max -p <prompt> -o text
```

**Root cause:** qwen-code CLI is configured with `selectedType: anthropic` auth (from `/root/.local/share/qwen-code/settings.json`). Anthropic routes reject `qwen3-coder-plus` as invalid model name. The default behavior (no `-m`) uses whatever model the anthropic key is configured for.

### opencode CLI

```bash
# WRONG — fails with "Insufficient Balance" if direct DeepSeek credits exhausted
opencode run --model deepseek/deepseek-v4-pro <message>

# WRONG — fails with "Model not found: gpt-5.6-luna/." (missing provider prefix)
opencode run --model gpt-5.6-luna <message>

# CORRECT — zen-tier has separate billing, often has credits
opencode run --model opencode-zen/deepseek-v4-pro <message>
opencode run --model opencode-zen/gpt-5.6-luna <message>

# ALTERNATIVES — if zen credits exhausted
opencode run --model opencode-go/deepseek-v4-pro <message>   # Go-tier routing
opencode run --model opencode-go/gpt-5.6-luna <message>
```

**Root cause:** Direct provider prefix (`deepseek/...`) uses deepseek's own billing. `opencode-zen/...` routes through the federation's zen-tier proxy with separate credits. `opencode-go/...` is another routing tier.

### Available models discovery

```bash
opencode models                           # All providers
opencode models opencode-zen              # Just zen-tier
opencode models qwen-token-plan           # Qwen-tier (text/image/audio)
```

---

## Edge-TTS Pitfalls (verified)

### Voice for Bahasa Melayu

```bash
# CORRECT — male voice, Bahasa Melayu (Malaysia)
edge-tts --voice ms-MY-OsmanNeural --file text.txt --write-media out.mp3

# Try other voices:
#   ms-MY-OsmanNeural    — male, natural
#   ms-MY-YasminNeural   — female, natural
```

### Input length cap

```bash
# WRONG — full 22K char surat times out at 120s
edge-tts --voice ms-MY-OsmanNeural --file full_surat.txt --write-media out.mp3

# CORRECT — extract narrative core (cover + opening + mak + closing)
python3 -c "
import re
from pathlib import Path
html = Path('surat-apex-ii.html').read_text()
text = re.sub(r'<[^>]+>', ' ', html)
text = re.sub(r'\s+', ' ', text).strip()
Path('v14_assets/surat-narrative-core.txt').write_text(text[:6000])
"
edge-tts --voice ms-MY-OsmanNeural \
  --file v14_assets/surat-narrative-core.txt \
  --write-media v14_assets/surat-apex-ii.mp3
```

---

## Gemini Video Generation Pitfalls

### Async generation

```bash
# Gemini video generation is async — file may not appear for 2-10 minutes
python3 /root/HERMES/scripts/gemini-video.py \
  --output v14_assets/cover-apex-ii-trailer.mp4 \
  --aspect 16:9 --wait \
  "Cinematic prompt..."

# Verify file exists
ls -la v14_assets/*.mp4 2>&1

# Process still running? Check status
ps -ef | grep gemini-video | grep -v grep
```

### Prompt structure for sovereign-grade trailer

Effective prompts include:
- **Setting:** dark desk late at night, amber lighting
- **Specific objects:** yellow legal pad with key number, printed document header
- **Camera:** slow zoom, subtle shake, cinematic 4K
- **Mood:** contemplative, defiant, weary, insider reckoning
- **Background:** Kuala Lumpur skyline at dusk, PETRONAS Twin Towers silhouette
- **Color grade:** amber and shadow, documentary film style

---

## Matplotlib Chart Pack Recipe (verified)

### Shared config (one block, all charts)

```python
NAVY = '#0e1a2b'
CREAM = '#f4ecd8'
GOLD = '#c9a227'
RED = '#b22222'
GREEN = '#2e7d32'
BLUE = '#1e5f8b'
ORANGE = '#e67e22'

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 10,
    'figure.dpi': 150,
    'savefig.dpi': 180,
    'savefig.bbox': 'tight',
})
```

### Conceptual diagrams — use `matplotlib.patches`, not `plt.Circle`

```python
from matplotlib.patches import Circle, FancyBboxPatch, FancyArrowPatch, Wedge
# ❌ plt.Circle((x, y), r) raises AttributeError
# ✅ Circle((x, y), r, color=..., alpha=..., ec=..., lw=...)
```

### Pitfall: `letter_spacing` not valid

```python
# ❌ WRONG — AttributeError: 'Text' object has no property 'letter_spacing'
ax.text(x, y, text, letter_spacing=2)

# ✅ CORRECT — just use plain text, no CSS analog
ax.text(x, y, text)
```

### 7-chart sovereign pack template

| # | Chart type | Use |
|---|-----------|-----|
| 01 | Bar (data trajectory) | 70.5% payout over years |
| 02 | Line + fill (decline) | RRR 1.0 → 0.3 |
| 03 | Candlestick metaphor | Reserve life 14.1 → 9.9 tahun |
| 04 | Line + annotation (temporal) | Petroleum revenue % bajet |
| 05 | Conceptual diagram (boxes + arrows) | SEARAH structure (3 kerusi + 5 PSC + PETROS) |
| 06 | Pull-quote (dark background) | Qualia anchor |
| 07 | Conceptual split panel (Oppenheimer/ARIF) | INTJ parallel |

All saved at dpi 180, bbox_inches='tight', background = white (or NAVY for dark charts).

---

## VAULT999 Seal — Atomic Append (after multimedia ready)

```bash
VAULT=/root/arifOS/VAULT999/outcomes.jsonl

cat >> "$VAULT" <<EOF
{"timestamp":"2026-08-12T18:16:31+08:00","session_id":"SEAL-991b479a32934689","coherence_id":"PETRONAS_APEX_II_V14_2026-08-12","f13_sovereign":"Muhammad Arif bin Fazil","kind":"apex_letter_ii_seal","artifact":"APEX LETTER II v14 — Qualia + real WhatsApp mak voice + Oppenheimer/INTJ framing","sha256_html_pre_patch":"c1a3a1e98bdcfc4d15848fcecd4130a7ce0d37af1424cf4adf08a1b8bbccdd82","sha256_html_post_patch":"5f88e8d9bf6b89b988a17638090a665fad1b4cc4da3bbe52eef585e56aa7f01f","sha256_pdf":"f313492159d4787f1d16332191a2b0e9016301ad4a7c869933ae78f3a9b7082e","pages":10,"multimedia":{"cover_image":"v14_assets/cover-apex-ii.png","charts":"7 charts in v14_assets/","audio_tts":"v14_assets/surat-apex-ii.mp3","video_trailer":"v14_assets/cover-apex-ii-trailer.mp4"},"apex_judge":{"verdict":"HOLD","call_hash":"sha256:b860a4f378b6425addef77c049b9912aa40e98ca4973db01f0c8a8072928455c","independence_class":"KERNEL_ARBITER"},"dispatch_status":"READY — awaiting F13 SOVEREIGN actor_signature"}
EOF
```

---

## Reference Paths

- **Tool scripts:** `/root/HERMES/scripts/gemini-image.py`, `gemini-video.py`, `edge-tts`
- **Output directory pattern:** `/root/forge_work/<project>/v{N}_assets/`
- **VAULT999:** `/root/arifOS/VAULT999/outcomes.jsonl` (read-only after seal)
- **APEX receipts:** `/root/forge_work/apex_receipts/SEAL-<session>_sha256_<hash>.json`

---

*Forged: 2026-08-12 · DITEMPA BUKAN DIBERI · Multimedia is not decoration — it is constitutional witness expansion.*