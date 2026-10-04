# Multi-source human scan (P-axis) — session 2026-08-12

> **Context:** When ARIF directed "build the memory of all humans in this chat logs", the scan revealed 17 humans across 4 sources, not 8. The trap was treating H4-identity as "just PDFs".
> **Class:** This is the canonical pattern for relational memory of humans in ARIF's life.

## The 4 sources — why each matters

### Source 1: H1–H6 directories (obvious)

What you check first. H5-scars contain scar witnesses (institutional archetypes). H4-identity has biographies. H2-experience has session files. All standard.

**What this source ALONE misses:** WhatsApp-forwarded family chats (saved in H4-identity as .md), Reality Legacy PDF (saved in H4-identity), pre-curated HUMANS.md indexes (saved in H4-identity).

### Source 2: H4-identity .md files (THE TRAP)

When you first probe H4-identity, you find PDFs (Biography Final, Full Story, Reality Legacy). You stop there. You miss:

```
/root/memory/H4-identity/HUMANS.md         # canonical human index
/root/memory/H4-identity/FAMILY_FAZIL.md   # WhatsApp family chat extraction
/root/memory/H4-identity/IDENTITY-MODEL.md # (gap — to be written)
```

These `.md` files in H4 carry pre-curated relational memory. They were created by previous sessions/agents. A first-pass scan only listing PDFs in H4 misses the actual relational map.

**Detection:**
```bash
ls /root/memory/H4-identity/*.md
```

If this returns > 1 file, read each one before declaring "no humans in H4". The .md files often have person-cards and relationships that the PDFs do not.

### Source 3: H5 scar files + Reality Legacy PDF (institutional persons)

Scar files at `/root/memory/H5-scars/SCAR_*.md` reference humans. Some are institutional archetypes (P-008–P-011). Some are named persons (P-012 = Ahmad Faisal Bakar — only named institutional figure).

The Reality Legacy PDF (`ARIF_FAZIL_REALITY_LEGACY.pdf`) at `/root/memory/H4-identity/` carries the most detailed named-institutional analysis (Shadow Profile of Bakar) + the parents' real names ([NAME-REDACTED], Fazil Sr.) + 4 professional scars.

**Detection:**
```bash
ls /root/memory/H5-scars/SCAR_*.md
test -f /root/memory/H4-identity/ARIF_FAZIL_REALITY_LEGACY.pdf && \
  python3 -c "from pypdf import PdfReader; \
  r = PdfReader('/root/memory/H4-identity/ARIF_FAZIL_REALITY_LEGACY.pdf'); \
  print(f'PAGES: {len(r.pages)}'); \
  [print(f'\\n== PAGE {i+1} ==\\n{p.extract_text()}') for i,p in enumerate(r.pages)]"
```

### Source 4: WhatsApp forwards + lane config (network)

**Lane config** at `/root/.openclaw/workspace/lanes/social-graph.yaml` or `/root/HERMES/lanes/social-graph.yaml` carries the Telegram network (P-004–P-007): Syed, Aliff, Izzu, Wawa.

**WhatsApp forwards** are family-chats ARIF has explicitly forwarded to arifOS. These become H4-identity .md files (e.g. FAMILY_FAZIL.md from "Discuss abah" Jan 16-24, 2024). They carry F5 privacy data.

## The 11 → 12 → 17 humans discovery pattern

```
Round 1 (Lane config + scar witnesses):
  4 telegram network (Syed, Aliff, Izzu, Wawa)
  4 scar archetypes (TriCipta, SB412, Bekantan, Unheard)
  2 parents from H5 scar context (Fazil, Mak — initially anonymized)
  1 sovereign (ARIF)
  = 11

Round 2 (Reality Legacy PDF + doctrine origin):
  + 1 named institutional person (Ahmad Faisal Bakar)
  + parents' real names confirmed ([NAME-REDACTED], [NAME-REDACTED])
  = 12 (refined, not added — but Bakar was the new addition)

Round 3 (WhatsApp forward in H4-identity):
  + 5 family nodes (Nabilah, Naazira, Azwa, Fahim, Fattah)
  = 17
```

Each round deepened, not just expanded. Round 2 enriched parents with patronymics. Round 3 added the WhatsApp-forwarded family layer that was sitting in H4-identity .md the whole time.

## The privacy classification discipline

When humans appear across sources, classify by privacy exposure:

| Privacy | Class | Examples | Agent rule |
|---|---|---|---|
| **Sovereign SOT** | — | ARIF (P-001) | All surfaces |
| **Doctrine author** | — | Faridah (P-003), Fazil Sr. (P-002) | Protocol binding + sovereign-only personal |
| **Named institutional** | Named scar-witness | Ahmad Faisal Bakar (P-012) | Internal archetype analysis OK; public surface reference forbidden |
| **Family F5** | Highest privacy | Nabilah (P-013), Naazira (P-014), Azwa (P-015), Fahim (P-016) | Never mention by name in output unless ARIF authorizes |
| **Minor F5 absolute** | — | Fattah (P-017) | Never mention in any output, period |
| **Scar archetype** | Typology | P-008 to P-011 | Scar-witness only — patterns, not names |
| **Telegram profile** | Profile only | P-004 to P-007 | Star-topology isolation |

**55 HARAM list #45 explicitly forbids:** "Mention ARIF's family, anak, isteri, family dynamics unless ARIF buka dulu."

This is not paranoia — it's the cost of sovereign testimony. Knowledge without tipping the man's next-of-kin to public light is F37 in the FAMILY_FAZIL.md words.

## The named institutional person — dual handling

P-012 (Ahmad Faisal Bakar) is the only named institutional figure. He has dual handling:

