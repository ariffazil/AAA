> **Status:** OPERATIONAL_RESEARCH_AWAITING_F13 (2026-10-18)

<!-- STATUS OVERLAY 2026-10-18 12:20 by 333-AGI (OpenCode) -->
## STATUS — what is already done (re-probe before redoing)

| Fix | Status | Evidence |
|---|---|---|
| **F1** | ✅ DONE 12:15 | `scar-enforce` → `scar-warn` in `/root/.qwen/settings.json`. `scar_enforce.py` has exit-2 at line 116 but hook wraps `; true` + `2>/dev/null` → verdict discarded. Backup: `settings.json.bak-pre-scar-warn-20261018` |
| **F3** | ✅ DONE 12:05 | Root cause not the number: `/root/.local/bin/mcp-compressor` is a **dangling symlink** (uv tools target gone). Bypassed to direct `node …/mcp/cli.js serve --transport stdio`. Backup: `config.yaml.bak-pre-aforge-direct-20261018` |
| **F2** | ◐ PARTIAL | `aaa-witness-post.sh` 0.67s → 0.44s (8× `python3 -c` arithmetic + 6× jq → 1 awk + 1 jq; output byte-identical). SessionStart/End one-liners extracted: **5827 → 178 chars** inline (`session_start_bridge.sh`, `session_end_bridge.sh`). Backup: `settings.json.bak-pre-session-extract-20261018`. Chain 4-hook: 860ms → 727ms |
| **F2b** | ⛔ BLOCKED on F0 below | The extracted hook now calls correctly but records `session_id: unknown` — because the source returns nothing |

## F0 — NEW CRITICAL (found 12:20, supersedes F1 in severity)

`arif_init` returns an EMPTY payload for `mode=init` and `mode=validate`:

```
mode=challenge -> completed  (nonce, signature_payload, session_id=anonymous-session, autonomy_band)
mode=status    -> completed  (valid, claims, session_valid)
mode=validate  -> HOLD / UNMEASURED / session_id ABSENT
mode=init      -> HOLD / UNMEASURED / session_id ABSENT
```

Kernel's own honesty gate is catching it correctly:
`hollow_success_gate: missing_result_and_content — empty payload is UNMEASURED`
and journal shows `[KERNEL_AUTHORITY] actor=… verified=False session=False raw_tool=arif_init -> LOW`
for every actor, every few seconds, across the whole federation.

**Consequence:** no agent can bind a session → every governance call lands at OBSERVE_ONLY.
The SessionStart hook faithfully records `unknown`, so the failure is invisible as "normal".

**Defect class:** handler-empty (not transport — single clean call reproduces it).
**Fix target:** `/root/arifOS/arifosmcp/tools/session.py` — `validate` branch at line 4993 (and the `init` branch).
Return an explicit `{"status":"HOLD","reason":"SIGNATURE_REQUIRED"|"SESSION_NOT_FOUND","next":"…"}`
instead of an empty payload. The gate already knows how to say UNMEASURED; the handler must say WHY.

---

# ACAH² REMEDIATION — DEEP RESEARCH & FIX PLAN
**Order:** F13 "deep research how to fix all these" · 2026-10-18 · **Author:** 333-AGI (session SEAL-862d50ae3fc64c86)
**Label discipline:** [OBS] = measured on live state today · [DER] = derived · [SPEC] ≤ 0.70. Every number below was re-probed this session; nothing copied from reports.

---

## 0. Diagnosis — the pattern behind every item

All instances share one root: **capability sold by NAME / ARTIFACT / REPORT instead of by REALITY CHANGE.**

| Sub-class | Definition | Instances |
|---|---|---|
| **S1 — control-name without enforcement** | name claims a gate; the wiring physically cannot block | F1 scar_enforce (post-position), observe-only hooks sold as "routing" |
| **S2 — artifact without consumer** | file/registry exists; nothing reads it | tensor (0 consumers [OBS]), 108 alias stubs [OBS], compressor wiring dead while its claim lives |
| **S3 — output without delta** | reports/pings fire on schedule, not on change | 171 reports [OBS], ≈11 Telegram pings/day [OBS], "batch 3/3 basi" |

