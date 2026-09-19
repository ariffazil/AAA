#!/usr/bin/env python3
"""Cost>value ranking from the Hermes skill usage ledger.
Witness: /root/.hermes/skills/.usage.json (last_used_at / last_viewed_at / created_at per skill name)
Cross-ref: /root/AAA/skills (what is actually on disk). Read-only."""
import json, os, datetime, collections

U = "/root/.hermes/skills/.usage.json"
CANON = "/root/AAA/skills"
NOW = datetime.datetime.now(datetime.timezone.utc)

u = json.load(open(U))
print("ledger entries:", len(u))

def age(ts):
    if not ts:
        return None
    try:
        t = datetime.datetime.fromisoformat(ts)
    except Exception:
        return None
    return (NOW - t).days

rows = []
for name, d in u.items():
    lu, lv, cr = d.get("last_used_at"), d.get("last_viewed_at"), d.get("created_at")
    rows.append({
        "name": name,
        "uses": d.get("use_count", 0),
        "views": d.get("view_count", 0),
        "used_days": age(lu),
        "viewed_days": age(lv),
        "age_days": age(cr),
        "patches": d.get("patch_count", 0),
        "pinned": d.get("pinned", False),
        "archived": d.get("archived_at"),
        "state": d.get("state") or "",
    })

never_used = [r for r in rows if r["used_days"] is None]
zero_use = [r for r in rows if r["uses"] == 0]
seen_only = [r for r in rows if r["uses"] == 0 and r["views"] > 0]
dead = sorted([r for r in rows if r["used_days"] is not None and r["used_days"] >= 30],
              key=lambda r: -r["used_days"])

print("\nLEDGER: use_count==0 (indexed, never actually used):", len(zero_use))
print("  of those, viewed at least once (loader index build):", len(seen_only))
print("NEVER USED AT ALL (no view, no use):", len(never_used))
print("uses_total:", sum(r["uses"] for r in rows), "| median uses:", sorted(r["uses"] for r in rows)[len(rows)//2])

# canon set for the ghost test: a ledger name with no body on disk
names_on_disk = set()
for dp, dn, fn in os.walk(CANON):
    if "/." in dp.replace(CANON, ""):
        continue
    if "SKILL.md" in fn:
        names_on_disk.add(os.path.basename(dp).lower())

ghost_names = [r["name"] for r in rows if r["name"].lower() not in names_on_disk]
print("LEDGER NAMES WITH NO BODY ON DISK:", len(ghost_names))

# cost proxy: bytes on disk per skill
size = {}
for dp, dn, fn in os.walk(CANON):
    if "/." in dp.replace(CANON, ""):
        continue
    if "SKILL.md" in fn:
        t = 0
        for ddp, ddn, dfn in os.walk(dp):
            for f in dfn:
                try:
                    t += os.path.getsize(os.path.join(ddp, f))
                except OSError:
                    pass
        size[os.path.basename(dp).lower()] = t

CUT = 20  # days
kill = []
for r in rows:
    nm = r["name"].lower()
    b = size.get(nm, 0)
    if r["uses"] == 0 and r["views"] == 0:
        kill.append((b, r, "NEVER TOUCHED"))
    elif r["uses"] == 0:
        kill.append((b, r, "INDEXED ONLY, NEVER USED"))
    elif r["used_days"] is not None and r["used_days"] >= CUT:
        kill.append((b, r, f"UNUSED {r['used_days']}d"))
kill.sort(key=lambda x: -x[0])

out = [f"# cost>value candidates from the usage ledger ({NOW.date()})",
       f"ledger entries: {len(u)} | uses==0: {len(zero_use)} | unused>= {CUT}d: {sum(1 for r in rows if r['used_days'] is not None and r['used_days']>=CUT)}",
       f"names in ledger with no body in canon: {len(ghost_names)}", ""]
out.append("## NEVER-USED, ranked by bytes they cost on disk")
for b, r, why in kill[:60]:
    out.append(f"  {b/1024:8.1f} KB  {why:26s} last_viewed={r['viewed_days']}d  {r['name']}")
out.append("")
out.append("## USED BUT DEAD (>=30 days since last use)")
for r in dead[:40]:
    out.append(f"  last_used={r['used_days']:5d}d  patches={r['patches']:2d}  {r['name']}")
out.append("")
out.append("## LEDGER NAMES WITH NO BODY ON DISK (phantom capability)")
out.extend("  " + g for g in sorted(ghost_names)[:60])

p = "/root/AAA/skills-retired/2026-09-19-namespace-collapse/USAGE-COST-VALUE.txt"
os.makedirs(os.path.dirname(p), exist_ok=True)
open(p, "w").write("\n".join(out))
print("\nreport:", p)
print("\n".join(out[:34]))