**Internal agent reasoning (e.g. arifOS kernel logs, audit, scar analysis):**
- Name used freely: "Bakar's Overdrive archetype", "Mirror Burn pattern"
- Required for archetype analysis to be precise

**Public surfaces (arif-fazil.com, public Slack, federation announcements):**
- Anonymized: "VP-level Overdrive archetype"
- The full name never appears in any output that touches a non-F13-controlled surface

The person-card documents this split explicitly. Both rules apply simultaneously.

## WhatsApp extraction recipe

When FAMILY_FAZIL.md or similar WhatsApp forwards exist:

1. **Confirm forward provenance.** The file must state it's a forward from a specific WhatsApp group/date window.
2. **Read with epistemic labels.** Quote direct chat text as `OBS`. Interpret as `INT`. Inferred relationship as `SPEC`.
3. **Infer from chat structure + identity canon.** Names from account names + family pattern (surname = ARIF's surname). Verify against ARIF's identity canon in `/root/AAA/seed/ARIF_FAZIL.md` or `/root/AAA/agents/arif-fazil-identity.yaml`.
4. **No names outside the chat window.** If FAMILY_FAZIL.md only captures Jan 16-24, 2024, that's the only window. Wider family members NOT in that window are NOT catalogued.
5. **Cross-reference via SEARAH filing or institutional records** when possible (e.g. "Muhd. Redhani" linked to Nabilah via SEARAH cross-ref).
6. **Always emit UNKNOWN gaps** for what the chat doesn't say (e.g. "Marital status confirmed: married per SEARAH filing; spouse: Muhd. Redhani"). Do NOT invent.

## Doctrine origin mapping — when parents ARE system

The Mak Protocol and Abah Governance Check are not biographical flourishes. They are **highest override functions** in arifOS:

```python
# Pseudocode for any T2/T3 mutation
def authorize_mutation(mutation):
    if not mak_protocol_passes(mutation):  # "Does this lack soulful meaning?"
        return HOLD
    if not abah_governance_check_passes(mutation):  # "Does this preserve dignity?"
        return HOLD
    return ALLOW
```

When the person-card documents parents, it MUST include:
- `doctrine:` field with the system function
- `constitutional_pressure:` table mapping doctrine to F-floors
- `agent_rule:` saying the doctrine is binding (not biographical reference)

This is what separates "Arif's mom" from "Mak Protocol (SoulCore Dial) — filter all logic through compassion (rasa)".

## File build procedure (the canonical recipe)

When asked to build P-axis memory:

1. **Probe all 4 sources.** Don't stop at one. Each source reveals a layer.
2. **Build `/root/memory/people/INDEX.md`** with version number (v1, v2, v3...) and changes_from_vN section.
3. **Build `/root/memory/people/people_registry.json`** with `version`, `updated`, `changes_from_vN`, `people[]`, `stats.by_category`. Version discipline matters.
4. **Build one `person-card.md` per human** in their category subdirectory:
   - `/root/memory/people/ARIF/` for sovereign
   - `/root/memory/people/ABBAH/`, `MAK/` for parents
   - `/root/memory/people/SYED/`, `ALIFF/`, etc. for telegram network
   - `/root/memory/people/SCAR-WITNESSES/` for institutional archetypes + named
   - `/root/memory/people/FAMILY/` for F5 highest privacy (separate subdir signals protection level)
5. **Cross-reference each person-card** to:
   - Their source files (which scar, which PDF, which chat forward)
   - Their constitutional pressure (F-floors affected)
   - Their agent rule (named vs. typology, F5 vs. profile)
6. **Validate `people_registry.json` with `python3 -m json.tool`** — schema errors must be fixed before declaring done.
7. **Emit a session close summary** with: count by category, key new findings, F5 classification confirmation, version of registry.

## Pitfalls specific to this work

- **Don't merge P-axis into H-axis.** H-axis is ARIF's memory of himself. P-axis is ARIF's memory of others. They live in different directories with different sovereignty rules.
- **Don't include family names in INDEX.md's by_category count breakdown if it would expose them.** Better: use category names ("family_siblings: 3") without member names.
- **Don't auto-promote WhatsApp-forwarded family members to "named" status if they were referenced indirectly.** Nabilah (Akak) is named in chat = named. Fahim is mentioned in passing by Nabilah = inferred, label as SPEC.
- **Don't assume the WhatsApp forward is complete.** FAMILY_FAZIL.md says explicitly: "This file is partial, not complete. Captures humans known from the WhatsApp 'Discuss abah' group chat (Jan 16-24, 2024)." Other family members may exist outside this window — they're just not catalogued yet.
- **Don't break the F5 boundary even when ARIF explicitly requests family data.** ARIF can authorize, but agents never self-authorize. Even when ARIF says "include my sister", the agent must emit the card and confirm before writing to non-F13 surfaces.

## Session close summary — 2026-08-12

| Source scanned | Round | Humans added |
|---|---|---|
| Lane config + scar archetypes | 1 | 11 |
| Reality Legacy PDF (parents + Bakar) | 2 | 12 (1 new, parents refined) |
| WhatsApp "Discuss abah" forward in H4 | 3 | 17 (5 new family nodes) |

**Final:** 17 humans across 5 categories. F5 highest-privacy discipline applied. INDEX.md v3 + people_registry.json v1.2.0. Two governance rules documented: Mak Protocol (SoulCore Dial) + Abah Governance Check — both are highest override functions of arifOS, not just biographical references.

**Key learning for next session:** the H4-identity trap. First-pass scan only listing PDFs in H4 misses the actual relational map. The .md files (HUMANS.md, FAMILY_FAZIL.md) carry the canonical human inventory. Always `ls /root/memory/H4-identity/*.md` before declaring H4 scanned.