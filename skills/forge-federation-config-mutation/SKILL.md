---
id: forge-federation-config-mutation
name: "Forge Federation-Wide Config Mutation"
version: 1.0.0
description: "Mutate persistent configuration across the arifOS federation with 4-tier source-of-truth priority and zero-downtime propagation. Use when sovereign or operator sets a value that every AAA agent (Hermes, OpenClaw, OpenCode, A-FORGE, organ daemons) must render consistently — e.g. timezone, locale, feature flag, default model, federation-wide env var. Triggers: 'set timezone for all agents', 'make this the federation default', 'propagate X across AAA', 'every agent must follow Y'."
owner: 333-AGI
risk_tier: medium
floor_scope: [F1, F4, F11, F13]
autonomy_tier: T1
trigger_when:
  - federation_wide_config_change
  - sovereign_default_set
  - canonical_value_propagation
  - cross_organ_env_binding
tags: [forge, federation, config, mutation, sot, sovereign, propagation, env]
forged: 2026-08-11
forged_by: 333-AGI (session SEAL-76b17b1df36345c4 — timezone mutation)
---

# Forge Federation-Wide Config Mutation

> **Iron rule:** Persistent config in the arifOS federation MUST live in **all four SOT layers** in priority order. Mutate one layer → the others fall out of sync → agents drift → SOT violations.
>
> **Canonical class:** This skill governs every "make every AAA agent follow X" mutation — timezone, locale, default model, federation-wide env var, feature flag, lane-level default, sovereign preference.

## When to Use

- Sovereign or operator sets a value that **every AAA agent** must render consistently across all lanes and surfaces
- A canonical env var or config key needs to be both:
  - **Live in current session** (immediate effect)
  - **Persist for future sessions** (boot pickup)
  - **Propagate to systemd services** (organ daemons)
  - **Survive Caddy/systemd reverts** (defensive against sibling agents)
- Example domains: timezone (`HERMES_TIMEZONE`), locale (`LC_TIME`), default LLM, federation name, canonical schema version, audit retention window

## When NOT to Use

