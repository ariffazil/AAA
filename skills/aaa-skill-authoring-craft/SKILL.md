---
name: aaa-skill-authoring-craft
description: "Use when authoring or patching a SKILL.md under /root/AAA/skills (the federation's canonical catalog). Captures the AAA-specific pitfalls, YAML frontmatter discipline, and cross-reference culture that the bundled hermes-agent-skill-authoring skill does not cover — notably the unquoted-colon failure class, sibling-subagent concurrency, and the AAA reference-stack (RSI / AUDIT / AGI / FORGE / substrate)."
version: 1.3.0
author: 333-AGI (subagent)
license: MIT
metadata:
  hermes:
    tags: [skills, authoring, aaa, federation, frontmatter, yaml, cross-reference]
    related_skills:
      - hermes-agent-skill-authoring
      - AUDIT-skill-atlas
      - AUDIT-recursive-audit
      - FORGE-skill-linter
---

# AAA Skill Authoring Craft

> **Scope:** This is the AAA-catalog-specific companion to the bundled `hermes-agent-skill-authoring` skill. The bundled skill covers the general SKILL.md contract (frontmatter, validator, structure). **This skill** covers the AAA-specific discipline: the federation reference stack, the non-obvious YAML pitfalls that fail in production, and the AAA mesh of skills that any new AAA skill should integrate with.
>
> **Iron rule:** AAA is the canonical catalog. All other agents are views. No parallel catalogs.

## Why This Skill Exists

The bundled `hermes-agent-skill-authoring` is protected and cannot be patched from a running session. AAA-specific pitfalls — especially the YAML colon failure and the cross-reference culture — must live somewhere editable. This skill is that somewhere.

## When to Use

- Authoring a new `SKILL.md` under `/root/AAA/skills/<name>/`
- Patching an existing AAA skill (frontmatter change, body update, version bump)
- Wiring a new skill into the federation reference stack (RSI / AUDIT / AGI / FORGE / substrate)
- Reviewing a sibling subagent's draft before SEAL
- After any YAML parse error on a SKILL.md frontmatter

## The Unquoted-Colon Failure Class (CRITICAL)

**Symptom:**

```python
yaml.scanner.ScannerError: mapping values are not allowed here
  in "<unicode string>", line 5, column 205:
     ... evel RSI to federation-wide sync: detects skill drift between ag ...
                                          ^
```

**Cause:** YAML treats unquoted `:` followed by a space as a key-value separator. A description like:

```yaml
description: Unified recursive-improvement protocol across all agents: detects drift between them.
```

...is parsed as `description: Unified recursive-improvement protocol across all agents` (key) followed by a malformed mapping. The validator cannot continue.

**Rule:** Any string field that contains `:` (descriptions, summaries, prose-y labels) MUST be wrapped in double quotes.

```yaml
description: "Unified recursive-improvement protocol across all agents: detects drift between them."
```

**Validate before declaring done:**

```python
import yaml, re, pathlib
content = pathlib.Path("/root/AAA/skills/<name>/SKILL.md").read_text()
assert content.startswith("---"), "missing leading ---"
m = re.search(r'\n---\s*\n', content[3:])
fm = yaml.safe_load(content[3:m.start()+3])
assert "id" in fm or "name" in fm
assert "description" in fm
assert len(fm["description"]) <= 1024
print("VALID")
```

**Same applies to:** `name` (if it contains punctuation), `description`, `notes`, any prose-y yaml field. The `id` field is almost always a slug so it's safe unquoted.

## AAA Frontmatter Convention (vs. Bundled Convention)

The bundled skill expects `name: <slug>` + `description:` + `version:` + `author:` + `license:` + `metadata.hermes.{tags, related_skills}`. AAA skills frequently use a different frontmatter shape:

