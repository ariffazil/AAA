# Event-Anchored Retrieval & Temporal Anchoring

Forged 2026-08-20 from a live session: user asked "find the exact date of the Siti Nurhaliza Genting concert, then reflect the WhatsApp logs from that date." The session produced two caught fabrications and one clean workflow. This reference encodes the workflow and the traps.

## When this applies

- User names an external, verifiable event (concert, court date, flight, wedding, holiday) and asks what the chat said around it
- User asks "why did X happen on that date" — any analysis where a **date, weekday, job title, or life circumstance** carries explanatory weight
- Cross-referencing a chat export against outside-world facts (venue, schedule, public calendar)

## Workflow (order matters)

1. **Fix the anchor FIRST, from an external source — never from memory or from the chat's own framing.**
   - Search the web for the event's exact date + venue. Prefer concert-archives / official venue listings over blogs.
   - The chat log itself is NOT the source for the event date — people discuss plans that change, cancel, or refer to different events. Example: user remembered "Siti concert at Genting a few years back"; the chat discussed TWO different Siti concerts (Genting 10 Aug 2024, Bukit Jalil 10 Jan 2026). Only external verification separated them.
2. **Verify the weekday with `date -d YYYY-MM-DD '+%A'`** (or equivalent). Never state a weekday from memory, even for famous dates. NEVER carry a weekday from a prior session's output — check the live calendar every time.
3. **Extract the chat window around the anchor with awk, not grep:**
   ```
   awk '/^8\/4\/24/,/^8\/13\/24/' "Chat.txt"
   ```
   WhatsApp US-format dates: `M/D/YY`. Watch the leading-zero trap — `8/10/24` not `08/10/24`, so grep patterns for `8/1[0-9]/24` must be built carefully; awk ranges are safer than grep for windows.
4. **Read the FULL window including days after the event** — the fight may happen after the concert, not at it. In the 8/10/24 case the morning logistics messages looked innocent; the explosion was 11:07 AM and again 8:16 PM the same day. A narrow grep for the date alone misses the arc.
5. **Pre-window context is causal context.** The month BEFORE the event (who bought tickets, who declined, who offered to pay, plans changed) is where the emotional debt accrues. The event is just the trigger.
6. **Only then interpret.** Present: anchor (verified, cited) → pre-window → event-day sequence → aftermath. Label every inference as inference.

## Fabrication traps (both caught live in one session, 2026-08-20)

### Trap 1: Weekday/narrative from memory
Agent repeated "24hb Ahad" (it was Isnin/Monday) and "hearing pusaka 27hb" (case settled the previous year) — stale data from memory carried forward into a fresh narrative. The user corrected it.
**Rule:** any date claim → run `date` command. Any case-status claim → check the document source again, never memory. Memory carries narrative residue; documents don't.

### Trap 2: Back-projecting CURRENT life circumstances onto a PAST window
Agent explained a person's August 2024 behavior with "schoolteacher holidays." The person only became a teacher around April 2026 — <5 months at analysis time. In 2024 they were NOT a teacher. The user caught it: "dia mana kerja cikgu lagi wei... baru start x sampai 5 bulan."
**Rule:** before explaining past behavior with a job/schedule/role, verify the person held that role AT THAT DATE. When start-date is unknown, say so — do not fill with a plausible calendar. A missing fact is a hole; an assumed fact is a fabrication with a shelf life.

### Trap 3 (near-miss): trusting the user's frame of the anchor either
User said "Genting"; the first concert offer in the log was for a DIFFERENT venue/date (Bukit Jalil Jan 2026). Both were real; conflating them would have produced a false timeline. Multiple similar events may exist — disambiguate by venue + year before anchoring.

## Payment/obligation claims — receipts or silence

In family-conflict sessions the user will assert financial claims ("I paid for almost everything"). The chat log contains conversations, not bank records. Only seal amounts that appear as numbers in the log or in a document (e.g., "Rm1500", "RM314.50", "RM300 ja la"). Everything else stays unlabeled: "no amount found in records — need receipts." Never convert a feeling of having paid into a sealed fact, and never dismiss it either — hold it as OPEN.

## Output shape

One compact narrative: verified anchor + what the log actually shows, hour by hour, with direct quotes for the load-bearing lines. Frequency-annotate any quote used to characterize a person or relationship. End with what remains unknown and would need a live source (receipts, the other person, a voice note).

## Cross-references

- `1on1-tenure-analysis.md` — the deeper per-person protocol this builds on
- SKILL.md §Cross-Medium Verification — always run before presenting
