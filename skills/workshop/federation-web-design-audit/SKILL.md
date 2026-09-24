---
name: federation-web-design-audit
description: "Audit sibling pages. Produces ranked fixes."
version: 0.1.0-2026-09-24
trigger_phrases:
  - "pages not aligned"
  - "design system drift"
dependencies:
  skills: []
floor_scope: [F2, F4, F6, F13]
risk_tier: low
autonomy_tier: T1
---

# federation-web-design-audit

> When a federation web surface loses internal consistency, the sovereign notices before any tool does. This skill audits, classifies, and proposes — without editing.

## When to use

Use when the sovereign reports visual / IA / architectural drift on a federation web surface, or asks for a sibling-page design-system comparison. Typical trigger quotes from arif-fazil.com or similar:

- "page system design navigation and architecture are not alligened with the rest"
- "pages look inconsistent — please align"
- "compare hub and child page styling"
- "design system drift — which pages are out"

## What this skill is NOT

- It is **not** a build skill. To create new UI use `forge-design-intelligence`.
- It is **not** a single-URL extractor. To scrape one URL → `DESIGN.md` use `firecrawl-website-design-clone`.
- It is **not** an editor. The deliverable is a written audit + ranked fix proposals; the sovereign decides what to apply.

## Procedure (works for any live site)

1. **Pick the comparison set.** If the sovereign names pages (e.g. "hub vs doctrine page"), use exactly those. Otherwise pick: hub root, hub index page, one sibling-page if any. Expand to siblings only after divergence between just the hub and one child is confirmed — most divergence is local, not systemic.

2. **Fetch each page once** with `curl -s -m 15 <url>`, saving each to `/tmp/<name>.html`. Do not retry; a single full body is enough for the audit. Total budget: ≤ 5 fetches per session.

3. **For each fetched page, compute five evidence bytes:**

   | Byte | How | What it tells you |
   |---|---|---|
   | `byte size` | `len(c)` | Page-level divergence — outlier pages are bigger because of inline `<style>` blocks or hand-authored copy |
   | `<link rel='stylesheet'>` paths | `re.findall(r'href="([^"]+\.css)"', c)` | Which design-system files each page consumes; check shared-ness |
   | `<style>` blocks total chars | `re.findall(r'<style[^>]*>(.*?)</style>', c, re.S)` then sum | Inline overrides — anything > 2000b is a smell |
   | `:root { ... }` blocks | `re.findall(r':root\s*\{([^}]+)\}', c)` | Custom CSS variables each page defines; compare with `tokens.css` to find re-definitions |
   | `<a href>` (in `<nav>` blocks) | regex over `<nav>` content | Nav IA divergence — count, order, missing items between sibling pages |

4. **Probe design-system shared files separately.** Hit `/_shared/design-system/{tokens.css, hub-*.css, components.css}` — confirm they exist, return 200, count their `:root` blocks. Compare the variables exposed there against the page-defined ones in step 3. **A custom variable that doesn't appear in the shared tokens.css is a finding**, not a feature.

5. **Probe sibling narrative pages** (pages that hand-author extra inline `<style>` on top of the hub). This catches the "one page is the prototype" smell — if `doctrine/` has 7.5KB inline style, `constitution/` and `atlas/` probably do too. Don't quote body counts from one page; quote the **distribution** across siblings.

6. **Classify each finding by evidence class** — `live_probe` / `configuration` / `structural` / `inferred`. Anything written about visual consistency from a text-only HTML scrape is at best `structural`; visual claim without a screenshot is `inferred`. State the class beside the finding, not just the claim.