```yaml
---
id: <skill-id>                          # AAA convention (lowercase-hyphen)
name: "RSI - Human Readable Title"      # With quotes if it contains punctuation
version: 2.0.0
description: "..."                      # ALWAYS quoted if it contains colons
owner: 333-AGI                           # AAA owner label (not "author")
risk_tier: low                           # AAA: low / medium / high / critical
floor_scope: [F2, F4, F7, F11]           # AAA: which F-floors this skill obeys
autonomy_tier: T1                        # AAA: T0 / T1 / T2 / T3
trigger_when:                            # AAA: explicit trigger list
  - session_end
  - phase_boundary
tags: [meta, rsi, recursion]             # AAA: tag list
forged: 2026-08-08                       # AAA: ISO date
forged_by: 333-AGI                       # AAA: which agent forged it
---
```

**Both shapes are valid.** This skill uses the AAA shape because the running profile is `aaa-hermes`. The bundled skill's authoring rules apply to BOTH shapes — the validator only cares about `name` + `description` + size limits.

### `floor_scope` + `autonomy_tier` are AUDITED, not decoration (2026-08-09)

`forge-constitutional-sync.sh` (A-FORGE duty, crontab `0 7 * * *` = 07:00 UTC / 15:00 MYT) greps every skill under `/root/.agents/skills/` for `floor_scope|floors|F1|F2|F4`. A skill lacking all of those tokens drops federation compliance below 100% (observed 2026-08-09: `hermes-gateway-image-routing` was the 1/166 offender → 98%). **Every new or patched AAA skill MUST include `floor_scope:` (or at least one F-floor token) and `autonomy_tier:` in its frontmatter** — treat them as required fields, not optional. `floor_scope` picks the F-floors the skill obeys (e.g. `[F2, F4, F9, F12]` for a gateway-routing skill: TRUTH, CLARITY, ANTI-HANTU, RESILIENCE). Pre-scan before SEAL:

```bash
for skill_dir in /root/.agents/skills/*/; do
  f="${skill_dir}SKILL.md"; [ -f "$f" ] || continue
  grep -qi "floor_scope\|floors\|F1\|F2\|F4" "$f" || echo "MISSING_FLOOR: $f"
done
```

Note: `/root/.agents/skills/` is a symlink mesh into `/root/AAA/skills/` — patching the resolved path edits the same file.

## The AAA Reference Stack (Cross-Reference Culture)

Every new AAA skill should integrate with the existing federation mesh. The five reference classes:

| Class | Skills | When your skill needs them |
|-------|--------|----------------------------|
| **RSI** | `RSI-recursive-improvement`, `RSI-federation-mesh` | Every skill that produces a session artifact |
| **AUDIT** | `AUDIT-recursive-audit`, `AUDIT-skill-atlas` | Every skill about skills, audit, or discovery |
| **AGI** | `AGI-decisions-reflect`, `AGI-skill-unification`, `AGI-plan-dag` | Every skill that involves decisions or planning |
| **FORGE** | `FORGE-skill-linter`, `FORGE-skill-creator`, `FORGE-cross-agent-handoff` | Every skill that forges or lints |
| **substrate** | `substrate/observe-ground`, `substrate/route-dispatch`, `substrate/audit-seal`, `substrate/kernel-bind`, `substrate/verify-gate`, `substrate/memory-manage` | Every skill that touches kernel or memory |

**Reference pattern in your SKILL.md body:**

```markdown
| # | Skill | Role | When to Load |
|---|-------|------|--------------|
| 1 | `<your-skill>` (v1.0.0) | This skill | — |
| 2 | `<upstream-skill>` (vX.Y.Z) | Upstream dependency | At session start |
| 3 | `<downstream-skill>` (vX.Y.Z) | Downstream consumer | After this skill's output |
```

Compounding skills are read together; the order matters. The body should describe the integration flow (this skill → upstream → downstream).

## Sibling-Subagent Concurrency

When two subagents write to the same `SKILL.md`, `write_file` overwrites the other's changes. The runtime warns:

```
_warning: /root/AAA/skills/<name>/SKILL.md was modified by sibling subagent
'<id>' but this agent never read it. Read the file before writing to avoid
overwriting the sibling's changes.
```

**Mitigation strategy:**

