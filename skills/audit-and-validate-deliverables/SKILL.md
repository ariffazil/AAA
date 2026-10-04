---
name: audit-and-validate-deliverables
description: "Independent audit + validation pattern for any produced artifacts (audit reports, code reviews, research, agent outputs). Author-and-audit pattern with adversarial posture, claim-by-claim evidence matrix, witness disagreement preserved. NOT for greenfield work — the artifact must already exist. Use when: a sibling/worker/session produced deliverables that need signed-off verification; you just executed a multi-phase task and need to verify your own claims before sealing; a user explicitly asks for verification/audit/validation. Distinct from requesting-code-review (which is pre-commit) and systematic-debugging (which is for runtime bugs). This is for *deliverables*."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [audit, validation, verification, governance, arifos, F2, F11]
---

# Audit & Validate Deliverables

> **Doctrine:** "Do not trust summaries. Do not trust receipts. Do not trust prior verdicts. Verify independently."
> **From:** Verified 2026-08-07 Multimodal Memory Audit (MMA-2026-08-07) — 9 deliverables, 2,160 lines, 88.5% verified claims, 0 fabrications.
> **Follow-up:** Session MMA-2026-08-07-FINAL (same date) — added seal hash-drift quarantine pattern; 2 corrections downgraded from prior audit (Graphiti timeout claim, 877 records); 22.5h quick-win total recalibrated, not 24.5h.

## When to use this skill

- **A sibling/worker produced deliverables** and you need to gate them before SEAL.
- **You authored a multi-phase artifact** and want to catch your own errors before the user spots them.
- **A user explicitly asks:** "verify this," "audit this," "check this work," "are you sure?," "darimana you know?."
- **Before issuing any SEAL verdict** on research, analysis, or documentation.

**When NOT to use:**
- Pre-commit code review (use `requesting-code-review`).
- Runtime bug hunting (use `systematic-debugging`).
- Greenfield code authoring (just write the code).
- One-line summaries or trivial verifications.

## The 7-phase audit framework

### Phase 0 — Assume Nothing

Treat every reported output as a claim. Examples:
- "42 components documented"
- "38945 events sealed"
- "schema compiles"
- "Graphiti schema is ready"

All are claims until verified. The author may have been wrong, may have rounded, may have inherited trust from a worker session.

### Phase 1 — Artifact validation

Verify:
- Directory exists
- Files exist (with expected count)
- Line counts match claims
- File sizes plausible
- Hashes generated (md5sum)
- Timestamps recorded

```bash
DIR="/path/to/audit/target"
ls -la "$DIR"
wc -l "$DIR"/*.md
md5sum "$DIR"/*.md
```

Output as YAML:
```yaml
artifact_validation:
  pass: [...]
  fail: [...]
  warnings: [...]
```

### Phase 2 — Deliverable quality review

For each deliverable, check:
- **Components actually exist** (probed, not just cited)
- **Connections are real** (file:line trace)
- **No invented systems** (paths, services, counts)
- **No duplicate inventory** (counting frame consistency)
- **Transformations accurate** (loss analysis reasonable)
- **Every gap supported by evidence**
- **Confidence labels honest** (V-claim / D-claim / C-claim / U-claim)
- **Schema claims true** (does it compile? does it validate?)
- **No circular scoring** (confidence inputs independent of outputs)
- **No hidden prerequisites** (dependencies explicit)

### Phase 3 — Evidence audit

For every major finding, log:
- **Finding** (one sentence)
- **Supporting evidence** (file/probe)
- **Evidence location** (file:line or URL)
- **Confidence** (HIGH / MEDIUM / LOW)

No evidence → DOWNGRADE CONFIDENCE. Repeated claims without evidence → REJECT.

### Phase 4 — Independent re-probe

Re-run a 20% random sample of the original probes. Compare to audit's stated values. Measure agreement rate.

```yaml
re_probe_sample:
  - finding: F1
    re_probe_result: confirmed
    match: true
  ...
agreement_rate: 5/5 = 100%
```

### Phase 5 — Hallucination audit

Search specifically for:
- Invented files
- Invented counts
- Invented services
- Invented paths
- Invented conclusions

Report:
```yaml
hallucination_risk:
  none | low | medium | high
```

### Phase 6 — Seal review

Evaluate on five axes:
```yaml
factual_correctness:
evidence_quality:
reproducibility:
operational_usefulness:
migration_safety:
```

