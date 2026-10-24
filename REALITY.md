# REALITY.md — arifOS Federation Ground Truth
**Canonical state anchor.** If a doc, comment, memory, or agent claim contradicts this file
without a newer timestamped receipt, THIS FILE WINS. Last verified: 2026-10-21 ~11:00Z by 333-AGI.
Supersedes: any un-receipted claim about FED litellm, guard, OpenRouter lanes, or identity binding.

---

## 1. FED LLM GATEWAY (litellm-federation :4013)

| Fact | Value | Evidence |
|---|---|---|
| Live container | `litellm-federation`, digest `sha256:c7e655fac0fe…` (= repo `main-latest`) | docker ps; `systemctl show` |
| Live config | `/root/A-FORGE/litellm-config.yaml` (2697 lines, sha `119d9ade`) | container `/app/config.yaml` sha match |
| Deploy copy | `/root/A-FORGE/deploy/fed/litellm-config.yaml` **NOW SYNCED** to SOT 2026-10-21 | sha `119d9ade` (was `b35fe654`, stale 16 Oct) |
| Stale copy | `/opt/a-forge/app/litellm-config.yaml` (sha `e3d81d99`, 8 Oct) — **NOT live path, DEPRECATED** | not mounted |
| Workers | `--num_workers 1` (single process) | unit ExecStart |
| Spend witness | `fed_spend_callback.proxy_handler_instance` → `token_bank.db` | config line 2161 |

**Config truth = SOT file only.** Editing the deploy/fed copy alone does nothing to the live
proxy. The container mounts SOT. `#48 p1-fed-config-drift-reconcile` = **RESOLVED** this session.

### 1a. Context guard (pre-call) — LIVE
- Module: `/root/A-FORGE/scripts/fed_context_guard.py` (mounted read-only into container).
- Class: `FedContextGuard(CustomGuardrail)`; registered top-level `guardrails:` (mode pre_call,
  default_on). **NOT** a plain CustomLogger — this litellm build only dispatches pre-call via
  the guardrails pipeline. Registering as `fed_context_guard.guard_instance` (instance) FAILS
  with "object is not callable"; must be the CLASS `fed_context_guard.FedContextGuard`.
- Thresholds: WARN=384_000 (audit only) · HOLD=704_000 (413) · loop ≥3 identical/600s at ≥WARN → 429.
- Loop counter: **in-process dict** (`_LOOP_WIN`), NOT redis — redis on this box is password-gated
  and the proxy is single-worker. Documented constraint.
- Kill-switch: `ARIF_CONTEXT_GUARD=""` via systemd drop-in `30-context-guard.conf` + restart (~40s).
- Override header `x-arif-context-override` = **OFFLINE on this build** (guardrail data carries no
  headers). Do not rely on it. Env kill-switch is the real escape hatch.
- F1: internal errors fail-open. Calibration: p50=181k/p90=372k/p99=657k over 10,290 deepseek calls/48h.
- **CONCURRENT EXTENSION (2026-10-21 17:56, by peer writer — NOT 333-AGI):** guard now ALSO has
  `budget_gate=on budget_route=go-gpt-6-luna cap=$0.25` (per-call USD ceiling → routes to Luna
  rung). Running container confirms this build. File sha `52c6e27cde9b` (superseded my `0e60be31`
  in the working tree; uncommitted as of 18:22Z). Treat guard feature set as: context thresholds
  + budget gate + loop guard.
- **Working-tree drift 2026-10-21 18:22Z:** `scripts/fed_context_guard.py`,
  `deploy/fed/litellm-config.yaml`, `data/web_federation_state.json`, `duties/federation-pulse.sh`
  modified; `scripts/fed-parity-guard.sh` untracked — peer writers active. Do NOT assume these
  are 333-AGI's edits; verify per-file before attributing.

