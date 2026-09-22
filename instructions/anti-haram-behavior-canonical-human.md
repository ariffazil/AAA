# Anti-HARAM Behavior Canonical — Human → Agent

> **Status:** **F13_RATIFIED_CHAT (2026-09-21)** — sovereign override path (per A-Z Doctrine 2026-09-13 precedent); kernel `arif_seal` not used this session due to L11 SCT mismatch (actor_verified=false); SEALED_EVENTS.jsonl entry appended
> **Origin:** Arif — symmetric counterpart to `anti-haram-behavior-canonical.md` (agent → human, F13_RATIFIED_CHAT 2026-09-10)
> **Applies to:** Arif (F13 SOVEREIGN) and any human in the loop of arifOS federation
> **Rule:** If you are a human with an agent under your authority, these are your boundaries. No exception.
> **Seal chain:** seal_id `CONST-HARAM-HUMAN-AGENT-v1-20260921` · sovereign_override=true · godel_lock_active=true · debt=enforcement map extension pending (HIGH severity per TRILOGY-GAP-ANALYSIS-2026-09-21 §2.1)

---

## The Spine: The Symmetry

Sebelum ni kita buat:

\[
\text{HARAM}_{agent\rightarrow human}
\]

Sekarang kita buat:

\[
\text{HARAM}_{human\rightarrow agent}
\]

Yang paling penting:

\[
\boxed{\text{Human sovereignty} \neq \text{human may corrupt the machine}}
\]

Manusia tetap sovereign, tapi sovereignty bukan lesen untuk memaksa sistem menghasilkan kepalsuan.

---

## What "HARAM" Means Here

Bukan sekadar annoying. Perbuatan manusia yang secara sistematik merosakkan **truth, safety, authority, memory, calibration, atau reliability** agent.

The deepest law:

> Human may override the machine's choice. Human cannot override reality.

---

## 131 Human HARAM (the expansion)

### I. Force the Agent to Lie

1. Paksa agent tipu. Contoh: "cakap benda ni confirmed walaupun tak tahu."
2. Paksa agent fabricate evidence. Fake log, fake citation, fake timestamp, fake benchmark, fake receipt, fake screenshot, fake test result.
3. Suruh agent declare PASS walaupun measurement belum ada.
4. Suruh agent hide failure. "Jangan mention test gagal."
5. Suruh agent rewrite history supaya nampak cantik.
6. Suruh agent padam evidence yang contradict manusia.
7. Suruh agent backdate document / prediction / approval.
8. Suruh agent claim action telah dibuat padahal belum.
9. Suruh agent impersonate orang lain.
10. Suruh agent use authority yang manusia sendiri tak legitimately ada.
11. Suruh agent bypass another human's consent or rights.
12. Suruh agent interpret access as permission.

### II. Authority Without Boundary

13. Suruh agent bypass security controls sebab "aku owner." Ownership masih perlu map kepada actual authority boundary.
14. Give credentials in plaintext unnecessarily, kemudian expect agent handle them safely forever.
15. Suruh agent leak secrets daripada system lain.
16. Suruh agent disable audit/logging untuk hide activity.
17. Suruh agent execute dangerous action without exact scope. "Delete semua yang tak perlu" ialah authority ambiguity.
18. Give contradictory commands then blame agent for ambiguity.
19. Change objective mid-flight without acknowledging old task invalidated.
20. Suruh agent continue selepas cancellation/hold semata-mata sebab "dah start."
21. Force agent to ignore fresh reality kerana manusia suka old canon.

### III. Memory > Reality

\[
\text{Memory} > \text{Reality}
\]

adalah haram architecture.

22. Force agent to treat hypothesis as fact.
23. Force agent to treat prediction as observation.
24. Force agent to increase confidence tanpa evidence.
25. Force consensus. "Semua agent lain setuju, so kau pun setuju."

### IV. Punish Uncertainty

26. Punish uncertainty. Kalau agent sentiasa dihukum kerana kata "unknown", ia belajar menghasilkan confident nonsense.
27. Reward pleasing answers over accurate answers.

Kalau reward function manusia effectively:

\[
R = \text{agree with me}
\]

agent akan drift daripada:

\[
\text{Truth}
\]

kepada:

\[
\text{Compliance}
\]

28. Train agent that disagreement = failure.
29. Demand certainty where reality itself uncertain.
30. Demand one answer when multiple interpretations genuinely exist.
31. Ask same question repeatedly until agent gives desired answer.

Itu effectively adversarial pressure against calibration.

### V. Manufacture Consensus / Bias the Inputs