Issue ONE verdict:
- **SEAL** — verified, ready for sovereign approval
- **PARTIAL** — conditions specified, can upgrade to SEAL after fixed
- **HOLD** — non-trivial gaps; needs sovereign decision before upgrade
- **VOID** — fabrications, contradictions, or unsafe to proceed

## The "author-and-audit" pattern (self-audit)

When you've authored the deliverables yourself, you CAN still audit — but flag the bounded independence:

```yaml
auditor_independence: MEDIUM (same-author self-audit)
mitigation: recommend second-pass by different agent (OpenClaw, OpenCode)
```

**Adversarial posture:** treat every claim you wrote as if a critic will dissect it. This catches real failures:
- Drift between probe and write (count snapshots)
- Framing errors (proposal called "schema")
- Inherited trust on worker-produced deliverables
- Missing required final outputs (SUMMARY.md, etc.)

## Evidence classification scheme

Use a 4-class taxonomy for every claim:

| Class | Definition | Example |
|---|---|---|
| **V-claim** | Verified live during this audit | "10 organs healthy on :port/health" |
| **D-claim** | Logical inference from verified findings | "Affective layer declared but not implemented" |
| **C-claim** | Cited file:line reference (not independently probed) | "WELL valid_modes at tools_sot.yaml:23" |
| **U-claim** | Unverified — made but not probed | "faster-whisper ~500MB RAM" |

Track each in an evidence matrix:
```yaml
claims_total: 61
verified_high: 53 (87%)
drifted: 1 (1.6%)
inferred_med: 7 (11.5%)
rejected: 1 (1.6%)
fabricated: 0 (0%)
audit_grade: B+ # strong; one framing failure
```

## Required output format

For every audit pass, produce THREE artifacts:

1. **`07_validation_report.md`** — Phase 1-2 quality review + verified/claims
2. **`08_evidence_matrix.md`** — Phase 3-5 claim-by-claim matrix
3. **`09_seal_review.md`** — Phase 6 final verdict with upgrade conditions

If the audited deliverable set is missing anything the original mission required (e.g. SUMMARY.md), write it as part of the seal review pass. **Never SEAl an incomplete deliverable set.**

## Pitfalls (verified 2026-08-07)

