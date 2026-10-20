---
name: body-composition-assessment
description: "Use when a body photo needs a body-fat verdict."
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Body Composition Assessment

Trigger: torso/physique photos with "body fat?", "sado ka x?", "analyze badan dia", or a coach's verdict the room wants checked. Serves the SADO lane — a number, a consequence, and what to do next, not a lecture and not a prescription.

Companion skills: compound evidence tiers live in `BIOHACK-PEPTIDES`; TRT, labs and prep rules live in `ped-hormone-advisory`. This skill answers only the body read.

## Procedure

1. **Batch every image in one turn.** One `vision_analyze` call per photo, each carrying a *different* clinical question — body-fat range, fat carriage sites, muscle development, skin marks. Sequential single reads waste turns and drift; two photos of the same body must never yield two different ranges.
2. **Put the discipline in the question string.** Ask for estimated range, visceral vs subcutaneous, specific depots (lower abs, flanks, chest), distension, muscle development by group, skin marks. Append "be clinical, no identity guesses" — vision models otherwise volunteer nationality, age and setting.
3. **Report a range plus midpoint.** "13–17%, take 15%." Then three lines of evidence: why the ab outline stops where it stops, which depot is carrying, which muscle group is most advanced. A bare number without the cue it came from is unfalsifiable.
4. **Convert the number into consequence** — kilograms and weeks, not adjectives. Health (soft lower abdomen = subcutaneous, not visceral), stage (physique/bodybuilding lean is 5–7%), visible abs (10–11%).
5. **Ask for the four inputs before any macro math** — weight, height, age, training days per week. Offer once. Never compute intake from a photo.

## Threshold bands (adult male, photo read)

| Band | What shows |
|---|---|
| 20%+ | no abs, softened chest, fuller face and neck |
| 15–18% | upper abs faint, lower abs gone, love handles starting |
| 12–15% | upper abs visible, lower abs soft, delt and bicep shape |
| 10–11% | full abs outline, forearm vascularity |
| 7–9% | striations, serratus, stage lean for most |
| 5–7% | physique/bodybuilding stage condition, not year-round |

Depot order (male): stored lower abdomen → flanks → lower back → chest → arms/face; lost in reverse. Read from the depot that has *lost* definition, not from the total impression. Soft lower abdomen with visible upper abs is subcutaneous, not visceral — firm distension would be the visceral cue. Targets: visible abs 10–11% (~4–6 kg off an 80 kg frame at mid-teens); men's physique stage 5–7% (8–10% of bodyweight, a 12–20 week job). Deficit sizing: 300–500 kcal/day for 0.3–0.5 kg/week; protein floor 1.6 g/kg or the loss skews to muscle; first 1–2 kg is glycogen and water.

## Always-on rules

- **Never open with background.** Verdict on line one, mechanism after.
- **Answer the body before pharmacology.** If the body is trained and sits in the 13–17% band, peptides are not the constraint — say it plainly on the first line. BPC/TB-500 are injury repair, MOTS-c and AOD-9604 are the lowest evidence tiers, GLP-1 is an obesity indication that costs muscle at this body fat. Then the one honest exception that fits: old injury → recovery stack; GH pulse → ipamorelin alone; skin → GHK-Cu topical.
- **The boring answer is the answer**: protein 1.6–2 g/kg, 300–500 kcal deficit, progressive overload, 7 h sleep. State it once, no moralizing, no calorie guilt.
- **Mass vs definition** — never answer "sado ka x?" with one word. Mass = muscle built, visible in a shirt. Definition = what shows, driven by fat. Register: "sado, tapi sado basah" (mass yes, definition no) versus "sado kering". Tie-breaker: same weight and muscle can look ordinary or carved — the difference is the kitchen, not the gym.
- **Nipple and areola are glandular tissue plus smooth muscle, not adipose.** Their size and feel do not change with a cut in a lean man; the fat pad under and around them does. Pseudogynecomastia = fat over a normal gland, resolves with fat loss. True gynecomastia = firm, rubbery, often tender central disc that does not shrink with fat loss. Hand over the self-test — pinch behind the nipple: a rubbery disc that stays put is gland, flat shapeless tissue that slides out of the grip is fat — instead of arguing from feeling.
- **Check a coach's verdict, do not accept or dismiss it.** "Semua fat" is a reading of the fat pad, not of the gland. Say which half is right, then redirect to the strongest group in the photo.
- **No identity work on the person in the frame** — no name attribution, no age or ethnicity guesses.
- **Never narrate the photo back.** He sent it; he does not need the parking garage described.
- **Never merge bodies.** Establish whose body it is before quoting any past data, sleep or meals.

## Photo reads degrade — say so once

Overhead fluorescent (garage, gym, locker room) flattens abs and reads 1–2 points leaner than daylight; a single front shot hides flank and back fat; flexed versus relaxed moves the read more than a week of dieting. One clause of caveat, and never a caveat in place of the answer.

## Pitfalls

- **One image, one range, one turn.** Splitting images across turns produces inconsistent numbers and looks like guessing.
- **At the start of a cut the scale moves and the mirror does not for 2–3 weeks** — lower abs and flanks are last. Say it before he starts, not after he quits.
- **Do not diagnose a lump, pain or asymmetry from a photo.** That is a scan. One line, move on.
- **Register is Penang kampung BM with gym vocabulary left in English** — cut, bulk, deficit, bodyfat, maintenance. No clinical distance, no "as an AI".
