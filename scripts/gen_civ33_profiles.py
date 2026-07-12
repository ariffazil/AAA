#!/usr/bin/env python3
"""
gen_civ33_profiles.py — Generate 33 CIV-33 domain atlas profiles.

Physics layer (000-400): What IS — material reality
Math layer (444-700):    What CAN BE — abstract structure
Code layer (777-999):     What WILL BE — executed intent

Each profile includes: name, sigil, citations, axiomatic constraints,
tool preferences (MCP organs), evidence standards, blind spots.
"""

from pathlib import Path
import os

ROOT = Path("/root/AAA/domain-atlas")

# Domain map: layer → {number → (slug, name, sigil, focus)}
DOMAINS = {
    "physics": {
        "000": ("void",          "Void",              "○",  "Pre-existence; the substrate before manifestation; quantum vacuum state"),
        "100": ("monad",         "Monad",             "·",  "Atomic unity; the indivisible; conservation of identity"),
        "133": ("wave",          "Wave",              "∿",  "Vibration; oscillation; frequency-domain phenomena"),
        "200": ("duality",       "Duality",           "☯",  "Polarity; binary opposition; complementarity without contradiction"),
        "233": ("field",         "Field",             "⟿",  "Spacetime; gauge fields; force carriers"),
        "266": ("structure",     "Structure",         "△",  "Crystallography; lattice; symmetry breaking"),
        "300": ("trinity",       "Trinity",           "△³", "Three-fold symmetry; phase transitions; triple points"),
        "333": ("reason",        "Reason",            "λ",  "Pattern recognition; signal extraction; logos"),
        "366": ("complexity",    "Complexity",        "✦",  "Emergence; non-linear dynamics; self-organisation"),
        "399": ("chaos",         "Chaos",             "⚡", "Turbulence; sensitive dependence; deterministic chaos"),
        "400": ("material",      "Material",          "◆",  "Tetrahedral Earth; condensed matter; classical mechanics"),
    },
    "math": {
        "444": ("structure",     "Structure",         "▢",  "Foundational form; axioms; scaffolding"),
        "500": ("proportion",    "Proportion",        "φ",  "Golden ratio; pentagonal symmetry; harmonic ratios"),
        "533": ("transformation","Transformation",    "↦",  "Functions; mappings; morphisms between categories"),
        "555": ("bridge",        "Bridge",            "⊃⊂", "Topology; connectivity; bridges and tunnels"),
        "566": ("dynamics",      "Dynamics",          "∂",  "Calculus; change; differential equations"),
        "600": ("measure",       "Measure",           "∡",  "Quantification; metric spaces; measurement theory"),
        "633": ("probability",   "Probability",       "ℙ",  "Statistics; likelihood; Bayesian inference"),
        "650": ("information",   "Information",       "ℍ",  "Entropy; bits; information theory"),
        "666": ("paradox",       "Paradox",           "∞⁻", "Incompleteness; self-reference; undecidability"),
        "699": ("completeness",  "Completeness",      "□",  "Limiting behaviour; closure; asymptotic structure"),
        "700": ("sabbath",       "Sabbath",           "⊥",  "Foundation; rest; invariant ground"),
    },
    "code": {
        "777": ("forge",         "Forge",             "⚒",  "Construction; building; first-stone commit"),
        "800": ("routing",       "Routing",           "↯",  "Logistics; flow control; message passing"),
        "833": ("validation",    "Validation",        "✓",  "Type-checking; testing; contract enforcement"),
        "850": ("optimization",  "Optimization",      "⊕",  "Algorithmic efficiency; minimisation; lean"),
        "888": ("judgment",      "Judgment",          "⚖",  "Verification; logical adjudication; verdict"),
        "900": ("iteration",     "Iteration",         "↺",  "Loops; recursion; fixed points"),
        "920": ("compilation",   "Compilation",       "→",  "Translation; transpilation; code-as-data"),
        "933": ("deployment",    "Deployment",        "▶",  "Shipping; release; production"),
        "950": ("monitoring",    "Monitoring",        "◉",  "Observability; telemetry; metrics & traces"),
        "977": ("evolution",     "Evolution",         "↝",  "Adaptation; learning; version drift"),
        "999": ("seal",          "Seal",              "■",  "Completion; archival; immutable ledger"),
    },
}