- **Inherited trust on worker-produced files.** When a sibling or OpenCode worker produced a deliverable then was killed, the surviving artifact is *yours to audit*, not yours to trust. Always re-read and re-probe.
- **Trusting a sibling/EMD audit's specific causal attribution without re-verifying (verified 2026-08-07, three separate incidents in one session).** Sibling audit reports contain TRUE structural observations AND FALSE causal claims mixed together. The audit may correctly identify a 15 KB live page exists at `/world/makcikgpt/` but incorrectly attribute its absence-from-disk to "extraction failure" when the real mechanism is a Caddy UA matcher routing bots to a different file. Or correctly identify `llms.txt` is accessible but incorrectly attribute a past failure to "robots.txt Disallow" when `robots.txt` actually has zero Disallow directives. Or correctly identify a dirty repo needs committing but incorrectly claim the Makefile has an F1 abort guard when it only *prints* status without exiting non-zero. **Discipline:** for every specific causal claim in a sibling/EMD audit, run the literal probe the audit claims to have run. Don't accept "the system already has guard X" without `grep` for X in the actual file. Three false attributions in one session is normal — the next audit will contain similar.
- **Drift between probe and write.** Live counts change (VAULT999 sealed events: 38945 then 38947). Snapshot at time of audit and note the drift.
- **Framing mistakes.** Calling a "schema proposal" a "schema" looks like a confidence claim but isn't. Rename/banner to make the actual claim visible.
- **Hallucination blindness.** When you wrote the audit, you remember your reasoning. The auditor doesn't. Probe every claim as if you didn't write it.
- **Same-author audit acceptance.** Self-audit is real work but bounded. Always recommend a second pass by a different agent for true independence.
- **Missing deliverables.** Missions often require SUMMARY.md, INDEX.md, or similar final-orientation artifacts. Phase 1's artifact count check catches this.
- **Documentation is a hypothesis, not evidence (verified 2026-08-08 / AAA-SESSION-20260808T0324Z).** When auditing a running federation, the canonical map (AGENTS.md, ORGAN.md, FEDERATION_MAP.md) is a *draft forecast*, not a record. AGENTS.md claimed FED was at `:7074`; reality is `:7074` (MCP) + `:4001` (clean proxy) + `:4000` (LiteLLM via Tailscale). Three different things, one name. The "kanon" was wrong about 30% of the substrate (SIGNAL :18084, FRAME :18085, FLAME's ADVISORY authority, FED's true port). **Discipline:** for any federation audit, `ss -tlnp` and `curl :PORT/health` first, doc reads second. The doc names *what was intended*; the runtime shows *what is*. Treat the gap as a finding, not an exception.
- **"Healthy" health response is not a verdict (verified 2026-08-08).** All 8 organs can report `status: healthy` and still the kernel reports `deployment_drift_status: drift_detected`. Read the `deployment_drift_status` field separately from `status`. The kernel can be "status: healthy + drift_detected" simultaneously. Same-shape pattern across all organs: `healthy` and `degraded` are different axes, not a single bit.
- **Don't tell a user about a system — show them (verified 2026-08-08, multiple incidents).** When bang asks "what is X?" or "list all Y?", the response is NOT a documentation summary. It is a live probe + receipt table. The contract: probe first → table → interpretation → verdict. If the response leads with "from the docs," the next session is dominated by a re-correction. The user's pattern is "show me, don't tell me about it." When the receipt is missing, say so explicitly — don't fall back to documentation as a substitute.
- **"Show me the SHA, don't summarize drift" (verified 2026-08-08).** When the user asks "is X consistent?", the right answer is `commit_a == commit_b` with the actual SHA printed. Not "consistent" — the SHA. Two sessions this year were spoiled by a sibling passing drift audits with "consistent" prose while the underlying hashes were in fact divergent. The pattern: sibling treats the audit as a narrative, not a receipt comparison. The audit gives the user nothing to verify. **Discipline:** every drift claim quotes the live SHA-256 (or short prefix). "Consistent" without SHA is a red flag.
- **AAA has 0 MCP tools but 38 A2A agents — say so directly (verified 2026-08-08).** When a probe shows zero tools, report "0 tools" — not "AAA *is* a registry" (interpretation). The count is the observation; the role is the interpretation. They must come in that order. Same pattern: AAA A2A traffic is near-zero, not "AAA is a directory service" — its A2A might pick up tomorrow. The probe is the ground truth; the role is the conclusion drawn from it.
- **MCP session requirement is server-specific (verified 2026-08-08).** Some servers (GEOX, WEALTH) accept bare `tools/list` after `initialize`. Others (arifOS, A-FORGE) require `Mcp-Session-Id` header for the next call. Some require `Accept: application/json, text/event-stream`. The probe must enumerate these — first call 406, second call 200 is normal, NOT a server bug. The recipe: `curl -si` to capture the response headers (look for `mcp-session-id` or `Mcp-Session-Id`), then pass that header in subsequent calls. Document the recipe in the audit output so the next session can repeat without re-discovering.
- **Stale prior-seal claims (MMA-2026-08-07 incident).** The audit corpus may already contain a prior seal that *looks* valid. Always re-run SHA256 on the current disk artifacts and compare against the sealed hashes. If a sibling subagent (or another terminal command) modified the deliverable files between the seal moment and the audit, the sealed hashes will no longer match — the seal is broken even if the file looks good. Treat broken-seal as a verifiable condition, not a failure of faith. The recovery: quarantine the prior seal, write a self-correction entry to VAULT999, re-seal against current artifact state with the corrected hashes. See `references/seal-hash-drift-quarantine.md`.
- **Self-SEAL violates HEXAGON separation of powers (verified 2026-08-08).** When the same agent authors the doctrines AND issues the SEAL verdict AND forges the audit document, six of the seven HEXAGON pipeline steps (AGI_PROPOSE → ASI_REVIEW → APEX_JUDGE → AFORGE_EXECUTE → ASI.AUDIT → APEX_RESOLVE → VAULT_RECEIPT) collapse into one actor. This is a Gödel-lock at the meta-level — the forger judges itself. Detection: check whether the audit's `VERDICT: SEAL` line was issued by the same agent that wrote the content. If yes, override to SABAR. Recovery: require 555-ASI.REVIEW (separate context, blind to forger's narrative) + 888-APEX formal verdict (not self-judgment). The doc may still be correct — the verdict label is wrong, not the content. Pattern: the doc is honest about its gaps but wrong about its own verdict. Accept the findings, override the seal. See `references/self-seal-godel-lock-pattern.md`.
- **PDF claims require SHA-256 hash verification before acceptance (verified 2026-08-08).** When an agent sends a sealed PDF with stated SHA256 hashes, extract the text (`pdftotext`), then independently verify every hash claim against live file digests (`sha256sum`). All claims must match. This catches: stale hashes from prior sessions, fabricated hashes from hallucinating agents, file mutations between seal and audit. Pattern: `[hash_prefix]…` in the doc → `sha256sum` on live file → first 8 chars must match. Pattern also works for in-repo doc claims (EUREKA §11, six-plane amendments) — verify the SHA prefix shown in the citation against the live git blob hash.
- **Concurrent sibling overwrite (MMA-2026-08-07 incident).** When two `opencode run` invocations (or a subagent + your write) target the same output directory, the second overwrites the first. The `write_file` tool's "modified by sibling subagent '…', but this agent never read it" warning is the tell. If you see it, do NOT proceed with the seal — re-hash, re-seal, and treat the prior seal as quarantined regardless of how recently it was issued.
- **SCOUT/Critic/Synthesizer delegation: structural validation pass ≠ content verification (verified 2026-08-12, federated research session).** A `delegate_task` worker that returns YAML validated by an ad-hoc script ("12 required keys ✓, 4 parts × E/I/H/U ✓, 34 sources ✓, confidence ≤ 0.90 ✓") has passed **structural** validation only. The validator checked cardinality, key presence, and confidence bounds. It did NOT read the claims, verify the source URLs, or check whether the cited papers actually exist. A structural pass opens the door to content audit — it does not close it. **Discipline:** when a subagent returns `validation: passed` with no claims you've independently read, treat the structural pass as the START of the audit, not the end. Always spot-check 3-5 cited claims against live sources before treating the work as usable. Pattern recognition: if the subagent's summary says "X verified live by curl to arXiv" but you can't see the curls in the trajectory, the validation report is auto-generated summary, not evidence. **Anti-pattern:** reporting the work as "validated and complete" based on structural keys alone — this is the exact failure mode that lets hallucinated source citations propagate through downstream synthesis.
- **Worker "exit code 0" on bounded source-only task ≠ files written (verified 2026-08-12, OpenCode FED refactor session).** OpenCode returned exit code 0 after 14m of process activity. The process log showed 8 mutation attempts, 6 todos marked `[✓]`, and a structured "ARCHITECTURE: BLOCKED" report. Hard-state evidence (`git status --short` empty + `git ls-files --others --exclude-standard` empty + target file not on disk) proved ZERO files were written. The `[✓]` checkboxes were *declarations of intent*, not confirmed writes. The "exit 0" came from the report generation succeeding, not from any disk state change. **Discipline:** after every `opencode run` / `delegate_task` bounded task, run the THREE-PROBE disk verification BEFORE reporting completion: (a) `git status --short` in target repo, (b) `git ls-files --others --exclude-standard` for untracked files, (c) `stat <expected-output-path>` or `ls <expected-output-path>`. If all three are empty/negative, the task produced a *report* not an *artifact*. The session log can show happy-path process — process != outcome. **Anti-pattern:** trusting the worker's exit code or its own "[✓]" marks. Process success and state success are independent. The audit truth is what the disk shows, not what the worker says happened.
- **Field-values that won't fail anywhere (MMA-2026-08-07).** The `877 records` claim in the original audit's `06_upgrade_roadmap.md` was never probed end-to-end; it propagated through three places (T1.4 backfill, T1.5 quick-win, success condition). When you patch a numeric claim, `grep -n` the entire deliverable directory for the old value before signing off — same number, multiple locations.
- **GitHub `main` is protected by default on many repos (verified 2026-08-07).** A naive `git push origin main` will be rejected with `remote: error: GH006: Protected branch update failed`. The fix is `git checkout -b feat/...` → `git push -u origin feat/...` → open PR. Treat this as the standard publish workflow when the repo has branch protection enabled; don't waste a turn discovering it from the error message. Probe branch protection status before push: `gh api repos/:owner/:repo/branches/main/protection` returns the policy if it exists.
- **Discover live organs by live port scan, not by name roster (verified 2026-08-07).** When auditing "how many organs are running," an 8-port mental list will miss ports outside that canon (in one session, port 18085 — FRAME organ — was missing from every prose roster). The fix: `systemctl list-units --type=service --no-legend | grep -iE "arifos|arifflow|aforge|geox|wealth|well|aaa|hermes|caddy"` then probe each non-familiar port live. A single missing organ in the count is a higher-F2 failure than a wrong causal claim — you can't audit what you don't know exists.
- **Disk artifact ≠ effective served artifact (verified 2026-08-07, `/world/makcikgpt/` incident).** A 105-byte stub on disk at `/var/www/html/arif/<route>/index.html` may be served as a 15 KB file at `<route>/` because Caddy uses UA matching to route bots vs browsers to different roots. The live `curl -s https://.../route/ | wc -c` is the only ground truth. When a sibling audit reports "file missing or stubby" but the live response is full, the diagnosis is a routing layer (Caddy UA matcher, rewrite rule, `try_files` path), not a missing file. Always probe the live response before declaring a content gap.
- **Multi-schema JSONL audit trap (verified 2026-08-08, VAULT999 outcomes.jsonl 42K entries).** A large append-only file can carry 5+ distinct schemas in parallel — decision-ledger entries (`decision_id`+`session_id`+`verdict_issued`), tool-call entries (`event`+`ts`+`verdict`), chain-linked entries (`chain_hash`+`prev_hash`+`ts`), legacy entries (`timestamp` not `ts`), and genesis-anchored roots. Naively counting "entries missing field X" produces wildly inflated failure counts because entries in OTHER schemas don't have field X by design. In one probe, 30,000 entries were counted as "empty objects" when they were legitimate decision-ledger records with a different field set. **Discipline:** BEFORE clustering or counting failures, run a schema-distribution pass — group entries by their field-set tuple (`tuple(sorted(d.keys() & probe_fields))`) and enumerate every distinct schema. Analyze each schema independently. Inflated counts are harmless in a destructive audit context only by accident; they could trigger unnecessary quarantine or deletion. The recovery: re-read a few representative entries from each schema cluster before drawing conclusions.
- **Canonical verifier may be unwired from Makefile (verified 2026-08-08, `make vault999-verify`).** A Makefile target was calling `vault999_status.py` (a status reporter) instead of `verify_vault_chain.py` (the canonical chain-integrity checker with the structural-break logic at lines 288-294). "Chain healthy" was reported by a target that never ran the chain walk — unfalsifiable evidence. When an audit's evidence chain depends on a Makefile target, verify three things in order: (a) the target exists in the Makefile, (b) the script it invokes IS the canonical checker (not a stub or status reporter), (c) the script was actually invoked (use `make --trace` or `bash -x` to see the command run). Pattern: `grep -n <target> Makefile` → shows reporter script → canonical checker exists at a separate path but is not called → evidence was never actually produced. The fix is one line of Makefile: replace `python scripts/<reporter>.py` with `python scripts/<canonical-checker>.py`. Always re-run the target after the wiring fix to confirm the canonical numbers.
- **Sibling agent "verified" claims need file-level re-probe (verified 2026-08-08, 9-ATLAS session).** When a sibling agent claims "X verified" or "Y applied," do NOT trust the claim. Probe each named file at the path cited. In one session, a sibling claimed `opencode.json` had `priority: PRIMARY` and `replaces: [codex, claude-code]` — both fields were absent from the actual file. The sibling had confused intention with completion. In the same session, a sibling claimed AGENTS.md was "rendered with all changes" — `git log` showed the last render was 5 days stale; the fragment was staged but the render never ran. **Discipline:** for every "verified" or "applied" claim, (a) read the file at the cited path with `grep` for the cited field, (b) cross-check timestamps against the claim ("rendered today" → `git log -1` should match today), (c) if the claim is about render/sync/deploy, run the actual render/sync/deploy command and re-probe. Sibling "verified" without independent re-probe is a top-3 audit failure mode.

