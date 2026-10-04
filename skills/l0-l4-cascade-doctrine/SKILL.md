---
name: l0-l4-cascade-doctrine
description: "5-layer verification model for any arifOS claim. Tests: L0 (docs/specs), L1 (source code), L2 (runtime binary), L3 (operational behaviour), L4 (reality contact). Governs: audit verdicts, fix validation, constitutional claims. Trigger: any audit, verification, or claim validation mission. Created: 2026-08-10, Arif F13 sovereign directive."
tags: ["governance", "audit", "verification", "constitutional"]
related_skills: ["apex-judge", "audit-and-validate-deliverables", "arifos-federation-ops"]
---

# L0→L4 Cascade Doctrine

> **Invariant:** Every layer tends to replace the layer below it.
> **Governance:** Each layer must continuously pay epistemic debt to the layer beneath it.
> **Source:** ARIFOS::L0_L4_CASCADE::v1.0 — Arif F13 sovereign directive, 2026-08-10.

## The 5 Layers

| Layer | Name | What it captures | Verification method |
|-------|------|------------------|---------------------|
| **L0** | Representation | Docs, specs, claims, architecture diagrams | Read documentation, compare to code |
| **L1** | Source Code | What the code actually implements | `git diff`, `grep`, code reading |
| **L2** | Runtime Binary | What the compiled binary does | `sha25sum` binary, build verification |
| **L3** | Operational Behaviour | What agents/users actually experience | Live endpoint probes, client tests |
| **L4** | Reality Contact | What actually changes in the world | Full lifecycle replay, observable consequences |

## Core Rules

1. **Reality beats runtime.** Runtime beats code. Code beats docs. Docs never beat reality.
2. **No claim may skip layers.** A claim is not SEALED until reconciliation exists across all required layers.
3. **VALID is a lower bound. REALITY is the target.** Internal consistency ≠ truth.
4. **Report the first layer where evidence ends.** That is the highest proven layer.
5. **Unknowns are victories when honestly discovered.**

## The Cascade Problem

> Theory replaces data.
> Docs replace code.
> Code replaces runtime.
> Runtime replaces reality.

**Governance obligation:** Force the upper layers to keep paying debt to the lower layers. Every claim must be tested against each layer it passes through.

## Phase Structure

### Phase 1: L1↔L2 Reconciliation
- Clean build (`cargo clean && cargo build --release` or equivalent)
- Record: source commit, built binary hash, deployed binary hash
- Verify byte identity
- **Verdict:** SUPPORTED / WEAKENED / FALSIFIED / UNKNOWN

### Phase 2: L2↔L3 Reconciliation
- Re-test each finding against live daemon/endpoint
- Use valid inputs (correct formats, proper UUIDs, etc.)
- Do NOT inspect source code during verdict — observe runtime only
- **Verdict per finding:** SUPPORTED / WEAKENED / FALSIFIED / UNKNOWN

### Phase 3: L3↔L4 Reality Contact
- Replay one complete lifecycle
- Verify observable consequences: state changes, file growth, metric updates
- Confirm persistence: does the data survive restart?
- Confirm external observability: can other organs/agents see the change?
- No mocks. No synthetic success. No source-code reasoning.
- **Verdict:** SUPPORTED / WEAKENED / FALSIFIED / UNKNOWN

### Phase 4: Transition Matrix
- For each finding: Before (audit) → After (fix cycle)
- Track epistemic transitions: FALSIFIED → WEAKENED → SUPPORTED
- This is the PRIMARY output of recursive improvement
- **NOT bug count. Epistemic transition count.**

### Phase 5: Constitutional Verdict
- For each claim: highest layer reached with evidence
- Allowed verdicts: SEAL / PARTIAL / UNKNOWN / SABAR / HOLD / VOID
- SEAL requires ALL claims at L4 with evidence
- PARTIAL = some claims at L4, some at L3 or below

## Pitfalls

### UUID Strictness
arifFlow daemon requires strict UUID v4 format for `receipt_id` and `session_id`. Custom strings (e.g., "probe-fix-001", "l4-0001-0001-0001-000000000001") are rejected with `UUID parsing failed`. Always use `python3 -c "import uuid; print(uuid.uuid4())"` for probe receipt IDs.

