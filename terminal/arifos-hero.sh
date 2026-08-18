#!/usr/bin/env bash
# arifOS hero — the only process allowed to interpret federation reality.
# Observe writes state.json. Render reads state.json. Viewers call this.
# DITEMPA BUKAN DIBERI
set +e
case "${1:-}" in
    --observe|observe) MODE=observe ;;
    --json|json)       MODE=json ;;
    --compact|compact) MODE=compact ;;
    --mode|ps1|--ps1)  MODE=mode ;;
    --raw|full|"")     MODE=full ;;
    *)                 MODE=full ;;
esac
export ARIFOS_HERO_MODE="$MODE"
exec python3 - <<'PY'
import json, os, re, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

MODE = os.environ.get("ARIFOS_HERO_MODE", "full")
TERM = Path("/root/AAA/terminal")
STATE = TERM / "state.json"
TTL_S = 30

R = "\033[0m"
B = "\033[1m"
G = "\033[32m"
Y = "\033[33m"
RD = "\033[31m"
C = "\033[36m"
GR = "\033[90m"
USE_COLOR = MODE in ("full",) and os.environ.get("NO_COLOR") is None

ORGANS = [
    ("arifos", 8088),
    ("aforge", 7071),
    ("arifflow", 7073),
    ("aaa", 3001),
    ("geox", 8081),
    ("wealth", 18082),
    ("well", 18083),
]


def c(code, text):
    if not USE_COLOR:
        return str(text)
    return f"{code}{text}{R}"


def vislen(s):
    return len(re.sub(r"\033\[[0-9;]*m", "", s))


def box_line(inner, width=50):
    pad = max(0, width - vislen(inner))
    return c(GR, "║") + inner + (" " * pad) + c(GR, "║")


def read_txt(name, default=""):
    for cand in (name,):
        p = TERM / cand
        if not p.exists():
            continue
        try:
            lines = [
                ln.rstrip()
                for ln in p.read_text(encoding="utf-8").splitlines()
                if ln.strip() and not ln.lstrip().startswith("#")
            ]
            if lines:
                return " ".join(lines)
        except Exception:
            pass
    return default


def read_orders():
    p = TERM / "orders.txt"
    out = []
    try:
        for ln in p.read_text(encoding="utf-8").splitlines():
            ln = ln.rstrip()
            if not ln or ln.lstrip().startswith("#") or "\t" not in ln:
                continue
            role, duty = ln.split("\t", 1)
            out.append((role.strip(), duty.strip()))
    except Exception:
        pass
    return out or [
        ("333 THINK", "Unblock decisions stalled by redundant verification."),
        ("555 VERIFY", "Challenge only assumptions that change outcomes."),
        ("888 JUDGE", "Issue verdicts rapidly on mature proposals."),
        ("777 FORGE", "Execute only SEALed plans."),
        ("999 VAULT", "Witness significant state transitions."),
    ]



def read_handover(limit=5):
    """Last ACTIVE lines from append-only JSONL. Hero reads. Clerks append."""
    hp = Path("/root/AAA/telemetry/handover.log")
    out = []
    try:
        lines = [ln.strip() for ln in hp.read_text(encoding="utf-8").splitlines() if ln.strip()]
    except Exception:
        return out
    for ln in reversed(lines):
        try:
            rec = json.loads(ln)
        except Exception:
            continue
        if str(rec.get("status") or "ACTIVE").upper() not in ("ACTIVE", "SEALED"):
            continue
        ts = rec.get("ts") or ""
        time_s = ts[11:16] if len(ts) >= 16 else ts
        out.append({
            "ts": ts,
            "time": time_s,
            "actor": rec.get("actor") or "?",
            "category": rec.get("category") or "",
            "summary": (rec.get("summary") or "")[:100],
        })
        if len(out) >= limit:
            break
    out.reverse()
    return out


def read_declared_holds():
    holds = []
    for name in ("holds.txt", "holds.declared.txt"):
        p = TERM / name
        if not p.exists():
            continue
        try:
            for ln in p.read_text(encoding="utf-8").splitlines():
                s = ln.strip()
                if s and not s.startswith("#"):
                    holds.append(s)
        except Exception:
            pass
        break
    return holds


def get_json(url, timeout=1.2):
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8", "replace"))
    except Exception:
        return None


def apex_val(apex, key):
    node = (apex or {}).get(key) or {}
    if isinstance(node, dict):
        return node.get("value")
    if isinstance(node, (int, float)):
        return node
    return None


