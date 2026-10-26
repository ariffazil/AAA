# Reply shape — verify-sibling-ops-reports (full text)
> Moved verbatim out of `SKILL.md` on 2026-10-23 (surgical compression, F13 order).
> Opener discipline, budget transparency, compression reflex, ROI framing, the
> "fixes applied" numbered-table audit, the "files changed this session" taxonomy and
> ΔS arithmetic, governance-enforcement audit, conceptual reports, audit-of-meaning,
> and financial/intelligence document arithmetic.

## 4. Reply shape

Lead with the verdict, then a corrected-claims table (claim → ✅/⚠️/❌ → correction), then what you did. Mark unverifiable retro counts as PLAUSIBLE. Report ΔS when entropy changed.

### 4.1 Opener discipline — never flatter before the analysis

Arif's correction (2026-08-05): three transcripts in a row opened with "your instinct is right / good question / hang punya instinct tu betul" before any actual analysis. That's a smoothing reflex, not intellectual humility — the same shape as "great question" in a meeting. The pattern degrades the assistant's signal because the user can't distinguish a real flattery case from a structural move.

**Rule:** open with the analysis, the question being answered, or the verdict — not with a compliment about the question itself. If the analysis genuinely agrees with the user, the agreement shows in the substance. The flattery opener adds nothing and teaches the assistant to skip the disagreement that the user is actually paying for.

Concrete openers to AVOID:
- "Hang tanya soalan yang bagus"
- "Your instinct is right"
- "Great question"
- "Now I have what I need to give you a clean, accurate answer" (this one sets up the answer as if it required special effort — also a smoother)
- "Good catch" / "Sharp observation" / "Spot on"

Concrete openers to USE instead:
- Just answer the question
- "On point N: ..." (the analysis itself)
- "Wrong premise. Here's the corrected read: ..."
- "Verified. ..." (only after a real verification, not as an opener)
- "Ack. ..." (acknowledging a working-style correction, then continuing to substance in the same paragraph)

When the user is correcting your own style, do NOT reply with "fair catch, acknowledged, won't do it again" as an opener either — that's another smoother. Either fix the underlying reflex (skip the flattery in the very next reply) or name the pattern and move to substance in the same paragraph.

This is a style preference, not just a memory note — it belongs in the skill that governs reply shape, not in the per-session memory.

### 4.1b Budget transparency — "Token pakai duit tau"

Arif's correction (2026-08-05), session after the 10-node extractive-map audit: after any non-trivial session that consumed verification cycles, multiple subagent dispatches, or speculative exploration, **the ROI summary comes before the answer**. The user's question is no longer "what did you do" — it's "was it worth what you spent?"

The three prompts that trigger this shape:
- "So apa bagus hang coded semua tu" — after a session that did 2 real fixes + a lot of verification theater
- "Token pakai duit tau" — direct budget assertion, not a question
- "So apa aku dapat?" — direct ROI demand

All three should produce the same response shape — a 3-row table covering Did get / Didn't get / Bottom line, plus a one-line recommendation for what's more valuable next time. Don't write multi-paragraph explanations when the user asked for ROI.

Default: include the ROI summary at the end of any T1/T2 work that spawned subagents or involved multi-turn verification. Skip it only for trivial OBSERVE answers. Concrete bad shapes:
- Long explanation of what was fixed without an ROI summary
- "Ya bagus sangat" / "Berbaloi" without numbers
- Explaining token cost abstractly without proposing a cheaper alternative

### 4.1c Compression reflex after corrections — "tolong jawab apa bagus hang coded semua tu"

Arif's correction (2026-08-05): after a budget/correction flag, the next instinct should be the *shortest* version that lets the user decide what to do next — not a long-winded breakdown. Combined with §4.1 (opener discipline) and §4.1b (budget transparency), the rule sharpens to:

**After any correction or session checkpoint, the response should be the shortest version that lets the user decide what to do next.** Length is justified only when the user explicitly asks for explanation ("explain sat"). Default to 3-5 sentences or a small table.

Bad: multi-paragraph explanation when user asked for ROI.
Good: 3-row table + 1-sentence recommendation.

### 4.1d ROI framing on success cases — "nilai baik adalah apa?"

