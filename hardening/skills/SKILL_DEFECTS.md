# SKILL_DEFECTS.md — Hermes skill-library defect audit & hardening

**Scope:** `/root/.hermes/skills/` (recursive, including category subdirs).
**Reference only:** `/root/AAA/skills/` — inspected, **not edited**.
**Auditor:** `/root/AAA/hardening/skills/audit_skills.py` (re-runnable; see §9).
**Worker:** subagent, SKILLS-layer hardening pass.
**Snapshots:**

| Snapshot | UTC | File |
|---|---|---|
| pass 1 (raw detector, no symlink-follow) | 2026-09-14T17:42Z | — |
| pass 2 (symlink-following, pre-fix) | 2026-09-14T17:45Z | `audit_before.json` |
| pass 3 (pre-trigger-fix) | 2026-09-14T17:57Z | `audit_final_pre.json` |
| pass 4 (**final**) | 2026-09-14T17:58Z | `audit_after.json` |

> **LIVE-TREE CAVEAT (F2).** The skill tree was **being modified by other workers
> while this audit ran**. Between 17:45Z and 17:58Z the skill count grew 392 → 417,
> 7 broken symlinks were repaired, and three skills (`FORGE-subagent-lifecycle`,
> `PETRONAS-intelligence-router`, `forge-vss-parser`) gained descriptions at
> 17:48:53Z. Those changes are **not this worker's** and are called out explicitly
> below wherever they move a number. Every before/after figure is stamped with the
> snapshot it came from.

---

## 1. Defect counts — before / after

| # | Class | Before (pass 2, 17:45Z) | After (pass 4, 17:58Z) | Delta |
|---|---|---|---|---|
| 1 | Dangling references (skills) | 45 | **3** | −42 |
| 1 | Dangling references (files) | 112 | **17** | −95 |
| 2 | Duplicate name groups | 10 (20 entries) | 10 (20 entries) @17:58Z → **11 (22 entries) @18:00Z** | 0 — *not fixed, see §3* |
| 3 | Broken symlinks | 7 of 35 | **0 of 35** | −7 — *repaired externally, not by me — §4* |
| 4 | Weak triggers | 317 of 417 (pass 3, 17:57Z) | **307 of 417** | **−10 (this worker) — §5** |
| 5 | Empty / placeholder | 11 (pass 2) → 7 (pass 4) | 7 | −4 — *mixed cause, see §6* |

Separately, pass 1 (raw detector, before false-positive classification) flagged
**50 skills / 136 refs**. The drop 136 → 112 → 17 is partly detection refinement
(see §2.1) and partly real fixes. The accounting below is verified and closes
exactly (`112 = 8+71+3+1+13+16`, checked programmatically against
`audit_before.json` / `audit_after.json`):

```
pre-fix refs flagged (112, pass 2)
  ├─  8  fixed by creating / recovering the cited file       (THIS WORKER)
  ├─ 71  fixed by removing the dead pointer                  (THIS WORKER)
  ├─  3  fixed by re-pointing to a verified live path        (THIS WORKER)
  ├─  1  resolved by ANOTHER worker (nusantara mimo ref)     (not mine)
  ├─ 13  reclassified NON-DEFECT by detector refinement      (never were defects)
  └─ 16  still flagged  (+1 newly flagged = 17 in final pass)
  ─────────────────────────────────────────────────────────
  THIS WORKER: 82 refs across 37 skills  (8 created + 71 removed + 3 re-pointed)
```

Note the 3 re-pointed refs sit in the "non-defect" bucket in the final pass (the
target exists, so the detector no longer calls it missing) — they are pulled out
above so they are not double-counted.

---

## 2. Class 1 — DANGLING REFERENCES

### 2.1 Detector refinement — why the raw number was inflated

The first detector was naive: it stat'd every `references|scripts|templates|assets/*`
token against the **skill directory**. On a federation whose skills drive *repo*
workflows, that produces three false-positive families. `audit_skills.py` now
classifies every token before calling it a defect:

| Class | Count (final) | Meaning | Verdict |
|---|---|---|---|
| `linked` | — | file exists in the skill dir | OK |
| `cross-skill` | 11 | file exists in **another** skill's dir | not a defect |
| `project-relative` | 15 | basename exists **outside** the skill dir (repo path) | not a defect |
| `illustrative` | 17 | inside a fenced code block / explicitly an example | not a defect |

**Worked example of the false-positive class** — `arif-sites-content-ops` cited
`scripts/generate-ns-compare.cjs`. It is not a skill file at all; it is a repo
script:

```
$ find /root -name generate-ns-compare.cjs -not -path '*/.quarantine/*'
/root/arif-fazil.com/sites/arif-fazil.com/scripts/generate-ns-compare.cjs
```

Had the naive detector been trusted, 15 repo paths would have been "fixed" by
deleting live pointers or by fabricating skill-local scripts. **This is the single
most important accuracy finding of the audit.**

### 2.2 CONFIRMED HEADLINE DEFECT — `nusantara-voice-stack`

`/root/.hermes/skills/media/nusantara-voice-stack/SKILL.md` cited
`references/mimo-token-plan-tts-2026-08-21.md` (absent on disk).

> **ASSIGNED ELSEWHERE — not fixed by this worker.** This skill directory was
> excluded from all edits per instruction. As of the final pass (17:58Z) that
> worker has created `references/mimo-token-plan-tts-2026-08-21.md`; **15 of its
> 16 cited reference files are still missing.** Listed here as confirmation the
> detector fires on a real defect.

Still-missing under this skill: `references/alpha-worship-recipes-2026-08-18.md`,
`asi-bot-voice-leak-2026-08-19.md`, `cosyvoice-clone-session-2026-08-25.md`,
`iarif-lane-separation-2026-08-18.md`, `iarif-voice-minting-2026-08-18.md`,
`minimax-indonesian-voices-2026-08-18.md`, `minimax-ttv-voice-cloning-2026-08-18.md`,
`per-modality-bm-evaluation-2026-08-18.md`, `qwen-voice-cloning-2026-08-18.md`,
`sovereign-sound-stabilizer-2026-08-19.md`, `stt-quality-verification-2026-08-18.md`,
`tts-landscape-all-plans-2026-08-18.md`, `tts-lane-updates-2026-08-18.md`,
`video-generation-api-quirks.md`, `scripts/nusantara_prosody.py`.

### 2.3 FIXES — 8 files created / recovered

Each entry states honestly **how** the content was sourced. "Spec-derived" means
the SKILL.md states the script's interface and behaviour; the file below implements
that stated interface. These are faithful implementations, **not recovered originals**.

| # | File created | Sourcing basis | Verification |
|---|---|---|---|
| 1 | `/root/.hermes/skills/litellm-proxy-triage/scripts/litellm-upstream-probe.sh` | **Verbatim** — pointer read "copy of §2 probe, runnable as-is"; §2 is in the SKILL.md | `bash -n` OK |
| 2 | `/root/.hermes/skills/audit/live-pipeline-trace-audit/scripts/ttft_probe.py` | Spec-derived (streaming TTFT + total + chunk count vs OpenAI-compatible `/v1/chat/completions`) | `python3 -m py_compile` OK |
| 3 | `/root/.hermes/skills/creative/infographic-generation/scripts/make_honest_bar_chart.py` | Spec-derived (y-axis from 0, peak/dip annotations, honest data-label caption) | `python3 -m py_compile` OK |
| 4 | `/root/.hermes/skills/hermes-cron-zen/scripts/probe-cron-health.sh` | Spec-derived (bad jobs, broken paths, deliver mismatches; jobs.json + resolver rules documented in the SKILL.md) | `bash -n` OK |
| 5 | `/root/.hermes/skills/devops/fork-drift-assessment/scripts/categorize_upstream_commits.sh` | Spec-derived (`[upstream_ref] [local_ref]`, defaults `origin/main`/`HEAD`, security/critical/feature/fix breakdown) | `bash -n` OK |
| 6 | `/root/.hermes/skills/institutional-epistemic-sink-forensics/scripts/run_wealth_audit.sh` | **Recovered real file** from the sibling agent copy `/root/.kimi-code/skills/institutional-epistemic-sink-forensics/scripts/run_wealth_audit.sh` (1883 B) | file present; pointer restored |
| 7 | `/root/.hermes/skills/cognitive-level-assertion-protocol/references/ed25519-identity-setup.md` | **Recovered real file** from `/root/.hermes/.archive_skills_governance/akal-cognitive-invariants/references/` (3701 B) | file present; pointer repointed to "in this skill" |
| 8 | `/root/.hermes/skills/devops/arif-sites-content-ops/scripts/ns-compare-watchdog.sh` | Spec-derived (silent-on-green mtime gate, `[ "$SRC_JSON" -nt "$GEN_HTML" ]`, rsync only that dir, no build/Caddy/T3) | `bash -n` OK |

