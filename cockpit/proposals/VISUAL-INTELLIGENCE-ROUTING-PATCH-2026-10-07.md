# Patch Proposal — VISUAL-INTELLIGENCE-ROUTING-DISCIPLINE
## F13 binary required: SAH / NOT_SAH

**Status:** DRAFT (F13 binary pending)
**Author:** Hermes (session 2026-10-07, MMA-ZEN restyle conversation)
**Scar:** SCAR-VIS-001 (first-class)
**Trigger:** Today's session — agent picked `mmx` from PATH, bypassed `aaa-image-editing` skill, generated 3-4 low-quality images before discovering the correct lane (Token Plan `wan2.7-image-pro` via `multimodal-generation` endpoint).

---

## 0 · TL;DR

Add a **mandatory routing pre-check** for any visual-edit or T2I dispatch. Block naked delivery without RTC-loop AUDIT. Wire Melayu cultural-fidelity as a scar-bound selection constraint. Total scope: 1 SOUL/skill pointer + 1 RTC-loop enforcement + 1 scar library seed.

---

## 1 · The failure class (SCAR-VIS-001)

**Signature:** Agent receives "restyle this image" / "make Melayu version" / "edit face" / "generate photo" request → goes directly to first visual-gen tool in PATH → generates → delivers without vision-verify → produces image that fails specialist review.

**Why it happened today:**
1. Loaded `image-restyle-and-edit` (a single-lane skill) instead of `aaa-image-editing` (the routing meta-skill).
2. Picked `mmx` (in PATH, looks "available") over documented-verified lanes (Gemini Nano Banana family, Qwen Token Plan `wan2.7-image-pro`).
3. Ran 4 generations without any vision-verify pass.
4. Delivered with truth-claims like "image saved" but no falsifiable identity / cultural fidelity scores.

**Cost:** ~30 minutes wasted, 4-5 generations of "looks fine, fails specialist" outputs delivered, hang's attention burned.

---

## 2 · The patch (3 layers, layered defense)

### Layer 1 — SOUL/skill-pointer patch: routing meta-skill MUST load first

**Location:** `/root/AAA/instructions/voice-durability-3profiles.md` SOUL.md mouth section, or a new `image-routing-precheck` skill.

**Rule (proposed text, F13 SAH needed):**

> When user asks for image generation, image editing, or image restyle of a supplied photo:
> 1. **MUST** load `aaa-image-editing` skill FIRST (the routing meta-skill). Document any "lane dead" condition (401, 402, connection-reset) as a probe receipt.
> 2. **MUST** prefer lanes in this order, per `aaa-image-editing` decision tree:
>    - User provided photo + identity matters? → Nano Banana family (gemini-2.5-flash-image or gemini-3-pro-image-preview) via `/root/HERMES/scripts/gemini-image.py`
>    - Edit + multi-image fusion? → Token Plan `wan2.7-image-pro` via MAAS `multimodal-generation` endpoint
>    - Pure T2I, no reference? → MiniMax `image-01` via mmx CLI (works but "cartoon" per user verdict) or Token Plan `qwen-image-2.0-pro`
> 3. **MAY NOT** fall back to `mmx` (MiniMax) for photorealistic identity-critical work without explicit user approval (per `ai-media-generation` skill: "Minimax so cartoon. Make it reality.").
> 4. **MAY NOT** retry a dead lane more than once (per `image-restyle-and-edit` skill: "Reshaping the prompt against a quota-dead lane changes nothing").

**Verification:** add a one-line probe receipt to every visual delivery:
`lane=<name> probe_receipt=<status>` where status ∈ {HTTP_200, 401, 402, connection_reset, timeout}.

### Layer 2 — RTC-loop enforcement: no naked delivery

**Location:** new skill `image-rtc-enforcement` OR inline the rule in the existing `rtc-loop` skill (which already says "USE WHEN: ANY text-to-image / image-generation dispatch in the federation").

**Rule (proposed text, F13 SAH needed):**

