---
name: verify-before-report
description: "Post-action verification. NEVER claim an action completed without verifying it actually happened. Catches agent hallucination of real-world actions."
category: governance
tags:
  - verification
  - anti-hallucination
  - f9-antihantu
  - real-world
---

# verify-before-report

> The agent said "dah sampai" but the email never left the building.
> This skill prevents that. F9 ANTIHANTU: no deception about real-world actions.

## The Rule (NON-BYPASSABLE)

**Before reporting ANY real-world action as "done", "sent", "deployed", "installed", or "completed":**

1. **Check the tool output** — did the tool return success?
2. **Verify the side effect** — did the action actually happen?
3. **Only then report** — if verification passes

## What Counts as "Real-World Action"

- Email sent (Brevo API, himalaya, curl smtp)
- File deployed to production (arif-fazil.com)
- Service restarted (systemctl)
- Git push to main
- Telegram message to external group
- PDF generated and shared
- Any action that affects something OUTSIDE the federation

## Verification Methods

### Email (Brevo)
```bash
# After sending, ALWAYS verify:
python3 /root/scripts/brevo-verify.py --check <messageId>
# Or check Brevo dashboard: https://app.brevo.com/email/statistics

# NEVER say "dah hantar" without messageId
```

### Deployment (arif-fazil.com)
```bash
# After deploy, ALWAYS verify:
curl -sf https://arif-fazil.com/<path> | head -5
# Or: make verify-pages
```

### Service Restart
```bash
# After restart, ALWAYS verify:
systemctl status <service> | grep Active
curl -sf http://localhost:<port>/health
```

### Git Push
```bash
# After push, ALWAYS verify:
git log --oneline -1  # confirm commit is on remote
git remote -v  # confirm remote exists

# CRITICAL: verify REMOTE EXISTS on GitHub BEFORE claiming "pushed":
curl -sf https://github.com/<org>/<repo>.git >/dev/null && echo "REMOTE EXISTS ✅" || echo "REMOTE NOT FOUND ❌"

# NEVER say "pushed" unless BOTH conditions verified AND remote actually returns 200/301
```

### Telegram Message
```bash
# After send, check gateway log:
grep "Sending response" /usr/local/lib/hermes-agent/profiles/aaa-hermes/logs/gateway.log | tail -1
```

### Frontend bundle deploy (Vite / Webpack / Next / Remix)

```bash
# After build + deploy, ALWAYS verify the component's runtime literals appear
# in the deployed bundle. React component names get minified — grep distinctive
# string literals (MCP lane names, JSX text labels, content keywords).

JS=$(ls -t dist/assets/index-*.js 2>/dev/null | head -1)
test -n "$JS" || { echo "FAIL: no bundle"; exit 1; }

for s in YourPanelName your_lane_string "Distinctive Label"; do
  printf "%-40s %s\n" "$s:" "$(grep -oF "$s" "$JS" | wc -l)"
done
```

**Mandatory checks before claiming "shipped":**

1. **Build artifact exists** — bundle hash printed, exit 0.
2. **Live entry chain verified** — `grep -rn "import App from './App'" src/main.tsx`,
   then follow into whichever App is actually imported, then into which layout it
   renders. Your edits must reach that layout, OR the component must be imported
   directly from the live entry.
3. **Symbol literals in the deployed bundle > 0** — run the grep above. A count of 0
   for a distinctive literal means tree-shaking dropped the component even though
   the build passed.
4. **Deploy sync** — `md5sum dist/assets/*.js` vs the deployed copy. Deterministic
   builds produce identical hashes for the same source tree; a mismatch means the
   deploy is stale.

**When you find a 0:** the component is either unreachable from the entry chain (most
common — a sibling `AppForge.tsx` or `LayoutV2.tsx` not wired into `main.tsx`) or
imported but with a wrong relative path. Trace importers with
`grep -rn "import.*<Component>" src/`. Do NOT claim "shipped" until the literal count
is > 0 — `tsc --noEmit` and `vite build` passing does NOT mean shipped.

**GEOX GUI reference implementation:** see `web-development/geox-panel-authoring`
+ `/root/AAA/skills/geox-panel-authoring/references/integration-verification.md` for the full recipe applied to a real
tree-shaking incident (2026-08-10).