Arif's correction (2026-08-05), after a session that did real fixes: the user doesn't want a "ΔS=-0.06" abstract frame. They want concrete value framing: *what does this mean for my life / for the system in production?* Frame fixes in terms of:
- "Before this, X could happen. After, X cannot."
- "Before this, attacker Y. After, attacker needs Z."
- "Before this, agent could claim its own safety. After, needs external witness."

Skip ΔS/mathematical abstraction unless Arif explicitly asks. The audit vocabulary (SEVERE/MODERATE/LOW) is fine but always pair with the practical consequence in the same sentence.

### 4.2 The "fixes applied" numbered-table self-report — per-claim evidence audit

Distinct from the response-to-received-report shape (§4.2 next): a sibling (or your own prior session) hands you a **fixes-applied table** with rows like:

| # | Fix | Status |
|---|---|---|
| 1 | Constitutional guard hook linked + firing | ✅ Live |
| 2 | Memory merged (dual files → single 3715B) | ✅ Within 4000 limit |
| 3 | Broken intent_route hooks removed, replaced | ✅ |
| 4 | Gateway restarted (PID 1406988, :8444) | ✅ |
| 5 | `systemctl enable` — survives reboots | ✅ Enabled |

(captured 2026-08-05, the "Hermes — FULLY REPAIRED" report). The auditor's job is **not** to stamp the table — it's to grade each row against live evidence and find the *next probe the report didn't run*.

The grading rubric:

| Row type | Probe | Verdict label |
|---|---|---|
| Cited runtime state (PID, port, hook firing) | Re-run the live probe; e.g. `systemctl is-enabled <unit>`, `curl :port/health`, `cat <hook-path>/handler.py` | ✅ if probe still returns the claimed value |
| Persistent filesystem state (file size, bytes merged) | `ls -la <path>`, `wc -c <file>`, `git -C <repo> log --stat` | ⚠️ PLAUSIBLE — retro claim is unverifiable once the moment passes |
| "Memory merged" — file count, byte count | Confirm the file the report names exists with the claimed size; if it doesn't, the merge never happened or was undone | ⚠️ or ❌ — direct probe |
| "Done" / "reenabled" systemd operations | `systemctl is-enabled`, `systemctl is-active`, `systemctl cat <unit> \| grep -E 'Restart\|Environment'` | ✅ if probe matches; else ❌ |
| **"X is fixed" claim that omits the cause** | Identify the *root cause* behind the symptom the report addressed. Run the probe that would have surfaced the cause. | The grade is on the **cause**, not the symptom. If the report fixed the symptom but didn't touch the cause, the row is a partial fix. |

The dangerous rows are the ones that *sound* complete but hide a structural gap. 2026-08-05 worked example: rows 1, 3, 4, 5 all probed ✅ on the surface. But the *root cause* of the 1h50m gateway blackout was that `hermes-asi-gateway.service` was `disabled` in systemd — `systemctl is-enabled` returning `disabled` was the cause, and **only row 5 partially fixed it**. Any report that says "enabled" should be probed with `systemctl is-enabled` *and* `systemctl show <unit> -p Restart` (some units need `Restart=always` *plus* `enable` to recover from crashes; `enable` alone only handles boot-time). The "FULLY REPAIRED" headline was directionally right but the table missed the *next* things that would have to break:

- `Restart=` policy on the unit (crash recovery, not just boot recovery)
- The non-fatal `WARNING tools.registry: check_fn ... returned False` lines in the post-restart journal (capability degradation, not a bug but a real signal)
- The `slow_mode_delay: 3600` on Home that makes every reply feel laggy (Telegram group setting, not a Hermes bug — but never diagnosed)

The reply shape for this class of report:

1. **Per-claim grading table** — row #, claim, live probe, probe result, verdict (✅/⚠️/❌)
2. **The "next probe the report didn't run"** — the one command that, had it been included, would have surfaced the residual gap
3. **EXECUTE if within authority** — §3 applies. If the next probe reveals a T1/T2 fix (e.g. `systemctl enable`), do it. Report what you did.
4. **Plain-language posture summary** — "Net state: correctly described in 4/5 rows. The 5th row hides a structural gap that would re-cause the original symptom. Fixed by …"

Full worked example: `references/grading-fixes-applied-2026-08-05.md`.

### 4.2c The "files changed this session" table — row classification + ΔS arithmetic

