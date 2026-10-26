# Stage 5 — full text (moved verbatim 2026-10-23, surgical compression)

## Stage 5: VERIFY — Build

### Before build: check deps

```bash
cd /root/arif-fazil.com/sites/arif-fazil.com
npm install --legacy-peer-deps    # REQUIRED if dist/ doesn't exist or deps stale
```

Without `--legacy-peer-deps`, `npm ci` fails with ERESOLVE peer dependency conflict
(vite-plugin-ssg vs @vitejs/plugin-react version mismatch).

### Build

```bash
npm run build
```

If build fails, check:
- TypeScript syntax in the new .ts file
- Import statement in index.ts
- Metadata shape matches `MakcikArticleMeta` interface

### Post-build: generate static HTML/MD files for bot/crawler

TS article files alone only serve the React SPA. Bots (GPTBot, ClaudeBot, curl)
read from `public/makcikgpt-md/`. NEW article slugs need static HTML generated.
Use the extraction script pattern (see `references/build-fallback-html-extraction.md`).

---

