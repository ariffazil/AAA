# Hand-written MakcikGPT article design drift fix (verified 2026-08-11)

## Symptom

Arif reports "design lari" on a MakcikGPT article. Browser shows current live render; he shares a screenshot showing richer design than what's live. The drift is design-token-level, not accessibility-level.

## Diagnosis recipe

```bash
SLUG="<suspect-slug>"
# 1. Confirm static file exists
ls -la /var/www/html/arif/makcikgpt-md/$SLUG.html
# 2. Check for TS source — MISSING = hand-written static only
ls /root/arif-fazil.com/sites/arif-fazil.com/src/data/makcikgpt/$SLUG.ts 2>/dev/null
# 3. Compare kicker text — live vs target
grep -oE 'CIVILIZATION INTELLIGENCE|MAKCIKGPT \W PETRONAS' /var/www/html/arif/makcikgpt-md/$SLUG.html
# 4. Compare with a sibling that has full SPA treatment (e.g., one with .ts source)
```

## Root cause

Article was hand-written directly to static HTML, bypassing the SPA build pipeline. After the Caddy static-first fix (2026-08-09), static HTML is the primary view for ALL users (not just bots). The simpler "writing-article pattern" design is now exposed as the canonical MakcikGPT surface — and it diverges from the SPA component's richer design.

## Two fix paths — choose based on context

### Path A — Upgrade static HTML in place (faster, static-only)

1. Identify the target design from a sibling article with full SPA treatment (read both static HTML and SPA-rendered HTML; diff kicker / section-label / color tokens).
2. Patch the static HTML directly: update kicker to use `CIVILIZATION INTELLIGENCE · Ξ WEALTH · {domain}` prefix; align byline pills / tag pills to match SPA styling.
3. `chown www-data:www-data /var/www/html/arif/makcikgpt-md/<slug>.html && chmod 644`.
4. Verify with `browser_navigate` (W4 of Dual-Witness Verification).

### Path B — Add TS source for full SPA parity (more complete)

1. Author `src/data/makcikgpt/<slug>.ts` from the static HTML body content.
2. Register in `src/data/makcikgpt/index.ts` (makcikArticleModules + makcikArticlesMeta).
3. Add entry to `src/data/essays.json` (so static index regenerates).
4. Rebuild via `npm run build`.
5. Verify W1–W4 of Dual-Witness Verification recipe.

### When to choose which

**Path A** when:
- TS source isn't wanted (article is civic-journalism one-off)
- Apex judge verdict must precede any change (the static HTML holds the article in place while waiting)
- Time is constrained

**Path B** when:
- Full SPA/browser parity is needed (article should render identically in SPA fallback)
- Future rebuilds should pick up the article (TS source is the build pipeline's SOT)
- Static HTML may eventually drift if hand-edited

## Common pitfall

Confusing Path A with "the article is broken." The article is NOT broken — it renders correctly via Caddy static-first. The drift is design-token-level, not accessibility-level. Don't replace the static HTML with a blank or broken rebuild — upgrade it.

## Session case study (2026-08-11, syaitan-ingat-dirinya-malaikat)

Article had no `.ts` source; static HTML used simpler kicker `MAKCIKGPT × PETRONAS × AMANAH · SEALED 999` vs target `CIVILIZATION INTELLIGENCE · Ξ WEALTH · MAKCIKGPT × PETRONAS × AMANAH`. Apex judge review delegated to independent actor (see `apex-judge` skill § "When CLI/MCP unavailable"). Factual claims verified: revenue -17% (RM320B→RM266B) and dividend 70.5% match source; CAPEX rounded (RM40B article vs RM41.6B source, ~4% rounding error). Recommended Path A pending apex verdict.
