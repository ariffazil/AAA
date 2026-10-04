# FED/LiteLLM Stack Audit — 2026-08-09 (session recipe)

Context: Arif spawned a Grok build to "zen FED routing" for OpenCode/OpenClaw/Hermes.
Hermes acted as manager/auditor/validator. This file is the probe sequence that
produced the verdict — reusable verbatim for any future FED-door health audit.

## Topology (as of 2026-08-09)

| Port | Process | Role |
|---|---|---|
| :4000 | HAProxy (haproxy.service) | FED front door — ALL agents point here |
| :4011 | litellm (litellm-federation.service) | primary proxy, binds 0.0.0.0, unsets DATABASE_URL/PORT |
| :4012 | litellm (litellm-escape.service) | escape hatch (DeepSeek + MiMo only) |
| :4001 | python3 fed_clean_proxy.py | strips Responses API features for Codex |
| :26898 | litellm (litellm-proxy.service, zombie) | duplicate of :4011 config; disabled 2026-08-09 |

Health consumers that must all agree on the endpoint:
- HAProxy: `option httpchk GET /health/liveliness` (was `/health` → hung)
- fed-watchdog: `TARGET_URL="http://127.0.0.1:4011/health/liveliness"` (was `/health` → false-fail loop)
- Manual sweeps: always use `/health/liveliness` first

## Probe sequence (all T0 read-only)

```bash
# 1. Port truth — never trust curl -sf alone (litellm returns 401 without auth = "looks down")
ss -tlnp | grep -E ':(4000|4001|4011|4012|26898)\b'

# 2. Auth'd health sweep on BOTH endpoints (the /health hang trap)
source /root/.secrets/kunci-mas.env
for p in 4011 4012; do
  for ep in /health /health/liveliness /health/readiness; do
    curl -s -o /dev/null -w ":$p$ep -> %{http_code}\n" --max-time 4 \
      -H "Authorization: Bearer $LITELLM_MASTER_KEY" http://127.0.0.1:$p$ep
  done
done

# 3. Key reality check — hash-compare config key vs env key (never eyeball; redactor masks sk-…)
python3 << 'EOF'
import re, hashlib
hap = open('/etc/haproxy/haproxy.cfg').read()
env = open('/root/.secrets/kunci-mas.env').read()
ek = re.search(r'LITELLM_MASTER_KEY=([^\s"]+)', env).group(1)
eh = hashlib.sha256(ek.encode()).hexdigest()
for i, l in enumerate(hap.splitlines(), 1):
    if 'Bearer' in l:
        m = re.search(r'Bearer\s+"?([A-Za-z0-9_\-\.]+)"?', l)
        if m:
            k = m.group(1)
            print(i, len(k), hashlib.sha256(k.encode()).hexdigest()[:12] == eh[:12])
EOF

# 4. End-to-end door test — real completion through :4000
curl -s --max-time 25 http://127.0.0.1:4000/v1/chat/completions \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" -H 'Content-Type: application/json' \
  -d '{"model":"hermes-asi","messages":[{"role":"user","content":"say OK"}],"max_tokens":10}'

# 5. Model list through the door
curl -s --max-time 10 -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  http://127.0.0.1:4000/v1/models | python3 -c "import json,sys; print(len(json.load(sys.stdin).get('data',[])))"

# 6. Watchdog audit — the landmine
grep -n 'TARGET_URL' /usr/local/bin/fed-watchdog.sh   # must be /health/liveliness
journalctl -u fed-watchdog --no-pager -n 10           # "HTTP 000" spam = wrong endpoint
```

## The fed-watchdog fix (T1, reversible — backup first)

```bash
cp /usr/local/bin/fed-watchdog.sh /usr/local/bin/fed-watchdog.sh.bak-audit-$(date +%Y%m%dT%H%M%S)
# patch TARGET_URL → http://127.0.0.1:4011/health/liveliness
bash -n /usr/local/bin/fed-watchdog.sh
systemctl restart fed-watchdog
```

