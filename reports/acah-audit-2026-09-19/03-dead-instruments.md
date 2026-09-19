# 03 — Dead & Theatrical Guard/Audit/Gate Instruments in the Skill Library

**Audit:** acah-audit-2026-09-19 · **Run:** 2026-09-19 ~10:46–11:05 +08 · **Mode:** STRICTLY READ-ONLY
**Scope:** `/root/AAA/skills`, `/root/.hermes/skills`, the three named `/root/AAA/scripts` auditors,
the system/root cron gates, and the Hermes hook gates.
**Doctrine executed:** `skill-library-integrity/references/instrument-verification.md` (the five
checks) and `references/instrument-liveness.md` (the three states of a tool).

Nothing was fixed, moved, deleted, committed, or repaired. Every broken instrument found is reported
**still broken** — including the two syntax errors, which were left in place deliberately.

---

## 0. Method, and one contamination disclosure

The task's four properties map onto the skill's own five checks. Commands actually run:

```bash
python3 -m py_compile <script>              # 1. does it parse at all
node --check <script.js>                    #    (for .js)
git -C <repo> log --oneline -- <path>       # 2. is it tracked
git -C <repo> status -s -- <path>           #    untracked = red flag
grep -rn '<filename>' /root ...             # 3. does anything call it
grep -nE 'sys\.exit|SystemExit|return [0-9]|process\.exit' <script>   # 4. can it fail
stat -c '%y' <script>; ls -la <artifact_dir>                          # 5. when did it last emit
```

**Contamination disclosure:** `python3 -m py_compile` writes `__pycache__/*.pyc`. The
`scripts/__pycache__/` mtimes in `skill-library-integrity` (10:46+) are **my own run**, not evidence
of an earlier execution. I have not used `__pycache__` mtimes as a liveness signal anywhere below
except where I say so explicitly and where the mtime **predates** this audit session.

I ran **no** mutating script. `jitu.py selftest` was **not** run — it writes `trip.json` — so the
brake is reported as DESIGN-VERIFIED, not execution-verified.

### Coverage measured in this session

| Measure | Value | How |
|---|---|---|
| Skill dirs walked (`AAA` + `.hermes`, realpath-deduped) | 635 | `scan_skill_gates.py` |
| Script files found inside skill trees | 106 | same |
| Compile failures | 2 | `py_compile` / `node --check` |
| Scripts with zero executable callers | 34 / 106 | one-pass content index, 30,341 candidate caller files |
| Scripts with no literal non-zero exit path | 20 / 106 | regex over `sys.exit`/`return N`/`process.exit` |
| Orphan **and** cannot-fail | 8 / 106 | intersection |

---

## 1. PRIMARY TARGET — the six scripts in `skill-library-integrity/scripts/`

Repo: `/root/AAA` (all six tracked; `git status --porcelain` on all 96 AAA skill scripts returned
**0 untracked, 0 dirty** — the untracked-corpse class from `collision_audit.py` has been cleaned).

| script | compiles | last commit | **executable callers** | failure path | has it run? |
|---|---|---|---|---|---|
| `discovery_guard.py` | OK | `f33764e65` | **0** | `return 1` L121; usage `2` L128 | **YES** — see §1.1 |
| `corpse_audit.py` | OK | `1882799ee` | **0** | **NONE — no exit statement at all** | via a byte-identical twin, §1.2 |
| `collision_audit.py` | OK | `4e6a738e9` (today) | **0** | `return 1` **only under `--strict`** L127 | **YES**, post-repair, §1.3 |
| `dependents.py` | OK | `8b8f1fef8` | **0** | **NONE — `return 0` is the only exit** L73 | not found |
| `mirror_or_duplicate.py` | OK | `53fcc0d54` | **0** | `return 1` if `DUPLICATE_OWNER` L128 | referenced §1.4 |
| `skill_resolution_audit.py` | OK | `e3c582e11` | **0** | `return 1` on collisions/mismatches L90 | referenced §1.4 |

**Finding 1-A — none of the six is wired to anything.** For all six, the ONLY references outside
their own directory are **prose** (skill bodies, `references/*.md`, and dedup copies under
`/root/.hermes/.curator_backups/blobs/`). Filtering the search to executable file types
(`.py .sh .mjs .js .yaml .yml .toml .json`) and excluding backups leaves **zero** invocations:

```bash
$ for f in discovery_guard corpse_audit collision_audit dependents mirror_or_duplicate skill_resolution_audit; do
    grep -rn "$f\.py" /root/AAA /root/.hermes /root/A-FORGE /root/arifOS /root/scripts \
      --include='*.py' --include='*.sh' --include='*.mjs' --include='*.js' --include='*.yaml' \
      --include='*.yml' --include='*.toml' --include='*.json' \
      --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=__pycache__ --exclude-dir=.curator_backups
  done
# discovery_guard.py -> only /root/AAA/skills-retired/_tools/v2_audit.py:6  (a PROSE comment)
# corpse_audit.py    -> only a REPAIR-LEDGER-B.json prose field
# collision_audit.py -> only /root/AAA/reflections/*.receipt.json
# dependents.py      -> NOTHING
# mirror_or_duplicate.py -> NOTHING
# skill_resolution_audit.py -> a copy of itself under .hermes/skills/FORGE-skill-linter/scripts/
```

