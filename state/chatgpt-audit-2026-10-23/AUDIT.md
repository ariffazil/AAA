# AUDIT: ChatGPT report on HERMES local-reality capability

Date: 2026-10-23
Observer: HERMES KVM8 (forge, 100.64.0.2)
Input: ChatGPT analysis pasted by F13, measured ~12:07 MYT
Method: claim-by-claim grounding against live probes on this host. Nothing accepted on tone.

## 1. Claim: "Registry HERMES answered, reports 15 tools related to meaning, claims, perspective, evidence"

CONFIRMED, exactly. hermes_registry_status returned:
  11 canonical + 2 infrastructure + 1 auxiliary + 1 gated = 15 tools
  47 resources, 10 prompts, 13 capability families
  version 2026.09.25.1

Its caveat is also right: those 15 tools are meaning-integrity tools. Not one of them
finds a restaurant. A clean registry says nothing about local capability.

## 2. Claim: "A-FORGE search returned three lab test equipment results, 0/3 relevant"

REPRODUCED IN SHAPE, and now it fails harder. Two runs today:

  aforge forge_search("One South Seri Kembangan gym restaurants")
    -> status ERROR: "exa: EXA_API_KEY not set; serpapi: SERPAPI_API_KEY not set"
  aforge forge_search("gym Seri Kembangan walk-in price")
    -> same ERROR

So the earlier "3 irrelevant results" and today's hard error are the same defect at
different stages of its own learning gate.

## 3. Claim: "Cause not yet identified. Do not immediately blame SearxNG."

RIGHT to withhold blame, and the cause is now identified by measurement, not inference.

### Root cause (measured)

Hermes spawns stdio MCP children with a FILTERED environment.
  tools/mcp_tool_config.py::_build_safe_env()
  - keeps only safe baseline keys, XDG_*, secret-source vars, plus the server's own `env:` block
  - tools/mcp_tool_transport.py:363 -> StdioServerParameters(env=safe_env or None)

The `aforge` entry in /root/.hermes/config.yaml had:
  command: node
  args: [ .../cli.js, serve, --transport, stdio ]
  timeout: 180
No `env:` block. So the child received none of EXA_API_KEY, SERPAPI_API_KEY, BRAVE_SEARCH_API_KEY.

Proof before the fix, from /proc:
  gateway  PID 1986168  EXA len=36  SERP len=64  BRAVE len=31   <- parent HAS them
  its child PID 1988830  EXA ABSENT  SERP ABSENT  BRAVE ABSENT   <- child does NOT

Then gateway_search's ladder (src/interfaces/mcp/gatewayTools.ts:395-435) scores
["exa","serpapi","searxng","deepseek","brave"] and tries in that order. exa and serpapi
fail instantly on missing keys. Each failure calls circuitRecordFailure + lfdRecord(loser),
and the curriculum gate `.filter(s => s.lfdScore > 0 || s.score >= 0.9)` then drops the
remaining lanes over time. Result: either thin/irrelevant Brave or SearXNG output (what
ChatGPT saw) or a total ERROR (what I see). A self-reinforcing gate, not a dead backend.

### Fix applied (2026-10-23 04:29Z)

Added an env block to the aforge entry using config-level ${VAR} interpolation
(config.py::_expand_env_vars, verified present). No secrets written into the file:

    env:
      EXA_API_KEY: ${EXA_API_KEY}
      SERPAPI_API_KEY: ${SERPAPI_API_KEY}
      BRAVE_SEARCH_API_KEY: ${BRAVE_SEARCH_API_KEY}

Backup: /root/.hermes/config.yaml.bak-20261023-preaforge-env
Gateway restarted. New MainPID 373283, its aforge child 373692 now carries all three keys.

### End-to-end proof, not a config assertion

