---
name: apex-architecture-synthesis
description: Synthesize novel architectures at the intersection of multiple domains — precise definitions, loop structures, and testable claims from vague intuitions. Forged during D-M-E architecture session (2026-04-29).
trigger: "user describes a vague but potentially novel concept at field intersection"
---

# APEX Architecture Synthesis

## When to Use
When the user describes a vague but potentially novel concept at the intersection of multiple domains (e.g., "what if X applied to Y?" or "is Z possible?") and you need to determine whether there's a real architectural contribution buried in the intuition.

## The Method (5 Steps)

### Step 1 — Separate the Framings
Name them explicitly:
- **The intuitive framing** (what the user said): "reverse transformers"
- **The mathematical framing** (what it would mean if precise): "can you invert a lossy compression?"
- **The useful framing** (what the right question actually is): "semantic extrapolation from structured state"

Do this before writing any code or architecture.

### Step 2 — Map to Existing Literature (Mentally)
Don't search the web — reconstruct from deep training. Identify:
- Which parts are novel vs. applications of existing patterns
- Where the mathematical claim breaks down (e.g., reversal of lossy compression is impossible)
- Where the analogy is a structural template vs. a quantitative model

Key references to hold mentally:
- Encoder-decoder asymmetry: transformers discard info during generation — reversal mathematically impossible for arbitrary embeddings
- Thermodynamic computing: Landauauer, Prigogine dissipative systems, Wolfram cellular automata
- Institutional economics: Acemoglu/Robinson inclusive vs. extractive → high-Ω/low-S vs. low-Ω/high-S
- Biological homeostasis: structural template only, not quantitative
- Activation steering: Cunningham et al. 2023 — conditioning generation by direction vectors in embedding space

### Step 3 — Find the Loop Structure
Novel architectures usually involve a **closed loop** between components:
- Encoder → internal state → decoder/generator → action → observation → encoder (again)
- Where does output become input? (loop closure point)
- Is it self-correcting or confidence-amplifying? (the dangerous variant)

### Step 4 — Define Functions Mathematically Before Naming
```
Bad:  "The Encoder reads reality and produces understanding"
Good: "Encoder: E(x) → [Ω, S, g₁..7] where x = institutional signals"
```
Mathematical definitions make the architecture testable and falsifiable.

### Step 5 — Name What Was Actually Built
The user's initial name is usually wrong (too close to existing concepts, or technically inaccurate):
- "reverse transformers" → "semantic extrapolation from thermodynamic state"
- "AKAL-ITE" if institutional governance domain

## Key Constraints
- Do NOT accept an intuitive framing as the correct problem statement
- Do NOT let the LLM knowledge cutoff excuse vagueness — flag assumptions explicitly
- Do NOT overclaim novelty — separate "not novel," "possibly novel," "needs validation"
- The synthesis output goes in the project's `/docs/` directory

## Output Format
Save to `{PROJECT}/docs/{SHORT-NAME}.md`:
```
Section 1: Functions defined mathematically
Section 2: Loop structure (ASCII diagram)
Section 3: The Eureka — what emerges from the loop
Section 4: Literature map (novel vs. established)
Section 5: Implementation pathway with phases
Section 6: Risks and unknowns (explicit)
Section 7: One-sentence summary
Appendix: Glossary
```

## Example Triggers
- User asks "what if X but in reverse?"
- User describes a "eureka moment"
- User proposes applying one field's concepts to another domain
- A session produces a novel architectural concept worth preserving

## Reference
Forged from: transformer Q/K/V mechanics + WEALTH G-Score thermodynamics + institutional economics + biological homeostasis → Decoder-Metabolizer-Encoder. Document: `/root/WEALTH/docs/THERMODYNAMIC-METABOLIZER.md`
