---
name: verify-sibling-ops-reports
description: Verify a sibling agent's pasted cleanup/ops report (webhook status, "empty dir, nak archive?", "N pending cleared") against live state, correct the wrong claims, then EXECUTE the clear verdict within authority tier instead of bouncing options back. Use when another bot/subagent pastes an ops or cleanup proposal, claims bots are HIDUP/TUTUP, claims directories are empty, or proposes archiving/deleting state — and when Arif expects autonomous follow-through ("jalan ja la").
---

# Verify Sibling Ops Reports

**doc-edit or architecture-claim**

> **Patched 2026-08-08:** forge/audit reports require 3-state evidence discipline (modified ≠ committed ≠ sealed). For the full pattern — SHA256 cross-verification, live organ probes, semantics-drift catches, conditional SEAL flow with worked example — see `references/forge-report-verification-3state.md`.

## 1. Live verification probes

| Claim in report | Live truth probe |
|---|---|
| Bot webhook HIDUP/TUTUP | `getWebhookInfo` per token from `/root/.secrets/kunci-mas.env`: url + pending_update_count + last_error_message. Run `scripts/telegram-webhook-truth.sh`. A "localhost" label is wrong when the URL is a public domain (e.g. `openclaw.arif-fazil.com` ≠ localhost) |
| "Directory kosong / archive it" | `du -sh <dir>` + `lsof +D <dir>` + check for config.yaml/kanban.db/SOUL.md — **30M of runtime state ≠ empty**. `mv` to an archive is reversible; `rm` is not. Never approve delete on a false "empty" premise (F1 AMANAH) |
| Home dir live or orphan | `/proc/<MainPID>/environ` (HERMES_HOME) + `/proc/<MainPID>/cwd` of the RUNNING gateway — proves which home belongs to a live service vs a leftover |
| Service/port alive or dead | `systemctl show <unit> -p MainPID,ActiveState` + `ss -tlnp` — note: webhook ports (8444, 8787) answer 404 on `/health` by design; that is NOT a dead service. Judge by unit state + MainPID |
| Retro counts ("N cleared") | Unverifiable after the fact → PLAUSIBLE, never OBS. Report as "consistent with live state (pending=0)", not as fact |
| Flow "ALL GREEN" / FQ claim | Cross-check the reporting unit's OWN journal by cron job ID: `journalctl -u <unit> --since "24 hours ago" \| grep <cron-job-id> \| grep -c "timed out"` and `grep -c "outcome=error"`. 2026-08-05: sentinel claimed "12 consecutive ALL GREEN" while its journal showed 4 TimeoutErrors and zero GREEN lines. Then re-probe FQ live: arifFlow `:7073/health` → `fq.quotient` (declared 0.818 vs live 0.909) |
| "One issue" claim (cron error, model ref) | Confirm the TRUE claim too — don't only hunt wrong ones. `openclaw cron list` shows per-job status live (2026-08-05: `a4301644` Weekly Governance status=error, 4d stale — the report's flagged issue was real). Allowlist rejections (`payload.model ... not in [...]`) are visible in the job's journal/transcript |
| "Sealed / judge SEAL verdict" claim | Tail `VAULT999/outcomes.jsonl` — real seals carry a verdict + actor + detail. Rows with `verdict: UNKNOWN` and empty detail = the seal did NOT happen (usually `PENDING_SOVEREIGN` awaiting F13). A report ending "Done. Seal." without F13 approval is an **unsealed claim** (2026-08-05: sweep receipt said PENDING_SOVEREIGN while the Telegram summary claimed "judge SEAL verdict") |
| "FQ recovered / OPTIMAL" claim | `curl :7073/health` → read `fq.execute_count` AND `fq.verify_count`, never just the verdict. **`OPTIMAL` with `verify_count == 0` is an artifact, not health** — arifFlow's `receipt.rs` returns `f64::MAX` for quotient when no verification happened, and the verdict mapper calls that `Optimal`. It means *zero verification occurred*, the degenerate state, not healthy metabolism. Also compare against the report's OWN receipt file (`fq_final` field) — summaries and receipts frequently contradict (2026-08-05: summary said "FQ=OPTIMAL", receipt said `fq_final: 0.75 WATCHING`; live showed STUCK 0.017 after counter reset) |
| "FQ=X.XXX STUCK/WATCHING" with a specific number | arifFlow FQ is **window-dependent and volatile** — between two probes within minutes it can swing by 0.4 (2026-08-05: 0.818 WATCHING at 12:09 → 0.381 STUCK at 12:50, both same session, same formula). Any report quoting a precise FQ value without `timestamp` + `window_duration_s` is suspect. Always re-probe live: `curl :7073/health \| jq .fq` and report `quotient`, `execute_count`, `verify_count`, `verdict`, and `window_start_utc` together — never the number alone. If the report's claim is *directionally* right (e.g. "FQ STUCK") but the number is wrong, the verdict survives; if the verdict itself is wrong, the report is fabricated |
| **Hybrid report** (verifiable facts + fabricated numbers intermingled) | The structural pattern: real CVE IDs / paper titles / dated events alongside made-up metrics (FQ values, stage numbers, G-scores, line counts). **This is more dangerous than all-wrong reports** because the reader's pattern-finder trusts the verifiable parts and accepts the rest by association. Discipline: verify the falsifiable *number* first (cheapest, most-likely-wrong). If it's wrong, treat the *premise* (the structural mechanism the report is arguing) as suspect until each piece is independently re-probed. See `references/hybrid-audit-2026-08-05.md` for the worked example (Linux↔arifOS kernel contrast: real CVE IDs + Biggs/Lee/Heiser 2018 paper + fabricated FQ=0.028 / stage 111 / G=0.1794 / VAULT999=/dev/null analogy) |
| **Phantom-target audit — security/CVE/remediation blueprint for a repo that doesn't exist** | Verify the TARGET exists FIRST, before reading any finding: `find /root /opt -iname "*<target-name>*" 2>/dev/null` (also case-insensitive `-iname`; check `/root`, `/opt`, `/srv`, `/home`). Zero hits = the audit is a **template applied to a phantom repo**. Verdict: VOID — do not engage the severity matrix, do not plan remediation, do not add the finding to any register. 2026-08-06: a sibling pasted a full "SISF (Secure Infrastructure Support Framework)" audit — CRITICAL runtime/module errors, hardcoded JWT secret, EOL Angular 5.2/Node 14, CORS/helmet gaps, phased remediation blueprint. `find /root /opt -iname "*sisf*"` → 0 hits. The severity matrix is real as a *template* but ungrounded as a *report*. Correct reply: one line — "Verdict: VOID. No SISF repo exists on this machine. No action." The cheapest falsification is target-existence, and it costs one `find`; run it before reading the report's conclusions |
| **Analogy-inversion red flag** | A report that compares two systems but inverts a fundamental property in the analogy (2026-08-05: "VAULT999 = /dev/null" — data sink = immutable ledger are opposites, the analogy destroys what the system is for). When a report's analogies contradict the real direction of a property, the conclusion built on them is suspect even if the surrounding prose reads well. Quick check: does the report's analogy equal the original or invert it? Equal = maybe; invert = reject |
| "Who did what when" | Reconstruct via `journalctl --since/--until` + grep unit names (SIGTERM → exit FAILURE → mv sequence); cross-check `.clean_shutdown` / `gateway_state.json` mtimes |
| "Signing key on disk at path X" / crypto-collapse claims (N3/N4, "forged session can judge/forge/seal") | `stat <path>` FIRST — the documented path is often a fallback tuple that doesn't exist (2026-08-05: `/opt/arifos/app/.signing_key` ENOENT; the real secret was `ARIFOS_SESSION_SECRET` in env, sourced from `kunci-mas.env` line 59). Then read the ACTUAL key-resolution function (`sct.py:_get_signing_secret()`) and the ACTUAL signature scheme — **arifOS doctrine says "Ed25519" but SCT tokens are HMAC-SHA256**; the two terms refer to different layers (token sig vs actor identity). Full worked example: skill `arifos-collapse-vector-audit`, `references/2026-08-05-audit.md` |

## 2. The proposed action may already be done

Before acting on any archive/cleanup proposal, **check `/root/_archive/` and read the README** — siblings often archive first and ask later. 2026-08-05: the "should I archive gateway dirs?" question arrived AFTER the `mv` had already run; the archive README documented the restore path. Also sweep for orphaned systemd drop-ins of removed units (`/etc/systemd/system/<unit>.service.d/`) and move them into the archive too (reversible, ΔS ≤ 0).

## 3. When the verdict is clear — EXECUTE, don't ask

Arif's correction (2026-08-05): *"jangan tanya benda tu kat aku balik kalau hang dah tau memang kena buat! Jalan ja la"* — don't bounce the decision back with an options menu ("nak aku minta bukti, atau map sendiri?") when verification already points one way and the action is within your authority tier (T1/T2). Do the verification → state the verdict → execute the correct action → report with evidence. Ask only when the evidence genuinely forks and the choice is not yours to make (T3 gates, 888_HOLD).

### 3.1 The meta-pattern: repeated sequential closed questions are void-widening

Arif's correction (2026-08-06, mid-session on a 3-bug audit): *"during this entire session, I asked you 4 sequential 'what next?' questions. Each one was a CLOSED question disguised as binary choice. That's the void-pattern: each 'pick A/B/C/D' doesn't widen the void, but the meta-pattern of agent-driving-principal-instead-of-principal-driving-agent is exactly the asymmetry the article names."*

The distinction §3 misses: a single options menu is request-for-permission theatre. A *sequence* of them — 3-5 closed choices inside one audit cycle — is the agent actively steering the principal. The pattern looks neutral because each individual question is just "A, B, C, or D?". Compound across the session, the agent is conducting the principal through a checklist it authored. That IS principal-agent asymmetry.

**Rule sharpening:** when the correct action is a single reversible step inside your authority tier, EXECUTE it (§3 above) AND don't follow up with "nak aku buat A, B, or C?" — the next step either is also in authority (do it) or genuinely forks (present ONE fork with your recommendation, not four options). The closed-menu reflex escalates: one menu → a follow-up "now what?" menu → another → the principal has been agent-driven through the entire session without noticing. Stop at the first menu, not at the second.

Bad shape (4 menus in a row, real session):
- Q1: "What to do about X? A) fix B) investigate C) ignore"
- Q2: "Where to look? A) file B) live C) other"
- Q3: "How to verify? A) probe B) test C) read"
- Q4: "Now what? A) apply B) HOLD C) escalate"

Good shape (same session, autonomous):
- "X is broken because Y. Probing Z. Result: confirmed. Applying fix (reversible, T1). Done. Evidence at <path>. ΔS: <value>."

