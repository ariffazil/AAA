#!/bin/bash
# ==============================================================================
# probe_sys_health.sh  ->  /root/AAA/state/sys_health.json
#
# Supersedes the 2026-08 OpenClaw probe (kept at probe_sys_health.sh.bak-*).
# F1 Safe: read-only probes. Atomic write. Single-writer flock. No secret output.
#
# ------------------------------------------------------------------------------
# DEFECTS FIXED (audit 2026-09-15, KVM8)
# ------------------------------------------------------------------------------
# B1 VAULT999 SOURCE WAS A DEAD CHECK, AND THE WRONG CHECK.
#    Old code read /root/VAULT999/outcomes.jsonl and asserted only that its
#    LAST LINE parsed as JSON, plus `[ -s file ]`. On an append-only 28 MB log
#    that is vacuously true: the check could never fail, never compared against
#    the signed head, and never touched the authoritative writer.
#    REAL ACTIVE SEAL STORE ON KVM8 (established by live probe, this host):
#      AUTHORITATIVE : http://127.0.0.1:5001/vault/status
#                      -> vault_seals_total, chain_integrity, chain_gaps,
#                         append_only_enforced, pending_holds, last_seal
#                      served by vault999-writer.service
#                      (python3 /root/arifOS/deploy/vault999-writer/main.py)
#      EVENT LOG     : /root/VAULT999/outcomes.jsonl   (LIVE)
#                      hardlink, inode-identical with
#                      /root/arifOS/VAULT999/outcomes.jsonl
#      SEAL CHAIN    : /root/.local/share/arifos/vault999/seal_chain.jsonl
#                      + seal_chain_head.json
#      SIGNED HEAD   : /root/AAA/state/vault_head_attestation.json
#                      (emitted by /root/scripts/vault_head_attest.py)
#    STALE / DO NOT TRUST:
#      - VAULT_WRITER_URL=http://127.0.0.1:8100 and VAULT_API_URL=:8100
#        -> NOTHING is listening on :8100 (vault999-api.service = not-found).
#      - /root/.local/share/arifos/vault999/outcomes.jsonl -> frozen Aug 25.
#    The probe now prefers the live writer, records the stale env var, and
#    detects append-only truncation against the signed attestation.
# B2 SILENT DEFAULTS. Disk fell back to 0, git to 0, organs to ALL_GREEN.
#    "No data" now yields null / CANNOT_WITNESS, never a benign value.
# B3 EXIT CODE was always 0, so callers could not tell a dead probe from a
#    healthy host. Now non-zero when a probe could not be witnessed or an
#    integrity break was observed.
# B4 NO MONOTONIC TIMESTAMP. Wall clock alone can regress. Added monotonic_ns
#    (kernel CLOCK_MONOTONIC via /proc/uptime), run_seq (persisted, never
#    decrements), and wall_clock_regressed.
# B5 NOT IDEMPOTENT / RACE. Fixed $TMP_FILE path meant two concurrent runs
#    clobbered each other. Now mktemp + flock.
# B6 ORGAN HEALTH WAS A FALSE GREEN. `systemctl --state=failed` cannot see a
#    unit that is inactive or not-found, so a missing organ scored ALL_GREEN.
#    Now each canonical organ unit is probed by name.
# ------------------------------------------------------------------------------
# CONTRACT
#   probes   : read-only. Never mutates anything outside AAA/state.
#   write    : mktemp in the same dir, then mv -> readers never see a partial.
#   failure  : a probe that cannot be witnessed => null + probe_status.
#   exit 0   : every probe witnessed.
#   exit 1   : >=1 probe unwitnessed, and/or integrity break observed.
#              (the state file IS still written, in good faith, with nulls)
#   exit 2   : could not acquire the single-writer lock.
# ==============================================================================

set -uo pipefail
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
umask 022

STATE_DIR="/root/AAA/state"
STATE_FILE="$STATE_DIR/sys_health.json"
LOG_FILE="$STATE_DIR/sys_health_probe.log"
LOCK_FILE="$STATE_DIR/.sys_health.lock"
SEQ_FILE="$STATE_DIR/.sys_health_runseq.json"
HOSTNAME_SHORT="$(hostname -s)"

