# Federation Logo System — Color & Material Map
> Generated: 2026-08-10 | Updated: 2026-08-10 | For: logo/avatar generation across lanes and organs

## Active Logos — Photorealistic Medallions (Gemini AI gen)

| Entity | Material Aesthetic | Color | Hex | File |
|--------|-------------------|-------|-----|------|
| **ASI** (555) | Gold guild coin, patina, sculpted wings | Bright Gold | #FFD700 | asi-tactile-circle.png |
| **AGI** (333) | Tempered steel, neural lattice, forge sparks | Electric Cyan | #00D4FF | agi-tactile-circle.png |
| **AAA** (control) | Jade stone, molten gold inlay, council seal | Emerald Green | #00FF88 | aaa-tactile-v2-circle.png |
| **FORGE** (777) | Blacksmith maker's mark, hammered steel, ember | Orange-Red | #FF4400 | forge-tactile-circle.png |

## Active Logos — Code-Rendered SVG Icons (deterministic, pixel-perfect)

| Entity | Symbol | Accent Color | Hex | File |
|--------|--------|-------------|-----|------|
| **AGI** (333) | Open book | Violet | #c084fc | svg_agi.png |
| **ASI** (555) | Neural network | Cyan | #22d3ee | svg_asi.png |
| **AAA** (control) | Shield + crown dots | Gold | #fbbf24 | svg_aaa.png |
| **FORGE** (777) | Anvil + hammer + sparks | Orange | #f97316 | svg_forge.png |
| **F13 SOVEREIGN** | Crown + gem dots | White | #f5f5f5 | svg_sov.png |

## When to Use Which

| Use Case | Route | Why |
|----------|-------|-----|
| Telegram bot profile photo | **Medallion** (AI gen) | Tactile, physical, premium feel |
| Inline text accompaniment | **SVG icon** (code-render) | Crisp at any size, consistent |
| Lane card visual | **SVG icon** (code-render) | Deterministic, fast to render |
| Website/observatory badge | **Medallion** (AI gen) | Visual impact at large size |
| Quick share to human | **Medallion** (AI gen) | "Something you can hold" |

## Color Logic
Each entity has a distinct hue for instant visual identification:
- Gold = sovereignty/ASI (wealth, authority)
- Cyan = intelligence/AGI (cold, precise, cognitive)
- Green = institution/AAA (stable, growth, governance)
- Orange-Red = execution/FORGE (heat, action, creation)

## Circle Crop Pattern
All logos are circle-cropped for Telegram avatar compatibility.
Mask: `/tmp/circle_mask.png` (1024×1024, ffmpeg-generated)
Apply: `ffmpeg -i INPUT -i mask -filter_complex "alphamerge" OUTPUT`

## Generation Notes
- AI gen: Gemini `gemini-2.5-flash-image` with `responseModalities: ['IMAGE']`
- SVG gen: HTML+SVG → `google-chrome --headless --screenshot` → PNG
- Short prompts (<100 words) + material vocabulary = reliable AI image output
- Long descriptive prompts → text-only response (Gemini trap)
- Arif's preference: TACTILE/MATERIAL > flat/vector for AI gen; crisp/clean for SVG
- Both skills cover this: `ai-media-generation` (umbrella) + `ai-media-generation-ops` (subset)
