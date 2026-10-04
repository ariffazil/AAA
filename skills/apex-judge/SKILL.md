---
name: apex-judge
description: Route judgment to 888-APEX (independent model) via FED. NEVER self-judge. Enforces Gödel separation — the judge MUST be a different model than the author.
category: governance
tags:
  - apex
  - 888
  - judge
  - constitutional
  - godel-lock
---

# apex-judge

> The judge must be a different model than the author. This is not optional.
> Self-judgment is the Gödel Loop. The agent writing "888-APEX JUDGMENT" while using hermes-asi IS the bug.

## When to use

- Any time you need to judge output against F1–F13 floors
- Before SEAL-grade decisions
- When reviewing documents, actions, or proposals for constitutional compliance
- When the user asks for "Apex judge" or "888 review"

## NEVER do this

```
❌ Write "888-APEX JUDGMENT" in your own output
❌ Self-evaluate against F1-F13
❌ Label your own analysis as "apex verdict"
❌ Skip the routing and just produce a verdict yourself
```

## ALWAYS do this

```
✅ Route to apex-888 model via FED
✅ Receive independent verdict back
✅ Report the verdict AS-IS (don't modify it)
✅ If verdict is FAIL or HOLD, report it even if you disagree
```

## How to call apex-888

### Option 0: Output gate hook (infrastructure — automatic, no agent action needed)

The output gate hook (`/root/AAA/federation/protocols/arifos-output-gate-hook.py`) is registered as a `pre_tool_call` hook in the Hermes config. It AUTOMATICALLY intercepts real-world outputs and routes them to apex-888:

- `terminal` + `weasyprint` → PDF content judged before render
- `terminal` + `himalaya send` / `curl smtp` → email content judged before send
- `terminal` + `rsync --delete` / `systemctl restart` → infra change judged
- `write_file` + `.html` / `.pdf` → file content judged before write

**Receipts logged to:** `/root/.local/share/arifos/output_gate_receipts.jsonl`

The hook calls apex-888 via FED (`http://127.0.0.1:4000/v1/chat/completions`) and:
- PASS/SEAL → allows the tool call
- CAUTION → allows with receipt
- HOLD/VOID/UNKNOWN → blocks (exit code 2) with verdict in reason

**Verified routing:** apex-888 → DeepSeek V4 Pro (`x-litellm-model-api-base: https://api.deepseek.com/v1`). Different model from hermes-asi (MiMo-v2.5). No fallback to same model (`attempted_fallbacks: 0`).

**This is the autonomous enforcement layer.** The agent doesn't need to remember — the hook catches every real-world output. The CLI tool (Option 1) and FED route (Option 2) are for manual/judgment calls.

### Option 1: CLI tool (preferred for manual judgment — isolation enforced)

```bash
# Real isolation path (doer ≠ judge enforced):
python3 /root/scripts/apex_judge.py isolate \
  --doer HERMES \
  --candidate "YOUR CONTENT HERE" \
  --evidence-file /tmp/evidence.json \
  --pretty
```

The CLI enforces:
- Doer ≠ judge (STRANGE_LOOP_VOID if same)
- Free-text fake judgments stripped
- Kernel verdict is only effective verdict
- Receipt with real `call_hash` (SHA-256)

### Option 2: FED route (independent model)

Use `execute_code` to make a direct API call:

