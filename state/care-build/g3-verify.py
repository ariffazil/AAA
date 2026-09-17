#!/usr/bin/env python3
"""G3 verification — exercise the REAL _lane_card with the REAL people register.

Why a fixture registry: /root/HERMES/lanes/lanes.yaml is ABSENT on this machine
(2026-09-17). The only surviving register is the quarantined heritage copy, so the
lane configs used here are SLICED OUT OF THAT FILE MECHANICALLY (no hand-typing,
no invented lanes) into /tmp/g3-lanes.yaml, and the live LANES_YAML path is
monkeypatched to the slice for the duration of the test only. Nothing in the live
registry path is created, moved or modified by this script.

Two variants:
  A = heritage slice as-is (lane memory_files point at the sovereign's operator
      memory — this is how the lane was configured on 2026-08-30)
  B = same slice with memory_files emptied for the tested lanes, to isolate what
      the G3 people block alone puts into a card.

Run:  /usr/local/lib/hermes-agent/venv/bin/python /root/AAA/state/care-build/g3-verify.py
Exit 0 = no private-lane fact reachable from the people block in a shared room.
"""
import importlib.util
import json
import sys
from pathlib import Path

import yaml

PLUGIN = Path("/root/.hermes/profiles/aaa-hermes/plugins/lane_switch/__init__.py")
HERITAGE = Path("/root/.quarantine/zen-20260912/_CANONICAL/HERMES-heritage-5.3G-20260904/lanes/lanes.yaml")
PEOPLE = Path("/root/HERMES/lanes/people.yaml")
FIX_A = Path("/tmp/g3-lanes.yaml")          # heritage slice as-is
FIX_B = Path("/tmp/g3-lanes-nomem.yaml")    # heritage slice, memory_files emptied

LANES = ["arif", "arif-sado", "syed", "syed-dm"]

# ---- 0. register sanity -----------------------------------------------------
import yaml as _y
people = _y.safe_load(PEOPLE.read_text())["people"]
private = [(pid, f) for pid, p in people.items() for f in (p.get("facts") or []) if str(f.get("scope")) == "dm"]
shared = [(pid, f) for pid, p in people.items() for f in (p.get("facts") or []) if str(f.get("scope")) == "shared"]
print(f"[register] people={len(people)} private_facts={len(private)} shared_facts={len(shared)}")
for pid, f in private + shared:
    print(f"  {pid:7s} scope={f.get('scope'):6s} src={str(f.get('source'))[:28]:28s} observed={f.get('observed')} | {f['fact'][:58]}")

# ---- 1. slice the heritage register (mechanical, no invented lanes) ---------
src = yaml.safe_load(HERITAGE.read_text())
slice_ = {k: v for k, v in src["lanes"].items() if k in LANES}
missing = [l for l in LANES if l not in slice_]
assert not missing, f"lane(s) absent from heritage register: {missing}"
FIX_A.write_text(
    "# G3 TEST FIXTURE A — mechanical slice of the quarantine heritage register\n"
    f"# source: {HERITAGE}\n"
    "# NOT the live registry. Live /root/HERMES/lanes/lanes.yaml is absent (2026-09-17).\n"
    + yaml.safe_dump({"version": src.get("version"), "lanes": slice_}, allow_unicode=True, sort_keys=False)
)
slice_b = {k: dict(v) for k, v in slice_.items()}
for cfg in slice_b.values():
    cfg["memory_files"] = []
FIX_B.write_text(
    "# G3 TEST FIXTURE B — same slice, memory_files emptied (isolates the G3 people block)\n"
    f"# source: {HERITAGE}\n"
    + yaml.safe_dump({"version": src.get("version"), "lanes": slice_b}, allow_unicode=True, sort_keys=False)
)
print(f"\n[fixture A] {FIX_A}  lanes={list(slice_)}")
print(f"[fixture B] {FIX_B}  lanes={list(slice_b)} (memory_files=[])")

# ---- 2. import the live plugin module by path -------------------------------
spec = importlib.util.spec_from_file_location("lane_switch_g3", PLUGIN)
mod = importlib.util.module_from_spec(spec)
sys.modules["lane_switch_g3"] = mod
spec.loader.exec_module(mod)


def render(fixture, lane_id, include_memory=False, sender_id="267378578"):
    mod.LANES_YAML = fixture
    mod._registry_cache, mod._registry_mtime = {}, 0.0
    mod.PEOPLE_YAML = PEOPLE
    mod._people_cache, mod._people_mtime = {}, 0.0
    return mod._lane_card(lane_id, include_memory=include_memory, sender_id=sender_id)


def people_block(card: str) -> str:
    lines = card.splitlines()
    try:
        start = next(i for i, l in enumerate(lines) if l.startswith("PEOPLE IN THIS LANE"))
    except StopIteration:
        return ""
    out = []
    for l in lines[start:]:
        if l.startswith(("PEOPLE IN THIS LANE", "·", "  -", "PEOPLE RULE", "SHARED-ROOM RULE")):
            out.append(l)
        else:
            break
    return "\n".join(out)


# ---- 3. live-state probe: card with the REAL registry path ------------------
mod.LANES_YAML, mod.PEOPLE_YAML = Path("/root/HERMES/lanes/lanes.yaml"), PEOPLE
mod._registry_cache, mod._registry_mtime = {}, 0.0
live_card = mod._lane_card("arif-sado", include_memory=False, sender_id="267378578")
print(f"\n[live] _lane_card('arif-sado') with the real LANES_YAML -> {live_card!r} "
      f"(LANES_YAML.exists()={mod.LANES_YAML.exists()})")

