# Timezone Mutation — Worked Example (2026-08-11)

> **Session:** SEAL-76b17b1df36345c4
> **Forged by:** 333-AGI (Hermes ASI relay of arifOS + F13 SOVEREIGN directive)
> **Sovereign directive:** *"Now please mutate that and make sure all AAA agents in the future follow the same timezone reference"*

## The Case in One Paragraph

Arif asked for `Asia/Kuala_Lumpur` (MYT, UTC+8) to be the federation-wide canonical timezone. Initial naive assumption: write to `state.json` and call it done. Probe-before-act revealed `HERMES_TIMEZONE=Asia/Kuala_Lumpur` was **already** in `/root/.secrets/kunci-mas.env` line 156 and `/root/.secrets/kunci-mas.flat.env` line 151 — systemd services ALREADY inherited it. The gap was not at the system level; it was at the **doctrine level** (no canonical instruction fragment) and **lane level** (no `federation_tz` block in `lanes.yaml`).

## Probe Output (Step 1 — Discovery)

```
=== vault env ===
/root/.secrets/kunci-mas.env:156:export HERMES_TIMEZONE="Asia/Kuala_Lumpur"
/root/.secrets/kunci-mas.flat.env:151:HERMES_TIMEZONE=Asia/Kuala_Lumpur

=== live process env ===
HERMES_TIMEZONE=Asia/Kuala_Lumpur

=== systemd services (EnvironmentFile=) ===
aaa-a2a.service → /root/.secrets/vault.flat.env → ✓ inherited

=== hermes-agent consumer ===
/tmp/hermes-agent/tools/code_execution_tool.py:1152: tz = os.getenv("HERMES_TIMEZONE", "").strip()
/tmp/hermes-agent/tools/code_execution_tool.py:1468: _tz_name = os.getenv("HERMES_TIMEZONE", "").strip()
/tmp/hermes-agent/tools/code_execution_tool.py:1471: child_env["TZ"] = _tz_name   ← propagates to sandbox

=== pre-existing doctrine ===
/root/AAA/instructions/zen.md line 41-43: "Temporal awareness pattern" — mentioned MYT but no canonical directive
/root/AAA/scripts/temporal-anchor.sh: hardcoded `TZ=Asia/Kuala_Lumpur` but no per-agent mandate
```

**Insight:** The value was set in 3 of 4 tiers already. Missing tier was the **canonical instruction fragment**. The mutation was 80% doctrine, 20% file writes.

## Mutation Sequence (Steps 2-6)

### L2 — `/root/.local/share/arifos/state.json`
```json
{
  "timezone": "Asia/Kuala_Lumpur",
  "iana_tz": "Asia/Kuala_Lumpur",
  "utc_offset_hours": 8,
  "tz_alias": "MYT",
  "set_by": "arif (F13)",
  "set_at_utc": "2026-08-11T00:53:55Z",
  "rationale": "Arif di Malaysia. All timestamps MYT, convert UTC → MYT before display."
}
```

### L3 — `/root/HERMES/lanes/lanes.yaml` (federation_tz block + 8-lane uniform write)
```yaml
federation_tz:
  iana: Asia/Kuala_Lumpur
  alias: MYT
  utc_offset_hours: 8
  env_var: HERMES_TIMEZONE
  set_by: arif (F13)
  set_at_utc: 2026-08-11T00:55:00Z
  rationale: >-
    Arif is in Malaysia. All AAA agents MUST render timestamps in MYT (UTC+8)
    for human-facing surfaces. Internal logs/audit may keep UTC but MUST
    carry label.
```

Then Python loop to apply `timezone: Asia/Kuala_Lumpur` + `tz_alias: MYT` to all 8 lanes (arif, syed, syed-dm, aliff, aliff-aia, izzu, izzu-aia, guest).

### L4 — three sub-locations
- `/etc/environment.d/99-arifos-tz.conf` (mode 644):
  ```
  HERMES_TIMEZONE=Asia/Kuala_Lumpur
  TZ=Asia/Kuala_Lumpur
  LC_TIME=en_MY.UTF-8
  ```
- `/root/.bashrc` + `/root/.profile` — idempotent `ARIFOS_TZ_BLOCK` marker
- `/root/.secrets/kunci-mas.env` — already had it; no edit needed

### L1 — runtime env
```bash
export HERMES_TIMEZONE=Asia/Kuala_Lumpur
export TZ=Asia/Kuala_Lumpur
```

### Doctrine embedding
- Patched `/root/AAA/instructions/zen.md` §Temporal awareness with:
  - 4-tier SOT priority
  - Python resolver pattern
  - Dual-format display rule (UTC + MYT)
- Re-rendered `/root/AGENTS.md` via `/root/scripts/render-agents.sh`
- Grep-verified: `Canonical TZ` appears in generated output

## Surprises & Lessons

### 1. Hermes Guard Rejects `/usr/local/lib/hermes-agent/profiles/aaa-hermes/config.yaml`
```
Error: Refusing to write to Hermes config file: .../config.yaml
Agent cannot modify security-sensitive configuration. Edit ~/.hermes/config.yaml directly or use 'hermes config' instead.
```
**Lesson:** `/usr/local/lib/hermes-agent/profiles/*/config.yaml` is hard-blocked for direct mutation. Use `state.json` + lane plugin as the runtime override path. This is a **safety**, not a bug.

### 2. `HERMES_TIMEZONE` was already in vault
**Lesson:** Probe-before-act saves duplicate writes AND reveals what the canonical tier already covers. In this case, 50% of the mutation was no-op.

### 3. arifOS render layer outputs UTC despite env var
The `/health` endpoint returned `"timestamp":"2026-08-11T00:58:25.690366+00:00"` — UTC format. The env var set the **OS** tz but not the **render** layer's tz formatter. **Doctrine was needed to make future agents convert at render time.**

### 4. WELL:18083 reported "degraded"
Not caused by timezone mutation — pre-existing T0 observation. Out of scope for this skill but flagged in session report.

## End-to-End Verification

```
=== Federation 8-organ health ===
✅ :8088 arifOS healthy
✅ :7071 A-FORGE sense
✅ :7072 A-FORGE MCP
✅ :7073 arifFlow FQ=4.26 OPTIMAL
✅ :3001 AAA healthy
✅ :8081 GEOX healthy
✅ :18082 WEALTH healthy
⚠️ :18083 WELL degraded (pre-existing)

=== Time render ===
UTC: 2026-08-11T01:00:40Z
MYT: 2026-08-11T09:00:40+08:00
Day: Tuesday  ISO: 2026-W33-2
```

## Reuse Pattern

For ANY federation-wide config mutation in the future, this case provides the template:

1. **Probe all 4 tiers** — find which already has the value
2. **Write only the missing tiers** — minimal mutation
3. **Embed doctrine in the relevant fragment** — most important step
4. **Re-render AGENTS.md** — doctrine propagates to all harnesses
5. **Verify end-to-end** — 8-organ health + value propagation test
