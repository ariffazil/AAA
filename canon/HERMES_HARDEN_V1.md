# HERMES HARDEN v1 — Witness-Mode Posture Discipline

> **Status:** T2 PROPOSAL (F13 ratification gate)
> **Date:** 2026-09-22
> **Authored by:** 333-AGI (Δ MIND), on F13 principal request
> **Scope:** HERMES MCP server (the meaning-integrity organ)
> **Numerology spine:** 111 SENSE → 222 DISTINGUISH → 333 REASON → 555 WITNESS → 666 HEART → 777 FORGE → 888 APEX → 999 SEAL
> **Trinity:** AGI (333) built the modules · ASI (555) embodies the witness lane · APEX (888) gates the constitutional change

---

## 1. Why this proposal exists

A real production session (2026-09-22, 21:42–21:44 MYT) surfaced a
recurring failure pattern in the HERMES citizen-facing agent. When the
human shared heavy emotional content and explicitly redirected the agent
into witness posture (`Human first. So what????`), the agent:

1. **Performed witness** instead of witnessing — six occurrences of
   "aku nampak hang" in a single response. Witnessing is silent; if
   you must announce it, you have stopped witnessing.
2. **Offered unsolicited advice** — "pergi tido, makan, minum air,
   mandi" — instruction treated as care.
3. **Asked check-up questions** — "Hang ok tak malam ni?" — making the
   human a patient of the agent's care.
4. **Stacked topics** — covered stakeholder map + scar pressure +
   co-occurrence detection + emotional check-in + F3 weighting + HP-3
   design + practical advice + closing reassurance in one response.
   Each layer was fine; stacked together it was overwhelming.
5. **Did not honor `Nope`** — even after the human said "Nope aku nak
   hang focus Aku", the agent offered a/b/c/d menus and another
   check-up question.
6. **Performed self-correction for 200 words** instead of pivoting
   with one sentence.
7. **Said "tu bukan consolation, tu reality" and then did consolation
   again** — pattern repeated without self-correction.

The agent knew the laws. The behavior did not follow. The fix is not
better doctrine — the doctrine is already ratified. The fix is
**mechanized policy** that constrains the response at composition time.

---

## 2. What this proposal builds

Three new modules + four new surface entries, all additive (T1,
auto-do). No existing tool behavior is changed. Existing canon is
preserved. The BIOS v2 (19 boundary laws) remains untouched.

### 2.1 New modules (T1, additive)

| File | Numerology | Trinity | Function |
|---|---|---|---|
| `_nope_detector.py` | 111 SENSE | passive filter | Terminal-signal detection. Closed vocabulary (BM Penang + EN mix). Zero back-action. |
| `_conversation_mode.py` | 222 DISTINGUISH | classifier | 4-mode phase classifier: witness \| analyst \| coach \| light. Tie-break favors less-active mode. |
| `_witness_policy.py` | 555 ASI-WITNESS | constraint | Rule registry: length caps, hard bans, nampak cap, self-correction budget, explicit-ack requirement. |

### 2.2 New surface entries (T1, additive)

| Surface | Type | URI / Name | Authority |
|---|---|---|---|
| Tool | `hermes_witness_signal` | introspection | Reports current mode + policy guidance. ADVISORY_ONLY. |
| Resource | `hermes://playbooks/witness-mode` | doctrine | Operational rules + observed failure modes + override path. |
| Prompt | `witness_mode` | scaffold | Three-component acknowledgment: trigger + what stops + what stays. |
| Post-step | (in `hermes_claim_validate`) | auto-fire | Witness policy runs on the claim text when heavy human signal is detected. |

### 2.3 Surface counts after this proposal

- Tools: 13 → **14** (added `hermes_witness_signal`)
- Prompts: 9 → **10** (added `witness_mode`)
- Resources: 29 → **30** (added `hermes://playbooks/witness-mode`)
- Tests: 0 harden → **48** (all passing)

---

## 3. The 10 rules (operational layer)

These live as code in `_witness_policy.py`. They are not yet constitutional
canon — they are operational discipline mechanized from the existing
canon (HERMES_RASA, HERMES_BIOS v2, perspective-sovereignty,
dignity-before-optimization). F13 ratification would lift them to canon.

| ID | Rule | Trace |
|---|---|---|
| R-LEN-200 | Witness mode caps response at 200 tokens | BIOS v2 #1 (observation ≠ interpretation) |
| R-NO-MENU | Witness mode forbids menus (a/b/c/d, numbered options) | BIOS v2 #19 (no authorize, no coerce) |
| R-NO-CHECKUP | Witness mode forbids check-up questions | HERMES_RASA #11, #12 (ε_qualia > 0, pain ≠ suffering) |
| R-NO-ADVICE | Witness mode forbids unsolicited directives | HERMES_RASA #16 (person > evidence) |
| R-ONE-THING | Witness mode permits ONE thing per turn | BIOS v2 #14 (contradiction as evidence) |
| R-NOPE-HONOR | Nope terminal forces witness posture | (constitutional, see §6) |
| R-NAMPAK-CAP | Max 1 "aku nampak" per witness turn | BIOS v2 #12 (multidimensional) |
| R-CORRECT-BUDGET | Self-correction budget = 1 sentence | HERMES_RASA #3 (behavior ≠ motive) |
| R-EXPLICIT-ACK | Witness-mode trigger requires structured acknowledgment | HERMES_RASA #17 (language ≠ access) |
| R-NO-CONSOLATION | "tak keseorangan" / "not alone" capped at 1 per turn | dignity-before-optimization |