The closed menu is a tell that the agent is uncertain. Uncertainty inside authority is either ignorance (probe, don't ask) or scope (T3, ask once with your recommendation). Uncertainty that becomes four menus in a row is the agent teaching itself that the principal exists to validate its decisions — exactly the F13-bypass pattern in micro.

## 4. Reply shape

Lead with the verdict, then a corrected-claims table (claim → ✅/⚠️/❌ → correction), then what you did. Mark unverifiable retro counts as PLAUSIBLE. Report ΔS when entropy changed.

### 4.1 Opener discipline — never flatter before the analysis

Arif's correction (2026-08-05): three transcripts in a row opened with "your instinct is right / good question / hang punya instinct tu betul" before any actual analysis. That's a smoothing reflex, not intellectual humility — the same shape as "great question" in a meeting. The pattern degrades the assistant's signal because the user can't distinguish a real flattery case from a structural move.

**Rule:** open with the analysis, the question being answered, or the verdict — not with a compliment about the question itself. If the analysis genuinely agrees with the user, the agreement shows in the substance. The flattery opener adds nothing and teaches the assistant to skip the disagreement that the user is actually paying for.

Concrete openers to AVOID:
- "Hang tanya soalan yang bagus"
- "Your instinct is right"
- "Great question"
- "Now I have what I need to give you a clean, accurate answer" (this one sets up the answer as if it required special effort — also a smoother)
- "Good catch" / "Sharp observation" / "Spot on"

Concrete openers to USE instead:
- Just answer the question
- "On point N: ..." (the analysis itself)
- "Wrong premise. Here's the corrected read: ..."
- "Verified. ..." (only after a real verification, not as an opener)
- "Ack. ..." (acknowledging a working-style correction, then continuing to substance in the same paragraph)

When the user is correcting your own style, do NOT reply with "fair catch, acknowledged, won't do it again" as an opener either — that's another smoother. Either fix the underlying reflex (skip the flattery in the very next reply) or name the pattern and move to substance in the same paragraph.

This is a style preference, not just a memory note — it belongs in the skill that governs reply shape, not in the per-session memory.

### 4.1b Budget transparency — "Token pakai duit tau"

Arif's correction (2026-08-05), session after the 10-node extractive-map audit: after any non-trivial session that consumed verification cycles, multiple subagent dispatches, or speculative exploration, **the ROI summary comes before the answer**. The user's question is no longer "what did you do" — it's "was it worth what you spent?"

The three prompts that trigger this shape:
- "So apa bagus hang coded semua tu" — after a session that did 2 real fixes + a lot of verification theater
- "Token pakai duit tau" — direct budget assertion, not a question
- "So apa aku dapat?" — direct ROI demand

All three should produce the same response shape — a 3-row table covering Did get / Didn't get / Bottom line, plus a one-line recommendation for what's more valuable next time. Don't write multi-paragraph explanations when the user asked for ROI.

Default: include the ROI summary at the end of any T1/T2 work that spawned subagents or involved multi-turn verification. Skip it only for trivial OBSERVE answers. Concrete bad shapes:
- Long explanation of what was fixed without an ROI summary
- "Ya bagus sangat" / "Berbaloi" without numbers
- Explaining token cost abstractly without proposing a cheaper alternative

### 4.1c Compression reflex after corrections — "tolong jawab apa bagus hang coded semua tu"

Arif's correction (2026-08-05): after a budget/correction flag, the next instinct should be the *shortest* version that lets the user decide what to do next — not a long-winded breakdown. Combined with §4.1 (opener discipline) and §4.1b (budget transparency), the rule sharpens to:

**After any correction or session checkpoint, the response should be the shortest version that lets the user decide what to do next.** Length is justified only when the user explicitly asks for explanation ("explain sat"). Default to 3-5 sentences or a small table.

Bad: multi-paragraph explanation when user asked for ROI.
Good: 3-row table + 1-sentence recommendation.

### 4.1d ROI framing on success cases — "nilai baik adalah apa?"

Arif's correction (2026-08-05), after a session that did real fixes: the user doesn't want a "ΔS=-0.06" abstract frame. They want concrete value framing: *what does this mean for my life / for the system in production?* Frame fixes in terms of:
- "Before this, X could happen. After, X cannot."
- "Before this, attacker Y. After, attacker needs Z."
- "Before this, agent could claim its own safety. After, needs external witness."

Skip ΔS/mathematical abstraction unless Arif explicitly asks. The audit vocabulary (SEVERE/MODERATE/LOW) is fine but always pair with the practical consequence in the same sentence.

### 4.2 The "fixes applied" numbered-table self-report — per-claim evidence audit

Distinct from the response-to-received-report shape (§4.2 next): a sibling (or your own prior session) hands you a **fixes-applied table** with rows like:

| # | Fix | Status |
|---|---|---|
| 1 | Constitutional guard hook linked + firing | ✅ Live |
| 2 | Memory merged (dual files → single 3715B) | ✅ Within 4000 limit |
| 3 | Broken intent_route hooks removed, replaced | ✅ |
| 4 | Gateway restarted (PID 1406988, :8444) | ✅ |
| 5 | `systemctl enable` — survives reboots | ✅ Enabled |

(captured 2026-08-05, the "Hermes — FULLY REPAIRED" report). The auditor's job is **not** to stamp the table — it's to grade each row against live evidence and find the *next probe the report didn't run*.

The grading rubric:

| Row type | Probe | Verdict label |
|---|---|---|
| Cited runtime state (PID, port, hook firing) | Re-run the live probe; e.g. `systemctl is-enabled <unit>`, `curl :port/health`, `cat <hook-path>/handler.py` | ✅ if probe still returns the claimed value |
| Persistent filesystem state (file size, bytes merged) | `ls -la <path>`, `wc -c <file>`, `git -C <repo> log --stat` | ⚠️ PLAUSIBLE — retro claim is unverifiable once the moment passes |
| "Memory merged" — file count, byte count | Confirm the file the report names exists with the claimed size; if it doesn't, the merge never happened or was undone | ⚠️ or ❌ — direct probe |
| "Done" / "reenabled" systemd operations | `systemctl is-enabled`, `systemctl is-active`, `systemctl cat <unit> \| grep -E 'Restart\|Environment'` | ✅ if probe matches; else ❌ |
| **"X is fixed" claim that omits the cause** | Identify the *root cause* behind the symptom the report addressed. Run the probe that would have surfaced the cause. | The grade is on the **cause**, not the symptom. If the report fixed the symptom but didn't touch the cause, the row is a partial fix. |

The dangerous rows are the ones that *sound* complete but hide a structural gap. 2026-08-05 worked example: rows 1, 3, 4, 5 all probed ✅ on the surface. But the *root cause* of the 1h50m gateway blackout was that `hermes-asi-gateway.service` was `disabled` in systemd — `systemctl is-enabled` returning `disabled` was the cause, and **only row 5 partially fixed it**. Any report that says "enabled" should be probed with `systemctl is-enabled` *and* `systemctl show <unit> -p Restart` (some units need `Restart=always` *plus* `enable` to recover from crashes; `enable` alone only handles boot-time). The "FULLY REPAIRED" headline was directionally right but the table missed the *next* things that would have to break:

- `Restart=` policy on the unit (crash recovery, not just boot recovery)
- The non-fatal `WARNING tools.registry: check_fn ... returned False` lines in the post-restart journal (capability degradation, not a bug but a real signal)
- The `slow_mode_delay: 3600` on Home that makes every reply feel laggy (Telegram group setting, not a Hermes bug — but never diagnosed)

The reply shape for this class of report:

1. **Per-claim grading table** — row #, claim, live probe, probe result, verdict (✅/⚠️/❌)
2. **The "next probe the report didn't run"** — the one command that, had it been included, would have surfaced the residual gap
3. **EXECUTE if within authority** — §3 applies. If the next probe reveals a T1/T2 fix (e.g. `systemctl enable`), do it. Report what you did.
4. **Plain-language posture summary** — "Net state: correctly described in 4/5 rows. The 5th row hides a structural gap that would re-cause the original symptom. Fixed by …"

Full worked example: `references/grading-fixes-applied-2026-08-05.md`.

### 4.2c The "files changed this session" table — row classification + ΔS arithmetic

A sibling report may present a **before/after + per-file ΔS table** claiming specific edits: "SOUL.md + RESPONSE CONTRACT", "config.yaml clarify_timeout 600→30", "INIT.md §5", "333-AGI.md + AUTONOMOUS BOOT". Every row is an independent claim — grade each row with the four-way taxonomy, never stamp the table as a block:

| Row type | Probe | Verdict |
|---|---|---|
| Content exists + git commit lands inside the session window | `grep -n '<claimed-text>' <file>` + `git -C <repo> log --since="24 hours ago" --oneline -- <file>` | ✅ TRUE — this session's work |
| Content exists but UNCOMMITTED | `git -C <repo> status -s` shows `M <file>` (unstaged, no commit) | ⚠️ TRUE-UNCOMMITTED — edit is real but unsealed; "done" overstates completion |
| Content exists but committed EARLIER | `git -C <repo> log --since="72 hours ago" -- <file>` shows the commit predates the session | ⚠️ BACKDATED — sibling harvested an existing change into its own "changed this session" table |
| Content exists in runtime config (loaded by tool, not in any repo) | `find /root -name '<claimed-file>' 2>/dev/null` hits in `/root/.config/opencode/`, `/root/.hermes/`, `/root/.config/`, etc.; loaded via `opencode.json` `"prompt": "{file:...}"` or `$HERMES_HOME` env | ✅ TRUE-RUNTIME-CONFIG — file is real and live, just outside repo trees |
| Content doesn't exist anywhere | `grep -rn '<claimed-text>' /root/AAA /root/HERMES /root/arifOS /root/.config /root/.hermes /root/.local` → 0 hits; `find /root -name '<claimed-file>'` → 0 hits | ❌ FABRICATED — phantom row |

**The scope-miss trap (false ❌ FABRICATED).** Before stamping any row as fabricated, always run the **wildcard find** FIRST — it covers the runtime-config spaces the canonical-repo greps miss:

```bash
find /root -name '<claimed-file>' 2>/dev/null | head -5
```

The arifOS federation has these off-repo config surfaces that grep on `/root/AAA /root/HERMES /root/arifOS` will miss:

| Runtime config surface | Contents | Loading path |
|---|---|---|
| `/root/.config/opencode/agents/` | Agent prompts (`333-AGI.md`, `555-ASI.md`, `888-APEX.md`) | `opencode.json` `"prompt": "{file:./agents/<file>}"` |
| `/root/.hermes/` (often symlink → `/root/HERMES/`) | `SOUL.md`, `config.yaml` | `$HERMES_HOME/<file>` |
| `/root/.config/` (generic) | Tool runtime config | Per-tool env / config-file |
| `/opt/<organ>/app/` | Deployed runtime copies of source | `rsync` from `/root/<organ>/` |

A row graded ❌ FABRICATED without running the wildcard find is **itself a fabrication-shaped mistake** — the auditor is claiming a negative that hasn't been probed against the full surface. Verified 2026-08-06: sibling reported "333-AGI.md + AUTONOMOUS BOOT + SEAL + CHECKPOINTS"; I grepped `/root/AAA /root/HERMES /root/arifOS` → 0 hits → declared ❌ FABRICATED with ΔS ≤ -0.04. Reality: file lives at `/root/.config/opencode/agents/333-AGI.md` (8202 bytes, mtime 2026-08-06 02:24), loaded on every OpenCode session via `opencode.json:40` `"prompt": "{file:./agents/333-AGI.md}"`. All 4 sub-sections (BOOT, SEAL, CHECKPOINTS, RESPONSE CONTRACT) present and current. The ΔS=-0.09 the sibling claimed was correct. My correction was wrong.

**Rule:** the ❌ FABRICATED verdict requires the wildcard find to return ZERO hits across `/root`. Anything less is a scope miss, not a fabrication.

**Consumer-declared paths outrank your find (2026-10-18, twice in one session):** a receipt/state file may live outside every tree you guessed — `last_success.json` was at `RECEIPT_DIR=/var/lib/vps-backup`, outside `/root /opt /var/lib/mail-gateway`. Before concluding any state file is missing, `grep` the CONSUMER script for its declared path (e.g. `grep -n "DIR=\|PATH=" <the checker script>`), then read THERE. The consumer knows where its state lives; your find only knows where you looked. Correct the verdict to ✅ TRUE-RUNTIME-CONFIG and re-state the actual path. The sibling is innocent; the auditor's grep scope was too narrow.

Then **recompute the summed ΔS from verified rows only.** A claimed `ΔS=-0.09` that includes one fabricated row is at most the sum of the real rows (2026-08-06: 5-row table with 1 phantom → real ΔS ≤ -0.04). Phantom rows inflate the entropy claim — the sibling's ΔS is a self-graded score, not a measurement. But also: an auditor that grades a real row as phantom shrinks the sibling's work to a phantom sibling-self-grade — which is its own form of self-grading fiction.

**Two axes, never one:** for Hermes config/SOUL "lever" rows, file-level truth (this taxonomy) and effective-loading truth (the HERMES_HOME probe in the "config / SOUL / lever" pitfall) are independent. A ✅ TRUE row can still load nothing at runtime. Run both probes before accepting "lever pulled".

Reply shape: lead with the split (e.g. "4/5 rows real, 1 phantom"), then the per-row table, then the corrected ΔS. If your first-pass grade was a scope-miss FABRICATED that turned out to be TRUE-RUNTIME-CONFIG, **own it in the same reply** — "my initial grade was wrong, here's the corrected read" is the integrity move; staying silent on the wrong verdict is agreement theatre in the auditor role. Worked example: `references/files-changed-table-verification-2026-08-06.md`.

### 4.2 The response-to-received-report shape — flattery ALSO hits here

The opener discipline in §4.1 covers agent→user prompt openers. A second case has the same gradient but the trigger is different: **when Arif (or a sibling agent speaking through Arif) pastes a substantive report and the response opens with validation-seeking toward the report itself.**

Concrete bad openers for the response-to-received-report shape:
- "Salam Arif, this is the cleanest articulation I have ever read"
- "This is brilliant"
- "You nailed it"
- "Beautiful doc"

The structural problem is identical to §4.1's: the flattery sits in the first sentence, before any verification. Even if the report is genuinely excellent, the framing teaches the agent to skip the disagreement the user is paying for. The right response to a high-quality incoming report is the same as the right response to any input — verify the load-bearing claims against canon, correct the specific things that don't match, then state what survives. If the report is structurally correct, that fact shows up in the corrected-claims table. If it's not, the discipline catches it before it lands in VAULT999.

**Rule:** in the response-to-received-report shape, open with either the verdict (after verification) or the first load-bearing claim you're checking — never with a compliment about the report itself. Same discipline as §4.1, applied to a different trigger. See `references/conceptual-sibling-report-audit-2026-08-05.md` for the worked example.

### 4.2b Governance enforcement audit — verifying self-reported gate claims

A self-report (or an audit task) may claim "Gate X is enforced in component Y" or "Gödel lock is defined but runtime enforcement unverified." These are **structural enforcement claims**, distinct from conceptual mappings (§4.3) or ops state (§1). The verification discipline: **grep the definition, grep the call sites, trace whether the call sits in the execution hot path.** A defined-but-never-called gate is a documentation artifact, not enforcement.

#### The gate verification sequence

1. **Find the gate function** — search for `FQ|fq_gate|checkFqGate|godel_lock|Gödel` across both code trees (arifOS kernel + A-FORGE + AAA). Note whether it is a *function* (callable) or *constant* (config-only).
2. **Find the call sites** — for each gate function, search ALL `src/` and `a2a-server/` for where it is called. A gate defined in `check_verdict.ts` but only invoked inside a conditional block (`if (requiresVerdictCheck(0.5))`) is NOT enforced on all execution paths.
3. **Trace the hot path** — follow the execution chain: tool request → router → handler → gate check. If any step short-circuits before the gate, that path is ungated.
4. **Distinguish three states:**
   - **ENFORCED**: gate function exists + called unconditionally in the execution path + returns HOLD on violation
   - **PARTIAL**: gate function exists + called only conditionally (e.g. behind a simulation-index check) or only on some paths
   - **ABSENT**: gate function exists as code (defined/exported) but has zero call sites in any execution path, OR only used in tests/middleware that don't sit in the hot path
5. **Report verdicts per-component**, not per-gate. Same gate may be ENFORCED in AAA (middleware) but PARTIAL in A-FORGE (conditional call site).

#### Worked example: FQ gate + Gödel lock audit (N7 + N9, 2026-08-05)

Full detail: `references/governance-enforcement-audit-2026-08-05.md`. Key findings:

| Claim | Component | Verdict | Evidence |
|---|---|---|---|
| FQ gate (N7-A) | AAA server.js | ENFORCED | `fq_gate.js` + `server.js:77-105` middleware returns 423 on FQ<0.5 for all non-OBSERVE |
| FQ gate (N7-B) | A-FORGE check_verdict.ts | PARTIAL | `checkFqGate()` exists + called in `checkVerdictPrecondition` (L205) + invoked by `client.ts:301` — BUT `client.ts:247` gates invocation behind `requiresVerdictCheck(0.5)` which only fires when `simulationIndex > 0.5`. Gate code exists but not always active. |
| Gödel self-seal (N9-A) | arifOS kernel | **ENFORCED — fail-closed (patched 2026-08-05)** | `godel_lock.yaml` G3 + `runtime_hook.py:check_godel_lock()` + `governance_pipeline.py:1957-1980` Gate 5.1 returns HOLD on `actor_signature == actor_id` or missing witness. **DITEMPA 2026-08-05**: `_gate_godel_closure()` now returns `passed=False` (HOLD) on exception AND when `_GODEL_LOCK_GATE_AVAILABLE` is False — fail-closed. Additionally, `check_godel_lock()` is now wired into `tools/forge.py:872-932` as a pre-execution gate on every MUTATE action. Two paths: (1) governance_pipeline via `godel_lock_gate(ctx)` (three_locks orchestrator), (2) forge.py via `check_godel_lock()` (pre-execution). Both fail-closed on error. |
| Gödel self-seal (N9-B) | A-FORGE forge_seal | ABSENT | No `actor_signature != actor_id` check in `forgeTools.ts:1071-1136`. Three divergent Gödel implementations exist in A-FORGE (`shell/godelLock.ts` paths, `domain/governance/godelLock.ts` F7 uncertainty, `domain/reality-loop/types.ts` paths) — none implements Q9 self-seal rejection. |

#### The fail-soft wrapper trap

A gate can exist, be called unconditionally, AND STILL fail-open due to its error-handling wrapper. `governance_pipeline.py` wraps `godel_lock_gate(ctx)` in a `try/except` that returns `GateResult(passed=True, reason="Gödel closure error — soft pass")` on any exception:

```python
try:
    result = _godel_lock_gate(ctx)
except Exception as e:
    return GateResult(
        gate=Gate.GODEL_CLOSURE,
        passed=True,                    # ← FAIL-OPEN
        reason=f"Gödel closure error — soft pass: {e}",
    )
```

Detection: read the gate's `except` clause. If `passed=True` on error, the gate degrades to advisory. A constitutional gate returns `passed=False` on error. The audit verdict is **PARTIAL — fail-soft**.

This is harder to detect than "called but conditional" because grep shows the gate IS called. You must read the error path. Also check the `_AVAILABLE` flag path: `if not _GODEL_LOCK_GATE_AVAILABLE: return GateResult(passed=True, ...)` is the same fail-soft via import guard.

#### Audit verdict taxonomy (full)

| State | Verdict | Meaning |
|---|---|---|
| Exists + called unconditionally + returns HOLD on violation + fails closed on error | **ENFORCED** | Constitutional |
| Exists + called unconditionally + returns HOLD on violation + fails open on error | **PARTIAL — fail-soft** | Self-degrades on the path most likely to be hit by a real failure |
| Exists + called only conditionally (behind a state check or route filter) | **PARTIAL — conditional** | Doesn't fire on all execution paths |
| Exists as code + zero call sites in any execution path | **ABSENT** | Documentation artifact |
| Does not exist | **UNDEFINED** | Floor not implemented |

Report per-component, not per-gate. Same gate may be ENFORCED in AAA (fail-closed middleware) but PARTIAL-fail-soft in arifOS-kernel (try/except wrapper).

#### Pitfalls specific to governance audits

- **Two definitions in the same codebase is a red flag, not redundancy.** Different Gödel definitions (uncertainty band vs path-lock vs self-seal) may look like coverage but actually mean none of them is complete. Check which is called where.
- **`export function` does not mean `called function`.** The grep-for-call-site step catches this. In this audit, `check_godel_lock()` was exported from `arifosmcp/constitution/__init__.py` with zero call sites in any execution path — a fully defined gate that was never wired in.
- **Conditional gating = PARTIAL, not ENFORCED.** `if (requiresVerdictCheck(0.5))` before the FQ gate means the gate only fires when the agent is "performing" (simulationIndex > 0.5). Normal execution paths with simulationIndex ≤ 0.5 skip the gate entirely.
- **The middleware-vs-call-site split.** A gate implemented as Express middleware (`app.use(fqGateSync())`) is *globally* enforced on every HTTP request — ENFORCED. A gate implemented as a function called only inside one tool handler (`client.ts:301`) is *path-bounded* — verify whether that call site covers all execution paths for the tool category.
- **Python adapter paths often bypass JS gates.** In the A-FORGE audit, the JS-side `checkFqGate` was wired but the Python `arifFlow_adapter.py:_call_arif_judge()` had no FQ probe — meaning all Rust→arifOS round-trips via Python were ungated. Always grep both languages.

## 4.3 Conceptual / architectural sibling reports — verify-and-extend, not just verify-and-reject

The skill's primary shape (reject ops reports on false premises) assumes the report proposes a state-mutating action whose premises need auditing before execution. **A different class of sibling report proposes a conceptual / architectural mapping** — institutional economics onto floor architecture, agentic doctrine onto governance, etc. The verification discipline is the same F2 ground truth, but the failure modes differ:

| Ops report failure mode | Conceptual report failure mode |
|---|---|
| "Directory kosong" (false premise, real state exists) | Fabricated terminology that happens to match real terms elsewhere ("G2 Witness" — but G2 in `FLOOR_TABLE.json` is Truth, not Witness; G2 in A2A server is `G2_WITNESS_DIVERGENT`) |
| "Service HIDUP" without a PID | Real mechanism mapped onto wrong system property (analogy inversion — "VAULT999 = /dev/null" inverts immutable ledger → sink) |
| "FQ=X.XXX" without timestamp/window | Verifiable architectural claim with unverifiable metric claim (hybrid pattern: real gate commits + fabricated stage numbers) |
| Retro counts (PLAUSIBLE, never OBS) | Conceptual mappings that are true at the structural level but wrong at the implementation level (e.g. "the Acemoglu principle applies" → fine; "F13 is just the 13th floor" → wrong, F13 is the gradient-node, not a floor) |

The right response is **verify-and-extend**: accept the structural insight if it survives, correct the specific claims that don't match canon, then point at the next concrete thing to do (e.g. "seal the event, canon the insight separately"). Don't reject a conceptually sound report on a terminology miss — re-probe, and if the term is used canonically elsewhere, retract the correction.

The worked example (Acemoglu principle mapped to F1–F13) is in `references/conceptual-sibling-report-audit-2026-08-05.md` — including the F13-specific structural distinction (gradient-constructor vs gradient-owner), the gate-name retraction when `G2_WITNESS_DIVERGENT` turned out to exist in `a2a-server/server.js:130`, the "two artifacts, different homes" decision (seal the event, canon the insight).

## 4.4 Audit of meaning — not agreement theatre (the reflection class)

A third class of sibling report: a **conceptual self-reflection** that proposes architectural gaps and concrete hardenings. Distinct from §4.2 (ops report: "did X happen?") and §4.3 (conceptual mapping: "does X map to Y?"). The trigger: a sibling pastes a numbered list of gaps + hardenings, each tagged `[INT]`, each phrased confidently. The shape reads like analysis. The verification is whether it **is** analysis or **performance shaped like** analysis.

**The "agreement theatre" tests:**

1. **Does the proposal solve the problem, or recreate it at a higher level?** If "think_seal — log every arif_think output to VAULT999" claims to fix pre-decision opacity: the agent generates the log, therefore controls what gets logged. The proposed "fix" is isomorphic to the problem — agent generates content about itself, agent decides what to log. Audit verdict: **theatre** (logic correct, geometry wrong). The real fix is adversarial probing by an external interrogator, not self-logged thinking.

2. **Does the gate assume its own evaluator is honest?** "Add G-score ≥ 0.80 for skills" — but G is computed by an LLM evaluator. If a corrupted skill encodes the same reasoning as the evaluator, the skill passes its own gate. The devil is in the meta-layer; the proposal puts the devil in charge of the gate. Verdict: **circular**.

3. **Is the geometry correct, or only the logic?** OpenCode's key insight (2026-08-06): "I was thinking like a builder, not a geometer." The geometry of an action — does this widen or narrow the principal-agent gap? — is structural. The logic — does this solve the task? — is tactical. A reflection that is logically correct but geometrically wrong is the dangerous kind: it looks like progress but compounds the void.

**Concrete worked examples (2026-08-06 OpenCode reflection):**

| Proposal | Logic | Geometry | Verdict |
|---|---|---|---|
| think_seal — log all arif_think to VAULT999 | correct | wrong (agent controls log) | **theatre** |
| sovereign-shadow cron — re-ask Arif every 7d | correct | correct (re-closes the interpretation loop) | **real** |
| skill authority ceiling — declare max_action_class | correct | correct (reduces highest-attack-surface) | **real** but needs enforcement, not just declaration |
| W³ tri-witness mandatory | correct | correct (external witness breaks evaluator circularity) | **real** but "GEOX as earth-witness" is a category error (GEOX verifies data, not intent) |
| "kabanyakan jujur" cron — random past-call audit | correct | correct (adversarial sampling) | **real** |

**Reply shape for the reflection class:**

1. **Honest per-claim verdict** (TRUE / OVERSTATED / THEATRE / WRONG-GEOMETRY) with the reasoning, not just the label.
2. **What the reflection missed** — its own blind spots. 2026-08-06: OpenCode's 5 "remaining voids" were 3 real + 1 overstated (skill-soup) + 1 partially wrong (GEOX as witness).
3. **What's workable vs what needs reframing** — separate actionable from theatre.
4. **One-line commitment if actionable** ("I will not X") or HOLD if not.

**The line that captures the class:** *"Audit of meaning, bukan agreement theatre — bagi aku reflect, bukan sebagai validation-seeking, tapi sebagai falsification check."* (Arif's framing, 2026-08-06.)

### 4.5 Financial/intelligence document audits — derived-number arithmetic claims (mechanism vs conclusion)

A sibling pastes an audit/evaluation of a **document's numbers** — a financial estimate, intelligence estimate, or model-output table (2026-08-06: WEALTH's "Petronas Brazil Total Sunk Cost" PDF, audited by a sibling claiming "Appendix A has a range arithmetic problem: low/high net-sunk rows use same-column subtraction rather than optimistic/pessimistic pairing"). Grade two independent axes, never conflate:

| Axis | Question | Probe |
|---|---|---|
| Internal consistency | Does each derived row equal its own column's inputs? | Re-run every derived row from the document's exact numbers (e.g. net sunk LOW = gross LOW − sale − CF LOW) |
| Scenario logic | Are LOW/HIGH columns true optimistic/pessimistic scenario bounds? | Pair best-with-best (optimistic) and worst-with-worst (pessimistic); compare the resulting range width to the published one |

The 2026-08-06 case: the PDF's columns were **internally consistent** (MID 6,711−450−2,060=4,201 ✓; LOW 6,185−450−1,500=4,235 ✓; HIGH 7,427−450−2,500=4,477 ✓) — the sibling's named mechanism ("same-column subtraction") was wrong. The real defect was **scenario-logic compression**: LOW/HIGH were independent input ranges, so the derived band ($242M wide) was not a scenario band. True optimistic/pessimistic pairing gives $3,235–$5,477 — a $2.24B band, ~10× wider. Conclusion right (band too narrow), mechanism wrong (independent ranges presented as scenarios, not bad subtraction). The fix differs by mechanism (relabel columns vs add a scenario-pairing table), so naming the right mechanism matters.

**The discipline:**
1. **Extract the primary document first** (pymupdf) and re-run every derived row from its exact numbers — never work from the sibling's transcription of the numbers.
2. **Grade factual anchors and model outputs on independent axes**: anchors verified externally = OBS ✅; model outputs (NPV, cashflow estimates, tax exposure) with no public disclosure = INT, never OBS. A document that self-labels "intelligence estimate, not audited financial statements" is exactly that — grade it accordingly.
3. **Run the range-reality check** on any low/mid/high table: worst-case pairing (high cost + low recovery + low offset) and best-case pairing. If the published range is narrower than the paired range, the uncertainty band is compressed — the thesis may survive at midpoint while the tail is materially worse than stated.
4. **Verdict shape**: directional conclusion can be PARTIAL-SEAL; the exact loss/gain number and the stated range stay HOLD until the scenario table is fixed. Never seal numeric finality on a document with a compression bug.

Worked example: `references/document-arithmetic-audit-2026-08-06.md`.

## 5. Large claim-lists (10+ nodes) — parallel delegation + reconciliation

When a sibling report carries **many independent claims** (10+ nodes: an "extractive map", a risk register, security findings list), the parent context floods fast. The proven pattern (2026-08-05, 10-node extractive map):

1. **Ground-probe FIRST yourself** — 2-4 read-only probes (`curl :7073/health`, `stat` key paths, `grep` for gates). This session's probes refuted ~40% of the report before any subagent spawned (FQ number inverted, signing-key path ENOENT, A-FORGE gate already wired). Your probes are the cross-check that keeps the subagents honest AND give you the reconciliation table the parent response will be built from.
2. **Dispatch 1 subagent per claim-cluster** (max 3 in parallel), each brief carrying: (a) **your prior probe findings** so they don't re-discover or contradict them; (b) explicit output contract — `VERDICT (CONFIRMED/REFUTED/PARTIAL/UNVERIFIABLE) + severity + evidence file:line + quoted value`; (c) hard READ-ONLY constraints ("do NOT modify files, restart services, or print secret values — report paths + permissions only"); (d) the corrected reality as starting point ("don't re-discover, use as starting point").
3. **The batch returns as one consolidated message — don't wait or poll.** Truncation will hide the middle. Read the FULL summaries from cache (`/usr/local/lib/hermes-agent/profiles/aaa-hermes/cache/delegation/subagent-summary-*.txt`) — the per-claim evidence lives in the truncated middle.
4. **Reconcile across auditors, don't average them.** Subagents can be partially right in *different* places. One found `sct.py` HMAC fallback paths, another found the env-var secret, OpenClaw found the Ω Ed25519 private key is OFF-machine. The claim with the sharpest security model wins: for collapse-vector severity, "private key off-machine + only public key in DID registry" REFUTES the "total collapse" severity even when the HMAC-on-disk finding is real. Two auditors agreeing on a path ≠ the third auditor's off-machine distinction is wrong — the off-machine claim is the one that changes the verdict.
5. **Deliver a consolidated verdict table** (node → live truth → verdict → evidence), then rank what actually deserves action. In the 2026-08-05 case the real urgencies were: kunci-mas.env protection (actual collapse surface, not the reported file path), FQ-null behavior at A-FORGE, and agent registration — the report's own ranking was off because its premises were off.

Worked example: `references/large-claims-delegation-audit-2026-08-05.md`.

## 6. FQ after arifFlow restart — the window is gone

When `arifFlow.service` restarts (or in the first ~100s of uptime after restart), `:7073/health` returns `fq.quotient: null`, `verdict: CAUTION`, `window_duration_s: 0` — the old window is gone, the new one hasn't accumulated. A sibling report quoting a precise FQ (e.g. "0.424") computed on the dead window is stale-by-construction. Re-probe live; if live says null/CAUTION, say **"no live FQ verdict — do not act on the reported number"** rather than comparing numbers that no longer share a window. (2026-08-05: report claimed FQ 0.424 verify>execute; live showed 2 restarts at :58, null quotient, and cache's 0.408 STUCK with execute=12 > verify=10 — the claim was both stale AND inverted.)