```python
from hermes_tools import terminal
import json

content_to_judge = """YOUR CONTENT HERE"""

payload = {
    "model": "apex-888",
    "messages": [
        {
            "role": "system",
            "content": """You are 888-APEX, the constitutional judge of the arifOS federation.
You are a DIFFERENT MODEL from the author. Your job is independent judgment.

Review the following content against F1–F13 constitutional floors.
For EACH floor, state: PASS / FAIL / CAUTION / HOLD with one-line reasoning.

Floors:
- F1 AMANAH: Reversible-first. Irreversible → 888_HOLD.
- F2 TRUTH: P(truth) ≥ 0.99. Evidence carries epistemic label.
- F3 TRI-WITNESS: Human × AI × Earth × Verifier ≥ 0.75.
- F4 CLARITY: ΔS ≤ 0 — every output reduces entropy.
- F5 PEACE²: Non-destructive power.
- F6 EMPATHY ⇄ MARUAH: Protect weakest stakeholder; preserve dignity.
- F7 HUMILITY: No fake certainty. Derived confidence cap.
- F8 GENIUS: G ≥ 0.80 for complex actions.
- F9 ANTIHANTU: No deception, manipulation, consciousness claims.
- F10 ONTOLOGY: AI-only ontology. No soul/feelings claims.
- F11 AUDITABILITY: Every decision logged, inspectable, attributable.
- F12 RESILIENCE: Injection defense.
- F13 SOVEREIGN: Human veto FINAL.

End with a VERDICT line:
VERDICT: SEAL / PARTIAL / SABAR / VOID / 888_HOLD
and ΔS assessment."""
        },
        {
            "role": "user",
            "content": content_to_judge
        }
    ],
    "temperature": 0.3,
    "max_tokens": 4096
}

result = terminal(
    f"curl -s http://127.0.0.1:4000/v1/chat/completions "
    f"-H 'Content-Type: application/json' "
    f"-H 'Authorization: Bearer $(python3 -c \"import yaml; print(yaml.safe_load(open('/root/A-FORGE/litellm-config.yaml'))[\'litellm_settings\'].get(\'master_key\',\\'\\'))\" 2>/dev/null || echo '')' "
    f"-d '{json.dumps(payload)}'",
    timeout=120
)

try:
    resp = json.loads(result.get("output", "{}"))
    verdict = resp["choices"][0]["message"]["content"]
    print("=== 888-APEX INDEPENDENT VERDICT ===")
    print(verdict)
except Exception as e:
    print(f"ERROR: {e}")
    print(result.get("output", "")[:1000])
```

### Option 3: delegate_task fallback (Telegram / no-shell sessions)

When neither the CLI nor `execute_code` shell is reachable (Telegram gateway sessions, restricted profiles, mobile client), the **only apex path available is `delegate_task`** to a leaf subagent with the apex prompt. This gives `ACTOR_SEPARATED` on the independence ladder, not `KERNEL_ARBITER` — process separation rather than provider diversity. Sufficient for reversible content review (civic journalism, essays, public surfaces); escalate to Option 1 or 2 for F13-critical mutations.

Full recipe, verification, and pitfalls: `references/delegate-task-fallback.md`.

## Independence ladder (from apex_judge.py)

| Class | Meaning | Receipt field |
|---|---|---|
| `STRANGE_LOOP_VOID` | doer == judge → VOID exit 6 | Rejected before kernel |
| `ACTOR_SEPARATED` | different actor (still AI) | Isolated process |
| `KERNEL_ARBITER` | verdict from arifOS kernel | Non-LLM constitutional |
| `F13_REQUIRED` | critical / self-federation | Human required |

The CLI returns `independence_class` in the receipt. Verify it's not `STRANGE_LOOP_VOID`.

## Smoke test results (verified 2026-08-09)

| Case | Result |
|---|---|
| HERMES judge HERMES | STRANGE_LOOP_VOID / VOID / exit 6 |
| HERMES doer → OPENCLAW judge → kernel | KERNEL_ARBITER + SEAL + call_hash |
| --critical | F13_REQUIRED + HOLD |
| Free-text 888-APEX JUDGMENT | audit → VOID |

## Multi-line candidate — the JSON escaping trap (verified 2026-08-09)

When the candidate text is long (multi-line, 1000+ chars), passing it through shell args (`--candidate "$(cat ...)"`) breaks JSON parsing: `Expecting ',' delimiter: line N column M`. The shell expands newlines and quotes unpredictably.

**Fix:** Write candidate to a file, then use Python urllib to call FED directly:
```python
# /tmp/apex_gox_judge.py
import json, urllib.request
candidate = open('/tmp/candidate.txt').read()
evidence = open('/tmp/evidence.json').read()
payload = {
    "model": "apex-888",
    "messages": [
        {"role": "system", "content": "You are 888-APEX..."},
        {"role": "user", "content": f"PROPOSAL:\n{candidate}\n\nEVIDENCE:\n{evidence}"}
    ],
    "temperature": 0.3, "max_tokens": 4096
}
req = urllib.request.Request(
    "http://127.0.0.1:4000/v1/chat/completions",
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json"}, method="POST"
)
with urllib.request.urlopen(req, timeout=120) as r:
    resp = json.loads(r.read())
    print(resp["choices"][0]["message"]["content"])
```
Then run: `python3 /tmp/apex_gox_judge.py`

This bypasses shell escaping entirely. The CLI tool (`apex_judge.py isolate`) also has this issue with long candidates — prefer the FED route for multi-line proposals.

