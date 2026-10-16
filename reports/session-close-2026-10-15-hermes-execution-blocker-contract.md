# Session close — 2026-10-15 · Hermes question policy → Execution Blocker Contract v1 + Part II

**Actor:** FI-008 (kimi-code) · **Sovereign directives this session:** question-policy correction →
Execution Blocker Contract v1 → implementation checklist + agentic-execution research → *"compile
all remaining task and seal the session"*.

## Shipped (verified)

| Artifact | Verification |
|---|---|
| `/root/AAA/instructions/hermes-question-policy.md` (494 lines) — Contract v1 (7 conditions, B0–B11, `classify_blocker`) + Part II (5 amendments, target state machine, build checklist with PROBED status, forge order) | content grep + registry row |
| `/root/AAA/registries/HERMES_EXECUTION_BLOCKER_V1.json` | `jsonschema.validate()` §4 record **PASS**; approval-style record **REJECTED** |
| `config.yaml::hermes_question_policy` — 12-condition gate, dedup, one-question, transport_tool: clarify | YAML parse + assertions PASS |
| `SOUL.md` Question Policy paragraph → contract v1 (LIVE prompt surface) | grep 1 hit |
| `AAA/AGENTS.md` fragment row (v1 + Part II) | grep 1 hit |
| Live map: Telegram GUI = existing `clarify` tool chain (`clarify_tool.py:188` → `send_clarify` `adapter.py:4387` → `cl:` callback `:4920` → Event → resume) | subagent probe w/ file:line |
| Research UNKNOWNs resolved by probe: `classify_execution_gap`/`task_contract`/`OUTCOME_UNKNOWN`/`success_checks` **ABSENT**; `idempotency_key` only in unrelated tools | per-pattern grep |

## REMAINING TASKS (compiled)

### Forge track — Hermes agentic execution (order = priority)

1. **Classifier + unit tests** — `classify_execution_gap` (v1 + amendments: `agent_choice_explicitly_permitted` → else `BLOCK_UNRESOLVED_AUTHORITY`). Pure function; enforce via gate hook (precedent `hooks/inbound-injection-gate`), not prompt appeal. *Accept: Phase-11 unit list (14 cases) green; model prose cannot override disposition.*
2. **Durable blocker store** — transactional consume + resume event + recovery scan (resolved-but-unresumed) at gateway start; B9 fingerprint `SHA256(execution_id+blocker_code+field+canonical_options)` with `sent_at/message_id/chat_id`. *Accept: crash-after-consume test green; restart orphans recoverable.*
3. **Gate in front of `clarify`** — B8: exactly one question per blocker (tool capacity 1–5 must not leak). *Accept: second-question-blocked test.*
4. **Renderer + callback hardening** — server-side option map keyed `hbx:<short>:<opt>`; reject unknown option / wrong user / replay / expired-blocker; `answerCallbackQuery` then edit buttons away; no secrets in callback_data (≤64 B). *Accept: Phase-8 checklist + replay/no-second-execution test.*
5. **`task_contract` + OUTCOME_UNKNOWN reconcile** — success_checks + preconditions + budgets before start; timeout-with-possible-effect → query effect first, never blind retry; resume → REVALIDATE → authority check → resume exact step. *Accept: idempotency key provably reaches the actuator mutation point.*
6. **Failure-injection suite** (9 scenarios: Telegram down, store down, double callback, drift during wait, option invalid, bot restart, handler crash post-consume, success-but-receipt-fail) on an isolated destination. *Metrics: verified success · avoidable questions/task · unauthorized effects · duplicate effects · false completion · crash-recovery · cost. Never optimize question-count alone.*
7. **Baseline eval before any adaptive loop** — 20–50 real tasks × 3 configs (fixed workflow / v1 gate / bounded controller). GEPA/Reflexion-style learning = candidate lessons only, human-governed promotion (`memory-promotion-gate`); optimizer may never touch F13, approval bindings, success rubrics.

### Side debts (this session)

8. **Skill-index alias defect** — name `telegram-ops` resolves to retired alias door `forge-telegram-audit` (Skill loader loops the alias text; agents must read `/root/AAA/skills/telegram-ops/SKILL.md` directly). Fix: repoint index or retire the door.
9. **`secret_required` transport** — design side channel (file/SSH); NEVER Telegram text (telegram-ops CORE RULE 7: Telegram blocks login codes in messages; secrets persist in chat history).
10. **Schema v2** (at build time) — `on_answer` → `resolves_current_input_blocker: true` + `next_step: REVALIDATE_AND_CHECK_AUTHORITY`; conditions += `agent_choice_explicitly_permitted`.
11. **`hermes_question_policy` loader** — config block is DECLARED-only; machine enforcement needs a loader (today: prompt-level via SOUL.md).
12. **Unverified detail** — post-timeout behavior of `agent.clarify_timeout` (default 3600 s) must be confirmed to match B10 (silent, `NO_MUTATION`).

## Provenance notes

- Design research (11-phase checklist + 5 corrections + architecture) = external artifact ingested
  testimony-gated; live-status claims PROBED on box. Source's "999 SEAL ALIVE" close = styled text,
  not a kernel seal.
- v1 over-ban corrected via amendment 1: approval lane (`WAITING_AUTHORIZATION`) stays legitimate;
  "no Approve/Reject buttons" binds the INPUT gateway only.
- Leverage audit (scar-2026-10-01-003): this session produced 4 canon/registry artifacts + 1 live
  map + 1 policy layer — leverage claim = the ask-gate now has a canonical, machine-validated
  contract and a build order; zero behavior change in the live agent loop yet (honest: the
  membrane is specified, not yet enforced in code).

## Seal status (honest, 2026-10-15T00:08Z)

- **Kernel `arif_seal` (999):** refused — first call carried a corrupted token (my transcription
  error, `TOKEN_INVALID`); the deeper truth is `seal_allowed: false` — actor identity self-asserted
  → OBSERVE_ONLY token, `arif_seal` not in `allowed_next_verbs`. Identity escalation path exists
  (Ed25519 challenge or sovereign signing lane :18900) but is **F13-class — sovereign decides**.
- **`carry_forward` writer allowlist denies FI-008** (writers: 333-AGI, 555-ASI, FI-003, FI-009,
  FI-002, hermes) — open-loops could not be appended there.
- **Durable closure record = this file** + `arif_memory` L1 entry (session SEAL-61aeaaba02644f9a).
- Same honest shape as precedent (A-Z doctrine row): sovereign-chat + ritual-marker closure,
  `SEALED_EVENTS.jsonl` untouched.

DITEMPA BUKAN DIBERI ⚒️