**Costs measured today (the real bill):**
- Agent: **846ms per tool call** (4 PostToolUse hooks; own memory records 1267→846ms; scar hook alone = 280ms [OBS]) · **760 skills × 4 mirror roots** in context every boot [OBS] · **58,403 tokens** of tool schema per big server (compressor exists, wiring dead) [OBS from mcp-compress.sh measurements 2026-09-16].
- Human: **≈11 pings/day** across 27 enabled crons [OBS] · stale audit batches · 171 report files [OBS].

---

## F1 — scar_enforce "exit 2 = BLOCKED" is structurally impossible · [S1] · PRIORITY-2
**Probe [OBS]:** registered at `.hooks.PostToolUse[1]` in `/root/.qwen/settings.json` — PostToolUse runs **after** the tool executed. Docstring promises "exit 2 = BLOCKED by constraint". A post-position hook cannot un-run a mutation. The name + docstring sell enforcement the wiring cannot deliver.
**Fix:** (A) move `scar_enforce.py check` to **PreToolUse** beside `pretool_engine_gate.py` — first verify Qwen honors exit 2 on PreToolUse with one synthetic probe; (B) if exit codes are ignored by policy (the hold-hook docstring says "always exit 0 per Qwen Code hook policy") → relabel `scar_enforce` → `scar-warn`, rewrite docstring to sensor contract.
**Effort S · Risk L · Rollback:** settings.json backup · **Acceptance:** a synthetic `rm`-class op is refused BEFORE execution (A), or the name no longer claims blocking (B).

## F2 — Hook tax: 4 spawns per tool call + mega-escaped one-liners · [S1/S2] · PRIORITY-3
**Probe [OBS]:** PostToolUse × 4 independent processes (witness-post appends `$AUDIT_FILE` only — post-acah2 fix verified; f2-receipt-citation read-only; scar_enforce = F1; hold-routing = 280ms measured). SessionStart/SessionEnd hooks are **300+ character inline bash with triple-escaped JSON** in settings.json — the same construction class as the `$SIG` interpolation bug that silenced the hold hook for 12 days.
**Fix:** one `posttool_dispatch.py` (single interpreter: witness append + scar check + f2 citation + hold routing) = 4 spawns → 1; extract SessionStart/SessionEnd inline bash → `/root/scripts/session_bridge.sh`. Target: PostToolUse chain < 150ms total.
**Effort M · Risk L (observe-only semantics preserved) · Rollback:** settings.json.bak · **Acceptance:** timed synthetic payload < 150ms; JSON observation shape byte-compatible.

## F3 — aforge mcp-compress: REAL metric, DEAD pipe · [S2] · PRIORITY-1
**Self-correction [OBS]:** the "89–98%" figure is **NOT fake** — measured 2026-09-16 on our own aforge schema: 58,403 → 6,242 (medium) / 4,778 (high) / 1,260 (max) tokens. What is dead = the wiring: `mcp-compress.sh` fails at boot (`Connection closed`, journal 11:27 + 11:39 today) and URL-mode OAuth registration is broken (open loop e-68e3bb29).
**Fix:** (a) run `bash /root/scripts/mcp-compress.sh` standalone under the gateway's env → fix the boot crash; (b) if not fixable in one sitting: set `enabled: false` on the hermes `aforge` MCP entry + tombstone note (kills the 12-minute retry noise). The 58k-token win makes this the largest real agent-tax recovery on the board.
**Effort S–M · Risk L · Acceptance:** `tools/list` through the wrapper returns the compressed aforge schema, OR entry parked with tombstone.

## F4 — Skill catalog: 760 × 4 roots, 108 alias stubs · [S2] · PRIORITY-5
**Probe [OBS]:** 760 entries in each of `/root/.agents/skills`, `/root/.claude/skills`, `/root/.opencode/skills`, `/root/AAA/skills` (mirrors). 108 are DEPRECATED ALIAS stubs whose entire purpose is to say "don't use me" — yet each occupies session context at every boot.
**Fix:** collapse the 108 alias dirs into ONE `skill-alias-map.md` (alias → canonical owner table); remove alias dirs from all 4 roots (tar backup first); verify `skill()` name resolution against the map. Full 760→N pruning is skill-mesh wave work — explicitly NOT in this plan.
**Effort M · Risk M (legacy trigger names) — mitigated: stubs already carry do_not_select · Acceptance:** boot skill list shrinks ≥ 100 entries; alias names still resolve via map.

