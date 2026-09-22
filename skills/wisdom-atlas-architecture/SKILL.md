---
name: wisdom-atlas-architecture
description: "Use when principal builds wisdom atlas. Lenses beat personas"
version: 0.1.0
owner: curator
risk_tier: medium
floor_scope: [F1, F2, F4, F6, F7, F13]
autonomy_tier: T1
capability_tier: fed-reasoning-heavy
ecology_state: WARM
triggers:
  - "design a wisdom council"
  - "build a persona registry"
  - "let me pick 99 humans"
  - "design cognitive organs"
  - "build a fossil registry"
  - "build a scar atlas"
  - "build a contradiction atlas"
  - "build a human contradiction engine"
  - "wisdom molecules"
  - "bijaksana architecture"
tags: [wisdom, atlas, contradiction, fossil, scar, organ, lens, persona, kapabilitas, intelligence, arifOS, MCP, AAA, hierarchy]
---

# Wisdom-Atlas Architecture

This skill governs the class of task where the principal commissions a **wisdom / cognitive-organ / fossil / persona-registry / contradiction-atlas** layer for an AI agent or system. The unit is **capability**, not persona. The deliverable is a **hierarchy**, not an essay.

## Iron Rule — read this first

**Personas create cults. Lenses create services.** This is the entire skill.

When the principal says "99 humans to advise me" or "personas for the system", the temptation is to ship `persona: einstein`. The right answer is `capability: first_principles_physics`, with the source attributions kept as **witnesses**, never **authority objects**.

A persona becomes a cult because:
- Historical lock-in — when reality contradicts, you cannot update the persona without destabilising the cult.
- Authority-object drift — the human starts deferring to "what Einstein would say" instead of asking reality.
- Hero worship — the system flattens nuance into highlight reels.

