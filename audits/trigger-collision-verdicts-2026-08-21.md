# Trigger-Collision Verdicts — 2026-08-21 (Door 3, F13 "execute all")

Cluster 1 (context-compress trio) EXECUTED today: FORGE-context-compressor v1.1.0
canonical (protocol absorbed), 2 retired to skills-retired-20260821/.
Remaining 14 verdicts below. Default owner: Hermes single-writer pass.

| # | Cluster | Verdict | Action |
|---|---------|---------|--------|
| 2 | apex_verdict_hold ↔ seal | KEEP-BY-DESIGN + DIFFERENTIATE | Fungsi berbeza (HOLD vs SEAL); trigger text identikal perlu dibezakan |
| 3 | observe-ground ↔ know-* | NARROW | observe-ground "fires on ANY claim" terlalu rakus — sempitkan ke non-domain claims |
| 4 | know-math/physics/language | KEEP-BY-DESIGN | Keluarga template sengaja; bezakan trigger ringan |
| 5 | memory-manage ↔ audit-seal | KEEP | Perkongsian session_end sahaja; risiko rendah |
| 6 | apex_scope_check ↔ floor_check | KEEP + DIFFERENTIATE | Scope vs floors = semakan berbeza |
| 7 | MCP cluster (6 skills) | MERGE-CANDIDATE (6→3) | ops+federation-ops→satu; smoke-test+probe+testing→satu; lifeguard kekal |
| 8 | hermes/openclaw/opencode families | KEEP-BY-DESIGN | Primitif per-harness sengaja (×3 agent) |
| 9 | pr-review/governance/precommit | KEEP-BY-DESIGN | 3 lapisan (policy/checklist/gate) |
| 10 | vps-docker ↔ vps-runbook | MERGE-CANDIDATE (weak) | Runbook jadi appendix docker |
| 11 | incident-escalation ↔ triage | KEEP + DIFFERENTIATE | Policy vs playbook |
| 12 | github-ops ↔ github-workflow | MERGE-CANDIDATE | ops masuk umbrella workflow |
| 13 | skill-creator ×3 | SINGLE-WRITER DECISION | FORGE-skill-creator + harness builtins kekal; create-skill (Grok) dinilai |
| 14 | code-review ↔ check-work ↔ review-agent | KEEP | Kimi-specific + builtin berbeza konteks |
| 15 | vss-parser ↔ vss-verifier | KEEP-BY-DESIGN | Parse vs verify bersebelahan sengaja |

Eksekusi hari ini: cluster 1 sahaja (blast radius rendah, provenance FI-008).
Cluster 7 & 12 = merge seterusnya paling berbaloi (6→3, 2→1). Lain-lain:
differentiate trigger lines, kerja ringan single-writer.