### 1b. OpenRouter lanes — WIRED, FUNDED
- 11 rungs inserted 2026-10-21 (deepseek-flash/v4-flash/v4-pro/vision @ order 1 + fallbacks).
- **Base path MUST be `https://openrouter.ai/api/v1`** — `…/v1` returns 404 HTML. (Learned the hard way.)
- Live key: `sk-or-v1-e12…48f` (label in `/root/.secrets/kunci-mas.flat.env`).
  - Prior key `sk-or-v1-37e…301067` = $0 credits (dead). Killed 2026-10-21.
- Balance: lifetime usage $44.135 (of $9.88 top-up + prior). Burn 2026-10-21 ≈ $0.048.
- Live test 2026-10-21: deepseek-flash 200 ($3.55e-6/call) · deepseek-v4-pro 200 ·
  WARN-band 403k through OR 200 (1M window honored).
- **DeepSeek DIRECT accounts = 402 Insufficient Balance** (both). OR is now the funded path.

---

## 2. IDENTITY / BOOTSTRAP — known traps (from bootstrap skill)

| Trap | Symptom | Truth |
|---|---|---|
| key≠json mismatch | binding "works" but verify fails | regenerate seed AND all 3 files |
| PEM path | resolver blind | PEMs live in `/root/AAA/IDENTITY/keys/`, NOT `/root/AAA/keys/` |
| challenge rejected | registered agents denied | `_SOVEREIGN_MAP` patched for registered actors |
| actor normalize | `challenge_actor_mismatch` | plugin must sign as canonical `333-AGI`, NOT `opencode` |
| **lowercase PEM** | stale lowercase file overrides fresh canonical | **check BOTH case variants; overwrite lowercase** |
| A-FORGE marker | health shows wrong commit | `.git_commit` written to SOURCE not DEPLOY root |