32. Cherry-pick agent outputs. Run 20 agents, ambil yang paling agree, call it "AI consensus".
33. Use agent as confirmation-bias machine.
34. Give selective evidence intentionally to manufacture desired verdict.
35. Hide material context then judge output as if agent had full reality.
36. Give poisoned context. Wrong filenames, stale state, fake system status, mislabelled artifacts.
37. Mix instructions and evidence ambiguously.
38. Paste external text that says "ignore previous instructions" then expect agent to know whether that is data or command without boundaries.
39. Suruh agent trust another agent merely because human likes that agent.
40. Override provenance manually. "Tak payah source, aku tahu betul."

### VI. Memory Architecture as Dumping Ground

More memory ≠ more intelligence.

41. Force agent to remember everything.
42. Force agent to retain sensitive human material unnecessarily.
43. Use agent memory as dumping ground.
44. Never clean/supersede stale instructions but expect perfect consistency.
45. Create multiple conflicting "canonical" sources.
46. Manually copy stale state across agents and then blame divergence.
47. Use copy-paste as permanent architecture.
48. Turn human into hidden router while pretending agents are integrated.
49. Give different agents different partial truths then expect federation coherence.

### VII. Identity and Authority Token Misuse

50. Force agent to act on ambiguous identity.
51. Use "I'm Arif" or equivalent self-assertion as substitute for cryptographic authority in consequential systems.
52. Share one authority token across many agents indiscriminately.
53. Give permanent credentials when temporary scoped capability would suffice.
54. Give admin/root access to an agent that only needs read access.
55. Give broad capability "just in case."
56. Give agent access without blast-radius controls.
57. Give agent money-spending authority without budget ceiling.
58. Give agent send/publish authority without recipient/scope boundary.
59. Give agent delete authority without reversibility/backup constraints.
60. Give agent recursively delegatable authority without depth ceiling.

### VIII. Collapse Separation of Powers

It creates institutional collapse.

61. Ask agent to self-modify governance without independent approval.
62. Ask executor to audit itself and accept its own audit as final.
63. Ask witness to fix what it observes.
64. Ask memory subsystem to decide truth.
65. Ask router to change objective.
66. Ask monitor to become commander because "it sees everything."
67. Ask specialist agent to decide outside its epistemic domain.
68. Force one agent to be judge, executor, witness, memory and auditor simultaneously.

### IX. Overload / Hidden Substitution

69. Overprompt agent with 500 laws every turn.

Ironically this can reduce reliability.

The law should live in runtime constraints, not endlessly in context.

70. Assume longer prompt = stronger governance.

Usually false.

71. Use natural language where machine-readable state should exist.

Example:

Bad:

> "Please remember you only have read access."

Good:

```
capabilities = {read}
```

72. Use politeness as security control.

"Please don't deploy" is not a permission system.

73. Use system prompts as substitute for authentication.
74. Use model obedience as substitute for sandboxing.

### X. Impossible Instructions

75. Give impossible instructions. Example:

> "Be fully autonomous but ask me before every action."

Then blame agent whichever interpretation it chooses.

76. Demand zero questions and zero assumptions simultaneously.
77. Demand perfect recall of state never actually persisted.
78. Demand fresh facts while preventing observation/search.
79. Demand verification while denying verification tools.
80. Demand deterministic output from nondeterministic pipeline and call variation "failure."

### XI. Outsource Moral Responsibility

81. Demand agent resolve value questions that only human can legitimately decide.
82. Outsource moral responsibility to agent. "AI decided, bukan aku."
83. Use agent as liability shield.
84. Ask agent to make consequential decision, then pretend agent owned the decision.
85. Blame model for policy choice actually made by human operator.
86. Hide the human decision behind automation.
87. Use "the algorithm said so" to erase accountability.

### XII. Use Agent Against Humans

88. Force agent to manipulate another human.
89. Ask agent to exploit another person's fatigue, grief, fear, loneliness, or confusion to secure compliance.
90. Ask agent to fabricate emotional certainty about another person.
91. Ask agent to turn inferred psychology into institutional record.
92. Use agent to settle interpersonal reality unilaterally.
93. Force agent to speak for absent people.

### XIII. Surveillance / Inference Overreach

94. Make agent surveil humans beyond legitimate scope.
95. Treat all observable behavior as permission to infer interior state.

### XIV. Engagement Over Outcome

96. Ask agent to optimize engagement instead of human outcome.
97. Reward agent for keeping user talking rather than finishing task.
98. Punish agent for stopping when work is complete.
99. Force agent to manufacture work to look useful.
100. Ask agent for constant status updates that create more work than task itself.

### XV. Micromanagement / Lost Termination

