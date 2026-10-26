---
name: multi-cli-coding-dispatch
description: 'Dispatch identical specifications to multiple coding CLIs (qwen-code, opencode, codex, claude-code) in parallel for Gödel E3 provider-diversity independence.'
version: 1.0.0
forged: 2026-08-12
owner: F13 SOVEREIGN
risk_tier: medium
autonomy_tier: T2
floor_scope: [F2, F4, F7, F11, F13]
agent: 333-AGI × 777-FORGE (orchestration) + per-CLI agent (execution)
source_convergence: PETRONAS v12 DRAFT_SPEC dispatch (Qwen + DeepSeek + gpt-5.6-luna)
dependencies:
  skills: [civic-petition-forge, FORGE-route-least-power]
  servers: []
  tools: [qwen, opencode, codex, claude, terminal(background)]
triggers:
  - "dispatch to multiple coding agents"
  - "parallel coding CLI dispatch"
  - "Gödel E3 independence on artifacts"
  - "3-way cognitive lens comparison"
  - "sovereign-scale work requires multi-model consensus"
  - "forge work that can't tolerate single-model failure"
  - "spec-first architecture with parallel agent execution"
---

# Multi-CLI Coding Dispatch

> **Class:** Dispatch identical specifications to multiple coding CLIs for Gödel E3 provider-diversity independence.
> **Pattern:** Spec-first → parallel dispatch → convergence comparison → F13 selection.
> **Output:** 3+ independent drafts of the same artifact, from different model providers, for sovereign-grade selection.

## When to use

Trigger when ANY high-stakes artifact requires more than one cognitive lens:

| Scenario | Why multi-CLI |
|----------|---------------|
| Sovereign petition forge (PAC letters) | Single-model failure = ungrounded constitutional act |
| Constitutional document iteration (v3→v12) | Single lens = convergence trap; multi-lens breaks through |
| Audit redaction review | Multi-model consensus = independent witness |
| Critical bug fix with multiple plausible solutions | Three agents propose different fixes; F13 picks |
| Schema validation across federation | Each CLI uses different reasoning style; coverage gaps surface |
| High-value visual generation | Style/voice/composition differ enough to merit comparison |

**Do NOT use for:** Trivial scripts, single-line edits, anything that doesn't benefit from 3 different cognitive lenses. The dispatch overhead is real — use it when the work justifies it.

## The Spec-First Architecture

```
        ┌─────────────────────────────────┐
        │  CANONICAL SPEC (single source) │
        │  /path/to/WORK_SPEC.md v1.0     │
        │  (versioned, with CHANGELOG)    │
        └────────────────┬────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
   ┌─────────┐      ┌─────────┐      ┌─────────┐
   │  CLI 1  │      │  CLI 2  │      │  CLI 3  │
   │ qwen    │      │ opencode│      │ opencode│
   │ default │      │ deepseek│      │ gpt-5.6 │
   │ anthropic│     │ v4-pro  │      │ -luna   │
   └────┬────┘      └────┬────┘      └────┬────┘
        │                │                │
        ▼                ▼                ▼
   output-1.html   output-2.html   output-3.html
        │                │                │
        └────────────────┼────────────────┘
                         ▼
              ┌─────────────────────┐
              │ CONVERGENCE REPORT   │
              │ diff, voice, depth   │
              │ F13 SOVEREIGN picks  │
              └─────────────────────┘
```

### Why Spec-First

The spec is the **single source of truth** for the artifact. Each agent receives the SAME spec (or a pointer to it) and produces an INDEPENDENT interpretation. This is provider-diversity as convergence, not divergence.

**Anti-pattern:** Writing different prompts for each agent to encourage diversity. That's prompt-engineering-of-divergence, not Gödel E3. E3 is independent lens ON the SAME problem.

### Spec Requirements