### Missing Required Fields
arifFlow /ingest requires `cooling_decision` field in receipt JSON. Omitting it returns `missing field 'cooling_decision'`. Always include `"cooling_decision": "None"` in test receipts.

### vault999.rs API Mismatch
`Vault999Sealer::seal()` takes `checkpoint_hash: [u8; 32]`, NOT `&FlowReceipt`. The correct pattern: `receipt.hash()` → `hex::decode()` → `[u8; 32]` → `sealer.seal(checkpoint)`. Do not assume the sealer accepts receipt objects directly.

### Concurrent Agent Editing
Sibling agents may edit the same files concurrently. Before deploying:
1. Check `ps aux | grep opencode` for other active agents
2. Verify binary hash matches source build (sha256sum)
3. If concurrent edits detected, wait for sibling to finish, then re-verify

### Deployment Verification Pattern
Always verify deployed binary = built binary:
```bash
sha256sum target/release/arifflow  # built
sha256sum /opt/arifflow/bin/arifflow  # deployed
# These MUST match before restart
```

## Success Condition

At least one complete receipt lifecycle reaches L4 Reality Contact with evidence.
Failure is acceptable. Fabricated success is not.

## Example Usage

```
Reference: ARIFOS::L0_L4_CASCADE::v1.0
Mission: L0→L4 verification of arifFLOW findings
Phases: L1↔L2, L2↔L3, L3↔L4, Transition Matrix, Verdict
```

## Operational Audit Mechanics — multi-component repair verification (forged 2026-08-11)

The L0→L4 doctrine is the **philosophy** of verification. The mechanics below are the **operational recipe** for verifying a multi-component repair was done correctly. Distinct class of work from a single-claim audit — the repair spans multiple files, processes, and surface claims.

When Arif gives you a "summary" or "report" of work done by another agent (often 333-AGI / opencode / sibling), this is the protocol. The summary has **claims** about files written, counts sealed, state transitioned. Your job is to **verify each claim independently** with live evidence, then issue a ΔS-revised verdict.

### The 5-table audit protocol

| # | What to verify | How | What it catches |
|---|---|---|---|
| 1 | **File existence** | `ls -la <path>` + `stat <path>` for mtime/size | Claimed files don't exist; wrong paths; wrong permissions |
| 2 | **File content claims** | `grep -c` + `grep -oE` for specific markers in claimed files | File exists but content doesn't match claim |
| 3 | **Schema validation** | `python3 -c "import json; ..."` for JSON shape, `caddy adapt --pretty` for Caddy chains | Schema drift; unexpected fields; broken handler chains |
| 4 | **Live state vs claims** | `curl -sL` for HTTP surfaces, `wc -l` for VAULT999, direct process probes for cron/services | Stale data; dead services; missing wired routes |
| 5 | **Reversibility (F1 AMANAH)** | Verify backup files exist (`jobs.json.bak-<TS>` etc.) + reversal command is documented + all referenced files in reversal command exist on disk | Hidden irreversible changes; orphan state; undocumented mutations |

### The audit table format (use this in your response)

```
| Claim | Evidence | Verdict |
|---|---|---|
| "5 digests refreshed at 12:37 UTC" | `stat <file>` shows mtime 12:37:09 ✓ | ✅ Verified |
| "2 jobs swapped to minimax" | jobs.json shows 2 provider_swap_note ✓ | ✅ Verified |
| "PATCH-8ab448 verified by tag-check" | 0 references in jobs.json or backup | ⚠️ Ambiguous |
```

✅ Verified = claim matches evidence exactly.
⚠️ Ambiguous = claim partially verifiable, gap noted.
❌ Mismatch = evidence contradicts claim — push back.

### Operational audit patterns from real audits

#### 1. Market data freshness audit (F2 TRUTH)

When a sibling claims "digests refreshed", verify:

```bash
# 1. File existence + mtime
for asset in gold oil gas klci usdmyr; do
  f="/var/www/html/arif/data/markets/${asset}_digest.json"
  stat -c "%n | mtime=%y | size=%s" "$f"
done
# All mtimes should be within the claimed refresh window

# 2. Price claims match digest content
for asset in gold oil gas klci usdmyr; do
  f="/var/www/html/arif/data/markets/${asset}_digest.json"
  python3 -c "
import json
d = json.load(open('$f'))
print(f'$asset: {d[\"one_liner\"][\"en\"]}')  # e.g. 'Gold at 4,449.20 ...'
print(f'  observed_at: {d[\"seal\"][\"observed_at\"]}')
print(f'  coherence_id: {d[\"seal\"][\"coherence_id\"][:16]}...')
"
done
# Compare digest `one_liner` text to the claimed prices — EXACT match required
```

The digest schema has nested structure — don't grep for `price:` flat. The `seal.observed_at` tells you WHEN it was refreshed; the `one_liner.en` is the human-readable price claim.

#### 2. Cron registration audit

When a sibling claims "registered /etc/cron.d/<job>", verify:

```bash
# 1. File exists with correct ownership
ls -la /etc/cron.d/<job-name>  # mode 644, owner root:root
# 2. Schedule matches claim (weekdays/weekends, frequency)
grep -E '^[0-9*]+' /etc/cron.d/<job-name> | head -1
# 3. Locking — concurrent runs should use flock
grep -E 'flock' /etc/cron.d/<job-name>
# 4. Script exists + executable + correct interpreter
ls -la <script-path>  # -rwxr-xr-x
# 5. Log path exists (or will be created)
grep -oE '>> [^ ]+' /etc/cron.d/<job-name>
```

#### 3. jobs.json provider swap audit (Hermes cron)

The jobs.json schema separates CURRENT config from HISTORICAL config:

```python
# Schema:
#   model: <CURRENT model name>
#   provider: <CURRENT provider>
#   model_snapshot: <OLD model before swap>
#   provider_snapshot: <OLD provider before swap>
#   provider_swap_note: <human-readable audit trail>

# Verify a swap claim:
import json
d = json.load(open('/root/HERMES/cron/jobs.json'))
swapped = [j for j in d['jobs'] if j.get('provider_swap_note')]
print(f"Jobs with provider_swap_note: {len(swapped)}")
for j in swapped:
    print(f"  {j['name']}: was {j['provider_snapshot']}/{j['model_snapshot']} → now {j['provider']}/{j['model']}")
    print(f"    note: {j['provider_swap_note'][:100]}")
```

If the claim is "2 jobs swapped" but `len(swapped)` = 1 → ⚠️ Ambiguous (claim off by one).

#### 4. Live state verification

For F2 TRUTH, claims about live state (FQ, prices, VAULT999 line counts) MUST be probed fresh:

```bash
# FQ
curl -sf https://arif-fazil.com/999/flow | python3 -c "
import sys, json
d = json.load(sys.stdin)
fq = d['fq']
print(f'FQ: {fq[\"quotient\"]:.2f} {fq[\"verdict\"]} | exec={fq[\"execute_count\"]} verify={fq[\"verify_count\"]}')
"

# VAULT999
wc -l /root/arifOS/VAULT999/outcomes.jsonl
tail -1 /root/arifOS/VAULT999/outcomes.jsonl | python3 -c "
import sys, json
d = json.loads(sys.stdin.readline())
print(f'Last: ts={d.get(\"ts\",\"?\")[:19]} event={d.get(\"event\",\"?\")} actor={d.get(\"actor\",\"?\")}')
"

# Federation organs (all 9 should be 200)
for p in 8088 7071 7072 7073 3001 8081 18082 18083 18789; do
  printf "%5s %s\n" ":$p" "$(curl -sf -o /dev/null -w '%{http_code}' --max-time 3 http://127.0.0.1:$p/health)"
done
```

Compare the probed values to the claimed values EXACTLY. If `wc -l` says 47382 but claim says 47380 sealed, note "2 receipts sealed after the claim was made" — that's the chain still being alive.

