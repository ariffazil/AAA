# Receipt-first verification before retirement — reference transcript

**Date:** 2026-08-11, MYT 09:35–09:50
**Trigger:** 23-cron audit produced 3 obvious-kill candidates (`hermes-dna-metrics-refresh`, `rehat-minda-logistics`, `provenance-audit`). User directive at 09:35: "Start full execution. Make sure cron job tak makan token berlebihan and ada value to the system."

## Initial instinct (wrong path)

Plan was to kill the 3 cron bodies + convert 5 agent-driven crons to `no_agent=true` based on heuristic reasoning:
- 3 crons had no live downstream consumers (probe confirmed)
- 5 agent crons had prompts that read like script specs (`python3`, `ls -la`, `du -sh`)

Total proposed: 8 mutations in one T2 patch.

## User pushback

F13 SOVEREIGN returned an **advisory verdict** structure (third-party AI format, not direct command):

> "If verified true, this is a classic entropy source: 1 outcome, 2 jobs"
> "Your federation is now mature enough that deletion should never be justified by 'It looks redundant.' Instead: Verify redundancy. Measure utility. Retire the less-fit implementation."
> "Not: observe → kill. But: observe → verify → receipt → retire → witness"

## The 6-step pattern that worked

```
1. Identify candidate pairs by NAME/SCHEDULE/DELIVER similarity
2. For EACH pair, verify 4 dimensions:
   - schedule_match:     parse cron expression, compare
   - deliver_target:     compare chat_id / path / mode
   - data_source:        compare file paths in prompts/scripts
   - output:             run scripts, compare last lines / format
3. Generate per-pair verification receipt at:
   /root/forge_work/verification/<date>-verification-receipts.json
4. Apply verdict per pair (NOT_DUPLICATE / DUPLICATE_WRITER / ORPHAN_WRITER)
5. Retire only confirmed low-fitness implementations
6. Update lineage + commit + receipt
```

## Verified cases

### Case 1: `arifflow-daily-digest` vs `arifflow-daily-governance-digest`

Both: schedule `0 22 * * *`, deliver `telegram:267378578`. LOOKS identical.

| Check | digest | gov |
|---|---|---|
| script path | `/root/HERMES/scripts/arifflow_digest.py` | `/root/forge_work/ariflow-audit/scripts/governance_digest.py` |
| data source | `/root/arifOS/VAULT999/arifflow_sealed.jsonl` (history) | `/var/lib/arifflow/receipts.jsonl` (live) |
| output | "🍓 Governance Digest" — priority-sorted events, FQ state, daemon health, override count | "WHY Bridge" — receipts-by-step, top actors, open/closed loops |
| epistemic frame | state snapshot | workflow narrative |

**Verdict:** NOT_DUPLICATE — different functions. Both kept.

### Case 2: `vault-data-refresh` (Hermes L2) vs `/etc/cron.d/arifos-vault-tail` (system)

Both: write JSON to webroot. LOOKS duplicate.

| Check | Hermes | cron.d |
|---|---|---|
| schedule | every 15min (after lane-routing optimization) | every 1min (`*/1 * * * *`) |
| output path | `/var/www/html/arif/999/vault-data.json` | `/var/www/html/999/vault-data.json` |
| source | `/root/arifOS/VAULT999/outcomes.jsonl` | `/root/.local/share/arifos/vault999/seal_chain.jsonl` |
| consumer | Caddy `@validation` rule serves via `strip_prefix /999` → root `/var/www/html/arif/999` | **NONE** — no Caddy route, file is orphan |
| output file mtime | 09:42 MYT (recent, healthy) | 20:20 MYT (13h stale despite 1m schedule → silent failure) |

**Verdict:** DUPLICATE_WRITER + ORPHAN. Hermes wins (canonical, consumed). cron.d loses (orphan, silent failure, write amplification).

### Case 3: Live probe of orphan detection

```bash
# 1. Find cron.d entries writing to webroot
grep -rE "/var/www/html|chown www-data" /etc/cron.d/

# → /etc/cron.d/arifos-vault-tail: writes /var/www/html/999/vault-data.json

# 2. Check consumer via Caddy route
grep -E "999|vault-data" /etc/caddy/Caddyfile

# → @validation strip_prefix /999, root * /var/www/html/arif/999
# → only arif/999/ is served, not /999/

# 3. Compare output mtime to schedule
stat -c '%y %n' /var/www/html/arif/999/vault-data.json /var/www/html/999/vault-data.json
# /var/www/html/arif/999/vault-data.json: 2026-08-11 09:42:08 (fresh)
# /var/www/html/999/vault-data.json:        2026-08-10 20:20:42 (13h stale)

# 4. Check log for cron.d success vs output freshness
tail -20 /var/log/arifos-vault-tail.log
# → "OK: vault-data.json refreshed" lines every 6 minutes
# → but file mtime says 13h stale = writes failing silently
```