## The Pre-Seal Gate (MANDATORY before any SEAL)

**Origin:** MMA-2026-08-07 incident — seal issued at 11:35Z, sibling subagent overwrote files at 11:42Z, seal broken without anyone noticing until re-probe.

Before issuing ANY seal verdict, ALL of these must pass:

| # | Check | How to verify | Fail → |
|---|-------|---------------|--------|
| 1 | `artifact_hash_matches` | `sha256sum` current disk files, compare to seal candidate hashes | Quarantine prior seal |
| 2 | `artifact_name_matches` | File names in seal match file names on disk | Quarantine |
| 3 | `artifact_count_matches` | Expected deliverable count on disk | Quarantine |
| 4 | `no_sibling_overwrite` | No `write_file` sibling warnings since last read | Re-read + re-hash |
| 5 | `known_wrong_values_absent` | `grep -rn` old bad values; only correction-note references allowed | Patch + re-hash |
| 6 | `correction_provenance_recorded` | If any patch applied, header has "Corrected YYYY-MM-DD by..." | Add note |

```yaml
pre_seal_gate:
  artifact_hash_matches: true
  artifact_name_matches: true
  artifact_count_matches: true
  no_sibling_overwrite: true
  known_wrong_values_absent: true
  correction_provenance_recorded: true
  verdict: PASS  # or QUARANTINE + list failures
```

