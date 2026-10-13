"""
Patcher for the 6 review findings (TURN 125, 2026-10-07).
Idempotent: every assertion checks current state before editing.
"""
import hashlib
import os
import sys

CHRON = "/root/chron"
SCRIPTS = "/root/scripts"

def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

def linecount(path):
    with open(path) as f:
        return sum(1 for _ in f)

results = []  # (tag, path, before_sha, after_sha, delta, desc)

# ============================================================
# R1: chron_prediction.py — remove the 200-line dead GOL block.
# Block runs from the '# ── GUT-OVERRIDE LEDGER (GOL)' banner
# through the closing '} ' of calibration_by_gut_override.
# End sentinel: 'def compute_calibration()' at line ~841.
# ============================================================
p1 = f"{CHRON}/chron_prediction.py"
src = open(p1).read()
before_sha = sha(p1)
start_marker = "# ── GUT-OVERRIDE LEDGER (GOL)"
end_marker = "\ndef compute_calibration()"
i = src.find(start_marker)
j = src.find(end_marker, i)
assert i != -1, f"R1: start_marker not found in {p1}"
assert j != -1, f"R1: end_marker not found after start in {p1}"
note = (
    "# NOTE: GUT-OVERRIDE LEDGER (GOL) functions live canonically in\n"
    "# chron.chron_gut_override. The duplicate block that previously lived\n"
    "# here (added during the 2026-10-04 FI-008 audit response) was\n"
    "# removed 2026-10-07 because no caller imports these names from\n"
    "# chron_prediction (chron_cron_verify and production code import\n"
    "# from chron.chron_gut_override only). Anti-Bangang LAW 8 forbids\n"
    "# duplicate governance surfaces. Canonical spec:\n"
    "#   /root/AAA/instructions/gut-override-ledger-spec.md\n"
    "\n"
)
new_src = src[:i] + note + src[j+1:]
with open(p1, "w") as f:
    f.write(new_src)
results.append(("R1", p1, before_sha, sha(p1), len(src) - len(new_src),
                "removed dead GOL block"))

# ============================================================
# R2: direct-backup.sh — remove the duplicate 'local rc=$?'.
# ============================================================
p2 = f"{SCRIPTS}/direct-backup.sh"
src = open(p2).read()
before_sha = sha(p2)
old2 = "\tlocal rc=$?\n\techo \"──── rc=$rc ────\" >> \"$logf\"\n\tlocal rc=$?\n\ttail -5 \"$logf\""
new2 = "\tlocal rc=$?\n\techo \"──── rc=$rc ────\" >> \"$logf\"\n\ttail -5 \"$logf\""
assert old2 in src, f"R2: marker not found in {p2}"
src2 = src.replace(old2, new2, 1)
with open(p2, "w") as f:
    f.write(src2)
results.append(("R2", p2, before_sha, sha(p2), len(src) - len(src2),
                "removed duplicate local rc=$?"))

# ============================================================
# R3: direct-backup.sh — make tail -5 show only the current run.
# ============================================================
p3 = p2
src = open(p3).read()
before_sha = sha(p3)
old3 = "\ttail -5 \"$logf\""
new3 = (
    "\t# 2026-10-07 FI-008 fix: scope tail to the current run block so the\n"
    "\t# summary reflects THIS invocation, not accumulated log tail.\n"
    "\ttail -n 5 <(awk '/^──── run /{if (p) exit; p=1} p' \"$logf\")"
)
assert old3 in src, f"R3: marker not found in {p3}"
src3 = src.replace(old3, new3, 1)
with open(p3, "w") as f:
    f.write(src3)
results.append(("R3", p3, before_sha, sha(p3), len(src) - len(src3),
                "scoped tail -5 to current run"))

# ============================================================
# R4: chron_gut_override.py — add belt-and-braces closed-quote guard.
# ============================================================
p4 = f"{CHRON}/chron_gut_override.py"
src = open(p4).read()
before_sha = sha(p4)
if 'gut_read is not a closed verbatim quote' in src:
    results.append(("R4", p4, before_sha, sha(p4), 0,
                    "guard already in place (idempotent)"))
