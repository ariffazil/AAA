# HERMES 1572-Dirty Triage — Loop #4 of 9-loop 2026-09-12

> **Author:** FI-008 Kimi (warga-aaa) · **Scope:** `/root/.hermes` git state — OBSERVE only; zero mutations to hermes performed this session (hermes core + VAULT999 untouched, per directive).
> **Evidence class:** OBS — all numbers probed live 2026-09-12 00:1x–00:22 MYT (2026-09-11 16:1x–16:22 UTC).
> **Repo state at probe:** branch `main` · HEAD `36a01da` "helix memory bridge: experiential patterns pointer → SOUL.md" (committed 2026-09-10 02:37:49 +0800) · 5 commits total (young repo) · no stash · nothing staged.

---

## 1. The headline correction (F2)

The 9-loop triage doc called all 1572 files "modified". **Wrong class.** Live breakdown:

| Status | Count | What it actually is |
|---|---|---|
| ` D` (unstaged delete) | **1,095** | Skill dirs relocated to `skills-archive/` (a MOVE, §3) + 33 old `cron/output/` run reports |
| `??` (untracked) | **409** | New runtime output + the entire untracked `skills-archive/` tree + media + backups |
| ` M` (modified) | **68** | Genuine content drift: SKILL.md edits, snapshots, carry-forward, ledgers |
| **Total** | **1,572** | reconciled: 1095 + 409 + 68 = 1572 ✓ |

Falsify: `git -C /root/.hermes status --short | awk '{print $1}' | sort | uniq -c`

## 2. Untracked breakdown (409, by top dir — git lists untracked dirs as ONE entry)

```
141 pastes/            — runtime paste drops → ignore class
127 cron/              — new output reports + state → ignore class
 71 workspace/         — generated media (alpha-zen posters PDFs/JPGs) → review class
 26 skills/            — new/renamed skill files → canonical class
  5 scripts/ 5 profiles/ 4 experience/ 2 terminal-sessions/ 2 memories/ 2 backups/
  1 skills-archive/    — THE ENTIRE 1083-file archive tree behind one entry
  1 each: mem0.json.bak-zen-20260911 · mem0-promotion-ledger.jsonl · config.yaml.golden-20260910 ·
          config.yaml.gutted-20260910T1213 · config.yaml.bak-ctxfix-20260912 · config.yaml.bak-bitrate-20260910 ·
          crontab.bak-ctxwire-20260911 · carry_forward.bak-20260910 · gateway_state.json · state.db locks ·
          verification_evidence.db-wal/-shm · kanban locks · runtime/ pending/ data/ logs/ state-snapshots/
```

⚠️ **Security flag before any commit:** `config.yaml.*` backups (5 files) and `mem0.json.bak` may embed provider tokens / user memory. MUST pass a secret scan (`grep -cE 'sk-|token|api_key' <file>`) before they are ever tracked — otherwise they stay untracked or get ignored.

## 3. The 1095 "deletes" are a MOVE — proof chain (W1–W4)

- **W1:** `skills/creative/` on disk = 1 file (`DESCRIPTION.md`); git tracks 228 → exactly the 227 `D` under `skills/creative` reported in status. The dir was hollowed, not lost.
- **W2:** `skills-archive/` exists untracked, **1,083 files, 163 top-level entries**, containing the moved skill trees — including §B corpse-list members (`AAA-malaysian-rasa`, `AAA-OCR-optical-compression`, …).
- **W3:** Of 158 distinct deleted `skills/*` dirs, **155 reconcile 1:1 with archive entries**. Only 3 do not: `.curator_state`, `FORGE-vps-runbook`, `iarif-v8-pipeline` (likely regenerated or genuinely dropped — 2 need intent confirmation from the mover).
- **W4:** Reflog shows the repo's own convention: commits `F-3`/`F-4` explicitly "exclude runtime drift from git tracking" — this cleanup is the same discipline extended to skills.

