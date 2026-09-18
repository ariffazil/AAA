#!/usr/bin/env bash
# node-posture-probe.sh — posture of each FED node WITHOUT reading a single credential.
#
# Answers four questions per node: alive? DB-wired? crash-looping? config stale?
# It never prints `.Config` / `.Config.Env` VALUES — only key names, counts, statuses and mtimes.
#
# Usage: ./node-posture-probe.sh [container ...]     (default: the two FED proxy containers)
set -u

NODES=("$@")
[ ${#NODES[@]} -eq 0 ] && NODES=(litellm litellm-federation)

echo "== local listeners (:4000 front door, :4012 zen, :4013 backend) =="
ss -lntp 2>/dev/null | grep -E ':(4000|4012|4013)\b' || echo "  none bound"

for n in "${NODES[@]}"; do
  if ! docker inspect "$n" >/dev/null 2>&1; then
    echo; echo "== $n == NOT PRESENT on this host (wrong node? check before concluding anything)"
    continue
  fi

  echo; echo "== $n =="
  docker inspect "$n" --format '  image={{.Config.Image}} net={{.HostConfig.NetworkMode}} restarts={{.RestartCount}} exit={{.State.ExitCode}} oom={{.State.OOMKilled}} started={{.State.StartedAt}}'

  # DB-wired? Decide on the KEY NAME, with values dropped BEFORE the filter runs.
  if docker inspect "$n" --format '{{range .Config.Env}}{{println .}}{{end}}' \
       | cut -d= -f1 | grep -qx 'DATABASE_URL'; then
    echo "  DATABASE_URL: present  -> node validates virtual keys; readiness should read db=connected"
  else
    echo "  DATABASE_URL: ABSENT   -> master-key path only; readiness reads db=Not connected, which is"
    echo "                           POSTURE, not a fault. Alerting on it is a false alarm."
  fi

  # Config files the container actually mounts, with mtime — compare against .State.StartedAt.
  while read -r src dst; do
    [ -z "${src:-}" ] && continue
    if [ -e "$src" ]; then
      printf '  mount %s -> %s  mtime=%s\n' "$src" "$dst" "$(stat -c '%y' "$src" 2>/dev/null)"
    else
      printf '  mount %s -> %s  (source missing on host)\n' "$src" "$dst"
    fi
  done < <(docker inspect "$n" --format '{{range .Mounts}}{{.Source}} {{.Destination}}{{"\n"}}{{end}}')

done

echo
echo "== readiness per local port (needs no auth) =="
for p in 4000 4013; do
  out=$(curl -s -m 6 "http://127.0.0.1:$p/health/readiness" 2>/dev/null) \
    && echo "  :$p $out" \
    || echo "  :$p NO ANSWER — bound is not serving; probe the backend port directly"
done

echo
echo "REMINDERS"
echo "  * 401 from /health (the heavy endpoint) means UP + auth-gated, never 'down'."
echo "  * never test allow_requests_on_db_unavailable by breaking the DB — read the flag instead."
echo "  * a `backup` line in haproxy is INTENT: exercise the node with one real call before counting it."