# ---- vault surfaces (see B1) -------------------------------------------------
VAULT_WRITER_PRIMARY="http://127.0.0.1:5001"
VAULT_OUTCOMES="/root/VAULT999/outcomes.jsonl"
VAULT_OUTCOMES_STALE="/root/.local/share/arifos/vault999/outcomes.jsonl"
VAULT_SEAL_CHAIN="/root/.local/share/arifos/vault999/seal_chain.jsonl"
VAULT_SEAL_HEAD="/root/.local/share/arifos/vault999/seal_chain_head.json"
VAULT_ATTEST="/root/AAA/state/vault_head_attestation.json"

# ---- canonical organ units (probed by name, see B6) --------------------------
ORGAN_UNITS="arifos a-forge aaa-mcp geox-mcp wealth-organ well vault999-writer"
GIT_REPOS="/root/arifOS /root/A-FORGE /root/AAA /root/GEOX /root/WEALTH /root/WELL"

# ---- freshness budget advertised to consumers -------------------------------
VALID_FOR_SECONDS=1800

mkdir -p "$STATE_DIR" || { echo "FATAL cannot create $STATE_DIR" >&2; exit 1; }

log() { printf '[%s] %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*" >>"$LOG_FILE" 2>/dev/null || true; }

# ---- single-writer lock (B5) -------------------------------------------------
exec 9>"$LOCK_FILE" || { echo "FATAL cannot open lock file $LOCK_FILE" >&2; exit 2; }
if ! flock -n 9; then
    echo "FATAL concurrent probe already running (lock held on $LOCK_FILE)" >&2
    log "SKIP: concurrent run, lock busy"
    exit 2
fi

# ---- secrets: optional; absence is recorded, never defaulted -----------------
# CAUTION (audit 2026-09-15): /root/.secrets/kunci-root.env has a FORWARD
# REFERENCE — the assignment at line 82 interpolates $QWEN_INDIVIDUAL_API_KEY,
# which is only defined at line 399. Sourcing it while `set -u` is active aborts
# with "unbound variable" (exit 127) and, for a script without -e, silently
# truncates the env. That file is outside this script's edit scope, so -u is
# relaxed for the source only; every later use of a secret stays guarded.
SECRETS_SOURCED=false
SECRETS_SOURCE_ERROR=""
if [ -f /root/.secrets/kunci-root.env ]; then
    set +u
    set -a
    if source /root/.secrets/kunci-root.env >/dev/null 2>&1; then
        SECRETS_SOURCED=true
    else
        SECRETS_SOURCE_ERROR="source returned non-zero (see forward-reference note above)"
    fi
    set +a
    set -u
else
    SECRETS_SOURCE_ERROR="file missing: /root/.secrets/kunci-root.env"
fi

FAILURES=()                      # strings: "<probe>: <reason>"
add_failure() { FAILURES+=("$1"); log "FAIL $1"; }

num_or_null()  { case "$1" in ''|*[!0-9]*) echo null ;; *) echo "$1" ;; esac; }
bool_or_null() { case "$1" in true|false) echo "$1" ;; *) echo null ;; esac; }

# ==============================================================================
# 1. TIMESTAMPS — wall + monotonic (B4)
# ==============================================================================
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
TS_EPOCH="$(date -u +%s)"
MONO_NS="$(awk '{printf "%.0f", $1*1000000000}' /proc/uptime 2>/dev/null)"
MONO_NS="$(num_or_null "$MONO_NS")"

PREV_TS="$(jq -r '.timestamp_utc // empty' "$STATE_FILE" 2>/dev/null)"
PREV_EPOCH=""
WALL_REGRESSED=false
if [ -n "$PREV_TS" ]; then
    PREV_EPOCH="$(date -u -d "$PREV_TS" +%s 2>/dev/null || echo '')"
    if [ -n "$PREV_EPOCH" ] && [ "$TS_EPOCH" -lt "$PREV_EPOCH" ]; then
        WALL_REGRESSED=true
        add_failure "clock: wall clock regressed (prev=$PREV_TS now=$TS)"
    fi
