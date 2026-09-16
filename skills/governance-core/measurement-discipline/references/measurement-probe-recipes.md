# Measurement probe recipes

Read-only harnesses for the rules in SKILL.md. None mutates state; each prints a number you
can re-derive.

## 1. Phased memory-pressure harness

Three phases — idle / workload / recovery — with counter families sampled at phase boundaries
and a fixed-operation latency control running throughout.

```python
import time, subprocess, sqlite3, statistics

def snap():
    d = {}
    for path, tag in (('/proc/pressure/memory', 'mem'),
                      ('/proc/pressure/io',     'io'),
                      ('/proc/pressure/cpu',    'cpu')):
        for line in open(path):
            k, v = line.split(None, 1)          # 'some avg10=.. avg60=.. avg300=.. total=NNN'
            d[f'{tag}_{k}'] = int(v.split('total=')[1])   # NAMED keys, never positional indices
    for line in open('/proc/vmstat'):
        p = line.split()
        if p[0] in ('pswpin', 'pswpout', 'pgmajfault', 'pgpgin', 'pgpgout'):
            d[p[0]] = int(p[1])
    mi = dict(l.split(':', 1) for l in open('/proc/meminfo') if ':' in l)
    d['MemFree']  = int(mi['MemFree'].split()[0])
    d['MemAvail'] = int(mi['MemAvailable'].split()[0])
    d['SwapFree'] = int(mi['SwapFree'].split()[0])
    return d
```

The control is a real fixed query against a real datastore, timed in every phase:

```python
con = sqlite3.connect('file:/path/to/state.db?mode=ro', uri=True)

def control():
    t = time.perf_counter()
    con.execute("select count(*) from <fts_table> where <fts_table> match '<term>'").fetchone()
    return (time.perf_counter() - t) * 1000        # ms
```

Driver: 15 s idle → spawn N CPU-bound children (`subprocess.Popen`) for 20 s → 10 s recovery.
Between phases call `snap()` and print:

- PSI as a percentage of wall: `delta_ns / (phase_seconds * 1e9) * 100`
- `pswpin` / `pswpout` / `pgmajfault` as counts **and** per-second rates
- MemFree / MemAvail / SwapFree start → end
- control median and p95 per phase

**Flat control latency across all phases ⇒ the resource is not the binding constraint**, whatever
the occupancy says. Non-zero `pswpin`/`pswpout` sustained in every phase is the real evidence of
active paging.

### Guard before any allocation stress test

```bash
grep -E 'free-mem|free-swap|avoid|prefer' /etc/default/earlyoom 2>/dev/null
earlyoom --help 2>&1 | head -20
systemctl show earlyoom -p ExecStart --no-pager
```

Check whether the watcher requires *both* thresholds below minimum before acting, and print its
avoid/prefer lists. If the target process — or its interpreter (`python3`, `node`) — is on the
prefer list, do not provoke pressure. Record the refusal and its reason.

## 2. Prefix-cache harness (isolating prefix cache from request cache)

Vary the user turn on every call, keeping the system prompt byte-identical:

```python
import json, time, urllib.request

def call(url, model, system, user, headers):
    # `headers` carries the provider's standard auth values, sourced from the environment
    # and never printed or logged.
    body = json.dumps({"model": model,
                       "messages": [{"role": "system", "content": system},
                                    {"role": "user",   "content": user}],
                       "max_tokens": 16}).encode()
    req = urllib.request.Request(url, data=body, headers=headers)
    t = time.perf_counter()
    d = json.load(urllib.request.urlopen(req, timeout=180))
    u = d.get('usage', {})
    print(f"{(time.perf_counter()-t)*1000:8.1f}ms  prompt={u.get('prompt_tokens')} "
          f"cached={u.get('prompt_cache_hit_tokens')} miss={u.get('prompt_cache_miss_tokens')}")

for user in ("ping-a", "ping-b", "ping-c"):     # DIFFERENT every call
    call(URL, MODEL, SYSTEM, user, HEADERS)
```

Call 1 is cold; calls 2+ show the steady-state hit ratio. `cached ≈ prompt_tokens` means the
prefix is amortised. Report hit ratio and latency, then state separately that the cognitive axis
was **not** measured.

## 3. Cold/warm local-model benchmark

Report the **first-call latency separately from the mean** — the first call carries the model load.

```python
import time, json, urllib.request

def task(url, model, prompt):
    body = json.dumps({"model": model,
                       "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": 60}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    t = time.perf_counter()
    d = json.load(urllib.request.urlopen(req, timeout=300))
    return (time.perf_counter() - t), (d.get('choices') or [{}])[0].get('message', {}).get('content', '')
```

Task set: arithmetic, extraction, classification, JSON shaping, unit conversion, and at least one
**logical negation** item (`"If all A are B and no B are C, can any A be C?"`). Small models pass
surface extraction while failing negation, and a negation failure is invisible in the pass rate of
the easy items. Six items is enough to kill a routing hypothesis, not enough to set a policy — say
which one the result supports.

## 4. Route / embedder resolution trace

Six steps, in order, all read-only:

```bash
# 1 — does the process exist?
pgrep -af '<service-name>'; systemctl show <unit> -p MainPID --value

# 2 — what its LIVE environment holds (not the config file on disk)
PID=$(systemctl show <unit> -p MainPID --value)
tr '\0' '\n' < /proc/$PID/environ | grep -E '^(EMBED|OLLAMA|API|BASE_URL)' | sed 's/=.*/=<set>/'

# 3 — the module's own ordered fallback list; first match wins
grep -nE 'settings|fallback|config\[' <module>.py | head -20

# 4 — does the resolved endpoint answer?
curl -s -m 6 "$SERVICE_BASE/api/tags" | head -c 300

# 5 — what contract does the response carry? (send a real input)
curl -s -m 20 -X POST "$SERVICE_BASE/api/embed" \
  -d '{"model":"<embed-model>","input":"dimension check"}' | head -c 300

# 6 — what does the TARGET declare it wants?
curl -s -m 6 "$STORE_BASE/collections/<name>" | grep -oE '"size":[0-9]+'
```

Step 6 is what prevents a false mismatch: a store whose declared shape differs may be a
deliberately separate index with its own owner. Find the writer that owns it before calling the
difference drift.
