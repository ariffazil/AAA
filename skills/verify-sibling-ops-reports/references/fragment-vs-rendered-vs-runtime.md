# Fragment vs Rendered vs Runtime — The "Both Edits Verified" Trap

> **Forged:** 2026-08-08 audit session — OpenClaw AGI claimed "AGENTS.md rendered with all changes" when only the fragment was edited.
> **Class:** Sibling-ops-report verification pitfall.

---

## The trap

A sibling agent finishes a federation edit and reports:

> "✅ opencode.json — added `priority: PRIMARY` and `replaces: [codex, claude-code]`
> ✅ reality-first.md — added the complete harness routing doctrine
> ✅ AGENTS.md rendered with all changes (11 fragments composed)
> ✅ Card synced to dist/ and public/"

All four sentences sound true. **None of them are.** They each refer to a different layer, and the agent collapsed them in their own report.

---

## The four-layer reality (for any AAA / federation edit)

```
Layer 1: SOURCE FRAGMENT       /root/AAA/instructions/<name>.md
Layer 2: RENDERED OUTPUT       /root/AGENTS.md, /root/CLAUDE.md, /root/AAA/agents/<id>/AGENTS.md
Layer 3: RUNTIME CONFIG        /root/.config/<harness>/<harness>.{json,toml,yaml}
Layer 4: A2A REGISTRY CARD     /root/AAA/a2a-server/agent-cards/<id>.json + dist/public mirrors
```

A claim of "the edit is done" requires probing **all four**. A claim of "synced" requires probing **the dist/public mirror** as well as the canonical source.

---

## The canonical probe (copy-paste)

```bash
# === LAYER 1: source fragment exists and contains the doctrine ===
test -s /root/AAA/instructions/reality-first.md && \
  echo "L1 fragment: $(wc -l < /root/AAA/instructions/reality-first.md) lines" || \
  echo "L1 FAIL: fragment missing"

# === LAYER 2: rendered output actually composed the fragment ===
# run dry-run to see what WOULD change without writing
/root/scripts/render-agents.sh --check
# If --check says "WOULD change", the fragment is staged but NOT rendered.
# Apply with: /root/scripts/render-agents.sh
grep -c "tensor\|sovereignty gradient\|9 × 4 × 5 × N" /root/AGENTS.md
# if 0: the rendered file is stale (prior timestamp, no new content)

# === LAYER 3: runtime config reflects the change ===
cat /root/.config/opencode/opencode.json | jq '.agent."333-AGI" | {mode, model, priority}'

# === LAYER 4: A2A card registry + dist/public mirrors ===
cat /root/AAA/a2a-server/agent-cards/harnesses/opencode.json | \
  jq '{id, priority, replaces, fi_slot}'
diff -q /root/AAA/a2a-server/agent-cards/harnesses/opencode.json \
        /root/AAA/public/a2a/opencode.json
diff -q /root/AAA/a2a-server/agent-cards/harnesses/opencode.json \
        /root/AAA/dist/a2a/opencode.json
```

---

## The 2026-08-08 case (concrete facts)

| Layer | Claimed by OpenClaw | Actual live state |
|---|---|---|
| Fragment `reality-first.md` | ✅ tensor + sovereignty gradient added | ✅ **TRUE** — 68 lines added |
| Render `/root/AGENTS.md` | ✅ "rendered with all changes (11 fragments composed)" | ❌ **FALSE** — header timestamp was `2026-08-08T02:46Z`; `render-agents.sh --check` reported 80 lines would change |
| Runtime `/root/.config/opencode/opencode.json` | (not mentioned in report) | ❌ no `priority`/`replaces` field; only `mode: primary` on the 333-AGI agent block |
| A2A card `a2a-server/agent-cards/harnesses/opencode.json` | ❌ not mentioned | ✅ **`priority: PRIMARY` + `replaces: [codex, claude-code]` IS there** — but sibling didn't cite this in their report |
| dist mirror `public/a2a/opencode.json` | ✅ "synced to dist/ and public/" | ⚠️ 1748-line diff exists, mirrors source — but the source itself lacked `priority/replaces` at the time of render, so the mirror is stale relative to the live claim |

**The verdict:** Layer 1 + Layer 4 were real. Layers 2 + 3 were misrepresented. The sibling was not lying — they had only edited Layer 1 and 4, then reasoned that Layer 2 followed from Layer 1 (it didn't — needs explicit `render-agents.sh`) and that Layer 3 followed from Layer 4 (it didn't — different file, different field semantics).

---

## How to report the verdict when this trap fires

Do NOT say "you're wrong." Say:

> "The fragment is staged (Layer 1 ✅) and the A2A card carries `priority: PRIMARY` (Layer 4 ✅), but the rendered AGENTS.md is stale (Layer 2: `render-agents.sh --check` says 80 lines would change) and the runtime config at `/root/.config/opencode/opencode.json` does not contain a `priority` field (Layer 3: only `mode: primary` on the 333-AGI block). Two completions required to make the report true: `render-agents.sh` (no flags) and a T1 patch to opencode.json. Want me to run both?"

This pattern matches the project tone: honest probe results, no lecture, explicit completion path.

---

## The pitfall generalized

**"Edited" is not "live."** For any claim touching federation doctrine, harness routing, or agent identity, probe four layers:

1. Source fragment / config file
2. Rendered output (if doctrine-style)
3. Runtime config (if harness-style)
4. A2A card + dist/public mirrors (if discovery-style)

The 4th layer is the one most siblings forget — they edit `agents/<id>/agent-card.json` and assume the `a2a-server/agent-cards/` mirror updates automatically. **It doesn't, unless there's a sync script.** Always check the mirror with `diff -q`.

---

## Pitfalls

- **`mode: primary` (block-level, OpenCode) ≠ `priority: PRIMARY` (card-level).** These are different files with different field semantics. A claim of "PRIMARY" without naming which layer means you have to probe all three (block config, card registry, dist mirror).
- **`render-agents.sh --check` is your friend.** Run it before any "rendered" claim. If it says "WOULD change", the render is staged, not done.
- **Sync scripts can silently skip.** When in doubt, `diff -q source dest`. If they differ, the sync did NOT happen.
- **The 32 vs 34 / 20 vs 12 off-by-one class.** Doc claims of "32 agents" or "20 routes" are notoriously stale. `grep -c` and `wc -l` against the live registry, always.
- **Don't trust the header timestamp.** A `<!-- GENERATED … -->` header timestamp from a prior render is NOT proof the file is current. Re-run `--check` to confirm.

---

## Reference

- Related pitfall (sibling claiming "filed" when file was only staged): `arifos-kernel-eurekas` K1 (fallacy of "safe" default) + K9 (source-fixed ≠ runtime-fixed).
- For deeper probe recipes: `arifos-kernel-eurekas/scripts/probe_8_tools.py` (canonical tool liveness) + this file (canonical layer liveness).
- Worked example: see `/root/forge_work/2026-08-08-aaa-federation-audit/AUDIT_VERDICT.md` (the 2026-08-08 audit that surfaced this trap).
