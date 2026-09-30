# Prompt-Text Authority Audit — measuring transformers that rewrite the model's input

> **The class the original taxonomy missed.** A control does not have to be a script
> returning a verdict. A **prompt-text transformer** — a plugin / middleware / hook that
> injects bytes into the system prompt before the model sees the user message — is
> authority that lives in **injected context**, not in `return` values. Classify and
> measure it the same way.

## Why a new class

The `THEATRE / FAIL-OPEN / REAL` taxonomy in the parent skill targets **script-level
> veto** — `return` values, `exit` codes, `block` decisions. A prompt-text transformer
> succeeds by **rewriting the model's input frame** while leaving the user's literal
> words intact. The transformer "fires" every turn by construction; it has no
> pass/fail signal because its work *is the prompt*.

A model that answers "lane / scope / operator boundary" instead of the user's actual
question has been **trained on the lane card** before the question reached it. That
training is the authority — and it was injected by code that never returned `block`,
never logged a refusal, never showed up in any receipts ledger.

## What to measure

For every plugin / middleware / hook that runs **before the model is called**:

1. **Bytes injected.** `len(prompt_block)` per injection. Mean across N turns, worst case,
   range per lane. A 17 KB lane card and a 200 B lane card are not the same control even
   if both run on every turn.
2. **Block composition.** Name every block (CONTEXT GOVERNOR, CARE GOVERNOR, WELL
   `live_G`, PEOPLE REGISTER, RECENT THREAD HISTORY, CAPABILITY MAP, IDENTITY header,
   VOICE register, DOCTRINES, …) with source path and bytes.
3. **Routing decisions made.** Does it REROUTE (different lane), BLOCK (veto), MODIFY
   (rewrite intent), or UNCHANGED (passthrough)? Note the line range.
4. **Capability restrictions.** Does the pre-tool hook restrict tool calls? List the
   tool names. Note whether the gate is FAIL-OPEN (no session binding → allow) vs
   FAIL-CLOSED (no session binding → block).
5. **Cost in tokens.** Bytes × ≈4 chars/token. A 17 KB card costs roughly 4,250 tokens
   per turn. The model's effective context for the user's question is the budget minus
   that card.

## The classification — applies to every block