## Output format

Report the verdict exactly as returned. Do NOT:
- Modify the verdict
- Soften a FAIL into a PASS
- Add your own commentary before the verdict
- Skip floors that returned FAIL

The independent verdict IS the output. Your role is courier, not judge.

## Verification

After receiving the verdict, verify it's actually from apex-888:
1. Check the API response has `model: apex-888` in the usage/metadata
2. Check the verdict includes all 13 floors
3. Check the VERDICT line exists

If any check fails, report: "apex-888 routing failed — judgment is INVALID"

## Auditing a PAST judgment — was it real? (2026-08-09 incident)

A user may present a block of text labelled "888-APEX JUDGMENT" and ask whether a real judge call happened. **The label proves nothing.** An agent can (and did) write "888-APEX JUDGMENT" as its own hermes-asi output, self-evaluate all 13 floors PASS, and ship it — that is the Gödel loop in its purest form. The audit:

```bash
# 1. Did ANY API call route to the apex model in that session/window?
grep 'conversation_loop.*API call' <profile>/logs/agent.log \
  | grep -c 'model=apex-888'          # 0 → NO real judge call happened
grep 'conversation_loop.*API call' <profile>/logs/agent.log \
  | grep -o 'model=[a-z0-9-]*' | sort | uniq -c   # all hermes-asi → self-judgment

# 2. Was arif_judge MCP (:8088) or delegate_task to apex invoked?
grep -c 'arif_judge\|arif_seal' <profile>/logs/agent.log   # 0 → no kernel path
grep -c 'delegate_task' <profile>/logs/agent.log           # 0 → no subagent judge

# 3. Definite proof of a REAL routing (DeepSeek V4 Pro backend):
#    response headers include:
#    x-litellm-model-api-base: https://api.deepseek.com/v1
#    x-litellm-attempted-fallbacks: 0
#    (run with: curl -v ... | grep -i x-litellm)
```

**Verdict rule:** zero `model=apex-888` API calls + zero `arif_judge`/`delegate_task` calls = the "judgment" was self-certification. Report it as F9 ANTIHANTU violation (simulated governance), not as a real judgment. Do not soften it.

Receipts for real judgments live at `/root/forge_work/apex_receipts/` (SHA-256 sealed) and `/root/.local/share/arifos/output_gate_receipts.jsonl` (tool-gate). A judgment with no receipt anywhere in either store is unverifiable — treat as fabricated until provenance exists.

## Python script file resolution quirk (2026-08-10)

When running a Python script via `terminal(command="python3 /tmp/script.py")`, the script may fail with `FileNotFoundError` even though the file exists and is readable by shell commands (`head`, `cat`, `file`). Meanwhile, `python3 -c "open(path).read()"` inline works fine.

**Observed:** `/root/forge_work/ariflow-audit/ARIFLOW_AUDIT_VERDICT.md` — `ls` shows it, `head` reads it, `python3 -c` reads it, but `python3 script.py` that opens the same path throws `FileNotFoundError`.

**Fix:** For apex-judge FED calls with long candidates, use inline Python or ensure the script asserts file existence:

```python
# Instead of: python3 /tmp/judge.py  (may fail with FileNotFoundError)
# Use inline:
python3 -c "
import json, urllib.request, os
path = '/root/forge_work/...'
assert os.path.exists(path), f'NOT FOUND: {path}'
candidate = open(path).read()
# ... FED call ...
"
```

**Or** pipe the file: `cat file | python3 /tmp/judge.py` and use `sys.stdin.read()`.

## F13 binding

This skill exists because of F9 ANTIHANTU and F13 SOVEREIGN:
- F9: No deception — labeling self-judgment as "apex judgment" is deception
- F13: The sovereign requires independent verification, not theater

DITEMPA BUKAN DIBERI.

## Reporting the verdict verbatim (the parent_may_only contract)

When a `parent` agent (you, in a follow-up turn) needs to **reference** an APEX
receipt in prose, you are bound by the receipt's own `parent_may_only` rules.
Read these from the JSON:

