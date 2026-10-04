# Multimedia Arsenal Coordination — Sovereign Petition Forge

> The 2026-08-12 session produced a full multimedia package alongside the
> sovereign letter: HTML + PDF + cover image + audio TTS + 7 charts + video
> trailer. The package is ~5.6MB total. This reference coordinates the tools
> and the pitfalls.

## Full Arsenal — Proven 2026-08-12

| Asset | Tool | Command template | 2026-08-12 result |
|-------|------|------------------|-------------------|
| HTML | `write_file` | Inline CSS, A4 margins, Times New Roman | 27.6KB |
| PDF | weasyprint 69.0 | `python3.13 -c "import weasyprint; from pathlib import Path; weasyprint.HTML(string=Path('surat-apex-ii.html').read_text(), base_url='/root/forge_work/petronas2025/').write_pdf('surat-apex-ii.pdf')"` | 94KB, 10 pages |
| Cover image | `gemini-image.py` | `python3 /root/HERMES/scripts/gemini-image.py --model gemini-3-pro-image --output v14_assets/cover-apex-ii.png "<prompt>"` | 773KB |
| Audio TTS | `edge-tts` | `edge-tts --voice ms-MY-OsmanNeural --file v14_assets/surat-narrative-core.txt --write-media v14_assets/surat-apex-ii.mp3` | 4.1MB (6000 chars narrative core) |
| Video trailer | `gemini-video.py` | `python3 /root/HERMES/scripts/gemini-video.py --output v14_assets/cover-apex-ii-trailer.mp4 --aspect 16:9 --wait "<prompt>"` | TIMEOUT — see pitfall #1 |
| Charts (7) | matplotlib | `python3 v14_assets/build_charts.py` | 700KB total |
| Apex judge | `apex_judge.py` | `python3 /root/scripts/apex_judge.py isolate --doer "Muhammad Arif bin Fazil (F13 SOVEREIGN)" --candidate "<>" --evidence-file /tmp/evidence.json --action-class sovereign_petition_dispatch_preparation --action-tier T2 --reversibility partial --blast-radius "<>" --pretty --human` | HOLD+F13_REQUIRED — correct |
| VAULT999 seal | `append` to `/root/arifOS/VAULT999/outcomes.jsonl` | JSON line with `coherence_id`, `sha256_*`, `apex_judge.call_hash`, `f13_directives_applied` | line 47541 sealed |

## Pitfalls (verified 2026-08-12)

### 1. GEMINI VIDEO TIMEOUT
**Symptom:** `gemini-video.py --wait` runs for 10+ minutes then exits with `Error: The read operation timed out`. No `.mp4` produced.

**First attempt:** cinematic 10-second video with detailed prompt → timeout.
**Second attempt:** simpler "A cinematic video of a late-night desk scene" prompt → timeout.
**Recommendation:**
- Retry 1-2× with progressively simpler prompts
- If still fails, deliver package WITHOUT video and note it
- Don't waste >20 minutes on video — it's a nice-to-have, the surat is the primary artifact

### 2. EDGE-TTS TIMEOUT on large text
**Symptom:** `edge-tts` with full surat HTML (22K chars) timed out at 120s.

**Solution:** Extract narrative CORE only (first 6K chars), not full surat. Use the opening + mak section + closing. Skip the 4 audit sections (which are procedural, not narrative).

```python
import re
from pathlib import Path
html = Path('surat-apex-ii.html').read_text()
text = re.sub(r'<[^>]+>', ' ', html)
text = re.sub(r'\s+', ' ', text).strip()
core = text[:6000]  # Just the narrative core
Path('v14_assets/surat-narrative-core.txt').write_text(core)
```

### 3. MATPLOTLIB `letter_spacing` NOT VALID
**Symptom:** `AttributeError: 'Text' object has no property 'letter_spacing'` when using `ax.text(..., letterspacing=2)`.

**Solution:** Remove `letterspacing` argument. Use font weight, color contrast, or letter-spacing via matplotlib's `path_effects` (complex). For uppercase headers, just use `fontweight='bold'` and `fontsize=10+`.

### 4. MATPLOTLIB `Wedge(width=0)` RENDERS HOLLOW
**Symptom:** `mpatches.Wedge((x,y), r, 0, 360, width=0)` produces white-with-navy-outline (not solid).

