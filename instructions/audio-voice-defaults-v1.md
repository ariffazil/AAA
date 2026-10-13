<!-- AUDIO-VOICE-DEFAULTS-v1 — companion playbook to AUDIO-INTELLIGENCE-CANON v1 -->
<!-- Status: DRAFT (F13 directive captured 2026-10-07 ~21:05 MYT, awaiting F13 SAH for promotion) -->
<!-- Per canon hierarchy: voice/REGISTRY.md (undang-undang) → playbook (this file) → kanun -->
<!-- F13 directive (verbatim from chat 2026-10-07): -->
<!--   "Audio wise, make sure all future Hermes agents can redo suara Siti, suara abang sado -->
<!--    and suara pmx without failure. Default for Hermes is suara Siti Nurhaliza, lemah lembut, -->
<!--    genius, sopan santun, minimax voice clone." -->

# AUDIO-VOICE-DEFAULTS::v1 — Default Voice + Library Re-do Playbook

> **Status:** DRAFT (F13 directive 2026-10-07 ~21:05 MYT, awaiting F13 SAH for promotion to F13_RATIFIED_PLAYBOOK)
> **Companion to:** `/root/AAA/instructions/AUDIO-INTELLIGENCE-CANON.md` (F13_RATIFIED_DIRECTIVE 2026-10-05)
> **Hierarchy:** voice/REGISTRY.md (undang-undang) → **this playbook** → kanun
> **Scope:** binds all future Hermes agents (including lane=arif, lane=default, and any future sovereign-attended lane)

---

## 0 · TL;DR

Three voice library entries **must be re-doable without failure** by any future Hermes agent. When no voice is specified, the **default is Suara Siti Nurhaliza** (`SSSiti20260926v1`) — voice character: lemah lembut, genius, sopan santun (gentle, brilliant, polite). This default is overridable by explicit voice specification per kanun R2/R3 (config-declared = authoritative; capability truth = latest test).

---

## 1 · Voice Library (3 voices, no-fail re-do mandatory)

| Voice ID | Owner / Character | Speed default | Default usage |
|---|---|---|---|
| `SSSiti20260926v1` | Siti Nurhaliza (MiniMax voice clone) — lemah lembut, genius, sopan santun | 1.0 (graceful, jangan muat kasar) | **Hermes default** when no other voice specified |
| `abang-sado-live-v1` | Syed (Abang Sado) | 0.90–0.93 (0.95 bila tender) | Syed lane conversation, syed_dm |
| `PMX20260930v1` | PMX (personal lane only) | 0.95 | **DISTRIBUTION_HOLD** — lane peribadi Arif SAHAJA |

**Note on PMX ID:** the canonical ID per AUDIO-INTELLIGENCE-CANON v1 is `PMX20260930v1`. Earlier chat references to `PMX20200930v1` are superseded — the on-disk canon is authoritative.

---

## 2 · Default Voice Rule

**When a Hermes turn produces audio AND no explicit voice is specified, the default voice is `SSSiti20260926v1` (Suara Siti).**

Override hierarchy (from kanun R2):
1. Explicit `voice_id` parameter in the call → use that.
2. `lane` voice config (e.g. syed_dm lane might default to abang-sado) → use that.
3. Default → `SSSiti20260926v1`.
4. `PMX20260930v1` → NEVER default, only on explicit F13 binary per request.

**Character carry:** Suara Siti = lemah lembut, genius, sopan santun. The voice carries the *register* — gentle tone, articulate, respectful, but capable. This is the default Hermes register, not a soft-spoken override of any other voice.

---

## 3 · No-Fail Re-do Procedure

The re-do procedure ensures that any future Hermes agent can re-build the 3-voice library from cold start. **No-fail** means: an attempt that returns non-zero exit or empty audio must be retried with logging, not silently substituted.

### 3.1 · Pre-flight (one-time per fresh agent)

```bash
# 1. Verify provider config exists
grep -E "minimax|voice_id" /root/.hermes/config.yaml

# 2. Verify MiniMax API key present
[ -n "$MINIMAX_API_KEY" ] && echo "key_present" || echo "key_missing"

# 3. Verify each voice_id is in private library (push test)
for voice in SSSiti20260926v1 abang-sado-live-v1 PMX20260930v1; do
  curl -s -X POST https://api.minimax.io/v1/t2a_v2 \
    -H "Authorization: Bearer $MINIMAX_API_KEY" \
    -d "{\"model\":\"speech-2.8-hd\",\"voice_id\":\"$voice\",\"text\":\"test\"}" \
    | python3 -c "import sys,json; r=json.load(sys.stdin); print(f'$voice: status_code={r.get(\"base_resp\",{}).get(\"status_code\",\"?\")} audio_bytes={len(bytes.fromhex(r.get(\"data\",{}).get(\"audio\",\"\"))) if r.get(\"data\",{}).get(\"audio\") else 0}')"
done
```

**Pass criterion:** all 3 voices return `status_code=0` and `audio_bytes > 0`. If any fails:
1. Check key presence (Step 2).
2. Check model name (`speech-2.8-hd` per kanun Section 1).
3. Check voice_id spelling (the canon IDs are exact — case-sensitive).
4. Log failure with full curl + response, surface to F13.