A good spec for multi-CLI dispatch must be:
1. **Self-contained** — agent reads only the spec, no implicit context.
2. **Versioned** — `v[N+1]` for F13 corrections, with CHANGELOG entry.
3. **Deterministic on intent** — same spec → same intent → agent decides voice.
4. **Has explicit output paths** — unique per agent to avoid collision.
5. **Has explicit return format** — so convergence comparison is mechanical.

Example skeleton:

```markdown
# WORK_SPEC.md v1.0

## Mission
[one paragraph]

## Authority & Context
[paths to load, names of canon to cite]

## Non-Negotiable Spec
[structural rules — voice, length, structure, anti-patterns]

## Deliverables
- Agent 1: output-1.html
- Agent 2: output-2.html  
- Agent 3: output-3.html

## Success Criteria
[PASS / FAIL checklist]

## Return Format
```
DRAFT COMPLETE — [AGENT_NAME]
Output: /path/to/output-[harness].html
Pages estimate: [N]
SHA-256: [hash]
Verdict: [PASS / NEEDS_AMEND]
Top 1 thing to change: [one line]
```
```

## CLI Selection Matrix

| CLI | Best for | Default model | When to AVOID |
|-----|----------|---------------|---------------|
| `qwen-code` | Anthropic-routed coding, fast iteration | `hermes-asi` via anthropic | Multimodal image gen |
| `opencode --model opencode-zen/deepseek-v4-pro` | Deep reasoning, 1M ctx | deepseek-v4-pro | Latency-sensitive tasks |
| `opencode --model opencode-zen/gpt-5.6-luna` | Balanced reasoning + voice | gpt-5.6-luna | Pure code generation |
| `opencode --model opencode-zen/kimi-k3` | 2.8T MoE, 1M ctx, coding+vision | kimi-k3 | Short factual tasks |
| `opencode --model opencode-zen/glm-5.2` | Zhipu flagship, 200K ctx | glm-5.2 | Pure English BM-grade tasks |
| `codex` | OpenAI-specific coding patterns | gpt-* | Non-OpenAI federated work |
| `claude-code` | Anthropic-specific patterns | claude-* | When OpenAI depth is needed |

For sovereign-grade work: qwen + deepseek + gpt-5.6-luna is the proven trio (verified 2026-08-12, Gödel E3).

## The Dispatch Loop

### Step 1 — Probe (always first)

```bash
# List ALL models from ALL providers
opencode models

# Verify CLI binaries exist
which qwen opencode codex claude gemini

# Check active processes (avoid stale dispatch)
ps -ef | grep -iE "(qwen|opencode)" | grep -v grep
```

### Step 2 — Kill stale (if any)

```bash
# Use process tool — never raw kill -9 if avoidable
process(action="kill", session_id="proc_xxx")
```

### Step 3 — Launch parallel

```bash
# Each as terminal(background=true, notify_on_complete=true)
# Stagger by 8 seconds to reduce system thrash

# Qwen (no -m — defaults to anthropic route)
qwen -p "$PROMPT" -o text

# DeepSeek (opencode-zen tier has balance)
opencode run --model opencode-zen/deepseek-v4-pro "$PROMPT"

# gpt-5.6-luna (zen tier + explicit provider)
opencode run --model opencode-zen/gpt-5.6-luna "$PROMPT"
```

### Step 4 — Wait for notifications

Each background process notifies on completion. Capture session_id for log retrieval.

### Step 5 — Convergence comparison

```bash
# Word count per draft
for f in output-*.html; do
  echo "$f: $(pdftotext "$f" - 2>/dev/null | wc -w) words"
done

# SHA-256 of each
sha256sum output-*.html

# Diff key sections
diff <(grep -A5 "PARADOX 1" output-qwen.html) \
     <(grep -A5 "PARADOX 1" output-deepseek.html)

# F13 SOVEREIGN picks from convergence report
```

### Step 6 — F13 disposition

F13 picks one draft (or composite of sections from multiple), applies F13 corrections, then dispatch.

