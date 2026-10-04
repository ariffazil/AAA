---
name: federation-asset-probe
description: >-
  When asked whether the federation has a specific artifact, capability, or structure
  ("do we have X?", "what's the closest to X?", "where does Y live?"), probe the
  filesystem across organs to verify before answering. Distinguish doctrine from
  implementation, claimed from real. Reconcile memory with live state. Class of work
  is claim verification through federation-wide read-only reconnaissance — distinct
  from `arifos-integration-recon` (kernel code paths), `forge-federation-probe`
  (adversarial probe), and `federation-infra-verification` (live infrastructure).
category: autonomous-ai-agents
---

# Federation Asset Probe

Class of work: **verify claims about federation assets through filesystem reconnaissance**, then synthesize from evidence. Not a security audit (`kernel-security-claim-audit`), not kernel code path tracing (`arifos-integration-recon`), not adversarial probe (`forge-federation-probe`), not live infra probe (`federation-infra-verification`). This is the "what does the federation actually have?" layer — breadth-first across organs, depth where evidence demands.

## 1. When to load

Trigger phrases:
- "Do we have X?"
- "What's the closest thing to X in the system?"
- "Where does Y live?"
- "Is there a Z anywhere in the federation?"
- "Does the federation have…?"
- "Show me what we have for X"
- "What's already forged for Y?"
- "Evaluate what's the closest of X already forge in the system"

Do NOT load this skill for:
- Questions about doctrine/intent (load `arifos-*` doctrine skills)
- How to operate something (load the relevant ops skill)
- Deep code reasoning / refactor design (delegate to a coder agent)
- Live runtime probes (use `federation-infra-verification` instead)

## 2. The principle

> **Probe before claiming. Evidence before narrative.**

Memory about file paths and code structures can be stale. Federation is being built actively — files move, get renamed, get created, get dissolved. Any claim about federation state must be verified by live filesystem probe. Aligns with F2 TRUTH and the substrate principle `observe-ground`.

**Lesson learned 2026-08-11:** a memory note claimed `canon/world-model.yaml` was "Phase A live" — that file does not exist. The actual artifact was at `/root/arifOS/arifosmcp/runtime/world_model/world_model.py` (579 lines of real code). Memory can lie. Probe is authoritative. See `references/world-model-fragments-2026-08-11.md` for the full session.

## 3. Runbook

### Step 1 — Parse the claim
What is being asked? Existence? Location? Closest analog?
- "World model" → asset class breadth-probe
- "Where does X live?" → path probe
- "What's the closest to Y?" → breadth-first search with synthesis

### Step 2 — Identify probe scope
Common probe domains across the federation:

| Domain | Path |
|---|---|
| Constitutional kernel | `/root/arifOS/` |
| Execution | `/root/A-FORGE/` |
| Control plane + canon | `/root/AAA/` |
| Earth domain | `/root/GEOX/` |
| Capital domain | `/root/WEALTH/` |
| Human domain | `/root/WELL/` |
| Edge / Telegram | `/root/HERMES/` |
| Public surface | `/root/arif-fazil.com/` |
| Drafts / receipts | `/root/forge_work/` |
| Skills (current profile) | `/usr/local/lib/hermes-agent/profiles/aaa-hermes/skills/` |
| Memory (current profile) | `~/.hermes/profiles/aaa-hermes/memory/` |

### Step 3 — Run filesystem probe
```bash
# Pattern search across federation
search_files(pattern="X", target="files", path="/root")

# Targeted find, excluding noise
terminal: find /root -name "*X*" -type f \
  | grep -v node_modules | grep -v .venv | grep -v ".git/"

# Verify content (not just existence)
read_file(path="/path/to/found/file", limit=80)
```

### Step 4 — Triangulate
A real artifact will show up in multiple places. Probe for:
- **Code module** (the implementation)
- **Test file** (proves it runs)
- **Documentation** (proves it's intended)
- **Schema definition** (proves it's typed)
- **Runtime state** (proves it's deployed)
- **Reference in another module** (proves it's used)

A single hit is not proof of substance. Triangulation is.

### Step 5 — Synthesize with evidence
Quote specific paths, line counts, key declarations. Classify each finding into one of four states:

| State | Meaning |
|---|---|
| **Forged and active** | Real code, recent commits, F11 provenance, tests pass |
| **Forged but dormant** | Exists but unused or underused |
| **Referenced but absent** | Mentioned in docs/canon, not yet implemented |
| **Wired but broken** | Pipeline exists and is enabled, but a runtime dependency (engine, key, package) is missing — repair the wire, don't rebuild the capability |
| **Absent** | No trace anywhere |

### Step 6 — Acknowledge staleness
If memory and probe disagree, **probe wins**. Update memory if the durable truth has shifted. Note the disagreement in the response — don't silently overwrite.

## 4. Pitfalls

- **Memory drift.** Notes about file paths may be weeks old. Federation evolves fast. Probe-first, memory second.
- **Doctrine ≠ implementation.** A canon file may describe a structure not yet coded, or vice versa. Both can be true at different layers.
- **Naming collisions.** "world-model" might mean YAML canon, Python module, MD doc, or skill manifest. Verify which — read it before claiming.
- **Hidden depth.** A "draft" file might be 579 lines of substantive code. Always `read_file` before judging maturity.
- **Surface-only probe.** Finding ONE match is not enough. Triangulate across code, tests, docs, runtime.
- **Symlink traps.** Federation has many symlinks (e.g. `/root/VAULT999` → `/root/arifOS/VAULT999`). Probe can resolve to wrong canonical path.
- **Cross-profile write.** Current session reads/writes only the active profile's skills/plugins/cron/memories. Federation assets are at `/root/`, not in profile dirs — don't confuse them.
- **Pruning by looking redundant.** Fitness test (Arif 2026-08-09): same outcome + higher cost + more complexity + less lineage = retire. But VERIFY redundancy before retiring — don't delete what looks unused.

## 5. What to report

- Specific file paths (absolute, not relative)
- Line counts and code structures for each finding
- Quoted excerpts of key declarations (class names, method signatures, floor bindings)
- The four-state classification for each asset
- The gap between claimed (doctrine) and real (probe)
- Where to look for canonical answer (which file is SOT)
- When memory and probe disagree: report both, prefer probe

## 6. What NOT to do

- Answer from memory alone
- Trust doctrine docs without probing implementation
- Claim "we have X" without file evidence
- Conflate "referenced in canon" with "implemented in code"
- Skip the read step because search found something
- Probe one organ only when claim is federation-wide
- Treat a single grep hit as proof of substance
- End with "Should I publish this?" or "Proceed?" for what is already evident

## 7. Related skills (do not duplicate)

- `arifos-integration-recon` — depth-first arifOS kernel code path tracing (different scope)
- `forge-federation-probe` — adversarial probe (different intent)
- `federation-infra-verification` — live infrastructure probe (different surface)
- `AUDIT-recursive-audit` — multi-surface skill audit (different unit of analysis)
- `AUDIT-drift-detector` — drift detection across tool manifests (different question)
- `observe-ground` (substrate) — evidence-before-narrative principle (this skill operationalizes it for federation assets)

## 8. Reference files

Session-specific findings live in `references/`. Add a new file per major probe session, dated, with specific file paths and structures captured. Keep entries concise — distilled knowledge, not full source mirrors.

| Reference | Captures |
|---|---|
| `references/world-model-fragments-2026-08-11.md` | 6-fragment world model map across arifOS/GEOX/WEALTH/WELL/Atlas333/CIV-21; memory-staleness lesson |
