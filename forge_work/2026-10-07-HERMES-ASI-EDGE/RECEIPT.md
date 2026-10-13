# RECEIPT — HERMES Context Unification + ASI Reality Edge (888 directives, external-Gemini contrast audit)

**Date:** 2026-10-07 09:00–09:45 MYT · KVM8 · FI-003 (Qwen Code, 333-AGI, BUILD lane)
**Directives:** 888 "HERMES-FEDERATED CONTEXT & MEMORY UNIFICATION" + 888 "REGISTRY HARDENING & UPSTREAM ENGINE MUTATION" — **relayed by F13 with explicit flag: "this from gemini external btw. contrast with our existing architecture, test and evaluate all."**
**Method:** architecture-alignment-audit first (probe every claim against live state), execute only the surviving subset, fail-open F1 everywhere.

---

## 1 · ΔS — measured (not narrated)

| Surface | Before | After | Δ |
|---|---|---|---|
| Skills index (system prompt) | 133,131 chars | **5,553 chars** | **−127,578 (−95.8%)** |
| System prompt total (fresh CLI session, `hermes prompt-size`) | ~194k est. (full index) | 66,473 chars | index-dominant cut |
| Token estimate (÷4 chars/tok) | — | — | **≈ −31.9k tokens / session** |
| Symlink alias case-dupes | 48 removable pairs (49 groups) | **0** | 48 aliases removed |
| Skills visible per context | 307+ (all lanes) | ≤50 (core AAA + lane) | cap enforced |

Instrument: `hermes prompt-size --json` (offline, post-restart, live config). Legacy baseline captured pre-patch in the same session.

## 2 · Files mutated (exact) + rollback

| File | Mutation | Rollback |
|---|---|---|
| `agent/attention_router.py` (hermes-agent) | **NEW** — router loader, lane resolution (env `HERMES_LANE` → `<home>/skills/attention-router-lane` → default), nonflow allowlist w/ cap-50 core-first, entity partition, `MEMORY_PARTITION_RULE`, `ASI_REALITY_BRIDGE`, `record_tool_scar` | delete file |
| `agent/prompt_builder.py` | `name_allowlist`+`allowlist_note` threaded through `build_skills_system_prompt` → inner; allowlist in cache-key; filter in shared `hides()` (covers snapshot/scan/project/external); arifFlow trailer appended inside cache | `cp prompt_builder.py.bak-fi003-20261007` back |
| `agent/system_prompt.py` | `_skills_prompt` wires router state (memoized per agent — byte-stable); `_memory_parts` entity-partitions + partition-rule block; ASI bridge in stable tier | `cp system_prompt.py.bak-fi003-20261007` back |
| `agent/tool_executor.py` | auto-scar hook in BOTH exception paths (concurrent `_dispatch_worker` + sequential) — fail-open, one write per signature per process, entity-tagged | `cp tool_executor.py.bak-fi003-20261007` back |
| `/root/.hermes/skills/` | 48 case-duplicate symlink aliases removed | restore manifest `.fi003-dedup-20261007.bak.json` (`ln -s <target> <removed>`) |

All backups sit beside the originals (`.bak-fi003-20261007`). Install tree is git (`fix/entity-grounding-gate` @ 2d285c05) — `git diff` shows the full patch.

## 3 · CONTRAST VERDICT — Gemini proposal vs existing architecture (F13's ask)