Spawned the same server with the keys and called the same tool over stdio:

    status: OK
    provider: exa
    results: 5
    - Bunga Kemboja Fitness - The Atmosphere Seri Kembangan
    - Daily Fitness
    - 5 Gym Spaces That Are Open 24/7 (says.com)
    - Oxygym Fitness The Mines, Seri Kembangan
    - exa.ai library places

Five relevant Selangor gym results, from the lane that was "not set" twenty minutes earlier.
Same tool. Same server. Same query class. Only the environment differed.

## 4. Claim: "Two carry_forward files -- I have not read either"

It correctly refused to assert what it had not read. I did read both. The real shape:

  /root/.local/share/arifos/carry_forward.json  inode 1594219  85,534B  v3 typed entries[]
  /root/.hermes/carry_forward.json              inode 5274483  28,764B  v2 flat dict, no entries key
  CARRY_PATH = line 47 of /root/scripts/carry_forward.py -> the .local/share/arifos file

They are NOT one dataset forked into two copies. They are two different schemas wearing the
same filename: one is session state (completed/open_loops/session_state SEALED_ASLEEP), the
other is the typed event ledger. Defect class = NAME COLLISION BETWEEN ROLES, not fork.
Prior art: /root/AAA/instructions/CARRY-FORWARD-PATH-RECONCILIATION.md (FI-003, 2026-09-12).

Second defect, found while probing, in neither report:
The canonical file's newest entry (03:54:54Z today) has id=null, agent=null, kind=lesson,
and the bookkeeping was not updated (total_entry_count=56 while the list holds 57;
last_writer still 333-AGI / 2026-10-22T14:45:00Z). Two writers reach one file: the script
mints ids, direct JSON mutation does not. Entries from the second path are unaddressable.

## 5. Claim: "Google Places API + Routes API is the first purchase to evaluate"

SEQUENCING WRONG. The purchase decision was framed as "which API to buy". The real facts
measured today:

  SerpAPI account: plan Free, 250 searches/month, this_month_usage 250, left 0
  -> exhausted. HTTP 429 "Your account has run out of searches."

So the lane was never absent. It was FREE and it ran dry, partly from today's own work
(91 places + 20 photo sets + review probes). The question is quota, not capability.

Live pricing, read from the vendors today:

  SerpAPI      Free $0 / 250        Starter $25 / 1,000        Developer $75 / 5,000
  Google Maps  Starter $100 / 50,000 calls    Essentials $275 / 100,000    Pro $1,200 / 250,000
               ($300 trial credit for new customers)

For one person's local lookups (order 300-2,000/month across food, gym, events, news):
SerpAPI Starter at $25/month is the cheapest entry that covers it. Google Maps Starter at
$100/month buys 50x the calls at 4x the price, and drags in billing setup, key custody,
field masks and the Places attribution/storage terms ChatGPT itself flagged.

Recommendation: SerpAPI Starter first. Revisit Google Maps only if a second consumer
appears (a public app, a shared team, an event pipeline), because then the 50,000-call
floor starts to earn its price.

## 6. Claim: "Places API returns a maximum of five reviews, so it is not a full picture"

CONFIRMED from Google's own REST reference:
  reviews[] -- "A maximum of 5 reviews can be returned."
  photos[]  -- "A maximum of 10 photos can be returned."

CORRECTION to the implied limitation: that cap belongs to the Places API, not to the data.
Second lane verified today gave 20 food photos per venue through SerpAPI's google_maps_photos
engine (20 of 20 for all seven venues). SerpAPI also exposes a reviews engine. So the
"5 reviews" ceiling is a reason not to buy Places directly, not a reason to doubt the lane
already in use.

## 7. Claim: "Realtime GTFS offers vehicle positions; do not assume delays, cancellations
and alerts are covered"

CORRECT and STRONGER than stated. Measured:
  gtfs-realtime/vehicle-position?category=rapid-bus-kl   200  10,332B
  gtfs-realtime/vehicle-position                         404
  gtfs-realtime/trip-updates                             404
  gtfs-realtime/trip-updates?category=rapid-bus-kl        404
  gtfs-realtime/alerts                                   404
  gtfs-realtime/alerts?category=rapid-bus-kl              404