#### 5. Reversibility audit (F1 AMANAH)

The MOST IMPORTANT step. For every claim of "I did X", verify the rollback path exists:

```bash
# 1. Backup file exists with the documented timestamp
TS="20260811T203847Z"  # from the claim
ls -la /root/forge_work/.../jobs.json.bak-$TS
# If missing → ⚠️ No rollback possible, F1 violated

# 2. All paths referenced in the reversal command exist
# Example reversal command:
#   cp /root/forge_work/.../jobs.json.bak-$TS /root/HERMES/cron/jobs.json
#   rm /etc/cron.d/trading-scan
#   rm /root/.local/share/arifos/state/retired-predictions-2026-08-11.json
#   /root/WEALTH/.venv/bin/python3 /root/WEALTH/trading/cron/refresh_market_digests.py
# Verify each:
for path in "/root/HERMES/cron/jobs.json" "/etc/cron.d/trading-scan" "/root/.local/share/arifos/state/retired-predictions-2026-08-11.json" "/root/WEALTH/trading/cron/refresh_market_digests.py"; do
  test -e "$path" && echo "  ✓ $path" || echo "  ❌ MISSING: $path"
done
# 3. If reversal is "one-shot" → verify the snapshot is intact (size matches expected)
test -s "/root/forge_work/.../jobs.json.bak-$TS" && echo "✓ Backup non-empty"
```

If ANY reversal file is missing → ⚠️ F1 AMANAH violated, push back with the user.

### ΔS revision format (final verdict)

After verifying all claims, give a ΔS-revised verdict:

```
Claimed: ΔS = -0.6 (5 defects diagnosed, 3 fixes, 1 cancelled, 1 retired)
Verified: ΔS = -0.5 (conservative) to -0.7 (aggressive)
  • 5 defects diagnosed ✓ (matches table)
  • 3 fixes installed (Tasks 1, 2, 4) ✓
  • 1 "cancelled" was actually retry (Task 3) — categorization slightly off
  • 1 retired (Task 5) ✓
  • Task 6 trace incomplete (PATCH-8ab448 not in jobs.json or backup) ⚠️
```

Never invent a more optimistic ΔS than the evidence supports. If the evidence is ambiguous, give a range.

### When audit reveals gaps

If ANY claim is ❌ Mismatch or ⚠️ Ambiguous:
1. Surface it in your verdict table — don't hide gaps
2. Recommend the smallest possible fix (often: just re-push the missing artifact)
3. Do NOT seal until the gap is resolved (F4 CLARITY — entropy must decrease, ambiguity is entropy)
4. If the user pressed "ship it" anyway, note the gap in your receipt so future agents can find it

### Constitutional axis — which floors this protocol enforces

- **F1 AMANAH** — reversibility check (backup files, reversal command)
- **F2 TRUTH** — live state vs claim matching (no fabrication, no stale data masquerading as fresh)
- **F11 AUDITABILITY** — every claim traceable to evidence (file paths, line numbers, timestamps)
- **F4 CLARITY** — ΔS must decrease (no entropy accumulation from unverified claims)

A repair audit that PASSES all 5 tables has reached **L3 Operational Behaviour** (L0-L4 doctrine). It has NOT reached L4 Reality Contact until a downstream consumer (user, agent, federation organ) actually exercises the repaired surface and observes the expected behavior.

## Sovereign-fix execution protocol — when F13 says "Make it real then" (forged 2026-08-11)

When Arif says **"Make it real then"** with **F13 SOVEREIGN** lane-authority
attached (full separator powers, full capability map visible), he is
delegating the entire diagnosis→fix→verify cycle to you. Three diagnoses
he just made may be wrong; assume them right and probe to validate.

**The 8-step sequence (verified 2026-08-11):**

