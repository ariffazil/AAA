# Hermes Question Policy — Execution Blocker Contract v1

**Status:** F13_RATIFIED_CHAT (2026-10-15, sovereign in-session dictation; no separate seal marker) — **v1 contract supersedes the earlier same-day 5-rule draft.**
**Owner:** ask doctrine = `agent-question-budget` · transport = `AAA/telegram-ops` + live `clarify` tool · live surfaces = `SOUL.md` + `config.yaml`.
**Schema:** `hermes.execution-blocker.v1` → canonical JSON Schema at `/root/AAA/registries/HERMES_EXECUTION_BLOCKER_V1.json` (single source; not duplicated here).
**Kin:** `agent-question-budget` (F13 2026-09-23) · SOUL.md Action / First-Ask / Energy Ledger · scar FLOW rule · `care-governor` · `telegram-ops`.

---

## 0. The correction — and the acknowledgment pattern

> "Betul, aku salah tafsir. **Bukan human-in-the-loop dan bukan approval system.** Hermes berjalan autonomi."

How to acknowledge a correction: **satu ayat akui** → restate the corrected rule → execute under it
immediately. No re-litigation (First-Ask Compliance), no second cleverer reading (care-governor), no
apology loops or scorekeeping (Energy Ledger — invoice-scan violation).

**The Telegram button is not authorization. It is merely a typed input mechanism for a genuinely
missing execution parameter.**

---

## 1. Canonical definition

```text
EXECUTION_BLOCKER exists only when:

1. A concrete execution has been requested.
2. Execution has reached a specific decision point.
3. One required input is missing, invalid, or irreducibly ambiguous.
4. Hermes cannot obtain that input from available evidence or tools.
5. No authorized safe default exists.
6. Choosing incorrectly could change the target, consequence, or irreversibility.
7. Arif can resolve it with one bounded answer.
```

All seven conditions **MUST** be true.

```text
If any condition is false: NO TELEGRAM QUESTION
```

---

## 2. Exact blocker rules

### B0: Concrete execution must exist

A question is permitted only if Hermes is already processing a specific executable request.

```text
### Blocker
"Deploy repository X" / "Send report Y" / "Run job Z" / "Update configuration A"

### Not a blocker
"Explore possible improvements" / "Think about deployment" /
"Review the architecture" / "Maybe we should update this"
```

For non-execution work, Hermes may research or prepare silently, but must not summon Arif through Telegram.

### B1: The missing value must be execution-critical

The answer must be required by the executor, API, command, or operation contract.

```text
### Valid
target_environment is required / destination_chat_id is required /
repository is unresolved / destructive scope cannot be determined /
two credentials are available but account ownership differs

### Invalid
preferred writing style / whether Arif wants more detail /
whether Hermes should continue investigating / whether a nicer implementation exists /
whether Arif agrees with Hermes' reasoning

Test: Can execution technically and correctly continue without this answer?
If yes, it is not a blocker.
```

### B2: Hermes must attempt resolution first

Before asking, Hermes must resolve the missing value from:

```text
1. Current instruction  2. Current execution context  3. Command or workflow parameters
4. Canonical configuration  5. Existing project metadata  6. Recent valid task state
7. Available read-only tools  8. Explicitly authorized defaults
```

Prohibited: "Ask first because asking is easier." Required: **Resolve first. Ask only after resolution fails.**
Hermes must not ask Arif to supply information it can retrieve itself.

### B3: No authorized safe default may exist

If a valid default is declared by configuration, workflow policy, or the current request, Hermes must use it.

```yaml
default_resolution_order:
  - explicit_current_instruction
  - execution_manifest
  - canonical_project_config
  - workflow_specific_default
  - reversible_lowest_scope_default
```

Hermes must not invent a default merely because one seems conventional.

```text
deployment.default_environment: staging  →  Use staging. Do not ask.
No default declared and choosing changes the consequence  →  Ask once.
```

### B4: Ambiguity must be material

Ambiguity is a blocker only when different interpretations produce materially different execution.

```text
Material: different recipient / repository / environment / account / data scope /
mutation / financial consequence / external communication / irreversibility

Non-material: formatting / wording / log verbosity / internal implementation choice /
temporary filename / equivalent tool selection / retry strategy within policy
```