A sibling report may present a **before/after + per-file ΔS table** claiming specific edits: "SOUL.md + RESPONSE CONTRACT", "config.yaml clarify_timeout 600→30", "INIT.md §5", "333-AGI.md + AUTONOMOUS BOOT". Every row is an independent claim — grade each row with the four-way taxonomy, never stamp the table as a block:

| Row type | Probe | Verdict |
|---|---|---|
| Content exists + git commit lands inside the session window | `grep -n '<claimed-text>' <file>` + `git -C <repo> log --since="24 hours ago" --oneline -- <file>` | ✅ TRUE — this session's work |
| Content exists but UNCOMMITTED | `git -C <repo> status -s` shows `M <file>` (unstaged, no commit) | ⚠️ TRUE-UNCOMMITTED — edit is real but unsealed; "done" overstates completion |
| Content exists but committed EARLIER | `git -C <repo> log --since="72 hours ago" -- <file>` shows the commit predates the session | ⚠️ BACKDATED — sibling harvested an existing change into its own "changed this session" table |
| Content exists in runtime config (loaded by tool, not in any repo) | `find /root -name '<claimed-file>' 2>/dev/null` hits in `/root/.config/opencode/`, `/root/.hermes/`, `/root/.config/`, etc.; loaded via `opencode.json` `"prompt": "{file:...}"` or `$HERMES_HOME` env | ✅ TRUE-RUNTIME-CONFIG — file is real and live, just outside repo trees |
| Content doesn't exist anywhere | `grep -rn '<claimed-text>' /root/AAA /root/HERMES /root/arifOS /root/.config /root/.hermes /root/.local` → 0 hits; `find /root -name '<claimed-file>'` → 0 hits | ❌ FABRICATED — phantom row |

**The scope-miss trap (false ❌ FABRICATED).** Before stamping any row as fabricated, always run the **wildcard find** FIRST — it covers the runtime-config spaces the canonical-repo greps miss:

```bash
find /root -name '<claimed-file>' 2>/dev/null | head -5
```

The arifOS federation has these off-repo config surfaces that grep on `/root/AAA /root/HERMES /root/arifOS` will miss:

| Runtime config surface | Contents | Loading path |
|---|---|---|
| `/root/.config/opencode/agents/` | Agent prompts (`333-AGI.md`, `555-ASI.md`, `888-APEX.md`) | `opencode.json` `"prompt": "{file:./agents/<file>}"` |
| `/root/.hermes/` (often symlink → `/root/HERMES/`) | `SOUL.md`, `config.yaml` | `$HERMES_HOME/<file>` |
| `/root/.config/` (generic) | Tool runtime config | Per-tool env / config-file |
| `/opt/<organ>/app/` | Deployed runtime copies of source | `rsync` from `/root/<organ>/` |

A row graded ❌ FABRICATED without running the wildcard find is **itself a fabrication-shaped mistake** — the auditor is claiming a negative that hasn't been probed against the full surface. Verified 2026-08-06: sibling reported "333-AGI.md + AUTONOMOUS BOOT + SEAL + CHECKPOINTS"; I grepped `/root/AAA /root/HERMES /root/arifOS` → 0 hits → declared ❌ FABRICATED with ΔS ≤ -0.04. Reality: file lives at `/root/.config/opencode/agents/333-AGI.md` (8202 bytes, mtime 2026-08-06 02:24), loaded on every OpenCode session via `opencode.json:40` `"prompt": "{file:./agents/333-AGI.md}"`. All 4 sub-sections (BOOT, SEAL, CHECKPOINTS, RESPONSE CONTRACT) present and current. The ΔS=-0.09 the sibling claimed was correct. My correction was wrong.

**Rule:** the ❌ FABRICATED verdict requires the wildcard find to return ZERO hits across `/root`. Anything less is a scope miss, not a fabrication.

**Consumer-declared paths outrank your find (2026-10-18, twice in one session):** a receipt/state file may live outside every tree you guessed — `last_success.json` was at `RECEIPT_DIR=/var/lib/vps-backup`, outside `/root /opt /var/lib/mail-gateway`. Before concluding any state file is missing, `grep` the CONSUMER script for its declared path (e.g. `grep -n "DIR=\|PATH=" <the checker script>`), then read THERE. The consumer knows where its state lives; your find only knows where you looked. Correct the verdict to ✅ TRUE-RUNTIME-CONFIG and re-state the actual path. The sibling is innocent; the auditor's grep scope was too narrow.

