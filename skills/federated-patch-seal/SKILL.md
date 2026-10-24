---
name: federated-patch-seal
description: Full lifecycle of a multi-agent MCP tool-bug fix in the arifOS federation — probe → identify → delegate to coding agent → peer audit (OpenClaw) → re-delegate or manual completion → deploy → live verify → seal. Use when a bug is found in a federation organ's MCP tool, needs fixing, and must be sealed to VAULT999. Covers the coding-agent routing rule (opencode primary, Kimi/codex/claude-code secondary), the peer audit gate, and the seal ceremony failure modes.
tags: [forge, federation, seal, patch, multi-agent, opencode, audit]
---

# Federated Patch-Seal Lifecycle

> Forged: 2026-08-08 | Canonical session: `wea-seal-2026-08-08` (WEALTH capital_entropy F1–F4)
> Doctrine: DITEMPA BUKAN DIBERI

## When to use

- A probe (MCPJam, manual, live) found a bug in a federation organ's MCP tool
- The fix requires source edits + tests + deployment + seal
- Multiple agents may be involved (coding agent writes, peer agent audits, Hermes orchestrates)

## The 7-stage lifecycle

### Stage 1: PROBE — confirm the bug exists on live wire
```
1. Health gate first: curl http://127.0.0.1:<port>/health
2. Session handshake (if organ is session-required: GEOX, WEALTH, WELL, FED)
3. Call tool with the buggy input AND a correct-input variant (4-variant matrix for type bugs)
4. Record: verdict, coverage, warnings, reflection — the exact fields that differ
5. Check: is the bug a schema issue (pydantic accepts wrong shape), a logic issue (handler ignores valid input), or an architectural issue (gate at wrong layer)?
```

**Critical rule:** Re-probe after any claim about what a tool returned. Memory of output = stale. Wire = truth.

### Stage 2: CLASSIFY — what tier is the fix?
| Tier | Scope | Agent |
|---|---|---|
| T1 (single file, ≤200 lines) | Add a type coercion, add a `shadow=True` gate, fix a constant | opencode (primary) or manual (Hermes) |
| T2 (multi-file, ≤3 files) | Gate threading across modules, schema change + handler change | opencode (primary), manual backup |
| T3 (cross-organ, >3 files) | A-FORGE path fix, schema change affecting all callers | A-FORGE execute gate required |

### Stage 3: DELEGATE — coding agent + task brief
**Routing (EMD doctrine):**
```
opencode (PRIMARY F13 sovereign path) → agy (Claude Sonnet 4.6, good for T1–T2) → Kimi/codex/claude-code (secondary)
```
If `opencode run` times out → do it manually; don't spawn a different agent for the same T1 task.

**Task brief format (self-contained):**
- What the bug is + exact repro output
- What the previous attempt got wrong (if any — always include if you have audit findings)
- Where to find the code: `file:line_range` + function name
- What to fix (concretely — "add `shadow` param here", "check `arguments.get("shadow")` before `_emit_receipt`")
- What NOT to touch (scope boundary)
- How to test: exact `pytest` command + expected pass count

**Pitfall:** If the brief is too long, opencode hits step limit. Put the bug, the fix location, and the test command in 15 lines max; put context in attached files (`-f file.py`).

### Stage 4: PEER AUDIT — before merging any coding agent's patch
**Always. No exceptions.** Use OpenClaw for peer audit (SENSE lane, not coding lane).

**The 3 questions that catch recurring failure modes:**
1. **Wrong architectural layer?** Does the fix touch where the bug lives (the `_emit_receipt` call site) or just a symptom (the `result["shadow"]` in the envelope)?
2. **Field-scoped only?** Does the fix apply to the field CLASS (`CoercedDictList` across all 7 fields) or only the reported INSTANCE (`current_kpis`)?
3. **Blanket downgrade?** Does the fix create a regression for a mode that legitimately emits the same signal (`metric_purpose_audit` always emits `evidence_quality=MISSING` by design)?

**OpenClaw audit command (via federation-peer-consultation):**
```bash
openclaw agent --agent main \
  --message "Audit this patch for [N] bugs. Look for: wrong-layer fixes, field-scoped-only gaps, regression from blanket downgrades. Output: 1-line verdict + 3-bullet risk list." \
  --timeout 180
```

If OpenClaw flags architectural bugs → cancel the patch, revise the brief, re-delegate or complete manually.

### Stage 5: DEPLOY — land + restart organ
```bash
cd /root/<organ>
git merge <worktree-branch> --no-ff -m "merge: <brief description>"
make deploy-local   # rsync + systemctl restart + health check
curl -sf http://127.0.0.1:<port>/health
```
**Reversible-first:** If tests pass but health fails, `git revert HEAD` + redeploy.

