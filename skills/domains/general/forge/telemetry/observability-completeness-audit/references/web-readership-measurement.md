# Web Readership Measurement — the origin access-log lane

Answering "how many visitors does the site have?" when there is no analytics product and no
third-party beacon. Load this when the question is traffic, readership, or "do we have
analytics" for a self-hosted site behind a reverse proxy and a CDN.

This is a coverage question in the same family as a telemetry-plane audit: the first honest
answer may be **"there is no instrument"**, and establishing one is the deliverable.

---

## 0. Confirm absence before promising numbers

Check, in order: an analytics script in the source tree; a beacon tag in the live HTML; a
`log` directive in the reverse-proxy vhost; and whether the CDN credential you hold can read
zone analytics at all. A `log` directive absent or global means the proxy is not recording
requests — everything downstream is moot.

"We have no measurement" is a legitimate finding. Reach for it before inventing a metric.

---

## 1. THE critical fact — behind a tunnel, the peer IP is meaningless

When a CDN/tunnel front-ends the origin over loopback (a cloudflared or equivalent tunnel,
`reverse_proxy localhost:...`), the proxy's TCP peer is **loopback on every request**:

- `remote_ip` = `127.0.0.1`
- `client_ip` = `127.0.0.1`

**Counting either reports exactly one visitor, forever.** Trusted-proxy configuration that
lists only the CDN's *edge* ranges does not help — the loopback peer is untrusted, so the
forwarded-for header is not folded in.

The real client IP lives in the CDN's own header (`Cf-Connecting-Ip` for Cloudflare;
`X-Forwarded-For` first entry as fallback). Any analyzer must resolve in that order and
**record which source it used** so the number stays auditable.

Adding loopback to the trusted-proxy list is a global-config change; reading the header costs
nothing and is the safer fix. Prefer the header.

---

## 2. Prove the log is complete before trusting any count

An origin log silently undercounts if the CDN serves pages from cache. Two cheap checks:

```bash
# Page response: is it cached at the edge?
curl -sI -m 10 https://<host>/ | grep -iE 'cf-cache-status|age|cache-control'
```

`cf-cache-status: DYNAMIC` plus `cache-control: no-cache, no-store, must-revalidate` means
every page view reaches the origin — the count is complete.

Also confirm no cache-everything rule overrides it (CDN page-rules endpoint, or the equivalent
config for your CDN).

**State the known blind spot out loud:** static assets (JS/CSS) usually *are* edge-cached
(`cf-cache-status: HIT`, non-zero `age`) and are invisible in the origin log. That is fine —
fetching a bundle is not reading the site — but say it, rather than letting a later reader find
the gap and distrust the whole number.

Free bonus worth extracting while you are there: the CDN country header gives a geographic
distribution that is otherwise a paid feature.

---

## 3. User-Agent classification is semantic, not cosmetic

If the site serves **different bytes by User-Agent** (a bot lane vs a browser lane), then a lane
assignment is a claim about *which version of the site a request received*. Two rules follow:

- **A headless browser is a bot.** Generic bot tokens placed *after* a browser-shaped check are
  unreachable for any `Mozilla/...` UA, so headless traffic gets counted as human readers —
  the fastest way to inflate the headline number.
- **The lane must agree with the bytes actually served.** Pin a regression test on it.

Separate at minimum: HUMAN · INTERNAL_AGENT · AI_CRAWLER · SEARCH_ENGINE · SOCIAL_PREVIEW ·
MONITORING · CLI · OTHER_BOT · UNKNOWN.

Keep `INTERNAL_AGENT` as its own lane, checked **first**. Your own probes otherwise land in
`UNKNOWN`, which destroys `UNKNOWN` as a signal and can misreport a self-probe named
`<something>-gptbot-check` as a real GPTBot.

**HUMAN is an upper bound.** UA-only classification cannot catch a scraper sending a real
browser UA. Cross-check against distinct IPs and label the number a ceiling.

---

## 4. Size log rotation from a measured rate, never from convention

Derive bytes/day from the log's own timestamps rather than guessing:

```python
import re
lines = open(LOGFILE, errors='replace').readlines()
ts = [float(m.group(1)) for l in lines if (m := re.search(r'"ts":([0-9.]+)', l))]
span = ts[-1] - ts[0]
print(f"{sum(len(l) for l in lines)/span*86400/1e6:.1f} MB/day")
```

`roll_size × roll_keep` is the disk ceiling; `roll_keep_for` is the retention window. The
binding constraint is usually the **window**, not the per-file size.

A smoke-test rate is not a traffic rate — probes and agents inflate it by orders of magnitude
over real readership. Size for the smoke rate so the ceiling holds in the worst case, and expect
the real rate to be far lower.

---

## 5. File permissions reset on rotation

A proxy running as root creates its log `0600 root:root`, unreadable by non-root consumers.
`chmod` on the live file is a temporary patch — **the next rotation re-creates it 0600.** The
persistent fix is `UMask=0027` in the systemd override. State which one you applied.

---

## 6. Do not buy a dashboard you already have

If the origin log already carries request, real client IP, path, method, status, duration,
User-Agent, and country — and pages are never edge-cached — then coverage is complete. Granting
a broader CDN-analytics scope buys a UI, not new information.

Two traps before reaching for the API:
- **A product setting is not a provisioned product.** A zone setting reading `on` with
  `editable: true` and a site tag is not a working beacon. Probe the beacon endpoint and read
the footer of the 404: a CDN-branded page means the edge answered, which means it is not
provisioned.
- **An alternative credential may exist but be dead.** Verify with the provider's token-verify
  endpoint before assuming a second lane is available.

---

## 7. Report the numbers honestly

- **Never report a smoke-test window as readership.** A log open for minutes, sourced from a
  handful of IPs, is your own agents. "Instrument is live and reading correctly" is a different
  and true claim.
- **Let it accumulate before interpreting.** A short window turns your own noise into a fake
  finding; low human counts then get misread as absence of audience.
- **Report the human number, not total requests.** Total requests is the number that flatters.