def fmt_num(v, digits=2):
    if isinstance(v, (int, float)):
        return f"{v:.{digits}f}"
    return "?"


def fmt_age_hours(h):
    try:
        h = float(h)
    except (TypeError, ValueError):
        return "?"
    if h < 1:
        return f"{int(h * 60)}m"
    if h < 48:
        return f"{h:.0f}h"
    return f"{h / 24:.0f}d"


def probe():
    urls = {
        "kernel": "http://127.0.0.1:8088/health",
        "flow": "http://127.0.0.1:7073/health",
        "well": "http://127.0.0.1:18083/health",
    }
    for name, port in ORGANS:
        urls[f"org:{name}"] = f"http://127.0.0.1:{port}/health"
    got = {}
    with ThreadPoolExecutor(max_workers=8) as pool:
        futs = {pool.submit(get_json, url): key for key, url in urls.items()}
        for fut in as_completed(futs):
            got[futs[fut]] = fut.result()
    return got


def machine():
    mem = swap = load = disk = "?"
    mem_pct = swap_pct = disk_pct = 0
    try:
        kv = {}
        for ln in Path("/proc/meminfo").read_text().splitlines():
            if ":" in ln:
                k, v = ln.split(":", 1)
                kv[k] = int(v.strip().split()[0])
        total = kv.get("MemTotal") or 1
        avail = kv.get("MemAvailable") or 0
        used = total - avail
        mem_pct = int(used * 100 / total)
        mem = f"{used // 1024 // 1024}Gi/{total // 1024 // 1024}Gi"
        st = kv.get("SwapTotal") or 0
        sf = kv.get("SwapFree") or 0
        if st > 0:
            su = st - sf
            swap_pct = int(su * 100 / st)
            swap = f"{su // 1024 // 1024}Gi/{st // 1024 // 1024}Gi"
        else:
            swap = "0"
    except Exception:
        pass
    try:
        load = Path("/proc/loadavg").read_text().split()[0]
    except Exception:
        pass
    try:
        st = os.statvfs("/")
        used_b = (st.f_blocks - st.f_bfree) * st.f_frsize
        tot_b = st.f_blocks * st.f_frsize
        disk_pct = int(used_b * 100 / tot_b) if tot_b else 0
        disk = f"{disk_pct}%"
    except Exception:
        pass
    return {
        "mem": mem,
        "mem_pct": mem_pct,
        "swap": swap,
        "swap_pct": swap_pct,
        "load": load,
        "disk": disk,
        "disk_pct": disk_pct,
    }


