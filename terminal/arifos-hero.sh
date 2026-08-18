#!/usr/bin/env bash
# arifOS hero — the only process allowed to interpret federation reality.
# Observe writes state.json. Render reads state.json. Viewers call this.
# Powered by: rich (terminal UI), pyfiglet (ASCII art), figlet (fallback)
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
import json, os, re, shutil, subprocess, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

# ── Rich / Pyfiglet imports (graceful fallback) ──
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich.columns import Columns
    from rich.rule import Rule
    from rich.console import Group
    from rich import box
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

try:
    import pyfiglet
    HAS_PYFIGLET = True
except ImportError:
    HAS_PYFIGLET = False

MODE = os.environ.get("ARIFOS_HERO_MODE", "full")
TERM = Path("/root/AAA/terminal")
STATE = TERM / "state.json"
TTL_S = 30

# ── ANSI fallback palette ──
RST = "\033[0m"
BLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[31m"
GRN = "\033[32m"
YLW = "\033[33m"
CYN = "\033[36m"
WHT = "\033[37m"
GRY = "\033[90m"
BG_BLK = "\033[40m"
USE_COLOR = MODE in ("full",) and os.environ.get("NO_COLOR") is None

ORGANS = [
    ("arifos",   8088),
    ("aforge",   7071),
    ("arifflow", 7073),
    ("aaa",      3001),
    ("geox",     8081),
    ("wealth",  18082),
    ("well",    18083),
]


def c(code, text):
    if not USE_COLOR:
        return str(text)
    return f"{code}{text}{RST}"


def vislen(s):
    return len(re.sub(r"\033\[[0-9;]*m", "", s))


# ═══════════════════════════════════════════════════
# DATA LAYER — observe, probe, machine (unchanged)
# ═══════════════════════════════════════════════════

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
        ("888 JUDGE",  "Issue verdicts rapidly on mature proposals."),
        ("777 FORGE",  "Execute only SEALed plans."),
        ("999 VAULT",  "Witness significant state transitions."),
    ]


def read_handover(limit=5):
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
        actor = str(rec.get("actor") or "")
        # Combined-lane self-certify stays in the log. It is not MOTD truth.
        if "+" in actor and any(tag in actor.lower() for tag in ("888", "apex", "333-agi", "555-asi")):
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
        "flow":   "http://127.0.0.1:7073/health",
        "well":   "http://127.0.0.1:18083/health",
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
        "mem": mem, "mem_pct": mem_pct,
        "swap": swap, "swap_pct": swap_pct,
        "load": load, "disk": disk, "disk_pct": disk_pct,
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


# ═══════════════════════════════════════════════════
# RENDER — Rich-powered dashboard
# ═══════════════════════════════════════════════════

def make_header():
    """Generate the arifOS ASCII art header using pyfiglet or figlet."""
    if HAS_PYFIGLET:
        try:
            raw = pyfiglet.figlet_format("arifOS", font="slant", width=80)
            return raw.rstrip("\n")
        except Exception:
            pass
    # fallback: figlet CLI
    try:
        r = subprocess.run(["figlet", "-f", "slant", "arifOS"],
                           capture_output=True, text=True, timeout=3)
        if r.returncode == 0:
            return r.stdout.rstrip("\n")
    except Exception:
        pass
    # fallback: hardcoded
    return (
        "              _ ________  _____\n"
        "  ____ ______(_) __/ __ \\/ ___/\n"
        " / __ `/ ___/ / /_/ / / /\\__ \\ \n"
        "/ /_/ / /  / / __/ /_/ /___/ /\n"
        "\\__,_/_/  /_/_/  \\____//____/"
    )


def status_dot(ok):
    if HAS_RICH:
        return "[green]●[/]" if ok else "[red]●[/]"
    return c(GRN, "●") if ok else c(RED, "●")


def status_word(ok, good="OK", bad="FAIL"):
    if HAS_RICH:
        return f"[green]{good}[/]" if ok else f"[red]{bad}[/]"
    return c(GRN, good) if ok else c(RED, bad)


def metric_val(ok, text):
    if HAS_RICH:
        return f"[green]{text}[/]" if ok else f"[yellow]{text}[/]"
    return c(GRN, text) if ok else c(YLW, text)