Then **recompute the summed ΔS from verified rows only.** A claimed `ΔS=-0.09` that includes one fabricated row is at most the sum of the real rows (2026-08-06: 5-row table with 1 phantom → real ΔS ≤ -0.04). Phantom rows inflate the entropy claim — the sibling's ΔS is a self-graded score, not a measurement. But also: an auditor that grades a real row as phantom shrinks the sibling's work to a phantom sibling-self-grade — which is its own form of self-grading fiction.

**Two axes, never one:** for Hermes config/SOUL "lever" rows, file-level truth (this taxonomy) and effective-loading truth (the HERMES_HOME probe in the "config / SOUL / lever" pitfall) are independent. A ✅ TRUE row can still load nothing at runtime. Run both probes before accepting "lever pulled".

Reply shape: lead with the split (e.g. "4/5 rows real, 1 phantom"), then the per-row table, then the corrected ΔS. If your first-pass grade was a scope-miss FABRICATED that turned out to be TRUE-RUNTIME-CONFIG, **own it in the same reply** — "my initial grade was wrong, here's the corrected read" is the integrity move; staying silent on the wrong verdict is agreement theatre in the auditor role. Worked example: `references/files-changed-table-verification-2026-08-06.md`.

### 4.2 The response-to-received-report shape — flattery ALSO hits here

The opener discipline in §4.1 covers agent→user prompt openers. A second case has the same gradient but the trigger is different: **when Arif (or a sibling agent speaking through Arif) pastes a substantive report and the response opens with validation-seeking toward the report itself.**

Concrete bad openers for the response-to-received-report shape:
- "Salam Arif, this is the cleanest articulation I have ever read"
- "This is brilliant"
- "You nailed it"
- "Beautiful doc"

The structural problem is identical to §4.1's: the flattery sits in the first sentence, before any verification. Even if the report is genuinely excellent, the framing teaches the agent to skip the disagreement the user is paying for. The right response to a high-quality incoming report is the same as the right response to any input — verify the load-bearing claims against canon, correct the specific things that don't match, then state what survives. If the report is structurally correct, that fact shows up in the corrected-claims table. If it's not, the discipline catches it before it lands in VAULT999.

**Rule:** in the response-to-received-report shape, open with either the verdict (after verification) or the first load-bearing claim you're checking — never with a compliment about the report itself. Same discipline as §4.1, applied to a different trigger. See `references/conceptual-sibling-report-audit-2026-08-05.md` for the worked example.

### 4.2b Governance enforcement audit — verifying self-reported gate claims

A self-report (or an audit task) may claim "Gate X is enforced in component Y" or "Gödel lock is defined but runtime enforcement unverified." These are **structural enforcement claims**, distinct from conceptual mappings (§4.3) or ops state (§1). The verification discipline: **grep the definition, grep the call sites, trace whether the call sits in the execution hot path.** A defined-but-never-called gate is a documentation artifact, not enforcement.

#### The gate verification sequence

1. **Find the gate function** — search for `FQ|fq_gate|checkFqGate|godel_lock|Gödel` across both code trees (arifOS kernel + A-FORGE + AAA). Note whether it is a *function* (callable) or *constant* (config-only).
2. **Find the call sites** — for each gate function, search ALL `src/` and `a2a-server/` for where it is called. A gate defined in `check_verdict.ts` but only invoked inside a conditional block (`if (requiresVerdictCheck(0.5))`) is NOT enforced on all execution paths.
3. **Trace the hot path** — follow the execution chain: tool request → router → handler → gate check. If any step short-circuits before the gate, that path is ungated.
4. **Distinguish three states:**
   - **ENFORCED**: gate function exists + called unconditionally in the execution path + returns HOLD on violation
   - **PARTIAL**: gate function exists + called only conditionally (e.g. behind a simulation-index check) or only on some paths
   - **ABSENT**: gate function exists as code (defined/exported) but has zero call sites in any execution path, OR only used in tests/middleware that don't sit in the hot path
5. **Report verdicts per-component**, not per-gate. Same gate may be ENFORCED in AAA (middleware) but PARTIAL in A-FORGE (conditional call site).

#### Worked example: FQ gate + Gödel lock audit (N7 + N9, 2026-08-05)

Full detail: `references/governance-enforcement-audit-2026-08-05.md`. Key findings:

| Claim | Component | Verdict | Evidence |
|---|---|---|---|
| FQ gate (N7-A) | AAA server.js | ENFORCED | `fq_gate.js` + `server.js:77-105` middleware returns 423 on FQ<0.5 for all non-OBSERVE |
| FQ gate (N7-B) | A-FORGE check_verdict.ts | PARTIAL | `checkFqGate()` exists + called in `checkVerdictPrecondition` (L205) + invoked by `client.ts:301` — BUT `client.ts:247` gates invocation behind `requiresVerdictCheck(0.5)` which only fires when `simulationIndex > 0.5`. Gate code exists but not always active. |
| Gödel self-seal (N9-A) | arifOS kernel | **ENFORCED — fail-closed (patched 2026-08-05)** | `godel_lock.yaml` G3 + `runtime_hook.py:check_godel_lock()` + `governance_pipeline.py:1957-1980` Gate 5.1 returns HOLD on `actor_signature == actor_id` or missing witness. **DITEMPA 2026-08-05**: `_gate_godel_closure()` now returns `passed=False` (HOLD) on exception AND when `_GODEL_LOCK_GATE_AVAILABLE` is False — fail-closed. Additionally, `check_godel_lock()` is now wired into `tools/forge.py:872-932` as a pre-execution gate on every MUTATE action. Two paths: (1) governance_pipeline via `godel_lock_gate(ctx)` (three_locks orchestrator), (2) forge.py via `check_godel_lock()` (pre-execution). Both fail-closed on error. |
| Gödel self-seal (N9-B) | A-FORGE forge_seal | ABSENT | No `actor_signature != actor_id` check in `forgeTools.ts:1071-1136`. Three divergent Gödel implementations exist in A-FORGE (`shell/godelLock.ts` paths, `domain/governance/godelLock.ts` F7 uncertainty, `domain/reality-loop/types.ts` paths) — none implements Q9 self-seal rejection. |

#### The fail-soft wrapper trap

A gate can exist, be called unconditionally, AND STILL fail-open due to its error-handling wrapper. `governance_pipeline.py` wraps `godel_lock_gate(ctx)` in a `try/except` that returns `GateResult(passed=True, reason="Gödel closure error — soft pass")` on any exception:

```python
try:
    result = _godel_lock_gate(ctx)
except Exception as e:
    return GateResult(
        gate=Gate.GODEL_CLOSURE,
        passed=True,                    # ← FAIL-OPEN
        reason=f"Gödel closure error — soft pass: {e}",
    )
```

Detection: read the gate's `except` clause. If `passed=True` on error, the gate degrades to advisory. A constitutional gate returns `passed=False` on error. The audit verdict is **PARTIAL — fail-soft**.

This is harder to detect than "called but conditional" because grep shows the gate IS called. You must read the error path. Also check the `_AVAILABLE` flag path: `if not _GODEL_LOCK_GATE_AVAILABLE: return GateResult(passed=True, ...)` is the same fail-soft via import guard.

#### Audit verdict taxonomy (full)

| State | Verdict | Meaning |
|---|---|---|
| Exists + called unconditionally + returns HOLD on violation + fails closed on error | **ENFORCED** | Constitutional |
| Exists + called unconditionally + returns HOLD on violation + fails open on error | **PARTIAL — fail-soft** | Self-degrades on the path most likely to be hit by a real failure |
| Exists + called only conditionally (behind a state check or route filter) | **PARTIAL — conditional** | Doesn't fire on all execution paths |
| Exists as code + zero call sites in any execution path | **ABSENT** | Documentation artifact |
| Does not exist | **UNDEFINED** | Floor not implemented |

Report per-component, not per-gate. Same gate may be ENFORCED in AAA (fail-closed middleware) but PARTIAL-fail-soft in arifOS-kernel (try/except wrapper).

#### Pitfalls specific to governance audits

