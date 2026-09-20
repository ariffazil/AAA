# Diagnosing Which Layer Drops a Computed Value

> Use when a field is absent from a response but you believe the logic produces it. The goal is to
> locate the **first layer** that loses it, so the repair lands there instead of one layer late.

## The shape of the failure

```
builder() produces the value   ->  some layer drops it  ->  payload lacks it
```

Reporting this as "the builder is broken" is wrong in the common case: builders are usually
unit-testable and correct. The loss is typically a **projection**, **allow-list**, **serializer**, or
**verbosity filter** between the builder and the wire.

## Procedure

### 1. Invoke the builder directly, in the DEPLOYED interpreter

Do not test from a dev checkout, and do not import from a different virtualenv — the deployed copy is
the artifact under suspicion.

```bash
cd <site-packages>
<deployed-venv>/bin/python3 - <<'PY'
import inspect, json
from <module> import <builder>
print(inspect.signature(<builder>))
src = inspect.getsource(<builder>)
print('\n'.join(src.splitlines()[:40]))
out = <builder>(<production-shaped kwargs>)
print('KEYS:', list(out.keys()))
print(json.dumps(out)[:800])
PY
```

- `inspect.signature` first: a keyword-only signature tells you exactly which kwargs production must
  pass, and which are commonly left `None`.
- Run it with **production-shaped** arguments (including the `None`s and the empty dicts). A builder
  that only survives happy-path inputs will raise in production and be swallowed.

### 2. Call it through the production wrapper too

If call sites use a defensive wrapper (`_safe_build(...)`, `try/except: return None`), call the builder
**through that wrapper** as well. A wrapper that catches every exception converts a hard failure into a
silent `None` — indistinguishable at the payload from "never called".

```python
from <module> import <builder>, <wrapper>
print(<wrapper>(<builder>, **kwargs))   # None here but a dict above == the builder raises in prod
```

### 3. Inspect the projection layer

Search the payload-assembly module for allow-lists and field filters:

```bash
grep -rn "exclude_none\|exclude_unset\|_KEEP\|_STRIP\|keep_fields\|verbosity" <site-packages> --include=*.py | head -20
```

Distinguish two lists that usually coexist: a top-level keep-list and a **nested result** keep-list.
Adding a field to one while the value is filtered by the other changes nothing — and adding it to the
right one changes nothing either when the value is absent upstream.

### 4. Decide which side of the boundary is broken

| Builder returns it? | Payload has it? | Verdict |
|---|---|---|
| yes | yes | live and correct |
| yes | no | **projection defect** — fix the keep-list/serializer |
| no | no | **builder defect** — fix the logic |
| output seen only when calling the builder directly, never via the wrapper | no | **swallowing wrapper** — it hides a real exception; surface it |

### 5. Prove the repair by the boundary, not by the diff

Re-issue the same public call and show the field at the payload. A code diff, a passing unit test, or a
restart is not evidence that the value now reaches a caller.

## Pitfalls

- **A rebuild/restart does not replay an old response.** Confirm process start time against the
  artifact mtime when a fix "should" be live; a restart that precedes the file write is not a deploy.
- **Timestamp both sides.** Record the artifact mtime and the service start time in the receipt, so a
  later reader can tell "fix not yet live" from "fix live and ineffective".
- **Check field NAMES, not just presence.** A pluralised or suffixed twin (`*_roots` vs `*_root`) means
  a grep for one will miss the other; search every near-miss spelling before concluding absence.
- **Do not patch the projection first because it is easier.** If the value is absent at the builder
  boundary, a projection patch is a no-op that produces a convincing-looking commit.