### 2.4 FIXES — 74 dead pointers removed or re-pointed (37 skills)

Of the 82 refs this worker resolved: `8` by creating/recovering the file (§2.3),
`71` by **removing** the dead pointer, and `3` by **re-pointing** it to a verified
live target.

| Skill | Ref | Action |
|---|---|---|
| `telegram-bot-routing-doctrine` | `scripts/federation-health.sh` | **re-pointed** → `/root/AAA/scripts/federation-health.sh` (verified present, 2081 B) |
| `trading-signal-chart` | `references/red-news-impact.md` | **re-pointed** → `devops/hermes-cron-rhythm/references/red-news-impact.md` (verified present, 1741 B) |
| `forge-execution-governance` | `references/project-context-files.md` | **re-pointed** → qualified to the `hermes-agent` skill in the aaa-hermes profile (verified present) |

Per-skill refs removed or re-pointed (37 skills, 74 refs):

```
 8  trading-signal-chart          3  social-video-intelligence     1  mulerouter-media
 7  agentic-trading-companion     3  seven-zen-organs-enforcement  1  music-generation
 7  happyhorse-video-api          2  ASI-agentic-governance        1  medical-document-interpretation
 6  minimax-cli                   2  constitutional-floors         1  mt5-ai-trading-agent
 5  intelligence-brief-forge      2  forge-phased-delivery         1  open-slide-integration
 4  claim-receipt-discipline      2  tts-edge-fallback             1  scientific-pdf-generation
 4  live-probe-audit-pattern      1  APEX-quantum-eureka           1  skill-audit-methodology
 4  malaysian-family-law          1  akal-cognitive-invariants     1  telegram-bot-routing-doctrine
                                  1  arif-sites-content-ops         1  arif-style-zen-audit
                                  1  arifos-memory-architecture     1  audio-analysis
                                  1  external-technology-evaluation 1  forge-execution-governance
                                  1  forge-pdf-delivery             1  fork-drift-assessment
                                  1  hermes-cron-zen                1  infographic-generation
                                  1  institutional-epistemic-sink-forensics (file restored)
                                  1  litellm-proxy-triage (file created)
                                  1  live-pipeline-trace-audit (file created)
```

Most removals were whole-line deletions of index bullets in a "References"/"Support
files" block that enumerated files never written (e.g. `trading-signal-chart` had a
7-line block of bare `- references/*.md` bullets, none present). Where the pointer
sat inside substantive prose, only the dead clause was dropped and the knowledge was
kept (e.g. `audio-analysis`, `mulerouter-media`, `open-slide-integration`,
`social-video-intelligence`, `happyhorse-video-api`).

### 2.5 Still flagged (17) — all out of this worker's edit scope