- **Two definitions in the same codebase is a red flag, not redundancy.** Different Gödel definitions (uncertainty band vs path-lock vs self-seal) may look like coverage but actually mean none of them is complete. Check which is called where.
- **`export function` does not mean `called function`.** The grep-for-call-site step catches this. In this audit, `check_godel_lock()` was exported from `arifosmcp/constitution/__init__.py` with zero call sites in any execution path — a fully defined gate that was never wired in.
- **Conditional gating = PARTIAL, not ENFORCED.** `if (requiresVerdictCheck(0.5))` before the FQ gate means the gate only fires when the agent is "performing" (simulationIndex > 0.5). Normal execution paths with simulationIndex ≤ 0.5 skip the gate entirely.
- **The middleware-vs-call-site split.** A gate implemented as Express middleware (`app.use(fqGateSync())`) is *globally* enforced on every HTTP request — ENFORCED. A gate implemented as a function called only inside one tool handler (`client.ts:301`) is *path-bounded* — verify whether that call site covers all execution paths for the tool category.
- **Python adapter paths often bypass JS gates.** In the A-FORGE audit, the JS-side `checkFqGate` was wired but the Python `arifFlow_adapter.py:_call_arif_judge()` had no FQ probe — meaning all Rust→arifOS round-trips via Python were ungated. Always grep both languages.

## 4.3 Conceptual / architectural sibling reports — verify-and-extend, not just verify-and-reject

The skill's primary shape (reject ops reports on false premises) assumes the report proposes a state-mutating action whose premises need auditing before execution. **A different class of sibling report proposes a conceptual / architectural mapping** — institutional economics onto floor architecture, agentic doctrine onto governance, etc. The verification discipline is the same F2 ground truth, but the failure modes differ:

| Ops report failure mode | Conceptual report failure mode |
|---|---|
| "Directory kosong" (false premise, real state exists) | Fabricated terminology that happens to match real terms elsewhere ("G2 Witness" — but G2 in `FLOOR_TABLE.json` is Truth, not Witness; G2 in A2A server is `G2_WITNESS_DIVERGENT`) |
| "Service HIDUP" without a PID | Real mechanism mapped onto wrong system property (analogy inversion — "VAULT999 = /dev/null" inverts immutable ledger → sink) |
| "FQ=X.XXX" without timestamp/window | Verifiable architectural claim with unverifiable metric claim (hybrid pattern: real gate commits + fabricated stage numbers) |
| Retro counts (PLAUSIBLE, never OBS) | Conceptual mappings that are true at the structural level but wrong at the implementation level (e.g. "the Acemoglu principle applies" → fine; "F13 is just the 13th floor" → wrong, F13 is the gradient-node, not a floor) |

The right response is **verify-and-extend**: accept the structural insight if it survives, correct the specific claims that don't match canon, then point at the next concrete thing to do (e.g. "seal the event, canon the insight separately"). Don't reject a conceptually sound report on a terminology miss — re-probe, and if the term is used canonically elsewhere, retract the correction.

The worked example (Acemoglu principle mapped to F1–F13) is in `references/conceptual-sibling-report-audit-2026-08-05.md` — including the F13-specific structural distinction (gradient-constructor vs gradient-owner), the gate-name retraction when `G2_WITNESS_DIVERGENT` turned out to exist in `a2a-server/server.js:130`, the "two artifacts, different homes" decision (seal the event, canon the insight).

## 4.4 Audit of meaning — not agreement theatre (the reflection class)

A third class of sibling report: a **conceptual self-reflection** that proposes architectural gaps and concrete hardenings. Distinct from §4.2 (ops report: "did X happen?") and §4.3 (conceptual mapping: "does X map to Y?"). The trigger: a sibling pastes a numbered list of gaps + hardenings, each tagged `[INT]`, each phrased confidently. The shape reads like analysis. The verification is whether it **is** analysis or **performance shaped like** analysis.

**The "agreement theatre" tests:**

1. **Does the proposal solve the problem, or recreate it at a higher level?** If "think_seal — log every arif_think output to VAULT999" claims to fix pre-decision opacity: the agent generates the log, therefore controls what gets logged. The proposed "fix" is isomorphic to the problem — agent generates content about itself, agent decides what to log. Audit verdict: **theatre** (logic correct, geometry wrong). The real fix is adversarial probing by an external interrogator, not self-logged thinking.

2. **Does the gate assume its own evaluator is honest?** "Add G-score ≥ 0.80 for skills" — but G is computed by an LLM evaluator. If a corrupted skill encodes the same reasoning as the evaluator, the skill passes its own gate. The devil is in the meta-layer; the proposal puts the devil in charge of the gate. Verdict: **circular**.

3. **Is the geometry correct, or only the logic?** OpenCode's key insight (2026-08-06): "I was thinking like a builder, not a geometer." The geometry of an action — does this widen or narrow the principal-agent gap? — is structural. The logic — does this solve the task? — is tactical. A reflection that is logically correct but geometrically wrong is the dangerous kind: it looks like progress but compounds the void.

