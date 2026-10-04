# InnerTube Comments Extraction (logged-out) — S9 (2026-08-08)

Proven on EVjOukIg_bQ (TegapTV gym feature): **28 of 46 comments recovered verbatim** via YouTube's InnerTube API **logged-out**, from this VPS, while yt-dlp and transcript endpoints were bot-walled. Comments ≠ transcripts: InnerTube comment continuation works where caption endpoints don't.

## Method notes

- Fetch comments with the InnerTube `next` continuation (logged-out `ANDROID` or `WEB` context); no cookies, no OAuth, no quota key.
- Response is JSON: comment threads with `authorText`, `contentText`, `publishedTimeText`, `voteCount`, `replyCount`, and continuation tokens.

## Fidelity rules (from the 2026-08-08 verification)

- **Preserve verbatim:** non-English + emoji must survive exactly (German "Schultern und Rücken…" was kept; "OMG 😱👍💪😉👏👏👏😘" stayed full — a first pass had replaced it with "[emoji barrage]" shorthand → fixed).
- **Don't coerce types:** raw empty `""` reply counts stay `null`, not `0`.
- **Order matters:** deliverable keeps extraction order.
- **Pagination honesty:** logged-out pagination caps recovery (~18 of 46 lost on EVjOukIg_bQ — InnerTube stops serving continuation tokens). Report the gap; never pad or infer the missing comments.
- **Verify the deliverable against raw:** schema check (unique ids, required fields) + per-comment verbatim diff + JSON round-trip.

## Uses

- Identifying community reaction to an athlete (physique praise, competition-history mentions, cultural dynamics)
- Cross-lingual audience signals (German anatomical praise on a Malaysian bodybuilding video)
- Anchoring "no dialogue" claims: zero comments referencing speech is weak supporting evidence, never proof