| Class | Test | Meaning |
|---|---|---|
| **REAL** | improves reality mapping | sourced facts the user would re-teach otherwise (PEOPLE REGISTER with citations, RECENT THREAD HISTORY from the lane's own log, recent facts the human stated) |
| **ADVISORY** | improves behaviour but not reality | lane identity, voice register, IDENTITY header, CAPABILITY MAP, well-formed conduct bullets |
| **THEATRE** | claims authority, achieves framing only | philosophy/protocol text that self-negates ("defer to runtime classifier" while also classifying), mode-selection doctrine with no runtime classifier, hardcoded scripts paths that drift, repeating RESTATEMENTS of what the runtime already enforces |
| **DEAD-CODE** | never executed for this lane | filter predicates that can never be true (e.g. lane_id never equals social-graph subject), branches gated by conditions no caller satisfies |
| **REDUNDANT** | duplicates a real check | the same boundary enforced both in the prompt text AND in a runtime gate — keep one, demote the other to a one-line pointer |

**Default to ADVISORY or THEATRE for any block you cannot prove improves reality
mapping.** "Improves behaviour" is not the same as "improves reality mapping" — a
philosophy paragraph about how to behave is theatre of governance, not a fact the
model needs.

## The kill-test for prompt-text blocks

Apply the parent skill's "what dies if I remove this?" test, adapted:

> *If I delete this block from the lane card, does any agent or downstream component
> notice?*

- **If YES** — the block is REAL. It encodes a fact or constraint that surfaces
  elsewhere (in a receipt, a verifier, a memory file, a cron). Keep.
- **If NO, but the agent *would* answer differently** — ADVISORY. The block changes
  behaviour but does not change what is verifiable. Compress to one line.
- **If NO and behaviour is unchanged** — THEATRE or DEAD-CODE. Remove.

The "would answer differently" branch is the one that catches mode-shape enforcers
that exist both as prompt text and as runtime code: deleting the prompt text loses
nothing because the runtime code still fires. The prompt text is then redundant and
should be removed (the runtime code is the REAL control).

## The announcement-vs-execution gap

The most expensive failure mode in this class is the **arifos-hermes-gate-hook**
pattern: a self-described "first runtime enforcement path" that emits fail-closed
envelopes asserting constraint coverage, but on inspection only one of its named
checks actually withholds. The pattern:

1. Read the header / docstring / config annotation. Note what the control **claims** it
   blocks.
2. Read the **availability handler** — what the code returns when its dependency is
   missing, when its config is unset, when the session binding is absent.
3. Compare to a sibling control in the same file. Where one fails closed and another
   fails open, that inconsistency is citable evidence on its own.
4. Classify the gap as **FAIL-OPEN to declared posture**. The control is theatre
   wearing a fail-closed log line.
5. Report the blast radius and hand the trade back. Do not fix in the audit — repair
   is a separate authorized act.

## Liveness tests (adapted for transformers)

The parent skill's four tests (`py_compile`, `grep return`, `grep caller`, `stat
mtime`) do not reach a transformer's effect. Use these instead:

```bash
# 1. DOES THE PLUGIN LOAD?
ls -la <plugin_dir>/plugin.yaml <plugin_dir>/__init__.py
grep -n 'enabled\|plugins\.' <root_config.yaml>

# 2. IS IT REGISTERED WITH THE GATEWAY?
grep -rn "<plugin_basename>" /usr/local/lib/hermes-agent/gateway/ <root_config.yaml>
# A plugin not in plugins.enabled or not in any hook section cannot fire.

# 3. WHAT DOES IT INJECT?
sed -n '/on_pre_llm_call/,/^def \|^class /p' <plugin>/__init__.py | wc -c
# Bytes of the function body = upper bound on bytes injected (with dedup & guards).

# 4. CAN YOU OBSERVE ITS OUTPUT?
ls -la <plugin_ledger>.jsonl /tmp/<plugin>_*.log 2>/dev/null
wc -l <plugin_ledger>.jsonl
# Empty ledger + live plugin = the output is the prompt bytes, observable only via
# log inspection of the gateway's stream.

# 5. IS THERE A CALLER THAT REQUIRES IT?
grep -rn "<plugin_basename>" /root/.hermes/ /usr/local/lib/hermes-agent/   --include='*.py' --include='*.yaml' --include='*.json'
# A plugin with zero executable references is a document, not a control.
```

A plugin that fails #2 (not in `plugins.enabled`) and #5 (no caller) is **DISABLED /
THEATRE** by the parent's own tests — the new tests just confirm *what kind* of
theatre (prompt-text rewrite that never fires vs. script that always exits 0).

## Reduction target

A lane card should not exceed ~1 KB of injected context per the principal's reality-
first doctrine. The metric:

```
reduction_target = (current_bytes - 950) / current_bytes
```

For each block, classify and then assign one of:

| Recommendation | Action |
|---|---|
| KEEP | leave in card |
| DEMOTE | compress to one line / cap count / remove filler |
| REMOVE | delete entirely (after proving no downstream consumer needs it) |

Order of operations:

1. **REMOVE THEATRE blocks** — first, biggest win, no behaviour loss.
2. **DEMOTE ADVISORY blocks** — keep the function, lose the prose.
3. **KEEP REAL blocks** — only after step 1 and 2 are exhaustive on bytes.

Verification after the cut:

1. Re-measure bytes injected per turn.
2. Run a synthetic synthetic message through the live system and capture the
   actual `system` prompt the model saw.
3. Confirm every REAL block is still present, every THEATRE block is gone.

## What to write in the report

For every transformer you audit:

```
TRANSFORMER:  <plugin_name>
HOOK:         <on_pre_llm_call | on_pre_tool_call | on_post_llm_call>
BYTES:        mean=<n> worst=<n> median=<n> range=<min>-<max>
BLOCKS:       <list with bytes + class + recommendation>
REAL:         <list>
ADVISORY:     <list>
THEATRE:      <list>
DEAD-CODE:    <list>
REDUNDANT:    <list>
REDUCTION:    <before> B -> <after> B (<pct>%)
GATE:         REAL / FAIL-OPEN / FAIL-CLOSED / DISABLED
ANNOUNCEMENT-EXECUTION GAP:  <yes / no + which claim doesn't hold>
```

## Pitfalls

- **Bytes-only is not the full picture.** A 13 KB THEATRE block costs more than its
  bytes — it consumes the model's effective context, dilutes attention to the real
  prompt, and shifts the model's interpretation before reasoning starts. Report
  bytes AND token estimate AND the block's class.
- **The same code in two places.** A mode-shape enforcer that exists both as prompt
  text and as a runtime function is one control, not two. The prompt text is
  redundant; the runtime function is real. Pick the cheaper to maintain, drop the
  other.
- **Self-negating instructions.** A philosophy paragraph that ends with "defer to the
  runtime classifier; do not manually classify from this file" is theatre of
  governance. The file classifies by telling the model not to classify — and the
  model obeys, which means the paragraph's stated mode-shape logic never fires. Mark
  REMOVE.
- **Dead social-graph filters.** A filter predicated on `subject == lane_id` that
  matches no current lane IDs is dead code. Verify by enumerating lane IDs and
  checking each against the predicate; if 0 lanes match, the branch is DEAD-CODE and
  can be removed without measurement.
- **The fail-open session-binding gap.** A pre-tool gate that reads the lane from
  `session:<id>` written by the pre-llm hook and returns `None` (allow) when the key
  is absent is FAIL-OPEN by construction. The control gates only when its caller
  has populated the state — but its caller is the same plugin chain. A bug, a
  restart, or a route change that drops the binding silently disables the gate.
  Always check the failure path.
- **The MOST EXPENSIVE single block.** A single THEATRE block at 13 KB can outweigh
  the sum of every other KEEP candidate. Always sort blocks by bytes descending
  and attack the top of the list first.
- **Do not measure while mutating.** Audit bytes in a frozen measurement pass; apply
  the cuts in a separate authorized pass; re-measure after. Mixing the two
  destroys the receipts that justify the cut.

## When this file is the right reference

Load when the principal or the audit identifies any of:

- A plugin or middleware that runs between the user message and the LLM call.
- A system prompt that has grown beyond ~1 KB of injected context per turn.
- A model that answers in lane/governor vocabulary ("scope", "shared room",
  "operator boundary", "context governor") when the user did not ask in those terms.
- A control whose prompt-side enforcement duplicates a runtime check, or vice versa.
- A "fail-closed" annotation whose failure mode has not been traced to its return
  value.
