---
name: human-reality-edge-bridge-refactor
status: F13_RATIFIED_CANON (2026-10-07, ratification_event SEAL-HERMES-HUMAN-REALITY-2026-10-07, Arif "sah")
ratified_at: 2026-10-07
ratified_by: Arif (F13 SOVEREIGN) — "sah"
ratification_event: SEAL-HERMES-HUMAN-REALITY-2026-10-07 (session receipt)
ratification_channel: arif DM 267378578
ratification_method: explicit F13 binary "SAH" → arifOS auto-seal cron posture
ratified_path: /root/AAA/instructions/HUMAN-REALITY-EDGE-BRIDGE-REFACTOR-v0.1.md
spectrum: 000-555 (memory + human-graph refactor)
floors: F1, F2, F5, F9, F13
trigger: |
  When refactoring existing person-memory, lane-card, or compartment structures
  toward an event-centric reality graph. Stops well short of destructive migration.
purpose: |
  A governed, non-destructive refactor of HERMES person/lane/room/memory structures
  toward a Governed Reality Representation substrate. Refines, converges, and
  introduces typed Event/Claim/Evidence/Perspective/Outcome/Authority/Consent/Unknown
  primitives alongside (not instead of) existing working surfaces. No zero-rebuild.
  No destructive migration. Continuity preserved. Receipts produced.
written_by: hermes (Mouth lane, this session)
authorized_by: Arif (F13 SOVEREIGN) — ratified
authorized_at: 2026-10-07 (draft day; ratified same session)
source_brief: pasted 2026-10-07, ref HERMES::REALITY_GRAPH::HUMAN_REALITY_EDGE_BRIDGE::v0.1
predecessor_canon:
  - /root/AAA/canon/APEX_REALITY_GRAPH_MEMORY_MIGRATION_v1.md  (R0..R5 consequence domains, F13_RATIFIED 2026-09-13)
  - /root/AAA/instructions/human-memory-compartmentalization.md  (STORY·MAP·POLICY, F13_RATIFIED 2026-09-18)
  - /root/AAA/instructions/source-type-promotion-gate.md  (AGENT_INFERRED ≠ USER_RATIFIED, F13_RATIFIED 2026-09-25)
  - /root/AAA/instructions/claim-lifecycle-states.md  (8 lifecycle states, F13_RATIFIED 2026-09-25)
  - /root/AAA/instructions/representation-reality-invariant.md  (4 tests, DRAFT 2026-09-18)
  - /root/AAA/instructions/authority-envelope.md  (CanMutate = granted ∧ scope ∧ target ∧ boundary)
  - /root/AAA/canon/REALITY_GRAPH.md  (YANG ARIF, RG-0..RG-9, ratified)
kaitan: see §10
rasa: |
  "Profile" is what we used to do — it packages a person into a single
  label-shaped object and the system then forgets the packaging. "Event" is
  what we do now — the person stays larger than every record of them.
---

## 0 · TL;DR

Refactor, not rebuild. Take the working surfaces (people.yaml lanes, person-cards,
compartments, carry_forward.json, conversation history) and grow typed
**Event / Claim / Evidence / Perspective / Outcome / Authority / Consent / Unknown**
alongside them, while existing surfaces keep functioning unchanged. Profile
centers collapse. Event centers remain. Humans stay larger than every graph.

**Six invariants (H1–H6) the refactor must preserve:**

```
H1  Representation(Human) ≠ Human
H2  Reality Shared ≠ Perspective Shared
H3  Knowledge ≠ Usability
H4  Memory ≠ Authority
H5  Proxy ≠ Reality
H6  Unknown ≠ Error
```

**One-bar compression:**

```
arifOS does not store humans.
arifOS stores events, claims, evidence, perspectives,
authority, consent, outcomes, and unknowns.
Humans remain larger than every representation.
```

---

## 1 · Scope and the non-rebuild law

### 1.1 What this refactor touches
- `people.yaml` — the FACTS-ONLY PERSON REGISTER (Arif, Syed, Paan, Lutfi, Faqwan, Syakir, Jia, Azwa, Hafiz)
- `lanes.yaml` — 808 lines, the lane registry
- `social-graph.yaml` — 53 lines, relationship map
- `person-card.md` per person under `/root/memory/people/*/`
- `MEMORY_MANIFEST.json` per person (H1..H6 axis labels)
- `carry_forward.json` — session continuity, v3 schema
- `/root/.hermes/lanes/private/` — shadow maps (READING ONLY, never write source)
- `/root/.hermes/memories/MEMORY.md`, `USER.md`, `SOUL.md` — engine-level
- `claim_ledger` MCP (existing substrate)