Why it matters: a watchdog on `/health` false-fails (000 ×3) → `systemctl restart
tailscaled + litellm-federation` every ~3 min → that restart loop killed the Hermes
gateway mid-audit. The watchdog's recovery is MORE destructive than the disease.

## Direct-provider preservation check (Arif's hard constraint: never strip direct)

| Runtime | Config | What must survive |
|---|---|---|
| OpenCode | `/root/.config/opencode/opencode.json` | `provider` keys (14 incl. deepseek, kimi, minimax, mimo-token-plan, qwen-token-plan, bailian, ollama), `enabled_providers`, per-agent `models` lists |
| OpenClaw | `/root/.openclaw/openclaw.json` | `.models.providers` (minimax, deepseek, openrouter, groq, gemini, cerebras, kimi-coding, sea-lion + `fed` @ :4000) |
| Hermes | profile `config.yaml` | `model.provider` (direct deepseek), `custom_providers` FED Federation @ :4000/v1 |

Verify with: `python3 -c "import json; print(list(json.load(open('<cfg>')).get('provider',{}).keys()))"` for OpenCode; walk `.models.providers` for OpenClaw; grep `custom_providers` + `model.provider` for Hermes.

## Outcome (2026-08-09)

- Grok fixed: HAProxy keys → real LITELLM_MASTER_KEY (sha256 match both lines),
  httpchk → `/health/liveliness`, zombie litellm-proxy.service disabled.
- Auditor fixed: fed-watchdog TARGET_URL → `/health/liveliness` (the missed landmine).
- Verified: :4000 door 200 on liveliness + /v1/models (13 models) + real completion.
- Zero direct providers removed across all three runtimes.

## Manager/auditor baseline technique (audit a spawned sibling build)

When Arif spawns a build agent ("be the manager auditor validator for this"), the
auditor's job is to detect WHAT the sibling changed and judge whether it crossed
the identity/runtime line — without trusting the sibling's self-report. Two
techniques made this session's audit precise:

**1. Config-hash snapshot BEFORE the sibling mutates anything:**

```bash
# Baseline (take BEFORE the build starts, or as your first audit act)
for f in /root/A-FORGE/litellm-config.yaml /etc/haproxy/haproxy.cfg \
         /root/.config/opencode/opencode.json /root/.openclaw/openclaw.json; do
  [ -f "$f" ] && echo "$(md5sum "$f" | cut -d' ' -f1)  $(stat -c '%y' "$f" | cut -d. -f1)  $f"
done > /tmp/audit-baseline.txt
```

Then at each audit checkpoint, re-run the same loop and `diff` against the
baseline. Hash + mtime together tell you (a) WHICH files changed, (b) WHEN —
so you can attribute changes to the sibling vs a cron vs yourself. This turns
"did grok touch agent-cards?" from a trust question into a diff answer
(`find /root/AAA/a2a-server/agent-cards -newermt '<sibling-start>'` = empty ⇒ untouched).

**2. Live-path trap — the config with the same name exists TWICE:**

Sibling reports said `opencode.json` and `openclaw.json` were edited. My first
probes hit the WRONG files: `/root/ariffazil/.openclaw/openclaw.json` (mtime
2026-07-28, stale) vs the LIVE `/root/.openclaw/openclaw.json` (mtime 2026-08-09
04:03). Same for `/root/HERMES/config.yaml` (repo copy) vs the live profile
config. **Rule: when verifying a config edit, stat mtimes FIRST — the newest
file with that name is the live one; the sibling edits the live path, not the
one your first `find` returns.** Compare values against `federation-models.json`
(`last_fed_alignment` timestamp) to confirm the sibling synced the ledger.

**3. Verify claims as a numbered checklist, not a narrative:**

For each sibling claim, produce one line: claim → live probe → ✅/❌. The
"verified but with nuance" verdict (e.g. "true, but primaries flipped to direct
which contradicts FED-primary doctrine") is the auditor's real value — it flags
doctrine drift even when the mechanical change is clean.
