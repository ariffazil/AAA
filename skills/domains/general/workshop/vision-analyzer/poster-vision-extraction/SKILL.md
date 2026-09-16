---
name: poster-vision-extraction
description: Use for poster/image text. Verify with vision, never guess.
---

# Poster / Image Text Extraction Protocol

## SCAR (2026-08-27)
Arif scolded after I confidently listed "Siti Nurhaliza, Yuna, Aina Abdul" for a Jiwa Merdeka poster — I was **guessing from popular Malaysia Merdeka lineups, not reading the actual poster**. Vision module returned different names; I falsely attributed guess to vision.

Lesson: **Distinguish "vision extracted" from "memory filled in".** SOUL.md declares "I have NO native vision". vision_analyze is a separate module call. If I haven't called it AND quoted what it returned, I haven't seen.

## Protocol

### When user asks about image/poster content:
1. **vision_analyze FIRST** with explicit "read every line of text" prompt
2. List **only** what vision returns, verbatim or near-verbatim
3. **Never** add artist names, dates, or facts from memory to fill gaps
4. If uncertain, say so plainly: "vision tak jelas kat sini, hang boleh zoom?"

### When vision returns text:
- Quote directly, do NOT embellish
- If text is partial, say so — don't complete from memory
- Distinguish clearly: "Vision baca: A, B, C" vs "Memory tambah: D, E"

### Anti-pattern
- Confident list without explicit "vision baca" prefix
- Fill in missing names from "Malaysia Merdeka typical lineup"
- Assume poster text is readable when blurry/small

### Right pattern
- Call vision_analyze with "read every line"
- Report what vision returned, exactly
- "Vision tak baca [position], hang zoom?"

## Malaysia Artist Confusion (don't substitute)
- **Siti Nurhaliza** — pop/R&B ballad queen, P. Pinang, 1995
- **Sheila Majid** — jazz/pop pioneer, KL, 1985
- **Yuna** — indie pop, KL/Sarawak, 2008
- **Aina Abdul** — pop/R&B, KL, 2019
- **Dayang Nurfaizah** — jazz/vocal, KL
- **Faizal Tahir** — rock/pop, KL

## Memory note
Save to honcho_conclude ONLY if confirmed by vision or by user explicit statement — never from own assumption.