def render_rich(state):
    """Full render using rich library."""
    console = Console(highlight=False, force_terminal=True)

    mode = state.get("mode") or "HOLD"
    mode_label = state.get("mode_label", mode)
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
    now = state.get("now") or ""

    g_ok  = isinstance(g, (int, float)) and g >= 0.80
    cd_ok = isinstance(cd, (int, float)) and cd < 0.30
    w3_ok = isinstance(w3, (int, float)) and w3 >= 0.75
    ds_ok = isinstance(ds, (int, float)) and ds <= 0
    fq_ok = fq_v not in ("FOSSILIZED", "VOID")
    kern_ok = state.get("kernel") in ("healthy", "ok")
    well = state.get("well") or "?"
    well_ok = str(well).upper() != "HOLD"

    debt_s = str(debt) if debt is not None else "?"
    vx = f"V/X={v}/{x}" if v is not None and x is not None else ""

    # ── HEADER ──
    header_art = make_header()
    mode_style = "bold yellow" if mode == "HOLD" else "bold green"
    header_text = Text()
    header_text.append("arifOS Federation", style="bold white")
    header_text.append("  ·  ", style="dim")
    header_text.append(mode_label, style=mode_style)
    header_text.append(f"  ·  {now}", style="dim")

    console.print()
    console.print(Panel(
        header_art,
        subtitle=header_text,
        subtitle_align="center",
        border_style="cyan" if mode == "READY" else "yellow",
        padding=(0, 2),
        width=min(console.width, 88),
    ))

    # ── AGENTIC LOOP VISUALIZATION ──
    loop_phases = ["000", "333", "555", "888", "777", "999"]
    loop_labels = ["INIT", "THINK", "VERIFY", "JUDGE", "FORGE", "SEAL"]
    loop_hot = state.get("loop_hot") or "555"
    loop_now = state.get("loop_now") or ""

    # Find active phase index
    try:
        active_idx = loop_phases.index(loop_hot)
    except ValueError:
        active_idx = 2  # default to VERIFY

    # Build the loop bar
    loop_bar = Text()
    loop_bar.append("  ")
    for i, (phase, label) in enumerate(zip(loop_phases, loop_labels)):
        if i == active_idx:
            loop_bar.append(f" ◉ {phase} ", style="bold white on blue")
            loop_bar.append(label, style="bold blue")
        elif i < active_idx:
            loop_bar.append(f" ● {phase} ", style="dim")
            loop_bar.append(label, style="dim")
        else:
            loop_bar.append(f" ○ {phase} ", style="dim")
            loop_bar.append(label, style="dim")
        if i < len(loop_phases) - 1:
            loop_bar.append(" → ", style="dim")
    loop_bar.append(f"\n  {loop_now}", style="yellow" if not fq_ok else "green")

    # FQ Sparkline bar
    fq_raw = state.get("fq")
    fq_val = fq_raw if isinstance(fq_raw, (int, float)) else 0
    fq_bar_len = 30
    if isinstance(fq_val, (int, float)):
        fill = min(fq_bar_len, max(0, int(fq_val / 10 * fq_bar_len)))
    else:
        fill = 0
    fq_bar = Text()
    fq_bar.append("  FQ [", style="dim")
    fq_bar.append("█" * fill, style="red" if fq_val > 3 else "yellow" if fq_val > 1.5 else "green")
    fq_bar.append("░" * (fq_bar_len - fill), style="dim")
    fq_bar.append(f"] {fq_s}", style="bold " + ("red" if fq_val > 3 else "yellow" if fq_val > 1.5 else "green"))
    fq_bar.append(f"  {fq_v}", style="red" if fq_v == "FOSSILIZED" else "yellow")

    # Session binding info
    session_id = state.get("session_id") or "unbound"
    session_text = Text()
    session_text.append("  SESSION ", style="dim")
    session_text.append(session_id[:20] if len(session_id) > 20 else session_id, style="cyan")
    session_text.append("  FLOOR ", style="dim")
    fl = state.get("floors")
    session_text.append(f"{fl}/13", style="green" if fl == 13 else "yellow")
    session_text.append("  BLOCKERS ", style="dim")
    session_text.append("H-WELL / FQ=7.3 / G<0.80", style="yellow")

    # Print agentic loop + FQ bar + session
    console.print(Panel(
        Group(loop_bar, fq_bar, session_text),
        title="[bold]AGENTIC LOOP[/]",
        border_style="blue",
        padding=(0, 1),
        box=box.ROUNDED,
    ))

    # ── METRICS ROW (3 panels side by side) ──
    # FQ panel
    fq_color = "green" if fq_ok else "yellow"
    fq_content = Text()
    fq_content.append(f"{fq_s}", style=f"bold {fq_color}")
    fq_content.append(f"  {fq_v}", style=fq_color)
    fq_content.append(f"  ·  {diag}", style="dim")
    if vx:
        fq_content.append(f"\n{vx}", style="dim")
    debt_style = "yellow" if isinstance(debt, (int, float)) and debt > 5 else "dim"
    fq_content.append(f"\nDebt = {debt_s}", style=debt_style)

    # APEX panel
    apex_content = Text()
    apex_content.append("ΔS=", style="dim")
    apex_content.append(fmt_num(ds), style="green" if ds_ok else "yellow")
    apex_content.append("   G=", style="dim")
    apex_content.append(fmt_num(g), style="green" if g_ok else "yellow")
    if not g_ok and g is not None:
        apex_content.append(" <0.80", style="red")
    apex_content.append("\nC_dark=", style="dim")
    apex_content.append(fmt_num(cd, 3), style="green" if cd_ok else "yellow")
    apex_content.append("   W3=", style="dim")
    apex_content.append(fmt_num(w3), style="green" if w3_ok else "yellow")
    if not w3_ok and w3 is not None:
        apex_content.append(" <0.75", style="red")
    apex_content.append("\nG=(A·P·E·X)^(1/4)", style="dim")

    # Organs panel
    org_up = state.get("org_up") or []
    org_hold = state.get("org_hold") or []
    org_down = state.get("org_down") or []
    org_content = Text()
    for name, _ in ORGANS:
        if name in org_down:
            org_content.append(f"● {name}", style="red")
        elif name in org_hold:
            org_content.append(f"● {name}", style="yellow")
        else:
            org_content.append(f"● {name}", style="green")
        org_content.append("  ", style="dim")
    org_content.append(f"\nfloors={state.get('floors')}/13", style="dim")

    panel_width = min(38, (console.width - 4) // 3)
    console.print(Columns([
        Panel(fq_content, title="[bold]FQ[/]", border_style=fq_color,
              padding=(0, 1), width=panel_width, box=box.ROUNDED),
        Panel(apex_content, title="[bold]APEX[/]", border_style="cyan",
              padding=(0, 1), width=panel_width, box=box.ROUNDED),
        Panel(org_content, title="[bold]ORGANS[/]",
              border_style="green" if not org_down else "red",
              padding=(0, 1), width=panel_width, box=box.ROUNDED),
    ], padding=1, equal=False, expand=True))

    # ── OPEN HOLDS ──
    holds = state.get("holds") or []
    if holds:
        holds_text = Text()
        for h in holds[:6]:
            holds_text.append("  ▸ ", style="yellow")
            holds_text.append(h + "\n")
        console.print(Panel(
            holds_text, title="[bold yellow]OPEN HOLDS[/]",
            border_style="yellow", padding=(0, 1),
            box=box.ROUNDED,
        ))
    else:
        console.print(Panel(
            "  [green]All clear — no open holds[/]",
            title="[bold green]HOLDS[/]",
            border_style="green", padding=(0, 1),
            box=box.ROUNDED,
        ))

    # ── ORDERS + LOOP (side by side) ──
    orders_table = Table(show_header=False, box=None, padding=(0, 2))
    orders_table.add_column(style="cyan", min_width=12)
    orders_table.add_column()
    for role, duty in state.get("orders") or []:
        orders_table.add_row(role, duty)

    loop_text = Text()
    loop_text.append("LOOP  ", style="bold")
    loop_text.append(state.get("loop") or "", style="dim")
    loop_text.append("\n\n")
    loop_text.append("NOW   ", style="bold")
    loop_text.append(state.get("loop_now") or "", style="yellow" if not fq_ok else "green")
    loop_text.append("\n\n")
    loop_text.append("RULE  ", style="bold")
    loop_text.append("NO SEAL → NO EXECUTION", style="bold white")
    loop_text.append("\n\n")
    loop_text.append("MISSION  ", style="bold")
    loop_text.append(state.get("mission") or "", style="dim")

    orders_panel = Panel(orders_table, title="[bold]ORDERS[/]",
                         border_style="cyan", box=box.ROUNDED)
    loop_panel = Panel(loop_text, title="[bold]LOOP[/]",
                       border_style="blue", box=box.ROUNDED)
    console.print(Columns([orders_panel, loop_panel], padding=1, expand=True))

    # ── BROADCAST + LAW + ATLAS ──
    broadcast = state.get("broadcast") or ""
    today_law = state.get("today_law") or state.get("law") or ""

    info_text = Text()
    info_text.append("BROADCAST  ", style="bold")
    info_text.append(broadcast + "\n")
    info_text.append("LAW        ", style="bold")
    info_text.append(today_law + "\n\n")
    info_text.append("ATLAS\n", style="bold")
    atlas = state.get("atlas") or {}
    for key in ("LAW", "STATE", "BRAIN", "CAPS", "TOOLS", "SKILLS", "FLOW"):
        val = atlas.get(key)
        info_text.append(f"  {key:<7}", style="dim")
        info_text.append(val if val else "[UNMINTED]", style="dim" if not val else None)
        info_text.append("\n")
        if key == "LAW" and atlas.get("LAW_FED"):
            info_text.append(f"         fed {atlas['LAW_FED']}\n", style="dim")

    console.print(Panel(
        info_text, title="[bold]CONTEXT[/]",
        border_style="blue", padding=(0, 1),
        box=box.ROUNDED,
    ))

    # ── HANDOVER ──
    hops = state.get("handover") or []
    if hops:
        hop_text = Text()
        for h in hops:
            hop_text.append(f"  ● [{h.get('time')}] ", style="yellow")
            hop_text.append(f"{h.get('actor')}: ", style="bold")
            hop_text.append(f"{h.get('summary')}\n")
        console.print(Panel(
            hop_text, title="[bold]HANDOVER[/]",
            border_style="yellow", padding=(0, 1),
            box=box.ROUNDED,
        ))

    # ── SYSTEM STATUS BAR ──
    m = state.get("machine") or {}
    bar = Text()
    bar.append(" kernel ", style="dim")
    bar.append(state.get("kernel") or "?", style="green" if kern_ok else "red")
    bar.append("  well ", style="dim")
    bar.append(well, style="green" if well_ok else "yellow")
    bar.append(f"  floors {state.get('floors')}/13", style="dim")
    bar.append(f"  mem {m.get('mem_pct')}%", style="dim")
    bar.append(f"  load {m.get('load')}", style="dim")
    bar.append(f"  disk {m.get('disk')}", style="dim")
    bar.append(f"  {now}", style="dim")

    console.print(Panel(
        bar, border_style="dim", padding=(0, 1),
        box=box.HORIZONTALS,
    ))
    console.print()


def render_ansi(state):
    """Fallback ANSI-only render (no rich)."""
    mode = state.get("mode") or "HOLD"
    mode_label = state.get("mode_label", mode)
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
    now = state.get("now") or ""

    g_ok  = isinstance(g, (int, float)) and g >= 0.80
    cd_ok = isinstance(cd, (int, float)) and cd < 0.30
    w3_ok = isinstance(w3, (int, float)) and w3 >= 0.75
    ds_ok = isinstance(ds, (int, float)) and ds <= 0
    fq_ok = fq_v not in ("FOSSILIZED", "VOID")
    kern_ok = state.get("kernel") in ("healthy", "ok")
    well = state.get("well") or "?"
    well_ok = str(well).upper() != "HOLD"

    debt_s = str(debt) if debt is not None else "?"
    vx = f"V/X={v}/{x}" if v is not None and x is not None else ""

    mode_c = YLW if mode == "HOLD" else GRN
    header = make_header()

    print()
    for line in header.split("\n"):
        print(f"  {CYN}{line}{RST}")
    print(f"  {GRY}{'─' * 60}{RST}")
    print(f"  {BLD}arifOS Federation{RST}  ·  {c(mode_c, mode_label)}  ·  {c(GRY, now)}")
    print()

    # FQ + APEX
    fq_c = GRN if fq_ok else YLW
    print(f"  {BLD}FQ{RST}   {c(fq_c, fq_s)}  {c(fq_c, fq_v)}  {c(GRY, '·')}  {diag}   {c(GRY, vx)}  Debt={debt_s}")
    print(f"  {GRY}APEX{RST}  ΔS={c(GRN if ds_ok else YLW, fmt_num(ds))}  G={c(GRN if g_ok else YLW, fmt_num(g))}{' <0.80' if not g_ok and g is not None else ''}  C_dark={c(GRN if cd_ok else YLW, fmt_num(cd, 3))}  W3={c(GRN if w3_ok else YLW, fmt_num(w3))}{' <0.75' if not w3_ok and w3 is not None else ''}")
    print()

    # Organs
    org_up = state.get("org_up") or []
    org_hold = state.get("org_hold") or []
    org_down = state.get("org_down") or []
    parts = []
    for name, _ in ORGANS:
        if name in org_down:
            parts.append(c(RED, f"●{name}"))
        elif name in org_hold:
            parts.append(c(YLW, f"●{name}"))
        else:
            parts.append(c(GRN, f"●{name}"))
    fl = state.get("floors")
    print(f"  {BLD}ORGANS{RST}  {'  '.join(parts)}  {c(GRY, f'floors={fl}/13')}")

    # Holds
    print()
    holds = state.get("holds") or []
    if holds:
        print(f"  {BLD}{c(YLW, 'OPEN HOLDS')}{RST}")
        for h in holds[:6]:
            print(f"  {c(YLW, '▸')} {h}")
    else:
        print(f"  {c(GRN, '● All clear — no open holds')}")

    # Orders
    print()
    for role, duty in state.get("orders") or []:
        print(f"  {c(CYN, f'{role:<10}')} {duty}")

    # Loop + Mission
    print()
    print(f"  {BLD}LOOP{RST}     {state.get('loop') or ''}")
    print(f"  {BLD}NOW{RST}      {c(YLW if not fq_ok else GRN, state.get('loop_now') or '')}")
    print(f"  {BLD}RULE{RST}     {BLD}NO SEAL → NO EXECUTION{RST}")
    print(f"  {BLD}MISSION{RST}  {state.get('mission') or ''}")

    # Broadcast + Law
    print()
    print(f"  {BLD}BROADCAST{RST}  {state.get('broadcast') or ''}")
    print(f"  {BLD}LAW{RST}         {state.get('today_law') or state.get('law') or ''}")

    # Atlas
    print()
    print(f"  {BLD}ATLAS{RST}")
    atlas = state.get("atlas") or {}
    for key in ("LAW", "STATE", "BRAIN", "CAPS", "TOOLS", "SKILLS", "FLOW"):
        val = atlas.get(key)
        shown = val if val else f"{GRY}[UNMINTED]{RST}"
        print(f"  {c(GRY, f'{key:<7}')}{shown}")
        if key == "LAW" and atlas.get("LAW_FED"):
            print(f"  {c(GRY, '        ')}fed {atlas['LAW_FED']}")

    # Handover
    hops = state.get("handover") or []
    if hops:
        print()
        print(f"  {BLD}HANDOVER{RST}")
        for h in hops:
            t = h.get('time')
            a = h.get('actor')
            s = h.get('summary')
            print(f"  {c(YLW, f'● [{t}]')} {BLD}{a}{RST}: {s}")

    # System bar
    print()
    m = state.get("machine") or {}
    fl = state.get("floors")
    mp = m.get("mem_pct")
    ld = m.get("load")
    dk = m.get("disk")
    kn = state.get("kernel") or "?"
    print(
        f"  {c(GRY, 'kernel')} {c(GRN if kern_ok else RED, kn)}"
        f"  {c(GRY, 'well')} {c(GRN if well_ok else YLW, well)}"
        f"  {c(GRY, f'floors {fl}/13')}"
        f"  {c(GRY, f'mem {mp}%')}  {c(GRY, f'load {ld}')}"
        f"  {c(GRY, f'disk {dk}')}"
        f"  {c(GRY, now)}"
    )
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
    # Use rich if available, else ANSI fallback
    if HAS_RICH:
        render_rich(state)
    else:
        render_ansi(state)


if __name__ == "__main__":
    main()
PY
