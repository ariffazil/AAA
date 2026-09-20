# WhatsApp Export Mining — worked example (2026-08-20, Nabilah/Fahim case)

Companion to SKILL.md Source 7. The positive-path case: person has NO Telegram presence, but full WhatsApp history exports existed in `/root/.hermes/cache/documents/`.

## Situation

User (on a train, pre-hearing stress): dropped fragments — "hutang since before married?", "voice note = PROPA", "duit lawyer". Two claims needed verification:
1. Voice note story: whose voice was it, what did it claim (Fahim: along loan → credit card debt)?
2. "Duit lawyer" — which lawyer, which case, who paid?

## Moves that worked

### 1. Discover exports by listing, not guessing
```bash
ls -la /root/.hermes/cache/documents/ | grep -i "WhatsApp"
# Found 6: Nabilah Fazil, FaridahOthman, Azwa, Naazira Fazil,
# siblings for life, Family kita, Discuss abah  (2015–2026 ranges)
```
The Nabilah export alone was 2.2MB uncompressed — 38k+ lines, 11 years.

### 2. Keyword grep with line numbers, then `sed` context windows
```bash
grep -n -i "ctos" "WhatsApp Chat with Nabilah Fazil.txt"
# 38394: 7/7/26 11:31 Nabilah: Ni fahim punya ctos
sed -n '38380,38430p' ...   # recovered the WHOLE 7/7/26 confrontation thread
```
Findings that overturned assumptions:
- The "voice note" was **Fahim's own voice** — next-line: `Fahim yg reply ni. Not me.` (attribution confirmed by chat participant, not inferred).
- The CTOS brief in chat was **agent-generated earlier from the actual CTOS image** — numbers (RM123K, 300/850, first line Okt 2017) were real data, not fabrication. Verified by cross-reading the brief text in the export.
- Pre-kahwin vs post-kahwin debt question answered by the brief itself: first line 2017, six more lines 2023–2025.

### 3. Cross-chat timeline join (the powerful move)
Keyword "lawyer" hit in a DIFFERENT export (Naazira):
```
8/9/24 1:13PM Arif: Lawyer ni pon pi genting jugak
8/9/24 5:33PM Arif: Sebab dia esok nak pi kl konsert siti jugak
8/10/24 4:45PM Arif: Duit lawyer tu satu sen pon I x mintak duit dia kot
```
→ "duit lawyer" ≠ divorce lawyer. It was **Munirah (SKSG), the pusaka lawyer**, engaged Aug 2024. Family chat 3/3/25 confirmed payment: `Mak: Ini bayaran Arif dah bayar. Kat Munirah ka`.

### 4. External date anchor
User demanded exact concert date. Web backends failed (SearXNG junk results, firecrawl 402, minimax quota). Working fallback:
```bash
curl -s "https://html.duckduckgo.com/html/?q=<query>" -H "User-Agent: Mozilla/5.0..." | python3  # parse result__a / result__snippet
```
→ Siti Nurhaliza "Love Is In The Sky", Arena of Stars Genting, **10 Aug 2024, 8:30PM** (3 sources concur). Locked the window: pusaka engagement (8/4) → lawyer-and-family concert weekend (8/9–10) → aftermath vent (8/10–11), same week.

## Pitfalls hit (encode, don't repeat)

- **Rotated-`gateway.log` grep alone would have returned "nothing"** — the story lived entirely in WhatsApp exports. Named-person pre-flight MUST include the cache/documents listing.
- **User's shorthand ("PROPA semua tu") is a verdict about FRAMING, not about facts.** The facts inside a one-sided narrative can still be real (CTOS was). Verify the artifact, describe the framing separately.
- **Shared display handle**: "Fahim Nabilah" account posts are Fahim. Check surrounding turns before attributing.
- **Archive immediately**: copied Nabilah zip to `/root/.hermes/lanes/private/nabilah/whatsapp-export-2015-2026.zip` (chmod 600) — cache is evictable, case files must not be.
- **DuckDuckGo HTML endpoint via curl works when every search tool backend is down.** UA header required.

## Output pattern that landed with the user

Timeline table: date | source-chat | exact quote → then interpretation kept separate and labeled (OBS vs DER). The user audited sourcing hard ("Mana hang dapat info lelaki tu x balik rumah?" — answer: I never claimed it; traced the phrase back to my own question list). Keep claim provenance explicit line-by-line; this user falsifies.
