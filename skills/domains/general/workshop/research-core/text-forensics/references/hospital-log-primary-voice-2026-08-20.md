# Hospital Log Primary-Voice Read — "Discuss abah" (learned 2026-08-20/21 night)

Class: family-group log where one member's OWN typing is the only direct data on that person (all prior knowledge = sovereign testimony). Worked case: Faridah (Mak) — card was a draft-stub built from Arif's interpretation; the group export delivered 281 lines of her own voice.

## Trigger

Sovereign sends (or already delivered, see P13) a family WhatsApp group export centered on a medical crisis. One participant is a person you hold only testimony-level data on. Their lines in the group = UPGRADE from testimony → primary source.

## Why the group export is different from a 1:1 export

- A 1:1 chat gives you the dyad. A **family medical-crisis group** gives you the full division of labor under load: who reports, who pays, who coordinates beds, who protects the youngest from news, who goes silent.
- Message VOLUME is role, not affection. Mak's 281 lines were mostly logistics — that IS the love-language data. Don't weight senders by count; weight by WHAT they carried.
- The group often dies at the event boundary (last line 29 Feb, death 2 Mar). **The silence after the last line is part of the timeline.** Note where the log stops and why.

## Pipeline additions (on top of standard Phase 1-5)

1. **Per-sender line extraction FIRST**: `grep -n " - <NAME>:" file | wc -l` per participant. The person you're upgrading gets their own full read — every line, in order.
2. **Identify the update grammar.** Crisis coordinators develop one (shift-logbook style: times in/out, doctor names, med flow). Quote it verbatim in the card — the grammar itself is the personality data: "Sampai hos 7.20 balik 9.10", "Mak pi dari pukul 12.10 sampai 2.40 balik rumah. Letihlah jiaa."
3. **Grief-leak collection.** In logbook grammar, emotion escapes one word at a time, never sentences ("Penatnya." "Takutnya tengok." "Kesian kat abah." "Ya Allah."). Collect these into a block — they are the person's actual emotional register, primary-sourced.
4. **The care-work inventory.** List the physical acts the person REPORTS DOING THEMSELVES (salin pampers, mandikan, sapu ubat, bagi makan, check tiub). Never infer care-work from role — only from their own reports or others' direct attestation in-log.
5. **Money-moment isolation.** Find every money exchange in the group and extract the exact micro-sequence. Worked case (27 Jan, 3 minutes): Mak tags eldest "@ARIFFAZIL cukup ka duit?" → he offers RM550 transfer → "Xyahh, mak guna duit kad mak." A person's money grammar under crisis resolves decade-old ambiguities (hands-love vs invoice-love) better than any testimony.
6. **Last-line archaeology.** Quote the person's final message in the group + what was pending when it went silent. "doktor kena ambil darah hari ni sekali lg baru buat keputusan" — the decision that never arrived. This line will outlive everything else in the card.
7. **Sovereign's own lines = infrastructure audit.** His lines look thin ("Kuman banyak lagi ka?") — cross-reference with others' attestations of what he DID (paid hospitals, insurance placement 15 days before death, gated info to protect the SPM sibling). When a logistics-parent's presence is invisible in his own lines, it's visible in others' gratitude lines. Cite both.
8. **Memory-surface cascade after the read.** Same-turn writes: person-card upgrade (testimony→primary sections, keep both labeled) → H1 reality memory person section → people/INDEX.md row → people_registry.json status fields. Then report surfaces written. (See crisis-shadow-decode pitfall 15 for the question design that feeds this.)

## Card-writing rules for the upgrade

- Keep testimony sections, re-label: `[F13 testimony, <date>]`. New sections: `PRIMARY VOICE READ (<n> lines, <range>)`.
- The grammar-resolution paragraph (e.g. love-as-work vs love-as-invoice) must cite WHICH layer resolved it. If the log resolved a testimony ambiguity, say so explicitly — the provenance is the finding.
- Mark remaining gaps as OPEN threads — a primary read usually CLOSES some and OPENS others (which twin, why the give-ups).
- **False-receipt guard (P14 applies)**: "card dah upgrade" may only be said AFTER write_file returns verified. If said early, own it in-card (correction log entry) and in-chat.

## Diff-verified dual-export note

Two exports of the same chat (original + retry) = free chain-of-custody. Normalize (`tr -d '\r'`, trim, drop blanks) then `diff`. Expect mention-format variance between export generations (`@⁨Mak⁩` → `@60124910258`), ±1min timestamp drift, merged wrapped lines — after normalization these are artifacts, not content drift. Identical content = safe to ratify cards built on it.

## Session-boundary disclosures stay OUT of cards

Same-night vents (the "BANGANG satu kampung" discharge, the 1AM "benda ghaib" category) do NOT enter person cards or reality memory unless the sovereign says so. Cards carry the people; the session carries the night. (crisis-shadow-decode pitfall 13.)