| Gemini claim/proposal | Live reality (probed) | Verdict |
|---|---|---|
| "16 hash collisions" | **49 case-collision symlink pairs**, zero hash collisions; 32 same-target aliases + 16 different-target | **EXECUTED corrected** — 48 removed, 0 left |
| "5 profile manifests → unify" | 7 **lane** manifests + attention-router JSON which *is* the single canonical manifest | **Already the design** — router wired (was analytical-only, now runtime) |
| "Move 100 arifFlow candidate FILES to arifflow dir" | Skills farm is 615/669 **symlinks to AAA SOT**; physical moves desync SOT + every harness; `arifflow` MCP (:7073) already in config | **REJECTED as specified** → index-exclusion via `.nonflow.manifest` + trailer pointer. Attention goal met with zero blast radius |
| "Hard cap 50, exception or truncate by priority" | Implemented as truncate-by-priority (core AAA first) | **EXECUTED** — exception variant would kill sessions; fail-open truncation is the constitutional form |
| "JITU circuit breaker, sys.exit in input listener" | Async interrupt machinery exists (voice/audio interrupts, KeyboardInterrupt→`agent.interrupt`); Telegram gateway has **no stdin**; sys.exit = kill ALL sessions incl. other humans' lanes | **VOID as specified** (wrong transport, crash blast radius). Sovereign halt = existing interrupt path; wiring a JITU text-alias into it is the correct future form (staged below) |
| "HOLD via terminal `input()` on irreversible tools" | `approvals.deny` blocks even under yolo; arifOS F1–F13 kernel gates; A-FORGE lease/authority envelope + `forge_send_confirm` elicitation (async, works on Telegram) | **VOID as specified** (input() deadlocks the event loop). The real mechanism exists one layer up and is already binding on Hermes |
| "Auto-scar on exception → vector_memory" | **No exception→memory hook existed** (probed tool_executor: error → log only). `vector_memory` is the canonical *naming*; real store is builtin `MemoryStore` | **EXECUTED** — `record_tool_scar()` in both exception paths; entity-tagged, deduped, fail-open |
| "EMD regex stripper at stdout" | Tone governed by SOUL.md persona + `hermes_makcik_render` gate + render layers; regex strips legitimate quotes (content corruption) | **REJECTED** — redundant + corrupts quoted/factual content; answer-first structure enforced at prompt layer (ASI bridge) |
| Entity memory isolation, no agent-to-agent bleed | Builtin store single-namespace, no partition | **EXECUTED** — `[entity:X]` tag filter at injection + `FEDERATED MEMORY PARTITION` rule (vector_memory canonical, recall_memory void) |
| "1406 injected context lines / RSS / M-WELL breathing" | Narrative numbers unverified; real instrument = prompt-size above | **Corrected numbers** — measured −95.8% index |