Non-material ambiguity must be resolved autonomously.

### B5: The answer must belong to Arif

```yaml
human_owned:
  - intended_target
  - external_recipient
  - account_identity
  - irreversible_scope
  - mutually_exclusive_business_choice
  - missing_secret_or_credential
  - requested_output_destination

agent_owned:
  - implementation_method
  - library_selection
  - retry_count_within_policy
  - internal_file_layout
  - diagnostic_procedure
  - reversible_technical_optimization
  - ordinary_error_recovery
```

Hermes may ask only for human-owned values. Agent-owned matters are decided by Hermes itself.

### B6: The question must unlock immediate execution

```text
Valid:    "Which target?" [Production] [Staging]
Invalid:  "How would you like me to approach this?" [Carefully] [Quickly] [Explain more]

Formal test: answer → bind missing field → resume execution
```

If further analysis is still required after the answer, Telegram interruption is generally not justified.

### B7: The question must be bounded

```yaml
allowed_question_types:
  - single_choice
  - bounded_multi_choice
  - yes_no_for_missing_fact
  - short_value
  - secret_required

forbidden_question_types:
  - approval_request
  - open_ended_consultation
  - status_acknowledgement
  - emotional_reassurance
  - reasoning_review
  - policy_delegation
  - repeated_clarification
```

### B8: One question per blocker

One compact Telegram message for the smallest unresolved field. Never a questionnaire.

```text
Resolve all possible fields autonomously.
Ask only for the first field that blocks the next executable step.
After Arif answers, resume. One additional question only for a new, genuinely unavoidable blocker.
```

### B9: No repeated interruption

A blocker question requires a stable `blocker_id`. The same unresolved question is never sent twice.

```yaml
deduplication:
  key: [execution_id, blocker_code, field, options_hash]
  duplicate_action: SILENT
```

No reminder, escalation, or "still waiting" message unless Arif explicitly requests reminders.

### B10: Timeout means silence

```text
Do not proceed with the blocked mutation.
Do not send reminders. Do not announce HOLD. Do not produce a failure monologue.
Remain silent. Internal state may stay WAITING_INPUT — the label must not create Telegram noise.
```

### B11: HOLD is not a question

Never a button trigger: uncertainty · governance HOLD · low confidence · incomplete verification ·
tool failure · elevated risk · wanting approval · wanting reassurance.

```text
Required: recover autonomously if possible, otherwise stop silently.
A HOLD becomes a valid blocker only if Hermes identifies one exact missing value satisfying B0–B10.

Bad:    "Deployment is on HOLD. Approve?" [Approve] [Reject]
Valid:  "The command requires an environment, but none is defined." [Staging] [Production]
```

---

## 3. Blocker decision function

```python
def classify_blocker(ctx) -> str:
    if not ctx.concrete_execution_requested:
        return "SILENT"
    if not ctx.at_execution_decision_point:
        return "CONTINUE"
    if not ctx.required_field_missing:
        return "CONTINUE"
    if ctx.recoverable_by_tools_or_evidence:
        return "RESOLVE_AUTONOMOUSLY"
    if ctx.authorized_safe_default_exists:
        return "USE_DEFAULT"
    if not ctx.material_consequence_difference:
        return "CHOOSE_AUTONOMOUSLY"
    if not ctx.answer_owned_by_arif:
        return "CHOOSE_AUTONOMOUSLY"
    if not ctx.answer_immediately_unlocks_execution:
        return "SILENT_STOP"
    if not ctx.question_can_be_bounded:
        return "SILENT_STOP"
    if ctx.same_blocker_already_sent:
        return "SILENT_WAIT"
    return "ASK_TELEGRAM_ONCE"
```

---

## 4. Machine-readable instance schema (example record)

> **Shape note:** the nested view below is the logical view; `hermes.execution-blocker.v1` (§5)
> serializes the record **flat** (`execution_id` / `blocker_id` / … at top level). Validate the flat
> form — verified 2026-10-15: §4 values pass `jsonschema.validate()` against the canonical schema,
> and approval-style records (`resume_execution: false` / `send_acknowledgement: true`) are
> correctly rejected.