def observe():
    data = probe()
    k = data.get("kernel") or {}
    f = data.get("flow") or {}
    w = data.get("well") or {}
    apex = k.get("apex_scalars") or {}
    thermo = k.get("thermodynamic") or {}
    fq = f.get("fq") or {}
    vec = ((f.get("vector") or {}).get("diagnosis") or {})

    g = apex_val(apex, "G")
    cd = apex_val(apex, "C_dark")
    w3 = apex_val(apex, "W3")
    ds = thermo.get("entropy_delta")
    floors = k.get("floors_active")
    kernel_st = (k.get("status") or "down").lower()
    vault = k.get("vault999_health") or "?"

    fq_q = fq.get("quotient")
    fq_v = (fq.get("verdict") or "?").upper()
    fq_diag = fq.get("diagnosis") or vec.get("primary_pathology") or "?"
    verify = fq.get("verify_count")
    execute = fq.get("execute_count")
    try:
        debt = int(verify) - int(execute)
    except (TypeError, ValueError):
        debt = None

    well_signal = str(w.get("well_signal") or "")
    well_st = str(w.get("status") or "").lower()
    honesty = (w.get("honesty") or {}) if isinstance(w.get("honesty"), dict) else {}
    well_mock = bool(honesty.get("is_mock_or_test")) or str(honesty.get("code") or "").upper() == "MOCK"
    well_age = w.get("state_age_hours")
    well_hold = (
        well_signal == "WELL_HOLD"
        or well_st not in ("healthy", "ok", "")
        or well_mock
        or (data.get("well") is None)
    )

    org_up, org_hold, org_down = [], [], []
    for name, _port in ORGANS:
        body = data.get(f"org:{name}")
        if body is None:
            org_down.append(name)
            continue
        st = str(body.get("status") or "").lower()
        if name == "well" and well_hold:
            org_hold.append(name)
        elif st in ("healthy", "ok", "ok-v3-vector"):
            org_up.append(name)
        else:
            org_hold.append(name)

    holds = []
    if fq_v == "FOSSILIZED" or (isinstance(fq_q, (int, float)) and fq_q >= 3.0):
        vx = f"{verify}v/{execute}x" if verify is not None and execute is not None else "ratio unknown"
        holds.append(f"FQ fossilization — {fq_diag} ({vx})")
    if well_hold:
        why = "MOCK" if well_mock else well_signal or well_st or "no pulse"
        age = fmt_age_hours(well_age)
        holds.append(f"WELL sensor debt — {why}, stale {age} (not operator state)")
    if isinstance(g, (int, float)) and g < 0.80:
        holds.append(f"G below floor — {g:.2f} < 0.80")
    if isinstance(w3, (int, float)) and w3 < 0.75:
        holds.append(f"W3 below tri-witness — {w3:.2f} < 0.75")
    if org_down:
        holds.append("organ down — " + ",".join(org_down))
    holds.extend(read_declared_holds())

    if org_down or fq_v == "FOSSILIZED" or well_hold or (isinstance(g, (int, float)) and g < 0.80):
        mode = "HOLD"
        mode_label = "GOVERNANCE-FIRST"
    elif kernel_st in ("healthy", "ok") and not holds:
        mode = "READY"
        mode_label = "READY"
    else:
        mode = "HOLD"
        mode_label = "GOVERNANCE-FIRST"

    if fq_v == "FOSSILIZED" or (isinstance(verify, int) and isinstance(execute, int) and verify > execute):
        loop_now = "555 VERIFY dominates · 777 FORGE starved"
        loop_hot = "555"
    else:
        loop_now = "flow toward 777 FORGE → 999 SEAL"
        loop_hot = "777"

    law = read_txt("todays-law.txt") or read_txt("law.txt", "Opportunity Debt = Verify − Execute")
    atlas = {
        "LAW": "/root/arifOS/GENESIS/000_KERNEL_CANON.md",
        "LAW_FED": "/root/AAA/prompts/INIT.md",
        "BOOT": "/root/AAA/terminal/BOOT.md",
        "STATE": "/root/AAA/terminal/state.json",
        "BRAIN": "/root/.config/federation-models.json",
        "CAPS": "/root/AAA/registries/models/CAPABILITIES.json",
        "TOOLS": None,
        "SKILLS": None,
        "HANDOVER": "/root/AAA/telemetry/handover.log",
        "FLOW": "http://127.0.0.1:7073",
        "FLOW_RECEIPTS": "/var/lib/arifflow/receipts.jsonl",
    }
    state = {
        "schema": "arifos.terminal.state/v1",
        "ts": datetime.now(timezone.utc).isoformat(),
        "authority": "ARIF",
        "mode": mode,
        "mode_label": mode_label,
        "kernel": kernel_st,
        "floors": floors,
        "vault": vault,
        "thermo_verdict": thermo.get("verdict") or "",
        "thermo_is_not_seal": True,
        "fq": fq_q,
        "fq_s": f"{fq_q:.1f}" if isinstance(fq_q, (int, float)) else "?",
        "fq_state": fq_v,
        "fq_verdict": fq_v,
        "diagnosis": fq_diag,
        "verify": verify,
        "execute": execute,
        "debt": debt,
        "ds": ds,
        "g": g,
        "c_dark": cd,
        "w3": w3,
        "well": "HOLD" if well_hold else well_st or "?",
        "well_mock": well_mock,
        "well_note": "sensor debt, not operator state" if well_hold else "",
        "org_up": org_up,
        "org_hold": org_hold,
        "org_down": org_down,
        "holds": holds,
        "loop": "000 → 333 → 555 → 888 → 777 → 999",
        "loop_now": loop_now,
        "loop_hot": loop_hot,
        "broadcast": read_txt("broadcast.txt", "Seek decisions where extra verification changes nothing."),
        "mission": read_txt("mission.txt", "Restore equilibrium"),
        "today_law": law,
        "law": law,
        "orders": read_orders(),
        "machine": machine(),
        "now": datetime.now(ZoneInfo("Asia/Kuala_Lumpur")).strftime("%H:%M MYT"),
        "atlas": atlas,
        "handover": read_handover(5),
    }
    tmp = STATE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, default=str, indent=2) + "\n", encoding="utf-8")
    tmp.replace(STATE)
    return state


