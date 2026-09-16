---
name: civic-social-infographic
description: "Use when user asks for infographic for civic topics."
trigger: User asks for infographic, poster, social card, "buat poster", "vs reality", "for the rakyat".
tool_gate: strict
capability_tier: fed-multimodal
ecology_state: WARM
---

# Civic Social Infographic — Dark Mode 9:16

When the deliverable is a **phone-screen-shareable** explainer — not a PDF dossier — this skill applies. Class-level: civic intelligence / sovereign corporate analysis / propa detection / public-facing factual reframing.

## When to Use

- User asks "infographic", "poster", "social card", "for TikTok", "for IG story", "for share"
- Topic is Malaysian civic / corporate / sovereign (PETRONAS, Petros, dividends, fiscal, governance, healthcare reality)
- Goal: convey 3-5 signals in <30 seconds on a phone
- Source input may be propa-leaning (corporate PR, government narrative page) and needs reality check

## When NOT to Use

- Long-form dossier (use `civic-intelligence-pdf`)
- Academic / archival / print-bound (use `scientific-pdf-generation`)
- User wants exact copy of an existing image (use `image-text-editing`)
- Pure data chart with no narrative (use matplotlib directly)

## Output Spec — Proven Aug 2026

**Dimensions:** 1080px wide, height = content-driven (auto). Phone screens vary — design to fill one screen without scroll.

**Palette (dark, high contrast):**
```
Background:    #07070d  (near-black, slight blue)
Panel surface: #0e0d17  (cards)
Border subtle: #26243a
Hero red:      #ff3b30  (problem / hook / on-book contradiction)
Hero green:    #2ecc71  (positive / accountable framing)
Hero blue:     #2f80ed  (data / on-balance-sheet)
Hero amber:    #ff9f0a  (off-balance-sheet / caution / warn)
Hero purple:   #a855f7  (categorical)
Text tier 1:   #ffffff  (headlines)
Text tier 2:   #dfe6ee  (body)
Text tier 3:   #9aa4b2  (captions)
Text tier 4:   #6b7386  (footer / source)
```

**Layout (5-zone vertical):**
1. Header — kicker (13pt, amber, uppercase) + h1 (46pt, mixed colours) + sub (14pt, dim) + gradient divider
2. Hero numbers — 1-2 contrast cards side-by-side
3. Body — 2-4 stacked/grid sections, each with coloured left border
4. Truth box — single red-bordered conclusion (always present)
5. Footer — sources + DITEMPA BUKAN DIBERI

## Stack

- **HTML + inline CSS** → render with Chrome headless → PNG output
- 1 HTML file, all CSS inline, no external dependencies
- Single render, single crop to content-height
- Platform: `google-chrome --headless`

## Mandatory Workflow (Measure → Crop)

**This pattern is required. Skipping it produces empty bands or clipped text.**

```bash
# 1. Build HTML with body { height:auto; overflow:hidden }

# 2. Render oversized to detect content height
google-chrome --headless --disable-gpu --no-sandbox --hide-scrollbars --disable-cache \
  --window-size=1080,2400 --default-background-color=FF07070D \
  --screenshot=/tmp/measure.png "file:///root/forge_work/page.html"

# 3. Measure content bottom with PIL
python3 <<'EOF'
from PIL import Image
im = Image.open('/tmp/measure.png').convert('RGB')
w, h = im.size
px = im.load()
bg = (7, 7, 13)  # match your background EXACTLY
last = 0
for y in range(h-1, -1, -1):
    for x in range(0, w, 40):
        if abs(px[x,y][0]-bg[0]) + abs(px[x,y][1]-bg[1]) + abs(px[x,y][2]-bg[2]) > 25:
            last = y
            break
    if last: break
crop = im.crop((0, 0, w, last + 24))  # +24px breathing
crop.save('/root/forge_work/final.png')
EOF
```

**If content must fill a fixed height (e.g. 1920):** add CSS `zoom:1.X` on the wrapper div, then re-measure. Iterate until bottom row is within ~30px of target. Chrome headless supports `zoom`; WeasyPrint does not.

## Mandatory Pitfalls (Aug 2026 lessons)

### 1. Matplotlib can't wrap text
Filled body text in matplotlib cards overflows silently. **Use HTML+CSS** for any infographic with body text. Reserve matplotlib for decorative numbers and external chart PNGs.

