# Tectonic Regime Deduction from Horizon Geometry

How to reason from stratal and fault geometry toward a tectonic regime, and where the reasoning must stop.
Load when the question is "what regime produced this?" or "when did it move?".

## 1. The one step that is genuinely deductive

Almost all regime deduction is abduction — many-to-one mapping from mechanism to geometry. There is exactly one hard
constraint, and it comes from mechanics rather than from pattern-matching:

A free surface cannot support shear traction, so one principal stress axis is vertical near the surface. With
Coulomb failure at θ = 45° − φ/2 measured from σ1 (Byerlee μ ≈ 0.6–0.85 ⇒ φ ≈ 31°–40°), that fixes a dip family:

- **σ1 vertical → normal fault, dip ≈ 60°** (θ ≈ 30° from vertical)
- **σ3 vertical → thrust, dip ≈ 30°**
- **σ2 vertical → strike-slip, dip ≈ 90°**

So dip is the one first-order regime indicator readable almost directly from fault geometry. Everything else is
inference, and every inference carries alternatives.

**Scope limits on that triple.** It holds for newly formed faults in isotropic rock near the surface with a free
surface. Stress rotates with depth and σh can overtake σv, so the 60° figure describes a near-surface state, not the
whole crust. A deviation beyond roughly ±15° is a **rule of thumb, not a derivation** — treat it as a prompt to
enumerate alternatives, never as evidence that the regime changed. The alternatives are: inherited fabric or
reactivation, weak substrate or overpressure, block rotation (domino/bookshelf rotation shallows normal faults while
the regime stays pure extension), oblique or transtensional stress, depth-dependent stress rotation, or friction
outside the Byerlee range.

Two **measurement preconditions** gate whether dip may be used at all, and both are display problems rather than
geology:

- **Vertical exaggeration inflates apparent dip.** tan θ_apparent = VE · tan θ_true, where VE is the *dimensionless*
  display ratio (v_display/v_true), never a velocity — writing it as a velocity equates a dimensionless quantity to
  m/s. Never measure a dip off an exaggerated display.
- **Migrated data do not follow that relation**, so migration changes apparent-dip behaviour. A migration-state
declaration (migrated / unmigrated / unknown) is required before any dip is trusted, and *unknown means untrusted*,
not "probably fine". Time-domain dips additionally need an interval-velocity model before they are depth geometry.

## 2. Regime → geometry map

**Extension.** Listric faults with rollover anticlines; half-grabens; domino/bookshelf rotation; growth wedge
thickening toward the hanging wall with its apex at the fault. Small vertical offsets with few antithetic faults.

**Contraction (thin-skinned).** Ramp-flat geometry; fault-bend folds; duplexes; imbricate fans; triangle zones;
forelimb steepening or overturn.

**Contraction (basement-involved).** Shortcut faults, basement-cored uplifts, monoclinal drape rather than a throughgoing
fault — a different family from thin-skinned, with different balancing rules.

**Strike-slip / wrench.** Near-vertical master fault; positive (transpressive) or negative (transtensional) flower;
en-échelon folds oblique to the master; Riedel shears at roughly 15° (R), 75° (R′), 10–15° (P) from the master.

**Reaction / inversion.** A pre-existing extensional fault carrying later reverse separation — selectively along
strike, not for its whole length. A null point that migrates upward as inversion proceeds. Crestal uplift with erosion
passing laterally into conformity.

**Gravity-driven (delta or margin collapse).** Extensional growth faults updip, rollover, toe thrusts downdip, all
above a common décollement. A separate family from tectonic extension, not a subtype of it.

**Decoupling mechanisms — not regimes.** Salt, mobile shale, and thermal sag do not express the regional stress field;
they mask or decouple it. Salt above a weld says nothing about stress below, and salt in section makes area/bed-length
conservation inapplicable rather than violated. A saucer geometry with regional onlap and **no growth wedge** is
thermal sag, and it is routinely misread as extension.

## 3. Confounders that flip a call

- **Differential compaction** is the leading false positive for syn-tectonic growth: it produces thickness variation
  over a paleo-high that mimics a growth wedge. Require thickness change *localised to a structure* plus depositional
  terminations, not thickness variation alone.
- **Crestal thinning is not evidence for compression.** In most basins it is erosion (truncation = missing section) or
  reduced accommodation on a pre-existing high. Thinning is a thickness observation; truncation is a superposition
  observation. Test them separately — a truncated crest with no measured shortening is uplift plus erosion, which may
  equally be inversion, salt withdrawal, or epeirogeny.
- **Symmetric isochores are not evidence of post-depositional sag.** Symmetric thickness also results from differential
  compaction, a graben with both bounding faults active, and strike-slip basins. Asymmetry is not the discriminator.
- **Depositional dip must be removed before any structural tilt is claimed.** Clinoform foresets commonly 1–25°
  (carbonate margins steeper). These are envelopes, not constants.
- **A uniform interval does not identify eustasy.** Steady sediment supply, thermal subsidence, pure strike-slip, and
  post-depositional sag all produce uniform thickness. The eustatic test is a regionally correlative surface with
  synchronous onlap or truncation at a consistent stratigraphic level across unrelated structures.
- **Decompact before using any thickness.** "Constant thickness" in a pre/syn/post-kinematic division means constant
  in *time*, not in *depth*. Compaction thins parallel beds with zero tectonics, so an un-decompacted isopach produces
  a differential whose cause is lithology — and that differential is then priced as growth. This is a prerequisite on
  the thickness axis, not a refinement.
