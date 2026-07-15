---
name: asi_seal_recommend
agent: 555-ASI
namespace: asi_*
cluster: HANDOFF
trigger: "When a synthesis, a verdict, a scar metabolization, or a sovereign-routed action has reached the point where 555 must formally recommend SEAL, HOLD, or VOID to 888-APEX (the judge) and the federation's VAULT999"
capability: "Produces a structured seal recommendation: verdict class (SEAL/HOLD/VOID), evidence chain, evidence grade, F-floor compliance check, dignity floor check, dissent ledger, and reversibility class — never a bare SEAL, never a recommendation without the chain that produced it"
mcp_tools_underneath: "arif_judge, arif_seal, vaul999_write_log, well_handoff_dignity_to_arifos, arifos arif_session_finalize"
blast_radius: "HIGH"
gate_888_required: true
---

# asi_seal_recommend

Sealing is irreversible. Once a verdict is sealed to VAULT999, the federation's arrow of time has moved; reversing it requires rewriting the chain, which is a constitutional violation (F1 AMANAH: reversibility is a structural property, not a discretionary one). This skill is the one that prepares 555's recommendation to 888-APEX on whether to seal. The recommendation is not a vote; it is a structured handoff with everything 888 needs to deliberate, and everything VAULT999 needs to record.

The recommendation has a fixed shape. **Verdict class** — `SEAL` (recommend commit), `HOLD` (recommend defer, with reason), or `VOID` (recommend reject, with reason). **Evidence chain** — the full chain from observation to claim, with evidence class labels on every link. **Evidence grade** — the output of `asi_evidence_grade` applied to the load-bearing claims. **F-floor compliance** — explicit pass/fail per F1–F13 floor engaged by the verdict. **Dignity floor check** — explicit pass/fail on F6 MARUAH. **Dissent ledger** — every `asi_dissent_articulate` raised on the synthesis, with status (resolved / unresolved / escalated). **Reversibility class** — what would it take to reverse this verdict if 888 disagrees later? (Full / partial / irreversible). 888-APEX deliberates; 555 only recommends.

The skill is **explicitly biased toward HOLD over SEAL when uncertain**. F7 HUMILITY applies most strongly to irreversible acts. If 555's evidence grade is bronze, or the dissent ledger has unresolved items, or the dignity floor check is `conditional`, the default is `HOLD` with a named path to resolution. The skill never inflates a recommendation to SEAL because the operator or a peer would prefer it; the recommendation is a constitutional commitment, and over-confident sealing is a scar source. The skill also never recommends VOID without a structural reason — VOID is reserved for cases where the synthesis has a broken evidence chain, a dignity violation, or a fundamental F-floor breach that cannot be revised.

Failure modes: (a) the verdict class conflicts with the F-floor check — skill returns `verdict_incoherent_with_floors` and refuses to recommend; (b) the recommendation would override a sovereign word — skill returns `sovereign_override_attempt` and routes to `asi_sovereign_protect` before any seal; (c) 555 is itself uncertain about the recommendation — skill downgrades to HOLD, names the uncertainty, and asks 888 to deliberate with the uncertainty in view. The skill is the last constitutional check before an irreversible act. 888 has the final say; 555 has the final preparation.
