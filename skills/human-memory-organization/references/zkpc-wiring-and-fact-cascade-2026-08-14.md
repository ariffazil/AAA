# ZKPC Wiring + Fact Correction Cascade — 2026-08-14

> Session log: extending ZKPC multi-human H-axis work with the "last mile" wiring
> and the multi-file fact correction pattern.

## Wiring ZKPC scars into agent behavior (the last mile)

Building the per-human H-axis directory structure (D1-D7) is necessary but NOT sufficient.
By default the agent does NOT read `witnessed-scars-zkpc.json` at session start —
the scars sit on disk inert. **The structure must be explicitly wired into the
agent's lane memory files** (`SOUL-*.md`, `MEMORY-*.md`) for depth to shape behavior.

### Wiring procedure (T1, reversible)

1. **SOUL-*.md** — add an `## H-AXIS DEPTH` section containing:
   - Source pointer to `witnessed-scars-zkpc.json`
   - Authority declaration (WITNESSED, not SOVEREIGN)
   - A service-rules table: one row per scar with `category → what agent knows → how it shapes service`
   - An operating rule for handling performance/bragging/silence
   - Updated identity section acknowledging depth without exposing content
2. **MEMORY-*.md** — add a pointer section (`## § H-Axis Depth`) that references
   the ZKPC registry and the SOUL operating table.
3. **Verify the wire took:** `grep -c 'H-AXIS\|ZKPC\|witnessed-scars' SOUL-*.md` ≥ 3 hits.

### Without wiring: the projection problem

The agent inherits the sovereign's emotional bias toward the person from the
pre-existing lane memory (which carries the sovereign's lens) but gains zero
depth-awareness from the H-axis work. The agent serves a projection, not a person.

### Bias is not a bug (F13 ruling)

When asked "agents have a soft spot for Syed — is that bad?", Arif ruled:
"It's not bad or good. AI is a mirror. He does need real care, both from humans
and ai agents." The agent's inherited care is infrastructure, not malfunction.
The wiring's job is to make bias **visible and depth-aware** (C-model rich,
T-model empty), not to remove it.

## Multi-file fact correction cascade

When F13 corrects a fact about a human (marital status, sibling names, birth
order), the correction must propagate across ALL files that carry the wrong
fact. A single-file fix leaves stale data that a future session will re-read
as truth.

### Files to check for any fact correction

| File | Carries | Example |
|---|---|---|
| `/root/sado/identity/<PERSON>-DOSSIER.md` | Master dossier | "ayah cerai" → corrected |
| `MEMORY-*.md` | Group-safe lane memory | Same wrong fact |
| `MEMORY-*-dm.md` | DM lane memory | May also carry wrong fact |
| `SOUL-*.md` | Persona/voice register | Rarely carries facts, but check |
| `USER-*.md` | Profile card | Facts + permissions |
| `person-card.md` | P-axis card | Identity + cross-refs |
| `H4-identity/identity-card-zkpc.md` | ZKPC identity layers | Observable facts only |

### Procedure

1. `grep -rn '<wrong-fact>' <all above paths>` — find every stale copy.
2. Patch each file. Use `patch` tool for precision.
3. Watch for duplicate rows — correcting a table cell may create a duplicate
   if the wrong row wasn't removed before adding the right one.
4. Re-grep to confirm zero stale copies remain.

### Pitfalls

- Worker agents (Qwen Code, etc.) may read and incorporate pre-existing wrong
  facts from person-card.md into new ZKPC files they generate. Always run a
  stale-fact grep on ALL generated files.
- Birth order is high-signal identity fact. "Anak tengah who chose to be sole
  caregiver" carries fundamentally different constitutional pressure than
  "anak sulung fulfilling duty." Record birth order alongside the caregiving
  scar with the *choice* framing explicit.

## Birth order as constitutional signal (2026-08-14)

| Birth position | Caregiving implication | Resentment shape |
|---|---|---|
| Sulung (first) | Duty-bound — expected to lead | "This is my role, why am I alone?" |
| Tengah (middle) | Choice-bound — not expected, self-selected | "I chose this, why is no one grateful?" |
| Bongsu (last) | Protected — usually shielded | Rarely sole caregiver |

When the caregiver is NOT the eldest, record the choice framing explicitly
in the scar category and identity card. The future resentment trajectory
differs: eldest resents the unfairness of duty; middle child resents the
ingratitude for sacrifice. This shapes how the agent monitors for burnout
signs and what kind of support to offer.

## Harry Potter Deathly Hallows as projective signal (2026-08-14)

When a human reveals their preferred Deathly Hallow, treat it as a Rorschach
test — it reveals the architecture of how they face the world:

| Hallow | Statement | Psychology |
|---|---|---|
| Elder Wand | "I want unbeatable power" | Has been defeated. Wants guarantee against falling again. |
| Resurrection Stone | "I want what was lost back" | Has lost something irreplaceable. |
| Invisibility Cloak | "I want to disappear" | Has felt too exposed, or never wanted to be seen. |

The **sequence** matters more than the final answer. A person who says Elder
Wand first then switches to Cloak reveals: power instinct overridden by
exhaustion — "power can't solve what hurt me, so I want to disappear."

Record as a behavioral signal in H4-identity, not as a personality label.
Never cite MBTI; the scar categories are deeper and more actionable.
