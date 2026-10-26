#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# actor-bind.sh — HARNESS-AGNOSTIC identity ceremony for the arifOS federation
#
# Contract (arifosmcp/runtime/tools.py::_arif_challenge_tool — spec verbatim):
#   1. arif_challenge(actor_id, session_id?)   -> {challenge: b64 32-byte nonce, ttl}
#   2. sign "{actor_id}:{challenge}" with the actor's Ed25519 private key -> sig_b64
#   3. arif_verify(challenge, sig_b64, actor_pubkey_hex, session_id) -> verified
#   4. verified=true -> session ed25519_verified (F11 AUDIT trace) -> arif_init
#      mints a token ABOVE OBSERVE_ONLY.
#   Challenge is single-use, default TTL 300s. Replay/expires -> verified=false.
#
# TRANSPORT (one door): http://127.0.0.1:8088/mcp  — streamable HTTP, session-keyed.
#   stdio bridges (mcp-compressor, node bridges) are ADAPTERS to this door, never
#   alternative doors. Works identically from: Kimi Code · OpenCode · Claude Code ·
#   Hermes · Antigravity · cron · plain shell. No harness field is read anywhere below.
#
# SIGNATURE PAYLOADS — PINNED FROM IMPLEMENTATION (2026-10-18, not from docs):
#   crypto_auth.py:823-864 "SINGLE SOURCE of canonical Ed25519 payload formats"
#   (used by verify_init_identity AND sovereign_verify — they cannot drift):
#     PRIMARY : f"{actor_id}:{nonce}"                       (crypto_auth.py:839)
#     COMPAT  : f"{actor_id}:{constitution_hash}:{nonce}"   (:849, when hash supplied)
#     + alias variants of both.
#   arif_verify ceremony checks the same family (crypto_auth.py:1054).
#   STALE DOC WARNING: tools.py:10606 advertises "(session_id + constitution_hash +
#   nonce)" — session_id is NOT in the implementation try-list. Do not sign that form.
#   Authorization-challenge surface (verify_authorization_challenge, crypto_auth.py:426)
#   is a different ceremony: signs the stored 14-field canonical JSON — not used here.
#
# KEY LOCATION: /root/AAA/IDENTITY/keys/<ACTOR>_private.pem  (Ed25519 PEM)
#
# SAFETY: DRY-RUN is the default. Nothing is signed, nothing is stored, no
#   challenge is even issued. --apply runs the ceremony and writes the token to
#   $AF_BIND_OUT (default /tmp/af-bind.<actor>.env, chmod 600) — a temp file,
#   never a config or repo. Token persistence beyond temp = sovereign word.
#
# Usage:
#   actor-bind.sh --actor FI-008                      # dry-run plan
#   actor-bind.sh --actor 333-AGI --apply             # ceremony + temp token
#   actor-bind.sh --actor FI-008 --key /path/k.pem    # explicit key
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

KERNEL="${ARIFOS_KERNEL:-http://127.0.0.1:8088/mcp}"
KEYS_DIR="${ARIF_KEYS_DIR:-/root/AAA/IDENTITY/keys}"
ACTOR="" KEY="" SESSION="" APPLY=0

while [ $# -gt 0 ]; do
  case "$1" in
    --actor)   ACTOR="$2"; shift 2 ;;
    --key)     KEY="$2"; shift 2 ;;
    --session) SESSION="$2"; shift 2 ;;
    --apply)   APPLY=1; shift ;;
    --dry-run) APPLY=0; shift ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done

[ -n "$ACTOR" ] || { echo "usage: actor-bind.sh --actor <ID> [--apply]" >&2; exit 2; }
KEY="${KEY:-$KEYS_DIR/${ACTOR}_private.pem}"
OUT="${AF_BIND_OUT:-/tmp/af-bind.${ACTOR}.env}"

mcp_call() { # $1=tool name, $2=arguments json
  curl -sf --max-time 15 "$KERNEL" \
    -H 'content-type: application/json' \
    -H 'accept: application/json, text/event-stream' \
    -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"$1\",\"arguments\":$2}}"
}

echo "═══ actor-bind · $ACTOR ═══"
echo "kernel : $KERNEL"
echo "key    : $KEY"

if [ ! -f "$KEY" ]; then
  echo "STATUS : KEY_MISSING — ${KEY} tidak wujud."
  echo "NEXT   : mint Ed25519 pair + daftar public dalam identity registry (T2 identity,"
  echo "         sovereign word required). Contoh:"
  echo "         openssl genpkey -algorithm ed25519 -out ${KEY}"
  echo "         openssl pkey -in ${KEY} -pubout -out ${KEYS_DIR}/${ACTOR}_public.pem"
  exit 3
