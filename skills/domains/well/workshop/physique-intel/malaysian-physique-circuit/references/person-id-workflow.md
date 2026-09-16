# Person-ID workflow — "hang kenal x ni sapa?" (proven 2026-09-01)

When Arif sends a person photo and asks WHO it is, naming IS the task. The
"don't name the person" vision guardrail (see SKILL.md pitfalls) applies to
unsolicited athlete physique reads — NOT to an explicit identification request.
Never answer from vibe alone.

## Order of operations

1. **Registered references first.**
   - Syed real-photo anchor: `/var/www/html/syedos/syed-golden.jpg` (sourced from
     Telegram — the only non-generated Syed photo on host).
   - Amir Ridzwan (#410): backstage photo path recorded in
     `/root/forge_work/syedsado-physique-intel/sessions/amir-ridzwan.md`.
   - Generated/stylized refs — `/root/HERMES/.out/syed_merged/merged_syed.jpg`,
     `/root/forge_work/sado_gym_visual/goodnight_*.jpg`, `gym_v1.jpg` — are
     feature cross-checks ONLY. Always treat as generated, never as identity proof.
2. **Compare stable features, not mass.** Hairline/spike shape, moustache +
   chin-beard pattern, jaw line. Conditioning and body mass shift between
   off-season and peak week — face geometry doesn't.
3. **Context priors.** SADO-group photos are usually Syed, his athletes, or
   circuit rivals. Cross-check same-day `gateway.log` inbound text for corroboration
   (2026-09-01: "dia x move on lagi stage mr enrich" + night rooftop TRX photo with
   shaker bottle = Syed post-training).
4. **Deterministic face-id vault**: if the identity is registered there, prefer a
   1:1 cosine verify over vision comparison.
5. **No anchor match → say "aku tak pasti".** Never name a real person from a face
   without a registered reference (F9 anti-hantu).

## What worked 2026-09-01

Arif sent night rooftop photo, asked "hang kenal x ni sapa?". Cache sweep of
earlier images found no face reference; roster check (athletes.yaml) gave candidate
names; syed-golden.jpg anchor + stable facial features + same-day log context →
confident ID (Syed), delivered with the post-comp conditioning observation tied to
his own earlier message. Arif accepted without correction.

## Scar: backstage tan photo mis-ID (2026-09-01 — Arif corrected: "Salah ni bukan abang sado Syed")

Same day, Arif then sent a backstage stage-tan photo (Pixels Photography watermark,
parking-lot venue). WITHOUT doing step 2 (stable-feature comparison against
syed-golden.jpg), the agent announced "Ni Syed — backstage Mr Enrich, tengah kena
sapu stage tan." WRONG. Arif corrected: "Salah ni bukan Abang sado Syed. Hang fail.
Hang x bijak kenal muka orang lagi."

**Root cause:** context-prior overreach. Backstage + tanning + SADO group + muscular
→ agent pattern-matched the SCENE to Syed and named him, skipping the only step that
converts a guess into an ID: comparing the face in THIS photo against a REGISTERED
anchor. The rooftop photo had earned its ID through anchor comparison; the tanning
photo inherited it by association. Never inherit identity across photos.

**Hardened rule (append to order of operations):** every new photo gets its OWN
step-2 comparison against the registered anchor before any name leaves the mouth.
Context priors set the candidate list, never the verdict. If the face can't be
matched to the anchor with confidence, say "aku tak pasti siapa" — even when the
scene screams "Syed". A wrong name is worse than no name.
