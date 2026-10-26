# HERMES CHAOS MAP — 2026-10-17

**Verdict (1 baris):** Hermes crash = symlink `/root/.hermes` menunjuk home separuh-siap (`/root/AAA/hermes/.hermes`) yang takda bundled Python. **Sudah fixed.** Tapi seluruh estate Hermes+FED ada 7 kluster entropi dari kempen agent selari tanpa owner — perlu lock-down pass, bukan patch lagi.

## State sekarang (diukur)
- Hermes gateway: `active`, NRestarts=0, Telegram `connected` (polling). ✅
- Canary blocking wired (`70-home-canary.conf` → `/root/scripts/hermes-home-canary.sh`). ✅ tested PASS/FAIL.
- litellm :4013: `active/enabled`, docker container `Up (health: starting)` — **agent auto-RCA lain sedang naikkan dia.**
- FED :4000: `503` (haproxy up, backend litellm belum healthy; backup 100.64.0.5:4000 unreachable).
- fed-aware-middleware :4010: `200` UP — ni yang Hermes guna, sebab tu inference tak mati.
- Disk: 79% (84G free). Tidak kritikal, tapi sediment tinggi.

---

## CHAOS MAP (7 kluster)

### A — HERMES_HOME fragmentation [ROOT CAUSE]
| id | item | state | action |
|----|------|-------|--------|
| A1 | `/root/.hermes` symlink | ✅ → `/root/runtime/hermes/.hermes` (aku repoint) | KUNCI (canary enforce) |
| A2 | `/root/runtime/hermes/.hermes` | ✅ home sebenar (config 30K, state.db 1.25G, tools, installs, .env, auth, tests) | Canonical. Jangan sentuh |
| A3 | `/root/AAA/hermes/.hermes` | ❌ home palsu (skills bundle + runtime separa; state.db 176K, TIADA tools/config/installs/.env/auth) | **Archive** (move → /root/.arifbak/, bukan delete) |
| A4 | `/root/runtime/hermes/` (parent) | ⚠️ double-nested: kanban.db, cron, memories, pairing, logs di top-level + `.hermes/` subdir + `tools/` stray | Decide: ini home ke workspace? |
| A5 | dangling symlink `/root/runtime/hermes/mcp` | ❌ → `/root/AAA/hermes/.hermes/mcp` (target tak wujud) | Repoint ke home sebenar / buang |
| A6 | dangling symlink `/root/runtime/hermes/tools/python-3.14.7+…` | ❌ → `/root/AAA/hermes/.hermes/tools/python-…` (tak wujud) | Buang (stray, parent-level) |
| A7 | `/root/AAA/hermes-prod → /root/scripts/hermes-prod` | ⚠️ alias, target wujud | Decide simpan/buang |
| A8 | dangling: `.federation-worktrees/…/hermes-propose-seal`, `forge_work/…/hermes-propose-seal` | ❌ 2× | Buang |

### B — systemd drop-in sprawl (21 live + 2 .bak pada SATU unit)
Overlap nyata: timeout×3 (`timeout-override` vs `ultra-short-timeout` vs `drain-grace`) · fed×3 (`10-fed-guard-frontdoor`, `fed-auth`, `zzz-fed-model-fix`) · zzz×2 · `debug.conf`, `mem-guard`, `brave-key`, `cron-script-timeout`, `disable-fallback`, `observe-all-groups`, `parallel-key`, `post-restart-check` + `.bak-20261001`, `ultra-short-timeout.bak-20260821`.
→ **Ini punca "kenapa susah debug".** Action: consolidate → 1 set koheren + buang .bak.

### C — dua guard duplicate (satu masalah, dua owner)
| id | item | state |
|----|------|-------|
| C1 | `hermes-symlink-guard.sh` | ❌ dead code — tak wired ke mana-mana drop-in, auto-mutate (`ln -sfn` sendiri) |
| C2 | `hermes-home-canary.sh` + `70-home-canary.conf` | ✅ aku buat — wired, blocking, tested |

