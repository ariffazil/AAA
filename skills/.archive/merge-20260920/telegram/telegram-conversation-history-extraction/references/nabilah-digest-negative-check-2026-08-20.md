# Worked example — "digest group X" when the group is absent locally (2026-08-20)

## Request
User (Arif, at KL Sentral before the night train to Penang): "Now digest everything in group dear NABILAH telegram."

## Definitive negative check (all four steps before concluding "not reachable")
1. `jq -r '.platforms.telegram[] | "\(.id) | \(.name)"' /root/.hermes/channel_directory.json` — 28 known chats, none named Nabilah. Closest lookalikes: "Kanak-kanak" (-1003768847825), "YANG Arif" (-5443591163).
2. `grep -i nabilah` over gateway.log + every rotated gateway.log.{1,2,3} — all hits were Arif *mentioning* Nabilah in DMs/SADO; zero inbound from any Nabilah group.
3. Sender census: `grep "inbound message" <log> | grep -oE "user=[^ ]+" | sort | uniq -c` — only ARIF / No name / Mohd in the window. If a group wrote to us, an unknown sender would appear.
4. `find /root/.hermes -iname "*nabilah*" -not -path "*/cache/*"` → `/root/.hermes/lanes/private/nabilah/kes-nafkah-anak-2026-08-17.pdf` (scanned Syariah court filing) — the real artifact to substitute.

## What was delivered instead
- Plain statement: bot never added to that group; Bot API cannot back-fetch history. Offer: add @ASI_arifOS_bot (visibility starts at add-time) or forward/attach the content. Do NOT improvise a substitute group.
- Case digest from the lane PDF: Kes Mal No 2008-040-0633, Mahkamah Rendah Syariah Seberang Perai Utara; Nabilah (plaintif) v Fahim bin Ahmad Shukri; nafkah anak; peguam syarie Tuan Shazril Khairy; anak Fattah Nuqman (3).

## Traps hit
- `pdftotext` returned ~7 chars on the scanned image PDF → pdftoppm + vision path. But BEFORE re-OCRing: `session_search` found a sibling lane (same session lineage, model agi-333) had already run `pdftoppm -png -r 80` + `vision_analyze` on the same file minutes earlier — reused its transcription.
- Same inbound DM mirrored under two chat ids (267378578 and 8410138119, the latter also logging `Blocked unauthorized user` warnings while still processing). Dedupe on text + timestamp.
- Stale weekday inherited from a prior session's packing summary ("24/8 Ahad") — actual: Monday. Always `date -d YYYY-MM-DD '+%A'` before asserting a weekday to the user.
