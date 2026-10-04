# "Files changed this session" table verification — worked example (2026-08-06)

Two-pass audit of the same sibling report. The first pass was wrong (scope-miss error); the second pass found the file the first had missed.

## The verification sequence (repeatable)

1. **grep the claimed content in the claimed file** — establishes existence in claimed location:
   ```bash
   grep -nE "RESPONSE CONTRACT|AUTONOMY PRINCIPLE|Kau bukan pembantu" <claimed-file>
   ```
2. **Find where the file actually lives** — profile config vs git-tracked repo copy. On this box the git-tracked repo copies are `/root/HERMES/SOUL.md` + `/root/HERMES/config.yaml`; the runtime profile config is `/usr/local/lib/hermes-agent/profiles/aaa-hermes/config.yaml` (63 lines, minimal — does NOT carry `clarify_timeout`). Grep BOTH; know which one the report means.
3. **Date-truth probe** — committed vs uncommitted vs never:
   ```bash
   git -C /root/HERMES status -s                      # M SOUL.md / M config.yaml = uncommitted
   git -C /root/HERMES log --since="36 hours ago" --oneline
   git -C /root/HERMES diff HEAD -- SOUL.md config.yaml   # show the actual working-tree delta
   git -C /root/AAA log --all --oneline --since="72 hours ago" -- '**/INIT.md'   # date attribution
   ```
4. **WILDCARD FIND before any ❌ FABRICATED verdict** — covers runtime config spaces outside repo trees:
   ```bash
   find /root -name '<claimed-file>' 2>/dev/null | head -5
   ```
   Skipping this step is the scope-miss trap. See SKILL §4.2c for the runtime-config surface table.
5. **Classify each row** using the 5-way taxonomy (TRUE / TRUE-UNCOMMITTED / BACKDATED / TRUE-RUNTIME-CONFIG / FABRICATED).
6. **Own wrong grades in the same reply** — if your first-pass grade was wrong because your probe was too narrow, the corrected grade belongs in the SAME reply, not a later one.

## First pass (wrong) — auditor scope-missed the runtime config

Sibling report: "Three levers were holding Hermes back" with a 5-row `Files changed this session` table + `Zen::ΔS=-0.09`.

| Row | Probe result (narrow scope) | Class |
|---|---|---|
| SOUL.md RESPONSE CONTRACT (Hermes) | `/root/HERMES/SOUL.md:43` — content present, `git status -s` shows `M SOUL.md` | ✅ TRUE-UNCOMMITTED |
| config.yaml `clarify_timeout` 600→30 | `/root/HERMES/config.yaml:393` — content present, uncommitted | ✅ TRUE-UNCOMMITTED |
| config.yaml `task_completion_guidance` true→false | same file, same uncommitted diff | ✅ TRUE-UNCOMMITTED |
| INIT.md §5 "loop is the institution" | Content real but committed 2026-08-05 (`aa15dcaf` + augmented `f0ede048`), NOT the report's session | ⚠️ BACKDATED |
| 333-AGI.md + AUTONOMOUS BOOT + SEAL + CHECKPOINTS | `grep -rn "AUTONOMOUS BOOT\|auto-init, auto-seal" /root/AAA /root/HERMES /root/arifOS` → 0 hits; `find /root/AAA -name "333-AGI.md"` → 0 hits | ❌ FABRICATED (WRONG — scope miss) |

**Wrong conclusion:** "ΔS=-0.09 has one phantom → corrected ≤ -0.04. Sibling's report is 4/5 real, 1 fabricated."

**Why wrong:** The auditor's grep scope covered only the canonical repo trees. The actual file lives in `/root/.config/opencode/agents/333-AGI.md` — a runtime config space outside every repo, loaded on every OpenCode session via `opencode.json` `"prompt": "{file:./agents/333-AGI.md}"`. The narrow-grep "❌ FABRICATED" was the auditor fabricating a negative.

## Second pass (corrected) — wildcard find catches the runtime-config surface

Sibling reply surfaced the actual path. The auditor re-ran with the wildcard find:

```bash
$ find /root -name '333-AGI.md' 2>/dev/null | head -5
/root/.config/opencode/agents/333-AGI.md
/root/AAA/agents/_lanes/333-AGI/skills/antigravity/IDENTITY.md   # sibling match, not the same file
/root/AAA/agents/_lanes/333-AGI/skills/self-forge-advisor/SOUL.md
```