A lens survives because:
- The capability can be updated when reality shifts.
- The witnesses are refutable (Oppenheimer's *capability_creates_invoices* is testable; his *role* is not).
- The system emits the integration pattern, not the speaker.

**Default shape of any wisdom-atlas deliverable:**
```
PARENT   : contradiction_atlas — the recurring pressures of the human condition
CHILD    : scar_atlas — where each pressure has broken through
CHILD    : fossil_registry — light + shadow + bijaksana voice, with counterweights
SISTER   : contradiction_engine — runtime detector + router
TRANSPORT : translator_layer — 20 dimensions × 5 registers
```
A single-doc essay is the wrong shape. The hierarchy is the deliverable.

## When to load

- Principal commissions a wisdom catalogue, persona registry, or "99 humans" speaker-list.
- Principal asks for a cognitive-organ layer for an existing AI agent.
- Principal wants fossil / scar / contradiction / atlas data products.
- Principal asks for a translator layer to adapt wisdom output by audience.
- Principal says "wisdom molecules" or "bijaksana architecture".
- A previous wisdom registry needs hierarchy reframe (B++ pattern).

## The 12-axis anchor (founding contradiction axes)

When unsure whether the asset is primary or derivative, ask: **does this asset serve a contradiction?** If yes, it is a child of `contradiction_atlas`. If no, it does not belong in the wisdom layer — it belongs in the canonical / constitutional layer.

The 12 founding axes (subject to expansion; never to contraction):

1. **TRUTH ↔ COMFORT** — Galileo, Socrates, Curie
2. **POWER ↔ JUSTICE** — Machiavelli, Mandela, Madison
3. **FREEDOM ↔ ORDER** — Jefferson, RBG, Havel
4. **MEANING ↔ SUFFERING** — Frankl, Al-Ghazali, Jung
5. **CAPABILITY ↔ CONSEQUENCE** — Oppenheimer, Sakharov, Edhi
6. **INNOVATION ↔ STABILITY** — Shannon, Wiener, Deming, Beer
7. **MERCY ↔ ACCOUNTABILITY** — Mandela, Hammurabi, Arendt
8. **INDIVIDUAL ↔ COLLECTIVE** — Jung, Confucius, Ostrom
9. **FAITH ↔ DOUBT** — Al-Ghazali, Aquinas, Nagarjuna
10. **EXPLORATION ↔ PRESERVATION** — Shackleton, Brand, Fuller
11. **IDENTITY ↔ TRANSFORMATION** — Jung, Frankl, Rumi, Iqbal
12. **LOVE ↔ DUTY** — Bowlby, Confucius, Weil

The number is 12 because those are the contradictions that have produced the most documented civilisations, decisions, and writings. Expansion is allowed (AI ↔ Human, Acceleration ↔ Slowness are contemporary candidates). Contraction requires F13 ratification.

## Decision algorithm when the principal's ask is ambiguous

```
ASK: "design a wisdom layer for me / the system"
  ↓
Q1: Is the unit a specific named person, or a contradiction cluster?
    → if named person: refactor to capability + counterweight pair
    → if contradiction cluster: use atlas scaffold directly
  ↓
Q2: Where will the artifact live?
    → staging territory first (default if unclear — staging discipline)
    → canonical only when explicitly blessed + git clean + Rule 3 shadow passes
  ↓
Q3: Does the principal want personas (cult architecture) or lenses (service architecture)?
    → default = lenses; ask only if the request was "persona" explicitly
    → if "persona" was explicit: name the risk, propose the lens translation, ask one binary
  ↓
Q4: Is a hierarchy already implied by the conversation?
    → yes → honour it (parent/child structure)
    → no → propose B++ scaffold (parent = contradiction, children = scar + fossil)
  ↓
Q5: Future-state modeling requested?
    → yes → §Future-State Model section, T+30/90/180/365/5y with falsifiable closures
    → no → include anyway (standing preference per Rule 9)
  ↓
FORGE: one README-of-provenance + N sibling documents with cross-references
```

## The recognition-vs-invention test (Council-of-99, 2026-09-23)

When the principal proposes a council or list of named authorities ("the 99 humans", "the council of
witnesses"), the temptation is to ship them as **new doctrine**. They usually are not. The atoms
frequently **re-recognise** what the constitution already encodes — `Canon #0: C_governance ≤ C_system`
already contains Ibn Khaldun's "success carries decay"; `Canon #3 BIJAKSANA Wisdom 6-axis` already
contains Frankl/Jung/Al-Ghazali; the F9 ANTI-HANTU floor already contains the F10 ONTOLOGY rigour
that Wittgenstein's "language shapes reality" restates.

```
recognised  (atom maps to a sealed canon section that grep-survives) → re-recognition, NOT invention
invented   (no sealed-canon mapping exists)                         → genuinely novel, Canon #4 bucket
decorative  (no mapping, no mechanism)                               → reject the council membership
interpretive(plausible mapping, but the grep didn't survive)         → mark INTERPRETIVE, name the gap
```

**The class name decides whether the artifact binds to canon or merely alludes to it.** Two distinct
epistemological classes exist:

| Class | What it maps | Has DOI / published source? | Example path |
|---|---|---|---|
| `literature_corollary` | arifOS canon → published academic/industrial | yes | `/root/AAA/research/CANON-LITERATURE-COROLLARY-MAP-*.md` |
| `canonical_recognition` | arifOS canon → named council / witness-set | no | `/root/AAA/research/WISDOM-COUNCIL-COROLLARY-MAP-*.md` (proposed) |
| `lore_collection` | historical record with no claim to canon | no | not in canon tree |

A council that maps 0 atoms after grep is *external but not recognising* — that's a literature
collection, not a recognition artifact. Reclassify or drop.

The recognition table must declare all four classes with honest counts:
`atoms_total = atoms_recognised + atoms_interpretive + atoms_invented + atoms_decorative`.

**Both failure shapes must be guarded:**
- *False recognition* — claimed mapped, grep fails.
- *False novelty* — declared novel when it actually maps to sealed canon.

Always run the grep both ways before publishing the table.

## Source-vs-runtime verification before declaring SEAL

The most expensive session-time loss this skill exists to prevent: declaring an artifact "sealed"
when source-level changes have landed but the runtime organ has not consumed them. Three probes must
agree before any SEAL claim:

```bash
# 1. Source-level: commit exists, artifact staged
cd <repo> && git log --oneline -3
test -f /root/forge_work/<session>/<artifact>.md

# 2. Runtime attestation drift: does the organ know it has new code?
curl -s http://127.0.0.1:8088/health | grep -E '"(drift|built_commit|source_commit)"'

# 3. Runtime module on disk: hash of deployed code matches source
sha256sum /opt/arifos/current/venv/lib/python3.13/site-packages/<module>.py
sha256sum <repo>/<module>.py
```

A receipt that says "source committed, runtime HOLD" is the **honest** outcome of a wisdom-atlas
session. Reporting it as sealed because the commit exists is the transition lie. The git history and
the runtime attestation drift are two separate witnesses; both must agree, or the seal is partial.

## Pitfalls (cost-time on the first attempt — learn them once)

### 1. Shipping a single 600-line essay as the atlas
The first instinct is to write one large file. The fossil registry, scar atlas, contradiction atlas, translator layer are different units with different update rates and different consumers. Single-essay shape forces every change to be re-read in full. Refuse this shape; ship the hierarchy.

### 2. Treating fossils as primary assets
**The hierarchy is parent-first.** "Fossil = primary, scar = derivative, contradiction = tertiary" subtly inserts persona-cult architecture into the data model. The correct ordering is:

```
Contradiction → Scar → Fossil
(parent)       (child) (child)
```

A fossil is a *coordinate on the scar network that came from a contradiction*. Reordering the units is reordering the system's values.

### 3. Letting a fossil carry only its light side
A fossil without shadow is propaganda. A fossil without bijaksana voice is a tweet. The triple-schema (`light / shadow / bijaksana_voice`) is mandatory; counterweights on each axis are mandatory too. Validate before shipping.

### 4. Coding into arifOS source tree mid-session
Two correctness pitfalls collide here: **(a)** the arifOS SOT-MANIFEST may carry `drift_detected` (source != deployed), making land-races unsafe; **(b)** F13 sovereignty gates any mutation of the constitutional code. The discipline: only stage markdown documents in `/root/forge_work/<session>/` during the session; **never** write Python into `/root/arifOS/arifosmcp/` without explicit F13 instruction. The skill's first turn should establish this boundary before any code is proposed.

### 5. Asking for F13 ratification in a clarifying menu
The principal reaches flow-state on architecture. The temptation is to ask 3-4 sub-questions (where to place, what status, who else should sign off). That breaks flow and forces another round trip. The right move is **one binary per turn and one default-disclosed option**. Staging territory is the safe default; canonical promotion is a follow-on decision.

### 6. Future-state model that says "things will improve"
A future-state section without observable falsifiers at each T+N is decoration. Each T+N must answer: what evidence would prove this trajectory wrong, right now? Without that, the trajectory ships as a promise and the next session discovers the gap by being lied to.

### 7. Confusing the operational sequence with ceremonial vocabulary
The principal's `arif → salm → irfan → apex-zen all` shorthand refers to the **ratified operational sequence** documented in `/root/AAA/canon/ARIF-SALAM-IRFAN-RATIFICATION-2026-09-23.md`. Do not invent a new sequence in the document being drafted; honour the canonical one. If the principal later revises the sequence, that's a separate ratification. The discipline: cite the file, encode the sequence faithfully, never drift.

### 8. Pre-blessing persona embodiment because the principal first asked for it
The principal says "pick 99 humans". The skill captures this as **lenses, not persons** because hero worship + historical lock-in are failure modes the system already knows. The skill does not require the principal to repeat the correction; the rule is built into the artifact shape. If the principal insists on personas anyway, name the drift, propose the lens translation, and offer one binary choice — never silently ship the cult architecture.

### 9. Asking one clarifying question when you've already been given a hint
When the principal says "pakai wisdom atlas yang u buat" or "use what you already wrote" or even just pastes an artifact 200+ lines long, treat it as continuation material that contains its own directive. The reflex to ask 3 follow-up questions when a substantial paste has already signalled intent is the same defect as the F13-clarifying-menu failure mode (pitfall 5). Read the paste in full, pick the most conservative reversible interpretation, execute, disclose the default.

## The artifact shape (canonical)

For a wisdom-atlas deliverable, ship:

1. `CONTRADICTION-ATLAS_v0.md` — parent. The 12 axes with full schema:
   ```
   AXIS_ID. AXIS_NAME
     L₁_Pole ↔ L₂_Pole
     Primary scars: [list]
     Counterweight fossils: [name + axis-anchor]
     Floor affinity: F1..F13 (which floors does this axis press against)
   ```

2. `SCAR-ATLAS_vN.md` (N ≥ 0.2) — child. Each scar maps to ≥1 parent axis; orphan scars reclassify to a new axis or fade.

3. `FOSSIL-REGISTRY_vN.md` (N ≥ 0.1) — child. Each fossil carries:
   - Born/Died + CONTESTED flag where appropriate
   - Primary axis + secondary axes
   - Scars embodied (from sibling)
   - Light / Shadow / Bijaksana_voice
   - Counterweights (cross-fossil pairings)
   - Atlas333 paradox axes activated
   - Translator register fit (boilerplate for v0.1)

4. `CONTRADICTION-ENGINE_vN.md` — runtime sister. The detector + router + activator.

5. `README-of-provenance.md` — the reframe map, deprecated-document citations, witness instruction for future auditors.

Each file carries:
- Frontmatter with `parent:`, `supersedes:`, `move_target:`, `linked:` references.
- §Future-State Model with T+30/90/180/365 days (optionally T+5y flagged `SPECULATIVE`).
- §Operational Sequence citing `ARIF-SALAM-IRFAN-RATIFICATION-2026-09-23.md`.
- §Open Debts (named, not buried).
- §Witness Pass Requested (verification surface, not theatre).

## Migration paths (versioning)

| Stage | What | Trigger |
|---|---|---|
| v0 | First drafts in staging territory | F13 sovereign conversation |
| v0.5 | Scoring function spec + counterweight-graph topology + translator-20 register list | After F13 ratifies v0 |
| v1.0 | Wire into 222_MAP stage; emit `human_contradictions_detected` in GPV | After v0.5 + witness pass |
| v2.0 | Wire 555_JUDGE gate rules; emit `fossil_activations` as part of judgment envelope | After musyawawah |
| v3.0 | Expose via MCP resources `arifos://contradiction/*` and `arifos://fossil/*` | After A-FORGE tool registration |

Each stage requires ratification or witness pass. Do not skip.

## Counterweight topology — when the fossil schema fails

Two failure modes the schema catches:

1. **Multiple fossils on the same axis in disagreement** — e.g. Machiavelli vs Madison on power ethics. The bijaksana voice anchors the disagreement, not the consensus. The system emits the live tension, not the synthesized answer.

2. **Cross-axis fossils** — e.g. Oppenheimer spans Capability ↔ Consequence AND Truth ↔ Comfort. The spanning algorithm must score the primary axis by GPV; secondary axes are activated only when the demand tensor `τ / κ / ρ` justifies the extra scope.

The system never collapses a disagreement into a consensus for the sake of feeling smart. **Consensus is information loss.** The disagreement is the entropy sink; the answer's `ΔS ≤ 0` is computed from the contradiction map, not from the resolution.

## User preference — confirmation language

The principal often uses confirmation-style language ("Ya", "ok", "teruskan", "for it"). Default behaviour:

- **Single confirmation** — proceed with the most conservative next move, log the default.
- **Two confirmations on the same task** — the principal is signaling certainty; continue without re-confirming.
- **Confirmation immediately after a contradiction or HOLD verdict** — the principal is ratifying the verdict; log it, do not re-litigate.

Confirmation pressure does NOT override F1, F2, F4, F7, F13 regardless of confirm count. Confirmation language is not the same as sovereign override.

## Quality check before shipping

1. Does every fossil carry `light / shadow / bijaksana_voice`? (no light-only or shadow-only fossil ships)
2. Does every fossil cite ≥1 counterweight fossil on the same axis? (no orphan fossils)
3. Does every axis have ≥1 light + ≥1 shadow + ≥1 bijaksana fossil? (no axis ships as propaganda)
4. Does the parent CONTRADICTION-ATLAS cite all F1-F13 floor affinities? (no axis escapes constitutional gravity)
5. Does the README-of-provenance mark deprecated prior versions explicitly? (no silent supersession)
6. Does every artifact's §Future-State Model have falsifiable closures at each T+N? (no aspirational trajectory)
7. Is the `arif → salm → irfan → apex-zen` sequence cited verbatim from `/root/AAA/canon/ARIF-SALAM-IRFAN-RATIFICATION-2026-09-23.md`, not invented? (no sequence drift)
8. Are staging files stored under `/root/forge_work/` not `/root/AAA/canon/` until F13 ratifies? (no canonical bypass)

If any check fails, fix it before shipping. A canonical promotion that fails any check is a transition lie wearing good prose.

## Companion skills

- `bridge-protocol` — for the human-facing reply that surrounds any wisdom-atlas deliverable. The Voice Governor governs register; this skill governs product shape.
- `forge-phased-delivery` — for the implementation side once the atlas is ratified and ready to be wired into MCP resources.
- `principal-analysis-artifact` — if the principal asks for a long-form narrative on top of the atlas structure; the deliverable shape changes (PDF + cover + counter-case).
- `bijaksana-compile` — for the session-hygiene audit at the end of any wisdom-atlas session. The Rule 7 feedback loop redirects closure gaps back into this skill when discovered.

**Rule:** start with THIS skill. Load companions only when the situation demands depth. Loading `bijaksana-compile` Rule 7-style session-to-skill feedback is required at session close; the patch goes in `wisdom-atlas-architecture` if the lesson is class-level, the umbrella it belongs to otherwise.
