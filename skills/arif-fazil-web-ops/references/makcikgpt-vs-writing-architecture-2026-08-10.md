# MakcikGPT vs Writing — Architecture Mapping (2026-08-10)

## Deployment Architecture

### MakcikGPT

| Surface | URL | Served from | How |
|---------|-----|-------------|-----|
| Browser | `/world/makcikgpt/` | SPA shell (`index.html`) | React renders client-side |
| Bot UA | `/world/makcikgpt/<slug>/` | `makcikgpt-md/<slug>.html` | Caddy `@ai-bot-world` strips prefix |
| No-JS | same | `makcikgpt-md/<slug>.html` | Caddy `@makcikgpt_nojs` |
| Static landing | `/world/makcikgpt/` | `makcikgpt-md/index.html` | Bot/No-JS only |

**4 registers to publish one article:**
1. `src/data/makcikgpt/<slug>.ts` — body (html template literal)
2. `src/data/makcikgpt/index.ts` — import + meta array (3 edits)
3. `src/data/essays.json` — machine index
4. `public/makcikgpt-md/<slug>.html` — bot-serving static HTML

**Caddy routing (3 matchers, 3 disk roots):**

| Matcher | UA | Root | Serves |
|---------|-----|------|--------|
| `handle /world/makcikgpt/*` | Browser | `/var/www/html/arif` → SPA | React shell |
| `@ai-bot-world` | GPTBot, ClaudeBot, curl... | `makcikgpt-md/` | Static article |
| `@makcikgpt_nojs` | Non-HTML Accept | `makcikgpt-md/` | Static article |

### Writing

| Surface | URL | Served from | How |
|---------|-----|-------------|-----|
| Browser | `/words/writing/` | SPA shell | React `EssayPage` renders |
| Listing | `/words/writing/` | `words/writing/index.html` | Static (`@static_dirs`) |
| Per-essay | `/words/writing/<slug>/` | SPA shell | React renders from `.ts` data |
| Bot UA | same path | SPA shell (no bot branch) | Bots get SPA |

**5 registers to publish one essay:**
1. `src/data/essays/<NN>-<slug>.ts` — body (EssayContent interface)
2. `src/data/essays/articles.json` — slug list with metadata
3. `src/data/essays/index.ts` — import + meta + CURATED_SLUGS (4 edits)
4. `public/words/writing/index.json` — machine-readable listing
5. `src/App.tsx` — SPA route (`/words/writing/:slug`)

**Caddy routing:**

| Matcher | Path | Serves |
|---------|------|--------|
| `@static_dirs` | `/words/writing/` | Static `index.html` (listing) |
| `@spa_routes` | `/words/writing/*` | SPA shell → React renders essay |
| (no bot branch) | — | Bots get SPA (no pre-rendered HTML) |

## Design Contrast

| Dimension | MakcikGPT | Writing |
|-----------|-----------|---------|
| **Language** | Bahasa Melayu (kampung) | English (academic) |
| **Voice** | Makcik at pasar malam | Arif the systems architect |
| **Tone** | Investigative, punchy, rhetorical | Philosophical, analytical, structured |
| **Hero** | Title + description paragraph | Compass SVG + T.S. Eliot quote |
| **Accent color** | Red (#E4572E) | Gold/Amber (#D4A24C) |
| **Tags** | Domain-specific (10+ per article) | Uniform (seal 999 · INT) |
| **Registers to publish** | 4 | 5 |
| **Bot rendering** | Static pre-rendered HTML | SPA only (no bot branch) |
| **SPA route** | `/world/makcikgpt/:slug` | `/words/writing/:slug` |
| **Listing** | SPA card grid + static bot index | Static `index.html` |
| **CSS** | System fonts, inline styles | Premium fonts, shared design system |
| **Article format** | `.ts` html template literal | `.ts` EssayContent interface |
| **Content scope** | Political/civic journalism | AI governance/institutional theory |
| **Audience** | Malaysian public (jiran-jiran) | Global (AI researchers, thinkers) |
| **Caddy matchers** | 3 (browser/bot/noJS) | 2 (static_dirs/spa_routes) |
| **Dual-witness verify** | Mandatory (4-gate) | SPA-only (curl unreliable) |

## Shared Patterns

| Pattern | Both use |
|---------|----------|
| **5-lane nav** | HOME · EARTH · WORDS · WORLD · WORK |
| **Brand** | ARIF FAZIL (top bar) |
| **Dark theme** | Black bg, light text |
| **Deploy** | `npm run build` → `deploy-site.sh --apply` |
| **Source of truth** | `.ts` files with html template literals |
| **SPA rendering** | React client-side for browsers |
| **Static fallback** | Bot/No-JS get pre-rendered HTML |
| **Tagline** | "Ditempa bukan diberi" |
| **Footer** | Byline + seal + date + source paths |
| **Article pattern** | kicker → h1 → hr → body → footer |

## Key Architectural Difference

**MakcikGPT has a bot branch. Writing doesn't.**

MakcikGPT serves pre-rendered static HTML to AI crawlers via Caddy's `@ai-bot-world` matcher. Writing has NO bot branch — bots get the SPA shell.

**Implication:** Essays published under Writing may not be visible to AI crawlers. MakcikGPT articles are always visible to bots. Trade-off: reach vs voice.

## Design Alignment Principle

**Contrast yet federated:** Same card pattern (MakcikGPT benchmark), different accent color (red vs gold). Same nav, same brand, different voice.

- MakcikGPT: red accent line, BM voice, domain-specific tags
- Writing: gold accent line, English academic, series tags (S4/S6/S8)
