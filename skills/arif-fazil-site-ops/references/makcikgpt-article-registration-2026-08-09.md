# MakcikGPT Article Registration Recipe (2026-08-09)

## Symptom

Browser shows **"Article Not Found"** at `/world/makcikgpt/<slug>/` even though
the article HTML exists on disk. Bot UAs (GPTBot) may or may not serve the file.

## Root Cause

The article was published to ONE surface only (typically `makcikgpt-md/` bot branch)
but never registered in the SPA article registry. The React SPA calls
`getMakcikArticle(slug)` → searches `makcikArticleModules` → not found → "Article Not Found".

## Diagnosis (30 seconds)

```bash
# 1. Is the slug in the SPA registry?
grep -c "<slug>" /root/arif-fazil.com/sites/arif-fazil.com/src/data/makcikgpt/index.ts
# 0 = not registered → this is the bug

# 2. Is the .ts source file present?
ls /root/arif-fazil.com/sites/arif-fazil.com/src/data/makcikgpt/<slug>.ts

# 3. Is it in essays.json (generator source)?
grep -c "<slug>" /root/arif-fazil.com/sites/arif-fazil.com/src/data/essays.json

# 4. Does the bot HTML exist?
ls /root/arif-fazil.com/sites/arif-fazil.com/public/makcikgpt-md/<slug>.html
```

## Fix — Step 1: Create the .ts file

Extract the article body from the deployed static HTML (or author fresh).
The `html` field must contain ONLY the body content — the SPA renders
the header (title, subtitle, domain, tags, date) from `MakcikArticleMeta`.

```python
import re

with open('/var/www/html/arif/makcikgpt-md/<slug>.html') as f:
    html = f.read()

# Extract makcik-voice body (anchor on markers, not greedy regex)
si = html.index('<div class="makcik-voice max-w-3xl">') + len('<div class="makcik-voice max-w-3xl">')
ei = html.index('</body>')
tail = html[si:ei].rstrip()
# Strip trailing two </div> (voice + site-frame)
tail = tail[:tail.rfind('</div>')].rstrip()
tail = tail[:tail.rfind('</div>')]
body = tail.strip()

# Transform static-page CSS classes for SPA
body = re.sub(r'<div class="question">\s*<p>(.*?)</p>\s*</div>',
              r'<blockquote><p>\1</p></blockquote>', body, flags=re.DOTALL)

def fix_fact(m):
    variant, angka, fakta = m.group(1), m.group(2).strip(), m.group(3).strip()
    color = '#ff5d5d' if variant == 'void' else '#4ecdc4'
    return (f'<div style="display:flex;gap:1rem;align-items:baseline;padding:0.6rem 1rem;'
            f'margin:0.4rem 0;background:rgba(255,255,255,0.03);border-radius:4px;">'
            f'<div style="min-width:80px;font-family:monospace;font-size:1.3rem;'
            f'font-weight:700;color:{color};text-align:right;">{angka}</div>'
            f'<div style="font-size:0.95rem;color:rgba(255,255,255,0.7);">{fakta}</div></div>')

body = re.sub(r'<div class="makcik-fact (void|sabar)">\s*<div class="angka">(.*?)</div>'
              r'\s*<div class="fakta">(.*?)</div>\s*</div>', fix_fact, body, flags=re.DOTALL)

body = body.replace('<div class="makcik-closing">',
                    '<div style="border-top:1px solid rgba(255,255,255,0.1);padding-top:1.5rem;margin-top:2rem;">')

# Escape for JS template literal
body_escaped = body.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
```

Write `src/data/makcikgpt/<slug>.ts`:
```typescript
import type { ArticleContent } from './types';

const content: ArticleContent = {
  slug: '<slug>',
  html: `<escaped body here>`,
};

export default content;
```

## Fix — Step 2: Register in index.ts

Three edits in `src/data/makcikgpt/index.ts`:

```typescript
// (a) Add import after existing imports
import <camelCaseName> from './<slug>';

// (b) Add to makcikArticleModules array (newest first)
export const makcikArticleModules: ArticleContent[] = [
  <camelCaseName>,
  // ... existing entries
];

// (c) Add MakcikArticleMeta to makcikArticlesMeta array
{
  slug: '<slug>',
  title: 'Article Title',
  subtitle: 'Subtitle text',
  date: 'YYYY-MM-DD',
  domain: 'MAKCIKGPT × TOPIC',
  language: 'ms',
  excerpt: 'Short excerpt for cards/SEO',
  tags: ['tag1', 'tag2', 'makcikgpt', 'malaysia'],
  seal: '999',
},
```

## Fix — Step 3: Add to essays.json

Insert at the TOP of the makcik section (newest first). Find the position
of the most recent existing makcik entry and insert before it:

```json
{
  "id": "m2-9",
  "title": "Article Title",
  "date": "2026-08-09",
  "lang": "bm",
  "series": { "id": "M2", "n": 9 },
  "tags": ["petronas", "amanah", "makcikgpt", "malaysia"],
  "dest": {
    "type": "onsite",
    "path": "/world/makcikgpt/<slug>"
  },
  "seal": "999"
},
```

## Fix — Step 4: Generate bot HTML + rebuild + deploy

```bash
cd /root/arif-fazil.com/sites/arif-fazil.com

# Generate bot-serving HTML
node scripts/generate-makcik-articles.cjs

# Verify it was created
ls public/makcikgpt-md/<slug>.html

# Build (mirrors public/ → dist/)
npm run build

# Verify in dist/
ls dist/makcikgpt-md/<slug>.html

# Deploy
cd /root/arif-fazil.com
bash scripts/deploy-site.sh arif-fazil.com --apply
```

## Verification (three surfaces)

```bash
# 1. SPA browser — full render, not "Article Not Found"
# browser_navigate → snapshot → check title + sections present

# 2. Bot branch — GPTBot gets static HTML
curl -sI -H "User-Agent: GPTBot" "https://arif-fazil.com/world/makcikgpt/<slug>" | head -3
# Expected: HTTP/2 200, content-type: text/html

# 3. Landing page — article in card grid
curl -s "https://arif-fazil.com/world/makcikgpt/" | grep -c "<slug>"
# Expected: >= 1
```

## Key Files

| File | Role |
|---|---|
| `src/data/makcikgpt/<slug>.ts` | SPA article body (ArticleContent) |
| `src/data/makcikgpt/index.ts` | SPA registry (modules + meta) |
| `src/data/essays.json` | Generator source (feed, sitemap, bot HTML) |
| `scripts/generate-makcik-articles.cjs` | Generates `public/makcikgpt-md/<slug>.html` |
| `scripts/lib/makcik-source.cjs` | Reads essays.json, filters `lang: "bm"` + `dest.path` prefix |
| `public/makcikgpt-md/<slug>.html` | Bot-serving static HTML |