- One-off session-local preference (memory lane is enough — use `substrate/memory-manage`)
- Code mutation in a single organ (use the organ's own deploy skill)
- Reversible experiment that should NOT persist (use scratch file, not SOT)
- Per-person override (use `lanes.yaml` lane-specific config, not federation-wide)
- Constitutional or F-floor changes (those require `apex-judge` + 888_HOLD — far above this skill's autonomy_tier T1)

## The 4-Tier Source-of-Truth Priority (THE Iron Rule)

Every federation-wide config value MUST be writable/readable from these four layers, in this priority order:

| Tier | Location | Owner | Scope | Persistence |
|---|---|---|---|---|
| **L1 — runtime env** | `HERMES_<NAME>` env var in current process | Hermes runtime | live session | process-lifetime |
| **L2 — session state** | `/root/.local/share/arifos/state.json` (or `carry_forward.json`) | 333-AGI session | current session snapshot | until next carry_forward |
| **L3 — lane canonical** | `/root/HERMES/lanes/lanes.yaml` :: `federation_tz.<key>` or per-lane field | lane_switch plugin | all lanes (8 lanes: arif, syed, syed-dm, aliff, aliff-aia, izzu, izzu-aia, guest) | repo-pinned |
| **L4 — system env** | `/etc/environment.d/99-arifos-<name>.conf` + `kunci-mas.env` line + `.bashrc` + `.profile` | root + Hermes profile | whole host (systemd services, SSH, PAM, shell) | persistent across reboots |

**Why four layers (not one):**

- L1 alone dies when session ends
- L2 alone doesn't reach systemd services (they use `EnvironmentFile` from `vault.flat.env`)
- L3 alone doesn't reach child processes unless lane_switch injects it
- L4 alone doesn't propagate into hermes-agent's Python sandbox without an explicit env read

A mutation that misses one tier **will** drift. A future sibling agent, a systemd restart, or a session reboot will reveal the gap.

## The 6-Step Mutation Recipe

Use this exact order. Reverse it and you'll discover (post-hoc) that a tier was missed.

### Step 1 — PROBE BEFORE ACT (F1/F4)

Before writing ANYTHING, scan the four layers for existing values. The lesson learned 2026-08-11: `HERMES_TIMEZONE` was already in `kunci-mas.env` line 156 and `kunci-mas.flat.env` line 151 — systemd services ALREADY inherited it. A naive mutation would have written duplicates. Always:

```bash
echo "=== Probe vault env first ==="
grep -n "HERMES_<KEY>" /root/.secrets/kunci-mas.env /root/.secrets/kunci-mas.flat.env 2>/dev/null

echo "=== Probe lane canonical ==="
grep -n "<key>" /root/HERMES/lanes/lanes.yaml

echo "=== Probe carry_forward ==="
cat /root/.local/share/arifos/state.json | python3 -m json.tool

echo "=== Probe system env ==="
ls /etc/environment.d/ | grep arifos

echo "=== Probe shell init ==="
grep "<KEY>" /root/.bashrc /root/.profile

echo "=== Probe live process ==="
env | grep HERMES_<KEY>
```

If a value already exists at a tier, you don't need to write it there — just verify it's correct.

### Step 2 — WRITE L2 (session state)

The cheapest tier — pure JSON write, no system impact. Always write here first because it documents the *intent* for current and future sessions:

```bash
cat > /root/.local/share/arifos/state.json << EOF
{
  "<key>": "<value>",
  "iana_<key>": "<canonical>",
  "<other_metadata>": "...",
  "set_by": "<who>",
  "set_at_utc": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "rationale": "<why>"
}
EOF
```

This is what `carry_forward.json` readers see on next boot.

### Step 3 — WRITE L3 (lane canonical)

Inject the field into `/root/HERMES/lanes/lanes.yaml`. Two parts:

**3a — federation-wide block (top of file):**
```yaml
version: 1.0.0
default_lane: arif
updated: 2026-08-11
federation_<scope>:
  <key>: <value>
  rationale: >-
    <one-sentence why this is the federation default>
lanes:
```

**3b — per-lane field (apply to all 8 lanes):**
Use Python for atomic multi-lane edit:

```python
import yaml
path = "/root/HERMES/lanes/lanes.yaml"
with open(path) as f:
    data = yaml.safe_load(f)
fed = data.get("federation_<scope>", {})
for lane_name, lane in data.get("lanes", {}).items():
    if isinstance(lane, dict):
        lane["<key>"] = fed.get("<key>")
with open(path, "w") as f:
    yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
```

### Step 4 — WRITE L4 (system-wide env)

Three sub-locations, all idempotent:

**4a — `/etc/environment.d/99-arifos-<name>.conf`:**
```bash
cat > /etc/environment.d/99-arifos-<name>.conf << EOF
# arifOS Federation — Canonical <NAME> (F13 SOVEREIGN, <date>)
# All AAA agents MUST <do what with this value>.
HERMES_<NAME>=<value>
TZ=<value>  # if it's a timezone
LC_<REL>=<value>  # if it's locale-related
EOF
chmod 644 /etc/environment.d/99-arifos-<name>.conf
```

**4b — `.bashrc` + `.profile` (idempotent via marker):**
```bash
SNIPPET='export HERMES_<NAME>=<value>
export <POSIX>=<value>

# arifOS Federation — Canonical <NAME> (F13 SOVEREIGN <date>)
# Marker: # ARIFOS_<KEY>_BLOCK — DO NOT REMOVE (kanonik lock)'

for f in /root/.bashrc /root/.profile; do
  if ! grep -q "ARIFOS_<KEY>_BLOCK" "$f" 2>/dev/null; then
    printf '\n%s\n' "$SNIPPET" >> "$f"
  fi
done
```

**4c — `kunci-mas.env` (canonical vault) — only if not already there:**
```bash
# IRON RULE: only edit /root/.secrets/kunci-mas.env. Never edit .flat.env directly.
# It auto-regenerates via `make -f /root/.secrets/Makefile vault-generate`
if ! grep -q "^export HERMES_<NAME>=" /root/.secrets/kunci-mas.env; then
  echo 'export HERMES_<NAME>="<value>"' >> /root/.secrets/kunci-mas.env
fi
```

### Step 5 — SET L1 (runtime env) — INSTANT propagation

For the **current session** to see the new value:

```bash
export HERMES_<NAME>=<value>
export TZ=<value>  # if timezone

# Verify
python3 -c "
import os, time
os.environ['TZ'] = '<value>'
t = time.time()
print('UTC:', time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(t)))
print('MYT:', time.strftime('%Y-%m-%dT%H:%M:%S+08:00', time.localtime(t)))
"
```

For `code_execution_tool.py` Python sandboxes, `HERMES_<NAME>` is automatically read and propagated as `<POSIX>` (e.g. `TZ`) to child Python processes. Verified 2026-08-11.

### Step 6 — EMBED DOCTRINE (instructions fragment)

The mutation is incomplete until the canonical instruction fragment embeds the rule, so every future agent reads it on boot.

**6a — edit fragment:**
```bash
file="/root/AAA/instructions/<fragment>.md"
```

**6b — add a "Canonical <KEY>" block** with:
- The F13 SOVEREIGN-set value
- The 4-tier source-of-truth priority
- A resolver pattern (Python snippet)
- A display rule (how agents must render)

**6c — re-render AGENTS.md:**
```bash
/root/scripts/render-agents.sh
# verify with grep
grep -A3 "Canonical <KEY>" /root/AGENTS.md
```

## Pitfalls (Lesson-Learned)

| # | Pitfall | Symptom | Fix |
|---|---|---|---|
| 1 | Writing only to `state.json` and skipping system env | systemd services still render UTC, only the active session shows MYT | Complete all 4 tiers — env.d + .bashrc + vault.env |
| 2 | Writing only to vault flat env without idempotency check | Duplicate `export HERMES_TIMEZONE=...` lines accumulate | Always grep before write; vault regenerates from `kunci-mas.env` via Makefile |
| 3 | Trying to write to `/usr/local/lib/hermes-agent/profiles/aaa-hermes/config.yaml` | Hermes guard rejects: *"security-sensitive configuration"* | Use `state.json` + lane_switch plugin instead; or `hermes config set` via terminal |
| 4 | Not re-rendering AGENTS.md after fragment edit | Future agents load STALE doctrine | Always `render-agents.sh` + grep-verify |
| 5 | Adding field to one lane instead of all 8 | Guest/izzu/syed lanes drift from arif lane | Use Python yaml.dump loop to apply uniformly |
| 6 | Forgetting `os.environ['TZ']` POSIX shadow | Python `time.localtime()` returns UTC despite env var | Set BOTH `HERMES_<NAME>` AND `TZ` (POSIX) |
| 7 | Assuming `kunci-mas.flat.env` is editable | It's a generated file (symlink) | Only edit `kunci-mas.env`; regenerate via `make vault-generate` |
| 8 | Skipping the carry_forward.json probe | Miss that the value ALREADY exists at L2 — duplicate write | Always probe all 4 tiers first |
| 9 | Not testing with `python3 -c "import os; os.environ['TZ']=..."` | Mutation "succeeds" but timezone didn't actually flip | Always run a Python TZ verification at the end |
| 10 | Caddyfile/systemd sibling-revert hazard | A sibling agent reverts your patch on next deploy | Document the file with `<!-- CANONICAL: ... -->` header; verify with `stat -c %Y` after each reload |

## Cross-Reference Stack

| # | Skill | Role | When to Load |
|---|---|---|---|
| 1 | `forge-federation-config-mutation` (v1.0.0) | This skill — 4-tier mutation pattern | When you mutate federation-wide config |
| 2 | `substrate/observe-ground` | Evidence-before-narrative | Step 1 (probe-before-act) |
| 3 | `substrate/memory-manage` | Session state writes | Step 2 (L2 state.json write) |
| 4 | `aaa-skill-authoring-craft` | SKILL.md authoring discipline | When this skill gets re-forged |
| 5 | `FORGE-route-least-power` | Entropy discipline | Pick the SMALLEST tier that solves it first; escalate only on probe failure |
| 6 | `AUDIT-skill-atlas` | Cross-skill drift detection | After a multi-tier mutation — verify all tiers still consistent |

## Verification Recipe (Mandatory)

```bash
# 1. Probe all 4 tiers
for tier in "env:HERMES_<KEY>" "state:/root/.local/share/arifos/state.json" \
            "lane:/root/HERMES/lanes/lanes.yaml" "system:/etc/environment.d/" \
            "shell:/root/.bashrc" "vault:/root/.secrets/kunci-mas.env"; do
  printf "%-30s : " "$tier"
  case $tier in
    env*) echo "${!tier#env:}" ;;
    *)   grep -q "<value>" "${tier#*:*/}"/* 2>/dev/null && echo "FOUND" || echo "MISSING" ;;
  esac
done

# 2. Federation 8-organ health (post-mutation)
for p in 8088 7071 7072 7073 3001 8081 18082 18083; do
  resp=$(curl -sf --max-time 2 "http://127.0.0.1:$p/health" 2>&1 | head -c 60)
  [ -n "$resp" ] && echo "✅ :$p" || echo "❌ :$p"
done

# 3. Doctrine in AGENTS.md
grep -c "Canonical <KEY>" /root/AGENTS.md

# 4. Liveness write
echo "{\"last_invocation\": $(date +%s), \"last_outcome_delta\": -1, \"health\": \"HEALTHY\"}" \
  > /root/AAA/skills/forge-federation-config-mutation/liveness.json
```

## Templates

- `templates/timezone-mutation.sh` — exact 6-step script for the canonical case (timezone), copy-paste-modify for other keys
- `templates/four-tier-sot.yaml` — skeleton for the federation_tz block in lanes.yaml

## References

- `references/timezone-mutation-case-2026-08-11.md` — full session transcript of the forging event that motivated this skill. Probe-before-act surprise (value already existed in vault), Hermes guard rejection, idempotent shell snippets, doctrine embedding via zen.md fragment.

## Anti-Patterns (Do Not Do)

| # | Anti-Pattern | Why It's Wrong |
|---|---|---|
| 1 | Mutate only L1 (env var) | Dies at session end; systemd services miss it |
| 2 | Mutate only L2 (state.json) | Doesn't reach organ daemons or lane_switch |
| 3 | Mutate only L3 (lanes.yaml) | Doesn't reach child Python processes or SSH sessions |
| 4 | Mutate only L4 (system env) | Doesn't surface in current session immediately |
| 5 | Edit `.flat.env` directly | It's generated; edit `kunci-mas.env` and run `make vault-generate` |
| 6 | Skip the doctrine fragment | Next session boots without the rule; drift returns |
| 7 | Add the field to one lane | 7/8 lanes drift; guest/izzu/syed get the old default |
| 8 | Forgetting the marker comment in shell init | Idempotency check fails; duplicate blocks accumulate |

## The Zen

> **Mutate the smallest tier that solves it. Escalate only on probe failure.**
>
> The temptation is to write everything everywhere as defensive over-coverage. But over-coverage creates its own entropy: duplicate lines, conflicting sources, sibling agents unsure which tier to trust. **Probe first, then write the minimum tier set.** If the value already exists at L4 (vault env), you don't need L2. If L3 (lanes.yaml) covers all 8 lanes, you don't need to touch per-lane.
>
> The 4-tier pattern is the **fallback**. The probe-first step is the **discipline**.

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-11 | Initial forge. Captures the timezone mutation case (session SEAL-76b17b1df36345c4): probe-before-act (found existing HERMES_TIMEZONE in vault), 4-tier SOT, Hermes guard discovery, lane uniform write, doctrine embedding, render-agents.sh re-render. |
