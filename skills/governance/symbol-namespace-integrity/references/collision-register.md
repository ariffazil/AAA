# Collision Register — worked classes

Reference for `symbol-namespace-integrity`. Read when a proposal's notation *looks* fine and you need
to decide whether it collides, or when extending `SYMBOL_TABLE.json`.

## The three collision classes seen in practice

### 1. Borrowed letter, different axis (FATAL)

An external artifact proposed `R0–R5` as **authority tiers** (R0 read · R1 analyze · R2 dry-run ·
R3 write · R4 deploy · R5 irreversible). This federation binds `R0–R5` as **consequence domains**
(R0 World · R1 Human · R2 Machine · R3 Witness · R4 Who-pays · R5 Governance).

Same tokens, unrelated meanings. Importing would make `R4` ambiguous between *"who pays if wrong"*
and *"deploy needs approval"* for every future reader.

### 2. Corrected letter, still colliding (FATAL — the repeat offender)

After the `R` rejection, the artifact corrected itself and proposed `T0–T3` for authority
(T0 read · T1 analyze · T2 dry-run · T3 external write). The federation's `T0–T3` was already ratified
with different semantics — critically, **`T1` here means edit/test/commit/restart-one-service,
auto-do**, and many skills already carry `autonomy_tier: T1`.

Importing would have **silently relabelled those skills from "auto-do writes" to "read-only"** with
zero changes to any doctrine text. That is the archetype: no error, no failing test, an authority
downgrade invisible until an agent is asked why it is seeking approval to commit.

The same artifact then proposed `W0–W4` for witness state, colliding with `W1–W6` attention-waste
classes (marked *sole enforcement authority*) and `W888` sovereign attention cost.

**Lesson:** a revision needs its own probe. Self-correction proves responsiveness, not correctness.

### 3. Letter already in informal use (AMBIGUOUS)

`K0–K4` as a kill/rollback scale — but `K3` already names a model and `K4` names a node in federation
text. The symbol is not formally reserved, so the probe returns AMBIGUOUS rather than FATAL.

**Lesson:** spelling it out in words costs one sentence and removes the ambiguity permanently.
`kill condition: reversible | retractable-with-cost | irreversible` needs no prefix at all.

## Recognising a notation proposal in prose

The probe detects these, but knowing the shapes helps you spot them before running it:

- **Indexed prefix ranges** — `X0–X5`, `Xn`, `X-1`. A range implies a scale.
- **Band/tier/ladder language near the token** — "tier", "band", "level", "axis", "gradient",
  "classification", "domain", "state", "spectrum". The probe treats a free letter used at ≥2 indices
  in such a document as `NEW_AXIS`, because that is the failure shape even on an unclaimed letter.
- **A tidy taxonomy that arrives fully formed** — four axes, clean names, no derivation shown. Tidiness
  is a symptom, not evidence. Ask what was derived from what.
- **A table mapping one letter to instructions** — `R0 = read, list, inspect`. That form is always a
  scale proposal, never a definition.

## Hyphen and dash variants

Arrows, en-dashes and hyphens are used interchangeably (`R0-R5`, `R0–R5`, `R0→R5`). The probe
normalises these; when writing them by hand into a document, use the plain hyphen so a future grep
finds them.

## Extending SYMBOL_TABLE.json safely

Add an entry when a federation symbol becomes **binding** — i.e. it gates behaviour, carries
enforcement, or is read by more than one agent.

```json
"R0-R5": {
  "means": "CONSEQUENCE DOMAINS — R0 World Reality · R1 Human Reality · ...",
  "owner": "/root/AAA/instructions/three-consequence-domains.md",
  "status": "F13_RATIFIED_CHAT <date>",
  "collision_class": "FATAL",
  "known_bad_imports": ["R0-R5 as authority tiers (external artifact — REJECTED)"]
}
```

- `collision_class`: `FATAL` for reserved/enforced symbols · `AMBIGUOUS` for informal in-use names ·
  `RESERVED` for symbols forbidden by glossary rule (e.g. bare `Φ`).
- `known_bad_imports` is the highest-value field: it lets the probe print *why* a notation was already
  rejected, which stops a future session re-litigating it.
- Machine counts never live here. This table is hand-kept because it holds ratified meaning; anything
  derived belongs in the census/registry, not the namespace.

## Where the probe belongs in an intake pipeline

Probe is **step 0**, before the citation check and before any attempt to correct overclaims — reading
for content first is how notation gets absorbed ahead of its check. Wire it as the first step of the
owning intake reference (`aaa-doctrine-sealing/references/external-artifact-intake.md`) rather than
leaving it as a separate habit.

## Fixture discipline

Keep at least one fixture of a known-colliding artifact and re-run it after any change to the table or
probe. A probe that has never returned `FATAL` on a real artifact is untested. Verify both directions:
a known-colliding fixture must fail, and a clean prose document must return `CLEAR` — a probe that
fires on everything is as useless as one that fires on nothing.
