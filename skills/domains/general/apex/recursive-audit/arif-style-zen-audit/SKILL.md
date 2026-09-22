---
name: arif-style-zen-audit
slug: arif-style-zen-audit
description: "Run constitutional ZEN audits of Hermes/federation state per Arif Fazil's epistemic standards."
version: 1.0.0
owner: hermes-prime
license: MIT
metadata:
  clawdbot:
    emoji: 🔍
  references:
    - references/directive-templates.md
    - references/strict-classifier-patterns.md
    - references/identity-inflation-rules.md
    - references/hermes-repo-entropy-pattern.md
    - references/context-geometry-audit.md
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# arif-style-zen-audit

Constitutional audit pattern forged from the 2026-08-10 ZEN audit session with Arif Fazil (F13 SOVEREIGN). This is the class of work Arif calls "audit", "purge", "scan drift", "verify identity", "trace counts", or "validate state". The pattern emerged from a multi-loop session where Arif repeatedly corrected overclaim patterns until the report was epistemically sound.

## When to use

Use this skill when the user asks for any of:
- Constitutional / ZEN audit of Hermes or federation state
- Context geometry audit — semantic overlap across AGENTS.md / CLAUDE.md /
  instruction fragments / SOUL.md / memory stores ("update and zen context
  files", "context jadi blob", orthogonal-axis restore)
- Skill commons inventory, dedup, or purge scan
- Drift detection (authority / execution / model-coupling / BANGANG)
- Identity verification (e.g. "is Hermes actually META_ORGAN?")
- Count reconciliation (e.g. "you said 424 skills — where?")
- Capability / tool discoverability audit
- QQQ ontology mapping proposal
- Anything producing a "gate map" with verified / false-positive / unresolved / blocked states

Do NOT use for: ad-hoc questions, deployment ops (use `arifos-deployment` family), code review (use `code-review`).

## Core epistemic standards (binding)

These are not suggestions — they are the standards Arif enforces. Violate any of them and the audit is rejected.

1. **No inflated completion %.** Use `PARTIAL_UNQUANTIFIED` over `85%`. Numeric percentages give false precision.

2. **No "sealed" claims for local files.** A receipt in `/root/forge_work/.../RECEIPT.md` is `LOCAL_UNSEALED_EVIDENCE` UNLESS `forge_vault(mode="seal")` (or `arif_seal`) returns a valid VAULT999 receipt ID. Do not collapse "I wrote a file" into "I sealed".

3. **No "0 drift" corpus-wide without 5-class classifier + full corpus scan.** A 4-spot-check finding is sample-only, not corpus-wide.

4. **No identity inflation.** Runtime identity is canonical (per `SOUL.md`, `INIT_HERMES.md`, `topology.md`, `emd-architecture.md`). Directive-only aspirational roles (e.g., META_ORGAN) are NOT runtime-effective until fragment + re-render + verify. Never rename `SOUL.md` to claim a role whose minimum_contract isn't implemented.

5. **No inference-based resolution of UNTRACED claims.** If a count like "424 skills" has no source-of-truth declaration, label it `UNTRACED` — do not collapse into a scope hypothesis that wasn't verified.

6. **Exact provenance per denominator.** Before any percentage claim, record: command, root path, depth, file pattern, inclusion/exclusion rules, symlink handling, deduplication rule, timestamp.

7. **5-class strict classifier for drift/bangang scans:**
   - `direct_violation` — imperative form, no negation/delegation
   - `diagnostic_reference` — audit/check/detect/scan pattern
   - `quoted_example` — quoted, blockquoted, anti-marker, or `> - * •`
   - `allowed_governance_delegation` — routes to apex/arif_judge/arif_seal/sovereign/888/F13/arifos
   - `allowed_execution_delegation` — routes to aforge/forge_/A-FORGE/forge_shell
   - `ambiguous` — cannot determine

8. **Pattern density ≠ violation rate.** "26% of files match 'ask user'" is density, not violation count. Reclassify to direct_violation after context reading, then report.

9. **Phased serial bounded loops.** Explicit `max_passes`. No unbounded "loop forever". One pass, one verify, then next.

10. **Review-before-apply for non-trivial mutations.** Show patch in chat, await "apply"/"go". Offer Option 1/2/3 (apply/review/hold). "Push seal ja la" is F13 override.

11. **"Doctrine exists, operationalization gap exists" > "we built it".** When canon/fragment declares X but runtime shows Y missing, name the gap, don't paper over it.

12. **Identity-effective role from runtime, not from directive.** If `SOUL.md` says EDGE_BRIDGE, that's the runtime identity. META_ORGAN in directive = aspirational until verified.

## Operating pattern (phased serial, bounded)

### PHASE 0 — Session integrity
- Try `arif_init` to mint valid SCT. If session is `guest_observe` with no SCT → continue read-only, label all receipts `LOCAL_UNSEALED_EVIDENCE`, never claim VAULT999 seal.
- Record: session_id, timestamp, active identity, source paths, corpus denominator, runtime harness, tool visibility.

### PHASE 1 — Reality inventory (denominators)
For every asserted count, record provenance:
- Command (exact)
- Root path
- Depth
- File pattern
- Inclusion/exclusion rule
- Symlink handling
- Deduplication rule
- Timestamp

Mark `UNTRACED` (not RESOLVED) if no source-of-truth found. Do not resolve by inference.

### PHASE 2 — Drift scan (if applicable)
Authority patterns: `approve`, `authorize`, `final_verdict`, `seal`.
Execution patterns: `deploy`, `write`, `modify`, `delete`, `commit`, `push`.
Run 5-class classifier. Report `direct_violation` count separately from total hits.

### PHASE 3 — BANGANG candidate adjudication (if applicable)
For each pattern-match candidate, READ full context (±5 lines). Re-classify. Most "ask user" matches are FALSE_POSITIVE in wizard-input contexts. Only report confirmed violations.

### PHASE 4 — QQQ dry-run (if applicable)
Keyword-inference classifier across all skills. Output categories:
- `high_confidence_proposal` (conf ≥ 0.7)
- `review_required` (0.4-0.7)
- `ambiguous` (0.2-0.4)
- `genuinely_unmapped` (< 0.2)

DO NOT write frontmatter in audit phase. Output dry-run proposal only.

### PHASE 5 — Skill↔tool evidence map (if applicable)
Read-only in-memory map. Tools referenced per skill (explicit vs inferred). MCP server usage. NO registry artifact created — that's a mutation requiring sovereign ratification.

### PHASE 6 — Capability resolution (if applicable)
Diagnose incompatibility (transport mismatch, harness exclusion, tools empty). Design facade/adapter WITHOUT writing code. Document: transport assumptions, permissions, test plan, rollback path.

### PHASE 7 — Identity gap (if applicable)
Inspect runtime identity sources (SOUL.md, INIT_HERMES.md, topology.md, emd-architecture.md). Diagnose gap between runtime and aspirational. Recommend non-inflated target (e.g., META_OBSERVER_CANDIDATE) not META_ORGAN.

### PHASE 8 — Patch packets
For each verified defect or proposed change, build a minimal packet:
- packet_id
- finding_id (linked to phase)
- evidence (path to phase JSON)
- exact_file (target)
- unified_diff (proposed change)
- risk_class
- reversibility
- verification_test
- authority_required

NO mutation in audit phase. All packets await sovereign ratification.

## Stop conditions (any one)

- Canonical-source conflict survives re-probe → escalate with receipts
- Valid SCT unavailable when VAULT999 receipt is required → label LOCAL_UNSEALED_EVIDENCE
- Tool/runtime failure prevents evidence collection → report and halt
- Mutation boundary reached → escalate to F13
- All passes completed AND every finding has a state → emit gate map

## Final output: GATE_MAP

```yaml
HERMES_REALITY_GATE_MAP::v1.0

result: PARTIAL_UNQUANTIFIED
audit_completion: PARTIAL_UNQUANTIFIED
mutation_in_loop: false
receipt_type: LOCAL_UNSEALED_EVIDENCE

verified:
  - finding_1 (with evidence path)
  - finding_2

false_positives:
  - false_signal_X_reclassified_after_context_reading

unresolved:
  - UNTRACED_claim_1
  - ambiguous_class_item_1

blocked:
  - VAULT999_seal_blocked_due_to_missing_SCT
  - any_mutation_blocked_by_authority_band

proposed_patch_packets:
  - PATCH-001: title (sovereign review required)

stop_conditions_met: true/false
```

## Anti-patterns to avoid

- ❌ End with `Jalan?`, `Proceed?`, `Should I?` — autonomous within authority
- ❌ "Confirm A?", "Confirm B?", "Confirm C?" — phased serial, show evidence, wait for review only on mutations
- ❌ Claiming "Hermes = META_ORGAN" without verifying runtime
- ❌ Inferred "scope hypothesis" as "resolved" — UNTRACED stays UNTRACED
- ❌ "5-10 true positives" without denominator — use stratified sample or full classification
- ❌ Logging "audit completion 85%" — false precision
- ❌ Calling local files "sealed" — LOCAL_UNSEALED_EVIDENCE unless forge_vault returns VAULT999 ID
- ❌ "Executing on corrected framing" before F13 explicitly signals "go" — see F13 Correction-Lock pattern below
- ❌ **Code-edit "wire-verified" without the wire response (scar 2026-08-19).** A prior session sealed "A-FORGE-MCP B complete on both code paths" — env var set, dist/ edited, wire-verified. Next session discovered all 6 hardcoded `"2025-11-25"` literals still in the dist code; the env was set but the code never read it; gate re-parked on every restart. The "wire-verified" claim was narrative, not witness. **Rule:** a "wire-verified" or "live-tested" seal MUST include the actual probe output (raw response, exit code, or file diff). Without the wire, it is an inflation — write the receipt as `WIRE_VERIFIED_PENDING` or `EDIT_APPLIED_NOT_VERIFIED`, never as `WIRE_VERIFIED_CLEAN`. See `live-probe-audit-pattern` § "Code-Edit Receipt Verification" for the 4-step probe recipe.

## F13 Correction-Lock Pattern (the "correction before executing" reflex)

### What it looks like (caught 2026-08-12)

When F13 says "correction before executing" — explicitly or implicitly, by pointing out
a doctrine violation, a hallucination, a fabrication, or an overclaim — the agent MUST
enter **lock-state** before doing any further work:

```
F13: "Gemini error: It says push to fix/allow-mcpjam-origin then..."
F13: "correction before executing."

Agent reflex (correct):
  1. Acknowledge correction received
  2. Lock execution gate — no file mutations, no remote calls, no registry writes
  3. Emit [🦾ACT] receipt: Action=HOLD execution; Proof=correction-received lock; W_scar=pending F13 directive
  4. Wait for explicit F13 authorization before resuming

Agent reflex (INCORRECT):
  - Continue executing the previous task assuming F13 will accept the correction retroactively
  - Start the next phase of work while the correction is still being metabolized
  - "Already did it, here's the result" — pastes the locked-out action as if the lock didn't exist
```

### The lock-state protocol (5-step)

When F13 issues a correction or a HOLD signal:

1. **Acknowledge** — emit `[🦾ACT] HOLD LOCK ACQUIRED: <correction-summary>`
2. **Inventory pending actions** — list every action queued or in-flight that might
   be affected by the correction
3. **Disable mutation paths** — explicitly state "execution gate locked" with the
   F13 reason; the substrate (Hermes, OpenClaw, etc.) should not pick up new
   `delegate_task` / `forge_shell` / `write_file` calls until released
4. **Wait for explicit release** — F13 must say "go", "proceed", or specific
   task authorization before the lock lifts
5. **Resume only on F13 signal** — re-emit `[🦾ACT] LOCK RELEASED: <reason>`

### Why this is its own pattern (not just H13)

H13 says: read-only + reversible + auditable + discoverable → execute autonomously.

F13 Correction-Lock says: when F13 has flagged an issue with the current direction,
**all bets are off** — even read-only work should pause until the correction is
acknowledged and the new direction is clear. The asymmetry: F13's attention is the
scarcest resource; if F13 is spending attention on correcting, the agent should
not be spending its own attention on continuing the previous direction.

### Detection rule (reflex-migration markers)

When F13 sends a correction, watch for these markers in your own next response:

- Continuing the previous task in the same message that acknowledges the correction
- Prefacing the correction acknowledgement with "Done. Now..." (signals no real
  lock occurred)
- Listing new actions to take before F13 has confirmed the new direction
- "I see — and here's what I'll do next" (this is a plan, not a lock)
- Treating the correction as informational rather than gating

If any of these appear, **the lock did not engage**. Re-emit the lock receipt and
wait.

### Failure consequence

Executing on corrected framing without explicit F13 release is an F13 SOVEREIGN
violation regardless of whether the new direction is correct. The agent is
substituting its own judgment for F13's veto — even if the substitution happens
to align with what F13 would have wanted. The form (sovereign acknowledgment)
matters as much as the content (correct direction).

### When this rule does NOT apply

- F13 asks a clarifying question (no correction embedded)
- F13 says "and also..." (extending the same task, not correcting it)
- F13 says "?" or "..." (seeking more info, not halting)
- F13 issues a T0/T1 directive that the agent can execute within H13 scope
  (H13 still applies; the lock pattern is only for correction-against-current-direction)

## Context Geometry Audit (semantic overlap across context files)

Use when drift is reported as "semantic overlap" / "context jadi blob" across
AGENTS.md, CLAUDE.md, AAA instruction fragments, SOUL.md, or memory stores.
Context is an orthogonal vector space, not files — each surface owns exactly
one axis (IDENTITY / LAW / MEMORY / INTENT / STATE / PROTOCOL). Overlap = debt.

Binding rules:
1. **One fact, one owner, one axis.** If a fact can be true from two files,
   one becomes a pointer or is deleted. Never fork the fact to "resolve" it.
2. **Fix pattern:** delete duplicate → leave pointer to canonical owner →
   forge new fragment if an axis is unnamed → wire into composer → re-render
   → verify rendered output.
3. **Never edit rendered files** (`/root/AGENTS.md`, `/root/CLAUDE.md`) —
   generated by `/root/scripts/render-agents.sh` from
   `/root/AAA/instructions/*.md`. Edit fragments + composer, then re-render.
4. **Memory stores obey the same axes.** Agent-memory duplicating USER-profile
   facts (identity axis) is the same overlap class — consolidate: identity in
   user store, ops intel in memory notes, pointer the rest.
5. Before declaring overlap, READ both surfaces and quote the duplicated
   content — snapshot claims of "potential overlap" are hypothesis, not finding.

Full axis table + render-wiring recipe: `references/context-geometry-audit.md`.

## HERMES repo commit-wave pattern (when audit reveals 300+ dirty files)

When the HERMES repo has massive uncommitted drift (common after multi-agent sessions), use the commit-wave technique:

1. **`git add -u`** — stages ALL tracked deletions + modifications in one go (skills migrated to AAA, config drift, cron runtime drift). Do NOT commit file-by-file.
2. **`git add -A`** — stages all untracked new files (new skills, references, archives)
3. **`.gitignore` hardening** — add runtime tmp files (`.gateway_state_*.tmp`, `.restart_notify.json`)
4. **Verify** — `git status --porcelain | wc -l` must be 0, `jobs.json` must be valid JSON

Batch by class: deletions first, new content second, residue third. Verify jobs.json integrity before any commit that includes cron changes.

For HERMES-specific entropy inventory (what to clean, what to keep, what to NEVER remove), see `references/hermes-repo-entropy-pattern.md`.

## VAULT999 seal fallback

If `arif_seal` MCP call times out on large payloads (5min cap), write directly to `/root/VAULT999/local_seals.jsonl` with the receipt JSON. The `seal_to_vault999.py` script may have broken imports — direct JSONL append is the reliable fallback. See `references/hermes-repo-entropy-pattern.md` for the recipe.

## Reference files

- `references/directive-templates.md` — common directive shapes Arif uses
- `references/strict-classifier-patterns.md` — full classifier code templates
- `references/identity-inflation-rules.md` — when to recommend META_OBSERVER_CANDIDATE vs META_ORGAN
- `references/hermes-repo-entropy-pattern.md` — HERMES-specific entropy inventory, commit-wave technique, seal fallback, mesh policy
- `references/context-geometry-audit.md` — orthogonal-axis audit recipe for semantic overlap across context files, composer wiring, memory-store consolidation