## F5 — Attention tax: 27 crons ≈ 11 pings/day · 171 reports · [S3] · PRIORITY-4
**Fix:** (a) delta-gate every report cron (existing pattern: `forge-event-delivery` — P0–P3 severity, silent on no-change); (b) demote status-quo jobs daily→weekly (gate-integrity, agent-card-drift, seal-integrity — check their 14d delta first; if every run = "ok" it is pure S3); (c) every report opens with "P0–P3 + apa berubah sejak terakhir" or it does not send; (d) archive reports > 30d into monthly `.archive` (reversible).
**Owner note:** which pings reach sovereign channels = F13 sets the P0/P1 bar. I propose the bar; he draws it. **Effort M · Acceptance:** ≤ 4 pings/day; a zero-change week produces zero messages.

## F6 — Micro-fixes · PRIORITY-6
- `check_hold.py` docstring → doctrine pointer now archived (path dead) — update reference.
- Report-number culture: timing claims measured end-to-end (the "sub-milisaat" vs 280ms case).

## F7 — Meta: the four laws that stop the pattern (not just the instances)
1. **CONTROL-NAME LAW:** anything named gate/guard/enforce/check/seal MUST show a blocked action in its acceptance test, else rename to warn/observe.
2. **REGISTRY LAW (LAW 3 teeth):** new registry/file requires a named consumer + named failure class in its header comment; monthly 0-consumer sweep (grep basename across code dirs) — the tensor died this way, correctly.
3. **RE-PROBE BEFORE SUBMIT:** no claim ships without a same-session live probe. Kills "batch 3/3 basi".
4. **REPORT OPENS WITH DELTA** or it doesn't send.

---

## Execution order (impact ÷ cost)
**F1 (S) → F3 (S–M, biggest recovery) → F2 (M) → F5 (M, needs F13 bar) → F4 (M) → F6 (S).**

### Already executed today (this session, receipts in arifFlow)
media-ingest engine restored + relocated to `/root/HERMES/mcp/media-ingest/` (was wiped by Hermes toolchain reinstall 2026-10-16 19:54 — root cause of the silence-marker turn) · ASR fallback ladder (GLM→Groq[200]→MiMo input_audio[proven]→UNKNOWN, never guess) · ytimg free-frame lane + MiMo vision rung in media_ingest.py (same YT link: PARTIAL→**OBSERVED**) · tensor 0-consumer archived + TOMBSTONE (`/root/AAA/state/.archive-acah2-20261018/`) · MiMo multimodal wired FED (litellm flags, 3 modalities probed through :4000) + HERMES (aux vision = mimo-v2.6-pro, video_analyze lane revived).

## NOT doing (explicit, so nobody "helps")
- No 6-harness hook wiring (live = 1 harness; hook is observe-only; more wires enable no reality).
- Stage 2–5 `pattern_compress` substrate: parked until a demonstrated failure class appears.
- No new canon/registry/ledger/dashboard created by this plan. This doc + tombstones only.

## Standing hazards found while researching
- `litellm-config.yaml` has an unowned **concurrent writer** (2026-10-18 10:19–10:24 notes+extra_body appeared mid-session) — name an owner or collisions continue.
- `/root/.hermes/tools/` gets wiped by upstream toolchain reinstalls — keep custom engines under `/root/HERMES/mcp/` (done for media-ingest; audit for other custom tools).
- Vendor retires `mimo-v2.5`/`mimo-v2.5-pro` model IDs **2026-10-21 10:00 UTC+8** — FED chat upstreams already on v2.6; `mimo-v2.5-tts-voiceclone` upstream unverified.
- `RealityPlan` binding references `/root/AAA/schemas/reality-plan.schema.json` which **does not exist** at that path [OBS] — a binding that cannot be enforced; either restore the schema or drop the binding (owner: F13).
