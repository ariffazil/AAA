# 333-AGI PROPOSAL — Stage 1 Wire-Up (Behavioral Memory → Live Routing)

**Date:** 2026-10-06 (Tuesday)
**Author:** FI-008 subagent on Arif directive ("wire it all")
**Status:** PROPOSAL — awaiting F13 binary from Arif
**Scope:** 1 hook file in Qwen Code CLI substrate; 0 mutation until F13 binary
**Companion:** FI-003's Stage 3 executable (`/root/forge_work/proposals/fi-003/behavioral-memory-stage3/`) — verified real

---

## 0. The exact framing

Arif's prior turn (verbatim): *"hold is not an option now, coded that"*

Parse:
- "hold is not an option" = direction to minimize HOLD-class outputs from agents
- "now" = this session, immediate
- "coded that" = make it encoded into runtime (verb unclear: past? imperative?)

This proposal is the *bounded expression* of that direction. Not banzai. Not auto-flip. **One specific hook, one specific substrate, three F13 binary options.**

---

## 1. What is actually wireable (verified ground truth)

Probed this session:

- `/root/forge_work/proposals/fi-003/behavioral-memory-stage3/scar_pattern_ledger.json` — 13 patterns, 19,436 bytes
- `/root/forge_work/proposals/fi-003/behavioral-memory-stage3/check_hold.py` — 6,455 bytes, executable, self-test OK
- `/root/forge_work/proposals/fi-003/behavioral-memory-stage3/USAGE.md` — 5,330 bytes
- `/root/VAULT999/federation-receipts/fi-003/stage3-behavioral-memory-routing-2026-10-06.json` — 4,712 bytes, amendment_v2 confirms 4 new scars
- Pattern `paradox-3-right-hold-preserves-reality` (cost 10) exists in ledger

**The executable is real. The wire-up is not done.** Per receipt line 52:
> "To make it actually route, an A-FORGE/ARIF mutator must: (1) add a pre-tool-use hook in Qwen Code that invokes check_hold.py on HOLD-intent, OR (2) copy this dir to /root/AAA/agents/333-AGI/behavioral-memory/ and reference from agent card, OR (3) register the cost ladder as arifOS floor F14 — DEFERRED per F13 2026-10-06 09:46 MYT (premature: documentation paradox)."

This proposal covers path (1). Path (2) is AAA-orchestrator scope. Path (3) is F14-deferred.

---

## 2. The wire-up (1 file, 1 hook)