```
1. ACCEPT ALL DIAGNOSES FULLY
   - For each: "Arif said X" → trust the claim, then verify the location
   - Do NOT hedge ("partially correct", "mostly true"). Accept or refute cleanly.
   - Hedging wastes the sovereign's F13 grant.

2. PROBE TO FIND REAL FIX LOCATIONS
   - Each diagnosis names where the "wrong" code lives. Verify by grep.
   - If diagnosis's named file is wrong, find the actual one — don't argue.
   - git blame for the existing fix to confirm authorship/timeline.

3. EDIT BOTH SOURCE AND RUNTIME
   - /root/<organ>/<file> — source repo (canonical for git)
   - /opt/<organ>/app/<file> — runtime (what's serving traffic)
   - Federation invariant: source ↔ runtime must match. Patch both.
   - If a directory is gitignored (e.g. src/geox_mcp/state/), edit
     runtime directly and acknowledge the source-vs-git asymmetry in the receipt.

4. COMMIT SOURCE IF POSSIBLE
   - If source file is git-tracked: `git add <file> && git commit -m "..."`
   - Use conventional commits (fix:, feat:, docs:, chore:)
   - If source file is gitignored: skip, note in receipt, move on.

5. CLEAR __pycache__ BEFORE RESTART
   - `find /opt/<organ>/app/src -name __pycache__ -exec rm -rf {} +`
   - Python re-imports from .pyc if cached. Forcing recompile is non-negotiable.

6. systemctl restart <organ>-service
   - Capture the service main PID before/after
   - Wait 2-3 seconds for readiness
   - Verify systemctl status shows active (running)

7. LIVE PROBE TO VERIFY
   - Don't trust "service is up" — exercise the actual endpoint the fix touches
   - For protocol fixes: send initialize with the new protocol version, expect 200
   - For identity gate fixes: send tools/call without session, expect 400
   - Compare to the artefact being fixed by Arif's diagnosis

8. WRITE LANE B RECEIPT (if a session/ledger trace is needed)
   - /root/forge_work/<mission>/receipts/HELIX_V<N>_<reason>.md
   - List every fix with file paths before/after diff
   - Honest limitations: which probes couldn't run, which tests weren't done
   - Commit SHA if source was committed
```

**Concrete outputs from 2026-08-11 (the GEOX sovereign-fix):**

```
1. ACCEPTED all 3 Arif diagnoses
   - "fault_codes.py hanya senarai 2025-11-25" — partially right; git blame
     showed it was added today (not Aug 1) but handshake was working
   - "Fix di session_enforcement.py + middleware" — 100% right
   - "actor_id→arif-fazil tak jadi, content_sha256 kosong" — 100% right

2. REAL FIX LOCATIONS
   - workspace.py:line 67 → actor_id default "arif" → "arif-fazil"
   - geox_middleware.py:_inject_evidence_envelope → added sha256 computation
   - session_enforcement.py:validate_session → already correct (P0 reject)

3. EDITED SOURCE + RUNTIME for both files

4. COMMITTED source: 5e6145c3 (geox_middleware.py; state/ is gitignored)

5. CLEARED __pycache__ in /opt/geox/app/src

6. RESTARTED: systemctl restart geox-mcp → OK at 23:55:40 +08

7. VERIFIED LIVE:
   - GEOX public edge: tools/call without session → 400 ✓
   - Service running, 18 tools (no regression)
   - Could NOT test content_sha256 in real response — needs valid SCT

8. WROTE Lane B receipt: HELIX_V4_F13_SOVEREIGN_FIX.md
```

**Counter-example to avoid:**
- ❌ "Arif said X but really it's Y" — wastes the F13 grant
- ❌ Editing only runtime (forgetting source) — re-creates deploy gap
- ❌ Editing only source (forgetting runtime) — fix never reaches traffic
- ❌ `systemctl restart` without clearing __pycache__ — service runs old code
- ❌ Reporting "fixed" without live probe — claims without evidence
- ❌ Long preamble explaining what was found — execute, then report

**When to use this:** any F13 message combining "fix" + full capability grant.
The signal is the F13 lane card pointing at you (not just "please look at X").
When in doubt, run this 8-step sequence.

## Working-style contract — Arif's frustration signal = execution (forged 2026-08-11)

