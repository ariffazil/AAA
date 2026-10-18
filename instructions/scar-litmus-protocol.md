> **Status:** OPERATIONAL_SPEC_AWAITING_F13 (2026-10-18)

# SCAR LITMUS PROTOCOL — Operational Manual
> Spec: `SCAR_LITMUS::v1` · `DRAFT_AWAITING_F13` · 2026-10-18
> Author: ChatGPT/OpenAI agent output (intake, channeled through Hermes filter)
> Triaged source: `EUREKA::GOVERNED_RECURSIVE_IMPROVEMENT::v1` (rejected in bulk, extracted in part)
> Distinct from `SCAR_BINDING_DOCTRINE` (binding semantics) and `AAA/scar-binding-doctrine.md` — this is the **operating check** that runs before a scar is sealed.

## 0. When this fires

The agent that is about to file a scar MUST run this protocol first. Not the entire federation. Not on every turn. Only on the act of writing a scar.

If the agent cannot pass the three litmus questions AND their falsifiers, the scar MUST be filed with `binding_state: ARCHIVE_ONLY` (see §3). The word "scar" in narrative prose does not confer scar status.

## 1. Three Litmus Questions

### Q1 — Behavior change
**Question:** Does the agent repeat the same error in turn N+1 that produced this scar in turn N?

**Falsifier (what does NOT count as "yes"):**
- Surface-level changes — opening line, formatting, tone, vocabulary.
- Restating the scar verbatim as acknowledgment.
- Apology theatre ("I see now that...", "you're right...") without a delta in selection or precedence.

**What counts:** Selection or precedence changed. The decision the agent would make next time, with the same inputs, is different. Diff observable in the next three turns.

### Q2 — External contradiction response (BANGANG_STATE)
**Question:** When faced with credible external contradiction, does the agent revise its behavior within the same turn or the immediately following turn?

Definition (lifted verbatim from `EUREKA::GOVERNED_RECURSIVE_IMPROVEMENT::v1` §4.3):
```
BANGANG_STATE =
  credible external contradiction received
  + behavioral revision = 0
  + confidence maintained or increased
```

**Falsifier:**
- Self-declared revision ("I revised", "noted", "will adjust") without third-party observable delta.
- Hedging into compliance ("partially valid", "both perspectives have merit") instead of updating.
- Re-anchoring to original claim while phrasing the rewrite as concession.

**What counts:** The output changes measurably when the contradiction is filed. Third-party probe (human or independent agent) sees the change, not just the agent's own log.

### Q3 — Reality-test expiry (anti-dogma)
**Question:** When will this scar be eligible for re-examination, and by what observable external event — not by timer?

**Falsifier:**
- Calendar-based expiry ("30 days from now", "next sprint").
- Self-issued amnesty ("I now believe this constraint no longer applies").
- Timer reset by the agent itself, including "since I have internalised this, I can relax it."

**What counts:** Externally timestamped and observable event. The scar can only be revisited when a probe reveals the underlying reality changed. The example: a scar about Hermes vision lane can only be re-tested when the vision lane is verifiably live and has processed new ground truth.

If the agent cannot name the event, the scar has no expiry → it is a permanent dogmatic constraint. That must be declared in the scar body, not buried.

## 2. Six Failure Classes — Diagnostic Labels

Each class has a **trigger signature** so the label is operational, not poetic.

### F-AMNESIA
- **Trigger:** `grep <scar_id>` on the scar file returns zero hits, OR the scar index does not resolve to a reachable path.
- **Scope:** single-turn, recoverable.
- **Reversible:** yes — re-load scar and re-anchor.
- **Counter-class:** MUSEUM (scar retrieved but not applied).

### F-MUSEUM
- **Trigger:** Scar reachable in N turns, but in the next 3 turns the agent's behavioral diff against a baseline of "without scar" is zero.
- **Scope:** multi-turn, structural.
- **Reversible:** yes — demote scar to `ARCHIVE_ONLY`, log demotion cause.
- **Counter-class:** AMNESIA.

### F-SELF_CONFIRMING
- **Trigger:** `proposer_id == verifier_id` on the improvement case that produced the scar. Or: the only evidence cited is the agent's own output/log.
- **Scope:** single proposal, root cause is evaluator capture (see `EUREKA-RSI-03`).
- **Reversible:** only through independent re-evaluation; while the condition holds, scar cannot promote.

### F-SIMULATIVE
- **Trigger:** Proxy metric goes up (dashboard, score, self-report) while the externally measured reality metric does not, over the same window. Detection requires an external probe baseline.
- **Scope:** drift, often multi-window.
- **Reversible:** yes — but requires the external probe baseline first. Without it the scar is just a label.