# Citations — canonical references per layer (used as defaults)
LAYER_CITATIONS = {
    "physics": [
        "Heisenberg, W. (1927). Über den anschaulichen Inhalt der quantentheoretischen Kinematik und Mechanik. Zeitschrift für Physik 43, 172–198.",
        "Einstein, A. (1916). Die Grundlage der allgemeinen Relativitätstheorie. Annalen der Physik 354 (7), 769–822.",
        "Boltzmann, L. (1877). Über die Beziehung zwischen dem zweiten Hauptsatze der mechanischen Wärmetheorie und der Wahrscheinlichkeitsrechnung. Wiener Berichte 76, 373–435.",
        "Prigogine, I. (1977). Self-Organization in Non-Equilibrium Systems. Wiley.",
        "Penrose, R. (2004). The Road to Reality. Jonathan Cape.",
        "Laughlin, R.B. (2005). A Different Universe. Basic Books.",
        "Merdith, A.S. et al. (2021). Extending full-plate tectonic models into deep time. Nature Communications 12, 1569.",
    ],
    "math": [
        "Gödel, K. (1931). Über formal unentscheidbare Sätze der Principia Mathematica. Monatshefte für Mathematik und Physik 38, 173–198.",
        "Shannon, C.E. (1948). A Mathematical Theory of Communication. Bell System Technical Journal 27, 379–423.",
        "Kolmogorov, A.N. (1965). Three approaches to the quantitative definition of information. Problems of Information Transmission 1 (1), 1–7.",
        "Mandelbrot, B. (1982). The Fractal Geometry of Nature. W.H. Freeman.",
        "Nash, J. (1950). Equilibrium points in n-person games. PNAS 36 (1), 48–49.",
        "Landauer, R. (1961). Irreversibility and Heat Generation in the Computing Process. IBM Journal of Research and Development 5, 183–191.",
    ],
    "code": [
        "Knuth, D.E. (1968). The Art of Computer Programming, Vol. 1. Addison-Wesley.",
        "Dijkstra, E.W. (1968). Go To Statement Considered Harmful. CACM 11 (3), 147–148.",
        "Lamport, L. (1998). The Part-Time Parliament. ACM TOCS 16 (2), 133–169.",
        "Hoare, C.A.R. (1969). An Axiomatic Basis for Computer Programming. CACM 12 (10), 576–580.",
        "Borg, A. (2003). Open Source Development with CVS, 3rd ed. Paraglyph.",
        "Nakamoto, S. (2008). Bitcoin: A Peer-to-Peer Electronic Cash System. self-published.",
    ],
}

# MCP organ preferences per layer
ORGAN_PREFS = {
    "physics": ["geox", "well"],
    "math":    ["wealth", "well"],
    "code":    ["arifos", "aforge", "aaa-gateway"],
}

# Blind spots per layer
BLIND_SPOTS = {
    "physics": "Consciousness claims (F9). Reductionism risk (mistaking model for reality). Confirmation bias on visualisation artefacts.",
    "math":    "Gödel ceiling — every formal system has true statements it cannot prove. Numerical precision theatre. Mistaking elegance for truth.",
    "code":    "Sovereign veto bypass. Mutable infrastructure drift. Premature optimisation. Speed claimed without measurement.",
}

# Evidence standards per layer
EVIDENCE = {
    "physics": "Reproducible measurement. Multi-source corroboration. Falsifiable hypothesis before claim. SI units or explicit conversion.",
    "math":    "Symbolic proof or computational verification. Counterexample before generalisation. Numeric check before symbolic claim.",
    "code":    "Hash-changed artifact (VAULT999 seal). Test coverage on the changed surface. Determinism check (rerun = same result).",
}

# Axiomatic constraints per layer
AXIOMS = {
    "physics": "Conservation (mass, energy, momentum). Thermodynamics (ΔS ≥ 0 in closed system). Causality (no retroactive effect).",
    "math":    "Non-contradiction. Identity (A = A). Excluded middle (only within decidable domains). Bivalence held where Gödel does not bite.",
    "code":    "F1 AMANAH (no irreversible mutation without seal). F2 TRUTH (every claim has evidence). F11 AUDIT (every action sealed). F13 SOVEREIGN (Arif holds final veto).",
}


def render_profile(layer: str, num: str, slug: str, name: str, sigil: str, focus: str) -> str:
    citations = LAYER_CITATIONS[layer]
    return f"""# Domain {num} — {name} ({slug})

> **Sigil:** {sigil}
> **Layer:** {layer}
> **Question:** "{("What IS?" if layer == 'physics' else "What CAN BE?" if layer == 'math' else "What WILL BE?")}" — {{
  *physics*: material reality, what exists independently of observation,
  *math*:    abstract structure, what is provably possible,
  *code*:    executed intent, what will exist after we build it,
}}[domain **{layer}**]

---

## Focus

{focus}

---

## Canonical Citations

""" + "\n".join(f"{i+1}. {c}" for i, c in enumerate(citations)) + f"""

---

## Axiomatic Constraints

{AXIOMS[layer]}

---

## Tool Preferences (MCP Organs)

""" + "\n".join(f"- `{o}` — primary reasoning substrate" for o in ORGAN_PREFS[layer]) + f"""

For all domains: **`arifos`** governs, **`aaa-gateway`** routes, **`aforge`** executes.

---

## Evidence Standards

{EVIDENCE[layer]}

---

## Blind Spots

{BLIND_SPOTS[layer]}

---

## Routing Rule

> When this domain is invoked, defer to the `arifos` kernel for constitutional
> gating before answering. Every claim must carry an evidence tag (OBS / DER / INT /
> SPEC) and a confidence cap ≤ 0.90.

*Forged under CIV-33 orchestration · 2026-07-12 · domain-atlas/{layer}/{num}/*
"""


def main():
    written = 0
    for layer, domains in DOMAINS.items():
        for num, (slug, name, sigil, focus) in domains.items():
            target = ROOT / layer / num / "profile.md"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(render_profile(layer, num, slug, name, sigil, focus))
            written += 1
    print(f"✓ Wrote {written} domain profiles under {ROOT}")


if __name__ == "__main__":
    main()