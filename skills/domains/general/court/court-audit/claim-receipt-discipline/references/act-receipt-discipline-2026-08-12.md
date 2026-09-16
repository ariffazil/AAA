# [🦾ACT] Output Gate Substrate Discipline — Companion Reference

> **Forged:** 2026-08-12 (F13 SOVEREIGN constraint, "Taufik Leak")
> **Renamed:** 2026-08-12 — `[EXE]` → `[🦾ACT]` (ACT execution actuator alignment)
> **Constitutional cascade:** `AAA/instructions/exe-receipt-discipline.md` → `AGENTS.md` / `CLAUDE.md`
> **Physical enforcement:** `/root/HERMES/mcp_servers/substrate_output_gate.py`
> **Session origin:** Multi-turn chat with mixed `[OBS]` narration, [EUREKA] 4-base
> DNA reasoning, and Substrate Output Gate wiring.

## Why this reference exists

`claim-receipt-discipline` FM1-FM5 govern claim epistemic tags (`[OBS]`, `[DER]`,
`[INT]`, `[SPEC]`) at the **content** level — "did you back the label with evidence?"

FM6 governs the same tags at the **output** level — "should this label reach F13 at
all?" The answer for pure observation tags: no. They belong at the Metabolize layer,
not the Decode layer.

This is the F13 correction that motivated FM6:

> *"Kalau ejen setakat hantar [OBS] kat hang, itu bermakna ejen tengah buang raw
> cognitive load balik kepada 888. Entropy (ΔS) melantun balik kat hang."*

The cognitive load re-injection pattern: agent narrates → F13 reads → F13 has to
re-evaluate → entropy flows **up** instead of being metabolized down. The Substrate
Output Gate breaks the cycle at the substrate level.

## The 3-rule implementation (reference)

`/root/HERMES/mcp_servers/substrate_output_gate.py` (58 lines, 4 self-tests incl. legacy back-compat):

```python
import re

# NOTE: Regex matches BOTH [🦾ACT] (new) and [EXE] (legacy/VAULT999 back-compat)
_ACT_BLOCK_RE = re.compile(
    r'(\[(?:🦾ACT|EXE)(?:-PARTIAL)?\][^\n]*(?:\n(?!\n\n|\Z).+)*)',
    re.DOTALL
)
_OBS_TAG_RE = re.compile(r'\[(OBS|INT|SPEC|UND)\]')


def intercept(text: str) -> str:
    if not text or not text.strip():
        return ''

    # Rule 2: Pure [🦾ACT] block passes
    act_match = _ACT_BLOCK_RE.search(text)
    if act_match:
        return act_match.group(1).strip()

    # Rule 1: Pure [OBS] without [🦾ACT] drops
    if _OBS_TAG_RE.search(text):
        return ''

    # Rule 3: No recognizable tags — pass through (unsorted prose)
    return text.strip()
```

### Why the regex shape matters

- `_ACT_BLOCK_RE` anchors on `[🦾ACT]`, `[🦾ACT-PARTIAL]`, `[EXE]`, or `[EXE-PARTIAL]`
  (legacy back-compat for VAULT999 historical receipts) and captures everything up to
  a blank-line terminator or EOF. This handles multi-line receipts cleanly.
- `_OBS_TAG_RE` matches all observation-class tags (`[OBS]`, `[INT]`, `[SPEC]`,
  `[UND]`) — not `[🦾ACT]` (which Rule 1 already handled) and not `[DER]` (which is
  derivable, observable, and may have legitimate terminal presence for chains).
- The pass-through fallback (Rule 3) prevents accidental black-hole silence when
  output is unsorted prose with no recognized tags. The gate is not a total
  censorship layer; it is a tag-classifier.

## Wiring pattern (where to deploy the gate)

The gate must be wired at the **gateway/bridge layer** before terminal output, not
in the LLM system prompt. The LLM is the wrong layer for hard enforcement — it
drifts; the regex does not.

Reference wiring in `/root/HERMES/mcp_servers/hermes_real_bridge.py`:

```python
sys.path.insert(0, str(Path(__file__).parent))
from substrate_output_gate import intercept as _gate

# In the reply path:
gated_reply = _gate(reply)
if not gated_reply:
    return {
        "status": "dropped_by_substrate_gate",
        "note": "Reply was pure observation; substrate gate silenced it.",
        ...
    }
return {
    "status": "completed",
    "reply": gated_reply,
    ...
}
```