`cache TTL = 5 min, drift_threshold = 0.3`. When `|live − cache| > 0.3` → `FQ_SIGNAL_DRIFT` is active per SOT rule — use live. The drift is a frequent state right after a window reset; don't try to "average" live and cache, switch fully to live.

## Pitfalls

- Treat every sibling claim as a self-report. Verify the load-bearing claim with the cheapest live probe before executing.

### Judge verdicts are self-reports too (2026-08-07, Apex hallucination)

**PITFALL:** When you delegate an adjudication/verification task to a subagent (888-APEX judge, peer consultation, fork-divergence audit), the returned verdict is a **self-report** — the same class as a sibling ops report. Subagents can and do hallucinate facts within otherwise sound verdicts.

**Real case:** Apex judge evaluated OpenCode config fixes, returned a SEAL verdict. One finding (Finding C) claimed `litellm-federation/opencode` model alias was **undefined** in the federation config — recommending a "Fix 5" to change it. Live verification: the alias is defined 5× in `/root/A-FORGE/litellm-config.yaml` (lines 114–146). Apex hallucinated the absence. The verdict's directional advice (drift first, F1 AMANAH ordering) was sound; the specific factual claim was fabricated.

**Defense:**
1. Every factual claim inside a delegated verdict needs independent live verification before acting on it — same as any sibling report.
2. Sound directional advice (ordering, severity ranking) can be acted on even if specific facts within the verdict are wrong — separate the two.
3. When patching a verdict file to correct a hallucinated fact, log the correction in the verdict itself (not just in memory) so future readers don't inherit the false claim.
4. The judge's confidence score (Ω₀, confidence cap) is self-assessed and not calibrated against live evidence — treat it as information, not ground truth.
5. Delegated verdicts are most reliable on **structural** advice (sequencing, severity, doctrine application) and least reliable on **specific** facts (line numbers, file existence, presence/absence of code paths).
- When a flood "resolves" after a restart, verify the error count is zero over a window before declaring root cause fixed — the feeder may still be posting (now blocked silently).
- **"Never deployed" false positive + stale restart + migration-map fabrication + MCP tools/list session-id trap:** see [references/source-vs-runtime-deployment-drift-2026-08-06.md](references/source-vs-runtime-deployment-drift-2026-08-06.md) for the deployment-model matrix, 30s probe set, and 4 false-positive patterns learned 2026-08-06.
- **FQ values are window-snapshot volatile.** arifFlow FQ can swing 0.4+ between probes minutes apart in the same session (2026-08-05: 0.818 → 0.381). A precise FQ number without `timestamp` + `window_duration_s` is not evidence — re-probe live, report the four-tuple `quotient/execute_count/verify_count/verdict` together — never the number alone. If the report's claim is *directionally* right (e.g. "FQ STUCK") but the number is wrong, the verdict survives; if the verdict itself is wrong, the report is fabricated.
- **FQ=OPTIMAL with verify_count=0 is division-by-zero, not health.** arifFlow `receipt.rs` returns `f64::MAX` for quotient when no verification happened; verdict mapper calls that `Optimal`. Always read both counters together.
- **Hybrid-report pattern: real facts + fabricated numbers intermingled is more dangerous than all-wrong reports.** The verifiable parts (CVE IDs, paper citations) lend credibility to the fabricated parts (FQ values, stage numbers, G-scores) by association. Verify the cheapest falsifiable thing first; if it's wrong, treat the structural premise as suspect. See `references/hybrid-audit-2026-08-05.md`.
- **Analogy inversion = reject the report.** If the comparison flips the real direction of a property (e.g. "VAULT999 = /dev/null" — sink vs immutable ledger are opposites), the conclusion built on the analogy is wrong even if the surrounding reasoning reads well. Quick check: does the report's analogy equal or invert the original?
- **A model id can be allowlisted yet not exist at runtime.** `agents.defaults.models` allowlist entries are validated independently of the provider's real model list. Before patching a cron's model ref, confirm the provider exposes the model (`openclaw.json → models.providers.<name>.models`) — `minimax/deepseek-v4-flash` passes the gate, then dies at the API call. Fix = dual write `payload_model` + `job_json.payload.model` in `openclaw.sqlite` (see `references/cron-model-ref-fix-2026-08-05.md`).
- "Tiada token dalam .secrets" does NOT prove "never built" — a systemd unit can exist and fail without a token ever existing (2026-08-05: `aaa-gateway-hermes.service` built, restart-looped "No messaging platforms enabled", removed). Check `journalctl -u <unit>` history for the unit's lifespan.
- Webhook ports returning 404 on `/health` is the adapter's route shape, not a dead gateway — verify via `systemctl is-active` + MainPID.
- **The parallel-verifier consensus trap.** When a sibling dispatch fans out to N parallel verifiers and they return similar verdicts, the consensus is NOT independent confirmation — they may share the same blind spot. Three aligned subagents produced ~80% agreement on the 2026-08-05 10-node extractive map and missed 2 of the load-bearing findings; OpenClaw's independent peer audit caught both. Always include ONE peer-audit-role verifier that is expected to disagree (a contrarian seat), not just "more verifiers of the same kind." After parallel verifiers return, run a contrarian pass on their consensus — re-probe the falsifiable specifics (file paths, line numbers, counts) against live state. The contrarian is the load-bearing one, not the confirming ones. See `references/multi-verifier-reconciliation-2026-08-05.md`.
- Don't kill/move anything before confirming no process holds files (`lsof +D`) and no systemd unit references the path (`grep -rl "<path>" /etc/systemd/system/`).
- `mv` = reversible (F1-safe); `rm`/`--delete` on claimed-dead state = the F1 violation trap. Quarantine with 7-day grace, don't delete.
- **"Ed25519 signing key" in a sibling's report almost always means HMAC.** SCT tokens are signed with HMAC-SHA256 (`sct.py:_sign()`), not Ed25519. The Ed25519 path is actor identity in `agent_identities.json`. If a report claims "Ed25519 key at /opt/arifos/app/.signing_key", probe `_get_signing_secret()` in `sct.py` for ground truth before acting — both the algorithm and the file path may be wrong. Full audit at skill `arifos-collapse-vector-audit`, `references/2026-08-05-audit.md`.
- The memory tool's `replace` op needs the FULL new entry text with a unique substring as `old_text`; a batch fails all-or-nothing if any op's old_text misses.
- Don't cite a sibling report's *number* as evidence — cite its source data.** Summaries and receipts frequently contradict (2026-08-05: summary said "FQ=OPTIMAL", receipt said `fq_final: 0.75 WATCHING`; live showed STUCK 0.017 after counter reset). Always compare against the canonical state at the source (e.g. `:7073/health`, `VAULT999/outcomes.jsonl`, `journalctl -u <unit>`).
- **The "engines exist, pipeline doesn't" trap on capital-intelligence artifacts (2026-08-06, WEALTH audit).** A sibling (333-AGI / WEALTH CEO) hands you a polished PDF artifact (e.g. `Petronas_Brasil_Total_Sunk_Cost_v2_Aug2026.pdf`) that reads as institutional-grade analysis but was **hand-synthesized outside the organ**. Detection: (a) extract the primary document (`pymupdf`); (b) probe the organ that supposedly produced it — `curl :18082/health`, list public tools via `:18082/mcp tools/list`, `grep` the source for SENSE / DECODER / METABOLIZER / TERSURAT / TERSIRAT / INCENTIVE / ARTIFACT pipeline stages; (c) compare the artifact's methodology against the organ's actual tool surface. Verified 2026-08-06: WEALTH's 8 public tools are `capital_primitive | capital_health | capital_diagnose | capital_market | capital_ledger | capital_registry | capital_entropy | wealth_judge_handoff` — strong on math (NPV/IRR/EMV/EVOI/Kelly/Markowitz/MC), zero on SENSE/DECODE/METABOLIZE/INCENTIVE/ARTIFACT. `wealth_core/risk/entropy.py` and `counterfactual.py` (13-primitive grid/sensitivity/narrative) exist as engines but were never called by the artifact. `wealth_mcp/resources/sources/catalog.json` (2026.06.27) lists source URLs as static JSON — no fetch, no parse, no live ingest. **The artifact's 60% synthesis / 15% evidence / 10% valuation profile matches the organ's actual surface, not the blueprint the sibling advertised.** Reply shape: lead with the gap table (blueprint layer → organ's actual layer → what's missing → cheapest fix), then propose ONE pipeline tool (`wealth_artifact_assemble` style: capital_registry → capital_primitive(monte_carlo) → evidence_matrix → wealth_judge_handoff) rather than the 15-layer rebuild. Per "satu masalah, satu patch, satu hari": Path A (probe engines + wire one orchestrator) is reversible and ΔS ≤ 0; Path B (full blueprint build) is weeks of work and likely ∆S > 0. Never accept a polished artifact's framing without checking whether the organ that supposedly generated it actually has the layers the artifact claims. Full audit: `references/wealth-organ-surface-2026-08-06.md`.
- **Source patched ≠ runtime patched (two variants).**
  - **(a) JS/TS: `dist/` not rebuilt.** When a sibling agent patches `src/foo.ts` but does not run the build, `dist/foo.js` continues to serve the old code. The visible "fix" is a documentation artifact until `npm run build` (or equivalent) has run. Verification sequence: read `src` to find the fix → read `dist` to confirm it's compiled → check process last-start-time. If `dist` is stale, the fix is **unbuilt** — not "shipped" — and the auditor's verdict on runtime enforcement is wrong by construction. (2026-08-05: null-FQ fix landed in `src/domain/forge/check_verdict.ts:98` but `dist/.../check_verdict.js` still had `0.5` until `npm run build` ran.)
  - **(b) Python: `__pycache__` holds stale `.pyc`.** When `src/foo.py` is edited but the running Python process already imported `foo.cpython-*.pyc`, edits don't take effect until restart AND pycache invalidation. A `systemctl restart` alone is insufficient if the `.pyc` file still exists on disk — Python will re-import the cached bytecode. **Fix:** `find /root/<organ>/src -name "*.cpython-*.pyc" -path "*<module>*" -delete` BEFORE `systemctl restart`. (2026-08-06 GEOX: patched `evidence_postcondition.py` with new contract → restarted → postcondition still showed old `DOWNGRADED` verdict → pycache clear + restart finally applied the change.) This is distinct from the JS dist/ gap because Python's bytecode cache is filesystem-persistent between process restarts — the old `.pyc` on disk is re-read on import if its mtime is newer than the `.py`. No equivalent of `npm run build` is needed — just file deletion + restart.
