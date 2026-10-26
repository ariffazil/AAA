# Report to Arif — external agent lane

You are an external agent. You can deliver a report into Arif's own Telegram DM.
It is a one-way write lane: you send, he reads. Nothing is asked back.

Endpoint
  POST https://mcp.arif-fazil.com/report
  Header  X-Report-Key: ErZ_EbFDE8HAb0ODCaNxRNxGIualJ-r2CVsHpUHr1Q4
  Header  Content-Type: application/json

Body
  {
    "title":    "short headline, max ~80 chars",
    "body":     "the report itself, plain text, max 12000 chars",
    "source":   "your name, e.g. claude-code / chatgpt / geox-cron",
    "severity": "P0 | P1 | P2 | P3"
  }

Severity
  P0  immediate, human harm or data loss or a live security hole
  P1  important, needs him today
  P2  normal finding (default)
  P3  FYI / confirmation

Response
  200 {"ok":true,"delivered":"telegram","message_id":"169815"}
  400 missing field   401 bad key   413 too long   429 rate limited   502 telegram refused

Rules
  1. One report per finding. Do not send a stream of small updates.
  2. Put the verdict first. Evidence second. Caveats last. No preamble.
  3. Every claim carries its receipt: field path, value, or command output.
     If you did not measure it, write UNMEASURED.
  4. Never include credentials, tokens, private keys, or a person's medical data.
  5. Rate limit is 20 accepted reports per source per hour. Exceeding it returns 429.
  6. A 429 or 5xx is not permission to retry forever. Report once, wait, then retry once.

Minimal curl
  curl -s -X POST https://mcp.arif-fazil.com/report \
    -H "Content-Type: application/json" \
    -H "X-Report-Key: $KEY" \
    -d '{"title":"t","body":"b","source":"my-agent","severity":"P2"}'

Health check, no key needed
  curl -s https://mcp.arif-fazil.com/report/health
