# 2026-06-07 — dream_engine v0.1 forged

**Session:** ses_15e2f80d1ffeQQVr6hXEq5s2wx (post-reset)
**Trigger:** Arif asked "How should we forge dream engine?" in group AAA (#29411)
**Authority:** F13 SOVEREIGN waived for this session (per 2026-06-06 17:26 UTC directive)

## What was built

9 files, 100KB total, at `/root/.openclaw/workspace/dream_engine/`:

```
dream_engine/
├── DESIGN.md              # 4.9KB — full architecture, 3-phase cycle, 5 passes
├── SKILL.md               # 2.0KB — OpenClaw skill description
├── dreams/
│   └── consolidate.py     # 11.3KB — Nightly pass: L1/L2/L3/L4 audit + shadow ns
├── scheduler/
│   ├── dream_cron.sh      # Wrapper for nightly/weekly/monthly
│   ├── dream_cron.service # systemd unit
│   └── dream_cron.timer   # 04:00 MYT (20:00 UTC) nightly
├── state/
│   ├── manifest.yaml      # Schedule contract
│   └── last_dream.json    # Rolling 30-run history (live, audit trail)
└── tests/
    └── golden_dreams.py   # 7 tests, all pass
```

## Honest test results

- ✅ 7/7 golden_dreams tests pass
- ✅ L1/L2 Redis: 1 key scanned, all <1h TTL
- ✅ L3 Qdrant: 5 collections found (arif_evidence, arifbrain_states, arifos_l5_graph, arifos_memory, mcp_capabilities) — matches HEARTBEAT "5 colls"
- ⚠️ L4 Supabase: 401 on real run (env var truncation, not a dream engine issue)
- 🔒 Cutover blocked at L4 — sovereign-tier action, must use /forge

## Architectural decisions (mine, awaiting Arif)

1. **Substrate, not LLM.** Dreams run as cron Python, not in-me. LLM only for cross-domain synthesis in recombine.py.
2. **Shadow namespaces.** All writes go to `qdrant_v2_<date>` first, 7-day dual-write, atomic cutover.
3. **L6 stays sovereign.** Dreams never touch VAULT999. The dream never sleeps there.
4. **Authority tiers:**
   - T1 (consolidate, defuse, housekeep) = L4 autonomous in F13-waived
   - T2 (rehearse, recombine) = L5, needs L11 Ed25519 sig
   - T3 (constitutional, witness) = L6, sovereign only

## Open design questions (sent to Arif, awaiting response)

1. Dedup threshold: 0.90 (my pick), 0.95 (strict), 0.85 (loose)?
2. LLM in recombine.py: local ollama bge-m3 only (free) or hit MiniMax-M3 (paid, better synthesis)?
3. Schedule: 04:00 MYT nightly (my pick, deep-sleep window) or 02:00 MYT (Arif's sleep, lower load)?

## Reversibility

```bash
systemctl disable --now dream_cron.timer
rm -rf /root/.openclaw/workspace/dream_engine/
```

No state outside the directory. No L6 touch. Fully reversible. F1 Amanah ✅.

## What this does NOT do (F2 truth)

- Does not yet run on a schedule (timer not activated)
- Does not yet write shadow namespaces (only audits)
- Does not yet re-embed (would need ollama call, deferred to weekly)
- Does not yet do creative recombination (Phase 2)
- Does not yet do constitutional recalibration (Phase 3)
- Does not touch L6 VAULT999 (sovereign)
- Does not touch L7 AAA (sovereign)

## Next steps (mine, pending Arif go)

1. Wire systemd timer: `systemctl daemon-reload && systemctl enable dream_cron.timer`
2. Wire defuse.py + housekeep.py (small, ~100 lines each)
3. Wire weekly/monthly (rehearse + recombine, harder)
4. Add the OpenClaw skill registration so the gateway knows about dream-engine

## Carry forward

- F2 finding: empty Redis on this system (1 key). Real L1/L2 traffic is in arifOS kernel, not exposed to dream engine yet. Need to find the right connection point.
- F2 finding: ollama bge-m3 not tested yet. Need to verify it serves 1024-d embeddings as expected.
- F2 finding: HEARTBEAT says "3,588 pts / 5 colls" but Qdrant only reports collection names, not point counts. Need a count() call per collection to confirm.
