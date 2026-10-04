# Lane-Aware Cron Prompts — Reference

Companion to SKILL.md "Lane-aware cron prompts — SADO/group audience pattern" section. Verified against live deployments 2026-08-11.

## Why this reference exists

Group-targeted cron jobs (SADO, AIA, any public chat lane) require a structurally different prompt than DM-to-Arif human intel briefs. The differences are subtle but consequential — wrong shape = noise, leaks, or workflow blocks.

## Verified reference jobs (live)

| Job ID | Name | Deliver | Schedule | Owner |
|---|---|---|---|---|
| `9eddcab58b5c` | sado-physique-radar | telegram:-1003815535761 | `0 22 * * 0` Ahad 22:00 MYT | Arif (consolidated from iron-radar) |

Spec source: `/usr/local/lib/hermes-agent/profiles/aaa-hermes/cron/jobs.json` (gateway canonical registry).

## The 4 mandatory blocks of a group-targeted prompt

### Block 1 — Lane card preamble (FIRST in prompt)

```
═══════════════════════════════════════════════════════
LANE CARD — emitted FIRST in every output
═══════════════════════════════════════════════════════
[LANE:arif] Muhammad Arif bin Fazil
Authority: SOVEREIGN
Capabilities: FULL

CAPABILITY MAP (use what you have):
- IMAGE GEN: /root/HERMES/scripts/gemini-image.py (Gemini 3 Pro Image default)
- VIDEO GEN: /root/HERMES/scripts/gemini-video.py
- PDF: weasyprint from HTML source
- CHARTS: matplotlib via trading-screenshot-analysis skill
- IMAGE EDIT: gemini-image.py --image ref
- TTS: edge-tts ms-MY-OsmanNeural / MiniMax text_to_audio
Never say "I cannot" — check this map first.
```

Rationale: when cron fires in a fresh session with empty context, the LLM has no memory of what tools exist. Capability map = contract, spelled by exact command path. Without it, the job either invents capabilities (F9 violation) or declines tasks it could do.

### Block 2 — Governance ladder

```
GOVERNANCE LADDER:
- in-chat output (Telegram): auto, reversible, in-chat
- external publish / cron / web: apex-judge isolate FIRST
- money: heavy judge + F13 consent
- self-modification: proposal → apex-judge → git commit
```

Rationale: every output is a potential external surface. The job must know when to invoke apex-judge and when it doesn't need to.

### Block 3 — Doctrines (F2/F4 binding)

```
DOCTRINES: unknown beats invented · fabrication hard block · [OBS]/[DER]/[INT]/[SPEC] epistemic labels · ΔS ≤ 0 · F2 evidence carries.
```

Rationale: short version (one line) of the constitutional floor the prompt must enforce. F2 (truth with epistemic labels) and F4 (ΔS ≤ 0) are mandatory for any SADO output.

### Block 4 — Social graph with DM-vs-group demarcation

```
SOCIAL GRAPH — Theory of Mind
Read these nodes before drafting. They shape voice and relevance:
- arif (sovereign): Petronas lineage · MakcikGPT persona · "jangan buat semak" · wants mechanism not figures
- syed: XAUUSD trader 0.3 lots MT5 · GERD · gym regular · nasi lemak stall · flirt banter ok · personal medical timeline NEVER surfaces group-side
- aliff: Petronas geologist · geology shared vocabulary
- izzu: AIA group · WebOfProjects business
Active room: chat_id=-1003815535761 (SADO group) · sender=267378578 (arif)
```

The DM-only column is critical. Without explicit "never surfaces group-side" tags, the LLM may default-include personal material when it's tangentially related.

## Mission + OUTPUT blocks follow Blocks 1–4

After the lane card, mission instructions and output template can look like any cron job spec. The lane card's role is to install the institutional frame; the mission then provides the task-specific instructions.

## Visual + PDF artifact pattern (sado-physique-radar composite)

For event-scanner / calendar-type jobs that need both narrative and visual outputs:

1. **Visual poster**:
   ```bash
   /root/HERMES/scripts/gemini-image.py \
     "<detailed dark editorial prompt — 1080x1080, neon accent gold=Asian major / cyan=LOCAL>" \
     --output /root/<job-name>/output/calendar_poster.png \
     --model gemini-3-pro-image
   ```