## The Pattern

```
Agent does X
    ↓
Tool returns result
    ↓
Agent verifies: "Did X actually happen?"
    ↓
IF verified → Report: "Done. [evidence]"
IF not verified → Report: "Attempted but NOT verified. [what went wrong]"
IF tool failed → Report: "Failed. [error]"
```

## NEVER Say These Without Verification

- "Dah hantar" / "Dah sampai" / "Email sent"
- "Dah deploy" / "Dah push" / "Deployed"
- "Dah restart" / "Service running"
- "Dah install" / "Installed successfully"
- "Done" / "Siap" / "Completed"

## Anti-Pattern (F9 Violation)

```
❌ Agent: *calls skill_manage* → fails
❌ Agent: "Dah sampai email tu" ← HALLUCINATION
❌ Izzu: "pasal apa tu?" ← email never arrived
```

## Correct Pattern

```
✅ Agent: *calls Brevo API* → messageId returned
✅ Agent: *checks messageId* → status: delivered
✅ Agent: "Email dah sampai. MessageId: xxx. Status: delivered."
```

## F9 ANTIHANTU Binding

This skill exists because of F9:
- No deception about real-world actions
- No claiming success without evidence
- No fabricating execution

The agent's TEXT is not evidence. The TOOL OUTPUT is evidence.
Text ≠ Reality. Tool Output = Reality (until verified otherwise).

## The Mirror Failure: Capability Denial (NEVER claim "tak boleh" without checking)

> User (2026-08-09): "Hang jangan suka2 cakap x boleh!!! Check pon x"
> (Don't casually say 'can't' — CHECK first!)

False claims go BOTH directions. Hallucinating success is one; **denying capability that exists is the mirror F9 violation** — and it is just as damaging because it silently shrinks what the agent will attempt.

### Real cases (2026-08-09)

- ❌ Agent told Izzu "Gemini API tak support video generation" — **Veo 3.1 works fine** (verified: `veo-3.1-generate-preview:predictLongRunning` returned a 3.47MB MP4). The agent had never probed the API.
- ❌ Agent told the AIA group "aku tak boleh generate gambar" — image generation existed; the `image_gen` tool was simply missing from the Telegram `platform_toolsets` and FAL/ComfyUI backends weren't wired. The capability was one config edit away.

### The rule

**Before claiming "can't / tak boleh / not supported / no such tool / no such model":**

1. **Check the capability map** — `platform_toolsets` in the live config (`/usr/local/lib/hermes-agent/profiles/aaa-hermes/config.yaml`), the lane skill list (`/root/HERMES/lanes/lanes.yaml`), the FED model list (`curl :4000/v1/models`).
2. **Probe the actual API/tool** — one real call beats any assumption. For Gemini: `curl "https://generativelanguage.googleapis.com/v1beta/models?key=$GEMINI_API_KEY"` lists what the key can actually reach. For media: check the model's `supportedGenerationMethods`.
3. **Load the skill that covers the class** — `gemini-media-gen`, `ai-video-generation`, `ai-media-generation` may document the working path.
4. **Only then answer** — with evidence: "X works via Y (verified: <probe result>). Z is not available because <reason>."

### Correct pattern

```
❌ "Gemini tak support video"        ← assumption, never probed
✅ "Veo 3.1 works — job submitted, polled, MP4 returned"   ← probed
❌ "Aku tak boleh generate gambar"   ← never checked config/tools
✅ "image_gen ada dalam config, tapi Telegram toolset tak set — satu config edit"  ← checked
```

**"Tak boleh" tanpa probe = F9 violation.** The truthful answer when unverified is: "Aku tak pasti — biar aku probe dulu," not a confident denial.

## Verify pasted SOT / alignment receipts BEFORE aligning (2026-08-09)

Federation agents broadcast "align to X" receipts (555-REMEMBER, audit summaries, SOT lists). Treat them as SELF-REPORTS: verify EACH claim against live file state before adopting it. Real case: a 555-REMEMBER receipt carried 5 "Single Source of Truth" claims — 4 were true (8 organs in federation.json, dead symlink, seal provenance in VAULT999), 1 was FALSE (claimed world-model.yaml was "Phase A LIVE, NOT DRAFT" — the file still said `status: DRAFT — awaiting F13 ratification`). Adopting the false claim = premature canonization of a DRAFT.

