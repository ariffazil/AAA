# Extracting an expansion index (EI) from a 2-D section

Load when producing or reviewing code that measures lateral thickness change between two picked
horizons — the growth-wedge / isochore axis that gates like K-GROWTH and K-EXT-GROWTH consume.
The doctrine is in the parent SKILL.md; this file is the implementation surface — the traps that
cost time, in the order they bite.

## 1. Separate the refinement from the evidence

An EI is a ratio of interval thicknesses against a declared reference:

    EI(x) = T(x) / T_ref          T(x) = lower_pick(x) - upper_pick(x)

Measure it from the picks. Picks are the evidence; anything correlation-derived is refinement.
Whatever smooths T(x) (a 3-trace median, a filter) is a **smoothing device and changes the number**.
Say so in the receipt, because a reader who recomputes from the picks must get the same answer.

Name the reference basis. "Ratio to the section median" is not a hanging-wall/footwall ratio: a
median reference silently measures *wedge symmetry about the median*, which is a different and
weaker claim. Emit the basis string, and never let the number travel without it.

**A scalar velocity leaves EI invariant.** EI is a ratio, so a single V cancels: time→depth
conversion changes both thicknesses identically. Only a *laterally varying* V(t,x) changes EI. If
someone defends a depth EI on the grounds that "we supplied a velocity", check whether it varies
laterally — if it does not, the number is exactly the time-domain number wearing a metre label.

## 2. The slop constraint censors correlation, not steep geology

Constrained (Sakoe-Chiba banded) DTW is the standard refinement, and the band is usually built as

    band = ceil(|structural_shift_from_picks| + max_slop_fraction * T_median)

**Consequence:** the band already accommodates whatever the picks say the structure is doing. A
structurally consistent wedge — even a steep one — is therefore never censored, because the
optimum fits inside the expanded band. Tightening `max_slop_fraction` on a self-consistent wedge
does not produce censoring either; it only shrinks the allowance for *unexplained* warp.

What actually censors is **correlation that outruns the picks**: picks declaring no change while
the waveform inside the interval does change laterally. That is the adversarial construction,
and the only one that exercises the constraint:

- wire the picks flat, and make the interval's internal beds alternate in thickness laterally
  (e.g. 40/60 samples on alternate traces, when the slop allows ~10).
- expect: nearly every pair censored, `n_pairs_compared < n_pairs_sampled`, a
  `dtw_warp_censored_by_band` flag, and a status that is neither PASS nor KILL.

**A test that merely steepens the wedge while keeping picks consistent with the waveform tests
nothing** — it passes whether or not the constraint exists. Two further null constructions to
avoid: (a) stretching the interval *uniformly across all traces* makes adjacent traces identical,
so DTW finds the diagonal and reports no warp; (b) windows extracted as the same sample range for
both traces are equal-length by construction, which biases the optimal path toward the diagonal.
Neither can detect a missing slop constraint. Verify a slop test by deleting the constraint and
confirming the test fails.

Also drop censored pairs from the comparison rather than counting them as agreement. A path riding
the band edge is unconstrained, not informative, and averaging it in manufactures agreement.

## 3. Screen wavelet phase OUTSIDE the interval

The contamination screen for wavelet phase rotation must measure instantaneous phase on a
reference event **above the interval**, not on the interval's own bounding event. A thickness
change legitimately shifts the interval event's apparent phase (interference, tuning, bed spacing),
so measuring there fires false contamination on clean synthetic data — and a QC gate that cries
wolf on clean input gets switched off, which is worse than not having it.

Practical form: take the envelope maximum inside `[0, upper_pick - guard]` where
`guard ≈ 0.5 * T_median`, read its instantaneous phase, then test lateral behaviour — a median
adjacent-trace step and an end-to-end drift against declared tolerances. Reject traces whose
envelope is too weak (< ~0.2 x section median) instead of reading phase from noise.

The honest limit: a **section-wide uniform rotation is invisible** to this test. Only a laterally
varying rotation is detectable from the data alone; a uniform one needs a well tie or a known
source wavelet. State that limit in the receipt rather than implying the screen is complete.

## 4. Wavelength estimation punishes interference; let the caller declare it

Estimating the dominant vertical wavelength by peak-picking the pooled vertical Fourier spectrum
is fragile in a layered interval, because interference between the bounding events creates side
peaks that are not the wavelet — an estimate can land on roughly 2x the true period and silently
halve both the λ/4 tuning limit and the λ/8 floor. Three responses:

1. Accept a **declared** wavelength from the caller (source wavelet, well tie) and record its
   provenance; fall back to the estimate only when nothing is declared.