fi

# monotonic run counter: persisted, increments, never decrements
PREV_SEQ="$(jq -r '.run_seq // 0' "$SEQ_FILE" 2>/dev/null)"
case "$PREV_SEQ" in ''|*[!0-9]*) PREV_SEQ=0 ;; esac
RUN_SEQ=$((PREV_SEQ + 1))
jq -n --argjson s "$RUN_SEQ" --arg ts "$TS" '{run_seq:$s, last_run_utc:$ts}' >"$SEQ_FILE" 2>/dev/null

# ==============================================================================
# 2. DEEPSEEK LIVENESS
#    Observed HTTP status is a real value. Only an unreachable host is a probe
#    failure — an HTTP 402/401 is a witnessed fact and is recorded verbatim (B2).
# ==============================================================================
DS_STATUS="$(curl -s -o /dev/null -w '%{http_code}' --max-time 8 https://api.deepseek.com/v1/models 2>/dev/null || echo '')"
DS_AUTH_USED=false
if [ "$DS_STATUS" = "401" ] || [ -z "$DS_STATUS" ] || [ "$DS_STATUS" = "000" ]; then
    # retry authenticated against a real endpoint (models list requires auth)
    if [ -n "${DEEPSEEK_API_KEY:-}" ]; then
        DS_AUTH_USED=true
        DS_STATUS="$(curl -s -o /dev/null -w '%{http_code}' --max-time 8 \
            -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
            https://api.deepseek.com/v1/models 2>/dev/null || echo '')"
    fi
fi
case "$DS_STATUS" in
    ''|000) DS_JSON=null
            DS_STATE="UNREACHABLE"
            add_failure "deepseek: no HTTP response (network/timeout)" ;;
    *)      DS_JSON="$(num_or_null "$DS_STATUS")"
            if [ "$DS_STATUS" = "200" ]; then DS_STATE="OK"; else DS_STATE="HTTP_${DS_STATUS}"; fi ;;
esac

# ==============================================================================
# 3. VAULT999 INTEGRITY  (rebuilt — see B1)
# ==============================================================================
# 3a. authoritative writer: prefer the live one, record a dead env override
ENV_WRITER_URL="${VAULT_WRITER_URL:-}"
SEL_WRITER=""
SEL_WRITER_STATE=""
ENV_WRITER_LIVE=null
if [ -n "$ENV_WRITER_URL" ]; then
    code="$(curl -s -o /tmp/.vsh_w_env.$$ -w '%{http_code}' --max-time 5 "$ENV_WRITER_URL/health" 2>/dev/null || echo '')"
    case "$code" in 200) ENV_WRITER_LIVE=true; SEL_WRITER="$ENV_WRITER_URL"; SEL_WRITER_STATE="OK" ;;
        *) ENV_WRITER_LIVE=false ;; esac
    rm -f /tmp/.vsh_w_env.$$ 2>/dev/null
fi
if [ -z "$SEL_WRITER" ]; then
    code="$(curl -s -o /tmp/.vsh_w_pri.$$ -w '%{http_code}' --max-time 5 "$VAULT_WRITER_PRIMARY/health" 2>/dev/null || echo '')"
    if [ "$code" = "200" ]; then SEL_WRITER="$VAULT_WRITER_PRIMARY"; SEL_WRITER_STATE="OK"; fi
    rm -f /tmp/.vsh_w_pri.$$ 2>/dev/null
fi

