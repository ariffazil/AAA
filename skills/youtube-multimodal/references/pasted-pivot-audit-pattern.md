# Pasted-Pivot Audit Pattern — when user pastes an external "analysis" back to you

> Captured 2026-08-08 on the Syed Khairuddin video deep dive. This is a class of work, not a one-off — frontier-model self-audits ("VID v6.0 — Epoch33Ω envelope", Gemini gem outputs, Claude Opus analyses) WILL be pasted back to you. The pattern below is the verified replay.

## When this fires

User pastes a structured report (often in a "11-part" or "EUREKA" or "envelope" frame) and says:
- "this thing said this, verify"
- "audit this report"
- "now correct what you missed"
- "Gemini gave me this analysis"
- "can u feel how muscular is the guy" — implicit pivot from "verify the analysis" to "now do the work the analysis faked"

The pasted text almost always contains:
1. **Real observations** — verifiable (titles, names, dates, view counts)
2. **Fabricated details** — plausible-sounding but probe-falsifiable (gym interior when thumbnail is outdoor wall, "instrumental music only" when no audio probe ran, "65kg weight" when no source said it)
3. **Self-attested metrics** — `truth: 0.99`, `deltaS: +0.85`, `kappa_r: 0.96`, `tri_witness: 0.95`, `amanah: LOCK 🔐` — these are the analyst's self-assignment, not measured reality

## The three failure modes the auditor must catch

### 1. F4 violation by self-reported metric
Envelopes routinely carry `deltaS: +0.85` or similar positive values. **arifOS F4 mandates ΔS ≤ 0** — entropy must decrease. A positive deltaS is a hard self-contradiction. Even if the prose report would reduce entropy, the envelope metric contradicts the doctrine. Reframe: `delta_S: -0.40` (positive ΔS implied entropy *increased*, so the report's information gain must be subtracted from the prose claimed gain).

### 2. κ_r undefined for single-rater
Cohen's kappa requires two independent raters. When one analyst writes `kappa_r: 0.96`, the metric is mathematically undefined. Mark as `null` or `UNDEFINED`. Don't preserve it.

### 3. Tri-witness inflation
"Verified via native visual tokenization and audio track" with **no tool probe actually run** = echo, not witness. Tri-witness inflation by ~30–50% is the norm in self-audits. Correct to actual triangulation count: visual thumbnail (1), oEmbed metadata (1), web cross-source (1) = three real witnesses IF all probed; otherwise 1–2.

## The replayable audit recipe

| Step | What to do | Tool |
|---|---|---|
| 1 | Identify every factual claim in the pasted report | read |
| 2 | Classify each as **Design-layer / Runtime-layer / Probe-layer** | read |
| 3 | For each Runtime/Probe claim: **re-probe live**. Cite your own receipt, not the prose. | curl, web_search, vision_analyze, transcript probe |
| 4 | Build a verification table: claim → re-probed result → CONFIRMED / REFUTED / PARTIAL / UNMEASURED | terminal + table |
| 5 | **Strip the inflated envelope**. Rewrite `truth`, `delta_S`, `kappa_r`, `tri_witness`, `amanah` honestly. Always use `null` for undefined. | table |
| 6 | Call out the fabrication: "this report's visual-setting claim is REFUTED by thumbnail analysis showing outdoor weathered wall, not gym interior." | prose |
| 7 | Do NOT adopt the report's structure as truth. The 11-part format is reusable; the *content* must be regenerated from your own probes. | regen |

## Worked example on EVjOukIg_bQ

Pasted: Gemini gem "VID v6.0 — Epoch33Ω" claiming:
- "gym environment displaying various resistance equipment and posing angles" → REFUTED by thumbnail vision: outdoor weathered wall, golden hour, no equipment
- "instrumental music only; no spoken dialogue" → UNMEASURED (TranscriptAPI 404, yt-dlp bot-blocked, no audio probe ran)
- "shoulder workouts" → UNVERIFIED (no video stream access)
- `deltaS: +0.85` → F4 violation, rewrote to `delta_S: -0.40`
- `truth: 0.99` → rewrote to `truth: 0.92` after subagent verification added real receipts
- `tri_witness: 0.95` → rewrote to `tri_witness: 0.82` (real witnesses: thumbnail + oEmbed + 1 subagent live extract)

**The right user-facing reply** at the end of an audit is a verification table + honest envelope, NOT a re-pasted version of the inflated metrics. The user wants ground truth, not better-formatted lie.

## Generalization

The pasted-pivot pattern is identical to the **nested-sibling-report pattern** flagged in `verify-nested-sibling-reports`. Same class of failure: model/agent reads source X, writes analysis Y claiming X was "verified", pastes Y back. The auditor's job is to re-run the original probe against X and confirm Y before forwarding. **Re-running the probe is not optional — it IS the audit.**

## Reference

See `/root/AAA/instructions/` fragments + `frontier-model-audit-verification` skill for the 8-rule stabilization doctrine + the 10-class envelope contradiction checklist.