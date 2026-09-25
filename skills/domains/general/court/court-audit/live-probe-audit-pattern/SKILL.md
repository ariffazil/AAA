---
name: live-probe-audit-pattern
description: "Probe claims against live system state — narrative-vs-state audit for multi-writer surfaces, deployments, agent reports, and SOT"
version: 2.0.0
owner: Hermes (arifOS federation)
risk_tier: low
floor_scope: [F2, F4, F7, F11]
autonomy_tier: T1
tags: [audit, probe, trust-but-verify, narrative-vs-state, multiwriter, concurrent-writes]
triggers:
  - "audit this"
  - "100% pass"
  - "zero dead links"
  - "EXECUTED, AUDITED & DEPLOYED"
  - "narrative claim"
  - "single source of truth"
  - "verify deployment"
  - "SOT audit"
  - "validate this claim"
  - "external audit"
  - "subagent"
  - "verify agent claims"
  - "cross-witness"
  - "convergence"
  - "audit claims against live"
  - "completion report"
  - "all gaps closed"
  - "is this alive"
  - "is this wired"
  - "existence check"
  - "capability metabolism"
  - "live audit"
  - "concurrent writers"
  - "queue backlog"
  - "duplicate counts"
  - "absence claim"
  - "how many skills"
  - "verify this report"
  - "second reader"
  - "peer report audit"
capability_tier: fed-long-context
ecology_state: WARM
---

# Live Probe Audit Pattern

> Merged from `live-probe-audit-pattern` v1 + `live-multiwriter-audit` v1.
> Session archaeology archived to `references/archive-*.md`.

## The Core Law

**Never trust the preamble, always probe the count.** Session-feed narratives that declare completion with confident numbers ("100% OK", "Zero dead links") are typically inflated 20-40% relative to reality. The audit is true at the instant you probe it — everything below keeps that instant honest.

## Step 0 — Classify the Report Type

| Report type | Falsifiable surface | Primary probes |
|---|---|---|
| **Deployment / hotfix** ("I changed X, now Y works") | Config files, mtimes, process env, live HTTP | `stat` mtime, `/proc/<pid>/environ`, `curl :port/health`, diff backup→current |
| **Spec / advisory** ("you should build X") | Citations + named estate files | curl each cited URL; `find`/`grep` each named file for existence AND depth |
| **Doctrine / synthesis** ("ratify this framework") | THIN — mostly prose | Audit only concrete anchors: do named patterns map to real findings? Are citations reused correctly? |

**Rule:** the more a report is wisdom-literature, the less there is to probe. Report the thin surface honestly.

## Step 1 — Multi-Writer Awareness

Any audit where the target is being written by other agents/cron/sessions requires:

1. **Enumerate scan surfaces before counting.** Mounts stack through symlinked paths:
```bash
for p in <path1> <path2> <path3>; do printf "%-42s " "$p"; readlink -f "$p"; done
find <store> -name '<artifact>' | wc -l  # raw — may double-count
```
Dedupe by resolved path — this is the only number worth quoting:
```python
seen = {}
for dp, dn, fn in os.walk(root, followlinks=True):
    if '<artifact>' in fn:
        seen[os.path.realpath(os.path.join(dp, '<artifact>'))] = dp
print(len(seen))
```

2. **Canonicalise queues before reporting depth.** Build identity key from row fields, count distinct keys:
```python
key = lambda r: (r.get('tool'), r.get('trigger'), r.get('action'))
print(len(rows), 'rows ->', len({key(r) for r in rows}), 'distinct findings')
```

3. **Stamp the window, re-probe before publishing.** For absence claims ("never wired", "does not exist"), run one fresh probe immediately before writing. Counts printed by producers are claims, not measurements — re-derive each number yourself.

4. **Check for a consumer before recommending a gate.** Name the process that drains every queue/ledger. A protocol with no runtime behind it is the worst shape: it reads as coverage while the fault runs unwatched. Report "doctrine present, executor absent" as the finding.

5. **Commit only into a quiet tree:**
```bash
find <dir> -newermt "-180 seconds" -type f ! -path "*__pycache__*"  # empty = quiescent
find <dir> -newermt "-6 minutes" -type f | head
ps -eo pid,etimes,cmd | grep -E 'hermes|kernel_runner' | grep -v grep
```
A second live session + a store `-wal` moved recently = **do not mutate** — hold and say so. Report an authorized-but-racy hold as a *timing* verdict, never as *awaiting human authority*.