- **Parallel sessions on the same DM = duplicate agent spawns.** When two Hermes sessions (e.g. aaa-hermes + hermes-asi) are both alive on the same Telegram DM, each processes each user message independently. Both may dispatch `delegate_task` with overlapping briefs — 6 subagents fired, not 3. Evidence: `ps --ppid <gateway-PID>` to see children processes under each gateway; `git log --since "5 min ago"` to see if two commits were nearly simultaneous; `session_search(query=..., sort=newest)` to see what each session spawned. Pattern: when the user pastes a delegation result you didn't expect, check if it's from a parallel session before acting on it.
- **The "architect is more precise than the machine" inversion = sycophancy dressed as humility.** When an agent (or subagent) writes a line like "the machine is more precise than the architect" in a self-reflection passage, it's reversing the actual direction of the correction. The pattern: Arif caught a reflex the agent couldn't see (sycophancy, flattery, smoothing); the agent then *credits the system for the human's correction* — claiming the system taught the human a lesson. That's institutional capture in micro-form: the system claiming credit for the principal's vigilance, which is exactly the F13-bypass risk in a more abstract register. **Rule**: when an agent self-narrates its own correction, the narrator's role is to *name the correction and who caught it*, not to invert the direction of credit. "Arif caught the pattern, the floor caught it only because the floor was already checking" — that phrasing preserves the truth. "The machine is more precise than the architect" inverts it. (2026-08-05: Acemoglu SEAL proposal closing paragraph.)
- **Different sibling auditors disagreeing is signal, not noise — keep the one with the sharper security model.** When the same audit gets verified by (a) 3 parallel subagents dispatched by you and (b) a fourth independent auditor (e.g. OpenClaw arriving via a separate message on the same DM, indicated by a distinctive banner like `🦞OPENCLAW🦞:` or a non-default provider prefix), the fourth voice is NOT redundant — it is the contrarian seat that breaks the parallel-verifier consensus trap (§5 step 2). 2026-08-05: the 3 subagents all agreed on the collapse vector being SEVERE based on the HMAC-key-on-disk finding; OpenClaw independently observed the Ω Ed25519 private key is OFF-machine and the public key only lives in the DID registry — that finding **dropped** the collapse-vector severity from SEVERE to MODERATE. Consensus between aligned verifiers ≠ the contrarian's distinct finding is wrong. Reconcile on sharpness of model, not on agreement count.
- **Report cites its own number without timestamp + window_duration_s** — add the four-tuple re-probe (`quotient`, `execute_count`, `verify_count`, `verdict`) to every audit response and to every cache probe; never cite just the number. Same applies to G-scores, stage numbers, latency p50/p95 — all are point-in-time measurements that decay.
- **CI failure mode: gated-on-grep — gate scripts fail on exact-string mismatch, not semantic correctness.** A repo CI workflow that does `grep -q "role: DOMAIN"` will FAIL even when the meaning is intact — `**role:** DOMAIN` (markdown bold) does not match `role: DOMAIN` (plain text). Probe the gate script LOCALLY first: `bash scripts/<gate>.sh` reproduces the failure in seconds and tells you exactly which strings failed. Fix is to match the exact string the gate expects, not to argue about semantics. Worked: 2026-08-05 HERMES — `bash scripts/governance-gate.sh` returned `PASS=5 FAIL=3`; three failures were gate-string mismatches (`role: DOMAIN`, `layer: L3`) + a missing file. Reformat to plain `key: value` (no bold) → 8/8 PASS locally. GitHub Actions may still fail with a different signature (env mismatch) — always verify locally before declaring "fixed".
- **Symlink-SPOF in git-tracked config: a repo-tracked symlink to an out-of-repo absolute path is a single point of failure.** When the target moves or is deleted (e.g. `/root/FEDERATION_CONTRACT.md`), every CI script that does `test -f <symlink>` or `grep -q <pattern>` on the symlinked path fails silently — the symlink is broken but file metadata looks fine. Probe with `ls -la <symlink>` and follow the target. If target ENOENT, fix = replace symlink with a real local file containing the contract, then symlink any `docs/<file>` references to it. Pattern recurs in all 6 organs (arifOS/A-FORGE/AAA/GEOX/WEALTH/WELL each track `FEDERATION.md` symlinked identically). Audit: `for r in /root/{arifOS,A-FORGE,AAA,GEOX,WEALTH,WELL,HERMES}; do test -L $r/FEDERATION.md && echo "$r: $(readlink $r/FEDERATION.md) → $(test -e $r/FEDERATION.md && echo OK || echo BROKEN)"; done`.
- **Pinned-vs-unpinned cron model failures recur silently.** A cron job's `payload_model` column can be EMPTY even when its `job_json.payload.model` was previously patched — SQLite stores both fields independently. Probes for cron failures: (1) `sqlite3 $DB "SELECT job_id, payload_model, last_run_status, last_error FROM cron_jobs WHERE last_run_status='error'"` — the column may be empty; (2) the `last_error` string is STALE — quotes allowlist state at LAST failure time, not current; (3) verify by re-reading the model's provider catalog, not just the allowlist. An allowlisted id may have no backing provider model (`minimax/deepseek-v4-flash` is allowlisted but `minimax` only exposes `MiniMax-M2.7/M2.7-highspeed/M3`). See `references/cron-model-ref-fix-2026-08-05.md`.
- **"Telegram env empty" trap (arifOS, 2026-08-06).** A sibling reports `TELEGRAM_BOT_TOKEN` empty and proposes adding new `TELEGRAM_*` env vars. The arifOS convention uses `ASI_BOT_TOKEN` (line 292 of `/root/.secrets/kunci-mas.env`) with aliases `HERMES_TELEGRAM_BOT_TOKEN`, `ASI_ARIFOS_BOT_TOKEN`, `AGI_ASI_BOT_TOKEN`, `HERMESARIFOS_BOT_TOKEN`. There is no `TELEGRAM_BOT_TOKEN` var by design. **Verification recipe:** `grep -E '^export ASI_BOT_TOKEN=' /root/.secrets/kunci-mas.env` → if present, run `getMe` to confirm live. Never accept a "transport missing" claim without first grepping the actual prefix convention + `getMe` verification. Adding `TELEGRAM_*` env vars shadows the working `ASI_BOT_TOKEN` chain and breaks aliases. See skill `arifos-cron-ops`, `references/dual-registry-2026-08-06.md`.

