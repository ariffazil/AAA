#!/usr/bin/env python3
"""Composite reality pulse (BM). Runs all 5 adapters, prints compact brief.
Degradation: satu adapter mati → pulse terus + flag; TIDAK pernah fabricated data."""
import json, subprocess, sys, os

AD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "adapters")

def run(name, *args):
    p = subprocess.run([sys.executable, os.path.join(AD, name), *args],
                       capture_output=True, text=True, timeout=45)
    try:
        return json.loads(p.stdout), p.returncode
    except Exception:
        return {"error": (p.stdout or p.stderr)[:100]}, p.returncode or 1

parts, flags = [], []

prayer, rc = run("prayer.py")
if rc == 0:
    parts.append(f"🌙 Subuh {prayer['fajr']} · Zohor {prayer['dhuhr']} · Asar {prayer['asr']} · Maghrib {prayer['maghrib']} · Isyak {prayer['isha']} (JAKIM)")
else:
    flags.append(f"solat:{prayer.get('error', 'fail')}")

weather, rc = run("weather.py")
if rc == 0:
    fc = weather.get("forecast") or []
    if fc and isinstance(fc[0], dict):
        f0 = fc[0]
        parts.append(f"🌤 {f0.get('loc')}: {f0.get('summary')} ({f0.get('when')}), {f0.get('min_c')}-{f0.get('max_c')}°C")
    else:
        parts.append("🌤 Cuaca: tiada baris padanan")
    parts.append(f"⚠️ Amaran MET aktif: {weather.get('warning_count', 0)}")
else:
    flags.append(f"cuaca:{weather.get('error', 'fail')}")

flood, rc = run("flood.py")
if rc == 0:
    n = flood.get("alert_count", 0)
    line = f"🌊 Stesen banjir PP+Sel: {flood.get('stations_seen', 0)} dikesan, {n} alert"
    alerts = flood.get("alerts") or []
    if alerts:
        a0 = alerts[0]
        line += f" — tertinggi: {a0.get('station')} ({a0.get('indicator')})"
    parts.append(line)
else:
    flags.append(f"banjir:{flood.get('error', 'fail')}")

fx, rc = run("fx.py", "USD")
if rc == 0:
    parts.append(f"💰 USD/MYR beli {fx.get('buy')} jual {fx.get('sell')} (BNM {fx.get('date')})")
else:
    flags.append(f"fx:{fx.get('error', 'fail')}")

gold, rc = run("gold.py")
if rc == 0:
    oz = gold.get("one_oz") or {}
    parts.append(f"🪙 Kijang Emas 1oz beli RM{oz.get('buy')} jual RM{oz.get('sell')} ({gold.get('effective_date')})")
else:
    flags.append(f"emas:{gold.get('error', 'fail')}")

for line in parts:
    print(line)
if flags:
    print(f"❌ {len(flags)} adapter gagal: {'; '.join(flags)}")
    sys.exit(3)
