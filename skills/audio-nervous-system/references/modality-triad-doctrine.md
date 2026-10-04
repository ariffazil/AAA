# Modality Triad Doctrine

> Forged 2026-08-13. Conceptual framework for understanding each modality's failure mode in multimodal systems.

## The Three Modalities & Their Lies

### Image — "I see it, therefore I understand"

Image gives access to *appearance* but rarely *cause*. It projects onto a symbolic subspace where spatial layout ≈ ontological structure. This creates the illusion of comprehension from pattern recognition alone.

**Failure mode:** Seeing ≠ Understanding
- One oil rig photo shows: workers, equipment, scaffolding
- What you DON'T see: reservoir pressure, kick risk, economic decision history, regulatory compliance
- ~90% reality invisible, but image makes brain say "aku dah faham"

**Epistemik cost:** Low. No symbolic decomposition needed. Pattern matching is cheap.

### Audio/Voice — "It feels real, therefore it matters"

Audio enters through pre-linguistic presence circuits — auditory system evolved 200k+ years before vision processing written language. Breath and voice are continuous and time-bound: information lives in the derivative (rate, pause, tremor, latency), not in discrete artifacts.

**Failure mode:** Presence ≠ Validity
- Emotion sounds authentic but context can be wrong
- Urgency feels important but urgency ≠ truth
- Tone conveys physiological state (stress, fatigue) — costly-to-fake signal because physiologically coupled to human body

**Why this matters:** Audio carries BOTH content AND source state simultaneously — multiplexed in one waveform. Text strips the state. Image hides behind appearance.

**Epistemik cost:** Moderate. Partial collapse — superposition maintained until interpreted by listener's amygdala/prefrontal cortex interplay.

### Text/LLM — "It coheres, therefore it's true"

LLMs perform entropy reduction over symbols — comparison, conflict detection, synthesis. This requires traversing wide symbolic spaces. They don't find truth; they maximize plausible coherence.

**Failure mode:** Consistency ≠ Ontology
- LLM chains logic beautifully even on false premises
- Summary feels more coherent than original document → users trust summary more
- "Konistensi simbolik ≠ konsistensi ontologi"

**Why LLMs are most expensive:** Because they try hardest to reduce ΔS in epistemic space. Each good answer involves approximately: Reality → Language → Representation → Comparison → Contradiction check → Synthesis → Language. This is the closest we have to symbolic audit machinery.

**Epistemik cost:** High. Full symbolic decomposition required. Every inference layer compounds uncertainty.

## Mathematical Framing

If we model modalities as projections onto different subspaces:

| Modality | Space Type | Collapse Point | Retained Complement |
|---|---|---|---|
| Image | Spatial eigenstate | Pixel → object recognition | Temporal dynamics, causation |
| Audio | Continuous waveform | Breath prosody → meaning | Physiological state source |
| Text/LLM | Symbolic subspace | Token sequence → coherent thought | Emotional provenance, embodied context |

**Sidecar principle:** `text = projection × state_manifold_discarded`. VoiceState sidecar retains the orthogonal complement so projection loss doesn't become trust loss.

When an agent reads audio-only input, the transcript IS the projection. Without the paralinguistic sidecar (VoiceState), the agent sees what was said without seeing who said it, how they felt saying it, or whether their physiological state contradicts their words.

## Practical Application

For Hermes / I-ARIF design:
1. Never let transcript-only text represent full audio input
2. Always preserve VoiceState alongside transcript
3. Tag all paralinguistic claims [INT] cap 0.70 (F7 HUMILITY)
4. WELL reads VoiceState → reflects only → never gates action (W0)
5. Never manufacture empathy from audio analysis (F9 ANTIHANTU) — measure, don't simulate

## References
- Source session: `/usr/local/lib/hermes-agent/profiles/aaa-hermes/skills/audio-nervous-system/SKILL.md`
- Eureka entry: `audio_as_quantum_superposition_vs_generic_incomplete_info` → RESOLVED
- APEX ruling: 2026-08-13 — quantum framing VOIDED, voice-as-pre-linguistic-presence SEALED