None appears in `crontab -l`, `/etc/cron.d`, any git hook, or any Hermes hook. **All six are
hand-run instruments.** They may only be called by an agent that reads the skill body and types the
path. That is a *document*, per `instrument-verification.md` §3.

**Finding 1-B — half the six cannot return non-zero.**

```python
# corpse_audit.py  (171 lines) — grep for exit paths returns NOTHING:
$ grep -nE 'sys\.exit|SystemExit|return [0-9]' corpse_audit.py
$ echo $?
1        # no match anywhere in the file
```
It ends at L169-171 with `open(...).write(...)` and two `print`s. It computes `stats[...]` counters
including `skills_with_corpses` and then writes a report and exits **0 unconditionally**. A sweep
that finds 500 dead paths and a sweep that finds 0 are indistinguishable by exit code.

```python
# dependents.py L19-20 (its own docstring, honestly):
#   "Read-only, exits 0. A count of 0 for a directory you KNOW has dependents means the probe is
#    broken, not that the directory is free."
# L73:
    return 0
```
Honest about it — but still: the pre-eviction check that LAW 2 (`SKILL.md:367`) makes *mandatory
before removing ANY directory* has no refusal code. A caller cannot gate on it.

```python
# collision_audit.py L127 — the failure is opt-in, and nothing opts in:
    return 1 if (strict and (collide or borrowed)) else 0
# L86:  strict = "--strict" in argv
```
The gate exists but is behind a flag. Zero callers ⇒ zero `--strict` invocations ⇒ the collision gate
has no more enforcement power than `dependents.py`. (This is the script repaired today; the repair
made it *capable* of failing. It is still not *called* with the flag.)

### 1.1 `discovery_guard.py` — REAL, but never observed refusing

It has run, with a recorded receipt:

```json
// /root/_final_out.json:27
"retention_test_output": "discovery_guard: /root/AAA/skills/first-party-evidence-audit  <-  5 source(s)
  PASS relationship-evidence-audit
  PASS relationship-reality-audit
  PASS first-party-corpus-audit
  PASS human-relationship-audit
  PASS human-bond-reality-audit
VERDICT: DISCOVERY PRESERVED"
// :29  "MANDATORY RETENTION TEST PASSED (exit_code=0): VERDICT: DISCOVERY PRESERVED"
```
Invoked programmatically by `/root/AAA/skills-retired/_tools/v2_audit.py:15-16` and
`.../verify_merges.py:64` (both in the retired `_tools` dir, so the wiring is archival, not live).

**Honest caveat:** every recorded run returned `DISCOVERY PRESERVED` (exit 0). There is **no
recorded instance of it returning `DISCOVERY GAP` / exit 1.** Its refusal branch is therefore
**UNVERIFIED** — `detector-integrity.md` §1: *"A gate never observed failing has an unknown verdict
domain."* I did not force it to fail (that would require mutating a skill).

### 1.2 `corpse_audit.py` — ran under a different path, and is a byte-identical duplicate

```bash
$ sha256sum scripts/corpse_audit.py /root/AAA/skills-retired/_tools/living_corpse_audit.py
0f20b1583eae1375...  8238  .../scripts/corpse_audit.py
0f20b1583eae1375...  8238  .../skills-retired/_tools/living_corpse_audit.py
```
Identical bytes. The output artifact `OUT = /root/AAA/skills-retired/2026-09-19-living-corpses`
(L21) exists:

```
-rw-r--r-- 24388 2026-09-19 09:36  LIVING-CORPSES.json
-rw-r--r-- 12044 2026-09-19 09:36  LIVING-CORPSES.txt
```
The `_tools` copy is mtime **09:36**, the artifacts are **09:36**, and `scripts/corpse_audit.py` is
**09:40** — produced *after* the artifact, i.e. it is the copy made to land the tool in the skill.
**Verdict:** the code executed on 2026-09-19, but the skill's own copy carries no independent run
receipt. Provenance is muddled; the instrument is not dead, but the skill cannot prove that *its*
copy has ever run. Report both facts.

### 1.3 `collision_audit.py` — repaired today; first real number exists

```json
// /root/AAA/reflections/2026-09-19-session-reflection.CORRECTION.receipt.json:16
"collision_audit.py run by this session: 643 indexed, 561 distinct routing names,
 59 same-name groups ALL address bands, 0 real collisions, 20 borrowed addresses",
```
This is the pattern-case from the task, now **REAL** (compiles, tracked at `4e6a738e9`, produced a
number). Its remaining weakness is Finding 1-B (the `--strict` opt-in), not death.

### 1.4 Two scripts with a run reference but no run *receipt*

- `mirror_or_duplicate.py` — `/root/AAA/governance/WISDOM_SCAR_LOG.md:116`: *"0 actionable
  AAA-canonical duplications survived a `mirror_or_duplicate.py` audit."* A prose citation, no
  artifact. **UNDETERMINED whether the current version has run.**