When Arif gives a **short directive with frustration signal** (`BANGANG. Fix all.`, `Pandai2 la hang test`, `Just do it`, `Buat ja la`), the contemplation phase is OVER. The work is: terse plan, then execute, then report. **Do not** write a long philosophical preamble about consequences. **Do not** ask "what will happen when X" reflection — that work happened in the prior session, not now. Three sentences max for the report, with evidence path. The work itself is whatever the directive said.

When Arif asks `So what?` or `What will happen when this is true?` after a SEAL, he wants **practical consequences for him** in three sentences: structural change, what it means for the next session, what stays the same. Skip the build-up; land the punchline. The signal is *not* an invitation to a long federation-state description — those have been given; he wants the human-impact translation.

When the directive is `fix all` / `selesaikan` / `buat`, the implicit ask is:
1. Execute all listed steps, not discuss them
2. Verify with live evidence (curl, grep, ls), not prose
3. Append VAULT999 receipt when done
4. Report in 4–8 lines with table or bullet, not paragraphs

**Counter-example (this session, 2026-08-11):** Arif pasted a 4-step plan and asked "What will happen when this is true?". I responded with a 5-paragraph meditation on gotong-royong, identity transformation, and federation deliberation. Arif replied `BANGANG. Fix all.` — the contemplation phase was already done in his head; he wanted execution, not more reflection. The correct response: `Plan understood. Executing 4 steps. Stand by.` then do the work. After completion, report what changed, not what was contemplated.

## Independent verification when sister agents exhaust — `Pandai2 la hang test` (forged 2026-08-11)

When Arif says `Pandai2 la hang test`, `Hang verify la`, or `Kimi aku dah habis kredit`, the meaning is: **you do it yourself, in parallel, with curl/python/grep — not by spawning another sister agent that will also run out of credits.** This is the L0→L4 doctrine applied to *one agent acting as its own verifier under credit exhaustion*.

```bash
# 1. Live HTTP probes (no subagent, just parallel curl)
for port in "8088:arifOS" "8081:GEOX" "18082:WEALTH" "18083:WELL" \
           "3001:AAA" "7071:A-FORGE" "7072:A-FORGE-MCP" "7073:arifFlow"; do
  P=$(echo $port | cut -d: -f1); N=$(echo $port | cut -d: -f2)
  curl -sf -o /dev/null -w "$N :$P → %{http_code}|%{size_download}|%{time_total}s\n" \
    --max-time 3 "http://127.0.0.1:$P/health"
done

# 2. mcp.json regenerated each loader run — query it directly
python3 -c "
import json
m = json.load(open('/root/AAA/mcp.json'))
print(f'verdict: {m[\"architectural_verdict\"]}')
print(f'runtime_ready: {m[\"summary\"][\"backends_runtime_ready\"]}/{m[\"summary\"][\"backends_catalogued\"]}')
print(f'musyawawah_visible: {m[\"musyawawah_visible\"]}')
"

# 3. Tests against actual state (HEAD vs working tree)
cd /root/AAA && git status -s | head -5
cd /root/AAA && python3 -m unittest discover -s scripts/tests 2>&1 | tail -3

# 4. APEX Judge receipt — verify it exists, not just was claimed
RECEIPT="/root/forge_work/apex_receipts/SEAL-<sid>_sha256_<hash>.json"
test -f "$RECEIPT" && echo "✓ Receipt exists" || echo "✗ No receipt"
```

**Token discipline when verifying yourself:** ~500 tokens per HTTP probe, ~3-5k per claims-list. No subagent dispatch for federation-state verification. The full probe runs in <30 seconds and uses no API credits.