7. **Produce ranked fix proposals.** For each finding, propose a fix with:

   - **Effort** in minutes (rough but bounded; don't over-promise)
   - **Reversible** yes/no
   - **Impact** what changes
   - **Risk** which page surface it touches

   Rank by impact × reversibility. **Do not pre-commit to "do all of them"** — that's the sovereign's call. Apply only when explicitly directed. Default output of this skill is *audit + ranked options*, not *audit + applied patches*.

8. **Write the audit file** to `/root/forge_work/site-audit/<topic>-audit-<date>.md`. Required sections:

   - **TL;DR** — three-sentence executive summary
   - **Three concrete divergences** with byte-budget evidence table
   - **Why the divergence exists** — pattern classification, not a narrative ("first narrative page used inline `<style>` as a prototype; the prototype never got extracted to a shared file" is a pattern explanation; "the developer ran out of time" is a narrative)
   - **4 fix proposals** ranked by impact × reversibility
   - **Receipts** — what bytes each page has, how many tokens, how many siblings probed

   Cite every figure to its probe. No unattributed numbers.

9. **Honest scope declaration:** every audit ends with what the probe did NOT cover. Text scrapes don't see visual rendering; CSS rule interactions in a browser engine are out-of-band. A finding is `inferred` (visual) if no screenshot was taken. **Tell the sovereign what evidence class each finding carries.**

## Pitfalls

**P1 — propose menus when the directive is "fix it".** A sovereign saying "Buat ja semua" or "Fix it" is not asking for a 4-option menu with reversibility rankings — it's asking to apply the fix. The audit + ranked options output is the **default**, but the moment the directive is explicit, switch to execute-on-say. Pre-commit when the cost is bounded and reversible; save the menu for ambiguous cases where the sovereign wants to choose.

**P2 — fabricate visual claims from text-only probes.** A text scrape can read class names, inline `<style>` blocks, and `:root` variables, but it cannot see whether the page renders correctly. A finding of the form "the doctrine page has a different colour palette than the hub" is `inferred` (visual) — quote the bytes, not your assumption about rendered appearance. State the evidence class. Do not write "the page LOOKS broken" from text alone.

**P3 — claim a probe was run when it wasn't.** Every quoted figure in the audit must trace to a `curl` / `cat` / `python3` invocation actually run in this session. If you read a number from a tool output earlier and quoted it later, that's fine — but if you wrote "the page has 154 tokens" without running the grep that produced 154 in this session, retract and rerun. Use `live_probe` only when you have a timestamp proving the read.

**P4 — one-page findings become systemic diagnoses without siblings.** A single page with 7.5KB inline style is a "divergent page", not "system has no design system". Probe at least one sibling narrative page before claiming the pattern is systemic — and use the distribution (how many / total) as evidence, not the absolute count. "3 of 3 narrative pages diverge" is a finding; "doctrine/ diverges" is a single observation.

**P5 — same evidence class for visual and structural claims.** Page byte sizes are `live_probe` (you fetched them this session). `:root` block contents are `live_probe` (you grep'd them). A claim that "the hub and doctrine page visually clash" is `inferred` unless you have a screenshot. Mix classes explicitly — drop the structural claims into "structural" rows, the visual claims into "inferred" rows, and never promote an inferred row to the headline.

**P6 — propose fixes that touch every page.** Hotfix the smallest unit first. The pattern that nearly always wins is "extract one inline block to one shared file" — that fixes every page that uses that block, doesn't touch pages that don't, and is reversible. Multi-page restructures are F13 territory, not hotfixes.

**P7 — overwrite the source file by accident.** The audit file is `/root/forge_work/site-audit/<topic>-audit-<date>.md`. Do not write to `/root/.hermes/skills/...`, the design-system source files, or any production page file. Stops mistakes that become irreversible on a live public site.

**P8 — answer "what is this for" before answering "what's wrong".** When the sovereign asks about the page system as a whole, the response should start with **what the page is** (it's a /words/* hub system serving essay-style content), not **what's wrong** (inline style drift, missing nav items, etc.). The why-it-exists context precedes the divergence diagnosis. Otherwise the sovereign reads the audit as "everything is broken" instead of "one subsystem needs alignment".

## Refusal surface

- ❌ Do not edit `tokens.css`, `hub-*.css`, or any production page without explicit F13-class authority
- ❌ Do not commit changes; the audit produces a markdown file, not a git diff
- ❌ Do not run browser automation / Playwright to "really see" the page; text-only probes are the class boundary and visual screenshots are `inferred` at best
- ❌ Do not produce a fix recipe that requires a full design-system rebuild as the first option; lead with the smallest reversible change
- ❌ Do not spend sovereign attention on per-incident audit files; the file is the deliverable, not a back-and-forth

## Depth

`references/audit-recipe-detail.md` — concrete commands, regex patterns, byte-level evidence thresholds, and worked audit walkthroughs.

---

*Forged: 2026-09-24 by hermes-edge-bridge after the arif-fazil.com /words/doctrine/ audit.*
*DITEMPA BUKAN DIBERI ⚒️*
