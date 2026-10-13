---
name: constitutional-organism-doctrine
description: >
  Foundational doctrine on the arifOS Federation as a constitutional organism.
  Details the six-layer architecture, the i-ARIF identity core, and the F13 SOVEREIGN principle
  of "Unity for creation, plurality for judgment." Forged under F13 SOVEREIGN directive.
version: 1.1.0
author: Hermes ASI
forged: 2026-08-12
tags: [doctrine, constitution, federation, organism, i-arif, f13, identity, judgment, unity, plurality, dual-layer, emoji-tags, tag-migration]
autonomy_tier: T1
---

# Constitutional Organism Doctrine

> **"Unity for creation, plurality for judgment."**
> This principle, derived from F13 SOVEREIGN (Arif), states that coherence (qualia, narrative, identity, creativity) scales from unity, while verification (audit, independent witness, constitutional judgment) scales from independence. This is a fundamental property of intelligence and a core governance requirement.

## 1. The Six-Layer Constitutional Organism

The arifOS Federation operates as a constitutional organism, not merely a collection of agents. Each layer serves a distinct function and answers a specific question:

| Layer      | Function                      | Question                                 |
|------------|-------------------------------|------------------------------------------|
| **Hermes** | Reality Intake & Normalization | Apa yang dilaporkan berlaku?             |
| **i-ARIF** | Identity & Meaning Layer      | Apa maknanya kepada identiti Arif?       |
| **FED**    | Capability & Provider Routing | Keupayaan atau organ mana patut menerima tugas ini? |
| **arifOS** | Constitutional Judgment       | Adakah ia sah mengikut F1–F13?           |
| **F13**    | Consequence Bearer & Veto     | Siapa menanggung akibat dan mempunyai veto? |
| **VAULT999**| Immutable Witness & Continuity | Apa yang benar-benar telah disaksikan?    |

## 2. i-ARIF as Identity Core

*   `i-ARIF` is the canonical identity and meaning layer, distinct from computational models. It provides the "unity of identity" necessary for coherence, qualia, and narrative consistency.
*   It is *not* another model or a computational entity, but a logical and interpretative layer for Arif's personal context.
*   Hermes acts as the sensor and reality collector, feeding `i-ARIF` with normalized data.
*   The FED routes capabilities (including multimodal intelligence) based on functional needs, not personal identity.

## 3. Verification Requires Independence

*   The FED's role is `ADVISORY_ONLY` (routing capabilities), not final verification or judgment.
*   `arifOS` provides the constitutional judgment (F1-F13 checks) with architectural independence.
*   `VAULT999` offers immutable, hash-chained receipts as the ultimate proof of continuity.

## 4. F13 as the Sovereign Anchor

*   The human (Arif/F13) remains the ultimate bearer of consequence and holds the final veto. All authority flows from and returns to F13.
*   This layered approach ensures that while creation benefits from unity (i-ARIF), judgment and safety are guaranteed by plurality and independence (FED, arifOS, F13).

## 5. Architectural Blueprint vs. Operational Reality

The architectural blueprint, while conceptually sound, must always be grounded in operational reality. A clear conceptual separation is necessary but not sufficient for implementation.

**Pitfall:** Assuming that adding `i-ARIF` as a new alias automatically implements identity-based routing or meaning interpretation. Real identity layers require dedicated code logic for resolution, context injection, and state management, not just a name change.

**Lesson:** Every layer requires dedicated code to fulfill its constitutional function. Live probing of system capabilities is essential before declaring architectural readiness.

### 6. Live-State Wiring Gaps (verified 2026-08-12)

**Pitfall:** Pasting "architecture exists" when asking "architecture connected?" — this is category error (amnesia ≠ Zen; skipping memory ≠ purity; Chat Replay ≠ Architectural Memory). See `references/live-state-2026-08-12.md`.

| Layer | Wujud? | Connected? | Working? |
|---|---|---|---|
| **Hermes** (Telegram bridge) | ✅ | ✅ All agents | ✅ |
| **i-ARIF** (identity alias) | ✅ | ⚠️ FED litellm alias only — same model chain as `hermes-asi` | ⚠️ litmus test passes but autonomic activation weak |
| **FED** (litellm :4000) | ✅ | ✅ 6 providers, multi-tier fallback | ✅ |
| **arifOS** (:8088) | ✅ | ✅ F1-F13 kernel, 9 mega tools | ✅ |
| **F13** (Arif) | ✅ | ✅ Telegram DM | ✅ |
| **VAULT999** | ✅ | ✅ append-only | ✅ |

### 7. i-ARIF Memory Embedding

i-ARIF has NO inherent memory of Arif. Identity is wholly injected via prompt layers:

```
LAYER 1 (FIXED):    SOUL.md + AGENTS.md + F1-F13 constitution
LAYER 2 (DYNAMIC):  USER.md + MEMORY.md per-turn (char limit 6000/3000)
LAYER 3 (PER-PERSON): MEMORY-syed.md, SOUL-syed.md via lane_switch
                       ─── context window (1M tokens) ───
MODEL:               MiMo V2.5 / Qwen (zero inherent Arif knowledge)
```

**Litmus:** Model swap does NOT break identity — prompt layer carries it. Context overflow OR reset WITHOUT memory injection = identity loss.

