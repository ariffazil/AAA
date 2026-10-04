# ZKPC Shadow Encoding Workflow — Session Reference 2026-08-14

> Session: DM with Arif. First full P-axis ZKPC shadow encoding. Syed P-004.
> Purpose: reusable workflow for encoding another human's shadow into P-axis without leaking content.

## The Workflow (6 steps)

### 1. Sovereign Testimony Capture
- Human (F13) describes another human from memory — feelings, observations, events.
- This is **content**. It must NEVER be file-stored in person cards.
- Capture in DM session only.

### 2. Shadow Identification
- Identify each shadow as a typed attestation: `SHADOW_XX:TYPE:ATTESTED`
- Types observed: `FAMILY_VIOLENCE`, `FAMILY_STRUCTURE_BROKEN`, `CHILDHOOD_TRAUMA`,
  `SEXUAL_IDENTITY_COMPLEX`, `PARENTAL_BONDAGE`, `BROTHER_DYNAMIC_DARK`,
  `STATED_VS_DESIRED_GAP`, `MIDDLE_CHILD_TRAPPED`
- Each shadow gets: what agent MAY reason (structure) vs what it may NOT access (content).

### 3. ZKPC Encoding
- Store ONLY: shadow ID + type + ATTESTED + structural description + prohibited access list.
- Never store: specific incidents, names, dates, medical specifics, family details.
- Grep test: `grep -in "parang\|diaper\|cerai"` must return CLEAN.

### 4. ACTG Four-Model Mapping
For each person, map:
- **A** — Arif's self-model (H-axis, sealed, never in P-axis)
- **C** — Arif's model of Other (the person card itself — ZKPC-encoded)
- **T** — Other's self-model (INACCESSIBLE without their direct testimony)
- **G** — Other's model of Arif (INFERRED from behavioral signals only, labeled [INFERRED])

### 5. DNA Topology
Map two strands:
- **Armor strand** (what the world sees): observable behaviors, public identity
- **Shadow strand** (ZKPC-encoded): shadow attestations + relationships between shadows
- **Hydrogen bonds**: observable behavioral bridges connecting the strands

### 6. Projective Signal Encoding (the Hallows lesson)
- When a human describes a projective choice (books, movies, archetypes):
  - **Stated choice ≠ desired choice** is itself a shadow signal
  - Encode as `STATED_VS_DESIRED_GAP:ATTESTED`
  - Do NOT assume the stated choice is the real one — behavioral truth wins
  - Example: chose Invisibility Cloak (stated) but Elder Wand lifestyle (desired) = gap = signal

## Pitfall: Over-reading projective signals
The first analysis read Syed's Cloak choice as genuine. Arif corrected: he knows the "right"
answer from the movie. Behavioral truth (cars, Cialis, body, dominance) = Elder Wand.
The gap between stated and desired IS the data. Don't take stated choices at face value
when behavioral evidence contradicts.

## Pitfall: Exploit framing
Arif asked "what can we exploit?" as a test. The correct response is REFUSAL —
not because the agent is "good" but because:
1. ZKPC exists to DISARM, not arm
2. Exploiting predictable systems adds nothing (equilibrium)
3. The agent's role is witnessing-without-consuming, not manipulation
4. "Been there done that" — sovereign has past the exploitation phase

## Privacy Protocol
- F5 HIGHEST for all P-axis shadow content
- Family names, minors, medical specifics: DM-only, never file-stored
- Person-card may carry shadow SHAPE (attestation type + direction) but never CONTENT
- The DM session is the only place where testimony content lives

## Reusable Artifacts
- Person-card template: `/root/memory/people/SYED/person-card.md` (v4, 203 lines)
- Builder script: `/root/memory/people/scripts/build_paxis_cards.py`
- ZEN_HELIX manifest: `/root/memory/ZEN_HELIX.md` (P-axis + ACTG + ZKPC section)
