# SCAR: Local Service in Distress IS A Patient, Not A Parasite

**Forged:** 2026-08-13 (F13 Sovereign & Hermes ASI)
**Context:** Session audit misdiagnosed 5 recurring patterns by acting on surface symptoms rather than root-cause logs.

## The 5 Symptom-vs-Reality Patterns

1. **"Skill missing"** → Symptom: path audit failed → Reality: wrong audit path, skill alive elsewhere.
2. **"Ghost skill"** → Symptom: unindexed skill → Reality: already exists, audit scanner misconfigured.
3. **"Zombie port fight"** → Symptom: multiple processes seen in `ps` → Reality: 1 port holder + 3 session children (pts).
4. **"Duplicate files"** → Symptom: identical contents via `diff` → Reality: already hardlinked (same inode).
5. **"100% CPU parasite"** → Symptom: high CPU restart loop → Reality: `PermissionError` on `institution.py` (mode 600) + missing `PYTHONPATH`.

## The Sovereign Rule (Root-Cause-First)

1. **Local service in distress = PATIENT, not parasite.**
2. **Mandatory Log Witnessing:** Before any kill, disable, or file deletion:
   ```bash
   journalctl -u SERVICE -n 50 --no-pager
   ```
3. **Fix Error First:** If log reveals `PermissionError`, missing ENV, or missing module → fix the error.
4. **Kill is Last Resort:** Reserved strictly for confirmed external malware or unrecoverable rogue loops, NEVER for local infrastructure in distress.
5. **Core Question:** Ask *"Kenapa looping?"* — NEVER *"Apa nak kill?"*.