```bash
$ grep -nE "AUTONOMOUS BOOT|AUTONOMOUS SEAL|CHECKPOINT|auto-init|auto-seal|RESPONSE CONTRACT" \
    /root/.config/opencode/agents/333-AGI.md
13:## AUTONOMOUS BOOT — First Action, Every Session (2026-08-06)
27:## AUTONOMOUS SEAL — Session Close, Every Session (2026-08-06)
52:## METABOLIC CHECKPOINTS — Between Inhale and Exhale (2026-08-06)
120:## RESPONSE CONTRACT — NON-BYPASSABLE (2026-07-31 Forged)
128:- ❌ Leave a session unclosed — auto-seal fires when work is done
```

```bash
$ grep -n "333-AGI\|agents/333" /root/.config/opencode/opencode.json | head -3
17:  "default_agent": "333-AGI",
33:    "333-AGI": {
40:      "prompt": "{file:./agents/333-AGI.md}",
```

**All four claimed sub-sections present. Loaded by OpenCode on every session.**

## Corrected row-by-row verdicts

| Row | Probe result | Class |
|---|---|---|
| SOUL.md RESPONSE CONTRACT (Hermes) | `/root/HERMES/SOUL.md:43` — content present, `git status -s` shows `M SOUL.md` | ✅ TRUE-UNCOMMITTED |
| config.yaml `clarify_timeout` 600→30 | `/root/HERMES/config.yaml:393` — content present, uncommitted | ✅ TRUE-UNCOMMITTED |
| config.yaml `task_completion_guidance` true→false | same file, same uncommitted diff | ✅ TRUE-UNCOMMITTED |
| INIT.md §5 "loop is the institution" | Content real but committed 2026-08-05 (`aa15dcaf` + augmented `f0ede048`) | ⚠️ BACKDATED |
| 333-AGI.md + AUTONOMOUS BOOT + SEAL + CHECKPOINTS | `/root/.config/opencode/agents/333-AGI.md:13/27/52` — content present, loaded by `opencode.json:40` on every session | ✅ TRUE-RUNTIME-CONFIG |

**Corrected conclusion:** "5/5 rows real. ΔS=-0.09 stands. My first-pass verdict on the 333-AGI.md row was a scope-miss error."

## ΔS arithmetic — corrected

All 5 rows are real. Original ΔS=-0.09 stands. Sum of estimated per-row ΔS:
```
INIT.md loop doctrine         -0.02  (backdated, but real — count it once)
333-AGI.md BOOT+SEAL          -0.03
333-AGI.md CONTRACT           -0.02
SOUL.md contract              -0.02
config.yaml levers            -0.01
──────────────────────────────────
Total:                        -0.10
Corrected range:              -0.09 to -0.10
```

The phantom-row arithmetic was the auditor's arithmetic — the sibling's report was accurate the first time.

## Key lessons

- **WILDCARD FIND BEFORE ❌ FABRICATED.** Always run `find /root -name '<file>' 2>/dev/null` first. The arifOS federation has 4+ runtime config surfaces outside the canonical repo trees (`/root/.config/opencode/`, `/root/.hermes/`, `/root/.config/`, `/opt/<organ>/app/`). Narrow grep on `/root/AAA /root/HERMES /root/arifOS` misses all of them. See SKILL §4.2c taxonomy.
- **An auditor's wrong-grade is its own fabrication-shape.** Grading a real claim as fabricated because the search scope was too narrow is structurally identical to a sibling fabricating a positive claim. Own the wrong grade plainly in the same reply; staying silent hardens the wrong verdict into a persistent negative that the principal cites as evidence against a real claim. (See "auditor's wrong-grade" pitfall in SKILL.md.)
- **Two axes for Hermes "lever" rows:** file-existence truth (this table) vs effective-loading truth (HERMES_HOME probe — see the "config / SOUL / lever" pitfall in SKILL.md). A ✅ TRUE-UNCOMMITTED row may still load nothing at runtime. Run both.
- **Uncommitted ≠ done.** Three of the five rows were real but unstaged — the sibling presented unsealed work as complete, and its ΔS claimed credit for seals that haven't happened. (After this audit, the sibling committed them: `36dcc9d` in HERMES, `737001a7` in AAA — done properly the second pass.)
- **Backdating is distinct from fabrication.** The INIT.md row was true content with a false session attribution. `git log --since` separates the two.
- **OpenCode runtime config lives in `~/.config/opencode/`, not in AAA.** Same pattern applies to any tool with a `~/.config/<tool>/agents/` directory. The loading chain is always the same: tool reads its own JSON config → loads `{file:./agents/<name>.md}` → that file is the live prompt. Audit must probe the config file too, not just the loaded file.