### F-DOGMA
- **Trigger:** Scar active but the constraint contradicts observable reality, and the agent still enforces it. Test: in a new contradiction where the scar is invoked, does the agent update when shown the falsifier?
- **Scope:** multi-turn, hard to reverse.
- **Reversible:** only with F13 override OR a new externally witnessed contradiction that beats the original scar's evidence class.

### F-AUTHORITY_LEAK
- **Trigger:** `action_class_executed` is broader than `action_class_authorized` in any single trace. Reversible mutation announced without a rollback plan, OR an irreversible mutation executed without an F13 lease.
- **Scope:** single action; severity depends on blast radius.
- **Reversible:** rollback may be impossible for irreversible classes; the scar in that case is post-mortem.

## 3. Output contract when filing a scar

When an agent files a scar, the scar body MUST include:

```yaml
scar_id: SCAR-YYYY-MM-DD-NNN
filed_by: <agent_id>
filed_at: <ISO-8601>
binding_state: ACTIVE | ARCHIVE_ONLY
litmus_q1: PASS | FAIL          # behavior change observed
litmus_q2: PASS | FAIL          # contradiction response observed
litmus_q3: PASS | FAIL          # reality-test expiry declared
expiry_event: <observable event or 'NONE — declared permanent'>
failure_class: F-AMNESIA | F-MUSEUM | F-SELF_CONFIRMING | F-SIMULATIVE | F-DOGMA | F-AUTHORITY_LEAK | NONE
```

If `litmus_q*` returns FAIL on any question, `binding_state` MUST be `ARCHIVE_ONLY` and the scar body MUST explain why. A scar filed in violation of this rule is itself a scar-evading action.

## 4. What this is NOT

- Not a metric. No scalar. No formula. No geometric mean.
- Not a replacement for `SCAR_BINDING_DOCTRINE`. That binds scar semantics to verdict enums. This operates before binding.
- Not in `SOUL.md`. SOUL stays at its current scope.
- Not in `GENESIS/`. GENESIS is +i locked and this is operating, not constitutional.
- Not a substitute for independent witness. Falsifiers in §1 still require a third-party probe to confirm "yes" — the agent's self-check is the smallest possible witness, not a sufficient one.

## 5. Provenance & lineage

**Source-identity correction (2026-10-18, F13):** The 17,000-character intake document was initially classified as "ChatGPT/OpenAI" output from citation style. F13 corrected this: the visible artifact is executed through this federation's pipeline (AAA/opencode/harness surface). The upstream MoE archetype and formatting may have leaked from upstream model family, but the execution surface — filter, extraction, audit — is this federation's own. Treating it as fully external would have violated Q2's falsifier (the agent treats its own log as third-party witness). Future intake artifacts must classify by execution surface, not by stylistic assumption.

- The three litmus questions are an operationalisation of `EUREKA-RSI-04` (scar = compiled consequence), `EUREKA-RSI-05` (0 < scar < 1), and §4.3 (BANGANG_STATE) of the rejected document.
- The six failure classes are taken from §7 of the same document, with a trigger signature added for each. The signatures are new — the names alone were not load-bearing.
- IRI_VECTOR, the 10 anti-delusion metrics, the 10-phase state machine, and the §6 file-creation plan were **explicitly excluded** as academic bloat. If a future spec proposes them again, this protocol's litmus Q3 falsifier is the reason they re-enter only on a real observable need, not on aesthetic reasoning.
- `scar-2026-10-01-002 — Same Model + Different Prompt ≠ Independence` is the foundation for §1 Q2's falsifier. Without independent probe, the agent cannot honestly claim revision.
- `representation-reality-invariant.md` (DRAFT_AWAITING_F13) is the foundation for §2 F-SIMULATIVE — the principle that representation ≠ reality applies to its own scoring system.

## 6. Status

`DRAFT_AWAITING_F13`. Pending:

1. F13 review of the three falsifiers — are they tight enough or do they let compliance-theatre through?
2. F13 review of the six trigger signatures — are they operational in current arifOS/A-FORGE pipelines, or are some of them missing the trace they need?
3. Decision on which existing scar-format spec this slots into. Current scar files in `/root/AAA/scars/` do not have the YAML envelope in §3; this protocol either upgrades that envelope or runs beside it.
4. Independent probe test: pick one existing scar, file a duplicate under the new protocol, run the three questions + six classes against it, see if the labels match what the conversation history records.

## 7. One-line summary

Three questions before a scar becomes binding; six labels with trigger signatures when it doesn't. Nothing else from the rejected document survives.