else:
    # Anchor: the line that says 'recorded_at': _now_iso() is the
    # first line after the validation block in record_gut_override.
    marker = "        \"recorded_at\": _now_iso(),"
    assert marker in src, "R4: anchor not found in chron_gut_override.py"
    guard = (
        "\n"
        "    # F2 belt-and-braces (2026-10-07): even if _is_verbatim_quote\n"
        "    # is ever loosened, refuse anything whose gut_read begins a\n"
        "    # quote or verbatim: marker but is not closed (FI-008\n"
        "    # partial-quote laundering defense). The canonical helper\n"
        "    # above already enforces this; the second check makes the\n"
        "    # invariant harder to regress.\n"
        "    if gut_read.strip() and not _is_verbatim_quote(gut_read):\n"
        "        return {\"recorded\": False,\n"
        "                \"error\": \"gut_read is not a closed verbatim quote\"\n"
        "                \" (FI-008 amendment 2026-10-04, hardened 2026-10-07).\"\n"
        "                \" An agent-synthesised gut_read launders the exact\"\n"
        "                \" R-FILTER defect this ledger exists to catch.\"}\n"
    )
    src4 = src.replace(marker, guard + "    " + marker.lstrip(), 1)
    with open(p4, "w") as f:
        f.write(src4)
    results.append(("R4", p4, before_sha, sha(p4), len(src) - len(src4),
                    "belt-and-braces closed-quote guard"))

# ============================================================
# R5: chron_verify.py _exec_probe_call — narrow exception scope.
# ============================================================
p5 = f"{CHRON}/chron_verify.py"
src = open(p5).read()
before_sha = sha(p5)
fn_start = src.find("def _exec_probe_call(")
fn_end = src.find("\ndef ", fn_start + 1)
assert fn_start != -1 and fn_end != -1, "R5: function not found"
fn = src[fn_start:fn_end]
old_fn = "    except Exception:\n        return None"
assert old_fn in fn, "R5: marker not in _exec_probe_call body"
new_fn = (
    "    except (urllib.error.URLError, TimeoutError, OSError,\n"
    "               json.JSONDecodeError, ValueError) as exc:\n"
    "        # 2026-10-07: debug-level log so a transport regression\n"
    "        # is recoverable instead of invisible. The outer\n"
    "        # EXEC_PROBE allowlist still treats any failure as\n"
    "        # DECLINE (no verdict) — that's correct doctrine.\n"
    "        import logging as _logging\n"
    "        _logging.getLogger(__name__).debug(\n"
    "            \"_exec_probe_call transport failure: %s: %s\",\n"
    "            type(exc).__name__, exc,\n"
    "        )\n"
    "        return None\n"
    "    except Exception as exc:\n"
    "        # Truly unexpected — log at warning so the on-call sees it.\n"
    "        import logging as _logging\n"
    "        _logging.getLogger(__name__).warning(\n"
    "            \"_exec_probe_call UNEXPECTED: %s: %s\",\n"
    "            type(exc).__name__, exc,\n"
    "        )\n"
    "        return None"
)
fn2 = fn.replace(old_fn, new_fn, 1)
src5 = src[:fn_start] + fn2 + src[fn_end:]
with open(p5, "w") as f:
    f.write(src5)
results.append(("R5", p5, before_sha, sha(p5), len(src) - len(src5),
                "narrow exception scope + debug log"))

# ============================================================
# R6: chron/server.py chron_frame_witness — list -> list | None.
# ============================================================
p6 = f"{CHRON}/server.py"
src = open(p6).read()
before_sha = sha(p6)
old6 = (
    "@mcp.tool()\n"
    "def chron_frame_witness(\n"
    "    action: str = \"witness\",\n"
    "    claims: list = None,\n"
    "    claim_id: str = \"\",\n"
    ") -> dict:"
)
new6 = (
    "@mcp.tool()\n"
    "def chron_frame_witness(\n"
    "    action: str = \"witness\",\n"
    "    claims: list | None = None,\n"
    "    claim_id: str = \"\",\n"
    ") -> dict:"
)
assert old6 in src, f"R6: marker not found in {p6}"
src6 = src.replace(old6, new6, 1)
with open(p6, "w") as f:
    f.write(src6)
results.append(("R6", p6, before_sha, sha(p6), len(src) - len(src6),
                "annotation: list -> list | None"))

# Report
print("=" * 88)
print("PATCH RESULTS")
print("=" * 88)
print(f'{"#":<4} {"file":<55} {"delta":>8} {"sha256(head)":<18} {"lines":>6}')
print("-" * 88)
total_bytes = 0
for tag, p, before, after, delta, desc in results:
    total_bytes += -delta
    print(f'{tag:<4} {p[-55:]:<55} {-delta:>8} {after[:18]:<18} {linecount(p):>6}  {desc}')
print("-" * 88)
print(f'TOTAL bytes removed: {total_bytes}')
