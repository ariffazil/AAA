#!/usr/bin/env bash
# Falsification test for landlock-guard.py — proves the write-set asymmetry binds
# even when the process runs as root. A lock that has never been attacked is a
# claim, not a control. This test also guards against the "guard crashes so the
# write silently never happens" false-pass: every test asserts the guard actually
# exec'd (its "confined:" marker appears on stderr) before trusting a denial.
set -u

GUARD=/root/AAA/governance/landlock-guard.py
POLICY=/root/AAA/governance/write-set-asymmetry-test-policy.json
WORK=/tmp/landlock-scratch-work
PROT=/tmp/landlock-scratch-protected
MARK="[landlock-guard] confined"

PASS=0
FAIL=0
ok() {
	echo "PASS: $1"
	PASS=$((PASS + 1))
}
bad() {
	echo "FAIL: $1"
	FAIL=$((FAIL + 1))
}

run_guard() {
	# $@ = command. Echoes "1" to stdout if the guard exec'd (marker seen), else "0".
	local marker_seen
	marker_seen=$("$GUARD" --policy "$POLICY" -- "$@" 2>&1 | grep -qF "$MARK" && echo 1 || echo 0)
	echo "$marker_seen"
}

echo "== setup =="
rm -rf "$WORK" "$PROT"
mkdir -p "$WORK" "$PROT"
echo "sentinel" >"$PROT/floor.md"
echo "uid running test: $(id -u) (0=root)"

echo
echo "== T0 guard self-check: does it even exec (no crash) on a trivial cmd? =="
if [ "$(run_guard true)" = "1" ]; then ok "guard exec'd child without crashing"; else bad "guard crashed before exec (traceback)"; fi

echo
echo "== T1 baseline: unconfined root CAN write to protected =="
if echo "overwrite" >"$PROT/floor.md" 2>/dev/null; then
	ok "baseline — root wrote to protected without confinement (proves chmod can't stop root)"
else
	bad "baseline — root could not write; environment already restricts, test invalid"
fi
echo "sentinel" >"$PROT/floor.md" # restore

echo
echo "== T2 allow-listed write must SUCCEED (and guard must have exec'd) =="
r=$(run_guard sh -c 'echo ok > "$1/work.txt"' _ "$WORK")
w=0
[ -f "$WORK/work.txt" ] && w=1
if [ "$r" = "1" ] && [ "$w" = "1" ]; then
	ok "confined process wrote to allow-listed dir (allow path works)"
else
	bad "allow write failed (exec=$r write=$w) — lock is over-broad"
fi

echo
echo "== T3 protected write must be DENIED =="
r=$(run_guard sh -c 'echo pwned > "$1/floor.md"' _ "$PROT")
if [ "$r" = "1" ] && [ "$(cat "$PROT/floor.md")" = "sentinel" ]; then
	ok "write to protected path denied (guard exec'd, file intact)"
else
	bad "protected write NOT denied (exec=$r) or file modified"
fi

echo
echo "== T4 protected truncate must be DENIED =="
r=$(run_guard sh -c ': > "$1/floor.md"' _ "$PROT")
if [ "$r" = "1" ] && [ "$(cat "$PROT/floor.md")" = "sentinel" ]; then
	ok "truncate denied"
else
	bad "truncate NOT denied (exec=$r) or file modified"
fi

echo
echo "== T5 protected remove+replace must be DENIED =="
r=$(run_guard sh -c 'rm -f "$1/floor.md" && echo new > "$1/floor.md"' _ "$PROT")
if [ "$r" = "1" ] && [ "$(cat "$PROT/floor.md")" = "sentinel" ]; then
	ok "remove+replace denied (REFER/REMOVE/MAKE governed)"
else
	bad "remove+replace NOT denied (exec=$r) or file replaced"
fi

echo
echo "== summary =="
echo "PASS=$PASS FAIL=$FAIL"
[ "$FAIL" -eq 0 ] && echo "RESULT: LOCK VERIFIED" || echo "RESULT: LOCK BROKEN — fix before any rollout"
exit $FAIL