```yaml
schema_version: "hermes.execution-blocker.v1"

execution:
  execution_id: "EXEC-20261015-001"
  requested: true
  operation: "deploy"
  target: "GEOX"
  state: "BLOCKED_INPUT"

blocker:
  blocker_id: "BLK-20261015-001"
  code: "MISSING_REQUIRED_TARGET_ENVIRONMENT"
  field: "target_environment"

  conditions:
    concrete_execution_requested: true
    at_execution_decision_point: true
    required_field_missing: true
    resolution_attempted: true
    recoverable_from_evidence: false
    recoverable_from_tools: false
    authorized_safe_default_exists: false
    materially_changes_execution: true
    answer_owned_by_arif: true
    answer_immediately_unlocks_execution: true
    bounded_question_possible: true
    duplicate_question: false

  resolution_trace:
    checked:
      - current_instruction
      - execution_manifest
      - canonical_project_config
      - recent_valid_task_state
      - available_read_only_tools
    result: "UNRESOLVED"

  question:
    type: "single_choice"
    text: "Target environment?"
    options:
      - { id: "staging",    label: "STAGING",    value: "staging" }
      - { id: "production", label: "PRODUCTION", value: "production" }

  telegram:
    allowed: true
    send_once: true
    reminders: false
    expose_internal_reasoning: false
    callback_prefix: "hbx"
    expires_at: null

  on_answer:
    bind_to: "execution.parameters.target_environment"
    resume_execution: true
    send_acknowledgement: false

  on_no_answer:
    state: "WAITING_INPUT"
    telegram_action: "SILENT"
    execution_action: "NO_MUTATION"
```

## 5. JSON Schema

Canonical validator: **`/root/AAA/registries/HERMES_EXECUTION_BLOCKER_V1.json`**
(`$id: arifos://schemas/hermes-execution-blocker-v1.json`). It is the single source of truth for
record validation — deliberately not duplicated in this file.

---

## 6. Mapping — the morning's 5 rules → B-rules

| Rule (2026-10-15 dictation) | Contract home |
|---|---|
| 1. Cukup maklumat → terus execute | B2 (resolve first) |
| 2. Tak cukup maklumat yang menghalang execution → tanya butang | §1 seven conditions |
| 3. Boleh guna default selamat → guna default | B3 |
| 4. HOLD, warning, status, progress, banyak songeh → diam | B10 + B11 |
| 5. Tiada pilihan munasabah → berhenti senyap | B6 + B7 |

---

## 7. Transport — the live wiring (probe 2026-10-15)

**The button GUI already exists end-to-end in the live stack** — the discipline layer was the gap,
not the mechanism. The `clarify` tool is the transport for B7 question types:

| Layer | Live location |
|---|---|
| Tool (1–5 questions, ≤4 choices, multi-select, open text) | `tools/clarify_tool.py:188`, schema `:246` |
| Turn suspension (blocking thread + in-memory Event) | `tools/clarify_gateway.py:46/58` via `gateway/run_turn_runner.py:1287` |
| Keyboard send (`cl:` prefix, numbered rows, callback_data ≤64 bytes) | `plugins/platforms/telegram/adapter.py:4387` `send_clarify` |
| Callback dispatch + auth gate | `adapter.py:4794/4920` (`cl:` table) + `_callback_authorized` `:898` |
| Typed-answer capture ("✏️ Other") | `gateway/run_inbound.py:399` |
| Timeout (`agent.clarify_timeout`, default 3600 s) | `clarify_gateway.py:259` |
| Answer ack (toast + buttons collapse via `edit_message_text`) | `adapter.py:4868` pattern |

**Known gaps (honest):**

1. **Nothing is persisted** — pending questions live in process memory; a gateway restart orphans
   them (buttons answer "expired"). B9 dedup and B10 `WAITING_INPUT` need a durable blocker store.
2. **`secret_required` must NOT travel as a Telegram message** — Telegram blocks login codes shared
   in messages, and secrets land in chat history (telegram-ops CORE RULE 7). Type stays in the
   schema; its transport is a side channel (file/SSH), never the chat.