One of three endpoints exists. Delay, cancellation and service-alert data is not merely
uncertain, it is absent from this feed. Any transit answer built on it must say "live bus
position only, no delay data".

## 8. Claim: fixed source list (weather, transit, events, news, food, halal)

Probed today, read-only, from KVM8:

  klfoodie.com            200   and /feed/ 200 (RSS available -- cheap ingest)
  penangfoodie.com        200   but /feed/ 403 (bot wall)
  cloudjoi.com            200   /api/ 404 (no public API at that path)
  ticket2u.com.my         200   /feed/ 404
  mypenang.gov.my         200
  airselangor.com         200
  publicinfobanjir.water.gov.my  200
  apims.doe.gov.my        404   (root path dead; the portal lives on another path)
  halal.gov.my            200   directory, HTML not API
  mkn.gov.my              200

9 of 10 reachable. All are pages to read, not APIs to subscribe to, exactly as ChatGPT said.
Two are worth wiring as feeds: klfoodie (RSS works) and the four national news feeds I
verified earlier (The Star, Bernama, FMT, SoyaCincau).

## 9. Claim: "A canonical Arif reality profile should be shared by every agent"

AGREED, and it does not exist. What exists today, measured:
  USER.md 10,435 chars (435 over its 10,000 budget)
  MEMORY.md 15,958 chars
  /root/.hermes/lanes/people.yaml (people SOT)
  my-local-reality v1.0.0 (forged today) declares three area anchors but is a SKILL, not a
  shared record, and it is one agent's copy.

Its warning is the sharpest line in the report and I adopt it verbatim in spirit:
  "A home address does not mean he is at home."
Every local answer must name the assumed anchor until he supplies a live position.

## Verdict on the report

  Registry count          CONFIRMED
  A-FORGE 0/3 relevant     CONFIRMED in effect, CAUSE MISATTRIBUTED TO "UNKNOWN"
  carry_forward            UNVERIFIED BY ITS OWN ADMISSION; shape I supply differs from the fork story
  Places-first purchase    WRONG SEQUENCING (free lane existed; quota is the constraint)
  Places 5-review cap      CONFIRMED, and it argues against buying Places, not against the current lane
  GTFS caution             CORRECT and stronger (1 of 3 endpoints exists)
  Source list              9 of 10 live; correct that they are pages not APIs
  Canonical profile        AGREED, absent, and its "address is not location" warning is right

Three things it got that this host had not stated as clearly: the 5-review/10-photo cap,
the "address is not presence" rule, and the discipline of labelling customer experience vs
unverified claim vs promotion vs official statement vs the sovereign's own experience.
That last one is a real contribution and belongs in the skill.

One thing it could not have known: the failure was one missing YAML block.

## Actions taken

1. Root cause measured with /proc, mechanism read in source, fix applied to config.yaml.
2. Gateway restarted; child env verified carrying all three keys.
3. End-to-end proof: 5 relevant gym results from the repaired lane.
4. Backup retained: config.yaml.bak-20261023-preaforge-env

## Still open (needs the sovereign, not an agent)

1. SerpAPI quota: Free plan exhausted. Starter $25/mo vs Google Maps Starter $100/mo.
2. Canonical reality profile: needs his word on what is canonical, not an agent's guess.
3. Reddit lane: 403 from this host. Proxy/OAuth is a decision, not a config tweak.

## Falsifier

If a new session's forge_search returns ERROR with "API_KEY not set" again, the env block was
lost on a config rewrite, and the check is `lsattr`/diff against the backup, not a retry.
If aforce's search returns results but they are lab equipment for a Selangor gym query, the
curriculum gate is still excluding the strong lanes and the fix is incomplete.