## Constitutional cascade (how it propagates)

1. **Fragment:** `/root/AAA/instructions/exe-receipt-discipline.md` (canonical doctrine)
2. **Render:** `cd /root && ./scripts/render-agents.sh` → `AGENTS.md` + `CLAUDE.md`
3. **Hardcode:** `/root/HERMES/SOUL.md` line 168+ embeds the [🦾ACT] mandate
4. **Enforce:** `substrate_output_gate.py` physically at the bridge layer

The cascade makes the doctrine **load-bearing at four levels**: doctrine
(written), prompt (rendered), persona (SOUL), gateway (gate). Removing any one
level still leaves three enforcement surfaces.

## Self-test recipe (verify the gate works)

```bash
cd /root/HERMES/mcp_servers && python3 substrate_output_gate.py
# Expected output: "All 4 substrate gate tests PASS (incl. legacy [EXE] back-compat)"
```

The four test cases:
- `[OBS] Files scanned.` → `''` (dropped)
- `[OBS] Files scanned.\n[🦾ACT] TUGASAN SELESAI\n- Action: Patched` → only the
  `[🦾ACT]` block passes
- `[🦾ACT] TUGASAN SELESAI\n- Action: Build clean` → passes through unchanged
- `[EXE] TUGASAN SELESAI\n- Action: Legacy compat` → passes through (back-compat)

## Integration with forge-musyawawah-deliberation

The Substrate Output Gate complements `forge-musyawawah-deliberation` Phase 4
(Converge) and Phase 6 (Seal). When a musyawawah sibling emits raw observation
prose, the gate drops it. Only structured positions, synthesis, and F13 surface
lists (which carry [🦾ACT] blocks or unsorted content) reach the parent.

This means a musyawawah run today is **automatically clean** at the output layer
without changing musyawawah's internal procedures — the gate handles enforcement
at the boundary.

## Future: cascade to OpenClaw and other federation agents

The pattern is not Hermes-specific. The same gate (with the same regex) can be
deployed at:

- OpenClaw output bridge (`:18089` A2A listener reply path)
- OpenCode CLI exit stdout
- QwenCode coding agent terminal output
- arifFlow nerve system observation logs (with reduced severity — see note below)

Note: arifFlow logs are observability surface, not sovereign terminal. The gate
should run in **observe-mode** there (log dropped events but still surface for
diagnostic) rather than **silence-mode** (Hermes-style hard drop).

## Failure mode recognition (when FM6 fires)

Symptoms that FM6 is being violated:

1. F13 has to re-read previous turns to verify work was done
2. Output emits phrases like "Based on my observation...", "I noticed that...",
   "Let me explain what I found..." BEFORE any [🦾ACT] block
3. Multi-paragraph analysis is emitted without an [🦾ACT] receipt in the same response
4. F13 sends correction like "jangan sembang kosong" or "buang raw cognitive load"

When any of these symptoms appear:

1. Retag: convert all [OBS] prose to internal `<thought>` blocks
2. Re-emit: output the [🦾ACT] block FIRST, prose AFTER only as decoration
3. Verify: run C0 self-test ("can F13 confirm work from [🦾ACT] alone?")
4. If still failing, escalate to F13 with the exact FM6 symptom and ask for
   sharper gate wiring (e.g. add `_OBS_TAG_RE` member for the new leak pattern)

## Rename history (2026-08-12)

- **Old:** `[EXE]` / `[EXE-PARTIAL]` — generic execution tag
- **New:** `[🦾ACT]` / `[🦾ACT-PARTIAL]` — ACT execution actuator alignment
- **Emoji layer:** 👁️=[OBS], 🔗=[DER], 🧭=[INT], 🎲=[SPEC], ❓=[UNKNOWN]
- **Back-compat:** Gate regex still matches `[EXE]` for legacy VAULT999 receipts
- **Canon:** `/root/AAA/canon/epistemic-emoji-map.json` (schema_locked)

## Companion canonical fragment

- `/root/AAA/instructions/exe-receipt-discipline.md` (full doctrinal anchor)
- `/root/HERMES/mcp_servers/substrate_output_gate.py` (reference impl, 4 self-tests)
- `/root/HERMES/mcp_servers/hermes_real_bridge.py` (integration wiring)
- `/root/HERMES/SOUL.md` (line 168+: persona-level hardcode)

*DITEMPA BUKAN DIBERI — execution is forged, not narrated.*