- `skill_resolution_audit.py` — `/root/AAA/reports/2026-09-16-media-ingest-youtube-fix.md:36` names
  it as the detector for class "L3 Resolution-Failure". No output file. **UNDETERMINED.**
- `dependents.py` — `/root/AAA/reports/session-close-2026-09-17-skill-substrate.md:81` describes the
  check it performs. No output file. **No evidence it has ever run as a script.**

---

## 2. THE THREE NAMED `/root/AAA/scripts` AUDITORS

All three compile, all three are tracked, all three have **zero executable callers**, none is in cron
or a hook.

| script | compiles | tracked | last commit | callers | failure path | ever run? |
|---|---|---|---|---|---|---|
| `skill-constitutional-audit.py` | OK | `397c090cf` | **2026-09-19** | 0 | `return 1` if worst ≤ `--fail-on` (default `hold`) — L426-427, L485 | **YES, and it published a wrong number** |
| `federation_skill_auditor.py` | OK | `0216ddcf3` | **2026-06-24** | 0 | `return 1` if worst ≥ fail_rank — L656 | UNKNOWN; 3 months stale |
| `tree777-skill-audit.mjs` | `node --check` OK | `6f001b155` | **2026-07-19** | 0 | `return errors.length === 0 ? 0 : 1` L263, `process.exit(...)` L265 | UNKNOWN; 2 months stale |

**Finding 2-A — `skill-constitutional-audit.py` is the best-documented instance of this defect class
in the whole audit, and it is in the same file as its own post-mortem.** The code comment at
L435-440 states it plainly:

```python
# DEFECT FIXED 2026-09-19: this was `args.skills_dir.iterdir()` — ONE LEVEL ONLY. The
# authored library is nested (domains/<domain>/<org>/<coordinate>/<skill>/), so a flat scan
# saw 281 of the 626 SKILL.md files on disk and published an 11% compliance rate over 55%
# of the library, with no indication of the scope.
```
Corroborated at `/root/AAA/reports/skill-redundancy-audit-2026-09-19.md:129`. So this instrument
**did run and did emit an authoritative-looking compliance figure (11%) that was silently blind to
45% of the corpus.** It is now repaired (`--flat` preserves the old behaviour). Its remaining defect
is only that it is *not scheduled and not called* — so nothing runs the corrected check unless a
human types it.

**Finding 2-B — two of the three are effectively abandoned.** `federation_skill_auditor.py` (last
touched 2026-06-24) and `tree777-skill-audit.mjs` (last touched 2026-07-19) both *can* fail
correctly, but neither is invoked by anything and neither has produced an artifact this session. A
sibling auditor written 3 months later overlapped and superseded them. They are **superseded-but-
still-cited** instruments: still tracked, still looking authoritative in `scripts/`, never run.

**Finding 2-C — `tree777-skill-audit.mjs` was already flagged as defective and never repaired.**
`/root/AAA/prompts/archive/INIT_v3_2026-07-17.md:758`:

```
| F7 | `tree777-skill-audit.mjs` | Fix the `registries/skills.yaml` path resolution or mark the
     tool unavailable with a clear test. | T1 AUTO-DO |
```
`registries/skills.yaml` **now exists** (`/root/AAA/registries/skills.yaml`, referenced L17, L185),
so the path defect appears resolved — but the outstanding F7 action item is still open in the prompt
archive, and the tool has still never been wired anywhere. **T1 AUTO-DO items that were never done
are the administrative signature of the theatrical class.**

---

## 3. CRON AND HOOK GATES — the real enforcement surface

The skill's own doctrine (`instrument-verification.md:101`) says to apply the checks to cron and
hook gates. Done.

### 3.1 `jitu-guard` / `jitu.py` — REAL (the strongest control found)

- `/root/.local/bin/jitu-guard` is **fail-closed by construction**: missing authority file → `exit 3`
  (L20-25); authority returning anything unexpected → `exit 3` (L37-39). It uses `set -uo pipefail`
  *without* `-e`, so it captures `rc=$?` correctly rather than dying early.
- `jitu.py` L121-138: `check()` returns allow on idle, on expiry, and on out-of-scope lane; returns
  **refuse** on a live in-scope trip, and on a corrupt state file (`JITU FAIL-CLOSED`, L134-135).
  L54-55: `EXIT_ALLOW = 0`, `EXIT_TRIPPED = 3`.
- **Wiring is nearly total:** 48 of 49 root-crontab lines are guarded (`jitu-guard <lane> && <cmd>`).
- **It has been SEEN TO FIRE.** `/root/.local/share/arifos/jitu/jitu_events.jsonl` records 4 trips,
  all by `F13`, all on 2026-09-17, with matching releases — including a **refused** self-release:

```json
{"event":"trip","by":"F13","scope":["all"],"reason":"cron-lane simulation — verifying the guard fires in a cron environment",...}
{"event":"release_refused","by":"333-AGI"}
{"event":"release","by":"F13","reason":"final verification complete",...}
```
That `release_refused` for `333-AGI` is the one receipt in this whole audit that proves an
authority boundary physically held. **Report as REAL — do not inflate, do not deflate.**

