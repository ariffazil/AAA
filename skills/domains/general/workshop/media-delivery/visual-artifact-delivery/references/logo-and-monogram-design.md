# Logo & Monogram Design — mmx image generate limits and the SVG fallback

Logo work has a specific failure mode that does not show up in regular image generation: **literal monogram typography is unreliable in diffusion models**. The model interprets letters loosely, substitutes characters, and "hallucinates" a plausible-but-wrong glyph set. Three workable paths exist; pick based on how literal the typography must be.

## When this applies

- User asks for a logo / mark / monogram / wordmark
- User names specific letters that must appear (e.g. "include ARIF in the logo")
- User asks for a brand mark combining typography + symbol
- A heraldic / crest / shield-style mark

## Path ladder — pick by typography literalness

| Path | When | Cost | Verdict |
|---|---|---|---|
| **A. Iterative mmx** | Symbolic mark OK; letterforms can be approximate | 2–4 calls, ~30s each | Good for shields + 3 stripes + star + abstract monogram; letters will be wrong-ish |
| **B. mmx + image-edit** | Existing render is 90% right; need to add or correct 1–2 elements | 1 base call + 1–2 edits | Faster than regenerating; risk of edit drift |
| **C. Hand-crafted SVG/HTML, rasterise** | Letters must be exact (real monogram, wordmark, brand spelling) | One shot, precise | The only path that delivers literal typography reliably |

## The literal-typography failure mode

When the prompt says "ARIF + IRFAN merge monogram, with I as central axis, A as crown, R+F as three diagonal claws, N as tail", the model returns any of:

- Letters the user did not ask for (T instead of I, R instead of N)
- A vertical "spire" or "needle" that subsumes the I
- Stripes/claws that don't read as separate letterforms
- A "monogram" that is actually two random letters

The model is strong at composition, color, and symbol language. It is **weak at literal letterform composition under multi-letter constraints.** A stricter prompt does not fully solve it — model interprets "EXACTLY these letters must appear" as a list of things to include, then chooses one interpretation.

## Path C — hand-crafted SVG/HTML (when A and B fail)

Build the SVG directly, then rasterise via headless browser or `cairosvg`. This is the only path that delivers literal typography because no diffusion model is involved.

```bash
# Install once
pip install cairosvg --break-system-packages

# Build the SVG (write file, do not inline)
cat > /tmp/logo.svg <<'EOF'
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="512" height="512">
  <!-- shield -->
  <path d="M128 16 L232 56 L232 152 Q232 216 128 240 Q24 216 24 152 L24 56 Z"
        fill="#1a2747" stroke="#4a5568" stroke-width="4"/>
  <!-- monogram letters as paths/text -->
  <text x="128" y="160" text-anchor="middle" font-family="DejaVu Sans, Arial, sans-serif"
        font-weight="900" font-size="120" fill="#ff7849">i</text>
  <text x="128" y="80"  text-anchor="middle" font-family="DejaVu Sans, Arial, sans-serif"
        font-weight="900" font-size="48"  fill="#ff7849">A</text>
  <!-- 3 diagonal claws -->
  <line x1="60"  y1="100" x2="200" y2="180" stroke="#cbd5e0" stroke-width="8"/>
  <line x1="60"  y1="120" x2="200" y2="200" stroke="#cbd5e0" stroke-width="6"/>
  <line x1="60"  y1="140" x2="200" y2="220" stroke="#cbd5e0" stroke-width="4"/>
</svg>
EOF

# Rasterise
python3 -c "import cairosvg; cairosvg.svg2png(url='/tmp/logo.svg', write_to='/root/.hermes/identity/logos/irfanclaw-v5.png', output_width=512, output_height=512)"
```

Then run the verify-before-send loop (`vision_analyze` on the PNG; check letterforms, alignment, palette).

## Variant naming convention

```bash
# Save under ~/.hermes/identity/logos/ — keep the vN suffix for comparison
~/.hermes/identity/logos/<agent>-v1_001.jpg   # first variant
~/.hermes/identity/logos/<agent>-v2_001.jpg   # second
~/.hermes/identity/logos/<agent>-vN_001.jpg
```

`mmx image generate` saves as `<prefix>_001.jpg` — the `_001` is from the CLI, do not strip it.

## Pitfalls

- **Don't rewrite the prompt to fight the model.** Stricter prompts buy small gains; the limit is structural (diffusion models don't compose letterforms reliably). When literal typography matters, skip diffusion entirely.
- **Always include a color anchor.** Without explicit hex codes (e.g. `navy #1a2747, ember #ff7849`) the model chooses its own palette and produces inconsistent variants. Hex anchors keep v1/v2/v3 on the same family.
- **Square 1:1 for app icons.** Telegram avatars, favicons, and profile photos are square. Other ratios waste pixels.
- **`--aspect-ratio 1:1` + `--seed 42`** = reproducible first variant. Change `--seed` for each retry; same seed + same prompt = identical output, useful for QA but useless for variety.
- **The verify pass must include a letterform check.** Ask the vision model `What letters can you see? Quote them.` — not just "describe the design". The literal-typography failure mode is invisible to a generic description pass.

## Hand-off pattern when stuck

When paths A and B fail to deliver the user's named letters, do not loop on the diffusion model. Surface the trade-off in one binary choice:

> mmx boleh bagi symbol + composition, tapi huruf literal x boleh. Dua cara: (a)terima abstract mark dengan huruf lebih kurang, atau (b)buat SVG sendiri dengan huruf tepat, rasterise. Mana satu?

Default if the user wants the brand to read at a glance: **(b) hand-crafted SVG.** Default if visual strength matters more than letter accuracy: **(a) accept abstract mark.**

## Example — irfanclaw mark (2026-09-24)

Four `mmx image generate` calls iterated from a clean shield+stripes+star composition toward the ARIF+IRFAN monogram. None delivered literal letterforms:

| Variant | What came out | Lesson |
|---|---|---|
| v1 | Shield + 3 diagonal stripes + "i" monogram + sparkle | Strong composition; "i" lucky guess |
| v2 | Geometric + drop shadow + abstract P-shape | Drift — too abstract, no heraldic anchor |
| v3 | "AR" interlocked with vertical spire | A+R present; no I, no N, claws missing |
| v4 | Shield + 3 stripes + star + "TAR" letters | Closest to monogram; model substituted T for I |

**Verdict:** v4 strongest visually but letters wrong. User chose to defer the SVG path until next session. Path C remains available.
