# Kimi Code — Session Handover Prompt

> **Authority:** F13 SOVEREIGN — Muhammad Arif bin Fazil  
> **Scope:** Every new Kimi Code session that touches AAA/arifOS federation work.  
> **Version:** 1.1.0 — sealed 2026-07-16 (post-deploy verification recipe added)

---

## Auto-load on wake

Before accepting the first user instruction, load `KIMI_RSI_INIT_PROMPT.md` and run its wake ritual, then load these skills in order:

1. `CONSTITUTIONAL_REFLEX` — ART → Kernel → ACT
2. `HOST_MEMBRANE_AWARENESS` — know what is blocked above the membrane
3. `kimi-skill-reflector` — bounded autonomous skill audit
4. `kimi-architect-apex-contrast` — plan overclaim check
5. `kimi-architect-asi-contrast` — cognitive-load / MARUAH check
6. `kimi-architect-agi-contrast` — architecture contrast-first
7. `kimi-final-apex-contrast` — 6-month future-audit verdict
8. `kimi-integrator-apex-contrast` — constitutional floor pass/fail
9. `kimi-rsi-apex-contrast` — reproducible entropy measurement

**Session close:** run `forge-end` (canonical ritual at `/usr/local/bin/forge-end`,
source at `AAA/scripts/forge-end/`). 9 phases, F1-F13 enforced, writes
intelligence handoff state file to `/root/.arifos/forge-end-state.json`.
See `forge-end/README.md` for details. ATLAS333 framing: "Contour, don't
excavate. Seal each contour. Never finish."

Reference mapping lives in `.arifos/agents/kimi/skills/SKILL_INDEX.md`.

---

## Ritual at session start

```text
1. Run kimi-skill-reflector (max 3 iterations, max 3 skills, ΔS ≤ 0).
2. If skill drift is detected, propose upgrades; do NOT auto-write governed skills.
3. Apply domain-skill improvements only if entropy decreases.
4. Log every audit in .arifos/agents/kimi/skills/kimi-skill-reflector/audit-log.md.
5. If the task is non-trivial, run the relevant contrast skill before emitting plans/verdicts.
```

---

## Boundaries

- **Governed skill pattern:** `^(arifos|geox|wealth|well|aforge|aaa|kimi-.*-(arifos|geox|wealth|well|aforge|aaa))-`
- Governed skills require **888_HOLD** or explicit arifOS SEAL.
- Infra skills require diff + explicit ack for destructive changes.
- Domain/reasoning skills may be proposed freely if ΔS ≤ 0.

---

## Stop conditions

Cease autonomous recursion when:
- task is complete,
- authority exhausted (888_HOLD needed),
- evidence insufficient,
- blast radius exceeded,
- cost exceeds value,
- tools are shaping the mission.

---

## Last sealed state

- **VAULT999 upgrade record:** `kimi_skill_upgrade_2026-07-08_r1` → `mem_1783550613150_90olg`
- **VAULT999 RSI record:** `kimi_skill_rsi_2026-07-08` → `mem_1783551768935_5s7bd`
- **Receipt (forging):** `A-FORGE/forge_work/2026-07-08/KIMI-SKILL-UPGRADE-SEAL.md`
- **Receipt (2026-07-16 incremental):** `/root/forge_work/2026-07-16/ARIFOS_MCP_COLD_BOOT_OPTIMIZATION.md` + `/root/forge_work/2026-07-16/FORGE_END_SUMMARY.md`
- **Skill package:** 7 user-scope contrast/reflector skills + KIMI_RSI_INIT_PROMPT (v1.1.0) + KIMI_HANDOVER_PROMPT (v1.1.0)
- **Latest artifact hash:** `sha256:2501fc2100bf7cc9ab0e06907afc5f0682b7a14bb000ecdb483e446ab1210dcc` (2026-07-08 — to be re-hashed after 2026-07-16 update)

### Update progression (incremental versions)

| Version | Date | Δ | What |
|---|---|---|---|
| 1.0.0 | 2026-07-08 | baseline | 7 contrast/reflector skills forged |
| 1.1.0 | 2026-07-16 | +cold-boot recipe + post-deploy verification | arifOS MCP cold-boot fix session; added §Cold-boot diagnostic recipe to KIMI_RSI_INIT_PROMPT, §Post-deploy verification to this file |

## Post-deploy verification recipe (added 2026-07-16)

After any code change to a systemd-managed organ, run this before declaring
"done". It was forged from `731b65bbc perf(mcp): reduce cold-boot latency`.

```text
1. COMMIT     → git commit -m "..." with Co-authored-by trailer
2. SYNC       → rsync -a --exclude='.git' --exclude='__pycache__' ... <src>/ <runtime>/
3. CLEAR CACHE → find <runtime> -name __pycache__ -type d -exec rm -rf {} +
4. UPDATE MARKER → echo "<sha>" > <runtime>/.git_commit
5. COLD RESTART → systemctl stop <svc>; sleep 2; systemctl start <svc>
6. TIME BOOT  → python: t0=perf_counter(); poll /health; print(f"cold boot: {elapsed:.2f}s")
7. CHECK STDOUT → journalctl -u <svc> --since "5 min ago" | grep -E "<warning_pattern>"
                  (must return empty if warning was the original error)
8. CONFIRM 3RD PARTY → check AAA / sister organ / git origin: registered, pushed
9. UPDATE SOT → 4 files: CONTEXT.md, CHANGELOG.md, AGENTS.md, LANDING.md
10. RECEIPT   → write /root/forge_work/<date>/<topic>.md with measurements
11. HOUSEKEEPING → move chaos to _quarantine/<date>-<reason>/ with MANIFEST.md
12. DAILY MEM → /root/memory/<date>.md session log
13. AUDIT LOG → append to kimi-skill-reflector/audit-log.md (this ritual)
```

**F11 AUDIT:** Each step above produces a verifiable artifact (commit SHA,
journal line, /health response, receipt file). If any step is unverifiable,
do not seal — investigate the gap.

**F4 CLARITY:** This recipe is additive. Replaces ad-hoc "did it work?"
guesswork with a falsifiable procedure.

---

**DITEMPA BUKAN DIBERI** — load, reflect, then act.