V_SEALS=null; V_INTEGRITY=null; V_GAPS=null; V_APPEND=null; V_HOLDS=null; V_LAST_TS=null
WRITER_STATE="UNREACHABLE"
# A live writer computes chain integrity while seals are being appended, so a
# single sample can report a spurious gap during a concurrent write (observed
# live on KVM8 at 15:11:43Z, contradicted by 6/6 corroborating polls). Never
# cry wolf on one sample: confirm a bad reading before failing the probe.
INTEGRITY_POLLS=0
INTEGRITY_TRANSIENT=false
V_INTEGRITY_FIRST=null
_vault_status_fetch() {
    local vs="/tmp/.vsh_vs.$$"
    curl -s --max-time 6 "$SEL_WRITER/vault/status" -o "$vs" 2>/dev/null && jq -e . "$vs" >/dev/null 2>&1 || { rm -f "$vs"; return 1; }
    V_SEALS="$(jq -r '(.vault_seals_total // .vault_seals_count) // null' "$vs" 2>/dev/null)"
    V_INTEGRITY="$(jq -r '.chain_integrity // null' "$vs" 2>/dev/null)"
    V_GAPS="$(jq -r '.chain_gaps // null' "$vs" 2>/dev/null)"
    V_APPEND="$(jq -r '.append_only_enforced // null' "$vs" 2>/dev/null)"
    V_HOLDS="$(jq -r '.pending_holds // null' "$vs" 2>/dev/null)"
    V_LAST_TS="$(jq -r '.last_seal.chain_hash // .last_seal.seal_hash // null' "$vs" 2>/dev/null)"
    rm -f "$vs"
    return 0
}
if [ -n "$SEL_WRITER" ]; then
    if _vault_status_fetch; then
        WRITER_STATE="OK"
        INTEGRITY_POLLS=1
        V_INTEGRITY_FIRST="$V_INTEGRITY"
        # confirm any non-INTACT / non-zero-gap reading up to 3 more times
        while [ "$INTEGRITY_POLLS" -lt 4 ] \
              && { [ "$V_INTEGRITY" != "INTACT" ] || [ "$V_GAPS" != "0" ]; }; do
            sleep 1
            if _vault_status_fetch; then
                INTEGRITY_POLLS=$((INTEGRITY_POLLS + 1))
                if [ "$V_INTEGRITY" = "INTACT" ] && [ "$V_GAPS" = "0" ]; then
                    INTEGRITY_TRANSIENT=true     # first sample was a write race
                    V_INTEGRITY="$V_INTEGRITY"; V_GAPS="$V_GAPS"
                fi
            else
                break
            fi
        done
    else
        WRITER_STATE="UNPARSEABLE"
    fi
else
    add_failure "vault: no reachable seal writer (tried env '${ENV_WRITER_URL:-unset}' and $VAULT_WRITER_PRIMARY)"
fi
[ "$WRITER_STATE" = "UNPARSEABLE" ] && add_failure "vault: writer $SEL_WRITER responded but /vault/status was unparseable"

# 3b. event log: identity + append-only truncation vs the signed attestation
OUT_LINES=null; OUT_BYTES=null; OUT_AGE=null; OUT_LAST=null; OUT_STATE="MISSING"
if [ -f "$VAULT_OUTCOMES" ]; then
    OUT_BYTES="$(stat -c %s "$VAULT_OUTCOMES" 2>/dev/null)"
    OUT_AGE="$(( $(date -u +%s) - $(stat -c %Y "$VAULT_OUTCOMES" 2>/dev/null || echo 0) ))"
    OUT_LINES="$(wc -l <"$VAULT_OUTCOMES" 2>/dev/null | tr -d ' ')"
    if tail -1 "$VAULT_OUTCOMES" 2>/dev/null | jq -e . >/dev/null 2>&1; then
        OUT_LAST="$(tail -1 "$VAULT_OUTCOMES" | jq -r '.ts // .timestamp // empty' 2>/dev/null)"
        OUT_STATE="OK"
    else
        OUT_STATE="TAIL_UNPARSEABLE"
        add_failure "vault: last line of $VAULT_OUTCOMES is not valid JSON"
    fi
else
    add_failure "vault: event log missing at $VAULT_OUTCOMES"
fi

# 3c. signed attestation cross-check -> truncation detection
ATT_LINES=null; ATT_EMITTED=null; TRUNCATED=false
if [ -f "$VAULT_ATTEST" ] && jq -e . "$VAULT_ATTEST" >/dev/null 2>&1; then
    ATT_LINES="$(jq -r '.payload.outcomes.lines // null' "$VAULT_ATTEST" 2>/dev/null)"
    ATT_EMITTED="$(jq -r '.payload.emitted_at // null' "$VAULT_ATTEST" 2>/dev/null)"
    if [ "$OUT_LINES" != "null" ] && [ "$ATT_LINES" != "null" ] \
       && [ "$OUT_LINES" -lt "$ATT_LINES" ] 2>/dev/null; then
        TRUNCATED=true
        add_failure "vault: APPEND-ONLY BREACH — live lines ($OUT_LINES) < signed attestation ($ATT_LINES, $ATT_EMITTED)"
    fi