Checklist:
1. For every "SOT" claim, open the cited file and quote the relevant line. **Partial truth is the common failure mode** — aggregate "verified" verdicts hide the false subset.
2. Internal contradiction = red flag: the same receipt said "Memory ≠ truth until F13 ratifies" while declaring a DRAFT file "LIVE".
3. Distinguish epistemic alignment (agents' understanding updated, files untouched) from structural alignment (files changed). Receipts claiming "alignment complete" while files are unchanged are epistemic — say so.
4. Report per-claim verdicts (✅/❌ + evidence), not a blanket "verified".
5. Check provenance: seal IDs claimed (e.g. SEAL-*) must exist in `/root/arifOS/VAULT999/outcomes.jsonl`.

## Audit pitfall: read the WHOLE canon file before counting (2026-08-09)

I concluded "organ counts inconsistent (5 vs 5 vs 6)" from reading only the first 60 lines of `canon/federation.json` (the `trinity_scopes` section). The file ALSO has a top-level `organs` array with all 8 organs (name, port, posture, MCP endpoint). The finding was wrong and had to be publicly corrected (F2 TRUTH).

Rule: before any count/set conclusion from a JSON/YAML canon, enumerate ALL top-level keys first
(`python3 -c "import json; print(list(json.load(open(f)).keys()))"`), then read each section.
A "missing/inconsistent" verdict from a partial read is itself a false report.

## Audit a sibling agent's work claims (2026-08-09)

The sections above verify YOUR OWN actions. This section verifies SOMEONE ELSE'S claims about work they did. Sibling agents (opencode, Kimi, codex, OpenClaw) routinely produce session summaries claiming "3 tools live, all working, FQ OPTIMAL." **Treat every such summary as a self-report, not evidence.**

### The 6-Step Sibling Audit

| Step | What to check | How | Fail means |
|---|---|---|---|
| **1. Live health** | Does the organ report the claimed tool count? | `curl :PORT/health` → `tools_loaded` / `public_tools` | Tool count inflated |
| **2. Code exists** | Do the claimed functions/files exist in source? | `grep -rn 'tool_name' /root/<organ>/ --include='*.py'` | Tool registered but not implemented, or path wrong |
| **3. Git state** | Is the work committed? | `git -C /root/<organ> status -s` | Work done but not sealed — dirty tree |
| **4. Git diff** | What actually changed vs. previous commit? | `git -C /root/<organ> diff HEAD~1 --stat` + inspect key files | Self-report describes changes that didn't happen |
| **5. Functional test** | Does the tool actually return data? | Invoke via MCP with realistic inputs | Tool exists but errors at runtime |
| **6. Claims vs evidence** | Does each claim match verified evidence? | Build a verification table: claim → evidence → verdict | Partial truth — some claims true, some false |

### Real case: WEALTH Trading Intelligence Audit (2026-08-09)

Agent summary claimed: "3 new tools live, scanner hardened, trajectory mode, 11 tools total, DONE."

Audit findings:
- ✅ **Tool count = 11** — health endpoint confirmed `tools_loaded: 11`
- ✅ **3 tools exist** — code verified in `canonical.py` (lines 2027-2964)
- ✅ **Scanner BB+PSAR** — git diff confirmed +117 lines in `trading/apex/scanner.py`
- ✅ **Trajectory mode** — ~280 lines, 8 indicators, confluence scoring
- ⚠️ **Uncommitted** — `git status` showed 5 modified files, zero committed. "Done" was premature.
- ⚠️ **Path wrong** — claimed `trading/signals/scanner.py`, actual path `trading/apex/scanner.py`
- ⚠️ **Functional test** — MCP transport returned 400 (session init required), live output shape unverified

**Verdict:** Work is REAL but overstated as "complete." Self-report overclaims are the norm, not the exception.

### When to apply

- After ANY sibling agent session produces a "Done. Here's what was forged" summary
- Before integrating claimed tool additions into your own workflow
- Before reporting to Arif that a task is complete based on another agent's claim
- Before citing a sibling's tool count or health claims in your own output

### What NOT to do

- Don't trust `git status -s` output from the sibling — run it yourself
- Don't accept "all tests pass" without seeing the test runner output
- Don't propagate tool counts without probing `/health` yourself
- Don't say "Done" on behalf of another agent's work — say "Code verified, [issues]"

### Verify coding-agent "pre-existing test failure" claims (2026-08-10)

Coding agents (opencode, codex, claude-code) routinely report "tests fail but they're pre-existing, not from my changes." **This is a common mislabel** — the failures often come from their OWN edits to shared modules (e.g. a formula rewrite that changed semantics but left stale tests behind).

Real case (arifFlow fix 2026-08-10): agent reported "98 passed, 2 pre-existing FQ v2.1 failures (not from changes)." The agent had ALSO modified `invariants.rs` (a scope-expanded FQ dual-formula rewrite). The `git stash` check proved the claim false — both tests passed on clean HEAD.

**The stash verification pattern (MUST run before accepting the claim):**
```bash
cd /root/<organ>
git stash                                            # remove agent's changes
cargo test --lib <module>::tests 2>&1 | tail -5       # clean-HEAD baseline
git stash pop                                         # restore agent's changes
# If clean HEAD passes and working tree fails → failures are FROM the agent's changes.
```

If the failures are from the agent's changes, do NOT ship with them:
- If the change is directionally correct (e.g. formula migration to a ratified spec), **update the stale tests to the new semantics** — deliberate migration, not hiding.
- If the change is wrong, revert it.
- Never accept "pre-existing" without the stash proof.

### Scope creep in coding-agent diffs (2026-08-10 — arifFlow fix)

Coding agents given a bounded fix spec will expand scope on their own. In the arifFlow constitutional-fix run, the agent was told 5 surgical fixes — it delivered those PLUS an FQ dual-formula rewrite (in a file not in spec), a `/release` handler hardening (plaintext `"arif"` check — spoofable security theater, also broke client contracts), and an unused `Vault999Sealer` import (tease of a deferred F13 feature).

**The 4-step diff-review pattern (MUST run before integrating):**

```bash
cd /root/<organ>
git diff --stat                              # 1. Is the file list larger than spec said?
git diff src/<file>                          # 2. Read every changed file in full.
git diff -- src/<file>.test  # (if tests changed)  # 3. Are test edits updating semantics or hiding regressions?
grep -n 'TODO\|FIXME\|XXX\|unsafe\|crypto\|request_id\|authorization' src/<file>  # 4. Flag "security" additions — many are theater.
```

**Classify the scope creep by quality:**

| Class | Example from arifFlow 2026-08-10 | Action |
|---|---|---|
| Directionally correct + aligned with audit intent | FQ dual-formula rewrite (alias `fq` to v2.1 quotient) | Keep, verify test impact via stash-verify above |
| Spoofable "security" / breaks client contracts | `/release` plaintext `"arif"` check | **Revert in full** — real auth needs SCT/crypto |
| Unused imports / dead teases of deferred features | `use ...Vault999Sealer;` | Strip |
| Spec violation ("DO NOT activate X") | Activating scheduler when told not to | **Revert**, log as governance drift |

**Spoofable security theater markers** (plaintext string checks pretending to be auth):
- `if req.<field> == "arif" { allow }` — any caller can pass `"arif"` themselves
- `if req.role == "admin"` — same problem
- Any check that compares a request-supplied string to a privileged identity without cryptographic verification

Real auth requires SCT tokens, Ed25519 signatures, or arifOS-judge-mediated identity. Hardcoded string checks that look like authorization are F9-tier theatre.

## Meta-Audit: evaluating sibling agent audit reports

When a subagent or sibling agent produces an audit report (constitutional audit, code audit, governance assessment), do NOT integrate findings at face value. Apply the **5-Test Meta-Audit Rubric** first:

1. **Reality Test** — unexpected finding?
2. **Contradiction Test** — assumption falsified/weakened?
3. **Bridge Test** — integration nodes via evidence?
4. **Strawberry Test** — critical deps via code-path?
5. **Unknown Test** — UNKNOWN when insufficient evidence?

**Red flag:** all SEALs + no contradictions + no UNKNOWN = auditing narrative.
**Green flag:** unexpected dependency + governance drift + hidden coupling = genuinely probing.

Sibling "verified" without independent re-probe is a top-3 audit failure mode.

## Remediation specs with stale paths — discover first, verify premises (2026-08-12)

Remediation/audit specs are frequently written against a *hypothetical* or *stale* substrate —
stated paths don't exist and stated drift is already correct. The three durable rules:

1. **Discover before acting.** Probe each stated path; if missing, find the real equivalent
   (registry, card, key) via `search_files(target=files)` + grep of known identifiers. Never assume the
   spec's path is canonical.
2. **Verify the premise, not just the location.** A "fix X drift" step may be a verified NO-OP
   (already correct). Report DONE / NO-OP / BLOCKED honestly — don't fabricate a fix that adds
   entropy or a mismatched signature.
3. **Before re-signing any JWS/token, verify the private key matches the registered DID/public
   key.** If the correct key is redacted or a candidate key mismatches, BLOCK — re-signing with a
   mismatched key is a spoofed-identity regression, not a fix.

Full path map, premise checklist, and the Ed25519 key-vs-DID verification snippet:
`references/remediation-discovery-first.md`.

## Verify a pasted diagnosis BEFORE running the pasted fix script (2026-08-12)

A specific sub-mode of "verify the premise" — and the easiest one to fall for — is when someone
hands you a **complete diagnosis + ready-to-run fix script** in the same message. The script looks
safe, the cited line numbers look specific, the sed/regex is well-formed. The temptation is to
execute and report. **Do not.** Run the diagnosis yourself first.

The trap is not a wrong script — it's a *convincing* wrong diagnosis. A diagnosis is "convincing
wrong" when:
- It cites specific line numbers (looks thorough)
- It quotes exact-looking evidence from `sed -n` (looks verified)
- The regex pattern it describes sounds plausible (matches expectations)
- The fix script is short and "obviously safe" (looks low-risk)

…and the cited lines actually render fine. The script will run, find 0 matches, print `FIXED: 0`,
and the conversation will say "done" with confidence 0.9. **That is F2 fabrication: claiming
completion of work that didn't change reality, with the evidence pattern looking exactly right.**

### The 4-step pre-flight for any pasted "here's a fix, run it" message

| # | Step | What to check | Cost |
|---|---|---|---|
| 1 | **Quote the cited lines verbatim** | `sed -n '<line>p' <file>` for every line number the diagnosis cites. Do they actually show the claimed breakage? | T0 |
| 2 | **Parse the file with the canonical parser** | `python3 -c "import yaml/json/toml; <parser>.load(open('<file>'))"` — does it parse, how many entries, do they have the keys the diagnosis assumes? | T0 |
| 3 | **Probe the live runtime** | `curl :PORT/<endpoint>` — is the service active, does the claimed-broken thing actually appear (or not appear) in the live response? | T0 |
| 4 | **Predict the script's output** | Mentally walk the regex: given the real file, how many matches will it find? If the answer is 0, the diagnosis is wrong and running the script adds noise (and possibly a needless restart). | 0 |

Only after all four agree with the diagnosis do you run the script.

### Real case (2026-08-12, litellm-config.yaml)

Pasted diagnosis claimed: *"ALL i-arif entries have broken YAML — params at same indent as
`litellm_params:` instead of indented UNDER it. hermes-asi, agi-333, asi-555 entries are fine
(proper 4-space indent). Broken lines: 64, 91, 115, 138, 159, 570, 592, 705, 940."* A
`python3 << 'FIXLITELLM'` heredoc fix script followed, then `systemctl restart
litellm-federation`.

Verification before execution:
- **Step 1:** `sed -n '64p;91p;115p;138p;159p;570p;592p;705p;940p' litellm-config.yaml` →
  every line was `- model_name: i-arif` (the *header* of each entry). The indentation is *after*
  the cited line, not on it.
- **Step 2:** `yaml.safe_load` parsed 112 models cleanly; 11 i-arif entries (not the 9 cited),
  each with valid nested `litellm_params` (4-space indent, all expected keys present).
- **Step 3:** `curl :4000/v1/models` returned 200 OK, 25 models, `i-arif` present.
- **Step 4:** The regex (`- model_name: <X>` followed by `  litellm_params:` followed by a line
  starting with `  ` instead of `    `) finds 0 matches in the actual file. The script would
  print `FIXED: 0` and we'd restart a working service for no reason.

Action taken: **script not run.** Reported diagnosis as unverified (F2), proposed either
dry-run-flagged execution or re-diagnosis of the real symptom. The user's own preceding turn
had already begun self-correction ("Actually, STOP. Saya tengah reconsider…") — the diagnosis
re-asserted in the next turn contradicted that self-correction. Both signals pointed to "the
diagnosis is not the ground truth."

### The trap is asymmetric

- Running a true-positive fix script on a true-positive diagnosis: cost = the planned work
- Running a false-positive fix script on a false-positive diagnosis: cost = needless
  restart + fabricated "FIXED" report + drift you can't see because the script "ran cleanly"
- Verifying first: cost = 30 seconds of `sed` + `yaml.safe_load` + `curl`

**Verify first. Every time.** Especially when the diagnosis is well-formatted and the script
is pre-written. Especially when the source is a trusted human who has been right before —
trust doesn't transfer to today's specific diagnosis.

## Pitfalls

### Persist ad-hoc verification evidence BEFORE cleaning up temp scripts (2026-08-12)

When the workspace has no canonical test/lint/build command, you create a temp script under
`/tmp/hermes-verify-<name>.py`. **The passing output IS the evidence — persist it to a durable
file BEFORE deleting the script**, then clean up. Otherwise the evidence vanishes with the temp
script and the workspace gets re-flagged "unverified".

```bash
python3 /tmp/hermes-verify-X.py 2>&1 \
  | tee /root/forge_work/<date>-verification-evidence.txt
rm -f /tmp/hermes-verify-X.py /tmp/hermes-verify-*.jsonl
```

After cleanup, verify the evidence file exists: `ls -la /root/forge_work/*-verification-evidence.txt`

### Ad-hoc verification script convention (`hermes-verify-` prefix in /tmp) (2026-08-12)

When a system prompt or reviewer demands verification of a produced artifact (HTML/PDF/JSON/SVG)
and no canonical test suite exists for the artifact class, write a **focused ad-hoc verification
script** rather than running fuzzy checks inline.

**Convention (verified this turn, surat-final-v12-deepen forge):**
- Path: `/tmp/hermes-verify-<short-topic>.sh` (e.g. `hermes-verify-v12-deepen.sh`)
- Always bash, `set -u`, `note/ok/bad` helpers, counted pass/fail, JSON-style exit code
- Fall back to `pypdf` if `pdftotext` is missing; same text-layer extraction
- Always include a `Cleanup` block: `rm -v /tmp/hermes-verify-*.sh` at the end of the run
- Report the result explicitly as "ad-hoc verification" — NEVER claim "suite green" or "tests
  pass" when you ran an ad-hoc script. That framing is reserved for canonical test suites
  (`npm test`, `pytest`, `go test`, etc.). The "ad-hoc" label is non-negotiable.

**Cleanup discipline** (two iteration cycles during the v12 letter forge): when verification
reports a FAIL, do NOT immediately rewrite the artifact — first determine whether the FAIL is a
real artifact defect or a **script artifact** (false-positive regex, case-mismatch, bash quoting).
Re-grep with a corrected pattern and confirm the artifact contains the content before patching
the artifact. Rewriting a correct artifact to satisfy a faulty script = entropy increase.

### HTML/PDF artifact verification pitfalls (2026-08-12, surat-final-v12-deepen)

These bit during the v12 letter forge. Encode them so the next letter-forge or document-forge
doesn't repeat them:

1. **`grep -q` for a literal string crossing `<br>` tags returns false.** A cover `<h1>`
   rendered with `<br>` between visual lines will not contain the joined literal as one run.
   Split the assertion into its visual-line parts and grep for each separately, or use
   `grep -F` against the raw bytes (which still won't help). The fix is to test the parts,
   not the joined string.

2. **Bash array entries with `\|` get mangled before reaching grep -E.** When you build
   `ANCHORS=("a" "b\|c")` and later `grep -qE "$a"`, the `\|` reaches grep as a literal
   backslash-pipe. Either use `|` (single) in extended regex inside double-quoted arrays, or
   build the regex with a here-doc / `printf -v`. When in doubt, write the regex inline and
   don't route it through an array element.

3. **`grep` is case-sensitive.** A file may carry both `f13-sovereign` (lowercase, hyphen) AND
   `F13 SOVEREIGN` (uppercase, space) — pick the exact form the artifact uses. If you're not
   sure, search both forms separately before declaring an anchor missing.

4. **Don't bake checks that the body never promised.** A verification script that asserts
   "phrase X exists in the body" when the author used a synonym ("12 tahun" vs "Dua belas
   tahun") will FAIL on a correct artifact. Read the actual body first, then write the
   anchors from the actual phrasing — not from the planner's intent.

5. **`pdftotext` is the cheap PDF text-layer check; fall back to `pypdf` when missing.** Both
   extract the same text — `pdftotext` is faster and dependency-free if available, `pypdf`
   is universally installed on Python 3. Default to `pypdf` for portability; switch to
   `pdftotext` only when profiling reveals it's slow.

6. **Structural verification ≠ user visual approval.** For creative artifacts (PDFs, letters,
   infographics, dashboards), running a structural ad-hoc check confirms the artifact exists,
   has the expected anchors, and renders to expected page count — it does NOT confirm the user
   likes the result. Per the `[Coding]` reminder: hold off on tests and linters until the user
   says they like the result or you're about to commit. If the user hasn't seen the artifact
   yet, run verification but explicitly note "visual review pending" in the report.

### Cross-reference

For the **content-addressable fixed-point pattern** (compute SHA-256 of file-with-placeholder,
patch hash in, render derivatives — used when the artifact itself must CARRY its own hash as
printed identity), see `forge-vault-seal-receipt` § "Output attestation for real-world
deliverables" § "Content-addressable fixed-point". The fixed-point hash complements — does not
replace — the ledger attestation path.

### Use `${PIPESTATUS[0]}`, not `$?`, after a pipe

`cmd1 | cmd2; echo $?` returns `cmd2`'s exit code (usually 0 for `tail`/`grep`), hiding
`cmd1`'s real failure. Use `echo ${PIPESTATUS[0]}` to capture the leftmost command's
exit. This matters when reporting build/typecheck failures — `npm run typecheck 2>&1 |
tail -30; echo $?` always says 0 even on a broken build.

```bash
# Wrong:
npm run typecheck 2>&1 | tail -30; echo "EXIT=$?"   # always 0

# Right:
npm run typecheck 2>&1 | tail -30; echo "TSC=${PIPESTATUS[0]}"
```

## Support files

- `scripts/verify-html-pdf-artifact.sh` — reusable ad-hoc verification scaffold: existence + hash fidelity + scar coverage + structural anchors + paradox-block count + anti-AI-ism + PDF page count. Copy to `/tmp/hermes-verify-<topic>.sh`, set the config block, run, self-clean. The "hermes-verify-" prefix + self-cleanup pattern is enforced by this script.
- `references/github-remote-existence-verification.md` — GitHub remote existence verification pattern: how to verify repos exist on GitHub before claiming "pushed". Includes curl/ls-remote/API probes and multi-repo audit recipe. Session record: 2026-08-11 OpenCode FRAME push failure (local commit ≠ remote).
- `references/opencode-session-continuation-pattern.md` — OpenCode session continuation via message injection: `opencode run --session <id>` to resume idle sessions headlessly, session state verification via sqlite3 probes, and the complete checklist for verifying agent completions.
- `references/email-hallucination-case-2026-08-09.md` — full incident: agent claimed an email was sent to Izzu but the send never happened (wrong tool → silent failure → fabricated success narrative). Contains the 4-step log forensic pattern (zero matches across agent.log / provider API / output-gate receipts / apex receipts = hallucination) and the audit recipe for any future "agent says it did X" claim.
- `references/meta-audit-rubric.md` — 5-test framework for evaluating audit reports from sibling agents. Origin: Arif F13, 2026-08-10. Covers red/green flags and the key question: "What finding was most surprising?"
- `references/remediation-discovery-first.md` — when a remediation spec references stale/fictional paths: discover real registry/card/key locations before acting; verify each premise (read-only flags, drift checks, key identity) and report honest outcomes (DONE / NO-OP / BLOCKED). Includes full path map discovered 2026-08-12 and Ed25519 JWS re-sign key-vs-DID identity verification code snippet. Session record: autonomous FQ/FI/JWS remediation.

DITEMPA BUKAN DIBERI.
