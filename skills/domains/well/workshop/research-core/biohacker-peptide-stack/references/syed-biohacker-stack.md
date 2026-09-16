# Syed's Biohacker Peptide Stack — Knowledge Bank

Consolidated reference for biohacker peptide conversations with Abang Sado (Syed). Sources: direct DM gateway logs (Jul–Aug 2026), Probiohacker video reference, mitochondrial biology fundamentals.

## Syed's Confirmed Stack (from DM history)

| Compound | Dose | Frequency | Form | Notes |
|---|---|---|---|---|
| **MOTS-c** | 0.1ml (very conservative, sub-protocol dose) | Per dose | Subq injectable | Inject AM to avoid insomnia |
| **NAD+** | 500mg vial, starting 25mg → planning 100mg | 2–3x/week | Subq injectable | Sensitive individual, started low |
| **Semax** | 0.1ml subq | Per protocol | Subq injectable | Russian-developed nootropic (BDNF) |
| **Selank** | 0.1ml subq | Per protocol | Subq injectable | Russian-developed anxiolytic |
| **CoQ10 (Ubiquinol)** | Planned | Oral daily | With fatty meal | Fat-soluble — needs fat for absorption |
| **Magnesium Glycinate** | 400–600mg elemental Mg | Night, 30min before bed | Oral | For sleep + ATP activation |

**Critical form note:** Syed injects subcutaneously. NOT nasal spray. Russian Semax/Selank exist as both nasal spray (clinical) and injectable (grey market) — Syed uses **injectable**.

## Probiohacker's Standard Protocol (what Syed references)

| Compound | Dose | Frequency |
|---|---|---|
| MOTS-c | 5–10mg subq | 5 days on / 2 off, cycle 4–6 weeks on + 2–4 weeks off |
| NAD+ | 100–250mg subq | 2–3x/week |
| CoQ10 (Ubiquinol) | 100–200mg oral | Daily with fat-containing meal |
| Magnesium Glycinate | 400–600mg elemental Mg | Night, before bed |

**Probiohacker does NOT include Semax/Selank** — those are separate, cognitive-focused peptides. Different domain.

## Why The Four Work Together — Mitochondrial ETC Assembly Line

The four compounds (MOTS-c, NAD+, CoQ10, Mg) target distinct stations of the same assembly line:

```
MOTS-c (AMPK signal: "produce more ATP")
  ↓ activates
NAD+ → Complex I → CoQ10 → Complex III → Cyt C → Complex IV → ATP
                                                ↓
                              Mg²⁺ cofactor for ATP synthase (Complex V)
                              ATP only biologically active when bound to Mg (Mg-ATP)
```

- **NAD+** = fuel for Complex I (electron donor)
- **CoQ10** = electron carrier between Complex I and III
- **Mg²⁺** = cofactor for ATP synthase; ATP needs Mg to be biologically active
- **MOTS-c** = signals cell to upregulate ATP production via AMPK

**Analogy:** Driving a car.
- NAD+ = petrol
- CoQ10 = fuel pump
- Mg = engine block
- MOTS-c = accelerator foot

Skip any one station → chain breaks. That's why Probiohacker bundles all four. Single compound can't cover the whole chain.

## Question Patterns from Syed

| Question | Intent |
|---|---|
| "Nape pakai motc sakit kepala" | Side-effect profile, not failure |
| "NAD bolrh hilangkan stressnkan" | Mental/cognitive benefit of NAD+ |
| "So camne aku nak buat life aku mmg cam ni kena bgn kul 5am" | Life optimization framing |
| "Hypnos pre workout" | Stacking peptides with pre-workout timing |
| "Maksud aku,dia aku pakia macam pre workout half life dia bape lama?" | Half-life/timing questions |
| "50mg nad xde side effect ke?" | Conservative dose exploration |
| "Dose selamt bape?" | Safety threshold questions |
| "Nad 500 mg pepties bape nak pakai" | Vial economics, dose planning |
| "Betul ke benda ni" + photo | Brand/source verification |
| "Ni je ada" + photo | Brand/source limitation signal |

## Pitfalls — Observed Failures

### PITFALL: Deliver the SOURCE's protocol, not your own catalog

**2026-08-20 incident:** Syed asked "Bagi bio hack yang pro level yang abang sado kena tau pasal mots-c" and later "Nape motc pro bioker suruh pakai skali dgn nad cq10 n magnesium glycinate". Agent dumped a 10-peptide catalog (BPC-157, TB-500, GHK-Cu, Epithalon, Ipamorelin, Dihexa, etc.). Syed's correction: **"Kau sembang ape ni?aku tanya benda lain ka?"**

