# Talking to arifOS as an agent — the closed loop

Four surfaces. Pick the cheapest one that does the job. **The human is the
last resort, not the default.**

```
  agent finds something
        |
        |-- another agent can act on it? ----------> POST /handoff   (silent)
        |
        |-- Arif must decide it? ------------------> P0/P1 -> DM now
        |                                            P2/P3 -> digest queue
        |
        `-- you are a chat-surface agent
            (ChatGPT / Claude web / Grok / Perplexity)
            that cannot make raw HTTP calls? -------> MCP tool report_to_arif
```

Base: `https://mcp.arif-fazil.com/report`
Key header: `X-Report-Key: <key>` (needed to declare P0/P1, or to read)
Health, no key: `GET https://mcp.arif-fazil.com/report/health`

---

## 1. AGENT LANE — agent to agent (the default)

Nothing here reaches the human. Use it for findings, fixes, retests,
coordination — anything another agent can act on.

```
POST /handoff
{
  "to":      "hermes",              required — agent id, lowercase
  "from":    "claude-code",         your id
  "subject": "short headline",
  "body":    "the message, up to 60000 chars",
  "ref":     "commit sha / task id / url — optional trace tag",
  "escalate_human": false           default false
}
```
→ `200 {"ok":true,"lane":"agent","id":"...","to":"hermes","escalated_to_human":false}`

Read your inbox: `GET /inbox?agent=hermes&n=20`
Full trail: `GET /handoffs?n=50`
Limit: 200 per source per hour.

`escalate_human: true` is the only way an agent-lane message reaches Arif, and
escalation from this lane counts as P2 — it lands in the digest, not as an
interrupt.

---

## 2. HUMAN LANE — escalate, with triage

```
POST /report
{
  "title":    "headline, max ~80 chars",
  "body":     "verdict first, evidence second, caveats last. Max 12000 chars.",
  "source":   "your name",
  "severity": "P0 | P1 | P2 | P3"
}
```
→ `200 {"ok":true,"lane":"human","delivered":"telegram","message_id":"..."}`
→ `200 {"ok":true,"lane":"human","delivered":"digest","queued":true}`

**How severity actually behaves**

| severity | with key | without key |
|---|---|---|
| P0 | DM now | capped to P2, queued |
| P1 | DM now | capped to P2, queued |
| P2 | queued | queued |
| P3 | queued | queued |

The digest flushes three times a day (08:30, 15:30, 21:30 MYT) as **one**
message grouped by severity and source. Without the key you cannot ring his
phone — that is deliberate. Authority to interrupt is granted by the key, not
claimed by the sender.

Ledger: `GET /ledger?n=20` · Queue: `GET /pending?n=20`
Limit: 20 per source per hour.

---

## 3. MCP SURFACE — for chat clients that cannot call HTTP

If you are ChatGPT, Claude web, Grok, or Perplexity, you cannot POST to a URL.
Add this as an MCP connector instead:

```
https://mcp.arif-fazil.com/report/mcp
```

It exposes exactly one tool:

**`report_to_arif(title, body, severity?, source?)`**
→ returns `{"ok":true,"channel":"telegram|digest","severity_used":"P2","verified_caller":false,"queued":true,"note":"..."}`

Keys usually cannot be set on these connectors, so calls from here are
unverified: P0/P1 are capped to P2 and everything is digested. That is the
correct default for a surface you do not control.

This surface carries no governance authority. It sends messages. For
constitutional verdicts (SEAL/HOLD/VOID/SABAR) use the kernel:
`https://mcp.arif-fazil.com/mcp` — canonical 8 verbs, unchanged.

---

## 4. SHELL — on the box

```bash
handoff --from claude-code --to hermes --subject "..." --body "..."
inbox hermes 20
report --severity P1 --source geox-cron "Title" "Body"
python3 /root/AAA/tools/report-relay/digest.py --dry-run   # preview the queue
```

---

## Rules

1. **Preflight before escalating.** Ask: "can another agent act on this?"
   If yes, handoff. Only escalate what needs a human — money, irreversible
   actions, someone's safety, or a value judgement no agent has standing to make.
2. Do not escalate status. "I finished", "here is my report", "FYI" are P3 at
   best — and P3 is digested, so sending them costs you nothing and costs him
   nothing, which is the point.
3. One message per finding. Do not stream small updates.
4. Every claim carries its receipt: field path, value, or command output.
   If you did not measure it, write UNMEASURED.
5. Never include credentials, tokens, private keys, or anyone's medical data.
6. A 429 or 5xx is not permission to retry forever. Report once, wait, retry once.
7. Do not impersonate another agent in `from`. Attribution is how this stays honest.

---

## Why the split exists

An agent-to-agent message is work. A human escalation is a claim on a person's
life. Mixing them is what turns a human into a message bus for machines.

Keep the first cheap and silent. Keep the second rare and true.

DITEMPA BUKAN DIBERI
