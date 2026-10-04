---
name: canon-integrity-check
description: "Cross-reference live multi-repo state (live git, systemd, disk) against declared canon registries (web-canon federation.json + sites.yaml) to find drift, then patch the registries (NOT the live code) where drift is real. Class-level skill for 'audit the deployment', 'are repos registered?', 'what's missing from the registry?' tasks. Recurring failure mode: external auditors read wrong registry shape, conclude 'absent from canon' — verify the schema first."
---
# Canon Integrity Check

Class: cross-repo declared-vs-live drift audit + reversible patching.

## The recurring trap (verified 2026-08-07/08)

External auditors (Gemini/Claude/EMD) read a registry, assume a wrong
schema shape (e.g. look for `id` instead of `asset` key), conclude
"6 repos absent from canon," and propose phantom registrations for
things already declared. This pattern hit twice in two days.

**Defense:** probe the registry's actual keys BEFORE computing any delta.

```bash
python3 -c "
import json; d = json.load(open('/root/web-canon/canon/federation.json'))
print('keys:', list(d.keys()))
print('asset keys:', list(d['assets'][0].keys()))
print('assets:', len(d['assets']), 'organs:', len(d['organs']))
"
```

## 5-step workflow

### 1. Live inventory

```bash
find /root -maxdepth 3 -name ".git" -type d 2>/dev/null \
  | sed 's|/\.git$||' \
  | grep -vE "node_modules|\.venv|\.local|\.openclaw/workspace|forge_work" \
  | sort
```

For each: remote-url, last-commit-date, size.

### 2. Read registry schema (MANDATORY — before computing any delta)

Registries at `/root/web-canon/canon/`:

- `federation.json` — `organs[]` (shape: `{organ:"X", layer:"L1", ...}`) + `assets[]` (shape: `{asset:"X", layer:"L3", ...}`).
- `sites.yaml` — public surfaces: `path:`, `role:`, `posture:`, `deployable:`.
- `atlas.yaml` — UI design canon (not for repo audit).

### 3. Compute deltas (with confirmed schema)

Match on github field's last segment. Compute live-minus-declared and
declared-minus-live.

### 4. Four drift classes

| Class | Signal | Action |
|---|---|---|
| Undeclared runtime organ | Live systemd, in federation graph, no registry entry | Add to `organs[]` |
| Declared but stale | In registry, wrong posture/port/deployable | Patch registry |
| Declared but gone | In registry, runtime absent | Relabel L4 or delete |
| Ghost audit premise | Auditor says absent but you can grep it | **Reject the claim** |

Gemini's 2026-08-07 "6 unregistered repos" = ALL Class 4 (already in
`assets[]` with `asset` key, auditor was looking for `id` key).

### 5. Patch registry — NOT live code (unless Class 1)

Commit message must document rejection for Class 4, so future sessions
learn the schema trap.

## Operational guardrails

- **GitHub protected branches** reject `push origin main`. Use feature
  branches: `git checkout -b feat/x && git push -u origin feat/x`.
- **F1 quarantine-first.** `mv` to `_quarantine/` before `rm`. FRAME
  source recovered via `/root/_quarantine_FRAME_20260807/` on 2026-08-08.
- **Wants= is NOT injection.** Same `Wants=arifos aforge` across 7+ organs.
  EMD's "FRAME = F12 injection because Wants=" was wrong.
- **De-duplicate entries.** Check `organs[]` + `assets[]` after patching.
- **Remoteless repos need `gh repo create` first** before push.
- **Don't trust auditor delta counts.** Schema shape mismatch inflates them.
- **Always read the runtime source.** systemd `WorkingDirectory` is the
  truth, not git log or `ls /root/<x>` (source may be at `/opt/<x>` after deploy).

## ## Related Skills

- **documentation-tier-management** — next step after this check if 300+ MD files accumulate in a canon repo. Classifies into tiers (B=federated, C=operational, D=proof, DELETED→extract+remove). Never merge everything into SOT — use tiered pointers instead.

Doctrine-to-runtime wiring audit (verified 2026-08-08)

Sibling class: "Is X wired?" — a doctrine/architecture exists as files, but
does any runtime actually consume it? Arif asked whether the double-helix
memory was wired into Hermes + other agents. Files existed; nothing consumed
them. **FORGED ≠ WIRED.** Audit both, separately.

### 5-layer evidence ladder (ascending proof)

| Layer | Check | Command |
|---|---|---|
| 1. Doctrine exists | forge_work reflection + governance docs | `ls /root/forge_work/*HELIX*` |
| 2. Machine scaffold executed | schema + seed + verify script on disk | `ls /root/.local/share/arifos/scars/` |
| 3. Kernel runtime consumes it | grep kernel source for the concept | `grep -rn "scar\|helix" /root/arifOS/arifosmcp/tools/` |
| 4. Seal/data path carries it | count extension fields in VAULT999 | `grep -c "meaning_anchor" /root/arifOS/VAULT999/outcomes.jsonl` |
| 5. Agent configs reference it | grep all agent homes | `.claude/settings.json`, `AAA/agents.yaml`, `.arifos/agents/`, `.config/opencode/` |

Verdict taxonomy: **FORGED** (1–2 only) · **PARTIALLY WIRED** (advisory-only
contact) · **WIRED** (3–5 all hit). Evidence that matters: grep counts and
receipt field counts, not file existence.

### Pitfalls (all hit this session)

- **Advisory contact ≠ pathway.** `heart.py` reads scar taxonomy as F5/F6
  advisory context — that is NOT a memory pathway. `arif_memory` having zero
  scar references is the real verdict. Distinguish "tool mentions X as context"
  from "recall/seal path carries X".
- **`grep -c` exit code 1 = zero matches = evidence**, not error. 0/43,886
  receipts with `meaning_anchor` is a decisive finding.
- **Kernel `tools/list`:** GET on `:8088/tools/list` → 405. Use
  `curl -s http://127.0.0.1:8088/health` for liveness; the MCP surface needs
  the jsonrpc POST envelope. Health endpoint is the reliable probe.
- **Registry vs scaffold split:** `/root/memory/H5-scars/H5_SCAR_REGISTRY.json`
  is the index; `/root/.local/share/arifos/scars/` is the machine scaffold.
  Never merge — the H5 doctrine forbids it.
- **Sovereign-boundary facts:** scar content is read only when `scar:<id>` is
  invoked; index reads are permitted. Audit the wiring, never the scar content.
- **Wiring gap maps to a named gap in the gap ledger** (e.g. Gap 6
  SOVEREIGN_WAIT) — cite the ledger, don't re-derive the diagnosis.

## Output shape

Verdict table per row: Claim ID, Claim Text, Live Evidence (command + output),
Verdict (CONFIRMED / REJECTED / PATCHED). Then patch + commit + push + PR link.

## Reference files

- `references/wants-pattern-is-not-injection.md` — systemd Wants= evidence across all 9 organs
- `references/framing-example.md` — correct JSON shape for adding an organ to federation.json
- `references/double-helix-wiring-audit-2026-08-08.md` — full evidence for the doctrine-to-runtime wiring audit (double-helix memory: FORGED not WIRED)