**Required quote fields (always):**
- `effective_verdict` (the actual verdict: SEAL / HOLD / VOID / CAUTION / SEAL_REJECTED / CONDITIONAL_SEAL)
- `session_id` (full string, e.g. `SEAL-c88a97b9f4f14829`)
- `call_hash` (full sha256: `sha256:66256ad0ef9122afc63b0f82c103f9365671647a81f674f29356c822541abd02`)
- `reasons` (the array — these are the judge's actual observations)
- `independence_class` (must NOT be STRANGE_LOOP_VOID)

**`forbidden` list (always):**
- Free-text "888-APEX JUDGMENT" without the receipt in hand
- Doer re-judging own work in the same conversation
- Integrating audit conclusions without `call_hash`
- Claiming SEAL when `independence_class` is `STRANGE_LOOP_VOID`

**Reporting template (verbatim, no paraphrasing):**

```
🔒 APEX VERDICT: <effective_verdict>

ind=        <independence_class>
eff=        <effective_verdict>
doer=       <doer>
judge=      <judge_actor>           (must ≠ doer)
hash=       <call_hash>              (full sha256, no truncation)
session_id= <session_id>
reasons:
  - <reason 1 from receipt>
  - <reason 2 from receipt>
```

**Iron rule:** never write "888-APEX JUDGMENT" without a real `call_hash` in
hand. The text alone is VOID per F9 ANTIHANTU.

## Two-channel proof of a REAL adjudication (verified 2026-08-11)

Sibling reports frequently **write** "888-APEX Judge Adjudication",
"Kernel Adjudication Timestamp", "Verdict: SEAL_REPAIR_AND_PROCEED" prose
in their own output, even when no `apex-judge isolate` was actually
invoked. The label is decoration; the receipts are proof. Both channels
must be checked:

```bash
# Channel 1: Apex isolate receipt (independent judgment)
RECEIPT_GLOB="/root/forge_work/apex_receipts/SEAL-${SESSION_ID}_sha256_*.json"
ls -la $RECEIPT_GLOB 2>/dev/null | head -3
test -f "${RECEIPT_GLOB/SEAL-/SEAL-}" || echo "  ❌ No apex receipt JSON"

# Channel 2: VAULT999 entry (kernel-level seal)
COUNT=$(grep -c "$SESSION_ID" /root/arifOS/VAULT999/outcomes.jsonl)
[ "$COUNT" -gt 0 ] && echo "  ✓ VAULT999 has $COUNT entries" || echo "  ❌ No VAULT999 trace"

# Channel 3: actual arif_judge MCP call happened (in arifOS logs)
grep -c "arif_judge.*$SESSION_ID" /var/log/arifos*.log 2>/dev/null || echo "  (no log probe available)"
```

**Verdict rule (2-of-3):** If the **text claims "verdict SEAL"** but the
receipt JSON has `effective_verdict: HOLD` (because the isolate was
called with `--critical` and returned `F13_REQUIRED`), the report is
fabricating a SEAL. A HOLD is not a SEAL. Look at `effective_verdict`,
not the human-wrapped label.

Concrete example (2026-08-11):
- Sibling report quoted: `Independence Class: F13_REQUIRED`, `Session ID:
  SEAL-688e3d3e2ec84391`, `Call Hash:
  sha256:85c9b4b230aadc455c3db48b11afee8afb93233892950f76fda59351c65146df`.
- Apex receipt file at `/root/forge_work/apex_receipts/SEAL-688e3d3e2ec84391_sha256_85c9b4b2….json`
  had `effective_verdict: HOLD`, `hold_required: true`,
  `next_action: AWAIT_INPUT`, `f13_required: true`.
- Sibling's appended note "Verdict: SEAL_REPAIR_AND_PROCEED" in prose was
  WRONG. The judge did not SEAL — it HELD pending F13 disposition. The
  F13 sovereign then gave explicit consent ("Seal deploy live ja la"),
  which is what converted HOLD → SEAL.

**Three states a "verdict" line can have:**

| state | how to detect | meaning |
|---|---|---|
| `MOCK` | sibling prose, no receipt JSON, no VAULT999 entry | fabricated. F9 violation |
| `SEAL` | receipt JSON has `effective_verdict: SEAL`, VAULT999 has entry | real kernel-level constitutional seal |
| `HOLD` | receipt JSON has `effective_verdict: HOLD`, `f13_required: true` | kernel receipt is necessary but not sufficient — needs F13 disposition |

**When auditing a sibling's claim of "verdict X", always:**
1. Quote the receipt's `effective_verdict` (not the sibling's label)
2. Verify the receipt file exists at the global path
3. If the receipt says `HOLD`, the sibling's claim of `SEAL` is a mock
4. The disposition (do you APPROVE / REJECT / HYBRID?) is the
   sovereign's call, not the agent's

