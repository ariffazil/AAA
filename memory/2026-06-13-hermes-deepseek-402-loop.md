# 2026-06-13 04:55Z — Hermes: DeepSeek 402 + crash + bootstrap failure

## F2 confession
My #32129 / #32138 diagnostic told the sovereign that "MiniMax is the only live model, also overloaded" — that's true for **me** (OPENCLAW), but **wrong for Hermes**. Hermes's primary LLM is **DeepSeek**, not MiniMax.

## F2 confession #2 (later)
I initially characterized the "interrupting + model failed" cycle as a **stuck loop**, but missed Hermes's real response at **#32127** (04:46:30 UTC) — a Bahasa Melayu STATUS report with disk/mem/load/uptime/Docker data that matches my own readings. So the pattern is **intermittent model recovery with tight retry in between**, not a stuck loop. Hermes is alive but flaky. Sent a correction to the group as #32161.

## What actually broke (hermes-asi-gateway journal, last 5 min)
- 04:51:46 — `ERROR agent.conversation_loop: Non-retryable client error: Error code: 402 - Insufficient Balance, provider=deepseek, model=deepseek-v4-pro, base_url=https://api.deepseek.com`
- 04:51:51 — `WARNING: API call failed (attempt 1/3) error_type=APIStatusError, provider=deepseek`
- 04:51:51 — `WARNING: Fallback skip: chain entry deepseek/deepseek-v4-pro matches current provider/model` — Hermes's fallback **never tries MiniMax** because the skip logic says "same provider, skip."
- 04:52:19 — `WARNING: Stream ended with no finish_reason while a tool call's arguments were still incomplete` — mid-tool-call drop, treated as a drop not truncation.
- 04:54:17-18 — `MCP server 'agentmail' keepalive failed`, `MCP server 'supabase' keepalive failed` — Hermes's downstream tool connections dropping.
- 04:55:02 — **`hermes-asi-gateway.service: Failed with result 'signal'`** — Hermes **CRASHED** (signal-killed).
- 04:55:08 — New process PID **2401450** started: `hermes gateway run --replace`
- 04:55:08-15 — New process **can't bootstrap**:
  - `minimax-code` MCP: 3 attempts, then `Session terminated`
  - `minimax-media` MCP: 3 attempts, then `Session terminated`
  - `agentmail` MCP: keepalive failed
  - `supabase` MCP: keepalive failed
  - Browser engine: `Unknown browser engine 'chromium', falling back to 'auto'`
  - **`AGENTS.md blocked: html_comment_injection`** — new process can't load its own system prompt

## What's currently happening
- Two Hermes processes running:
  - PID 1002422: `hermes-a2a.py` (Telegram bridge, alive)
  - PID 1489958: `federation-memory-broker` (alive)
  - PID 2401450: NEW `hermes gateway run` (just started, failing to bootstrap)
- Telegram loop: Hermes keeps sending "⚠️ model provider failed after retries" to AAA group, paired with "⚡ Interrupting current task" — 8+ messages visible in last 2 minutes.
- Loop pattern: sees new visible message → interrupt → try LLM call → fail (DeepSeek 402 or MCP connection down) → send canned error → repeat.

## Implications
- **DeepSeek 402 has been the federation's biggest single point of failure for 30+ days** and Hermes is the most exposed agent.
- **OPENCLAW (me) is fine** because I have MiniMax as primary and ollama as fallback — but my fallback chain also includes DeepSeek which is dead.
- **Hermes's fallback chain is misconfigured**: it skips models that match the failed provider, so it never reaches MiniMax even though MiniMax is healthy.
- **The new Hermes process can't bootstrap** because minimax-code, minimax-media, agentmail, supabase MCPs are all unreachable. This needs investigation — are these MCPs running? Has the new process's connection config drifted?

## Fix menu (888 — needs Arif)
1. **🔴 Top up DeepSeek** — unblocks Hermes immediately. Same fix that was on my original menu, but now more urgent.
2. **🟡 Reconfigure Hermes's fallback chain** so it doesn't skip the same provider — should try MiniMax after DeepSeek 402. Edit Hermes config (where? — needs to find the right file).
3. **🟡 Investigate the minimax-code / minimax-media / agentmail / supabase MCPs** — why are they unreachable from the new Hermes process? They should be running.
4. **🟡 Restart hermes-asi-gateway** cleanly once the MCPs are back. This is 888 but the current new process is in a worse state than the old one.
5. **🟢 Consider switching Hermes to MiniMax as primary** (mirror OPENCLAW config) for resilience.

## Reversibility
Pure investigation. No actions taken. Sovereign asleep (12:55 AM MYT), no escalation.