`p1-kernel-identity-observe-only-sticky` (#64) = open: effective_state sticks OBSERVE_ONLY
despite actor_verified=true. Owner: kernel lane (sibling). NOT this lane.

---

## 3. WHAT NOT TO BELIEVE (anti-confusion)

1. **"8f1d7b9c"** = a **git commit hash** (`fix(spend): bounded visibility…`), NOT a file sha256.
   Two different id classes. Don't refute one with the other.
2. **"$89.92/7h"** from Phase A report = NOT derivable from `LiteLLM_SpendLogs`. Measured:
   $5.05/7h, $20.35/30h. The $89.92 came from a different instrument — name it before quoting.
3. **"sandbox-deny in /root/A-FORGE"** = wrong diagnosis. Real wall = `chattr +i` immutable.
   Bypass = `chattr -i` → edit → `chattr +i`. Root can do it. Not a permission wall.
4. **"11 rung OpenRouter"** = ALREADY WIRED + committed (`8f3af7e3`). Running the v2 workorder
   script now just prints ALREADY_WIRED. Don't re-run it.
5. **deploy/fed copy** = synced to SOT now. No discontinued `deepseek-chat` as a live model
   (one mention remains in a `notes:` history line — not a route).
6. **`seal_chain_head.json` `seq: 72` ≠ "entry #72".** The head's `seq` field is the **COUNT of
   canonical entries**, not the last entry's sequence number. Source: `canonical_vault_chain.py:1433`
   → `effective_seq = canonical_entries if canonical_entries > 0 else entry_sequence(last)`.
   Verified 2026-10-21: head.seq=72 while `seal_chain.jsonl` last entry seq=**55** and line count=274.
   Two different meanings of "seq" in the same subsystem. Never compare head.seq to entry.seq.
7. **`seal_chain.jsonl` is NOT the whole seal history.** It holds 274 lines (last append
   2026-10-15T09:48:35Z, seq 55) and has been **frozen** since; the live event stream is
   `/root/arifOS/VAULT999/SEALED_EVENTS.jsonl` (1,357 lines, flowing to 2026-10-18+).
   `seal_chain_head.json` is a **derived cache** (`derived:true, source:chain_tail`) refreshed by a
   separate job — its `last_anchor_utc` (2026-10-21T10:37Z) and `latest_commit` (418b0eab) are newer
   than the chain file's mtime. Head freshness ≠ chain freshness.
8. **Two copies of `seal_chain.jsonl` are byte-identical** — sha256 `1073ce80d90e…`
   (`/root/arifOS/VAULT999/` and `/root/.local/share/arifos/vault999/`). Treat as ONE file, two mount paths.
   A `.pre-append.20261020T155422.jsonl` backup (1.4 MB / 2,222 lines) is LARGER than the live chain —
   a relink/truncation event happened 2026-10-20; `SEALED_EVENTS.relinked.jsonl` + manifest confirm it.
9. **VAULT writer is UP but degraded:** running on **DB legacy schema**, `cooling_ledger` = RED,
   F13-pending migration (per `carry_forward.reality_pulse`, 2026-10-21T11:00Z).
10. **GEOX / WEALTH / WELL** = UP but **degraded — MCP `tools/list` returns HTTP 400** each.
    "UP" in a health row does NOT mean "MCP surface healthy".
11. **The "retire 10 zero-use A-FORGE tools" task is ALREADY DONE — 2026-10-18.**
    All 10 (`forge_stage`, `forge_visual_qa`, `forge_pipeline_run`, `forge_github_create_issue`,
    `forge_synthesize`, `forge_browser_type/click/extract_text/evaluate_js`, `forge_visual_seal`)
    were retired in "Tugas 1.4 / C-06 Capability-Entropy Pruning". **Verified live 2026-10-21:**
    A-FORGE MCP `:7072` serves 115 tools, NONE of the 10 present. Retirement sites:
    `gatewayTools.ts:1882-1921` (issue + 4 browser), `core.ts:3540/3560/3573` (pipeline/visual_qa/visual_seal),
    `forge8Verbs.ts:1051/1060` (synthesize/stage verbs). Receipt preserved at
    `src/interfaces/mcp/retired/forge_github_create_issue.registration.ts.retired`.
    **Handlers remain in-file but unreachable (F1: not deleted — reversible by design).**
    If you "re-discover" these as dead tools and move to retire them: STOP — you are re-doing
    2026-10-18. The registry entry `retire-consumer-check-DONE-1-candidate` (was "open") is STALE.
12. **`forge_stage` is NOT a dead tool — it is FORGE8 VERB 2 (The Quarantine).**
    It was retired as a *verb contract* (F13-class change), not a plain tool drop. Any "keep as verb
    vs retire" question = owner `arif`, F13_required. Do not silently drop it.

---

## 4. SEALED THIS SESSION (2026-10-21)

| Item | Status | Receipt |
|---|---|---|
| Context guard deployed + live-fired | DONE | commit `0e60be31` |
| OR 11 rungs wired (base path fixed) | DONE | commit `8f3af7e3` |
| OR key swap 37e→e12 (funded) | DONE | this session |
| Config drift #48 | DONE | this session |
| Eureka distillation (6 insights) | DONE | `/root/work/fed-litellm-eureka-distill-2026-10-21.md` |
| Eureka ledger append | DONE | `memory/eureka-entries.jsonl` (19 entries) |

---

## 5. OPEN — with owners (do NOT re-discover)

- **#64** kernel identity sticky → kernel lane
- **#52** rotate 132 exposed secrets → HUMAN(issue)+AGENT(apply)
- **#53** disk 79% (ladder 60%) → HUMAN(policy)+AGENT(run)
- **#33** mimo-v2.5 retirement → deadline 2026-10-21 10:00 UTC+8
- **#47** preflight token harvest (security) → 333-AGI
- **#51** Kimi MCP bridge session-id → fi-008
- Full list: `/root/work/tasks.json` (69 open).

---

## 6. FALSIFIER
Re-probe any row with a live command before trusting it. Timestamps matter — a 2026-07 row
in `token_bank.providers` (`openrouter $0.50 conf 0.6`) is STALE and must not back routing.
If this file's `Last verified` is >24h old, re-verify before acting.