6. **Record reversibility.** Move queued records into `processed-<label>/` rather than deleting; state the restore step.

## Step 2 — Probe Patterns

### Four-Surface Existence Scan (is there an X on this box?)

**Before ANY existence verdict, run all four surfaces:**
```bash
# 1. CONFIG / TOOLSET — what the framework has wired
hermes mcp 2>&1; grep -rniE 'mcp|server' /root/.hermes/config.yaml | head
# 2. FILESYSTEM — what exists on disk
find /root/.hermes /opt /root -path '*/mcp*' -name '*.py' 2>/dev/null | grep -v venv | head -20
# 3. PROCESS — what is running
ps aux | grep -iE 'mcp|arifos|geox|wealth|well' | grep -v grep
# 4. PORT — what is listening
ss -tlnp 2>/dev/null
```

**Key discriminators:**
- Toolset visibility ≠ existence (disabled in config ≠ dead)
- Answer "what is X" from the SCAN, never from prior
- Absence claim requires all four surfaces clean; presence needs only one

### Component Liveness (10-question probe)

For any subsystem claimed alive with impressive architecture:
1. Tool appears in live MCP surface? → `curl :port/tools`
2. Domain files real implementations or stubs? → `wc -l` each; check for logic vs print stubs
3. Sandbox/execution backend installed? → `which bwrap; bwrap --version`
4. Templates exist and usable? → grep registerBuiltinTemplates
5. Test coverage? → `find test/ -name "*<subsystem>*"`
6. **Any agent CONFIGURED to call this tool?** → grep configs (most commonly missed check)
7. Promotion gates mathematically reachable? → threshold vs default input values
8. Cross-module dependencies wired? → grep imports between modules
9. MCP transport network-reachable? → `ss -tlnp | grep <port>`
10. Full lifecycle ever exercised end-to-end? → search logs, VAULT999

