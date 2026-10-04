# ZKPC Person-Card Encoding Workflow (2026-08-14)

> When a sovereign reveals shadow content about another human, encode STRUCTURE without CONTENT.
> This reference documents the actual technique used on Syed P-004 v4.

## The problem

Arif revealed deep shadow content about Syed (family violence, brother dynamics, 
sexual complexity). The agent needs to REASON from this knowledge in future 
interactions without STORING the raw content in any file. Standard memory 
storage = data leak risk across surfaces.

## The technique — ZKPC shadow attestation

For each shadow domain, create a table row:

```
| SYED_SHADOW_XX | TYPE:ATTESTED | What agent may reason | What agent may NOT access |
```

**Encoding rules:**
1. The TYPE field names the category (FAMILY_VIOLENCE, SEXUAL_IDENTITY_COMPLEX, etc.)
2. "What agent may reason" = structural observation (e.g., "armor thickness inversely 
   correlates with confidence")
3. "What agent may NOT access" = the specific content (names, incidents, dates)
4. The content lives ONLY in the DM session transcript — never file-stored
5. F5 privacy enforced: family names, minors, medical specifics never leave DM

## Shadow types observed in practice

| Shadow type | Signal pattern | Encoding |
|---|---|---|
| `FAMILY_VIOLENCE` | Identification with aggressor; anger = inverted care | May track behavioral correlates |
| `FAMILY_STRUCTURE_BROKEN` | Multiple family failures | May note structural dysfunction |
| `CHILDHOOD_TRAUMA` | Repressed memories; some parties remember, some don't | May note asymmetry exists |
| `SEXUAL_IDENTITY_COMPLEX` | Performance armor exceeds security needs; boundary crossing causes retreat | May note armor-to-security ratio |
| `PARENTAL_BONDAGE` | Compulsive caretaking; resentment risk | May track care-to-energy ratio |
| `BROTHER_DYNAMIC_DARK` | Flinch when sibling sexuality questioned | May note mirror/parallel patterns |
| `STATED_VS_DESIRED_GAP` | Knows "right" answer but doesn't live it | May track stated vs behavioral choices |

## Projective signal patterns (bonus technique)

Recreational media choices can serve as accidental projective tests:

**Deathly Hallows projection:**
- Elder Wand = wants power, control, dominance (often compensating for past loss)
- Invisibility Cloak = wants safety through non-detection (often genuinely cautious)
- Resurrection Stone = wants to bring back what's gone (unprocessed grief)
- KEY SIGNAL: the GAP between stated choice and behavioral truth. Someone who 
  says "Cloak" but lives "Wand" has an unresolved tension between aspiration 
  and drive. That gap IS a shadow.

**Rule:** Projective signals are always [INT] — agent interpretation, not [OBS]. 
Encode the structural observation, not the raw content of the revelation.

## Verification after encoding

```bash
# Shadow content must NEVER appear in the person card file
grep -in "parang\|diaper\|specific_incident\|real_name" /root/memory/people/NAME/person-card.md
# Expected: CLEAN
```

## DNA topology section

After encoding shadows, add a topology map to the person card showing:
- Armor strand (what the world sees)
- Shadow strand (ZKPC-encoded attestations)
- Hydrogen bonds (observable behavioral bridges between armor and shadow)
- One-line zen synthesis

This makes the card both machine-readable (attestations) and human-readable (topology).
