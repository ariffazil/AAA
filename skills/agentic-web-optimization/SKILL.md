# SKILL: Agentic Web Optimization

> **Purpose:** Make web content maximally extractable by LLMs, Agentic RAG systems, and search indexers.
> **Target metric:** τ≥0.99 (high signal-to-noise ratio, ΔS≤0)
> **Domain:** arif-sites / arif-fazil.com / any web property
> **Sealed:** 2026-07-01 · 999 Meterai

---

## When To Load

- Building or deploying any web property that needs LLM/AI discoverability
- Optimizing existing pages for agentic extraction
- Auditing a site's machine-readability
- Publishing civic intelligence articles (MakcikGPT, WEALTH briefings)

---

## The 6-Layer Architecture

### Layer 1: robots.txt — AI Crawler Whitelisting

**Goal:** Explicitly allow AI crawlers. Block only known abusers.

```
User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Anthropic-AI
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Bytespider
Allow: /

User-agent: Applebot
Allow: /

User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

# Block known abusers
User-agent: CCBot
Disallow: /

User-agent: omgili
Disallow: /

Sitemap: https://<domain>/sitemap.xml
```

**Why allow Bytespider?** High-volume but feeds Perplexity and other RAG systems. Block only if bandwidth abuse detected.

---

### Layer 2: llms.txt + llms.json — Agent Discovery

**llms.txt** (root): Human-readable markdown with:
- Site ontology (who, what, why)
- Direct links to core content with 2-sentence semantic summaries
- MCP endpoint declaration
- Machine-readable discovery surfaces

**llms.json** (root): Structured JSON with:
- `route_roles`: every route with semantic description
- `machine_surfaces`: all agent-discovery URLs
- `semantic_architecture`: what techniques are deployed (pre_rendered, json_ld, etc.)
- `last_updated`: ISO 8601

**When adding new content:** Always update both llms.txt AND llms.json with the new route + summary.

---

### Layer 3: SSR / Pre-Rendering — Content Without JavaScript

**Problem:** React/Vue SPAs render content client-side. LLM scrapers that don't execute JS see empty shells.

**Solution:** Pre-render article pages as static HTML via Puppeteer after build.

**Script:** `scripts/prerender-articles.cjs`

```javascript
const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

// For each article:
// 1. Navigate to live URL
// 2. Wait for React render
// 3. Extract rendered HTML
// 4. Wrap in semantic HTML5 with JSON-LD + meta tags
// 5. Save as {slug}/index.html in dist/
```

**Key design decisions:**
- Use `<article itemscope>` wrapper for Schema.org microdata
- Include `<h1>`, `<h2>`, `<p>`, `<blockquote>` — semantic HTML5
- Strip JS bundles, tracking pixels, unnecessary divs
- Keep CSS for visual readability when humans open the static file

**Deploy integration:** Add pre-render step AFTER `npm run build` in deploy script:
```bash
npm run build
node scripts/prerender-articles.cjs
```

---

### Layer 4: JSON-LD Structured Data

**Schema:** `NewsArticle` or `BlogPosting`

```json
{
  "@context": "https://schema.org",
  "@type": "NewsArticle",
  "headline": "...",
  "description": "...",
  "author": { "@type": "Person", "name": "...", "url": "..." },
  "publisher": {
    "@type": "Organization",
    "name": "...",
    "url": "...",
    "logo": { "@type": "ImageObject", "url": "..." }
  },
  "datePublished": "2026-07-01",
  "dateModified": "2026-07-01",
  "mainEntityOfPage": "https://...",
  "image": "https://...",
  "keywords": "...",
  "inLanguage": "ms",
  "isAccessibleForFree": true,
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": [".cover-subtitle", ".pull-quote", ".callout"]
  }
}
```

**`speakable`** tells voice-search AI which paragraphs to read aloud.

---

### Layer 5: Metadata & Open Graph

Per article page:
```html
<title>{title} | {site_name}</title>
<meta name="description" content="{2-sentence summary}">
<meta name="author" content="{author}">
<meta name="keywords" content="{comma-separated}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{exact_url}">

<meta property="og:title" content="{title}">
<meta property="og:description" content="{summary}">
<meta property="og:type" content="article">
<meta property="og:url" content="{exact_url}">
<meta property="og:image" content="{image_url}">
<meta property="og:site_name" content="{site_name}">
<meta property="og:locale" content="{locale}">
<meta property="article:published_time" content="{date}">
<meta property="article:author" content="{author}">
<meta property="article:section" content="{section}">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{summary}">
<meta name="twitter:image" content="{image_url}">
```

---

### Layer 6: Canonical + Sitemap

**Canonical:** Every page must have `<link rel="canonical">` pointing to the exact live URL. Prevents duplicate content indexing.

**Sitemap:** Update `sitemap.xml` with:
- All new URLs
- `<lastmod>` in ISO 8601
- `<changefreq>` (weekly for dynamic, monthly for static)
- `<priority>` (0.9 for flagship content, 0.8 for standard, 0.5 for utility)

**Submit:** Google Search Console + Bing Webmaster Tools via API if configured.

---

## Caddy Configuration

For SSG pre-rendered routes, add BEFORE the SPA fallback:

```caddyfile
# SSG pre-rendered pages — serve static HTML instead of SPA shell
@makcikgpt path /wealth/makcikgpt/*
handle @makcikgpt {
    try_files {path}/index.html /index.html
    file_server
}
# SPA fallback (must come AFTER SSG handlers)
handle /wealth/* {
    try_files /static/wealth.html /index.html
    file_server
}
```

**Rule:** More specific routes MUST come before catch-all routes in Caddy.

---

## Verification Checklist

After deployment, verify each layer:

```bash
# 1. robots.txt
curl -sf https://domain/robots.txt | grep "GPTBot"

# 2. llms.txt
curl -sf https://domain/llms.txt | head -5

# 3. SSR (article content in raw HTML, no JS needed)
curl -sf https://domain/wealth/makcikgpt/petronas-dna | grep "<article"

# 4. JSON-LD
curl -sf https://domain/wealth/makcikgpt/petronas-dna | grep "application/ld+json"

# 5. OG meta
curl -sf https://domain/wealth/makcikgpt/petronas-dna | grep "og:title"

# 6. Canonical
curl -sf https://domain/wealth/makcikgpt/petronas-dna | grep "canonical"

# 7. Sitemap
curl -sf https://domain/sitemap.xml | grep "makcikgpt"
```

---

## Anti-Patterns

- ❌ Relying on client-side JS to render primary content (LLMs won't see it)
- ❌ Blocking AI crawlers in robots.txt (you WANT LLMs to find your truth)
- ❌ Missing canonical URLs (duplicate content penalty)
- ❌ No JSON-LD (search engines can't classify your content)
- ❌ Generic OG meta (social agents can't differentiate articles)
- ❌ No sitemap updates (new content stays invisible to indexers)
- ❌ Deploy script that rebuilds dist AFTER pre-rendering (wipes SSR files)

---

## The Agentic Web Thesis

> The web is no longer just "pages for human eyes." It is a data substrate for machine intelligence.
> 
> Every page you publish is either:
> - **Signal** (structured, semantic, machine-readable) — τ≥0.99
> - **Noise** (JS-rendered, unstructured, opaque) — τ≤0.5
> 
> arifOS publishes signal. The machines read the truth before the humans see the design.
> 
> DITEMPA BUKAN DIBERI.

---

*Forged: 2026-07-01 · Meta-Mesa Agentic Web Agent*
*Source: arif-sites deploy + MakcikGPT SSR pipeline*
*999 SEAL ALIVE*
