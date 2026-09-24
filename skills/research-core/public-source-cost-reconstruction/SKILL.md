---
name: "public-source-cost-reconstruction"
description: "Reconstruct event cost from public sources for viral post."
version: 1.0.0
capability_tier: fed-reasoning-heavy
risk_tier: medium
tags: [cost, public-source, event, social-media, methodology, defendability, viral, malaysia]
metadata:
  hermes:
    category: research-core
---

# Public-Source Cost Reconstruction for Viral Use

Reconstruct the cost of a public event, public programme, or public-facing programme from publicly available sources, then translate that cost into a viral, defendable social-media framing. The output is two-layer: a viral-facing surface (caption, image, one-liner) AND a methodology artifact (per-input tagging, sensitivity ranges, source citations) that survives challenge.

## When this skill applies

Use this skill when ALL THREE of these are true:

1. The user is asking "how much did X cost" where X is a public event / programme / campaign — not a private transaction.
2. The user wants the answer turned into a viral or shareable surface (IG caption, poster, one-liner).
3. The user has signalled concern about defensibility — explicitly or implicitly — through phrases like "kalau kena saman", "bukti", "calculation", "methodology", or by asking for sensitivity/range output.

If the user only wants an analyst-grade report without the viral surface, route to `principal-analysis-artifact` instead. If they want only the viral surface without the methodology, route to `public-column-publishing`. This skill covers the **two-layer bridge** between them — viral *and* defensible.

## Procedure

### 1. Confirm the event identity and pull KNOWN inputs

Before estimating, separate known from unknown:

- **Known (UKUR)**: event name, edition count, dates, attendance figures, speaker count, sponsor count, host, knowledge partner, organiser, venue, dates of editions.
- **Source hierarchy**: prefer the host's own press releases, then major outlets covering the event (The Star / FMT / Bernama / NST / DagangNews), then the knowledge partner's official channels, then organiser's company profile, then industry comparable rates for costs.

Record each known input with its source. Do NOT estimate before the known list is complete — every estimate cascades from a known anchor.

### 2. Reconstruct revenue side (Low / Mid / High scenarios)

Build a tier-mix estimate for sponsorships. Standard industry tier structure for major conferences:

```
Diamond/Title      — top 3 sponsors
Platinum           — next 8–10
Gold               — next 15–20
Silver             — the rest
```

Three rule-of-thumb references:
- **CERAWeek Houston** publishes tier rates publicly — these are the upper bound for a flagship energy conference.
- **Asia editions** of major conferences typically run at 40–60% of the Houston rate.
- **Government / institutional conferences** (with PM keynote, OPEC SecGen present) sit at the upper end of that range.

Run three scenarios (Low / Mid / High) for sponsor revenue AND for attendee fee revenue (delegate pass). Compute totals in each scenario. Do not pick one — present all three so the reader can pick the conservative frame.

### 3. Reconstruct operating cost side

Standard line items for a 3-day, 4,000-person conference at a KLCC-tier venue:

- Venue (KLCC 3-day full-hall rental)
- Production / A/V / broadcast
- F&B (per-pax-per-day industry standard ~$300)
- Speaker travel (international + domestic mix)
- Executive hospitality (PM + ministerial hosting)
- Branding (billboards, social, ads)
- Organiser fee (10% of revenue is standard industry)

Tag every line item with its basis. Anything that comes from a public comparable (CERAWeek, KLCC rate card, F&B industry standard) is UNJUR. Anything that comes from a primary PETRONAS / organiser disclosure is UKUR.

### 4. Compute net cost to the host

For each scenario: `Net = Revenue - Opex`. Show all three. **The point is NOT to find a single number — it is to show that no scenario can hide the underlying pattern.** If the event is net-loss in every scenario, that is itself the finding.

### 5. Translate to human-scale framing

Pick a translation the user can defend:

- **Years of salary** at a relevant band (entry-level / mid-senior / Principal). Use total compensation (gaji + EPF + 13th + allowances + bonus), not just gaji pokok.
- **Comparison ratio** against a known anchor (e.g., "this single event = 7% of one year of layoff savings" — both numbers must be sourced).
- **Per-pax** if the framing is about scale ("RM X per attendee for 3 days").

