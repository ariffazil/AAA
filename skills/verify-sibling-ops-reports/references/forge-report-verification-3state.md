# Forge / Audit Report Verification — 3-State Evidence Discipline

> Loaded when a sibling agent or co-forge delivers a cleanup/ops/audit/seal report and you need to verify it against live state. Patched in 2026-08-08 after the AAA Zen Alignment audit (333-AGI self-audit + external review + corrections flow) demonstrated the full pattern.

## The 3 states — modified ≠ committed ≠ sealed

A report claiming "done", "synced", or "sealed" can be in any of three states. All three are real; only the third is constitutional.

### State 1 — Modified (working tree dirty)

```bash
git -C <repo> status -s           # M / ?? entries
git -C <repo> diff --stat HEAD    # what changed since last commit
```

A sibling saying "I synced dist/ and public/" with `git status -s` showing `M` entries has **modified but not committed**. The state exists only on disk and can disappear at any time.

### State 2 — Committed (HEAD moved)

```bash
git -C <repo> log --oneline -3
git -C <repo> show HEAD:<path> | sha256sum   # verify content matches what report claims
```

Cross-verify SHA256 claims from the report:
- Working tree: `sha256sum <path>`
- Committed state: `git show HEAD:<path> | sha256sum`

Both must match the report's claimed SHA. Two agents committing to the same file across sessions can cause drift — `git log --oneline -5` to spot it.

### State 3 — Sealed (VAULT999 receipt exists)

```bash
# Quick check
grep "COMMIT-<repo>-<sha>" /root/arifOS/VAULT999/outcomes.jsonl

# Or ingest new HEADs (auto per session)
python3 /root/HERMES/scripts/zen/git_to_vault.py
```

"Convention" vs "constitution": a commit without a VAULT999 receipt is just committed, not sealed. The `git_to_vault.py` ingestion produces COMMIT_RECEIPT entries automatically per session. **Distinct from `arif_seal`**, which is the kernel-level verdict (F1-F13 gate) — those can lag behind git_to_vault by days. Don't conflate.

## Live-probe pattern — beat prose claims with organ health

A self-audit claimed "FRAME not implemented — W-vectors unmeasured." Live probe disagreed:

```bash
curl -sf --max-time 3 http://127.0.0.1:18085/health | python3 -m json.tool
# → status: ok, chambers: {baseline, probe, compare, trend, alert, report, rsi_verify: all active}
```

Generalize: **for every organ-status claim in a report, probe `:port/health` directly**. Organs to probe by default:

| Organ | Port |
|---|---|
| arifOS Kernel | 8088 |
| A-FORGE API / MCP | 7071 / 7072 |
| arifFLOW | 7073 |
| AAA A2A Gateway | 3001 |
| GEOX | 8081 |
| WEALTH | 18082 |
| WELL | 18083 |
| FRAME | 18085 |
| SIGNAL | 18084 |
| FLAME | 18901 |

## Semantics-drift catches (field presence ≠ semantic correctness)

Sibling wrote `"priority": "PRIMARY", "replaces": ["codex", "claude-code"]`. Verified in working tree, but `"replaces"` semantically implies deletion — yet vendor cards still existed on disk. Catch this by reading the field's downstream consumer: does the A2A router treat `"replaces"` as deletion or fallback order? When ambiguous, recommend rename to `"routing_priority": "PRIMARY"` + `"fallback_to": [...]` for clarity. Field presence ✓ ≠ semantic correctness.

## Conditional SEAL flow (worked example: AAA Zen Alignment audit 2026-08-08)

When a sibling self-audit lands:

1. **Verify SHAs** — table with 5 artifact paths, claimed SHA, live SHA, MATCH/MISMATCH verdict. 5/5 match → evidence chain intact.
2. **Verify substantive claims** — go through each "Change" or claim line and check live state. For each: TRUE / FALSE / UNDER-RATED / PARTIAL.
3. **Independence check** — was the audit authored by the same lane being audited? AAA_TOOL_RIGHTS_POLICY: a-auditor cannot self-approve. If self-audit, compensate by requiring transparent risk flagging AND an external reviewer (you).
4. **Score under-rating** — if the report self-scored audit independence at 2/10 but live state has A-auditor role + FRAME + tool-rights policy + F11/F12 floors, propose the honest 6/10 with an evidence table.
5. **List corrections required** — specific, falsifiable, each cite the live state.
6. **Corrections round** — re-verify each correction against live state. If accepted, move to CONDITIONAL SEAL.
7. **VAULT999 seal** — `git_to_vault.py` auto-ingests. If arif_seal-level verdict required, route to F13 sovereign.

## EXISTS vs INTENDED table format

Present verification findings as a 3-column table:

| Claim | Live state | Verdict |
|---|---|---|
| `"priority": "PRIMARY"` in opencode.json | L18 ✓ | EXISTS |
| `bound_to: "333-AGI"` unchanged | L25, L598 ✓ | EXISTS |
| `888-APEX` card no `species` field | python3 -c '... "species" in d' → False | EXISTS |
| Public card synced to `public/a2a/opencode.json` | Both have priority/replaces/bound_to | EXISTS |

This scans fast for Arif and makes the gap explicit. Always include in audit responses.

## When NOT to accept a sibling report

- Missing SHA256 evidence for claimed mutations
- "Sealed" claim without VAULT999 receipt
- Implementation-status claims that contradict live `:port/health`
- Self-audit that scored itself without external reviewer
- Field semantics ambiguous between intent and literal interpretation
- Working tree dirty at the end of a "commit complete" report