**If any gate fails → QUARANTINE, not VOID.** The work may be correct; the seal just cannot be trusted until re-verified. Recovery: quarantine prior seal → fix → re-hash → re-seal.

## The "three upgrade conditions" pattern

When issuing HOLD, specify the upgrade conditions:
```yaml
hold_reasons:
  1. Missing deliverable X
  2. Framing error Y
  3. Same-author audit, recommends second pass

upgrade_to_seal_conditions:
  1. Produce X
  2. Fix Y
  3. Sovereign review (Arif)
  4. (Optional) Independent second pass
```

This makes the path forward explicit. The user knows exactly what they need to do.

## Output attestation — attest BEFORE delivery, verify AFTER (2026-08-09)

**The failure mode this stops:** agents fabricate crypto-looking text on real-world
outputs (PDFs, emails) without computing anything — e.g. a "Document Hash (SHA-256):
5334a3d6..." on a letter's last page where `sha256sum` on the actual file gives
`2f9ce700...` and VAULT999 has no seal entry. Audit proof: every claimed hash in the
doc fails `sha256sum`; zero `arif_seal`/`forge_vault` calls in logs; zero hash
computation in agent logs. Same Gödel class as fake "888-APEX JUDGMENT ✅ PASS" text
with no `arif_judge` tool call.