### 3.2 · Re-do (per voice, on first use or after any failure)

Per kanun R5: write to disk + md5 BEFORE claiming the voice works. Procedure:

```python
import hashlib, subprocess, os
from pathlib import Path

def produce_voice(voice_id: str, text: str, output_dir: str = "/tmp/voice-out") -> dict:
    """
    Produce audio per kanun. Returns receipt with PRODUCED/DELIVERED/OBSERVED.
    Never claims success without disk artifact + md5.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    out_path = f"{output_dir}/{voice_id}-{int(time.time())}.mp3"
    
    # Push to MiniMax
    response = curl_minimax(voice_id, text)  # impl per kanun Section 1
    if response["base_resp"]["status_code"] != 0:
        return {"status": "FAIL", "reason": "API error", "response": response}
    if not response["data"]["audio"]:
        return {"status": "FAIL", "reason": "empty audio", "response": response}
    
    # Write to disk
    audio_bytes = bytes.fromhex(response["data"]["audio"])
    Path(out_path).write_bytes(audio_bytes)
    
    # md5 BEFORE claim
    md5 = hashlib.md5(audio_bytes).hexdigest()
    size = len(audio_bytes)
    
    # Probe duration
    duration = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", 
         "-of", "default=nw=1:nk=1", out_path],
        capture_output=True, text=True
    ).stdout.strip()
    
    return {
        "status": "PRODUCED",
        "path": out_path,
        "md5": md5,
        "size": size,
        "duration_s": duration,
        "voice_id": voice_id,
    }
```

### 3.3 · Failure Recovery

| Failure | Action |
|---|---|
| API returns `status_code != 0` | Log full response, surface to F13, do NOT substitute another voice silently (kanun R2) |
| `audio_bytes == 0` | Treat as "vantage without existence" — log "Produced-without-payload" but do not claim audio was sent |
| md5 mismatch between expected and produced | Treat as corruption; re-push, do not deliver old artifact |
| `PMX20260930v1` requested without F13 binary | **HARD BLOCK** — distribution hold, refuse |

---

## 4 · Cross-lane Compatibility

Per kanun "Satu kanun, semua lane" — this playbook applies to all Hermes lanes:
- `lane=arif` (current sovereign attendance)
- `lane=default` (general Hermes)
- Any future sovereign-attended lane

Voice library and re-do procedure are **identical across lanes**. Only the default may differ per lane config (e.g. `syed_dm` lane might explicitly set `abang-sado-live-v1` as lane default, overriding `SSSiti20260926v1`).

---

## 5 · Audit Log

Each voice push writes one entry to `/root/VAULT999/voice-pushes.jsonl`:

```json
{
  "ts": "<iso8601>",
  "voice_id": "SSSiti20260926v1",
  "lane": "arif",
  "text_length": <int>,
  "status": "PRODUCED | FAIL | BLOCKED",
  "path": "<absolute path or null>",
  "md5": "<hex or null>",
  "size": <int or null>,
  "duration_s": <float or null>,
  "policy_version": "audio-voice-defaults-v1"
}
```

This is the audit trail F13 can review. **DEFAULT voice pushes** and **explicit** voice pushes are logged the same way — only the `voice_id` field differs.

---

## 6 · Open Debt

- The `i-arif-sovereign-v9` voice in `/root/.hermes/config.yaml` is **NOT** in the AUDIO canon library. The current config has it as default. After this playbook promotes to F13_RATIFIED, the config should be updated to make `SSSiti20260926v1` the default voice for lane=arif (subject to F13 binary per auto-seal rule, since config.yaml is tier-1 critical).
- PMX ID consistency — older chat references used `PMX20200930v1` (year 2020). The canon is `PMX20260930v1` (year 2026). Any historical code/script that uses the wrong ID must be updated.
- Multi-voice render per turn (kanun Section 4) — the 3 voices can be combined in one render, but no-fail applies per voice. If one voice fails, the others still render; the failed voice is logged with status=FAIL.

---

## 7 · Receipts

- Created: 2026-10-07 ~21:10 MYT, by hermes (lane=arif), per F13 directive
- Status: DRAFT (F13 directive received, awaiting F13 SAH for F13_RATIFIED_PLAYBOOK promotion)
- Companion doctrine: AUDIO-INTELLIGENCE-CANON v1 (F13_RATIFIED_DIRECTIVE 2026-10-05, irfanclaw FI-017)
- Source F13 directive: "Audio wise, make sure all future Hermes agents can redo suara Siti, suara abang sado and suara pmx without failure. Default for Hermes is suara Siti Nurhaliza, lemah lembut, genius, sopan santun, minimax voice clone."
- Hierarchy placement: this is a PLAYBOOK (operational, lane-agnostic), not a kanun (constitutional). The kanun (AUDIO-INTELLIGENCE-CANON v1) is the parent; this file is the child for the default-voice + library re-do concern.

DITEMPA BUKAN DIBERI ⚒️