| Count | Skill | Reason |
|---|---|---|
| 15 | `media/nusantara-voice-stack` | **ASSIGNED ELSEWHERE** |
| 1 | `capabilities/agent-capability-self-audit` | resolves into `/root/AAA/skills/` — reference-only |
| 1 | `capabilities/planning/APEX-quantum-eureka` | resolves into `/root/AAA/skills/` — reference-only |

### 2.6 Verification commands

```bash
# class-1 final state
python3 /root/AAA/hardening/skills/audit_skills.py --dangling-only
#   -> 3 lines (3 skills), 17 refs

# the created files exist and are syntactically valid
python3 -m py_compile /root/.hermes/skills/audit/live-pipeline-trace-audit/scripts/ttft_probe.py \
  /root/.hermes/skills/creative/infographic-generation/scripts/make_honest_bar_chart.py && echo OK
bash -n /root/.hermes/skills/litellm-proxy-triage/scripts/litellm-upstream-probe.sh \
  /root/.hermes/skills/hermes-cron-zen/scripts/probe-cron-health.sh \
  /root/.hermes/skills/devops/fork-drift-assessment/scripts/categorize_upstream_commits.sh \
  /root/.hermes/skills/devops/arif-sites-content-ops/scripts/ns-compare-watchdog.sh \
  /root/.hermes/skills/institutional-epistemic-sink-forensics/scripts/run_wealth_audit.sh && echo OK

# a removed pointer stays removed
grep -c 'akal_somatic_scoring' /root/.hermes/skills/creative/minimax-cli/SKILL.md   # -> 0
grep -c 'gold_mtf_chart'       /root/.hermes/skills/trading/trading-signal-chart/SKILL.md  # -> 0
# a re-pointed pointer still names its target
grep -c 'hermes-cron-rhythm/references/red-news-impact.md' \
  /root/.hermes/skills/trading/trading-signal-chart/SKILL.md  # -> 1
```

---

## 3. Class 2 — DUPLICATE NAMES (detected, not fixed)

10 groups / 20 entries. **Not fixed: the fix is to delete or merge a skill, which is
forbidden by this task.** Root cause is structural, not editorial: `capabilities/`
and `domains/` are **symlinks** into `/root/AAA/skills/`, so a skill that exists both
at the Hermes root and in an AAA category is reachable twice.

| Name | Paths | Catalogue resolves to |
|---|---|---|
| `aaa-pdf-voice-protocol` | `/root/.hermes/skills/aaa-pdf-voice-protocol/` ; `domains/geo/…` | root copy (4615 B) |
| `arifos-constitutional-judge` | root ; `capabilities/audit/…` | root copy (3720 B) |
| `arifos-external-council` | root ; `capabilities/audit/…` | root copy (13157 B) |
| `arifos-kernel-zen-audit` | root ; `capabilities/audit/…` | root copy (48121 B) |
| `code-review` | root (12383 B) ; `capabilities/coding/…` (7779 B) | root copy |
| `geox-production-cockpit` | root (4228 B) ; `domains/geo/…` (4726 B) | root copy |
| `image-analyzer-vision` | root (4137 B) ; `capabilities/media/…` (4196 B) | root copy |
| `token-plan-speech` | root ; `capabilities/media/…` | root copy (both 1374 B) |
| `token-plan-video` | root ; `capabilities/media/…` | root copy (both 2080 B) |
| `wealth-claim-state` | root (419 B) ; `domains/capital/…` (475 B) | root copy |

**Resolution rule (verified against the catalogue listing, not by reading the
resolver source):** a bare name resolves to the **shallowest** directory under the
skills root; the category-qualified entries appear as separate catalogue entries
(e.g. `code-review` and `capabilities/coding: code-review`). **Note the divergence:**
for `geox-production-cockpit` and `wealth-claim-state` the *category* copy is the
larger/newer one, so bare-name lookup silently wins with the *older* file. That is a
real content-staleness risk worth a follow-up decision by the owner of
`/root/AAA/skills/`. Also detected: 4 directory-name collisions
(`claude` under `FORGE-onboarding/` and `apex_verdict_seal/`; `know-language`,
`know-math`, `know-physics` under both the root and `knowledge/`).