### Stage 6: LIVE VERIFY — re-probe on live organ
Run the same probe from Stage 1 against the deployed code. Assert the exact field values changed:
- `verdict` shifted from buggy value to expected value
- `coverage.ratio` moved from 0.0 to >0.0 (F1 type bug)
- `shadow` field present in result when `shadow=True` (F2)
- `kappa_r` varies between call modes (F3 — was constant before)

**Unit tests are necessary but not sufficient.** Live wire verification is the SOVEREIGN_VERIFY discipline.

### Stage 7: SEAL — append to VAULT999
**Lane B (autonomous, no 888_HOLD):**
```python
forge_vault(
    mode="receipt",
    name="<session-label>-<date>",
    category="<organ>",
    reason="SESSION_CLOSE",
    tier="session.ledger",
    actor_id="ARIF",
    content=json.dumps({...patch summary, files, test_result, live_verify, open_loops...})
)
```
**Gate reality (verified 2026-08-08):**
- `forge_vault(mode="receipt")` → requires `URLElicitationRequiredError` (-32042) unless SOVEREIGN actor_id is used
- `arif_seal` → requires SOVEREIGN authority (kernel-level gate)
- Both gates return `888_HOLD` when actor is not F13 SOVEREIGN
- **When gate blocks:** Report "SEAL blocked at F13, awaiting your ack" — don't retry, don't fake receipt. The gate working is the correct behavior.

**F13 authorization pattern (Arif):** verbal `push seal ja la` or `seal` = F13 authorization to (1) land code to canonical source, (2) push to origin, (3) deploy, (4) seal. No re-presenting options or re-explaining gates after this signal.

**Seal content must include:**
- `patch_ref`: branch, commit, worktree path, live path
- `test_result`: "N/N PASS"
- `live_verify`: per-bug before/after values
- `delta_s`: "≤ N bugs fixed, no new surface added"
- `open_loops`: anything not in this patch
- `co_authors` and `verified_by` credit chain
- `audit_chain`: who caught what (e.g. "OpenClaw caught 3 architectural bugs in Kimi patch")

---

### canon-mutate argv boundary loss — "rc=0 + lock_restored=true" is NOT effect (Forged 2026-10-22)

MARKER:CANONMUTATE-D1-ARGBOUNDARY-2026-10-22

`canon-mutate run <tree> -- <cmd>` built `CMD="$*"`, which **flattens argv** and
destroys quoting, so nested shell forms silently no-op:

```
bash -c "cat staging >> target"    # flattened to: bash -c cat staging >> target
```
The inner `bash` gets `cat` as its command, `staging` becomes `$0`, and the OUTER
shell performs `>>`. Result: **rc=0, lock_restored=true, ZERO bytes written.**
Confirmed in production receipts [141][142] (staging payload absent from target).

- Flat `cat a >> b` and heredoc forms happened to work -> historical successes do
  NOT falsify the defect (different invocation forms, different outcomes).
- **Fix shipped** (canon-mutate scheme 1.3): rebuild `CMD` word-by-word, `printf %q`
  each word, pass pure shell operators (`&& || ; | >> < << 2>`) unquoted. Verified
  12/12 suite + live canary flat/nested/cd = VERIFIED_EFFECT on the prod ledger.
- **Always verify EFFECT, not rc:** pass `--expect-target <file>` +
  `--expect-lines-delta N` (or `--expect-sha256-post`). Verdicts: `FAIL` (rc!=0),
  `VERIFIED_EFFECT`, `NO_EFFECT`, `UNVERIFIED` (no postcondition declared).
  `lock_restored` is a SEPARATE field, never proof of effect.
- **Concurrent-mutation check:** a `chattr +i` tree can still be
  thawed->written->relocked by another actor. Re-derive digests and check mtimes
  before trusting a pin — a sealed digest that no longer re-derives is void.

## Coordination patterns

### Kimi auto-commit before opencode finishes
Kimi Code may auto-commit on a branch while you're waiting for opencode. When this happens:
1. Don't panic. Read Kimi's diff — it may be correct or partially correct.
2. Run peer audit (Stage 4) against Kimi's commit.
3. If clean → adopt it (amend commit message, add test, keep going).
4. If architecturally wrong → `git reset --hard <pre-kimi-commit>`, re-delegate or fix manually.

### opencode step-limit hit
opencode `run` with `--variant high` + `--thinking` + 4 files of context may hit step limit mid-task (observed: 12/15 tests pass). When this happens:
1. Check `git status` — opencode usually wrote 80% of the patch before the limit.
2. Complete the remaining 20% manually (usually a missing param in a function signature).
3. Don't re-spawn; the model already understood the task — the limit is token-count, not comprehension.

### ⚠️ Model ID verification before `--model` (Forged 2026-08-13)

**The `--model` string must be the exact registered provider/model ID. Plausible-looking wrong IDs fail silently** (with `Error: Model not found` and a `Did you mean` suggestion list).

**Real failure:** `--model minimax/MiniMax-M1` → `Error: Model not found: minimax/MiniMax-M1. Did you mean: MiniMax-M2.1, MiniMax-M2.1-highspeed?` Session terminated before any task execution.

