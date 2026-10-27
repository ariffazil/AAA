---
name: arif-fazil-landing-page
description: "Use before building or restyling any landing/entry page for arif-fazil.com. A rulebook: intake → fixed section order → copy rules → one token file → ship checklist run at 3 widths. Not a deploy skill (see arif-sites-ops) and not a W3 witness (see forge-visual-qa-w3)."
version: "1.0.0-2026-10-28"
owner: FI-002
risk_tier: low
floor_scope: ['F1', 'F4', 'F9']
source: "https://x.com/alex_prompter/status/2115112687650709511 — 'two halves and a checklist', applied to this site"
---

# arif-fazil.com landing page rulebook

Write the rulebook once; every page follows it. Two halves and a checklist.

## When NOT to use
- Deploying / Caddy / rsync → `arif-sites-ops`
- Screenshot tri-witness sealing → `forge-visual-qa-w3`
- Federation-wide palette (decks, PDFs) → `forge-visual-design-system`

## Part A — Strategy

### A1. Intake (ask all six in one batch, never drip-feed)
1. The one action a visitor takes (one button, one destination).
2. The offer, in one sentence a stranger understands.
3. Who the buyer is.
4. Their top three objections, in the buyer's own words.
5. Traffic source — what page/post/ad they clicked just before.
6. Proof you can back with a number, a name, or a document.

Can't answer one → assume, state the assumption in one line, continue.

### A2. Section order (fixed; same twelve, same order, every page)
1. Hero — headline naming outcome + audience, one subheadline, one button
2. The problem, in the buyer's words
3. The offer, plainly
4. How it works — 3 steps, numbered
5. Proof — the number/name/document from A1.6
6. What you get — concrete deliverables, not benefit adjectives
7. Objection 1 answered
8. Objection 2 answered
9. Objection 3 answered
10. Who this is for / not for
11. FAQ — plain questions, plain answers
12. Final button — same label, same destination as #1

Live homepage today is 4 sections (hero · idea · wells · proof). That is the gap, not the target.

### A3. Copy rules
- One offer, one audience, one button label (repeated verbatim at #1 and #12).
- Every claim carries a number, a unit, and a source. "Save time" is banned; "cut weekly reporting 4h → 15min" passes.
- Epistemic labels are part of the copy, not decoration: OBS / DER / INT / SPEC on any factual claim about the world.
- No adjective without a measurement behind it. No "seamless", "robust", "world-class", "streamline".
- Cut 50% of sentences. If meaning survives, it was decoration.

## Part B — Visual system

**Single source of truth: `/root/arif-fazil.com/sites/shared/tokens.css`** (v1.0, sealed 2026-07-24, F13: ARIF). Never fork values into a skill, a component, or a Tailwind literal.

| Decision | Canonical value |
|---|---|
| Display font | `'DM Serif Display'` via `--font-display` |
| UI font | `'IBM Plex Sans'` via `--font-sans` |
| Mono | `'IBM Plex Mono'` via `--font-mono` |
| Ground | `--bg` `#0a0c10` |
| Primary ink | `--ink` `#e6edf3` |
| Secondary ink | `--dim` `#8b98a8` |
| Hairline | `--line` `#1f2733` |
| Accent | `--accent` (family-scoped) |
| Spacing scale | `--sp-1..5` = 6 / 12 / 18 / 26 / 40 px |
| Radii | `--r-sm 8` · `--r 12` · `--r-lg 16` · `--r-pill 999` |
| Max width | `--maxw` 1120px |
| Motion | `--ease .18s cubic-bezier(.4,0,.2,1)` — one curve, every transition |

Rules:
- **No raw hex in a page or component.** Use `var(--token)` or the Tailwind `forge.*` names. Tailwind `paper/ink/ember/gold` are a *second* palette and are the current drift source — do not add to it, migrate off it.
- Red/green are status only (seal / void). They never carry identity or decoration.
- One accent per family scope; accents are muted (no-neon doctrine).

## Part C — Ship checklist

Run at **390 / 768 / 1440 px**, screenshot each, fix top 3, repeat up to 3 rounds.

**Strategy**
- [ ] One button label, repeated at top and bottom, same destination
- [ ] Headline names outcome *and* audience
- [ ] All three objections answered in the buyer's own words
- [ ] Every factual claim carries a number + unit + source, labelled OBS/DER/INT/SPEC
- [ ] FAQ written as real questions people ask

**Visual**
- [ ] Zero raw hex outside `tokens.css` (`grep -nE '#[0-9A-Fa-f]{6}' <file>` is empty)
- [ ] One display font, one UI font, one mono — no third stack in the fonts.googleapis `<link>`
- [ ] Accent used once per viewport; red/green appear only as status
- [ ] Spacing values come from `--sp-*`; no 7px / 13px / 23px one-offs
- [ ] Every transition uses `--ease`

**Shipping**
- [ ] `<title>`, meta description, canonical, OG + Twitter image
- [ ] Favicon; every image has alt text
- [ ] Custom 404 exists and is branded
- [ ] Form (if any) rejects empty + malformed email
- [ ] Privacy + Terms linked in footer
- [ ] Evergreen → indexed with title/description/FAQ; campaign → `noindex`
- [ ] Phone check: no button wraps to two lines, no orphan word on the last headline line

## Measured drift — live probe 2026-10-28
Served CSS `index-Cuat_Uam.css`, 184,636 B, from `https://arif-fazil.com/`:

| Token | Canon | Live occurrences |
|---|---|---|
| `#0A0B0D` (paper) | not canon (`--bg` = `#0a0c10`) | 18 |
| `#EDEAE2` (ink) | not canon (`--ink` = `#e6edf3`) | 35 |
| `#9AA0A8` (ink-soft) | not canon (`--dim` = `#8b98a8`) | 38 |
| `#E4572E` (ember) | not canon | 54 |
| `#4aa8ff` (`--accent`) | canon | **0** |

Two dark palettes ship at once; the declared accent is dead code. Until this is closed, every new page doubles the drift.