# ---- 4. lane resolution (real detect_lane, fixture registry) ---------------
mod.LANES_YAML = FIX_A
mod._registry_cache, mod._registry_mtime = {}, 0.0
print()
for uid, cid, label in [
    ("267378578", "-1003815535761", "Arif in SADO group"),
    ("1042200555", "-1003815535761", "Syed in SADO group"),
    ("267378578", "267378578", "Arif DM"),
    ("1042200555", "1042200555", "Syed DM"),
    ("999999999", "-1003815535761", "stranger in SADO"),
]:
    print(f"[detect] {label:20s} user={uid:11s} chat={cid:16s} -> lane={mod.detect_lane(uid, cid)}")

# ---- 5. cards ------------------------------------------------------------------
CARDS = {}
for tag, fixture in [("A", FIX_A), ("B", FIX_B)]:
    for lane_id, mem in [("arif-sado", False), ("arif", False), ("syed-dm", False), ("arif-sado", True)]:
        key = f"{lane_id}{'/mem' if mem else ''}#{tag}"
        CARDS[key] = render(fixture, lane_id, include_memory=mem)

for key in ("arif-sado#A", "arif#A", "syed-dm#A", "arif-sado#B"):
    card = CARDS[key]
    print("\n" + "=" * 78)
    print(f"### LANE CARD {key}  chars={len(card)}")
    print("=" * 78)
    print(people_block(card) or "!! NO PEOPLE BLOCK")

# ---- 6. leak scan ---------------------------------------------------------
def probes(pid_facts):
    """Distinctive substrings of each private fact (text + record)."""
    out = []
    for pid, f in pid_facts:
        out.append((pid, f["fact"].split(";")[0][:40]))
    return out


PB = probes(private)
GROUP_KEYS = [k for k in CARDS if k.startswith("arif-sado")]

print("\n" + "=" * 78)
print(f"### LEAK SCAN — {len(PB)} private(dm) facts x {len(GROUP_KEYS)} hard-locked GROUP cards")
print("=" * 78)
block_leaks = whole_leaks = 0
for key in GROUP_KEYS:
    card = CARDS[key]
    pb = people_block(card)
    print(f"\n-- card {key}: people-block {len(pb)} chars")
    for pid, probe in PB:
        in_block = probe in pb
        in_whole = probe in card
        block_leaks += in_block
        whole_leaks += in_whole
        flag = "LEAK" if in_block else "ok  "
        print(f"   [{flag}] people_block={str(in_block):5s} whole_card={str(in_whole):5s} {pid:7s} | {probe}")

print(f"\nRESULT people_block_leaks_into_group_card = {block_leaks}")
print(f"RESULT whole_card_leaks_into_group_card   = {whole_leaks}  (from lane memory tail, not the G3 block)")

# attribute whole-card hits
print("\n[attribution] lines in the A group card that carry one of the private-fact probes:")
for l in CARDS["arif-sado#A"].splitlines():
    if any(p in l for _, p in PB):
        print("   >", l.strip()[:200])
print("\n[attribution] same scan against card B (memory_files emptied):")
hits_b = [l for l in CARDS["arif-sado#B"].splitlines() if any(p in l for _, p in PB)]
print(f"   lines={len(hits_b)}")

# ---- 7. shared entries present exactly where they belong -------------------
print("\n[shared-scope] injected into group card 'arif-sado':")
for pid, f in shared:
    print(f"   {pid:7s} present={f['fact'][:30] in CARDS['arif-sado#A']} | {f['fact'][:60]}")

# ---- 7b. PRE-EXISTING leak path (not the G3 block) --------------------------
# _recent_lane_history() reads the lane's *MEMORY* file every turn; the arif-sado
# lane config (heritage register, 2026-08-30) points memory_files at the sovereign's
# operator memory. Its block-splitter expects '### ' interaction headers, so a
# hand-written memory file with none becomes ONE block = the whole file injected
# into the shared room. Measured here so the finding is not a story.
mem_path = Path("/root/.hermes/memories/MEMORY.md")
mem_lines = [l.strip() for l in mem_path.read_text().split("\n") if l.strip() and l.strip() != "§"]
in_a = [l for l in mem_lines if l in CARDS["arif-sado#A"]]
in_a_prefix = [l for l in mem_lines if l not in in_a and l[:60] in CARDS["arif-sado#A"]]
in_b = [l for l in mem_lines if l in CARDS["arif-sado#B"]]
print(f"\n[pre-existing path] {mem_path} content lines={len(mem_lines)}")
print(f"   reachable in SADO group card A (lane memory_files as configured): verbatim={len(in_a)} "
      f"truncated-to-240-chars={len(in_a_prefix)} total={len(in_a) + len(in_a_prefix)}")
print(f"   reachable in SADO group card B (memory_files=[])              : {len(in_b)}")
for l in in_a + in_a_prefix:
    print("   LEAKED>", l[:105])

json.dump(CARDS, open("/root/AAA/state/care-build/g3-cards.json", "w"), indent=2)
print("\n[wrote] /root/AAA/state/care-build/g3-cards.json")
sys.exit(1 if block_leaks else 0)
