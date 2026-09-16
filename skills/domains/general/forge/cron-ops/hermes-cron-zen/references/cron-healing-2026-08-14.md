# Cron healing — 2026-08-14 session (drift-guard cluster + false-unreachable digest + prompt recovery)

## 1. Drift-guard skip cluster (20:48 MYT catch-up burst)

Six jobs failed with `RuntimeError: Skipped to prevent unintended spend: global inference config drifted since this job was created (provider 'openai-api' -> 'custom'; model 'hermes-asi' -> 'i-arif'), and this job is unpinned`:

- `0e37cdaf4a37` arif-world-reality-intel (prompt ALSO stubbed to 420 chars — see §3)
- `5d87405c1770` syed-mak-dressing
- `0f07d72c0673` syed-gerd-log
- `cf1c6b534b2f` syed-sambal-preorder
- `3d369c28f1ab` artifact-drift-audit
- `50149e42f6d9` seal-integrity-sweep

Key evidence: all six ALREADY had `provider: qwen-token-plan-individual` + `model: qwen3.7-plus` in jobs.json. The guard skips on a stale consent stamp (job last written before the global config change), not on missing pin fields. Jobs touched after the 2026-08-11 config change ran fine in the same burst.

Fix: `cronjob action=update job_id=<id>` re-asserting full prompt + provider/model per job. Overdue jobs catch up immediately — artifact-drift-audit and seal-integrity-sweep re-ran OK at 21:07 the same evening. The three Syed caregiver jobs were left to their natural 06:30/08:00 schedule: **never test-fire caregiver/citizen-facing jobs for verification** — you would spam a human at 21:00; a one-morning delay is cheaper.

Verification trap: `provider_snapshot` / `model_snapshot` still showed `openai-api` / `hermes-asi` after successful re-save + ok run. They lag; trust `last_status` + `last_error` only.

## 2. False "Daemon unreachable" in the arifFlow governance digest

- Job: `6c672e289f80` (22:00 MYT daily), script `/root/forge_work/ariflow-audit/scripts/governance_digest.py`.
- Symptom: digest reported "⚠️ Daemon unreachable" while `curl 127.0.0.1:7073/health` was alive: status `ok-v3-vector`, FQ 0.792 FLOWING, 290 enforcement cycles, 0 holds.
- Cause: script did exact-match `health.get("status") == "ok"`; arifFlow's QG formula upgrade to v0.3.1-vector (sealed 2026-08-14) versioned the status string to `ok-v3-vector`.
- Fix: `if str(health.get("status", "")).startswith("ok"):` — verified by re-running the digest (FQ / receipts / enforcement lines all returned).
- General rule: versioned daemons get prefix-matched or schema-parsed, never `== "ok"`. Before reporting "down" from a monitor script, curl the endpoint directly (T0) — a JSON-valid response with an unfamiliar status string is schema drift, not outage.

## 3. Prompt stub recovery recipe

arif-world-reality-intel's 6,649-char prompt had been replaced by a 420-char stub. The full as-run prompt is preserved in every cron output file (`/root/.hermes/cron/output/<job_id>/<YYYY-MM-DD_HH-MM-SS>.md`, section `## Prompt`):

```python
import re, os
d = f'/root/.hermes/cron/output/<job_id>'
fn = sorted(os.listdir(d))[-1]          # newest run file
src = open(os.path.join(d, fn)).read()
m = re.search(r'## Prompt\n(.*?)\n## (?:Response|Error)', src, re.S)
raw = m.group(1)
body = raw[raw.find('You are <job-name>'):]   # strip runtime-injected wrappers
open(f'/tmp/prompt-<job_id>.txt', 'w').write(body)
```

Then `cronjob action=update` with the recovered body VERBATIM. Notes:

- The runtime prepends a skills-skip notice and a SILENT-delivery preamble to the stored prompt; slicing from the `You are <job-name>` marker removes both cleanly.
- `cronjob action=update` replaces the prompt wholesale and clears `skills` unless re-passed — paste the FULL recovered prompt, never a summary. (In this cluster the cleared skills had already been failing to load in cron sessions, so the loss was nil — but check before relying on that.)
- Output files are therefore the canonical backup for job prompts; nothing else stores the as-run text.

## 4. Classification notes (don't escalate non-incidents)

- arifFlow `/health` vector diagnosis `ONTOLOGY_BREACH` with 6/7 dimensions UNMEASURED (only `fq` LIVE) is the expected state right after the v0.3.1 formula seal — producers for g/j/w3/ds/c_dark/omega had not started emitting yet. Schema-stage artifact, not an outage.
- arifOS kernel YELLOW on `deployment_attestation.drift` (source_commit != built_commit, explicitly labeled "SOT drift, not code drift") is a known standing warning, not a new incident.
