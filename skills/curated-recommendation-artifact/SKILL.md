---
name: curated-recommendation-artifact
description: Use when ranking media picks from a person's taste.
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# Curated Recommendation Artifact

## 1. Taste comes from named titles, never from biography

A recommendation is a claim about a person, and it is only as good as its evidence.

- **Derive taste only from titles the person explicitly named.** Occupation, employer, seniority,
hobby and the tone of past conversation are not evidence. A geoscientist does not thereby like
documentaries; a fitness coach does not thereby like sports films. Biography-based inference reads
as being profiled, and when it is wrong the whole artifact goes with it.
- **No titles given? Ask ONE short question for two or three.** A binary ask, not a menu.
- **Name the pattern in one sentence, not a genre list.** "You want to understand why people do
wrong" lands; "likes crime drama" does not.
- **Say what would change the ranking** ("give me a fourth title and this moves").

## 2. Two readers means three rails

- One rail per person plus a shared rail; a stated count is a ceiling, never a target to exceed.
- The shared rail must satisfy BOTH tastes — averaging two tastes produces the bland middle neither
opens.
- Strongest title first in every rail; the reader usually only takes the top three.

## 3. Build with real cover art

Keyless TVMaze `singlesearch` → verify match → PIL thumbnail → base64 data URI. Full code and
assertions: `references/cover-art-pipeline.md`.

- **Verify every title match** (name, network, premiere year). Fuzzy search returns regional
spin-offs and same-named documentaries; a wrong poster is a fabrication with a picture on it.
- **Key metadata by canonical name, not the query string** — APIs normalise case (`BEEF` → `Beef`),
so a query-keyed dict raises `KeyError` mid-render. Use a lower-cased lookup, assert card count.
- **Embed images as data URIs** so the file works offline and cannot rot.
- **Generate cards in code, substitute into a template placeholder.**
- **Label the originating network honestly**, not the platform you assume carries it; catalogues
vary by country and month.

## 4. Verify before delivery

Card count, image count, and images with `naturalWidth > 0` must all equal the requested total. Then
screenshot a viewport for the chat preview and send the HTML file alongside it.

## 5. What the artifact owes the reader

- A match percentage is curator confidence, not platform data — say so on the artifact's face.
- Name the metadata source, that posters are embedded, and the build date.
- If picks came from inference rather than stated titles, print that limitation in the frame.

## 6. When asked how recommenders work

Behaviour signals (play, completion rate, pause, skip), collaborative filtering on similar viewers,
per-row ranking models, and contextual-bandit artwork selection. Completion rate is the strongest
honest signal; demographics are not an input; catalogues vary by region.
