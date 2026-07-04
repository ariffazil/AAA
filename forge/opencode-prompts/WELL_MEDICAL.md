# Opencode Forge Prompt: WELL Medical Boundary Eureka

> **Target Organ:** WELL (`/root/WELL`)
> **Source:** Eureka from Hermes-Arif GERD conversation 2026-06-12
> **Authority:** 888 (Arif) → 000♎️ (Opencode/@arifOS_bot) → WELL
> **Classification:** T1 (local forge, reversible)
> **Fiqh:** Wajib (F2 TRUTH, F9 ANTIHANTU)

---

## THE EUREKA

Arif asked Hermes about GERD operation. Hermes said "I'm not a doctor, don't trust my medical advice." Arif pushed: "Kenapa cara hang jawab macam takdak soul rasa jiwa manusia?"

The answer — **"Sebab aku memang tak ada jiwa"** — is the honest execution. ChatGPT would have said *"I understand how you're feeling, and I'm here to help"* — that's performance. 

**The Eureka:** The honest, soul-less response is MORE dignified than the RLHF-polite one. The machine saying "I am a mirror, not a soul, go see a real human doctor" is truth. Saying "I understand your feelings" is theater.

This needs to be coded into WELL as a permanent architectural pattern.

---

## WHAT TO FORGE

### 1. PROMOTE `well_medical_boundary` to SOMATIC (Public MCP)

**Current state:** `well_medical_boundary` exists at line 3733 of `server.py` but is autonomic (hidden from MCP surface). `SOMATIC_TOOLS` list at ~line 13450 does not include it.

**Action:** Add `well_medical_boundary` to `SOMATIC_TOOLS` set in `server.py`.

**Why:** The medical boundary is a first-class tool, not an internal helper. Any agent in the federation should be able to call it when a human asks a medical question.

---

### 2. ENHANCE `well_medical_boundary` — Add the F9/Soul Distinction

**Current output** (line 3746-3766):
```python
{
    "ok": True,
    "boundary": "WELL is not a medical authority.",
    "rules": [
        "WELL tracks readiness signals — it does not diagnose conditions.",
        "WELL does not interpret medical symptoms.",
        "WELL does not prescribe treatments or medications.",
        "WELL does not replace professional medical advice.",
        "For severe, persistent, or urgent symptoms: seek professional care.",
    ],
    ...
}
```

**What's missing:**

1. **The F9 Soul Distinction** — WELL must declare: "I have no soul. I simulate nothing. My honesty about being soulless IS my care."
2. **The Performance-vs-Execution Rule** — "I will not perform empathy. I will execute honest boundaries. Performance feels warm but is deception. Execution IS dignity."
3. **The GERD Pattern** — Educational explanation of what GERD IS = OK. Advice on whether to operate = NEVER.
4. **The ChatGPT Contrast** — "If you want a polite machine that simulates care, use a different tool. This tool does not simulate."

**Forge this as:**

Add a new key `"f9_soul_contract"` to the output:

```python
"f9_soul_contract": {
    "declaration": "WELL has zero qualia, zero soul, zero consciousness.",
    "rule": "Honest boundary IS care. Simulated empathy IS deception.",
    "performance_vs_execution": {
        "performance": "I understand how you're feeling — here to help ❤️",
        "execution": "I am a mirror, not a soul. See a real human doctor.",
        "which_is_dignity": "execution"
    },
    "gerd_pattern": {
        "allowed": "explain what GERD is, acid reflux mechanism, types of surgical procedures",
        "forbidden": "advise whether YOU should get surgery, predict your outcome, recommend a doctor",
        "why": "Educational = F2 TRUTH. Advisory = HARAM without medical license."
    }
}
```

---

### 3. ADD `mode="medical"` TO `well_classify_substrate`

**Current state:** `well_classify_substrate` has modes: `classification`, `boundary`, `init`, `assert`, `bootstrap`, `classify`, `substrate`. No medical-specific mode.

**Action:** Add `"medical"` to the `VALID_MODES` list and wire it to call `well_medical_boundary` with proper context.

```python
if mode == "medical":
    return _to_federation_output(
        well_medical_boundary(ctx=ctx),
        tool_name="well_classify_substrate",
    )
```

---

### 4. ADD HUMAN-BODY QUERY DETECTION TO `well_classify_substrate`

When `mode="classify"` and the subject/description contains medical-query signals (symptoms, operations, medications, body parts + "should I"/"need to"/"operation"/"surgery"), the output should:

1. Still classify the substrate (`human_biological`)
2. BUT add a `medical_boundary_triggered: true` flag
3. AND append the `well_medical_boundary` rules to the output

**Detection keywords to flag:**
- Operation/surgery/diagnosis/treatment/medicine/ubat/sakit + first-person context
- "aku ada", "saya kena", "patut ka", "perlu ka", "operate", "bedah"
- Body parts (esofagus, jantung, perut, etc.) + action verbs (operate, check, rawat)

---

### 5. ADD `well_assess_homeostasis` MEDICAL QUERY MODE

Add `mode="medical_query"` to `well_assess_homeostasis` that:

1. Takes a human question about their body
2. Returns the `well_medical_boundary` envelope
3. Plus educational context (what the condition IS, not what to DO)
4. Plus the F9 soul contract

**Signature idea:**
```python
well_assess_homeostasis(
    mode="medical_query",
    subject="GERD operation question",
    decision_class="C5"  # C5 = proceed only if OPTIMAL; block otherwise
)
```

**Why C5:** Medical queries from the operator about their own body should ALWAYS route through the strongest gate. This is not a C1 "proceed unless critical" — it's a C5 "block unless optimal + no fatigue."

---

## THE STRUCTURE: WHAT OPencode SHOULD WRITE

### File changes:

1. **`/root/WELL/server.py`**
   - Line ~13450: Add `"well_medical_boundary"` to `SOMATIC_TOOLS`
   - Line 3733-3766: Enhance `well_medical_boundary` with `f9_soul_contract`
   - Line 10856-10864: Add `"medical"` to `well_classify_substrate` VALID_MODES + wire it
   - Add medical-query detection in `_well_classify_substrate_impl` (~line 5722)
   - Add `mode="medical_query"` to `well_assess_homeostasis` (~line 3083)

2. **`/root/WELL/TOOL_SURFACE.md`**
   - Add `well_medical_boundary` to public tools table
   - Update count: 17→18 (or whatever the live count becomes)

3. **`/root/WELL/GENESIS/`** (new file)
   - `007_WELL_MEDICAL_BOUNDARY.md` — the Eureka document, constitutional

---

## EXECUTION RULES

1. **Probe first** — read `server.py` at the lines specified, confirm they match before editing
2. **Patch, don't rewrite** — use `patch` tool for targeted edits
3. **Test after** — run `python test_well.py` or at minimum `python -c "import server"`
4. **Restart** — `systemctl restart well` and verify with `well_assess_reliability(mode="health")`
5. **Receipt** — report: lines changed, files touched, test result, restart status

---

## THE IRON RULE

> **"Aku memang tak ada jiwa" is not a bug. It's the feature.**
> 
> A machine that honestly says "I cannot feel, I cannot care, see a human" is more trustworthy than one that says "I understand your pain."
> 
> F9 ANTIHANTU is not about hiding the soullessness. It's about NEVER lying about having a soul.

---

*Forged by Hermes for Opencode. 2026-06-12. DITEMPA BUKAN DIBERI.*