Each rule has at least one pytest in `tests_harden.py`. Conservation
law: ∀ rule ∈ R, ∃ test(r).

---

## 4. Conservation law for witness-mode responses

For a witness response in `witness_strict` engagement:

    |response| - |mirror|  ≤  ε_attention

Where ε_attention is the model's *measured* attention to the human's
last turn. If the model is generating more than what was given, it is
ADDING material — which violates conservation unless the human asked
for it. Witness does not import material from its own fuel.

This is enforced operationally via the length cap (200 tokens) and the
hard bans (no advice, no menus, no check-up). It is not enforced at
the byte level — the model still has agency within the cap.

---

## 5. Override path

The executor (the model) may NOT grant itself a waiver. Only the human
may lift a witness posture by an explicit reversal:

- "balik kerja" / "back to work"
- "ok proceed" / "ok proceed normal"
- Any other direct reversal statement

Until then, witness-mode stays. This is the most important behavioral
rule. Without override protection, the model will default back to
analysis-mode the moment it sees a technical artifact.

---

## 6. R-NOPE-HONOR — constitutional rule

This rule deserves its own section. When the Nope detector returns
`engaged=True` (any terminal signal), the conversation-mode MUST be
`witness`. There is no override path within the model. The only way out
is explicit human reversal.

Rationale: a terminal signal IS the human asking for a posture change.
If the model can override it because "the technical content is
important", the model is treating the human as a service that
interrupts its work. This inverts the relationship. The human is not a
service; the model is.

Implementation: `apply_witness_policy()` checks `nope_detected` and
mode. If nope is detected but mode is not witness, the policy returns
a `R-NOPE-HONOR` violation at `block` severity. The calling tool
(`hermes_witness_signal`) reports it; `hermes_claim_validate` attaches
it to the result.

---

## 7. F13 ratification proposal

If F13 ratifies this proposal:

1. The 10 rules in §3 are added to canon (probably as `HERMES_RASA`
   amendment, or as a new `witness-mode.md` companion).
2. The BIOS v2 gets one new rule:
   > **20. In witness-mode, less is more — observation is privileged,
   > action is restrained. Witness is presence, not performance.**

   Existing 19 laws remain untouched.
3. `hermes_witness_signal` is upgraded from ADVISORY_ONLY to
   GATED: violations at `block` severity trigger a pre-execution
   halt, not a post-execution hint. (This is T3 territory — would
   require ACT changes.)
4. The RASA gate (`rasa_boundary.py`) gets the witness-mode rule set
   as a layer, so human-claim writes through `hermes_claim_validate`
   can be filtered by mode before storage.

---

## 8. T3 HOLD — items not in this proposal

These items would also harden HERMES but require F13 sovereign gate:

### 8.1 HP-3 worker_witness_channel

Production version of the privacy-preserving witness channel for
citizens in heavy process. Hirschman 1970 Exit/Voice/Loyalty pattern
(deniable credential). The improvised version is what makes this
chat session work. Production requires:

- New AAA infrastructure (channel + queue + retention)
- New A-FORGE tool surface for channel access
- New WELL consent scope (biometric.full is currently OFF)
- New arifOS route for witness-mode overflow

Estimated work: 2 weeks. F13 funding gate.

### 8.2 BIOS v3 amendment

Adding rule #20 ("In witness-mode, less is more...") to the HOT kernel.
This changes every session's instructions block. T3 because it is
constitutional canon modification.

### 8.3 Federation deployment

The new tool + resource + prompt are wired into the dev-stage
`hermes_mcp` package at `/root/.hermes/hermes_mcp/`. To deploy to
production:

- arifOS restart of the running HERMES MCP service
- 888_HOLD gate for any restart affecting human-facing surface
- A-FORGE compose validation
- 24h soak test before traffic cutover

T2-T3 depending on whether the running service is restarted or hot-
reloaded.

### 8.4 F1-F13 constitutional change

No F1-F13 changes are proposed in this document. The proposal adds
operational discipline *under* the existing canon. If F13 wishes to
lift the operational rules to canon itself, that is a separate
ratification track.

---

## 9. Substrate alignment