### 2. CSS class colour selectors silently no-op on `.vf.X` patterns
When child `<div>` is inside a flex parent, complex class selectors sometimes lose specificity. **Always inline the colour and width on the bar fill:**
```html
<!-- WRONG — may render invisible -->
<div class="vtrack"><div class="vfill on" style="width:80%"></div></div>

<!-- RIGHT — always renders -->
<div class="vtrack"><div style="width:80%;height:100%;background:#3b9bff;border-radius:8px;"></div></div>
```

### 3. Hard-coded `body { height:1920px; overflow:hidden }` clips content
If content is taller than 1920, bottom rows disappear silently. **Always `height:auto`** + measure-crop.

### 4. Gradients invisible on dark tracks
`linear-gradient(90deg,#2f80ed,#6db2ff)` looks washed out when the only coloured element in a dark row. Use **solid bright colours** on data bars: `#3b9bff`, `#ffa500`, `#ff4444`, `#b066f9`. Reserve gradients for header dividers and hero cards.

### 5. y-axis truncation in source charts
If the input source uses chart with y-axis starting at 100 instead of 0, **rebuild the chart with `ax.set_ylim(0, max*1.15)`** before visualising. Honest scale is non-negotiable for civic work.

### 6. Sources must be auditable
Every number must carry a tag: `[AUDITED]` / `[COMPANY-DISC]` / `[PUBLIC RECORD]` / `[DERIVED]` / `[PROXY]`. Proxy numbers (e.g. RM300B = 3B boe × USD30/boe) get inline footnote in the infographic and a clarifying sentence in the footer.

## Propa Detection Patterns

When the input is a corporate PR or government narrative page, audit before visualising. Proven patterns from Aug 2026 PETRONAS session:

1. **Y-axis truncation** — chart starts at 100 not 0 to exaggerate trend
2. **Strategic omission** — "Cash RM204B" headline, no mention of USD5B bond issued same period
3. **Categorical error** — comparing corporate cash to federal OPEX (different entities)
4. **Symmetric narrative substitution** — pairing "kaya" and "borrowed" as if non-contradictory; they ARE contradictory
5. **Scale-less aggregation** — "Dividen RM32B–RM50B" inflated range (actual FY2025: RM20B)
6. **Anonymous dossiers** — heavy analysis with no author; mark sources as unverified
7. **Selective highlight** — government pension payment success story when actual fiscal collapse is happening

**Counter-frame always:** show the 2 numbers side-by-side. The contradiction IS the story.

## Off-Balance-Sheet Inventory (PETRONAS-style)

When audit topic is sovereign wealth / national oil company / large state enterprise, always inventory off-balance-sheet vehicles:

| Vehicle | Type | Where to verify |
|---|---|---|
| 50:50 JV with foreign IOC | SEARAH (Eni), various LNG JVs | UK Companies House, joint announcement, RCF counsel |
| Renewables SPV | Gentari, Gentari Hydrogen | Portfolio capex announcements |
| Floating LNG | PFLNG Saturn, PFLNG Terra | FID value, operating lease |
| Carbon capture | Kasawari CCS | FID value, CO2 storage capacity |
| Listed subs | PDB, PGB, PCG, MISC | Bursa quarterly (still public) |
| Overseas subs | Energy Canada, Brazil blocks | Local regulator filings |

Rule: if asset is in `JV with foreign partner` or `UK/Cayman/Singapore SPV`, it's almost certainly **off the parent's audited accounts**.

## Language Conventions (BM-Penang for Arif)

- Use "rakyat" not "masyarakat" — closer to user
- "bukan propa", "realiti", "fakta" are powerful civic-vocabulary signals
- Numbers in Malay spelling for voice: "enam belas ribu" not "16,000"
- Code-switch naturally: BM narrative + English technical terms (capex, cash, dividend)
- "Hang" / "kau" / "abang" as register — match user's previous turn
- Avoid academic register in civic deliverables — write for WhatsApp forwards

## Reference Files

- `references/dark-palette-tokens.css` — proven colour variables and component CSS
- `references/propa-detection-checklist.md` — full audit checklist with examples
- `references/chrome-headless-measure-crop.py` — reusable measure-and-crop script (auto-crop after render)

The skeleton HTML is intentionally not templated — each infographic is bespoke to the topic, so copy from a previous `/root/forge_work/petronas_*.html` or similar and modify the body content.

## Verification

After every render:
1. View PNG in vision_analyze
2. Check: any text clipped at edges or bottom? Any white/empty band? Any invisible colour bars?
3. Check: all 5 zones present (header, hero, body, truth, footer)?
4. Check: source line present and audit-tags correct?
5. File size ~300-500KB for 1080×1500-2000 PNG
