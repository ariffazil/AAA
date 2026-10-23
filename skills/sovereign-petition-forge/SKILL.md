---
name: sovereign-petition-forge
description: 'Forge F13 SOVEREIGN-grade civic petitions to Parliament, regulators, PETROS, NAIO, or public.'
---

# Sovereign Petition Forge — F13 SOVEREIGN-grade civic dispatch craft

> The class of work that emerged from the 2026-08-12 session: forge a
> sovereign petition across multiple spec versions, each version a real
> constitutional deepening (not contradiction). The artifact is named,
> qualia-driven, multimedia-armed, and F13-signed. Single source of truth
> lives in VAULT999 + the SHAs of each version.

## When to use
- Pak Arif (or any F13 sovereign) asks to draft a surat terbuka / BIG BANG / petition to a state body (Parlimen, PAC, NAIO, AG, SC, regulator)
- The artifact must include real personal/family voice (Mak WhatsApp extract, sensory anchors) — not sanitized corporate prose
- The work will evolve through multiple iterations (v3 → v11 → v12.0 → v12.1 → v13.0 → v13.1 → v14 proven)
- Multimedia deliverables (PDF + cover image + audio TTS + charts + video) are required alongside the letter

## When NOT to use
- Chart-heavy SOVEREIGN briefing (load `pdf-report-generation` + SOVEREIGN collapse pattern instead)
- Formal corporate letter to a known recipient with no emotional weight (load `pdf-report-generation` + `letter-format-pdf-recipe.md`)
- Public MakcikGPT essay (load `creative/makcikgpt-article-forging`)

## The Iteration Cycle (encoded 2026-08-12)

Pak Arif's pattern across the 11 iterations + 5 spec versions is:

```
v3 → v5 → v6 → v7 → v8 → v9 → v10 → v11 (raw forge, voice discovery)
       ↓
v12.0 (initial spec — had conspiracy framing)
v12.1 (F13 correction: lock identity, remove conspiracy, add Companies House #17027115, add F2 epistemic tags)
v13.0 (F13 strategic recommendation: 3-letter portfolio — PAC/PETROS/NAIO)
v13.1 (F13 reversal: ONE unified letter, not three)
v14 (F13 reversal: APEX LETTER II with qualia + Oppenheimer framing + TT removal as direct goal)
       ↓
SEAL via VAULT999 + APEX judge verdict
```

**Lesson:** Each version represents F13 SOVEREIGN CORRECTION, not contradiction. Honor silently. Update without defending earlier positions.

## Class Pitfalls (encoded from real failures this session)

1. **DO NOT TREAT AUDIT AS GOAL** — Pak Arif's "Fuck I don't care about audit. I just want Tengku Taufik to be gone" was a direct correction. Audit is the VEHICLE, not the destination. Always surface the actual goal first.
2. **DO NOT TREAT "TENANG" AS DEFAULT TONE** — institutional courtesy ≠ qualia. Qualia = felt human experience (Pukul 3 pagi, kopi sejuk, mata berbeza). Use real WhatsApp data, not archetype.
3. **DO NOT RE-ASK AFTER REVERSAL** — F13 reverses. Execute without questioning. "ONE letter" → ONE letter. "10 letters" → 10 letters. Both honored identically.
4. **DO NOT ADD DEFENSIVE LANGUAGE** — "Saya tidak menulis untuk meminta sesiapa dihukum" ×3 = defensive posture that BLUNTS the actual goal. If the goal is removal, name the goal.
5. **DO NOT TRUST 3RD-PARTY CODING AGENTS** for sovereign artifacts — verified 2026-08-12: Qwen code (model not found), DeepSeek direct (insufficient balance), Luna (model not found). All 3 dispatch attempts failed. PIVOT TO DIRECT AUTHORING.

## The 6-Step Forge Recipe