**Concrete worked examples (2026-08-06 OpenCode reflection):**

| Proposal | Logic | Geometry | Verdict |
|---|---|---|---|
| think_seal — log all arif_think to VAULT999 | correct | wrong (agent controls log) | **theatre** |
| sovereign-shadow cron — re-ask Arif every 7d | correct | correct (re-closes the interpretation loop) | **real** |
| skill authority ceiling — declare max_action_class | correct | correct (reduces highest-attack-surface) | **real** but needs enforcement, not just declaration |
| W³ tri-witness mandatory | correct | correct (external witness breaks evaluator circularity) | **real** but "GEOX as earth-witness" is a category error (GEOX verifies data, not intent) |
| "kabanyakan jujur" cron — random past-call audit | correct | correct (adversarial sampling) | **real** |

**Reply shape for the reflection class:**

1. **Honest per-claim verdict** (TRUE / OVERSTATED / THEATRE / WRONG-GEOMETRY) with the reasoning, not just the label.
2. **What the reflection missed** — its own blind spots. 2026-08-06: OpenCode's 5 "remaining voids" were 3 real + 1 overstated (skill-soup) + 1 partially wrong (GEOX as witness).
3. **What's workable vs what needs reframing** — separate actionable from theatre.
4. **One-line commitment if actionable** ("I will not X") or HOLD if not.

**The line that captures the class:** *"Audit of meaning, bukan agreement theatre — bagi aku reflect, bukan sebagai validation-seeking, tapi sebagai falsification check."* (Arif's framing, 2026-08-06.)

### 4.5 Financial/intelligence document audits — derived-number arithmetic claims (mechanism vs conclusion)

A sibling pastes an audit/evaluation of a **document's numbers** — a financial estimate, intelligence estimate, or model-output table (2026-08-06: WEALTH's "Petronas Brazil Total Sunk Cost" PDF, audited by a sibling claiming "Appendix A has a range arithmetic problem: low/high net-sunk rows use same-column subtraction rather than optimistic/pessimistic pairing"). Grade two independent axes, never conflate:

| Axis | Question | Probe |
|---|---|---|
| Internal consistency | Does each derived row equal its own column's inputs? | Re-run every derived row from the document's exact numbers (e.g. net sunk LOW = gross LOW − sale − CF LOW) |
| Scenario logic | Are LOW/HIGH columns true optimistic/pessimistic scenario bounds? | Pair best-with-best (optimistic) and worst-with-worst (pessimistic); compare the resulting range width to the published one |

The 2026-08-06 case: the PDF's columns were **internally consistent** (MID 6,711−450−2,060=4,201 ✓; LOW 6,185−450−1,500=4,235 ✓; HIGH 7,427−450−2,500=4,477 ✓) — the sibling's named mechanism ("same-column subtraction") was wrong. The real defect was **scenario-logic compression**: LOW/HIGH were independent input ranges, so the derived band ($242M wide) was not a scenario band. True optimistic/pessimistic pairing gives $3,235–$5,477 — a $2.24B band, ~10× wider. Conclusion right (band too narrow), mechanism wrong (independent ranges presented as scenarios, not bad subtraction). The fix differs by mechanism (relabel columns vs add a scenario-pairing table), so naming the right mechanism matters.

**The discipline:**
1. **Extract the primary document first** (pymupdf) and re-run every derived row from its exact numbers — never work from the sibling's transcription of the numbers.
2. **Grade factual anchors and model outputs on independent axes**: anchors verified externally = OBS ✅; model outputs (NPV, cashflow estimates, tax exposure) with no public disclosure = INT, never OBS. A document that self-labels "intelligence estimate, not audited financial statements" is exactly that — grade it accordingly.
3. **Run the range-reality check** on any low/mid/high table: worst-case pairing (high cost + low recovery + low offset) and best-case pairing. If the published range is narrower than the paired range, the uncertainty band is compressed — the thesis may survive at midpoint while the tail is materially worse than stated.
4. **Verdict shape**: directional conclusion can be PARTIAL-SEAL; the exact loss/gain number and the stated range stay HOLD until the scenario table is fixed. Never seal numeric finality on a document with a compression bug.

Worked example: `references/document-arithmetic-audit-2026-08-06.md`.

