# Agentic Dream Engine — Implementation Plan

## Scope

This plan implements Phase 0 + Phase 1 of the federation dream-engine extension:
1. **Phase 0:** Fix observed drift/bugs in the live nightly engine + add F1 snapshot.
2. **Phase 1:** Deploy Phase 2 weekly counterfactual rehearsal (`stage5_rehearse.py`).
3. Phase 2/3 (federation inbox, cross-warga recombination) are deferred until Phase 1 is sealed.

## Verified Live State

- Nightly dream-engine runs at 04:00 MYT via cron (`0 20 * * *`).
- 2026-06-16 run: 4.4s, 0 seals (quiet night), entropy decision = STEADY.
- Two bugs observed:
  - `consolidate.py` Supabase query fails: `column arifosmcp_memory_records.id does not exist`.
  - `entropy_controller.py` R6 vault read fails: `'str' object has no attribute 'get'`.
- arifOS + WEALTH systemd services are `active`; MCP attestation reports DEGRADED (probe mismatch).

## Deliverables

| File | Purpose |
|------|---------|
| `/root/.hermes/skills/dream-engine/scripts/stage5_rehearse.py` | Weekly counterfactual rehearsal (Phase 2 learning engine) |
| `prototype/systemd/arif-dream-phase2.service` | Systemd service for weekly rehearsal |
| `prototype/systemd/arif-dream-phase2.timer` | Systemd timer (Sunday 02:00 MYT) |
| `prototype/systemd/arif-dream.service` | Optional migration of nightly cron to systemd |
| `prototype/systemd/arif-dream.timer` | Optional nightly systemd timer |
| `prototype/openclaw_sleep_manager.py` | Reversible sleep-time compute prototype (deferred) |
| `prototype/morning_briefing_merge.py` | F1/F2 validation handshake (deferred) |
| `SKILL.md` | Federation dream-engine skill |

## Phase 0 — Safety Baseline (Kernel Health + F1 Snapshot)

1. Fix `consolidate.py` Supabase table/column mismatch.
2. Fix `entropy_controller.py` R6 vault read guard.
3. Add pre-seal snapshot to dream-engine stage4:
   - Before any write, dump dream-engine rows to `snapshots/memory_records_YYYY-MM-DD_HHMMSS.jsonl`.
   - Add rollback script: `rollback_dream_seal.py --date YYYY-MM-DD`.
4. Resolve MCP organ attestation degradation for arifOS/WEALTH.

## Phase 1 — Phase 2 Counterfactual Rehearsal

1. `stage5_rehearse.py` is already written and syntax-checked.
2. Default mode: `dry_run=True`.
3. Execute mode: `--execute` updates metadata only (survival) or emits alerts (fracture).
4. Systemd deployment:
   - Copy `arif-dream-phase2.service` and `arif-dream-phase2.timer` to `/etc/systemd/system/`.
   - `systemctl daemon-reload && systemctl enable --now arif-dream-phase2.timer`.
5. Monitor first run via `journalctl -u arif-dream-phase2.service -n 50 --no-pager`.

## Testing Plan

1. **Dry-run:** `python3 stage5_rehearse.py --dry-run`
2. **Execute on staging:** `python3 stage5_rehearse.py --execute` on a copy of `memory_records`.
3. **Verify audit rows:** `SELECT count(*) FROM memory_audit_log WHERE event_type LIKE 'rehearsal_%' AND session_id LIKE 'dream-rehearsal-%';`
4. **Verify alerts:** Check `/root/.hermes/cron/output/dream-engine/alerts.jsonl` for FRACTURE_HOLD entries.
5. **Verify report:** Check `/var/log/arifos/rehearsal-report-YYYY-MM-DD.md`.

## 888_HOLD Gates Summary

| Gate | Condition | Cleared By |
|------|-----------|------------|
| G0 | arifOS + WEALTH attestation fixed | Ops + Arif ack |
| G1 | Phase 2 systemd timer deployed | Arif |
| G2 | Federation inbox enabled | Arif (deferred) |

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Hallucinated counterfactual | Stub replaced with MiniMax-M3 + F2 witness before Phase 1 seal |
| Rule wrongly marked stress-tested | Confidence threshold + tri-witness check |
| Fracture false positive | Human reviews 888_HOLD alerts; no auto-amend |

## Rollback

If anything goes wrong:
1. Stop timer: `systemctl disable --now arif-dream-phase2.timer`
2. Remove service files: `/etc/systemd/system/arif-dream-phase2.*`
3. Revert metadata: restore from Phase 0 snapshot.
4. Clear alerts: archive `alerts.jsonl`.

---

*Forged: 2026-06-16 by FORGE (000Ω) — DITEMPA BUKAN DIBERI*
