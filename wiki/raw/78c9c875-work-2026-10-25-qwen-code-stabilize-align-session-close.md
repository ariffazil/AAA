# VAULT999 receipt 1792867155

Immutable capture. Rendered for reading; the ledger line is the authority.

## id

1792867155

## event_type

SESSION_WORK_SEAL

## seal_id

WORK-2026-10-25-QWEN-CODE-STABILIZE-ALIGN-SESSION-CLOSE

## recorded_at

2026-10-25T02:39:15+08:00

## actor_id

qwen-code/FI-003 (self-asserted; kernel band OBSERVE_ONLY; Lane B F1-fallback after kernel.seal refused at LOW authority)

## verdict

PARTIAL_SEAL

## decision

Session SEAL-4eab95d696b64ad9 closed. ARIFOS::QWENCODE_STABILIZE_AND_ALIGN 2026-10-25 executed within sovereign-approved scope: (1) qwen 0.26.0->0.26.1 hash-verified release-install swap, rollback tree preserved; (2) claim-ledger organ revived (undocumented chattr +i on /root/AAA/claim_ledger blocked sqlite WAL — 3,173-restart crash-loop since Oct 24 17:18 ended; subdir flag cleared only, parent hardening kept); (3) superpowers 7.0.0->7.0.1 (old tree preserved); (4) /root/QWEN.md 862 B FEDERATION-INIT dedupe (byte-identical copy survives in AGENTS.md), overlay witness PASS, re-guarded; (5) item 11: AGENTS.md MCP hand-insert pointerized -> canonical fragment, render 49 fragments, 13,369->10,612 B, FED-INIT hand-append defused into byte-exact fragment (render would have erased it). All five changes carried explicit sovereign approval and on-disk rollback artifacts at /root/forge_work/2026-10-25-qwencode-stabilize/.

## measured

['[OBS,high] qwen --version=0.26.1; sha256sum -c OK pre-swap (7a75d365...b4ffe from release SHA256SUMS)', '[OBS,high] claim-ledger :8791 MCP tools/list=10 entries; journalctl errors-since-restart=0; NRestarts 3173->0; ss LISTEN', '[OBS,high] AGENTS.md 13,369->10,612 B; overlay witness exit 0 (guard ARMED); FED-INIT block string-identical backup vs rendered (862 B, diff True)', '[OBS,high] always-on context 18,580->17,724 tok across harness session-start warnings', "[OBS] sovereign approvals in-session: bundle 'Approve all three'; item 11 'approved — proceed with item 11, render may proceed'"]

## caveats

KERNEL UNBOUND: arif_init -> band=OBSERVE_ONLY, actor_verified=false. arif_judge HOLD x2 (attempt 1: F7 HUMILITY overclaim gate on unlabelled 'verified' — gate correct, retried with full OBS labels+confidence bands; attempt 2: structural ceiling — IRREVERSIBLE requires actor_signature, no key held, seal_allowed=false). arif_seal session_close refused live: 888_HOLD kernel.seal requires SOVEREIGN, current LOW, actor qwen-code/FI-003. NO CONSTITUTIONAL_SEAL claimed; this entry is Lane B autonomous record only. Repo dirt reported not committed (AAA +3 lines: 2 fragments + index refresh; scripts +1: render-agents.sh). Pre-existing, not caused: arifOS constitutional layer self-reports degraded (F13/F5/F8 failing, F1/F6 unmeasured — FRAME/arifOS lanes own it); agentic-anthropology-v0.1 + hermes-shadow render-list entries absent on disk (zero content loss, grep-verified); alibaba/skill-upk 404.