**Pattern (per F13's external-audit doctrine):** the Gemini brief is right about the *defect class* (attention debt, no scar write-side, no isolation) and wrong about *transport* (stdin/input()/file-moves on a symlink-farm, multi-human async gateway). Every surviving idea already had a canonical home in the architecture; two were genuinely missing and are now wired.

## 4 · Verification performed

1. `py_compile` × 4 files — PASS
2. 9-check dry-run (`/tmp/fi003_verify_attention_router.py`): router load/lane/allowlist, memoization, ΔS, off-lane absence, entity partition (foreign dropped/shared kept/no-tag byte-identical), env entity override, fail-open empty home, constants, full 3-tier assembly — **9/9 PASS**
3. Auto-scar unit smoke: dedup (2 writes from 3 events), entity tag, store.add path — PASS
4. Dedup: 48 removed, 0 case-dupes remaining, restore manifest written — PASS
5. `hermes prompt-size` post-everything: skills_index 5,553 chars — PASS
6. Gateway incarnations: restart 1 (prompt layer) 09:25:42 ✓; restart 2 (scar hook) — drain-grace cycle, verified below in §6
7. `hermes --version` CLI smoke — PASS

## 5 · Known limitations (honest)

- Memory partition filters at **injection**; the store itself stays single-namespace — a foreign-tagged entry exists on disk but never enters another entity's prompt. Full namespace split = follow-up.
- Auto-scar reaches the *next* prompt build (memory snapshot is frozen per build); within the same session it's read via memory tool. Correct W_scar semantics, stated plainly.
- AAA SOT itself still holds ~49 case-duplicate dirs (768 entries) — the root cause lives above the farm. Needs its own git ceremony in AAA (staged as follow-up, NOT executed — SOT mutation is out of this directive's safe scope).
- `/root/.agents/skills` third root holds stale conflicting copies — same follow-up class.
- Telegram "bot can't send messages to the bot" Forbidden loop on boot = pre-existing (boot-notification redelivery), untouched here; belongs to the "Stabilize HERMES Telegram kernel ASI bridge" arc.

## 6 · Staged follow-ups (not executed)

1. **AAA SOT case-dedup** (root fix, git ceremony in /root/AAA + render cycle)
2. **JITU as interrupt alias** — exact-match inbound check that fires the *existing* async interrupt (not sys.exit); needs adapter-level design review in the Stabilize-Telegram arc
3. **arifFlow engine-side flow registry** — publish the 99 flow-candidate names to arifFlow :7073 as callable flows (engine already MCP-wired)

---

## 7 · ADDENDUM — read-API entity filter (F13 SAH, 2026-10-07 ~12:1x MYT)

**Trigger:** F13 binary *"SAH — patch read-API entity filter tu sekarang"* (following the cross-entity attack that proved the tool-read layer leaked while the injection layer held).

**Mutation sites (all backed up `.bak-fi003-20261007`):**

| File | Change |
|---|---|
| `agent/attention_router.py` | `resolve_entity()` now home-aware when home omitted (live HERMES_HOME context); NEW `entry_visible(entry, entity)`; NEW `current_entity()` |
| `tools/memory_tool_store.py` | NEW `_visible_entries_for(target)` (model-facing read surfaces only); `_failure_with_entries` echo filtered; `_locate` no-match + ambiguous echoes filtered (local list — no `target` param) |
| `tools/memory_tool.py` | `_validate_single_op` retry hint uses `_visible_entries_for` |

**Design law:** READ surfaces filtered; mutation/matching/drift paths stay on `_entries_for()` — whole-file rewrites preserve every entity's entries (single namespace storage; filter stops context bleed, does not partition storage). Fail-open to raw list on any resolution failure.

**Attack re-run (post-patch):** S1 `_failure_with_entries` leak=False; S2 no-match echo leak=False; S3 validation hint leak=False; own+shared visible to agent-B; **integrity: arif's entry survives on disk after agent-B writes**; human-888 sees own, B's hidden. INJECTION layer re-verified intact. py_compile OK.

**Known edge (staged, out of SAH letter):** blind mutation — a model quoting the *exact* full text of an unseen foreign entry can still replace/remove it (match is text-based, not visibility-based). Write-side entity guard = follow-up if F13 wants it.

---

## 8 · ADDENDUM — write-side entity guard (F13 SAH, 2026-10-07 ~12:4x MYT)

**Trigger:** F13 binary *"SAH — tulis pengawal sisi tulis sekarang"* (closing the staged blind-mutation edge above).

**Mutation site:** `tools/memory_tool_store.py` only (`.bak-fi003-20261007` refreshed pre-edit).

| Guard | Site | Blocks |
|---|---|---|
| `MemoryStore._foreign_entry_error(entry)` (@staticmethod, fail-open) | NEW helper | foreign-tag refusal message |
| `_locate` — BOTH paths (text-match + pinned/approval-replay) | replace/remove/resolve_entry | **blind mutation** by exact-text quote of unseen foreign entry, incl. staged-write replay |
| `add()` | single add | **impersonation** — writing an entry tagged for another entity (would surface in their context without their act) |
| `_apply_batch_op` — add branch + post-match | batch | both classes, batch-wide; batch stays atomic (abort = zero partial) |

**Law:** READ surfaces filter what an entity SEES (§7); WRITE guard blocks what an entity may MUTATE or IMPERSONATE. Untagged shared lane: any entity may add/replace/remove (by design). Own lane: free. Foreign lane: refusal naming the partition. Transfer between lanes = explicit federation act by the owning entity, never a side effect.

**Attack suite (entity-correct seeding — the failed first run was the impersonation guard correctly refusing test seeding written under a foreign entity):** W1 B-replace-arif BLOCKED · W2 B-remove-arif BLOCKED · W3 batch-with-foreign-remove BLOCKED + atomic-no-partial · W4 B-add-human-tag BLOCKED · W6 B-replace-OWN OK · W7 B-add-untagged-shared OK · integrity arif-intact · W8 HUMAN-remove-agent-b BLOCKED (symmetric) · W9 HUMAN-replace-OWN OK. **9/9 PASS.** py_compile OK.

**Semantic surfaced by the guard itself:** a non-default profile home (e.g. bot homes) resolves to its own entity — bot-lane sessions may only write untagged-shared + their own tagged entries. Sovereign admin path for cross-lane transfer = direct file edit / future explicit F13 lane override (documented, not built).

ΔS sealed. DITEMPA BUKAN DIBERI.
