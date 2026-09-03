# /propa — Decision Memo

**Status:** Recommendation
**Priority:** P1
**Session:** SEAL-d7d3fde881a74721
**Author:** 333-AGI Δ Mind

---

## The Finding

`/propa` currently renders **byte-identical content** to `/vitals`. Verified 2026-08-26 via Firecrawl scrape — both URLs returned the same PETRONAS institutional intelligence page.

This is a **misconfiguration**. Either `/propa` is a redundant mirror (bad for SEO) or it's supposed to be a different surface (currently broken).

---

## Two Options

### Option A: Canonical redirect (RECOMMENDED if /propa is unused)

Add to `/etc/caddy/Caddyfile` (or equivalent routing layer):

```
redir 301 /propa /vitals
```

OR add to the HTML head of the current `/propa` page:
```html
<link rel="canonical" href="https://arif-fazil.com/vitals/" />
```

**Pros:**
- Single source of truth
- SEO consolidation (no duplicate content penalty)
- Zero maintenance

**Cons:**
- Lose whatever `/propa` was meant to be

---

### Option B: Rebuild /propa as a different surface

If `/propa` is meant to be a "Property / Procurement" surface (PETRONAS Activity Outlook 2026-2028 already lives at `/partner-us/malaysia-oil-gas-outlook`), then:

1. Replace content with the PETRONAS Activity Outlook PDF
2. Add civic commentary on PETRONAS capex pipeline
3. Link to /vitals for institutional health context

**Proposed content for /propa:**

```markdown
# PETRONAS · PROPA — Capex, Procurement & Partnership Pipeline

**FY2026 DECLARED STATE · BOARD-APPROVED · NOT YET AUDITED**
Capex guidance: RM45-50 billion annually over five years, up from RM41.6B in FY2025.
International upstream: planned 60% expansion over ten years.

**The procurement question for ordinary Malaysians:**
- Where does this capex go?
- Who benefits? (OGSE vendors, Petronas Carigali, JV partners?)
- What is the audit trail?
- Is the procurement process still under the old "fight like bulldogs" DNA, or has it shifted to deal-making?

[Source: PETRONAS Activity Outlook 2026-2028 PDF, FY2025 IFR]

**Cross-link:** [PETRONAS · VITALS — institutional health context](https://arif-fazil.com/vitals/)
```

**Pros:**
- Distinct surface for distinct concern
- Aligns with existing menu (PETRONAS / MALAYSIA / OIL / GAS / GOLD)
- Adds Malaysian-language commentary layer to corporate procurement

**Cons:**
- Requires content authoring
- Maintenance overhead

---

### Option C: Delete /propa entirely

If the surface is genuinely unused, delete the route entirely from `surfaces.json`.

---

## Recommendation

**Option A — Canonical redirect.** This is the lowest-risk, highest-clarity action. The PETRONAS intelligence surface is `/vitals`. `/propa` should not exist as a duplicate.

If, in the future, you want a distinct procurement commentary surface, build it intentionally — don't repurpose a broken mirror.

---

## Execution Steps (Option A)

1. Edit `/etc/caddy/Caddyfile`:
   ```
   redir 301 /propa /vitals
   ```
2. Validate: `caddy validate`
3. Reload: `systemctl reload caddy`
4. Verify: `curl -I https://arif-fazil.com/propa` → should return `301 Location: /vitals`

Alternative (no Caddy change):
1. Add `<link rel="canonical" href="https://arif-fazil.com/vitals/" />` to `<head>` of current `/propa` HTML
2. This signals to search engines that /vitals is the canonical version
3. Less aggressive than 301 but no infra change required

---

**Receipt:** Memo drafted 2026-08-26, Session SEAL-d7d3fde881a74721, 333-AGI Δ Mind.