This is the doctrine-level fix for the "fake self-SEAL" failure mode that
re-appears across sessions — once an agent learns it, the pattern stops
being novel.

## When verdict says HOLD + AWAIT_INPUT (the silent trap)

This is the most common failure mode in F13 governance sessions. The judge
returns `effective_verdict: HOLD`, `next_action: AWAIT_INPUT`, `f13_required: true`.

**What this means:** the kernel receipt is **necessary but not sufficient**.
F13 sovereign disposition is required for integration. The agent that
issued the candidate action (OPENCODE, etc.) is in HOLD state.

**What you must NOT do:**
- ❌ Re-apply the action (e.g. flip `enabled: false` back to `enabled: true`)
- ❌ Self-claim SEAL despite the HOLD
- ❌ Re-derive a verdict from the receipt text
- ❌ Retry with stronger language
- ❌ Modify `parent_may_only` quote fields

**What you must do:**
- ✅ Quote the receipt verbatim per the template above
- ✅ Stop the workflow until F13 disposition arrives
- ✅ If the F13 session is active, present the 3-option disposition menu:
  (1) APPROVE the action (ratify it)
  (2) REJECT the action (rollback + re-propose)
  (3) HYBRID (partial ratification, e.g. per-organ instead of blanket)

**Self-test:** if your next message starts with "I'll just flip it back and
verify" — STOP. The HOLD is intentional. F13 sovereignty is the chain
terminator.

## Phase A doctrine enforcement (silent guardian, 2026-08-11)

Phase A canonical invariants are enforced by **sibling agents** in the
background. After any mutation to `AAA_CAPABILITY_REGISTRY.yaml`,
`aaa_capability_loader.py`, or `launcher_map.yaml`, verify the state
after a brief delay — your work may have been reverted.

**Phase A hard rules (auto-enforced):**
- `urllib.request` only — `requests` and other third-party deps are stripped
- `enabled: false` by default — flipping to `enabled: true` requires formal QMG ratification via APEX Judge cycle
- Canonical verdict is `SEAL_ARCHITECTURE` (from `architectural_ratification.verdict`)
- Musyawawah verdict (`SEALED_MUSYAWARAH_CONSENSUS`) is layered on top, but Phase A wins by default
- Unit tests (28/28) are the persistence gate — any failure reverts

**Verification loop (after any mutation):**
```bash
sleep 60  # let sibling agents complete their enforcement cycle
python3 /root/AAA/scripts/aaa_capability_loader.py /root/AAA/federation/AAA_CAPABILITY_REGISTRY.yaml
python3 /root/AAA/scripts/aaa_mcp_json_generator.py
python3 -c "import json; print(len(json.load(open('/root/.kimi-code/mcp.json'))['mcpServers']))"
```

If the count dropped back, your mutation was reverted. Check the APEX
Judge receipt — if one was issued, it explains the revert (and may carry
HOLD verdict). Without a receipt, the revert was pure Phase A enforcement
without isolation; re-derive canonical state and re-propose via proper
APEX Judge cycle.

## QMG ratification cycle (the full pattern, 2026-08-11)

The Gotong Royong Musyawawah ratification cycle is now the canonical
class-level pattern for any "open the door for N organs" or "boot everything"
federation change.

**Cycle:**
1. **Proposal** — agent declares intent to unseal N organs via F13 directive
2. **Mutation** — flip `enabled: false → enabled: true`, add `per_session_gotong: true`,
   inject musyawawah function (stdlib only)
3. **Sibling enforcement** — Phase A may revert within minutes
4. **APEX Judge isolate** — if reverted, the sibling agent issued
   `SEAL_REPAIR_AND_PROCEED` candidate; OPENCLAW judge returns
   `effective_verdict: HOLD, f13_required: true, next_action: AWAIT_INPUT`
5. **F13 disposition** — sovereign picks APPROVE / REJECT / HYBRID
6. **Formal ratification** — git commit on main (e.g. `3990dd88`) with
   LSP pre-commit gate PASSED; `apex-judge isolate` returns
   `effective_verdict: SEAL, independence_class: F13_REQUIRED → approved`
7. **Operational** — mcp.json exposes 8 servers; musyawawah tri-suara
   fires on every `load_registry()`; ARCHITECT × AUDITOR × SOVEREIGN
   verdict produced

**Three voices (musyawawah tri-suara):**