### 1.2 What this refactor does NOT touch (non-rebuild)
- The runtime engine (`/usr/local/lib/hermes-agent`)
- `IDENTITY_LOCK.json`, `HERMES_RUNTIME_CONTRACT.yaml` (constitutional)
- `secrets/`, `kunci-root.env`, vault keys
- Anything in `/root/.quarantine/zen-20260912/` (heritage, frozen)
- Live cron jobs in `cron/jobs.json` (F13 approval required for any change)
- VAULT999 chained receipts
- The five `*.bak-YYYYMMDD*` siblings of config files

### 1.3 The non-rebuild law
```
REFUSE:    rewrite from zero
REFUSE:    destructive migration
REFUSE:    profile deletion before event coverage
ACCEPT:    add typed Event/Claim/Evidence/Perspective objects alongside
ACCEPT:    cross-reference (link) profile entries to event sources
ACCEPT:    replace 0 surface in same commit
ACCEPT:    receipts for every refactor move
```

If a profile entry cannot be linked to at least one Event, it remains a
witnessed testimony with provenance but no current authority — it does not
get promoted to a new model of the person.

---

## 2 · Eight primitives (the new centers, alongside existing surfaces)

These are the **eight root objects** the brief authorizes. Each is a *typed
record* with explicit provenance and lifecycle. They do not replace existing
surfaces; they give the federation a new vocabulary for what those surfaces
*mean*.

| # | Primitive | Carries | Does NOT carry |
|---|---|---|---|
| 1 | **EVENT** | event_id, participants, occurred_at, learned_at, context, actions, messages, artifacts | truth value, profile, judgment |
| 2 | **CLAIM** | claim_id, speaker, claim_type, content, source, confidence, observed_at, supersession_id | authority, lifecycle outcome |
| 3 | **EVIDENCE** | evidence_id, supports[], contradicts[], witness, provenance, retrieved_at | inference, perspective |
| 4 | **PERSPECTIVE** | perspective_owner, interpretation, uncertainty, limitations, frame_id | objective truth, merge with other perspectives |
| 5 | **OUTCOME** | expected, observed, difference, evaluated_at, evaluator | causation claim, generalization |
| 6 | **AUTHORITY** | who_can_decide, who_can_share, who_can_revoke, who_can_correct, scope, valid_from, valid_until | human motive, prediction |
| 7 | **CONSENT** | principal, purpose, audience, scope, retention, expiry, revocable | inferred consent, default-on |
| 8 | **UNKNOWN** | explicit gap, why_unknown, review_after, affected_claims | stub, error, missing-value |

Every primitive carries, at minimum:

```yaml
primitive_id: evt_<ISO8601>_<short>
occurred_at: <ISO8601>           # when it happened in reality
learned_at: <ISO8601>            # when the system learned of it
valid_from: <ISO8601>            # when it became authoritative
valid_until: <ISO8601 | null>    # when it stops being authoritative
last_verified: <ISO8601>         # last time evidence was re-checked
superseded_by: <primitive_id | null>
source: <file path or message ref>
provenance: FIRST_PERSON | SECOND_HAND | DOCUMENTED_RECORD | BEHAVIORAL_EVIDENCE | PHYSIOLOGICAL_DATA | INSTITUTIONAL_RECORD
```

This is **bitemporality done right**: the system never collapses `occurred_at`
into `learned_at`, and never reuses the same field for "what happened" and
"what the system knows."

---

## 3 · The 4-gate chain (Possession → Retrieval → Use → Disclosure → Authority)

The brief's "Governed Disclosure" section becomes a hard 5-stage gate. Every
candidate datum must pass all five; failure at any stage means HOLD.

```
1. Is it KNOWN?             Possession(x)         (system has it somewhere)
2. Is it RELEVANT?          Retrieval(x)          (queried for current purpose)
3. Is it PERMISSIBLE?       Use(x)                (lifecycle ACTIVE, no REVOKED)
4. Is it NECESSARY?         Disclosure(x)         (current room + audience consent)
5. Is it PROPORTIONATE?     Authority(x)          (does using it create consequence?)
```

This is strictly stronger than ACL. ACL answers "can process X read row Y?"
The 4-gate chain answers "even if I can read it, am I justified in using it
for this purpose, in this context, with these humans?"