else
    add_failure "vault: signed head attestation missing/unparseable at $VAULT_ATTEST"
fi

# 3d. seal chain file + head
SC_STATE="MISSING"; SC_AGE=null; SC_HEAD_SEQ=null
if [ -f "$VAULT_SEAL_CHAIN" ]; then
    SC_STATE="OK"; SC_AGE="$(( $(date -u +%s) - $(stat -c %Y "$VAULT_SEAL_CHAIN" 2>/dev/null || echo 0) ))"
else
    add_failure "vault: seal chain missing at $VAULT_SEAL_CHAIN"
fi
[ -f "$VAULT_SEAL_HEAD" ] && SC_HEAD_SEQ="$(jq -r '.seq // null' "$VAULT_SEAL_HEAD" 2>/dev/null)"

# 3e. stale surfaces reported, never trusted
STALE_PRESENT=false; STALE_AGE_DAYS=null
if [ -f "$VAULT_OUTCOMES_STALE" ]; then
    STALE_PRESENT=true
    STALE_AGE_DAYS="$(( ( $(date -u +%s) - $(stat -c %Y "$VAULT_OUTCOMES_STALE" 2>/dev/null || echo 0) ) / 86400 ))"
fi

# 3f. verdict: true only on positive evidence; null when unwitnessable
if [ "$WRITER_STATE" = "OK" ] && [ "$V_INTEGRITY" = "INTACT" ] && [ "$TRUNCATED" = "false" ] && [ "$OUT_STATE" = "OK" ]; then
    VAULT_SEAL=true
elif [ "$WRITER_STATE" != "OK" ] || [ "$V_INTEGRITY" = "null" ]; then
    VAULT_SEAL=null      # cannot witness
else
    VAULT_SEAL=false     # observed broken
fi
[ "$V_INTEGRITY" != "null" ] && [ "$V_INTEGRITY" != "INTACT" ] && \
    add_failure "vault: chain_integrity=$V_INTEGRITY (expected INTACT)"
[ "$V_GAPS" != "null" ] && [ "$V_GAPS" != "0" ] && \
    add_failure "vault: chain_gaps=$V_GAPS (expected 0)"

# ==============================================================================
# 4. DISK  (df -P: single-line POSIX output, cannot wrap)
# ==============================================================================
DISK_PCT=null; DISK_AVAIL=null; DISK_FS=null; DISK_STATE="FAILED"
DISK_LINE="$(df -P / 2>/dev/null | tail -1)"
if [ -n "$DISK_LINE" ]; then
    DISK_PCT="$(printf '%s\n' "$DISK_LINE"  | awk '{gsub(/%/,"",$5); print $5}')"
    DISK_AVAIL="$(printf '%s\n' "$DISK_LINE" | awk '{print $4}')"
    DISK_FS="$(printf '%s\n' "$DISK_LINE"     | awk '{print $1}')"
    DISK_PCT="$(num_or_null "$DISK_PCT")"; DISK_AVAIL="$(num_or_null "$DISK_AVAIL")"
    [ "$DISK_PCT" != "null" ] && DISK_STATE="OK"
fi
[ "$DISK_STATE" = "OK" ] || add_failure "disk: could not parse df -P / output"

