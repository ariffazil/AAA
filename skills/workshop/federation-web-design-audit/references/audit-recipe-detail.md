# federation-web-design-audit · references/audit-recipe-detail.md

> Concrete commands and patterns for the audit procedure. Read this when running an audit; the SKILL.md tells you what to do, this file tells you exactly how.

## Step 1 — Pick the comparison set

Default triplet to start with:

| Slot | URL pattern | What it represents |
|---|---|---|
| Hub root | `https://<site>/<hub>/` | Index page of the hub being audited |
| Hub itself (full SPA) | `https://<site>/` | The site's own home — establishes the design source-of-truth |
| One child page | `https://<site>/<hub>/<child>/` | The page the sovereign named, or the first sibling if generic |

Expand to siblings only if the root-vs-child comparison reveals a divergence. **One observation is not a class** — quote "1 of 1" not "system has no design system".

## Step 2 — Fetch

Single endpoint per page. No retry, no parallel fan-out — keep the budget predictable:

```bash
curl -s -m 15 "https://arif-fazil.com/words/doctrine/" -o /tmp/doctrine.html
curl -s -m 15 "https://arif-fazil.com/words/" -o /tmp/words.html
curl -s -m 15 "https://arif-fazil.com/" -o /tmp/home.html
```

If a page returns 0 bytes with a 2xx, it's a soft-404 — record that as the finding, do not retry.

## Step 3 — Five bytes per page

All five metrics can be extracted with `python3` inline. Save the script and re-run across siblings:

```python
import re
text = open("/tmp/doctrine.html").read()

# 1. byte size
print(len(text))

# 2. stylesheets
print(re.findall(r'href="([^"]+\.css)"', text))

# 3. inline <style> total chars
blocks = re.findall(r'<style[^>]*>(.*?)</style>', text, re.S)
print(sum(len(b) for b in blocks))

# 4. :root variables defined in page
print(re.findall(r'--[\w-]+', '\n'.join(re.findall(r':root\s*\{([^}]+)\}', text))))

# 5. nav links
navs = re.findall(r'<nav[^>]*>(.*?)</nav>', text, re.S)
for n in navs:
    print(re.findall(r'<a[^>]+href="([^"]+)"[^>]*>([^<]+)</a>', n))
```

Threshold rules:
- Inline `<style>` > 2000b → smell, log it
- Inline `<style>` > 5000b → almost always means "prototype was never extracted"
- Page that defines 5+ custom CSS variables the shared `tokens.css` doesn't define → finding

## Step 4 — Probe shared design-system files

```bash
for f in tokens.css hub-words.css hub-earth.css hub-world.css hub-work.css components.css typography.css; do
  curl -s -m 8 -o /dev/null -w "%{http_code} %{size_download}b  $f\n" \
    "https://<site>/_shared/design-system/$f"
done
```

Then count `:root` blocks and their variables:

```bash
curl -s -m 10 "https://<site>/_shared/design-system/tokens.css" -o /tmp/tokens.css
grep -oE '\-\-[\w-]+' /tmp/tokens.css | sort -u | wc -l    # count unique vars
```

A live tokens.css with 154+ vars and a sibling page defining 8 brand-new variables in inline `<style>` is the smoking gun for "design system ignored". Even if the visual output looks fine, the **namespace collision** is a structural finding.

## Step 5 — Probe sibling narrative pages

Use `find` or known sitemap. For arif-fazil.com:

```bash
for p in doctrine constitution atlas writing; do
  curl -s -m 10 -o /dev/null \
    -w "$p: %{http_code} %{size_download}b\n" \
    "https://arif-fazil.com/words/$p/"
done
```

Then probe the same 5 bytes on each. **Use the distribution** ("X of Y narrative pages diverge by > 5KB inline") rather than the absolute count. The pattern explanation should be "first narrative page used inline `<style>` as a prototype; the prototype never got extracted".

## Step 6 + 7 + 8 + 9 — produce, rank, write, scope

These steps are judgment calls. The SKILL.md covers them. The skeleton:

```markdown
# TL;DR

Three concrete divergences found; one systemic (X), two page-local (Y, Z).

# Divergences (with evidence class)

## D1 — <divergence name>  [evidence class: live_probe|configuration|structural|inferred]

| Page | Property | Value | Class |
|---|---|---|---|
| ... | ... | ... | ... |

Fix proposal ranked by impact × reversibility:
- F1 — Extract inline to shared stylesheet (15 min, reversible)
- F2 — Rename custom tokens to consume design-system vocabulary (30 min, reversible)
- F3 — Unify navigation via shared component (45 min, reversible)
- F4 — Full design-system unification (deferred, multi-day)

# Why it exists

Pattern: <what type of inconsistency>. Not a narrative of who decided what.

# Receipts

| Probe | Method | Bytes | Note |
|---|---|---|---|
| <URL> | curl -s -m 15 | <size> | as run in this session at <timestamp> |

# What this audit does NOT cover

- Visual rendering (text scrapes only — visual claims are `inferred`)
- Browser engine CSS rule interactions
- Accessibility audit beyond structural class checks
- Performance / CLS measurements
```

## Worked walkthrough — minimal example

A real audit on a 3-page site:

```python
import re, urllib.request, time
from pathlib import Path

OUT = Path("/root/forge_work/site-audit")
OUT.mkdir(parents=True, exist_ok=True)

pages = [
    ("home", "https://example.com/"),
    ("hub", "https://example.com/words/"),
    ("doctrine", "https://example.com/words/doctrine/"),
]

def fetch(url):
    return urllib.request.urlopen(url, timeout=15).read().decode("utf-8", errors="replace")

results = {}
for name, url in pages:
    t0 = time.time()
    body = fetch(url)
    t1 = time.time()
    inline = sum(len(b) for b in re.findall(r"<style[^>]*>(.*?)</style>", body, re.S))
    sheets = re.findall(r'href="([^"]+\.css)"', body)
    var_decls = sum(len(re.findall(r"--[\w-]+", p)) for p in re.findall(r":root\s*\{([^}]+)\}", body))
    results[name] = {
        "url": url,
        "bytes": len(body),
        "fetch_ms": int((t1 - t0) * 1000),
        "stylesheets": sheets,
        "inline_style_bytes": inline,
        "custom_vars": var_decls,
    }

(OUT / "doctrine-audit-2026-09-24.md").write_text(
    render_results(results),  # render_results defined inline
)
```

This compresses to ~80 lines. Run, write, present the rendered table, and stop.

## What to skip

- Browsing the site with Playwright to "see" the page — `inferred` at best. If the sovereign wants a screenshot, ask them to send one and bind evidence class to `live_probe` with the screenshot timestamp.
- Running lighthouse / a11y audits. Those are real and useful but a different skill.
- Editing CSS files. The deliverable is the audit markdown, not a fix.
- Quoting browser-console errors, network waterfall timings, or interaction timing. The audit is structural, not performance.