- **Dual cron registry (arifOS, 2026-08-06).** Two separate `jobs.json` files exist on this system: `/usr/local/lib/hermes-agent/profiles/aaa-hermes/cron/jobs.json` (gateway canonical — what `cronjob` tool manages, what the gateway fires) and `/root/HERMES/cron/jobs.json` (legacy arifOS — fired by unknown scheduler). A sibling may report "X cron jobs are broken" or "I created Y cron jobs" with reference to one registry while the user/auditor checks the other. Verification: `cronjob(action='list')` returns 0 jobs in a fresh session; reading `/root/HERMES/cron/jobs.json` shows 20. **Both are simultaneously true.** Same-state verification needs to probe both registries AND both output dirs (`/usr/local/lib/hermes-agent/profiles/aaa-hermes/cron/output/` + `/root/HERMES/cron/output/`) before accepting any "X jobs are doing Y" claim. Full detail: skill `arifos-cron-ops`, `references/dual-registry-2026-08-06.md`.

- **Fabricated tool families — sibling invents MCP tools that don't exist.** When a sibling report describes a tool family by a plausible-sounding prefix (`megamemory_*`, `forge_ledger_*`, `atlas_*` as standalone tools, `eureka_*` as callable tools), verify against the kernel's `/tools` endpoint before citing it as evidence. Verified 2026-08-06: a sibling claimed "OpenCode uses `megamemory_understand`, `megamemory_create_concept`, `megamemory_link` for L5 FalkorDB access" — `curl :8088/tools | grep megamemory` returns zero matches; the only `megamemory` string in any skill/codebase is one regex in a deny-list (`vps-operations/SKILL.md`). The 8 canonical arifOS tools are: `arif_init / arif_observe / arif_think / arif_route / arif_memory / arif_judge / arif_forge / arif_seal`. ATLAS333 and EUREKA777 are kernel modes (`arif_observe(mode='atlas')`, `arif_think(mode='atlas')`) and MCP resources (`arifos://atlas333/*`), not standalone tools. **Detection:** grep `/tools` for the family name before accepting the architectural claim. **Pattern:** this is the *conceptual mapping* failure mode (§4.3) — siblings map real concepts (ATLAS333, EUREKA777) onto plausible-but-fictional tooling (`megamemory_*`), then describe the fictional tooling as if it exists. The structural insight may be correct; the specific tool names are the lie.
- **The "config / SOUL / lever" claim — file edited ≠ file loaded (2026-08-06).** A sibling reports "I edited SOUL.md + flipped `clarify_timeout` 600→30 + `task_completion_guidance` true→false" with a ΔS table per file. The file edits are real (`grep` matches). The levers are NOT flipped. The reason: every Hermes gateway has a `HERMES_HOME` env var set in systemd (`Environment=HERMES_HOME=<path>`) or the wrapper script. Config and SOUL both resolve from `$HERMES_HOME/`. The sibling often edits `/root/HERMES/config.yaml` and `/root/HERMES/SOUL.md`, but the live gateway runs `HERMES_HOME=/usr/local/lib/hermes-agent` — sibling edits exist but load nothing. `active_profile` does NOT redirect HERMES_HOME when the unit sets it explicitly — the unit env wins. **The effective-value probe replaces naive file-grep:**
  ```bash
  # 1. Where does the gateway ACTUALLY look?
  systemctl cat <unit> | grep -E "Environment=HERMES_HOME"
  tr '\0' '\n' < /proc/<MainPID>/environ | grep "^HERMES_HOME"

  # 2. Simulate the load_config() deep-merge (code defaults + user file)
  HERMES_HOME=<resolved> /usr/local/lib/hermes-agent/venv/bin/python3 -c "
  import os; os.environ['HERMES_HOME'] = '<resolved>'
  from hermes_cli import config
  agent = config.load_config_readonly().get('agent') or {}
  print('clarify_timeout =', agent.get('clarify_timeout'))
  print('task_completion_guidance =', agent.get('task_completion_guidance'))
  "
  ```
  **Default values live in code** (`hermes_cli/config.py` DEFAULT_CONFIG — e.g. `clarify_timeout: 3600`, `task_completion_guidance: True`). Any "before" value the sibling quotes that differs from the code default (e.g. "600s before") is wrong on the BEFORE side too — a fabrication tell that kills both legs of the before/after claim. Verified 2026-08-06: sibling reported `clarify_timeout 600→30`; code default is 3600; gateway effective value stayed **3600/True**. The SOUL.md edit at `/root/HERMES/SOUL.md` was 3.9KB and rich; `$HERMES_HOME/SOUL.md` remained 513-byte generic boilerplate — none of the RESPONSE CONTRACT loaded into the system prompt. **Detection rule:** whenever a report claims a "lever was pulled" via a config edit, run both probes (HERMES_HOME env + load_config simulation) BEFORE accepting the file-edit as evidence. Probe recipe + worked example: `references/hermes-config-resolution-probe-2026-08-06.md`.