# ==============================================================================
# 5. GIT DIRTY COUNT (per-repo, so the number is actionable)
# ==============================================================================
GIT_TOTAL=0; GIT_OK=true; GIT_REPOS_JSON="{}"
for repo in $GIT_REPOS; do
    name="$(basename "$repo")"
    if [ ! -d "$repo" ]; then
        GIT_REPOS_JSON="$(jq -c --arg n "$name" '. + {($n):"MISSING"}' <<<"$GIT_REPOS_JSON" 2>/dev/null || echo "$GIT_REPOS_JSON")"
        GIT_OK=false; add_failure "git: repo dir missing $repo"; continue
    fi
    if ! git -C "$repo" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        GIT_REPOS_JSON="$(jq -c --arg n "$name" '. + {($n):"NOT_A_REPO"}' <<<"$GIT_REPOS_JSON" 2>/dev/null || echo "$GIT_REPOS_JSON")"
        GIT_OK=false; add_failure "git: not a git work tree: $repo"; continue
    fi
    # --no-optional-locks: status must not refresh the index (F1-safe read-only);
    # also required for this probe to work under systemd ProtectSystem=strict.
    c="$(git --no-optional-locks -C "$repo" status --porcelain 2>/dev/null | wc -l | tr -d ' ')"
    c="$(num_or_null "$c")"
    if [ "$c" = "null" ]; then
        GIT_OK=false; add_failure "git: status failed for $repo"
        GIT_REPOS_JSON="$(jq -c --arg n "$name" '. + {($n):null}' <<<"$GIT_REPOS_JSON" 2>/dev/null || echo "$GIT_REPOS_JSON")"
        continue
    fi
    GIT_TOTAL=$((GIT_TOTAL + c))
    GIT_REPOS_JSON="$(jq -c --arg n "$name" --argjson v "$c" '. + {($n):$v}' <<<"$GIT_REPOS_JSON" 2>/dev/null || echo "$GIT_REPOS_JSON")"
done
if [ "$GIT_OK" = true ]; then GIT_JSON="$GIT_TOTAL"; GIT_STATE="OK"; else
    # B2 (void guard): a partial sweep must NOT publish a total. Summing the
    # repos that answered and labelling it "git_dirty_count" reads as "clean
    # host" when it really means "we could not see everything". Null it out and
    # let probe_failures + probes.git.repos carry the per-repo detail.
    GIT_JSON="null"; GIT_STATE="PARTIAL"; add_failure "git: one or more repos could not be witnessed (total suppressed)"; fi

# ==============================================================================
# 6. ORGAN HEALTH (per-unit, B6)
# ==============================================================================
ORG_JSON="{}"; ORG_STATE="OK"; ORG_DEGRADED=false; ORG_MISSING=false
for u in $ORGAN_UNITS; do
    st="$(systemctl is-active "$u" 2>/dev/null || true)"
    [ -n "$st" ] || st="unknown"
    ORG_JSON="$(jq -c --arg u "$u" --arg s "$st" '. + {($u):$s}' <<<"$ORG_JSON" 2>/dev/null || echo "$ORG_JSON")"
    case "$st" in
        active) : ;;
        failed) ORG_DEGRADED=true ;;
        *)      ORG_MISSING=true ;;
    esac
done
# any failed unit anywhere (context, not an organ verdict)
FAILED_ALL="$(systemctl list-units --state=failed --no-legend --plain 2>/dev/null | awk '{print $1}' | tr '\n' ' ' | sed 's/ *$//')"
FAILED_ALL_COUNT=0
[ -n "$FAILED_ALL" ] && FAILED_ALL_COUNT="$(printf '%s' "$FAILED_ALL" | wc -w | tr -d ' ')"

if [ "$ORG_DEGRADED" = true ]; then
    ORGAN_HEALTH="SYSTEM_DEGRADED"; ORG_STATE="DEGRADED"
elif [ "$ORG_MISSING" = true ]; then
    ORGAN_HEALTH="CANNOT_WITNESS"; ORG_STATE="CANNOT_WITNESS"
    add_failure "organs: one or more canonical organ units were not active"
else
    ORGAN_HEALTH="ALL_GREEN"; ORG_STATE="OK"
fi

# ==============================================================================
# 7. VERDICT + ATOMIC WRITE
# ==============================================================================
if [ "${#FAILURES[@]}" -eq 0 ]; then
    PROBE_STATUS="OK"; EXIT_CODE=0; FAILURES_JSON="[]"