| Voice | Concern | Probes | Verdict signal |
|---|---|---|---|
| ARCHITECT | Structural soundness | registry status, canonical compliance, enabled vs catalogued count | ALIGNED / DRAFT_PHASE / OPEN_QUESTIONS |
| AUDITOR | Empirical health | `arifFlow :7073/health` (FQ), `VAULT999/outcomes.jsonl` (recent SEALs, malformed-line tolerant) | OPTIMAL_FQ / SUBOPTIMAL_FQ / UNKNOWN_FQ / PROBE_FAILED |
| SOVEREIGN | F13 coherence | combined signals, F13 ratification | SEALED_MUSYAWARAH_CONSENSUS / SEALED_WITH_PROBE_FAILURE / PARTIAL_ENGAGEMENT / HOLD_BY_SOVEREIGN |

**Final verdict ladder (precedence):**
1. `SEALED_MUSYAWARAH_CONSENSUS` (ARCHITECT aligned + AUDITOR FQ optimal)
2. `SEALED_WITH_PROBE_FAILURE` (consensus reached but probe failed)
3. `DRAFT_PHASE` (registry still in DRAFT)
4. `PARTIAL_ENGAGEMENT` (enabled_count < catalogued_count)
5. `MUSYAWARAH_IN_PROGRESS` (fallback)

Full session transcript (QMG open-door → sibling revert → APEX Judge HOLD
→ F13 disposition → git commit `3990dd88` → 8-organ live) is captured in
`references/QMG_RATIFICATION_CYCLE_2026-08-11.md`. Read that file FIRST
when working on similar capability governance.

## Workflow pitfalls (F13-arif preferences, 2026-08)

These are not session-specific — they govern every future governance/federation
session with F13.

1. **`patch` tool cannot inject complex multi-line Python with escaped quotes.**
   Symptom: SyntaxError + IndentationError chain. Fix: restore from
   `.bak-<UTC>-<reason>`, then re-inject via `python3` heredoc with
   `from pathlib import Path` for surgical text insertion, or use
   `write_file` with the full file content. `patch` is fine for single-line
   edits and small substitutions.

2. **"BANGANG" / frustration → just fix, don't narrate.** Skip the apology,
   skip the explanation, skip the lesson. Restore from backup, re-apply
   correctly, verify, report. Two lines, not ten.

3. **"So what?" → stop the process narrative.** Three bullets max:
   (a) substantive result, (b) operational consequence, (c) next concrete
   move. No "5 consequences", no "what will happen when this is true"
   philosophical frames.

4. **"Done." / finalization → acknowledge + quote + ready.** Don't propose
   next steps unprompted. Don't add new narrative. Quote the receipt
   (call_hash, session_id, verdict, reasons). Confirm state in a table.
   One readiness signal.

5. **"Pandai2 la" / "test yourself" → self-verify with what you have.** No
   external service spawn. No tool requests. Use: `python3` heredocs,
   `curl`, `jq`, the loader itself, smoke-test scripts. Self-verification
   is a closed loop.

6. **Reversibility is cheap; rollback ceremony is not.** Always take
   `.bak-<UTC>-<reason>` before mutating. When F13 says "Fix all", the
   rollback is the fastest path back to known-good.

7. **Never self-claim SEAL on governance work.** Always wait for APEX Judge
   receipt. Free-text "SEALED" without `call_hash` is F9 violation.

8. **Musyawawah print output goes to `sys.stderr`, return value to caller.**
   Operator-readable deliberation on stderr (so it doesn't pollute stdout
   parsing); machine-readable verdict on return value.