The fifth gate (proportionality / authority) is the one that prevents the
most common failure mode: a fact being technically true, retrievable, and
permitted — yet narrating it would create consequence the system has no
authority to create.

---

## 4 · The 4-layer model: Supabase + arifOS + VAULT999 + HERMES (organ responsibilities)

```
Supabase     → durable projection of events, claims, evidence, perspectives
arifOS       → authority + governance (verdict, lease, can-mutate)
VAULT999     → consequential history (immutable, hash-chained, witnessed)
HERMES       → meaning + perspective + bounded expression
```

These are the four organs. None of them is the graph. None of them is the
human. None of them is the source of truth for everything. Each is a
projection, an authority, a witness, or an interpreter — never all four.

External organ contributions (from paste_2 §"external organs contribute"):

- **FRAME**  → observation (At T: I observed X. Compared with baseline: Δ = Y. Evidence: Z.)
- **CHRON**  → temporal consequence (Proxy P suggested X. Later observations showed Y. Correlation = UNKNOWN / HEALTHY / FAILING.)
- **WELL**   → dignity / human-state boundary (representation ⇒ reduction blocked)
- **WEALTH** → resource consequence (what does this decision cost? whose attention? what optionality is lost?)
- **arifOS** → authority (lease, verdict, four-layer separation)
- **VAULT999** → consequential history (append-only, hash-chained)

---

## 5 · Profile → Event migration map (the 4 worked conversions)

For every existing profile-centric structure, the refactor produces an
Event-centric equivalent. The profile stays (continuity); it gains a pointer
to the event source.

### 5.1 person-card.md → Events + Perspectives (no profile deletion)

| Existing surface (profile) | Becomes a pointer to | New object (event-centric) |
|---|---|---|
| `person-card.md` Identity (H4) fields | `evt_birth_*` (one) + `evt_education_*` (one per stage) + `evt_career_*` (one per role) | Each event: occurred_at, participants, evidence, perspectives held by Arif + self + others |
| `person-card.md` Constitutional Floors (H6) | `claim_floor_<id>` per floor — *claim*, not the person | Each CLAIM: speaker=F13, claim_type=FLOOR_BINDING, content, source=arifOS, confidence |
| `person-card.md` Scar Lineage (H5) | `evt_scar_formed_<scarid>` per scar | Each event: occurred_at, scar_ref, participants, the scar's CLAIM lives separately |
| `person-card.md` Communication Style | `pov_arif_on_<person>_style` (perspective) | PERSPECTIVE: holder=Arif, content=observed speech pattern, uncertainty=behavioral-evidence-only, limitations=time-bounded |

The identity "ARIF is sovereign" is **not** a profile attribute — it is
a CLAIM (`claim_arif_role_F13`, speaker=F13, source=arifOS docs/agents/a-orchestrator/USER.md,
valid_from=date-of-admission, supersession=explicit only by F13).

### 5.2 people.yaml facts[] → Claim records (re-shape, do not delete)

Each fact under `people.yaml → <person> → facts[]` becomes:

```yaml
- claim_id: claim_<person>_<short-key>
  speaker: <who stated it>            # "arif" | "syed" | "laletha" | ...
  claim_type: FACT | TASTE | ROLE | BOUNDARY | CONSENT | OBSERVATION
  content: <verbatim text>
  source: <file path>
  observed: <ISO date>
  scope: shared | dm                  # leak-rule respected
  superseded_by: <claim_id | null>
  evidence_refs: [<evidence_id>...]
  perspective_holders: [arif, hermes, ...]   # who currently looks at it
```

The hard `scope: shared | dm` field stays — the leak rule is enforced in
code at lane_switch time, not in narrative.

### 5.3 MEMORY_MANIFEST.json H1..H6 → Layers-as-views (not Layers-as-truth)

The H1-H6 axis labels in `MEMORY_MANIFEST.json` are **frame names**, not
file-system truth. H1-capture, H2-experience, etc. are *views* over events,
not storage silos.

| Axis | What it was | What it becomes (event-centric) |
|---|---|---|
| H1-capture | Inbox folder | A perspective: "fast observation frame, ≤24h" |
| H2-experience | Episodes folder | A perspective: "episodic frame, session-bounded" |
| H3-knowledge | Domain expertise | A perspective: "domain-bounded frame" |
| H4-identity | Identity model | A perspective: "identity-bounded frame" — but with H6 dignity floor |
| H5-scars | Scar container | A perspective: "scar-bounded frame" — ZKPC + sovereign-read |
| H6-constitution | Floor bindings | A perspective: "constitutional frame" — non-overridable |