### 6. Round the headline number to fit human mental models

The user may ask for "X years of salary". Round the headline to a number that fits the audience's intuition:

- 206 → 99 years (human lifespan frame, more viral)
- 99 → 33 or 50 if needed for shareability
- Keep the precise number in the methodology artifact; use the round number in the caption

**The reason:** analyst-precise numbers do not viral. Round-to-2-digit numbers that fit a mental lifespan do. The defensibility comes from the methodology file, not the headline.

### 7. Build the two-layer deliverable

**Viral layer** (what gets posted):
- Caption (short, max 2 screens of text)
- Image/poster if requested (typography-driven, no logos, no trademarks — those create legal exposure)
- One-liner that survives screenshotted out of context

**Defensive layer** (what survives challenge):
- Calculation file (`cost_calc.txt` or equivalent) with every input tagged UKUR / UNJUR
- Source list at the bottom of the file
- Anti-saman checklist: what you can write (methodology, sourced numbers, public-domain terms of office), what you cannot write (allegations of corruption, unverified personal attacks, names without independent verification)

### 8. Build a per-claim rebuttal grid

For every number in the caption, write a one-line rebuttal:

```
Soalan: "Macam mana hang tahu RM53.5m?"
Jawapan: "Mid-scenario opex. CERAWeek tier rates published,
         KLCC venue benchmark, F&B industry standard. Methodology ada."
```

This grid lives in the methodology file, not in the caption. Its purpose is to make the user ready when challenged.

## Pitfalls

- **Single-number confidence.** A single headline number ("the event cost RM X") is the failure shape. Always show Low / Mid / High with explicit basis, and let the user / audience pick the frame. The headline rounds; the methodology carries the precision.
- **Wrong landmark name in caption.** Naming a building or location incorrectly poisons the whole argument. If unsure of a building's name, use the city ("KLCC", "Menara KLCC") or the role ("PETRONAS HQ") rather than a specific name that might be wrong. Verify before publishing.
- **Personal allegations in caption.** "X is corrupt" is defamation. "The event cost X years of salary for a Principal geoscientist" is methodology. Target structures and decisions, not people. Satire is welcome; invented facts are not.
- **Trademarked text in poster.** Logos, sponsor names, event brand names reproduced verbatim can trigger takedown. Use paraphrases ("the state energy company's annual flagship event") or descriptive references, not reproductions.
- **"Hang kat kvm8" trap.** If the user says "ada laaa, hang kat kvm8" — meaning "the file you produced, just send it" — interpret as "give me the file path" not as "you are physically located at KVM8". State the path; do not promise features the environment cannot deliver (4K photo upscaling, image generation when no image-gen tool is available).
- **Tool-availability failure.** This skill produces typography-driven posters via WeasyPrint HTML→PDF. It does NOT generate photorealistic images. If the user asks for photo-quality output, the response is "I do not have an image generation tool in this environment" plus the alternative the user CAN use (phone Remini / Snapseed / phone Print-to-PDF of the HTML).
- **Missing source-of-record.** When the event is hosted by a private GLC (PETRONAS, Khazanah, etc.), the methodology must note which items are from public disclosure vs from comparable estimation. Hiding the boundary between "they disclosed" and "we estimated" is what makes a credible reconstruction collapse under cross-examination.

## Quality check before delivering

1. Is every input in the methodology file tagged UKUR (public primary source) or UNJUR (estimate with explicit comparable)?
2. Are three scenarios (Low / Mid / High) presented for the load-bearing numbers?
3. Does the headline number fit a mental lifespan frame the audience can grasp in 2 seconds?
4. Is the rebuttal grid ready for every claim in the caption?
5. Is the personal-vs-structural line drawn (no individual targeted, only the structure / decision / pattern)?
6. Are logos, trademarks, and unverified personal names absent from the viral surface?
7. Is the deliverable two-layer (viral + methodology), not just one or the other?

If any answer is wrong, fix it before delivering.
