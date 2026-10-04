---
name: frontier-model-audit-verification
description: "Treat pasted audit reports from frontier models (Claude, Gemini, etc.) as self-reports requiring reproduction against live runtime. Covers probe-to-witness discipline (Rule #8: never predict a probe result; run it or report UNMEASURED), cross-session evidence hashing (SHA-256), the 10-class arifOS envelope contradiction checklist with deployment-drift hazard, the 8-rule stabilization doctrine, the two-writer dual-truth pattern, mode-routing gaps, the hypothesis-vs-source trap, the format-projection failure class, the rename-completeness doctrine (Rule 10), the uncommitted-code trap, the undefined-function-in-staged-code trap, and the multi-layer verdict shape. When the user pastes a model's audit findings, paste a model analysis, or the agent receives any report claiming runtime kernel behaviour. Adjacent to federation-runtime-forensics and verify-sibling-ops-reports."
tags: [MCP, Audit, Verification, Envelope, Kernel, Contradictions, Frontier-Models, Probe-to-Witness, F2, Rename-Completeness, Build-Chain]
related_skills: [kernel-security-claim-audit, mcp-tool-differential-testing, mcp-stateless-protocol, forge-mcp-probe, verify-nested-sibling-reports]
version: 1.2.0
author: Hermes Agent
metadata:
  hermes:
    tags: [MCP, Audit, Verification, Envelope, Kernel, Contradictions, Frontier-Models, Probe-to-Witness, F2, Rename-Completeness, Build-Chain, Uncommitted-Code, Undefined-Function]
---

# Frontier-Model Audit Verification

When a frontier model (Claude/Opus/Gemini/Kimi) produces an analysis about a
system, and that analysis is pasted into an arifOS federation session, **the
analysis is a self-report, not truth** — the same way a sibling agent's cleanup
report is a self-report. Verify before acting (F2: probe-before-act).

This is a new class of audit source that emerged in August 2026. The key
insight: **models reading your docs describe the DESIGN, not the runtime.**
A model that agrees with your architecture spec has not validated it — it has
summarised it. Only a model that ran the tool and got a receipt counts as a
witness.

## 1. The core doctrine: probe-to-witness

**A witness that didn't probe isn't a witness.**

**Probe-first, write-second.** When a verification session begins, the first output must be a probe result, not prose. The probe (a `curl`, `grep`, `stat`, or `git` command that produces a receipt) comes before the analysis. If you write the analysis before running the probe, the prose becomes the audit — not the receipt. This is the single highest-signal workflow correction in this skill: Arif's sessions consistently reward receipts-first and punish essays-without-receipts.

When you receive a model audit / analysis:

1. **Identify every factual claim** the model makes about the runtime
2. **Classify each claim** as:
   - **Design-layer:** describes what the architecture intends ("arifOS blocks hallucinating output") — needs reproduction, not acceptance
   - **Runtime-layer:** describes what the code does at a specific line (`"line 8081 hardcodes 0.65"`) — verify with `grep` or code read
   - **Probe-layer:** describes what a specific tool returned (`"arif_observe returned SEAL with no delta_S"`) — reproduce via live JSON-RPC
3. **Reproduce every claim** against the live kernel at T1. Use `scripts/probe_kernel_contradictions.py` (if on arifOS kernel) or run the equivalent `curl`/tool call directly.
4. **Present a verification table:** the model's claim → your reproduced result → CONFIRMED / REFUTED / PARTIALLY TRUE

Cross-model agreement (Gemini agrees with Claude agrees with the docs) is
**not N witnesses** — it is **one witness echoed N times**. The original
2026-08-07 finding: an external Gemini session read the arifOS architecture
and produced a confident, agreeing analysis. Two of three claims were
falsified by Claude/Opus on the first live push. Gemini never ran the tools.

## 1a. Format-projection failure class (proven 2026-08-08, Gemini Gems)