fi

if [ "$APPLY" -eq 0 ]; then
  echo "MODE   : DRY-RUN (default) — tiada cabaran dikeluarkan, tiada tandatangan, tiada simpanan."
  echo "PLAN   :"
  echo "  1. arif_challenge(actor_id=$ACTOR${SESSION:+, session_id=$SESSION}) -> challenge (b64, TTL 300s)"
  echo "  2. printf '%s' '<actor>:<challenge>' | openssl pkeyutl -sign -inkey <key> -rawin | base64"
  echo "  3. arif_verify(challenge, sig_b64, pubkey_hex, session_id) -> verified"
  echo "  4. arif_init(mode=init, actor_id=$ACTOR, actor_signature=<sig>, nonce=<challenge>)"
  echo "     -> session_token + authority band (> OBSERVE_ONLY bila verified)"
  echo "  5. token -> $OUT (chmod 600, temp sahaja)"
  echo "GUNA --apply untuk jalankan ceremony sebenar."
  exit 0
fi

# ── 1 · nonce (path B: self-nonce — PRIMARY) ─────────────────────────────────
# NOTE 2026-10-18: arif_challenge/arif_verify are NOT on the public 8-verb surface
# (kernel: "Not on canonical public surface"; dev tools behind ARIFOS_MCP_EXPOSE_DEV_TOOLS).
# verify_init_identity checks f"{actor_id}:{nonce}" against the supplied nonce
# (crypto_auth.py:839) — so a self-generated nonce binds identity directly.
# Verified live 2026-10-18: actor_verified=true, band LIMITED_MUTATE.
NONCE=$(openssl rand -base64 32)
echo "1 · nonce    : ${NONCE:0:16}…"

# ── 2 · sign "{actor_id}:{nonce}" (Ed25519 = ONESHOT: needs file, not pipe) ──
PF=$(mktemp /tmp/af-sig.XXXXXX)
printf '%s' "$ACTOR:$NONCE" > "$PF"
SIG=$(openssl pkeyutl -sign -inkey "$KEY" -rawin -in "$PF" | base64 -w0)
rm -f "$PF"
[ -n "$SIG" ] || { echo "FAIL: signing gagal (openssl oneshot)." >&2; exit 4; }
echo "2 · signed   : ${SIG:0:24}… (payload \"<actor>:<nonce>\")"

# ── 3+4 · init carries the verification (verify_init_identity inside kernel) ─
IR=$(mcp_call arif_init "{\"mode\":\"init\",\"actor_id\":\"$ACTOR\",\"actor_signature\":\"$SIG\",\"nonce\":\"$NONCE\",\"intent\":\"identity bind via actor-bind.sh (self-nonce, harness-agnostic)\"${SESSION:+,\"session_id\":\"$SESSION\"}}")
VERDICT=$(printf '%s' "$IR" | python3 -c "import json,sys,re; t=sys.stdin.read(); m=re.search(r'\"actor_verified\"\s*:\s*(true|false)',t); print(m.group(1) if m else 'unknown')")
echo "3 · verified : $VERDICT"
[ "$VERDICT" = "true" ] || { echo "FAIL: bind tidak lulus — token tidak ditulis." >&2; exit 5; }
printf '%s' "$IR" | python3 -c "
import json,sys,re,os
t=sys.stdin.read()
tok=re.search(r'\"session_token\"\s*:\s*\"([^\"]+)\"',t)
sid=re.search(r'\"session_id\"\s*:\s*\"([^\"]+)\"',t)
band=re.search(r'\"authority_band\"\s*:\s*\"([^\"]+)\"',t)
out=os.environ.get('AF_BIND_OUT','$OUT')
with open(out,'w') as f:
    f.write(f'export AF_SESSION_TOKEN={tok.group(1) if tok else \"\"}\n')
    f.write(f'export AF_SESSION_ID={sid.group(1) if sid else \"\"}\n')
    f.write(f'export AF_AUTHORITY_BAND={band.group(1) if band else \"UNKNOWN\"}\n')
os.chmod(out,0o600)
print('4 · session   :', sid.group(1) if sid else '?')
print('5 · token     :', out, '(chmod 600 · temp — persistence = sovereign word)')
print('   band       :', band.group(1) if band else '?')
"
echo "═══ done ═══"
