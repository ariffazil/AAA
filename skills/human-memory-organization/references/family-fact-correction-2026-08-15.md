# Family fact-correction cascade — 2026-08-15 session

> Sovereign DM (F13 lane). Trigger: Arif asked "tell me everything you know about my siblings" after Hermes was added to the family "Kanak-kanak" Telegram group (all sisters present).
> Privacy: F5 HIGHEST. This reference describes the CORRECTION MECHANICS; it intentionally restates only facts already in the person-cards under `/root/memory/people/FAMILY/` (F13-owned). Never surface family names outside sovereign DM / F5 audit contexts.

## Sequence of events

1. **Inquiry.** Sovereign asked what the system knows about his siblings. Cards pulled from `/root/memory/people/FAMILY/` (P-013 Nabilah "Akak", P-014 Naazira "Jia", P-015 Azwa, P-016 Fahim, P-017 minor) + `people_registry.json` + `INDEX.md` + `FAMILY_FAZIL.md`.

2. **Honest uncertainty flagged (worked).** Two UNKNOWNs surfaced instead of guessed:
   - Card said Nabilah "elder sister of ARIF" but chat showed her calling him "abg bendahara" → conflicting signals.
   - Fahim (hospital companion) vs "Muhd. Redhani" (SEARAH filing spouse) — same person or two? Still unresolved at session end.

3. **Sovereign correction (terse, multi-clause):** "Akak tu adik aku. Aku anak sulung. Naazira kerja kat Penang."
   - Fact 1: Nabilah is a younger sister — "Akak" is the eldest-daughter honorific among the sisters.
   - Fact 2: Arif is anak sulung (eldest child, above all siblings).
   - Fact 3: Naazira works in Penang; the Ipoh reference was travel, not workplace.

4. **Cascade attempted → concurrent-edit collision.** A parallel subagent (session `20260815_084041_cb693948`) had already applied the same corrections at 08:46. Patch results: registry P-013 + P-014 landed; nabilah card patches no-opped (stale-file warning, content already fixed); naazira card + FAMILY_FAZIL.md header landed with rewording.

5. **Verifier flag + "Ubah jala".** Platform file-mutation verifier reported "1 file NOT modified" after the "done" claim. Sovereign: "Ubah jala" (= fix it now). Response: full re-read + tree-wide grep sweeps:
   - `grep -rn 'elder sister' /root/memory/` → zero hits (excluding archetypes)
   - Ipoh-sweep across people/, H4-identity/ → all remaining Ipoh mentions correctly framed as travel/family base
   - Registry re-parsed via python json → P-013 relation + P-014 work_location correct
   - End state verified consistent; only then reported "rekod dah selari".

6. **Identity join already made:** azwa-fazil.md carries "Full name: Azwa Safrina binti Fazil (confirmed by ARIF 2026-08-15, Telegram 'Kanak-kanak')" — joining P-015 (family) with P-007 Wawa (telegram_network, node srv1642546). Cross-reference both entries; do not duplicate the human.

## Generalized rules (also in SKILL.md)

1. Chat honorifics encode sibling-internal rank, not relation to the sovereign. Birth order = sovereign testimony only.
2. Transit messages are not employment facts.
3. Verify the fact's end-state tree-wide after any cascade; per-file patch success is not verification. Handle stale-file warnings by re-reading, not re-patching blindly.
4. One human may occupy two registry categories until a sovereign disclosure joins them — check for unjoined duplicates when family members appear in telegram_network.
5. F5 uncertainties are stated as uncertainties, never resolved by inference; offer to lock one correction per turn.

## Open items at session end

- Fahim ↔ Muhd. Redhani relationship: UNKNOWN, awaiting sovereign (do not infer).
- Family "Kanak-kanak" Telegram group: Hermes added; group chat ID not yet seen. When it appears, wire a dedicated family-group lane (group-safe register, F5 discipline: no family names, no family dynamics in any group surface; sovereign memory files never enter that lane). Until wired, family topics stay DM-only.

*Pattern: same wound-class as all P-axis work — testimony is sacred, inference is decoration.*