2. **HTML calendar source** (write via heredoc / write_file):
   ```html
   <!DOCTYPE html><html lang="en">
   <head><style>
   /* dark theme: background #0a0a0a, gold #d4af37, cyan #00c8dc */
   body { font-family: 'Helvetica Neue', Arial, sans-serif; background: #0a0a0a; color: #f5f5f5; }
   /* 5-column grid for current month + next 4 */
   /* color legend for LOCAL / MAJOR / PAST / TRAINING events */
   </style></head>
   <body><h1>SADO PHYSIQUE RADAR</h1>
   <!-- 5-column grid -->...</body></html>
   ```

3. **PDF render** (Python one-liner):
   ```python
   from weasyprint import HTML
   HTML('/root/<job-name>/output/calendar.html').write_pdf('/root/<job-name>/output/calendar_2026.pdf')
   ```

4. **F11 audit**:
   ```bash
   sha256sum /root/<job-name>/output/* > delivery receipt
   ```

Each artifact must be **explicitly listed in cron prompt mission block** so the LLM knows file paths. Symlink convention: `/root/<job-name>/output/` is sentinel — one dir per radar/scanner job.

## Voice-shape differences (group vs DM)

| Aspect | DM to Arif | Group lane (SADO et al.) |
|---|---|---|
| Length | 250–500 words | max 250 words |
| Voice | personal, gym-bro ok when targeted | intelek advisory, no cringe |
| Persona references | arif-specific terminology | social graph nodes but no personal DM material |
| Visual artifacts | single Telegram message | TGT message + attached PNG + PDF |
| Emoji | situational | lean (one emoji per section, no spam) |
| Closing | "Stay hard." (DM) | none (group-appropriate silence) |

## Pre-create similarity scan — when to consolidate vs parallel

Run before `cronjob(action='create')`:

```
similarity_axes:
  - name_substring
  - prompt_topic_keywords
  - deliver_target_chat_id
  - schedule_day_and_hour

decision_tree:
  similarity_high + same_function + same_deliver → SUPERSEDE (rename + re-scope, mark old enabled=false)
  similarity_high + different_function + same_deliver → KEEP BOTH (parallel if scope disjoint)
  similarity_high + same_function + different_deliver → SPLIT (one per lane, shared prompt DNA)

verified_cases:
  - 2026-08-11: iron-radar → sado-physique-radar (consolidation per user "gabung jadi satu, jangan buat semak")
```

## Pre-fire model pinning discipline (extends drift ritual)

Skip the silent `last_status=error` from model drift by pinning explicitly at create:

```python
cronjob(action='create', name=X, schedule=Y, deliver=Z, prompt=P,
        model={'provider': '<current>', 'model': '<current>'})  # explicit pin
```

Benefits:
- First scheduled fire won't drift-skip even if global inference config shifts.
- Audit chain: job spec → pinned model = contract, not "resolves at fire time".
- Predictable spend: provider billing aligns with named job ownership.

Cost: pinning locks the job to one provider. For a posture that needs poly-provider resilience (apex/constitutional jobs), use `model: null` resolution + drift-aware re-pin ritual from SKILL.md main section. For SADO/group-lane informational jobs, pin freely.

## What this reference DOES NOT cover

- Apex judgment calls (F13 / 888 lane) — see `arifos-constitutional-judge`
- Kernel-level state mutation (cron → not the path; A-FORGE is) — see `arifos-federation-ops`
- OpenClaw L1 cron layer — see `openclaw-ops`
- Telegram delivery token mechanics — see `hermes-telegram-gateway-ops`

## Pitfalls captured

1. **Forget the lane card** → cron fires with no frame, output feels random, agent invents capabilities.
2. **DM material in group output** → F6 EMPATHY ⇄ MARUAH violation (dignity breach). Always tag "NEVER surfaces group-side" for each persona.
3. **Capability map as "ideas to consider"** → must be exact paths, else the LLM uses defaults that may not exist on this host.
4. **Visual art without watermark** → loses the institutional frame. Always include "arifos · intelligence brief" or equivalent.
5. **PDF without HTML source archived** → audit trail broken; the HTML is the editable receipt for the PDF.
6. **Skills generation from cron job** → cron jobs are ephemeral agents. Don't pollute the skill mesh; if the technique is reusable, capture it manually via `skill_manage` (post-session, like this reference).

## Future work

- Multi-language lane cards (BM / EN / ZH) — same capability map, locale-aware voice.
- Wider delivery surfaces (Discord, Slack, email digest) — same lane-card shape, different deliver target.
- Cron-prompt template registry — generated from canonical job spec, versioned in `/root/AAA/prompts/cron/`.
