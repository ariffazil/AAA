# Voice Physics Invariants — Canonical Reference

Source: Arif (F13), 2026-08-14 22:24-22:26 MYT
Purpose: Grounding layer for all voice synthesis, corpus design, and fine-tuning strategy.
Status: SEAL ratified. Evidence/Interpret/Seal separation enforced.

---

## SEAL (Canonical Invariant)

```
Identity ≈ Airflow ⊕ Oscillation ⊕ Resonance ⊕ Information
```

Teks sahaja tidak membawa identiti.
Audio sahaja tidak membawa makna.
Corpus yang disahkan manusia menyimpan kedua-duanya serentak.

---

## EVIDENCE (Physics — Falsifiable)

Source-Filter Model: Voice(f) = Source(f) × Filter(f)

- Source = vocal fold oscillation → f0 (pitch, gender)
- Filter = vocal tract resonance → F1/F2/F3 (vowel, accent, dialect)
- Source and filter are largely separable (I5)
- f0 ∝ √(k/m) — tension/mass ratio determines pitch (I2)
- Harmonics fn = n·f0 — integer multiples, must be preserved (I3)
- Formants Fn ∝ 1/L — tract length determines vowel identity (I4)
- Energy conservation: P_acoustic ≤ P_airflow (I1)

References:
- voicescience.org/lexicon/source-filter-theory/
- phys.unsw.edu.au/jw/voice.html
- scienceinsights.org/what-is-the-source-filter-theory-of-speech/

---

## INTERPRET (Vault Mapping — Hypothesis, Evidence-Grounded)

| Layer | Physical | Human Perception | Corpus Label |
|-------|----------|-----------------|-------------|
| Airflow | Breath mechanics | "hidup" | breath_present: bool, breath_ms: float |
| Oscillation | f0, jitter, shimmer | "ada perasaan" | f0_mean: Hz, f0_range: Hz, emotion_class: str |
| Resonance | Formant structure | "orang ini siapa" | dialect_class: str, code_switch_ratio: float |
| Information | Intent, prosody, entropy | "dia nak cakap apa" | intent: str, entropy_band: low|mid|high |

Uncanny valley as identity mismatch:

```
Identity_expected ≠ Identity_observed
```

Not because text is wrong, but because identity layers are inconsistent.

---

## VOCAL FOLD OSCILLATION (Physics Detail)

Female voice: higher f0 → harmonics spaced further apart → vocoder needs
32-64 independent spectral channels to resolve upper formants (F2, F3, F4).
Legacy vocoders fail here → metallic artifact on female voices.
Male voice: lower f0 → harmonics closer → easier for vocoders → "passable".

---

## INFORMATION-THEORETIC

```
H(speech) ≠ 0 AND H(speech) ≠ H(noise)
```

Speech occupies middle entropy band. "Rasa" lives inside this entropy:
micro-pauses, breath intakes, failure grammar, emotional prosody.

When AI flawlessly executes physics without high-entropy organic imperfections,
prediction error in human brain → evolutionary avoidance → "hantu" response.

---

## CORPUS ARCHITECTURE (from Identity Invariant)

Previous model: audio → text (one-way extraction)
Current model:

```
waveform → meaning (bidirectional)
audio + transcript + intent + human verification
```

Each sample = one observation of a complete human state.
Not a recording. A measurement of Airflow × Oscillation × Resonance × Information.

---

## SCALE INFERENCE

Identity ≈ Constant across sentences → model learns identity once, generalizes.
F5-TTS fine-tune needs 1-10 hours because identity is low-dimensional constant.
BUT: 3 minutes is NOT enough for full identity estimation.

3 minutes is enough to begin measuring:
- pitch distribution → partial Oscillation
- pause distribution → partial Airflow
- speaking rate → partial Information
- discourse rhythm → partial Information
- lexical preference → partial Information

Full identity estimation requires:
```
VoiceIdentity = (BreathPattern, PitchDynamics, FormantProfile, InformationFlow)
```

Airflow and Resonance require more data than Oscillation and Information.
The vault grows from partial measurements toward full identity.

---

## THESIS

Audio dump dan dataset besar tidak semestinya membawa kepada suara yang terasa hidup.
Sejumlah kecil rakaman yang mempunyai identiti, konteks, dan verifikasi
boleh menjadi jauh lebih bernilai.

This validates the micro-loop strategy against the "National Speech Corpus" approach:
100,000 hours undifferentiated audio ≠ small, labeled, human-verified corpus.
Quality of labels > Quantity of hours.