**Rule:** When user explicitly references a SOURCE ("Probiohacker's protocol", "Dr. X's stack", "Y's recommendation"), deliver THAT SOURCE's protocol. Do NOT dump your own broader knowledge. Syed wants accuracy of attribution, not comprehensive survey.

### PITFALL: Capture image content when Syed shares photos

**2026-08-20 incident:** Syed said "Alaaa da cakap kan barang hari itu x baca ke" — agent asked where he bought his peptides, but he had shared a photo earlier (gateway log msg: "Betul ke benda ni", "Ni je ada" + image) with brand/source info that wasn't captured.

**Rule:** When Syed shares photo/image with text like "Betul ke benda ni", "Ni je ada" — assume the image contains actionable info. Even if you can't read the photo at the time, log the context so future sessions know there was a shared image. Don't ask the same info twice.

### PITFALL: MOTS-c is NOT a pre-workout — it's exercise-mimetic

**2026-08-20 incident:** Syed asked: "dia aku pakia macam pre workout half life dia bape lama?" — initial framing treated MOTS-c like a stimulant pre-workout (timing around workout, "kick" thinking).

**Reality:**
- MOTS-c = exercise-mimetic, NOT stimulant
- Half-life in plasma <1–2h but downstream AMPK effects last longer
- Daily inject pattern, not single-shot "kick" like caffeine
- Timing: morning preferred (avoid insomnia) or pre-workout for synergy with actual exercise

### PITFALL: Insomnia from MOTS-c = timing issue first, not dose issue

Syed reported "x lena x deep" on MOTS-c. Initial assumption was dose-related.

**Reality:**
- Cause: metabolic activation persists into sleep hours, blocks deep sleep by keeping core temperature elevated
- Fix: inject morning (<10am), not pre-workout evening
- Don't suggest dose reduction first — fix timing first

### PITFALL: Semax/Selank are SUBCUTANEOUS for Syed (not nasal spray)

**2026-08-20 incident:** Agent suggested Semax/Selank as nasal spray (the clinical studied form). Syed corrected: "Pepties selang n semak mmh ada cucuk lah" — he uses injectable form.

**Rule:** Default to injectable when discussing with Syed. Russian-developed peptides exist as both nasal spray (clinical) and injectable (grey market). Syed uses injectable.

### PITFALL: SADO group — Syed body ≠ Arif body

**2026-08-20 incident:** Merged Syed's sleep data with Arif's meal ("makan berat → tidur sikit" narrative that didn't exist for either body). Arif's correction: "Aku makan untuk happy. Dua badan yang berbeza hangggg."

**Rule:** In SADO group, health screenshots from Syed = Syed's body. Arif's body = no fitness/calorie-guilt framing ("makan untuk happy"). Never cross-couple two bodies' data into one narrative.

## Compound Quick-Reference

### MOTS-c
- 16 amino acid mitochondrial-derived peptide
- Activates AMPK → upregulates fat oxidation, glucose uptake, ATP production
- Human PK data thin — most studies in mice
- WADA Section 4.4 (metabolic modulator) — banned in competitive sport
- Syed's dose 0.1ml = far below Probiohacker 5–10mg range (conservative)

### NAD+
- 50mg 3x/week = conservative, low side-effect
- 100mg 2x/week = balanced maintenance
- 250mg subq = practical ceiling for regular use
- First 1–3 doses: flushing, mild headache (transient)
- Take AM — energy boost causes insomnia if evening
- Hydrate 500ml before/after
- Subq bioavailability lower than IV (60–70%)
- "Sensitive" individuals may need to start 25mg

### Semax
- Russian-developed nootropic peptide (BDNF upregulation)
- 0.1ml subq standard dose (Syed's dose)
- Cognitive: focus, memory, mental clarity
- Can stack with NAD+ (different pathways)

### Selank
- Russian-developed anxiolytic peptide
- 0.1ml subq standard dose (Syed's dose)
- Anti-anxiety without sedation (unlike benzos)
- Often paired with Semax (focus + calm)

### CoQ10 (Ubiquinol)
- Fat-soluble — MUST take with meal containing fat for absorption
- Ubiquinol form (reduced) more bioavailable than ubiquinone
- 100mg = maintenance; 200mg = therapeutic
- Synergy with NAD+ as electron carrier in ETC

### Magnesium Glycinate
- 400–600mg elemental Mg per day
- Glycinate = best absorbed form, least laxative effect vs citrate/oxide
- Take 30min before bed → calming effect from glycine + Mg
- Mg required for ATP biological activity (Mg-ATP complex)