**Interpretation (DER):** a curator/archive session (~2026-09-11/12, consistent with the §B 117-dead-skills verdict and `.curator_ledger.jsonl`/`.usage.json`/`.bundled_manifest` being among the 68 modified files) relocated ~155 skill dirs into `skills-archive/`. 158 deleted dirs vs 117 corpse verdict = the sweep was broader than the corpse list; archive contains 163 entries (some new/untracked-before). Git renders this as 1095 deletes + 1 untracked archive dir. **No data loss observed.** Nothing is staged; the move is fully recoverable both directions until committed.

## 4. The 68 modified — split by fate

| Class | Files | Fate |
|---|---|---|
| Runtime state (snapshots, deliveries.db, charts, digest_inbox, quotes/state JSONs) | ~25 | `git rm --cached` + ignore (drifts every 30 min — commits here are noise forever) |
| Curator bookkeeping (`.bundled_manifest`, `.curator_ledger.jsonl`, `.usage.json`) | 3 | commit WITH the archive move (they describe it) |
| Genuine skill content edits (~20 SKILL.md: syed-care-architecture, hermes-federated-identity, forge-multimodal-router, autonomous-ai-agents/* …) | ~30 | review diff, then chore commit |
| Session continuity (carry_forward.json, briefing-output.txt, spawn-ledger, memories/, experience/, terminal-sessions/, state/) | ~10 | commit carry_forward + briefing; ignore volatile ledgers |

## 5. Safe commit plan (for FI-009/hermes team to EXECUTE — not executed by FI-008 this session)

Order matters; each phase is one atomic commit, reversible via `git revert`/`reset`; nothing touches gateway code or config.yaml.

**Phase 0 — safety net (no commit):** `git -C /root/.hermes branch pre-archive-cleanup` — a movable pointer makes every later phase trivially reversible.

**Phase 1 — ignore the ephemeral (extends F-3/F-4 precedent):** append to `.gitignore`:
`cron/output/`, `cron/snapshots/`, `cron/charts/`, `pastes/`, `terminal-sessions/`, `workspace/zen/`, `*.lock`, `*.db-wal`, `*.db-shm`, `backups/`, `state-snapshots/`, `runtime/`, `pending/`, `logs/`. Then `git rm -r --cached` those paths already tracked. Commit: `chore: exclude runtime drift (F-3/F-4 discipline extended)`. Kills the recurring 30-minute churn at its root (cron/output alone was 122 entries of this batch and will regrow every run).

**Phase 2 — the archive move, atomic:** `git add -A skills/ skills-archive/` → git rename-detects old→new paths (content identical), so history survives. Commit: `chore(skills): archive 155 dormant skill dirs to skills-archive/ per curator ledger + 117-dead verdict`. **Pre-condition:** FI-009 confirms the 3 non-reconciled paths and the 41-dirs-beyond-corpse-list delta were intentional. This single commit clears 1,062 D + the 1,083-file untracked archive in one reversible step.

**Phase 3 — canonical drift:** stage the ~30 real SKILL.md edits + carry_forward.json + briefing-output.txt + the 26 untracked canonical skills/ files. Commit: `chore: skill content drift + session carry 2026-09-10..12`.

**Phase 4 — security review, then decide:** scan the 5 config.yaml backups + mem0.json.bak + crontab.bak for secrets. Clean → commit as recovery points under `backups/`; dirty → delete or ignore. NEVER blind-add.

**Never commit:** `gateway.lock`, `auth.lock`, `*.db-wal/-shm`, `mem0.json.bak` (user memory export — PII risk).

**Expected end state:** `git status` ≈ clean; repo tracks canonical content only; runtime churn invisible.

## 6. Handles (Claim–Receipt binding)

- Triage source: `/tmp/opencode/triage-2026-09-12-9loop.md` §D
- This report: `/root/AAA/reports/hermes-1572-dirty-triage-2026-09-12.md`
- Companion deliverable: `/root/AAA/governance/mem0-arifos-routing-matrix.md` (Loop #2)
- Re-derive any number: `git -C /root/.hermes status --short | awk '{print $1}' | sort | uniq -c`

DITEMPA BUKAN DIBERI ⚒️