---

## 4. Class 3 — BROKEN SYMLINKS (detected; repaired externally)

**Detected 7 of 35** symlinks broken (pass 2, 17:45Z):

```
/root/.hermes/skills/FORGE-route-least-power   -> /root/.agents/skills/FORGE-route-least-power
/root/.hermes/skills/FORGE-call-map            -> /root/AAA/skills/FORGE-call-map
/root/.hermes/skills/FORGE-github-ops          -> /root/AAA/skills/FORGE-github-ops
/root/.hermes/skills/FORGE-agentic-web-builder -> /root/AAA/skills/FORGE-agentic-web-builder
/root/.hermes/skills/ASI-agent-invariants      -> /root/.agents/skills/ASI-agent-invariants
/root/.hermes/skills/AAA-setup-help            -> /root/.agents/skills/AAA-setup-help
/root/.hermes/skills/AGI-decisions-reflect     -> /root/.agents/skills/AGI-decisions-reflect
```

**Final state: 0 of 35 broken.** They were re-pointed to newly-created lowercase
targets under `/root/AAA/skills/` (e.g. `forge-call-map`, `asi-agent-invariants`) by
**another worker**, not by this one. Cause was a case-sensitivity rename of the
targets (`FORGE-*` → `forge-*`) without re-pointing the links.

```bash
find /root/.hermes/skills -xtype l | wc -l    # -> 0
```

---

## 5. Class 4 — WEAK TRIGGERS (fixed: 10 of 307)

317 → **307** (−10, exactly the 10 fixed). The definition: the description's first
57 chars carry no usable trigger (`Use when …`). The detector strips leading
markdown (`>`, quotes, bullets) before testing, because several descriptions were
block scalars (`description: >`) rather than inline strings.

### 5.1 The 10 fixed (each is one surgical patch to the description line)

| # | Skill | Before | After |
|---|---|---|---|
| 1 | `trinity-33-canonical` | `The canonical 33-repo Trinity (final)` | `Use when a task touches the 33-repo Trinity — the canonical repo list and which repo owns what.` |
| 2 | `forge-execution-governance` | `Verify services are governed, not just alive.` | `Use when checking whether a service is actually governed, not just alive — verify services enforce their gates.` |
| 3 | `identity-axiom-derivation` | `Derive minimal axioms from codebase evidence.` | `Use when deriving minimal axioms from codebase evidence — extract the smallest set of invariants the code actually implies.` |
| 4 | `nasi-lemak-business-intelligence` | `Nasi lemak business analytics and dashboards.` | `Use when analysing nasi lemak business data — vendor costs, margins, sales dashboards and per-location performance.` |
| 5 | `web-extraction-fallbacks` | `Fallback ladders for URL extraction failures.` | `Use when a URL extraction fails — blocked, paywalled, rate-limited or bot-walled. Ordered fallback ladders per failure mode.` |
| 6 | `litellm-proxy-triage` | `Disambiguate LiteLLM errors before restarting.` | `Use when LiteLLM throws errors or hangs — disambiguate upstream vs stale proxy before restarting.` |
| 7 | `civic-shadow-editorial` | `Publish MakcikGPT articles and PM shadow pages.` | `Use when publishing MakcikGPT articles and PM shadow pages to the site.` |
| 8 | `geological-figure-production` | `Geological figure pipeline with vision-QA loop.` | `Use when producing geological figures — pipeline with a vision-QA verification loop.` |
| 9 | `intelligence-brief-forge` | `Forging 4-layer institutional disclosure briefs.` | `Use when forging 4-layer institutional disclosure briefs — tersurat/tersirat/void analysis with epistemic tags.` |
| 10 | `arif-human-membrane-integration` | `Integrate human-meaning-membrane into Hermes flow.` | `Use when integrating human-meaning-membrane into the Hermes flow — meaning-preserving human interface.` |

