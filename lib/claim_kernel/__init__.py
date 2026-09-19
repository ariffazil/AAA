"""claim_kernel — the explanatory-class axis for federation claims.

Import surface for every organ:

    from claim_kernel import (
        classify,            # text -> ClassVerdict (declared vs inferred class)
        require_baseline,    # comparative claim must name its baseline
        causal_invariance,   # Turchin test: does the cause discriminate?
        rope_test,           # artifact on disk but never called = rope held
        action_eligible,     # the gate: may this claim justify a mutation?
        MEASURED, MECHANISM, PATTERN, NARRATIVE, UNCLASSIFIED,
        CLAIM_CLASSES, ACTION_ELIGIBLE_CLASSES, SCHEMA,
    )

Axis 1 (existing, owned by AAA/claim_ledger): claim_type — HOW obtained.
Axis 2 (this module): claim_class — WHAT KIND of explanation.

The one rule other organs enforce:
    A NARRATIVE-class claim may be true, valuable and worth reading, and still
    carry zero explanatory power. Publishable; never a mutation's justification.
    UNCLASSIFIED fails closed.

Add this module's parent to sys.path if it is not installed:
    sys.path.insert(0, "/root/AAA/lib")
"""

from .claim_kernel import (  # noqa: F401
    SCHEMA,
    CLAIM_TYPES,
    CLAIM_CLASSES,
    ACTION_ELIGIBLE_CLASSES,
    MEASURED,
    MECHANISM,
    PATTERN,
    NARRATIVE,
    UNCLASSIFIED,
    ClassVerdict,
    BaselineVerdict,
    InvarianceVerdict,
    RopeVerdict,
    classify,
    require_baseline,
    causal_invariance,
    rope_test,
    action_eligible,
)

__all__ = [
    "SCHEMA",
    "CLAIM_TYPES",
    "CLAIM_CLASSES",
    "ACTION_ELIGIBLE_CLASSES",
    "MEASURED",
    "MECHANISM",
    "PATTERN",
    "NARRATIVE",
    "UNCLASSIFIED",
    "ClassVerdict",
    "BaselineVerdict",
    "InvarianceVerdict",
    "RopeVerdict",
    "classify",
    "require_baseline",
    "causal_invariance",
    "rope_test",
    "action_eligible",
]