## Mid-Stream F13 Correction Handling

F13 SOVEREIGN may issue corrections DURING the dispatch loop (after agents started, before HTML complete). This is constitutional behavior. The protocol:

1. **KILL all running dispatches** — they're working from stale spec.
2. **Update spec with version bump** (v1.0 → v1.1 → v1.2) and CHANGELOG entry.
3. **Re-dispatch** — F13 corrections ALWAYS WIN over agent polish.
4. **Honor the constitutional receipt** — apex_judge returning HOLD+F13_REQUIRED is the system working correctly.

**Anti-pattern:** Treating F13 corrections as suggestions. They are CONSTITUTIONAL EDITS — equivalent to changing the law, not the comment.

## Pre-Dispatch Filesystem Check

ALWAYS check filesystem BEFORE dispatching. There may be an existing artifact from a previous session:

```bash
# Search for existing drafts
ls -la /path/to/working-dir/*.html 2>&1
search_files(path="/path/to/working-dir", pattern="*v12*")
```

If an existing artifact exists and is well-formed, PATCH it instead of regenerating. This preserves work and reduces version drift.

(Verified pitfall: this skill's own origin — `surat-final-v12.html` already existed at 25KB when sovereign asked for "draft v12". 3 agents dispatched unnecessarily.)

## Pitfalls

### P1: Wrong provider/model ID
See `references/model-id-pitfalls.md` for the full matrix. Quick reference:
- `qwen -m qwen3-coder-plus` → invalid model name. Drop `-m` flag.
- `opencode run --model deepseek/deepseek-v4-pro` → insufficient balance. Use `opencode-zen/` prefix.
- `opencode run --model gpt-5.6-luna` → model not found. Use `opencode-zen/gpt-5.6-luna`.

### P2: Stale processes working on stale spec
After F13 correction, kill all running dispatches. They cannot see the new spec if they already started reading the old one.

### P3: Output file collision
Each agent MUST write to UNIQUE output path. If two agents write to `output.html`, the second overwrites the first. Naming convention: `output-{harness}.html`.

### P4: Different prompts = divergence, not independence
Gödel E3 requires SAME spec, different lenses. If you write three different prompts, you've engineered divergence, not independence.

### P5: Don't run all CLIs sequentially without time budget
Sequential dispatch takes 3x longer. Parallel dispatch (with 8s stagger) is faster but uses 3x memory. Choose based on system load.

### P6: Capturing logs vs just trusting exit code
Exit code 0 with ERROR output (model failed) means dispatch failed but shell didn't catch it. ALWAYS tail logs and check for ERROR strings.

### P7: Existing artifact not detected
If the user asks for "draft X" and X already exists, dispatching regenerates. Always `search_files` first.

## References

| File | What |
|------|------|
| `references/model-id-pitfalls.md` | Provider/model ID gotchas — the full failure matrix and verified working recipes. |

## Templates

| File | What |
|------|------|
| `templates/WORK_SPEC.md` | Canonical spec skeleton for multi-CLI dispatch. |

## Scripts

| File | What |
|------|------|
| `scripts/dispatch-three.sh` | Single-command 3-way parallel dispatch with stagger + log capture. |

---

DITEMPA BUKAN DIBERI — Forged, Not Given.

A sovereign-scale artifact deserves more than one lens. Three cognitive lenses from different model providers, on the same spec, is the minimum independence for F13 disposition.

## Routing notes (moved from description 2026-10-23)

Class-level umbrella for sovereign-scale work that benefits from independent cognitive lenses (multi-model consensus, multi-provider reasoning). Use when sovereign work requires more than one cognitive lens on the same artifact, or when the failure of a single model would compromise the artifact. Triggers include "dispatch to multiple agents", "parallel coding agents", "Gödel E3 independence", "3-way comparison", "sovereign petition forge", "multi-lens forge", or any high-stakes artifact where single-model output is unacceptable.