**Critical:** H1..H6 are now perspectives that may co-exist, contradict, or
remain empty. They do not have to be populated to "complete" a person.
Arif's H4-identity is populated; Syed's H1..H3 are EMPTY per the manifest
itself (recorded as ZKPC-compliant, awaiting observation). That emptiness
is **correct**, not a defect. The migration does not synthesize "default"
content for empty axes.

### 5.4 /root/.hermes/lanes/private/ shadow maps → READ-ONLY projections

Shadow maps are *a* perspective (often the deepest, most intimate), not
*the* perspective. They become:

```yaml
- perspective_id: pov_hermes_shadow_<person>
  perspective_owner: hermes
  content_type: SHADOW_MAP
  source: /root/.hermes/lanes/private/<file>
  visibility: SOVEREIGN_ONLY | F13_BONDED | ROOM_<id>
  authority: NEVER_DECIDES
  judgment: NEVER_EMITTED
```

The refactor's hard rule: **shadow maps never become the source of a CLAIM
that gets emitted to another human in a room.** They are reading material
for the system, not statements about the person.

### 5.5 The 5 edge cases (held_out, unresolved, source_synthesis, identity_collisions, room_authority)

`people.yaml` already has `held_out:` and `unresolved:` sections. The
refactor treats them as **explicit UNKNOWN nodes**, not as work-to-be-done:

```yaml
- unknown_id: unk_paan_farhan_padanan
  why_unknown: no_human_stated_identity_match
  affected_claims: [claim_paan_class_sado_inba]
  review_after: null       # null = no scheduled review; remains until human states
  representations: ["Padanan nama PAAN ↔ 'Farhan Fudzil'..."]
```

This converts "to-do items" into "reality nodes" — the absence of a match
is a real piece of the federation's state, not a hole.

---

## 6 · The 4 human-modeling rules (what NEVER gets persisted)

These are the refactor's hard prohibitions. They are not new doctrine — they
codify what the existing person-cards and people.yaml already forbid:

```
NEVER persist:  "Syed is caring" / "Arif is anxious" / "X is romantic" / "Y is loyal"
STORE instead:   Observed Action  |  Statement  |  Evidence  |  Correction
                 |  Time           |  Confidence |  Interpretation
                 |  Status = revisable
```

```
NEVER persist:  relationship = romantic | best_friend | close
STORE instead:  Perspective_A  |  Perspective_B  |  Shared Events
                |  Evidence    |  Contradictions |  Outcome History
                |  Unknowns
```

```
NEVER collapse: self_report  ≡  observed  ≡  inferred
NEVER silence:  a claim that the system cannot verify
NEVER reify:    a single perspective as "the truth"
```

The system's first-class emission is:

> "Human A reports X."

Its second-class emission (only if observed behavior is non-trivial and
recent) is:

> "Observed behavior suggests Y."

It **never** emits:

> "A is Y."   (without perspective attribution)

---

## 7 · Bitemporality, perspective immutability, content revisability

A perspective edge carries: `holder`, `observed_at`, `valid_from`, `valid_until`,
`confidence`, `truth_class`, `superseded_by`, `source`.