2. Cross-check the estimate against a stacked-trace autocorrelation side-lobe lag: agreement is
   reassuring, disagreement means the estimator is measuring bedding, not the wavelet.
3. Because both are estimates, the resolution screen should be able to return **NOT_EVALUATED** —
   not a silent pass. An unevaluated screen reported as PASS is a fabrication.

Then apply the two floors with different force. Below **λ/8** (absolute resolvability floor) the
interval is not resolvable: withhold the number, return UNMEASURED, and name vertical resolution
as the missing input. Between **λ/8 and λ/4** the interval is only partly resolved: emit the number
but downgrade the QC verdict to a caveat and flag `tuning_risk_below_lambda4`.

## 5. Receipt shape for this axis

A number emitted without its frame is a defect. Every EI receipt carries, together:

- the candidate, the **domain** (TIME or DEPTH) and the units;
- the domain **conversion** record, including whether the velocity was scalar or laterally varying;
- the **QC verdict** with each check's measured value, threshold and verdict — tuning, phase,
  lateral amplitude, lateral coherence, slop censoring, pick-vs-correlation agreement;
- `missing_inputs` on every refusal;
- the falsifier **direction** (`CONTRADICTION` when a measured EI ≤ 1 exists everywhere,
  `NOT_AVAILABLE` otherwise), never a KILL, since a wedge can be absent and invisible at once;
- status semantics stated explicitly: status describes **extraction quality**, not a geological
  verdict. PASS means "measured with a clean QC", never "growth proven".

A missing surface, an unidentified domain, or an absent velocity model is UNMEASURED with the input
named — never a number, and never a default. Declared scales (sample interval, bin spacing) must be
passed in explicitly; an extractor that inherits a workspace vertical scale will silently emit a
wrong ratio on the next dataset.

**A refusal receipt must have the SAME key shape as a success receipt, with values `None`.** Build
one empty-result constructor and have every refusal path flow through it, rather than letting each
early return invent its own dict. Consumers read `result["expansion_index_max"]` unconditionally — a
refusal that simply omits the key raises `KeyError` in the caller and turns a clean UNMEASURED into a
crash. The rule generalises to every gate: an UNMEASURED verdict is a value, not an absent schema.

## 6. Prove the suite is load-bearing by mutating the module

A gate suite that passes on both correct and broken code is documentation, not a gate. Passing tests
prove nothing on their own — a test can be green because the guard it targets was never exercised.

Procedure, after the suite is green:

1. For each load-bearing behaviour, apply ONE targeted mutation to the module (hardcode the emitted
   number to a constant; delete the velocity-model refusal; let the UNMEASURED path emit a number;
   remove the λ/8 floor; disable the phase screen; drop the slop band; silence the missing-input
   naming).
2. Re-run the suite and confirm a **distinct** test fails for each mutation.
3. Restore from a backup copy and re-confirm green.

A mutation that no test catches means that behaviour is untested regardless of coverage numbers, and
the mutation is the fix list. This is the cheapest way to answer the only question that matters about
a QC gate: *if I broke it, would anything stop me?*

Corollary for the adversarial tests themselves: when a test is written to prove a *constraint* fires,
verify it by deleting the constraint and confirming the test then fails. A constraint test that passes
with the constraint removed was testing something else.

## 7. Running the suite in the GEOX repo — and what a failure while others are writing means

Use the repo's own venv. The default interpreter is a trap:

    cd /root/GEOX && PYTHONPATH=src .venv/bin/python -m pytest tests/test_<name>.py -q

- The bare `python3` on this host is **Hermes's own venv**, which has no `pytest_asyncio`. The symptom
  is an ImportError while loading `tests/conftest.py` — that is the wrong interpreter, not a broken
  project, and installing packages does not fix it.
- Do not pipe pytest through `tail`/`head` when you need the status: the pipe returns the last
  command's exit code, so a failing suite can report success. Read the summary line instead.
- `pyproject.toml` already sets `--import-mode=importlib --ignore=CLAUDE.md --ignore=AGENTS.md`; adding
  a test file needs no conftest change.
- **Run only your own test file, and re-run a failing test alone before diagnosing it.** In a shared
  working tree with concurrent writers a run churns: unrelated failures can appear and vanish, and a
  single-test re-run is what separates a real defect from the churn. Never conclude a defect from a
  suite run taken while other agents were mid-write — and check `git status` before claiming authorship
  of a change, because a sibling agent can edit a file that sits inside your declared ownership
  boundary. Report the true state (blocked at a gate / changed by another writer) rather than a clean
  story, and never assert a mechanism for a transient failure you did not reproduce.
