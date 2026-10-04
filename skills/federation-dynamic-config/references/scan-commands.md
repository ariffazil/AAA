# Banda Haram Scan Commands (copy-paste ready)

## Per-harness scan

```bash
# Generic scan for any harness
HARNESS=/root/HERMES  # or /root/.config/opencode, /root/.codex, etc.

echo "=== Domain 2: Hardcoded ports ==="
grep -rnE "127\.0\.0\.1:[0-9]+|localhost:[0-9]+" $HARNESS/ 2>/dev/null | grep -v "os.environ\|process.env\|# env:"

echo "=== Domain 3: Hardcoded paths ==="
grep -rnE '"/root/(VAULT999|HERMES|\.hermes)' $HARNESS/ 2>/dev/null | grep -v "os.environ\|getenv"

echo "=== Domain 5: Math constants in Python ==="
grep -rnE "^[A-Z_]+: ?(float|int|dict)" $HARNESS/ 2>/dev/null | head -20

echo "=== Domain 6: Timeout magic numbers ==="
grep -rnE "timeout=[0-9]" $HARNESS/ 2>/dev/null | grep -v "os.environ"
```

## Hermes-specific scan

```bash
# Full Hermes federation scan (6 domains)
echo "=== CONFIG.YAML PORTS ==="
grep -n "port:" /root/HERMES/config.yaml | grep -v "# env:" | head -20

echo "=== PYTHON VAULT999 HARDCODED ==="
grep -rn '/root/VAULT999' /root/HERMES/mcp_servers/*.py /root/HERMES/scripts/*.py 2>/dev/null | grep -v "os.environ"

echo "=== TIMEOUTS IN PYTHON ==="
for f in /root/HERMES/mcp_servers/*.py; do
  raw=$(grep -cE "timeout=[0-9]" "$f" 2>/dev/null)
  if [ "$raw" -gt "0" ]; then echo "  $(basename $f): $raw raw timeouts"; fi
done

echo "=== COGNITIVE CONSTANTS ==="
python3 -c "from cognitive.config import OMEGA_0, CONFIDENCE_CAP; print(f'OMEGA_0={OMEGA_0} CAP={CONFIDENCE_CAP}')"
```

## OpenCode-specific scan

```bash
echo "=== PLUGIN HARDCODED URLs ==="
for f in /root/.config/opencode/plugins/*.ts; do
  hits=$(grep -cE '"http://127\.0\.0\.1:[0-9]+|"http://localhost:[0-9]+' "$f" 2>/dev/null)
  if [ "$hits" -gt "0" ]; then echo "  $(basename $f): $hits bare URLs"; fi
done

echo "=== AGENT .MD MODEL REFS ==="
for f in /root/.config/opencode/agents/*.md; do
  model=$(head -5 "$f" | grep "^model:.*[a-z]" 2>/dev/null)
  if [ -n "$model" ]; then echo "  $(basename $f): $model"; fi
done
```

## Post-patch verification

```bash
# After patching, confirm no bare literals remain
# (should return empty or only comments/docstrings)
grep -rnE "127\.0\.0\.1:[0-9]+" <harness>/ 2>/dev/null | grep -v "os.environ\|process.env\|# env:\|import\|comment"
```