Action: retire C1, keep C2. Satu owner.

### D — FED / litellm [isu berasingan, agent lain sedang urus]
| id | item | state |
|----|------|-------|
| D1 | litellm :4013 | 🔄 `active/enabled`, docker `health: starting` — **auto-RCA agent naikkan** |
| D2 | haproxy :4000 | 503 (backend belum healthy) |
| D3 | middleware :4010 | ✅ 200 UP |

Action: **JANGAN duplicate.** Verify D1 jadi healthy, kalau tak baru campur.

### E — consolidation campaign remnants / sediment
- git log: "grounding campaign D2", "alignment sweep", "direct-lanes campaign", "housekeeping" — kempen selari tanpa koordinasi.
- `mv HERMES/CHRON/FRAME source → /root/AAA/agents/` (dari .hermes_history) — sumber federation dipindah.
- `_housekeeping-2026-10-17` (00:16): logs-rotated, sessions-dumps.
- `/root/.arifbak/`: ~34 dir backup (memory-compact-*, memory-prune-*, quarantine-*) — sediment.
- `carry_forward.json` STALE (2026-10-07) — session close tak propagate.

### F — hermes services lain
6 unit `active/enabled` (a2a, mcp-server, rasa-mcp, voice-governor, health, asi-gateway) — semua UP pasca symlink fix. 4 `disabled` (gateway, gateway-api, arifos-bot, agui-bridge) — decide intentional/orphan. 2 `masked` (agent-mcp, mcp) — OK.

### G — Telegram delivery errors [berasingan dari crash]
`Blocked unauthorized user 8410138119 / 8324190535`, `Forbidden: bot can't send messages to the bot` — allowlist/delivery, bukan crash. Action: separate triage.

### H — Concurrent agents [KONTEKS KRITIKAL]
opencode (aku) + qwen-code serve + auto-RCA agent aktif (litellm baru naik). → Semua patch mesti koordinasi, bukan tambah lagi.

---

## PATH FORWARD (gelombang, reversible-first)

**Wave 0 — SELESAI:** restore symlink + wire canary. ✅

**Wave 1 — KUNCI kanonik (aku boleh auto, reversible):**
1. Repoint/buang 4 dangling symlink (A5, A6, A8×2) → tunjuk home sebenar / buang.
2. Retire C1 (dead guard) — fold ke C2.
3. `systemctl daemon-reload` — canary aktif boot seterusnya.

**Wave 2 — STOP conflation (perlu F13 confirm, tapi move=reversible):**
4. Archive `/root/AAA/hermes/.hermes` → `/root/.arifbak/hermes-home-frag-2026-10-17/`.
5. Decide A4 (parent double-nested) + A7 (hermes-prod alias).

**Wave 3 — consolidate drop-in (reversible, hati-hati):**
6. Merge 21 → ~8 koheren. Buang 2 .bak. Satu owner per concern.

**Wave 4 — FED/litellm (koordinasi, JANGAN duplicate):**
7. Verify litellm :4013 healthy. Kalau fail, RCA docker image/config.

**Wave 5 — sediment (perlu F13 untuk delete):**
8. Sweep `/root/.arifbak/` + `_archive` + `_housekeeping` + stale carry_forward.

**Wave 6 — lock governans:**
9. Canonical-home record (single SOT) + "jangan sentuh /root/.hermes" rule.
10. Scar 2026-10-16 → RUNTIME-ENFORCED (canary C2 = dah buat).

---

## Decision binaries untuk Arif (F13)
1. **Archive `/root/AAA/hermes/.hermes`?** (move, reversible) — [SAH / TUNGGU]
2. **Consolidate 21 drop-ins?** (reversible, tapi sentuh unit live) — [SAH / TUNGGU]
3. **Delete sediment `/root/.arifbak/` ~34 dir?** (irreversible) — [SAH / TUNGGU]
4. **Siapa owner Hermes estate?** (satu agent, bukan 3 selari) — [Nama]