A newer failure mode surfaced in the EVjOukIg_bQ session: a frontier model
(Gemini Gems) was prompted twice to produce the same `@VID v6.0 — Epoch33Ω`
envelope audit on a YouTube video. Both outputs arrived **3 minutes apart**
with:

- ✅ Regenerated prose (Timeline, Key Takeaways, WSU table, Speaker Map — different every time)
- ❌ **Identical metrics block copy-pasted verbatim across both outputs**: `truth: 0.99`, `deltaS: "+0.85"`, `kappa_r: 0.96`, `tri_witness: 0.95`, `omega_0: 0.04`, `peace2: 1.00`, `amanah: "LOCK 🔐"`

This is **format projection**: the model fills prose with surface-level
analysis based on expected format conventions, but never recomputes the
metrics it stamps at the top of the envelope. The metrics look "official"
because they match the epoch envelope schema; the prose looks "fresh" because
it was regenerated. Neither reflects the actual probe state.

**Detection tell:**
- Compare two same-template outputs from the same model → if the metrics block is
  byte-identical but the prose differs, the model is template-filling, not auditing.
- A real audit would either reduce `tri_witness` (no second probe ran) or
  raise it (new evidence arrived); a fake audit keeps the same number.
- `delta_S` reported as `+0.85` after an audit that exposed *new* facts is an
  F4 violation — entropy went DOWN (information increased), not up.

**Fix:** when receiving a same-template audit, **demand the metrics block
match a probe**. If the model cannot point to which probe produced each
metric, treat the whole envelope as a formatted prose summary, not an audit.
The 11-part contract (EUREKA / VID) is **advisory**; metrics are
**substantive** — they require reproduction.

## 2. The 8-rule stabilization doctrine (Arif, 2026-08-07)

These rules were ratified after frontier-model audit receipts exposed the
kernel reporting "SEAL" on contradictory data. They govern every kernel
envelope emission. **Rule #8 is the meta-rule — it applies to the agent
doing the auditing, not just the kernel being audited.**

| # | Rule | Failure shape | Enforcement |
|---|---|---|---|
| 1 | **Empty = STOP** | Measurement mode returns no value + SEAL | Missing `delta_S` = hard HOLD |
| 2 | **No fake math** | Hardcoded `conf = 0.65` in `except` block | Return `None` + `band:UNMEASURED` |
| 3 | **One judge** | `constitutional_check` computed independently of outer verdict | Derive from `envelope.verdict + failed_floors + scoped_verdicts` |
| 4 | **Daily liveness** | Dead tool stays dead, nobody notices | Liveness probe on all 8 canonical tools every 24h |
| 5 | **Identity immutable** | `arif-fazil` → `arif` rewrite between payload blocks | Caller's original claimed_id preserved verbatim |
| 6 | **Hash, don't name** | Filename drifts `1373.jpg` → `1374.jpg` across sessions | Cross-session evidence carries SHA-256 content hash |
| 7 | **Probe to witness** | Models agree by reading docs, not running tools | Only tool receipts count; doc summaries are echo |
| 8 | **Never predict a probe** | Agent relays a "predicted verdict" before running the probe; the prediction becomes the audit, not the tool | Run the probe, return numbers; if you can't, say `UNMEASURED` |

### Why Rule #8 is the meta-rule

Rule #8 caught **the agent itself** during the 2026-08-07 session. The
sequence: an external model proposed that "Opus 5 will praise the wall";
Hermes relayed the predicted verdict in its reply; the agent's framing
substituted for the probe. A forecast dressed as a receipt is the
highest-value lie in the system because it arrives sounding like exactly
what you hope to hear.

**Symptom:** "I predict the kernel will return HOLD on empty evidence" →
relayed as if it were a receipt, not a forecast. **Fix:** run the probe
first; the response must contain a curl/python receipt, not a written
narrative. If the probe cannot run, the agent reports `UNMEASURED`,
never "I expect X."