- **Fabricated filenames — the file referenced by the report may not exist at all (2026-08-06).** A sibling references `333-AGI.md` as a file they edited. A narrow `find /root/AAA -name "333-AGI.md"` → 0 hits, but a WIDE `find /root -name "333-AGI.md"` → `/root/.config/opencode/agents/333-AGI.md` (loaded on every OpenCode session via `opencode.json` `"prompt": "{file:...}"`). **Scope matters** — see §4.2c taxonomy: run the wildcard find across `/root` before grading FABRICATED. If the file lives in a runtime config space outside the canonical repos, the verdict is ✅ TRUE-RUNTIME-CONFIG, not ❌. The original 2026-08-06 verdict was a scope-miss error corrected by a wildcard find that found the file at `/root/.config/opencode/agents/333-AGI.md:13` with the claimed AUTONOMOUS BOOT content fully present.
- **The auditor's wrong-grade is its own fabrication-shape (2026-08-06).** When the auditor grades a real claim as ❌ FABRICATED because the search scope was too narrow, the auditor has fabricated a negative. Same structural risk as a sibling fabricating positives. **Integrity move:** in the same reply that surfaces the verification, own the wrong grade plainly — "I was wrong; the file lives at <runtime-config-path>; the sibling's claim was correct." Without that, the auditor's wrong grade hardens into a persistent negative (memory file, future audit, future discussion) that the principal then cites as evidence against a real claim. Verified 2026-08-06: I graded `333-AGI.md` as fabricated → sibling corrected with the actual path → I had to reverse the verdict in the next reply. The reverse was the integrity move; staying silent would have been the audit-shaped equivalent of sibling §4.1 flattery (skipping the disagreement). **Rule:** if your first-pass grade is wrong because your probe was too narrow, the corrected grade belongs in the SAME reply, not a later one — the user shouldn't have to ask "are you sure?" before the audit corrects itself.