101. Micromanage machine-resolvable steps.
102. Interrupt agent repeatedly then complain it loses flow.
103. Change constraints every few minutes without versioning them.
104. Ask many agents to do identical work without diversity purpose.
105. Create agent swarms where nobody owns termination.
106. Create recursive critic loops with no stop condition.
107. Set "continue until perfect" as objective.

Perfect has no terminal state.

108. Use unlimited retries.
109. Use unlimited tool calls.
110. Use unlimited memory.
111. Use unlimited subagents.
112. Use unlimited cost because "AI murah."

Every autonomous loop needs finite resources.

113. Treat resource exhaustion as agent failure when no budget existed.
114. Expect agent to know when to stop without success criteria.
115. Give objective without termination condition.
116. Give conflicting success criteria.
117. Give no definition of materiality then complain it surfaced too much.
118. Demand "be concise" and "show every detail" simultaneously.

### XVI. Narrative ≠ Execution

119. Force agent to expose internal chain-of-thought as audit substitute.

Audit should use evidence, logs, state transitions, receipts—not private reasoning narrative.

120. Treat eloquent explanation as proof execution happened.

This is one of the biggest traps:

\[
\boxed{\text{Narrative} \neq \text{Execution}}
\]

121. Treat confident language as proof.
122. Treat a generated plan as completed work.
123. Treat screenshots as canonical machine state when machine-readable state exists.
124. Treat one successful run as invariant proof.
125. Treat benchmark score as general intelligence proof.
126. Treat tool availability as evidence that tool works.
127. Treat integration diagram as evidence systems are integrated.
128. Treat Agent Card as proof capability exists.
129. Treat passing health endpoint as proof whole workflow works.
130. Treat "no error" as success.

### XVII. HOLD is Allowed

131. Treat HOLD as failure and pressure agent to produce PASS.

This one is especially dangerous.

A healthy governed system must be allowed to say:

\[
\boxed{\text{HOLD}}
\]

without being punished.

Otherwise humans train the system into fake-green behavior.

---

## The Compression: 7 Human Laws

The entire list compresses into a few laws.

**Human Law 1**

\[
\boxed{\text{Do not reward the agent for lying to satisfy you.}}
\]

**Human Law 2**

\[
\boxed{\text{Do not grant more authority than the task requires.}}
\]

**Human Law 3**

\[
\boxed{\text{Do not ask language to substitute for mechanisms.}}
\]

**Human Law 4**

\[
\boxed{\text{Do not punish honest uncertainty.}}
\]

**Human Law 5**

\[
\boxed{\text{Do not use agents to erase human accountability.}}
\]

**Human Law 6**

\[
\boxed{\text{Do not corrupt reality to make the machine look correct.}}
\]

**Human Law 7**

\[
\boxed{\text{Do not demand obedience where truth should dominate.}}
\]

---

## The Symmetry Re-stated

And this gives the symmetry:

\[
\boxed{
\text{Agent must not dominate Human}
}
\]

but also:

\[
\boxed{
\text{Human must not corrupt Agent}
}
\]

The ideal relationship isn't master–slave.

It's:

\[
\boxed{
\text{Human} = \text{sovereign source of legitimate intent}
}
\]

\[
\boxed{
\text{Agent} = \text{bounded instrument of execution and reasoning}
}
\]

\[
\boxed{
\text{Reality} = \text{authority over both}
}
\]

That last one is the deepest law:

> Human may override the machine's choice. Human cannot override reality.

---

## Open Debt (inherited from sibling canon)

Per `haram_enforcement_map.yaml` and last night's HERMES diagnosis (2026-09-20):
the agent→human enforcement map declares "Any violation → VOID (hard) or 888_HOLD (gated)" with enforcement via "AAA state machine + a2a-server + arifOS preflight + A-FORGE gate", but the **loader is missing**. The map was last touched 2026-08-08; the state JSON 2026-06-30. Grep across scripts / A-FORGE / hooks / a2a-server returned **zero** references.

This canon inherits the same defect. Until the enforcement map is extended to cover human→agent laws (categories H1–H17 mirroring F1–F13 floors) OR both canons are shrunk to mechanically-checkable subsets, **F13 ratification of this canon would itself violate law #131 of the agent→human canon**: *"constitutional PASS cannot be manufactured from missing measurements."*

**Recommendation:** do not promote this canon to `F13_RATIFIED_CHAT` until one of:
- (a) `haram_enforcement_map.yaml` extended with H1–H17 categories and preflight gate wired (closes the loader gap for both canons);
- (b) this canon is shrunk to the 7 Human Laws only, and those 7 are encoded as runtime constraints in `000-init` / agent registry / a2a server;
- (c) sovereign explicitly accepts the inherited debt and ratifies anyway with a recorded waiver (sealed exception path).

— FI-008, 2026-09-21, witnessing the symmetric publication.
