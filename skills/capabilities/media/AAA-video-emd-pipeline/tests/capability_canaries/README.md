# Capability Canaries — falsification harness for model capability claims
# Evidence for: knowledge-graph/FED_VIDEO_CANARY_LEDGER.yaml (v2) + router/video-routing.yaml (v2)
#
# Distinct from the F01–F08 epistemic fixture suite (tests/fixtures/video):
#   - F01–F08 test the PIPELINE CONTRACT (schemas, invariants, fusion semantics).
#     validate-mode makes ZERO model calls.
#   - These canaries test the MODELS themselves: can model X actually perceive what
#     the registry claims it perceives? They DO make live model calls.
#
# Protocol (binding): single canary is not proof. A capability is VERIFIED only when
# the model reproduces a property NOT recoverable from another channel, on PAIRED
# OPPOSITE fixtures, across >=3 repeated trials. Inadmissible as capability evidence:
# self-reported modality flags, HTTP 200, billed modality tokens.
#
# Run:  set -a; source /root/.secrets/kunci-root.env; set +a
#       python3 tests/capability_canaries/<script>.py
#
# | script               | what it proves / finds                                        |
# |----------------------|---------------------------------------------------------------|
# | probe_video4.py      | which gemini ids ingest video natively (usage VIDEO tokens)   |
# | canary_antibias.py   | paired opposite-tone fixtures, 1 trial — first-pass filter    |
# | canary_stability.py  | paired fixtures x3 trials -> AUDIO-VERIFIED-STABLE grade      |
# | canary_vision3.py    | frame-OCR vision lane (ZIRCON/BASALT word fixtures)           |
# | canary_asr2.py       | ASR route liveness + tone-hallucination guard                 |
#
# Fixtures these scripts synthesize (in /tmp): fed_video_probe.mp4, canary_A_asc.mp4,
# canary_B_desc.mp4, canary_frames/{ZIRCON,BASALT}.jpg, canary_tones.wav.