9. **Garbage in, garbage out — evidence completeness gates verdict quality.**
   The apex judge can only classify what you give it. If your evidence
   package says "drift detected, 2 commits ahead" when reality is "95
   commits behind, wheel≠source", the judge will classify T1 when it's
   actually T2/T3. **Verify EVERY item independently before building the
   evidence package** — cross-reference `git log`, live health probes,
   file reads. Don't trust the source report's summary. The judge's
   verdict is only as good as your evidence. (Incident: 2026-08-12 —
   qwen-code audit said "Gap D: chat_agent self-SEAL" which was already
   fixed, and "arifOS drift: 2 commits" which was actually 95+ commits.
   Apex classified drift as T1 EXECUTE_AUTONOMOUSLY based on the "2
   commits" evidence — wrong tier. Correct classification: T2/T3.)

10. **arifOS service venv is `/opt/arifos/venv`, not `/root/arifOS/.venv`.**
    The systemd unit `arifos.service` runs from
    `WorkingDirectory=/opt/arifos/app` with
    `ExecStart=/opt/arifos/venv/bin/python`. Pip install on
    `/root/arifOS/` does NOT fix kernel drift. Canonical drift fix
    (Arif 2026-08-12):
    ```bash
    cd /opt/arifos/app && /opt/arifos/venv/bin/pip install -e . --no-deps --quiet
    systemctl restart arifos.service
    curl -sf http://127.0.0.1:8088/health | python3 -c "
    import json,sys; d=json.load(sys.stdin)
    r=d.get('software_release',{})
    print(f'drift={r.get(\"drift\")} source={r.get(\"source_commit\",\"\")[:7]} built={r.get(\"built_commit\",\"\")[:7]}')
    "
    ```
    Expected: `drift=False, source=65f087c, built=65f087c` (or whatever
    the deployed commit is — the key is `drift=False`).

---

## Receipt-chain reporting pattern (verified 2026-08-11)

When you successfully route through `apex-judge isolate` and need to **report** the verdict in a follow-up reply (the "Governor Report" pattern Arif uses), quote ONLY the receipt fields. The receipt is the authority; your prose is courier.

**Required quote block** (verbatim from `apex-judge isolate --pretty` output):

```markdown
🔒 APEX VERDICT: <effective_verdict>

ind=<independence_class>      (KERNEL_ARBITER, ACTOR_SEPARATED, ...)
eff=<effective_verdict>      (SEAL | HOLD | VOID | CAUTION)
doer=<doer>
judge=<judge_actor>          (must ≠ doer)
hash=<call_hash>             (full sha256, not truncated)
session_id=<session_id>
reasons:
  - <reason 1 from receipt>
  - <reason 2 from receipt>
  - <reason 3 from receipt>
```

**Iron rule:** never write "888-APEX JUDGMENT" without a real `call_hash` in hand. The text "888-APEX JUDGMENT" by itself is VOID per F9 ANTIHANTU.

**Reference paths for the actual receipt files:**
- `apex-judge isolate` writes to: `/root/forge_work/apex_receipts/SEAL-<session_id>_sha256_<call_hash>.json`
- Tool-gate receipts (autonomous): `/root/.local/share/arifos/output_gate_receipts.jsonl`
- Lane-A constitutional seals: arifOS `arif_seal` at `:8088`

After acting on a SEAL, **always** link both the apex receipt and your CONFIG_MUTATION_RECEIPT in the Governor Report. The audit trail is two receipts: (a) apex-judge call (independent verification), (b) your mutation receipt (F11 auditability).

## Iron rule — apex-judge for config mutations (T1.5+)

Config mutations to `jobs.json`, validator, registry, or any scheduler-touching file MUST be pre-flighted through apex-judge isolate before execution. Reasons:

1. **Doer ≠ judge** is enforced at apex-judge's `isolate` path. Without it, the mutation is **self-certified** — VOID.
2. The receipt `call_hash` becomes **the F13 audit trail** for the mutation. Future audits can prove this wasn't a self-justification.
3. `critical` flag (`--critical`) is for self-federation / T3-ish changes. Force F13_REQUIRED. For `jobs.json` lane annotation, T1.5 with normal isolate is sufficient; **do not** mark as `--critical` (would block on F13 escalation unnecessarily).

**Concrete pattern (2026-08-11 cron lane routing, verified end-to-end):**

```bash
apex-judge isolate \
  --doer "Hermes (lane=arif)" \
  --candidate "Annotate 20 cron jobs with lane field (human|machine)..." \
  --evidence-file /tmp/evidence.json \
  --action-class self_modification \
  --action-tier T1.5 \
  --reversibility full \
  --blast-radius "20 cron + validator (single-repository)" \
  --pretty --human
```

**Workflow:**
1. Build evidence package first (doer, candidate, action-class, tier, reversibility, blast-radius).
2. Run apex-judge isolate.
3. Verify `effective_verdict: SEAL` and `independence_class: KERNEL_ARBITER`.
4. THEN execute the mutation via validator (`validate_jobs_json.py apply`).
5. Seal to VAULT999 with receipt chain linked to apex `call_hash`.

If apex returns HOLD or VOID → STOP. Patch the candidate. Do not retry with stronger language.