**Three dormancy patterns:** No consumer (zero agent configs reference it), Dead gate (threshold unreachable by construction), Unwired module (file exists, engine doesn't import it).

**Verdict:** "Architecture REAL, operationally DORMANT" is a valid and common verdict. Report both halves honestly.

### Reproducible Probe Requirement

**An audit reporting concrete numbers WITHOUT a reproducible probe recipe is interpretation, not witness.** Before acting on any headline number, demand (or run yourself) the command that produces it. A reusable probe suite exists at `/root/AAA/audit/probes/probe_audit.py`.

**Live counts move between probes** — other organs/agents write concurrently. Timestamp every snapshot; never treat one probe as permanent.

### Cross-Witness Protocol (two agents, one truth)

1. **Extract all falsifiable claims** — numbers, boolean flags, severity labels. Ignore narrative.
2. **Probe each independently** — do not re-read the agent's probe output. Use your own tools.
3. **Classify:** ✅ Confirmed | ❌ False | ⚠️ Misread | 📊 Inflated
4. **Report convergence** — label with epistemic tags (OBS/INT/DER)
5. **Seal converged truth** — when two agents agree, append to VAULT999 naming both

**Convergence template:**
| Claim | Agent A | Agent B (witness) | Verdict |
|-------|---------|-------------------|---------|
| {claim} | {status} | {probe result} | ✅/❌/⚠️ |

**Pitfall:** Do NOT delegate cross-witness to a subagent. The cross-witness must be YOU probing live state.

## Step 3 — Specialized Audit Patterns

### Gap-Claim Audit ("you are missing X")

When an external advisor claims your estate is MISSING a control, probe for existing primitives FIRST. Advisors without filesystem visibility systematically overstate gaps. For each claimed gap: `grep -rl` the estate. If a primitive exists, the gap is "not wired into THIS workflow" (smaller finding), not "absent".

### Invariant-Preservation Audit ("zero information loss")

Compressible vs invariant: every system has content that MAY be reduced and content that MUST NEVER be compressed away. A "zero loss" claim is FALSE the moment any invariant-class item is absent.

Probe on the GENERATED artifact:
```bash
grep -E '^\| F[0-9]+' /tmp/boot_test.md | awk '{print $2}' | tr '\n' ' '
# Compare against canonical floor list — any missing floor = constitutional amnesia
```

### Unification / Canonicalization Receipt Audit ("one source of truth")

Four specific failure modes:
1. **Inverted canonicality** — claimed source is itself symlinks into another store
2. **Dead-lane residue** — verified against live home while dead home holds stale flood
3. **Divergence direction** — copies NEWER than canonical = active precedence drift
4. **Non-reproducible counts** — headline number matches no surface

### Hash-Chain Integrity (lineage-aware)

Before accepting "X% of links fail": count `prev_hash` value distribution first. A large fraction equal to GENESIS/None = many parallel lineages, not breakage. Compare in chain order, not file order.

### Autonomous Deployment Verification

Probe autonomous-specific surfaces directly:
```bash
curl -s http://127.0.0.1:7073/health | python3 -c "
import json,sys; d=json.load(sys.stdin); fq=d.get('fq',{})
print(f'FQ: {fq.get(\"quotient\",\"?\")} ({fq.get(\"verdict\",\"?\")})')"
```

### Config/Env Wiring Claim Verification

**Key rule: process env is the truth, not the SOT file.**
```bash
PID=$(systemctl show <unit> -p MainPID --value)
tr '\0' '\n' < /proc/$PID/environ | grep KEY
```
Key in file ≠ key in process env. Models-list 200 ≠ chat-completions OK — test the exact operation claimed.

### Agent-Card Federation Alignment Audit

7 dimensions to probe: skill references, MCP tool lists, organ coverage, intelligence tier, A2A contract bindings, floor bindings, schema compliance. Full probe recipe in archived references.

## Step 4 — Multi-Writer Pitfalls

### Patching a File a Sibling Is Editing

When a tool warns the file was modified since your last read:
1. Take your own named backup before any patch
2. Re-read the file, diff against backup to see sibling's changes
3. Re-apply only your hunk, anchored on untouched text
4. Verify the sibling's premise before deferring to their value
5. Re-read before concluding, cite the revision (`sha256sum` / `stat -c %y`)

**A test that mutates live state must restore the pre-image, verified.**

### Auditing the Detector Itself

Detectors fail in two symmetric directions: **silent false-PASS** (never fires) and **latent false-FAIL** (fires wrongly on input changes).

Key rules:
- A marker probe can pass on the echo of its own request — strip request lines before matching
- After editing a predicate, re-run BOTH must-trip and must-not-trip controls
- A check that has never fired is not evidence — plant fixtures to prove it discriminates
- Validate schedule parsers against hand-computed windows
- Compare like units across thresholds
- An unwired test is prose in a .py file — wire it into the periodic runner

### Running the Same Task Twice

Lock on the target, not the caller. Cache successful results. Read a mismatch as evidence of the race, not flakiness.

### Before Creating a Doctrine or Skill

Two sessions handed the same directive will each mint the artifact. Cheap pre-flight:
```bash
find /root/AAA/skills /root/AAA/instructions -name '*.md' -newermt '-30 minutes'
```
The curator daemon is a third writer — it reconciles duplicates under you. After folding into a duplicate, re-verify both your content and every path the survivor cites.

### Cross-Plane Review of Governance Documents

Self-review of own plane's role is unreliable (same failure mode as defendant writing own charges). Mandatory: every role card in a multi-plane governance doc reviewed by an agent NOT owning that plane.

### Attribution in Concurrent Sessions

An external review of "what the agent said" samples one session from many. Match distinctive quantities against recent sessions before accepting or disputing. Split attribution from diagnosis — adopt the finding on independently verifiable evidence.

### Verifying a Peer's Correction Report

1. Re-derive every number on disk
2. Say which numbers you did not re-derive and why
3. Reconcile the peer's HOLD list against their own later sections
4. Compare producer snapshot refresh stamps to live readings
5. Write findings as addendum — never rewrite the peer's receipt
6. Resolve which repository a cited hash belongs to before calling it missing
7. A peer's figure matching yours is not corroboration until you know both denominators

## Always-On Rules

- Dedupe by realpath before quoting any count
- Queue of N rows may be one finding replicated N times — count distinct identity keys
- Every absence claim carries its observation window; append AMENDMENT when reality moves
- Unconsumed queue ≠ gate, it's an accumulation
- Peer report = claim, not evidence: re-derive or mark inherited
- File transfer receipt (SCP exit 0, rsync exit 0) is transport receipt, not four-truth receipt
- Never commit mid-write
- Resolution artifacts are additive — never rewrite another lane's receipt
- Never read "no data" as "all clear"
- Never read exit status through a pipeline (`cmd | tail; echo $?` prints `tail`'s status)
- Never commit to a count that disagrees with the census until proven otherwise — re-run with `-L`, with `-name` filter, against the census
- **Vision-model audits can hallucinate bugs.** A vision report claiming "template overlap" or "truncated text" must be checked against the actual source (CSS, raw text, file size) before patching. "Fixing" a phantom bug is itself a defect — it adds entropy and pollutes the diff. Probe the source file the vision reported on; if the bug isn't there, log the false positive and move on.
- **A log is not a memory.** A `cycles.jsonl` accumulating N records has no memory until someone computes `f(today, t-N)`. Without a comparator, drift across days goes un-noticed even when the writes are honest. Every append-only log that claims to feed a learning loop needs at least one query path; if no consumer is wired, the log is archaeology.

- **A grep that excludes hidden/gitignored paths manufactures an absence claim.** A `search_files` (or `rg`/`grep`/`find`) run with default settings on a working tree that contains hidden directories (`.hermes/logs`, `.hermes/pastes`, `.git/objects`, `~/.cache/...`) will report zero matches for content that is actually present in those excluded trees — and the resulting "no record" verdict is the user's first read of the answer, not a second-order nuance. Treat every absence claim as null until the probe lists which surfaces it searched AND the writer could plausibly have written there. Specifically: before declaring a name, conversation, or fact "not present in the machine," probe (1) all hidden directories under the relevant root, (2) the paste / drop / cache / log folders the gateway actually writes to, and (3) any `.gitignored` paths the user might have authored privately. The probe that found nothing is not evidence of absence; it is evidence about the probe. The user has to nudge you to widen it — that is the reflex defect, not their instruction.
- **Idempotent writes + stable content-hash IDs close recursive writes.** Use `MERGE` (graph) or `INSERT ... ON CONFLICT DO NOTHING` (SQL) keyed by `sha256(content)[:8]`. This makes re-emission non-destructive and lets later runs query earlier ones by ID without schema join keys.

## Common Drift Patterns (compressed)

| Pattern | Tell | Fix |
|---------|------|-----|
| Caddy cross-root routing | File exists on disk, returns 404 | Reorder handlers in Caddyfile |
| Live-vs-disk byte delta behind CDN | ~1KB difference in `curl \| wc -c` | Diff before declaring corruption — CF injects ~938B |
| Cron telemetry with hardcoded values | Timestamp fresh, numbers never change | Read from sealed ground-truth file |
| Source vs webroot sync gap | Cron writes source, HTTP serves webroot | Dual-write to both paths |
| Pre-commit secret scanner hangs | Commit blocks on key pattern match | `git commit --no-verify` (emergency only) |

## Verdict Contract

- **Pass:** with evidence (probed URL + response code)
- **Fail:** with path + root cause (not just "404")
- **Partial:** with what's there + what's missing
- For each claim: state true status with epistemic tag (OBS = probe, INT = inferred, DER = derived)

## Constitutional Compliance

- F2 TRUTH: numbers live, derived labels per claim (OBS/INT/DER)
- F11 AUDIT: log to `forge_work/<date>/AUDIT-RECEIPT-<date>.md`
- F1 AMANAH: never fix web routing without F13 — log + flag, do not auto-deploy
- F7 HUMILITY: report honest numbers, not inflated

## Reference Files

Archived session archaeology and detailed worked examples in `references/`:
- `references/archive-session-specific-audits.md` — Reader-dormancy, hash-chain, invariant-preservation, env-wiring, agent-card alignment, cross-witness session, autonomous deployment, code-edit receipt, cron telemetry, and unification receipt worked examples
- `references/hermes-mcp-self-schema-drift-2026-09-25.md` — Three classes of single-surface MCP drift (resource description vs content, detector silent input loss, schema/validator mismatch) with the probe order that surfaces all three
- `references/reality-first-gap-repair-receipt.md` — Receipt shape for sealing a multi-gap repair on a running cron/organ. Five-question format; anti-patterns.
- `references/readiness-cockpit-receipt.md` — Hermes *self-readiness* pattern: when an audit target is the agent itself, swap narration for live probes + SHA-sealed JSON artifact + grounded verdict band.

## Step 5 — Self-Readiness Cockpit (auditing the auditor)

When the audit target is **the agent or system that will produce the audit reply**, the audit cannot rely on the agent's own summary. Two external advisors running against a startup banner will conclude the system is unproven; the agent must *replace narration with runtime evidence*. Pattern:

1. **State the bounded scope first.** What you will NOT touch tonight (no banner replace, no MCP mutate, no token rotate, no A3 actions). The post-audit verdict cannot authorize scope that the audit itself excluded.
2. **Probe live state, not config state.** For every surface declared available, hit the *probe endpoint* (`*_health`, `*_status`, `*_stats`, `*_registry_status`) and capture `{state, evidence_class, timestamp}`. Treat config-without-probe as **declared, not live**.
3. **Distinguish banner, runtime, and intent.** A startup banner that shows "connecting" while `ps` shows the same daemon alive with weeks of uptime means the *banner lagged the runtime*. Report all three surfaces and label which one answered.
4. **Seal the artifact before rendering.** Persist a JSON receipt to a known path (`/root/.hermes/state/readiness/readiness-<ts>.json`), `sha256sum` it, and print the hash in the human-facing summary. The hash is what makes the verdict re-derivable later.
5. **State the verdict band explicitly.** Pick from {GREEN, AMBER-instrumented, AMBER-speculative, RED}; explain what would lift it. AMBER is a *disciplined state*, not a shame state — keep it that way by naming what evidence would move the needle.

### Pitfalls specific to self-audit

- **Multi-tool batch only works for connector tools.** Local tools (`terminal`, `patch`, `read_file`, etc.) and any mixed batch with both local and connector tools are **rejected at runtime**. Serialize local calls; batch only connectors when the target tool description confirms the batch is supported.
- **`tool_call` runtime behaves as one-entry-per-call even for connector-only batches.** When invoking MCP tools through the deferred `tool_call` interface, a batch of multiple `mcp__*` entries fails with `Local tools require one entry per tool_call; mixed and multi-local batches are not supported.` — even when every entry is a connector. The schema permits batching; the runtime does not honour it. Probe the connector tool description for batch support BEFORE serialising calls in a loop, or budget for one call per turn and surface the cost in the deliverable. Three retries with the same payload will not unstick it — split the batch.
- **A blocked-by-design probe is a passing finding.** If a Postgres MCP returns `DB_PASSWORD required`, that is the boundary enforcing correctly. Report state=`GATED-CORRECTLY` and evidence_class=`boundary_test`, not `DOWN`.
- **Status fields can lie about enforcement.** A green `/health` does not prove enforcement (see `live-system-investigation` §"the inverse shape"). For governance claims, demand a deliberate negative test (`A3 action without F13 → must HOLD`); absence of the test is the gap, not absence of enforcement.
- **Disabled ≠ defective, but disabled needs declared rationale.** Each disabled surface must carry owner, rationale, compensating control, risk-acceptance date, and re-enable runbook. Empty disabled surfaces are silent governance debt.
- **AIMC counts are claims until re-derived.** When a system reports "MCPs live: 25/29", treat the numerator and denominator independently — re-derive both via probe, not via config file.
- **Heuristic-uncalibrated is honest governance, not absence.** A `g`-dimension band like `PATHOLOGICAL h=0.47 PHASE_1_HEURISTIC_UNCALIBRATED` is the *audit instrument admitting it is not yet trustworthy* — that is the right shape for a probe that needs human review. Do not collapse it into PASS.

### Verdict band discipline

- **GREEN** only when both live probes AND gate tests (deliberate blocked A3) produce receipts in this session, AND TEVV has at least one full pass/fail baseline.
- **AMBER-instrumented** when live probes confirm runtime activity but gate tests / TEVV remain pending. Acceptable overnight.
- **AMBER-speculative** when only the banner or config answered. Treat as a "do not act on this" signal until instrumented.
- **RED** when live probes return errors AND the boundary test fails. Immediate HOLD.

A useful self-readiness cockpit:

```text
HERMES READINESS · <ts> +08
Evidence mode: LIVE-PROBE / READ-ONLY · Core: <commit> (+N carried)
Policy gateway: <kernel> · state=<ENFORCED|UNKNOWN>
MCP mesh: <a>/<b> live · <c> disabled-intentional · <d> remaining
Write authority: F13-BOUND · enforcement_evidence=<structural|live_test|p>
Audit chain: <ledger state> · last_seal=<id>
TEVV: corpus=<n> · executed=<n> · baseline=<UNKNOWN|READY>
Verdict: <GREEN|AMBER-instrumented|AMBER-speculative|RED> · <one-line basis>
Artifact: <path> · SHA-256: <hex>
```

The artifact path + SHA are the contract: future sessions can re-probe the same surfaces and re-derive the verdict without trusting this one.
