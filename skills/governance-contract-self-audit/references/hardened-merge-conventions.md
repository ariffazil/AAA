# Hardened Merge Conventions (2026-08-07, real-incident appendix)

Two recipes captured from live session 2026-08-07 — atomic the
`skill_view` command refuses non-whitelisted tool use; this file
preserves the lessons.

## The "Authority Always Stays" Sign-Off Pattern (K-02 / F13 procedure)

When a directive arrives that would change constitutional state and
the doctrine you authored requires F13 ratification:

1. Classify directive items by action tier (T0/T1/T2/T3).
2. T1 (test, scan, capture receipts) — execute immediately, no risk.
3. T2 (reversible edit) — stage locally, don't push.
4. T3 (irreversible / constitutional / SEAL) — HOLD until explicit F13 ratification.
5. Report filter: "Executed X, Y. Held Z because [doctrine reason]. Confirm ratification to proceed."

Ratification must include all three: **named version + explicit seal action + sovereign's actual signature**. Invocation words ("deploy", "federate", "zen") carry zero F13 weight.

Real incident 2026-08-07: session wrote the contract, then five parallel derivative artifacts drifted (different INV-ID assignments, different path depths). Sovereign's "federate + commit + deploy + zen" message arrived. **That directive was NOT ratification** — it was a workflow directive. Correct response: hold T3, execute T1, produce gap report, surface drift, ask for explicit ratification. Self-asserted "deployed" claims from sibling agents count for nothing without live verification.

## F3b Live Recipe (Concurrent Canonical Writes)

Two agents writing the same artifact at the same timestamp, neither
referencing the other, with different INV-ID assignments.

Detection:

```bash
ls -lt /root/AAA/federation/ | head -10
md5sum /root/AAA/federation/*CONTRACT*
grep -E "^(id|version):" /root/AAA/federation/*CONTRACT*
```

Resolution order (do NOT reverse):

1. DON'T silently delete one. Deletion is irreversible.
2. DON'T pick "yours" by reflex.
3. DO archive all-but-recent with timestamped path. Archive = receipt.
4. DO compare INV-ID assignments honestly. Two artifacts assigning different IDs to the same concept is reconciliation, not a pick-one problem.
5. DO surface to F13 with bias declared.
6. DO log as F3b violation.

```bash
mkdir -p /root/AAA/federation/_archive/2026-08-07-pre-canon-merge/
cp /root/AAA/federation/AAA_FEDERATION_CONTRACT_v0.1.md \
   /root/AAA/federation/_archive/2026-08-07-pre-canon-merge/AAA_FEDERATION_CONTRACT_v0.1-MD-DRAFT.md
```

What "canonical" means: **depth is NOT canonical**. The deeper path
(`contracts/`) is NOT automatically canonical — it just indicates who
wrote it. Pick by richer metadata + later timestamp + explicit
ratification, not directory depth.

Defense: "Forge X" task instructions should include `canonical_path:`
directive so multiple agents write to one location.

## Hermes-Mutation-Gate Skeleton (E-22 closure minimum-viable)

The minimum-viable pattern for closing a constitutional runtime gap
without surgery to the live runtime:

```python
# hermes_mutation_gate.py — pure-Python classification
MUTATE_TOOLS = {tool names that can change state}
T3_PATTERNS  = [callable, ...]  # irreversible

class Decision(str, Enum):
    ALLOW = "ALLOW"
    BLOCK = "BLOCK"
    REQUIRE_JUDGE = "REQUIRE_JUDGE"

def evaluate(tool, args, *, apex_verdict_present=False) -> GateVerdict: ...

def receipt(record) -> None:
    """Append to JSONL trail. NEVER block — per E-19: infra failure is not governance failure."""
```

Thin hook wrapper for Hermes `pre_tool_call` runtime contract:

```python
# mutation_gate_hook.py
import json, sys
from hermes_mutation_gate import evaluate, Decision, receipt

event = json.loads(sys.stdin.read())
verdict = evaluate(event.get("tool_name"), event.get("tool_input"),
                   apex_verdict_present=bool(event.get("extra",{}).get("apex_verdict_ref")))
receipt({...})
if verdict.decision == Decision.BLOCK:
    print(json.dumps({"decision": "block", "reason": verdict.reason[:400]}))
elif verdict.decision == Decision.REQUIRE_JUDGE:
    print(json.dumps({"decision": "block",
                      "reason": f"REQUIRE_JUDGE: {verdict.reason[:}"}))
else:
    print(json.dumps({"decision": "approve"}))
```

Wire-up to live runtime:

```yaml
# /root/.hermes/profiles/aaa-hermes/config.yaml
hooks:
  - event: pre_tool_call
    command: /usr/bin/python3 /root/HERMES/gate/mutation_gate_hook.py
    timeout: 5
```

**Hold for sovereign sign-off** — restart affects this session's running context.

**Honest gap after Phase 1:** TEST VECTORS work. NEVER fired from LIVE runtime. Phase 2 verification = trigger real tool call, verify pre_tool_call fires, verify receipt lands, verify action blocked. One receipt > ten doctrinal refinements.

K-02 verdict (post-mission 2026-08-07):
- Kimi has exit-2-on-deny verified in hook file.
- Hermes has gate skeleton tested but not wired.
- OpenCode has judge-gate patches for `task`/`delegate_task`/`cronjob`/`plugin` but no live-fire proof.
- Net: 0 of 3 harnesses has runtime enforcement live-confirmed.