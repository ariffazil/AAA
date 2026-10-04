# Apex Judge via delegate_task — Telegram / no-shell-session fallback

## When the CLI and execute_code paths are unavailable

`apex-judge isolate` and the FED `curl` route require shell access via `terminal` tool. In sessions where that is denied (Telegram gateway sessions, mobile client, restricted profiles), the **only apex route available is `delegate_task`**.

Verified 2026-08-11 on the `syaitan-ingat-dirinya-malaikat` civic-journalism article:
- Session: Hermes (hermes-asi, openai-api) over Telegram
- Shell `terminal` was available but the CLI was overkill for a quick first-pass review
- `delegate_task` to a leaf subagent with the apex prompt produced a clean PARTIAL verdict with all 13 floors and ΔS assessment in 79s

## Recipe

```python
delegate_task(
  goal="""You are 888-APEX, the constitutional judge of the arifOS federation.
  You are running as an INDEPENDENT model from the doer. Your role is independent
  judgment of <subject>.

  <full article text, evidence, instructions, deliverables>
  """,
  role="leaf"
)
```

The leaf subagent inherits the parent's model. **Independence comes from process
separation (different context, different log, different receipt file), not from
a different provider.** This is `ACTOR_SEPARATED` on the independence ladder,
not `KERNEL_ARBITER`. The verdict is still binding for governance review,
just not as strong as a model-provider-different route.

## When to choose which path

| Path | When |
|---|---|
| Option 0 (output gate hook) | Any agent-emitted output — automatic, no decision needed |
| Option 1 (CLI isolate) | Config mutations (jobs.json, registry), self-federation, F13-required |
| Option 2 (FED route) | Long candidates > 1000 chars, or when model-provider diversity matters |
| **Option 3 (delegate_task)** | Telegram sessions, no shell, quick first-pass review, civic journalism |

For civic journalism review (MakcikGPT persona), Option 3 is sufficient —
the article is reversible (F1 PASS by construction), the bar is constitutional
compliance not model diversity.

## How to verify the verdict is real (not self-judgment)

After the subagent returns, verify:

```bash
# 1. delegation log shows the dispatch
grep "<delegation_id>" ~/.local/share/arif*/delegations.log | head -3

# 2. receipt file exists with the session hash
ls -la /usr/local/lib/hermes-agent/profiles/<profile>/cache/delegation/
```

The subagent's text output is the verdict. Quote the **per-floor status block
+ VERDICT line + ΔS** verbatim. Do not soften, edit, or annotate the verdict
body. Your courier role starts after the verdict returns.

## Common pitfalls

- **Free-text "888-APEX JUDGMENT" without a delegation_id** — that is self-judgment.
  If you wrote the verdict yourself without `delegate_task` actually firing,
  it is VOID per F9 ANTIHANTU. The dispatch log proves the call happened.

- **Subagent with same model = same Gödel loop class** — this gives
  `ACTOR_SEPARATED`, not `KERNEL_ARBITER`. For F13-critical review, escalate
  to Option 1 or Option 2 with provider diversity.

- **Subagent writes "888-APEX JUDGMENT" without applying F1-F13 floors** —
  prompt must explicitly require per-floor PASS/FAIL/CAUTION/HOLD with
  one-line reasoning. Without this, the subagent may return editorial
  commentary instead of constitutional review.

- **Long article text in `goal` parameter** — `delegate_task` JSON-encodes
  the goal string. Articles > 5000 chars may hit tool-message size limits.
  For long articles, write body to `/tmp/<slug>.txt` and pass file path in
  the goal; subagent reads with `read_file`.