**Before passing `--model`:**
1. `opencode models <provider>` to list exact model strings
2. Or `opencode auth list` + check provider config
3. Do NOT guess model generation suffixes (M1, v1, latest)
4. MiniMax family: `MiniMax-M2.1` (balanced), `MiniMax-M2.1-highspeed` (faster, trade-off). Never `MiniMax-M1`.

**Recovery:** if a spawn dies with model-not-found, fix the ID and respawn. Don't try to coax the same wrong ID into working.

### Worktree ≠ canonical source
- `/tmp/wealth-fix-*` is a clone, not the real code.
- `git push origin <branch>` from worktree may fail if origin is `/root/<organ>` (the same repo, with branch checked out).
- **Canonical land path:** `git merge <worktree-branch>` inside `/root/<organ>`, then `make deploy-local`.
- Never `rsync` from worktree — use `git merge` to preserve commit history.

### Concurrent writer on shared repo (detect, wait, reconcile)
The federation may dispatch two coding agents (you + a sibling) to the same repo with overlapping but **contradictory** briefs. One common case: a sibling opencode mission explicitly forbids what your mandate requires (e.g., sibling's rules say "Do NOT wire VAULT999" while yours says "FIX 6: wire VAULT999"). Detection and reconciliation is the survival skill.

**Trigger signals (any one = suspect a sibling):**
- `patch` returns `_warning: ... was modified since you last read it on disk (external edit or unrecorded writer). Re-read the file before writing.`
- A file's mtime jumps between two `stat` calls (e.g., a file you just edited gets rewritten 2s later by someone else).
- `ps aux | grep -E 'opencode|claude|codex|hermes'` shows a long-running sibling coding agent whose argv references files in the same repo you're patching.

**Action sequence:**
1. **Stop patching immediately.** Your next edit will either clobber the sibling or trigger repeated "external edit" warnings. Neither is recoverable mid-flight.
2. **Poll the sibling to finish.** Check the process every ~30s (e.g., `ps -p <pid>`) until it disappears. Sibling tasks are bounded — they run cargo test / report / exit.
3. **Enumerate scope via git, not memory.** Run `git status --short` and `git diff --stat` to see exactly what the sibling touched. Trust the diff, not your recall of the original.
4. **Re-read the full current state of every file the sibling modified.** Partial-view reads from before the sibling started are stale. A full `read_file` (no offset/limit) is the ground truth.
5. **Classify each sibling change into one of three buckets:**
   - **Compatible improvement** (resolves your audit finding, doesn't contradict your spec) → **KEEP.** Example: sibling added `push_chain_aware` while you were going to use `push()`; both resolve the same audit finding; keep theirs and add your spec's log line.
   - **Reverted your mandate item** → **re-apply yours.** Example: sibling reverted your `/release` auth with a "deferred to F13" comment → restore your checks. Your spec is your contract; mandate items are not optional.
   - **Direct conflict on a constraint** → **your spec wins.** Document the deviation in your report so the parent can reconcile.
6. **Re-add any imports/types the sibling's rewrite stripped.** A "Do NOT wire X" sibling mission will often delete the import you added for X. Re-add; cargo build will fail without it.
7. **Save originals early** (`cp <file> /tmp/<file>.orig`) before your first edit — enables clean unified diff generation for your final report even after the sibling's rewrite shifts line numbers.
8. **Build + test.** Expect missing imports and type mismatches introduced by the sibling's rewrite; fix surgically.

**Pitfall — patching during a live sibling:** Repeated partial edits produce accumulating "external edit" warnings and inconsistent intermediate states. Worse, your `FIX N` re-application may itself be clobbered 30s later. Always wait for the sibling to terminate.

**Pitfall — removing the sibling's new methods/tests:** If the sibling added Rust tests for their new method (e.g., `push_chain_aware`), removing the method to force your variant breaks those tests → `cargo test` fails → fails your "zero failures" rule. Default to **keeping** the sibling's compatible additions (new methods + their tests) and reconciling to your spec at the call site, not by deletion.

**Pitfall — silent type unification break:** The sibling's rewrite may turn a hand-rolled HTTP handler arm (`let response = if ... { ... } else if arm { ... }` where each arm produces `Vec<u8>`) into a shape that no longer unifies. If your re-applied block uses `let _ = stream.write_all(...);` inside an arm and then `return;`, the arm now evaluates to `()` while siblings arms evaluate to `Vec<u8>` → E0308. Fix: make the success path return the response bytes (outer `write_all` handles them); forbidden paths write directly and `return;` early from the function. The early-return branches must `return;` from `handle_client`, not `return write_result;` (function returns `()`).

## References

## References

- `references/wea-seal-2026-08-08.md` — full session transcript: 4-bug lifecycle from probe → OpenClaw audit → Kimi patch → opencode hit → manual completion → deploy → seal, including the exact `forge_vault` call shape and the `-32042` elicitation gate.
