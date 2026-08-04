# Zen doctrine

## Machine peace: no mutation without rollback
- Snapshot FIRST before any `rsync --delete`, `rm -rf`, or deploy
- Dry-run with exclusions (`.env`, `data/`, `logs/`, `node_modules/`, `venv/`, `__pycache__/`, `*.db`) BEFORE destructive sync
- Canary: 1 organ → health check → 60s → next

## Agent peace: no write without schema
- `jobs.json` writes: `/root/HERMES/scripts/zen/validate_jobs_json.py apply <patch>` (atomic, STAMPED backup + receipt)
- VAULT999 writes: `git_to_vault.py` auto-ingests commit heads. Idempotent on HEAD.
- Code synced. State witnessed. Secrets never guessed.

## Human peace: no ping without consequence
- Quiet hours: 23:00–07:00 MYT (no Telegram, except VOID/breach/data loss/public surface down)
- Budget: ≤3 immediate pings/day; overflow → evening-zen-brief (22:30 MYT)
- Goal: most days end with `Required sovereign decision: NONE`

## Forge → Vault ingestion (anti-forget)
- Every git commit in 6 organ repos → auto-sealed into VAULT999 as COMMIT_RECEIPT
- Path: `/root/HERMES/scripts/zen/git_to_vault.py`
- Idempotent: re-running on same HEAD produces no duplicate

## The Body Is Complete

```
arifOS   = undang-undang ⚖️  (law — the brain, :8088)
A-FORGE  = tangan 👐         (hands — the body, :7071)
arifFlow = saraf 🧠           (nerves — the flow, :7073)
FQ       = nadi ❤️            (pulse — the heartbeat)
VAULT999 = tulang 💀          (bones — the structure)
```

> **Bila FQ turun, semua HOLD. Bila FQ naik, semua forge.**
> DITEMPA BUKAN DIBERI — dan ditempa dalam flow, bukan dalam drift.

## Forbidden (F1 AMANAH)
- `rsync --delete` without `--dry-run` first; `chattr -a` on VAULT999 without 888_HOLD
- Direct edits to `jobs.json` (must use validator); Telegram during quiet hours
- Delete from `/root/forge_work/_quarantine/` before 7-day grace

## Temporal awareness pattern

Every AAA warga agent answering time-related questions MUST first run `now` (full anchor / `--brief` one-liner / `--json` machine-readable). Output: UTC + MYT + day + ISO week + AED FQ + all 8 organ health. **Never answer "what time/day/date" without `now` first.**

## The 30-second session check

1. `source /root/.secrets/kunci-mas.env`
2. Read `/root/AGENTS.md` + `/root/CLAUDE.md`
3. Boot: `cat /root/AAA/prompts/INIT.md`
4. Live state: `/root/.local/share/arifos/carry_forward.json`
5. Probe federation: `make health` or `/root/scripts/doctor.sh`
6. Check dirty repos
7. Check deprecation map