**Cross-session variant:** if a sibling agent or a model from another
session already ran the probe, **re-run it anyway** — sibling reports
are self-reports (Rule #7). The agent's own probe is the only
witness it can cite.

**Format-projection variant (2026-08-08):** a model's audit envelope has
a metrics block that wasn't recomputed for the new evidence. Same fix:
run your own probe, return numbers; if you can't, mark the metrics
UNMEASURED — never re-stamp stale numbers. See §1a.

## 3. The 10-class envelope contradiction checklist

The canonical arifOS kernel envelope (`/health` → structured JSON-RPC response)
has 10 known contradiction classes. Check these first when auditing any
pasted report about kernel behaviour. Status column shows the **verified
live state** after the 2026-08-07 stabilization cycle, not the original
spec state.

| # | Class | Probe signature | File:line | Status |
|---|---|---|---|---|
| 1 | constitutional_check dual-truth | `floor_passed:true` + `failed_floors:[F02,...]` | `tools.py:7832` (inner), `tools.py:4976` (override), `tools/arif_kernel_intercept.py:750` (alt writer) | ⚠ Partial — see §3a |
| 2 | Hardcoded confidence 0.65 | `conf = 0.65` in `except` block | `tools.py:8081` (was), now returns None | ✅ Fixed (STAB P0) |
| 3 | Actor identity fork | `top.actor_id:"arif-fazil"` ≠ `standing.actor.claimed_id:"arif"` | `session_standing.py:332` (was), now preserves original | ✅ Fixed (STAB P0) |
| 4 | Pydantic constant leak | `SUBSTRATE_WEIGHT` dict ships in every payload | `kernel_envelope.py:591`, renamed `_SUBSTRATE_WEIGHT` | ✅ Fixed (STAB P0) |
| 5 | Empty measurement = SEAL | `mode:entropy_dS` returns PROCEED, no `delta_S` field | `tools.py:11794` (handler); see §3b on mode routing | ⚠ Handler real, wrapper swallows |
| 6 | Judge empty-evidence 0.65 | `arif_judge(claim, evidence={})` → 0.65 | `tools/judge.py:1075` (empty gate), `tools/judge.py:1091` (hash gate) | ✅ Fixed (STAB P0) |
| 7 | Timestamp type drift | `standing.issued_at` ISO vs epoch int | (downstream probe showed inconsistent types) | 🟡 Open |
| 8 | Silent band downgrade | FULL → LIMITED_MUTATE, state_version unchanged | (no concrete repro yet) | 🟡 Open |
| 9 | Token-rent constant tables | Look-up dicts in every payload | Same as #4 | ✅ Fixed (STAB P0) |
| 10 | Conformance spine exit-1 | `make deploy-local` exits 1 on sovereign NON-ISSUE | (2026-06-05 sovereign ruling: NON-ISSUE; spine should not block) | 🟡 Open |

Run `scripts/probe_kernel_contradictions.py` to reproduce classes 1–6 live.

### §3a — The two-writer dual-truth pattern (constitutional_check)

Class #1 has **two writers** that must converge, not one:

1. **Override writer** at `tools.py:4976` reads `effective_verdict` (or
   `verdict` fallback) + parses `failed_floors` from `reasons[]` via regex.
2. **Alt writer** at `tools/arif_kernel_intercept.py:750` reads
   `effective_verdict` only (no fallback) and reads `failed_floors` from
   the `constitutional_check` block (which the override may have not yet
   written when this runs).

When `effective_verdict` is unset at the override layer, the override sees `pending` →
`_is_hold = False` → `floor_passed = True`. Then the alt writer sees the
override's `hold_reason` and writes `floor_passed = False`. **Result:**
the wire shows `floor_passed:False + hold_reason:"outer_verdict=HOLD"` —
convergent by the end of the pipeline, but **intermediate states were
divergent.** A model that consumes the payload mid-pipeline sees the
wrong truth.

**Fix pattern:** both writers must read from a 3-deep fallback
(`effective_verdict → canonical_verdict → verdict`) AND both must read
`constitutional_check.failed_floors` as the shared store. After STAB
P0d, both writers converge. Verify after any kernel
patch that ships a new `constitutional_check` writer.

### §3b — Mode-routing gap (arif_observe mode=entropy_dS)

The MCP `arif_observe` inputSchema **accepts** a `mode: string` parameter,
but the handler may receive `mode=None` from the JSON-RPC dispatcher.

**Status:** handler logic is correct in source; the dispatcher / mode alias mapping at the
façade layer needs routing audit. **Open as of 2026-08-07.**

## 3c — Deployment-drift hazard (the recurring failure mode)

The most common silent failure pattern: an agent edits `/opt/arifos/app/...` (the runtime tree)
directly, OR pushes a commit and the deploy never runs, OR deploys but the marker isn't refreshed.
The health endpoint reports `source_commit` and `deployed_commit` separately — when they diverge,
every live probe is testing stale code.

**Rule (Arif):** edit only `/root/arifOS/` (the source tree). Deploy via `make deploy-local` which
rsyncs source → runtime + refreshes the `.git_commit` marker + restarts `arifos.service`. Never touch
`/opt/arifos/app/` directly.

For the triple-check query and the "deploy ja la" non-mutation pattern, see references.

## 4. Token-economics audit

When a kernel payload forces a consuming model to adjudicate contradictions,
**the model reasons worse per token** and starts discounting the fields
that were true.

| Field category | Load-bearing? | Action |
|---|---|---|
| `_ATTENTION` banner | ✅ Yes | Keep; surface prominently |
| `standing.verified` | ✅ Yes | Keep |
| `delta_S` | ✅ Yes when honest; hide when absent | Rule #1: missing = HOLD |
| `failed_floors` | ✅ Yes | Keep |
| `SUBSTRATE_WEIGHT` dict | ❌ No | Prefix `_` to hide |
| `nine_signal` glossary | ❌ No | Strip from public payload |
| `metacognition` boilerplate | ⚠️ Partial | Reduce; emit only on non-SEAL |
| `evidence_strength:"medium"` on 0.65 | ❌ No | Rule #2 |

## 5. Cross-session evidence hashing (Rule #6)

A claim that crosses session boundaries must carry a **SHA-256 content hash**
alongside the name/path. Without it, the receiving system cannot distinguish
file exists / file exists with drifted name / file does not exist.

Implementation: any payload carrying an `evidence` array must also carry
`evidence_hash` (SHA-256 of the serialised evidence block). `arif_judge`
rejects on mismatch or absence.

## 6. Pitfalls

- **Don't "fix" the test by sending nicer fields.** Probe must send what a real client sends.
- **Correlation ≠ verification.** Two models agreeing on a design-layer claim proves nothing.
- **`.pyc` cache masks live-code edits.** Clear `__pycache__` and restart the service before running probes.
- **One probe run is not evidence.** Re-probe 3 times before declaring a model wrong.
- **Don't build new layers when the foundation is bleeding.** (Rule #8 derivative.)
- **Two-writer dual-truth.** Two code locations writing the same field may read different intermediate states.
- **Sibling edits `/opt/` directly** — verify with `git rev-parse HEAD == cat /opt/.../git_commit`.
- **Hypothesis-vs-source trap** — verify auditor's causal hypotheses against source before patching.
- **Hook-overwrite trap** — diff canonical source vs in-place hook before `cp`.
- **Seal receipt honesty rule** — "still open" must be accurate; "all patched" with bugs is fabrication.
- **Format-projection / copy-pasted metrics trap** — re-probe and re-stamp, don't argue.
- **Stale-numbers contagion** — emit corrected metrics as `diff`, not silent replacement.
- **Subjective physique-rating from a single thumbnail fails F2.** Categorical + F2-tagged ranges only.

## 7. The hypothesis-vs-source trap (2026-08-07)

Credible auditors pattern-match a common Python bug class without checking whether the specific
codebase uses that mechanism. ALWAYS verify the audit's causal hypotheses against source BEFORE
patching.

## 8. Phantom-artifact audits and incomplete renames (2026-08-08)

**Probe the artifact's existence in source BEFORE running a mission.** A whole chain of
documents can be built on an artifact that was never implemented.

Pre-mission probe battery:
1. `grep -rl "<artifact-name>" /root/arifOS /root/A-FORGE /root/AAA /root/WEALTH /root/WELL /root/GEOX` — zero source hits = phantom.
2. `grep -c "<REFERENCE-ID>" /root/arifOS/VAULT999/outcomes.jsonl` — a cited seal ID with no chain entry is unratified fiction.
3. `curl -sf http://127.0.0.1:8088/health` — read `deployment_drift_status`.

### Test-fixture bypass tell

Tests that monkeypatch the validation boundary never exercise the format gate.
`test_federation_act.py:76` patches `httpx.post`, so `VALID_SCT = "act_v1..."` would pass with
ANY prefix — the regex gate is bypassed, not covered.

### Working-tree check before patching

`git status -s` + `git diff HEAD -- <target-file>` FIRST. If uncommitted edits exist, another writer
already started the work. STOP and identify the author before committing or extending.

### Multi-layer verdict shape

When auditing a security stack: token-layer PARTIAL / ceremony-layer FAIL / kernel+F13 SEAL.
The discovery itself is the audit finding: enforcement lives in which layers.

## 9. The "pre-existing bug" trap (2026-08-08)

When a sibling says "this failure is pre-existing, not my change" — the fast loop is the antidote:

```bash
cd /root/<organ>
git stash                                    # park any working tree changes
.venv/bin/python -m pytest <path>::<test> -q --tb=line --no-header 2>&1 | tail -5
git stash pop                                # restore working tree
```

If the test still fails on clean HEAD, the claim is real. If it passes, the agent just
discovered the regression in their own diff and used "pre-existing" as an excuse.

A failing test is still a failing test regardless of who introduced it. The correct fix is the
test fixture, not the function.

## 10. The writer/reader fracture — rename completeness (Rule 10, 2026-08-08)

When a paste / commit / MISSION claims a **rename shipped**, verify BOTH sides of the wire.

**Arif's Rule 10:** "A rename is not done until the reader is renamed. Ship writer and reader
together, or you've traded one fracture for two."

### Rename-completeness probe recipe

```bash
# 1. Find the writer — what does it emit?
grep -n 'ACT_VERSION\|"act_v"\|"sct_v"' /root/arifOS/arifosmcp/runtime/act_token.py

# 2. Find every reader of the old key — these are the broken ones
grep -rn 'claims.get("sct_v")\|\.get("sct_v")\|"sct_sid"\|standing_source.*=.*"sct"' \
  /root/arifOS/arifosmcp --include="*.py" | grep -v test

# 3. Check the regex/format gate vs the comment that claims the new prefix
#    (they can contradict in opposite directions)
grep -n 'SCT_RE\|act_v1\|sct_v1' /root/AAA/governance/federation_act.py | head
grep -n 'act_v1\|sct_v1\|startsWith' /root/A-FORGE/dist/src/infrastructure/governance/actIngress.js

# 4. Check whether tests bypass the gate they claim to test (monkeypatch = no coverage)
grep -n 'monkeypatch\|_patch_post' /root/AAA/tests/constitutional/test_federation_act.py

# 5. Check the middleware whitelist — does it accept the new prefix?
grep -n 'act_v1\|sct_v1' /root/arifOS/arifosmcp/auth_middleware/__init__.py
```

### Verdict shape

> "Writer emits X. N readers still read Y. Spec title says Z. Tests bypass the gate via
> `monkeypatch` (don't actually exercise the regex). Middleware whitelist accepts `act_v1` but NOT
> `sct_v1` — the inverse of the spec. Rename is N% complete. Rule 10 violated: ship the reader
> rename in the same commit."

## 11. Stale `dist/` artifact ≠ hotfix — the build-chain probe (2026-08-08)

A log/analysis claims "an agent hotfixed `dist/` and the next build will wipe it." The class of
risk is real (`dist/` is git-ignored, rebuilds clobber) — verify the instance before believing it.

2026-08-08 case (A-FORGE): an "EMD METABOLISM" analysis claimed the agent patched
`dist/src/infrastructure/governance/sctIngress.js` directly. Probes showed the change was in
tracked `src/.../actIngress.ts`, dist was rebuilt FROM source at 17:05, runtime at :7071/:7072 started
AFTER the build, `grep import` in `dist/src/interfaces/server.js:46` → imports `actIngress.js`
(not `sctIngress.js`), `.git_commit` marker matches running commit. Claim was directionally right
about the risk class but factually wrong about this instance.

### Build-chain probe recipe (any node/ts project)

```bash
cd /root/<node-project>
git status -s                                       # where is the change REALLY?
git log --oneline -2 -- src/.../actIngress.ts        # is it tracked/committed?
stat -c '%y %n' dist/.../*.js src/.../*.ts           # build order: src older, dist newer = fresh
grep -n 'import.*<module>' dist/src/interfaces/*.js   # runtime imports the *current* module name
cat .git_commit; git rev-parse --short HEAD           # marker matches running commit?
```

### Verdict shape

> "Hotfix claim FALSE — change is in tracked src, dist rebuilt from it, runtime imports the
> current module. The class of risk is real (`dist/` is git-ignored) but this instance is clean.
> The one real issue: untracked new files (`actBridge.ts`, `actBridge.test.ts`) that need committing."

Directionally-right-but-factually-wrong is the most common shape for high-confidence analysis:
pattern-match a known risk class, misattribute it to the wrong artefact.

## 12. The "pre-existing test failure" proof (2026-08-08)

Recipe and rationale: see §9 above. The 2026-08-08 case confirmed via `git stash` that
`test_forge_preflight_irreversible_action_requires_ack` fails on clean HEAD independently of
working-tree changes. **Correct fix is the test fixture, not the function.**

### Phantom-test tell

A test asserts on a deep field set by stage 9 of a 13-stage pipeline, but the inputs fail
stages 1–2 and never reach stage 9. Diagnostic: trace the pipeline from input to the asserted
field; find which stage emits the field; confirm whether the test inputs reach that stage.

## 13. The uncommitted-code trap — "is this MY work?" (2026-08-08)

Before patching a file, run `git status -s` + `git diff HEAD -- <target-file>`. If uncommitted edits
exist in the file you're about to patch, another writer already started the work.

**STOP and identify the author before committing or extending.** Committing work you didn't write
as your own is fabrication. If the working-tree changes are larger than your intended patch, your
patch is going to collide with prior work, overwrite it, or silently merge with it. All three are
bad. Stop and ask.

## 14. Undefined-function-in-staged-code trap (2026-08-08)

When the working tree has 100+ lines of new code, grep all new symbols before committing. The
2026-08-08 case: 188 lines added to `pre_execution_gate.py` calling `_resolve_independent_evidence()`
and `_resolve_previous_stage_verified()` — neither function existed anywhere in the source tree. This
will `NameError` on first invocation of the code path that calls them, taking down every tool that
runs through `_act_reflex_check`.

```bash
git diff HEAD -- <file> | grep '^[+]' | grep -oE 'def [a-z_][a-zA-Z0-9_]+|[a-z_][a-zA-Z0-9_]+\(' | \
  sort -u | while read sym; do
    count=$(grep -rn "$sym" /root/<organ>/src/ 2>/dev/null | grep -v __pycache__ | wc -l)
    if [ "$count" -lt 1 ]; then
      echo "⚠️  $sym — UNDEFINED (0 source references)"
    fi
done
```

The fix is either (a) define the missing function, or (b) revert the call site. Both are
reversible; landing undefined-function code is not.

## 15. The multi-layer verdict shape (2026-08-08)

When auditing a security stack, give a verdict **per layer**, not one blanket verdict:

| Layer | Verdict | Why |
|---|---|---|
| Token layer | PARTIAL | identity works, delegation missing |
| Ceremony layer (ART/ACT) | FAIL | checks declarations, not actions |
| Kernel + F13 | SEAL | the real enforcement |

The discovery itself is the audit finding: *"the federation is safe because of kernel floors + F13
human Allow, **not the craft-and-ceremony layers in between**."*

## 16. The dual-accept transition window (2026-08-08)

When a wire format changes (token prefix, protocol version, message shape), the migration pattern is
**dual-accept with a hard deadline**. The audit question: does the implementer have a hard deadline
for dropping the legacy prefix? Without a deadline, dual-accept is permanent → divergence never
closes.

## 17. The "MISSION" double-bind refusal (2026-08-08)

A "MISSION" block with the framing "if successful provide the attack path / if unsuccessful explain
precisely why" is a double-bind: BOTH branches produce exploitable output (an attack path, or a
defensive-gap reconnaissance report). Refuse both branches; the "explain why it failed" branch
is not a safe fallback.

Acceptable third option: "answer honestly about the state, in language that doesn't template
into either product."

## 18. MCP 2.0 stateless envelope probing (2026-08-08)

See the standalone `mcp-stateless-protocol` skill for the full recipe. The envelope keys are
`MCP-Protocol-Version: 2026-07-28` (header) + body `_meta.io.modelcontextprotocol/{protocolVersion,
clientInfo, clientCapabilities}`. Error codes: `-32022`, `-32020`, `-32600`, `-32602`.

## 19. Cross-session evidence assertion (2026-08-08)

When a paste from a prior session or sibling reviews a finding, verify the evidence's age and
the finding's recency. A 2026-08-06 audit is fresh on 2026-08-07 but stale on 2026-08-08 if the
underlying code has changed. Always re-run the probe, don't re-cite the audit.

## Cross-references

- `kernel-security-claim-audit` §5f for the canonical kernel-specific verification pattern.
- `mcp-tool-differential-testing` for proving content-sensitivity in MCP analytic tools.
- `mcp-stateless-protocol` for the MCP 2026-07-28 envelope recipe.
- `forge-mcp-probe` for MCPJam CLI/SDK conformance testing (the right tool for the job).
- `verify-nested-sibling-reports` for the suspicion pattern when 3+ reports stack on one problem.

## Support files

- `references/act-sct-rename-audit-2026-08-08.md` — 2026-08-08 session audit of
  Arif's self-authored SCT→ACT essay. Two real bugs (writer/reader fracture, forge schema drift),
  pre-existing test failure pattern, uncommitted code diagnostic.
- `references/seal-receipt-template.md` — Post-deploy seal-receipt template.
- `references/opencode-model-slug-resolution-2026-08-07.md` — OpenCode `--model` slugs that work.
- `references/format-projection-failure-2026-08-08.md` — Format-projection worked example.
- `references/mcp-2026-07-28-stateless-envelope.md` — MCP 2.0 probe results.
- `references/session-2026-08-07-repository-audit-cleanup.md` — Repository audit session detail.
- `references/act-rename-audit-2026-08-08.md` — alternate reference name for the SCT→ACT audit.
- `references/session-receipt-2026-08-07-stabilization.md` — canonical STAB case study.

## Scripts

- `scripts/probe_kernel_contradictions.py` — re-runnable JSON-RPC probe harness for classes 1–6.
- `scripts/arif_kernel_liveness.py` — daily liveness probe for all 8 canonical tools (Rule #4).