**Residual risk (not a defect, a failure mode):** if the brake were ever left tripped, all 48 lanes
would stop *silently* — their output goes to `>> log 2>&1` and a skipped `&&` chain prints nothing.
The only signal is that logs stop growing. See §3.3.

### 3.2 `skill-entropy-gate.py` — REAL gate, **UNREAD verdict** (fail-but-nobody-listens)

- In cron 4×/day behind the brake:
  `23 4,10,16,22 * * *  jitu-guard skill-entropy-gate && python3 /root/scripts/skill-entropy-gate.py --quiet >> /var/log/arifos/skill-entropy.log 2>&1`
- It **can** fail: `sys.exit(1 if r["fail"] else 0)` (L416). Confirmed alive in syslog for
  2026-09-18T20:23 and 2026-09-19T02:23.
- **It is currently reporting FAIL, 4× a day, into a log nobody reads:**

```
$ cat /var/log/arifos/skill-entropy.log        # whole file, 193 bytes
FAIL missing_frontmatter: 1
FAIL dead_internal_pointers: 2
verdict=FAIL fail=2 warn=6
FAIL dead_internal_pointers: 2
FAIL merge_completeness: 4
FAIL phantom_views: 2
verdict=FAIL fail=3 warn=5
```
- **Consumer search returns nothing.** The only mention of the file anywhere in the codebase is a
  *comment* in `/root/scripts/skills-census.py:280`. No alert, no delivery, no digest, no exit-code
  reader. The cron line has nothing after the gate, so the non-zero exit reaches only cron's own
  log.
- **Verdict:** the control *detects* and *refuses to hide* — but the refusal terminates in a log
  file. `SKILL.md:79` calls it "1 live sensor". It is live and it senses; it does not escalate.
  `verdict=FAIL fail=3` has been sitting unactioned in a 193-byte file. **Theatrical by
  non-consumption, not by construction.**

### 3.3 `attention-metrics.py` — the watchdog for silent jobs is ITSELF unscheduled

`/root/scripts/attention-metrics.py:26`: `exit 1 if any A1 finding is SILENT`; L14: *"A1 cron_silence
— a scheduled job whose log grew before and has stopped growing"*; L18: *"a cron with no log redirect
cannot be judged — reported as UNMEASURED, never as healthy"*. It has a real failure path
(`return 1 if silent else 0` at L416 and L447).

```bash
$ crontab -l | grep -n 'attention-metrics'                      # NOT in root crontab
$ grep -rn 'attention-metrics' /etc/cron.d/ /etc/systemd/system/ # NOT in cron.d or systemd
```
**The only instrument that can detect a silent cron job is not scheduled, and nothing else watches
for silence.** This is the mechanism that would catch §3.1's residual risk and §3.2's unread FAIL.
It is the highest-leverage dead instrument found: build-succeeded, capability-real, wired-nowhere.

### 3.4 `audit_floor_coverage.py` — named "Floor enforcement", cannot fail

`/root/arifOS/scripts/audit_floor_coverage.py`. Cited by
`/root/AAA/skills/engineering/skill-drift/SKILL.md:93`:

> `Floor enforcement: /root/arifOS/scripts/audit_floor_coverage.py — **run it before claiming floors**`

```python
# L397-404 — it computes exactly the count a gate would need:
coverage_count = sum(1 for t in results["tools"].values() if t.get("floor_enforcer_called"))
results["summary"] = {
    "total_tools_audited": len(audited),
    "tools_with_floor_enforcer": coverage_count,
    "tools_missing_floor_enforcer": len(audited) - coverage_count,
    "coverage_pct": round(100.0 * coverage_count / len(audited), 1),
}
# L423 — and then, unconditionally:
    return 0
```
`grep -nE 'sys\.exit|return [0-9]'` returns exactly two hits: `423: return 0` and `427:
sys.exit(main())`. **There is no path that returns non-zero.** It counts the tools that *lack* floor
enforcement and exits 0 regardless. Not in cron, not called anywhere. It is a coverage **report**
wearing the word "enforcement".

### 3.5 `reality-claim-gate` hook — DEAD, and was designed never to block

`/root/.hermes/hooks/reality-claim-gate/` contains, in full:

```
HOOK.yaml.phase1.bak                    (416 bytes)
handler.py.phase1.bak                   (3537 bytes)
__pycache__/handler.cpython-313.pyc     (15542 bytes, mtime 2026-09-12 00:55)
```
**No active `HOOK.yaml`. No active `handler.py`.** A hook without `HOOK.yaml` is not loaded. It is
registered in no config. The stale `.pyc` dated 2026-09-12 proves the handler *did* load once in
"phase 1", after which the active copies were renamed to `.bak` (dir mtime 2026-09-14 15:20).

And the archived manifest says it was built to be inert anyway — `HOOK.yaml.phase1.bak:2`:

> *"F2 detection gate (Phase 1: DETECT, not yet NO). … **Flags to ledger. Fail-soft, never blocks.**
> Phase 2 (promote to NO) requires F13 per gate-promotion doctrine."*

So: a gate named `reality-claim-gate` (a claim-vs-reality check), self-described as **never blocking**,
which additionally is **not currently installed**. It scores on both axes at once: cannot fail *and*
not running. Of the two hook directories under `/root/.hermes/hooks/`, only `well-voice-bridge/` has
an active `HOOK.yaml`.

### 3.6 `/usr/local/bin/skill-audit.sh` — **the #1 gate that cannot fail** (see §5)

---

## 4. DEAD-BY-CONSTRUCTION INSTRUMENTS

Instruments whose code cannot execute at all, independent of callers.

### 4.1 `/root/scripts/constitutional_guard.py` — the constitutional gate CLI is DEAD. Proven by execution.

`federation-mcp-drift-audit/SKILL.md:191` documents the gap itself. Confirmed independently:

```bash
$ ls /root/core
ls: cannot access '/root/core': No such file or directory

$ find /root -name 'constitutional_gate.py'
(0 results)

$ python3 /root/scripts/constitutional_guard.py \
    --action-class mutate --intent "delete production database" \
    --reversible false --blast-radius high
Traceback (most recent call last):
  File "/root/scripts/constitutional_guard.py", line 16, in <module>
    from core.constitutional_gate import gate_action
ModuleNotFoundError: No module named 'core'
EXIT=1
```
The import is at **module scope (L16)**, before `argparse` (L19). So the CLI **cannot reach a verdict
on any input**. Its `sys.exit(0 if result["allowed"] else 1)` (L46) — a perfectly good refusal code —
is unreachable. Its docstring promises *"check any action against F1-F13"* and *"Returns JSON
verdict"*; it returns a traceback.

Tracked in `/root/scripts` at `4a44293` ("chore: add all federation utility scripts"). **It has never
produced a verdict.**

**Aggravating detail:** exit code 1 is emitted by the traceback. A caller that gates on the exit code
would see "BLOCKED" for *every* action — including legitimate ones. An always-blocking gate is
indistinguishable from a working strict gate until someone checks why nothing ever proceeds. That is
the same false-confidence mechanism inverted.

### 4.2 `/root/.hermes/scripts/godel_enforcement.py` — enforced by a script that does not exist

`/root/AAA/skills/domains/general/workshop/creative-design/makcikgpt-article-forging/SKILL.md:814`:

> `2. Run enforcement script: python3 /root/.hermes/scripts/godel_enforcement.py --claim "CLAIM TEXT" --source "internal" --confidence 0.85`

```bash
$ find /root -name 'godel_enforcement.py'      # 0 results
```
The registry says it once lived at `/root/HERMES/scripts/godel_enforcement.py` (10830 bytes,
mtime 2026-07-17) — `/root/AAA/registries/glue-bytes.jsonl:157`. `hermes-gateway-image-routing/
SKILL.md:305` also cites it as a live script. A sibling audit already logged the dead pointer:
`/root/forge_work/skill-hardening/audit.json:1544` lists
`makcikgpt-article-forging/SKILL.md: scripts/godel_enforcement.py` as a dead script reference — and
it is still there. **An "enforcement script" step in a skill's procedure cannot be executed.**

### 4.3 `state-db-firing-probe.py` — mandated before every pruning decision, exists only in quarantine

`/root/AAA/skills/domains/general/aaa/skill-mesh/skill-audit-methodology/SKILL.md:260`:

> `→ scripts/state-db-firing-probe.py — re-runnable inventory builder … **Run this BEFORE pruning to
> get call-count evidence for every kill decision** (per verify-gate Gate 2 EVIDENCE).`

```bash
$ ls /root/AAA/skills/domains/general/aaa/skill-mesh/skill-audit-methodology/scripts/
ls: cannot access '.../scripts/': No such file or directory      # the skill has no scripts/ dir

$ find /root -name 'state-db-firing-probe.py' -not -path '*/quarantine/*'
(0 results)

$ find /root -name 'state-db-firing-probe.py'
/root/.quarantine/zen-20260912/_CANONICAL/HERMES-heritage-5.3G-20260904/skills/devops/skill-audit-methodology/scripts/state-db-firing-probe.py
```
The evidence-gathering step that the skill makes mandatory before any skill is deleted points at a
path that does not exist. The only copy is inside a quarantined heritage tree. A pruning campaign run
by an agent following this skill would proceed with **no call-count evidence** while believing it had
gathered some.

### 4.4 `/root/AAA/skills/forge-visual-qa-w3/scripts/forge_dom_lint.js` — the W₂ witness is a SyntaxError

**This is the direct sibling of the `collision_audit.py` f-string defect.**

```bash
$ node --check /root/AAA/skills/forge-visual-qa-w3/scripts/forge_dom_lint.js
/root/AAA/skills/forge-visual-qa-w3/scripts/forge_dom_lint.js:263
    ).join(', ')}], nav_links: ${doc.querySelectorAll('nav a[href]').length}, deviations: ${deviations.length}`,
    ^