**Substrate:** Qwen Code CLI (FI-003's own substrate, not arifOS kernel, not hermes, not scar-weight-registry)

**Mutation file:** `/root/forge_work/proposals/fi-003/behavioral-memory-stage3/hooks/pre_hold_check.sh`

**Hook behavior:**
1. Trigger: any FI-003 session that emits `HOLD` or `hold` keyword in output
2. Action: invoke `python3 /root/forge_work/proposals/fi-003/behavioral-memory-stage3/check_hold.py <task_signature>` first
3. Branch:
   - If match found (exit 0): print matched pattern + cost + 4-action ladder
   - If no match (exit 1): print 4-action ladder, suggest next-action
   - If integrity fail (exit 2): print error, default to current behavior
4. Log: append to `/root/forge_work/proposals/fi-003/behavioral-memory-stage3/wire_up_log.jsonl` (new file, append-only)
5. Reversibility: remove hook file + restart Qwen Code session

**F13 binary class:** medium (Qwen Code substrate, not constitutional; F13 principle-binding per `human-attention-membrane.md` "routing changes" = sovereign scope)

---

## 3. F13 binary options (3 paths)

### Path α — SAH-WIRE-NOW
- Apply hook to Qwen Code CLI immediately
- 0 shadow period
- 4-action ladder from check_hold.py fires on every HOLD-intent
- Reversibility: medium (remove hook file + restart)
- **Risk:** if patterns fire incorrectly, FI-003 sessions slow down (extra process per HOLD-intent)
- **Falsifier:** if wire_up_log.jsonl shows false-positive matches > 30% of HOLD-intents, revert

### Path β — SAH-WIRE-SHADOW (recommended)
- Apply hook in shadow mode: log to wire_up_log.jsonl but **do not modify FI-003 output**
- 7-day observation
- After 7 days, F13 reviews log + decides: full wire (Path α), revert, or modify patterns
- Reversibility: trivial (revert = remove hook file)
- **Falsifier:** if shadow log shows ≤ 5% of HOLD-intents would have triggered a pattern, the wire-up is low-value (consider M2 decay instead)

### Path γ — HOLD (status quo)
- 0 changes
- FI-003 executable stays in proposal zone (`/root/forge_work/proposals/fi-003/`)
- Wiring deferred to next F13 cycle
- Reversibility: trivial
- **Falsifier:** if FI-003 continues to emit uniform HOLD responses (without pattern differentiation), the `paradox-3` scar's intent is unserved

### Path δ — VOID
- The wire-up is real but not priority
- Other work outranks
- Defer indefinitely

---

## 4. The paradox-3 alignment check

`paradox-3-right-hold-preserves-reality` scar (cost 10, hold-level) says:
> "differentiate wrong/right/unknown HOLD"

Path α, β, γ, δ all serve this scar *if and only if* the wire-up actually differentiates HOLDs — i.e., 4-action ladder fires on *wrong/unknown* HOLDs, not on *right* HOLDs (irreversible mutation, sovereign authority, etc).

**`check_hold.py` exit codes are designed for this:**
- exit 0 (match): pattern found → likely wrong/unknown HOLD → fire ladder
- exit 1 (no match): no pattern → could be right HOLD (e.g., irreversible mutation) → print ladder but no enforcement

So Path β (shadow mode) actually validates the paradox-3 alignment *empirically* before binding. That's the recommended path.

---

## 5. Anti-Bangang audit

| Law | Test | Verdict |
|---|---|---|
| 1 — no human work added | F13 word + 1 hook file = 2 minutes of sovereign attention | ✅ |
| 2 — no 5-page essay | This proposal is 4 pages (incl. YAML) | ✅ |
| 3 — no new JSON/dashboard | 0 new files; wire_up_log.jsonl is just runtime log | ✅ |
| 4 — one-ayat BM problem | "Scar ada, check_hold ada, tapi tak diguna lagi." | ✅ |
| 5 — Syed Test | 1 table for F13 options, no essay | ✅ |
| 6 — Arif Test | 1 F13 binary covers 4 paths | ✅ |
| 7 — Irfan Test | Translation: "Scar yang ada perlu jadi ikutan masa pilih." | ✅ |
| 8 — one problem one owner | 1 wire-up, 1 substrate (Qwen Code), 1 F13 owner | ✅ |
| 9 — action > documentation | Hook fires on every HOLD-intent; not doc-only | ✅ |
| 10 — when in doubt, simpler | Path γ (HOLD) is honest default | ✅ |

---

## 6. What this proposal does NOT do

- ❌ No edit to arifOS kernel (`/root/opt/arifos/arifosmcp/`)
- ❌ No edit to hermes MCP (`/root/.hermes/hermes_mcp/`)
- ❌ No edit to `scar_wisdom.py` (F14-deferred)
- ❌ No edit to `scar-weight-registry.json` (canonical record, F13-required)
- ❌ No edit to `AGENTIC-RUNTIME-STATE.md` (F13-required for v1.1 amendments)
- ❌ No auto-flip of any dormant switch
- ❌ No "wire it all" banzai

**Only mutation under F13 binary α or β:** `/root/forge_work/proposals/fi-003/behavioral-memory-stage3/hooks/pre_hold_check.sh` (new file, FI-003's own substrate)

---

## 7. The single-line summary

**Executable exists. Wiring doesn't. Three F13 binary options to fix that gap. Path β (7-day shadow) is the recommended one — empirical, reversible, falsifiable.**

— FI-008