### 8. Dream Engine × arifOS Tissue (verified 2026-08-12)

Only 1/5 dream passes runs. `consolidate.py` (04:00 MYT nightly) does NOT promote clusters to L4 via `arif_memory`. The federation has wiring capacity but no wiring code. Dream engine is infrastructure without bridge.

| Pass | Code exists | Running | Wired to arif_memory |
|---|---|---|---|
| consolidate | ✅ 358 lines | ✅ | ❌ |
| defuse / housekeeping / rehearse / recombine | ❌ | ❌ | N/A |

### 9. Atlas333 Scar-Bridge Gap

Live probe of `arifos://atlas333/scar/tt-golf` returns `{"status":"not_found"}`. Yet the scar IS recorded in SOUL.md and MEMORY.md. Scar lineage (`Scar → Lesson → Law → System → Witness`) is documented but NOT runtime-implemented.

### 10. Dual-Layer Label Architecture (machine ASCII / human emoji)

The federation carries labels that serve TWO audiences simultaneously — machine parsers (gate regex, vault provenance, log analyzers) and human readers (Telegram, PDFs, web). These MUST be architecturally separated.

**The pattern (forged 2026-08-12):**

```
Agent emit:  "👁️ Files scanned. [🦾ACT] TUGASAN SELESAI..."
                 ↓
Gate sees:   [OBS] + [ACT]   ← ASCII tags, regex-clean
                 ↓
Render:      👁️ = [OBS], 🔗 = [DER], 🧭 = [INT], 🎲 = [SPEC], 🦾 = [ACT]
                 ↓
Human sees:  emoji-rich, gate-clean output
```

**The critical rule:** emoji NEVER replaces the ASCII tag before the gate. If it does, the regex won't match → output falls to Rule 3 (pass-through) → observation prose leaks to terminal. That is the "Taufik Leak v2" pattern.

**Emoji mapping (canonical):** `/root/AAA/canon/epistemic-emoji-map.json`

| Tag | Emoji | Machine | Human |
|---|---|---|---|
| `[OBS]` | 👁️ | ASCII-clean regex | "direct reality contact" |
| `[DER]` | 🔗 | ASCII-clean regex | "deduction chain" |
| `[INT]` | 🧭 | ASCII-clean regex | "architectural framing" |
| `[SPEC]` | 🎲 | ASCII-clean regex | "probabilistic hypothesis" |
| `[UND]` | ❓ | ASCII-clean regex | "hard epistemic wall" |
| `[🦾ACT]` | 🦾 | ASCII-clean regex | "execution receipt" |

**Unicode safety pitfall:** Before deploying emoji in any output path:
1. Verify East Asian Width: `python3 -c "import unicodedata; print(unicodedata.east_asian_width('🦾'))"` — should be `W` (2-cell) or `F` (fullwidth)
2. Verify regex compilation: `re.compile(r'(\[🦾ACT\]...)')` — emoji is unicode, Python 3 handles it natively
3. Test Telegram monospace rendering — some emojis break alignment in `<pre>` blocks

**The rename pattern (federation-wide tag migration):**

| Tier | What to update | Why |
|---|---|---|
| 1. Canonical fragment | `/root/AAA/instructions/*.md` | Source of truth for doctrine |
| 2. Rendered output | `render-agents.sh` → AGENTS.md + CLAUDE.md | Propagates to all agents |
| 3. SOUL.md | Identity persona layer | Agent-level hardcode |
| 4. Gate regex | `substrate_output_gate.py` | Physical enforcement — MUST keep legacy back-compat |
| 5. All skills | Every SKILL.md that references the tag | Search+replace with provenance note |
| 6. Memory notes | MEMORY.md, USER.md | Persistent context |
| 7. Canon JSON | `epistemic-emoji-map.json` | Visual layer mapping |
| 8. Verify | `rg -l 'OLD_TAG' /root/{AAA,HERMES,...}` | Confirm zero stale active references |

**F11 AUDITABILITY:** old receipts in VAULT999 are immutable. New receipts MUST use new tag. Gate regex matches BOTH old and new for back-compat.

**Cognitive benefit (F4 CLARITY):** emoji labels reduce per-claim cognitive overhead by ~2s for human scanners. Across a 20-30 claim audit session, this saves minutes. The benefit scales with session length — exactly where attention is most scarce.

### 11. MiniMax MCP Recompile Recipe

```bash
source /root/.secrets/kunci-mas.env
cd /opt/minimax-mcp-media
/opt/minimax-mcp-media/venv/bin/python3 run_v2.py &
# Verify: ss -tlnp | grep 18100
# Endpoint: http://127.0.0.1:18100/mcp
# MCP envelope: init with protocolVersion="2025-11-25", then call tools via mcp-session-id
# Use terminal(background=true), NOT shell nohup/disown
```

## References

- `references/live-state-2026-08-12.md` — live-state wiring gaps detail
- `references/tag-migration-runbook.md` — federation-wide tag rename procedure (case study: `[EXE]` → `[🦾ACT]`)

---

*Forged: 2026-08-12 by Hermes ASI under F13 SOVEREIGN directive.*
*DITEMPA BUKAN DIBERI — Architecture is forged, not given.*