def load_state():
    try:
        return json.loads(STATE.read_text(encoding="utf-8"))
    except Exception:
        return None


def state_age_s():
    try:
        return max(0, int(datetime.now(timezone.utc).timestamp() - STATE.stat().st_mtime))
    except Exception:
        return None


def ensure_fresh():
    age = state_age_s()
    if age is None or age > TTL_S:
        return observe()
    return load_state() or observe()


def flag(ok, text):
    return c(G, text) if ok else c(Y, text)


def render(state):
    mode = state.get("mode") or "HOLD"
    mode_c = Y if mode == "HOLD" else G
    fq_s = state.get("fq_s") or "?"
    fq_v = state.get("fq_verdict") or state.get("fq_state") or "?"
    diag = state.get("diagnosis") or "?"
    v = state.get("verify")
    x = state.get("execute")
    debt = state.get("debt")
    ds = state.get("ds")
    g = state.get("g")
    cd = state.get("c_dark")
    w3 = state.get("w3")
    g_ok = isinstance(g, (int, float)) and g >= 0.80
    cd_ok = isinstance(cd, (int, float)) and cd < 0.30
    w3_ok = isinstance(w3, (int, float)) and w3 >= 0.75
    ds_ok = isinstance(ds, (int, float)) and ds <= 0
    fq_ok = fq_v not in ("FOSSILIZED", "VOID")

    # arifOS ASCII Art — larger letters, framed, enhanced visual hierarchy
    w_c   = "\033[37m"       # white
    dw    = "\033[2;37m"     # dim white
    lbl_c = c(B, mode_c if mode == "HOLD" else G,)

    def lbl(ok, text, bad_c=Y):
        return c(G, text) if ok else c(bad_c, text)

    g_ok   = isinstance(g, (int, float)) and g >= 0.80
    ds_ok  = isinstance(ds, (int, float)) and ds <= 0
    fq_ok  = fq_v not in ("FOSSILIZED", "VOID")
    w3_ok  = isinstance(w3, (int, float)) and w3 >= 0.75

    # Colored half-block art: 'a' 'r' 'i' 'f' small, 'OS' big
    h1 = (f"  {C}▄▄▄▄  ▄▄▄▄  ▄  ▄▄▄▄▄    {B}{C}╔═══╗      ╔═╗ {R}")
    h2 = (f"  {C}█  █▌ █  █▌ █  █▌       {B}{C}╠═╗ ╦╔═╗  ╔═╣ {R}")
    h3 = (f"  {C}▀▀▀▀  ▀▀▀▀  ▀  ▀▀▀▀▀    {B}{C}╚═══╩╚═╝  ╚═╝ {R}")

    thin  = "  ───────────────────────    ────────────────"
    thin_c = f"  {dw}───────────────────────────────{R}"

    # Right-side metadata
    def rmeta(label, value):
        return f"  {GR}{label:<12}{R}{value}"

    print()
    print(h1 + rmeta("FEDERATION",  c(B, "arifOS") + " · " + c(mode_c, state.get("mode_label", mode))))
    print(h2 + rmeta("AUTHORITY",   c(B, "ARIF") + " (F13) · " + c(GR, "DITEMPA BUKAN DIBERI")))
    print(h3 + rmeta("VERDICTS",    "UNKNOWN · SABAR · " + c(Y, "HOLD") + " · " + c(G, "SEAL") + " · " + c(RD, "VOID")))
    print(thin_c)
    print(f"  {GR}{'':>28}{R}"  + rmeta("LOOP",        state.get("loop") or "000→333→555→888→777→999") + c(GR, "  (") + c(Y if not fq_ok else G, state.get("loop_now", "")) + c(GR, ")"))
    print(f"  {GR}{'':>28}{R}"  + rmeta("RULE",        c(B, "NO SEAL → NO EXECUTION")))
    print()
    print()

    # ── ATLAS ──
    print(f"  {B}ATLAS{R}")
    atlas = state.get("atlas") or {}
    for key in ("LAW", "STATE", "BRAIN", "CAPS", "TOOLS", "SKILLS", "FLOW"):
        val = atlas.get(key)
        shown = val if val else f"{GR}[UNMINTED]{R}"
        print(f"  {GR}{key:<7}{R}{shown}")
        if key == "LAW" and atlas.get("LAW_FED"):
            print(f"  {GR}        {R}fed {atlas['LAW_FED']}")

    # ── HANDOVER ──
    print()
    print(f"  {B}HANDOVER{R}")
    hops = state.get("handover") or []
    if not hops:
        print(f"  {GR}none — clerks append /root/AAA/telemetry/handover.log{R}")
    else:
        for h in hops:
            print(f"  {Y}• [{h.get('time')}]{R} {h.get('actor')}: {h.get('summary')}")

    # ── METRICS (side-by-side compact) ──
    print()
    fq_color = G if fq_ok else Y
    ds_color = G if ds_ok else Y
    g_color  = G if g_ok  else Y
    w3_color = G if w3_ok else Y
    cd_color = G if cd_ok else Y

    debt_s = f"{debt}" if debt is not None else "?"
    vx = f"  FQ=V/X={v}/{x}" if v is not None and x is not None else ""

    print(f"  {B}FQ{R}  {fq_color}{fq_s}{R}  {fq_color}{fq_v}{R}  {GR}·{R}  {diag}")
    print(f"  {GR}APEX{R}  ΔS={ds_color}{fmt_num(ds)}{R}  G={g_color}{fmt_num(g)}{R}{(' <0.80' if not g_ok and g is not None else ' ≥0.80' if g_ok else '')}  C_dark={cd_color}{fmt_num(cd, 3)}{R}  W3={w3_color}{fmt_num(w3)}{R}{(' <0.75' if not w3_ok and w3 is not None else '')}")
    print(f"  {GR}     {R}  G=(A·P·E·X)^(1/4)  Debt=V−X={debt_s}{vx}")

    # ── BROADCAST / MISSION / HOLDS ──
    print()
    print(f"  {B}BROADCAST{R}")
    print(f"  {state.get('broadcast') or ''}")
    print()
    print(f"  {B}MISSION{R}  {state.get('mission') or ''}")
    print()
    print(f"  {B}OPEN HOLDS{R}")
    holds = state.get("holds") or []
    if not holds:
        print(f"  {G}none — board empty means resolved{R}")
    else:
        for h in holds[:6]:
            print(f"  {Y}•{R} {h}")

    # ── ORDERS ──
    print()
    for role, duty in state.get("orders") or []:
        print(f"  {C}{role:<10}{R} {duty}")

    # ── TODAY'S LAW ──
    print()
    print(f"  {B}TODAY'S LAW{R}")
    print(f"  {state.get('today_law') or state.get('law') or ''}")

    # ── SYSTEM STATUS BAR ──
    print()
    m = state.get("machine") or {}
    well = state.get("well")
    well_c = Y if str(well).upper() == "HOLD" else G
    kern_c = G if state.get("kernel") in ("healthy", "ok") else RD
    floors = state.get('floors')

    bar  = f"  {GR}kernel{R} {kern_c}{state.get('kernel') or '?'}{R}"
    bar += f"  {GR}well{R} {well_c}{well}{R}"
    bar += f"  {GR}floors{R} {floors}/13"
    bar += f"  {GR}mem{R} {m.get('mem_pct')}%  {GR}load{R} {m.get('load')}  {GR}disk{R} {m.get('disk')}"
    bar += f"  {GR}{state.get('now')}{R}"
    print(bar)
    print()


def render_compact(state):
    fq = state.get("fq_s") or "?"
    fv = state.get("fq_verdict") or ""
    well = state.get("well") or "?"
    mode = state.get("mode") or "HOLD"
    debt = state.get("debt")
    debt_s = f" Debt={debt}" if debt is not None else ""
    print(f"{mode} · FQ {fq} {fv} · WELL {well}{debt_s}")
    print(state.get("loop_now") or "")


def main():
    if MODE == "observe":
        state = observe()
        print(state["ts"])
        return
    if MODE == "json":
        state = ensure_fresh()
        print(json.dumps(state, default=str, indent=2))
        return
    if MODE == "mode":
        state = load_state() or ensure_fresh()
        print(state.get("mode") or "HOLD")
        return
    try:
        state = ensure_fresh()
    except Exception:
        print()
        print("ARIFOS FEDERATION · AUTHORITY ARIF")
        print("hero observe failed — run: now")
        print()
        return
    if MODE == "compact":
        render_compact(state)
        return
    render(state)


if __name__ == "__main__":
    main()
PY
