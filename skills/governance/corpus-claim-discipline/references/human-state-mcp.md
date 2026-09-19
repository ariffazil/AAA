# Human-state enforcement MCP — invocation patterns and refusals

When the environment exposes a human-state enforcement MCP (the `hermes_rasa` family), it is the
boundary layer for claims about people: it refuses illegal promotions at the tool boundary. Call it
before a claim reaches the human, and expect refusals — they are the point. Each item below cost a
retry to discover.

## Order that works

1. **observe** — one call per literal event. Class `O`, zero inference. Do this FIRST so evidence
   exists before any interpretation is stored.
2. **claim** — store the typed claim: provenance class, alternatives, `not_established`.
3. **paradox map** — when two readings compete, hold both; it refuses forced normalisation and
   returns `resolution_required: false`.
4. **counterstory** — for a candidate interpretation, force competing alternatives plus a
   falsification test; it returns `NARRATIVE_GRAVITY_BROKEN`, not a verdict.
5. **projection guard** — when the principal's feeling is being mapped onto a third party.
6. **cross-layer check** — before promoting a finding across disciplines.
7. **qualia boundary** — before any answer that needs interior access.

## Refusals and the fix for each

**`shadow_map` does not return shadow content.** It returns a tension count, a `qualia_boundary` of
`PRIVATE_QUALIA`, and `provenance: INFERENCE_ONLY`, capped at class `I`. Its own warning: *shadow
candidates are questions, never answers.* The analysis is yours; the tool only marks the boundary.
Never present its output as a finding.

**`cross_layer_check` needs layer names from a fixed enum.** A descriptive phrase is rejected as an
invalid layer. Valid values: `BIOLOGICAL` `BRIDGE_CLAIM` `CHEMICAL` `CULTURAL` `ECONOMIC` `NEURAL`
`NORMATIVE` `PERSONALITY` `PHENOMENOLOGICAL` `PHYSICAL` `PSYCHOLOGICAL` `RELATIONAL` `SEXUALITY`
`SOCIAL`. Bare enum names are still not enough: `SOCIAL → RELATIONAL` returns
`REJECT_CROSS_LAYER_PROMOTION` unless a falsifiable `bridge_evidence` is supplied. **Expect the
rejection for most social→relational reads**, and say so in the reply instead of silently dropping
the step — a discipline constrains, it does not translate.

**`claim` refuses archetype tokens — including inside quoted labels.** The anti-diagnostic restraint
check runs on the raw payload, so naming a room as it is titled (an archetype word appearing in a
`channel` or `addressee` field) trips it even though the token is a room name, not a claim about the
person. Fix: refer to rooms **generically** (`"telegram group <id>"`, `<group> (name withheld)`) and
route archetype language only as explicitly quoted speech, never as a description of a person.
Unknown extra keys are also refused — pass only schema fields.

**Required-parameter names are exact and unforgiving.** A near-synonym fails validation and the tool
does **not** partially execute. Read the parameter list out of the validation error rather than
guessing a second time.

## Batching

Local tools require one entry per call, and connector/MCP calls cannot be batched with ordinary local
tool calls. Send the MCP calls as one array; never mix an MCP tool and a local tool in the same
batch.

## Reporting a rejection to a human

A rejection is evidence, not an obstacle. Say it plainly and without theatre — *"I tried to carry
that from the social layer to the relational layer; the kernel refused; a discipline constrains, it
does not translate"* — because that restraint is exactly what protects a third party from the
principal's reading being filed as fact about them.
