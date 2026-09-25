---
name: third-party-software-evaluate
description: Evaluate third-party software before Arif installs.
---

# Third-Party Software Evaluation — Cold Outreach Triage

## The Law

When Arif shares unsolicited software outreach or asks to evaluate a third-party tool:

1. **The VPS cannot run Mac/Windows desktop apps.** State this constraint first; do not run installers from cold emails. Doing so is a verifiable-source violation and an unauthorized mutation.
2. **Provide verifiable alternative value.** Audit founder identity, install scripts, repo source, telemetry surface. REAL DATA, not narrative theater.
3. **Deliver an honest verdict.** Green/Yellow/Red plus what it means for Arif specifically plus clear options. Never fabricate "I tried it" output.

Trigger phrases Arif uses: "try la", "hang try sat", "test bagi result", "evaluate", "audit ni", "ni ok ke", "safe x", or any message forwarding a founder pitch / tool link.

## Procedure

### Step 1: Classify the Ask

State back to Arif which class of ask this is BEFORE running tools:
- "Try this tool" → cannot run on VPS, offer audit
- "Is this legit?" → founder verification + reputation check
- "Should I install?" → full security audit (script + repo + telemetry + privacy)
- "Evaluate this email" → claims-vs-evidence triage

### Step 2: Founder + Identity Verification (parallel)

Run in one batch:
- `web_search` for founder name + company + product name
- Check LinkedIn / GitHub profile if claimed
- Verify claimed institution (university, employer, accelerator)
- Confirm domain via public records if available
- Note if real but small (student, solo, early-stage) — signal, not red flag

### Step 3: Public-Surface Audit (parallel)

- `web_extract` landing page (homepage, /privacy, /terms, /pricing, /company)
- `web_extract` install scripts (`.sh`, `.ps1`) — read the EXACT bytes, not summaries
- Capture: download URL, destination paths, post-install telemetry, tracking pixels

### Step 4: Source Code Audit (if repo public)

GitHub API calls (parallel):
- `GET /repos/{owner}/{repo}` → size, lang, stars, last push, default branch, created
- `GET /repos/{owner}/{repo}/releases/latest` → version, asset list, SHA256
- `GET /repos/{owner}/{repo}/git/trees/{branch}?recursive=1` → full file tree

Identify security-relevant files: `main.ts`, `preload.ts`, `secretFilter.ts`, anything matching `fetch|telemetry|analytics|tracker|exfil|postinstall|secret|key`.

Download via `curl https://raw.githubusercontent.com/{owner}/{repo}/main/{path}` into `/tmp/<repo>-audit/`.

Read `package.json` for postinstall/preinstall hooks + suspicious deps + bundle config (electron-builder codesign flags, hardenedRuntime, identity).

### Step 5: Security Greps (run against downloaded source)

Target the audit directory with these greps:
- **Network endpoints:** `grep -nE 'https?://|fetch\(|request\(|axios|got\(' *.ts`
- **Analytics SDKs:** `grep -nE 'analytics|telemetry|track\(|posthog|mixpanel|sentry|amplitude|datadog|segment|fullstory|hotjar|gtag|gtm\.|google-analytics' *.ts`
- **Exfil patterns:** `grep -nE 'clipboard|keystroke|keylog|readFileSync|chokidar|fileWatcher|fs\.watch' *.ts`
- **Hardcoded URLs:** `grep -nE 'BACKEND\s*=|localhost:|127\.0\.0\.1|api\.[a-z]+\.' *.ts`
- **Postinstall hooks in package.json:** `grep -nE 'postinstall|preinstall|prepare' package.json`
- **Suspicious package-lock entries:** `grep -E 'telemetry|analytics|tracker|sentry|posthog|mixpanel' package-lock.json`

### Step 6: Marketing-vs-Code Reconciliation

For every claim in marketing copy / pitch email / website:
- Find the code path that implements (or doesn't implement) that claim
- Note discrepancy — claimed X, code does Y
- "Local-first" claim → check what triggers cloud calls
- "Privacy-respecting" claim → check for analytics SDKs and undisclosed network calls
- "Secret filter" claim → check `secretFilter.ts` for actual pattern list
- "Open source" claim → check if repo is public and source matches binary claims

### Step 7: Deliver Verdict

Format: **Identity verified · Repo state · Install behavior · Network surface · Telemetry reality · Marketing vs code · Green/Yellow/Red · For Arif · Options**

- Green = real evidence supports claim
- Yellow = true but Arif needs to know (permissions, unsigned binary, telemetry scope)
- Red = contradiction between marketing and code, or undisclosed behavior
- "For Arif" = specific to his context (governance-heavy code, MSS exit, secrecy needs)
- Options = usually 3 (install on laptop / decline politely / ignore)

## Pitfalls

- **Do not execute remote installation scripts received via cold outreach.** They are unverifiable and not authorized by Arif. The audit-then-decide sequence is the value, not blind execution.
- **Do not fabricate "I tried it" output.** The VPS cannot run Mac/Windows desktop apps. State the constraint, then offer an audit. Arif respects honest refusal; he hates fabricated success.
- **Do not trust marketing copy at face value.** Real products describe themselves accurately; sketchy ones overpromise. Read the code.
- **Founder verification does not equal endorsement.** "Real student at real school" is signal (not scam), but does not make the product good. Keep verification factual.
- **Telemetry is not always bad.** Local analytics with disclosed retention are not the same as exfiltration. Differentiate by destination, disclosed-ness, and opt-out.
- **Accessibility permissions are not red flags by themselves.** They are standard for desktop overlay tools, but Arif needs to know the scope before granting.
- **Unsigned binaries in beta are not red flags.** Expected for pre-launch. Note it; do not conflate with malware.
- **One founder outreach does not equal social proof.** A targeted pitch to a known founder is calculated outreach, not endorsement. State the asymmetry.
- **Quota claims like "30 explanations"** — verify in code (look for constants like `LOCAL_FREE_LIMIT`, `TRIAL_FREE_LIMIT`). Do not trust marketing numbers without a code path.

## Output Contract

For every cold-outreach evaluation, deliver:

1. **Identity verified** — founder name, institution, public footprint, real-vs-fake
2. **Repo state** — language, size, stars, last push, latest release tag
3. **Install behavior** — what the installer script actually does
4. **Network surface** — every endpoint the app talks to
5. **Telemetry reality** — what is disclosed versus what is in the code
6. **Marketing vs code reconciliation** — claims matched or contradicted
7. **Verdict format** — green/yellow/red + "for Arif" + 2-3 options

Output goes to chat (Arif's channel), not to `/tmp/`. Audit files in `/tmp/<repo>-audit/` are scratch — final verdict lands in conversation.