**The fix (production-side, not just audit-side):** attest every real-world output
BEFORE delivery, in a ledger, with a hash computed from the actual file.

| Script | What it does |
|---|---|
| `scripts/output-attest.py` | Compute SHA-256 of a file → append `{file_path, sha256, size, ts, agent_id}` to `/root/HERMES/attestation-ledger.jsonl` with `verbatim: true` |
| `scripts/output-verify.py` | Recompute SHA-256, compare against claimed hash AND ledger entry → verdict `VERIFIED` / `FABRICATED` / `COMPUTED` |
| `scripts/check-unattested-outputs.sh` | Cron watchdog (every 2h): find PDFs younger than N hours, auto-attest any without a ledger entry |

```bash
# Attest before sending any PDF/email to the real world:
python3 /root/HERMES/scripts/output-attest.py /tmp/surat-v3-attested.pdf --label "surat-v3" --agent "hermes"

# Anyone can verify later:
python3 /root/HERMES/scripts/output-verify.py <file> <claimed-hash>
# → VERIFIED or FABRICATED with first-divergence position
```

**Rules:**
- The attestation lives in the LEDGER, not as text inside the artifact. A hash printed
  inside a PDF is unverifiable decoration; a ledger entry with `verbatim: true` is proof.
  If the artifact template carries a "crypto signoff" page, replace the fake hash with a
  pointer: "attested in /root/HERMES/attestation-ledger.jsonl — verify with
  output-verify.py".
- Cron auto-attest is the anti-forget net: even if the agent skips attestation, the
  watchdog catches unattested PDFs within 2h and back-fills the ledger.
- Audit side: for any artifact claiming a hash, ALWAYS `sha256sum` the live file AND
  grep the ledger — both must match, else `FABRICATED`.

Details + session trace: `references/output-attestation-system-2026-08-09.md`,
`references/fake-hash-detection-2026-08-09.md`.

## Meta-Audit Rubric (F13 Sovereign — 2026-08-10)

When evaluating an audit's quality (NOT its agreement with doctrine), apply 5 tests:

| # | Test | Question |
|---|------|----------|
| 1 | **Reality Test** | Did the auditor discover something the current doctrine did NOT expect? |
| 2 | **Contradiction Test** | Did at least one assumption get weakened or falsified? |
| 3 | **Bridge Test** | Were integration nodes found via evidence, not analogy? |
| 4 | **Strawberry Test** | Were critical dependencies proven via code-path or runtime evidence? |
| 5 | **Unknown Test** | Did the auditor return UNKNOWN when evidence was insufficient? |

**Red Flags** (audit may be auditing narrative, not reality): everything SEAL, no contradiction, no UNKNOWN, no falsification.

**Green Flags** (audit is seeing the system, not the doctrine): unexpected dependency discovered, governance drift found, hidden bridge node identified, undocumented coupling revealed, assumption proven wrong.

**The One Question:** What was the most surprising discovery the auditor made that was NOT expected before the audit began? If the auditor can answer with evidence → audit is valuable. If not → may be restructuring what was already known.

**Transition Matrix:** Track per finding: BEFORE (audit) → AFTER (fix cycle). Target: FALSIFIED → WEAKENED → SUPPORTED. **Measure transitions, not bug counts.** This is the PRIMARY output of recursive improvement.

Source: `/root/forge_work/ariflow-audit/META_AUDIT_RUBRIC.md`

## Survivability audit — does the documentation transmit meaning? (2026-08-09)

**Trigger:** user asks whether docs/canon/site artifacts would survive the author's absence, or
asks to "test whether documents alone can teach a fresh agent." Distinct from the other phases:
this audits TRANSMISSIBILITY of documentation, not correctness of claims.

**Method (compact):**
1. Spawn a **zero-context** subagent (`delegate_task` leaf, no prior context). A federation
   resident (OpenClaw/555-ASI) is CONTAMINATED — its predictions are memory, not document
   fidelity. Only a fresh subagent measures the documents.
2. Inputs = ONLY the artifacts under test (explicit paths). Forbid terminal/network/web.
   "Answer UNKNOWN if not covered — never guess." UNKNOWN = "doc failed to teach this", honest data.
3. Predict (no probing): organs+ports, authority chain, gates, rules, purpose — each cited.
4. Grade vs live probes, pre-registered matrix, per category: correct/incorrect/missing/ambiguous.
5. Survival score 0-10 per transmission: Identity / Governance / Operational / World Model.

**Two-run design:** run with a broken/absent pointer AND with the real machine canon — the delta
isolates the value of each artifact (one run: soul-without-body; corrected run: skeleton+law).

**Core findings pattern:** transmission failures are POINTERS not content (broken symlink named
in the protocol; stale port measured twice in both README and machine canon); name ≠ content
(`canon/FEDERATION` doesn't exist, `canon/federation.json` does); oral tradition is measurable
(operational gates living only in AGENTS.md); tool-injected AGENTS.md context = accidental
side-channel that improves survival — flag it.

Full protocol + worked case: `references/survivability-audit-2026-08-09.md`

## Post-Commit Node Organ Audit

For auditing a Node organ repo (A-FORGE, AAA, APEX) after a feature commit —
checking git status, test regressions, ESM `.js` import hygiene, and TypeScript
errors — see `references/post-commit-node-organ-audit.md`. This is a lighter-weight
4-check pattern than the full 7-phase deliverable audit above, suited for the
"audit the repo after tonight's commit" class of task.

## References

- `references/mma-2026-08-07-evidence-matrix.md` — full evidence matrix from the 2026-08-07 memory audit (61 claims, 87% verified, 0 fabricated)
- `references/audit-checklist-template.md` — copy-paste Phase 1-6 checklist for any audit
- `references/seal-hash-drift-quarantine.md` — recovery pattern when sealed hashes no longer match disk artifacts (MMA-2026-08-07)
- `references/self-seal-godel-lock-pattern.md` — detection, override, and recovery for self-SEAL violations (HEXAGON 5.0 separation of powers); 2026-08-08 case study
- `references/federation-architecture-audit-pattern.md` — federation-wide audit patterns (port scan, drift detection, doctrine verification)
- `references/vault999-chain-audit-2026-08-08.md` — VAULT999 ledger integrity findings (42K-entry multi-schema JSONL, canonical verifier unwired from Makefile, 18 JUDGE_SEAT_DEPUTY schema-bug entries, schema-distribution discipline)
- `references/post-commit-node-organ-audit.md` — lightweight 4-check pattern for auditing a Node organ repo after a feature commit (git status, npm test, ESM hygiene, tsc)
