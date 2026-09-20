# Prune Session Record — 2026-08-15 (first F13-ratified execution)

Context: Arif pasted an external council's (Qwen W3 session) capability-mesh
analysis + prune plan and gave GO. The council's plan was built on a dead
directory. This record is the evidence trail for the veto + the corrected prune.

## The ghost

`/root/AAA/.hermes/skills` — 72 skills, Jul-5 relic of an old profile home:
- no `config.yaml` in the parent (live profiles have one)
- 0 SKILL.md touched in the previous 7 days (live surface: 233)
- no process env references, no open handles
- only "references": historical session DBs, CLI history, wiki docs, and a
  May disk-reclaim note that had already flagged the dir for cleanup

The council's "72→12" plan: prune apple, smart-home, social-media, email,
media, yuanbao, dogfood; collapse creative/mlops/productivity/research into
single abstractions. Executed against the LIVE surface it would have archived
`media/` (20 skills) containing nusantara-voice-layer, nusantara-voice-stack,
TTS/OCR — backbone of the I-ARIF voice identity + voice-corpus standing
directive. Content falsification vetoed the category sweep.

## What was actually pruned (all reversible mv, per F1)

1. **Ghost archived** → `/root/AAA/.hermes-archived-2026-08-15` (72 skills).
   First move attempt HOLDed by a ref-scan (5 hits); second pass categorized
   every hit as historical (state.db, CLI history, session dumps, wiki) with
   0 config/systemd/process bindings → executed.
2. **nasi-lemak 4→1**: canonical `business/nasi-lemak-sales` (109 lines,
   6 triggers, Khairuddin business context). Merged 3 unique triggers from
   daily-tracking (incl. vendor codes DSW/DSP/LRT/KEAI) → 9 triggers total.
   Archived: sales-tracking (235 lines, 0 triggers), daily-tracking,
   trading/nasi-lemak-tracking (307 lines, 0 triggers). All four wrote to the
   same `/root/forge_work/YYYY-MM-DD/` data — no data split, safe collapse.
   Substance > line count: the biggest files had zero triggers.
3. **apple/ (3 skills)**: macOS tooling on a Linux VPS — architectural
   mismatch, valid prune without traffic data.

Post-move pointer sweep found 2 danglers, both patched:
- `business/kpj-sales-dashboard` related_skills → `business:nasi-lemak-sales`
- `devops/federation-alignment-sweep` audit table row → "Consolidated 4->1 (2026-08-15)"

## Killed-options ledger (vetoed, with reasons — the moat, not the action log)

| Vetoed | Reason |
|---|---|
| media/ wholesale prune | contains live voice/TTS/OCR load-bearing skills |
| social-media/xurl | real X/Twitter capability, referenced in memory |
| business/kpj-sales-dashboard | Izzu automation, established format |
| email/himalaya, creative/32, research/36, devops/66 sweeps | no usage evidence gathered this session — needs usage-based pass (session_search / gateway log forensics), not category shape |

Ledger with revert commands: `/root/.hermes/skills/.archive-2026-08-15/PRUNE_LEDGER_2026-08-15.md`

## Counts

Live active skills: 442 → 434. Broken symlinks after: 0.

## Aftermath (same session): bundled-skill resurrection

`hermes update` (v0.20.0→v0.20.1, run hours after the prune) re-synced bundled
skills and resurrected apple into `profiles/aaa-hermes/skills/` — the
default-surface archive held, profile surfaces were refreshed from upstream
bundles. Also moved 3 skills to new upstream paths (findmy, apple-reminders,
apple-notes). Lesson: archiving bundled skills is surface-local; permanent
category kills need `hermes skills config` disable.

## Transferable rules

1. Trust no prune plan whose target dir hasn't passed the 5-point liveness battery.
2. Veto category sweeps lacking per-skill usage/architecture evidence.
3. Canonical-by-substance (triggers + context), merge losers' unique triggers first.
4. mv to dated archive + ledger with revert commands; never delete.
5. Sweep for dangling pointers AFTER the move; patch related_skills + audit tables.
6. Expect `hermes update` to resurrect bundled skills into profile surfaces — disable, don't just archive.