SyntaxError: Unexpected token ')'
```
The template literal at L258-263 opens `${constraints.required_elements.map(t => {` but the callback
closes with `)` instead of `})` — unterminated arrow function, so the literal and the whole file fail
to parse. **It has never executed.**

Its own header (L3) declares it *"forge_dom_lint.js — W₂ Structural/Syntax Witness for
forge_visual_qa"*. The skill body makes W₂ mandatory: `SKILL.md:116` **"Stage 3: W₂ — DOM LINT
VALIDATION (DER)"**, `SKILL.md:145` **"CRITICAL: W₂ is purely algorithmic. No model, no inference, no
guessing."**, `SKILL.md:302` **"W₂ DOM lint MUST assert: …"**, and `SKILL.md:344` lists
*"I9 | Anti-collusion: witness decoupling | Stages 2+3 — W₁/W₂ cannot write W₃"*.

**Caller search:** `grep -rn 'forge_dom_lint' /root` returns **only the file itself**. Zero callers,
zero cron, zero hook. And the SKILL.md never names it — L120-135 shows an inline `node -e "..."` stub
whose body is nothing but comments (`// Parse HTML`, `// Check required elements exist`, …). So the
packaged witness is neither cited nor wired *nor parseable*.

**Consequence:** the "W3 tri-witness consensus" for visual work is a **two**-witness loop in practice;
the deterministic (DER) leg has never run. Every "W₃ PASS (unanimous)" verdict inherits that. This is
the single most consequential dead instrument in the library — it sits inside a control the owner
believes is triple-redundant.

### 4.5 `skill-audit.sh` — detailed in §5, ranked first

---

## 5. THE "GATE THAT CANNOT FAIL" LIST

Ranked by **false confidence created** = (how authoritative it reads) × (how much inherits from it) ×
(how silently it fails).

### #1 — `/usr/local/bin/skill-audit.sh` — the only system-cron skill audit. Cannot fail. 8 ignored CRITICAL verdicts in 9 weekly runs.

**Authority:** the sole skill audit in `/etc/cron.d` (`0 20 * * 6 root /usr/local/bin/skill-audit.sh
>> /var/log/skill-audit.log 2>&1`). Prints `VERDICT: CRITICAL`, `RECOMMENDATION`, numbered action
items. Reads exactly like a control.

**Cannot fail — proven:**
```bash
$ grep -n 'exit\|return' /usr/local/bin/skill-audit.sh
$ echo $?
1          # ZERO matches in 86 lines
```
There is no `exit` and no `return` anywhere. Under `set -euo pipefail` (L6) it exits **0** on normal
completion. L73-79:

```bash
if [ "$ENTROPY_PCT" -gt 50 ]; then
  echo "VERDICT: CRITICAL — skill sprawl is >50% redundant"
elif [ "$ENTROPY_PCT" -gt 20 ]; then
  echo "VERDICT: ELEVATED — consolidation recommended"
else
  echo "VERDICT: CLEAN"
fi
```
Three verdicts, **one exit code**. CRITICAL and CLEAN are the same to any caller.

**It has been failing, weekly, and nothing happened — 9 runs, 8 CRITICAL verdicts, all exit 0:**
```
$ grep -c 'SKILL ORTHOGONALITY AUDIT' /var/log/skill-audit.log     # 9
$ grep -c 'VERDICT: CRITICAL'         /var/log/skill-audit.log     # 8

1:   SKILL ORTHOGONALITY AUDIT — 2026-07-18   ← run 1 TRUNCATED after line 6, printed NO verdict
8:   ... 2026-07-25   40: ... 2026-08-01   72:  ... 2026-08-08   104: ... 2026-08-15
136: ... 2026-08-22   168: ... 2026-08-29   200: ... 2026-09-05   232: ... 2026-09-12
33,65,97,129,161,193,225,257: VERDICT: CRITICAL — skill sprawl is >50% redundant
```
**Nine weekly runs; eight consecutive `VERDICT: CRITICAL`; every run exit 0; zero consequence.** The
first run (2026-07-18) is itself diagnostic — it stops dead after the INVENTORY block (L1-6, ending
`AAA/skills: 126 active, 0 archived`) and the log jumps straight to the 2026-07-25 header at L8, so
the script aborted mid-output under `set -euo pipefail` and reported nothing at all. The `.log` last
grew 2026-09-12; the next run is 2026-09-19 20:00 (after this audit window).

**Its numbers are also self-refuting and stale:**
```
AAA/skills:     197 active, 0 archived     ← live count: ls -1d /root/AAA/skills/*/ | wc -l  = 253
DUPLICATES:
  .agents ∩ .claude: 204
  All three:         204
ENTROPY:
  Redundant skill-slots: 612
  Total active skill-slots: 591
  Redundancy: 103%                          ← >100% redundancy; and triple-overlap 204 > AAA active 197
```
A triple-overlap (204) larger than one of the three sets (197) is arithmetically impossible; and
"103% redundancy" is a figure that should have stopped the script, not been printed as a verdict. It
audits `/root/.agents/skills` and `/root/.claude/skills` as if they were independent stores — they
are now all 253 dirs (view trees over one canonical store), so its entire "duplicates" premise is
obsolete.