3. Generic `send()` cannot carry a keyboard — keyboard prompts go through `_send_prompt` /
   `_send_control_message` (`adapter.py:4292/4278`).
4. `clarify` permits 1–5 questions per call; **B8 allows exactly one per blocker** — the gate
   enforces one, regardless of tool capacity.

---

## 8. Final invariant

```text
Hermes SHALL ask Arif only when one bounded, human-owned,
execution-critical value remains unresolved after autonomous resolution,
has no authorized safe default, materially changes the consequence,
and immediately unlocks the current execution.

Otherwise: EXECUTE, RECOVER, DEFAULT, OR REMAIN SILENT.
```

---

# Part II — Agentic execution: amendments, target state, build plan (2026-10-15)

**Provenance:** external design research ingested 2026-10-15 (forwarded by sovereign; testimony-gated —
design target, not observed fact). Key refs: ReAct (arXiv:2210.03629) · Anthropic *Building Effective
Agents* · Temporal idempotency/durable-execution docs · Anthropic *Demystifying evals* · Reflexion
(arXiv:2303.11366) · GEPA (arXiv:2507.19457). Live-status claims below are **PROBED on this box**
(2026-10-15, FI-008). The source's "999 SEAL ALIVE" close is styled text, not a kernel seal.

## 9. Amendments to v1 — the five corrections, audited and adopted