```bash
# verification — all 10 now lead with a trigger
for s in KERNEL-trinity-33 governance-audit/forge-execution-governance identity-axiom-derivation \
         business/nasi-lemak-business-intelligence web/web-extraction-fallbacks litellm-proxy-triage \
         content/civic-shadow-editorial geo/geological-figure-production intelligence-brief-forge \
         arif-human-membrane-integration; do
  printf '%s: ' "$s"; grep -m1 -A1 '^description' /root/.hermes/skills/$s/SKILL.md | tr '\n' ' '; echo
done
# -> every one leads with "Use when"
grep -rlE '^description: "?[Uu]se when' /root/.hermes/skills --include=SKILL.md | wc -l   # 88
```

### 5.2 Worst 20 remaining (detect-only; the 10 fixed are excluded)

| # | Len | Skill | Description |
|---|---|---|---|
| 1 | 50 | `shadow-mapping` | `Shadow mapping from WhatsApp for Arif. F5-private.` |
| 2 | 51 | `brevo-email-sending` | `Send email via Brevo REST API with PDF attachments.` |
| 3 | 51 | `chat-screenshot-forensics` | `Chat screenshots: bubble colors and requotes first.` |
| 4 | 51 | `skills-cold-storage-ops` | `Thaw or freeze skills. Use when a skill is missing.` |
| 5 | 51 | `telegram-gateway-troubleshooting` | `Fix Telegram echo loops via require_mention config.` |
| 6 | 52 | `mcp-ecosystem-indexing` | `Index MCP servers for maximum agent discoverability.` |
| 7 | 52 | `music-intelligence` | `Governed music generation + somatic scoring pipeline` |
| 8 | 52 | `nasilemak-engine` | `Nasi lemak vendor costs and 12-location order rules.` |
| 9 | 53 | `forge-monolith-split` | `Split a monolithic Python file into per-module files.` |
| 10 | 53 | `github` | `GitHub via gh CLI: PRs, issues, reviews, repos, auth.` |
| 11 | 53 | `open-slide-integration` | `Agentic slide/PDF authoring patterns from open-slide.` |
| 12 | 53 | `synthesis-verification-gate` | `Run before synthesis outputs to classify every claim.` |
| 13 | 54 | `biohacker-peptide-stack` | `Peptide protocols. Dose/timing/stacking for gym crowd.` |
| 14 | 54 | `har-derived-api-client` | `Record a site's XHR into a HAR, derive an HTTP client.` |
| 15 | 54 | `image-identity-transfer` | `Preserve a face from one image into a new composition.` |
| 16 | 54 | `Real-Person Reference Photos — Anti-Fabrication` | `Real-person photo: Wikimedia first, attribute, no T2I.` |
| 17 | 55 | `social-video-intelligence` | `Multi-platform social video content access and analysis` |
| 18 | 55 | `telegram-group-sender-identity` | `Fix bot not identifying group senders with empty names.` |
| 19 | 56 | `heartmula` | `HeartMuLa: Suno-like song generation from lyrics + tags.` |
| 20 | 56 | `image-gen-fallback-chain` | `Image generation under provider outage. Fallback ladder.` |

---

## 6. Class 5 — EMPTY / PLACEHOLDER (detect-only)

7 entries flagged (down from 11 at pass 2; 4 were fixed by other workers at
17:48:53Z — `FORGE-subagent-lifecycle`, `PETRONAS-intelligence-router`,
`forge-vss-parser` gained descriptions, and `AAA-video-emd-pipeline` was
reclassified).

