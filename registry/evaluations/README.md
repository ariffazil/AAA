# evaluations/ — scope-bound performance records

No evaluation records yet — every capability claim in this registry is advertised/
observed, none verified-by-evaluation. This is the honest state; do not seed
placeholders.

Adding an evaluation requires (schema enforces):
- release_ref + route_ref (WHERE it was measured)
- task_scope / language_scope / tool_state / kernel_state (UNDER WHAT conditions)
- dataset_bindings pinned to an IMMUTABLE HuggingFace commit — a floating `main`
  revision is not audit evidence (hf://datasets/ariffazil/AAA…FFF)
- prompt_set_revision + sampling_configuration + observed_results + verdict

Verdicts are scoped: "GLM-5.3 PASS on coding/mixed at revision X" — never
"GLM-5.3 is good at coding".