1. **Input ≠ authorization.** This contract governs the **input gateway** only (missing parameters).
   Authorization for authority-gated actions is a **separate lane** (`WAITING_AUTHORIZATION`) and
   remains legitimate. "No approve/reject buttons" binds the input gateway only — it does not
   abolish approval for money/irreversible/publish-as-person actions. *(Fixes an over-ban in v1 §7
   and the registry row: upstream `approval*.py` is excluded from the INPUT gateway, not from the
   federation's authority lane.)*
2. **Not-human-owned ≠ free choice.** Replace v1 §3's too-permissive branch:
   ```python
   if not ctx.answer_owned_by_arif:
       return "CHOOSE_AUTONOMOUSLY" if ctx.agent_choice_explicitly_permitted \
              else "BLOCK_UNRESOLVED_AUTHORITY"
   ```
   A value may belong to a registry, another owner, or no one yet. Likewise B3: "reversible
   lowest-scope default" must be **policy-declared** — convention is not authorization.
3. **Low confidence is not a missing field** — but may trigger bounded observation
   (`OBSERVE_AND_REVISE`: collect evidence → compare → revise plan), budgeted; never a Telegram
   question by itself.
4. **`FAILED_SILENT` is a notification policy, not an execution state.** Record
   `execution_status: FAILED · notification_policy: SILENT · failure_class · receipt_ref`.
   Silence ≠ absence of record (F2).
5. **Input resolution ≠ execution unlock.** `on_answer` semantics become
   `resolves_current_input_blocker: true → next_step: REVALIDATE_AND_CHECK_AUTHORITY` — authority,
   expiry, and target drift are re-checked before resume. *(v1 schema's `on_answer.resume_execution`
   reads as "resume the flow", not "execute blindly"; corrected in schema v2 at build time.)*

## 10. Target state machine (supersedes v1 state names)

```text
RECEIVED → PLANNING → READY → EXECUTING → VERIFYING → COMPLETED
                           ↑       │          │
                           │       ▼          ▼
                           └── RECOVERING / REPLANNING
READY → WAITING_INPUT      → REVALIDATING → READY
READY → WAITING_AUTHORIZATION → REVALIDATING → READY
EXECUTING → OUTCOME_UNKNOWN → RECONCILING → VERIFYING | READY | BLOCKED
Nonterminal → CANCELLED | EXPIRED | FAILED      (notification policy orthogonal, default SILENT)
```

Rules: no mutation from any `WAITING_*` · callback returns to **revalidation**, never straight to
the tool · a waiting task never blocks an independent task · budget expiry = recorded stop ·
repeated failure without new evidence forbids unbounded retry. **OUTCOME_UNKNOWN recovery:** timeout
with possible effect → never blind-retry the mutation → query destination/operation/idempotency
record → effect exists: verify · effect absent and retry safe: retry · still unknown: remain
blocked. ("Completion recorded once" ≠ "effect happened once" — Temporal idempotency refs.)

## 11. Build checklist — live status (PROBED 2026-10-15)

| Phase | Item | Live status |
|---|---|---|
| 1 | `hermes.execution-blocker.v1` canonical contract + JSON Schema | ✅ done (this file + `/root/AAA/registries/HERMES_EXECUTION_BLOCKER_V1.json`) |
| 1 | execution states + transitions | ❌ absent — no state machine; clarify pending = in-memory `threading.Event` only |
| 2 | required-field detection over tool schemas | ⚠️ tools carry JSON schemas (`clarify_tool.py:246`) but no blocker-detection layer |
| 3 | resolution ladder + `resolution_trace` | ❌ schema field exists, no executor |
| 4 | `classify_execution_gap` + unit tests | ❌ **PROBED absent** (0 hits on live path) |
| 5 | field-ownership registry (machine) | ❌ B5 lists exist as prose only |
| 6 | `is_material()` | ❌ absent |
| 7 | renderer rules (≤6 choices, one question, prompt callback ack) | ✅ transport exists (`send_clarify` `adapter.py:4387`, `cl:` dispatch `:4920`) — ⚠️ today ≤4 choices; needs gate + renderer rules |
| 8 | callback security (binding, consumed-once, replay guard, server-side options) | ⚠️ partial — `_callback_authorized` `:898` + opaque `cl:<id>:<idx>`; **no transactional consume, no replay guard** |
| 9 | dedup fingerprint + `sent_at/message_id/chat_id` | ❌ absent (in-memory; restart orphans) |
| 10 | transactional consume + durable resume event + revalidate | ❌ current = `Event.set()` → resume; crash after consume = stuck task (documented gap) |
| 11 | tests (14 unit + 8 integration + 9 failure-injection) | ❌ none exist |
| — | `task_contract` / `success_checks` / budgets | ❌ **PROBED absent** |
| — | `idempotency_key` honored at the actuator | ⚠️ exists in unrelated tools (kanban/modal/fal) — unproven in this path; acceptance test must show it reaches the mutation point |
| — | enforcement-hook precedent | ✅ `/root/.hermes/hooks/` carries `inbound-injection-gate` + `reality-claim-gate` (gate hooks) |

## 12. Forge order on this box

1. **Classifier + unit tests** (Phase 4 + 11-unit) — pure function with amendments §9; zero side
   effects; enforce via a gate hook (precedent: `inbound-injection-gate`), not prompt appeal.
2. **Durable blocker store** (Phase 9/10 prerequisite) — transactional consume + resume event +
   recovery scan for resolved-but-unresumed blockers at gateway start.
3. **Gate in front of `clarify`** — B8: exactly one question per blocker regardless of tool
   capacity (tool allows 1–5).
4. **Renderer + callback hardening** (Phase 7/8) — server-side option map keyed
   `hbx:<short>:<opt>`; reject unknown option / wrong user / replay / expired blocker; ack via
   `answerCallbackQuery` then edit buttons away.
5. **`task_contract` + OUTCOME_UNKNOWN reconcile** (Phase 5 + §10) — success checks before start;
   resume → revalidate → authority check → resume exact step.
6. **Failure-injection suite** (Phase 11) on an isolated destination. Metrics: verified success ·
   avoidable questions/task · unauthorized effects · duplicate effects · false completion ·
   crash-recovery · cost. **Do not optimize question-count alone** — silent failure scores zero
   questions while completing nothing.
7. **Baseline eval before any adaptive loop** (20–50 real tasks: fixed workflow vs v1 gate vs
   bounded controller). Reflexion/GEPA-style improvement = candidate lessons only, human-governed
   promotion (`memory-promotion-gate`); the optimizer may never touch F13, approval bindings, or
   success rubrics.

## 13. What this is — and is not

An **autonomy membrane**, not an intelligence generator. Success = more verified executions, fewer
avoidable questions, zero duplicate or unauthorized effects — never "Hermes asks better questions" as
a goal in itself. Intent and parameters (user/resolver with provenance) · planning and recovery
(Hermes, within scope) · authorization (arifOS + human where required) stay three separate layers.
The button fills a parameter; it never grants permission.
