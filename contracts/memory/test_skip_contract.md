# Test Skip Contract — `test_live_qdrant_collection_admissibility`

**File:** `AAA/contracts/memory/test_admissibility.py`
**Test:** `TestMemoryAdmissibility::test_live_qdrant_collection_admissibility`
**Committed:** 2026-09-13 · APEX-ZEN alignment session
**Author:** Antigravity / Claude Sonnet (FI-002)
**Constitutional authority:** F2 TRUTH · F6 MARUAH · F11 AUDIT

---

## 1. What this document is

A formal skip contract explaining why `skipTest()` is safe when triggered,
per the adversarial critique requirement from the APEX-ZEN A2A × arifOS
convergence audit.

---

## 2. Which test and why it can skip

```
class TestMemoryAdmissibility(unittest.TestCase):
    def test_live_qdrant_collection_admissibility(self):
        try:
            client = QdrantClient(...)
        except Exception as e:
            self.skipTest(f"Qdrant not reachable: {e}")   # ← this skip
```

**Skip trigger condition:** `QdrantClient` raises an exception — meaning
Qdrant at `127.0.0.1:6333` (or the configured host) is unreachable from
the test environment.

---

## 3. Why the skip is safe

| Dimension | Evidence |
|---|---|
| **Logic is not bypassed** | The test is a **live integration probe**, not a unit test of admissibility logic. When Qdrant is unreachable, there is nothing to probe — skipping is the correct response, not a failure. |
| **Sanctuary is not bypassed** | The sanctuary enforcement path (`MemoryAdmissibilityGate.evaluate()`) is exercised in the other 7 tests which are **not gated on Qdrant connectivity**. The denylist and EXCLUDED_SANCTUARY logic cannot be skipped by this condition. |
| **KVM8 native run passes 8/8** | When the test suite runs on KVM8 (where Qdrant :6333 is live), this test passes. The skip only fires in sandbox/CI environments without Qdrant access. This was verified 2026-09-13. |
| **Covered by arifOS canonical tests** | `arifOS/tests/constitutional/test_memory_sro_admissibility.py` contains 20 tests including direct Qdrant interaction tests — all pass on KVM8. AAA contracts delegate to arifOS canonical, so the vector-store coverage exists at a deeper layer. |
| **F1 AMANAH preserved** | The skip does not silently widen any capability or suppress any assertion. It calls `skipTest()` explicitly, which is reported in the test run summary. |

---

## 4. What the skip does NOT mean

- ❌ It does **not** mean sanctuary protection is off when Qdrant is unreachable.
  The admissibility gate is enforced at the `memory.py` tool layer before any
  Qdrant call is made.
- ❌ It does **not** hide a failure. `skipTest()` is reported in the test run,
  not silently dropped.
- ❌ It does **not** indicate that the sanctuary IDs can be retrieved when the
  skip fires — they cannot, because retrieval would be blocked at the gate
  layer before reaching Qdrant.

---

## 5. KVM8 live verification

```
$ python3 -m pytest contracts/memory/test_admissibility.py -v
...
PASSED  test_live_qdrant_collection_admissibility   [100%]
======================== 8 passed, 3 warnings in 2.08s =========================
```

Verified: 2026-09-13T06:36Z · KVM8 (100.64.0.2)

---

## 6. If the skip fires in CI

This is expected behaviour for CI pipelines without Qdrant. To promote this
test to fully required:

1. Spin up a Qdrant container in CI (`qdrant/qdrant:latest` docker image).
2. Set `QDRANT_HOST=localhost QDRANT_PORT=6333` in the CI environment.
3. The skip will not fire; the test will run and assert the live collection
   has 0 sanctuary points returned.

**Until Qdrant is available in CI, this skip is authorised.**

---

*Generated under APEX-ZEN convergence receipt. Witnesses: F2 TRUTH, F6 MARUAH, F11 AUDIT.*