- **Fault azimuth populations record stress intersected with inherited fabric**, not stress alone. Pre-existing
  low-cohesion faults reactivate even when unfavourably oriented, so a rose diagram is not a stress indicator by itself.

## 4. Timing: the only reliable clock

**Growth strata — lateral thickness divergence between correlated horizons, localised to a structure and supported by
terminations — is the one dependable dating signal.** Not fault position, not dip, not azimuth. The onset of fanning or
thickness divergence brackets the start of the pulse; the return to parallel geometry brackets its end.

Two qualifications that must travel with the claim:

- Thickness divergence is not by itself proof of deformation — depositional slope change and compaction produce it too.
- Geometry gives **bracketing, not dates**. Absolute age comes from biostratigraphy or geochronology. The temporal
  resolution of a tectonic event is the resolution of the age model, never the resolution of the seismic.

## 5. What geometry cannot decide

State these as limitations rather than resolving them by assertion.

- **Non-uniqueness is inherent.** Drape over a paleo-high, differential compaction, salt withdrawal, basement wrench,
  and pure-shear buckling can produce near-identical geometry. The test is not shape but context: does the fold die
  upward (compaction/drape) or reach basement (tectonic)? Is a detachment present?
- **The record is lossy and not invertible.** A second phase removes evidence of the first. Full history cannot be
  recovered from the final state.
- **Coaxial overprint is a blind spot.** A second phase coaxial with the first leaves minimum interference and is
  effectively undetectable from geometry. Say you are blind rather than claiming the absence.
- **Resolution sets a floor.** Beds below λ/4 (best case λ/8) are unresolvable, and sub-resolution fault throw appears as
  flexure — a monocline is not automatically a fault. Absence of a growth signature at that scale is not absence of
  growth.
- **Obliquity biases everything.** A section not parallel to transport underestimates strain and misreports dip. Section
  azimuth must be declared against the structural grain.
- **Regional population, not single structures.** A local stress perturbation (salt, shale, a basement high) reorients
  local faulting. The regional axis comes from population statistics; one fault gives nothing.
- **Stress magnitude is unrecoverable from geometry.** A reduced stress tensor resolves 4 of 6 parameters, and the
  absolute level requires external anchoring. Never quote a stress magnitude derived from fault geometry.

## 6. Falsifier direction, applied per regime

Each regime carries both kinds of test. Only the contradiction column may reject.

- **Extension.** *Contradiction:* a measured expansion index ≤ 1 across covered intervals at the fault while growth is
  claimed; or measured reverse separation at the same level with restored shortening > 0. *Deficit (UNMEASURED only):*
  no observable growth wedge; all fault planes planar with no rollover — planar domino rotation is a valid extensional
  mode.
- **Contraction.** *Contradiction:* restored bed length ≥ undeformed length with area conserved on a section valid under
  the conservation conditions; or measured net extension at the same level. *Deficit:* no syn-tectonic wedge into the
  foredeep; no consistent vergence.
- **Strike-slip.** *Contradiction:* measured slip vectors on three or more independent planes are all dip-slip dominant
  with consistent sense — and this requires 3-D cutoff-line vectors, so 2-D data must return UNMEASURED. *Deficit:* no
  flower imaged; no en-échelon train. Strike-slip is the regime most often misread on 2-D data: a near-vertical fault
  with small vertical offset makes an oblique section mimic dip-slip geometry, and pure strike-slip with no vertical
  component produces no growth strata and no thickness change at all. Map-view horizontal displacement is the only
  decisive discriminator.
- **Inversion.** *Contradiction:* no extensional growth wedge at depth across a covered window — inversion is *defined*
  as reactivation of an extension, so its absence means the structure is a new thrust or a wrench feature instead.
  *Deficit:* no thickness reversal. Keep three observations separate here — separation sense, thickness change, and
  truncation — and never let one stand in for another.
- **Gravity.** *Contradiction:* measured downdip shortening exceeding measured updip extension beyond tolerance, and
  only *within the closed system* — the equality is local, never basin-wide, since material crosses the section and
  isostasy and thermal subsidence operate independently. *Deficit:* no toe thrust imaged; the toe may lie beyond the
  survey or be eroded.

## 7. Errors that recur in supplied frameworks

Check for these when auditing a framework someone else wrote.

- Crestal thinning offered as evidence *for* compression (it is usually erosion or reduced accommodation).
- "σ1 shifts to σ3" during inversion. Impossible as written — principal axes are ordered by magnitude, so the *axes
  rotate and the labels exchange*: σ1(V) becomes σ1(H) while σ3(H) becomes σ3(V).
- Cross-cutting attributed to Walther's Law (it is Steno; Walther is facies correlation).
- A time-to-depth dip relation with a bare velocity where a dimensionless velocity *ratio* belongs, and the wrong
  trigonometric operator for migrated versus unmigrated data.
- A ±15° Coulomb tolerance presented as a hard constant rather than a rule of thumb with enumerated alternatives.
- "Uniform interval = eustasy" — a false-negative generator.
- Falsifiers written entirely as absence tests, which belong to the deficit column and may never kill.
- Halokinesis filed as a tectonic regime, which then contradicts any claim of universal area conservation in the same
  document.