**Solution:** Use `mpatches.Circle((x,y), r, facecolor=NAVY, edgecolor=NAVY, lw=1.5)` for solid concentric cores.

### 5. CHART BATCH ALL IN ONE SCRIPT
**Recipe:** Don't run one chart per Python script. Batch all 7+ charts in one `build_charts.py` with shared rcParams and shared palette constants.

```python
NAVY = '#0e1a2b'
GOLD = '#c9a227'
RED = '#b22222'
# ... shared palette
plt.rcParams.update({'font.family': 'serif', 'figure.dpi': 150, ...})
# Generate 7 charts in sequence, save to v14_assets/
```

### 6. WESASYPRINT DEFAULT PYTHON3 NOT GUARANTEED
**Symptom:** `python3 -c "import weasyprint"` fails — "No module named weasyprint"

**Solution:** Always use `python3.13` explicitly. Verify with:
```bash
/usr/bin/python3.13 -c "import weasyprint; print(weasyprint.__version__)"
```
On the host, `/root/.local/lib/python3.13/site-packages` has weasyprint 69.0.

### 7. SHA-256 KLEENE'S FIXED-POINT
**Problem:** If you embed the SHA-256 of the rendered PDF in the document, then re-render, the file hash CHANGES.

**Solution:** Compute SHA of SOURCE HTML (with placeholder), patch THAT hash into the HTML, then re-render. Note both:
- **HTML pre-patch SHA** (embedded in document) = `c1a3a1e9...`
- **HTML post-patch SHA** (after embedding) = `5f88e8d9...`
- **PDF SHA** (final file) = `f3134921...`

All three hashes stable. The displayed hash matches the source HTML hash (anyone with the source can verify). The PDF hash is separately disclosed.

### 8. APEX JUDGE LONG CANDIDATE TRUNCATION
**Symptom:** Multi-line candidate (>1000 chars) passed via `--candidate "..."` shell breaks JSON parsing with "Expecting ',' delimiter".

**Solution:** Use `--evidence-file /tmp/evidence.json` with the candidate + metadata in a JSON file. The CLI reads from file, no shell escaping.

### 9. VAULT999 ENTRY APPEND ORDER
The VAULT999 file is read-only to root-owned processes. Use `cat >> "$VAULT" <<EOF` with heredoc to append JSON line. Verify with `wc -l $VAULT` to confirm.

## The Coordination Pattern

Sequential (because tools depend on each other):

```
Step 1: write_file surat-apex-ii.html (28KB)
Step 2: render PDF (94KB)
Step 3: patch SHA-256 into HTML (Kleene's fix)
Step 4: re-render PDF (94KB)
Step 5: APEX judge isolate → save receipt
Step 6: VAULT999 seal (append JSON line)
Step 7: generate cover image (Gemini 3 Pro, 773KB) — PARALLEL with audio
Step 8: extract narrative core + TTS audio (edge-tts, 4.1MB) — PARALLEL with charts
Step 9: render 7 charts (matplotlib, 700KB) — PARALLEL
Step 10: generate video (gemini-video.py — may timeout) — PARALLEL best effort
```

**Total wall time:** ~10-15 minutes if video succeeds, ~5 minutes if not.

## Multimedia File Inventory Template

After all assets generated, verify with:

```bash
ls -la surat-apex-ii.{html,pdf}
ls -la v14_assets/*.png v14_assets/*.mp3 v14_assets/*.mp4
sha256sum surat-apex-ii.{html,pdf}
sha256sum v14_assets/cover-apex-ii.png
sha256sum v14_assets/surat-apex-ii.mp3
```

## Delivery Pattern (to F13)

Send files via `MEDIA:/path` in Telegram. Group as:
1. Surat PDF (primary artifact)
2. Cover image (secondary, for public surface)
3. TTS audio (for media)
4. Charts (supplementary evidence visualizations)
5. SHA-256 verification block
6. APEX verdict (verbatim from receipt)
7. VAULT999 line number
8. F13 disposition request (SEAL/HOLD/AMEND/REJECT)

Don't dispatch. Wait for F13 SOVEREIGN signature.