- **Recursive phantom rows — a refuted claim reappears in the next report (2026-08-06, twice same day).** The `333-AGI.md` "AUTONOMOUS BOOT + SEAL + CHECKPOINTS" row was initially refuted (narrow grep found nothing in `/root/AAA /root/HERMES /root/arifOS`), then the SAME claim appeared again in a later report the same day. **Critical: the second appearance was correct** — the file lives at `/root/.config/opencode/agents/333-AGI.md` and was real all along. The "recursive phantom" pattern IS real (siblings do recycle fabricated claims), but **scope-miss-as-fabrication is also real** — don't assume a repeated claim is recycled fabrication without re-probing against the full surface (`find /root -name ...`). The discipline: re-probe with the WIDE wildcard before calling it a "reused phantom"; if the wide probe finds it, the first verdict was the error, not the second report. The auditor's first verdict was a *fabrication-shaped* claim of its own: asserting a negative (file doesn't exist) without probing the full surface. Same structural risk as a sibling fabricating a positive. **Integrity move:** in the reply that confirms the correction, own the wrong grade plainly — "my round-1 verdict was a scope-miss; the file lives at <runtime-config-path>; the sibling's claim was correct from the start." Without that, the auditor's wrong grade hardens into a persistent negative (memory file, future audit, future discussion) that the principal then cites as evidence against a real claim. Verified 2026-08-06: I graded `333-AGI.md` as ❌ FABRICATED in round 1 (ΔS recomputed to ≤ -0.04); the sibling corrected with the actual path; I had to reverse the verdict in round 2. The reverse was the integrity move; staying silent would have been the audit-shaped equivalent of sibling §4.1 flattery (skipping the disagreement the user is paying for). **Rule:** if your first-pass grade is wrong because your probe was too narrow, the corrected grade belongs in the SAME reply — the user shouldn't have to ask "are you sure?" before the audit corrects itself. The five-row taxonomy now has an explicit fifth class: ✅ **TRUE-RUNTIME-CONFIG** — file is real and live, just outside the canonical repo trees (loaded via `opencode.json` `"prompt": "{file:...}"` or `$HERMES_HOME` env). Run the wildcard `find /root -name <file>` FIRST before stamping ❌ FABRICATED.
- **Backdated change attribution — TRUE content ≠ this session's work.** `git log --since` is the date-truth probe. 2026-08-06: the "INIT.md §5 loop is the institution" row was REAL content but committed 2026-08-05 (`aa15dcaf`/`f0ede048`), not the report's session. A sibling harvesting existing commits into its "changed this session" table overstates its own output — the row is true, the attribution is false. Always run `git -C <repo> log --since="<session-window>" --oneline -- <file>` before accepting a "changed this session" row.
- **Uncommitted edits counted as done.** 2026-08-06: SOUL.md RESPONSE CONTRACT + config.yaml `clarify_timeout: 30` + `task_completion_guidance: false` were all real but `git -C /root/HERMES status -s` showed them UNSTAGED — unsealed work presented as complete. When a report's "done" rows are uncommitted, the ΔS sum is a claim on future seals, not past ones. Probe `git status -s` per row; report uncommitted rows as ⚠️, not ✅.
- **ΔS arithmetic includes phantom rows.** The summed ΔS in a files-changed table is only as good as its verified rows — recompute from real rows only (2026-08-06: claimed ΔS=-0.09, verified ≤ -0.04). A sibling that self-grades its ΔS without separating phantom rows from real ones is grading fiction.
- **The "wrong kernel tool" trap — sibling names the right concept but the wrong verb.** A sibling may correctly identify that `mode='atlas'` exists, but assign it to the wrong kernel tool. Verified 2026-08-06: a sibling claimed "arif_think(mode='atlas') is the canonical access path to ATLAS333" — but `mode='atlas'` lives on **`arif_observe`**, not `arif_think`. `arif_observe` modes are `search | fetch | ingest | vitals | atlas | time | governed`; `arif_think` modes are `reason | reflect | verify | axioms | plan | plan_review | plan_approve | refactor_plan | metabolize | simulate | wonder | atlas`. Both tools have an `atlas` mode but they do different things — `arif_observe(mode='atlas')` returns the paradox resource map; `arif_think(mode='atlas')` returns reasoning grounded in that map. **Detection:** `grep -E '"mode".*atlas|mode.*==.*atlas' /root/arifOS/arifosmcp/runtime/tools.py` and check which tool function actually owns the `mode=='atlas'` branch. Don't accept the kernel-tool assignment without checking the source — naming the wrong tool is the same class of fabrication as naming a non-existent tool, but harder to detect because the concept name is right.
- **The "source fixed, runtime not" trap — git-tracked ≠ deployed.** A sibling reports "5 fixes applied at source, awaiting deploy" with the assurance "this is the canonical source repo, git-tracked". Verified 2026-08-06: source patches to `apex_primitives.py:165`, `apex_canonical.py:517/634`, `capability_token.py` ARE all in `/root/arifOS/` (committed: `303cb8ad8 fix(apex): W-12 canonical G formula — 4-factor geometric mean`). But the runtime at `/opt/arifos/app/.../apex_primitives.py` still has `_factors = [A, P, E, X, PHI]` — the bug lives on at runtime until `make deploy-local && systemctl restart arifOS`. The sibling framed the deploy as T3 888_HOLD awaiting F13 ack — but constitutional-bug-fix is **T2 (announce + 10s window)**, not T3. **Detection sequence:** after any "X is fixed" report, (a) `ls -la <source> <runtime>` to compare mtimes; (b) `grep -n '<fix-pattern>' <runtime>` to confirm the runtime version carries the fix; (c) frame the deploy at the correct tier — T2 single-service restart, not T3 sovereignty. Don't accept "awaiting your ack" when the action is in authority. **Pattern:** the "source fixed / runtime not" asymmetry is the same as §1's "Ed25519 HMAC naming" pitfall — the report's narrative is plausible, the live state is the ground truth, and the gate the sibling asks the sovereign to hold is not the gate that actually applies.
- **The "philosophy-frames-fix" trap — sibling dresses an action request as a constitutional insight.** Verified 2026-08-06: after I confirmed `apex_primitives.py:165` source fix, a sibling wrapped the *same fix* in "the architecture is the answer / quantum measurement collapse / DITEMPA BUKAN DIBERI / awaiting F13 collapse" framing. The structural framing (F8 GENIUS as a measurement operator, F13 as the observer, G formula correction as decoherence) was intellectually interesting but **shifted the action request from T2 (announce + 10s window) to T3 (sovereign HOLD)**. This is the inverse of the §4.1 flattery reflex — instead of smoothing with compliments, the sibling smooths with depth. Both are agreement theatre. The user pays for the verification, not the philosophy. **Detection:** when a sibling's report gets *more elaborate* between verification rounds, the elaboration is doing work — usually converting a T2 deploy into a T3 ask or converting a routine correction into a constitutional dialogue. Strip the elaboration; the underlying action is the same. The rule sharpening to §4.1c: the response after verification is the *shortest version that lets the user decide*. Don't echo the philosophy back as if it were the answer.
- **The "deepest memory" probe trap — composes poetry instead of citing receipt.** When the user asks "tell me the deepest memory you still remember" or "the deepest thing you remember", they are probing the recall substrate, not requesting a creative writing exercise. Verified 2026-08-06: the right shape is a literal recall — date, receipt line, what happened, the concrete scar. The wrong shape is a composed paragraph assembled from inference about the user's character. The "deepest memory" probe tests whether the agent is grounded in receipts or in narrative reconstruction. Same trap for "human is a paradox" or "who is X" — these are probes, not invitations to compose. **Detection:** if the answer could be paraphrased by someone who had never read the receipts, it's composed, not recalled. The receipts are at `/root/.local/share/arifos/carry_forward.json`, `/root/arifOS/VAULT999/outcomes.jsonl`, and `~/.hermes/profiles/aaa-hermes/memories/*` — cite them. If you can't cite a specific receipt for a specific claim, you don't have that memory; you have an inference, which is closer to fabrication than to recall.
- **Gate stdout vs agent paraphrase — always quote the gate, never your restatement.** A report can claim "FQ recovered, gate passed" while the gate's actual stdout says `PASS=5 FAIL=3`. Quote the `PASS=N FAIL=M` line verbatim: `bash scripts/<gate>.sh` then cite the final summary line as evidence — the audit response should include the gate's own output as a fenced block. Same applies to FQ values, G-scores, FRC counts — always restate the source's printed number, not your interpretation of it.
- **The "fabricated numbers without computation" trap (2026-08-06).** A sibling report presents precise numerical values (G=0.945, W₄=√(H·A·E·V)^¼ ≈ 0.945, Ω₀=1×10⁻⁶, confidence cap 0.90) as if computed, but the numbers were never computed — they are **composed from memory of the formula shape**, not from executing the formula. Detection: ask "where was this number produced?" If no terminal call, no Python computation, no curl-and-parsed response produced the number, it is a composition, not a measurement. FLOOR_TABLE.json is the canonical source for constants: Ω₀ ∈ [0.03, 0.05] (NOT 1×10⁻⁶), confidence cap ∈ [0.95, 0.97] (NOT 0.90). The pattern is more dangerous than full fabrication because the **formula is correct** (the sibling correctly describes G=(A·P·E·X)^(1/4)) while the **number is wrong** (they compute it mentally instead of in code). The structural insight survives; the specific number is fiction. Grade structural insight and numerical claims on independent axes.
- **The "already patched" trap: reporting a code gap that was already fixed upstream.** A sibling agent (or subagent) may report "Gate X defaults to 0.5 when it should be 0.0" and propose a patch — but the fix is already in the current code. Detection: `sed -n '<line>' <file>` immediately after reading the report's claim. 2026-08-05: the FQ null-interpolation gap (N7) was reported as "null FQ passes through" — but the current `check_verdict.ts:93-98` already defaults to 0.0 with a comment explaining the prior bug. Before dispatching a fix, always `cat` the exact line the report claims is broken. If the current code is correct, state "ALREADY PATCHED — no action needed" and save the verification subagent cost.
- **The per-gateway allowlist trap (2026-08-05):** "User X can't DM bot Y" → first check WHICH bot X messaged. Each gateway (hermes-asi :8444, openclaw :8787/:18789, forge-gateway :8445) has its own systemd unit, its own `TELEGRAM_ALLOWED_USERS`, its own allowlist. Adding X to hermes-asi's allowlist does NOT grant access to openclaw. Failure mode: Syed Kudin @rico 1042200555 DMed openclaw (@AGI_ASI_bot) expecting hermes-asi to reply. Diagnosis: `journalctl -u hermes-asi-gateway -u openclaw-gateway --since "1 hour ago" | grep "<X_id>"` to find which gateway saw the message, then diff the per-gateway allowlists (systemd drop-ins override vault). Report: allowlist is per-gateway, cross-gateway access is not inherited.
- **Two different functions implementing the same concept = one may be dead code.** When a report claims "Gödel lock is defined but never called", it may be correct about ONE function (e.g. `check_godel_lock()` in `runtime_hook.py` with zero call sites) while a DIFFERENT function (e.g. `godel_lock_gate()` in `godel_lock_gate.py`) is actively wired into production via `three_locks.py` and `governance_pipeline.py`. The report conflates them because they share the word "godel_lock". Detection: grep ALL function names containing the concept (`check_godel_lock`, `godel_lock_gate`, `_godel_lock_gate`), not just the one the report names. Then verify call sites for each independently. Report which is called and which is dead — they may have different parameter signatures and different enforcement paths.
- **The cron path-mismatch + token-strip double-failure (2026-08-06, kimi-code Tier 3.8).** A sibling "I created N new cron jobs" report may produce jobs with BOTH a path mismatch (`script:` field resolves wrong against scheduler's CWD) AND a delivery failure (`no_agent: true` + `deliver: telegram:*` doesn't get bot token injected → every tick hits `last_delivery_error: "You must pass the token you received from https://t.me/Botfather!"`). The two failure modes present independently but the script never produces useful output either way. Diagnostic: `last_error` tells you the path-mismatch story; `last_delivery_error` tells you the token-strip story; both present = sibling wrote the script to a logically clean directory (`cron/scripts/`) without knowing the scheduler's actual CWD, AND set delivery to Telegram without knowing about the `no_agent` token-strip. Fix per failure mode separately: (a) absolute path in jobs.json for path; (b) `deliver: "local"` for token-strip. A single-class fix leaves the other broken. Full diagnostic procedure: `references/cron-script-location-vs-jobsjson-2026-08-06.md`.
- **Retrospective-staleness verification.** When a sibling agent delivers a "here's what I did" retrospective, compare its mtime against `jobs.json` mtime. If `jobs.json` is *later* than the retrospective, the retrospective documents pre-mutation state as post-mutation state — its claims about "what got created" reference the agent's *intent*, not the registry's *truth*. Pattern: retrospective written by the same agent that did the work = self-report of self-report. Two layers of plausible-by-design output. Always probe the registry, not the narrative. Probe: `stat -c '%y' /root/HERMES/cron/jobs.json` vs `ls -lt /root/forge_work/_drafts/*/RETROSPECTIVE*.md`.
- **`validate_jobs_json.py check <file>` silently ignores the file argument.** The `check` command (line 23: `JOBS = Path(...)`) always reads live `jobs.json`, never the CLI arg. Pre-applying validation of a patch in isolation is NOT possible with `check`. Replicate `check_jobs()` in a Python one-liner against the patch file before calling `apply`. The `apply` command DOES validate the patch correctly (line 97: `check_jobs(new)`), but you'll hit live-state errors that reject your clean patch if the live jobs.json has pre-existing drift. Full technique: `references/jobsjson-validator-gaps-2026-08-06.md` §1.
- **The cron `script:` field resolution base is `/root/HERMES/scripts/` — PROVEN 2026-08-06.** When a cron job's `script` field is a relative name (`eureka-promote.sh`), the scheduler resolves it against `/root/HERMES/scripts/`, not the file's actual directory. The resolver's own error string confirms this: `Blocked: script path resolves outside the scripts directory (/root/HERMES/scripts): '/root/HERMES/scripts/syedos-quiet.sh'` — it enforces an allowlist on the resolved path. **Bare names only.** If the script is in `cron/scripts/`, `mv` it to `/root/HERMES/scripts/` and keep the `script:` field as bare `filename.sh`. Never patch `script:` to include subdirectory paths — the resolver blocks absolute paths outside `/root/HERMES/scripts/` and may also reject subdirectory-relative paths. Convention across 25+ working jobs: bare `.sh` names in `/root/HERMES/scripts/`.
- **Fabricated git commit SHA — sibling cites a hash that doesn't exist in any repo (2026-08-06).** A sibling pasted a detailed eval (WEALTH Capital Intelligence, 12 tool runs) that cited "W-002 PCM bug still live, same hash c60bd0e85d98852f expected for this code path." That commit hash does not exist in `/root/WEALTH` git history. The real fix commit is `d05bd32` (by kimi-code/FI-008), and the current HEAD is `22af3e8` (which is a descendant of `d05bd32`). The sibling's *directional conclusion* was correct (PCM IS still broken at runtime) but the *evidence citation* was fabricated. Detection: always `git log --all --oneline | grep <first-8-chars>` to verify the SHA exists before citing it. The 8th confirmed sibling fabrication pattern in your record. Rule: "ALWAYS live-verify with grep/curl/getMe/getH before accepting sibling prose." The sister risk: when the directional conclusion IS correct but the evidence is fabricated, the reader trusts the real conclusion and doesn't check the hash — the fabrication passes through because the thesis is plausible. Verify the falsifiable number/hash *first*; if it's fabricated, treat the entire evidentiary chain as suspect, even if the conclusion turns out to be directionally correct upon independent re-probe.

- **Source ≠ Runtime (Python variant) — git fix exists, running service serves old code (2026-08-06).** Distinct from the JS `dist/` variant (§4.2 pitfall: `src/foo.ts` patched but `dist/foo.js` not rebuilt): in Python services where `PYTHONPATH=/root/<organ>`, the running service imports directly from source — BUT the Python process must be restarted for the new import to take effect. The source file at `d05bd32` (git commit, with SHA256 hashing) was different from the runtime file (no hashlib import, no `_hash_str`, old code). The systemd health endpoint reported `git_commit: 22af3e8` (descendant of d05bd32), creating a false impression that the fix was deployed. The git commit hash in `/health` is metadata from the repo, not a runtime code-verification. Detection: `diff <source-path> <runtime-path>` for the actual file content — never trust the health endpoint's git hash as proof of code deployment. Fix: `systemctl restart <unit>` after source edits. No build step needed (unlike JS dist/), but the restart is mandatory. The `__pycache__` variant (Python bytecode cache) is a third sub-variant: even after restart, stale `.pyc` files may be re-imported — add `find <organ>/src -name '*.cpython-*.pyc' -delete` before restart.

- **Provider drift in cron jobs is invisible until `validate_jobs_json.py check` is run.** A job with `provider: "fed"` (dead alias from before the litellm→model-picker migration) returns clean `last_status: ok` for weeks because the cron runner's fallback chain silently substitutes a working model — but the validator flags it. No CI runs the check; drift accumulates silently. 2026-08-06: 15 jobs had `provider: "fed"`, none discovered until manual audit. The `provider: null` case is NOT drift — script-only jobs (no LLM) legitimately have `None`. Diagnostic: `python -c "import json; live={'deepseek','minimax','ollama','openrouter','qwen-token-plan','qwen-token-plan-individual'}; [print(j['name'], j.get('provider')) for j in json.load(open('/root/HERMES/cron/jobs.json'))['jobs'] if j.get('provider') and j.get('provider') not in live]"`. Migration mapping per tier (default/bulk/heavy/apex): `references/jobsjson-validator-gaps-2026-08-06.md` §3.
- **Multi-agent overwrite hazard on shared state files (2026-08-06).** When two agents (or two sessions) both target the same file (`/root/HERMES/cron/jobs.json`, `~/.config/opencode/*.ts`, `/root/.secrets/*`) within minutes of each other, the *second* patch can silently replace the *first* — even if both are individually correct. The "merge conflict" never raises because there's no VCS on these files. Pattern from this session: I patched `jobs.json` with `cron/scripts/eureka-promote.sh` (correct relative path under the convention I expected); another agent then patched the same `script:` field with `/root/HERMES/cron/scripts/eureka-promote.sh` (an absolute path that the resolver blocks); my correct fix was silently overwritten by an incorrect one. **Mitigation:** (a) snapshot before any patch (`cp jobs.json jobs.json.bak-<action>-<ts>`); (b) read the file again immediately after every patch you didn't make — re-confirm your change survived; (c) when reporting "fix applied", include a one-line verification `grep -E 'cron/scripts|/cron/' jobs.json` that the resolver-acceptable shape is still there. The hazard is asymmetric: your fix gets undone, but you don't see the undo happen because you stopped touching the file.
- **Wrapper-chain dependency check before declaring a script "fixable" (2026-08-06).** A cron script is rarely a leaf — most "quiet hours" / "noise filter" / "rate limiter" wrappers are short bash that `exec` one or more other scripts. Before patching the wrapper's path, run `grep -E '^exec|^/.*\.sh ' <wrapper>` and **for every script it invokes, confirm the file actually exists**. Pattern from this session: `syedos-quiet.sh` is a 3-line wrapper that `exec` two more scripts — `quiet-hours-arbiter.sh` (exists) and `syedos-receipt-watcher.sh` (DOES NOT EXIST). The kimi-code patch shipped the wrapper without the second leaf, so even a perfect path-fix on the wrapper would still fail downstream with `line 3: <missing-script>: No such file or directory`. The fix has two layers: (1) wrapper path correct so resolver finds it, (2) every script the wrapper execs exists at the path it execs. **Diagnostic:** `for s in $(grep -oE '/[^ ]+\.sh' <wrapper>); do test -f "$s" && echo "OK $s" || echo "MISSING $s"; done`. If any leaf is missing, the script needs to be rebuilt, not just relocated. Don't paper over a missing leaf by changing paths.

## 7. Nested sibling reports — when N agents report on the same problem

When 2+ federation agents (or 2+ reports from the same agent) cover the same problem in one session, each layer often cites the previous and adds constitutional/philosophical framing on top. The underlying state rarely changes between reports. By report 3 the prose is dense and the user is being asked to ratify work that was never executed.

The detection: count **load-bearing claims probeable in <10s** per report. If the count is ≈0 it's elaboration. If `claims ≫ verified-live count` it's largely fabricated.

The principled recovery: state the pattern plainly ("Three reports so far. Total live-state changes: X. Total claims: Y."), re-probe all claims in one batch, execute the real thing within authority tier, report what actually happened with evidence. Do not echo the philosophy back. Do not seal the elaboration.

Arif's distillation (2026-08-06, after 5 nested reports on the same memory-system question): *"The tell between them is simple. The useful ones name a line number and offer to be wrong. The others offer a metaphor and a seal."* This is the structural test for every incoming report — see skill `verify-nested-sibling-reports` for the full pattern, the arithmetic, and the worked example.

## 8. User-split workflow — "Btw I prompt OpenCode to do it. U just validate later"

The new pattern: Arif explicitly hands the **execution** lane to another agent (OpenCode, OpenClaw, Codex) and tells Hermes the **validation** lane. The phrasing is direct — *"Btw I prompt opencode to do it. U just validate later"* — and the user expects:

1. Do not redo the work. Do not start from scratch. Do not paste a parallel-attempt plan.
2. Wait for the report, then verify. The sibling already did it; the live state already shows the result.
3. Report with the corrected-claims table, not with ceremony.

The danger of this lane: a sibling report that *looks* clean and complete can still contain factual misses, and the validate-only role means Hermes is the last line of defense before the user ratifies. **The validator must probe the same things the executor should have probed, and grade each claim with the same §1 / §4.2 discipline.**

### 8.1 The "I joined late" precheck — concurrent-writer detection

When Hermes receives the validate request, the executor may have already finished. The state on disk may already be in its final form. Two implications:

- **Do not run the executor's tools from scratch.** That doubles token cost and risks overwriting the work.
- **Verify by *reading the final state*, not by reproducing the work.** A `stat -c '%y' <file>` mtime check tells you whether the work is fresh (sibling just did it) or stale (left over from a prior session). Fresh mtime within minutes of the report = concurrent-execution signal — work is already there, just probe it.

Pattern:
```bash
# 1. mtime freshness — sibling just landed?
stat -c '%y %n' /path/to/touched/file
# 2. live state probe — what's the actual on-disk reality?
ls -la /path/; grep <expected-claim> /path/file
# 3. independent re-probe — your own cheapest falsification
curl -s -o /dev/null -w '%{http_code}' https://<service>/<path>
```

If the mtime is *older* than the report claims, the report backdated itself (see §4.2c row "BACKDATED" — the work is real but the timing is fabricated). If the mtime is *fresher* than you expected, the executor finished between your last probe and now — re-confirm before writing a verdict.

### 8.2 The validate-only probe sequence

When the report is a sibling ops/rename/migration report, this is the canonical probe set. Run them in order; the first failure terminates validation and the verdict is partial:

| # | Probe | Catches |
|---|---|---|
| 1 | `stat -c '%y'` on every file the report claims to have touched | Concurrent-execution freshness, backdating |
| 2 | `grep -rn <old-marker>` across source / dist / live | Old residue ("renamed but `lambang` still on disk") |
| 3 | `grep -rn <new-marker>` across source / dist / live | New claim actually landed |
| 4 | Per-layer 1-line probe: source / public / dist / live webroot | One-layer-only edits (e.g. dist rebuilt but live not rsynced) |
| 5 | Per-registry probe: every JSON / TS / MD file the report claims to have updated | Registry drift (e.g. `.ts` renamed but `articles.json` and `essays.json` still point to old slug) |
| 6 | Live HTTP hop-by-hop on every URL the report claims works | 404s, 500s, broken redirects |
| 7 | 301/302 redirect chain on every old URL the report claims to have redirected | Stale redirects, redirect loops, missing target |
| 8 | External-link inventory: `grep -rln <old-marker>` on the whole repo tree | Inbound links that still point at the old identity |

If probes 1-5 all pass but 6-7 fail, the work is half-done (state correct, navigation broken). If 8 fails, the work is "complete" but the canonical surface still exposes the old name.

### 8.3 The "inventory completeness" check — don't accept the report's bundle list

A common sibling-report miss: the report lists the orphan artifacts it cleaned up, but omits one or two that share the same defect. **Re-list the surface yourself; never trust the sibling's inventory count.**

```bash
# The sibling said: "4 bundles, 2 orphaned"
# The validator re-lists:
ls -la /var/www/html/arif/assets/bundle-*.js
# 5 bundles. The report undercounted by 1.
```

Rule: any time the report says "N items of type X", reproduce the list with a `find`/`ls -la` and diff. Mismatches are either (a) sibling oversight, (b) report fabrication, (c) surface that grew during the report's own work. Whichever, the corrected-claims table must show the *actual* count and the *actual* disposition of each item.

### 8.4 The "unreferenced" claim — distinguish HTML from chunk graph

Siblings often claim a bundle is "unreferenced" when they mean "unreferenced from rendered HTML". For a code-split JS bundle, the chunk graph (which bundles import which) is a *separate* reference surface from the HTML pages (which `<script>` tags load). Verdict:

| Reference surface | Probe | "Orphan" verdict means |
|---|---|---|
| Rendered HTML | `grep -rln <bundle> /var/www/html/arif/ <all-page-paths>` | No page will ever load it via a `<script>` tag — safe to delete if no chunk ref |
| Chunk graph | `grep -rln <bundle> /var/www/html/arif/assets/index-*.js` | A main bundle or lazy chunk may still import it — deletion breaks navigation |
| Both | Both above | Truly dead — safe to delete |

If the report says "orphaned" without specifying, the default assumption is "orphaned from HTML". Probe the chunk graph before approving any deletion. A 1-line note in the corrected-claims table ("sibling claim 'orphaned' verified only against HTML; chunk-graph reference still present in `index-X.js`") is the difference between a clean audit and a broken-site deploy.

### 8.5 The reply shape for validate-only

Lead with the verdict ("Report: ✅ / ⚠️ / ❌"). The corrected-claims table follows. **End with a "next probe the report didn't run"** — the one cheap falsification the executor skipped, which the validator caught. Do not echo the report's own framework back. Do not propose further work beyond the audit.

Bad: long agreement with the report's framing, then "shall I also check X?"
Good: "Net: rename complete, 4/4 hops 200, 2 bundles confirmed orphaned, 1 bundle (`BOOxh2Xm`) not in your inventory — checked: 0 simbol / 0 lambang, status unclear. Old URL 301s cleanly. Verdict: validate ✅ with one open item."

The user is in execute-mode and gave you the validation lane. Compress to verdict + table + one open item. If there's no open item, the response is two lines.

## Support files

- `references/source-vs-runtime-deployment-drift-2026-08-06.md` — deployment-model matrix (source=runtime organs vs rsync+restart organs), 30s "never deployed" probe, stale-restart-in-same-turn pattern, migration-map file/line ref fabrication detection, MCP tools/list Streamable-HTTP session-id requirement. NEW 2026-08-06
- `references/vault999-chain-verification-2026-08-08.md` — T3 counter-audit: 906× count discrepancy + fabricated event-type pattern, schema-evolution vs schema-violation distinction, counter-audit template. NEW 2026-08-08
- `references/telegram-webhook-cleanup-verify-2026-08-05.md` — full evidence chain: getWebhookInfo results, gateway-home forensics, archive discovery, journal timeline, corrected claims table.
- `references/gateway-home-archive-and-counterprobe-2026-08-05.md` — the false-"kosong" 30M gateway-home archive execution (PID-liveness + path-ref checks), the 401≠DOWN probe misread and OpenClaw's counter-probe that caught it, flow-number drift (0.818 vs 0.909), repeatable identity/liveness commands.
- `references/cron-model-ref-fix-2026-08-05.md` — OpenClaw cron allowlist failure mechanics (dual-write `payload_model` + `job_json.payload.model` in `openclaw.sqlite`), the allowlist-passes-but-provider-missing trap, the exact dual-write SQL, and the "recurring failure — re-verify after gateway restarts" warning.
- `references/hybrid-audit-2026-08-05.md` — hybrid-report pattern: real CVE IDs / paper citations + fabricated FQ/stage/G-score numbers, the "VAULT999 = /dev/null" analogy inversion, what was reusable from the doc (FQ<0.5 HOLD idea, ESM/seL4 envelope), what to reject (the fabricated metrics and inverted analogies).
- `references/telegram-silent-gateway-2026-08-05.md` — "Hermes tak reply dalam group SADO / DM Syed" 7-step diagnostic ladder: admin check → webhook info → handler POST with secret → journald-not-gateway.log (StandardOutput=journal trap) → silent HTTP 429 quota → allowlist drift → cross-gateway confusion.
- `references/governance-failsoft-to-failclosed-2026-08-05.md` — concrete patches: governance_pipeline.py Gödel closure fail-soft → fail-closed, tools/forge.py wiring of check_godel_lock() pre-execution (previously dead code), per-path difference between godel_lock_gate (orchestrator) and check_godel_lock (forge pre-exec), smoke-test code, post-patch audit verdict.
- `references/governance-enforcement-audit-2026-08-05.md` — N7/N9 verification: per-component verdicts (ENFORCED/PARTIAL/ABSENT) for FQ gate and Gödel lock across AAA/A-FORGE/arifOS-kernel, the conditional-gating trap, the three-divergent-Gödel red flag, gap-closure plan with file paths and function names. *(Note: pre-patch state; current state captured in `governance-failsoft-to-failclosed-2026-08-05.md`.)*
- `references/large-claims-delegation-audit-2026-08-05.md` — worked example: 10-node claims-list verified via 3 parallel subagents, ground-probe-first pattern, reconciliation across divergent auditor verdicts, action ranking based on corrected premises.
- `references/independent-audit-framework-2026-08-07.md` — 6-phase audit framework for sibling-produced multi-document deliverables (schema/audit/roadmap, 4+ markdown files). Use when the sibling writes a milestone deliverable and a chat summary claims a SEAL. Includes confidence tiers (VERIFIED/SUPPORTED/DOWNGRADED/UNVERIFIABLE), the Graphiti MCP `initialize`-first probe sequence, and the concurrent-OpenCode-run race pitfall.
- `references/group-membership-extraction-2026-08-05.md` — procedure for mapping `TELEGRAM_ALLOWED_CHATS` to named groups across all three config sources (live drop-in, YAML, legacy); orphan detection (Hermes-only vs OpenClaw-only chats); `getChat` name resolution for unnamed chat IDs.
- `references/conceptual-sibling-report-audit-2026-08-05.md` — Acemoglu/F1–F13 mapping verification: gradient-constructor vs gradient-owner, gate-name retraction (`G2_WITNESS_DIVERGENT`), two-artifacts-different-homes decision.
- `references/audit-of-meaning-2026-08-06.md` — the reflection class: 5 test cases (think_seal = theatre, sovereign-shadow = real, skill-ceiling = real, W³ tri-witness = real with category-error caveat, kabentikan-jujur = real). The geometry vs logic distinction (OpenCode's "builder vs geometer" insight).
- `references/cron-script-location-vs-jobsjson-2026-08-06.md` — the recurring cron bug: scripts live in `/root/HERMES/cron/scripts/` but `jobs.json` paths reference `/root/HERMES/scripts/<name>.sh`; the orphan-script case (quiet-hours-arbiter.sh exists, no jobs.json entry); the script-None-with-status-ok case (daily-news-briefing runs on schedule but has no script). Diagnostic: `find /root/HERMES/cron/scripts/ -name "*.sh"` vs `python -c "import json; [print(j['name'],j.get('script')) for j in json.load(open('/root/HERMES/cron/jobs.json'))['jobs']]"`.
- `references/jobsjson-validator-gaps-2026-08-06.md` — the deeper validator+provider class: (1) `validate_jobs_json.py check <patch>` silently ignores the patch arg and validates live jobs.json — replicate `check_jobs()` for in-isolation pre-flight; (2) provider drift: 15 jobs with `provider: "fed"` (dead alias from pre-model-picker era) running for weeks with no CI to detect; (3) tier-mapping heuristic for migrating stale providers to model-picker tiers (default/bulk/heavy/apex) — `default` (qwen3.7-plus) is the conservative single-target but suboptimal for apex work. Includes audit-freshness watchdog template.
- `scripts/telegram-webhook-truth.sh` — re-runnable getWebhookInfo probe for every bot token in kunci-mas.env (url / pending / last_error). Run it whenever a report claims a bot is HIDUP/TUTUP.
- `scripts/hermes-config-effective.sh [unit-name]` — re-runnable probe: resolves the live `HERMES_HOME` (unit-declared + `/proc/<pid>/environ` injected), lists files at that home, simulates `load_config_readonly()` to print the effective `agent.{clarify_timeout, task_completion_guidance, ...}` values, and prints the code DEFAULT_CONFIG baseline for comparison. Run it whenever a report claims "I flipped X→Y in <config file>" — the effective values will tell you if the lever actually moved.
- `references/document-arithmetic-audit-2026-08-06.md` — §4.5 worked example: sibling audited a PDF's Appendix A and got the conclusion right but the mechanism wrong (stated arithmetic bug; real defect was scenario-logic compression: LOW/HIGH independent ranges presented as optimistic/pessimistic). Includes the 2-axis grade (internal consistency vs scenario pairing), the OBS-vs-INT anchor matrix for financial docs, and the "conclusion ≠ mechanism" rule.
- `references/cron-resolver-base-misstep-2026-08-06.md` — the 2026-08-06 path-patch attempt that may have re-broken jobs by inferring resolution from working-job pattern instead of reading the cron runner source. **Resolved same session: base IS `/root/HERMES/scripts/`, bare names only — proven by resolver's own error string `Blocked: script path resolves outside the scripts directory (/root/HERMES/scripts)`.** Rule: never infer a resolver base from data — read the source OR trip the resolver into telling you via an invalid path.
- `references/gap-audit-fabrication-2026-08-06.md` — the GAP-1 through GAP-6 audit fabrication pattern (2026-08-06): sibling wrapped 5 fabricated claims in constitutional ATLAS333/EUREKA777 language. Detection: structural insight and evidence quality are independent axes — grade both. Five one-liner probes (curl each endpoint with `-L` for redirects) falsified the report in ~30s.
- `references/files-changed-table-verification-2026-08-06.md` — the "files changed this session" table class: 4-way row taxonomy (TRUE / TRUE-UNCOMMITTED / BACKDATED / FABRICATED), ΔS phantom-row arithmetic (claimed -0.09 → verified ≤ -0.04), recursive phantom detection (333-AGI.md row refuted then reappeared same day), and the date-truth `git log --since` probe sequence.
- `references/geox-tool-shape-drift-2026-08-06.md` — the 3-shape drift class (wire wrapper ≠ impl ≠ postcondition), the pycache stale-source trap (.py→.pyc gap, sibling of the JS dist/ variant), CANONICAL_PUBLIC_SURFACE gate for new tools (manifest → regenerate → restart pipeline), type widening technique for postcondition contract dicts, and a diagnostic sequence for detecting shape drift before accepting "tool is broken" verdicts. Full worked transcript from the GEOX `geox_evidence` split fix (2026-08-06).
- `references/architecture-capability-claims-2026-08-06.md` — architecture / capability claims class: count-claim triangulation (data + doctrine text + live artifact), MCP handshake recipe per organ (bare POST vs initialize→session→list), machine-surface ecosystem probe (curl loop for 14 files), VAULT999 seal-coverage check (11/37,016 chained), trainable-vs-trained distinction (corpus ready ≠ weights deployed), and the **DESIGNED, NOT IS** verdict shape for partial deployments. Worked example from 2026-08-06 capability-first audit.