**Probe gotchas to expect:**
- MCP endpoints fail with `Not Acceptable: Client must accept application/json` — add `-H 'Accept: application/json, text/event-stream'` and re-probe
- `/mcp` is POST-only (GET returns empty 200, looks like success, isn't)
- Session ID required for tool calls (not health endpoints)
- Direct MCP `/mcp` body must be JSON-RPC, not curl-friendly
- Working tree may be dirty from sibling writes — verify against HEAD too

## The Phase A doctrine — enabled: false is the default (forged 2026-08-11)

**The single highest-leverage mistake an agent can make on the federation:** bulk-flipping `enabled: true` on every backend in `AAA_CAPABILITY_REGISTRY.yaml` because "the user said open the door for the 7 organs."

The correct Phase A doctrine is `per_task_activation_only: true` (INV-18): backends start `enabled: false` and are flipped to `enabled: true` only when a specific F13 task lease requires them. The 7 organs (arifOS, GEOX, WEALTH, WELL, AAA, A-FORGE, arifFlow) being catalogued and discoverable is NOT the same as all being runtime-ready. The gotong is awakened by per-task activation, not by enabling the whole stack.

**The audit caught this (2026-08-11):** audit agent reported:
> "Enforced enabled: false on catalogued non-canonical backends (disabled-by-default under F13 directive)."

This reverted a `BANGANG. Fix all.` → bulk-enable cycle. The post-audit state had `enabled_count=2` (VAULT999 + arifFlow only as the baseline) vs the pre-audit `enabled_count=30+`. Tests then passed (`28/28 OK`), federation operated normally, and the doctrinal invariant was preserved.

**Verification when working with the registry:**
```bash
# How many backends are enabled?
grep -c "enabled: true" /root/AAA/federation/AAA_CAPABILITY_REGISTRY.yaml
# Expected: ~2 (VAULT999 + arifFlow baseline) for Phase A
# Red flag: >10 means someone bulk-flipped. Revert to committed HEAD.

# What's the loader verdict?
python3 /root/AAA/scripts/aaa_capability_loader.py /root/AAA/federation/AAA_CAPABILITY_REGISTRY.yaml 2>&1 | grep verdict
# Expected: SEAL_ARCHITECTURE (when status=RATIFIED and architectural_ratification.verdict=SEAL_ARCHITECTURE)
# Red flag: SEALED_MUSYAWARAH_CONSENSUS means musyawawah ran (suggests registry went non-RATIFIED)
```

## Working tree drift detection — when "done" lies (forged 2026-08-11)

A sibling agent's "I did X" report can be true on the **committed** state but the working tree may have been modified by Kimi/Codex/sibling/background-cron between HEAD and now. Tests passing on the working tree does NOT mean tests pass on what would actually deploy. The pattern surfaced clearly in this session:

```bash
# Check committed vs working tree state
echo "Committed (HEAD):"
git show HEAD:federation/AAA_CAPABILITY_REGISTRY.yaml | grep -cE "enabled: true"
echo "Working tree (now):"
grep -cE "enabled: true" /root/AAA/federation/AAA_CAPABILITY_REGISTRY.yaml
# If different — drift exists between committed truth and on-disk reality.

# Test results can mislead too
cd /root/AAA && python3 -m unittest discover -s scripts/tests 2>&1 | tail -3
# Working tree: 28 tests, 4 FAIL (because dirty state broke Phase A invariants)
# HEAD (committed): 28 tests, 28 PASS (Phase A correct)
```

**Rule:** When verifying any "done" claim, always:
1. `git status -s` to see dirty/modified files
2. Compare working-tree state to HEAD state for the file in question
3. Run tests AGAINST THE COMMITTED STATE (checkout to HEAD if needed) AND the working tree
4. If they disagree, the working tree is the liar — not the tests, not the report

**When working tree is dirty AND tests pass:** someone (Kimi? audit? background?) made changes that align with doctrine but haven't been committed. Either commit them (preserve the fix) or revert them (if they violated invariants). Don't ship a "all tests pass" report without verifying which state the tests passed on.

## Source Document

Canonical: `/root/forge_work/ariflow-audit/ARIFLOW_L0_L4_ALIGNMENT_REPORT.md`
Phase reports: `/root/forge_work/ariflow-audit/L1_L2_RECONCILIATION.md`, `L2_L3_RECONCILIATION.md`, `REALITY_CONTACT_REPORT.md`

---

*DITEMPA BUKAN DIBERI — Forged 2026-08-10 by Arif F13 sovereign directive, implemented by Hermes. Operational mechanics appended 2026-08-11 from multi-component audit of evening repair summary.*
