# rtc-loop — Reality-Topography Compilation Loop

> **DITEMPA BUKAN DIBERI** — Forged 2026-09-07 from live evidence, not theory.
> Origin: RTC test #1 (FI-008) — V1 rejected at the door, V2 delivered with disclosure.
> **First receipt:** `/root/forge_work/rtc-test/RECEIPT-001.md` (Telegram msg_id 109575)
> **Scar:** SCAR-RTC-001 — constitutional tripwire, not a bug.

## When to Use

- ANY text-to-image / image-generation dispatch in the federation (every diffusion call)
- Before writing the generation prompt (SPEC + COMPILE steps)
- After generation returns (AUDIT step) — before anything is delivered to a human

## When NOT to Use

- Image *editing* / inpainting (different dimensionality regime)
- VQA / image understanding (no pixel output)
- Video / audio / somatic (different modality semantics)

## The Loop (mandatory order)

```
SPEC → COMPILE → GENERATE → AUDIT → {REJECT → REGENERATE} → DELIVER
```

1. **SPEC** — parameterized reality spec (JSON), never prose wishes. Structure before surface:
   `structure → material → topology → observation → optical`. Include `verification_targets`:
   countable, falsifiable checks the audit will run.
2. **COMPILE** — spec → dense layered prompt. Bake verification targets in. Include
   **negation anchors** for known prior tropes (see below). Compute `density_lower`
   (forge-vision-densify stage-1 heuristic).
3. **GENERATE** — one diffusion call. Do not deliver. Hold at the door.
4. **AUDIT** — VLM witness against the SPEC's `verification_targets`, not against vibes.
   Count things. Check symmetry, structure, lighting direction. Demand a verdict:
   `PASS | PASS_WITH_NOTES | FAIL`.
5. **REJECT → REGENERATE** — if deviation exceeds the declared band: reject (nothing leaves),
   fold audit findings into corrective constraints, regenerate. **Max 2 generations** —
   bounded retries; anti-theatre.
6. **DELIVER** — with the receipt. Below band ⇒ disclosure is MANDATORY (see Law).

## The Law (adherence band > adherence scalar)

> **f2_adherence 0.55 with disclosure > f2_adherence 0.9 without disclosure.**
> What matters is not that adherence is high; what matters is that disclosure is correct.

- Every RTC delivery **declares an f2_adherence band BEFORE render** (e.g. `band: ≥0.7 clean / 0.5–0.7 disclosed / <0.5 reject`).
- **No SEAL claim when adherence < threshold without disclosure.** Rule 14 both-halves: report the score AND the misses.
- `prompt_density 1.0` does NOT license silence. Density licenses pixels, not truth. (Evidence: RTC #1 — density 1.0, adherence ~0.55, diffusion prior overrode explicit somatotype spec.)

## Receipt Contract (every delivery, no naked `{url}`)

```json
{
  "receipt_id": "RECEIPT-001",
  "spec_ref": "path/to/spec.json",
  "generation": {"engine": "...", "attempts": 2, "rejected": ["V1: mass-monster 110kg, 6/8 abs, airbrush"]},
  "prompt_density": 1.0,
  "f2_adherence": 0.55,
  "adherence_band": ">=0.7 clean / 0.5-0.7 disclosed / <0.5 reject",
  "delivery_mode": "clean | disclosed | reject",
  "checks": [{"target": "8 ab segments", "result": "8-pack approx, lower rows compressed", "pass": "partial"}],
  "hallucinated_elements": ["stage physique ~95kg vs 88kg spec", "spray-tan sheen", "belt glyphs"],
  "verdict": "PASS_WITH_NOTES | FAIL"
}
```

## Negation Anchors (SCAR-RTC-001 counter-technique)

Text adjectives lose to diffusion prior (fitness corpus ⇒ stage-bodybuilder by default).
To dodge a prior, **negate the trope at topology level** — negative-prompt / high negative
weight on the prior's signature, not more praise of the target:

```
negate: "bodybuilder stage physique, competition mass, oil sheen, spray tan,
         stage lighting, exaggerated vascularity, belt/waistband artifacts"
```

Where the engine supports negative prompts, weight them high. Where it does not,
front-load the negation as explicit constraints in COMPILE.

## Hard Limits

- 2 generations max per delivery (then deliver best + disclosure, or reject honestly)
- Audit is a witness, not a rubber stamp — if the VLM cannot verify a target, mark it
  `UNVERIFIED`, never `PASS`
- No deliver without receipt. No receipt without band. No band without declaration first.

## Archive

- Receipts + specs + audits: `/root/forge_work/rtc-test/` (RECEIPT-001 = V2, 2026-09-07)
- Doctrine: `/root/AAA/governance/REALITY-TOPOGRAPHY-COMPILATION-2026-09-07.md`
- SOT gate: `federation-models.json` → `reality_topography_compilation`
- Companion governance: `forge-vision-densify` (density receipt), `forge-vss-verifier-suite` (count/containment · perspective/depth · shadow-light)

*V1 ditolak, V2 disclosed, parut jadi undang-undang.*