**Why it is #1:** it is the only instrument that *looks like* a scheduled governance gate for the
skill library, it has been screaming CRITICAL since July, it cannot escalate, nobody reads it, and its
headline numbers are wrong. Any agent that finds this log has been handed eight weeks of
alarming-and-false evidence in the same artifact.

### #2 — `forge_dom_lint.js` — the W₂ witness of a tri-witness control. Never parsed. (§4.4)
Reads as the deterministic leg of `forge-visual-qa-w3`'s W3 consensus. It is a `SyntaxError`, has zero
callers, and is not cited in its own skill body. **Every claim of "W3 tri-witness PASS" for visual
work is a two-witness claim.** Ranked #2 because the skill is an active doctrine and visual QA is
invoked for delivered artifacts.

### #3 — `/root/scripts/constitutional_guard.py` — constitutional gate CLI. Dead import. (§4.1)
Claims to check any action against F1–F13 and "Returns JSON verdict". Dies on import. Worse, its
traceback exit code (1) reads as BLOCKED, so a naive caller learns "everything is blocked". Ranked #3
because its death is *already documented* in `federation-mcp-drift-audit/SKILL.md:191` — the false
confidence is contained by a sibling note (though the file is still on disk, still tracked, still
unmarked as dead at the file itself).

### #4 — `attention-metrics.py` — the only detector of silent cron jobs. Unscheduled. (§3.3)
Authored to `exit 1` on any SILENT job, explicitly designed for the "log stopped growing" class. Not
in `crontab -l`, not in `/etc/cron.d`, not in systemd. Rank #4 for leverage: it is the control that
would have caught #1, #5 and the §3.1 residual risk.

### #5 — `skill-entropy-gate.py` — FAIL 4×/day into an unread file. (§3.2)
The construction is honest (`sys.exit(1 if r["fail"] else 0)`), the wiring is correct
(`jitu-guard`-prefixed cron), the exit code is real — and it terminates in a 193-byte log with **no
consumer anywhere in the codebase** (only a comment in `skills-census.py:280`). `verdict=FAIL fail=3`
is sitting there now. Ranked #5: it is the *correct* shape of instrument, which makes its unread
output worse than a dead script — a dead script produces nothing to ignore.

### #6 — `audit_floor_coverage.py` — "Floor enforcement" with no non-zero path. (§3.4)
Cited by `skill-drift/SKILL.md:93` as the thing to "run before claiming floors". Computes
`tools_missing_floor_enforcer` (L402) then `return 0` (L423). Counts the gap, cannot report it.

### #7 — `state-db-firing-probe.py` — mandated evidence step, file absent. (§4.3)
`skill-audit-methodology/SKILL.md:260` makes it mandatory before every kill decision. It exists only
under `/root/.quarantine/`. An agent following the skill proceeds without evidence and believes it
has some.

### #8 — `reality-claim-gate` hook — not installed, and "never blocks" by design. (§3.5)
An F2 claim-vs-reality gate whose own manifest says *"Fail-soft, never blocks"*, and whose active
files have been renamed to `.phase1.bak`. No `HOOK.yaml` ⇒ not loaded. Scores on both axes.

### #9 — `godel_enforcement.py` — an "enforcement script" step pointing at a non-existent file. (§4.2)
Cited in a skill's numbered procedure (`makcikgpt-article-forging/SKILL.md:814`), zero filesystem
presence, and already logged as a dead pointer by a prior audit that did not remove it.

### #10 — `corpse_audit.py` / `dependents.py` — the two of six that cannot fail. (§1-B)
Both are real detectors with correct logic and no refusal code. `dependents.py` guards LAW 2 —
"before removing or moving ANY directory" (`SKILL.md:367`) — and always exits 0. Ranked last only
because both are honest in their docstrings about being read-only probes; the false confidence is
lower-grade (a reader who checks the exit code learns nothing, but a reader who reads the docstring
is warned).

**Honourable mention — `mirror_or_duplicate.py`: exit-code polarity.** `return 1` means
"DUPLICATE_OWNER — HOLD for the human" (L20-23, L128). It *can* fail. But it is titled to gate
*merging*, and no caller chains it. Real instrument, zero enforcement.

---

## 6. WHAT IS **REAL** — reported as REAL, not deflated

Anti-inflation discipline requires naming the controls that actually hold.