else
    PROBE_STATUS="CANNOT_WITNESS"; EXIT_CODE=1
    FAILURES_JSON="$(printf '%s\n' "${FAILURES[@]}" | jq -R . | jq -s .)"
    [ -n "$FAILURES_JSON" ] || FAILURES_JSON="[]"
fi

DS_JSON_OBJ="$(jq -n --arg s "$DS_STATE" --argjson c "$DS_JSON" --argjson a "$DS_AUTH_USED" \
    '{status:$s, http_code:$c, authed_retry:$a}')"

VAULT_JSON_OBJ="$(jq -n \
    --arg ws "$WRITER_STATE" --arg wu "${SEL_WRITER:-none}" --arg ew "${ENV_WRITER_URL:-unset}" \
    --argjson ewl "$ENV_WRITER_LIVE" \
    --argjson seals "$(num_or_null "$V_SEALS")" --arg integ_raw "${V_INTEGRITY:-null}" \
    --argjson integ_bool "$(if [ "${V_INTEGRITY:-null}" = "INTACT" ]; then echo true; elif [ "${V_INTEGRITY:-null}" = "null" ]; then echo null; else echo false; fi)" \
    --argjson gaps "$(num_or_null "$V_GAPS")" \
    --argjson app "$(bool_or_null "$V_APPEND")" --argjson holds "$(num_or_null "$V_HOLDS")" \
    --argjson opts "$(num_or_null "$OUT_LINES")" --argjson ob "$(num_or_null "$OUT_BYTES")" \
    --argjson oa "$(num_or_null "$OUT_AGE")" --arg os "$OUT_STATE" --arg ol "${OUT_LAST:-}" \
    --argjson attl "$(num_or_null "$ATT_LINES")" --arg atte "${ATT_EMITTED:-}" \
    --argjson trunc "$TRUNCATED" \
    --arg scs "$SC_STATE" --argjson sca "$(num_or_null "$SC_AGE")" --argjson sch "$(num_or_null "$SC_HEAD_SEQ")" \
    --argjson sp "$STALE_PRESENT" --argjson sad "$(num_or_null "$STALE_AGE_DAYS")" \
    --argjson polls "$INTEGRITY_POLLS" --argjson trint "$INTEGRITY_TRANSIENT" --arg intfirst "$V_INTEGRITY_FIRST" \
    --arg op "$VAULT_OUTCOMES" --arg spth "$VAULT_OUTCOMES_STALE" --arg scp "$VAULT_SEAL_CHAIN" --arg ap "$VAULT_ATTEST" '
    {
      status: (if $ws=="OK" and $integ_raw=="INTACT" and ($trunc|not) and $os=="OK" then "OK" else "CANNOT_WITNESS" end),
      writer_url_used: $wu, writer_status: $ws,
      vault_seals_total: $seals,
      chain_integrity: (if $integ_raw=="null" then null else $integ_raw end),
      chain_integrity_intact: $integ_bool,
      chain_gaps: $gaps,
      integrity_polls: $polls,
      integrity_first_sample: (if $intfirst=="null" then null else $intfirst end),
      integrity_transient: $trint,
      append_only_enforced: $app, pending_holds: $holds,
      env_writer_url: $ew, env_writer_url_live: $ewl,
      outcomes_path: $op, outcomes_state: $os, outcomes_lines: $opts,
      outcomes_bytes: $ob, outcomes_age_seconds: $oa,
      outcomes_last_event_ts: (if $ol=="" then null else $ol end),
      attestation_path: $ap, attested_lines: $attl,
      attestation_emitted_at: (if $atte=="" then null else $atte end),
      truncation_detected: $trunc,
      seal_chain_path: $scp, seal_chain_state: $scs, seal_chain_age_seconds: $sca,
      seal_chain_head_seq: $sch, seal_chain_role: "derived_legacy_not_authoritative",
      stale_outcomes_path: $spth, stale_outcomes_present: $sp, stale_outcomes_age_days: $sad
    }')"

DISK_JSON_OBJ="$(jq -n --arg s "$DISK_STATE" --argjson p "$DISK_PCT" --argjson a "$DISK_AVAIL" --arg f "${DISK_FS:-unknown}" \
    '{status:$s, mount:"/", filesystem:$f, percent:$p, avail_kb:$a}')"