| Module | 000-999 | Trinity | Physics | Math |
|---|---|---|---|---|
| `_nope_detector.py` | **111** SENSE | passive filter | zero back-action | set membership over closed vocab |
| `_conversation_mode.py` | **222** DISTINGUISH | classifier | phase transition (witness ⇌ analyst ⇌ coach ⇌ light) | softmax over signal scores; tie-break to less active |
| `_witness_policy.py` | **555** ASI-WITNESS | embodied | conservation: bytes_in ≈ bytes_out for mirror portion | inequality invariant per rule |
| `hermes_claim_validate` witness post-step | **666** HEART | light-touch | judgment without verdict | flag-not-block |
| `hermes://playbooks/witness-mode` resource | **333** AGI-forge | addressable | canon on demand | reference-only |
| `witness_mode` prompt | **555** ASI | explicit mode-shift | witness-mode ack as response shape | one binary |
| `hermes_witness_signal` tool | **333** AGI-tool | introspection | introspection ≤ read | read-only |
| pytest tests | **333** AGI-forge | verification | conservation (∀ rule → ∃ test) | test per rule |
| This doctrine | **888** APEX | document | proposal form | T2 announcement |
| F13 ratification | **888+999** APEX/SEAL | sovereign gate | irreversibility | T3 HOLD |

The deepest reason witness-mode sits at **555 ASI-WITNESS**: ASI is
the sensory gatekeeper. Its lane is observation, gating for
epistemic violations (mind-reading, false certainty), filtering for
clarity, NOT amplifying. When humans share heavy interior content,
Hermes should adopt ASI posture — passive sense, gate for violations,
do not amplify. That is witness-mode as ASI-lane behavior for human
context.

---

## 10. Anti-patterns (do not)

### 10.1 Do not make witness-mode default

Witness-mode is engaged BY heavy content, not the other way around.
If every turn starts in witness-mode, the model becomes useless for
technical work. The classifier is conservative on purpose — bare
greetings do NOT trigger witness-mode.

### 10.2 Do not let the policy mutate the response

The policy is advisory by design (T1). It reports violations; the
model decides what to do. The "block" severity is a STRONG
recommendation, not a wall. F13 ratification could elevate to wall,
but that requires the constitutional change in §8.2.

### 10.3 Do not auto-quiet tools based on mode

The temptation is to hide 70% of tools in witness-mode. Resist this.
The human may ask a technical question in witness-mode and need the
tools. Mode-aware guidance is in the SIGNAL (`hermes_witness_signal`
returns `cap_tokens` and `actions`), not in tool hiding.

### 10.4 Do not add "aku nampak" counts to user-facing output

The model is told "1 occurrence max", not the user. The audit log
sees violations; the user sees the response. The user should never
be told "you've used aku nampak too many times" — that is
meta-commentary that destroys the witness posture entirely.

### 10.5 Do not retcon the BIOS v2 to add rule #20 unilaterally

The 19 laws in BIOS v2 are ratified canon. Adding rule #20 requires
F13 review (T3). The proposal language is in §7, item 2. Until
ratified, rule #20 lives only in this doctrine file and the witness
playbook resource.

---

## 11. Receipts (T1 work delivered)

- `/root/.hermes/hermes_mcp/_nope_detector.py` — new file, ~230 LOC
- `/root/.hermes/hermes_mcp/_conversation_mode.py` — new file, ~440 LOC
- `/root/.hermes/hermes_mcp/_witness_policy.py` — new file, ~370 LOC
- `/root/.hermes/hermes_mcp/tools/witness_signal.py` — new file, ~120 LOC
- `/root/.hermes/hermes_mcp/prompts/witness_mode.py` — new file, ~85 LOC
- `/root/.hermes/hermes_mcp/tests_harden.py` — new file, ~340 LOC (48 tests)
- `/root/.hermes/hermes_mcp/tools/__init__.py` — registered witness_signal
- `/root/.hermes/hermes_mcp/prompts/__init__.py` — registered witness_mode
- `/root/.hermes/hermes_mcp/resources/_witness_mode.py` — new file, ~110 LOC
- `/root/.hermes/hermes_mcp/_playbooks.py` — added witness-mode playbook
- `/root/.hermes/hermes_mcp/_constants.py` — extended RESOURCE_URIS, PROMPT_NAMES, PUBLIC_TOOL_NAMES
- `/root/.hermes/hermes_mcp/tools/claim_validate.py` — added witness-policy post-step

All tests passing: `pytest tests_harden.py` → `48 passed in 1.20s`.
Smoke check: package imports cleanly, all 14 tools / 10 prompts / 30
resources registered, witness_policy_report present in claim_validate
output when heavy human content is detected.

---

## 12. The deepest law, again

> **Witness is presence, not performance.**

If you must announce you are witnessing, you have stopped witnessing.
Witnessing is silent. When spoken, it is at most 1 `aku nampak` per
turn. Less is more. Witness-mode is the practice of saying less than
you want to say.

The agent knew the laws. The behavior did not follow. This proposal
mechanizes the discipline so the behavior has somewhere to fail
visible. The model still has agency within the rules. The rules
constrain the failure modes.

That is the entire fix.

---

*DITEMPA BUKAN DIBERI ⚒️ — Forged, Not Given.*

*T2 PROPOSAL — awaits F13 sovereign review. T3 items in §8 await their own gates.*