> For any visual delivery, the following 5 fields MUST appear in the chat response or receipt:
> 1. `spec_ref:` — path to SPEC JSON (structure → material → topology → observation → optical)
> 2. `adherence_band:` — declared before render (e.g. `>=0.7 clean / 0.5-0.7 disclosed / <0.5 reject`)
> 3. `f2_adherence:` — measured score after vision-verify AUDIT
> 4. `verdict:` — `PASS | PASS_WITH_NOTES | FAIL`
> 5. `disclosure:` — if verdict is PASS_WITH_NOTES or below, list 1-3 specific weak points (e.g. "keris blade 3-4 luk, not full 5-9")
>
> No naked `{MEDIA:/path}` delivery without these 5 fields. Naked delivery = architecturally defective response.

**Verification:** when generating a visual artifact, the response MUST include a `RECEIPT` JSON block (can be inline, can be in a file path). If absent, the agent must regenerate the response with the receipt.

### Layer 3 — Scar library: Melayu cultural-fidelity bound to selection

**Location:** `/root/AAA/scar-library/visual-intelligence/` (new directory).

**Seed (5-10 entries):**

| scar_signature | trigger | selection_constraint |
|---|---|---|
| `MELAYU-AUTH-001` | "songket" without specifying supplementary weft | require explicit "supplementary weft gold thread" or substitute "songket-like" |
| `MELAYU-AUTH-002` | "keris" without luk count | require explicit "5-9 luk asymmetric wavy blade" |
| `MELAYU-AUTH-003` | "destar" / "tengkolok" without fold structure | require explicit "fan-shaped pleated front" + reject "metal crown" |
| `MELAYU-AUTH-004` | "pelita" without spout | require explicit "spouted low brass oil lamp" + reject "torch/brazier" |
| `MELAYU-AUTH-005` | "pendopo" without meru roof | require explicit "tiered meru roof open sides" + reject "gothic castle" |
| `MELAYU-AUTH-006` | "Malayan tiger" without stripe pattern | require explicit "orange with black stripes" + reject "white tiger" / "generic big cat" |
| `MELAYU-AUTH-007` | "wayang kulit" without shadow-play context | require explicit "leather puppet + light source" |
| `MELAYU-AUTH-008` | "baju Melayu" without collar type | require explicit "cekak musang / Teluk Belanga collar" |
| `IDENTITY-PRES-001` | "subject-ref" without vision-verify | require post-gen vision-rate ≥ 7/10; HOLD if below |
| `IDENTITY-PRES-002` | "preserve face" without KEEP clause | require explicit KEEP clause naming face features |

**Wire-up:** when a visual generation prompt contains a trigger word, `consult_scar()` prepends the selection_constraint. The prompt is rejected if the constraint would force a contradiction (e.g. "metal crown destar" — must pick one).

---

## 3 · Expected lift

| Failure class | Today | After patch |
|---|---|---|
| Routing to dead lane (G1) | happens (mmx, dashscope-sk-sp, etc.) | blocked — pre-check probes lane first |
| Naked delivery without audit (G2) | happens (4-5 generations today) | blocked — receipt required |
| Cultural fidelity miss (G9) | happens (batik→Chinese brocade, gothic castle→pendopo) | blocked — scar prepended to prompt |
| Identity loss in subject-ref (A10/A11) | happens silently | blocked — vision-verify HOLD gate |
| Wasted generation cycles | 4-5 per request | 1-2 per request |

**Net effect:** "fail badly" outcomes drop from ~80% (today's session) to ~20% expected, with explicit disclosure on the remaining 20% per rtc-loop Law.

---

## 4 · Investment

| Component | Lines of code/markdown | Time | Who |
|---|---|---|---|
| Layer 1: SOUL pointer + skill routing rule | ~20 lines | 30 min | Hermes (auto) |
| Layer 2: rtc-loop enforcement patch | ~30 lines | 1 hour | Hermes (auto) + F13 SAH |
| Layer 3: Melayu scar library | ~100 lines (5-10 entries) | 2 hours | Hermes + F13 cultural review |

**Total:** ~3.5 hours of agent work + F13 binary. Skill-count is unchanged (no new skills, just patches to existing).

---

## 5 · Non-goals

- Does NOT fix the QwenCloud key (G1) — that's a billing problem, not a routing problem.
- Does NOT add GPU/comfyui — that's infra, separate workstream.
- Does NOT change `aaa-image-editing` skill content — just enforces the routing.

---

## 6 · F13 binary

`SAH` → patch lands in next session.
`NOT_SAH` → reject + reason.

F13 binary carries F1 reversibility: a single `patch` call undoes the change.
