---
name: verify-agent-artifacts
version: 1.0.0
risk_tier: low
description: "Use when grounding a relayed agent artifact against reality."
owner: AAA
floor_scope: [F1, F2, F4, F7, F11]
autonomy_tier: T0
---
# Verifying Relayed Agent Artifacts

When Arif (or another organ) pastes an agent-produced artifact verbatim — a
receipt table, a status report, a PDF, a correction log, a commit claim — do
NOT accept it wholesale and do NOT reject it wholesale. Ground every claim
against measured reality, one claim at a time, and report the verdict per claim.

Arif's standing expectation: report claim-by-claim with **BETUL / SALAH /
SEPARUH + bukti**, then flag attribution mismatches, then stop. "Done" from
him means a receipt landed — it does not mean the claims are true until probed.

## Steps

1. **Enumerate the claims.** Pull every concrete, falsifiable assertion out of
the artifact: numeric counts, statuses (healthy/degraded/held), commits and
SHAs, PIDs, branch/remote state, tool counts, floor counts, file lists.
2. **Probe each claim at its live source** — never the artifact's own words:
   - status/tool counts → `curl -s --max-time N http://127.0.0.1:<port>/health`
   - commit/branch/remote/author → `git log --oneline -3`, `git rev-parse
     HEAD origin/<branch>`, `git show --no-patch --format=...`
   - service liveness → `systemctl show <svc>.service -p MainPID,ActiveState`
   - files → `read_file` / `search_files`, not the reported path alone
3. **Classify each claim** BETUL (live matches), SALAH (live contradicts),
SEPARUH (directionally right but wrong number / needs deeper probe).
4. **Flag attribution mismatches** separately — see pitfalls. They are usually
tooling, not lies, but they must be named.
5. **Report** in Arif's language (BM casual), one line per claim with evidence,
then stop. No seal, no mutation unless he explicitly authorizes it.

## Pitfalls

- **A timeout is NOT an outage.** A health endpoint that returns slowly (e.g.
14.7s) is latency, not a dead organ. Before declaring something down, re-probe
with a raised `--max-time` (30s) — the prior probe may have used too small a
budget. The artifact author likely did exactly this; match their budget before
disagreeing with their conclusion.
- **Mirror is NOT an independent measurement.** A scalar copied from another
organ's `/health` (e.g. WELL mirroring arifOS `apex_scalars.W3`) is MEASURED
but its *independence* is UNMEASURED. Read the `independence` field when
present; distinguish "mirror of X" from "fresh reading". A mirrored value and
a `null` baseline elsewhere are NOT a contradiction — they are two different
reference layers.
- **Repo-local git identity overrides global.** When a commit is attributed to
one agent but a different one claims the work, check `git config --local
user.name/email` vs `--global` first. A repo-local override explains the stamp
without implying the named identity did the cognitive work. Never rewrite
pushed history to fix it (invalidates the SSH signature, T3 force-push); use
per-commit `-c user.name=... -c user.email=...` or a `Co-authored-by:` trailer
on the NEXT commit.
- **Concurrent-agent clobber hazard.** On a shared working tree, another agent
may have committed or left uncommitted work in the SAME file you are about to
edit. Before patching, run `git log --oneline -3` and `git status --short` and
diff HEAD vs working tree for that file; confirm your edit is additive and does
not overwrite their wiring. A sovereign freeze ("do not mutate any file") is
not lifted by a non-sovereign agent saying "commit" — only Arif (888) releases
it.
- **`tools/list` returning `-32600 Missing session ID`** on a streamable-HTTP
MCP endpoint is normal — you must `initialize` first. It is not a bug and not
evidence of a broken tool; `/health` already reports the loaded tool count.