The "OK" log lines are a lie. Cron.d reports success because the script `exit 0`s after the `tail | python3` pipeline, but the file write to a Caddy-served path was never in the path the consumer reads. **This is the canonical silent-failure mode.**

## Cost of the heuristic-only path (counterfactual)

If we had proceeded without verification, we would have:
- Killed `arifflow-daily-governance-digest` — losing the WHY Bridge + epistemic status output that the digest doesn't produce
- Kept `vault-data-refresh` (right) AND `/etc/cron.d/arifos-vault-tail` (wrong) — double-writer amplifying writes with no consumer benefit

Net: lost complementary coverage, kept orphan, no savings.

## Cost of the receipt-first path (actual)

- 2 verification receipts generated (~5KB each)
- 1 NOT_DUPLICATE decision documented (no mutation)
- 1 DUPLICATE_WRITER decision documented (cron.d retirement queued)
- All 20 cron bodies preserved, semantics intact, fitness gaps clear

Net: zero accidental capability loss, clear retirement lineage.

## F13 advisory verdict format (template)

When F13 SOVEREIGN returns advisory verdict (third-party AI evaluation), structure is:

```yaml
EVIDENCE: what was observed (claims, file paths, mtime)
P0:      first priority — observation/verification
P1:      second priority — fitness comparison
P2:      third priority — retirement ritual
Survival-of-the-fittest interpretation:
  Same outcome + higher cost + more complexity + less lineage → retire
Recommended order:
  1. Verify duplicate
  2. Generate receipt
  3. Retire
  4. Update lineage
Not: observe → kill
But:  observe → verify → receipt → retire → witness
```

**Treat advisory verdict as additional evidence layer, NOT as final verdict.** The Doer must still:
1. Run the verification the advisory requests
2. Generate the receipts the advisory demands
3. Apply own judgment on whether the advisory's retirement recommendation matches live fitness

Advisory verdict ≠ sovereignty seal. Sovereign seal = Arif direct command. Advisory = "here is a fitness framework, apply it."

## Reusable receipt schema

```json
{
  "schema": "arifos.evidence.v1",
  "case_id": "<DOMAIN>_DUPLICATE_VERIFICATION_<DATE>",
  "doer": "Hermes (lane=arif, actor=ariffazil)",
  "candidate": "Receipt-first duplicate verification before retirement",
  "verifications": [
    {
      "id": "V1",
      "candidate_pair": "<name_A> vs <name_B>",
      "candidate_to_retire": "<the one we suspected>",
      "checks": {
        "schedule_match": {"value": true|false, "evidence": "..."},
        "deliver_target_match": {"value": true|false, "evidence": "..."},
        "data_source_match": {"value": true|false, "evidence": "..."},
        "output_match": {"value": true|false, "evidence": "..."}
      },
      "verdict": "NOT_DUPLICATE | DUPLICATE_WRITER | ORPHAN_WRITER",
      "recommendation": "KEEP both | RETIRE <X> | RETIRE <X> + <Y>",
      "fitness_comparison": {"<A>": "...", "<B>": "..."}
    }
  ],
  "doctrine_check": {"F1_amanah": "...", "F11_auditability": "...", "F13_sovereign": "..."},
  "next_action_proposed": {"<case>": "..."}
}
```

## Triggers to load this reference

- A cron audit surfaces multiple "redundant-looking" candidates
- A user directive says "make sure X has value to the system" (quality-of-output audit)
- A user directive says "kill the duplicates" (verify before killing)
- A cron.d / systemd timer / external scheduler conflicts with Hermes L2 cron
- An apex-judge isolate returns HOLD/VOID with "duplicate_writer" or "orphan_writer" reason codes

## Anti-patterns (don't do these)

- "Same name substring → must be duplicate" → wrong, distinct functions often share substrings
- "Same schedule + same deliver → must be duplicate" → wrong, common pattern for paired jobs (digest + governance digest both at 22:00)
- "Same output format (JSON) → must be duplicate" → wrong, format ≠ function
- "Retire then verify what we lost" → wrong, verify FIRST, retire second
- "Trust the cron log line that says OK" → wrong, log says script exit 0, file mtime tells truth

## Postscript: this is a F11 auditability doctrine in disguise

Every retirement without verification is **deletion without witness**. The verification receipt IS the witness. The lineage IS the audit chain. Without verification + receipt, retirement is indistinguishable from accident — there is no way to prove the deletion was deliberate fitness-based vs careless destruction.

This is why F11 (auditability) trumps F4 (clarity) when in tension: clarity that erases lineage is clarity that destroys institutional memory. Receipt-first verification is how we ship clarity WITHOUT losing lineage.

---

*DITEMPA BUKAN DIBERI — verified, retired, witnessed.*