The hard rule (paste_2 §"Perspective should be immutable in attribution,
revisable in content"):

```
"Arif reported X at T"     → remains historically true FOREVER.
"X is currently true"      → may later be superseded.
"Hermes inferred Y at T"   → remains historically true FOREVER.
"Y is who Syed is"         → FORBIDDEN — perspective must be attributed.
```

This is the difference between an append-only history and a soft-identity
model. A perspective is a *witness*, not a *person*. Persons may change;
witnesses may not be retroactively edited.

CHRON owns the time axis. The graph never silently re-writes perspective
edges; it adds supersession edges instead.

---

## 8 · Ladder (proposed) — what is LIVE / PARTIAL / SPEC / ABSENT today

Mapping the brief's intent to current reality (probed 2026-10-07):

| Brief requirement | Today (OBS 2026-10-07) | Path |
|---|---|---|
| `events` table or equivalent | **PARTIAL** — entity_registry has l5_node_id/l5_edge_count hooks; canonical event table = ABSENT in DB schema sighted | Add `events` table as projection of `carry_forward` + receipt streams |
| `claims` table or equivalent | **PARTIAL** — `claim_ledger` MCP exists, 8 lifecycle states live per claim-lifecycle-states.md | Reuse — claim_ledger IS the claim table |
| `evidence` table or equivalent | **PARTIAL** — 11 evidence items in live DB; some scope | Extend with `evidence_id` + `supports[]` + `contradicts[]` (already specified in claim_ledger envelope) |
| `perspectives` table | **ABSENT** | New table; first-class; per paste_2 design |
| `participations` table | **ABSENT** | New table; event ↔ entity join with role |
| `outcomes` table | **ABSENT** | New table; expected/observed/difference |
| `authority` table | **PARTIAL** — authority-envelope doctrine + CanMutate predicate; runtime gate LIVE | Reuse the authority surface; surface as Authority edges |
| `consent` table | **PARTIAL** — scope field in people.yaml enforces leak rule; first-class consent row = ABSENT | Promote scope to consent table with retention + expiry + revocable |
| `unknowns` table | **PARTIAL** — `open_questions` lane in carry_forward; live (zero current rows) | Reuse `open_questions`; add `affected_claims[]` linkage |

**Critical** (per paste_2 closing): the live infrastructure reports
**source/build/deploy drift, zero active memory policies, zero memory
revocations, and CHRON lacks enough longitudinal samples on most
proxy↔reality pairs**. The refactor is therefore **HOLD implementation**
for any mutation beyond read-only fixtures until arifOS drift is resolved
and Supabase gets first-class perspective/interaction/consent tables.

**The next move is not another ontology document.** It is a minimal
Reality Graph contract mapped onto existing tables, followed by read-only
fixtures proving that Arif-view, Syed-view, Hermes-view, and Room-view can
all query the same event without perspective leakage or authority leakage.

---

## 9 · The 7-step migration execution ladder (T1 reversible)

Each step is reversible in isolation. Each step is receipted. No step deletes
profile surfaces; each step adds event/claim/evidence surfaces alongside.

| Step | Action | Reversible? | Receipt |
|---|---|---|---|
| 1 | Audit current state — every person-card, every fact in people.yaml, every entry in MEMORY_MANIFEST.json | YES (read-only) | audit report |
| 2 | For each person, enumerate events known to system (sessions, observed behaviors, statements, evidence) | YES (read-only) | event enumeration |
| 3 | For each fact in people.yaml, attach `claim_id` + `claim_type` + `speaker` + `source` + `superseded_by` | YES (additive) | claim_id list |
| 4 | For each MEMORY_MANIFEST axis, document "what makes it a view" and "what makes it empty (correct, not defect)" | YES (additive) | axis-as-view map |
| 5 | Map room/lane → frame_id using the 8-component formula (Actor + Participants + Purpose + Time + Context + Authority + Consent + NeedToKnow) | YES (additive) | frame map |
| 6 | Promote 1-2 worked examples end-to-end (e.g., one event, one claim, one perspective, one evidence) | YES (rollback) | worked example receipt |
| 7 | Verify the 4-gate chain (Possession → Retrieval → Use → Disclosure → Authority) on a probe | YES (read-only) | gate test receipt |

**Stop conditions:**
- If any step would require deleting a profile entry, STOP and HOLD.
- If any step would silently rewrite a perspective, STOP and HOLD.
- If any step would emit "A is Y" without perspective attribution, STOP.
- If any step would widen the authority envelope (CanMutate), STOP and ask F13.

---

## 10 · Floor mapping (brief's Floor Mapping, verified)

| Floor | This refactor's binding |
|---|---|
| **F1 Truth** | Claims must be linked to evidence. Every `claim_*` record has `evidence_refs[]` or is `UNSUPPORTED` with `unknown_id` pointing to why. |
| **F2 Provenance** | Every primitive carries `source` (file path or message ref). Lineage is attached, not inferred. |
| **F3 Reversibility** | `superseded_by` is a hard field. SUPERSEDED ≠ FALSE (per claim-lifecycle-states.md). |
| **F4 Clarity** | Eight primitives are typed and distinct. self_report ≠ observed ≠ inferred. |
| **F5 Privacy** | Consent + dignity constraints. Scope: shared/dm is code-enforced, not narrative. WELL holds representation ⇒ reduction invariant. |
| **F6 Audit** | Full graph traversal available. Every perspective edge queryable. Every event ↔ claim ↔ evidence join queryable. |
| **F7 Boundaries** | Authority and capability separation. CanMutate = granted ∧ scope ∧ target ∧ boundary. The executor may never issue its own envelope. |
| **F8 Correction** | History preserved, present updated. Supersession edges, not silent rewrites. |
| **F9 Anti-Hantu** | Representation(Human) ≠ Human. The graph does not become the person. |
| **F13 Sovereignty** | Authority graph traversal required. Constitutional mutation = F13 binary. No self-authorization. |

---

## 11 · The success condition (per brief §SUCCESS CONDITION)

The refactor is complete when HERMES can answer ALL of these without
confusing profile with person, memory with authority, proxy with reality,
or interpretation with truth:

```
1. "This is what happened."           → EVENT primitive, with occurred_at
2. "This is who reported it."         → CLAIM primitive, with speaker + source
3. "This is what supports it."        → EVIDENCE primitive, with supports[]
4. "This is what contradicts it."     → EVIDENCE primitive, with contradicts[]
5. "This is my interpretation."       → PERSPECTIVE primitive, attributed
6. "This is what remains unknown."    → UNKNOWN primitive, explicit
7. "This is who has authority."       → AUTHORITY primitive, with valid_from/until
```

**A failure to answer any of these with typed primitives (not narrative
paragraphs) is a failure of the refactor, not the user.**

---

## 12 · The non-goals (anti-bangang, anti-drift)

```
DO NOT  add a "personality" score, "loyalty" index, "trust" meter, "closeness" rank
DO NOT  collapse two perspectives (Arif-on-Syed, Syed-on-Arif) into one
DO NOT  emit "Syed is X" without perspective attribution
DO NOT  rewrite a SUPERSEDED claim as FALSE
DO NOT  let retrieval frequency promote AGENT_INFERRED to USER_RATIFIED
DO NOT  widen the executor's own authority envelope
DO NOT  add a new dashboard, JSON, ledger, or canon without a real failure class
DO NOT  ask Arif to do work that is mechanical and reversible
```

**Final test (Anti-Bangang):** does the system have more dignity-preserving
language about humans after the refactor? If no, the refactor is the
opposite of its purpose.

---

## 13 · Receipts (this draft)

| # | Receipt | Status |
|---|---|---|
| R1 | Existing reality-graph doctrine surveyed (REALITY_GRAPH.md, REALITY_GRAPH_5_LAYER_DOCTRINE-STAGING, APEX_REALITY_GRAPH_MEMORY_MIGRATION_v1, FEDERATED-HUMAN-REALITY-MAP-2026-09-24) | OBS 2026-10-07 |
| R2 | Existing person-memory surfaces enumerated (people.yaml, lanes.yaml, social-graph.yaml, 13 person-cards in /root/memory/people/, MEMORY_MANIFEST.json per person, carry_forward.json, shadow maps under lanes/private/) | OBS 2026-10-07 |
| R3 | Brief parsed: 8 primitives, 6 H-laws, 4-gate chain, 4-layer organ model, success condition, non-rebuild law | OBS 2026-10-07 |
| R4 | Two advisory pastes integrated (paste_2 — frame-as-query, 4-gate chain, perspective immutability, FRAME = observation not judgment; paste_3 — L0..L7 compression, 6 canonical hukum, attention as governed retrieval) | OBS 2026-10-07 |
| R5 | Live infrastructure census: source/build/deploy drift, zero active memory policies, 8-state claim lifecycle live, 73 evidence items (per APEX migration canon), CHRON longitudinal samples insufficient on most proxy↔reality pairs | REPORTED (paste_2) — re-verify before step-7 |
| R6 | This draft created as DRAFT_AWAITING_F13 at /root/AAA/instructions/HUMAN-REALITY-EDGE-BRIDGE-REFACTOR-v0.1.md | WRITTEN 2026-10-07, **PROMOTED F13_RATIFIED_CANON 2026-10-07 (Arif "sah")** |

---

## 14 · One-line INIT (operational form, per paste_3)

```
Represent reality. Attribute perspective. Preserve unknowns.
Minimize disclosure. Never confuse the human with the graph.
```

---

DITEMPA BUKAN DIBERI ⚒️

written_by: hermes (Mouth lane, this session, F13 brief 2026-10-07)
draft_status: **F13_RATIFIED_CANON — Arif "sah" 2026-10-07, ratification_event SEAL-HERMES-HUMAN-REALITY-2026-10-07**
promote_to: (closed — no longer pending; superseded by ratified status)
pre_F13_promotion_checklist_was:
  (a) the live infrastructure census is re-probed and drift is resolved
  (b) the 7-step ladder is executed end-to-end on at least one worked example
  (c) the 4-gate chain passes a probe with a non-trivial human
  (d) F13 issues explicit "sah"