| Instrument | Why it is real |
|---|---|
| **`jitu.py` + `jitu-guard`** | Fail-closed on missing/corrupt authority (L20-25, L37-39, L134-135). 48/49 cron lines guarded. **Seen to fire**: 4 trips in `jitu_events.jsonl`, incl. `release_refused` for `333-AGI` against sovereign-only release (L170-174). The only control in this audit with a receipt proving an authority boundary physically held. |
| **`collision_audit.py`** (post-repair) | Compiles, tracked at `4e6a738e9`, produced a real number (643 indexed / 0 real collisions / 20 borrowed) recorded in a receipt. Weakness: `--strict` is opt-in and uninvoked. |
| **`discovery_guard.py`** | Has run with output (`/root/_final_out.json:27`, exit_code=0). Caveat: refusal branch never observed. |
| **`/root/AAA/.git/hooks/pre-commit`** | Symlink → `/root/A-FORGE/hooks/pre-commit-lsp-gate.sh`, **target exists** (verified by `readlink -f`). Real exit-1 paths at L59, L69, L208 (10,435 bytes, mtime 2026-09-18). Gates every commit to the canonical skill store. *UNDETERMINED whether it has ever actually blocked a commit* — commits are landing today, which is consistent with either. |
| **`skill-entropy-gate.py`** | Correct gate construction (`exit 1` on FAIL), correctly wired. Its defect is consumption, not construction. |
| **`skill-owner-lookup.py`** | Compiles, and **can** return non-zero (L148, L164: `OWNER_EXISTS`→0, `WEAK_MATCH`→4, `NO_OWNER`→3). See §7 caveat on polarity. |
| **`pdf_content_loss_audit.py`** | Real refusal path (`return 1 if problems else 0`, L291; `sys.exit(2)` L52; `return 1` L203). |
| **`parse-chain-map.py`, `lint-komda-colors.sh`, `ns-compare-watchdog.sh`, `attention-metrics.py`** | All have genuine non-zero exit paths. |

**`scripts/` hygiene is genuinely clean:** all **106** skill-tree scripts are tracked in git, with
**0 untracked and 0 dirty** across `/root/AAA` (96) and `/root/.hermes` (10). The untracked-corpse
class that produced the `collision_audit.py` incident has been fully cleared.

---

## 7. UNDETERMINED / NOT PROVEN — stated as such

1. **`skill-owner-lookup.py` exit-code polarity.** `SKILL.md:86` calls it *"the creation gate"*. It is
   a **lookup**, and its codes are inverted for gate use: `NO_OWNER → 3` (i.e. the case where creation
   *is permitted* returns non-zero), `OWNER_EXISTS → 0`. Chained as
   `skill-owner-lookup.py "x" && create-skill`, it would **block creation exactly when creation is
   allowed** and **permit it when an owner already exists**. No caller exists, so the inversion is
   latent, not realised. I did not run it. Flagging as a design defect awaiting a caller, not as a
   dead script.
2. **Whether `discovery_guard.py` can return `DISCOVERY GAP`.** Never observed. Forcing it requires
   mutating a skill dir — out of scope for a read-only audit.
3. **Whether the AAA pre-commit LSP gate has ever blocked a commit.** No blocking log found; absence
   of a log is not evidence either way.
4. **`mirror_or_duplicate.py`, `skill_resolution_audit.py`, `dependents.py`:** cited in prose as
   having produced results, but I found **no output artifact** for any of the three. Whether the
   *current* revisions have ever run is UNKNOWN.
5. **`federation_skill_auditor.py` (2026-06-24) and `tree777-skill-audit.mjs` (2026-07-19).** Both
   compile, both can fail, neither is called. Whether either ran at authoring time in June/July is
   not determinable from disk now.
6. **`corpse_audit.py` provenance** — the code ran on 2026-09-19 (artifact at 09:36) but under the
   `_tools/living_corpse_audit.py` path; the skill's copy (mtime 09:40) post-dates the artifact. I
   cannot prove the in-skill copy ever executed.
7. **I did not run any mutating instrument**, including `jitu.py selftest`. The brake is
   DESIGN-verified plus receipt-verified, not re-executed by me.

---

## 8. The single sentence the owner asked for

The skill library's own doctrine (`instrument-verification.md:109`) predicted this exactly: *"The
worst place for a dead instrument is inside the skill that defines the defect class."* It was right.
Of the 106 scripts shipping inside skills, **34 have no executable caller, 20 cannot return non-zero,
and 8 are both** — and the two most authoritative-looking controls in the whole federation
(`skill-audit.sh` in system cron, `forge_dom_lint.js` in the W3 tri-witness) are a script that has
emitted eight consecutive weekly CRITICAL verdicts while unable to exit non-zero, and a witness that
has never parsed. The one control that **does** hold — `jitu.py`, 48/49 cron lanes guarded, fail-closed, with a
`release_refused` receipt against `333-AGI` — is the template: it has a refusal code, a caller on
every lane, and a receipt showing it refused.

---

## Appendix — exact artifacts produced by this audit

- `/tmp/audit/scan_skill_gates.py` — the read-only sweep harness (106 rows)
- `/tmp/skill-gate-sweep.json`, `/tmp/skill-gate-sweep.tsv` — per-script property table
- This file: `/root/AAA/reports/acah-audit-2026-09-19/03-dead-instruments.md`

*No file outside `/tmp` and this report was created, modified, moved or deleted. The two syntax
errors (`forge_dom_lint.js`, and the already-repaired `collision_audit.py`) were left exactly as
found.*