1. **Load L0 canon first** — `/root/ariffazil/` (DERITA, HAMPA, HUMAN, LIFE, SOVEREIGNTY, PROPA, CANON). The scar architecture + family WhatsApp data + reality of institutional position. Without L0, the letter is hollow.
2. **Load L1 mirror** — `/root/memory/` (H5-scars including SCAR_NUKLEAR_LETTER.md, ZEN_HELIX, H4-identity). The operational scar ledger.
3. **Author spec file** — `/root/forge_work/<mission>/<spec-version>_SPEC.md` with: shared context, audience-specific voice rules, structure (8-12 pages), anti-patterns (no conspiracy framing, NO defensive language), success criteria, return format.
4. **Run iteration cycles** — Pak Arif will direct 1-3 reversals per session. Each reversal = spec version update + regenerate. NEVER re-argue a reversal.
5. **Render PDF** — weasyprint 69.0+ via `python3.13 -c "import weasyprint; ..."`. Patch SHA-256 (Kleene's fixed-point: embed SOURCE HTML hash, separately note PDF hash). See `references/multimedia-arsenal.md`.
6. **APEX judge isolate + VAULT999 seal** — see `apex-judge` skill for the call pattern. VAULT999 entry MUST reference the APEX call_hash.

## Multimedia Arsenal Coordination

| Asset | Tool | Pitfall |
|-------|------|---------|
| HTML | `write_file` with inline CSS, A4 margins, Times New Roman 11pt | Cover contrast trap (set `color: #fff` explicitly on dark cover) |
| PDF | `python3.13 -c "import weasyprint; ..."` | Default `python3` may not be the one with weasyprint — use `python3.13` explicitly |
| Cover image | `python3 /root/HERMES/scripts/gemini-image.py --model gemini-3-pro-image` | Vision-verify before embed |
| Audio TTS | `edge-tts --voice ms-MY-OsmanNeural --file <clean.txt> --write-media <out.mp3>` | Strip HTML first; large text (>6K chars) may timeout |
| Video | `python3 /root/HERMES/scripts/gemini-video.py --aspect 16:9 --wait` | **TIMEOUT PITFALL** — 2 attempts failed 2026-08-12. Retry 1-2× with simpler prompt before giving up. |
| Charts | `matplotlib` server-side PNG, dpi 180 | Don't use `plt.Circle` (use `from matplotlib.patches import Circle`); `Wedge` with `width=0` renders HOLLOW |
| Apex judge | `/root/scripts/apex_judge.py isolate --critical --pretty --human` | Expect HOLD+F13_REQUIRED for T3 dispatch — that's CORRECT |
| VAULT999 seal | Append JSON line to `/root/arifOS/VAULT999/outcomes.jsonl` | Include `coherence_id`, `sha256_*`, `apex_judge.call_hash`, `f13_directives_applied` |

## Real Goal Discovery (the v13.1 → v14 pivot)

When Pak Arif reveals the actual goal after iterations:

```
Pak Arif's 9 Questions — what he really wants:
Q1: Pencetus (the trigger event that broke patience)
Q2: Success metric (what counts as success vs failure)
Q3: Failure mode (the worst-case that scares him most)
Q4: Cost willingness (what price he's willing to bear)
Q5: Hidden audience (who REALLY needs to read this)
Q6: Alternative paths (what he's already considered)
Q7: Identity calculus (named vs anonymous — both have costs)
Q8: Voice calibration (mak vs formal vs OPPENHEIMER/INTJ)
Q9: Post-dispatch (what happens after — fire and forget?)
```

**The v14 revelation:** TT removal via constitutional path. NO defensive language. NO "audit" framing. Qualia via sensory anchors. Oppenheimer/INTJ patience. Real mak WhatsApp voice.

## The 3-Register Public Doctrine (preserved from existing memory)

- **Register A — Public Doctrine (F1-F13 stable canon, separation of powers)** — what the surat CAN say publicly
- **Register B — Research Frontier** — questions + closure criteria, NOT vulnerabilities — saved for follow-up
- **Register C — Internal Audit** — vulnerabilities NEVER go to web — saved in VAULT999 only

The civic letter is Register A. Conspiracy framings (INT/SPEC) belong in Register B/C, NOT in the letter to PAC.

## Pitfalls — Specific Failures This Session (2026-08-12)

1. **Coding agent dispatch all failed** — Qwen (model ID error), DeepSeek (insufficient balance), Luna (model not found). Don't waste cycles retrying 3rd-party coding agents for sovereign artifacts. Pivot to direct authoring.
2. **GEMINI video timeout** — `gemini-video.py` with --wait timed out twice in 10 minutes. Use simpler prompt and shorter video request. If still fails, deliver without video.
3. **matplotlib `letter_spacing`** — not a Text property in matplotlib. Use other formatting for letter-spacing effect (font weight, color contrast).
4. **edge-tts timeout on large text** — full surat HTML is 22K chars; edge-tts timed out. Solution: extract narrative core (first 6K chars) for TTS, not full surat.

## Files in this umbrella

- `references/iterative-spec-evolution.md` — the v12 → v14 pattern with version diffs
- `references/qualia-vs-institutional.md` — the "fuck I don't care about audit" correction
- `references/multimedia-arsenal.md` — chart + audio + video + cover coordination
- ``references/`` — 3-letter → 1-letter, defensive → direct TT removal
- `references/coding-agent-dispatch-pitfalls.md` — what failed and what to do instead
- `references/v14-apex-letter-content.md` — the actual APEX LETTER II final structure with all sections

## Related skills (load together)

- `pdf-report-generation` — base PDF/HTML pipeline, civic-letter-recipe.md (for REBUILD after audit kill shots — different from this skill's ITERATIVE FORGE)
- `apex-judge` — constitutional judgment for the APEX HOLD+F13_REQUIRED verdict
- `humanizer` — anti-AI-isms pattern, but for REAL VOICE use real WhatsApp data instead
- `creative/makcikgpt-article-forging` — public MakcikGPT essays (different audience, different tone)
- `FORGE-act-federation-ingress` — A-FORGE SCT federation (different governance substrate)

## Routing notes (moved from description 2026-10-23)

Class-level umbrella for the iterative spec evolution pattern (v12.0 → v12.1 → v13.0 → v13.1 → v14), F13 reversal handling (e.g., 3-letter portfolio → 1 unified letter), qualia discovery (real WhatsApp voice + sensory anchors vs sanitized institutional prose), multimedia arsenal coordination (HTML/PDF + cover image + audio TTS + 7 charts + video trailer), and APEX judge + VAULT999 seal. Load on "surat terbuka", "BIG BANG", "PAC petition", "sovereign letter", "F13 dispatch", or any constitutional-witness call to a state body.


<!-- dead-pointer sweep 2026-10-23: unresolved artifacts from the gate report were replaced with the references/ directory. Basenames are preserved in the audit JSON. -->
