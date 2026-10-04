# Design Templates — Three-Surface Layout Matrix

arif-fazil.com publishes text in three distinct visual registers. This reference
captures the design identity of each so agents can route essays to the right surface.

## Surface A: Medium (External, Minimal)

**URL pattern:** `https://medium.com/@arifbfazil/<slug>`
**Example:** "The Scar Behind the Vision: Steve Jobs and the Architecture of Rejection"

| Element | Presence |
|---|---|
| Navigation | Medium global header only |
| Breadcrumb | None |
| Author byline | Medium profile metadata (avatar, name, followers) |
| Title | Large, dark, sentence case |
| Subtitle / dek | No explicit dek — lede sentence in body |
| Featured image | Full-bleed photo hero (Unsplash) |
| Body | Single column, ~680px, generous whitespace, clean typography |
| Section headings | Bold, no emoji (in this essay — emoji in others optional) |
| Tags | Below body: pill-style |
| Footer | Medium footer (write, sign up) + canonical URL |
| Seal / vault hash | Invisible to reader — embedded as `Canon Capsule Ref:` in footer |
| Data points | Inline, no special styling |
| Source panel | None |
| Reading time | Medium "3 min read" |

**Feel:** Intimate. Like a letter from the writer. No chrome between reader and emotion.

---

## Surface B: `/words/writing/` (Sovereign Host, SPA + Static Shell)

**URL pattern:** `https://arif-fazil.com/words/writing/<slug>/`
**Example:** "The AGI Paradox: Why Bigger Models Won't Save Us"
**Component:** `src/pages/EssayPage.tsx` (127 lines)

| Element | Presence |
|---|---|
| Navigation | Site nav bar: ARIF FAZIL · Home · Earth · Words · World · Work |
| Breadcrumb | `← Essays` (link back to index) |
| Section label | `Narrative · Ψ SOUL` in forge-gold |
| Title | `text-4xl md:text-5xl font-black italic uppercase leading-[0.9]` |
| Subtitle / dek | **None** — no excerpt/stats in the hero |
| Author byline | Date + tag pills only (mono font, forge-dim) |
| Featured image | None (title + label only in the hero) |
| Body | `max-w-3xl`, `prose-invert`, `text-lg leading-relaxed` |
| Bottom bar | "⚒️ Published directly on arif-fazil.com" badge OR "✍️ Read on Medium" link |
| Footer | Global layout footer (arif-fazil.com · Constitutional surface · MakcikGPT · Doctrine · /feed.xml · llms.txt · missions.json · surfaces.json) |
| Data points | Inline only — no special styling |
| Source panel | None |

**Feel:** Sovereign home for the essay. Forge brand — dark, gold-accented, italic title. Still intimate because no sidebar or data chrome.

**Note:** The "Narrative · Ψ SOUL" label and forge-branded hero header are
built into EssayPage.tsx. For personal/reflective essays, this is the default
and needs no SPA changes. The identity is already appropriate for intimate
register.

---

## Surface C: `/world/makcikgpt/` (Sovereign Host, Direct-Write Static)

**URL pattern:** `https://arif-fazil.com/world/makcikgpt/<slug>/`
**Example:** "Syaitan yang Ingat Dirinya Malaikat"
**Template:** `public/makcikgpt-md/<slug>.html` (direct write)

| Element | Presence |
|---|---|
| Navigation | Site nav bar |
| Breadcrumb | `← MakcikGPT` |
| Category line | `MAKCIKGPT × PETRONAS × AMANAH · SEALED 999` |
| Title | Large heading |
| Subtitle / dek | **Yes**: "CEO PETRONAS dapat perpanjangan kontrak..." |
| Byline | `By Arif Fazil · Sealed 999 · 9 Aug 2026 · 5 min read` |
| Tags | Below byline: pill-style |
| Featured image | None |
| Body | Full-width text with inline styled data points |
| Data highlights | **Bold red numbers** (`-17%`, `-23%`, `70.5%`, `RM4.2B`) pulled out as visual anchors |
| Blockquotes | Centered, styled — rhetorical questions |
| Source panel | **Yes**: 📊 Sovereign Economic Cockpit → · 📖 PETRONAS Capacity Pulse → · 📰 FMT source → |
| Attribution line | `— MakcikGPT · Civic Intelligence · 9 Ogos 2026 · Sumber: ... · [OBS]` |
| Footer | Full constitutional footer + "Ditempa bukan diberi — Forged, not given." |
| Seal stamp | Embedded in breadcrumb and byline |

**Feel:** Institutional civic journalism. Data-forward. The reader's trust is
built through visible sources, bold numbers, and constitutional branding. The
identity says: "This is audited. This is sealed. You can verify everything."

---

## The Golden Rule (Arif, 2026-08-11)

> Emotional essays need LESS scaffolding, not more.
> Data journalism needs MORE scaffolding — sources, numbers, seals.
> The surface that works for one will suffocate the other.

## When to Cross Surfaces

- **Personal essay with data references** → `/words/writing/` wins. Use
  inline numbers without the MakcikGPT chrome. The SPA template is clean
  enough for intimacy; no source panel needed — cite in body with links.

- **MakcikGPT article with personal voice** → MakcikGPT surface wins. The
  Makcik persona is a public register — it's personal on purpose, but it's
  not private. The data anchors make the voice legitimate, not the other way
  around.

- **Medium-only article (like "The Scar Behind the Vision")** → The Medium
  template is the destination. No need to republication on `/words/writing/`
  unless Arif explicitly asks. The article's `generated/g_scar_behind_the_vision.ts`
  stub with empty `html` and `mediumUrl` pointer is the correct state for
  Medium-only essays — it registers the essay in the site catalog without
  republishing the body.

---

## The "Two Agents, One Scar" Failure Mode

**What went wrong:** A sibling agent tried to fetch Arif's "The Scar Behind
the Vision" essay from Medium. `browser_navigate` hit Cloudflare. The agent
did not fall back to `web_extract`. Instead, it narrated from search snippets
and produced a fluent response claiming the essay was a "constitutional scar"
and "scar governance" — neither of which was in the actual text.

**The fix:** `web_extract(urls=[...])` works through a backend HTTP client
pathway that bypasses Cloudflare. It returned the full 3-minute essay including
the canon capsule tag and vault hash.

**The permanent lesson for essay publishing:** Before writing an article that
references a source essay:
1. Try `web_extract(urls=[source_url])` first
2. If that fails, try `forge_fetch(mode="readable")`
3. Only when ALL fetch pathways return blocked/empty: declare `SNIPPET_ONLY`
   or `UNKNOWN` — never write from fragments

See `references/cloudflare-bypass-web-extract.md` for the full failure
transcript and pathway ladder.

---

*Grouped: 2026-08-11 from the "Two Agents, One Scar" session.*
*Source: EssayPage.tsx (127 lines), live browser screenshots (MakcikGPT and /words/writing/), Arif's verbatim design preferences.*