GIT_JSON_OBJ="$(jq -n --arg s "$GIT_STATE" --argjson t "$GIT_JSON" --argjson r "$GIT_REPOS_JSON" \
    '{status:$s, total_dirty:$t, repos:$r}')"

ORG_JSON_OBJ="$(jq -n --arg s "$ORG_STATE" --argjson u "$ORG_JSON" --argjson fc "$FAILED_ALL_COUNT" --arg fl "$FAILED_ALL" \
    '{status:$s, units:$u, failed_unit_count:$fc, failed_units:($fl|if .=="" then [] else split(" ") end)}')"

TMP_FILE="$(mktemp "$STATE_DIR/.sys_health.tmp.XXXXXX")" || { echo "FATAL mktemp failed" >&2; exit 1; }
trap 'rm -f "$TMP_FILE"' EXIT

jq -n \
  --arg schema "arifos.sys_health.v2" \
  --arg host "$HOSTNAME_SHORT" \
  --arg ts "$TS" --argjson tse "$TS_EPOCH" --argjson mono "$MONO_NS" --argjson seq "$RUN_SEQ" \
  --arg prev "${PREV_TS:-}" --argjson regr "$WALL_REGRESSED" \
  --argjson vfs "$VALID_FOR_SECONDS" \
  --argjson secsrc "$SECRETS_SOURCED" --arg secerr "$SECRETS_SOURCE_ERROR" \
  --arg pstat "$PROBE_STATUS" --argjson fails "$FAILURES_JSON" \
  --argjson ds "$DS_JSON" --argjson vault "$VAULT_SEAL" --argjson disk "$DISK_PCT" \
  --argjson git "$GIT_JSON" --arg org "$ORGAN_HEALTH" \
  --argjson pds "$DS_JSON_OBJ" --argjson pvt "$VAULT_JSON_OBJ" \
  --argjson pdk "$DISK_JSON_OBJ" --argjson pgt "$GIT_JSON_OBJ" --argjson pog "$ORG_JSON_OBJ" '
  {
    schema_version: $schema,
    host: $host,
    generated_by: "probe_sys_health.sh",

    # --- time: wall + monotonic (B4) ---
    timestamp_utc: $ts,
    timestamp_epoch: $tse,
    monotonic_ns: $mono,
    run_seq: $seq,
    prev_timestamp_utc: (if $prev=="" then null else $prev end),
    wall_clock_regressed: $regr,
    valid_for_seconds: $vfs,

    # --- verdict: what was witnessed ---
    probe_status: $pstat,
    probe_failures: $fails,
    secrets_sourced: $secsrc,
    secrets_source_error: (if $secerr=="" then null else $secerr end),

    # --- legacy keys (consumed by evening_digest.md and others) ---
    deepseek_api_status: $ds,
    vault_seals_intact: $vault,
    disk_usage_percent: $disk,
    git_dirty_count: $git,
    organ_health: $org,

    # --- detail ---
    probes: { deepseek: $pds, vault: $pvt, disk: $pdk, git: $pgt, organs: $pog }
  }' >"$TMP_FILE"

if [ ! -s "$TMP_FILE" ]; then
    echo "FATAL jq produced empty output; state file left untouched" >&2
    log "FATAL jq produced empty output"
    exit 1
fi

mv -f "$TMP_FILE" "$STATE_FILE" || { echo "FATAL mv failed" >&2; exit 1; }
trap - EXIT

log "run_seq=$RUN_SEQ status=$PROBE_STATUS organ=$ORGAN_HEALTH vault=$VAULT_SEAL failures=${#FAILURES[@]}"

if [ "$EXIT_CODE" -ne 0 ]; then
    {
      echo "sys_health probe could not witness ${#FAILURES[@]} surface(s):"
      for f in "${FAILURES[@]}"; do echo "  - $f"; done
    } >&2
else
    echo "sys_health probe OK (run_seq=$RUN_SEQ) -> $STATE_FILE"
fi
exit "$EXIT_CODE"
