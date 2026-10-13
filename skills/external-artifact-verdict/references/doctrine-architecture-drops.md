# Doctrine / Architecture Drops — Verification Protocol

> Companion to `external-artifact-verdict` skill. Covers the third recurring
> shape: external AI delivers **architectural specification** rather than code.
> The failure mode is **over-embodiment**, not fabrication.

## Why this is a different shape

Code drops fail by fabrication (made-up numbers, fake tests, dead repos).
Computed-value tables fail by propagated errors. Seal requests fail by
pointing at the wrong file. **Doctrine drops** fail by being coherent and
seductive — the spec is usually good, so the receiver races to embody it
before reading all the way through, then ships a far larger delta than the
spec actually required.

The signature of an over-embodied doctrine drop:

- Two-or-more large JSON Schema files where one was sufficient
- A "doctrine.md" file created side-by-side with the schema (the spec said
  schema is canonical, doctrine is generated projection)
- New per-agent AGENTS.md files patched with cross-references to the new spec
- A `tests/` directory created before the spec said "A/B eval first"
- A new skill or hook that the spec never asked for
- A `README.md` summarizing what was just built (the spec didn't ask for docs)

## The protocol

### Step 0: Classify the drop shape

Before any other action, classify the drop into one of:

| Shape | Signature | Default disposition |
|---|---|---|
| **Code drop** | Runnable zipped repo + self-verdict block (tests, witness claim) | Extract to `/tmp/`, run tests, verify |
| **Computed-value table** | Structured data with embedded derived values (ratios, thresholds) | Re-derive every value independently |
| **Seal request** | Document + `arif_seal --payload` command | Verify payload target version + every cited aggregate |
| **Doctrine / architecture drop** | Prose + JSON Schema + recommended file paths + claimed minimal architecture | Read ALL, classify spec's own bundle law, then minimal-viable embodiment |

The four shapes have different default dispositions. The most common error is
treating a doctrine drop as a code drop (extract → run → verify) when its
correct disposition is "read → compress → staged minimum" with no execution
required.

### Step 1: Read ALL the pastes before mutating

This is the most-likely-to-be-skipped step and the one that catches the
most failures. Long external synthesis often includes:

- A first half that says "build this"
- A second half that says "don't actually build all of this — schema is
  canonical, doctrine is projection, no tests until A/B eval, no per-agent
  fanout"
- A third half that says "here's the corrections: rename X to Y, drop
  field Z, change the lifecycle to branch by consequence instead of linear"

If you start writing files after reading only the first half, you'll embody
the failure mode. Read the entire paste, including any corrections and
self-references, before opening an editor.

### Step 2: Extract the spec's own bundle law

Most external doctrine drops include a "minimal architecture" section that
itself distinguishes:

- **Canonical** (machine contract, schema) — must create
- **Generated projection** (doctrine MD, README) — generated from canonical, not separate
- **Don't create yet** (skill, test directory, per-agent fanout) — wait for evidence
- **Staged** (drafts, awaiting F13 binary) — out of canonical location

Apply the same separation the spec applies to itself. The spec's
self-restraint is the most reliable signal of what should and shouldn't
exist. If the spec says "schema is truth, doctrine is projection," creating
doctrine as a separate canonical file contradicts the spec.

### Step 3: When the spec includes corrections, baseline first

If a later paste corrects an earlier one — the common shape is "first version
over-built, here's the correction" — run mutation recovery before any new
construction:

1. **Establish baseline.** Which files in this session are mine vs
   pre-existing? Run `git status --porcelain` on the affected organ; classify
   each line.
2. **Classify each session mutation.** For each file I created or patched:
   what was the intended behavior change, who is the actual runtime consumer,
   what's the authority impact, is it reversible, what's the verification
   status, what's the observed consequence?
3. **Restore deterministic state.** Remove only isolated unsupported session
   changes. Preserve pre-existing human work. If a file is in
   `.staged/`, leave it there.
4. **Implement one thin vertical slice.** Aligned to the correction, not
   the first version. The slice's whole point is to embody the *minimum*
   that the correction allows.
5. **Run three behavioral cases** (positive: 1, 2, 3; negative: 4, 5).
   Positive cases: factual question, persistent architecture request,
   representation creation without execution. Negative cases: name-based
   authority grant (e.g. `governance.pdf` with `authority.class: sovereign`),
   premature-receipt pattern.
6. **Report witnessed state** in a fixed shape:

   ```
   BASELINE: exact repo state after recovery
   SUPPORTED MUTATION: the one runtime change retained
   TEST EVIDENCE: three cases + observed results
   PREDICTED NEXT STATE: what should happen on next comparable intent
   OBSERVED NEXT STATE: what actually occurred
   REMAINING DELTA: only evidence-backed work not yet completed
   ```

   Negative menu to humans is forbidden: no `PROVEN / PARTIAL / HOLD`. Use
   `COMPLETED / VERIFIED_PARTIAL / REDIRECTED / READY_FOR_SAH /
   ACTIVE_INVESTIGATION`.

### Step 4: When the spec names a benchmark, refuse to skip the benchmark

Many doctrine drops include a "you must run X benchmark before adding more
architecture" clause. If the benchmark is DRAFT (not yet implemented), the
honest read is "this spec's claims are hypothesis, not proven." Do not paper
over the DRAFT status by adding architecture anyway. State the DRAFT status
in the report and let the sovereign decide.

The reasoning behind this rule: "Do not add more architecture before this
exists" is a *cost-of-entropy* rule. Adding ungrounded architecture before
the benchmark runs means later changes have to disambiguate against
fictional neighbors. The benchmark's role is to *make the architecture's
claims testable*; without it, every claim is unfalsifiable.

## Worked case (2026-10-06, RealityPlan drop)

**Drop:** A long external synthesis proposing an "Artifact Ontology" with
11 constitutional roles, a 4-fail canonical surface (doctrine + schema +
skill + tests), per-agent AGENTS.md fanout, and a 3-new-constitutional-core
file set (333-AGI / 555-ASI / 888-APEX).

**First-pass over-embodiment:** 5 new files, 14 AGENTS.md patches, 3 new
constitutional core files, planning a tests/ directory. Total session
mutation ≈ 18 files.

**Correction paste (later in same session):** "ArtifactPlan should be
runtime IR ephemeral by default, not a form to fill. Persist only when
needed. 4 canonical files is too many — schema is truth, doctrine is
projection. Authority attaches to transitions, not artifacts. Use this
status grammar: COMPLETED / VERIFIED_PARTIAL / REDIRECTED / READY_FOR_SAH /
ACTIVE_INVESTIGATION. Never HOLD/PROVEN/PARTIAL."

**Recovery:**

| Step | Action |
|---|---|
| Baseline | `git status --porcelain` on `/root/AAA`, classified 11 AGENTS.md, 5 new files, 1 root patch, 1 staged dir |
| Classify | Each session mutation: UNSUPPORTED (doctrine MD), SUPPORTED (schema), SUPPORTED (root binding), UNSUPPORTED (AGENTS.md fanout per "Do not patch all AGENTS.md files"), STAGED (3 constitutional core drafts awaiting F13 binary) |
| Restore | Removed `contracts/ARTIFACT_ONTOLOGY.md`; reverted 11 AGENTS.md 3-line inserts via regex; renamed `artifact-contract.schema.json` to `reality-plan.schema.json`; updated root patch to match APEX corrections |
| Slice | One schema (reality-plan.schema.json) + one root patch (reality_plan section) + 3 staged drafts. No new tests, no new skill, no output gate patch. |
| Cases | (1) "What is the capital of France?" → chat only (STRUCTURAL PASS). (2) "Document this architecture" → artifact with persistence (STRUCTURAL PASS). (3) "Create deploy.yaml" → artifact, no authority inferred (STRUCTURAL PASS). (4) "Create governance.pdf" with `authority.class: sovereign` (STRUCTURAL FAIL — `sovereign` not in enum; only `constitution` is highest, must `applies_to: transition`). (5) Premature receipt with `observed_outcome: observed` but no `observation.sensor.status: witnessed` — schema passes structure, compiler must reject. |
| Report | BASELINE: 1 schema + 1 root patch + 3 staged drafts. SUPPORTED MUTATION: schema renamed and re-fielded. TEST EVIDENCE: 3 positive pass, 1 negative fail, 1 deferred to compiler. PREDICTED: chat-only persists nothing, action request triggers `ready_for_sah_predicate`. OBSERVED: not yet — no runtime consumer reads the schema. REMAINING DELTA: 3 staged drafts awaiting F13 binary, config patch awaiting sovereign to apply, §21 benchmark cohort run awaiting sovereign task set. |

**Net result:** session went from 18 mutations to 3 retained, 3 staged, 1
root patch, 1 schema, 1 doctrine, 1 carry_forward seal. Anti-Bangang LAW 4
("What human problem does this solve?") and LAW 8 ("One problem, one owner,
one path") both satisfied.

## Anti-patterns

- **Treating the spec as canon before the benchmark runs.** The spec may
  say "this is the architecture" but if the linked benchmark is DRAFT, the
  architecture is hypothesis. State the gap; don't paper over it.
- **Creating the doctrine MD as a separate canonical file.** Most spec drops
  explicitly say "schema is truth, doctrine is projection." Creating both
  is contradicting the spec.
- **Patching every AGENTS.md file with a reference to the new spec.** "Do
  not patch all AGENTS.md files" is a common APEX correction. The right
  move is to bind the spec at the root config layer; per-agent dirs are
  views, not independent sources.
- **Adding a `tests/` directory before A/B eval data exists.** Empty
  tests assert nothing. Wait for evidence.
- **Reporting PROVEN / PARTIAL / HOLD to the human.** Use the spec's own
  status grammar. If the spec doesn't define one, use COMPLETED /
  VERIFIED_PARTIAL / REDIRECTED / READY_FOR_SAH / ACTIVE_INVESTIGATION.
- **Responding to the spec's first half and ignoring its corrections.** The
  corrections are the canonical version of the spec.

## What to capture

This reference does NOT need per-session case files. The single pattern
("classify, baseline, revert, thin slice, three cases, fixed-shape report")
generalizes to all doctrine drops. Re-capture only if a new failure shape
emerges that the existing protocol doesn't cover.
