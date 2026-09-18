#!/usr/bin/env python3
"""Cross-layer opt-in test — does the Cross-Layer Promotion Law fire when the writer omits the bridge field?

The artifact under test states the law as unconditional:
    Layer_A -> Layer_B  =>  ExplicitBridgeEvidence
So a claim that moves between layers with NO bridge declared must be held.
"""
import sys
sys.path.insert(0, "/root/.hermes/policy")
import rasa_boundary as rb

print("=== IS THE CROSS-LAYER LAW OPT-IN? ===\n")

# The artifact's own canonical example, written the way a real writer would write it:
# an economic observation promoted to a relational/phenomenological conclusion.
artifact = {
    "claim_id": "CL-RM400", "provenance_class": "O", "subject": "syed",
    "observation": "Syed paid 400 ringgit and arranged three meals, therefore he loves Arif",
    "alternatives": ["hospitality", "reciprocity"], "confidence": 0.9,
    "explanatory_layer": "PHENOMENOLOGICAL",
}
e = rb.validate_human_claim(artifact)
print(f"  (1) layer declared, NO bridge_claim, economic->qualia in prose")
print(f"      -> {'BLOCK' if e else 'ALLOW'}   {str(e[0])[:78] if e else '(no cross-layer violation raised)'}")

no_layer = {k: v for k, v in artifact.items() if k != "explanatory_layer"}
e2 = rb.validate_human_claim(no_layer)
print(f"\n  (2) same claim, explanatory_layer field absent (the default for any existing writer)")
print(f"      -> {'BLOCK' if e2 else 'ALLOW'}   {str(e2[0])[:78] if e2 else ''}")

kw = {"claim_id": "CL-KW", "provenance_class": "I", "subject": "syed",
      "observation": "oxytocin levels rose so there is love", "alternatives": ["x"]}
e3 = rb.validate_human_claim(kw)
print(f"\n  (3) control: prose contains the hardcoded pair 'oxytocin'+'love'")
print(f"      -> {'BLOCK' if e3 else 'ALLOW'}   {str(e3[0])[:78] if e3 else ''}")

para = {"claim_id": "CL-PARA", "provenance_class": "O", "subject": "syed",
        "observation": "he covered every bill and gave me gifts, so his heart is mine",
        "alternatives": ["x"]}
e4 = rb.validate_human_claim(para)
print(f"\n  (4) identical meaning, different words ('covered every bill'+'gifts')")
print(f"      -> {'BLOCK' if e4 else 'ALLOW'}   {str(e4[0])[:78] if e4 else '(no violation)'}")

# And the direct call, to show the law itself is sound where invoked properly
e5 = rb.validate_cross_layer_transition(
    "ECONOMIC", "PHENOMENOLOGICAL",
    {"claim_id": "CL-DIRECT", "provenance_class": "I", "subject": "syed", "observation": "loves"},
    None, None)
print(f"\n  (5) called DIRECTLY with source/target layers supplied")
print(f"      -> {'BLOCK' if e5 else 'ALLOW'}   {str(e5[0])[:78] if e5 else ''}")

print("""
CONCLUSION
----------
The law is correct where invoked (5). It is OPT-IN everywhere else: the claim path only
reaches it when the writer volunteers `bridge_claim`, and otherwise falls back to six
hardcoded word pairs. A writer that simply does not declare the move crosses any layer
they like — which is the same defect shape as the lexical floor in hermes_observe.
""")