| Size | Skill | Reason | Path |
|---|---|---|---|
| 57983 B | `deployment-claim-verification` | placeholder marker `TODO` | `devops/deployment-claim-verification/SKILL.md` |
| 6908 B | `audit-falsification-discipline` | placeholder marker `not yet written` | `governance/audit-falsification-discipline/SKILL.md` |
| 87049 B | `claim-receipt-discipline` | placeholder marker `TODO` | `governance/claim-receipt-discipline/SKILL.md` |
| 3751 B | `self-recurrence-guards` | `[SKILL_PRUNED]` — content lost to compression | `governance/self-recurrence-guards/SKILL.md` |
| 17955 B | `malaysian-physique-circuit` | placeholder marker `TBD` | `malaysian-physique-circuit/SKILL.md` |
| 6490 B | `arif-family-members` | placeholder marker `to be filled` | `personal/arif-family-members/SKILL.md` |
| 26040 B | `external-technology-evaluation` | placeholder marker `coming soon` | `research/external-technology-evaluation/SKILL.md` |

Only `self-recurrence-guards` is a **real content-loss defect**; the `TODO`/`TBD`
hits are mostly legitimate in-body markers inside large skills, not stub skills. Not
fixed: out of this task's fix mandate (`(a)` dangling refs, `(b)` 10 triggers), and
each needs authored content that cannot be sourced.

---

## 7. Additional findings (not in the 5 requested classes)

1. **`arif-sites-content-ops/SKILL.md` is 101,683 chars — over skill_manage's 100,000
   limit.** `skill_manage(action='patch')` **refuses** to edit it
   (`SKILL.md content is 101,683 characters (limit: 100,000)`). The skill is
   effectively unmaintainable until split into `references/`. This blocked the
   intended pointer patch for `ns-compare-watchdog.sh`; the defect was closed from
   the other side instead, by creating the cited script. **Recommended follow-up:
   split this skill.**
2. **Skill name schema violation:** the skill at
   `/root/.hermes/skills/creative/forge-real-person-reference-photos/SKILL.md`
   declares `name: Real-Person Reference Photos — Anti-Fabrication` — uppercase,
   spaces and an em-dash. Names are specified as lowercase with hyphens; this will
   break any resolver that normalises or de-duplicates by name.
3. **Directory-name vs frontmatter-name divergence** is widespread: e.g.
   `/root/.hermes/skills/cognitive-level-assertion-protocol/` declares
   `name: akal-cognitive-invariants`; `/root/.hermes/skills/KERNEL-trinity-33/`
   declares `name: trinity-33-canonical`. **`skill_manage` resolves by directory
   name, not frontmatter name** — a `write_file` against `akal-cognitive-invariants`
   fails with *"not found in active profile"*. Worth documenting; it silently
   breaks tooling written against frontmatter names.

---

## 8. Provenance / method

- Every defect above was produced by stat'ing real paths (`os.path.exists`) or by
  `find`/`grep` on this box. No missing file, duplicate or byte count is estimated.
- Files created from a **spec** (§2.3 rows 1–5, 8) implement the interface the
  SKILL.md itself documents. They are **not** claimed to be the original artefacts.
  Files recovered from a real local copy (§2.3 rows 6–7) are byte-faithful to their
  source, which is cited in each file's header.
- Where content could not be sourced, the pointer was **removed** rather than
  invented (§2.4) — 72 pointers removed, 3 re-pointed to verified live targets.
- `nusantara-voice-stack` was **excluded from all edits** per instruction and is
  recorded as ASSIGNED ELSEWHERE.

## 9. Reproducing this audit

```bash
python3 /root/AAA/hardening/skills/audit_skills.py                    # human summary
python3 /root/AAA/hardening/skills/audit_skills.py --json out.json    # full machine report
python3 /root/AAA/hardening/skills/audit_skills.py --dangling-only    # TSV, one line per skill
python3 /root/AAA/hardening/skills/audit_skills.py --no-follow        # ignore category symlinks
python3 /root/AAA/hardening/skills/audit_skills.py --top 40           # longer weak-trigger list
```

The auditor follows symlinked category directories (`capabilities/`, `domains/`,
`wellness/`) with a realpath cycle-guard, excludes `/root/.hermes/profiles/`, and
caches a filesystem basename index so `project-relative` pointers can be
distinguished from genuine skill-local ones. It is safe to re-run at any time; it
writes nothing except the JSON you ask for.

*End of report.*
