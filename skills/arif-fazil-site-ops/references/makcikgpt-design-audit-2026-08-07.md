# MakcikGPT Design Audit — visual language for the Writing surface

Captured 2026-08-07 from `https://arif-fazil.com/world/makcikgpt/suara-terlalu-siap`.
Use this when designing ANY long-form essay page (`/words/writing/<slug>/`,
`/world/makcikgpt/<slug>/`) — the SPA EssayPage already implements all of this; this
file is the visual contract for future component work.

## Top navigation

- Dark charcoal/near-black background (~#0e0e0e to #141414)
- Brand mark left: "ARIF FAZIL" (white, uppercase, small caps tracking)
- Nav links right: HOME | EARTH | WORDS | WORLD | WORK — white uppercase, separated by pipes

## Article header (the "splash" zone)

- Breadcrumb: `← ESSAYS` muted gray
- Section label: small uppercase "NARRATIVE · Ψ SOUL · DIRECT PUBLICATION" in
  `text-forge-gold` (`#c9a84c`)
- H1 title: `text-3xl md:text-5xl lg:text-6xl font-black italic uppercase
  leading-[0.92] tracking-tighter text-forge-white` — dramatic display type
- Hook/dek: `text-forge-dim text-base md:text-lg leading-relaxed border-l-2
  border-forge-gold pl-4` — gold left-border callout under the title
- Metadata row: date pill (forge-iron border), 999 METERAI badge (gold border
  with `/5` background), INT badge, section count, tag pills (#governance, #agi, etc.)

## Hero background trick (for visual interest)

The MakcikGPT page uses a very subtle mono-char background pattern — repeated chars
from the article text at 4% opacity. Reproducible as an absolute-positioned div:

```jsx
<div className="absolute inset-0 opacity-[0.04] pointer-events-none font-mono text-[12px]
            text-forge-orange leading-tight whitespace-pre overflow-hidden">
  {`≡ ${essay.title.toUpperCase()} ≡\n\n${essay.html.replace(/<[^>]+>/g, ' ').slice(0, 800)}\n\n`.repeat(40)}
</div>
```

Set `relative` on the parent section so the absolute overlay anchors correctly.

## Body prose

Tailwind arbitrary variant selectors (used directly on the `<article>` element):

```
[&_h1]:hidden                              /* h1 in body duplicates hero — hide */
[&_h2]:font-black [&_h2]:italic [&_h2]:uppercase [&_h2]:tracking-tighter
[&_h2]:text-2xl [&_h2]:md:text-3xl [&_h2]:mt-16 [&_h2]:mb-6
[&_h2]:text-forge-white [&_h2]:border-b [&_h2]:border-forge-iron [&_h2]:pb-3
[&_h3]:font-bold [&_h3]:uppercase [&_h3]:text-sm [&_h3]:tracking-widest
[&_h3]:text-forge-orange [&_h3]:mt-10 [&_h3]:mb-3
[&_blockquote]:border-l-4 [&_blockquote]:border-forge-gold [&_blockquote]:bg-forge-steel
[&_blockquote]:py-4 [&_blockquote]:px-6 [&_blockquote]:my-8
[&_blockquote]:text-forge-dim [&_blockquote]:italic
[&_p_strong]:text-forge-white [&_p_strong]:font-bold
[&_code]:px-2 [&_code]:py-0.5 [&_code]:bg-forge-steel [&_code]:text-forge-orange
[&_code]:font-mono [&_code]:text-[0.92em]
[&_a]:text-forge-gold [&_a]:underline [&_a]:underline-offset-2 [&_a]:decoration-forge-gold/40
[&_a:hover]:decoration-forge-gold
[&_hr]:border-forge-iron [&_hr]:my-12
[&_ul]:list-disc [&_ul]:pl-6 [&_ol]:list-decimal [&_ol]:pl-6
[&_li]:my-2
```

## Author byline + CTA (below body)

```
<div className="mt-16 pt-8 border-t border-forge-iron">
  <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">
    <div>
      <div className="section-label text-forge-orange mb-2">Author · Forged</div>
      <p className="font-mono text-sm text-forge-dim leading-relaxed">
        <strong className="text-forge-white">Muhammad Arif bin Fazil</strong><br />
        Geoscientist · Architect of arifOS · Petronas Carigali · UW–Madison '13<br />
        Penang, Malaysia
      </p>
    </div>
    <div className="flex flex-col items-start sm:items-end gap-3">
      <span className="brutalist-card border border-forge-gold/50 px-5 py-3
                     inline-flex items-center gap-2 font-mono text-sm bg-forge-gold/5">
        <span className="text-forge-gold">⚒️</span>
        <span className="text-forge-dim">Published directly on</span>
        <span className="text-forge-white font-bold">arif-fazil.com</span>
      </span>
    </div>
  </div>
</div>
```

## Continue Reading (newer / older nav cards)

```
<section className="border-t border-forge-iron bg-forge-steel py-12">
  <div className="site-frame max-w-3xl">
    <div className="section-label text-forge-orange mb-4">Continue Reading · 999 Meterai</div>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <Link to="/words/writing/<slug>" className="brutalist-card border border-forge-iron
                                              hover:border-forge-gold transition-colors p-5 group">
        <div className="font-mono text-xs text-forge-dim uppercase tracking-widest mb-2">
          ↗ Newer · 7 Aug 2026
        </div>
        <h3 className="font-black italic uppercase tracking-tight text-lg text-forge-white
                       group-hover:text-forge-gold transition-colors leading-tight">
          The Next Essay Title
        </h3>
      </Link>
    </div>
    <div className="mt-6 text-center">
      <Link to="/words/writing/" className="font-mono text-sm text-forge-dim
                                              hover:text-forge-gold transition-colors">
        ← All Essays · /words/writing/
      </Link>
    </div>
  </div>
</section>
```

## Color tokens (Tailwind config)

```js
forge: {
  black: '#0a0c10',   // graphite base
  steel: '#11151c',   // surface
  iron:  '#1f2733',   // hairline
  dim:   '#8b98a8',   // warm-gray ink, secondary
  white: '#e6edf3',   // warm-gray ink, primary
  orange:'#b08d57',   // editorial bronze (world family accent — was #FF4500)
  gold:  '#c9a84c',   // muted gold (quotes / gold family)
  green: '#31c48d',   // STATUS ONLY — seal/live (was phosphor #00FF41)
  red:   '#f0506e',   // STATUS ONLY — void/hazard (was #FF003C)
},
```

## Keystones to remember

1. **NEVER ship a plain static `index.html` for an essay** when `EssayPage.tsx` exists.
   Static files shadow the SPA — users get the ugly version. Per the Aug 2026 doctrine,
   `scripts/render-words-essays.cjs` ONLY generates the index + index.json + llms.txt
   (no per-essay HTML).

2. **Forge tokens ARE the brand.** Black + steel + iron + dim + white is the foundation;
   gold + orange are accents. Don't introduce other palette colors without an F2/F4
   reason (e.g. red/green are STATUS ONLY).

3. **JSON-LD is mandatory.** Every essay page emits structured data via `useEffect`
   inserting `<script type="application/ld+json">` for `Article` with `headline`,
   `datePublished`, `author`, `publisher`, `url`, `keywords`. llms.txt crawlers
   depend on this.

4. **Reading is FORWARD motion.** Hero → body → author/CTA → Continue Reading. Don't
   add sidebars, comments, or social-share buttons — Arif's reading surfaces are
   minimalist. The "Continue Reading" cards are the only navigation.

## Reference: makcikgpt/suara-terlalu-siap structural pattern

The MakcikGPT article page adds a **Claim Register** + **Source Ledger** table at the
bottom of each article. This is BM-language journalism, not constitutional essays —
the pattern doesn't apply directly to `/words/writing/<slug>/` essays, but if you
build a new article surface that needs audit-grade evidence display, use the same
claim+source table pattern (numbered amber pills, status badges: ✅ VERIFIED /
❓ NEEDS REVIEW / ⚠️ UNVERIFIED, "Basis: ..." basis line for each claim).

## See also

- `references/essay-publish-recipe.md` — full publish workflow
- `arif-fazil-web-ops` skill — section on the gold/dark GitHub palette + zen pulse
- `src/pages/EssayPage.tsx` — current implementation (canonical)