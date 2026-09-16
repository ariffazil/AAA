# Scarce-Source Tiered Output

> Pattern for when the user asks for a list of N entities (top 10, all competitors, full roster) and the public record returns less than half. Forces a tiered, labeled deliverable instead of fabrication. F2 TRUTH + F9 ANTI-HANTU compliance.
>
> Complements `competitive-field-research.md` for the niche/local-event case where even the organizer hasn't published a full roster yet.

## When to Use

- User wants a ranked list or full roster
- Authoritative database (NPC/IFBB/UFC/etc.) doesn't have the event because it's a local/niche/sanctioning-body event
- Organizer official page exists but hasn't posted the full competitor list yet (typical for events 1-7 days out)
- IG/Facebook scraping hits 429 after a few handles
- `web_search` hits `loop_web_search_cap` returning garbage (see pitfall in `competitive-field-research.md`)
- Net verified: less than half the requested N

## The Three-Tier Output Structure

### Tier 1 — VERIFIED (with source URL)

What was found in primary or secondary sources with a traceable link.
- Include: name, source URL, source date, what was confirmed
- Do NOT extrapolate. If the source only confirms 2025 winner, the claim is "2025 X winner" — NOT "competing in 2026".
- Tag every claim with the source date. A 2025 result is not a 2026 prediction.

### Tier 2 — SCENE REGULAR (signal but unconfirmed)

Strong contextual signals that an entity is likely in the field — IG handle matches the event tag, federation roster, past coverage of the same category, sponsor cross-references — but no direct confirmation for THIS specific event.
- Label: `[SCENE REGULAR — not confirmed for this event]`
- Explain the inference (gym affiliation, past category, federation membership)
- Confidence cap: 0.50

### Tier 3 — DARK HORSE (structure-only expectation)

Expected to exist based on event structure (e.g. "15 categories → 15 winners' worth of names will eventually surface"), but no name attached yet.
- Label: `[DARK HORSE — category structure only]`
- Frame as the field you'll watch to fill in (e.g. "Champ of Champ 2024 winner — TikTok coverage exists, name TBD")
- Confidence cap: 0.20

## Mechanical Rules

1. **Count honestly.** If only 4 verified names exist, report "4 verified + 4 scene regular + 2 dark horse = 10." Never pad with fabricated bios to hit N.
2. **Every claim gets a source URL OR a tier label.** No middle ground.
3. **Reframe the deliverable if needed.** "Top 10 confirmed" is impossible; "Top 10 to scout before going" is honest.
4. **State the methodology gap.** "Public roster not posted yet — most likely releases on organizer IG/TikTok 24-48h before event."
5. **Offer the human the in-the-loop role.** "Hantar IG handle yang hang jumpa, aku cross-check + tambah list." Converts a one-shot into collaboration.

## Anti-Patterns (capture these as scars)

| Anti-pattern | What it looks like | Why it fails | Fix |
|---|---|---|---|
| **Pad to N** | Generate N plausible names with no sources to satisfy "top N" | F2 TRUTH violation; trust collapse | Report the gap; tier the deliverable |
| **Speculate as fact** | "Likely defending" stated without source | F9 ANTI-HANTU | Use `[SCENE REGULAR]` label |
| **Loop until N found** | Repeat `web_search` past `loop_web_search_cap` | Mirror loop — see `competitive-field-research.md` pitfall | Break strategy; report partial; defer rest |
| **Hide IG scraping limits** | Pretend no athletes found | False negative; user loses scouting head-start | State the 429/rate-limit explicitly |
| **Re-cast past winners as current** | 2024 winner → 2026 competitor without verification | F2 TRUTH | "2024 winner per [source] — 2026 participation not confirmed" |
| **Up-convert snippets to findings** | Pattern-complete snippet text into narrative claims | FM9 (Grand-Theorize Without Source) | Snippets are signals, not findings. Label them. |
| **Wait until perfect** | Hold the deliverable hoping for more data | User loses real-time scouting value | Deliver tiered NOW; user fills gaps live |

## Decision Tree

```
User asks for N entities
  │
  ├─ Sources return ≥ N verified? → normal deliverable
  │
  └─ Sources return < N? → SCARCE-SOURCE PROTOCOL
        │
        ├─ Tier 1: report with URLs
        ├─ Tier 2: report with signal explanation
        ├─ Tier 3: report with category structure
        ├─ State methodology gap
        └─ Invite user in-the-loop
```

## Worked Example — Mr. Enrich On The Go 2026, 2026-08-27

**User wanted:** "top 10 to watch" at a local Malaysian bodybuilding event 2 days before it starts.

**Sources exhausted:**
- Organizer IG (`@enrichbodybuildingclub`) — found, but full roster not posted
- IG scraping 429 after 3 handles
- `web_search` hit `loop_web_search_cap` after ~50 calls returning garbage
- Daily Express, Molek FM, Stadium Astro → 2025 winners confirmed (Kinabalu edition)
- TikTok → "Malek Noor Mr Enrich 2025 First Timer" found
- TegapTV Facebook → category-poster image (15 categories)
- `@urbangtm` (handle "MrEnrich") found but not verified

**Correct deliverable:**
- 4 VERIFIED (Malek Noor, Syed Muhammad Alhabshi, Mohd Asraf Hamza, Affan Aff — all 2025)
- 4 SCENE REGULAR (`@urbangtm`, TegapTV featured athletes, Binaraga cross-border, KL BBF roster)
- 2 DARK HORSE (Junior category breakout, Champ of Champ 2024 winner — name TBD)
- Plus methodology gap: "Public roster likely 24-48h before event on @enrichbodybuildingclub"

**User response:** "Buat ja la yang arif lagi bijaksana untuk abang sado" — accepted the methodology.

**Key learning:** The honest "10 to scout" is more useful to the user than a fabricated "10 to watch." The user can fill the gaps from event photos and live attendance. The fabricator cannot.

## Floor Alignment

- **F2 TRUTH:** every tier label is a truth signal; user reads and trusts the boundary.
- **F9 ANTI-HANTU:** never pretend to know more than the evidence supports.
- **F3 WITNESS:** user + AI + (when possible) external source URL form a tri-witness on each claim.
- **F7 HUMILITY:** confidence cap = whatever the source supports (0.90 for primary press, 0.50 for scene inference, 0.20 for dark horse).

## Proven

- 2026-08-27: Mr. Enrich On The Go 2026 athlete roster — 4 verified + 4 scene regular + 2 dark horse. User (F13) accepted the methodology as "lebih bijaksana" (smarter). Demonstrated the protocol works under real source scarcity.