1. **Prefer narrow `patch` calls over full `write_file`** when appending or fixing a specific section. Patch does not require a full read.
2. **Read the file fresh before your final write** if you did a full `write_file` — the runtime warning will tell you a sibling touched it.
3. **For class-level skills** (the skill this is), conflicts are rare. A re-read before SEAL is sufficient.
4. **For fresh new skills** (path didn't exist before), the warning is usually stale — your write is the only one. Verify by checking `stat -c %y <path>` matches your session start.

**Marker format for noting sibling writes:**

```markdown
> **Sibling note:** This skill was written by subagent `<id>` on `<date>`.
> Any subsequent edits should preserve the cross-reference table in §X.
```

## AAA Liveness & Mesh Sync

Every AAA skill SHOULD have a `liveness.json` next to it:

```json
{
  "last_invocation": 1723084800,
  "last_outcome_delta": 0.12,
  "invocation_count_30d": 47,
  "health": "HEALTHY"
}
```

Path: `/root/AAA/skills/<name>/liveness.json`. Run `AUDIT-recursive-audit` if `last_invocation` is >30 days old.

After authoring a new skill, ensure mesh sync:

```bash
bash /root/AAA/skills/scripts/skill-mesh-sync.sh --apply
```

This creates symlinks to `~/.grok`, `~/.claude`, `~/.codex`, etc. so other harnesses can resolve the skill.

## Anti-Patterns (AAA-Specific)

| Anti-pattern | Remedy |
|--------------|--------|
| Forging at `/root/AAA/skills/<name>/` without a `description:` field | Validator blocks. Always include description. |
| Forging at `/root/.grok/skills/<name>/` directly | Iron rule: AAA is canonical. Forge at AAA first, then symlink. |
| Bypassing `FORGE-skill-linter` before commit | Always lint: prompt must have 3-7 use-when, ≥3 do-not-use-when, no banned verbs. |
| Frontmatter with mixed ASCII and Unicode quotes | Use straight `"` only. Smart quotes break YAML. |
| Embedding Python code blocks inside YAML scalar without `\|` | Multi-line YAML scalars need `\|` literal block or `>` folded block. |
| Forgetting to update `FEDERATED_SKILLS_REGISTRY_V3.yaml` | Register the new skill at `/root/AAA/skills/FEDERATED_SKILLS_REGISTRY_V3.yaml`. |
| Reference to a non-existent skill | Use `audit-skill-atlas` to verify references resolve before SEAL. |
| **Using `patch` tool to inject complex Python source code** (verified failure 2026-08-11, AAA capability loader) | The `patch` tool is text-based replacement and **mishandles multi-line Python with escaped triple-quoted strings** (`"""..."""` docstrings, f-strings with nested quotes, backslash-escaped quotes). Produces `SyntaxError: unterminated string literal` + `IndentationError: unexpected indent` on the file you just patched. The same trap fires from `skill_manage(action='patch', ...)` whenever the patch payload contains Python source with escaped strings. See **`Patch-Tool Failure Modes for Python Source Injection`** section below for the three safer alternatives and recovery recipe. |

## Fix Failing Skills — Never Delete Them (F13 preference, 2026-08-09)

> Arif: "Skills yang fail need fixing please fix. Jangan buang skills sesuka hati."
> (Failing skills need fixing — don't delete skills arbitrarily.)

When a skill references a dead service, missing binary, deprecated model, or non-operational setup: **PATCH the skill with reality + point to the working alternative. Do NOT delete it.**

The demonstrated correct pattern (2026-08-09):

| Skill | Problem | Fix (not delete) |
|---|---|---|
| `comfyui` | Loaded everywhere but ComfyUI down, no GPU, no comfy-cli | Patched frontmatter with `box_status: "⚠️ NOT OPERATIONAL on this box — no GPU. Use gemini-media-gen / MiniMax (:18100) instead."` — skill stays loadable, honest, and routes correctly |
| `ai-video-generation` | Said MiniMax DEAD, ComfyUI DOWN, no working path | Patched surface table: **Veo 3.1 = PRIMARY (verified working)**, MiniMax ACTIVE on :18100, ComfyUI documented as down — old claims corrected, not removed |

Rules:
1. A skill that was wrong/outdated is a **liability that must be corrected**, not a file to delete — deletion loses reference knowledge (models, ports, alternate paths) that future sessions need.
2. When a service is down, document `box_status` / status in the skill body and route to the working alternative. The skill becomes the honest map, not a dead stub.
3. Environment-dependent failures (missing binary, dead port, deprecated model) belong in the skill as *status*, never as a standalone "this tool does not work" constraint — the fix is the patch, the alternative is the route.
4. Exception: a skill that is genuinely superseded (another skill covers the class better) may be consolidated — `absorbed_into=<umbrella>` — but that is consolidation, not deletion. Confirm with the user first.

## Unify, Don't Fragment (2026-08-09)

> Arif: "Make sure the skills all unified AAA. No need different users different group different skills. Penat wei."
> "Satu agent, satu skill set, semua user."

Never maintain per-user / per-group skill lists. One agent = one unified skill set for ALL humans; only the lane's **memory files, voice, and authority level** differ. The guest lane stays zero-skill (security), every named lane gets the SAME skill list.

Correct pattern (lanes.yaml):

```yaml
UNIFIED_SKILLS = [gemini-media-gen, comfyui, pdf-report-generation,
                  verify-before-report, apex-judge]
# applied identically to: arif, syed, syed-dm, aliff, aliff-aia, izzu, izzu-aia
# guest: skills: []  (zero personal data, zero tools)
```

Anti-pattern observed 2026-08-09: izzu-aia/aliff-aia had `skills: []` while syed had `trading/syedos` — the agent in AIA group claimed "aku tak boleh generate gambar" because its lane had no skills loaded. Per-user skill fragmentation is a capability-amnesia bug, not a feature.

## Common Pitfalls (Quick-Reference)

1. **Unquoted `:` in description** → YAML parse error. Always quote prose fields.
2. **Leading blank line before `---`** → `startswith("---")` fails. The validator rejects the file.
3. **`description` > 1024 chars** → Validator blocks. Move detail to body.
4. **No `name` field** → Validator blocks. Always include `name`.
5. **Banned verbs in trigger phrases** (`help`, `assist`, `improve`, `manage`, `optimize`, `support`) → `FORGE-skill-linter` flags L1.
6. **Fewer than 3 `do not use when` clauses** → `FORGE-skill-linter` flags L2.
7. **No `liveness.json`** → Mesh sync may not link the skill to other harnesses.
8. **Sibling-subagent overwrite** → Re-read + re-patch before SEAL.
9. **`patch` tool on Python source with escaped strings** → `SyntaxError` + `IndentationError`. Use `write_file` with full content, or `python3` heredoc with `Path.replace(MARKER, BLOCK, 1)`. See the section below.

## Validation Checklist (Before SEAL)

- [ ] File at `/root/AAA/skills/<name>/SKILL.md` (not under `~/.grok` or `~/.claude`)
- [ ] Frontmatter starts at byte 0 with `---`, closes with `\n---\n`
- [ ] YAML loads via `yaml.safe_load` with no errors
- [ ] `id` (or `name`) + `description` + `version` + `owner` + `risk_tier` + `autonomy_tier` all present
- [ ] Description ≤ 1024 chars, quoted if it contains `:`
- [ ] Body has at least one `## USE WHEN` and one `## DO NOT USE WHEN` (or AAA-convention equivalents)
- [ ] Cross-reference table for any upstream/downstream skills
- [ ] No banned verbs (`help`, `assist`, `improve`, `manage`, `optimize`, `support`)
- [ ] ≥ 3 `do not use when` clauses
- [ ] `liveness.json` exists at `/root/AAA/skills/<name>/liveness.json`
- [ ] `FEDERATED_SKILLS_REGISTRY_V3.yaml` updated with new skill entry
- [ ] `bash /root/AAA/skills/scripts/skill-mesh-sync.sh --check` is clean
- [ ] `FORGE-skill-linter` reports no L2/L3 violations

## Verification Recipe

```bash
# 1. YAML validity
python3 -c "
import yaml, re, pathlib
p = pathlib.Path('/root/AAA/skills/<name>/SKILL.md')
content = p.read_text()
assert content.startswith('---')
m = re.search(r'\n---\s*\n', content[3:])
fm = yaml.safe_load(content[3:m.start()+3])
assert 'description' in fm
assert len(fm['description']) <= 1024
print('OK')
"

# 2. Lint
# (load FORGE-skill-linter and run its 6-step procedure)

# 3. Mesh sync
bash /root/AAA/skills/scripts/skill-mesh-sync.sh --check

# 4. Schema presence
ls /root/AAA/skills/<name>/
# Expect: SKILL.md  liveness.json (optional)
```

## Templates

- `templates/AAA-SKILL-frontmatter.yaml` — copy-paste frontmatter template with all AAA-convention fields, the colon-quoting rule highlighted, and a sample body scaffold.
- `references/patch-tool-python-failure-modes.md` — verified failure transcript, root-cause analysis, three safer alternatives (write_file / python heredoc / multi-step patch), pre-flight decision tree, backup naming convention, recovery recipe. Read this before any `patch` call on Python source.

## Patch-Tool Failure Modes for Python Source Injection

> **Verified failure:** 2026-08-11, while modifying `/root/AAA/scripts/aaa_capability_loader.py` to add a `_musyawawah_phase()` function with a triple-quoted docstring and `f"..."` strings with nested quotes. After the `patch` call, the file produced `SyntaxError: unterminated string literal (detected at line 487)` and `IndentationError: unexpected indent (line 412, column 8)`. Arif: "BANGANG. Fix all." Recovery was possible only because a `.bak-20260811T224459Z-pre-musyawawah` file existed nearby.
>
> **Full transcript + recovery recipe:** `references/patch-tool-python-failure-modes.md`.

### Why `patch` fails here

The `patch` tool performs text-based replacement. It does not understand Python's indentation context, triple-quoted string delimiters, or escape rules. When the `old_string` or `new_string` parameter contains:

- **Triple-quoted strings** (`"""..."""`, `'''...'''`) — the backslashes that escape the inner quotes get interpreted at the tool's input layer, not the file layer. Result: unterminated string literal at runtime.
- **f-strings with nested quotes** — `f"AUDITOR: {recent_seals} recent SEALs"` inside a multi-line block survives, but mixing single and double quotes inside f-string braces breaks alignment.
- **Lines longer than ~15** with mixed indentation — `patch` preserves the literal indentation of `new_string`, which Python then re-interprets relative to the surrounding block scope, producing `IndentationError`.

The tool is fine for **single-line edits, renames, or one-line additions**. It is unsafe for **function injection, class addition, or any multi-line Python block with embedded strings**.

### Three safer alternatives (in order of preference)

**1. `write_file` with full file content** — best for major rewrites or any insertion > ~30 lines. The file is replaced byte-for-byte from your composed string; no escape ambiguity.

**2. `python3 << 'PYEOF' ... PYEOF` heredoc with `from pathlib import Path`** — surgical insertion. The pattern that worked on 2026-08-11:

```python
from pathlib import Path
BACKUP = Path('/root/AAA/scripts/aaa_capability_loader.py.bak-20260811T224459Z-pre-musyawawah')
TARGET = Path('/root/AAA/scripts/aaa_capability_loader.py')
src = BACKUP.read_text()
src = src.replace('import yaml\n', 'import yaml\nimport requests\nimport json\n', 1)  # imports
src = src.replace('# --- CLI ---', musyawawah_func + '# --- CLI ---', 1)          # function
src = src.replace(old_return_block, new_return_block, 1)                           # call site
TARGET.write_text(src)
import ast; ast.parse(src)  # mandatory pre-flight: catch SyntaxError before declaring done
print("OK")
```

**3. Multi-step narrow `patch`** — only for genuinely small edits. Never for a full function body.

### Pre-flight check before any `patch` on Python source

```text
1. Does new_string contain """...""" or '''...'''?          → STOP. Use write_file or python heredoc.
2. Does new_string contain an f-string with nested quotes?   → STOP. Use write_file or python heredoc.
3. Is new_string more than ~15 lines?                        → STOP. Use write_file or python heredoc.
4. Does new_string contain backslash-escaped quotes (\")?    → STOP. Use write_file or python heredoc.
```

If any answer is YES, the patch tool's text-based replacement cannot guarantee a valid Python file.

### Recovery recipe when `patch` has corrupted a Python file

```bash
# 1. Find a backup. Federated repos under /root/<organ>/ usually have a .bak-<ts> file nearby.
ls -la /root/AAA/scripts/*.bak* | head
# 2. Restore from the most recent backup
cp /root/AAA/scripts/aaa_capability_loader.py.bak-20260811T224459Z-pre-musyawawah \
   /root/AAA/scripts/aaa_capability_loader.py
# 3. Verify it parses cleanly
python3 -c "import ast; ast.parse(open('/path/to/file.py').read()); print('OK')"
# 4. Re-apply your intended change using one of the three safer alternatives above
```

**Defense in depth:** before any `patch` on Python source, take a backup:

```bash
cp /path/to/file.py /path/to/file.py.bak-$(date +%Y%m%dT%H%M%SZ)-pre-<reason>
```

This costs ~1 second and recovers hours of rework. The convention used in this session: `.<reason>` is a short tag like `-pre-musyawawah`, `-pre-forge`, or `-pre-deprecation`.

## Whole-library validation sweep (2026-08-09)

Per-file validation catches one skill. For a library-wide sweep (e.g. after bulk edits,
before mesh sync, or when the skill picker silently drops entries), run:

```bash
python3 scripts/validate-skill-library.py [root1 root2 ...]
# defaults: profile skills + /root/HERMES/skills
# exit 0 = all valid; exit 1 = prints PROBLEMS list (NO_FRONTMATTER / NO_NAME / PARSE_ERROR...)
```

Found 2 broken skills in 435 on 2026-08-09: `hermes-propose-seal` (unquoted colon
in description — the class this skill documents) and `wellness/scripts/SKILL.md`
(a reference-copy pointer file with no frontmatter at all). Fix pattern for pointer
files: add minimal `name:` + `description:` frontmatter rather than deleting the
file — it may be a symlinked reference copy inside another repo (e.g. WELL).



## Contrast-Hardening: mattpocock/skills (2026-10-23, F13-authorized)

Full contrast run against https://github.com/mattpocock/skills (38 skills, ~2.7KB median
body, MIT). AAA inverted contrast: 1,128 SKILL.md, 7.4KB median, 143 skills >20KB.
Patterns ABSORBED below; patterns REJECTED documented too, so nobody re-imports them.

### Absorb — write these rules into every new AAA skill

1. **Body budget: hard target ≤ 12KB per SKILL.md.** Matt\'s largest is 12.6KB (wayfinder)
   and it plans multi-session work. AAA has 143 skills above 20KB — a skill that big is a
   doctrine file wearing a skill costume. Move doctrine to `/root/AAA/instructions/` and
   leave the skill as a 5-verb executable pointer (AAA already does this for the /NNN spine —
   generalize it). Compression pass: keep trigger clauses, decision rules, receipts; cut
   narrative, incident history, and repeated doctrine prose (LAW 8).
2. **Front-load the description\'s first 57 chars as the trigger.** Matt: "Use when X.
   One-line behavior." The wording of the pointer decides whether the agent reaches the
   skill. A must-have skill behind a weakly worded description is a variance bug — sharpen
   wording before inlining more content.
3. **Feedback-loop-first diagnosis.** diagnosing-bugs: "build a tight pass/fail signal for
   THIS bug before any staring at code; bisection/hypotheses merely consume it." AAA has
   helix-diagnosis (loop structure) and probe-before-panic (probe first) but no skill
   states the loop-construction ladder (failing test → curl → CLI fixture → headless
   browser → trace replay → throwaway harness → fuzz → bisect → differential → HITL).
   Reference this ladder from 555-betul and live-system-investigation; propose
   `forge-feedback-loop-ladder` (see proposals list).
4. **Interview-frontier pattern for plans (grilling).** One round, whole frontier, numbered
   questions with recommended answers, sub-agent fetches facts so the human only decides.
   AAA\'s agent-question-budget already gates question frequency; the frontier shape is the
   missing structure for plan-sharpening. Compat check before composing questions.
5. **Wizard pattern: hand humans the steps only they can do.** Interactive bash script that
   opens URLs, says what to click, captures values, writes .env/secrets. AAA equivalent
   gap: credential/2FA/setup walks currently collapse into chat Q&A. The wizard\'s
   confirm-at-every-stage + progress count matches HERMES clarify-tool capacity (5 q/batch).
6. **Redact-first discipline inside diagnostic skills.** "Show commands and outputs with
   secrets replaced <REDACTED>; build loops against env vars so credentials stay in the
   environment." Verified AAA leak class (presigned S3 URLs into state.db) — make this a
   required section in every skill that captures artifacts.
7. **disable-model-invocation for human-entry skills.** Matt marks wayfinder/handoff as
   human-invoked only. AAA equivalent: skills whose trigger is a slash/verb should say so
   in frontmatter (`triggers:` exists — add explicit "not auto-invoked" line in body when
   the skill must never fire silently).

### Reject — do NOT import these

- **Per-repo `/setup-*` init skills.** Matt\'s setup asks tracker/config per repo. AAA\'s
  constitution is federation-level; per-repo setup skills would fragment LAW 8\'s "one road".
- **skills.sh copy-into-project model.** AAA is canonical-catalog + symlink mesh; copies
  rot (the 4 broken view links of 2026-10-22 prove it). Never copy bodies out of AAA.
- **Issue-tracker-as-shared-map (wayfinder\'s tickets).** AAA\'s map surface is
  carry_forward + tasks.json, already governed. A second tracker = duplicate system.
- **Retro-as-ceremony.** AAA\'s AGI-decisions-reflect + 999-ingat already close loops with
  receipts; a standalone retro skill adds ceremony without a new failure class.

### Structural lessons for the catalog (registry/census layer)

- Census VERDICT WARN (2026-10-23): broken view symlinks 4→0 fixed by removing stale
  hermes-view links into `.archive` + repointing openai-docs + typed alternative_to on the
  bundled variant. Same-body bundled copies (chatgpt-apps, migrate-to-codex,
  openai-docs, security-best-practices in kimi/qwen/gemini/opencode) remain WARN-debt:
  the overlay bundler re-exports bodies; typed `alternative_to` relations are the fix
  when bodies diverge, deletion is forbidden (fix-not-delete, above).
- Skill identity = BODY digest, not folder name (census law since 2026-10-18). When
  importing ANY external skill (including mattpocock/skills), forge into AAA at a distinct
  name, run census, register in FEDERATED_SKILLS_REGISTRY_V3.yaml, mesh-sync.

## The Zen

> The catalog is the federation's memory. Every skill forged is a promise: I will load when relevant, I will be honest about my limits, I will not duplicate my peers.
> If you forget the colon rule, the catalog forgets your skill. YAML is the gate. Pass it cleanly.

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-08-08 | Initial forge. Captures the unquoted-colon YAML failure class, AAA frontmatter convention, the reference stack (RSI/AUDIT/AGI/FORGE/substrate), and sibling-subagent concurrency discipline. |
| 1.3.0 | 2026-10-23 | Contrast-hardening vs mattpocock/skills: absorbed body-budget ≤12KB, trigger-front-loading, feedback-loop ladder, interview-frontier, wizard, redact-first, disable-model-invocation patterns; rejected per-repo setup / copy-out / second-tracker / retro-ceremony patterns; census WARN cleanup receipts (4 broken view links fixed, openai-docs identity typed). |
| 1.1.0 | 2026-08-11 | Added "Patch-Tool Failure Modes for Python Source Injection" section (verified failure 2026-08-11, AAA capability loader). Three safer alternatives + recovery recipe + pre-flight check. New pitfall #9 in Common Pitfalls; new row in Anti-Patterns table.
